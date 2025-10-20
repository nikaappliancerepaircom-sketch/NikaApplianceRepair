#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish 5 Blog Posts Daily - Automated System
Moves posts from _queue to published directories + updates sitemap
"""

import os
import sys
import shutil
import glob
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
POSTS_PER_DAY = 5
QUEUE_DIR = "blog/_queue"
SITEMAP_FILE = "sitemap.xml"

def get_queued_posts():
    """Get all posts in queue directory"""
    if not os.path.exists(QUEUE_DIR):
        print(f"❌ Queue directory not found: {QUEUE_DIR}")
        return []

    posts = glob.glob(f"{QUEUE_DIR}/*.html")
    return sorted(posts)

def extract_category_from_post(filepath):
    """Extract category from post filename or content"""
    # Read first few lines to find category
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(500)  # Read first 500 chars

    # Look for category in canonical URL
    if 'blog/troubleshooting/' in content:
        return 'troubleshooting'
    elif 'blog/maintenance/' in content:
        return 'maintenance'
    elif 'blog/cost-pricing/' in content:
        return 'cost-pricing'
    elif 'blog/brands/' in content:
        return 'brands'
    elif 'blog/seasonal/' in content:
        return 'seasonal'
    elif 'blog/location/' in content:
        return 'location'
    else:
        return 'general'

def publish_posts(posts_to_publish):
    """Move posts from queue to their category directories"""
    published = []

    for post_path in posts_to_publish:
        filename = os.path.basename(post_path)
        category = extract_category_from_post(post_path)

        # Create category directory if doesn't exist
        category_dir = f"blog/{category}"
        os.makedirs(category_dir, exist_ok=True)

        # Destination path
        dest_path = f"{category_dir}/{filename}"

        # Move file
        shutil.move(post_path, dest_path)
        published.append(dest_path)
        print(f"✅ Published: {dest_path}")

    return published

def update_sitemap(published_posts):
    """Add published posts to sitemap.xml"""

    # Read existing sitemap
    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()

    # Find insert position (before closing </urlset>)
    insert_position = sitemap_content.rfind('</urlset>')

    # Generate URL entries
    today = datetime.now().strftime('%Y-%m-%d')
    new_urls = []

    for post_path in published_posts:
        # Convert path to URL (remove .html extension)
        url_path = post_path.replace('\\', '/').replace('.html', '')

        url_entry = f'''  <url>
    <loc>https://nikaappliancerepair.com/{url_path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
        new_urls.append(url_entry)

    # Insert new URLs
    all_new_urls = '\n'.join(new_urls)
    new_sitemap = sitemap_content[:insert_position] + all_new_urls + sitemap_content[insert_position:]

    # Write updated sitemap
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(new_sitemap)

    print(f"\n✅ Updated sitemap with {len(published_posts)} new posts")

def main():
    print("=" * 70)
    print("📅 DAILY BLOG PUBLISHING - 5 POSTS/DAY")
    print("=" * 70)
    print()

    # Get queued posts
    queued_posts = get_queued_posts()

    if not queued_posts:
        print("📭 No posts in queue. All done!")
        return

    print(f"📊 Posts in queue: {len(queued_posts)}")
    print(f"📤 Publishing today: {min(POSTS_PER_DAY, len(queued_posts))} posts")
    print()

    # Select posts to publish today
    posts_to_publish = queued_posts[:POSTS_PER_DAY]

    # Publish posts
    published = publish_posts(posts_to_publish)

    # Update sitemap
    update_sitemap(published)

    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Published: {len(published)} posts")
    print(f"📭 Remaining in queue: {len(queued_posts) - len(published)}")
    print(f"📅 Days until completion: {(len(queued_posts) - len(published) + POSTS_PER_DAY - 1) // POSTS_PER_DAY}")
    print()
    print("Next steps:")
    print("1. Review published posts")
    print("2. Run: git add blog/ sitemap.xml")
    print("3. Run: git commit -m 'Publish 5 daily blog posts'")
    print("4. Run: git push")
    print("5. Run this script again tomorrow!")

if __name__ == "__main__":
    main()
