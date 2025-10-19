#!/usr/bin/env python3
"""
Add hover states and responsive styles for mobile CTA buttons
"""

import re
from pathlib import Path

def add_mobile_enhancements(file_path):
    """Add hover states and responsive styles"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'mobile-cta-call' not in content:
        return False

    original = content
    changed = False

    # 1. Add hover state for Call button (if missing)
    if '.mobile-cta-call:hover' not in content:
        content = re.sub(
            r'(\.mobile-cta-call \{\s*background: #7B1FA2;\s*\})',
            r'\1\n\n    .mobile-cta-call:hover {\n        background: #6A1B9A;\n    }',
            content
        )
        changed = True

    # 2. Add hover state for Book button (if missing)
    if '.mobile-cta-book:hover' not in content:
        content = re.sub(
            r'(\.mobile-cta-book \{\s*background: #2196F3;\s*\})',
            r'\1\n\n    .mobile-cta-book:hover {\n        background: #1976D2;\n    }',
            content
        )
        changed = True

    # 3. Update button padding for better conversion
    content = re.sub(
        r'(\.mobile-cta-btn \{[^}]*?)padding: \d+px;',
        r'\1padding: 11px 10px;',
        content
    )

    # 4. Update gap
    content = re.sub(
        r'(\.mobile-cta-btn \{[^}]*?)gap: \d+px;',
        r'\1gap: 5px;',
        content
    )

    # 5. Update font-size
    content = re.sub(
        r'(\.mobile-cta-btn \{[^}]*?)font-size: \d+px;',
        r'\1font-size: 12.5px;',
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] {file_path.name}")
        return True

    return False

def main():
    base_dir = Path('C:/NikaApplianceRepair')

    pages = [base_dir / 'index.html', base_dir / 'services.html', base_dir / 'locations.html']

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
            if add_mobile_enhancements(page):
                fixed += 1

    print(f"\n[DONE] Enhanced {fixed} pages")

if __name__ == '__main__':
    main()
