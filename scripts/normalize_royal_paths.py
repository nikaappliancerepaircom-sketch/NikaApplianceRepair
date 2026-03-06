from __future__ import annotations

import shutil
from pathlib import Path


TARGET_DIR = Path(r"C:\Royal Garagedoors OLD")
ASSETS_DIR = TARGET_DIR / "assets"

MOVE_MAP = {
    TARGET_DIR / "wp-content": ASSETS_DIR / "content",
    TARGET_DIR / "wp-includes": ASSETS_DIR / "core",
    TARGET_DIR / "images": ASSETS_DIR / "images",
}

TEXT_EXTENSIONS = {
    ".html",
    ".css",
    ".js",
    ".xml",
    ".json",
    ".txt",
    ".svg",
    ".webmanifest",
    ".md",
}

REPLACEMENTS = {
    "https://www.royalgaragedoors.ca/wp-content/": "/assets/content/",
    "https://royalgaragedoors.ca/wp-content/": "/assets/content/",
    "https://www.royalgaragedoors.ca/wp-includes/": "/assets/core/",
    "https://royalgaragedoors.ca/wp-includes/": "/assets/core/",
    "/wp-content/": "/assets/content/",
    "/wp-includes/": "/assets/core/",
    "https://www.royalgaragedoors.ca/images/": "/assets/images/",
    "https://royalgaragedoors.ca/images/": "/assets/images/",
    "/images/": "/assets/images/",
    "https://www.royalgaragedoors.ca/osdd.php": "/assets/opensearch.xml",
    "https://royalgaragedoors.ca/osdd.php": "/assets/opensearch.xml",
    "/osdd.php": "/assets/opensearch.xml",
    "https://www.royalgaragedoors.ca/site.webmanifest": "/assets/site.webmanifest",
    "https://royalgaragedoors.ca/site.webmanifest": "/assets/site.webmanifest",
    "/site.webmanifest": "/assets/site.webmanifest",
}


def move_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        for item in source.iterdir():
            target = destination / item.name
            if target.exists():
                if item.is_dir():
                    move_tree(item, target)
                else:
                    if target.is_file():
                        target.unlink()
                    shutil.move(str(item), str(target))
            else:
                shutil.move(str(item), str(target))
        source.rmdir()
        return

    shutil.move(str(source), str(destination))


def write_static_service_files() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    (ASSETS_DIR / "site.webmanifest").write_text(
        """{
  "name": "Royal Garage Doors",
  "short_name": "Royal Garage Doors",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#f1641e",
  "icons": [
    {
      "src": "/assets/content/uploads/2024/06/cropped-Untitled-design-27-1-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/assets/content/uploads/2024/06/cropped-Untitled-design-27-1-270x270.png",
      "sizes": "270x270",
      "type": "image/png"
    }
  ]
}
""",
        encoding="utf-8",
    )

    (ASSETS_DIR / "opensearch.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>Royal Garage Doors</ShortName>
  <Description>Search Royal Garage Doors site content</Description>
  <InputEncoding>UTF-8</InputEncoding>
  <Url type="text/html" method="get" template="/?s={searchTerms}"/>
</OpenSearchDescription>
""",
        encoding="utf-8",
    )


def remove_legacy_root_files() -> None:
    for path in (TARGET_DIR / "osdd.php", TARGET_DIR / "site.webmanifest"):
        if path.exists():
            path.unlink()


def rewrite_text_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    updated = text

    for old, new in REPLACEMENTS.items():
        updated = updated.replace(old, new)
        updated = updated.replace(old.replace("/", "\\/"), new.replace("/", "\\/"))

    if updated != text:
        path.write_text(updated, encoding="utf-8")


def iter_text_files() -> list[Path]:
    return [path for path in TARGET_DIR.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS]


def main() -> None:
    for source, destination in MOVE_MAP.items():
        move_tree(source, destination)

    write_static_service_files()
    remove_legacy_root_files()

    for path in iter_text_files():
        rewrite_text_file(path)


if __name__ == "__main__":
    main()
