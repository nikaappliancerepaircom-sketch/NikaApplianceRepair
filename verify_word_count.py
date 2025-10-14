#!/usr/bin/env python3
"""Verify actual content word count in Vaughan page"""

import re
from bs4 import BeautifulSoup

def count_content_words(html_file):
    """Count words in visible content only"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style', 'head']):
        script.decompose()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading/trailing space
    lines = (line.strip() for line in text.splitlines())

    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # Remove blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)

    # Count words
    words = text.split()
    return len(words)

def count_location_mentions(html_file):
    """Count Vaughan mentions"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(re.findall(r'\bVaughan\b', content, re.IGNORECASE))

if __name__ == '__main__':
    file_path = r'C:\NikaApplianceRepair\locations\vaughan.html'

    word_count = count_content_words(file_path)
    vaughan_count = count_location_mentions(file_path)

    print("=" * 60)
    print("VAUGHAN PAGE VERIFICATION")
    print("=" * 60)
    print(f"\nContent word count: {word_count:,}")
    print(f"Vaughan mentions: {vaughan_count}")
    print(f"\nTarget range: 2,000-2,500 words")

    if 2000 <= word_count <= 2500:
        print(f"\nSTATUS: SUCCESS - Within target range")
    elif word_count < 2000:
        print(f"\nSTATUS: {2000 - word_count} words below target")
    else:
        print(f"\nSTATUS: {word_count - 2500} words above target")

    if 30 <= vaughan_count <= 35:
        print(f"Vaughan mentions: OPTIMAL (30-35 range)")
    elif vaughan_count < 30:
        print(f"Vaughan mentions: LOW (add {30 - vaughan_count} more)")
    else:
        print(f"Vaughan mentions: HIGH (reduce by {vaughan_count - 35})")

    print("=" * 60)
