#!/usr/bin/env python3
"""
Add lazy loading to all images
Adds loading="lazy" attribute to img tags
"""

import re
from pathlib import Path

def add_lazy_loading(content):
    """Add loading=lazy to img tags that don't have it"""

    # Find all img tags without loading attribute
    def replace_img(match):
        img_tag = match.group(0)

        # Skip if already has loading attribute
        if 'loading=' in img_tag:
            return img_tag

        # Add loading="lazy" before closing >
        if img_tag.endswith('/>'):
            return img_tag[:-2] + ' loading="lazy"/>'
        elif img_tag.endswith('>'):
            return img_tag[:-1] + ' loading="lazy">'
        return img_tag

    # Replace all img tags
    content = re.sub(r'<img[^>]*/?>', replace_img, content)

    return content

def process_file(file_path):
    """Process a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        content = add_lazy_loading(content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("ADDING LAZY LOADING TO IMAGES")
    print("=" * 60)

    # Get all HTML files
    all_files = []
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    updated = 0
    for file_path in all_files:
        if process_file(file_path):
            print(f"[UPDATED] {file_path.name}")
            updated += 1

    print("\n" + "=" * 60)
    print(f"UPDATED: {updated}/{len(all_files)} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
