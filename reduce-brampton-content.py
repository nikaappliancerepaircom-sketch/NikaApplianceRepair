#!/usr/bin/env python3
"""
Reduce Brampton location page content from 4,748 words to 2,000-2,500 words.
Preserve all Brampton-specific content while reducing FAQs, redundancy, and generic statements.
"""

import re
from bs4 import BeautifulSoup

def count_words(text):
    """Count words in text (excluding HTML tags)"""
    text_only = re.sub(r'<[^>]+>', '', text)
    return len(text_only.split())

def reduce_brampton_content():
    # Read the file
    with open(r'C:\NikaApplianceRepair\locations\brampton.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original word count: {count_words(content)}")

    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Track changes
    changes = []

    # 1. REDUCE FAQ SECTION - trim answers by 40%
    faq_section = soup.find('section', class_='faq-section')
    if faq_section:
        faq_items = faq_section.find_all('div', class_='faq-item')
        for item in faq_items:
            answer = item.find('div', class_='faq-answer')
            if answer:
                original_text = answer.get_text()
                paragraphs = answer.find_all('p')

                # Keep first paragraph, trim subsequent ones
                if len(paragraphs) > 1:
                    # Remove all but first paragraph
                    for p in paragraphs[1:]:
                        p.decompose()
                    changes.append(f"FAQ trimmed: {item.find('h3').get_text()[:50]}")

                # Also shorten remaining paragraph if too long
                if paragraphs:
                    p_text = paragraphs[0].get_text()
                    if len(p_text) > 200:
                        # Keep first 2 sentences
                        sentences = p_text.split('. ')
                        if len(sentences) > 2:
                            paragraphs[0].string = '. '.join(sentences[:2]) + '.'

    # 2. REDUCE "Why Choose Us" benefit descriptions
    benefit_cards = soup.find_all('div', class_='benefit-card')
    for card in benefit_cards:
        p = card.find('p')
        if p:
            text = p.get_text()
            # Keep first sentence only
            sentences = text.split('. ')
            if len(sentences) > 1:
                p.string = sentences[0] + '.'
                changes.append(f"Benefit trimmed: {card.find('h3').get_text()[:40]}")

    # 3. REDUCE Service descriptions (keep them brief)
    service_cards = soup.find_all('div', class_='service-card')
    for card in service_cards:
        p = card.find('p')
        if p:
            text = p.get_text()
            # Keep only first sentence
            sentences = text.split('. ')
            if len(sentences) > 1:
                p.string = sentences[0] + '.'

    # 4. TRIM About section - reduce redundancy
    about_section = soup.find('section', class_='about-section')
    if about_section:
        company_story = about_section.find('div', class_='company-story')
        if company_story:
            paragraphs = company_story.find_all('p')
            # Keep only first paragraph
            if len(paragraphs) > 1:
                for p in paragraphs[1:]:
                    p.decompose()
                changes.append("About section: removed 2nd paragraph")

    # 5. REDUCE Common Problems - Keep structure but trim descriptions
    problem_cards = soup.find_all('div', class_='problem-card')
    for card in problem_cards:
        paragraphs = card.find_all('p')
        # Keep: title line (Brampton-specific), symptoms, solution
        # Remove: redundant explanations
        if len(paragraphs) >= 3:
            # Keep first 3 paragraphs max (challenge, symptoms, solution)
            for p in paragraphs[3:]:
                # Check if it's repetitive
                if 'common' in p.get_text().lower() or len(p.get_text()) > 250:
                    p.decompose()

    # 6. REDUCE location name mentions in AI summary
    ai_summary = soup.find('section', class_='ai-summary-section')
    if ai_summary:
        # Replace repetitive "Brampton" mentions with pronouns
        text = str(ai_summary)
        # Count current Brampton mentions
        brampton_count = text.count('Brampton')
        print(f"AI Summary has {brampton_count} 'Brampton' mentions")

    # Get updated content
    updated_content = str(soup)

    print(f"\nUpdated word count: {count_words(updated_content)}")
    print(f"\nChanges made: {len(changes)}")
    for change in changes[:10]:
        print(f"  - {change}")

    # Save the updated content
    with open(r'C:\NikaApplianceRepair\locations\brampton.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("\n✓ File updated successfully!")

    return count_words(updated_content)

if __name__ == '__main__':
    final_count = reduce_brampton_content()
    print(f"\n{'='*60}")
    print(f"TARGET: 2,200-2,400 words")
    print(f"ACHIEVED: {final_count} words")
    if 2200 <= final_count <= 2500:
        print("✓ TARGET MET!")
    else:
        print(f"⚠ Need to adjust by {abs(2300 - final_count)} words")
    print(f"{'='*60}")
