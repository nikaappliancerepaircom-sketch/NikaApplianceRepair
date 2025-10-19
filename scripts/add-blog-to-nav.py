#!/usr/bin/env python3
"""
Add 'Blog' link to navigation menu across all pages
"""
import os
import re
from pathlib import Path

def add_blog_to_nav(filepath, relative_path=''):
    """Add Blog link to navigation menu"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if Blog link already exists
    if 'href="blog"' in content or 'href="/blog"' in content or 'href="../blog"' in content:
        print(f"[SKIP] {filepath.name} - Already has Blog link")
        return False

    # Determine the correct path prefix based on file location
    if relative_path:
        blog_path = f'"{relative_path}blog"'
    else:
        blog_path = '"blog"'

    # Pattern to find the nav-list and add Blog after Brands
    # Looking for: <li><a href="brands" class="nav-link">Brands</a></li>
    pattern = r'(<li><a href="[./]*brands"[^>]*>Brands</a></li>)'

    # Replacement: Add Blog link after Brands
    replacement = rf'''\1
                    <li><a href={blog_path} class="nav-link">Blog</a></li>'''

    # Replace
    new_content = re.sub(pattern, replacement, content)

    if new_content == content:
        print(f"[ERROR] {filepath.name} - Pattern not found!")
        return False

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] {filepath.name} - Added Blog link")
    return True

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent

    print("="*70)
    print("Adding 'Blog' link to navigation menu across all pages")
    print("="*70)
    print()

    updated_count = 0

    # Root pages (no prefix needed)
    root_pages = ['index.html', 'services.html', 'locations.html', 'brands.html', 'about.html']
    print("=== ROOT PAGES ===")
    for page in root_pages:
        filepath = base_dir / page
        if filepath.exists():
            if add_blog_to_nav(filepath, ''):
                updated_count += 1
        else:
            print(f"[SKIP] {page} - File not found")

    # Location pages (need ../ prefix)
    print("\n=== LOCATION PAGES ===")
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        for filepath in sorted(locations_dir.glob('*.html')):
            if add_blog_to_nav(filepath, '../'):
                updated_count += 1

    # Brand pages (need ../ prefix)
    print("\n=== BRAND PAGES ===")
    brands_dir = base_dir / 'brands'
    if brands_dir.exists():
        for filepath in sorted(brands_dir.glob('*.html')):
            if add_blog_to_nav(filepath, '../'):
                updated_count += 1

    # Service pages (need ../ prefix)
    print("\n=== SERVICE PAGES ===")
    services_dir = base_dir / 'services'
    if services_dir.exists():
        for filepath in sorted(services_dir.glob('*.html')):
            if add_blog_to_nav(filepath, '../'):
                updated_count += 1

    print()
    print("="*70)
    print(f"COMPLETED: {updated_count} pages updated successfully!")
    print("="*70)

if __name__ == '__main__':
    main()
