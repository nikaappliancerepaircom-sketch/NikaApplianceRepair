#!/usr/bin/env python3
"""Count only visible content words in HTML file (excluding markup)"""

import re
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.content = []
        self.skip_tags = {'script', 'style', 'head', 'meta', 'link'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.content.append(text)

    def get_content(self):
        return ' '.join(self.content)

# Read the HTML file
with open(r'C:\NikaApplianceRepair\locations\pickering.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract content
parser = ContentExtractor()
parser.feed(html)
content = parser.get_content()

# Count words
words = content.split()
word_count = len(words)

print(f"Visible Content Word Count: {word_count}")
print(f"Target: 2,200-2,400 words")
print(f"{'✓ WITHIN TARGET' if 2200 <= word_count <= 2400 else '✗ NEEDS MORE REDUCTION' if word_count > 2400 else '✗ TOO SHORT'}")
