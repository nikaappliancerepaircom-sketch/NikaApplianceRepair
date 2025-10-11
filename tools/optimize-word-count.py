#!/usr/bin/env python3
"""
Optimize word count to 2500-3000 range
Remove excessive content while keeping quality
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

def count_words(text):
    """Count words in text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Count words
    words = text.split()
    return len(words)

def get_text_content(soup):
    """Get main text content"""
    # Remove script, style, nav, header, footer
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    main = soup.find('main') or soup.find('article') or soup.find('body')
    if main:
        return main.get_text()
    return soup.get_text()

def trim_paragraphs(soup, target_words, current_words):
    """Trim paragraphs to reach target word count"""
    if current_words <= target_words:
        return False

    words_to_remove = current_words - target_words
    removed = 0

    # Find main content
    main = soup.find('main') or soup.find('article')
    if not main:
        return False

    # Strategy: Remove every 4th paragraph until we reach target
    paragraphs = main.find_all('p')

    for i in range(len(paragraphs) - 1, -1, -1):
        if removed >= words_to_remove:
            break

        # Skip first 3 paragraphs (intro is important)
        if i < 3:
            continue

        # Skip paragraphs with strong tags (important content)
        if paragraphs[i].find('strong'):
            continue

        # Skip very short paragraphs
        p_text = paragraphs[i].get_text()
        p_words = len(p_text.split())
        if p_words < 15:
            continue

        # Remove if it's redundant
        if i % 4 == 0 or i > len(paragraphs) - 5:  # Remove every 4th or near end
            removed += p_words
            paragraphs[i].decompose()

    return removed > 0

def optimize_file(file_path):
    """Optimize word count of a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Get current word count
        text = get_text_content(BeautifulSoup(content, 'html.parser'))
        current_words = count_words(text)

        # Target range
        target_min = 2500
        target_max = 3000

        if target_min <= current_words <= target_max:
            print(f"[OK] {file_path.name}: {current_words} words (optimal)")
            return False

        if current_words < target_min:
            print(f"[SKIP] {file_path.name}: {current_words} words (too short, needs content)")
            return False

        # Trim to target (aim for 2750)
        target = 2750
        changed = trim_paragraphs(soup, target, current_words)

        if changed:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            # Verify new count
            new_text = get_text_content(soup)
            new_words = count_words(new_text)

            print(f"[OPTIMIZED] {file_path.name}: {current_words} -> {new_words} words")
            return True
        else:
            print(f"[SKIP] {file_path.name}: Could not optimize")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("OPTIMIZING WORD COUNT (Target: 2500-3000)")
    print("=" * 60)

    # Get all content pages
    all_files = []

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    optimized = 0
    for file_path in all_files:
        if optimize_file(file_path):
            optimized += 1

    print("\n" + "=" * 60)
    print(f"OPTIMIZED: {optimized}/{len(all_files)} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
