#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add FAQ section and location section from homepage to brand pages."""

import os
import sys
import glob
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_faq_section():
    """Extract FAQ section from homepage."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract FAQ section (from FAQ heading to end of section)
    # Looking for section with "Frequently Asked Questions"
    pattern = r'(<section[^>]*>.*?<h2[^>]*>Frequently Asked Questions</h2>.*?</section>)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("ERROR: Could not find FAQ section")
        return None

    faq = match.group(1)
    print(f"✓ Extracted FAQ section: {len(faq)} characters")
    return faq

def extract_location_section():
    """Extract location section from homepage."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract location section (from 60+ SERVICE AREAS to end of section)
    pattern = r'(<section class="areas-section-premium".*?</section>)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("ERROR: Could not find location section")
        return None

    location = match.group(1)
    print(f"✓ Extracted location section: {len(location)} characters")
    return location

def update_brand_page(file_path, faq_section, location_section):
    """Update brand page with FAQ and location sections."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix relative links for brand pages
        faq_brand = faq_section.replace('href="/', 'href="../')
        location_brand = location_section.replace('href="/', 'href="../')

        # Remove existing FAQ section if present
        faq_pattern = r'<section[^>]*>.*?<h2[^>]*>.*?FAQ.*?</h2>.*?</section>'
        content = re.sub(faq_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Remove existing location section if present
        location_pattern = r'<section class="areas-section-premium".*?</section>|<section[^>]*>.*?SERVICE AREAS.*?</section>'
        content = re.sub(location_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

        # Insert new sections before footer
        footer_pos = content.find('<footer class="seo-footer-premium"')
        if footer_pos != -1:
            # Insert location section, then FAQ section before footer
            insert_text = '\n    ' + location_brand + '\n\n    ' + faq_brand + '\n\n    '
            content = content[:footer_pos] + insert_text + content[footer_pos:]
        else:
            print(f"  WARNING: Could not find footer in {os.path.basename(file_path)}")
            return False

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {os.path.basename(file_path)}")
            return True
        else:
            print(f"- No changes: {os.path.basename(file_path)}")
            return False

    except Exception as e:
        print(f"✗ Error: {file_path}: {e}")
        return False

def main():
    """Main function."""
    print("Adding FAQ and location sections to brand pages...\n")

    # Extract sections
    faq_section = extract_faq_section()
    location_section = extract_location_section()

    if not faq_section or not location_section:
        print("\nERROR: Failed to extract sections")
        return

    print(f"\n{'='*60}")

    # Get all brand pages
    brand_files = glob.glob('brands/*-appliance-repair-toronto.html')

    if not brand_files:
        print("ERROR: No brand pages found")
        return

    print(f"Found {len(brand_files)} brand pages\n")

    updated_count = 0
    for file_path in sorted(brand_files):
        if update_brand_page(file_path, faq_section, location_section):
            updated_count += 1

    print(f"\n{'='*60}")
    print(f"Updated {updated_count}/{len(brand_files)} pages")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
