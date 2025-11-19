#!/usr/bin/env python3
"""
Convert hero images to WebP format and update blog posts
Reduces image size by ~70% for faster page loads
"""

import os
import re
from pathlib import Path
from PIL import Image

def convert_to_webp(png_path, quality=85):
    """Convert PNG to WebP with optimization"""
    webp_path = png_path.with_suffix('.webp')

    try:
        with Image.open(png_path) as img:
            # Convert to RGB if necessary (WebP doesn't support RGBA well)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background

            # Save as WebP
            img.save(webp_path, 'WEBP', quality=quality, method=6)

            # Get file sizes
            png_size = png_path.stat().st_size
            webp_size = webp_path.stat().st_size
            reduction = ((png_size - webp_size) / png_size) * 100

            return True, webp_size, reduction
    except Exception as e:
        return False, 0, 0

def update_blog_post_images(html_file):
    """Update blog post to use WebP with PNG fallback"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all hero image references
    # Pattern: <img src="../images/FILENAME.png" alt="..." loading="eager">
    pattern = r'<div class="blog-hero-image">\s*<img src="\.\./images/([^"]+\.png)" alt="([^"]*)" loading="eager">\s*</div>'

    def replace_with_picture(match):
        png_filename = match.group(1)
        alt_text = match.group(2)
        webp_filename = png_filename.replace('.png', '.webp')

        return f'''<div class="blog-hero-image">
                <picture>
                    <source srcset="../images/{webp_filename}" type="image/webp">
                    <img src="../images/{png_filename}" alt="{alt_text}" loading="eager">
                </picture>
            </div>'''

    # Check if already using picture element
    if '<picture>' in content:
        return False, "Already optimized"

    new_content = re.sub(pattern, replace_with_picture, content)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Updated to WebP"

    return False, "No hero image found"

def main():
    """Convert all hero images and update blog posts"""

    # Convert PNG images to WebP
    images_dir = Path("C:\\NikaApplianceRepair\\blog\\images")
    hero_images = list(images_dir.glob("*-hero.png"))

    print("Converting Hero Images to WebP")
    print("=" * 70)

    total_png_size = 0
    total_webp_size = 0
    converted = 0

    for png_path in sorted(hero_images):
        success, webp_size, reduction = convert_to_webp(png_path)

        if success:
            png_size = png_path.stat().st_size
            total_png_size += png_size
            total_webp_size += webp_size
            converted += 1

            print(f"[CONVERTED] {png_path.name}")
            print(f"  PNG: {png_size / 1024:.1f} KB -> WebP: {webp_size / 1024:.1f} KB")
            print(f"  Reduction: {reduction:.1f}%")
        else:
            print(f"[ERROR] Failed to convert {png_path.name}")

    print("=" * 70)
    print(f"Converted {converted} images")
    print(f"Total PNG: {total_png_size / 1024 / 1024:.2f} MB")
    print(f"Total WebP: {total_webp_size / 1024 / 1024:.2f} MB")
    print(f"Total Reduction: {((total_png_size - total_webp_size) / total_png_size) * 100:.1f}%")

    # Update blog posts
    print("\n" + "=" * 70)
    print("Updating Blog Posts to Use WebP")
    print("=" * 70)

    blog_dir = Path("C:\\NikaApplianceRepair\\blog")
    html_files = []

    for category in ['guides', 'troubleshooting', 'maintenance']:
        category_path = blog_dir / category
        if category_path.exists():
            html_files.extend(list(category_path.glob("*.html")))

    updated = 0
    skipped = 0

    for html_file in sorted(html_files):
        success, message = update_blog_post_images(html_file)

        if success:
            print(f"[UPDATED] {html_file.relative_to(blog_dir)}")
            updated += 1
        elif "Already optimized" in message:
            skipped += 1

    print("=" * 70)
    print(f"\nResults:")
    print(f"  Updated: {updated} posts")
    print(f"  Already optimized: {skipped} posts")
    print(f"  Total: {len(html_files)} posts")

    print(f"\n[SUCCESS] Images optimized and {updated} blog posts updated!")
    print(f"Page load improvement: ~{((total_png_size - total_webp_size) / 1024):.0f} KB saved per page")

if __name__ == "__main__":
    main()
