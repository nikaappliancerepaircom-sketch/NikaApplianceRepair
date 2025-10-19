#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add global header and footer to 4 location pages missing them."""

import os
import sys
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_header_footer():
    """Extract header and footer from index.html."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header
    header_pattern = r'(<header class="site-header".*?</style>)'
    header_match = re.search(header_pattern, content, re.DOTALL)

    if not header_match:
        print("ERROR: Could not find header in index.html")
        return None, None

    header = header_match.group(1)
    print(f"✓ Extracted header: {len(header)} characters")

    # Extract footer
    footer_pattern = r'(<footer class="seo-footer-premium".*?</footer>)'
    footer_match = re.search(footer_pattern, content, re.DOTALL)

    if not footer_match:
        print("ERROR: Could not find footer in index.html")
        return None, None

    footer = footer_match.group(1)
    print(f"✓ Extracted footer: {len(footer)} characters")

    return header, footer

def add_header_footer_to_page(file_path, global_header, global_footer):
    """Add header and footer to a location page."""
    print(f"\nProcessing: {os.path.basename(file_path)}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix paths for location subfolder
    location_header = global_header.replace('href="/', 'href="../')
    location_header = location_header.replace('action="/', 'action="../')
    location_header = location_header.replace('src="/', 'src="../')

    location_footer = global_footer.replace('href="/', 'href="../')
    location_footer = location_footer.replace('action="/', 'action="../')
    location_footer = location_footer.replace('src="/', 'src="../')

    # Remove existing header if present
    header_pattern = r'<header class="site-header".*?</header>\s*'
    content = re.sub(header_pattern, '', content, flags=re.DOTALL)

    # Remove existing footer if present
    footer_pattern = r'<footer class="seo-footer-premium".*?</footer>\s*'
    content = re.sub(footer_pattern, '', content, flags=re.DOTALL)

    # Insert header after <body>
    body_pattern = r'(<body[^>]*>)'
    if re.search(body_pattern, content):
        content = re.sub(body_pattern, r'\1\n\n    ' + location_header + '\n', content)
        print("  ✓ Header inserted")
    else:
        print("  ✗ ERROR: Could not find <body> tag")
        return False

    # Insert footer before </body>
    if '</body>' in content:
        content = content.replace('</body>', '\n    ' + location_footer + '\n\n</body>')
        print("  ✓ Footer inserted")
    else:
        print("  ✗ ERROR: Could not find </body> tag")
        return False

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated: {os.path.basename(file_path)}")
        return True
    else:
        print(f"  - No changes needed")
        return False

def main():
    """Main function."""
    print("="*60)
    print("Adding Global Header/Footer to 4 Location Pages")
    print("="*60)
    print()

    # Extract header and footer
    global_header, global_footer = extract_header_footer()

    if not global_header or not global_footer:
        print("\nERROR: Failed to extract header/footer")
        return

    print(f"\n{'='*60}\n")

    # Pages missing header/footer
    pages = [
        'locations/caledon.html',
        'locations/clarington.html',
        'locations/newmarket.html',
        'locations/whitby.html',
    ]

    updated_count = 0
    for file_path in pages:
        if os.path.exists(file_path):
            if add_header_footer_to_page(file_path, global_header, global_footer):
                updated_count += 1
        else:
            print(f"\n✗ ERROR: {file_path} not found")

    print(f"\n{'='*60}")
    print(f"✓ Added header/footer to {updated_count}/{len(pages)} pages")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
