#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Samsung brand page from optimized index.html template."""

import os
import sys
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def create_samsung_page():
    """Create Samsung page from index.html with brand-specific content."""

    print("Creating Samsung brand page from index.html template...\n")

    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print("✓ Loaded index.html")

    # BRAND-SPECIFIC REPLACEMENTS
    brand_name = "Samsung"
    brand_lower = "samsung"

    # 1. Title tag
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{brand_name} Appliance Repair Toronto | Same-Day Service | Save $40</title>',
        content
    )

    # 2. Meta description
    content = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="Expert {brand_name} appliance repair in Toronto & GTA. Same-day service on refrigerators, washers, dryers, dishwashers. Licensed technicians. 90-day warranty. Call 437-747-6737.">',
        content
    )

    # 3. H1 - Main heading
    content = re.sub(
        r'<h1[^>]*>.*?</h1>',
        f'<h1>We\'re the {brand_name} appliance repair experts that will fix your problem... FAST!</h1>',
        content,
        count=1
    )

    # 4. Hero section - replace generic text with Samsung-specific
    # Replace "appliance repair company" with "Samsung repair experts"
    content = content.replace(
        'the appliance repair company',
        f'the {brand_name} appliance repair experts'
    )

    # 5. Update service mentions to be Samsung-specific
    services = [
        ('Refrigerator Repair', f'{brand_name} Refrigerator Repair'),
        ('Dishwasher Repair', f'{brand_name} Dishwasher Repair'),
        ('Dryer Repair', f'{brand_name} Dryer Repair'),
        ('Washer Repair', f'{brand_name} Washer Repair'),
        ('Oven Repair', f'{brand_name} Oven Repair'),
        ('Stove Repair', f'{brand_name} Stove Repair'),
    ]

    # Only replace in service sections, not globally
    # Look for service section
    service_section_pattern = r'(<section[^>]*>.*?<h2[^>]*>What Appliance Repair Services Do You Offer.*?</section>)'
    service_match = re.search(service_section_pattern, content, re.DOTALL)
    if service_match:
        service_section = service_match.group(1)
        original_service = service_section

        for old, new in services:
            service_section = service_section.replace(old, new)

        content = content.replace(original_service, service_section)

    # 6. FAQ - Add Samsung-specific questions
    # Replace first FAQ question with Samsung-specific one
    content = re.sub(
        r'(<button[^>]*>)Is it worth it to fix an appliance\?(.*?</button>)',
        rf'\1How much does {brand_name} appliance repair cost?\2',
        content,
        count=1
    )

    # 7. Update "About Us" section to mention Samsung expertise
    content = re.sub(
        r'(Since 2019.*?)(appliance repair team)',
        rf'\1{brand_name} \2',
        content,
        count=1
    )

    # 8. Adjust file paths for brand subfolder (../ for CSS, images, etc.)
    content = content.replace('href="/css/', 'href="../css/')
    content = content.replace('src="/assets/', 'src="../assets/')
    content = content.replace('href="/services', 'href="../services')
    content = content.replace('href="/locations', 'href="../locations')
    content = content.replace('href="/about', 'href="../about')
    content = content.replace('href="/book', 'href="../book')
    content = content.replace('action="/', 'action="../')

    # 9. Keep review count at 5,200+ (already in index.html)

    # 10. Update canonical URL
    content = re.sub(
        r'<link rel="canonical" href=".*?">',
        f'<link rel="canonical" href="https://niappliancerepair.ca/brands/{brand_lower}-appliance-repair-toronto">',
        content
    )

    # Write to brands folder
    output_file = f'brands/{brand_lower}-appliance-repair-toronto.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created: {output_file}")

    # Count words in content
    text_content = re.sub(r'<[^>]+>', ' ', content)
    words = len(text_content.split())
    print(f"✓ Word count: ~{words} words")

    print("\n" + "=" * 60)
    print("Samsung brand page created successfully!")
    print("Next: Run BMAD test to verify all parameters")
    print("=" * 60)

if __name__ == '__main__':
    create_samsung_page()
