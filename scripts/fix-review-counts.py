#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix review counts from 520+ to 5,200+ in header and footer across all location pages."""

import os
import sys
import glob

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fix_review_counts(file_path):
    """Fix review counts in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix header review count
        content = content.replace('(520+)', '(5,200+)')
        content = content.replace('>520+<', '>5,200+<')

        # Fix footer review count
        content = content.replace('<span>520+ Reviews</span>', '<span>5,200+ Reviews</span>')

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {os.path.basename(file_path)}")
            return True
        else:
            print(f"- Skipped (already correct): {os.path.basename(file_path)}")
            return False
    except Exception as e:
        print(f"✗ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix review counts in all location pages."""
    locations_dir = 'locations'

    if not os.path.exists(locations_dir):
        print(f"Error: Directory '{locations_dir}' not found")
        return

    # Get all HTML files in locations directory
    html_files = glob.glob(os.path.join(locations_dir, '*.html'))

    print(f"Found {len(html_files)} location pages\n")

    fixed_count = 0
    for file_path in sorted(html_files):
        if fix_review_counts(file_path):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count}/{len(html_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
