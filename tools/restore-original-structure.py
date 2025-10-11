#!/usr/bin/env python3
"""
Restore original structure from index.html to all other pages
Insert all sections between Hero and Footer
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def extract_sections_from_index():
    """Extract all sections between Hero and Footer from index.html"""
    base_dir = Path(__file__).parent.parent
    index_file = base_dir / 'index.html'

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Find hero section
    hero = soup.find('section', class_='hero-section')
    if not hero:
        print("[ERROR] Hero section not found in index.html")
        return None

    # Find footer
    footer = soup.find('footer', class_='main-footer')
    if not footer:
        print("[ERROR] Footer not found in index.html")
        return None

    # Get all sections between hero and footer
    sections = []
    current = hero.find_next_sibling()

    while current and current != footer:
        if current.name == 'section':
            sections.append(str(current))
        current = current.find_next_sibling()

    print(f"[INFO] Extracted {len(sections)} sections from index.html")
    return sections

def restore_structure(file_path, sections_html):
    """Restore original structure to a page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Find hero section
        hero = soup.find('section', class_='hero-section')
        if not hero:
            print(f"[SKIP] {file_path.name}: No hero section found")
            return False

        # Find footer
        footer = soup.find('footer', class_='main-footer')
        if not footer:
            print(f"[SKIP] {file_path.name}: No footer found")
            return False

        # Remove everything between hero and footer
        current = hero.find_next_sibling()
        while current and current != footer:
            next_elem = current.find_next_sibling()
            if hasattr(current, 'decompose'):
                current.decompose()
            current = next_elem

        # Insert all sections from index.html
        for section_html in reversed(sections_html):
            section_soup = BeautifulSoup(section_html, 'html.parser')
            section = section_soup.find('section')
            if section:
                hero.insert_after(section)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"[RESTORED] {file_path.name}")
        return True

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("RESTORING ORIGINAL STRUCTURE FROM INDEX.HTML")
    print("=" * 70)

    # Extract sections from index
    print("\nStep 1: Extracting sections from index.html...")
    sections_html = extract_sections_from_index()

    if not sections_html:
        print("[ERROR] Could not extract sections from index.html")
        return

    print(f"  Found {len(sections_html)} sections to copy")

    # Get all files to restore
    all_files = []
    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    print(f"\nStep 2: Restoring structure to {len(all_files)} pages...")
    print("=" * 70)

    restored = 0
    for file_path in all_files:
        if restore_structure(file_path, sections_html):
            restored += 1

    print("\n" + "=" * 70)
    print(f"RESTORED: {restored}/{len(all_files)} files")
    print("=" * 70)
    print("\nOriginal structure from index.html applied to all pages!")
    print("Structure: Hero -> Countdown -> Services -> ... -> FAQ -> Footer")

if __name__ == '__main__':
    main()
