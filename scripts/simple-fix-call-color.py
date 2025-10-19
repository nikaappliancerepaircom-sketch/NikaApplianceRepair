#!/usr/bin/env python3
"""
Simple script to replace Call button color from green to purple
"""

from pathlib import Path

def fix_call_button_color(file_path):
    """Replace green (#4CAF50) with purple (#7B1FA2) for Call button"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'mobile-cta-call' in content and '#4CAF50' in content:
        content = content.replace('background: #4CAF50', 'background: #7B1FA2')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] {file_path.name}")
        return True
    return False

def main():
    base_dir = Path('C:/NikaApplianceRepair')

    pages = []
    pages.append(base_dir / 'services.html')
    pages.append(base_dir / 'locations.html')

    for service in ['refrigerator-repair', 'dishwasher-repair', 'washer-repair', 'dryer-repair',
                    'oven-repair', 'stove-repair', 'range-repair', 'microwave-repair', 'freezer-repair']:
        pages.append(base_dir / 'services' / f'{service}.html')

    for location in ['richmond-hill', 'mississauga', 'brampton', 'markham', 'vaughan',
                     'oakville', 'milton', 'burlington', 'ajax', 'pickering',
                     'whitby', 'oshawa', 'aurora', 'newmarket', 'etobicoke',
                     'north-york', 'scarborough', 'caledon', 'east-gwillimbury', 'halton-hills']:
        pages.append(base_dir / 'locations' / f'{location}.html')

    for brand in ['samsung', 'lg', 'whirlpool', 'ge', 'bosch',
                  'kitchenaid', 'maytag', 'frigidaire', 'electrolux', 'kenmore',
                  'miele', 'fisher-paykel', 'amana', 'hotpoint', 'danby']:
        pages.append(base_dir / 'brands' / f'{brand}-appliance-repair-toronto.html')

    fixed = 0
    for page in pages:
        if page.exists():
            if fix_call_button_color(page):
                fixed += 1

    print(f"\n[DONE] Fixed {fixed} pages")

if __name__ == '__main__':
    main()
