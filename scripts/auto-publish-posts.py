#!/usr/bin/env python3
"""
Auto-publish blog posts from drafts folder
Moves posts from /blog/_drafts/ to appropriate category folders
Supports date-based scheduling via article:published_time meta tag
"""
import os
import shutil
import argparse
import json
import re
from pathlib import Path
from datetime import datetime

def get_post_metadata(filepath):
    """Extract metadata from blog post HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {
        'filepath': filepath,
        'filename': os.path.basename(filepath),
        'category': 'posts',  # Default
        'title': '',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'publish_date': None  # For scheduled publishing
    }

    # Parse title
    if '<title>' in content:
        start = content.find('<title>') + 7
        end = content.find('</title>')
        metadata['title'] = content[start:end]

    # Parse scheduled publish date from multiple sources (in order of preference):
    # 1. article:published_time meta tag
    # 2. Jekyll front matter date
    # 3. Schema.org datePublished

    publish_match = re.search(r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})"', content)
    if publish_match:
        metadata['publish_date'] = publish_match.group(1)
        metadata['date'] = publish_match.group(1)
    else:
        # Check Jekyll front matter date (format: date: YYYY-MM-DD)
        frontmatter_match = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})["\']?', content, re.MULTILINE)
        if frontmatter_match:
            metadata['publish_date'] = frontmatter_match.group(1)
            metadata['date'] = frontmatter_match.group(1)
        else:
            # Check Schema.org datePublished
            schema_match = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', content)
            if schema_match:
                metadata['publish_date'] = schema_match.group(1)
                metadata['date'] = schema_match.group(1)

    # Parse category from canonical URL
    # Format: /blog/troubleshooting/slug or /blog/guides/slug
    canonical_match = re.search(r'<link rel="canonical" href="[^"]+/blog/([^/]+)/', content)
    if canonical_match:
        metadata['category'] = canonical_match.group(1)

    return metadata

def publish_posts(count=5, drafts_folder='blog/_drafts', dry_run=False, day=None, date_based=True):
    """
    Publish posts from drafts based on scheduled publish date

    Args:
        count: Number of posts to publish (only used if date_based=False)
        drafts_folder: Path to drafts folder
        dry_run: If True, don't actually move files
        day: If specified (e.g., 'day-1'), publish from that day's folder (legacy)
        date_based: If True, publish posts where publish_date <= today
    """
    base_dir = Path(__file__).parent.parent
    drafts_path = base_dir / drafts_folder
    today = datetime.now().strftime('%Y-%m-%d')

    if not drafts_path.exists():
        print(f"[INFO] Drafts folder not found: {drafts_path}")
        print("[INFO] Creating drafts folder...")
        drafts_path.mkdir(parents=True, exist_ok=True)
        return []

    # If day is specified, use day folder; otherwise get all .html files
    if day:
        day_path = drafts_path / day
        if not day_path.exists():
            print(f"[ERROR] Day folder not found: {day_path}")
            return []
        draft_posts = list(day_path.glob('*.html'))
    else:
        # Get all draft posts (excluding backup files, schedule file, and non-HTML files)
        draft_posts = []
        for file in drafts_path.glob('*.html'):
            if not file.name.endswith('.backup') and not file.name.startswith('_'):
                draft_posts.append(file)

    if not draft_posts:
        print(f"[INFO] No draft posts found in {drafts_folder}")
        return []

    # Filter by scheduled publish date if date_based is enabled
    if date_based:
        posts_ready = []
        for post in draft_posts:
            meta = get_post_metadata(post)
            publish_date = meta.get('publish_date')
            if publish_date and publish_date <= today:
                posts_ready.append((post, publish_date))
                print(f"[READY] {post.name} (scheduled: {publish_date})")
            elif publish_date:
                print(f"[SKIP] {post.name} (scheduled: {publish_date}, today: {today})")

        # Sort by publish date
        posts_ready.sort(key=lambda x: x[1])
        posts_to_publish = [p[0] for p in posts_ready[:count]]

        print(f"\n[INFO] Found {len(posts_ready)} posts ready for today ({today})")
    else:
        # Legacy mode: sort by filename and take first N
        draft_posts.sort()
        posts_to_publish = draft_posts[:count]

    published = []

    print(f"\n{'='*70}")
    print(f"PUBLISHING {len(posts_to_publish)} BLOG POSTS")
    print(f"{'='*70}\n")

    for post_path in posts_to_publish:
        metadata = get_post_metadata(post_path)

        # Determine destination folder based on category
        category_map = {
            'posts': 'blog/posts',
            'troubleshooting': 'blog/troubleshooting',
            'maintenance': 'blog/maintenance',
            'guides': 'blog/guides',
            'seasonal': 'blog/seasonal',
            'brands': 'blog/brands',
            'locations': 'blog/locations',
            'tips': 'blog/tips',
            'repair': 'blog/repair',
            'how-to': 'blog/how-to'
        }

        category = metadata.get('category', 'posts')
        dest_folder = base_dir / category_map.get(category, 'blog/posts')

        # Create destination folder if doesn't exist
        dest_folder.mkdir(parents=True, exist_ok=True)

        # Destination file path
        dest_file = dest_folder / metadata['filename']

        if dry_run:
            print(f"[DRY RUN] Would move: {post_path.name}")
            print(f"          To: {dest_file}")
        else:
            # Move file from drafts to category folder
            shutil.move(str(post_path), str(dest_file))
            print(f"[PUBLISHED] {metadata['filename']}")
            print(f"            Category: {category}")
            print(f"            Title: {metadata['title'][:60]}...")

        published.append({
            'filename': metadata['filename'],
            'title': metadata['title'],
            'category': category,
            'date': metadata['date'],
            'url': f"/{category_map.get(category, 'blog/posts')}/{metadata['filename'].replace('.html', '')}"
        })

    print(f"\n{'='*70}")
    print(f"[OK] Published {len(published)} posts successfully!")
    print(f"{'='*70}\n")

    # Save published posts log
    if published and not dry_run:
        log_file = base_dir / 'blog/_published_log.json'
        log_data = []

        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

        log_data.extend(published)

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)

    return published

def main():
    parser = argparse.ArgumentParser(description='Auto-publish blog posts from drafts')
    parser.add_argument('--count', type=int, default=1, help='Number of posts to publish per run (default: 1)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be published without actually moving files')
    parser.add_argument('--drafts-folder', default='blog/_drafts', help='Path to drafts folder')
    parser.add_argument('--day', default=None, help='Publish from specific day folder (legacy mode)')
    parser.add_argument('--no-date-check', action='store_true', help='Disable date-based scheduling')

    args = parser.parse_args()

    published = publish_posts(
        count=args.count,
        drafts_folder=args.drafts_folder,
        dry_run=args.dry_run,
        day=args.day,
        date_based=not args.no_date_check
    )

    if args.dry_run:
        print("\n[DRY RUN] No files were actually moved.")
        print("Run without --dry-run to publish posts.")

if __name__ == '__main__':
    main()
