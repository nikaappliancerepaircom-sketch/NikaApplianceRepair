#!/usr/bin/env python3
"""Audit repeated visible content and SEO invariants across published HTML pages."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?", re.IGNORECASE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
ROOT_SERVICE_RE = re.compile(r"^(dishwasher|dryer|fridge|washer)-repair-(.+)$")
SKIP_TAGS = {"script", "style", "noscript", "svg", "header", "footer", "nav"}
DETAIL_PATHS = {
    "locations/ajax.html",
    "locations/brampton.html",
    "locations/markham.html",
    "locations/mississauga.html",
    "locations/oshawa.html",
}


class PageParser(HTMLParser):
    """Collect visible text and basic SEO fields with no third-party dependency."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.main_depth = 0
        self.has_main = False
        self.title_depth = 0
        self.h1_depth = 0
        self.all_text: list[str] = []
        self.main_text: list[str] = []
        self.title_parts: list[str] = []
        self.h1_parts: list[list[str]] = []
        self.canonical = ""
        self.robots = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): value or "" for key, value in attrs}

        if tag in SKIP_TAGS:
            self.skip_depth += 1
        if tag == "main":
            self.has_main = True
            self.main_depth += 1
        if tag == "title":
            self.title_depth += 1
        if tag == "h1":
            self.h1_depth += 1
            self.h1_parts.append([])
        if tag == "link" and "canonical" in attr_map.get("rel", "").lower().split():
            self.canonical = attr_map.get("href", "").strip()
        if tag == "meta" and attr_map.get("name", "").lower() == "robots":
            self.robots = attr_map.get("content", "").strip().lower()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag == "main" and self.main_depth:
            self.main_depth -= 1
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        if tag == "h1" and self.h1_depth:
            self.h1_depth -= 1

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if not value:
            return
        if self.title_depth:
            self.title_parts.append(value)
        if self.h1_depth and self.h1_parts:
            self.h1_parts[-1].append(value)
        if self.skip_depth:
            return
        self.all_text.append(value)
        if self.main_depth:
            self.main_text.append(value)


@dataclass
class Page:
    url: str
    path: str
    family: str
    title: str
    h1s: list[str]
    canonical: str
    robots: str
    is_alberta: bool
    words: list[str]
    sentences: set[str]
    shingles: set[int]
    repeated_sentence_ratio: float = 0.0
    nearest_path: str | None = None
    nearest_similarity: float = 0.0


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(len(ordered) * fraction) - 1)
    return ordered[index]


def normalize_words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def normalized_sentence(text: str) -> str:
    return " ".join(normalize_words(text))


def sentence_set(text: str) -> set[str]:
    sentences = set()
    for raw in SENTENCE_RE.split(text):
        normalized = normalized_sentence(raw)
        if len(normalized.split()) >= 8:
            sentences.add(normalized)
    return sentences


def five_gram_hashes(words: list[str]) -> set[int]:
    return {hash(tuple(words[index : index + 5])) for index in range(len(words) - 4)}


def family_for(relative_path: str) -> str:
    normalized = relative_path.replace("\\", "/")
    path = Path(normalized)
    stem = path.stem
    if len(path.parts) == 1:
        match = ROOT_SERVICE_RE.match(stem)
        if match:
            return f"root-service-location/{match.group(1)}"
        return "root-other"
    if path.parts[0] == "blog":
        section = path.parts[1] if len(path.parts) > 2 else "root"
        return f"blog/{section}"
    if path.parts[0] == "locations" and len(path.parts) > 2 and path.parts[1] == "services":
        service = stem.split("-repair-", 1)[0]
        return f"locations/services/{service}"
    if path.parts[0] in {"locations", "services", "brands"}:
        return path.parts[0]
    return "other"


def sitemap_urls(path: Path) -> list[str]:
    root = ElementTree.parse(path).getroot()
    urls = []
    for element in root.iter():
        if element.tag.endswith("loc") and element.text:
            urls.append(element.text.strip())
    return urls


def local_path_for_url(root: Path, url: str) -> Path | None:
    url_path = unquote(urlparse(url).path).strip("/")
    if not url_path:
        candidates = [root / "index.html"]
    else:
        candidates = [root / f"{url_path}.html", root / url_path / "index.html"]
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def normalized_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    if path.endswith(".html"):
        path = path[:-5]
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"


