#!/usr/bin/env python3
"""
Fix all footer links across all pages with correct relative paths
Based on the SEO Interlinking Master Plan - Maximum Interlinking Strategy
"""

import os
import re
from pathlib import Path

# Page inventory
SERVICES = [
    'refrigerator-repair', 'dishwasher-repair', 'washer-repair', 'dryer-repair',
    'oven-repair', 'stove-repair', 'range-repair', 'microwave-repair', 'freezer-repair'
]

LOCATIONS = [
    'richmond-hill', 'mississauga', 'brampton', 'markham', 'vaughan',
    'oakville', 'milton', 'burlington', 'ajax', 'pickering',
    'whitby', 'oshawa', 'aurora', 'newmarket', 'etobicoke',
    'north-york', 'scarborough', 'caledon', 'east-gwillimbury', 'halton-hills'
]

BRANDS = [
    'samsung', 'lg', 'whirlpool', 'ge', 'bosch',
    'kitchenaid', 'maytag', 'frigidaire', 'electrolux', 'kenmore',
    'miele', 'fisher-paykel', 'amana', 'hotpoint', 'danby'
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

def generate_footer_services_links(category):
    """Generate service links based on page category"""
    links = []

    for service in SERVICES:
        if category == 'root':
            href = f'services/{service}'
        else:
            href = f'../services/{service}'

        # Capitalize properly (service already has -repair in it)
        name = service.replace('-', ' ').title()
        links.append(f'                        <li><a href="{href}">{name}</a></li>')

    return '\n'.join(links)

def generate_footer_locations_links(category):
    """Generate location links based on page category (TOP 12 only for footer)"""
    # Top 12 locations for footer
    top_locations = [
        ('mississauga', 'Mississauga'),
        ('brampton', 'Brampton'),
        ('markham', 'Markham'),
        ('vaughan', 'Vaughan'),
        ('richmond-hill', 'Richmond Hill'),
        ('oakville', 'Oakville'),
        ('burlington', 'Burlington'),
        ('oshawa', 'Oshawa'),
        ('ajax', 'Ajax'),
        ('pickering', 'Pickering'),
        ('milton', 'Milton'),
        ('whitby', 'Whitby'),
    ]

    links = []

    for slug, name in top_locations:
        if category == 'root':
            href = f'locations/{slug}'
        else:
            href = f'../locations/{slug}'

        links.append(f'                        <li><a href="{href}">{name}</a></li>')

    return '\n'.join(links)

def fix_footer_in_file(file_path):
    """Fix footer links in a single HTML file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    category = get_page_category(file_path)

    # Find and replace Services section
    services_pattern = r'(<h4 class="footer-heading">Our Services</h4>\s*<ul class="footer-links">)(.*?)(</ul>)'
    services_links = generate_footer_services_links(category)
    services_replacement = f'\\1\n{services_links}\n                    \\3'
    content = re.sub(services_pattern, services_replacement, content, flags=re.DOTALL)

    # Find and replace Locations section
    locations_pattern = r'(<h4 class="footer-heading">Top Service Areas</h4>\s*<ul class="footer-links">)(.*?)(</ul>)'
    locations_links = generate_footer_locations_links(category)
    locations_replacement = f'\\1\n{locations_links}\n                    \\3'
    content = re.sub(locations_pattern, locations_replacement, content, flags=re.DOTALL)

    # Fix Company section links
    if category == 'root':
        # Company links for root pages
        content = re.sub(r'href="/about"', 'href="about"', content)
        content = re.sub(r'href="/book"', 'href="book"', content)
        content = re.sub(r'href="/privacy"', 'href="privacy"', content)
        content = re.sub(r'href="/terms"', 'href="terms"', content)
        content = re.sub(r'href="/sitemap\.xml"', 'href="sitemap.xml"', content)
        content = re.sub(r'href="/#testimonials"', 'href="#testimonials"', content)
        content = re.sub(r'href="/#faq"', 'href="#faq"', content)
        content = re.sub(r'href="/#areas"', 'href="#areas"', content)
    else:
        # Company links for subfolder pages
        content = re.sub(r'href="/about"', 'href="../about"', content)
        content = re.sub(r'href="/book"', 'href="../book"', content)
        content = re.sub(r'href="/privacy"', 'href="../privacy"', content)
        content = re.sub(r'href="/terms"', 'href="../terms"', content)
        content = re.sub(r'href="/sitemap\.xml"', 'href="../sitemap.xml"', content)
        content = re.sub(r'href="/#testimonials"', 'href="../#testimonials"', content)
        content = re.sub(r'href="/#faq"', 'href="../#faq"', content)
        content = re.sub(r'href="/#areas"', 'href="../#areas"', content)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed: {file_path}")

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
    for service in SERVICES:
        pages_to_fix.append(base_dir / 'services' / f'{service}.html')

    # Location pages (20)
    for location in LOCATIONS:
        pages_to_fix.append(base_dir / 'locations' / f'{location}.html')

    # Brand pages (15)
    for brand in BRANDS:
        pages_to_fix.append(base_dir / 'brands' / f'{brand}-appliance-repair-toronto.html')

    # Process all pages
    fixed_count = 0
    error_count = 0

    for page in pages_to_fix:
        if page.exists():
            try:
                fix_footer_in_file(page)
                fixed_count += 1
            except Exception as e:
                print(f"[ERROR] Error processing {page}: {e}")
                error_count += 1
        else:
            print(f"[WARN] File not found: {page}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"FOOTER LINKS FIX COMPLETE")
    print(f"{'='*60}")
    print(f"[OK] Fixed: {fixed_count} pages")
    print(f"[ERROR] Errors: {error_count} pages")
    print(f"[INFO] Total: {fixed_count + error_count} pages processed")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
