#!/usr/bin/env python3
"""
Fix 60+ Service Areas section across all pages
Link to ALL 20 location pages that exist
Keep other locations as text only (no links)
"""

import os
import re
from pathlib import Path

# 20 locations that EXIST (have pages)
EXISTING_LOCATIONS = {
    'richmond-hill': 'Richmond Hill',
    'mississauga': 'Mississauga',
    'brampton': 'Brampton',
    'markham': 'Markham',
    'vaughan': 'Vaughan',
    'oakville': 'Oakville',
    'milton': 'Milton',
    'burlington': 'Burlington',
    'ajax': 'Ajax',
    'pickering': 'Pickering',
    'whitby': 'Whitby',
    'oshawa': 'Oshawa',
    'aurora': 'Aurora',
    'newmarket': 'Newmarket',
    'etobicoke': 'Etobicoke',
    'north-york': 'North York',
    'scarborough': 'Scarborough',
    'caledon': 'Caledon',
    'east-gwillimbury': 'East Gwillimbury',
    'halton-hills': 'Halton Hills'
}

# ALL 60+ locations to display (in alphabetical order for clean presentation)
ALL_SERVICE_AREAS = [
    ('ajax', 'Ajax'),
    ('aurora', 'Aurora'),
    ('agincourt', 'Agincourt'),
    ('bayview-glen', 'Bayview Glen'),
    ('berczy-village', 'Berczy Village'),
    ('beverley-glen', 'Beverley Glen'),
    ('bradford', 'Bradford'),
    ('beverley-acres', 'Beverley Acres'),
    ('brampton', 'Brampton'),
    ('burlington', 'Burlington'),
    ('cachet', 'Cachet'),
    ('caledon', 'Caledon'),
    ('cathedraltown', 'Cathedraltown'),
    ('concord', 'Concord'),
    ('don-valley-village', 'Don Valley Village'),
    ('elgin-mills', 'Elgin Mills'),
    ('east-gwillimbury', 'East Gwillimbury'),
    ('east-york', 'East York'),
    ('etobicoke', 'Etobicoke'),
    ('georgetown', 'Georgetown'),
    ('greensborough', 'Greensborough'),
    ('gormley', 'Gormley'),
    ('halton-hills', 'Halton Hills'),
    ('hillcrest-village', 'Hillcrest Village'),
    ('holland-landing', 'Holland Landing'),
    ('innisfil', 'Innisfil'),
    ('king-city', 'King City'),
    ('kleinburg', 'Kleinburg'),
    ('langstaff', 'Langstaff'),
    ('lamoreaux', 'Lamoreaux'),
    ('maple', 'Maple'),
    ('markham', 'Markham'),
    ('milton', 'Milton'),
    ('mount-albert', 'Mount Albert'),
    ('milliken', 'Milliken'),
    ('mississauga', 'Mississauga'),
    ('newmarket', 'Newmarket'),
    ('north-york', 'North York'),
    ('oak-ridges', 'Oak Ridges'),
    ('oakville', 'Oakville'),
    ('oshawa', 'Oshawa'),
    ('pickering', 'Pickering'),
    ('richmond-hill', 'Richmond Hill'),
    ('richvale', 'Richvale'),
    ('raymerville-markville-east', 'Raymerville Markville East'),
    ('steeles', 'Steeles'),
    ('scarborough', 'Scarborough'),
    ('schomberg', 'Schomberg'),
    ('stouffville', 'Stouffville'),
    ('thornhill', 'Thornhill'),
    ('toronto', 'Toronto'),
    ('unionville', 'Unionville'),
    ('uxbridge', 'Uxbridge'),
    ('vaughan', 'Vaughan'),
    ('whitby', 'Whitby'),
    ('woodbridge', 'Woodbridge'),
    ('wismer-commons', 'Wismer Commons'),
    ('yongehurst', 'Yongehurst'),
]

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

def generate_service_areas_grid(category):
    """Generate the 60+ service areas grid with links to existing pages only"""
    items = []

    for slug, name in ALL_SERVICE_AREAS:
        # Check if this location has a page
        if slug in EXISTING_LOCATIONS:
            # Generate link with correct relative path
            if category == 'root':
                href = f'locations/{slug}'
            else:
                href = f'../locations/{slug}'

            items.append(f'                <a href="{href}" class="area-item-premium"><span class="area-name-premium">{name}</span></a>')
        else:
            # No page - keep as text only
            items.append(f'                <span class="area-item-premium"><span class="area-name-premium">{name}</span></span>')

    return '\n'.join(items)

def fix_service_areas_in_file(file_path):
    """Fix the 60+ Service Areas section in a single HTML file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    category = get_page_category(file_path)

    # Find and replace the areas grid
    # Pattern: from opening <div class="areas-grid-premium"> to closing </div>
    pattern = r'(<div class="areas-grid-premium">)(.*?)(</div>)'

    # Check if section exists
    if not re.search(pattern, content, flags=re.DOTALL):
        print(f"[SKIP] No service areas section found in {file_path}")
        return

    areas_grid = generate_service_areas_grid(category)
    replacement = f'\\1\n{areas_grid}\n            \\3'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed service areas in: {file_path}")

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
    for location_slug in EXISTING_LOCATIONS.keys():
        pages_to_fix.append(base_dir / 'locations' / f'{location_slug}.html')

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
                fix_service_areas_in_file(page)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"SERVICE AREAS SECTION FIX COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Fixed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"[INFO] Total: {fixed_count + error_count} pages processed")
    print(f"[INFO] Linked to {len(EXISTING_LOCATIONS)} existing location pages")
    print(f"[INFO] Displaying {len(ALL_SERVICE_AREAS)} total service areas")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
