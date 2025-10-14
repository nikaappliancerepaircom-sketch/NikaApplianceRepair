#!/usr/bin/env python3
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'head', 'meta', 'link'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)

with open(r'C:\NikaApplianceRepair\locations\milton.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

parser = TextExtractor()
parser.feed(html_content)
text = parser.get_text()

# Clean up text
text = re.sub(r'\s+', ' ', text).strip()

# Count words
words = len(text.split())

print(f"Content word count: {words}")
