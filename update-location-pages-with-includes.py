#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update all location pages to use unified header/footer includes system
"""

import os
import re
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# List of location pages to update (excluding mississauga which is already done)
LOCATION_PAGES = [
    'ajax.html',
    'brampton.html',
    'burlington.html',
    'markham.html',
    'milton.html',
    'oakville.html',
    'oshawa.html',
    'pickering.html',
    'richmond-hill.html',
    'toronto.html',
    'vaughan.html'
]

def update_location_page(file_path):
    """Update a single location page with includes system"""
    print(f"\nUpdating: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Step 1: Add header-styles.css link before </head>
    if '/includes/header-styles.css' not in content:
        content = re.sub(
            r'(    }</script>\n)(</head>)',
            r'\1\n    <!-- Unified Header Styles -->\n    <link rel="stylesheet" href="/includes/header-styles.css">\n\2',
            content
        )
        print("  ✓ Added header-styles.css link")
    else:
        print("  ⊘ Header styles already added")

    # Step 2: Replace header section with placeholder
    # Match from "<!-- Header -->" or "<!-- Urgency Banner" to end of mobile-sticky-bottom div
    header_pattern = r'(    <!-- Skip to main content.*?\n\n)    <!-- (?:Header|Urgency Banner).*?</div>\n\n'

    if '<div id="header-placeholder"></div>' not in content:
        replacement = r'\1    <!-- Header Placeholder (loaded from /includes/header.html) -->\n    <div id="header-placeholder"></div>\n\n'
        content = re.sub(header_pattern, replacement, content, flags=re.DOTALL)
        print("  ✓ Replaced header with placeholder")
    else:
        print("  ⊘ Header placeholder already exists")

    # Step 3: Replace footer section with placeholder
    footer_pattern = r'    <!-- Footer -->\n    <footer class="main-footer">.*?</footer>\n\n(?:    <!-- Mobile Sticky CTA Button -->.*?</div>\n\n)?'

    if '<div id="footer-placeholder"></div>' not in content:
        replacement = r'    <!-- Footer Placeholder (loaded from /includes/footer.html) -->\n    <div id="footer-placeholder"></div>\n\n'
        content = re.sub(footer_pattern, replacement, content, flags=re.DOTALL)
        print("  ✓ Replaced footer with placeholder")
    else:
        print("  ⊘ Footer placeholder already exists")

    # Step 4: Remove old urgency banner script (between last form-validation.js and </body>)
    urgency_script_pattern = r'(<script src="\.\.\/js\/form-validation\.js" defer></script>\n)    <script>.*?urgencyBannerClosed.*?</script>\n(</body>)'

    if 'urgencyBannerClosed' in content and 'include-loader.js' not in content:
        content = re.sub(urgency_script_pattern, r'\1\2', content, flags=re.DOTALL)
        print("  ✓ Removed old urgency banner script")

    # Step 5: Add include-loader.js before </body>
    if '/includes/include-loader.js' not in content:
        content = re.sub(
            r'(<script src="\.\.\/js\/form-validation\.js" defer></script>\n)(</body>)',
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
    """Update all location pages"""
    print("=" * 60)
    print("UPDATING LOCATION PAGES WITH UNIFIED INCLUDES")
    print("=" * 60)

    locations_dir = 'locations'
    updated_count = 0
    skipped_count = 0

    for page in LOCATION_PAGES:
        file_path = os.path.join(locations_dir, page)

        if not os.path.exists(file_path):
            print(f"\n⚠️  File not found: {file_path}")
            continue

        try:
            if update_location_page(file_path):
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
