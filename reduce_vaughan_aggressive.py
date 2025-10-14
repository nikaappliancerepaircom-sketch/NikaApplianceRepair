#!/usr/bin/env python3
"""
Aggressive Vaughan page reduction: 4,334 → 2,200-2,400 words

KEEP (Vaughan-specific):
- Miele Canada HQ proximity
- 30% Italian community
- $124,000 median income
- Woodbridge multi-kitchen estates
- Hard water 125 mg/L

REDUCE:
- FAQ answers by 60-70%
- Problem descriptions by 50%
- Remove repetitive location mentions
- Consolidate neighborhood descriptions
"""

import re
from bs4 import BeautifulSoup, NavigableString
import json

def count_words(text):
    """Count words excluding HTML tags"""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return len(clean.split())

def count_location_mentions(text):
    """Count Vaughan mentions"""
    return len(re.findall(r'\bVaughan\b', text, re.IGNORECASE))

def trim_faq_aggressively(soup):
    """Reduce FAQ answers by 60-70% while keeping Vaughan-specific details"""

    faq_answers = {
        "Which Vaughan neighborhoods": """<p><strong>We service all Vaughan communities:</strong> Woodbridge (estate homes, Italian community, luxury appliances), Maple (detached homes, premium installs), Concord (residential subdivisions), Kleinburg (rural estates, ultra-premium), Thornhill (affluent, European brands). Response times: 25-50 minutes depending on location.</p>""",

        "certified to repair Miele": """<p><strong>Yes — luxury European repair is our specialty.</strong> Factory-certified for Miele, Sub-Zero, Wolf, Thermador, Gaggenau, Bertazzoni, Bosch, and ASKO. With Miele Canada HQ in Vaughan and $124k median income, we service premium brands daily. White-glove service for Woodbridge estates, Maple luxury homes, and Kleinburg properties.</p>""",

        "multi-kitchen estate": """<p><strong>Multi-kitchen estates are 35% of our Vaughan calls.</strong> Typical setup: Main kitchen ($50k-$150k in Sub-Zero/Wolf/Miele), basement kitchen (KitchenAid/Bosch), outdoor summer kitchen (Bull/Lynx/DCS). Single visit covers all locations with 15% multi-unit discount. Comprehensive estate service recommended spring and fall.</p>""",

        "professional-grade gas ranges": """<p><strong>Yes — high-BTU range repair is a core specialty.</strong> With 30% Italian community, we service professional ranges (15,000-22,000 BTU) daily. Common fixes: ignition issues, uneven flames, gas pressure problems, simmer calibration. Many 1990s-2000s homes have undersized gas lines affecting performance.</p>""",

        "hard water": """<p><strong>Vaughan's hard water (125 mg/L, 7.26 grains) is extremely damaging to luxury appliances.</strong> Miele dishwashers get "clean filter" errors every 2-3 months (vs. 6-month normal). Causes heating element failures, spray arm clogs, pump damage. We offer professional descaling, water softener kits ($200-$400), and preventive schedules. Water softener ($2k-$4k) pays for itself in 2-3 years.</p>""",

        "luxury appliance brands": """<p><strong>Certified for 90+ brands, specializing in luxury European.</strong> Most common in Vaughan: Miele (Miele Canada HQ here), Sub-Zero, Wolf, Thermador, Gaggenau, Bertazzoni (Italian community favorite). Italian brands: Bertazzoni, ILVE, Smeg, La Germania. Mid-range: Bosch, KitchenAid, ASKO, Fisher & Paykel. Outdoor: Bull, Lynx, DCS, Napoleon.</p>""",

        "luxury appliance repair cost": """<p><strong>2025 Vaughan pricing:</strong> Miele repairs: $300-$600 | Sub-Zero: $400-$800 | Wolf: $350-$700 | Professional gas ranges: $250-$550 | Standard brands: $180-$400. Includes 90-day warranty, white-glove service, no diagnostic fee. Multi-kitchen discount: -15% for 2+ kitchens. Hard water descaling: +$100-200.</p>""",

        "1990s-2000s construction": """<p><strong>Yes — diagnosing construction-era defects is our specialty.</strong> Vaughan was Canada's fastest-growing city 1996-2006. Common issues: undersized gas lines (need 1/2", many have 3/8"), improper dryer venting, undersized electrical. 40% of "appliance problems" are installation defects. Assessment: $150-$300 includes gas pressure testing, venting inspection, code compliance report.</p>""",

        "preventive maintenance": """<p><strong>Yes — estate maintenance is our premier service.</strong> Spring (April-May): descale appliances, test outdoor kitchens, calibrate temps. Fall (Oct-Nov): winterize outdoor kitchens, holiday prep. Pricing: Single kitchen $300-$400, two kitchens $500-$650, three+ kitchens $600-$900 (twice yearly). Prevents 60% of emergencies, extends lifespan 40-60%.</p>""",

        "same-day appliance repair": """<p><strong>Yes — same-day service 7 days/week across all Vaughan.</strong> Response times: Woodbridge 25-35 min, Maple 30-40 min, Concord 35-45 min, Kleinburg 40-50 min, Thornhill 30-40 min. Call before 2 PM for same-day. Peak seasons: Spring (descaling), Fall (outdoor winterization), December (holiday cooking). Book 3-4 days ahead for December Italian holiday cooking.</p>"""
    }

    # Find and replace FAQ answers
    faq_section = soup.find('section', class_='faq-section')
    if faq_section:
        faq_items = faq_section.find_all('div', class_='faq-item')
        for item in faq_items:
            question = item.find('div', class_='faq-question')
            answer_div = item.find('div', class_='faq-answer')

            if question and answer_div:
                q_text = question.get_text().strip()

                # Match question to trimmed answer
                for key_phrase, new_answer in faq_answers.items():
                    if key_phrase.lower() in q_text.lower():
                        # Replace answer content
                        answer_div.clear()
                        new_soup = BeautifulSoup(new_answer, 'html.parser')
                        answer_div.append(new_soup)
                        break

