#!/usr/bin/env python3
"""
Add responsive typography CSS to all pages
Adds link to responsive-typography.css
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup

def add_typography_css(file_path, css_path):
    """Add responsive typography CSS link to head"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has responsive typography
        if 'responsive-typography.css' in content:
            return False

        soup = BeautifulSoup(content, 'html.parser')
        head = soup.find('head')

        if not head:
            return False

        # Create link tag
        link_tag = soup.new_tag('link', rel='stylesheet', href=css_path)

        # Add after other CSS files
        last_css = None
        for link in head.find_all('link', rel='stylesheet'):
            last_css = link

        if last_css:
            last_css.insert_after(link_tag)
        else:
            head.append(link_tag)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        return True

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("ADDING RESPONSIVE TYPOGRAPHY CSS")
    print("=" * 60)

    # Process all pages
    pages = []

    # Main
    pages.append((base_dir / 'index.html', 'css/responsive-typography.css'))

    # Services
    services_dir = base_dir / 'services'
    for f in services_dir.glob('*.html'):
        if f.name != 'index.html':
            pages.append((f, '../css/responsive-typography.css'))

    # Locations
    locations_dir = base_dir / 'locations'
    for f in locations_dir.glob('*.html'):
        if f.name != 'index.html':
            pages.append((f, '../css/responsive-typography.css'))

    # Blogs
    blog_dir = base_dir / 'blog'
    for f in blog_dir.glob('*.html'):
        if f.name != 'index.html':
            pages.append((f, '../css/responsive-typography.css'))

    added = 0
    for file_path, css_path in pages:
        if add_typography_css(file_path, css_path):
            print(f"[ADDED] {file_path.name}")
            added += 1

    print("\n" + "=" * 60)
    print(f"ADDED: {added}/{len(pages)} pages updated")
    print("=" * 60)

if __name__ == '__main__':
    main()
