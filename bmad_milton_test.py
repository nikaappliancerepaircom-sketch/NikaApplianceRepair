#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMAD v3.1 COMPREHENSIVE TEST - MILTON PAGE
Testing 283 parameters (Speed Performance excluded)
Focus: Content Quality 98%+, Data Consistency 100%, Milton-specific content
"""

import re
from pathlib import Path

def analyze_milton_page():
    # Read the file
    with open('locations/milton.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print("=" * 80)
    print("BMAD v3.1 COMPREHENSIVE TEST - MILTON.HTML")
    print("Testing 283 parameters (Speed Performance excluded)")
    print("=" * 80)

    total_score = 0
    total_max = 283

    # ========================================================================
    # CATEGORY 1: META & SEO OPTIMIZATION (35 parameters) - Target: 100%
    # ========================================================================
    print("\n[1] META & SEO OPTIMIZATION (35 parameters)")
    print("-" * 80)

    score_meta = 0
    max_meta = 35

    # 1.1 Title tag (3 params)
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        title = title_match.group(1)
        if 'Milton' in title:
            score_meta += 1
            print("[OK] Title contains 'Milton'")
        if len(title) >= 50 and len(title) <= 60:
            score_meta += 1
            print(f"[OK] Title length optimal: {len(title)} chars (50-60)")
        elif len(title) > 60:
            print(f"[WARN] Title too long: {len(title)} chars (optimal: 50-60)")
        if 'Save' in title or '$40' in title:
            score_meta += 1
            print("[OK] Title contains offer/urgency")

    # 1.2 Meta description (3 params)
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    if desc_match:
        desc = desc_match.group(1)
        if 'Milton' in desc:
            score_meta += 1
            print("[OK] Meta description contains 'Milton'")
        if len(desc) >= 150 and len(desc) <= 160:
            score_meta += 1
            print(f"[OK] Meta description length optimal: {len(desc)} chars (150-160)")
        elif len(desc) > 160:
            print(f"[WARN] Meta description too long: {len(desc)} chars")
        if 'well water' in desc.lower() or 'escarpment' in desc.lower():
            score_meta += 1
            print("[OK] Meta description contains Milton-specific terms")

    # 1.3 Canonical URL (2 params)
    if '<link rel="canonical"' in content:
        score_meta += 1
        print("[OK] Canonical URL present")
    if 'https://nikaappliancerepair.com/locations/milton' in content:
        score_meta += 1
        print("[OK] Canonical URL correct")

    # 1.4 Open Graph tags (6 params)
    og_checks = [
        ('og:type', 'website'),
        ('og:title', 'Milton'),
        ('og:description', None),
        ('og:url', 'milton'),
        ('og:image', None),
        ('twitter:card', 'summary')
    ]

    for prop, required in og_checks:
        if f'property="{prop}"' in content or f'name="{prop}"' in content:
            if required is None or required in content:
                score_meta += 1
                print(f"[OK] {prop} present")

    # 1.5 Schema.org markup (10 params)
    schema_checks = [
        ('@type": "LocalBusiness"', 'LocalBusiness schema'),
        ('"name": "Nika Appliance Repair"', 'Business name'),
        ('"telephone"', 'Phone number'),
        ('"address"', 'Address'),
        ('"geo"', 'Geo coordinates'),
        ('"aggregateRating"', 'Ratings'),
        ('"areaServed"', 'Service areas'),
        ('"openingHoursSpecification"', 'Business hours'),
        ('@type": "FAQPage"', 'FAQ schema'),
        ('@type": "BreadcrumbList"', 'Breadcrumb schema')
    ]

    for check, desc in schema_checks:
        if check in content:
            score_meta += 1
            print(f"[OK] Schema: {desc}")

    # 1.6 H1 tag optimization (5 params)
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if h1_matches:
        h1_text = re.sub(r'<[^>]+>', '', h1_matches[0])
        if 'Milton' in h1_text:
            score_meta += 1
            print("[OK] H1 contains 'Milton'")
        if len(h1_text) >= 40 and len(h1_text) <= 70:
            score_meta += 1
            print(f"[OK] H1 length optimal: {len(h1_text)} chars")
        if 'Appliance' in h1_text and 'Repair' in h1_text:
            score_meta += 1
            print("[OK] H1 contains core keywords")
        if 'Save' in h1_text or '$' in h1_text or 'Fast' in h1_text:
            score_meta += 1
            print("[OK] H1 contains urgency/benefit")
        if len(h1_matches) == 1:
            score_meta += 1
            print("[OK] Single H1 tag (SEO best practice)")

    print(f"\nMeta & SEO Score: {score_meta}/{max_meta} ({score_meta/max_meta*100:.1f}%)")
    total_score += score_meta

    # ========================================================================
    # CATEGORY 2: CONTENT QUALITY (50 parameters) - Target: 98%+
    # ========================================================================
    print("\n[2] CONTENT QUALITY (50 parameters)")
    print("-" * 80)

    score_content = 0
    max_content = 50

    # 2.1 Milton-specific content (20 params) - CRITICAL
    milton_specifics = [
        ('well water', 'Well water mention'),
        ('400+ mg/L', 'Specific hardness data'),
        ('150 mg/L', 'Municipal water comparison'),
        ('Niagara Escarpment', 'Escarpment mention'),
        ('Escarpment climate', 'Climate uniqueness'),
        ('Harrison', 'Harrison neighborhood'),
        ('Mobility Hub', 'Mobility Hub development'),
        ('Mattamy', 'Mattamy builder'),
        ('Great Gulf', 'Great Gulf builder'),
        ('Branthaven', 'Branthaven builder'),
        ('2015-2018', 'Builder boom years'),
        ('compact condo', 'Compact appliances'),
        ('18-24"', 'Compact sizes'),
        ('600-800 sq ft', 'Condo sizes'),
        ('Escarpment Edge', 'Escarpment Edge area'),
        ('Beaty', 'Beaty neighborhood'),
        ('Dempsey', 'Dempsey neighborhood'),
        ('Scott', 'Scott neighborhood'),
        ('132,979', 'Population data'),
        ('3.3 people', 'Household size data')
    ]

    print("\nMilton-Specific Content Analysis:")
    for term, desc in milton_specifics:
        if term in content:
            score_content += 1
            print(f"[OK] {desc}: '{term}' found")
        else:
            print(f"[MISS] {desc}: '{term}' NOT found")

    # 2.2 Content depth (10 params)
    word_count = len(content.split())
    if word_count >= 3000:
        score_content += 2
        print(f"\n[OK] Word count excellent: {word_count} words (target: 3000+)")
    elif word_count >= 2500:
        score_content += 1
        print(f"[OK] Word count good: {word_count} words")

    # H2 headings
    h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    h2_count = len(h2_matches)
    if h2_count >= 8:
        score_content += 2
        print(f"[OK] H2 headings: {h2_count} (excellent structure)")
    elif h2_count >= 6:
        score_content += 1
        print(f"[OK] H2 headings: {h2_count}")

    # Question-based H2s
    question_h2s = [h for h in h2_matches if '?' in h]
    if len(question_h2s) >= 5:
        score_content += 2
        print(f"[OK] Question-based H2s: {len(question_h2s)} (AI search optimized)")
    elif len(question_h2s) >= 3:
        score_content += 1

    # Paragraphs
    p_count = content.count('<p>')
    if p_count >= 30:
        score_content += 2
        print(f"[OK] Paragraph count: {p_count} (comprehensive content)")
    elif p_count >= 20:
        score_content += 1

    # Lists
    li_count = content.count('<li>')
    if li_count >= 50:
        score_content += 2
        print(f"[OK] List items: {li_count} (scannable content)")
    elif li_count >= 30:
        score_content += 1

    # 2.3 Keyword optimization (10 params)
    keywords = [
        ('appliance repair', 15, 'Primary keyword'),
        ('Milton', 20, 'Location keyword'),
        ('well water', 5, 'Unique keyword'),
        ('Escarpment', 5, 'Unique keyword'),
        ('same-day', 3, 'Service keyword'),
        ('warranty', 5, 'Trust keyword'),
        ('certified', 3, 'Trust keyword'),
        ('licensed', 2, 'Trust keyword'),
        ('refrigerator', 5, 'Service keyword'),
        ('dishwasher', 5, 'Service keyword')
    ]

    print("\nKeyword Density Analysis:")
    for keyword, min_count, desc in keywords:
        count = content.lower().count(keyword.lower())
        if count >= min_count:
            score_content += 1
            print(f"[OK] {desc} '{keyword}': {count} occurrences (min: {min_count})")

    # 2.4 Unique content percentage (10 params)
    # Check for template/boilerplate vs unique content
    unique_indicators = [
        'Mattamy/Great Gulf/Branthaven',
        '400+ mg/L well water vs 150 municipal',
        'Niagara Escarpment microclimate',
        'Mobility Hub compact condos',
        'Harrison premium estates',
        '2015-2018 builder boom',
        'Escarpment climate extremes',
        'white crusty buildup',
        'compressor cycles on/off 40% more',
        'European 18-24" appliances'
    ]

    print("\nUnique Content Markers:")
    unique_count = 0
    for marker in unique_indicators:
        if marker in content:
            unique_count += 1
            score_content += 1
            print(f"[OK] Unique marker: '{marker}'")

    print(f"\nContent Quality Score: {score_content}/{max_content} ({score_content/max_content*100:.1f}%)")
    total_score += score_content

    # ========================================================================
    # CATEGORY 3: DATA CONSISTENCY (40 parameters) - Target: 100%
    # ========================================================================
    print("\n[3] DATA CONSISTENCY (40 parameters)")
    print("-" * 80)

    score_data = 0
    max_data = 40

    # 3.1 Phone number consistency (5 params)
    phone_patterns = [
        r'437-747-6737',
        r'4377476737',
        r'\(437\) 747-6737'
    ]

    phone_occurrences = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, content)
        phone_occurrences.extend(matches)

    if len(phone_occurrences) >= 8:
        score_data += 5
        print(f"[OK] Phone number appears {len(phone_occurrences)} times (consistent)")
    elif len(phone_occurrences) >= 5:
        score_data += 3
        print(f"[OK] Phone number appears {len(phone_occurrences)} times")
    else:
        score_data += 1
        print(f"[WARN] Phone number appears only {len(phone_occurrences)} times")

    # 3.2 Address consistency (5 params)
    if '60 Walter Tunny Cresent' in content:
        score_data += 2
        print("[OK] Address consistent")
    if 'Milton' in content and 'L9T 0A5' in content:
        score_data += 2
        print("[OK] City and postal code present")
    if '"latitude": "44.0389"' in content and '"longitude": "-79.4537"' in content:
        score_data += 1
        print("[OK] Geo coordinates present")

    # 3.3 Rating consistency (5 params)
    rating_checks = [
        ('"ratingValue": "4.9"', 'Schema rating'),
        ('4.9', 'Rating display'),
        ('"reviewCount": "5200"', 'Review count schema'),
        ('5,200', 'Review count display'),
        ('5 stars' or '⭐⭐⭐⭐⭐', 'Star display')
    ]

    for check, desc in rating_checks:
        if check in content:
            score_data += 1
            print(f"[OK] {desc} consistent")

    # 3.4 Warranty consistency (3 params)
    warranty_count = content.count('90-day') + content.count('90 days')
    if warranty_count >= 5:
        score_data += 3
        print(f"[OK] Warranty (90-day) mentioned {warranty_count} times (consistent)")
    elif warranty_count >= 3:
        score_data += 2
    else:
        score_data += 1

    # 3.5 Pricing consistency (5 params)
    price_ranges = [
        (r'\$150-\$400', 'Main price range'),
        (r'\$200-\$400', 'Refrigerator'),
        (r'\$150-\$350', 'Washer'),
        (r'\$150-\$300', 'Dryer'),
        (r'\$180-\$380', 'Dishwasher')
    ]

    for pattern, desc in price_ranges:
        if re.search(pattern, content):
            score_data += 1
            print(f"[OK] {desc} pricing present")

    # 3.6 Milton-specific data consistency (12 params)
    milton_data = [
        ('400+ mg/L', 'Well water hardness'),
        ('150 mg/L', 'Municipal hardness'),
        ('132,979', 'Population'),
        ('200,000', 'Projected population'),
        ('3.3 people', 'Average household'),
        ('2015-2018', 'Builder boom period'),
        ('5,000+', 'Homes built'),
        ('3,100', 'Mobility Hub units'),
        ('600-800 sq ft', 'Condo size'),
        ('18-24"', 'Compact appliance size'),
        ('45 minutes', 'Response time'),
        ('7-year', 'Appliance failure age')
    ]

    print("\nMilton Data Consistency:")
    for data, desc in milton_data:
        if data in content:
            score_data += 1
            print(f"[OK] {desc}: '{data}' consistent")

    # 3.7 Brand consistency (5 params)
    if content.count('Frigidaire') >= 3:
        score_data += 1
        print("[OK] Frigidaire brand consistency")
    if content.count('Samsung') >= 2:
        score_data += 1
        print("[OK] Samsung brand consistency")
    if content.count('LG') >= 2:
        score_data += 1
        print("[OK] LG brand consistency")
    if content.count('Whirlpool') >= 2:
        score_data += 1
        print("[OK] Whirlpool brand consistency")
    if content.count('Bosch') >= 2:
        score_data += 1
        print("[OK] Bosch brand consistency")

    print(f"\nData Consistency Score: {score_data}/{max_data} ({score_data/max_data*100:.1f}%)")
    total_score += score_data

    # ========================================================================
    # CATEGORY 4: USER EXPERIENCE & CONVERSION (35 parameters)
    # ========================================================================
    print("\n[4] USER EXPERIENCE & CONVERSION (35 parameters)")
    print("-" * 80)

    score_ux = 0
    max_ux = 35

    # 4.1 CTA buttons (8 params)
    cta_count = content.count('Book') + content.count('Call')
    if cta_count >= 10:
        score_ux += 3
        print(f"[OK] CTA count: {cta_count} (excellent conversion optimization)")
    elif cta_count >= 6:
        score_ux += 2

    if 'href="tel:' in content:
        score_ux += 2
        print("[OK] Click-to-call enabled")

    if 'Book Service Now' in content or 'Book Now' in content:
        score_ux += 1
        print("[OK] Primary CTA present")

    if '#book' in content:
        score_ux += 1
        print("[OK] Booking anchor links present")

    if 'Save $40' in content:
        score_ux += 1
        print("[OK] Discount offer prominent")

    # 4.2 Trust signals (10 params)
    trust_elements = [
        ('90-day warranty', 'Warranty guarantee'),
        ('licensed', 'Licensing'),
        ('insured', 'Insurance'),
        ('certified', 'Certification'),
        ('4.9', 'High rating'),
        ('5,200', 'Review count'),
        ('Same-day', 'Fast service'),
        ('Upfront pricing', 'Transparent pricing'),
        ('No hidden fees', 'Pricing transparency'),
        ('OEM parts', 'Quality parts')
    ]

    for element, desc in trust_elements:
        if element in content:
            score_ux += 1
            print(f"[OK] Trust signal: {desc}")

    # 4.3 Responsive design markers (5 params)
    responsive_checks = [
        ('viewport', 'Viewport meta'),
        ('@media', 'Media queries'),
        ('mobile-menu', 'Mobile menu'),
        ('clamp(', 'Responsive typography'),
        ('max-width: 768px', 'Mobile breakpoint')
    ]

    for check, desc in responsive_checks:
        if check in content:
            score_ux += 1
            print(f"[OK] Responsive: {desc}")

    # 4.4 Accessibility (7 params)
    a11y_checks = [
        ('alt=', 'Image alt text'),
        ('aria-label', 'ARIA labels'),
        ('aria-expanded', 'ARIA states'),
        ('role=', 'ARIA roles'),
        ('Skip to main content', 'Skip navigation'),
        ('tabindex', 'Keyboard navigation'),
        ('<h1', 'Semantic headings')
    ]

    for check, desc in a11y_checks:
        if check in content:
            score_ux += 1
            print(f"[OK] Accessibility: {desc}")

    # 4.5 Social proof (5 params)
    if 'testimonial' in content.lower():
        score_ux += 1
        print("[OK] Testimonials section present")
    if 'youtube' in content.lower() or 'video' in content.lower():
        score_ux += 1
        print("[OK] Video testimonials present")
    if '⭐' in content or 'star' in content.lower():
        score_ux += 1
        print("[OK] Star ratings displayed")
    if 'Verified' in content:
        score_ux += 1
        print("[OK] Verified reviews marker")
    if 'Real Customers' in content or 'Real Stories' in content:
        score_ux += 1
        print("[OK] Authenticity markers")

    print(f"\nUX & Conversion Score: {score_ux}/{max_ux} ({score_ux/max_ux*100:.1f}%)")
    total_score += score_ux

    # ========================================================================
    # CATEGORY 5: TECHNICAL SEO (35 parameters)
    # ========================================================================
    print("\n[5] TECHNICAL SEO (35 parameters)")
    print("-" * 80)

    score_tech = 0
    max_tech = 35

    # 5.1 Structured data (10 params)
    structured_data_types = [
        ('LocalBusiness', 'Local business'),
        ('FAQPage', 'FAQ page'),
        ('BreadcrumbList', 'Breadcrumbs'),
        ('WebPage', 'Web page'),
        ('HowTo', 'How-to'),
        ('Service', 'Service'),
        ('AggregateRating', 'Ratings'),
        ('OpeningHoursSpecification', 'Hours'),
        ('PostalAddress', 'Address'),
        ('GeoCoordinates', 'Location')
    ]

    for dtype, desc in structured_data_types:
        if dtype in content:
            score_tech += 1
            print(f"[OK] Structured data: {desc}")

    # 5.2 Image optimization (5 params)
    if 'loading="lazy"' in content:
        score_tech += 1
        print("[OK] Lazy loading enabled")
    if 'webp' in content:
        score_tech += 1
        print("[OK] WebP images used")
    if 'fetchpriority="high"' in content:
        score_tech += 1
        print("[OK] Priority hints present")
    if content.count('alt="') >= 10:
        score_tech += 1
        print("[OK] Image alt text coverage")
    if 'width=' in content and 'height=' in content:
        score_tech += 1
        print("[OK] Image dimensions specified")

    # 5.3 Performance optimization (8 params)
    perf_checks = [
        ('rel="preload"', 'Resource preloading'),
        ('rel="preconnect"', 'DNS preconnect'),
        ('defer', 'Script deferring'),
        ('async', 'Async loading'),
        ('.min.css', 'Minified CSS'),
        ('.min.js', 'Minified JS'),
        ('display=swap', 'Font display swap'),
        ('crossorigin', 'CORS optimization')
    ]

    for check, desc in perf_checks:
        if check in content:
            score_tech += 1
            print(f"[OK] Performance: {desc}")

    # 5.4 Internal linking (7 params)
    internal_links = re.findall(r'href="\.\./', content)
    if len(internal_links) >= 20:
        score_tech += 3
        print(f"[OK] Internal links: {len(internal_links)} (excellent site structure)")
    elif len(internal_links) >= 10:
        score_tech += 2

    if '../services/' in content:
        score_tech += 1
        print("[OK] Service page links present")
    if '../locations/' in content:
        score_tech += 1
        print("[OK] Location page links present")
    if '../areas/' in content:
        score_tech += 1
        print("[OK] Area page links present")
    if '#' in content:
        score_tech += 1
        print("[OK] Anchor links present")

    # 5.5 Mobile optimization (5 params)
    if 'width=device-width' in content:
        score_tech += 1
        print("[OK] Responsive viewport")
    if 'mobile' in content.lower():
        score_tech += 1
        print("[OK] Mobile-specific content")
    if 'max-width: 768px' in content or '768px' in content:
        score_tech += 1
        print("[OK] Mobile breakpoints")
    if 'overflow-x' in content:
        score_tech += 1
        print("[OK] Horizontal scroll prevention")
    if 'touch' in content.lower() or 'tap' in content.lower():
        score_tech += 1
        print("[OK] Touch optimization")

    print(f"\nTechnical SEO Score: {score_tech}/{max_tech} ({score_tech/max_tech*100:.1f}%)")
    total_score += score_tech

    # ========================================================================
    # CATEGORY 6: LOCAL SEO (30 parameters)
    # ========================================================================
    print("\n[6] LOCAL SEO (30 parameters)")
    print("-" * 80)

    score_local = 0
    max_local = 30

    # 6.1 Location mentions (10 params)
    location_targets = [
        ('Milton', 30, 'City name'),
        ('Halton Region', 5, 'Region'),
        ('Ontario', 3, 'Province'),
        ('GTA', 3, 'Metro area'),
        ('Burlington', 2, 'Nearby city'),
        ('Oakville', 2, 'Nearby city'),
        ('Mississauga', 2, 'Nearby city'),
        ('Georgetown', 1, 'Nearby town'),
        ('Halton Hills', 1, 'Nearby area'),
        ('Toronto', 1, 'Major city')
    ]

    for location, min_count, desc in location_targets:
        count = content.count(location)
        if count >= min_count:
            score_local += 1
            print(f"[OK] Location: {desc} '{location}' ({count} times)")

    # 6.2 Neighborhood mentions (10 params)
    neighborhoods = [
        'Harrison', 'Escarpment Edge', 'Mobility Hub', 'Beaty', 'Dempsey',
        'Scott', 'Downtown Milton', 'Escarpment', 'rural Milton', 'premium'
    ]

    print("\nNeighborhood Coverage:")
    for neighborhood in neighborhoods:
        if neighborhood in content:
            score_local += 1
            print(f"[OK] Neighborhood: {neighborhood}")

    # 6.3 Service area schema (5 params)
    if '"areaServed"' in content:
        score_local += 2
        print("[OK] Service area schema present")
    if '"@type": "City"' in content:
        score_local += 1
        print("[OK] City-level targeting")
    if '"name": "Milton"' in content:
        score_local += 1
        print("[OK] Milton in schema")
    if content.count('"@type": "City"') >= 5:
        score_local += 1
        print("[OK] Multiple cities in schema")

    # 6.4 Local business information (5 params)
    if 'Milton' in content and 'ON' in content:
        score_local += 1
        print("[OK] City and province")
    if 'L9T 0A5' in content:
        score_local += 1
        print("[OK] Postal code")
    if 'Service Hours' in content or 'openingHours' in content:
        score_local += 1
        print("[OK] Business hours")
    if 'care@niappliancerepair.ca' in content:
        score_local += 1
        print("[OK] Local email")
    if '437-747-6737' in content:
        score_local += 1
        print("[OK] Local phone")

    print(f"\nLocal SEO Score: {score_local}/{max_local} ({score_local/max_local*100:.1f}%)")
    total_score += score_local

    # ========================================================================
    # CATEGORY 7: CONTENT STRUCTURE (28 parameters)
    # ========================================================================
    print("\n[7] CONTENT STRUCTURE (28 parameters)")
    print("-" * 80)

    score_structure = 0
    max_structure = 28

    # 7.1 Section diversity (10 params)
    sections = [
        ('hero-section', 'Hero'),
        ('services-section', 'Services'),
        ('about-section', 'About'),
        ('testimonial', 'Testimonials'),
        ('common-problems', 'Problems'),
        ('faq-section', 'FAQ'),
        ('booking', 'Booking'),
        ('areas', 'Service areas'),
        ('brands', 'Brands'),
        ('how-it-works', 'Process')
    ]

    for section, desc in sections:
        if section in content:
            score_structure += 1
            print(f"[OK] Section: {desc}")

    # 7.2 FAQ structure (8 params)
    faq_items = content.count('faq-item')
    if faq_items >= 10:
        score_structure += 3
        print(f"[OK] FAQ items: {faq_items} (comprehensive)")
    elif faq_items >= 5:
        score_structure += 2

    if 'faq-question' in content:
        score_structure += 1
        print("[OK] FAQ questions structured")
    if 'faq-answer' in content:
        score_structure += 1
        print("[OK] FAQ answers structured")
    if 'aria-expanded' in content:
        score_structure += 1
        print("[OK] FAQ accordion accessibility")
    if '"@type": "FAQPage"' in content:
        score_structure += 1
        print("[OK] FAQ schema markup")
    if '"@type": "Question"' in content:
        score_structure += 1
        print("[OK] Question schema markup")

    # 7.3 Content hierarchy (5 params)
    h2_count = content.count('<h2')
    h3_count = content.count('<h3')

    if h2_count >= 8:
        score_structure += 2
        print(f"[OK] H2 headings: {h2_count}")
    elif h2_count >= 5:
        score_structure += 1

    if h3_count >= 10:
        score_structure += 2
        print(f"[OK] H3 headings: {h3_count}")
    elif h3_count >= 5:
        score_structure += 1

    if h2_count > 0 and h3_count > h2_count:
        score_structure += 1
        print("[OK] Proper heading hierarchy")

    # 7.4 List formatting (5 params)
    ul_count = content.count('<ul')
    ol_count = content.count('<ol')

    if ul_count >= 5:
        score_structure += 2
        print(f"[OK] Unordered lists: {ul_count}")
    elif ul_count >= 3:
        score_structure += 1

    if ol_count >= 1:
        score_structure += 1
        print(f"[OK] Ordered lists present")

    if li_count >= 50:
        score_structure += 2
        print(f"[OK] List items: {li_count}")

    print(f"\nContent Structure Score: {score_structure}/{max_structure} ({score_structure/max_structure*100:.1f}%)")
    total_score += score_structure

    # ========================================================================
    # CATEGORY 8: MILTON-SPECIFIC EXCELLENCE (30 parameters)
    # ========================================================================
    print("\n[8] MILTON-SPECIFIC EXCELLENCE (30 parameters)")
    print("-" * 80)

    score_milton = 0
    max_milton = 30

    # 8.1 Well water expertise (6 params)
    well_water_markers = [
        '400+ mg/L well water vs 150 municipal',
        'extreme hardness variance',
        'white crusty buildup',
        'mineral damage',
        'iron staining',
        'whole-house water softener'
    ]

    print("Well Water Expertise:")
    for marker in well_water_markers:
        if marker in content:
            score_milton += 1
            print(f"[OK] Well water detail: {marker}")

    # 8.2 Escarpment climate expertise (6 params)
    escarpment_markers = [
        'Niagara Escarpment microclimate',
        'temperature swings',
        'compressor cycles on/off 40% more',
        'garage installations',
        'Escarpment climate extremes',
        'UNESCO World Biosphere Reserve'
    ]

    print("\nEscarpment Climate Expertise:")
    for marker in escarpment_markers:
        if marker in content:
            score_milton += 1
            print(f"[OK] Escarpment detail: {marker}")

    # 8.3 Builder boom expertise (6 params)
    builder_markers = [
        'Mattamy, Great Gulf, Branthaven',
        '2015-2018 builder boom',
        '5,000+ homes',
        '7-year failure mark',
        'Frigidaire Gallery',
        'bulk-purchased'
    ]

    print("\nBuilder Boom Expertise:")
    for marker in builder_markers:
        if marker in content:
            score_milton += 1
            print(f"[OK] Builder detail: {marker}")

    # 8.4 Compact appliance expertise (6 params)
    compact_markers = [
        'Mobility Hub',
        '600-800 sq ft',
        'European compact appliances',
        '18-24"',
        'metric parts',
        'Bosch, Blomberg, Beko'
    ]

    print("\nCompact Appliance Expertise:")
    for marker in compact_markers:
        if marker in content:
            score_milton += 1
            print(f"[OK] Compact detail: {marker}")

    # 8.5 Premium luxury expertise (6 params)
    luxury_markers = [
        'Harrison premium',
        'Sub-Zero, Wolf, Thermador',
        'factory-certified',
        'Escarpment-view',
        '$100k-200k premium',
        'white-glove service'
    ]

    print("\nPremium Luxury Expertise:")
    for marker in luxury_markers:
        if marker in content:
            score_milton += 1
            print(f"[OK] Luxury detail: {marker}")

    print(f"\nMilton-Specific Excellence Score: {score_milton}/{max_milton} ({score_milton/max_milton*100:.1f}%)")
    total_score += score_milton

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("BMAD v3.1 COMPREHENSIVE TEST RESULTS")
    print("=" * 80)

    categories = [
        ("Meta & SEO Optimization", score_meta, max_meta),
        ("Content Quality", score_content, max_content),
        ("Data Consistency", score_data, max_data),
        ("UX & Conversion", score_ux, max_ux),
        ("Technical SEO", score_tech, max_tech),
        ("Local SEO", score_local, max_local),
        ("Content Structure", score_structure, max_structure),
        ("Milton-Specific Excellence", score_milton, max_milton)
    ]

    for name, score, maximum in categories:
        percentage = (score / maximum * 100) if maximum > 0 else 0
        status = "EXCELLENT" if percentage >= 95 else "GOOD" if percentage >= 85 else "NEEDS WORK"
        print(f"{name:.<40} {score}/{maximum} ({percentage:.1f}%) [{status}]")

    print("-" * 80)
    overall_percentage = (total_score / total_max * 100)
    print(f"OVERALL BMAD v3.1 SCORE: {total_score}/{total_max} ({overall_percentage:.1f}%)")
    print("=" * 80)

    # Deployment readiness
    print("\nDEPLOYMENT READINESS ASSESSMENT:")
    print("-" * 80)

    if overall_percentage >= 95:
        print("[READY] Deployment APPROVED - Excellent BMAD v3.1 compliance")
    elif overall_percentage >= 90:
        print("[READY] Deployment APPROVED - Good BMAD v3.1 compliance")
    elif overall_percentage >= 85:
        print("[CAUTION] Deployment CONDITIONAL - Minor improvements recommended")
    else:
        print("[NOT READY] Deployment NOT RECOMMENDED - Significant issues found")

    print("\nKEY FINDINGS:")
    print("-" * 80)

    # Content Quality Assessment
    content_pct = (score_content / max_content * 100)
    if content_pct >= 98:
        print(f"[OK] Content Quality: {content_pct:.1f}% - TARGET MET (98%+)")
    else:
        print(f"[WARN] Content Quality: {content_pct:.1f}% - Below target (98%+)")

    # Data Consistency Assessment
    data_pct = (score_data / max_data * 100)
    if data_pct >= 100:
        print(f"[OK] Data Consistency: {data_pct:.1f}% - TARGET MET (100%)")
    else:
        print(f"[WARN] Data Consistency: {data_pct:.1f}% - Below target (100%)")

    # Milton-Specific Assessment
    milton_pct = (score_milton / max_milton * 100)
    if milton_pct >= 90:
        print(f"[OK] Milton-Specific Content: {milton_pct:.1f}% - Excellent coverage")
    else:
        print(f"[WARN] Milton-Specific Content: {milton_pct:.1f}% - Needs more unique content")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_milton_page()
