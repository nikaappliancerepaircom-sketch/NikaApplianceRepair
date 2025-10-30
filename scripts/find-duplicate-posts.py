#!/usr/bin/env python3
"""Find duplicate or very similar blog posts"""
import re
from pathlib import Path
from difflib import SequenceMatcher

def extract_body_text(filepath):
    """Extract just the article body text (no HTML)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:1000]  # First 1000 chars for comparison

def get_title(filepath):
    """Extract post title"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    return match.group(1) if match else filepath.name

def main():
    blog_base = Path("blog")
    folders = ["troubleshooting", "maintenance", "guides"]

    print("\n" + "="*80)
    print("DUPLICATE POST DETECTION")
    print("="*80 + "\n")

    all_posts = []
    for folder in folders:
        folder_path = blog_base / folder
        if folder_path.exists():
            for filepath in sorted(folder_path.glob('*.html')):
                all_posts.append({
                    'path': filepath,
                    'folder': folder,
                    'name': filepath.name,
                    'title': get_title(filepath),
                    'text': extract_body_text(filepath)
                })

    print(f"Total posts scanned: {len(all_posts)}\n")

    # Check for same title
    print("[CHECKING TITLES]")
    titles = {}
    for post in all_posts:
        if post['title'] not in titles:
            titles[post['title']] = []
        titles[post['title']].append((post['folder'], post['name']))
    
    title_dups = {t: posts for t, posts in titles.items() if len(posts) > 1}
    
    if title_dups:
        print("[ALERT] POSTS WITH SAME TITLE:\n")
        for title, posts in sorted(title_dups.items()):
            print(f"Title: {title[:60]}...")
            for folder, name in posts:
                print(f"  - [{folder}] {name}")
            print()
    else:
        print("[OK] All posts have unique titles\n")

    # Check similar content
    print("[CHECKING SIMILAR CONTENT]")
    threshold = 0.90
    found = False
    
    for i, post1 in enumerate(all_posts):
        for post2 in all_posts[i+1:]:
            ratio = SequenceMatcher(None, post1['text'], post2['text']).ratio()
            if ratio > threshold:
                found = True
                print(f"[DUPLICATE] {ratio*100:.0f}% similar")
                print(f"  1. [{post1['folder']}] {post1['name']}")
                print(f"  2. [{post2['folder']}] {post2['name']}\n")
    
    if not found:
        print("[OK] No similar posts found (>90% match)\n")

    print("="*80 + "\n")

if __name__ == '__main__':
    main()