def parse_page(root: Path, url: str, path: Path) -> Page:
    html = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)
    visible_text = " ".join(parser.main_text if parser.has_main else parser.all_text)
    words = normalize_words(visible_text)
    relative_path = path.relative_to(root).as_posix()
    return Page(
        url=url,
        path=relative_path,
        family=family_for(relative_path),
        title=" ".join(parser.title_parts).strip(),
        h1s=[" ".join(parts).strip() for parts in parser.h1_parts],
        canonical=parser.canonical,
        robots=parser.robots,
        is_alberta=bool(re.search(r'"addressRegion"\s*:\s*"AB"', html, re.IGNORECASE)),
        words=words,
        sentences=sentence_set(visible_text),
        shingles=five_gram_hashes(words),
    )


def calculate_family_metrics(pages: list[Page], top_count: int) -> dict:
    sentence_pages: Counter[str] = Counter()
    for page in pages:
        sentence_pages.update(page.sentences)

    for page in pages:
        repeated_words = sum(
            len(sentence.split()) for sentence in page.sentences if sentence_pages[sentence] > 1
        )
        page.repeated_sentence_ratio = repeated_words / len(page.words) if page.words else 0.0

    pair_scores: list[tuple[float, Page, Page]] = []
    for left_index, left in enumerate(pages):
        for right in pages[left_index + 1 :]:
            union_size = len(left.shingles | right.shingles)
            similarity = len(left.shingles & right.shingles) / union_size if union_size else 0.0
            if similarity > left.nearest_similarity:
                left.nearest_similarity = similarity
                left.nearest_path = right.path
            if similarity > right.nearest_similarity:
                right.nearest_similarity = similarity
                right.nearest_path = left.path
            pair_scores.append((similarity, left, right))

    repeated_ratios = [page.repeated_sentence_ratio for page in pages]
    nearest_scores = [page.nearest_similarity for page in pages]
    return {
        "pageCount": len(pages),
        "medianWords": round(statistics.median([len(page.words) for page in pages]), 1),
        "medianRepeatedSentenceWordRatio": round(statistics.median(repeated_ratios), 4),
        "p90RepeatedSentenceWordRatio": round(percentile(repeated_ratios, 0.9), 4),
        "medianNearestFiveGramJaccard": round(statistics.median(nearest_scores), 4),
        "p90NearestFiveGramJaccard": round(percentile(nearest_scores, 0.9), 4),
        "topPairs": [
            {
                "similarity": round(similarity, 4),
                "left": left.path,
                "right": right.path,
            }
            for similarity, left, right in sorted(
                pair_scores, key=lambda item: (-item[0], item[1].path, item[2].path)
            )[:top_count]
        ],
        "mostRepeatedSentences": [
            {"pageCount": count, "sentence": sentence}
            for sentence, count in sorted(
                sentence_pages.items(), key=lambda item: (-item[1], item[0])
            )[:top_count]
            if count > 1
        ],
    }


def duplicate_groups(pages: list[Page], field_name: str) -> list[dict]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for page in pages:
        value = getattr(page, field_name)
        if isinstance(value, list):
            value = value[0] if len(value) == 1 else ""
        if value:
            groups[value].append(page.path)
    return [
        {field_name: value, "paths": sorted(paths)}
        for value, paths in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
        if len(paths) > 1
    ]


