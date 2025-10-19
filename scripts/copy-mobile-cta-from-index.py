#!/usr/bin/env python3
"""
Copy mobile CTA styles from index.html to all other pages
"""

import re
from pathlib import Path

# Read the correct styles from index.html
def get_mobile_cta_styles_from_index():
    """Extract mobile CTA styles from index.html"""
    with open('C:/NikaApplianceRepair/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the mobile CTA section
    # From .mobile-cta-btn { to the end of @media (max-width: 375px)
    pattern = r'(\.mobile-cta-btn \{.*?@media \(max-width: 375px\) \{.*?\n    \})'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1)
    return None

def replace_mobile_cta_styles(file_path, new_styles):
    """Replace mobile CTA styles in a file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has mobile CTA styles
    if '.mobile-cta-btn' not in content:
        print(f"[SKIP] No mobile CTA buttons")
        return

    original_content = content

    # Pattern to match old mobile CTA styles
    # From .mobile-cta-btn { to wherever it ends (before next major section)
    old_pattern = r'\.mobile-cta-btn \{.*?(?=\n    /\* |@media \(max-width: 768px\)|\.skip-to-content)'

    # Replace with new styles
    content = re.sub(old_pattern, new_styles, content, flags=re.DOTALL)

    if content == original_content:
        print(f"[SKIP] No changes needed")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Updated mobile CTA styles")

def main():
    """Main execution"""
    base_dir = Path('C:/NikaApplianceRepair')

    # Get correct styles from index.html
    print("Extracting mobile CTA styles from index.html...")
    new_styles = get_mobile_cta_styles_from_index()

    if not new_styles:
        print("[ERROR] Could not extract styles from index.html")
        return

    print(f"[OK] Extracted {len(new_styles)} characters of styles")
    print()

    # List of all pages to fix (excluding index.html)
    pages_to_fix = []

    # Root pages
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
    skipped_count = 0
    error_count = 0

    for page in pages_to_fix:
        if page.exists():
            try:
                replace_mobile_cta_styles(page, new_styles)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"MOBILE CTA STYLES COPY COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Processed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
