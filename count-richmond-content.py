from bs4 import BeautifulSoup
import re

# Read the HTML file
with open(r'C:\NikaApplianceRepair\locations\richmond-hill.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Remove scripts and styles
for script in soup(["script", "style", "head"]):
    script.decompose()

# Get text content
text = soup.get_text()

# Count words
words = re.findall(r'\b\w+\b', text)
total_words = len(words)

# Count Richmond Hill mentions in body content
body_text = soup.body.get_text() if soup.body else text
rh_mentions = len(re.findall(r'Richmond Hill', body_text))

print(f"Total content words: {total_words}")
print(f"Richmond Hill mentions in body: {rh_mentions}")

# Count words in specific sections
sections = {
    'FAQ Section': soup.find('section', class_='faq-section'),
    'Common Problems': soup.find('section', class_='common-problems-premium'),
    'Services': soup.find('section', class_='services-section'),
    'Why Choose Us': soup.find('section', class_='why-choose-section'),
}

print("\n--- Section Word Counts ---")
for name, section in sections.items():
    if section:
        section_text = section.get_text()
        section_words = len(re.findall(r'\b\w+\b', section_text))
        section_rh = len(re.findall(r'Richmond Hill', section_text))
        print(f"{name}: {section_words} words, {section_rh} RH mentions")
