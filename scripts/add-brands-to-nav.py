#!/usr/bin/env python3
"""
Add 'Brands' link to navigation menu across all pages
"""
import os
import re
from pathlib import Path

def add_brands_to_nav(filepath, relative_path=''):
    """Add Brands link to navigation menu"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if Brands link already exists
    if 'href="brands"' in content or 'href="/brands"' in content or 'href="../brands"' in content:
        print(f"[OK] {os.path.basename(filepath)} - Already has Brands link")
        return False

    # Determine the correct path prefix based on file location
    if relative_path:
        brands_path = f'"{relative_path}brands"'
    else:
        brands_path = '"brands"'

    # Pattern to find the nav-list and add Brands after Locations
    # Looking for: <li><a href="locations" class="nav-link">Locations</a></li>
    pattern = r'(<li><a href="[./]*locations"[^>]*>Locations</a></li>)'

    # Replacement: Add Brands link after Locations
    replacement = rf'''\1
                    <li><a href={brands_path} class="nav-link">Brands</a></li>'''

    # Replace
    new_content = re.sub(pattern, replacement, content)

    if new_content == content:
        print(f"[ERROR] {os.path.basename(filepath)} - Pattern not found!")
        return False

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] {os.path.basename(filepath)} - Added Brands link")
    return True

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent

    print("Adding 'Brands' link to navigation menu across all pages...\n")

    updated_count = 0

    # Root pages (no prefix needed)
    root_pages = ['index.html', 'services.html', 'locations.html', 'about.html']
    print("=== ROOT PAGES ===")
    for page in root_pages:
        filepath = base_dir / page
        if filepath.exists():
            if add_brands_to_nav(filepath, ''):
                updated_count += 1
        else:
            print(f"[SKIP] {page} - File not found")

    # Location pages (need ../ prefix)
    print("\n=== LOCATION PAGES ===")
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        for filepath in locations_dir.glob('*.html'):
            if add_brands_to_nav(filepath, '../'):
                updated_count += 1

    # Brand pages (need ../ prefix)
    print("\n=== BRAND PAGES ===")
    brands_dir = base_dir / 'brands'
    if brands_dir.exists():
        for filepath in brands_dir.glob('*.html'):
            if add_brands_to_nav(filepath, '../'):
                updated_count += 1

    # Service pages (need ../ prefix)
    print("\n=== SERVICE PAGES ===")
    services_dir = base_dir / 'services'
    if services_dir.exists():
        for filepath in services_dir.glob('*.html'):
            if add_brands_to_nav(filepath, '../'):
                updated_count += 1

    print(f"\n{'='*50}")
    print(f"TOTAL: {updated_count} pages updated successfully!")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
