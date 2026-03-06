from __future__ import annotations

import hashlib
import re
import shutil
from collections import deque
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree


BASE_DOMAIN = "royalgaragedoors.ca"
BASE_URL = f"https://{BASE_DOMAIN}"
TARGET_DIR = Path(r"c:\NikaApplianceRepair\Royal Garagedoors OLD")
SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0.0.0 Safari/537.36"
        )
    }
)

EXCLUDED_PAGE_PREFIXES = (
    "/royal-garage-doors-repair-blog",
    "/blog",
    "/category",
    "/tag",
    "/author",
)
SKIP_PREFIXES = (
    "/feed",
    "/comments",
    "/wp-admin",
    "/wp-json",
    "/xmlrpc.php",
    "/?s=",
)
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "blob:")
ASSET_EXTENSIONS = {
    ".css",
    ".js",
    ".json",
    ".php",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".bmp",
    ".avif",
    ".mp4",
    ".webm",
    ".ogg",
    ".mp3",
    ".wav",
    ".pdf",
    ".txt",
    ".webmanifest",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".map",
    ".xml",
}
TEXT_URL_ATTRS = (
    "href",
    "src",
    "poster",
    "data-src",
    "data-lazy-src",
    "data-bg-image",
    "data-background-image",
    "data-image",
    "data-thumb",
)
SRCSET_ATTRS = (
    "srcset",
    "data-srcset",
    "data-lazy-srcset",
)
URL_PATTERN = re.compile(r"url\(([^)]+)\)")
ABSOLUTE_SITE_URL_PATTERN = re.compile(r"https?://(?:www\.)?royalgaragedoors\.ca[^\s\"'<>\\)]+")
ROOT_SITE_ASSET_PATTERN = re.compile(r"(?<![A-Za-z0-9_./-])/(?:wp-content|wp-includes)[^\s\"'<>\\)]+")
ALLOWED_EXTERNAL_ASSET_HOSTS = {
    "fonts.googleapis.com",
    "fonts.gstatic.com",
}
RESOURCE_TAGS = {"img", "script", "source", "video", "audio", "link"}
SEED_PAGE_PATHS: set[str] = set()
DESCENDANT_PAGE_PREFIXES: set[str] = set()


def reset_target() -> None:
    if TARGET_DIR.exists():
        for child in TARGET_DIR.iterdir():
            if child.name == ".git":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    TARGET_DIR.mkdir(parents=True, exist_ok=True)


def is_same_domain(url: str) -> bool:
    hostname = (urlparse(url).hostname or "").lower()
    return hostname in {BASE_DOMAIN, f"www.{BASE_DOMAIN}"}


def sanitize_url(url: str, base: str | None = None) -> str | None:
    if not url:
        return None

    candidate = url.strip()
    if not candidate or candidate.startswith("#") or candidate.startswith(SKIP_SCHEMES):
        return None

    if candidate.startswith("//"):
        candidate = f"https:{candidate}"

    absolute = urljoin(base or BASE_URL + "/", candidate)
    parsed = urlparse(absolute)

    if parsed.scheme not in {"http", "https"}:
        return None
    if "*" in parsed.path:
        return None

    path = parsed.path or "/"
    return urlunparse((parsed.scheme, parsed.netloc, path, "", parsed.query, ""))


