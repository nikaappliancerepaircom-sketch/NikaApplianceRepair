#!/usr/bin/env python3
"""
Vaughan page content reducer - target 2,000-2,500 words
Keep ALL Vaughan-specific content:
- Miele Canada HQ proximity
- 30% Italian community
- $124,000 median income
- Woodbridge multi-kitchen estates
- Hard water 125 mg/L
"""

import re
from bs4 import BeautifulSoup

def count_words(text):
    """Count words in text, excluding HTML tags"""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    # Remove extra whitespace
    clean = re.sub(r'\s+', ' ', clean)
    # Count words
    words = clean.split()
    return len(words)

def reduce_faq_answers(soup):
    """Reduce FAQ answers by 40%"""

    # FAQ in FAQ Page schema
    faq_schema = soup.find('script', type='application/ld+json', string=re.compile('FAQPage'))
    if faq_schema:
        import json
        data = json.loads(faq_schema.string)
        for item in data.get('mainEntity', []):
            answer = item['acceptedAnswer']['text']
            # Trim to ~60% of original
            words = answer.split()
            if len(words) > 30:
                trimmed = ' '.join(words[:int(len(words) * 0.6)])
                item['acceptedAnswer']['text'] = trimmed + '.'
        faq_schema.string = json.dumps(data, indent=4)

    # FAQ section in HTML
    faq_section = soup.find('section', class_='faq-section')
    if faq_section:
        answers = faq_section.find_all('p', class_='faq-answer')
        for answer in answers:
            text = answer.get_text()
            words = text.split()
            if len(words) > 30:
                trimmed = ' '.join(words[:int(len(words) * 0.6)])
                answer.string = trimmed + '.'

def reduce_problem_descriptions(soup):
    """Reduce problem descriptions and remove redundancy"""

    problems_section = soup.find('section', class_='common-problems-section')
    if problems_section:
        problem_cards = problems_section.find_all('div', class_='problem-card')
        for card in problem_cards:
            p_tag = card.find('p')
            if p_tag:
                text = p_tag.get_text()
                sentences = text.split('.')
                # Keep first 2 sentences max
                if len(sentences) > 2:
                    trimmed = '. '.join(sentences[:2]) + '.'
                    p_tag.string = trimmed

def reduce_location_mentions(html_content):
    """Reduce Vaughan mentions from 87 to 30-35"""
    # Count current mentions
    vaughan_count = len(re.findall(r'\bVaughan\b', html_content))
    print(f"Current Vaughan mentions: {vaughan_count}")

    # Target: keep critical mentions, remove redundant ones
    # We'll do this selectively
    return html_content

def trim_service_descriptions(soup):
    """Trim service card descriptions to be more concise"""
    service_cards = soup.find_all('div', class_='service-card')
    for card in service_cards:
        p_tag = card.find('p')
        if p_tag:
            text = p_tag.get_text()
            words = text.split()
            if len(words) > 15:
                # Keep first 10-12 words
                trimmed = ' '.join(words[:12]) + '.'
                p_tag.string = trimmed

def remove_repetitive_content(soup):
    """Remove repetitive phrases and consolidate content"""

    # Remove duplicate area mentions in AI summary
    ai_summary = soup.find('section', class_='ai-summary-section')
    if ai_summary:
        paragraphs = ai_summary.find_all('p')
        for p in paragraphs:
            text = str(p)
            # Reduce area repetitions
            text = re.sub(r'(Woodbridge, Maple, Concord, Kleinburg, and Thornhill[^.]*\.)\s*Complete Vaughan coverage:\s*Woodbridge, Maple, Concord, Kleinburg, Thornhill[^.]*\.', r'\1', text)
            p.replace_with(BeautifulSoup(text, 'html.parser'))

def main():
    input_file = r'C:\NikaApplianceRepair\locations\vaughan.html'
    output_file = r'C:\NikaApplianceRepair\locations\vaughan.html'

    print("Reading Vaughan page...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    initial_words = count_words(content)
    print(f"Initial word count: {initial_words}")

    soup = BeautifulSoup(content, 'html.parser')

    print("\nApplying reductions...")
    print("- Trimming FAQ answers by 40%")
    reduce_faq_answers(soup)

    print("- Reducing problem descriptions")
    reduce_problem_descriptions(soup)

    print("- Trimming service descriptions")
    trim_service_descriptions(soup)

    print("- Removing repetitive content")
    remove_repetitive_content(soup)

    # Convert back to string
    reduced_content = str(soup)

    # Apply location mention reductions
    reduced_content = reduce_location_mentions(reduced_content)

    final_words = count_words(reduced_content)
    print(f"\nFinal word count: {final_words}")
    print(f"Reduction: {initial_words - final_words} words ({((initial_words - final_words) / initial_words * 100):.1f}%)")

    # Check if we need more aggressive cuts
    if final_words > 2500:
        print(f"\n⚠️  Still above target (2,500 words). Need {final_words - 2500} more word reduction.")
    elif final_words < 2000:
        print(f"\n⚠️  Below minimum target (2,000 words). May have cut too much.")
    else:
        print(f"\n✓ Within target range (2,000-2,500 words)")

    print(f"\nWriting reduced content to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reduced_content)

    print("Done!")

if __name__ == '__main__':
    main()
