#!/usr/bin/env python3
"""
Add optimized meta descriptions to all pages
150-160 characters for perfect SEO
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup

# Meta descriptions by page type
SERVICE_META_TEMPLATES = {
    'refrigerator-repair': 'Professional refrigerator repair service in Toronto & GTA. Same-day service • 90-day warranty • Licensed technicians. Call 437-747-6737!',
    'washer-repair': 'Expert washer repair in Toronto & GTA. Same-day service • All brands • 90-day warranty • Licensed technicians. Call 437-747-6737 now!',
    'dryer-repair': 'Professional dryer repair Toronto & GTA. Same-day service • All brands • 90-day warranty • Licensed & insured. Call 437-747-6737!',
    'dishwasher-repair': 'Dishwasher repair Toronto & GTA. Same-day service • All brands • 90-day warranty • Licensed technicians. Call 437-747-6737 today!',
    'oven-repair': 'Oven repair service in Toronto & GTA. Same-day repairs • All brands • 90-day warranty • Licensed & insured. Call 437-747-6737!',
    'stove-cooktop-repair': 'Stove & cooktop repair Toronto. Same-day service • Gas & electric • 90-day warranty • Licensed technicians. Call 437-747-6737!',
    'freezer-repair': 'Freezer repair Toronto & GTA. Same-day service • All brands • 90-day warranty • Licensed & insured technicians. Call 437-747-6737!',
    'dishwasher-installation': 'Professional dishwasher installation Toronto. Expert service • All brands • 90-day warranty • Licensed & insured. Call 437-747-6737!',
    'refrigerator-freezer-repair': 'Refrigerator & freezer repair Toronto. Same-day service • All brands • 90-day warranty • Licensed technicians. Call 437-747-6737!',
    'washer-dryer-repair': 'Washer & dryer repair Toronto & GTA. Same-day service • All brands • 90-day warranty • Licensed & insured. Call 437-747-6737!',
    'oven-stove-repair': 'Oven & stove repair Toronto. Same-day service • Gas & electric • 90-day warranty • Licensed technicians. Call 437-747-6737!'
}

def get_location_meta(location_name):
    """Generate meta description for location page"""
    return f"Professional appliance repair in {location_name} & area. Same-day service • 90-day warranty • All brands. Call 437-747-6737!"

def get_blog_meta(title):
    """Generate meta description for blog page"""
    clean_title = title.replace('How to Fix a ', '').replace('Complete Guide 2025', '').strip()
    return f"{clean_title}? Learn expert troubleshooting steps to fix issues. DIY solutions + when to call a professional. Save $100s!"

def add_meta_description(file_path, meta_description):
    """Add or update meta description in HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Check if meta description already exists
        existing_meta = soup.find('meta', attrs={'name': 'description'})

        if existing_meta:
            # Update existing
            existing_meta['content'] = meta_description
            updated = True
        else:
            # Add new meta description after charset or viewport
            head = soup.find('head')
            if head:
                meta_tag = soup.new_tag('meta', attrs={'name': 'description', 'content': meta_description})

                # Find viewport or charset to insert after
                viewport = head.find('meta', attrs={'name': 'viewport'})
                charset = head.find('meta', attrs={'charset': True})

                if viewport:
                    viewport.insert_after(meta_tag)
                elif charset:
                    charset.insert_after(meta_tag)
                else:
                    head.insert(0, meta_tag)

                updated = True
            else:
                return False

        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("ADDING META DESCRIPTIONS TO ALL PAGES")
    print("=" * 60)

    # Services
    print("\nSERVICE PAGES:")
    services_dir = base_dir / 'services'
    service_count = 0

    for service_file, meta_desc in SERVICE_META_TEMPLATES.items():
        file_path = services_dir / f"{service_file}.html"
        if file_path.exists():
            if add_meta_description(file_path, meta_desc):
                print(f"[ADDED] {service_file}.html ({len(meta_desc)} chars)")
                service_count += 1

    # Locations
    print("\nLOCATION PAGES:")
    locations_dir = base_dir / 'locations'
    location_count = 0

    location_names = {
        'ajax': 'Ajax',
        'aurora': 'Aurora',
        'barrie': 'Barrie',
        'bolton': 'Bolton',
        'brampton': 'Brampton',
        'burlington': 'Burlington',
        'caledon': 'Caledon',
        'concord': 'Concord',
        'east-gwillimbury': 'East Gwillimbury',
        'etobicoke': 'Etobicoke',
        'georgetown': 'Georgetown',
        'king-city': 'King City',
        'maple': 'Maple',
        'markham': 'Markham',
        'milton': 'Milton',
        'mississauga': 'Mississauga',
        'newmarket': 'Newmarket',
        'north-york': 'North York',
        'oakville': 'Oakville',
        'oshawa': 'Oshawa',
        'pickering': 'Pickering',
        'richmond-hill': 'Richmond Hill',
        'scarborough': 'Scarborough',
        'stouffville': 'Stouffville',
        'thornhill': 'Thornhill',
        'toronto': 'Toronto',
        'uxbridge': 'Uxbridge',
        'vaughan': 'Vaughan',
        'whitby': 'Whitby',
        'woodbridge': 'Woodbridge'
    }

    for location_file, location_name in location_names.items():
        file_path = locations_dir / f"{location_file}.html"
        if file_path.exists():
            meta_desc = get_location_meta(location_name)
            if add_meta_description(file_path, meta_desc):
                print(f"[ADDED] {location_file}.html ({len(meta_desc)} chars)")
                location_count += 1

    # Blogs
    print("\nBLOG PAGES:")
    blog_dir = base_dir / 'blog'
    blog_count = 0

    blog_metas = {
        'how-to-fix-refrigerator-not-cooling': 'Refrigerator not cooling? Learn expert troubleshooting steps to fix cooling issues. DIY solutions + when to call a professional. Save $100s!',
        'washer-not-draining-solutions': 'Washer not draining? Expert solutions for washing machine drainage issues. DIY fixes + professional help. Toronto appliance repair guide.',
        'dryer-not-heating-troubleshooting': 'Dryer not heating? Complete troubleshooting guide for heating issues. DIY solutions + expert help. Fix your dryer fast in Toronto!',
        'dishwasher-not-cleaning-solutions': 'Dishwasher not cleaning dishes? Expert solutions for cleaning issues. DIY fixes + professional help. Toronto appliance repair guide.',
        'oven-temperature-calibration-guide': 'Oven temperature wrong? Complete calibration guide for accurate cooking. DIY solutions + professional help. Toronto appliance repair.',
        'appliance-maintenance-schedule': 'Complete appliance maintenance schedule for Toronto homes. Extend lifespan • Prevent breakdowns • Expert tips. Save money on repairs!',
        'signs-appliance-needs-repair': '10 warning signs your appliance needs repair. Catch problems early • Save money • Prevent breakdowns. Toronto appliance repair guide.',
        'diy-vs-professional-appliance-repair': 'DIY vs professional appliance repair: When to call experts. Save money • Stay safe • Get reliable fixes. Toronto repair guide 2025.',
        'best-appliance-brands-2025': 'Best appliance brands 2025: Expert reviews & reliability ratings. LG • Samsung • Whirlpool • Bosch compared. Toronto buying guide.',
        'repair-vs-replace-appliances': 'Repair vs replace appliances: Cost analysis & decision guide. Expert advice • Calculate value • Make smart choices. Toronto 2025.',
        'energy-efficient-appliances-worth-it': 'Are energy-efficient appliances worth it? Complete cost analysis. ROI calculator • Savings breakdown • Expert recommendations 2025.',
        'buying-used-appliances-toronto': 'Buying used appliances Toronto: Complete safety & value guide. What to check • Red flags • Best deals. Expert tips 2025.',
        'appliance-warranties-explained': 'Appliance warranties explained: Coverage guide & claims process. Extended warranties • What\'s covered • Expert advice Toronto 2025.',
        'appliance-repair-costs-toronto-2025': 'Appliance repair costs Toronto 2025: Complete pricing guide. Average costs • What affects price • Save money. Expert breakdown.',
        'reliable-appliance-repair-gta': 'Finding reliable appliance repair in GTA: Complete guide. Check credentials • Compare prices • Avoid scams. Expert tips 2025.',
        'toronto-appliance-disposal-recycling': 'Toronto appliance disposal & recycling guide. Free pickup • Eco-friendly options • Rebates available. Safe disposal 2025.',
        'buy-appliance-parts-toronto': 'Where to buy appliance parts Toronto: Complete parts guide. OEM vs aftermarket • Best stores • Online options. Save money 2025.',
        'prepare-appliances-winter-toronto': 'Prepare appliances for winter Toronto: Complete winterization guide. Prevent damage • Save energy • Expert maintenance tips.',
        'spring-appliance-maintenance-gta': 'Spring appliance maintenance GTA: Complete checklist. Prevent breakdowns • Extend lifespan • Save money. Expert guide 2025.',
        'emergency-appliance-repair-fridge': 'Emergency refrigerator repair Toronto: 24/7 service guide. Same-day fixes • Save food • Prevent damage. Call 437-747-6737!'
    }

    for blog_file, meta_desc in blog_metas.items():
        file_path = blog_dir / f"{blog_file}.html"
        if file_path.exists():
            if add_meta_description(file_path, meta_desc):
                print(f"[ADDED] {blog_file}.html ({len(meta_desc)} chars)")
                blog_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Services:  {service_count}/{len(SERVICE_META_TEMPLATES)} updated")
    print(f"  Locations: {location_count}/{len(location_names)} updated")
    print(f"  Blogs:     {blog_count}/{len(blog_metas)} updated")
    print(f"  Total:     {service_count + location_count + blog_count} pages updated")
    print("=" * 60)

if __name__ == '__main__':
    main()
