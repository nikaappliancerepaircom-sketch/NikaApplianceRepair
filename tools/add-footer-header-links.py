#!/usr/bin/env python3
"""
Add internal links to footer and header on all pages
Adds locations dropdown in header and popular locations in footer
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup

# Popular locations for footer
POPULAR_LOCATIONS = [
    ('Toronto', '/locations/toronto.html'),
    ('Mississauga', '/locations/mississauga.html'),
    ('Brampton', '/locations/brampton.html'),
    ('Vaughan', '/locations/vaughan.html'),
    ('Markham', '/locations/markham.html'),
    ('Richmond Hill', '/locations/richmond-hill.html'),
    ('Oakville', '/locations/oakville.html'),
    ('Burlington', '/locations/burlington.html'),
]

# All locations for header dropdown
ALL_LOCATIONS = [
    ('Ajax', '/locations/ajax.html'),
    ('Aurora', '/locations/aurora.html'),
    ('Barrie', '/locations/barrie.html'),
    ('Bolton', '/locations/bolton.html'),
    ('Brampton', '/locations/brampton.html'),
    ('Burlington', '/locations/burlington.html'),
    ('Etobicoke', '/locations/etobicoke.html'),
    ('Markham', '/locations/markham.html'),
    ('Mississauga', '/locations/mississauga.html'),
    ('North York', '/locations/north-york.html'),
    ('Oakville', '/locations/oakville.html'),
    ('Richmond Hill', '/locations/richmond-hill.html'),
    ('Scarborough', '/locations/scarborough.html'),
    ('Toronto', '/locations/toronto.html'),
    ('Vaughan', '/locations/vaughan.html'),
]

HEADER_LOCATIONS_DROPDOWN = '''
                        <li class="has-dropdown">
                            <a href="#areas">Areas</a>
                            <ul class="dropdown-menu">
                                <li><a href="/locations/toronto.html">Toronto</a></li>
                                <li><a href="/locations/mississauga.html">Mississauga</a></li>
                                <li><a href="/locations/brampton.html">Brampton</a></li>
                                <li><a href="/locations/vaughan.html">Vaughan</a></li>
                                <li><a href="/locations/markham.html">Markham</a></li>
                                <li><a href="/locations/richmond-hill.html">Richmond Hill</a></li>
                                <li><a href="/locations/oakville.html">Oakville</a></li>
                                <li><a href="/locations/north-york.html">North York</a></li>
                            </ul>
                        </li>'''

def add_locations_to_footer(soup, base_path=''):
    """Add popular locations section to footer"""
    footer = soup.find('footer', class_='main-footer')
    if not footer:
        return False

    # Check if locations column already exists
    footer_columns = footer.find_all('div', class_='footer-column')

    # Find the Services column
    services_column = None
    for col in footer_columns:
        h4 = col.find('h4')
        if h4 and 'Services' in h4.text:
            services_column = col
            break

    if not services_column:
        return False

    # Check if locations column already exists
    for col in footer_columns:
        h4 = col.find('h4')
        if h4 and 'Service Areas' in h4.text:
            return False  # Already has locations

    # Create locations column
    locations_html = f'''<div class="footer-column">
                <h4>Service Areas</h4>
                <ul>'''

    for name, url in POPULAR_LOCATIONS:
        # Adjust path based on base_path
        if base_path:
            url = base_path + url
        locations_html += f'\n                    <li><a href="{url}">{name}</a></li>'

    locations_html += '''
                </ul>
            </div>'''

    # Insert after services column
    locations_col = BeautifulSoup(locations_html, 'html.parser')
    services_column.insert_after(locations_col)

    return True

def add_locations_to_header(soup, base_path=''):
    """Add locations dropdown to header navigation"""
    nav = soup.find('nav', class_='main-nav')
    if not nav:
        return False

    nav_ul = nav.find('ul')
    if not nav_ul:
        return False

    # Check if locations dropdown already exists
    for li in nav_ul.find_all('li'):
        a_tag = li.find('a')
        if a_tag and ('Areas' in a_tag.text or 'Locations' in a_tag.text):
            # Already has dropdown, check if it's populated
            dropdown = li.find('ul', class_='dropdown-menu')
            if dropdown and len(dropdown.find_all('li')) > 0:
                return False  # Already populated

    # Find the Areas or Locations link
    areas_li = None
    for li in nav_ul.find_all('li'):
        a_tag = li.find('a')
        if a_tag:
            href = a_tag.get('href', '')
            if href == '#areas' or 'locations' in href.lower():
                areas_li = li
                break

    if not areas_li:
        return False

    # Add has-dropdown class
    if 'has-dropdown' not in areas_li.get('class', []):
        classes = areas_li.get('class', [])
        classes.append('has-dropdown')
        areas_li['class'] = classes

    # Create dropdown menu
    dropdown_html = '<ul class="dropdown-menu">\n'
    for name, url in ALL_LOCATIONS[:8]:  # Top 8 locations
        if base_path:
            url = base_path + url
        dropdown_html += f'                                <li><a href="{url}">{name}</a></li>\n'
    dropdown_html += '                            </ul>'

    # Remove existing dropdown if any
    existing_dropdown = areas_li.find('ul', class_='dropdown-menu')
    if existing_dropdown:
        existing_dropdown.decompose()

    # Add new dropdown
    dropdown = BeautifulSoup(dropdown_html, 'html.parser')
    areas_li.append(dropdown)

    return True

def process_file(file_path, base_path=''):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        footer_added = add_locations_to_footer(soup, base_path)
        header_added = add_locations_to_header(soup, base_path)

        if footer_added or header_added:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            changes = []
            if footer_added:
                changes.append('footer')
            if header_added:
                changes.append('header')

            print(f"[UPDATED] {file_path.name} - added to {', '.join(changes)}")
            return True
        else:
            print(f"[SKIP] {file_path.name} - already has links")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name} - {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("ADDING INTERNAL LINKS TO FOOTER & HEADER")
    print("=" * 60)

    # Process index.html
    print("\nMAIN PAGE:")
    index_file = base_dir / 'index.html'
    if index_file.exists():
        process_file(index_file)

    # Process service pages
    print("\nSERVICE PAGES:")
    services_dir = base_dir / 'services'
    service_files = sorted(services_dir.glob('*.html'))

    service_updated = 0
    for file_path in service_files:
        if process_file(file_path, base_path='..'):
            service_updated += 1

    # Process location pages
    print("\nLOCATION PAGES:")
    locations_dir = base_dir / 'locations'
    location_files = sorted(locations_dir.glob('*.html'))

    location_updated = 0
    for file_path in location_files:
        if process_file(file_path, base_path='..'):
            location_updated += 1

    # Process blog pages
    print("\nBLOG PAGES:")
    blog_dir = base_dir / 'blog'
    blog_files = sorted(blog_dir.glob('*.html'))

    blog_updated = 0
    for file_path in blog_files:
        if process_file(file_path, base_path='..'):
            blog_updated += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Services: {service_updated}/{len(service_files)} updated")
    print(f"  Locations: {location_updated}/{len(location_files)} updated")
    print(f"  Blogs: {blog_updated}/{len(blog_files)} updated")
    print(f"  Total: {service_updated + location_updated + blog_updated} pages updated")
    print("=" * 60)

if __name__ == '__main__':
    main()
