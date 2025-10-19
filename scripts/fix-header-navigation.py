#!/usr/bin/env python3
"""
Fix header navigation links to use relative paths
"""

import re
from pathlib import Path

def get_page_category(file_path):
    """Determine which category a page belongs to"""
    path_str = str(file_path).replace('\\', '/')

    if '/services/' in path_str:
        return 'services'
    elif '/locations/' in path_str:
        return 'locations'
    elif '/brands/' in path_str:
        return 'brands'
    else:
        return 'root'

def fix_header_navigation(file_path):
    """Fix header navigation links in a file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    category = get_page_category(file_path)
    original_content = content

    # Fix header navigation links
    if category == 'root':
        # Root pages - logo link to homepage (same page)
        content = re.sub(r'<a href="/" aria-label="Nika Appliance Repair - Home">', '<a href="#" aria-label="Nika Appliance Repair - Home">', content)
        content = re.sub(r'href="/services"', 'href="services"', content)
        content = re.sub(r'href="/locations"', 'href="locations"', content)
        content = re.sub(r'href="/services/"', 'href="services"', content)
        content = re.sub(r'href="/locations/"', 'href="locations"', content)
    else:
        # Subfolder pages - logo link to homepage (parent directory)
        content = re.sub(r'<a href="/" aria-label="Nika Appliance Repair - Home">', '<a href="../" aria-label="Nika Appliance Repair - Home">', content)
        content = re.sub(r'href="/services"', 'href="../services"', content)
        content = re.sub(r'href="/locations"', 'href="../locations"', content)
        content = re.sub(r'href="/services/"', 'href="../services"', content)
        content = re.sub(r'href="/locations/"', 'href="../locations"', content)

    if content == original_content:
        print(f"[SKIP] No changes needed")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed header navigation")

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
                fix_header_navigation(page)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"HEADER NAVIGATION FIX COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Processed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
