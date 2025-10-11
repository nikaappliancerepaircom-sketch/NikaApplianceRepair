#!/usr/bin/env python3
"""
Fix header/footer links that are not working
- Fix malformed HTML structure
- Add proper dropdown CSS
- Fix relative paths
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def fix_header_dropdown(soup, base_path=''):
    """Fix header dropdown structure"""
    nav = soup.find('nav', class_='main-nav')
    if not nav:
        return False

    # Find Areas dropdown
    has_dropdown_items = nav.find_all('li', class_='has-dropdown')

    for item in has_dropdown_items:
        link = item.find('a', href='#areas')
        if link:
            # Remove existing dropdown if malformed
            old_dropdown = item.find('ul', class_='dropdown-menu')
            if old_dropdown:
                old_dropdown.decompose()

            # Create properly formatted dropdown
            dropdown = soup.new_tag('ul', **{'class': 'dropdown-menu'})

            locations = [
                ('Ajax', 'ajax.html'),
                ('Aurora', 'aurora.html'),
                ('Barrie', 'barrie.html'),
                ('Bolton', 'bolton.html'),
                ('Brampton', 'brampton.html'),
                ('Burlington', 'burlington.html'),
                ('Etobicoke', 'etobicoke.html'),
                ('Markham', 'markham.html'),
            ]

            for name, url in locations:
                li = soup.new_tag('li')
                path = f'{base_path}/locations/{url}' if base_path else f'../locations/{url}'
                a = soup.new_tag('a', href=path)
                a.string = name
                li.append(a)
                dropdown.append(li)

            # Append dropdown to parent li
            item.append(dropdown)
            return True

    return False

def fix_footer_links(soup, base_path=''):
    """Fix footer service area links"""
    footer = soup.find('footer')
    if not footer:
        return False

    # Find Service Areas column
    columns = footer.find_all('div', class_='footer-column')

    for column in columns:
        h4 = column.find('h4')
        if h4 and 'Service Areas' in h4.get_text():
            # Clear old links
            ul = column.find('ul')
            if ul:
                ul.decompose()

            # Create new properly formatted list
            new_ul = soup.new_tag('ul')

            locations = [
                ('Toronto', 'toronto.html'),
                ('Mississauga', 'mississauga.html'),
                ('Brampton', 'brampton.html'),
                ('Vaughan', 'vaughan.html'),
                ('Markham', 'markham.html'),
                ('Richmond Hill', 'richmond-hill.html'),
                ('Oakville', 'oakville.html'),
                ('Burlington', 'burlington.html'),
            ]

            for name, url in locations:
                li = soup.new_tag('li')
                path = f'{base_path}/locations/{url}' if base_path else f'../locations/{url}'
                a = soup.new_tag('a', href=path)
                a.string = name
                li.append(a)
                new_ul.append(li)

            column.append(new_ul)
            return True

    return False

def add_dropdown_styles(soup):
    """Add dropdown hover styles to head if missing"""
    head = soup.find('head')
    if not head:
        return False

    # Check if styles already exist
    existing_styles = head.find_all('style')
    for style in existing_styles:
        if '.has-dropdown:hover' in style.get_text():
            return False

    # Add dropdown styles
    style_tag = soup.new_tag('style')
    style_tag.string = """
/* Dropdown Navigation Styles */
.has-dropdown {
    position: relative;
}

.dropdown-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    min-width: 200px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 8px;
    padding: 10px 0;
    z-index: 1000;
}

.has-dropdown:hover .dropdown-menu {
    display: block;
}

.dropdown-menu li {
    list-style: none;
    margin: 0;
}

.dropdown-menu li a {
    display: block;
    padding: 10px 20px;
    color: #333;
    text-decoration: none;
    transition: background 0.3s;
}

.dropdown-menu li a:hover {
    background: #f5f5f5;
    color: #d4a00c;
}

/* Mobile dropdown */
@media (max-width: 768px) {
    .dropdown-menu {
        position: static;
        display: none;
        box-shadow: none;
        background: rgba(0,0,0,0.05);
    }

    .has-dropdown.active .dropdown-menu {
        display: block;
    }
}
"""
    head.append(style_tag)
    return True

def process_file(file_path):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Determine base path
        base_path = ''
        if 'services' in str(file_path) or 'locations' in str(file_path) or 'blog' in str(file_path):
            base_path = '..'

        changed = False

        # Fix header dropdown
        if fix_header_dropdown(soup, base_path):
            changed = True

        # Fix footer links
        if fix_footer_links(soup, base_path):
            changed = True

        # Add dropdown styles
        if add_dropdown_styles(soup):
            changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True

        return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("FIXING HEADER/FOOTER LINKS")
    print("=" * 60)

    # Get all HTML files
    all_files = []
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    fixed = 0
    for file_path in all_files:
        if process_file(file_path):
            print(f"[FIXED] {file_path.name}")
            fixed += 1
        else:
            print(f"[OK] {file_path.name}")

    print("\n" + "=" * 60)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
