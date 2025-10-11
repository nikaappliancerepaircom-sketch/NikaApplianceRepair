#!/usr/bin/env python3
"""
Fix pricing on location pages: $89 -> $119
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def fix_location_pricing(file_path):
    """Fix $89 to $119"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changes = []

    # Fix pricing table cells
    pricing_cells = soup.find_all('td', string=re.compile(r'\$89.*Waived', re.I))
    for cell in pricing_cells:
        cell.string = cell.string.replace('$89', '$119')
        changes.append("table $89->$119")

    # Fix text mentions
    content_str = str(soup)
    if '$89' in content_str:
        content_str = content_str.replace('$89', '$119')
        soup = BeautifulSoup(content_str, 'html.parser')
        changes.append("text $89->$119")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING LOCATION PAGES PRICING")
    print("=" * 70)

    locations_dir = base_dir / 'locations'
    all_files = list(locations_dir.glob('*.html')) if locations_dir.exists() else []

    print(f"\nProcessing {len(all_files)} location pages...\n")

    fixed = 0
    for file_path in all_files:
        changes = fix_location_pricing(file_path)
        if changes:
            print(f"[FIXED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