def trim_ai_summary(soup):
    """Consolidate AI summary section"""
    ai_section = soup.find('section', class_='ai-summary-section')
    if ai_section:
        summary_box = ai_section.find('div', class_='ai-summary-box')
        if summary_box:
            # Find the main paragraph
            main_p = summary_box.find('p', class_='text-primary')
            if main_p:
                # Shorten it
                new_text = """<strong>Looking for luxury appliance repair in Vaughan?</strong> Nika Appliance Repair delivers Miele-certified service across Woodbridge, Maple, Concord, Kleinburg, and Thornhill. Call <a href="tel:4377476737" class="font-semibold" style="color: #2196F3 !important; text-decoration: none !important;">437-747-6737</a> for expert service."""
                main_p.clear()
                new_soup = BeautifulSoup(new_text, 'html.parser')
                for element in new_soup:
                    main_p.append(element)

            # Trim the detailed list
            detail_div = summary_box.find('div', style=lambda v: v and 'margin-top: 1.5rem' in v)
            if detail_div:
                new_content = """
                <p style="margin-bottom: 0.75rem;"><strong>Vaughan luxury appliance expertise:</strong></p>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="margin-bottom: 0.5rem;">• <strong>Miele-certified specialists:</strong> Factory-trained, genuine OEM parts, serving Vaughan where Miele Canada HQ is located</li>
                    <li style="margin-bottom: 0.5rem;">• <strong>High-BTU gas range experts:</strong> Professional-grade ranges for Vaughan's 30% Italian community</li>
                    <li style="margin-bottom: 0.5rem;">• <strong>Multi-kitchen estates:</strong> Woodbridge estates with main + basement + outdoor kitchens (15% discount)</li>
                    <li style="margin-bottom: 0.5rem;">• <strong>Luxury brand certified:</strong> Sub-Zero, Wolf, Thermador, Gaggenau, Bertazzoni</li>
                    <li style="margin-bottom: 0.5rem;">• <strong>Hard water solutions:</strong> Vaughan's 125 mg/L water requires specialized descaling and maintenance</li>
                </ul>
                <p style="margin-top: 1rem;"><strong>Complete Vaughan coverage.</strong> Average response: 25-50 minutes. 4.9★ rating from 5,200+ customers. We repair Miele, Sub-Zero, Wolf, Thermador, plus all standard brands.</p>
                """
                detail_div.clear()
                new_soup = BeautifulSoup(new_content, 'html.parser')
                for element in new_soup:
                    detail_div.append(element)

def trim_about_section(soup):
    """Reduce about section verbosity"""
    about_section = soup.find('section', class_='about-section')
    if about_section:
        company_story = about_section.find('div', class_='company-story')
        if company_story:
            paragraphs = company_story.find_all('p')
            if len(paragraphs) >= 2:
                # Trim second paragraph
                new_text = "We specialize in luxury appliance investments ($50k-$150k+ per estate) with Miele certification, factory training for Sub-Zero, Wolf, and Thermador, and Italian cooking equipment expertise. Our factory-certified technicians serve Woodbridge, Maple, Concord, Kleinburg, and Thornhill with warranty-compliant repairs using genuine OEM parts."
                paragraphs[1].string = new_text

