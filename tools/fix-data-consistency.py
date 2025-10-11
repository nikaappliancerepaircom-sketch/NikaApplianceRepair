#!/usr/bin/env python3
"""
Fix data consistency issues across all pages
- Warranty: all to 90-day
- Review count: all to 5,200+
- Rating: all to 4.9
"""

import os
import re
from pathlib import Path

def fix_warranty(content):
    """Fix all warranty mentions to 90-day"""
    # Replace 1 year/1-year with 90-day
    content = re.sub(r'1[- ]year\s+warranty', '90-day warranty', content, flags=re.IGNORECASE)
    content = re.sub(r'1[- ]year\s+parts\s*(&amp;|&|and)\s*labor', '90-day parts &amp; labor', content, flags=re.IGNORECASE)

    # Replace any warranty without number to 90-day
    content = re.sub(r'<strong>Warranty:</strong>\s*1 year', '<strong>Warranty:</strong> 90 days', content)

    return content

def fix_review_count(content):
    """Fix review count to always be 5,200+"""
    # Replace "200+ reviews" or similar low numbers with 5,200+
    content = re.sub(r'\b200\+?\s+(reviews?|customers?)', '5,200+ \\1', content, flags=re.IGNORECASE)
    content = re.sub(r'\b300\+?\s+(reviews?|customers?)', '5,200+ \\1', content, flags=re.IGNORECASE)
    content = re.sub(r'\b500\+?\s+(reviews?|customers?)', '5,200+ \\1', content, flags=re.IGNORECASE)

    return content

def fix_rating(content):
    """Ensure all ratings are 4.9"""
    # Replace other ratings with 4.9
    content = re.sub(r'\b4\.[0-8]\s*[★⭐/]', '4.9 ★', content)
    content = re.sub(r'ratingValue["\']:\s*["\']4\.[0-8]["\']', 'ratingValue": "4.9"', content)

    return content

def process_file(file_path):
    """Process a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Apply all fixes
        content = fix_warranty(content)
        content = fix_review_count(content)
        content = fix_rating(content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("FIXING DATA CONSISTENCY ISSUES")
    print("=" * 60)

    # Process all HTML files
    all_files = []

    # Main page
    all_files.append(base_dir / 'index.html')

    # Services
    services_dir = base_dir / 'services'
    all_files.extend(services_dir.glob('*.html'))

    # Locations
    locations_dir = base_dir / 'locations'
    all_files.extend(locations_dir.glob('*.html'))

    # Blogs
    blog_dir = base_dir / 'blog'
    all_files.extend(blog_dir.glob('*.html'))

    fixed_count = 0
    for file_path in all_files:
        if file_path.name == 'index.html' and 'locations' in str(file_path):
            continue
        if file_path.name == 'index.html' and 'services' in str(file_path):
            continue
        if file_path.name == 'index.html' and 'blog' in str(file_path):
            continue

        if process_file(file_path):
            print(f"[FIXED] {file_path.name}")
            fixed_count += 1
        else:
            print(f"[OK] {file_path.name}")

    print("\n" + "=" * 60)
    print(f"FIXED: {fixed_count}/{len(all_files)} files updated")
    print("=" * 60)

if __name__ == '__main__':
    main()
