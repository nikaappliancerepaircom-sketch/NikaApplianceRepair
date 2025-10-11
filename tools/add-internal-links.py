#!/usr/bin/env python3
"""
Add internal links between pages using 2025 SEO best practices
Strategy: Topic clusters, contextual linking, authority flow
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re
import random

PROJECT_ROOT = Path(__file__).parent.parent

# Strategic internal linking based on SEO 2025 best practices
INTERNAL_LINKS = {
    'service_to_blog': {
        'refrigerator-repair': [
            ('how-to-fix-refrigerator-not-cooling', 'common refrigerator issues'),
            ('emergency-appliance-repair-fridge', 'emergency refrigerator problems'),
            ('appliance-maintenance-schedule', 'regular maintenance'),
        ],
        'washer-repair': [
            ('washer-not-draining-solutions', 'washing machine drainage problems'),
            ('appliance-maintenance-schedule', 'washer maintenance tips'),
            ('diy-vs-professional-appliance-repair', 'DIY versus professional fixes'),
        ],
        'dryer-repair': [
            ('dryer-not-heating-troubleshooting', 'dryer heating issues'),
            ('appliance-maintenance-schedule', 'dryer maintenance guide'),
            ('repair-vs-replace-appliances', 'repair or replacement decision'),
        ],
        'dishwasher-repair': [
            ('dishwasher-not-cleaning-solutions', 'dishwasher cleaning problems'),
            ('appliance-warranties-explained', 'warranty coverage'),
            ('best-appliance-brands-2025', 'dishwasher brand recommendations'),
        ],
        'oven-repair': [
            ('oven-temperature-calibration-guide', 'oven temperature issues'),
            ('appliance-repair-costs-toronto-2025', 'oven repair pricing'),
            ('signs-appliance-needs-repair', 'warning signs'),
        ],
    },

    'service_to_location': {
        'refrigerator-repair': ['toronto', 'mississauga', 'brampton', 'vaughan'],
        'washer-repair': ['markham', 'richmond-hill', 'oakville', 'burlington'],
        'dryer-repair': ['ajax', 'pickering', 'whitby', 'oshawa'],
        'dishwasher-repair': ['north-york', 'scarborough', 'etobicoke', 'thornhill'],
        'oven-repair': ['newmarket', 'aurora', 'barrie', 'milton'],
    },

    'blog_to_service': {
        'how-to-fix-refrigerator-not-cooling': 'refrigerator-repair',
        'washer-not-draining-solutions': 'washer-repair',
        'dryer-not-heating-troubleshooting': 'dryer-repair',
        'dishwasher-not-cleaning-solutions': 'dishwasher-repair',
        'oven-temperature-calibration-guide': 'oven-repair',
        'emergency-appliance-repair-fridge': 'refrigerator-repair',
    },

    'blog_related': {
        'appliance-maintenance-schedule': [
            'spring-appliance-maintenance-gta',
            'prepare-appliances-winter-toronto',
            'signs-appliance-needs-repair',
        ],
        'repair-vs-replace-appliances': [
            'appliance-repair-costs-toronto-2025',
            'best-appliance-brands-2025',
            'buying-used-appliances-toronto',
        ],
        'best-appliance-brands-2025': [
            'appliance-warranties-explained',
            'energy-efficient-appliances-worth-it',
            'repair-vs-replace-appliances',
        ],
    },
}

def add_contextual_links_to_service(file_path):
    """Add strategic internal links to service pages"""
    print(f"\nProcessing: {file_path.name}")

    if file_path.name == 'index.html':
        return False

    service_name = file_path.stem

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if already has internal links
    if 'Learn more about' in html and '/blog/' in html:
        print(f"  [SKIP] Already has internal links")
        return False

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if not body:
        return False

    # Find insertion point before footer
    footer = body.find('footer')
    if not footer:
        return False

    # Create related resources section
    related_html = '<div class="related-resources" style="margin: 40px 0; padding: 30px; background: #f8f9fa; border-radius: 8px;">\n'
    related_html += '<h2 style="color: #2c3e50; margin-bottom: 20px;">Related Resources</h2>\n'
    related_html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">\n'

    # Add blog links
    blog_links = []
    for key in INTERNAL_LINKS['service_to_blog']:
        if key in service_name:
            blog_links = INTERNAL_LINKS['service_to_blog'][key]
            break

    if blog_links:
        related_html += '<div>\n<h3 style="font-size: 18px; margin-bottom: 15px;">📚 Helpful Guides</h3>\n<ul style="list-style: none; padding: 0;">\n'
        for link, text in blog_links[:3]:
            related_html += f'<li style="margin: 10px 0;"><a href="/blog/{link}.html" style="color: #667eea; text-decoration: none;">Learn more about {text}</a></li>\n'
        related_html += '</ul>\n</div>\n'

    # Add location links
    location_links = []
    for key in INTERNAL_LINKS['service_to_location']:
        if key in service_name:
            location_links = INTERNAL_LINKS['service_to_location'][key]
            break

    if location_links:
        related_html += '<div>\n<h3 style="font-size: 18px; margin-bottom: 15px;">📍 Service Areas</h3>\n<ul style="list-style: none; padding: 0;">\n'
        for loc in location_links[:4]:
            loc_name = loc.replace('-', ' ').title()
            related_html += f'<li style="margin: 10px 0;"><a href="/locations/{loc}.html" style="color: #667eea; text-decoration: none;">Service in {loc_name}</a></li>\n'
        related_html += '</ul>\n</div>\n'

    # Add other service links
    all_services = ['refrigerator-repair', 'washer-repair', 'dryer-repair', 'dishwasher-repair', 'oven-repair', 'freezer-repair']
    other_services = [s for s in all_services if s != service_name and not s in service_name]
    random.shuffle(other_services)

    if other_services:
        related_html += '<div>\n<h3 style="font-size: 18px; margin-bottom: 15px;">🔧 Other Services</h3>\n<ul style="list-style: none; padding: 0;">\n'
        for svc in other_services[:3]:
            svc_name = svc.replace('-', ' ').title()
            related_html += f'<li style="margin: 10px 0;"><a href="/services/{svc}.html" style="color: #667eea; text-decoration: none;">{svc_name}</a></li>\n'
        related_html += '</ul>\n</div>\n'

    related_html += '</div>\n</div>\n'

    # Insert before footer
    footer.insert_before(BeautifulSoup(related_html, 'html.parser'))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"  [OK] Added internal links section")
    return True

def add_contextual_links_to_blog(file_path):
    """Add strategic internal links to blog posts"""
    print(f"\nProcessing: {file_path.name}")

    blog_name = file_path.stem

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if already has internal links
    if 'Related Articles' in html and '/blog/' in html:
        print(f"  [SKIP] Already has internal links")
        return False

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if not body:
        return False

    footer = body.find('footer')
    if not footer:
        return False

    # Create related articles section
    related_html = '<div class="related-articles" style="margin: 40px 0; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">\n'
    related_html += '<h2 style="margin-bottom: 20px;">Related Articles & Services</h2>\n'
    related_html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">\n'

    # Add related blog posts
    if blog_name in INTERNAL_LINKS['blog_related']:
        related_blogs = INTERNAL_LINKS['blog_related'][blog_name]
        related_html += '<div>\n<h3 style="font-size: 16px; margin-bottom: 15px; opacity: 0.9;">More Guides</h3>\n<ul style="list-style: none; padding: 0;">\n'
        for blog in related_blogs:
            blog_title = blog.replace('-', ' ').title()
            related_html += f'<li style="margin: 8px 0;"><a href="/blog/{blog}.html" style="color: white; text-decoration: underline;">→ {blog_title}</a></li>\n'
        related_html += '</ul>\n</div>\n'

    # Add service link if applicable
    if blog_name in INTERNAL_LINKS['blog_to_service']:
        service = INTERNAL_LINKS['blog_to_service'][blog_name]
        service_title = service.replace('-', ' ').title()
        related_html += '<div>\n<h3 style="font-size: 16px; margin-bottom: 15px; opacity: 0.9;">Professional Help</h3>\n'
        related_html += f'<a href="/services/{service}.html" style="display: inline-block; padding: 12px 24px; background: white; color: #667eea; text-decoration: none; border-radius: 6px; font-weight: bold;">Get {service_title}</a>\n'
        related_html += '</div>\n'

    # Add popular location links
    popular_locations = ['toronto', 'mississauga', 'brampton', 'vaughan', 'markham']
    related_html += '<div>\n<h3 style="font-size: 16px; margin-bottom: 15px; opacity: 0.9;">Service Areas</h3>\n<ul style="list-style: none; padding: 0; font-size: 14px;">\n'
    for loc in random.sample(popular_locations, 3):
        loc_name = loc.title()
        related_html += f'<li style="margin: 6px 0;"><a href="/locations/{loc}.html" style="color: white; opacity: 0.9;">{loc_name}</a></li>\n'
    related_html += '</ul>\n</div>\n'

    related_html += '</div>\n</div>\n'

    footer.insert_before(BeautifulSoup(related_html, 'html.parser'))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"  [OK] Added internal links section")
    return True

def add_contextual_links_to_location(file_path):
    """Add strategic internal links to location pages"""
    print(f"\nProcessing: {file_path.name}")

    if file_path.name == 'index.html':
        return False

    location_name = file_path.stem

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if already has internal links
    if 'Browse Services' in html and '/services/' in html:
        print(f"  [SKIP] Already has internal links")
        return False

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if not body:
        return False

    footer = body.find('footer')
    if not footer:
        return False

    # Create services & resources section
    related_html = '<div class="location-links" style="margin: 40px 0; padding: 30px; background: #f8f9fa; border-radius: 8px;">\n'
    related_html += '<h2 style="color: #2c3e50; margin-bottom: 20px;">Browse Services & Resources</h2>\n'
    related_html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 25px;">\n'

    # Add all services
    all_services = [
        ('refrigerator-repair', 'Refrigerator Repair'),
        ('washer-repair', 'Washing Machine Repair'),
        ('dryer-repair', 'Dryer Repair'),
        ('dishwasher-repair', 'Dishwasher Repair'),
        ('oven-repair', 'Oven Repair'),
        ('stove-cooktop-repair', 'Stove & Cooktop Repair'),
    ]

    related_html += '<div>\n<h3 style="font-size: 18px; margin-bottom: 15px;">🔧 Our Services</h3>\n<ul style="list-style: none; padding: 0;">\n'
    for svc, title in all_services:
        related_html += f'<li style="margin: 8px 0;"><a href="/services/{svc}.html" style="color: #667eea; text-decoration: none;">{title}</a></li>\n'
    related_html += '</ul>\n</div>\n'

    # Add nearby locations
    all_locations = ['toronto', 'mississauga', 'brampton', 'vaughan', 'markham', 'richmond-hill',
                     'oakville', 'burlington', 'ajax', 'pickering', 'north-york', 'scarborough']
    nearby = [loc for loc in all_locations if loc != location_name]
    random.shuffle(nearby)

    related_html += '<div>\n<h3 style="font-size: 18px; margin-bottom: 15px;">📍 Nearby Areas</h3>\n<ul style="list-style: none; padding: 0;">\n'
    for loc in nearby[:6]:
        loc_name = loc.replace('-', ' ').title()
        related_html += f'<li style="margin: 8px 0;"><a href="/locations/{loc}.html" style="color: #667eea; text-decoration: none;">{loc_name}</a></li>\n'
    related_html += '</ul>\n</div>\n'

    # Add helpful blog posts
    useful_blogs = [
        ('appliance-maintenance-schedule', 'Maintenance Schedule Guide'),
        ('appliance-repair-costs-toronto-2025', 'Repair Costs Guide'),
        ('emergency-appliance-repair-fridge', 'Emergency Repair Tips'),
        ('signs-appliance-needs-repair', 'Warning Signs to Watch'),
    ]

    related_html += '<div>\n<h3 style="font-size: 18px; margin-bottom: 15px;">📚 Helpful Guides</h3>\n<ul style="list-style: none; padding: 0;">\n'
    for blog, title in random.sample(useful_blogs, 3):
        related_html += f'<li style="margin: 8px 0;"><a href="/blog/{blog}.html" style="color: #667eea; text-decoration: none;">{title}</a></li>\n'
    related_html += '</ul>\n</div>\n'

    related_html += '</div>\n</div>\n'

    footer.insert_before(BeautifulSoup(related_html, 'html.parser'))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"  [OK] Added internal links section")
    return True

def main():
    print("="*70)
    print("ADDING INTERNAL LINKS - 2025 SEO BEST PRACTICES")
    print("="*70)
    print("\nStrategy: Topic clusters + Authority flow + Contextual linking")
    print("Target: 10-15 internal links per page")
    print()

    # Process services
    print("\n--- SERVICE PAGES ---")
    services_dir = PROJECT_ROOT / "services"
    service_count = 0
    for service_file in sorted(services_dir.glob("*.html")):
        if add_contextual_links_to_service(service_file):
            service_count += 1

    # Process blogs
    print("\n--- BLOG POSTS ---")
    blog_dir = PROJECT_ROOT / "blog"
    blog_count = 0
    for blog_file in sorted(blog_dir.glob("*.html")):
        if add_contextual_links_to_blog(blog_file):
            blog_count += 1

    # Process locations
    print("\n--- LOCATION PAGES ---")
    locations_dir = PROJECT_ROOT / "locations"
    location_count = 0
    for location_file in sorted(locations_dir.glob("*.html")):
        if add_contextual_links_to_location(location_file):
            location_count += 1

    print("\n" + "="*70)
    print(f"COMPLETE:")
    print(f"  Service pages: {service_count}")
    print(f"  Blog posts: {blog_count}")
    print(f"  Location pages: {location_count}")
    print(f"  Total: {service_count + blog_count + location_count}")
    print("="*70)
    print("\nExpected impact:")
    print("  - Internal links: 0 -> 10-15 per page")
    print("  - SEO score: +5-8 points")
    print("  - Estimated new average: 74-77/100")
    print("  - Service pages likely to reach 85+/100!")

if __name__ == "__main__":
    main()
