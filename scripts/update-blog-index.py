#!/usr/bin/env python3
"""
Update blog.html index page with all published posts
Scans all blog category folders and updates the blog index
"""
import os
from pathlib import Path
from datetime import datetime
import re

def extract_post_data(filepath):
    """Extract post data from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title = ''
    if '<title>' in content:
        start = content.find('<title>') + 7
        end = content.find('</title>')
        title = content[start:end].replace(' | Nika Appliance Repair', '')

    # Extract meta description (for excerpt)
    excerpt = ''
    if 'name="description"' in content:
        match = re.search(r'name="description"\s+content="([^"]+)"', content)
        if match:
            excerpt = match.group(1)[:150] + '...'

    # Extract quick answer (if available)
    quick_answer = ''
    if '<div class="quick-answer">' in content:
        match = re.search(r'<div class="quick-answer">.*?<strong>Quick Answer:</strong>(.*?)</div>', content, re.DOTALL)
        if match:
            # Clean HTML tags
            quick_answer = re.sub(r'<[^>]+>', '', match.group(1)).strip()[:200]

    # Get publish date from file modified time
    modified_timestamp = os.path.getmtime(filepath)
    date_published = datetime.fromtimestamp(modified_timestamp).strftime('%B %d, %Y')

    # Extract reading time from content (estimate)
    word_count = len(re.findall(r'\b\w+\b', content))
    reading_time = max(1, word_count // 200)  # Average reading speed: 200 words/min

    return {
        'title': title,
        'excerpt': excerpt or quick_answer[:150] + '...',
        'date': date_published,
        'reading_time': reading_time
    }

def get_category_emoji(category):
    """Get emoji for category"""
    emoji_map = {
        'troubleshooting': '🔧',
        'maintenance': '🛠️',
        'guides': '📚',
        'seasonal': '🌤️',
        'brands': '🏷️',
        'locations': '📍'
    }
    return emoji_map.get(category, '📝')

def generate_post_card(category, slug, post_data):
    """Generate HTML for a post card"""
    emoji = get_category_emoji(category)

    card_html = f'''
            <!-- {post_data['title']} -->
            <a href="/blog/{category}/{slug}" class="post-card" data-category="{category}">
                <div class="post-image">{emoji}</div>
                <div class="post-content">
                    <span class="post-category">{category.capitalize()}</span>
                    <h3>{post_data['title']}</h3>
                    <p>{post_data['excerpt'][:120]}...</p>
                    <div class="post-meta">
                        <span>{post_data['date']}</span>
                        <span>{post_data['reading_time']} min read</span>
                    </div>
                </div>
            </a>
'''

    return card_html

def update_blog_index():
    """Update blog.html with all published posts"""
    base_dir = Path(__file__).parent.parent
    blog_index_path = base_dir / 'blog.html'

    print("=" * 70)
    print("UPDATING BLOG INDEX")
    print("=" * 70)
    print()

    # Read current blog.html
    if not blog_index_path.exists():
        print("[ERROR] blog.html not found!")
        return False

    with open(blog_index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Scan all blog posts
    blog_dir = base_dir / 'blog'
    blog_categories = ['troubleshooting', 'maintenance', 'guides', 'seasonal', 'brands', 'locations']

    all_posts = []

    for category in blog_categories:
        category_dir = blog_dir / category
        if category_dir.exists():
            category_count = 0
            for post_file in sorted(category_dir.glob('*.html'), reverse=True):  # Newest first
                post_data = extract_post_data(post_file)
                post_card_html = generate_post_card(category, post_file.stem, post_data)
                all_posts.append(post_card_html)
                category_count += 1

            if category_count > 0:
                print(f"[+] Found {category_count} posts in {category}")

    print(f"\n[TOTAL] {len(all_posts)} blog posts found")

    if not all_posts:
        print("\n[INFO] No blog posts found to add")
        return True

    # Generate posts grid HTML
    posts_grid_html = '\n'.join(all_posts)

    # Find and replace the posts grid section
    # Looking for: <div class="posts-grid">...</div>
    # The pattern should match from "<!-- Posts Grid -->" to the closing </div>
    pattern = r'(<!-- Posts Grid -->\s*<div class="posts-grid">)(.*?)(</div>)'

    replacement = rf'\1\n{posts_grid_html}\n        \3'

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("\n[WARNING] Could not find posts-grid section to update")
        print("[ERROR] Pattern not found in blog.html!")
        return False

    # Write updated content
    with open(blog_index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n[OK] Blog index updated successfully!")
    print(f"     Location: {blog_index_path}")
    print(f"     Total posts: {len(all_posts)}")
    print("=" * 70)

    return True

def main():
    """Main function"""
    update_blog_index()

if __name__ == '__main__':
    main()
