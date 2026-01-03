#!/usr/bin/env python3
"""
Fix draft blog posts for auto-publishing
- Adds article:published_time meta tag if missing
- Sets scheduled publish dates starting from tomorrow
"""
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

def fix_draft_posts():
    base_dir = Path(__file__).parent.parent
    drafts_path = base_dir / 'blog' / '_drafts'

    # Get all draft posts
    draft_files = sorted(drafts_path.glob('*.html'))

    if not draft_files:
        print("[INFO] No draft files found")
        return

    # Start date is tomorrow (2026-01-04)
    start_date = datetime(2026, 1, 4)

    print("=" * 70)
    print("FIXING DRAFT POSTS FOR AUTO-PUBLISHING")
    print("=" * 70)
    print(f"\nFound {len(draft_files)} draft posts")
    print(f"Starting publish date: {start_date.strftime('%Y-%m-%d')}")
    print("-" * 70)

    posts_fixed = []
    date_idx = 0

    for draft_file in draft_files:
        with open(draft_file, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = draft_file.name
        needs_fix = False
        changes = []

        # Check for article:published_time meta tag
        has_publish_time = 'article:published_time' in content

        if has_publish_time:
            # Extract existing date
            match = re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})"', content)
            if match:
                existing_date = match.group(1)
                print(f"[OK] {filename} - Already has publish date: {existing_date}")
                continue

        # Calculate publish date for this post
        publish_date = start_date + timedelta(days=date_idx)
        date_str = publish_date.strftime('%Y-%m-%d')
        date_idx += 1

        # Add article:published_time meta tag after og:type or og:url
        if 'og:type' in content:
            # Add after og:type meta tag
            pattern = r'(<meta property="og:type" content="[^"]*">)'
            replacement = r'\1\n    <meta property="article:published_time" content="' + date_str + '">'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                needs_fix = True
                changes.append(f"Added article:published_time: {date_str}")
                content = new_content
        elif 'og:url' in content:
            # Add after og:url meta tag
            pattern = r'(<meta property="og:url" content="[^"]*">)'
            replacement = r'\1\n    <meta property="article:published_time" content="' + date_str + '">'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                needs_fix = True
                changes.append(f"Added article:published_time: {date_str}")
                content = new_content
        elif '<head>' in content:
            # Fallback: add near beginning of head
            pattern = r'(<meta name="viewport"[^>]*>)'
            replacement = r'\1\n    <meta property="article:published_time" content="' + date_str + '">'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                needs_fix = True
                changes.append(f"Added article:published_time: {date_str}")
                content = new_content

        # Also update Schema.org datePublished if present
        if '"datePublished":' in content:
            pattern = r'"datePublished":\s*"[^"]*"'
            replacement = f'"datePublished": "{date_str}"'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                changes.append(f"Updated Schema.org datePublished")

        # Update dateModified too
        if '"dateModified":' in content:
            pattern = r'"dateModified":\s*"[^"]*"'
            replacement = f'"dateModified": "{date_str}"'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content

        # Update front matter date if present
        if content.startswith('---'):
            pattern = r'^date:\s*["\']?\d{4}-\d{2}-\d{2}["\']?'
            replacement = f'date: {date_str}'
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            if new_content != content:
                content = new_content
                changes.append(f"Updated front matter date")

        if needs_fix:
            # Write fixed content back
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[FIXED] {filename}")
            for change in changes:
                print(f"        - {change}")
            posts_fixed.append(filename)
        else:
            print(f"[SKIP] {filename} - Could not add publish date")

    print("-" * 70)
    print(f"\nSummary: Fixed {len(posts_fixed)} posts")

    if posts_fixed:
        print("\nPublish Schedule:")
        date_idx = 0
        for draft_file in sorted(drafts_path.glob('*.html')):
            with open(draft_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})"', content)
            if match:
                print(f"  {match.group(1)}: {draft_file.name}")

    print("=" * 70)

if __name__ == '__main__':
    fix_draft_posts()
