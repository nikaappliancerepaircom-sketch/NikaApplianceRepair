#!/usr/bin/env python3
"""Validate HTML and local asset/link invariants for changed remediation pages."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


DOMAIN = "nikaappliancerepair.com"


class ValidatorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titles = 0
        self.head_depth = 0
        self.h1s = 0
        self.canonicals: list[str] = []
        self.local_refs: list[str] = []
        self.json_depth = 0
        self.json_parts: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "head":
            self.head_depth += 1
        elif tag == "title" and self.head_depth:
            self.titles += 1
        elif tag == "h1":
            self.h1s += 1
        elif tag == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonicals.append(values.get("href", ""))
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self.json_depth += 1
            self.json_parts.append([])

        for attribute in ("href", "src"):
            value = values.get(attribute, "")
            if value.startswith("/") and not value.startswith("//"):
                self.local_refs.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "head" and self.head_depth:
            self.head_depth -= 1
        if tag == "script" and self.json_depth:
            self.json_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.json_depth and self.json_parts:
            self.json_parts[-1].append(data)


def changed_html(root: Path, base: str) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, "--", "*.html"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [root / line for line in result.stdout.splitlines() if line]


def expected_route(root: Path, file_path: Path) -> str:
    relative = file_path.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return f"/{relative[:-11]}".rstrip("/") or "/"
    return f"/{relative[:-5]}"


def local_target_exists(root: Path, reference: str) -> bool:
    pathname = unquote(urlparse(reference).path)
    if pathname in {"", "/"}:
        return (root / "index.html").is_file()
    relative = pathname.lstrip("/")
    candidates = [root / relative, root / f"{relative}.html", root / relative / "index.html"]
    return any(candidate.is_file() for candidate in candidates)


def refs_at_base(root: Path, file_path: Path, base: str) -> set[str]:
    relative = file_path.relative_to(root).as_posix()
    result = subprocess.run(
        ["git", "show", f"{base}:{relative}"],
        cwd=root,
        capture_output=True,
    )
    if result.returncode:
        return set()
    parser = ValidatorParser()
    parser.feed(result.stdout.decode("utf-8", errors="replace"))
    return set(parser.local_refs)


def validate_file(root: Path, file_path: Path, base: str) -> list[str]:
    parser = ValidatorParser()
    parser.feed(file_path.read_text(encoding="utf-8", errors="strict"))
    issues: list[str] = []
    route = expected_route(root, file_path)

    if parser.titles != 1:
        issues.append(f"expected one title, found {parser.titles}")
    if parser.h1s != 1:
        issues.append(f"expected one h1, found {parser.h1s}")
    if len(parser.canonicals) != 1:
        issues.append(f"expected one canonical, found {len(parser.canonicals)}")
    elif urlparse(parser.canonicals[0]).netloc != DOMAIN or urlparse(parser.canonicals[0]).path.rstrip("/") != route.rstrip("/"):
        issues.append(f"canonical does not match route: {parser.canonicals[0]}")

    for index, parts in enumerate(parser.json_parts, start=1):
        try:
            json.loads("".join(parts))
        except json.JSONDecodeError as error:
            issues.append(f"JSON-LD block {index} is invalid: {error.msg}")

    existing_refs = refs_at_base(root, file_path, base)
    for reference in sorted(set(parser.local_refs) - existing_refs):
        if not local_target_exists(root, reference):
            issues.append(f"new local reference has no target: {reference}")
    return issues


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--root", type=Path, default=Path.cwd())
    argument_parser.add_argument("--base", default="HEAD", help="Git base used to identify changed HTML")
    args = argument_parser.parse_args()
    root = args.root.resolve()
    pages = changed_html(root, args.base)
    if not pages:
        print("No changed HTML pages found", file=sys.stderr)
        return 1

    failures: dict[str, list[str]] = {}
    for page in pages:
        issues = validate_file(root, page, args.base)
        if issues:
            failures[page.relative_to(root).as_posix()] = issues

    if failures:
        for page, issues in failures.items():
            print(page)
            for issue in issues:
                print(f"  - {issue}")
        return 1

    print(f"Validated {len(pages)} changed HTML pages: titles, H1s, canonicals, JSON-LD, and new local targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
