#!/usr/bin/env python3
"""
Generate all pages from main template (index.html)
Clones the design/structure of index.html to services, locations, and blog
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent.parent

# All locations to generate (30 total)
LOCATIONS = [
    # Existing
    {"name": "Toronto", "slug": "toronto", "region": "Central"},
    {"name": "Mississauga", "slug": "mississauga", "region": "West"},
    {"name": "Brampton", "slug": "brampton", "region": "West"},
    {"name": "Vaughan", "slug": "vaughan", "region": "North"},
    {"name": "Markham", "slug": "markham", "region": "East"},
    {"name": "Richmond Hill", "slug": "richmond-hill", "region": "North"},
    {"name": "Etobicoke", "slug": "etobicoke", "region": "West"},
    {"name": "Scarborough", "slug": "scarborough", "region": "East"},
    {"name": "North York", "slug": "north-york", "region": "Central"},
    # New
    {"name": "Barrie", "slug": "barrie", "region": "North"},
    {"name": "East Gwillimbury", "slug": "east-gwillimbury", "region": "North"},
    {"name": "Newmarket", "slug": "newmarket", "region": "North"},
    {"name": "Uxbridge", "slug": "uxbridge", "region": "East"},
    {"name": "Aurora", "slug": "aurora", "region": "North"},
    {"name": "Pickering", "slug": "pickering", "region": "East"},
    {"name": "Ajax", "slug": "ajax", "region": "East"},
    {"name": "Whitby", "slug": "whitby", "region": "East"},
    {"name": "Oshawa", "slug": "oshawa", "region": "East"},
    {"name": "Oakville", "slug": "oakville", "region": "West"},
    {"name": "Burlington", "slug": "burlington", "region": "West"},
    {"name": "Milton", "slug": "milton", "region": "West"},
    {"name": "Georgetown", "slug": "georgetown", "region": "West"},
    {"name": "King City", "slug": "king-city", "region": "North"},
    {"name": "Stouffville", "slug": "stouffville", "region": "East"},
    {"name": "Maple", "slug": "maple", "region": "North"},
    {"name": "Thornhill", "slug": "thornhill", "region": "North"},
    {"name": "Concord", "slug": "concord", "region": "North"},
    {"name": "Woodbridge", "slug": "woodbridge", "region": "North"},
    {"name": "Bolton", "slug": "bolton", "region": "West"},
    {"name": "Caledon", "slug": "caledon", "region": "West"},
]

# All services
SERVICES = [
    {"name": "Refrigerator Repair", "slug": "refrigerator-repair", "icon": "❄️", "emoji": "🧊"},
    {"name": "Washer Repair", "slug": "washer-repair", "icon": "👕", "emoji": "🌀"},
    {"name": "Dryer Repair", "slug": "dryer-repair", "icon": "🌪️", "emoji": "🔥"},
    {"name": "Oven Repair", "slug": "oven-repair", "icon": "🔥", "emoji": "🍕"},
    {"name": "Stove Cooktop Repair", "slug": "stove-cooktop-repair", "icon": "🔥", "emoji": "🍳"},
    {"name": "Freezer Repair", "slug": "freezer-repair", "icon": "🧊", "emoji": "❄️"},
    {"name": "Dishwasher Repair", "slug": "dishwasher-repair", "icon": "🍽️", "emoji": "💦"},
    {"name": "Refrigerator Freezer Repair", "slug": "refrigerator-freezer-repair", "icon": "❄️", "emoji": "🧊"},
    {"name": "Washer Dryer Repair", "slug": "washer-dryer-repair", "icon": "👕", "emoji": "🌀"},
    {"name": "Oven Stove Repair", "slug": "oven-stove-repair", "icon": "🔥", "emoji": "🍕"},
    {"name": "Dishwasher Installation", "slug": "dishwasher-installation", "icon": "🍽️", "emoji": "🔧"},
]

def load_main_template():
    """Load index.html as template"""
    index_path = PROJECT_ROOT / "index.html"
    with open(index_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_location_page(location, template):
    """Create location page from template"""
    soup = BeautifulSoup(template, 'html.parser')

    location_name = location['name']
    slug = location['slug']

    # Update title
    title = soup.find('title')
    if title:
        title.string = f"Appliance Repair {location_name} | Same Day Service | Nika"

    # Update meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        meta_desc['content'] = f"Professional appliance repair in {location_name} & area. Same-day service • 90-day warranty • All brands. Call 437-747-6737!"

    # Update H1
    h1 = soup.find('h1')
    if h1:
        # Keep the wow animation structure but change text
        h1_text = h1.get_text()
        if 'WOW' in h1_text:
            new_html = f'''Appliance Repair in <span class="highlight-yellow">{location_name}</span>
                        that will <span class="highlight-yellow">make</span> you say...
                        <span class="wow-text">WOW!</span>'''
            h1.clear()
            h1.append(BeautifulSoup(new_html, 'html.parser'))

    # Update about section if exists
    about_section = soup.find('section', class_=re.compile('about'))
    if about_section:
        story = about_section.find('div', class_='company-story')
        if story:
            p = story.find('p')
            if p and '6+ years' in p.get_text():
                p.string = f"With 6+ years of experience, Nika Appliance Repair has been serving homeowners in {location_name} and surrounding areas. We provide fast, reliable appliance repair with a focus on customer satisfaction."

    return str(soup)

def create_service_page(service, template):
    """Create service page from template"""
    soup = BeautifulSoup(template, 'html.parser')

    service_name = service['name']
    slug = service['slug']
    icon = service['icon']

    # Update title
    title = soup.find('title')
    if title:
        title.string = f"{service_name} Toronto | Same Day Service | Nika"

    # Update meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        meta_desc['content'] = f"Professional {service_name.lower()} service in Toronto & GTA. Same-day service • 90-day warranty • Licensed technicians. Call 437-747-6737!"

    # Update H1
    h1 = soup.find('h1')
    if h1:
        new_html = f'''{icon} <span class="highlight-yellow">{service_name}</span>
                    that will <span class="highlight-yellow">make</span> you say...
                    <span class="wow-text">WOW!</span>'''
        h1.clear()
        h1.append(BeautifulSoup(new_html, 'html.parser'))

    # Update about section
    about_section = soup.find('section', class_=re.compile('about'))
    if about_section:
        story = about_section.find('div', class_='company-story')
        if story:
            p = story.find('p')
            if p:
                p.string = f"With 6+ years of experience, Nika Appliance Repair specializes in {service_name.lower()}. Our certified technicians handle all major brands with precision and care, backed by our comprehensive 90-day warranty."

    return str(soup)

def main():
    print("=" * 70)
    print("GENERATING ALL PAGES FROM MAIN TEMPLATE")
    print("=" * 70)
    print()

    # Load template
    print("[1/3] Loading main template (index.html)...")
    template = load_main_template()
    print("  [OK] Template loaded")

    # Generate location pages
    print(f"\n[2/3] Generating {len(LOCATIONS)} location pages...")
    locations_dir = PROJECT_ROOT / "locations"
    locations_dir.mkdir(exist_ok=True)

    for i, location in enumerate(LOCATIONS, 1):
        page_content = create_location_page(location, template)
        output_path = locations_dir / f"{location['slug']}.html"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_content)

        print(f"  [{i}/{len(LOCATIONS)}] Created: {location['name']}")

    print(f"  [OK] All {len(LOCATIONS)} location pages created")

    # Generate service pages
    print(f"\n[3/3] Generating {len(SERVICES)} service pages...")
    services_dir = PROJECT_ROOT / "services"
    services_dir.mkdir(exist_ok=True)

    for i, service in enumerate(SERVICES, 1):
        page_content = create_service_page(service, template)
        output_path = services_dir / f"{service['slug']}.html"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_content)

        print(f"  [{i}/{len(SERVICES)}] Created: {service['name']}")

    print(f"  [OK] All {len(SERVICES)} service pages created")

    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nTotal pages created: {len(LOCATIONS) + len(SERVICES)}")
    print(f"  - Locations: {len(LOCATIONS)}")
    print(f"  - Services: {len(SERVICES)}")
    print()
    print("Next step: Generate blog posts")
    print("=" * 70)

if __name__ == "__main__":
    main()
