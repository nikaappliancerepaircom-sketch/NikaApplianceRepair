#!/usr/bin/env python3
"""
Fix all location and service pages to use ONLY unified header/footer includes.
Removes all hardcoded header/footer HTML, keeping only placeholder divs.
"""

import os
import re
import sys

# Configure UTF-8 for Windows console output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def remove_hardcoded_header_footer(file_path):
    """Remove hardcoded header and footer HTML from a file"""

    print(f"\n✓ Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_length = len(content)

    # Pattern 1: Remove hardcoded <header> tag and all its content
    # From <!-- Main Header --> or <header to </header>
    header_pattern = r'(<!--\s*Main Header\s*-->|<!--\s*Header\s*-->)?\s*<header[^>]*>.*?</header>'
    content = re.sub(header_pattern, '', content, flags=re.DOTALL)

    # Pattern 2: Remove mobile sticky bottom bar
    # From <!-- Mobile Sticky Bottom Bar --> to </div>
    mobile_bar_pattern = r'<!--\s*Mobile Sticky Bottom Bar\s*-->.*?<div class="mobile-sticky-bottom">.*?</div>\s*(?=<!--|\s*<section)'
    content = re.sub(mobile_bar_pattern, '', content, flags=re.DOTALL)

    # Pattern 3: Remove hardcoded footer HTML (but not footer placeholder)
    # Look for <footer> tags that are NOT placeholders
    footer_pattern = r'<!--\s*Footer\s*-->\s*<footer[^>]*>.*?</footer>'
    content = re.sub(footer_pattern, '', content, flags=re.DOTALL)

    # Pattern 4: Ensure header placeholder exists right after <body> and skip-to-content
    # Check if header-placeholder exists
    if '<div id="header-placeholder"></div>' not in content:
        # Add it after skip-to-content or after <body>
        if 'class="skip-to-content"' in content:
            content = re.sub(
                r'(<a [^>]*class="skip-to-content"[^>]*>.*?</a>)\s*',
                r'\1\n\n    <!-- Header Placeholder (loaded from /includes/header.html) -->\n    <div id="header-placeholder"></div>\n\n',
                content,
                flags=re.DOTALL
            )
        else:
            content = re.sub(
                r'(<body[^>]*>)\s*',
                r'\1\n    <!-- Header Placeholder (loaded from /includes/header.html) -->\n    <div id="header-placeholder"></div>\n\n',
                content
            )

    # Pattern 5: Ensure footer placeholder exists before closing </body>
    if '<div id="footer-placeholder"></div>' not in content:
        # Add it before JavaScript includes or before </body>
        if '<!-- JavaScript -->' in content or '<script' in content:
            content = re.sub(
                r'(\s*)(<!--\s*JavaScript\s*-->|<script)',
                r'\n    <!-- Footer Placeholder (loaded from /includes/footer.html) -->\n    <div id="footer-placeholder"></div>\n\n\1\2',
                content,
                count=1
            )
        else:
            content = re.sub(
                r'(</body>)',
                r'    <!-- Footer Placeholder (loaded from /includes/footer.html) -->\n    <div id="footer-placeholder"></div>\n\n\1',
                content
            )

    # Pattern 6: Ensure include-loader.js exists before </body>
    if '/includes/include-loader.js' not in content:
        content = re.sub(
            r'(</body>)',
            r'    <!-- Load Unified Header & Footer -->\n    <script src="/includes/include-loader.js"></script>\n</body>',
            content
        )

    new_length = len(content)
    removed = original_length - new_length

    # Write back the cleaned content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Removed {removed:,} characters of hardcoded header/footer HTML")

    return removed

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Location pages
    locations_dir = os.path.join(base_dir, 'locations')
    location_files = [
        'ajax.html', 'brampton.html', 'burlington.html', 'markham.html',
        'milton.html', 'mississauga.html', 'oakville.html', 'oshawa.html',
        'pickering.html', 'richmond-hill.html', 'toronto.html', 'vaughan.html'
    ]

    # Service pages
    services_dir = os.path.join(base_dir, 'services')
    service_files = [
        'dishwasher-repair.html', 'dryer-repair.html', 'freezer-repair.html',
        'microwave-repair.html', 'oven-repair.html', 'range-repair.html',
        'refrigerator-repair.html', 'stove-repair.html', 'washer-repair.html'
    ]

    total_removed = 0
    files_processed = 0

    print("\n" + "=" * 60)
    print("FIXING UNIFIED HEADER/FOOTER INCLUDES")
    print("=" * 60)

    print("\n📍 Processing Location Pages...")
    for filename in location_files:
        file_path = os.path.join(locations_dir, filename)
        if os.path.exists(file_path):
            removed = remove_hardcoded_header_footer(file_path)
            total_removed += removed
            files_processed += 1
        else:
            print(f"  ⚠ File not found: {filename}")

    print("\n🔧 Processing Service Pages...")
    for filename in service_files:
        file_path = os.path.join(services_dir, filename)
        if os.path.exists(file_path):
            removed = remove_hardcoded_header_footer(file_path)
            total_removed += removed
            files_processed += 1
        else:
            print(f"  ⚠ File not found: {filename}")

    print("\n" + "=" * 60)
    print(f"✅ COMPLETE!")
    print(f"   Files processed: {files_processed}")
    print(f"   Total HTML removed: {total_removed:,} characters")
    print(f"   All pages now use unified /includes/ system")
    print("=" * 60)

if __name__ == '__main__':
    main()
