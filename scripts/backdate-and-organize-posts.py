#!/usr/bin/env python3
"""
Backdate and Organize Blog Posts
- Backdates 10 posts to Oct-Nov 2025 (moves to posts/)
- Schedules 10 posts for Dec 6-25, 2025 (stays in _drafts)
- Updates sitemap.xml
- Updates blog index
"""

import os
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DRAFTS_DIR = ROOT_DIR / "blog" / "_drafts"
POSTS_DIR = ROOT_DIR / "blog" / "posts"
SITEMAP_PATH = ROOT_DIR / "sitemap.xml"

# Today's date
TODAY = datetime(2025, 12, 5)

# Generate dates for backdated posts (Oct 15 - Nov 30, every ~4-5 days)
BACKDATE_DATES = [
    datetime(2025, 10, 15),
    datetime(2025, 10, 20),
    datetime(2025, 10, 26),
    datetime(2025, 11, 1),
    datetime(2025, 11, 6),
    datetime(2025, 11, 12),
    datetime(2025, 11, 17),
    datetime(2025, 11, 22),
    datetime(2025, 11, 26),
    datetime(2025, 11, 30),
]

# Generate dates for future posts (Dec 6 - Dec 25, every 2 days)
FUTURE_DATES = [
    datetime(2025, 12, 6),
    datetime(2025, 12, 8),
    datetime(2025, 12, 10),
    datetime(2025, 12, 12),
    datetime(2025, 12, 14),
    datetime(2025, 12, 16),
    datetime(2025, 12, 18),
    datetime(2025, 12, 20),
    datetime(2025, 12, 22),
    datetime(2025, 12, 24),
]

def get_all_drafts():
    """Get all HTML files in _drafts (excluding schedule file)"""
    drafts = []
    for f in DRAFTS_DIR.glob("*.html"):
        if not f.name.startswith("_"):
            drafts.append(f)
    return sorted(drafts, key=lambda x: x.name)

def update_post_date(filepath, new_date):
    """Update the article:published_time in the HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    date_str = new_date.strftime("%Y-%m-%d")

    # Update article:published_time
    content = re.sub(
        r'<meta property="article:published_time" content="[^"]*">',
        f'<meta property="article:published_time" content="{date_str}">',
        content
    )

    # Also update any datePublished in JSON-LD schema
    content = re.sub(
        r'"datePublished":\s*"[^"]*"',
        f'"datePublished": "{date_str}"',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return date_str

def move_to_posts(filepath):
    """Move file from _drafts to posts"""
    dest = POSTS_DIR / filepath.name
    shutil.move(str(filepath), str(dest))
    return dest

def update_sitemap(published_posts):
    """Add published posts to sitemap.xml"""
    with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the closing </urlset> tag
    insert_pos = content.rfind('</urlset>')

    new_entries = ""
    for post_name, date in published_posts:
        slug = post_name.replace('.html', '')
        date_str = date.strftime("%Y-%m-%d")
        new_entries += f"""  <url>
    <loc>https://nikaappliancerepair.com/blog/posts/{slug}.html</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""

    # Insert before </urlset>
    content = content[:insert_pos] + new_entries + content[insert_pos:]

    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def update_post_schedule(future_posts):
    """Update _post_schedule.txt with future posts"""
    schedule_path = DRAFTS_DIR / "_post_schedule.txt"

    lines = ["# Blog Post Publishing Schedule",
             "# Format: YYYY-MM-DD | filename.html",
             "# Posts are published daily at 9:00 AM Toronto time",
             ""]

    for post_name, date in future_posts:
        date_str = date.strftime("%Y-%m-%d")
        lines.append(f"{date_str} | {post_name}")

    with open(schedule_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    print("=" * 60)
    print("BACKDATE AND ORGANIZE BLOG POSTS")
    print("=" * 60)

    # Create posts directory if needed
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    # Get all drafts
    drafts = get_all_drafts()
    print(f"\nFound {len(drafts)} draft posts")

    if len(drafts) != 20:
        print(f"WARNING: Expected 20 posts, found {len(drafts)}")

    # Split into backdated (first 10) and future (last 10)
    backdated_drafts = drafts[:10]
    future_drafts = drafts[10:]

    published_posts = []
    future_posts = []

    # Process backdated posts
    print("\n" + "-" * 40)
    print("BACKDATING POSTS (moving to posts/)")
    print("-" * 40)

    for i, draft in enumerate(backdated_drafts):
        date = BACKDATE_DATES[i]
        date_str = update_post_date(draft, date)
        new_path = move_to_posts(draft)
        published_posts.append((draft.name, date))
        print(f"  [{date_str}] {draft.name} -> posts/")

    # Process future posts
    print("\n" + "-" * 40)
    print("SCHEDULING FUTURE POSTS (staying in _drafts)")
    print("-" * 40)

    for i, draft in enumerate(future_drafts):
        date = FUTURE_DATES[i]
        date_str = update_post_date(draft, date)
        future_posts.append((draft.name, date))
        print(f"  [{date_str}] {draft.name}")

    # Update sitemap
    print("\n" + "-" * 40)
    print("UPDATING SITEMAP")
    print("-" * 40)
    update_sitemap(published_posts)
    print(f"  Added {len(published_posts)} posts to sitemap.xml")

    # Update schedule
    print("\n" + "-" * 40)
    print("UPDATING POST SCHEDULE")
    print("-" * 40)
    update_post_schedule(future_posts)
    print(f"  Scheduled {len(future_posts)} posts for future publishing")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Published (backdated): {len(published_posts)} posts")
    print(f"  Scheduled (future):    {len(future_posts)} posts")
    print(f"  Date range: Oct 15 - Dec 24, 2025")
    print("\nDone!")

if __name__ == "__main__":
    main()
