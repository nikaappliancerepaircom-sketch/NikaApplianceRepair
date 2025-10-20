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

def publish_posts(count=5, drafts_folder='blog/_drafts', dry_run=False):
    """
    Publish specified number of posts from drafts

    Args:
        count: Number of posts to publish
        drafts_folder: Path to drafts folder
        dry_run: If True, don't actually move files
    """
    base_dir = Path(__file__).parent.parent
    drafts_path = base_dir / drafts_folder

    if not drafts_path.exists():
        print(f"[INFO] Drafts folder not found: {drafts_path}")
        print("[INFO] Creating drafts folder...")
        drafts_path.mkdir(parents=True, exist_ok=True)
        return []

    # Get all draft posts
    draft_posts = list(drafts_path.glob('*.html'))

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
    print(f"✅ Published {len(published)} posts successfully!")
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
    parser.add_argument('--count', type=int, default=5, help='Number of posts to publish (default: 5)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be published without actually moving files')
    parser.add_argument('--drafts-folder', default='blog/_drafts', help='Path to drafts folder')

    args = parser.parse_args()

    published = publish_posts(
        count=args.count,
        drafts_folder=args.drafts_folder,
        dry_run=args.dry_run
    )

    if args.dry_run:
        print("\n[DRY RUN] No files were actually moved.")
        print("Run without --dry-run to publish posts.")

if __name__ == '__main__':
    main()