def is_excluded_page(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path or "/"
    return any(path.startswith(prefix) for prefix in EXCLUDED_PAGE_PREFIXES)


def should_skip_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path or "/"
    return any(path.startswith(prefix) for prefix in SKIP_PREFIXES)


def has_asset_extension(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    return suffix in ASSET_EXTENSIONS


def is_allowed_page_path(path: str) -> bool:
    if not SEED_PAGE_PATHS:
        return True
    if path in SEED_PAGE_PATHS:
        return True
    return any(path.startswith(prefix) for prefix in DESCENDANT_PAGE_PREFIXES)


def canonical_page_url(url: str) -> str | None:
    absolute = sanitize_url(url)
    if not absolute or not is_same_domain(absolute):
        return None
    if should_skip_url(absolute) or is_excluded_page(absolute):
        return None

    parsed = urlparse(absolute)
    if has_asset_extension(parsed.path):
        return None

    path = parsed.path or "/"
    if not is_allowed_page_path(path if path.endswith("/") or path == "/" else f"{path}/"):
        return None

    if path != "/" and not path.endswith("/"):
        path = f"{path}/"

    return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def infer_local_external_path(url: str, content_type: str | None = None) -> Path:
    parsed = urlparse(url)
    host = parsed.netloc.replace(":", "_")
    path = parsed.path.lstrip("/")
    suffix = Path(parsed.path).suffix

    if not suffix:
        if content_type and "css" in content_type:
            suffix = ".css"
        elif content_type and "javascript" in content_type:
            suffix = ".js"
        elif content_type and "json" in content_type:
            suffix = ".json"
        else:
            suffix = ".bin"

        stem = Path(parsed.path or "resource").name or "resource"
        stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-") or "resource"
        digest = hashlib.md5(parsed.query.encode("utf-8")).hexdigest()[:8]
        path = f"{Path(path).parent.as_posix().lstrip('/')}/{stem}-{digest}{suffix}".lstrip("/")

    return Path("_external") / host / path


def local_path_for_url(url: str, content_type: str | None = None) -> Path:
    parsed = urlparse(url)
    if is_same_domain(url):
        relative = parsed.path.lstrip("/")
        if not relative:
            relative = "index.html"
        return Path(relative)
    return infer_local_external_path(url, content_type)


def local_href_for_url(url: str, content_type: str | None = None) -> str:
    path = local_path_for_url(url, content_type)
    return "/" + path.as_posix()


def page_file_path(page_url: str) -> Path:
    parsed = urlparse(page_url)
    clean = parsed.path.strip("/")
    if not clean:
        return TARGET_DIR / "index.html"
    return TARGET_DIR / clean / "index.html"


def fetch_text(url: str) -> str:
    response = SESSION.get(url, timeout=45)
    response.raise_for_status()
    return response.text


def parse_sitemap_pages() -> list[str]:
    xml_text = fetch_text(f"{BASE_URL}/page-sitemap.xml")
    root = ElementTree.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []

    for loc in root.findall(".//sm:loc", ns):
      if not loc.text:
          continue
      candidate = canonical_page_url(loc.text)
      if candidate:
          urls.append(candidate)

    about_page = canonical_page_url(f"{BASE_URL}/about-us/")
    if about_page:
        urls.append(about_page)

    global SEED_PAGE_PATHS, DESCENDANT_PAGE_PREFIXES
    SEED_PAGE_PATHS = {urlparse(url).path or "/" for url in urls}
    DESCENDANT_PAGE_PREFIXES = {path for path in SEED_PAGE_PATHS if path != "/"}

    return sorted(set(urls))


def split_srcset(value: str) -> list[str]:
    results: list[str] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        results.append(item.split()[0])
    return results


def extract_urls_from_text(text: str, base_url: str) -> tuple[set[str], set[str]]:
    page_links: set[str] = set()
    asset_links: set[str] = set()

    for match in ABSOLUTE_SITE_URL_PATTERN.findall(text):
        normalized = sanitize_url(match, base_url)
        if not normalized:
            continue
        if is_same_domain(normalized) and not has_asset_extension(urlparse(normalized).path):
            page = canonical_page_url(normalized)
            if page:
                page_links.add(page)
        else:
            asset_links.add(normalized)

    for match in ROOT_SITE_ASSET_PATTERN.findall(text):
        normalized = sanitize_url(match, base_url)
        if normalized:
            asset_links.add(normalized)

    return page_links, asset_links


def collect_page_data(page_url: str, html: str) -> tuple[set[str], set[str]]:
    soup = BeautifulSoup(html, "html.parser")
    page_links: set[str] = set()
    asset_links: set[str] = set()

    for tag in soup.find_all(True):
        tag_name = tag.name.lower()

        for attr in TEXT_URL_ATTRS:
            value = tag.get(attr)
            normalized = sanitize_url(value, page_url) if value else None
            if not normalized:
                continue

            if attr == "href" and tag_name == "a":
                if is_same_domain(normalized):
                    if has_asset_extension(urlparse(normalized).path):
                        asset_links.add(normalized)
                    else:
                        page = canonical_page_url(normalized)
                        if page:
                            page_links.add(page)
                continue

            if is_same_domain(normalized):
                if not has_asset_extension(urlparse(normalized).path):
                    page = canonical_page_url(normalized)
                    if page and tag_name == "link":
                        page_links.add(page)
                    elif tag_name in RESOURCE_TAGS:
                        asset_links.add(normalized)
                else:
                    asset_links.add(normalized)
                continue

            hostname = (urlparse(normalized).hostname or "").lower()
            if tag_name in RESOURCE_TAGS and hostname in ALLOWED_EXTERNAL_ASSET_HOSTS:
                asset_links.add(normalized)

        for attr in SRCSET_ATTRS:
            value = tag.get(attr)
            if not value:
                continue
            for item in split_srcset(value):
                normalized = sanitize_url(item, page_url)
                hostname = (urlparse(normalized).hostname or "").lower() if normalized else ""
                if normalized and (is_same_domain(normalized) or hostname in ALLOWED_EXTERNAL_ASSET_HOSTS):
                    asset_links.add(normalized)

        style = tag.get("style")
        if style:
            for match in URL_PATTERN.findall(style):
                url_part = match.strip().strip("'\"")
                normalized = sanitize_url(url_part, page_url)
                hostname = (urlparse(normalized).hostname or "").lower() if normalized else ""
                if normalized and (is_same_domain(normalized) or hostname in ALLOWED_EXTERNAL_ASSET_HOSTS):
                    asset_links.add(normalized)

    text_pages, text_assets = extract_urls_from_text(html, page_url)
    page_links.update(text_pages)
    asset_links.update(text_assets)

    filtered_assets = {url for url in asset_links if not should_skip_url(url) and not is_excluded_page(url)}
    filtered_pages = {url for url in page_links if not is_excluded_page(url) and not should_skip_url(url)}
    return filtered_pages, filtered_assets


def crawl_site() -> tuple[dict[str, str], set[str]]:
    pages: dict[str, str] = {}
    assets: set[str] = set()
    queue = deque(parse_sitemap_pages())
    seen: set[str] = set()

    while queue:
        page_url = queue.popleft()
        if page_url in seen:
            continue

        seen.add(page_url)
        print(f"[page] {page_url}")
        response = SESSION.get(page_url, timeout=45)
        response.raise_for_status()
        html = response.text
        pages[page_url] = html

        new_pages, page_assets = collect_page_data(page_url, html)
        assets.update(page_assets)

        for discovered in sorted(new_pages):
            if discovered not in seen:
                queue.append(discovered)

    return pages, assets


def rewrite_text_urls(text: str, replacements: dict[str, str]) -> str:
    ordered = sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True)
    for original, local in ordered:
        text = text.replace(original, local)
        text = text.replace(original.replace("/", "\\/"), local.replace("/", "\\/"))
    return text


def download_asset(
    asset_url: str,
    queued: deque[str],
    seen_assets: set[str],
    written_assets: dict[str, str],
) -> None:
    if asset_url in seen_assets:
        return

    seen_assets.add(asset_url)
    print(f"[asset] {asset_url}")
    try:
        response = SESSION.get(asset_url, timeout=45)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[skip-asset] {asset_url} :: {exc}")
        return

    content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
    local_rel_path = local_path_for_url(asset_url, content_type)
    local_abs_path = TARGET_DIR / local_rel_path
    local_abs_path.parent.mkdir(parents=True, exist_ok=True)

    written_assets[asset_url] = "/" + local_rel_path.as_posix()

    if "text/css" in content_type or local_abs_path.suffix.lower() == ".css":
        css_text = response.text
        discovered_urls: set[str] = set()

        for match in URL_PATTERN.findall(css_text):
            raw = match.strip().strip("'\"")
            normalized = sanitize_url(raw, asset_url)
            if normalized:
                discovered_urls.add(normalized)

        for import_match in re.findall(r"@import\s+(?:url\()?['\"]?([^'\"\)]+)", css_text):
            normalized = sanitize_url(import_match, asset_url)
            if normalized:
                discovered_urls.add(normalized)

        for nested_url in sorted(discovered_urls):
            if nested_url not in seen_assets:
                queued.append(nested_url)

        nested_replacements = {
            nested_url: local_href_for_url(nested_url)
            for nested_url in discovered_urls
        }
        css_text = rewrite_text_urls(css_text, nested_replacements)
        local_abs_path.write_text(css_text, encoding="utf-8")
        return

    local_abs_path.write_bytes(response.content)


def build_pages(pages: dict[str, str], asset_replacements: dict[str, str]) -> None:
    page_replacements = {page_url: urlparse(page_url).path or "/" for page_url in pages}
    page_replacements.update(
        {
            page_url.rstrip("/"): urlparse(page_url).path or "/"
            for page_url in pages
            if page_url != f"{BASE_URL}/"
        }
    )
    page_replacements[BASE_URL] = "/"

    excluded_replacements = {
        f"{BASE_URL}{prefix}/": "#"
        for prefix in EXCLUDED_PAGE_PREFIXES
    }
    excluded_replacements.update(
        {
            prefix if prefix.startswith("/") else f"/{prefix}": "#"
            for prefix in EXCLUDED_PAGE_PREFIXES
        }
    )

    replacements = {}
    replacements.update(asset_replacements)
    replacements.update(page_replacements)
    replacements.update(excluded_replacements)
    replacements[f"https://www.{BASE_DOMAIN}"] = "/"
    replacements[f"https://www.{BASE_DOMAIN}/"] = "/"

    for page_url, html in pages.items():
        rewritten = rewrite_text_urls(html, replacements)
        output_path = page_file_path(page_url)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rewritten, encoding="utf-8")


def write_readme(page_count: int, asset_count: int) -> None:
    content = (
        "# Royal Garage Doors OLD\n\n"
        "Static local mirror of `royalgaragedoors.ca`, generated without blog pages.\n\n"
        f"- Pages mirrored: {page_count}\n"
        f"- Assets mirrored: {asset_count}\n\n"
        "Run a local static server from this folder, for example:\n\n"
        "```powershell\n"
        "cd 'C:\\NikaApplianceRepair\\Royal Garagedoors OLD'\n"
        "python -m http.server 8080\n"
        "```\n"
    )
    (TARGET_DIR / "README.md").write_text(content, encoding="utf-8")


def main() -> None:
    reset_target()
    pages, assets = crawl_site()
    asset_queue = deque(sorted(assets))
    seen_assets: set[str] = set()
    written_assets: dict[str, str] = {}

    while asset_queue:
        download_asset(asset_queue.popleft(), asset_queue, seen_assets, written_assets)

    build_pages(pages, written_assets)
    write_readme(len(pages), len(written_assets))
    print(f"Finished: {len(pages)} pages, {len(written_assets)} assets.")


if __name__ == "__main__":
    main()
