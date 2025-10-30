#!/usr/bin/env python3
"""
Add missing SEO meta tags:
1. Canonical tags
2. OpenGraph tags
3. Fix description length
4. Add missing keywords
5. Optimize title length
"""
import re
from pathlib import Path

def add_seo_tags(filepath):
    """Add missing SEO tags to a post"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    # 1. Get current meta tags
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    kw_match = re.search(r'<meta name="keywords" content="([^"]+)"', content)

    title = title_match.group(1) if title_match else "Blog Post"
    description = desc_match.group(1) if desc_match else ""
    keywords = kw_match.group(1) if kw_match else ""

    # 2. Shorten title if needed (max 60 chars without " - Nika Appliance Repair")
    clean_title = re.sub(r'\s*-\s*Nika Appliance Repair\s*$', '', title)
    if len(clean_title) > 60:
        # Find a good cut point
        words = clean_title.split()
        shortened = ""
        for word in words:
            if len(shortened) + len(word) + 1 <= 55:
                shortened += word + " "
            else:
                break
        clean_title = shortened.strip()
        changes.append("TITLE_SHORTENED")

    new_title = f"{clean_title} - Nika Appliance Repair"
    # Update title tag
    if title_match:
        content = content.replace(
            f'<title{title_match.group(0)[5:-8]}{title_match.group(0)[-8:]}',
            f'<title>{new_title}</title>'
        )
        content = re.sub(
            r'<title[^>]*>[^<]+</title>',
            f'<title>{new_title}</title>',
            content
        )
        if clean_title != title_match.group(1).replace(' - Nika Appliance Repair', ''):
            changes.append("TITLE_UPDATED")

    # 3. Trim description to 160 chars if needed
    if description and len(description) > 160:
        description = description[:157] + "..."
        old_desc = desc_match.group(0)
        new_desc = f'<meta name="description" content="{description}"'
        content = content.replace(old_desc, new_desc)
        changes.append("DESC_TRIMMED")

    # 4. Add keywords if missing (2 posts)
    if not keywords or keywords.strip() == "":
        # Generate keywords from title
        words = clean_title.lower().split()
        keywords = ", ".join(words[:5])
        # Add after description
        insert_pos = content.find('</head>')
        if insert_pos > 0:
            meta_kw = f'    <meta name="keywords" content="{keywords}">\n'
            content = content[:insert_pos] + meta_kw + content[insert_pos:]
            changes.append("KEYWORDS_ADDED")

    # 5. Add canonical tag if missing
    if '<link rel="canonical"' not in content:
        insert_pos = content.find('</head>')
        if insert_pos > 0:
            # Use filename as slug
            filename = filepath.stem
            canonical = f'    <link rel="canonical" href="/blog/{filename}.html">\n'
            content = content[:insert_pos] + canonical + content[insert_pos:]
            changes.append("CANONICAL_ADDED")

    # 6. Add OpenGraph tags if missing
    if '<meta property="og:' not in content:
        insert_pos = content.find('</head>')
        if insert_pos > 0:
            og_tags = f'''    <meta property="og:title" content="{clean_title}">
    <meta property="og:description" content="{description[:120] if description else 'Appliance Repair Guide'}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="/blog/{filepath.stem}.html">
'''
            content = content[:insert_pos] + og_tags + content[insert_pos:]
            changes.append("OG_TAGS_ADDED")

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

def main():
    blog_base = Path("blog")
    folders = ["maintenance", "troubleshooting", "guides"]

    print("\n" + "="*80)
    print("ADDING SEO META TAGS TO ALL 57 POSTS")
    print("="*80 + "\n")

    total_posts = 0
    posts_modified = 0
    total_changes = {}

    for folder in folders:
        folder_path = blog_base / folder
        if not folder_path.exists():
            continue

        html_files = sorted([f for f in folder_path.glob('*.html')])
        print(f"[{folder.upper()}] - {len(html_files)} posts\n")

        for filepath in html_files:
            try:
                changes = add_seo_tags(filepath)
                total_posts += 1
                if changes:
                    posts_modified += 1
                    print(f"  UPDATED {filepath.name}")
                    for change in changes:
                        print(f"    + {change}")
                        total_changes[change] = total_changes.get(change, 0) + 1
                else:
                    print(f"  OK {filepath.name}")
            except Exception as e:
                print(f"  ERROR {filepath.name}: {str(e)}")

        print()

    print("="*80)
    print(f"Total Posts: {total_posts}")
    print(f"Posts Modified: {posts_modified}")
    print("\nChanges Applied:")
    for change, count in sorted(total_changes.items()):
        print(f"  {change}: {count} posts")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
