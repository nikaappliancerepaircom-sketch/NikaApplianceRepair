#!/usr/bin/env python3
"""
Fix real visible issues from screenshots:
1. Change $89 to $119 in pricing tables
2. Remove duplicate sections if exist
3. Ensure hero image exists
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def fix_page_issues(file_path):
    """Fix all visible issues"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changes = []

    # 1. Fix $89 to $119 in pricing tables
    pricing_cells = soup.find_all('td', string=re.compile(r'\$89.*Waived', re.I))
    for cell in pricing_cells:
        cell.string = cell.string.replace('$89', '$119')
        changes.append("pricing $89 to $119")

    # 2. Remove duplicate "Transparent Pricing" tables (keep only first)
    pricing_sections = soup.find_all('h3', string=re.compile('Transparent Pricing', re.I))
    if len(pricing_sections) > 1:
        # Find tables after pricing headers
        for header in pricing_sections[1:]:  # Skip first, remove others
            # Remove entire pricing table section
            parent = header.find_parent('div')
            if parent:
                parent.decompose()
                changes.append("removed duplicate pricing")

    # 3. Check hero image exists
    hero_section = soup.find('section', class_=re.compile('hero'))
    if hero_section:
        hero_image = hero_section.find('img')
        if not hero_image:
            # Check if technician image path exists
            if 'assets/images/friendly-technician-character.png' not in str(hero_section):
                changes.append("WARNING: missing hero image")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING REAL VISIBLE ISSUES")
    print("=" * 70)
    print("\nFixing:")
    print("  1. Pricing table $89 to $119")
    print("  2. Remove duplicate sections")
    print("  3. Check hero images")
    print("=" * 70)

    all_files = []

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        all_files.extend([f for f in services_dir.glob('*.html')])

    print(f"\nProcessing {len(all_files)} service pages...\n")

    fixed = 0
    for file_path in all_files:
        if not file_path.exists():
            continue

        changes = fix_page_issues(file_path)
        if changes:
            print(f"[FIXED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
