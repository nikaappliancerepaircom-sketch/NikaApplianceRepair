#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert global header and footer into brand pages."""

import os
import sys
import glob
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_header_from_homepage():
    """Extract complete header section from homepage."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header (from <header to end of header styles)
    pattern = r'(<header class="site-header".*?</style>)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("ERROR: Could not find header section in homepage")
        return None

    header = match.group(1)
    print(f"✓ Extracted header: {len(header)} characters")
    return header

def extract_footer_from_homepage():
    """Extract complete footer section from homepage."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract footer (from <footer to </footer>)
    pattern = r'(<footer class="seo-footer-premium".*?</footer>)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("ERROR: Could not find footer section in homepage")
        return None

    footer = match.group(1)
    print(f"✓ Extracted footer: {len(footer)} characters")
    return footer

def insert_header_footer(file_path, global_header, global_footer):
    """Insert global header and footer into a brand page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix relative links for brand pages (../)
        brand_header = global_header.replace('href="/', 'href="../')
        brand_header = brand_header.replace('action="/', 'action="../')

        brand_footer = global_footer.replace('href="/', 'href="../')
        brand_footer = brand_footer.replace('action="/', 'action="../')

        # Insert header after <body> tag
        body_pattern = r'(<body[^>]*>)'
        if re.search(body_pattern, content):
            content = re.sub(body_pattern, r'\1\n\n    ' + brand_header + '\n', content)
        else:
            print(f"  WARNING: Could not find <body> tag in {os.path.basename(file_path)}")

        # Insert footer before </body> tag
        if '</body>' in content:
            content = content.replace('</body>', '\n    ' + brand_footer + '\n\n</body>')
        else:
            print(f"  WARNING: Could not find </body> tag in {os.path.basename(file_path)}")

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Inserted: {os.path.basename(file_path)}")
            return True
        else:
            print(f"- No changes: {os.path.basename(file_path)}")
            return False

    except Exception as e:
        print(f"✗ Error: {file_path}: {e}")
        return False

def main():
    """Main function."""
    print("Inserting global header and footer into brand pages...\n")

    # Extract header and footer from homepage
    global_header = extract_header_from_homepage()
    global_footer = extract_footer_from_homepage()

    if not global_header or not global_footer:
        print("\nERROR: Failed to extract header or footer from homepage")
        return

    print(f"\n{'='*60}")

    # Get all brand pages
    brand_files = glob.glob('brands/*-appliance-repair-toronto.html')

    if not brand_files:
        print("ERROR: No brand pages found")
        return

    print(f"Found {len(brand_files)} brand pages\n")

    updated_count = 0
    for file_path in sorted(brand_files):
        if insert_header_footer(file_path, global_header, global_footer):
            updated_count += 1

    print(f"\n{'='*60}")
    print(f"Inserted header/footer into {updated_count}/{len(brand_files)} pages")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
