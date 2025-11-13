#!/usr/bin/env python3
"""
Add share-buttons.js script reference to all blog posts
This script ensures all blog posts can handle social share button clicks
"""

import os
import re
from pathlib import Path

def add_share_script_to_blog_posts():
    """Add share-buttons.js script to all blog HTML files"""

    blog_dir = Path("C:\\NikaApplianceRepair\\blog")

    # Find all HTML files in blog directory
    html_files = list(blog_dir.rglob("*.html"))

    # Filter out the template file
    html_files = [f for f in html_files if "templates" not in str(f)]

    print(f"Found {len(html_files)} blog post files")

    updated_count = 0
    already_has_count = 0

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if share-buttons.js is already in the file
            if 'share-buttons.js' in content:
                already_has_count += 1
                print(f"[OK] Already has share script: {html_file.name}")
                continue

            # Look for the location to insert the script
            # We want to add it right before the closing </body> tag
            # or right after faq-accordion.js if it exists

            # Check for faq-accordion.js and add after it
            if 'faq-accordion.js' in content:
                # Find the faq-accordion.js script tag and add share-buttons.js after it
                pattern = r'(<script[^>]*src="/blog/js/faq-accordion\.js"[^>]*></script>)'
                replacement = r'\1\n    <script src="/blog/js/share-buttons.js"></script>'
                new_content = re.sub(pattern, replacement, content)
            else:
                # If no faq-accordion.js, add before responsive-tables.js
                if 'responsive-tables.js' in content:
                    pattern = r'(<script[^>]*src="/blog/js/responsive-tables\.js"[^>]*></script>)'
                    replacement = r'    <script src="/blog/js/share-buttons.js"></script>\n    \1'
                    new_content = re.sub(pattern, replacement, content)
                else:
                    # Last resort: add before closing body tag
                    new_content = content.replace('</body>', '    <script src="/blog/js/share-buttons.js"></script>\n</body>')

            # Check if content was actually modified
            if new_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                print(f"[UPDATED] {html_file.name}")
            else:
                print(f"[SKIP] Could not find insertion point: {html_file.name}")

        except Exception as e:
            print(f"[ERROR] {html_file.name}: {str(e)}")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total blog posts: {len(html_files)}")
    print(f"  Already had script: {already_has_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Total with share script: {already_has_count + updated_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    add_share_script_to_blog_posts()
