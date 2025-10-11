#!/usr/bin/env python3
"""
Sync YouTube video URLs from index.html to all other pages
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def get_youtube_urls_from_index():
    """Extract YouTube video IDs from index.html"""
    base_dir = Path(__file__).parent.parent
    index_file = base_dir / 'index.html'

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all YouTube embed URLs
    pattern = r'youtube\.com/embed/([a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, content)

    # Extract unique video IDs (in order)
    video_ids = []
    seen = set()
    for match in matches:
        if match not in seen:
            video_ids.append(match)
            seen.add(match)

    return video_ids

def replace_youtube_videos(file_path, video_ids):
    """Replace YouTube video IDs in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        soup = BeautifulSoup(content, 'html.parser')

        # Find all YouTube iframes
        iframes = soup.find_all('iframe', src=re.compile('youtube'))

        if not iframes:
            return False

        # Replace video IDs
        for i, iframe in enumerate(iframes):
            src = iframe.get('src', '')

            # Determine which video ID to use
            # First iframe = first video (story), rest = testimonials
            if i == 0 and len(video_ids) > 0:
                new_video_id = video_ids[0]  # Story video
            elif i > 0 and len(video_ids) > 1:
                # Cycle through testimonial videos (skip first which is story)
                testimonial_index = ((i - 1) % (len(video_ids) - 1)) + 1
                new_video_id = video_ids[testimonial_index]
            else:
                continue

            # Replace video ID in src
            new_src = re.sub(r'embed/[a-zA-Z0-9_-]+', f'embed/{new_video_id}', src)
            iframe['src'] = new_src

        # Write back
        new_content = str(soup)
        if new_content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("SYNCING YOUTUBE VIDEOS FROM INDEX.HTML")
    print("=" * 60)

    # Get video IDs from index
    video_ids = get_youtube_urls_from_index()
    print(f"\nFound {len(video_ids)} YouTube videos on index.html:")
    for i, vid in enumerate(video_ids, 1):
        print(f"  {i}. https://www.youtube.com/watch?v={vid}")

    # Get all HTML files (except index)
    all_files = []

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    print(f"\nReplacing videos on {len(all_files)} pages...")
    print("=" * 60)

    updated = 0
    for file_path in all_files:
        if replace_youtube_videos(file_path, video_ids):
            print(f"[UPDATED] {file_path.name}")
            updated += 1
        else:
            print(f"[OK] {file_path.name}")

    print("\n" + "=" * 60)
    print(f"UPDATED: {updated}/{len(all_files)} files")
    print("=" * 60)
    print("\nAll pages now use the same YouTube videos as index.html")

if __name__ == '__main__':
    main()
