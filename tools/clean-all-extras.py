#!/usr/bin/env python3
"""
Remove ALL extra/duplicate sections:
1. (5,5,5,200+ reviews) text in hero
2. service-feature-icons (6 boxes)
3. Keep ONLY one pricing table
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def clean_page(file_path):
    """Clean all extra elements"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changes = []

    # 1. Remove duplicate review text in hero (5,5,5,200+ reviews)
    hero_spans = soup.find_all('span', string=re.compile(r'\(5,200\+.*reviews\)', re.I))
    for span in hero_spans:
        span.decompose()
        changes.append("removed duplicate review text")

    # 2. Remove service-feature-icons section (6 boxes)
    feature_icons = soup.find_all('div', class_='service-feature-icons')
    for section in feature_icons:
        section.decompose()
        changes.append("removed feature icons")

    # 3. Check for multiple pricing tables (should be max 1)
    pricing_tables = soup.find_all('table')
    if len(pricing_tables) > 1:
        # Keep first, remove others
        for table in pricing_tables[1:]:
            table.decompose()
            changes.append(f"removed duplicate table")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("CLEANING ALL EXTRA SECTIONS")
    print("=" * 70)
    print("\nRemoving:")
    print("  1. Duplicate review text in hero")
    print("  2. Service feature icons (6 boxes)")
    print("  3. Duplicate tables")
    print("=" * 70)

    all_files = []

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        all_files.extend([f for f in services_dir.glob('*.html')])

    # Location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        all_files.extend([f for f in locations_dir.glob('*.html')])

    print(f"\nProcessing {len(all_files)} pages...\n")

    fixed = 0
    for file_path in all_files:
        changes = clean_page(file_path)
        if changes:
            print(f"[CLEANED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"CLEANED: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
