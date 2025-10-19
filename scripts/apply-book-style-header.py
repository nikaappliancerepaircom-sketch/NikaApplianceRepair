#!/usr/bin/env python3
"""
Apply book-style header to all pages

Changes:
1. Simplify logo to single line "NIKA Appliance Repair"
2. Change Book button to green (like book.html)
3. Ensure review count is 5,200+ everywhere
"""

import re
from pathlib import Path

def update_header_to_book_style(file_path):
    """Update header to book-style"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # 1. Simplify logo - single line version
    # BEFORE:
    # <div class="header-logo">
    #     <a href="#">
    #         <div class="logo-icon">🔧</div>
    #         <div class="logo-text">
    #             <span class="logo-name">NIKA</span>
    #             <span class="logo-tagline">Appliance Repair</span>
    #         </div>
    #     </a>
    # </div>

    # AFTER:
    # <div class="header-logo">
    #     <a href="#">NIKA Appliance Repair</a>
    # </div>

    logo_pattern = r'<div class="header-logo">\s*<a href="([^"]+)"[^>]*>\s*<div class="logo-icon">[^<]*</div>\s*<div class="logo-text">\s*<span class="logo-name">NIKA</span>\s*<span class="logo-tagline">Appliance Repair</span>\s*</div>\s*</a>\s*</div>'

    logo_replacement = r'<div class="header-logo">\n                <a href="\1" aria-label="Nika Appliance Repair - Home">NIKA Appliance Repair</a>\n            </div>'

    if re.search(logo_pattern, content, re.DOTALL):
        content = re.sub(logo_pattern, logo_replacement, content, flags=re.DOTALL)
        changed = True

    # 2. Change Book button color to green
    # Find .cta-book style and change background

    # Pattern 1: Blue gradient
    blue_book_gradient = r'(\.cta-book \{[^}]*background: ?)linear-gradient\(135deg, #2196F3 0%, #1976D2 100%\)'
    green_book_gradient = r'\1linear-gradient(135deg, #27AE60 0%, #229954 100%)'

    if re.search(blue_book_gradient, content):
        content = re.sub(blue_book_gradient, green_book_gradient, content)
        changed = True

    # Pattern 2: Solid blue color (common on index.html and others)
    blue_book_solid = r'(\.cta-book \{\s*background: )#2196F3;'
    green_book_solid = r'\1linear-gradient(135deg, #27AE60 0%, #229954 100%);'

    if re.search(blue_book_solid, content):
        content = re.sub(blue_book_solid, green_book_solid, content)
        changed = True

    # Also update hover state from blue to green
    blue_hover = r'(\.cta-book:hover \{\s*background: )#1976D2;'
    green_hover = r'\1#229954;'

    if re.search(blue_hover, content):
        content = re.sub(blue_hover, green_hover, content)
        changed = True

    # Update hover box-shadow color to green
    blue_shadow = r'(box-shadow: 0 4px 12px rgba\()33,150,243'
    green_shadow = r'\g<1>39,174,96'

    if re.search(blue_shadow, content):
        content = re.sub(blue_shadow, green_shadow, content)
        changed = True

    # 3. Update Book button hover state (optional)
    # Add green hover if missing
    book_hover_pattern = r'\.cta-book:hover \{'
    if not re.search(book_hover_pattern, content):
        # Find where to insert hover
        insert_after = r'(\.cta-book \{[^}]*\})'
        hover_style = r'\1\n\n    .cta-book:hover {\n        transform: translateY(-2px);\n        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);\n    }'

        if re.search(insert_after, content, re.DOTALL):
            content = re.sub(insert_after, hover_style, content, count=1, flags=re.DOTALL)
            changed = True

    # 4. Update review count to 5,200+ (if it's 520+)
    review_520_pattern = r'(<div class="trust-rating">4\.9 <span[^>]*>\()520\+(\)</span></div>)'
    review_5200 = r'\g<1>5,200+\g<2>'

    if re.search(review_520_pattern, content):
        content = re.sub(review_520_pattern, review_5200, content)
        changed = True

    # Also check for variations
    review_520_v2 = r'(<span class="trust-reviews">\()520\+(\)</span>)'
    if re.search(review_520_v2, content):
        content = re.sub(review_520_v2, r'\g<1>5,200+\g<2>', content)
        changed = True

    # 5. Simplify logo CSS styles
    # Remove logo-icon and logo-text styles, add simpler logo style

    logo_css_pattern = r'\.logo-icon \{[^}]+\}\s*\.logo-text \{[^}]+\}\s*\.logo-name \{[^}]+\}\s*\.logo-tagline \{[^}]+\}'

    simple_logo_css = '''/* Logo - Simple Single Line */
    .header-logo a {
        font-family: 'Fredoka', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2196F3;
        text-decoration: none;
        white-space: nowrap;
    }'''

    if re.search(logo_css_pattern, content, re.DOTALL):
        content = re.sub(logo_css_pattern, simple_logo_css, content, flags=re.DOTALL)
        changed = True

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    base_dir = Path('C:/NikaApplianceRepair')

    pages = []

    # Homepage
    pages.append(base_dir / 'index.html')

    # Service pages (9)
    services = ['refrigerator-repair', 'dishwasher-repair', 'washer-repair', 'dryer-repair',
                'oven-repair', 'stove-repair', 'range-repair', 'microwave-repair', 'freezer-repair']
    for service in services:
        pages.append(base_dir / 'services' / f'{service}.html')

    # Location pages (20)
    locations = ['richmond-hill', 'mississauga', 'brampton', 'markham', 'vaughan',
                 'oakville', 'milton', 'burlington', 'ajax', 'pickering',
                 'whitby', 'oshawa', 'aurora', 'newmarket', 'etobicoke',
                 'north-york', 'scarborough', 'caledon', 'east-gwillimbury', 'halton-hills']
    for location in locations:
        pages.append(base_dir / 'locations' / f'{location}.html')

    # Brand pages (15)
    brands = ['samsung', 'lg', 'whirlpool', 'ge', 'bosch',
              'kitchenaid', 'maytag', 'frigidaire', 'electrolux', 'kenmore',
              'miele', 'fisher-paykel', 'amana', 'hotpoint', 'danby']
    for brand in brands:
        pages.append(base_dir / 'brands' / f'{brand}-appliance-repair-toronto.html')

    # Listing pages
    pages.append(base_dir / 'services.html')
    pages.append(base_dir / 'locations.html')

    print('='*70)
    print('APPLYING BOOK-STYLE HEADER TO ALL PAGES')
    print('='*70)
    print()
    print('Changes:')
    print('  1. Logo: Simple single line "NIKA Appliance Repair"')
    print('  2. Book button: Green gradient (like book.html)')
    print('  3. Review count: 5,200+ everywhere')
    print('  4. Cleaner CSS')
    print()
    print('='*70)
    print()

    updated = 0
    skipped = 0

    for page in pages:
        if page.exists():
            print(f'Processing: {page.name}...', end=' ')
            if update_header_to_book_style(page):
                print('[UPDATED]')
                updated += 1
            else:
                print('[SKIP]')
                skipped += 1
        else:
            print(f'[WARN] Not found: {page}')

    print()
    print('='*70)
    print(f'COMPLETE!')
    print(f'  Updated: {updated} pages')
    print(f'  Skipped: {skipped} pages (already book-style)')
    print('='*70)

if __name__ == '__main__':
    main()
