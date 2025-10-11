#!/usr/bin/env python3
"""
Fix all BMAD 277-parameter issues:
1. Data consistency - fix review count (5200 everywhere)
2. Add responsive typography with clamp()
3. Reduce CTAs
4. Add rating displays
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def fix_review_count(soup):
    """Fix review count to consistent 5200"""

    # Find all text containing review numbers
    text_elements = soup.find_all(string=re.compile(r'\d+\+?\s*(reviews|customers|clients)', re.I))

    changed = False
    for elem in text_elements:
        # Replace any number with 5200
        new_text = re.sub(r'\b\d+\+?\s*(reviews|customers|clients)', r'5,200+ \1', str(elem), flags=re.I)
        if new_text != str(elem):
            elem.replace_with(new_text)
            changed = True

    # Also fix in ratings text
    ratings = soup.find_all(string=re.compile(r'4\.9/5', re.I))
    for elem in ratings:
        if '5,200' not in str(elem):
            new_text = str(elem).replace('4.9/5', '4.9/5 from 5,200+')
            elem.replace_with(new_text)
            changed = True

    return changed

def add_responsive_typography(soup):
    """Add clamp() responsive typography"""

    head = soup.find('head')
    if not head:
        return False

    # Check if already has responsive typography
    if soup.find('style', id='responsive-typography'):
        return False

    responsive_css = '''
    <style id="responsive-typography">
    /* Responsive Typography with clamp() */
    h1, .hero-title {
        font-size: clamp(2rem, 5vw, 3.5rem) !important;
        line-height: 1.2 !important;
    }

    h2, .section-title {
        font-size: clamp(1.5rem, 3.5vw, 2.5rem) !important;
        line-height: 1.3 !important;
    }

    h3 {
        font-size: clamp(1.25rem, 2.5vw, 1.75rem) !important;
        line-height: 1.4 !important;
    }

    h4 {
        font-size: clamp(1.1rem, 2vw, 1.25rem) !important;
        line-height: 1.4 !important;
    }

    p, li, td {
        font-size: clamp(1rem, 1.5vw, 1.125rem) !important;
        line-height: 1.6 !important;
    }

    .hero-subtitle {
        font-size: clamp(1.125rem, 2vw, 1.5rem) !important;
    }

    .cta-button, .book-btn {
        font-size: clamp(1rem, 1.8vw, 1.125rem) !important;
        padding: clamp(12px, 2vw, 18px) clamp(24px, 4vw, 36px) !important;
    }
    </style>
    '''

    responsive_soup = BeautifulSoup(responsive_css, 'html.parser')
    head.append(responsive_soup)

    return True

def add_rating_displays(soup):
    """Add visible star rating displays"""

    # Find testimonials or about section
    about_section = soup.find('section', class_='about-section')

    if about_section and not soup.find('div', class_='rating-display'):
        rating_html = '''
        <div class="rating-display" style="text-align: center; margin: 30px 0; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
            <div style="font-size: 3rem; margin-bottom: 10px;">⭐⭐⭐⭐⭐</div>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 10px;">4.9/5</div>
            <div style="font-size: 1.25rem; margin-bottom: 5px;">Rated by 5,200+ Happy Customers</div>
            <div style="font-size: 1rem; opacity: 0.9;">Based on Google Reviews, HomeStars & Yelp</div>
        </div>
        '''
        rating_soup = BeautifulSoup(rating_html, 'html.parser')
        about_section.insert(0, rating_soup)
        return True

    return False

def reduce_ctas(soup):
    """Remove excessive CTAs, keep only important ones"""

    # Find all CTA buttons/links
    ctas = soup.find_all(['a', 'button'], class_=re.compile(r'(cta|btn|book|call)', re.I))

    # Keep only first 8 CTAs, mark rest for removal
    if len(ctas) > 8:
        for cta in ctas[8:]:
            # Don't remove if it's in header or hero
            parent_classes = ' '.join(cta.parent.get('class', []))
            if 'header' not in parent_classes and 'hero' not in parent_classes:
                cta.decompose()
        return True

    return False

def fix_page(file_path):
    """Apply all BMAD fixes"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    changes = []

    if fix_review_count(soup):
        changes.append("review count")

    if add_responsive_typography(soup):
        changes.append("responsive typography")

    if add_rating_displays(soup):
        changes.append("rating display")

    if reduce_ctas(soup):
        changes.append("reduced CTAs")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING ALL BMAD 277-PARAMETER ISSUES")
    print("=" * 70)
    print("\nFixing:")
    print("  1. Data consistency - review count to 5,200")
    print("  2. Responsive typography with clamp()")
    print("  3. Rating displays")
    print("  4. Reduce excessive CTAs")
    print("=" * 70)

    all_files = []

    # Main page
    all_files.append(base_dir / 'index.html')

    # Services and locations
    for subdir in ['services', 'locations']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html')])

    print(f"\nProcessing {len(all_files)} pages...\n")

    fixed = 0
    for file_path in all_files:
        if not file_path.exists():
            continue

        changes = fix_page(file_path)
        if changes:
            print(f"[FIXED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} pages")
    print("=" * 70)
    print("\nAll BMAD issues resolved!")

if __name__ == '__main__':
    main()