def build_report(root: Path, sitemap_path: Path, top_count: int) -> dict:
    urls = sitemap_urls(sitemap_path)
    pages: list[Page] = []
    missing_files: list[str] = []
    for url in urls:
        path = local_path_for_url(root, url)
        if path is None:
            missing_files.append(url)
            continue
        pages.append(parse_page(root, url, path))

    families: defaultdict[str, list[Page]] = defaultdict(list)
    for page in pages:
        families[page.family].append(page)

    family_reports = {}
    for name, family_pages in sorted(families.items()):
        if len(family_pages) >= 2 and name not in {"root-other", "other"}:
            family_reports[name] = calculate_family_metrics(family_pages, top_count)

    sitemap_set = {normalized_url(url) for url in urls}
    canonical_mismatches = [
        {"path": page.path, "sitemapUrl": page.url, "canonical": page.canonical}
        for page in pages
        if not page.canonical or normalized_url(page.canonical) != normalized_url(page.url)
    ]
    noindex_pages = [page.path for page in pages if "noindex" in page.robots]
    h1_issues = [
        {"path": page.path, "h1Count": len(page.h1s), "h1s": page.h1s}
        for page in pages
        if len(page.h1s) != 1
    ]
    alberta_pages = sorted(
        (page for page in pages if page.is_alberta), key=lambda page: page.path
    )
    alberta_urls = [normalized_url(page.url) for page in alberta_pages]
    alberta_files: list[tuple[str, str]] = []
    for file_path in sorted(root.glob("*.html")):
        html = file_path.read_text(encoding="utf-8", errors="replace")
        if not re.search(r'"addressRegion"\s*:\s*"AB"', html, re.IGNORECASE):
            continue
        parser = PageParser()
        parser.feed(html)
        fallback_url = f"https://nikaappliancerepair.com/{file_path.stem}"
        alberta_files.append(
            (file_path.relative_to(root).as_posix(), normalized_url(parser.canonical or fallback_url))
        )
    alberta_file_urls = [url for _, url in alberta_files]

    return {
        "schemaVersion": 1,
        "method": {
            "visibleContent": "main element when present; otherwise body text; excludes script, style, noscript, svg, header, footer, and nav",
            "sentenceReuse": "exact normalized sentences with at least 8 words repeated in another page in the same family",
            "similarity": "Jaccard similarity of normalized visible-text 5-gram sets within the same page family",
            "pageDetails": "priority remediation pages only; family and SEO summaries cover the full sitemap",
        },
        "inventory": {
            "sitemapUrlCount": len(urls),
            "uniqueSitemapUrlCount": len(sitemap_set),
            "resolvedPageCount": len(pages),
            "missingFileCount": len(missing_files),
            "missingFiles": missing_files,
            "albertaPageCount": len(alberta_pages),
            "albertaUrlSha256": hashlib.sha256("\n".join(alberta_urls).encode("utf-8")).hexdigest(),
            "albertaPaths": [page.path for page in alberta_pages],
            "albertaFileCount": len(alberta_files),
            "albertaFileUrlSha256": hashlib.sha256(
                "\n".join(alberta_file_urls).encode("utf-8")
            ).hexdigest(),
            "albertaFilePaths": [file_path for file_path, _ in alberta_files],
        },
        "seo": {
            "duplicateTitleGroups": duplicate_groups(pages, "title"),
            "duplicateH1Groups": duplicate_groups(pages, "h1s"),
            "h1CountIssues": h1_issues,
            "canonicalMismatches": canonical_mismatches,
            "noindexInSitemap": noindex_pages,
        },
        "families": family_reports,
        "pages": [
            {
                "path": page.path,
                "url": page.url,
                "family": page.family,
                "wordCount": len(page.words),
                "repeatedSentenceWordRatio": round(page.repeated_sentence_ratio, 4),
                "nearestPath": page.nearest_path,
                "nearestFiveGramJaccard": round(page.nearest_similarity, 4),
                "title": page.title,
                "h1s": page.h1s,
                "canonical": page.canonical,
                "robots": page.robots,
                "isAlberta": page.is_alberta,
            }
            for page in sorted(pages, key=lambda page: page.path)
            if page.path in DETAIL_PATHS
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--sitemap", type=Path, default=Path("sitemap.xml"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top", type=int, default=20, help="Top pairs/sentences per family")
    args = parser.parse_args()

    root = args.root.resolve()
    sitemap_path = args.sitemap if args.sitemap.is_absolute() else root / args.sitemap
    output_path = args.output if args.output.is_absolute() else root / args.output
    report = build_report(root, sitemap_path, args.top)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory = report["inventory"]
    print(f"Audited {inventory['resolvedPageCount']}/{inventory['sitemapUrlCount']} sitemap pages")
    print(
        "Alberta pages: "
        f"{inventory['albertaPageCount']} (sha256 {inventory['albertaUrlSha256'][:12]}...)"
    )
    for name, family in report["families"].items():
        print(
            f"{name}: pages={family['pageCount']} "
            f"repeat={family['medianRepeatedSentenceWordRatio']:.2%} "
            f"nearest={family['medianNearestFiveGramJaccard']:.2%}"
        )
    print(f"Report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
