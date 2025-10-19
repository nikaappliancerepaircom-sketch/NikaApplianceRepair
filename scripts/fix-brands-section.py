#!/usr/bin/env python3
"""
Fix 90+ Brands section across all pages
Make brand logo cards clickable for brands that have pages
"""

import os
import re
from pathlib import Path

# 15 brands that EXIST (have pages)
# Format: display name -> slug
EXISTING_BRANDS = {
    'Samsung': 'samsung',
    'SAMSUNG': 'samsung',
    'LG': 'lg',
    'Whirlpool': 'whirlpool',
    'WHIRLPOOL': 'whirlpool',
    'GE': 'ge',
    'Bosch': 'bosch',
    'BOSCH': 'bosch',
    'KitchenAid': 'kitchenaid',
    'Maytag': 'maytag',
    'MAYTAG': 'maytag',
    'Frigidaire': 'frigidaire',
    'FRIGIDAIRE': 'frigidaire',
    'Electrolux': 'electrolux',
    'Kenmore': 'kenmore',
    'Miele': 'miele',
    'MIELE': 'miele',
    'Fisher & Paykel': 'fisher-paykel',
    'Fisher &amp; Paykel': 'fisher-paykel',
    'Amana': 'amana',
    'AMANA': 'amana',
    'Hotpoint': 'hotpoint',
    'Danby': 'danby',
    'DANBY': 'danby',
}

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

def fix_brand_cards_in_content(content, category):
    """Convert brand logo card divs to links for brands with pages"""

    # Pattern to match brand-logo-card divs
    # <div class="brand-logo-card logo-xxx">
    #     <span class="brand-name-premium">BrandName</span>
    # </div>
    pattern = r'<div class="brand-logo-card([^"]*)">\s*<span class="brand-name-premium">([^<]+)</span>\s*</div>'

    def replace_card(match):
        logo_class = match.group(1)  # Captured text after "brand-logo-card"
        brand_name = match.group(2).strip()

        # Check if this brand has a page
        brand_slug = EXISTING_BRANDS.get(brand_name)

        if brand_slug:
            # Generate link with correct relative path
            if category == 'root':
                href = f'brands/{brand_slug}-appliance-repair-toronto'
            else:
                href = f'../brands/{brand_slug}-appliance-repair-toronto'

            # Build class attribute
            # If logo_class is not empty and doesn't start with space, add one
            if logo_class and not logo_class.startswith(' '):
                full_class = f"brand-logo-card {logo_class}"
            else:
                full_class = f"brand-logo-card{logo_class}"

            # Return <a> tag instead of <div>
            return f'<a href="{href}" class="{full_class}" style="color: inherit; text-decoration: none;">\n                    <span class="brand-name-premium">{brand_name}</span>\n                </a>'
        else:
            # No page - keep as div
            return match.group(0)

    # Replace all matching brand cards
    content = re.sub(pattern, replace_card, content)

    return content

def fix_brands_section_in_file(file_path):
    """Fix brand logo cards in a single HTML file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    category = get_page_category(file_path)

    # Check if page has brands section
    if 'brand-logo-card' not in content:
        print(f"[SKIP] No brands section found in {file_path}")
        return

    # Fix brand cards
    original_content = content
    content = fix_brand_cards_in_content(content, category)

    if content == original_content:
        print(f"[SKIP] No changes needed in {file_path}")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed brand cards in: {file_path}")

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
    skipped_count = 0
    error_count = 0

    for page in pages_to_fix:
        if page.exists():
            try:
                fix_brands_section_in_file(page)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"BRANDS SECTION FIX COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Processed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"[INFO] Total: {fixed_count + error_count} pages processed")
    print(f"[INFO] Linked to 15 brand pages")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
