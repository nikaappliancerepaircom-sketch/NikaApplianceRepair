#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix nested phone links in brand page headers."""

import os
import sys
import glob

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fix_phone_links(file_path):
    """Fix nested phone link in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix nested phone link in header
        content = content.replace(
            '<span class="cta-phone-number"><a href="tel:4377476737">(437) 747-6737</a></span>',
            '<span class="cta-phone-number">(437) 747-6737</span>'
        )

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
    """Fix phone links in all brand pages."""
    brands_dir = 'brands'

    if not os.path.exists(brands_dir):
        print(f"Error: Directory '{brands_dir}' not found")
        return

    # Get all HTML files in brands directory
    html_files = glob.glob(os.path.join(brands_dir, '*-appliance-repair-toronto.html'))

    print(f"Found {len(html_files)} brand pages\n")

    fixed_count = 0
    for file_path in sorted(html_files):
        if fix_phone_links(file_path):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count}/{len(html_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
