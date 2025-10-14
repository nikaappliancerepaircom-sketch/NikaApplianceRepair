#!/usr/bin/env python3
"""
Phase 2: Additional aggressive cuts to reach 2,000-2,500 words
Current: 3,399 words → Target: 2,200-2,400 words
Need to remove: 999-1,199 more words
"""

import re
from bs4 import BeautifulSoup

def count_words(text):
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return len(clean.split())

def remove_second_testimonial_row(soup):
    """Remove the second row of testimonials (2 videos)"""
    testimonial_section = soup.find('section', class_='testimonials-premium')
    if testimonial_section:
        second_grid = testimonial_section.find('div', class_='testimonials-grid-two-col')
        if second_grid:
            second_grid.decompose()
            print("    Removed 2 testimonials")

def reduce_brands_description(soup):
    """Shorten brands section description"""
    brands_section = soup.find('section', class_='brands-section-premium')
    if brands_section:
        subtitle = brands_section.find('p', class_='section-subtitle')
        if subtitle:
            new_text = "Expert appliance repair for 90+ brands: Miele, Sub-Zero, Wolf, Thermador, Gaggenau, Bosch, Bertazzoni, Samsung, LG, Whirlpool, GE, KitchenAid, and many more."
            subtitle.string = new_text
            print("    Reduced brands description")

def remove_redundant_vaughan_mentions(html):
    """Strategic removal of redundant Vaughan mentions"""
    # In generic phrases, remove Vaughan
    html = re.sub(r'in Vaughan and the GTA', 'across the GTA', html)
    html = re.sub(r'Vaughan and GTA homeowners', 'GTA homeowners', html)
    html = re.sub(r'across Vaughan and ', 'across ', html, count=5)
    return html

def trim_why_choose_subtitle(soup):
    """Shorten why choose subtitle"""
    why_section = soup.find('section', class_='why-choose-section')
    if why_section:
        subtitle = why_section.find('p', class_='section-subtitle')
        if subtitle:
            new_text = "4.9/5 rating from 5,200+ GTA customers. Miele-certified luxury appliance specialists with white-glove service."
            subtitle.string = new_text

def trim_services_subtitle(soup):
    """Shorten services subtitle"""
    services_section = soup.find('section', class_='services-section')
    if services_section:
        subtitle = services_section.find('p', class_='section-subtitle')
        if subtitle:
            new_text = "4.9-star rating | 5,200+ repairs | 90-day warranty"
            subtitle.string = new_text

def reduce_video_info(soup):
    """Remove video description paragraph"""
    video_info = soup.find('div', class_='video-info')
    if video_info:
        p_tag = video_info.find('p')
        if p_tag:
            p_tag.decompose()

def trim_service_features_list(soup):
    """Reduce service features list from 6 to 4 items"""
    features_list = soup.find('ul', class_='features-list')
    if features_list:
        items = features_list.find_all('li')
        if len(items) > 4:
            # Keep first 4, remove last 2
            for item in items[4:]:
                item.decompose()
            print(f"    Trimmed features list from {len(items)} to 4")

def main():
    input_file = r'C:\NikaApplianceRepair\locations\vaughan.html'

    print("=" * 60)
    print("PHASE 2: ADDITIONAL CUTS")
    print("=" * 60)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    initial_words = count_words(content)
    print(f"\nStarting word count: {initial_words:,}")
    print(f"Target: 2,200-2,400 words")
    print(f"Need to remove: {initial_words - 2400:,} - {initial_words - 2200:,} words")

    soup = BeautifulSoup(content, 'html.parser')

    print("\nApplying additional cuts...")
    print("  [1/7] Removing second testimonial row...")
    remove_second_testimonial_row(soup)

    print("  [2/7] Reducing brands description...")
    reduce_brands_description(soup)

    print("  [3/7] Trimming why choose subtitle...")
    trim_why_choose_subtitle(soup)

    print("  [4/7] Trimming services subtitle...")
    trim_services_subtitle(soup)

    print("  [5/7] Removing video description...")
    reduce_video_info(soup)

    print("  [6/7] Trimming service features list...")
    trim_service_features_list(soup)

    # Convert to string for text replacements
    reduced_content = str(soup)

    print("  [7/7] Removing redundant Vaughan mentions...")
    reduced_content = remove_redundant_vaughan_mentions(reduced_content)

    final_words = count_words(reduced_content)
    word_reduction = initial_words - final_words
    word_reduction_pct = (word_reduction / initial_words * 100)

    print("\n" + "=" * 60)
    print("PHASE 2 RESULTS")
    print("=" * 60)
    print(f"Word count: {initial_words:,} -> {final_words:,}")
    print(f"Removed: {word_reduction:,} words ({word_reduction_pct:.1f}%)")

    if 2000 <= final_words <= 2500:
        print(f"\nSUCCESS: Within target range!")
    elif final_words > 2500:
        print(f"\nStill {final_words - 2400} words above target")
    else:
        print(f"\n{2000 - final_words} words below minimum target")

    print(f"\nWriting final content...")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(reduced_content)

    print(f"Saved to: {input_file}")
    print("=" * 60)

if __name__ == '__main__':
    main()
