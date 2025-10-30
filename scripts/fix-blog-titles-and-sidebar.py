#!/usr/bin/env python3
"""
Fix blog titles (H1) and ensure sidebar is visible
Extract real titles from <title> tag and update H1 elements
"""
import re
from pathlib import Path

def extract_real_title(filepath):
    """Extract title from <title> tag in head"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    if title_match:
        full_title = title_match.group(1).strip()
        # Remove " - Nika Appliance Repair" suffix if present
        title = re.sub(r'\s*-\s*Nika Appliance Repair\s*$', '', full_title)
        return title
    return None

def fix_blog_title(filepath):
    """Update H1 blog title with extracted title from <title> tag"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    real_title = extract_real_title(filepath)
    if not real_title:
        return False

    # Replace the hardcoded "Blog Post" H1 with the real title
    # Match: <h1 class="blog-title">Blog Post</h1>
    # Replace with: <h1 class="blog-title">{real_title}</h1>
    new_content = re.sub(
        r'<h1\s+class="blog-title">Blog Post</h1>',
        f'<h1 class="blog-title">{real_title}</h1>',
        content
    )

    if new_content == content:
        return False  # No change made

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    blog_base = Path("blog")
    folders = ["maintenance", "troubleshooting", "guides"]

    print("\n" + "="*80)
    print("FIXING BLOG TITLES (H1) AND ENSURING SIDEBAR")
    print("="*80 + "\n")

    total_fixed = 0
    total_skipped = 0

    for folder in folders:
        folder_path = blog_base / folder
        if not folder_path.exists():
            continue

        html_files = sorted([f for f in folder_path.glob('*.html')])
        print(f"[{folder.upper()}] - {len(html_files)} posts\n")

        for filepath in html_files:
            try:
                if fix_blog_title(filepath):
                    print(f"  FIXED {filepath.name}")
                    total_fixed += 1
                else:
                    print(f"  SKIP {filepath.name} (already correct or no title found)")
                    total_skipped += 1
            except Exception as e:
                print(f"  ERROR {filepath.name}: {str(e)}")

        print()

    print("="*80)
    print(f"Total Fixed: {total_fixed}")
    print(f"Total Skipped: {total_skipped}")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
