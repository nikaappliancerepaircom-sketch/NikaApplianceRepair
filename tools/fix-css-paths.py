#!/usr/bin/env python3
"""
Fix CSS paths in service and location pages
Changes href="css/ to href="../css/ for pages in subdirectories
"""

import os
from pathlib import Path

def fix_css_paths(file_path):
    """Fix CSS paths in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has correct paths
        if 'href="../css/' in content:
            print(f"[OK] {file_path.name} - already correct")
            return False

        # Replace incorrect paths
        original = content
        content = content.replace('href="css/', 'href="../css/')

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[FIXED] {file_path.name} - fixed CSS paths")
            return True
        else:
            print(f"[SKIP] {file_path.name} - no changes needed")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name} - Error: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("FIXING CSS PATHS IN SUBDIRECTORY PAGES")
    print("=" * 60)

    # Fix service pages
    print("\nSERVICE PAGES:")
    services_dir = base_dir / 'services'
    service_files = sorted(services_dir.glob('*.html'))

    service_fixed = 0
    for file_path in service_files:
        if fix_css_paths(file_path):
            service_fixed += 1

    print(f"\nFixed {service_fixed}/{len(service_files)} service pages")

    # Fix location pages
    print("\nLOCATION PAGES:")
    locations_dir = base_dir / 'locations'
    location_files = sorted(locations_dir.glob('*.html'))

    location_fixed = 0
    for file_path in location_files:
        if fix_css_paths(file_path):
            location_fixed += 1

    print(f"\nFixed {location_fixed}/{len(location_files)} location pages")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Services: {service_fixed}/{len(service_files)} fixed")
    print(f"  Locations: {location_fixed}/{len(location_files)} fixed")
    print(f"  Total: {service_fixed + location_fixed}/{len(service_files) + len(location_files)} fixed")
    print("=" * 60)

if __name__ == '__main__':
    main()
