#!/usr/bin/env python3
"""
Add Hero Section with Animated Background to all pages
Copy hero design from index.html to all service/location pages
"""

from pathlib import Path
from bs4 import BeautifulSoup

def get_hero_bg_animation():
    """Return the animated background HTML from index.html"""
    return '''
<div class="hero-bg-animation">
<!-- Refrigerator Icon -->
<div class="floating-icon icon-1">
<svg fill="white" height="48" viewbox="0 0 24 24" width="48" xmlns="http://www.w3.org/2000/svg">
<path d="M7 2C5.9 2 5 2.9 5 4V19C5 20.1 5.9 21 7 21H17C18.1 21 19 20.1 19 19V4C19 2.9 18.1 2 17 2H7ZM7 4H17V10H7V4ZM7 12H17V19H7V12ZM8 5V8H10V5H8ZM8 13V16H10V13H8Z"></path>
</svg>
</div>
<!-- Dishwasher Icon -->
<div class="floating-icon icon-2">
<svg fill="white" height="48" viewbox="0 0 24 24" width="48" xmlns="http://www.w3.org/2000/svg">
<path d="M18 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V4C20 2.9 19.1 2 18 2ZM18 4V8H6V4H18ZM6 20V10H18V20H6ZM8 5C7.45 5 7 5.45 7 6C7 6.55 7.45 7 8 7C8.55 7 9 6.55 9 6C9 5.45 8.55 5 8 5ZM10 5C9.45 5 9 5.45 9 6C9 6.55 9.45 7 10 7C10.55 7 11 6.55 11 6C11 5.45 10.55 5 10 5ZM8 12C7.45 12 7 12.45 7 13S7.45 14 8 14 9 13.55 9 13 8.55 12 8 12ZM8 16C7.45 16 7 16.45 7 17S7.45 18 8 18 9 17.55 9 17 8.55 16 8 16ZM11.5 12C10.67 12 10 12.67 10 13.5S10.67 15 11.5 15 13 14.33 13 13.5 12.33 12 11.5 12ZM15.5 13C15.22 13 15 13.22 15 13.5S15.22 14 15.5 14 16 13.78 16 13.5 15.78 13 15.5 13Z"></path>
</svg>
</div>
<!-- Dryer Icon -->
<div class="floating-icon icon-3">
<svg fill="white" height="48" viewbox="0 0 24 24" width="48" xmlns="http://www.w3.org/2000/svg">
<path d="M6 2H18C19.11 2 20 2.89 20 4V20C20 21.11 19.11 22 18 22H6C4.89 22 4 21.11 4 20V4C4 2.89 4.89 2 6 2ZM6 4V7H18V4H6ZM6 9V20H18V9H6ZM8 5C8.55 5 9 5.45 9 6C9 6.55 8.55 7 8 7C7.45 7 7 6.55 7 6C7 5.45 7.45 5 8 5ZM10 5C10.55 5 11 5.45 11 6C11 6.55 10.55 7 10 7C9.45 7 9 6.55 9 6C9 5.45 9.45 5 10 5ZM12 11.5C14.21 11.5 16 13.29 16 15.5S14.21 19.5 12 19.5 8 17.71 8 15.5 9.79 11.5 12 11.5ZM12 13.5C10.9 13.5 10 14.4 10 15.5S10.9 17.5 12 17.5 14 16.6 14 15.5 13.1 13.5 12 13.5Z"></path>
</svg>
</div>
<!-- Stove Icon -->
<div class="floating-icon icon-4">
<svg fill="white" height="48" viewbox="0 0 24 24" width="48" xmlns="http://www.w3.org/2000/svg">
<path d="M4 8H20V5H4V8ZM6 2C6.55 2 7 2.45 7 3S6.55 4 6 4 5 3.55 5 3 5.45 2 6 2ZM9 2C9.55 2 10 2.45 10 3S9.55 4 9 4 8 3.55 8 3 8.45 2 9 2ZM15 2C15.55 2 16 2.45 16 3S15.55 4 15 4 14 3.55 14 3 14.45 2 15 2ZM18 2C18.55 2 19 2.45 19 3S18.55 4 18 4 17 3.55 17 3 17.45 2 18 2ZM4 10V19C4 20.1 4.9 21 6 21H18C19.1 21 20 20.1 20 19V10H4ZM8 18C6.9 18 6 17.1 6 16C6 14.9 6.9 14 8 14S10 14.9 10 16C10 17.1 9.1 18 8 18ZM16 18C14.9 18 14 17.1 14 16C14 14.9 14.9 14 16 14S18 14.9 18 16C18 17.1 17.1 18 16 18Z"></path>
</svg>
</div>
<!-- Oven Icon -->
<div class="floating-icon icon-5">
<svg fill="white" height="48" viewbox="0 0 24 24" width="48" xmlns="http://www.w3.org/2000/svg">
<path d="M4 3C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H20C21.1 21 22 20.1 22 19V5C22 3.9 21.1 3 20 3H4ZM4 5H20V9H4V5ZM4 11H20V19H4V11ZM5 6V8H7V6H5ZM8 6V8H10V6H8ZM19 6C18.45 6 18 6.45 18 7C18 7.55 18.45 8 19 8C19.55 8 20 7.55 20 7C20 6.45 19.55 6 19 6ZM6 13V17H18V13H6Z"></path>
</svg>
</div>
<!-- Washing Machine Icon -->
<div class="floating-icon icon-6">
<svg fill="white" height="48" viewbox="0 0 24 24" width="48" xmlns="http://www.w3.org/2000/svg">
<path d="M6 2H18C19.11 2 20 2.89 20 4V20C20 21.11 19.11 22 18 22H6C4.89 22 4 21.11 4 20V4C4 2.89 4.89 2 6 2ZM6 4V20H18V4H6ZM12 7C14.76 7 17 9.24 17 12S14.76 17 12 17 7 14.76 7 12 9.24 7 12 7ZM12 9C10.34 9 9 10.34 9 12S10.34 15 12 15 15 13.66 15 12 13.66 9 12 9ZM8 5C8.55 5 9 5.45 9 6S8.55 7 8 7 7 6.55 7 6 7.45 5 8 5ZM10 5C10.55 5 11 5.45 11 6S10.55 7 10 7 9 6.55 9 6 9.45 5 10 5Z"></path>
</svg>
</div>
<!-- Hidden icons -->
<div class="floating-icon icon-7" style="display: none;"></div>
<div class="floating-icon icon-8" style="display: none;"></div>
</div>
'''

def add_hero_animation(file_path):
    """Add animated hero background to pages that don't have it"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Find hero section
    hero = soup.find('section', class_='hero-section')

    if not hero:
        return False

    # Check if already has animation
    if hero.find('div', class_='hero-bg-animation'):
        return False

    # Add animation as first child of hero section
    animation_html = get_hero_bg_animation()
    animation_soup = BeautifulSoup(animation_html, 'html.parser')

    # Insert at beginning of hero section
    hero.insert(0, animation_soup)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return True

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("ADDING HERO ANIMATED BACKGROUNDS")
    print("=" * 70)
    print("\nAdding animated appliance icons to hero sections")
    print("Same design as main page")
    print("=" * 70)

    all_files = []
    for subdir in ['services', 'locations']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html')])

    print(f"\nProcessing {len(all_files)} pages...\n")

    added = 0
    for file_path in all_files:
        if add_hero_animation(file_path):
            print(f"[ADDED] {file_path.name}")
            added += 1

    print("\n" + "=" * 70)
    print(f"ADDED: {added}/{len(all_files)} pages")
    print("=" * 70)
    print("\nHero animations added!")

if __name__ == '__main__':
    main()
