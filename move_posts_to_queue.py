#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Move all new blog posts to queue for daily publishing
"""

import os
import sys
import shutil
import glob

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Directories with new posts
SOURCE_DIRS = [
    'blog/troubleshooting',
    'blog/maintenance',
    'blog/cost-pricing',
    'blog/brands',
    'blog/seasonal',
    'blog/location'
]

QUEUE_DIR = 'blog/_queue'

# Create queue directory
os.makedirs(QUEUE_DIR, exist_ok=True)

print("=" * 70)
print("📦 MOVING BLOG POSTS TO QUEUE")
print("=" * 70)
print()

moved_count = 0

for source_dir in SOURCE_DIRS:
    if not os.path.exists(source_dir):
        continue

    # Get all HTML files in directory
    posts = glob.glob(f"{source_dir}/*.html")

    for post_path in posts:
        filename = os.path.basename(post_path)

        # Skip if it's an old post (published before today)
        # For now, move ALL posts from these directories
        dest_path = f"{QUEUE_DIR}/{filename}"

        # Move file
        try:
            shutil.move(post_path, dest_path)
            moved_count += 1
            print(f"✅ Moved: {filename}")
        except Exception as e:
            print(f"❌ Error moving {filename}: {e}")

print()
print("=" * 70)
print(f"🎉 Moved {moved_count} posts to queue")
print("=" * 70)
print()
print("Next step: Run 'python publish_daily_blogs.py' to publish first 5 posts")
