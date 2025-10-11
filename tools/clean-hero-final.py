#!/usr/bin/env python3
"""
Final hero cleanup:
1. Remove hero-rating div (stars and 4.9 rating)
2. Remove hero-trust-text
3. Center pricing table
"""

from pathlib import Path
from bs4 import BeautifulSoup

def clean_hero_final(file_path):
    """Clean hero section and center pricing"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changes = []

    # 1. Remove hero-rating div
    hero_rating = soup.find_all('div', class_='hero-rating')
    for rating in hero_rating:
        rating.decompose()
        changes.append("removed hero rating")

    # 2. Remove hero-trust-text
    trust_text = soup.find_all('p', class_='hero-trust-text')
    for text in trust_text:
        text.decompose()
        changes.append("removed trust text")

    # 3. Center pricing section
    pricing_headers = soup.find_all('h3', string=lambda s: s and 'Transparent Pricing' in s)
    for header in pricing_headers:
        # Add center style to header
        if header.get('style'):
            header['style'] = header['style'] + '; text-align: center;'
        else:
            header['style'] = 'text-align: center;'

        # Find parent div and center it
        parent = header.find_parent('div')
        if parent:
            if parent.get('style'):
                parent['style'] = parent['style'] + '; text-align: center;'
            else:
                parent['style'] = 'text-align: center;'
            changes.append("centered pricing")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FINAL HERO CLEANUP")
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
        changes = clean_hero_final(file_path)
        if changes:
            print(f"[CLEANED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"CLEANED: {fixed}/{len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
