#!/usr/bin/env python3
"""
Fix multiple H1 tags - keep only one H1 (blog-title) and convert others to H2
This is a critical SEO fix - pages should have only one H1 tag
"""
import re
from pathlib import Path

def fix_h1_tags(filepath):
    """
    Fix multiple H1 tags by:
    1. Keep the first H1 with class="blog-title" (the main page title)
    2. Convert all other H1 tags to H2 tags
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all H1 tags
    h1_matches = list(re.finditer(r'<h1([^>]*)>(.*?)</h1>', content, re.DOTALL))

    if len(h1_matches) <= 1:
        return 0  # No fix needed

    # Keep only the first H1 (blog-title), convert others to H2
    fixed_count = 0

    # Process in reverse order to maintain positions
    for i in range(len(h1_matches) - 1, 0, -1):
        match = h1_matches[i]
        attrs = match.group(1)
        text = match.group(2)

        # Replace H1 with H2
        old_tag = f'<h1{attrs}>{text}</h1>'
        new_tag = f'<h2{attrs}>{text}</h2>'
        content = content.replace(old_tag, new_tag, 1)
        fixed_count += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return fixed_count

def main():
    blog_base = Path("blog")
    folders = ["maintenance", "troubleshooting", "guides"]

    print("\n" + "="*80)
    print("FIXING MULTIPLE H1 TAGS (SEO CRITICAL)")
    print("="*80 + "\n")

    total_fixed = 0
    total_posts = 0

    for folder in folders:
        folder_path = blog_base / folder
        if not folder_path.exists():
            continue

        html_files = sorted([f for f in folder_path.glob('*.html')])
        print(f"[{folder.upper()}] - {len(html_files)} posts\n")

        for filepath in html_files:
            try:
                fixed = fix_h1_tags(filepath)
                total_posts += 1
                if fixed > 0:
                    print(f"  FIXED {filepath.name} ({fixed} extra H1 -> H2)")
                    total_fixed += fixed
                else:
                    print(f"  OK {filepath.name}")
            except Exception as e:
                print(f"  ERROR {filepath.name}: {str(e)}")

        print()

    print("="*80)
    print(f"Total Posts Checked: {total_posts}")
    print(f"Total H1 Tags Fixed: {total_fixed}")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
