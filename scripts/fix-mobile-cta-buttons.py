#!/usr/bin/env python3
"""
Fix mobile CTA buttons across all pages:
1. Change Call Now to purple (#7B1FA2)
2. Keep Book Online blue (#2196F3)
3. Optimize button sizes for better conversion
4. Add responsive styles for all mobile sizes
"""

import re
from pathlib import Path

def fix_mobile_cta_styles(file_path):
    """Fix mobile CTA button styles in a file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Pattern 1: Fix old call button color (green to purple)
    content = re.sub(
        r'\.mobile-cta-call \{\s*background: #4CAF50;\s*\}',
        '.mobile-cta-call {\n        background: #7B1FA2;\n    }',
        content
    )

    # Pattern 2: Add hover states if missing
    if '.mobile-cta-call:hover' not in content:
        # Find .mobile-cta-call block and add hover after it
        content = re.sub(
            r'(\.mobile-cta-call \{\s*background: #7B1FA2;\s*\})',
            r'\1\n\n    .mobile-cta-call:hover {\n        background: #6A1B9A;\n    }',
            content
        )

    if '.mobile-cta-book:hover' not in content:
        content = re.sub(
            r'(\.mobile-cta-book \{\s*background: #2196F3;\s*\})',
            r'\1\n\n    .mobile-cta-book:hover {\n        background: #1976D2;\n    }',
            content
        )

    # Pattern 3: Update button sizing for better conversion
    content = re.sub(
        r'(\.mobile-cta-btn \{[^}]*padding:)[^;]+(;)',
        r'\1 11px 10px\2',
        content
    )

    content = re.sub(
        r'(\.mobile-cta-btn \{[^}]*gap:)[^;]+(;)',
        r'\1 5px\2',
        content
    )

    content = re.sub(
        r'(\.mobile-cta-btn \{[^}]*font-size:)[^;]+(;)',
        r'\1 12.5px\2',
        content
    )

    # Pattern 4: Update 480px breakpoint
    content = re.sub(
        r'(@media \(max-width: 480px\) \{[^}]*\.mobile-cta-btn \{[^}]*padding:)[^;]+(;)',
        r'\1 10px 8px\2',
        content
    )

    content = re.sub(
        r'(@media \(max-width: 480px\) \{[^}]*\.mobile-cta-btn \{[^}]*gap:)[^;]+(;)',
        r'\1 4px\2',
        content
    )

    # Pattern 5: Add 375px breakpoint if missing
    if '@media (max-width: 375px)' not in content and '.mobile-cta-btn' in content:
        # Find the 480px media query closing brace
        pattern_375 = r'(@media \(max-width: 480px\) \{[^}]*\})\s*(\})'
        replacement_375 = r'''\1
    }

    /* Very Small Mobile (iPhone SE, etc) */
    @media (max-width: 375px) {
        .mobile-cta-btn {
            font-size: 11.5px;
            padding: 9px 6px;
        }

        .mobile-cta-btn svg {
            width: 20px;
            height: 20px;
        }
    '''
        content = re.sub(pattern_375, replacement_375, content)

    if content == original_content:
        print(f"[SKIP] No changes needed")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed mobile CTA buttons")

def main():
    """Main execution"""
    base_dir = Path('C:/NikaApplianceRepair')

    # List of all pages to fix
    pages_to_fix = []

    # Root pages
    pages_to_fix.append(base_dir / 'index.html')
    pages_to_fix.append(base_dir / 'services.html')
    pages_to_fix.append(base_dir / 'locations.html')

    # Service pages (9)
    services = [
        'refrigerator-repair', 'dishwasher-repair', 'washer-repair', 'dryer-repair',
        'oven-repair', 'stove-repair', 'range-repair', 'microwave-repair', 'freezer-repair'
    ]
    for service in services:
        pages_to_fix.append(base_dir / 'services' / f'{service}.html')

    # Location pages (20)
    locations = [
        'richmond-hill', 'mississauga', 'brampton', 'markham', 'vaughan',
        'oakville', 'milton', 'burlington', 'ajax', 'pickering',
        'whitby', 'oshawa', 'aurora', 'newmarket', 'etobicoke',
        'north-york', 'scarborough', 'caledon', 'east-gwillimbury', 'halton-hills'
    ]
    for location in locations:
        pages_to_fix.append(base_dir / 'locations' / f'{location}.html')

    # Brand pages (15)
    brands = [
        'samsung', 'lg', 'whirlpool', 'ge', 'bosch',
        'kitchenaid', 'maytag', 'frigidaire', 'electrolux', 'kenmore',
        'miele', 'fisher-paykel', 'amana', 'hotpoint', 'danby'
    ]
    for brand in brands:
        pages_to_fix.append(base_dir / 'brands' / f'{brand}-appliance-repair-toronto.html')

    # Process all pages
    fixed_count = 0
    error_count = 0

    for page in pages_to_fix:
        if page.exists():
            try:
                fix_mobile_cta_styles(page)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"MOBILE CTA BUTTONS FIX COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Processed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
