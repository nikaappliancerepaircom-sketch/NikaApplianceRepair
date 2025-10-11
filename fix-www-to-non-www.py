#!/usr/bin/env python3
"""
Fix www to non-www URLs across all production files
Because Vercel redirects www -> https://nikaappliancerepair.com
"""

import os
import re
from pathlib import Path

# Files to update (production only, skip backups and tools)
FILES_TO_UPDATE = [
    'sitemap.xml',
    'robots.txt',
    'index.html',
    # Service pages
    'services/refrigerator-repair.html',
    'services/dishwasher-repair.html',
    'services/washer-repair.html',
    'services/dryer-repair.html',
    'services/freezer-repair.html',
    'services/stove-repair.html',
    'services/oven-repair.html',
    'services/range-repair.html',
    'services/microwave-repair.html',
    # Location pages (21 files)
    'locations/ajax.html',
    'locations/aurora.html',
    'locations/barrie.html',
    'locations/bolton.html',
    'locations/brampton.html',
    'locations/burlington.html',
    'locations/caledon.html',
    'locations/concord.html',
    'locations/east-gwillimbury.html',
    'locations/etobicoke.html',
    'locations/georgetown.html',
    'locations/king-city.html',
    'locations/maple.html',
    'locations/markham.html',
    'locations/milton.html',
    'locations/mississauga.html',
    'locations/newmarket.html',
    'locations/north-york.html',
    'locations/oakville.html',
    'locations/oshawa.html',
    'locations/pickering.html',
    'locations/richmond-hill.html',
    'locations/scarborough.html',
    'locations/stouffville.html',
    'locations/thornhill.html',
    'locations/toronto.html',
    'locations/uxbridge.html',
    'locations/vaughan.html',
    'locations/whitby.html',
    'locations/woodbridge.html',
]

def fix_www_in_file(filepath):
    """Replace www.nikaappliancerepair.com with nikaappliancerepair.com"""
    if not os.path.exists(filepath):
        print(f"⚠️  SKIP: {filepath} (file not found)")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count occurrences before
    before_count = content.count('www.nikaappliancerepair.com')

    if before_count == 0:
        print(f"✓ SKIP: {filepath} (already no www)")
        return False

    # Replace www.nikaappliancerepair.com -> nikaappliancerepair.com
    new_content = content.replace('www.nikaappliancerepair.com', 'nikaappliancerepair.com')

    # Verify replacement
    after_count = new_content.count('www.nikaappliancerepair.com')
    replaced_count = before_count - after_count

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ FIXED: {filepath} ({replaced_count} replacements)")
    return True

def main():
    print("=" * 70)
    print("🔧 FIXING WWW → NON-WWW URLs")
    print("=" * 70)
    print()
    print("Vercel redirects: www.nikaappliancerepair.com → nikaappliancerepair.com")
    print("So ALL canonical/schema/sitemap URLs must be WITHOUT www")
    print()

    base_dir = Path(__file__).parent

    updated_files = 0
    skipped_files = 0

    for file_path in FILES_TO_UPDATE:
        full_path = base_dir / file_path

        if fix_www_in_file(full_path):
            updated_files += 1
        else:
            skipped_files += 1

    print()
    print("=" * 70)
    print(f"✅ COMPLETE!")
    print(f"   Updated: {updated_files} files")
    print(f"   Skipped: {skipped_files} files")
    print("=" * 70)
    print()
    print("Changed:")
    print("  ❌ https://www.nikaappliancerepair.com/")
    print("  ✅ https://nikaappliancerepair.com/")
    print()
    print("Files updated:")
    print("  • sitemap.xml (32 pages)")
    print("  • robots.txt (sitemap URL)")
    print("  • index.html (canonical, schema, OG)")
    print("  • 9 service pages (canonical, schema, OG)")
    print("  • 21 location pages (canonical, schema, OG)")
    print()
    print("Now URLs match Vercel redirect configuration!")

if __name__ == '__main__':
    main()
