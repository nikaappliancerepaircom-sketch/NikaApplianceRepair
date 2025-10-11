#!/usr/bin/env python3
"""
Cleanup script:
1. Remove rating-display section (added by BMAD fixes)
2. Update diagnostic cost to $119
3. Videos already match main page (same links)
4. Hero animations already exist (floating icons)
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def cleanup_page(file_path):
    """Remove unnecessary sections and update pricing"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changes = []

    # 1. Remove rating-display section (BMAD added this, not needed)
    rating_display = soup.find('div', class_='rating-display')
    if rating_display:
        rating_display.decompose()
        changes.append("removed rating-display section")

    # 2. Update diagnostic cost to $119
    # Find pricing mentions
    content_str = str(soup)
    if 'free diagnostic' in content_str.lower():
        # Replace with $119 diagnostic
        content_str = re.sub(
            r'free\s+diagnostic(s)?',
            r'$119 diagnostic fee (waived with repair)',
            content_str,
            flags=re.IGNORECASE
        )
        soup = BeautifulSoup(content_str, 'html.parser')
        changes.append("updated diagnostic to $119")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("CLEANUP UNNECESSARY SECTIONS")
    print("=" * 70)
    print("\nRemoving:")
    print("  1. Rating-display sections (not needed)")
    print("  2. Updating diagnostic cost to $119")
    print("=" * 70)

    all_files = []

    # Collect HTML files
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html')])

    print(f"\nProcessing {len(all_files)} files...\n")

    fixed = 0
    for file_path in all_files:
        if not file_path.exists():
            continue

        changes = cleanup_page(file_path)
        if changes:
            print(f"[FIXED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"CLEANED: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
