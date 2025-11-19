#!/usr/bin/env python3
"""
Fix Canonical Tags in Blog Posts
Replaces .html canonical URLs with clean URLs for SEO
"""

import os
import re
from pathlib import Path

def fix_canonical_tags():
    """Fix canonical tags in all blog post HTML files"""

    blog_dir = Path("C:\\NikaApplianceRepair\\blog")

    # Find all HTML files
    html_files = list(blog_dir.rglob("*.html"))

    # Filter out templates and special files
    html_files = [
        f for f in html_files
        if "templates" not in str(f)
        and "test" not in str(f).lower()
        and "demo" not in str(f).lower()
    ]

    print(f"Found {len(html_files)} blog post files")

    updated_count = 0
    errors = []

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract current canonical tag
            canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content, re.IGNORECASE)

            if not canonical_match:
                print(f"[SKIP] No canonical tag found: {html_file.name}")
                continue

            old_canonical = canonical_match.group(1)

            # Determine the clean URL path based on file location
            relative_path = html_file.relative_to(blog_dir)

            # Convert path to clean URL
            # Example: guides/bosch-dishwasher-repair.html -> /blog/guides/bosch-dishwasher-repair
            path_parts = list(relative_path.parts)

            # Remove .html extension
            if path_parts[-1].endswith('.html'):
                path_parts[-1] = path_parts[-1][:-5]

            # Build clean URL
            if len(path_parts) == 1:
                # Root blog file like index.html
                clean_path = f"/blog/{path_parts[0]}"
            else:
                # Category/subcategory files
                clean_path = "/blog/" + "/".join(path_parts)

            new_canonical = f"https://nikaappliancerepair.com{clean_path}"

            # Skip if already correct
            if old_canonical == new_canonical:
                print(f"[OK] Already correct: {html_file.name}")
                continue

            # Replace canonical tag
            new_canonical_tag = f'<link rel="canonical" href="{new_canonical}"'
            content = re.sub(
                r'<link\s+rel="canonical"\s+href="[^"]+"',
                new_canonical_tag,
                content,
                flags=re.IGNORECASE
            )

            # Write updated content
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

            updated_count += 1
            print(f"[UPDATED] {html_file.name}")
            print(f"  Old: {old_canonical}")
            print(f"  New: {new_canonical}")

        except Exception as e:
            error_msg = f"{html_file.name}: {str(e)}"
            errors.append(error_msg)
            print(f"[ERROR] {error_msg}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Canonical Tag Fix Summary:")
    print(f"  Total files processed: {len(html_files)}")
    print(f"  Successfully updated: {updated_count}")
    print(f"  Errors: {len(errors)}")
    print(f"{'='*60}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")

if __name__ == "__main__":
    fix_canonical_tags()
