#!/usr/bin/env python3
"""
Final Keyword Density Reducer
Aggressively reduce keyword density from 4.64% to target 2-3%
"""

from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re

def reduce_keywords_in_text(text):
    """Replace repetitive keywords with synonyms and variations"""

    replacements = [
        # Appliance variations
        (r'\bappliance repair\b', 'appliance service', 0.5),
        (r'\bappliance repair\b', 'appliance fix', 0.3),
        (r'\bappliance repair\b', 'repair work', 0.2),
        (r'\brepair service\b', 'service', 0.4),
        (r'\brepair services\b', 'services', 0.4),
        (r'\brepair technician\b', 'technician', 0.3),
        (r'\brepair expert\b', 'expert', 0.3),

        # Location variations
        (r'\bin Toronto\b', 'in the GTA', 0.4),
        (r'\bToronto area\b', 'Greater Toronto Area', 0.5),
        (r'\bToronto\b', 'the area', 0.2),

        # Generic reductions
        (r'\bour repair\b', 'our', 0.3),
        (r'\brepair issues\b', 'issues', 0.3),
        (r'\bfor repair\b', 'for service', 0.4),
    ]

    modified_text = text

    for pattern, replacement, probability in replacements:
        # Find all matches
        matches = list(re.finditer(pattern, modified_text, re.IGNORECASE))

        # Replace based on probability (skip some occurrences)
        for i, match in enumerate(matches):
            if i % int(1/probability) == 0:  # Replace every Nth occurrence
                start, end = match.span()
                # Preserve original case
                original = modified_text[start:end]
                if original[0].isupper():
                    replacement_text = replacement.capitalize()
                else:
                    replacement_text = replacement

                modified_text = modified_text[:start] + replacement_text + modified_text[end:]

    return modified_text

def process_element_text(element):
    """Process text content of an element recursively"""

    # Skip script and style tags
    if element.name in ['script', 'style', 'code']:
        return False

    changed = False

    # Process direct text nodes
    for child in element.children:
        if isinstance(child, NavigableString):
            original = str(child)
            if len(original.strip()) > 10:  # Only process substantial text
                new_text = reduce_keywords_in_text(original)
                if new_text != original:
                    child.replace_with(new_text)
                    changed = True
        elif hasattr(child, 'children'):
            if process_element_text(child):
                changed = True

    return changed

def reduce_page_keywords(file_path):
    """Reduce keyword density on a page"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Process main content areas
    sections_to_process = [
        soup.find('section', class_='services-section'),
        soup.find('section', class_='why-choose-section'),
        soup.find('section', class_='about-section'),
        soup.find('div', class_='voice-search-content'),
        soup.find('div', class_='local-service-info'),
    ]

    changed = False
    for section in sections_to_process:
        if section and process_element_text(section):
            changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True

    return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FINAL KEYWORD DENSITY REDUCTION")
    print("=" * 70)
    print("\nReducing keyword density from 4.64% to target 2-3%")
    print("Replacing repetitive keywords with natural synonyms")
    print("=" * 70)

    services_dir = base_dir / 'services'
    all_files = list(services_dir.glob('*.html'))

    print(f"\nProcessing {len(all_files)} service pages...\n")

    reduced = 0
    for file_path in all_files:
        if reduce_page_keywords(file_path):
            print(f"[REDUCED] {file_path.name}")
            reduced += 1

    print("\n" + "=" * 70)
    print(f"REDUCED: {reduced}/{len(all_files)} pages")
    print("=" * 70)
    print("\nKeyword density optimized to natural levels!")

if __name__ == '__main__':
    main()
