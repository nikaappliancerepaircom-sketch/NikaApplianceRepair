#!/usr/bin/env python3
"""
Fix dropdown CSS - add link to external CSS file
Remove inline styles, use dropdown-styles.css instead
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def fix_dropdown_css(file_path):
    """Add dropdown-styles.css link and remove inline styles"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has dropdown-styles.css
        if 'dropdown-styles.css' in content:
            print(f"[SKIP] {file_path.name}: Already has dropdown-styles.css link")
            return False

        soup = BeautifulSoup(content, 'html.parser')
        head = soup.find('head')

        if not head:
            print(f"[ERROR] {file_path.name}: No <head> found")
            return False

        # Determine CSS path
        if str(file_path.name) == 'index.html' and 'services' not in str(file_path) and 'locations' not in str(file_path) and 'blog' not in str(file_path):
            css_path = 'css/dropdown-styles.css'
        else:
            css_path = '../css/dropdown-styles.css'

        # Create link tag
        link = soup.new_tag('link', rel='stylesheet', href=css_path)

        # Find last CSS link and insert after it
        css_links = head.find_all('link', rel='stylesheet')
        if css_links:
            css_links[-1].insert_after(link)
        else:
            head.append(link)

        # Remove inline dropdown styles if they exist
        for style_tag in head.find_all('style'):
            style_text = style_tag.get_text()
            if '.has-dropdown:hover' in style_text or 'Dropdown Navigation Styles' in style_text:
                style_tag.decompose()

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"[FIXED] {file_path.name}")
        return True

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("FIXING DROPDOWN CSS LINKS")
    print("=" * 60)

    # Get all HTML files
    all_files = []
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    fixed = 0
    for file_path in all_files:
        if fix_dropdown_css(file_path):
            fixed += 1

    print("\n" + "=" * 60)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 60)
    print("\nExternal CSS file created: css/dropdown-styles.css")
    print("This fixes Playwright visibility issues")

if __name__ == '__main__':
    main()