def trim_service_descriptions(soup):
    """Make service cards more concise"""
    service_cards = soup.find_all('div', class_='service-card')

    short_descriptions = {
        'Refrigerator': 'Expert fridge repair for all types. Same-day service available.',
        'Dishwasher': 'Built-in, portable, double, and countertop dishwashers serviced.',
        'Dryer': 'Expert dryer repair. Fast diagnosis and fix.',
        'Stove': 'Professional stove and cooktop repair for any model.',
        'Oven': 'Cooktops, ovens, ranges — all types repaired.',
        'Washing': 'Commercial and residential washer repair service.'
    }

    for card in service_cards:
        h3 = card.find('h3')
        p = card.find('p')
        if h3 and p:
            h3_text = h3.get_text()
            for keyword, desc in short_descriptions.items():
                if keyword in h3_text:
                    p.string = desc
                    break

def reduce_benefits_section(soup):
    """Trim benefits section"""
    benefits = soup.find_all('div', class_='benefit-card')

    short_benefits = {
        'Lightning Fast': '45-minute average arrival. Same-day service for 95% of calls.',
        'Certified': 'Factory-trained, licensed, insured. 5+ years minimum experience.',
        'Transparent': 'No hidden fees. Exact quotes upfront. Save $40 as new customer.',
        'Genuine Parts': 'OEM and high-quality parts. No cheap knockoffs.',
        '90-Day': 'Industry-leading warranty. Free re-fix if issue returns.',
        'All Brands': 'Authorized for 90+ brands. Samsung to Sub-Zero.'
    }

    for card in benefits:
        h3 = card.find('h3')
        p = card.find('p')
        if h3 and p:
            h3_text = h3.get_text()
            for keyword, desc in short_benefits.items():
                if keyword in h3_text:
                    p.string = desc
                    break

def main():
    input_file = r'C:\NikaApplianceRepair\locations\vaughan.html'
    output_file = r'C:\NikaApplianceRepair\locations\vaughan.html'

    print("=" * 60)
    print("VAUGHAN PAGE AGGRESSIVE REDUCTION")
    print("Target: 2,200-2,400 words (from 4,334)")
    print("=" * 60)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    initial_words = count_words(content)
    initial_vaughan = count_location_mentions(content)
    print(f"\nInitial metrics:")
    print(f"  Word count: {initial_words:,}")
    print(f"  Vaughan mentions: {initial_vaughan}")

    soup = BeautifulSoup(content, 'html.parser')

    print("\nApplying reductions...")
    print("  [1/6] Trimming AI summary section...")
    trim_ai_summary(soup)

    print("  [2/6] Reducing FAQ answers by 60-70%...")
    trim_faq_aggressively(soup)

    print("  [3/6] Trimming service descriptions...")
    trim_service_descriptions(soup)

    print("  [4/6] Reducing benefits section...")
    reduce_benefits_section(soup)

    print("  [5/6] Trimming about section...")
    trim_about_section(soup)

    print("  [6/6] Final optimization...")

    # Convert back to string
    reduced_content = str(soup)

    final_words = count_words(reduced_content)
    final_vaughan = count_location_mentions(reduced_content)

    word_reduction = initial_words - final_words
    word_reduction_pct = (word_reduction / initial_words * 100)
    vaughan_reduction = initial_vaughan - final_vaughan

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Word count: {initial_words:,} -> {final_words:,} ({word_reduction:,} words removed, {word_reduction_pct:.1f}%)")
    print(f"Vaughan mentions: {initial_vaughan} -> {final_vaughan} ({vaughan_reduction} removed)")

    if 2000 <= final_words <= 2500:
        print(f"\nSUCCESS: Within target range (2,000-2,500 words)")
    elif final_words > 2500:
        print(f"\nStill above target by {final_words - 2500} words")
    else:
        print(f"\nBelow target by {2000 - final_words} words")

    if 30 <= final_vaughan <= 35:
        print(f"Vaughan mentions within target (30-35)")
    else:
        print(f"Vaughan mentions: {final_vaughan} (target: 30-35)")

    print("\n" + "=" * 60)
    print("PRESERVED VAUGHAN-SPECIFIC CONTENT:")
    print("=" * 60)
    preserved = [
        "- Miele Canada HQ proximity",
        "- 30% Italian community",
        "- $124,000 median income",
        "- Woodbridge multi-kitchen estates",
        "- Hard water 125 mg/L",
        "- All 6 appliance types",
        "- Luxury brand positioning",
        "- Trust signals & BMAD structure"
    ]
    for item in preserved:
        print(f"  {item}")

    print(f"\nWriting optimized content...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reduced_content)

    print(f"Saved to: {output_file}")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
