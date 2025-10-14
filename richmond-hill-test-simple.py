#!/usr/bin/env python3
"""BMAD v3.2 Test - Richmond Hill"""

import re
from bs4 import BeautifulSoup
import json

def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def count_visible_words(soup):
    for tag in soup(['script', 'style', 'head', 'meta', 'link']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip=True)
    words = text.split()
    return len(words), text

def main():
    print("="*80)
    print("BMAD v3.2 EXCELLENCE STANDARD TEST - Richmond Hill")
    print("="*80)

    file_path = r'C:\NikaApplianceRepair\locations\richmond-hill.html'
    soup = load_html(file_path)
    word_count, visible_text = count_visible_words(soup)

    print(f"\nWORD COUNT: {word_count} words (target: 2000-2500)")

    # SEO tests
    print("\n" + "="*80)
    print("SEO + AI OPTIMIZATION")
    print("="*80)

    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    h3_tags = soup.find_all('h3')

    print(f"H1 tags: {len(h1_tags)} (target: 1)")
    if h1_tags:
        print(f"  H1: {h1_tags[0].get_text(strip=True)}")
    print(f"H2 tags: {len(h2_tags)} (target: 5-10)")
    print(f"H3 tags: {len(h3_tags)} (target: 12-15)")

    title = soup.find('title')
    title_text = title.get_text() if title else ""
    print(f"\nTitle: {len(title_text)} chars (target: 50-60)")
    print(f"  '{title_text}'")

    meta_desc = soup.find('meta', {'name': 'description'})
    desc_text = meta_desc.get('content', '') if meta_desc else ""
    print(f"\nMeta desc: {len(desc_text)} chars (target: 150-160)")
    print(f"  '{desc_text}'")

    # Schema
    schema_scripts = soup.find_all('script', {'type': 'application/ld+json'})
    schema_types = []
    for script in schema_scripts:
        try:
            data = json.loads(script.string)
            schema_type = data.get('@type', '')
            if schema_type:
                schema_types.append(schema_type)
        except:
            pass
    print(f"\nSchema types: {', '.join(schema_types)}")

    # Question headers
    question_headers = []
    for tag in soup.find_all(['h2', 'h3']):
        text = tag.get_text(strip=True)
        if '?' in text or any(text.lower().startswith(q) for q in ['what', 'how', 'why', 'when', 'where', 'can', 'do', 'does', 'should', 'is', 'are']):
            question_headers.append(text)

    print(f"\nQuestion headers: {len(question_headers)} (target: 6+)")
    for i, q in enumerate(question_headers[:8], 1):
        print(f"  {i}. {q}")

    # Location mentions
    location_mentions = visible_text.lower().count('richmond hill')
    print(f"\nLocation mentions: {location_mentions} (target: 15-40)")

    # Phone mentions
    phone_matches = re.findall(r'437[- ]?747[- ]?6737', str(soup))
    print(f"Phone mentions: {len(phone_matches)} (target: 8+)")

    # Tel links
    tel_links = soup.find_all('a', href=re.compile(r'tel:'))
    print(f"Click-to-call links: {len(tel_links)} (target: 5+)")

    # Images
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]
    print(f"\nImages: {len(images)} (target: 10+)")
    print(f"Alt text coverage: {len(images_with_alt)}/{len(images)} ({len(images_with_alt)/len(images)*100:.1f}%)")

    # CTAs
    print("\n" + "="*80)
    print("CRO - CONVERSION RATE OPTIMIZATION")
    print("="*80)

    cta_elements = soup.find_all(['a', 'button'], class_=re.compile(r'cta|btn|call|book', re.I))
    print(f"CTA elements: {len(cta_elements)} (target: 5-8)")

    whatsapp_links = soup.find_all('a', href=re.compile(r'whatsapp|wa.me', re.I))
    form_elements = soup.find_all('form')

    cta_types = []
    if tel_links:
        cta_types.append('phone')
    if whatsapp_links:
        cta_types.append('whatsapp')
    if form_elements:
        cta_types.append('form')

    print(f"CTA types: {len(cta_types)} (target: 3+) - {', '.join(cta_types)}")

    # Psychology
    print("\n" + "="*80)
    print("PSYCHOLOGY TRIGGERS")
    print("="*80)

    pain_words = ['broken', 'leaking', 'not cooling', 'not heating', 'not working',
                  'failed', 'stopped', 'emergency', 'urgent', 'worried', 'stressed',
                  'flooding', 'spoiling', 'wasted']
    pain_count = sum(visible_text.lower().count(word) for word in pain_words)
    print(f"Emotional pain words: {pain_count} instances (target: 10+)")

    solution_words = ['fix', 'repair', 'solve', 'restore', 'working', 'fixed',
                      'same-day', 'fast', 'quick', 'expert', 'certified']
    solution_count = sum(visible_text.lower().count(word) for word in solution_words)
    print(f"Solution words: {solution_count} instances (target: 20+)")

    # Check for prohibited content
    prohibited = ['commercial appliance', 'factory-authorized', 'factory-certified',
                  'manufacturer-approved', 'official service center', 'microwave repair',
                  'range hood', 'wine fridge', 'coffee maker', 'ice maker']
    found_prohibited = [word for word in prohibited if word in visible_text.lower()]

    if found_prohibited:
        print(f"\nWARNING - Prohibited content found:")
        for item in found_prohibited:
            print(f"  - {item}")
    else:
        print(f"\nCompliance: No prohibited content found")

    # Data consistency
    print("\n" + "="*80)
    print("DATA CONSISTENCY")
    print("="*80)

    warranty_mentions = re.findall(r'(\d+)[-\s]?day[s]?\s+warranty', visible_text.lower())
    print(f"Warranty mentions: {warranty_mentions}")

    rating_mentions = re.findall(r'(4\.\d|5\.0)', visible_text)
    print(f"Rating mentions: {rating_mentions}")

    review_mentions = re.findall(r'(\d+)\+?\s+reviews?', visible_text.lower())
    print(f"Review count mentions: {review_mentions}")

    # Content quality
    print("\n" + "="*80)
    print("CONTENT QUALITY")
    print("="*80)

    rh_specific = ['oak ridges', 'yonge street', 'richmond hill centre',
                   'luxury home', 'affluent', 'chinese community', 'persian community']
    specific_mentions = sum(1 for phrase in rh_specific if phrase in visible_text.lower())
    print(f"Richmond Hill-specific references: {specific_mentions}/{len(rh_specific)}")
    for phrase in rh_specific:
        if phrase in visible_text.lower():
            print(f"  - {phrase}")

    sentences = re.split(r'[.!?]+', visible_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    avg_words = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    print(f"\nAverage sentence length: {avg_words:.1f} words (target: 15-20)")
    print(f"Sections (H2s): {len(h2_tags)} (target: 7-12)")

    # Visual design
    print("\n" + "="*80)
    print("VISUAL DESIGN")
    print("="*80)

    style_content = str(soup.find_all('style'))

    has_line_height = 'line-height' in style_content
    has_hover = ':hover' in style_content
    has_focus = ':focus' in style_content
    has_clamp = 'clamp(' in style_content

    print(f"Line-height defined: {'YES' if has_line_height else 'NO'}")
    print(f"Hover states: {'YES' if has_hover else 'NO'}")
    print(f"Focus states: {'YES' if has_focus else 'NO'}")
    print(f"Responsive typography (clamp): {'YES' if has_clamp else 'NO'}")

    lazy_images = [img for img in images if img.get('loading') == 'lazy']
    print(f"Lazy loading images: {len(lazy_images)}/{len(images)} ({len(lazy_images)/len(images)*100:.1f}%)")

    # Responsive design
    print("\n" + "="*80)
    print("RESPONSIVE DESIGN")
    print("="*80)

    viewport = soup.find('meta', {'name': 'viewport'})
    print(f"Viewport meta tag: {'YES' if viewport else 'NO'}")

    has_overflow_fix = 'overflow-x: hidden' in style_content or 'overflow-x:hidden' in style_content
    print(f"Overflow-x prevention: {'YES' if has_overflow_fix else 'NO'}")

    has_mobile_queries = '@media' in style_content and 'max-width' in style_content
    print(f"Mobile media queries: {'YES' if has_mobile_queries else 'NO'}")

    css_links = soup.find_all('link', rel='stylesheet')
    responsive_css = [link for link in css_links if 'responsive' in link.get('href', '').lower() or 'mobile' in link.get('href', '').lower()]
    print(f"Responsive CSS files: {len(responsive_css)}")

    # FINAL SCORING
    print("\n" + "="*80)
    print("BMAD v3.2 CATEGORY SCORING")
    print("="*80)

    scores = {}

    # SEO scoring
    seo_score = 0
    if 2000 <= word_count <= 2500:
        seo_score += 10
    if len(h1_tags) == 1:
        seo_score += 5
    if 5 <= len(h2_tags) <= 10 and 12 <= len(h3_tags) <= 15:
        seo_score += 10
    if 50 <= len(title_text) <= 60:
        seo_score += 5
    if 150 <= len(desc_text) <= 160:
        seo_score += 5
    if len(question_headers) >= 6:
        seo_score += 10
    if 15 <= location_mentions <= 40:
        seo_score += 10
    if len(phone_matches) >= 8:
        seo_score += 5
    if len(images) >= 10 and len(images_with_alt) == len(images):
        seo_score += 10
    seo_score += 10  # Base points

    seo_pct = (seo_score / 80) * 100
    scores['SEO + AI'] = (seo_score, 80, seo_pct, 'PASS' if seo_pct >= 98 else 'NEAR' if seo_pct >= 95 else 'FAIL')

    # Responsive scoring
    resp_score = 0
    if viewport:
        resp_score += 10
    if has_overflow_fix:
        resp_score += 15
    if has_mobile_queries:
        resp_score += 15
    if has_clamp:
        resp_score += 10
    if len(responsive_css) >= 3:
        resp_score += 10
    resp_score += 10  # Base

    resp_pct = (resp_score / 70) * 100
    scores['Responsive'] = (resp_score, 70, resp_pct, 'PASS' if resp_pct >= 95 else 'NEAR' if resp_pct >= 90 else 'FAIL')

    # Visual scoring
    vis_score = 0
    if has_line_height:
        vis_score += 8
    if has_hover:
        vis_score += 8
    if has_focus:
        vis_score += 8
    if has_clamp:
        vis_score += 8
    if len(lazy_images) >= len(images) * 0.7:
        vis_score += 8

    vis_pct = (vis_score / 40) * 100
    scores['Visual'] = (vis_score, 40, vis_pct, 'PASS' if vis_pct >= 95 else 'NEAR' if vis_pct >= 90 else 'FAIL')

    # Content scoring
    cont_score = 0
    if specific_mentions >= 4:
        cont_score += 8
    elif specific_mentions >= 2:
        cont_score += 6
    if 15 <= avg_words <= 20:
        cont_score += 8
    if 7 <= len(h2_tags) <= 12:
        cont_score += 8

    cont_pct = (cont_score / 24) * 100
    scores['Content'] = (cont_score, 24, cont_pct, 'PASS' if cont_pct >= 98 else 'NEAR' if cont_pct >= 95 else 'FAIL')

    # CRO scoring
    cro_score = 0
    if 5 <= len(cta_elements) <= 8:
        cro_score += 10
    if len(cta_types) >= 3:
        cro_score += 10

    cro_pct = (cro_score / 20) * 100
    scores['CRO'] = (cro_score, 20, cro_pct, 'PASS' if cro_pct >= 95 else 'NEAR' if cro_pct >= 90 else 'FAIL')

    # Psychology scoring
    psych_score = 0
    if pain_count >= 15:
        psych_score += 8
    elif pain_count >= 10:
        psych_score += 6
    if solution_count >= 20:
        psych_score += 8
    elif solution_count >= 10:
        psych_score += 6
    if not found_prohibited:
        psych_score += 9

    psych_pct = (psych_score / 25) * 100
    scores['Psychology'] = (psych_score, 25, psych_pct, 'PASS' if psych_pct >= 98 else 'NEAR' if psych_pct >= 95 else 'FAIL')

    # Data consistency
    data_score = 15
    if len(set(warranty_mentions)) > 1:
        data_score -= 3
    if len(set(rating_mentions)) > 1:
        data_score -= 3
    if len(set(review_mentions)) > 1:
        data_score -= 3

    data_pct = (data_score / 15) * 100
    scores['Data Consistency'] = (data_score, 15, data_pct, 'PASS' if data_pct == 100 else 'NEAR' if data_pct >= 95 else 'FAIL')

    # Conversion design
    conv_score = 0
    if has_hover and has_focus:
        conv_score += 5
    if 'mobile' in str(soup).lower() and 'cta' in str(soup).lower():
        conv_score += 5

    conv_pct = (conv_score / 10) * 100
    scores['Conversion Design'] = (conv_score, 10, conv_pct, 'PASS' if conv_pct >= 98 else 'NEAR' if conv_pct >= 95 else 'FAIL')

    # Print results
    print(f"\n{'CATEGORY':<25} {'SCORE':<12} {'%':<8} {'STATUS':<10} {'GATE'}")
    print("-"*80)

    gates_passed = 0
    total_gates = 8

    for cat, (score, max_s, pct, status) in scores.items():
        gate = 'CRITICAL' if cat in ['SEO + AI', 'Responsive', 'Visual', 'Content', 'CRO', 'Psychology', 'Data Consistency', 'Conversion Design'] else ''
        if status == 'PASS':
            gates_passed += 1
        print(f"{cat:<25} {score}/{max_s:<9} {pct:>6.1f}%  {status:<10} {gate}")

    total_score = sum(s[0] for s in scores.values())
    total_max = sum(s[1] for s in scores.values())
    overall = (total_score / total_max) * 100

    print("="*80)
    print(f"OVERALL SCORE: {total_score}/{total_max} ({overall:.1f}%)")
    print(f"CRITICAL GATES PASSED: {gates_passed}/{total_gates}")
    print("="*80)

    # Recommendation
    print("\nDEPLOYMENT RECOMMENDATION:")
    if gates_passed == total_gates and overall >= 95:
        print("  APPROVED - All gates passed, meets BMAD v3.2 Excellence Standard")
    elif gates_passed >= total_gates - 1 and overall >= 92:
        print("  CONDITIONAL - Nearly all gates passed, minor fixes recommended")
    else:
        print("  NOT APPROVED - Critical gates failed, improvements required")

    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
