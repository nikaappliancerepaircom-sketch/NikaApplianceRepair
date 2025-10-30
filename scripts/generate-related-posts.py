#!/usr/bin/env python3
"""
Generate related posts based on:
1. Same category (maintenance, troubleshooting, guides)
2. Similar keywords
3. Popular posts in category
"""
import re
from pathlib import Path
from collections import defaultdict

def get_post_info(filepath):
    """Extract post info: title, category, keywords"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else "Post"
    title = re.sub(r'\s*-\s*Nika Appliance Repair\s*$', '', title).strip()

    # Get keywords
    kw_match = re.search(r'<meta name="keywords" content="([^"]+)"', content)
    keywords = kw_match.group(1).split(',') if kw_match else []
    keywords = [kw.strip().lower() for kw in keywords]

    # Determine category from path
    category = "maintenance"
    if "troubleshooting" in str(filepath):
        category = "troubleshooting"
    elif "guides" in str(filepath):
        category = "guides"

    return {
        'path': filepath,
        'filename': filepath.name,
        'title': title,
        'category': category,
        'keywords': keywords
    }

def find_related_posts(post_info, all_posts, limit=3):
    """Find related posts based on category and keywords"""
    related = []

    # First, find posts in same category (excluding self)
    same_category = [
        p for p in all_posts
        if p['category'] == post_info['category'] and p['filename'] != post_info['filename']
    ]

    # Score by keyword similarity
    scored = []
    for candidate in same_category:
        # Count matching keywords
        matches = len(set(post_info['keywords']) & set(candidate['keywords']))
        scored.append((matches, candidate))

    # Sort by match count (descending) and take top N
    scored.sort(reverse=True, key=lambda x: x[0])
    related = [p[1] for p in scored[:limit]]

    # If not enough, add from other categories
    if len(related) < limit:
        other_category = [
            p for p in all_posts
            if p['category'] != post_info['category'] and p['filename'] != post_info['filename']
        ]
        for candidate in other_category:
            if len(related) >= limit:
                break
            if candidate not in related:
                matches = len(set(post_info['keywords']) & set(candidate['keywords']))
                if matches > 0:  # At least one matching keyword
                    related.append(candidate)

    return related[:limit]

def generate_related_posts_html(related_posts):
    """Generate HTML for related posts section"""
    if not related_posts:
        return None

    html = ''
    for post in related_posts:
        # Convert filename to URL path
        url = f"/blog/{post['category']}/{post['filename']}"
        html += f'''                <div class="related-post">
                    <a href="{url}">{post['title']}</a>
                    <div class="related-post-meta"><i class="far fa-calendar"></i> Oct 30, 2025</div>
                </div>
'''

    return html

def update_related_posts(filepath, related_html):
    """Replace the related posts widget content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: <div class="related-widget">...<div class="related-post">..content..</div>...</div>
    pattern = r'(<div class="related-widget">\s*<h3>Related Posts</h3>)([\s\S]*?)(?=\s*</div>\s*</aside>)'

    if re.search(pattern, content):
        new_section = r'\1\n' + related_html
        content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    blog_base = Path("blog")
    folders = ["maintenance", "troubleshooting", "guides"]

    print("\n" + "="*80)
    print("GENERATING RELATED POSTS FOR ALL 57 POSTS")
    print("="*80 + "\n")

    # First pass: collect all post info
    all_posts = []
    for folder in folders:
        folder_path = blog_base / folder
        if folder_path.exists():
            for filepath in sorted(folder_path.glob('*.html')):
                post_info = get_post_info(filepath)
                all_posts.append(post_info)

    print(f"Total posts found: {len(all_posts)}\n")

    # Second pass: generate and update related posts
    total_updated = 0
    total_failed = 0

    for folder in folders:
        folder_path = blog_base / folder
        if not folder_path.exists():
            continue

        html_files = sorted([f for f in folder_path.glob('*.html')])
        print(f"[{folder.upper()}] - {len(html_files)} posts\n")

        for filepath in html_files:
            try:
                # Get post info
                post_info = get_post_info(filepath)

                # Find related posts
                related = find_related_posts(post_info, all_posts, limit=3)

                if not related:
                    print(f"  SKIP {filepath.name} (no related posts found)")
                    continue

                # Generate HTML
                related_html = generate_related_posts_html(related)

                # Update file
                if update_related_posts(filepath, related_html):
                    print(f"  OK {filepath.name} (3 related posts)")
                    total_updated += 1
                else:
                    print(f"  ERROR {filepath.name} (could not update)")
                    total_failed += 1

            except Exception as e:
                print(f"  ERROR {filepath.name}: {str(e)[:60]}")
                total_failed += 1

        print()

    print("="*80)
    print(f"Total Updated: {total_updated}")
    print(f"Total Failed: {total_failed}")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
