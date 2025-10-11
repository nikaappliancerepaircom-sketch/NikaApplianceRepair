#!/usr/bin/env python3
"""
Remove voice-search-content blue FAQ section (duplicate/unnecessary)
"""

from pathlib import Path
from bs4 import BeautifulSoup

def remove_blue_section(file_path):
    """Remove voice-search-content section"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changes = []

    # Remove voice-search-content
    voice_sections = soup.find_all('div', class_='voice-search-content')
    for section in voice_sections:
        section.decompose()
        changes.append("removed blue FAQ")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("REMOVING BLUE FAQ SECTIONS")
    print("=" * 70)

    all_files = []

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        all_files.extend([f for f in services_dir.glob('*.html')])

    # Location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        all_files.extend([f for f in locations_dir.glob('*.html')])

    print(f"\nProcessing {len(all_files)} pages...\n")

    fixed = 0
    for file_path in all_files:
        changes = remove_blue_section(file_path)
        if changes:
            print(f"[REMOVED] {file_path.name}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"REMOVED FROM: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
