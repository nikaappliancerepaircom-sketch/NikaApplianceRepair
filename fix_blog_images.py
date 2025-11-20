"""Fix blog post hero image paths to use correct WebP images"""
import os
import re
from pathlib import Path

blog_dir = Path('C:/NikaApplianceRepair/blog')

# Map of slug to correct hero image
def get_hero_image_for_post(filepath):
    """Get the correct hero image filename for a blog post"""
    slug = filepath.stem
    webp_image = f"{slug}-hero.webp"

    # Check if this specific WebP exists
    images_dir = blog_dir / 'images'
    if (images_dir / webp_image).exists():
        return webp_image

    # Fallback to generic images based on category
    category = filepath.parent.name
    if category == 'guides':
        return 'general-appliance-repair-hero.webp'
    elif category == 'maintenance':
        return 'appliance-maintenance-hero.webp'
    elif category == 'troubleshooting':
        return 'appliance-troubleshooting-hero.webp'

    return 'general-appliance-repair-hero.webp'

# Process all HTML files
fixed_count = 0
for category in ['guides', 'maintenance', 'troubleshooting']:
    category_path = blog_dir / category
    if not category_path.exists():
        continue

    for html_file in category_path.glob('*.html'):
        if html_file.name == 'index.html':
            continue

        # Read file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get correct hero image
        hero_image = get_hero_image_for_post(html_file)

        # Replace PNG with WebP
        # Pattern: <img src="../images/anything-hero.png"
        new_content = re.sub(
            r'<img\s+src="../images/[^"]*?-hero\.png"',
            f'<img src="../images/{hero_image}"',
            content
        )

        # Also update any webp references to use correct slug-based name
        new_content = re.sub(
            r'<img\s+src="../images/[^"]*?-hero\.webp"',
            f'<img src="../images/{hero_image}"',
            new_content
        )

        # Write back if changed
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] Fixed: {category}/{html_file.name} -> {hero_image}")
            fixed_count += 1
        else:
            print(f"  Skipped: {category}/{html_file.name} (no change needed)")

print(f"\n[DONE] Fixed {fixed_count} blog posts")
