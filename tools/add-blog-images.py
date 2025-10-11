#!/usr/bin/env python3
"""
Add images to blog posts
Each blog needs 5-8 relevant images with proper alt tags
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

# Image templates for each blog topic
BLOG_IMAGES = {
    'how-to-fix-refrigerator-not-cooling': [
        ('refrigerator-thermostat-check.jpg', 'Technician checking refrigerator thermostat settings'),
        ('condenser-coils-cleaning.jpg', 'Cleaning dirty condenser coils on refrigerator'),
        ('refrigerator-door-seal-inspection.jpg', 'Inspecting refrigerator door seal for damage'),
        ('evaporator-fan-repair.jpg', 'Repairing refrigerator evaporator fan'),
        ('temperature-gauge-reading.jpg', 'Checking refrigerator temperature with digital gauge'),
    ],
    'washer-not-draining-solutions': [
        ('washer-drain-hose-check.jpg', 'Inspecting washing machine drain hose for clogs'),
        ('washer-pump-filter-cleaning.jpg', 'Cleaning washing machine pump filter'),
        ('washer-drain-pump-replacement.jpg', 'Replacing faulty washing machine drain pump'),
        ('washer-lid-switch-test.jpg', 'Testing washing machine lid switch'),
    ],
    'dryer-not-heating-troubleshooting': [
        ('dryer-heating-element-test.jpg', 'Testing dryer heating element with multimeter'),
        ('dryer-thermal-fuse-check.jpg', 'Checking dryer thermal fuse for continuity'),
        ('dryer-vent-cleaning.jpg', 'Professional dryer vent cleaning service'),
        ('dryer-thermostat-replacement.jpg', 'Replacing dryer cycling thermostat'),
    ],
    'dishwasher-not-cleaning-solutions': [
        ('dishwasher-spray-arm-cleaning.jpg', 'Cleaning clogged dishwasher spray arms'),
        ('dishwasher-filter-maintenance.jpg', 'Removing and cleaning dishwasher filter'),
        ('dishwasher-detergent-dispenser.jpg', 'Checking dishwasher detergent dispenser'),
        ('dishwasher-water-inlet-valve.jpg', 'Inspecting dishwasher water inlet valve'),
    ],
    'oven-temperature-calibration-guide': [
        ('oven-thermometer-placement.jpg', 'Placing oven thermometer for temperature check'),
        ('oven-temperature-calibration.jpg', 'Calibrating oven temperature settings'),
        ('oven-thermostat-adjustment.jpg', 'Adjusting oven thermostat dial'),
        ('digital-oven-control-panel.jpg', 'Programming digital oven control panel'),
    ],
}

# Default images for blogs without specific images
DEFAULT_IMAGES = [
    ('appliance-technician-repair.jpg', 'Professional appliance technician performing repair'),
    ('modern-kitchen-appliances.jpg', 'Modern kitchen with stainless steel appliances'),
    ('appliance-maintenance-tools.jpg', 'Professional appliance repair tools and equipment'),
    ('customer-satisfaction-service.jpg', 'Happy customer after appliance repair service'),
    ('emergency-repair-service.jpg', 'Emergency appliance repair service call'),
]

def add_images_to_blog(file_path):
    """Add images to blog post"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')

        if not main_content:
            print(f"[SKIP] {file_path.name}: No main content area found")
            return False

        # Get images for this blog
        blog_slug = file_path.stem
        images = BLOG_IMAGES.get(blog_slug, DEFAULT_IMAGES)

        # Find all h2 sections
        h2_tags = main_content.find_all('h2')

        if len(h2_tags) < 3:
            print(f"[SKIP] {file_path.name}: Not enough h2 sections")
            return False

        # Add images after every 2nd h2
        images_added = 0
        for i, h2 in enumerate(h2_tags):
            if i % 2 == 1 and images_added < len(images):  # After 2nd, 4th, 6th h2
                img_file, alt_text = images[images_added]

                # Create figure with image
                figure = soup.new_tag('figure', **{'class': 'blog-image'})
                img = soup.new_tag('img',
                                   src=f'/images/blog/{img_file}',
                                   alt=alt_text,
                                   loading='lazy',
                                   width='800',
                                   height='600')
                figcaption = soup.new_tag('figcaption')
                figcaption.string = alt_text

                figure.append(img)
                figure.append(figcaption)

                # Insert after h2's next sibling (usually a paragraph)
                next_elem = h2.find_next_sibling()
                if next_elem:
                    next_elem.insert_after(figure)
                else:
                    h2.insert_after(figure)

                images_added += 1

        if images_added > 0:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            print(f"[ADDED] {file_path.name}: {images_added} images")
            return True
        else:
            print(f"[SKIP] {file_path.name}: No images added")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent
    blog_dir = base_dir / 'blog'

    print("=" * 60)
    print("ADDING IMAGES TO BLOG POSTS")
    print("=" * 60)

    blog_files = [f for f in blog_dir.glob('*.html') if f.name != 'index.html']

    added = 0
    for file_path in blog_files:
        if add_images_to_blog(file_path):
            added += 1

    print("\n" + "=" * 60)
    print(f"ADDED IMAGES: {added}/{len(blog_files)} blog posts")
    print("=" * 60)
    print("\nNOTE: Image files need to be created in /images/blog/")
    print("Use placeholder images or generate with AI image tools")

if __name__ == '__main__':
    main()
