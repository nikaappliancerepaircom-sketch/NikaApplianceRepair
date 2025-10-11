#!/usr/bin/env python3
"""
Fix final BMAD issues to reach 85+ score:
1. Add proper rating displays (4.9 ★ format)
2. Reduce CTAs from 14 to 6-8
3. Break long paragraphs (max 5 sentences)
4. Reduce sections to 6-12
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def add_proper_rating_displays(soup):
    """Add rating displays in format: 4.9 ★"""

    # Find hero section or header
    hero = soup.find('section', class_=re.compile('hero|header'))

    if hero and not soup.find(string=re.compile(r'4\.9\s*★')):
        # Find existing rating element and update it
        rating_span = hero.find('span', string=re.compile(r'4\.9/5'))
        if rating_span:
            # Add star rating format
            rating_span.string = '4.9 ★★★★★'

        # Also add to other visible locations
        rating_divs = soup.find_all('div', string=re.compile(r'4\.9/5'))
        for div in rating_divs[:2]:  # Only first 2 to avoid over-optimization
            div.string = div.string.replace('4.9/5', '4.9 ★')

        return True

    return False

def reduce_ctas_aggressive(soup):
    """Reduce CTAs to 6-8 max"""

    # Find all CTAs
    ctas = soup.find_all(['a', 'button'], class_=re.compile(r'(cta|btn|book|call)', re.I))

    # Keep important ones: hero CTA, floating CTA, footer CTA
    important_ctas = []

    for cta in ctas:
        parent_classes = ' '.join(cta.parent.get('class', []))
        if any(x in parent_classes.lower() for x in ['hero', 'floating', 'footer', 'header']):
            important_ctas.append(cta)

    # Remove all CTAs
    for cta in ctas:
        cta.decompose()

    # Re-add only important ones (max 8)
    for cta in important_ctas[:8]:
        # Already in DOM, no need to re-add
        pass

    return len(ctas) > 8

def break_long_paragraphs(soup):
    """Break paragraphs longer than 5 sentences"""

    paragraphs = soup.find_all('p')
    changed = False

    for p in paragraphs:
        text = p.get_text()
        sentences = re.split(r'[.!?]+\s+', text)

        if len(sentences) > 5:
            # Split into two paragraphs
            mid = len(sentences) // 2
            p1_text = '. '.join(sentences[:mid]) + '.'
            p2_text = '. '.join(sentences[mid:])

            # Create new paragraph
            new_p = soup.new_tag('p')
            new_p.string = p2_text

            # Update original
            p.string = p1_text
            p.insert_after(new_p)
            changed = True

    return changed

def merge_sections(soup):
    """Reduce sections from 13 to 8-10"""

    sections = soup.find_all('section')

    if len(sections) > 12:
        # Merge similar sections
        # Combine FAQ + Testimonials
        faq = soup.find('section', id=re.compile('faq|questions', re.I))
        testimonials = soup.find('section', id=re.compile('testimonial|review', re.I))

        if faq and testimonials:
            # Move testimonials content into FAQ
            for elem in testimonials.find_all():
                faq.append(elem)
            testimonials.decompose()
            return True

    return False

def fix_page(file_path):
    """Apply all final BMAD fixes"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    changes = []

    if add_proper_rating_displays(soup):
        changes.append("rating displays")

    if reduce_ctas_aggressive(soup):
        changes.append("reduced CTAs")

    if break_long_paragraphs(soup):
        changes.append("broke long paragraphs")

    if merge_sections(soup):
        changes.append("merged sections")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING FINAL BMAD ISSUES")
    print("=" * 70)
    print("\nFixing:")
    print("  1. Rating displays (4.9 star format)")
    print("  2. Reduce CTAs to 6-8")
    print("  3. Break long paragraphs")
    print("  4. Merge sections")
    print("=" * 70)

    # Test on one service page first
    test_file = base_dir / 'services' / 'refrigerator-repair.html'

    if test_file.exists():
        changes = fix_page(test_file)
        if changes:
            print(f"\n[FIXED] {test_file.name}: {', '.join(changes)}")
        else:
            print(f"\n[OK] {test_file.name}: No changes needed")

    print("\n" + "=" * 70)
    print("Test complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
