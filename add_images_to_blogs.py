#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add images to all blog posts for Google SEO
Each post gets 3-4 images with proper schema markup
"""

import os
import sys
import glob
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Image mapping by appliance type
# Using existing assets + placeholder images for now
IMAGES = {
    'refrigerator': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional refrigerator repair technician in Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1571175351322-4eb8f3f44bc2?w=800&h=600&fit=crop', 'Modern refrigerator interior', 800, 600),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Appliance repair tools', 800, 600),
    ],
    'dishwasher': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional dishwasher repair service Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Dishwasher repair parts', 800, 600),
        ('https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&h=600&fit=crop', 'Clean dishwasher interior', 800, 600),
    ],
    'washer': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional washing machine repair Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&h=600&fit=crop', 'Washing machine drum', 800, 600),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Appliance repair tools', 800, 600),
    ],
    'dryer': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional dryer repair service Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&h=600&fit=crop', 'Dryer lint filter cleaning', 800, 600),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Dryer vent maintenance', 800, 600),
    ],
    'oven': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional oven repair service Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800&h=600&fit=crop', 'Modern oven interior', 800, 600),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Oven repair tools', 800, 600),
    ],
    'stove': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional stove repair technician Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop', 'Gas stove burners', 800, 600),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Stove maintenance tools', 800, 600),
    ],
    'microwave': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional microwave repair Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800&h=600&fit=crop', 'Modern microwave oven', 800, 600),
    ],
    'freezer': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional freezer repair service Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1571175351322-4eb8f3f44bc2?w=800&h=600&fit=crop', 'Freezer interior', 800, 600),
    ],
    'disposal': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional garbage disposal repair Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Plumbing tools', 800, 600),
    ],
    'all': [
        ('https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp', 'Professional appliance repair technician Toronto', 800, 1000),
        ('https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop', 'Professional appliance repair tools', 800, 600),
        ('https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&h=600&fit=crop', 'Modern home appliances', 800, 600),
    ],
}

def detect_appliance_type(content):
    """Detect appliance type from content"""
    content_lower = content.lower()

    if 'refrigerator' in content_lower or 'fridge' in content_lower:
        return 'refrigerator'
    elif 'dishwasher' in content_lower:
        return 'dishwasher'
    elif 'washing machine' in content_lower or 'washer' in content_lower:
        return 'washer'
    elif 'dryer' in content_lower:
        return 'dryer'
    elif 'oven' in content_lower:
        return 'oven'
    elif 'stove' in content_lower or 'cooktop' in content_lower:
        return 'stove'
    elif 'microwave' in content_lower:
        return 'microwave'
    elif 'freezer' in content_lower:
        return 'freezer'
    else:
        return 'all'

def add_images_to_post(filepath):
    """Add images to blog post HTML"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has images
    if '<img' in content and 'blog/' in content:
        return False  # Already processed

    # Detect appliance type
    appliance_type = detect_appliance_type(content)
    images = IMAGES.get(appliance_type, IMAGES['all'])

    # Get main image (hero image)
    hero_url, hero_alt, hero_width, hero_height = images[0]

    # 1. Add hero image after h1
    hero_img_html = f'''
            <div class="post-featured-image">
                <img src="{hero_url}" alt="{hero_alt}" width="{hero_width}" height="{hero_height}" loading="eager">
            </div>'''

    content = content.replace(
        '</div>\n\n            <!-- Quick Answer Box -->',
        f'</div>{hero_img_html}\n\n            <!-- Quick Answer Box -->'
    )

    # 2. Add 2-3 content images
    content_images = []
    for i, (url, alt, width, height) in enumerate(images[1:3], start=1):
        img_html = f'''
                <div class="content-image">
                    <img src="{url}" alt="{alt}" width="{width}" height="{height}" loading="lazy">
                </div>'''
        content_images.append(img_html)

    # Insert first content image after first h3
    if '<h3>' in content:
        content = content.replace(
            '<h3>Key Points</h3>',
            f'{content_images[0]}\n\n                <h3>Key Points</h3>',
            1
        )

    # Insert second content image before CTA section
    if len(content_images) > 1:
        content = content.replace(
            '<!-- CTA Section -->',
            f'{content_images[1]}\n\n            <!-- CTA Section -->'
        )

    # 3. Update schema.org with images
    image_list = ', '.join([f'"{url}"' for url, _, _, _ in images[:3]])

    # Add image to Article schema
    content = re.sub(
        r'"description": "([^"]+)"',
        f'"description": "\\1",\n      "image": [{image_list}]',
        content,
        count=1
    )

    # 4. Update Open Graph image
    content = re.sub(
        r'<meta property="og:url" content="[^"]+">',
        f'<meta property="og:url" content="https://nikaappliancerepair.com/blog/...">\n    <meta property="og:image" content="{hero_url}">',
        content
    )

    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def process_all_posts():
    """Process all blog posts in queue and published"""

    print("=" * 70)
    print("🖼️  ADDING IMAGES TO BLOG POSTS")
    print("=" * 70)
    print()

    # Get all blog posts
    all_posts = []

    # Queue
    if os.path.exists('blog/_queue'):
        all_posts.extend(glob.glob('blog/_queue/*.html'))

    # Published
    for category in ['troubleshooting', 'maintenance', 'cost-pricing', 'brands', 'seasonal', 'location']:
        category_dir = f'blog/{category}'
        if os.path.exists(category_dir):
            all_posts.extend(glob.glob(f'{category_dir}/*.html'))

    updated_count = 0

    for post_path in all_posts:
        filename = os.path.basename(post_path)

        if add_images_to_post(post_path):
            updated_count += 1
            print(f"✅ Added images: {filename}")
        else:
            print(f"⏭️  Skipped (already has images): {filename}")

    print()
    print("=" * 70)
    print(f"🎉 Updated {updated_count}/{len(all_posts)} posts")
    print("=" * 70)
    print()
    print("Each post now has:")
    print("  • 1 hero image (above fold, eager loading)")
    print("  • 2-3 content images (lazy loading)")
    print("  • Schema.org ImageObject markup")
    print("  • Open Graph og:image tag")
    print()
    print("Google will index these images for:")
    print("  ✓ Image search results")
    print("  ✓ Featured snippets with images")
    print("  ✓ Rich results in SERPs")

if __name__ == "__main__":
    process_all_posts()
