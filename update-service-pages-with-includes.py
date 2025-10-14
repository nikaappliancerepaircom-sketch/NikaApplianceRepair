#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update all service pages to use unified header/footer includes system
"""

import os
import re
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# List of service pages to update
SERVICE_PAGES = [
    'dishwasher-repair.html',
    'dryer-repair.html',
    'freezer-repair.html',
    'microwave-repair.html',
    'oven-repair.html',
    'range-repair.html',
    'refrigerator-repair.html',
    'stove-repair.html',
    'washer-repair.html'
]

def update_service_page(file_path):
    """Update a single service page with includes system"""
    print(f"\nUpdating: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Step 1: Add header-styles.css link before </head>
    if '/includes/header-styles.css' not in content:
        content = re.sub(
            r'(</script>\n)(</head>)',
            r'\1\n    <!-- Unified Header Styles -->\n    <link rel="stylesheet" href="/includes/header-styles.css">\n\2',
            content
        )
        print("  ✓ Added header-styles.css link")
    else:
        print("  ⊘ Header styles already added")

    # Step 2: Replace header section with placeholder
    # Service pages have simpler header structure
    header_pattern = r'    <!-- Header -->\n    <header class="main-header">.*?</header>\n\n'

    if '<div id="header-placeholder"></div>' not in content:
        replacement = r'    <!-- Header Placeholder (loaded from /includes/header.html) -->\n    <div id="header-placeholder"></div>\n\n'
        content = re.sub(header_pattern, replacement, content, flags=re.DOTALL)
        print("  ✓ Replaced header with placeholder")
    else:
        print("  ⊘ Header placeholder already exists")

    # Step 3: Replace footer section with placeholder
    footer_pattern = r'    <footer class="main-footer">.*?</footer>\n\n'

    if '<div id="footer-placeholder"></div>' not in content:
        replacement = r'    <!-- Footer Placeholder (loaded from /includes/footer.html) -->\n    <div id="footer-placeholder"></div>\n\n'
        content = re.sub(footer_pattern, replacement, content, flags=re.DOTALL)
        print("  ✓ Replaced footer with placeholder")
    else:
        print("  ⊘ Footer placeholder already exists")

    # Step 4: Add include-loader.js before </body>
    if '/includes/include-loader.js' not in content:
        content = re.sub(
            r'(</script>\n)(</body>)',
            r'\1\n    <!-- Load Unified Header & Footer -->\n    <script src="/includes/include-loader.js"></script>\n\2',
            content
        )
        print("  ✓ Added include-loader.js")
    else:
        print("  ⊘ Include loader already added")

    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Successfully updated {os.path.basename(file_path)}")
        return True
    else:
        print(f"  ⊘ No changes needed for {os.path.basename(file_path)}")
        return False

def main():
    """Update all service pages"""
    print("=" * 60)
    print("UPDATING SERVICE PAGES WITH UNIFIED INCLUDES")
    print("=" * 60)

    services_dir = 'services'
    updated_count = 0
    skipped_count = 0

    for page in SERVICE_PAGES:
        file_path = os.path.join(services_dir, page)

        if not os.path.exists(file_path):
            print(f"\n⚠️  File not found: {file_path}")
            continue

        try:
            if update_service_page(file_path):
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"\n❌ Error updating {page}: {e}")

    print("\n" + "=" * 60)
    print(f"✅ COMPLETED!")
    print(f"   - Updated: {updated_count} pages")
    print(f"   - Skipped: {skipped_count} pages (already updated)")
    print("=" * 60)

if __name__ == '__main__':
    main()
