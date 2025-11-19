#!/usr/bin/env python3
"""
Add hero images to blog posts that are missing them
Maps each post to appropriate stock hero image based on appliance type
"""

import os
import re
from pathlib import Path

# Mapping of appliance categories to hero image filenames
CATEGORY_IMAGES = {
    'dishwasher': 'dishwasher-repair-hero.png',
    'refrigerator': 'refrigerator-repair-hero.png',
    'washer': 'washer-repair-hero.png',
    'dryer': 'dryer-repair-hero.png',
    'oven': 'oven-repair-hero.png',
    'microwave': 'microwave-repair-hero.png',
    'garbage-disposal': 'garbage-disposal-repair-hero.png',
    'water-heater': 'water-heater-repair-hero.png',
    'general': 'general-appliance-repair-hero.png',
}

def categorize_post(filename):
    """Determine appliance category from filename"""
    filename_lower = filename.lower()

    if 'dishwasher' in filename_lower:
        return 'dishwasher'
    elif 'refrigerator' in filename_lower or 'freezer' in filename_lower or 'ice-maker' in filename_lower or 'ice maker' in filename_lower:
        return 'refrigerator'
    elif 'washer' in filename_lower or 'washing-machine' in filename_lower or 'washing machine' in filename_lower:
        return 'washer'
    elif 'dryer' in filename_lower:
        return 'dryer'
    elif 'oven' in filename_lower or 'stove' in filename_lower or 'range' in filename_lower:
        return 'oven'
    elif 'microwave' in filename_lower:
        return 'microwave'
    elif 'garbage-disposal' in filename_lower or 'garbage disposal' in filename_lower:
        return 'garbage-disposal'
    elif 'water-heater' in filename_lower or 'water heater' in filename_lower:
        return 'water-heater'
    else:
        return 'general'

def get_alt_text(category, filename):
    """Generate descriptive alt text for hero image"""
    filename_clean = filename.replace('.html', '').replace('-', ' ').title()

    alt_templates = {
        'dishwasher': 'Professional dishwasher repair technician servicing modern appliance in Toronto home',
        'refrigerator': 'Refrigerator repair specialist diagnosing cooling issues in modern kitchen',
        'washer': 'Washing machine repair technician inspecting appliance components',
        'dryer': 'Dryer repair expert servicing appliance in clean laundry room',
        'oven': 'Oven repair technician servicing stove in Toronto kitchen',
        'microwave': 'Microwave repair specialist diagnosing appliance issues',
        'garbage-disposal': 'Garbage disposal repair technician working under kitchen sink',
        'water-heater': 'Water heater repair specialist servicing modern equipment',
        'general': 'Professional appliance repair technician servicing household appliances',
    }

    return alt_templates.get(category, 'Professional appliance repair service in Toronto')

def add_hero_image(html_file):
    """Add hero image to blog post if missing"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if hero image already exists
    if 'blog-hero-image' in content or '<img src="../images/' in content:
        return False, "Already has hero image"

    # Determine category and image
    category = categorize_post(html_file.name)
    image_filename = CATEGORY_IMAGES[category]
    alt_text = get_alt_text(category, html_file.name)

    # Create hero image HTML
    hero_html = f'''
            <!-- Hero Image -->
            <div class="blog-hero-image">
                <img src="../images/{image_filename}" alt="{alt_text}" loading="eager">
            </div>
'''

    # Find insertion point (after social share section, before blog content)
    # Pattern: </div> (end of social-share) optionally followed by <!-- comment --> then <article class="blog-content">
    pattern = r'(</div>\s*(?:<!--.*?-->\s*)?)(<article class="blog-content">)'

    # Try to find the pattern
    match = re.search(pattern, content)

    if match:
        # Insert hero image between social share and content
        new_content = content[:match.end(1)] + hero_html + content[match.start(2):]

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, f"Added {category} hero image"
    else:
        return False, "Could not find insertion point"

def main():
    """Process all blog posts"""
    blog_dir = Path("C:\\NikaApplianceRepair\\blog")

    # Find all HTML files in blog subdirectories
    html_files = []
    for category in ['guides', 'troubleshooting', 'maintenance']:
        category_path = blog_dir / category
        if category_path.exists():
            html_files.extend(list(category_path.glob("*.html")))

    print(f"Found {len(html_files)} blog posts")
    print("=" * 70)

    updated = 0
    skipped = 0
    errors = 0

    for html_file in sorted(html_files):
        success, message = add_hero_image(html_file)

        if success:
            print(f"[UPDATED] {html_file.relative_to(blog_dir)} - {message}")
            updated += 1
        elif "Already has" in message:
            skipped += 1
        else:
            print(f"[SKIP] {html_file.relative_to(blog_dir)} - {message}")
            errors += 1

    print("=" * 70)
    print(f"\nResults:")
    print(f"  Updated: {updated} posts")
    print(f"  Skipped (already has image): {skipped} posts")
    print(f"  Errors: {errors} posts")
    print(f"  Total: {len(html_files)} posts")

    if updated > 0:
        print(f"\n[SUCCESS] Added hero images to {updated} blog posts!")
    else:
        print(f"\n[INFO] No updates needed - all posts already have hero images")

if __name__ == "__main__":
    main()
