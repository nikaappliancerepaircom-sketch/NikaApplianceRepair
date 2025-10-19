#!/usr/bin/env python3
"""
Fix Services section across all pages
Make all service headings clickable links to service pages
"""

import os
import re
from pathlib import Path

# Service name mapping to file slugs
SERVICE_MAPPING = {
    'Refrigerator Repair': 'refrigerator-repair',
    'Refrigerator': 'refrigerator-repair',  # Alternative match
    'Dishwasher Repair': 'dishwasher-repair',
    'Dishwasher': 'dishwasher-repair',
    'Washer Repair': 'washer-repair',
    'Washing Machine Repair': 'washer-repair',
    'Washer': 'washer-repair',
    'Dryer Repair': 'dryer-repair',
    'Dryer': 'dryer-repair',
    'Oven Repair': 'oven-repair',
    'Oven': 'oven-repair',
    'Stove Repair': 'stove-repair',
    'Stove': 'stove-repair',
    'Range Repair': 'range-repair',
    'Range': 'range-repair',
    'Microwave Repair': 'microwave-repair',
    'Microwave': 'microwave-repair',
    'Freezer Repair': 'freezer-repair',
    'Freezer': 'freezer-repair',
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

def fix_service_links_in_content(content, category):
    """Fix service headings to be links"""

    # Pattern 1: Match service headings that are already links (to update styling)
    pattern_existing = r'<h3><a href="([^"]*)" style="[^"]*">([^<]*(?:Refrigerator|Dishwasher|Washer|Washing Machine|Dryer|Oven|Stove|Range|Microwave|Freezer)[^<]*Repair?)</a></h3>'

    # Pattern 2: Match service headings without links
    pattern_new = r'<h3>([^<]*(?:Refrigerator|Dishwasher|Washer|Washing Machine|Dryer|Oven|Stove|Range|Microwave|Freezer)[^<]*Repair?)</h3>'

    def replace_existing_link(match):
        """Update existing links with proper gradient styling"""
        old_href = match.group(1)
        service_name = match.group(2).strip()

        gradient_style = 'background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-decoration: none;'
        return f'<h3><a href="{old_href}" style="{gradient_style}">{service_name}</a></h3>'

    def replace_new_heading(match):
        """Add links to headings without links"""
        service_name = match.group(1).strip()

        # Find the matching service slug
        service_slug = None
        for key, slug in SERVICE_MAPPING.items():
            if key.lower() in service_name.lower():
                service_slug = slug
                break

        if not service_slug:
            # No match, return original
            return match.group(0)

        # Generate correct path based on category
        if category == 'root':
            href = f'services/{service_slug}'
        else:
            href = f'../services/{service_slug}'

        # Return h3 with link (preserve gradient styling)
        gradient_style = 'background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-decoration: none;'
        return f'<h3><a href="{href}" style="{gradient_style}">{service_name}</a></h3>'

    # First update existing links
    content = re.sub(pattern_existing, replace_existing_link, content, flags=re.IGNORECASE)

    # Then add links to headings without links
    content = re.sub(pattern_new, replace_new_heading, content, flags=re.IGNORECASE)

    return content

def fix_services_section_in_file(file_path):
    """Fix service headings in a single HTML file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    category = get_page_category(file_path)

    # Check if page has service section
    if 'What Appliance Repair Services' not in content and 'service-card' not in content:
        print(f"[SKIP] No services section found in {file_path}")
        return

    # Fix service links
    original_content = content
    content = fix_service_links_in_content(content, category)

    if content == original_content:
        print(f"[SKIP] No changes needed in {file_path}")
        return

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed service links in: {file_path}")

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
                fix_services_section_in_file(page)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"SERVICES SECTION FIX COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Fixed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"[INFO] Total: {fixed_count + error_count} pages processed")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
