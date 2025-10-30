#!/usr/bin/env python3
"""
Auto-publish blog posts from drafts folder
Moves posts from /blog/_drafts/ to appropriate category folders
"""
import os
import shutil
import argparse
import json
from pathlib import Path
from datetime import datetime

def get_post_metadata(filepath):
    """Extract metadata from blog post HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract category from folder structure or meta tags
    # You can parse HTML meta tags or use folder naming
    metadata = {
        'filepath': filepath,
        'filename': os.path.basename(filepath),
        'category': 'troubleshooting',  # Default, can be parsed
        'title': '',  # Parse from <title> tag
        'date': datetime.now().strftime('%Y-%m-%d')
    }

    # Parse title
    if '<title>' in content:
        start = content.find('<title>') + 7
        end = content.find('</title>')
        metadata['title'] = content[start:end]

    # Parse category from file path or meta
    if 'data-category' in content:
        # Extract category from HTML
        pass

    return metadata

def publish_posts(count=5, drafts_folder='blog/_drafts', dry_run=False, day=None):
    """
    Publish specified number of posts from drafts

    Args:
        count: Number of posts to publish
        drafts_folder: Path to drafts folder
        dry_run: If True, don't actually move files
        day: If specified (e.g., 'day-1'), publish from that day's folder
    """
    base_dir = Path(__file__).parent.parent
    drafts_path = base_dir / drafts_folder

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
        # Get all draft posts (excluding backup files and non-HTML files)
        draft_posts = []
        for root, dirs, files in os.walk(drafts_path):
            for file in files:
                if file.endswith('.html') and not file.endswith('.backup'):
                    draft_posts.append(Path(root) / file)

    if not draft_posts:
        print(f"[INFO] No draft posts found in {drafts_folder}")
        return []

    # Sort by filename (assuming numbered or dated filenames)
    draft_posts.sort()

    # Limit to requested count
    posts_to_publish = draft_posts[:count]

    published = []

    print(f"\n{'='*70}")
    print(f"PUBLISHING {len(posts_to_publish)} BLOG POSTS")
    print(f"{'='*70}\n")

    for post_path in posts_to_publish:
        metadata = get_post_metadata(post_path)

        # Determine destination folder based on category
        category_map = {
            'troubleshooting': 'blog/troubleshooting',
            'maintenance': 'blog/maintenance',
            'guides': 'blog/guides',
            'seasonal': 'blog/seasonal',
            'brands': 'blog/brands',
            'locations': 'blog/locations'
        }

        category = metadata.get('category', 'troubleshooting')
        dest_folder = base_dir / category_map.get(category, 'blog/troubleshooting')

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
            'url': f"/{category_map[category]}/{metadata['filename'].replace('.html', '')}"
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
    parser.add_argument('--count', type=int, default=1, help='Number of posts to publish (default: 1 - for Vercel automation)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be published without actually moving files')
    parser.add_argument('--drafts-folder', default='blog/_drafts', help='Path to drafts folder')
    parser.add_argument('--day', default=None, help='Publish from specific day folder (e.g., day-1, day-2)')

    args = parser.parse_args()

    published = publish_posts(
        count=args.count,
        drafts_folder=args.drafts_folder,
        dry_run=args.dry_run,
        day=args.day
    )

    if args.dry_run:
        print("\n[DRY RUN] No files were actually moved.")
        print("Run without --dry-run to publish posts.")

if __name__ == '__main__':
    main()
