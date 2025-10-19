#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove header and footer from brand pages."""

import os
import sys
import glob
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def remove_header_footer(file_path):
    """Remove header and footer from a brand page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove header (from <header to </header>)
        header_pattern = r'<header class="site-header".*?</header>\s*'
        content = re.sub(header_pattern, '', content, flags=re.DOTALL)

        # Remove footer
        footer_pattern = r'<footer class="seo-footer-premium".*?</footer>\s*'
        content = re.sub(footer_pattern, '', content, flags=re.DOTALL)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Removed header/footer: {os.path.basename(file_path)}")
            return True
        else:
            print(f"- No header/footer found: {os.path.basename(file_path)}")
            return False

    except Exception as e:
        print(f"✗ Error: {file_path}: {e}")
        return False

def main():
    """Main function."""
    print("Removing header and footer from brand pages...\n")

    # Get all brand pages
    brand_files = glob.glob('brands/*-appliance-repair-toronto.html')

    if not brand_files:
        print("ERROR: No brand pages found")
        return

    print(f"Found {len(brand_files)} brand pages\n")

    removed_count = 0
    for file_path in sorted(brand_files):
        if remove_header_footer(file_path):
            removed_count += 1

    print(f"\n{'='*60}")
    print(f"Removed header/footer from {removed_count}/{len(brand_files)} pages")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
