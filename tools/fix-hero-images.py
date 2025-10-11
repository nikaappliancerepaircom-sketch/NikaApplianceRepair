#!/usr/bin/env python3
"""
Fix hero image paths on service pages
Change: assets/images/ -> ../assets/images/
"""

from pathlib import Path
import re

def fix_image_paths(file_path):
    """Fix relative image paths"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix: src="assets/images/ -> src="../assets/images/
    content = re.sub(r'src="assets/images/', r'src="../assets/images/', content)

    # Fix: src='assets/images/ -> src='../assets/images/
    content = re.sub(r"src='assets/images/", r"src='../assets/images/", content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING HERO IMAGE PATHS")
    print("=" * 70)

    all_files = []

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        all_files.extend([f for f in services_dir.glob('*.html')])

    # Location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        all_files.extend([f for f in locations_dir.glob('*.html')])

    print(f"\nProcessing {len(all_files)} pages...\n")

    fixed = 0
    for file_path in all_files:
        if not file_path.exists():
            continue

        if fix_image_paths(file_path):
            print(f"[FIXED] {file_path.name}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
