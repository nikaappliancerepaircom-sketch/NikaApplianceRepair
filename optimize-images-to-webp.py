#!/usr/bin/env python3
"""
Replace images with optimized WebP versions for better performance
"""

import os
import re
from pathlib import Path

# Production pages to update
PAGES = [
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
    # Location pages
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

# Pages that should use "Technician with drill.webp" in hero (high-tech services)
DRILL_HERO_PAGES = [
    'services/dryer-repair.html',
    'services/oven-repair.html',
    'services/range-repair.html',
    'services/microwave-repair.html',
]

def optimize_images_in_file(filepath, use_drill_hero=False):
    """Replace PNG images with optimized WebP versions"""

    if not os.path.exists(filepath):
        print(f"⚠️  SKIP: {filepath} (file not found)")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    # Determine path prefix based on file location
    if filepath == 'index.html':
        path_prefix = 'assets/images/'
    else:
        path_prefix = '../assets/images/'

    # 1. Replace hero image
    if use_drill_hero:
        # Use "Technician with drill.webp" for high-tech appliances
        hero_pattern = rf'<img src="{re.escape(path_prefix)}friendly-technician-character\.png"'
        hero_replacement = f'<img src="{path_prefix}Technician with drill.webp"'
        if re.search(hero_pattern, content):
            content = re.sub(hero_pattern, hero_replacement, content)
            changes_made.append('hero → Technician with drill.webp')
    else:
        # Use optimized friendly-technician-character-min.webp
        hero_pattern = rf'<img src="{re.escape(path_prefix)}friendly-technician-character\.png"'
        hero_replacement = f'<img src="{path_prefix}friendly-technician-character-min.webp"'
        if re.search(hero_pattern, content):
            content = re.sub(hero_pattern, hero_replacement, content)
            changes_made.append('hero → friendly-technician-character-min.webp')

    # 2. Replace About Us section image (if exists)
    # Look for about section images
    about_patterns = [
        # Modern video card style
        (rf'<img src="{re.escape(path_prefix)}[^"]*about[^"]*\.png"',
         f'<img src="{path_prefix}about us page-min.webp"'),
        # Direct about image
        (rf'src="{re.escape(path_prefix)}about-us[^"]*\.png"',
         f'src="{path_prefix}about us page-min.webp"'),
    ]

    for pattern, replacement in about_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            changes_made.append('about → about us page-min.webp')
            break

    # 3. Update Schema.org image references to WebP
    schema_pattern = rf'"image":\s*"https://nikaappliancerepair\.com/{re.escape(path_prefix)}friendly-technician-character\.png"'
    schema_replacement = f'"image": "https://nikaappliancerepair.com/{path_prefix}friendly-technician-character-min.webp"'
    if re.search(schema_pattern, content):
        content = re.sub(schema_pattern, schema_replacement, content)
        changes_made.append('schema image → webp')

    # 4. Update logo image reference
    logo_pattern = rf'"logo":\s*"https://nikaappliancerepair\.com/{re.escape(path_prefix)}friendly-technician-character\.png"'
    logo_replacement = f'"logo": "https://nikaappliancerepair.com/{path_prefix}friendly-technician-character-min.webp"'
    if re.search(logo_pattern, content):
        content = re.sub(logo_pattern, logo_replacement, content)
        changes_made.append('schema logo → webp')

    # 5. Update Open Graph image
    og_pattern = rf'<meta property="og:image" content="https://nikaappliancerepair\.com/{re.escape(path_prefix)}friendly-technician-character\.png"'
    og_replacement = f'<meta property="og:image" content="https://nikaappliancerepair.com/{path_prefix}friendly-technician-character-min.webp"'
    if re.search(og_pattern, content):
        content = re.sub(og_pattern, og_replacement, content)
        changes_made.append('og:image → webp')

    # Check if any changes were made
    if content == original_content:
        print(f"✓ SKIP: {filepath} (no images found to optimize)")
        return False

    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ UPDATED: {filepath} ({', '.join(changes_made)})")
    return True

def main():
    print("=" * 80)
    print("🖼️  OPTIMIZING IMAGES TO WEBP")
    print("=" * 80)
    print()
    print("Optimized images available:")
    print("  • friendly-technician-character-min.webp (hero - most pages)")
    print("  • Technician with drill.webp (hero - technical services)")
    print("  • about us page-min.webp (about section)")
    print()

    base_dir = Path(__file__).parent

    updated_count = 0
    skipped_count = 0

    for page in PAGES:
        file_path = base_dir / page
        use_drill = page in DRILL_HERO_PAGES

        if optimize_images_in_file(str(file_path), use_drill):
            updated_count += 1
        else:
            skipped_count += 1

    print()
    print("=" * 80)
    print(f"✅ COMPLETE!")
    print(f"   Updated: {updated_count} files")
    print(f"   Skipped: {skipped_count} files")
    print("=" * 80)
    print()
    print("Benefits of WebP:")
    print("  • 25-35% smaller file size than PNG")
    print("  • Faster page load times")
    print("  • Better Core Web Vitals scores")
    print("  • Improved mobile performance")
    print()
    print("Next: Commit and push to trigger Vercel deploy")

if __name__ == '__main__':
    main()
