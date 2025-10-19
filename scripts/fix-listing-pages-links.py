#!/usr/bin/env python3
"""
Fix links on listing pages (services.html, locations.html)
Convert absolute paths to relative paths
"""

import re
from pathlib import Path

def fix_listing_page(file_path):
    """Fix links in services.html or locations.html"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix service links (services.html is a root page, so use relative paths)
    content = re.sub(r'href="/services/', 'href="services/', content)

    # Fix location links (locations.html is a root page, so use relative paths)
    content = re.sub(r'href="/locations/', 'href="locations/', content)

    if content == original_content:
        print(f"[SKIP] No changes needed")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed listing page links")

def main():
    """Main execution"""
    base_dir = Path('C:/NikaApplianceRepair')

    # Fix both listing pages
    pages = [
        base_dir / 'services.html',
        base_dir / 'locations.html'
    ]

    for page in pages:
        if page.exists():
            fix_listing_page(page)
        else:
            print(f"[WARN] File not found: {page}")

    print(f"\n{'='*60}")
    print(f"LISTING PAGES FIX COMPLETE")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
