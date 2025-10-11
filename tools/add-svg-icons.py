#!/usr/bin/env python3
"""
Add SVG icons as images throughout the site
Google will count these as images for SEO
Each icon has proper alt tags
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent

# SVG icons for different appliances and services
SVG_ICONS = {
    'refrigerator': '''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Refrigerator icon">
        <rect x="15" y="5" width="50" height="70" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <line x1="15" y1="35" x2="65" y2="35" stroke="#4c51bf" stroke-width="2"/>
        <circle cx="60" cy="20" r="2" fill="#fff"/>
        <circle cx="60" cy="50" r="2" fill="#fff"/>
        <rect x="20" y="10" width="8" height="15" rx="1" fill="#e0e7ff"/>
    </svg>''',

    'washer': '''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Washing machine icon">
        <rect x="10" y="10" width="60" height="65" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <rect x="15" y="15" width="50" height="10" rx="2" fill="#4c51bf"/>
        <circle cx="25" cy="20" r="2" fill="#10b981"/>
        <circle cx="35" cy="20" r="2" fill="#ef4444"/>
        <circle cx="40" cy="45" r="18" fill="#e0e7ff" stroke="#4c51bf" stroke-width="2"/>
        <circle cx="40" cy="45" r="12" fill="none" stroke="#667eea" stroke-width="2" stroke-dasharray="8 4"/>
    </svg>''',

    'dryer': '''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dryer icon">
        <rect x="10" y="10" width="60" height="65" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <rect x="15" y="15" width="50" height="10" rx="2" fill="#4c51bf"/>
        <circle cx="25" cy="20" r="2" fill="#fbbf24"/>
        <circle cx="35" cy="20" r="2" fill="#10b981"/>
        <circle cx="40" cy="48" r="20" fill="#e0e7ff" stroke="#4c51bf" stroke-width="2"/>
        <path d="M 35 43 Q 40 48 45 43" stroke="#667eea" stroke-width="2" fill="none"/>
        <path d="M 35 53 Q 40 48 45 53" stroke="#667eea" stroke-width="2" fill="none"/>
    </svg>''',

    'dishwasher': '''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dishwasher icon">
        <rect x="10" y="15" width="60" height="60" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <rect x="15" y="20" width="50" height="8" rx="1" fill="#4c51bf"/>
        <circle cx="25" cy="24" r="2" fill="#10b981"/>
        <rect x="15" y="32" width="50" height="38" rx="2" fill="#e0e7ff"/>
        <line x1="20" y1="45" x2="60" y2="45" stroke="#667eea" stroke-width="1.5"/>
        <line x1="20" y1="55" x2="60" y2="55" stroke="#667eea" stroke-width="1.5"/>
        <circle cx="30" cy="40" r="3" fill="#bae6fd"/>
        <circle cx="45" cy="50" r="3" fill="#bae6fd"/>
        <circle cx="50" cy="62" r="3" fill="#bae6fd"/>
    </svg>''',

    'oven': '''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Oven icon">
        <rect x="10" y="10" width="60" height="65" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <circle cx="25" cy="22" r="3" fill="#4c51bf"/>
        <circle cx="40" cy="22" r="3" fill="#4c51bf"/>
        <circle cx="55" cy="22" r="3" fill="#4c51bf"/>
        <rect x="15" y="33" width="50" height="37" rx="2" fill="#e0e7ff" stroke="#4c51bf" stroke-width="2"/>
        <circle cx="60" cy="50" r="2" fill="#fff"/>
        <line x1="25" y1="50" x2="45" y2="50" stroke="#ef4444" stroke-width="2"/>
        <line x1="25" y1="58" x2="45" y2="58" stroke="#ef4444" stroke-width="2"/>
    </svg>''',

    'stove': '''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Stove icon">
        <rect x="10" y="15" width="60" height="55" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <circle cx="28" cy="35" r="8" fill="#4c51bf"/>
        <circle cx="52" cy="35" r="8" fill="#4c51bf"/>
        <circle cx="28" cy="55" r="8" fill="#4c51bf"/>
        <circle cx="52" cy="55" r="8" fill="#4c51bf"/>
        <circle cx="28" cy="35" r="4" fill="#ef4444"/>
        <circle cx="52" cy="35" r="4" fill="#ef4444"/>
        <circle cx="28" cy="55" r="4" fill="#fbbf24"/>
        <circle cx="52" cy="55" r="4" fill="#fbbf24"/>
    </svg>''',

    'checkmark': '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Checkmark icon">
        <circle cx="30" cy="30" r="28" fill="#10b981" stroke="#059669" stroke-width="2"/>
        <path d="M 15 30 L 25 40 L 45 20" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>''',

    'warning': '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Warning icon">
        <path d="M 30 5 L 55 50 L 5 50 Z" fill="#fbbf24" stroke="#f59e0b" stroke-width="2"/>
        <line x1="30" y1="20" x2="30" y2="35" stroke="#78350f" stroke-width="3" stroke-linecap="round"/>
        <circle cx="30" cy="42" r="2" fill="#78350f"/>
    </svg>''',

    'phone': '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Phone icon">
        <rect x="15" y="8" width="30" height="44" rx="3" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <rect x="18" y="12" width="24" height="32" rx="1" fill="#e0e7ff"/>
        <circle cx="30" cy="48" r="2" fill="#fff"/>
    </svg>''',

    'calendar': '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Calendar icon">
        <rect x="10" y="15" width="40" height="38" rx="2" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <rect x="10" y="15" width="40" height="10" rx="2" fill="#4c51bf"/>
        <line x1="20" y1="10" x2="20" y2="20" stroke="#4c51bf" stroke-width="2" stroke-linecap="round"/>
        <line x1="40" y1="10" x2="40" y2="20" stroke="#4c51bf" stroke-width="2" stroke-linecap="round"/>
        <circle cx="20" cy="35" r="2" fill="#fff"/>
        <circle cx="30" cy="35" r="2" fill="#fff"/>
        <circle cx="40" cy="35" r="2" fill="#fff"/>
        <circle cx="20" cy="45" r="2" fill="#fff"/>
        <circle cx="30" cy="45" r="2" fill="#fff"/>
    </svg>''',

    'tools': '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tools icon">
        <path d="M 15 45 L 15 25 L 25 15 L 30 20 L 20 30 L 20 45 Z" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
        <path d="M 35 20 L 45 10 L 50 15 L 40 25 Z" fill="#10b981" stroke="#059669" stroke-width="2"/>
        <circle cx="40" cy="40" r="8" fill="none" stroke="#4c51bf" stroke-width="2"/>
        <line x1="45" y1="45" x2="52" y2="52" stroke="#4c51bf" stroke-width="3" stroke-linecap="round"/>
    </svg>''',

    'dollar': '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dollar icon">
        <circle cx="30" cy="30" r="25" fill="#10b981" stroke="#059669" stroke-width="2"/>
        <text x="30" y="42" font-size="30" font-weight="bold" fill="#fff" text-anchor="middle" font-family="Arial">$</text>
    </svg>'''
}

def add_icons_to_blog(file_path):
    """Add relevant SVG icons to blog posts"""
    print(f"\nProcessing blog: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    content_div = soup.find('div', class_='blog-content')

    if not content_div:
        print(f"  [WARN] No content div found")
        return False

    # Check if already has icons
    if soup.find('svg'):
        print(f"  [SKIP] Already has SVG icons")
        return False

    # Add icon at the top (after h1)
    h1 = content_div.find('h1')
    if h1:
        # Determine which appliance icon to use
        title_lower = h1.text.lower()
        icon_type = 'tools'
        if 'refrigerator' in title_lower or 'fridge' in title_lower:
            icon_type = 'refrigerator'
        elif 'washer' in title_lower or 'washing' in title_lower:
            icon_type = 'washer'
        elif 'dryer' in title_lower:
            icon_type = 'dryer'
        elif 'dishwasher' in title_lower:
            icon_type = 'dishwasher'
        elif 'oven' in title_lower:
            icon_type = 'oven'
        elif 'stove' in title_lower or 'cooktop' in title_lower:
            icon_type = 'stove'

        icon_html = f'<div style="text-align: center; margin: 30px 0;">{SVG_ICONS[icon_type]}</div>'
        h1.insert_after(BeautifulSoup(icon_html, 'html.parser'))

    # Add checkmark icons to "Why This Matters" section
    why_matters = content_div.find('h2', string=re.compile(r'Why This Matters', re.I))
    if why_matters:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["checkmark"]}</div>'
        why_matters.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Add phone icon to CTA sections
    for cta in content_div.find_all('div', class_='cta-box'):
        h3 = cta.find('h3')
        if h3:
            icon_html = f'<div style="text-align: center; margin-bottom: 15px;">{SVG_ICONS["phone"]}</div>'
            h3.insert_before(BeautifulSoup(icon_html, 'html.parser'))

    # Add warning icon to tip boxes
    for tip in content_div.find_all('div', class_='tip-box'):
        strong = tip.find('strong')
        if strong and 'Pro Tip' in strong.text:
            icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["checkmark"]}</div>'
            strong.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Add dollar icon to cost sections
    cost_h2 = content_div.find('h2', string=re.compile(r'Cost', re.I))
    if cost_h2:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["dollar"]}</div>'
        cost_h2.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Save
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    # Count images
    img_count = len(soup.find_all(['img', 'svg']))
    print(f"  [OK] Added SVG icons - Total images: {img_count}")
    return True

def add_icons_to_service(file_path):
    """Add relevant SVG icons to service pages"""
    print(f"\nProcessing service: {file_path.name}")

    if file_path.name == 'index.html':
        print(f"  [SKIP] Index page")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Check if already has our SVG icons (with role="img")
    if soup.find('svg', role='img'):
        print(f"  [SKIP] Already has SVG icons")
        return False

    # Find body instead of main
    body = soup.find('body')
    if not body:
        print(f"  [WARN] No body element found")
        return False

    # Find first h1 to work from
    h1 = body.find('h1')
    if not h1:
        print(f"  [WARN] No h1 found")
        return False

    # Add relevant appliance icon at top (after h1)
    title_lower = h1.text.lower()
    icon_type = 'tools'
    if 'refrigerator' in title_lower:
        icon_type = 'refrigerator'
    elif 'washer' in title_lower:
        icon_type = 'washer'
    elif 'dryer' in title_lower:
        icon_type = 'dryer'
    elif 'dishwasher' in title_lower:
        icon_type = 'dishwasher'
    elif 'oven' in title_lower:
        icon_type = 'oven'
    elif 'stove' in title_lower or 'cooktop' in title_lower:
        icon_type = 'stove'

    icon_html = f'<div style="text-align: center; margin: 30px 0;">{SVG_ICONS[icon_type]}</div>'
    h1.insert_after(BeautifulSoup(icon_html, 'html.parser'))

    # Add checkmark to "Why Choose" section
    why_choose = body.find('h2', string=re.compile(r'Why Choose', re.I))
    if why_choose:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["checkmark"]}</div>'
        why_choose.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Add phone icon to emergency sections
    for h2 in body.find_all('h2'):
        if 'Emergency' in h2.text:
            icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["warning"]}</div>'
            h2.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Add calendar to schedule section
    schedule = body.find('h2', string=re.compile(r'Schedule|Book', re.I))
    if schedule:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["calendar"]}</div>'
        schedule.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Save
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    img_count = len(soup.find_all(['img', 'svg']))
    print(f"  [OK] Added SVG icons - Total images: {img_count}")
    return True

def add_icons_to_location(file_path):
    """Add relevant SVG icons to location pages"""
    print(f"\nProcessing location: {file_path.name}")

    if file_path.name == 'index.html':
        print(f"  [SKIP] Index page")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Check if already has our SVG icons (with role="img")
    if soup.find('svg', role='img'):
        print(f"  [SKIP] Already has SVG icons")
        return False

    # Find body instead of main
    body = soup.find('body')
    if not body:
        print(f"  [WARN] No body element found")
        return False

    # Find first h1 to work from
    h1 = body.find('h1')
    if not h1:
        print(f"  [WARN] No h1 found")
        return False

    # Add tools icon at top (after h1)
    icon_html = f'<div style="text-align: center; margin: 30px 0;">{SVG_ICONS["tools"]}</div>'
    h1.insert_after(BeautifulSoup(icon_html, 'html.parser'))

    # Add phone icon to contact sections
    for a in body.find_all('a', href=re.compile(r'tel:')):
        if 'style=' not in str(a):
            icon_html = f'<span style="display: inline-block; vertical-align: middle; margin-right: 5px;">{SVG_ICONS["phone"]}</span>'
            a.insert(0, BeautifulSoup(icon_html, 'html.parser'))
            break  # Only first phone link

    # Add checkmark to why choose section
    why_choose = body.find('h2', string=re.compile(r'Why', re.I))
    if why_choose:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["checkmark"]}</div>'
        why_choose.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Add calendar icon to Book/Schedule section
    book_section = body.find('h2', string=re.compile(r'Book.*Repair', re.I))
    if book_section:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["calendar"]}</div>'
        book_section.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Add dollar icon to Save/discount section
    save_section = body.find('h2', string=re.compile(r'Save.*\$', re.I))
    if save_section:
        icon_html = f'<div style="display: inline-block; vertical-align: middle; margin-right: 10px;">{SVG_ICONS["dollar"]}</div>'
        save_section.insert(0, BeautifulSoup(icon_html, 'html.parser'))

    # Save
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    img_count = len(soup.find_all(['img', 'svg']))
    print(f"  [OK] Added SVG icons - Total images: {img_count}")
    return True

def main():
    print("="*70)
    print("ADDING SVG ICONS TO ALL PAGES")
    print("="*70)

    # Process blogs
    print("\n--- BLOG POSTS ---")
    blog_dir = PROJECT_ROOT / "blog"
    blog_count = 0
    for blog_file in sorted(blog_dir.glob("*.html")):
        if add_icons_to_blog(blog_file):
            blog_count += 1

    # Process services
    print("\n--- SERVICE PAGES ---")
    services_dir = PROJECT_ROOT / "services"
    service_count = 0
    for service_file in sorted(services_dir.glob("*.html")):
        if add_icons_to_service(service_file):
            service_count += 1

    # Process locations
    print("\n--- LOCATION PAGES ---")
    locations_dir = PROJECT_ROOT / "locations"
    location_count = 0
    for location_file in sorted(locations_dir.glob("*.html")):
        if add_icons_to_location(location_file):
            location_count += 1

    print("\n" + "="*70)
    print(f"COMPLETE:")
    print(f"  Blog posts: {blog_count}")
    print(f"  Service pages: {service_count}")
    print(f"  Location pages: {location_count}")
    print(f"  Total: {blog_count + service_count + location_count}")
    print("="*70)
    print("\nNote: SVG elements have role='img' and aria-label for accessibility")
    print("Google will count these as images for SEO scoring")

if __name__ == "__main__":
    main()
