#!/usr/bin/env python3
"""
Make area-item grid items clickable
Add links to locations that have pages
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

# Map of location names to their HTML files
LOCATION_MAP = {
    'Ajax': 'ajax.html',
    'Aurora': 'aurora.html',
    'Barrie': 'barrie.html',
    'Bolton': 'bolton.html',
    'Brampton': 'brampton.html',
    'Burlington': 'burlington.html',
    'Caledon': 'caledon.html',
    'Concord': 'concord.html',
    'East Gwillimbury': 'east-gwillimbury.html',
    'Etobicoke': 'etobicoke.html',
    'Georgetown': 'georgetown.html',
    'King City': 'king-city.html',
    'Maple': 'maple.html',
    'Markham': 'markham.html',
    'Milton': 'milton.html',
    'Mississauga': 'mississauga.html',
    'Newmarket': 'newmarket.html',
    'North York': 'north-york.html',
    'Oakville': 'oakville.html',
    'Oshawa': 'oshawa.html',
    'Pickering': 'pickering.html',
    'Richmond Hill': 'richmond-hill.html',
    'Scarborough': 'scarborough.html',
    'Stouffville': 'stouffville.html',
    'Thornhill': 'thornhill.html',
    'Toronto': 'toronto.html',
    'Uxbridge': 'uxbridge.html',
    'Vaughan': 'vaughan.html',
    'Whitby': 'whitby.html',
    'Woodbridge': 'woodbridge.html',
}

def make_area_items_clickable(file_path):
    """Add links to area-items that have corresponding pages"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        changed = False

        # Find all area-item divs
        area_items = soup.find_all('div', class_='area-item')

        for item in area_items:
            # Skip if already has a link
            if item.find('a'):
                continue

            # Get text content (remove emoji)
            text = item.get_text().strip()
            text = re.sub(r'[📍🏠🌆]', '', text).strip()

            # Check if we have a page for this location
            if text in LOCATION_MAP:
                # Determine path prefix
                if 'services' in str(file_path) or 'blog' in str(file_path):
                    link = f'../locations/{LOCATION_MAP[text]}'
                elif 'locations' in str(file_path):
                    link = f'{LOCATION_MAP[text]}'
                else:  # index.html
                    link = f'/locations/{LOCATION_MAP[text]}'

                # Wrap content in link
                a_tag = soup.new_tag('a',
                                    href=link,
                                    style='text-decoration: none; color: inherit; display: block; height: 100%;')

                # Move text into link
                original_text = item.get_text()
                item.clear()
                a_tag.string = original_text
                item.append(a_tag)

                changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True

        return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("MAKING AREA ITEMS CLICKABLE")
    print("=" * 60)

    # Get all HTML files
    all_files = []
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    print(f"\nProcessing {len(all_files)} pages...")
    print(f"Adding links for {len(LOCATION_MAP)} locations")
    print("=" * 60)

    updated = 0
    for file_path in all_files:
        if make_area_items_clickable(file_path):
            print(f"[UPDATED] {file_path.name}")
            updated += 1
        else:
            print(f"[OK] {file_path.name}")

    print("\n" + "=" * 60)
    print(f"UPDATED: {updated}/{len(all_files)} files")
    print("=" * 60)
    print(f"\nArea items for {len(LOCATION_MAP)} locations are now clickable!")

if __name__ == '__main__':
    main()
