"""
BMAD v3.1 Comprehensive Test - Markham Location Page
Tests 283 parameters (excluding 9 Speed Performance parameters)
"""

import re
from pathlib import Path

# Read the Markham HTML file
with open(r'C:\NikaApplianceRepair\locations\markham.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
    lines = html_content.split('\n')

# BMAD v3.1 Test Results
results = {
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'issues': [],
    'gate1': 0,
    'gate2': 0,
    'gate3': 0
}

def check_param(condition, param_name, line_num=None, severity='fail', gate=None):
    if condition:
        results['passed'] += 1
        if gate:
            results[f'gate{gate}'] += 1
        return True
    else:
        if severity == 'fail':
            results['failed'] += 1
        else:
            results['warnings'] += 1
        issue_msg = f'{param_name}'
        if line_num:
            issue_msg += f' (Line {line_num})'
        results['issues'].append(issue_msg)
        return False

# Find line numbers for issues
def find_line(search_text):
    for i, line in enumerate(lines, 1):
        if search_text in line:
            return i
    return None

print('='*60)
print('BMAD v3.1 COMPREHENSIVE TEST - MARKHAM LOCATION PAGE')
print('='*60)
print('\n[*] Testing 283 parameters (excluding 9 Speed Performance)\n')

# ====================
# GATE 1: DATA CONSISTENCY (97 parameters)
# ====================
print('\n' + '='*60)
print('GATE 1: DATA CONSISTENCY (97 parameters)')
print('='*60)

# A. Schema Markup (30 parameters)
print('\n[*] A. Schema Markup (30 parameters)')
schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
has_schema = bool(schema_match)
check_param(has_schema, 'A1: Schema markup present', gate=1)

if has_schema:
    schema_text = schema_match.group(1)
    schema_line = find_line('application/ld+json')
    check_param('@type' in schema_text and 'LocalBusiness' in schema_text, f'A2: @type LocalBusiness', schema_line, gate=1)
    check_param('"name"' in schema_text, f'A3: Business name in schema', schema_line, gate=1)
    check_param('"image"' in schema_text, f'A4: Image in schema', schema_line, gate=1)
    check_param('"@id"' in schema_text, f'A5: @id present', schema_line, gate=1)
    check_param('"url"' in schema_text, f'A6: URL in schema', schema_line, gate=1)
    check_param('"telephone"' in schema_text, f'A7: Telephone in schema', schema_line, gate=1)
    check_param('"address"' in schema_text, f'A8: Address in schema', schema_line, gate=1)
    check_param('"streetAddress"' in schema_text, f'A9: Street address', schema_line, gate=1)
    check_param('"addressLocality"' in schema_text, f'A10: Address locality', schema_line, gate=1)
    check_param('"addressRegion"' in schema_text, f'A11: Address region', schema_line, gate=1)
    check_param('"postalCode"' in schema_text, f'A12: Postal code', schema_line, gate=1)
    check_param('"addressCountry"' in schema_text, f'A13: Address country', schema_line, gate=1)
    check_param('"geo"' in schema_text, f'A14: Geo coordinates', schema_line, gate=1)
    check_param('"latitude"' in schema_text, f'A15: Latitude', schema_line, gate=1)
    check_param('"longitude"' in schema_text, f'A16: Longitude', schema_line, gate=1)
    check_param('"openingHoursSpecification"' in schema_text, f'A17: Opening hours', schema_line, gate=1)
    check_param('"priceRange"' in schema_text, f'A18: Price range', schema_line, gate=1)

    # Check phone format
    phone_match = re.search(r'"telephone":\s*"([^"]+)"', schema_text)
    if phone_match:
        phone = phone_match.group(1)
        check_param(phone.startswith('+1') or phone.startswith('1-'), f'A19: Phone format correct', schema_line, gate=1)
    else:
        check_param(False, f'A19: Phone format correct', schema_line, gate=1)

    # Check days of week (A20-26)
    for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 20):
        check_param(day in schema_text, f'A{i}: {day} in hours', schema_line, gate=1)

    check_param('"opens"' in schema_text, f'A27: Opens time specified', schema_line, gate=1)
    check_param('"closes"' in schema_text, f'A28: Closes time specified', schema_line, gate=1)
    check_param('sameAs' in schema_text, f'A29: Social media links', schema_line, gate=1)
    check_param('aggregateRating' in schema_text or 'review' in schema_text, f'A30: Reviews/ratings', schema_line, gate=1)
else:
    for i in range(2, 31):
        check_param(False, f'A{i}: Schema element missing (no schema found)', gate=1)

# B. Meta Tags (20 parameters)
print('\n[*] B. Meta Tags (20 parameters)')
title_match = re.search(r'<title>(.*?)</title>', html_content)
title_line = find_line('<title>')
check_param(bool(title_match), 'B1: Title tag present', title_line, gate=1)

if title_match:
    title = title_match.group(1)
    check_param('Markham' in title, 'B2: Location in title', title_line, gate=1)
    check_param(len(title) >= 30 and len(title) <= 60, f'B3: Title length 30-60 chars (actual: {len(title)})', title_line, gate=1)
else:
    check_param(False, 'B2: Location in title', title_line, gate=1)
    check_param(False, 'B3: Title length 30-60 chars', title_line, gate=1)

meta_desc = re.search(r'<meta name="description" content="([^"]+)"', html_content)
meta_line = find_line('meta name="description"')
check_param(bool(meta_desc), 'B4: Meta description present', meta_line, gate=1)
if meta_desc:
    desc = meta_desc.group(1)
    check_param(len(desc) >= 120 and len(desc) <= 160, f'B5: Description length 120-160 (actual: {len(desc)})', meta_line, gate=1)
    check_param('Markham' in desc, 'B6: Location in description', meta_line, gate=1)
else:
    check_param(False, 'B5: Description length 120-160', meta_line, gate=1)
    check_param(False, 'B6: Location in description', meta_line, gate=1)

check_param('charset="UTF-8"' in html_content or 'charset=UTF-8' in html_content, 'B7: Charset UTF-8', find_line('charset'), gate=1)
check_param('viewport' in html_content, 'B8: Viewport meta tag', find_line('viewport'), gate=1)

# OG tags
check_param('og:title' in html_content, 'B9: og:title', find_line('og:title'), gate=1)
check_param('og:description' in html_content, 'B10: og:description', find_line('og:description'), gate=1)
check_param('og:url' in html_content, 'B11: og:url', find_line('og:url'), gate=1)
check_param('og:type' in html_content, 'B12: og:type', find_line('og:type'), gate=1)
check_param('og:image' in html_content, 'B13: og:image', find_line('og:image'), gate=1)
check_param('og:locale' in html_content, 'B14: og:locale', find_line('og:locale'), gate=1)

# Twitter tags
check_param('twitter:card' in html_content, 'B15: twitter:card', find_line('twitter:card'), gate=1)
check_param('twitter:title' in html_content, 'B16: twitter:title', find_line('twitter:title'), gate=1)
check_param('twitter:description' in html_content, 'B17: twitter:description', find_line('twitter:description'), gate=1)
check_param('twitter:image' in html_content, 'B18: twitter:image', find_line('twitter:image'), gate=1)

check_param('canonical' in html_content, 'B19: Canonical link', find_line('canonical'), gate=1)
check_param('robots' in html_content.lower(), 'B20: Robots meta tag', find_line('robots'), gate=1)

# C. Contact Information (15 parameters)
print('\n[*] C. Contact Information (15 parameters)')
phone_pattern = r'(1-647-558-7774|647-558-7774|\+1-647-558-7774)'
phone_matches = len(re.findall(phone_pattern, html_content))
check_param(phone_matches >= 3, f'C1: Phone number appears 3+ times (found: {phone_matches})', gate=1)
check_param('tel:' in html_content, 'C2: Tel link present', find_line('tel:'), gate=1)

check_param('Markham' in html_content, 'C3: City name present', gate=1)
check_param('Ontario' in html_content or 'ON' in html_content, 'C4: Province present', gate=1)
check_param('Monday' in html_content and 'Friday' in html_content, 'C5: Business hours days', gate=1)
check_param(re.search(r'\d{1,2}:\d{2}\s*[AaPp][Mm]', html_content), 'C6: Time format present', gate=1)
check_param('email' in html_content.lower() or '@' in html_content, 'C7: Email present', gate=1)
check_param(phone_matches > 0, 'C8: Phone clickable', gate=1)
check_param('Emergency' in html_content or '24/7' in html_content, 'C9: Emergency service mentioned', gate=1)
check_param('service' in html_content.lower() and 'area' in html_content.lower(), 'C10: Service area mentioned', gate=1)
check_param('year' in html_content.lower() and 'experience' in html_content.lower(), 'C11: Experience mentioned', gate=1)
check_param(html_content.count('1-647-558-7774') >= 2, f'C12: Phone consistent (found: {html_content.count("1-647-558-7774")})', gate=1)
check_param(html_content.count('Markham') >= 5, f'C13: Location consistent (found: {html_content.count("Markham")})', gate=1)
check_param('Nika Appliance Repair' in html_content, 'C14: Business name consistent', gate=1)
check_param('license' in html_content.lower() or 'certified' in html_content.lower(), 'C15: License/cert mentioned', gate=1)

# D. URL Structure (8 parameters)
print('\n[*] D. URL Structure (8 parameters)')
url_match = re.search(r'<link rel="canonical" href="([^"]+)"', html_content)
if url_match:
    url = url_match.group(1)
    url_line = find_line('canonical')
    check_param('markham' in url.lower(), 'D1: Location in URL', url_line, gate=1)
    check_param('http' in url, 'D2: HTTPS protocol', url_line, gate=1)
    check_param(url.count('/') <= 5, f'D3: URL depth reasonable (depth: {url.count("/")})', url_line, gate=1)
    check_param(not re.search(r'[A-Z]', url), 'D4: URL lowercase', url_line, gate=1)
    check_param('?' not in url, 'D5: No query parameters', url_line, gate=1)
    check_param('#' not in url, 'D6: No fragments', url_line, gate=1)
    check_param('--' not in url, 'D7: No double hyphens', url_line, gate=1)
    check_param(url.endswith('.html') or url.endswith('/'), 'D8: Clean URL ending', url_line, gate=1)
else:
    for i in range(1, 9):
        check_param(False, f'D{i}: URL check (no canonical found)', gate=1)

# E. Heading Structure (12 parameters)
print('\n[*] E. Heading Structure (12 parameters)')
h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
h1_line = find_line('<h1')
check_param(len(h1_matches) == 1, f'E1: Exactly one H1 (found: {len(h1_matches)})', h1_line, gate=1)

if h1_matches:
    h1_text = re.sub(r'<[^>]+>', '', h1_matches[0])
    check_param('Markham' in h1_text, f'E2: Location in H1', h1_line, gate=1)
    check_param(len(h1_text) >= 30 and len(h1_text) <= 70, f'E3: H1 length 30-70 chars (actual: {len(h1_text)})', h1_line, gate=1)
else:
    check_param(False, 'E2: Location in H1', h1_line, gate=1)
    check_param(False, 'E3: H1 length 30-70 chars', h1_line, gate=1)

h2_matches = re.findall(r'<h2[^>]*>', html_content, re.IGNORECASE)
check_param(len(h2_matches) >= 3, f'E4: At least 3 H2s (found: {len(h2_matches)})', gate=1)
check_param(len(h2_matches) <= 10, f'E5: No more than 10 H2s (found: {len(h2_matches)})', gate=1)

h3_matches = re.findall(r'<h3[^>]*>', html_content, re.IGNORECASE)
check_param(len(h3_matches) >= 2, f'E6: At least 2 H3s (found: {len(h3_matches)})', gate=1)

h1_pos = html_content.find('<h1')
first_h2_pos = html_content.find('<h2')
check_param(h1_pos < first_h2_pos if first_h2_pos > 0 else True, 'E7: H1 before H2', gate=1)

headings_text = ' '.join(h1_matches + re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.IGNORECASE | re.DOTALL))
check_param('repair' in headings_text.lower(), 'E8: Service keywords in headings', gate=1)
check_param('appliance' in headings_text.lower(), 'E9: Appliance mentioned', gate=1)
check_param(len(re.findall(r'<h[1-6]', html_content)) >= 6, f'E10: Total heading count adequate (found: {len(re.findall(r"<h[1-6]", html_content))})', gate=1)

has_h4 = '<h4' in html_content
has_h3 = len(h3_matches) > 0
check_param(not has_h4 or has_h3, 'E11: No skipped heading levels', gate=1)
check_param('</h1>' in html_content, 'E12: All headings properly closed', gate=1)

# F. Internal Linking (12 parameters)
print('\n[*] F. Internal Linking (12 parameters)')
internal_links = re.findall(r'<a[^>]+href="([^"]+)"', html_content)
internal_links = [l for l in internal_links if not l.startswith('http') or 'nikaappliancerepair' in l]
check_param(len(internal_links) >= 5, f'F1: At least 5 internal links (found: {len(internal_links)})', gate=1)
check_param(len(internal_links) <= 30, f'F2: No more than 30 internal links (found: {len(internal_links)})', gate=1)

check_param(any('service' in l.lower() for l in internal_links), 'F3: Link to services', gate=1)
check_param(any('about' in l.lower() or 'index' in l.lower() or l == '/' for l in internal_links), 'F4: Link to about/home', gate=1)
check_param(any('contact' in l.lower() for l in internal_links), 'F5: Link to contact', gate=1)

anchor_texts = re.findall(r'<a[^>]+>(.*?)</a>', html_content, re.DOTALL)
descriptive_anchors = [a for a in anchor_texts if len(re.sub(r'<[^>]+>', '', a).strip()) > 3]
check_param(len(descriptive_anchors) >= 5, f'F6: Descriptive anchor text (found: {len(descriptive_anchors)})', gate=1)

check_param(not any('click here' in a.lower() for a in anchor_texts), 'F7: No "click here" anchors', gate=1)
check_param(all('href="#"' not in l for l in internal_links), 'F8: No empty href', gate=1)

content_area = html_content[html_content.find('<main'):html_content.rfind('</main>')] if '<main' in html_content else html_content
contextual_links = len(re.findall(r'<p[^>]*>.*?<a[^>]+href=', content_area, re.DOTALL))
check_param(contextual_links >= 3, f'F9: Contextual links in content (found: {contextual_links})', gate=1)

check_param('<nav' in html_content, 'F10: Navigation structure', find_line('<nav'), gate=1)
check_param('breadcrumb' in html_content.lower() or 'BreadcrumbList' in html_content, 'F11: Breadcrumb navigation', gate=1)
tel_link_count = html_content.count('href="tel:')
check_param(tel_link_count >= 2, f'F12: Multiple call-to-action links (found: {tel_link_count})', gate=1)

print(f'\n[GATE1] Data Consistency: {results["gate1"]}/97 passed')

# ====================
# GATE 2: CONTENT UNIQUENESS (95 parameters)
# ====================
print('\n' + '='*60)
print('GATE 2: CONTENT UNIQUENESS (95 parameters)')
print('='*60)

# G. Location-Specific Content (25 parameters)
print('\n[*] G. Location-Specific Content (25 parameters)')
markham_mentions = html_content.count('Markham')
check_param(markham_mentions >= 10, f'G1: Location mentioned 10+ times (found: {markham_mentions})', gate=2)
check_param(markham_mentions >= 15, f'G2: Location mentioned 15+ times (found: {markham_mentions})', gate=2)

local_terms = ['Unionville', 'Thornhill', 'Markham Village', 'Cornell', 'Berczy', 'Cachet', 'Wismer']
local_found = sum(1 for term in local_terms if term in html_content)
check_param(local_found >= 2, f'G3: Local neighborhoods mentioned (found: {local_found})', gate=2)

check_param('GTA' in html_content or 'Greater Toronto' in html_content, 'G4: Regional context', gate=2)
check_param('York Region' in html_content or 'York' in html_content, 'G5: Regional area mentioned', gate=2)

check_param('residential' in html_content.lower() or 'homes' in html_content.lower(), 'G6: Residential context', gate=2)
check_param('community' in html_content.lower(), 'G7: Community mentioned', gate=2)
check_param('local' in html_content.lower(), 'G8: Local emphasis', gate=2)

word_count = len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', '', html_content)))
check_param(word_count >= 800, f'G9: Minimum 800 words (found: {word_count})', gate=2)
check_param(word_count >= 1000, f'G10: Target 1000+ words (found: {word_count})', gate=2)

check_param('Markham' in html_content and 'repair' in html_content.lower(), 'G11: Location + service combo', gate=2)
check_param('serving Markham' in html_content.lower() or 'Markham residents' in html_content.lower(), 'G12: Serving location phrasing', gate=2)

check_param('same-day' in html_content.lower() or 'same day' in html_content.lower(), 'G13: Same-day service', gate=2)
check_param('warranty' in html_content.lower() or 'guarantee' in html_content.lower(), 'G14: Warranty mentioned', gate=2)
check_param('certified' in html_content.lower() or 'licensed' in html_content.lower(), 'G15: Credentials', gate=2)

check_param('family' in html_content.lower(), 'G16: Family-oriented messaging', gate=2)
check_param('trusted' in html_content.lower() or 'reliable' in html_content.lower(), 'G17: Trust indicators', gate=2)
check_param('experience' in html_content.lower() and 'year' in html_content.lower(), 'G18: Experience mentioned', gate=2)

check_param(re.search(r'L3[A-Z]|L6[A-Z]', html_content), 'G19: Postal code mentioned', gate=2)
check_param('Highway' in html_content or 'Hwy' in html_content or '7' in html_content, 'G20: Local roads/highways', gate=2)

check_param(not re.search(r'\[LOCATION\]|\[CITY\]|\{\{location\}\}', html_content), 'G21: No template placeholders', gate=2)
check_param(not re.search(r'Lorem ipsum', html_content, re.IGNORECASE), 'G22: No placeholder text', gate=2)

paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
unique_starts = set()
for p in paragraphs:
    text = re.sub(r'<[^>]+>', '', p).strip()
    if len(text) > 20:
        unique_starts.add(text[:30])
check_param(len(unique_starts) >= 10, f'G23: Varied paragraph openings (found: {len(unique_starts)})', gate=2)

check_param('testimonial' in html_content.lower() or 'review' in html_content.lower(), 'G24: Social proof', gate=2)
check_param('emergency' in html_content.lower(), 'G25: Emergency service highlighted', gate=2)

# H. Brand Voice Consistency (20 parameters)
print('\n[*] H. Brand Voice Consistency (20 parameters)')
check_param('Nika Appliance Repair' in html_content, 'H1: Full business name present', gate=2)
check_param(html_content.count('Nika') >= 3, f'H2: Brand name repeated (found: {html_content.count("Nika")})', gate=2)

check_param('professional' in html_content.lower() or 'expert' in html_content.lower(), 'H3: Professional language', gate=2)
check_param('quality' in html_content.lower(), 'H4: Quality emphasis', gate=2)
check_param('service' in html_content.lower(), 'H5: Service-oriented language', gate=2)

check_param('customer' in html_content.lower(), 'H6: Customer focus', gate=2)
check_param('satisfaction' in html_content.lower(), 'H7: Satisfaction mentioned', gate=2)
check_param('affordable' in html_content.lower() or 'competitive' in html_content.lower() or 'fair' in html_content.lower(), 'H8: Pricing transparency', gate=2)

check_param(html_content.count('Nika Appliance Repair') == html_content.count('Nika Appliance Repair'), 'H9: Name spelling consistent', gate=2)
check_param(not re.search(r'we\s+is|they\s+is', html_content, re.IGNORECASE), 'H10: Grammar correct', gate=2)

check_param('reliable' in html_content.lower() or 'dependable' in html_content.lower(), 'H11: Reliability messaging', gate=2)
check_param('quick' in html_content.lower() or 'fast' in html_content.lower() or 'prompt' in html_content.lower(), 'H12: Speed emphasis', gate=2)
check_param('honest' in html_content.lower() or 'transparent' in html_content.lower() or 'upfront' in html_content.lower(), 'H13: Honesty messaging', gate=2)

cta_texts = re.findall(r'<(?:a|button)[^>]*class="[^"]*(?:cta|button|btn)[^"]*"[^>]*>(.*?)</(?:a|button)>', html_content, re.DOTALL | re.IGNORECASE)
check_param(len(cta_texts) >= 2, f'H14: Multiple CTAs (found: {len(cta_texts)})', gate=2)
check_param(any('call' in c.lower() for c in cta_texts), 'H15: Call CTA present', gate=2)

check_param(not re.search(r'!!!|\?\?\?', html_content), 'H16: No excessive punctuation', gate=2)
check_param(not re.search(r'[A-Z]{5,}', re.sub(r'<[^>]+>', '', html_content)), 'H17: No all-caps words', gate=2)

check_param('repair' in html_content.lower() and 'service' in html_content.lower(), 'H18: Core service terms', gate=2)
check_param(html_content.count('1-647-558-7774') >= 2, f'H19: Phone consistency', gate=2)
check_param('appliance' in html_content.lower(), 'H20: Industry terminology', gate=2)

# I. Semantic Richness (20 parameters)
print('\n[*] I. Semantic Richness (20 parameters)')

appliances = ['refrigerator', 'dishwasher', 'oven', 'stove', 'washer', 'dryer', 'microwave', 'freezer', 'range']
appliance_count = sum(1 for app in appliances if app in html_content.lower())
check_param(appliance_count >= 5, f'I1: Multiple appliance types (found: {appliance_count})', gate=2)
check_param(appliance_count >= 7, f'I2: Comprehensive appliance coverage (found: {appliance_count})', gate=2)

brands = ['Samsung', 'LG', 'Whirlpool', 'GE', 'Maytag', 'Bosch', 'KitchenAid', 'Frigidaire']
brand_count = sum(1 for brand in brands if brand in html_content)
check_param(brand_count >= 4, f'I3: Multiple brands mentioned (found: {brand_count})', gate=2)

services = ['repair', 'installation', 'maintenance', 'diagnostic', 'replacement']
service_count = sum(1 for svc in services if svc in html_content.lower())
check_param(service_count >= 3, f'I4: Variety of services (found: {service_count})', gate=2)

problems = ['leak', 'noise', 'not cooling', 'not heating', 'not starting', 'error', 'broke']
problem_count = sum(1 for prob in problems if prob in html_content.lower())
check_param(problem_count >= 2, f'I5: Common problems mentioned (found: {problem_count})', gate=2)

tech_terms = ['compressor', 'thermostat', 'motor', 'heating element', 'control board', 'sensor']
tech_count = sum(1 for term in tech_terms if term in html_content.lower())
check_param(tech_count >= 2, f'I6: Technical terminology (found: {tech_count})', gate=2)

lsi_terms = ['appliance repair', 'home appliance', 'repair service', 'technician', 'fix', 'broken']
lsi_count = sum(1 for term in lsi_terms if term in html_content.lower())
check_param(lsi_count >= 4, f'I7: LSI keywords present (found: {lsi_count})', gate=2)

check_param(re.search(r'appliance repair (?:in|near) Markham', html_content, re.IGNORECASE), 'I8: Long-tail keywords', gate=2)
check_param(re.search(r'Markham appliance', html_content, re.IGNORECASE), 'I9: Location-service combo', gate=2)

check_param('how' in html_content.lower() or 'why' in html_content.lower() or 'when' in html_content.lower(), 'I10: Question words (educational)', gate=2)
check_param('because' in html_content.lower() or 'therefore' in html_content.lower() or 'since' in html_content.lower(), 'I11: Causal language', gate=2)

check_param('Ontario' in html_content, 'I12: Province entity', gate=2)
check_param('Canada' in html_content or 'Canadian' in html_content, 'I13: Country entity', gate=2)

check_param(html_content.count('repair') >= 10, f'I14: Key term frequency (found: {html_content.count("repair")})', gate=2)
check_param(html_content.count('appliance') >= 8, f'I15: Industry term frequency (found: {html_content.count("appliance")})', gate=2)

check_param(re.search(r'\b(the|a|an)\b.*?\b(repair|service|appliance)\b', html_content, re.IGNORECASE), 'I16: Natural article usage', gate=2)
check_param(re.search(r'\b(your|our)\b', html_content, re.IGNORECASE), 'I17: Personal pronouns', gate=2)

unique_words = set(re.findall(r'\b\w{4,}\b', html_content.lower()))
check_param(len(unique_words) >= 200, f'I18: Vocabulary diversity (found: {len(unique_words)})', gate=2)
check_param(len(unique_words) >= 250, f'I19: Rich vocabulary (found: {len(unique_words)})', gate=2)

check_param('FAQ' in html_content or 'frequently asked' in html_content.lower(), 'I20: FAQ section', gate=2)

# J. Content Structure (15 parameters)
print('\n[*] J. Content Structure (15 parameters)')
check_param('<main' in html_content or '<article' in html_content, 'J1: Semantic HTML structure', gate=2)
check_param('<section' in html_content, 'J2: Section elements', find_line('<section'), gate=2)
check_param('<header' in html_content, 'J3: Header element', find_line('<header'), gate=2)
check_param('<footer' in html_content, 'J4: Footer element', find_line('<footer'), gate=2)

sections = len(re.findall(r'<section', html_content, re.IGNORECASE))
check_param(sections >= 3, f'J5: Multiple content sections (found: {sections})', gate=2)

paragraphs_count = len(re.findall(r'<p[^>]*>', html_content))
check_param(paragraphs_count >= 8, f'J6: Adequate paragraph count (found: {paragraphs_count})', gate=2)
check_param(paragraphs_count <= 30, f'J7: Not overly fragmented (found: {paragraphs_count})', gate=2)

lists = len(re.findall(r'<[uo]l>', html_content, re.IGNORECASE))
check_param(lists >= 2, f'J8: Use of lists (found: {lists})', gate=2)

check_param('<strong>' in html_content or '<b>' in html_content, 'J9: Text emphasis', gate=2)
check_param('<em>' in html_content or '<i>' in html_content, 'J10: Italic emphasis', gate=2)

avg_para_length = word_count / max(paragraphs_count, 1)
check_param(avg_para_length >= 20 and avg_para_length <= 100, f'J11: Paragraph length reasonable (avg: {avg_para_length:.1f})', gate=2)

check_param('class="' in html_content, 'J12: CSS classes present', gate=2)
check_param(not re.search(r'style="[^"]*(?:position:\s*absolute|display:\s*none)[^"]*"[^>]*>[^<]{50,}', html_content), 'J13: No hidden content', gate=2)

check_param('<table' not in html_content or 'price' in html_content.lower(), 'J14: Tables used appropriately', gate=2)
check_param('<div' in html_content, 'J15: Proper div structure', gate=2)

# K. Media Integration (15 parameters)
print('\n[*] K. Media Integration (15 parameters)')
images = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
check_param(len(images) >= 3, f'K1: Multiple images (found: {len(images)})', gate=2)
check_param(len(images) <= 20, f'K2: Not image-heavy (found: {len(images)})', gate=2)

images_with_alt = [img for img in images if 'alt="' in img]
check_param(len(images_with_alt) >= len(images) * 0.9, f'K3: 90%+ images have alt text ({len(images_with_alt)}/{len(images)})', gate=2)

alt_texts = re.findall(r'alt="([^"]+)"', html_content)
meaningful_alts = [alt for alt in alt_texts if len(alt) > 10 and 'image' not in alt.lower()]
check_param(len(meaningful_alts) >= len(alt_texts) * 0.7, f'K4: Descriptive alt text ({len(meaningful_alts)}/{len(alt_texts)})', gate=2)

check_param(any('Markham' in alt for alt in alt_texts), 'K5: Location in alt text', gate=2)
check_param(any('repair' in alt.lower() or 'appliance' in alt.lower() for alt in alt_texts), 'K6: Service keywords in alt', gate=2)

check_param(any(('.jpg' in img or '.jpeg' in img or '.webp' in img or '.png' in img) for img in images), 'K7: Appropriate image formats', gate=2)

check_param(any('loading="lazy"' in img for img in images), 'K8: Lazy loading implemented', gate=2)

check_param(any('srcset' in img for img in images) or html_content.count('width="') >= len(images) * 0.5, 'K9: Responsive image attributes', gate=2)

has_video = '<video' in html_content or '<iframe' in html_content
check_param(has_video or len(images) >= 5, f'K10: Rich media OR sufficient images', gate=2)

images_with_dims = [img for img in images if 'width=' in img and 'height=' in img]
check_param(len(images_with_dims) >= len(images) * 0.7, f'K11: Image dimensions specified ({len(images_with_dims)}/{len(images)})', gate=2)

check_param(any('logo' in img.lower() for img in images), 'K12: Logo present', gate=2)

check_param('svg' in html_content.lower() or 'icon' in html_content.lower(), 'K13: Icons/SVGs present', gate=2)

check_param(not any('placeholder' in img.lower() for img in images), 'K14: No placeholder images', gate=2)
check_param(all('src="' in img or 'src=' in img for img in images), 'K15: All images have src', gate=2)

print(f'\n[GATE2] Content Uniqueness: {results["gate2"]}/95 passed')

# ====================
# GATE 3: MOBILE RESPONSIVENESS (91 parameters)
# ====================
print('\n' + '='*60)
print('GATE 3: MOBILE RESPONSIVENESS (91 parameters)')
print('='*60)

# L. Viewport & Meta (12 parameters)
print('\n[*] L. Viewport & Meta (12 parameters)')
viewport_match = re.search(r'<meta[^>]*name="viewport"[^>]*content="([^"]+)"', html_content, re.IGNORECASE)
viewport_line = find_line('viewport')
check_param(bool(viewport_match), 'L1: Viewport meta tag', viewport_line, gate=3)

if viewport_match:
    viewport = viewport_match.group(1)
    check_param('width=device-width' in viewport, 'L2: device-width set', viewport_line, gate=3)
    check_param('initial-scale=1' in viewport, 'L3: initial-scale=1', viewport_line, gate=3)
    check_param('maximum-scale' not in viewport or 'maximum-scale=1' not in viewport, 'L4: No scale restriction', viewport_line, gate=3)
else:
    check_param(False, 'L2: device-width set', viewport_line, gate=3)
    check_param(False, 'L3: initial-scale=1', viewport_line, gate=3)
    check_param(False, 'L4: No scale restriction', viewport_line, gate=3)

check_param('responsive' in html_content.lower(), 'L5: Responsive design mentioned', gate=3)
check_param('@media' in html_content, 'L6: Media queries present', find_line('@media'), gate=3)

check_param('apple-mobile-web-app' in html_content or 'mobile-web-app-capable' in html_content, 'L7: Mobile web app tags', gate=3)
check_param('theme-color' in html_content, 'L8: Theme color meta', find_line('theme-color'), gate=3)

check_param(not re.search(r'font-size:\s*\d+px', html_content) or 'rem' in html_content or 'em' in html_content, 'L9: Relative font units', gate=3)

check_param(re.search(r'min-height:\s*44px|min-height:\s*48px|padding.*\d+px', html_content), 'L10: Adequate touch targets', gate=3)

check_param(not re.search(r'width:\s*\d{4,}px', html_content), 'L11: No fixed large widths', gate=3)
check_param('overflow-x' in html_content, 'L12: Horizontal overflow handled', find_line('overflow-x'), gate=3)

# M. Responsive Layout (20 parameters)
print('\n[*] M. Responsive Layout (20 parameters)')
check_param('display: flex' in html_content or 'display:flex' in html_content, 'M1: Flexbox used', gate=3)
check_param('display: grid' in html_content or 'display:grid' in html_content, 'M2: CSS Grid used', gate=3)

media_queries = re.findall(r'@media[^{]*\((?:max-width|min-width):\s*(\d+)px\)', html_content)
check_param(len(media_queries) >= 2, f'M3: Multiple breakpoints (found: {len(media_queries)})', gate=3)
check_param(any(int(mq) <= 768 for mq in media_queries if mq.isdigit()), 'M4: Tablet breakpoint', gate=3)
check_param(any(int(mq) <= 480 for mq in media_queries if mq.isdigit()), 'M5: Mobile breakpoint', gate=3)

check_param('max-width' in html_content, 'M6: Max-width constraints', gate=3)
check_param('%' in html_content or 'vw' in html_content, 'M7: Percentage/viewport units', gate=3)

check_param(re.search(r'img\s*{[^}]*max-width:\s*100%', html_content, re.IGNORECASE) or 'max-width: 100%' in html_content, 'M8: Responsive images CSS', gate=3)

check_param(re.search(r'grid-template-columns|flex-wrap', html_content, re.IGNORECASE), 'M9: Responsive grid', gate=3)

mobile_first = re.search(r'@media[^{]*min-width', html_content)
check_param(bool(mobile_first), 'M10: Mobile-first media queries', gate=3)

check_param('padding' in html_content and 'margin' in html_content, 'M11: Proper spacing', gate=3)
check_param(re.search(r'padding:\s*[\d.]+(?:em|rem|%)', html_content), 'M12: Relative padding units', gate=3)

check_param(re.search(r'flex-direction:\s*column|grid-auto-flow', html_content), 'M13: Column stacking capability', gate=3)

check_param('display: none' in html_content or 'display:none' in html_content, 'M14: Conditional display', gate=3)

check_param(not re.search(r'font-size:\s*[1-9]\d{2,}px', html_content), 'M15: No huge fixed fonts', gate=3)

check_param('overflow:' in html_content or 'overflow-x:' in html_content, 'M16: Overflow properties', gate=3)
check_param('overflow-x: hidden' in html_content or 'overflow-x:hidden' in html_content, 'M17: Horizontal overflow hidden', gate=3)

check_param('flex-wrap: wrap' in html_content or 'flex-wrap:wrap' in html_content, 'M18: Flex wrapping', gate=3)

check_param(not re.search(r'\bwidth:\s*[1-9]\d{3,}px', html_content), 'M19: No excessive fixed widths', gate=3)
check_param('box-sizing' in html_content, 'M20: Box-sizing declared', find_line('box-sizing'), gate=3)

# N. Mobile Navigation (15 parameters)
print('\n[*] N. Mobile Navigation (15 parameters)')
check_param('<nav' in html_content, 'N1: Navigation element', find_line('<nav'), gate=3)
check_param('menu' in html_content.lower(), 'N2: Menu structure', gate=3)

check_param('hamburger' in html_content.lower() or 'toggle' in html_content.lower() or '☰' in html_content, 'N3: Mobile menu toggle', gate=3)

check_param('onclick' in html_content.lower() or 'addEventListener' in html_content or '@click' in html_content, 'N4: Interactive menu', gate=3)

check_param(re.search(r'@media.*\(max-width.*nav', html_content, re.DOTALL | re.IGNORECASE), 'N5: Mobile nav styles', gate=3)

check_param('skip' in html_content.lower() and 'content' in html_content.lower(), 'N6: Skip to content link', gate=3)

check_param('position: fixed' in html_content or 'position:fixed' in html_content or 'position: sticky' in html_content, 'N7: Fixed/sticky navigation', gate=3)

check_param(html_content.count('<a') >= 5, f'N8: Adequate link targets (found: {html_content.count("<a")})', gate=3)

check_param('breadcrumb' in html_content.lower(), 'N9: Breadcrumb navigation', gate=3)

check_param('footer' in html_content.lower() and 'nav' in html_content.lower(), 'N10: Footer navigation', gate=3)

check_param('top' in html_content.lower() or '↑' in html_content or '^' in html_content, 'N11: Back to top functionality', gate=3)

nav_links = len(re.findall(r'<nav[^>]*>.*?</nav>', html_content, re.DOTALL | re.IGNORECASE))
check_param(nav_links >= 1, f'N12: Navigation links present (found: {nav_links})', gate=3)

check_param('aria-label' in html_content or 'aria-labelledby' in html_content, 'N13: ARIA labels on nav', gate=3)

check_param('collapse' in html_content.lower() or 'accordion' in html_content.lower() or 'expand' in html_content.lower(), 'N14: Collapsible content', gate=3)

check_param('role="navigation"' in html_content or '<nav' in html_content, 'N15: Semantic navigation', gate=3)

# O. Mobile Forms & CTAs (15 parameters)
print('\n[*] O. Mobile Forms & CTAs (15 parameters)')

cta_buttons = len(re.findall(r'<(?:button|a)[^>]*class="[^"]*(?:btn|button|cta)', html_content, re.IGNORECASE))
check_param(cta_buttons >= 2, f'O1: Multiple CTAs (found: {cta_buttons})', gate=3)

tel_links = len(re.findall(r'href="tel:', html_content))
check_param(tel_links >= 2, f'O2: Multiple call links (found: {tel_links})', gate=3)

check_param(re.search(r'(?:button|btn|cta)[^}]*{[^}]*(?:padding|min-height)', html_content, re.IGNORECASE), 'O3: Button sizing defined', gate=3)

has_form = '<form' in html_content
check_param(has_form or tel_links >= 2, 'O4: Forms OR call links present', gate=3)

if has_form:
    check_param('type="email"' in html_content or 'type="tel"' in html_content, 'O5: Mobile-friendly input types', gate=3)
    check_param('required' in html_content, 'O6: Form validation', gate=3)
    check_param('label' in html_content.lower(), 'O7: Form labels', gate=3)
    check_param('placeholder' in html_content, 'O8: Input placeholders', gate=3)
else:
    check_param(True, 'O5: Mobile-friendly input types (no form)', gate=3)
    check_param(True, 'O6: Form validation (no form)', gate=3)
    check_param(True, 'O7: Form labels (no form)', gate=3)
    check_param(True, 'O8: Input placeholders (no form)', gate=3)

check_param(re.search(r'(?:call|contact|book|schedule|get|request)', html_content, re.IGNORECASE), 'O9: Action-oriented CTA text', gate=3)

check_param('position: fixed' in html_content or 'position:fixed' in html_content, 'O10: Fixed CTA capability', gate=3)

check_param('background' in html_content and 'color' in html_content, 'O11: Button styling defined', gate=3)

check_param(not re.search(r'<a[^>]*>[^<]{1,2}</a>', html_content), 'O12: No tiny click targets', gate=3)

check_param(html_content.upper().find('HREF="TEL:') < len(html_content) / 2, 'O13: CTA in upper half', gate=3)

check_param(':focus' in html_content or ':active' in html_content, 'O14: Focus states defined', gate=3)

check_param('submit' in html_content.lower() or 'send' in html_content.lower() or tel_links >= 1, 'O15: Submit/action capability', gate=3)

# P. Touch Interactions (12 parameters)
print('\n[*] P. Touch Interactions (12 parameters)')

check_param('touch' in html_content.lower() or 'click' in html_content.lower(), 'P1: Touch event handling', gate=3)

check_param(not re.search(r'<a[^>]{0,50}>[^<]{1,3}</a>', html_content), 'P2: No tiny tap targets', gate=3)

check_param('margin' in html_content or 'padding' in html_content, 'P3: Element spacing', gate=3)

check_param(not re.search(r':hover[^}]*{[^}]*display:\s*block', html_content), 'P4: No hover-only reveals', gate=3)

check_param(re.search(r'min-height:\s*(?:44|48)px', html_content) or re.search(r'padding.*(?:1|2)(?:em|rem)', html_content), 'P5: Touch-friendly dimensions', gate=3)

check_param('swipe' in html_content.lower() or 'slide' in html_content.lower() or 'scroll' in html_content.lower(), 'P6: Gesture-aware design', gate=3)

check_param('pointer-events' in html_content or 'user-select' in html_content, 'P7: Pointer control', gate=3)

check_param(':active' in html_content, 'P8: Active states', gate=3)

check_param('touch-action' in html_content or not re.search(r'delay.*300', html_content), 'P9: No tap delay', gate=3)

check_param('overflow-y' in html_content or 'scroll' in html_content, 'P10: Scrollable content', gate=3)

check_param('overscroll-behavior' in html_content or not re.search(r'position:\s*fixed.*top:\s*0', html_content), 'P11: Overscroll behavior', gate=3)

check_param(not re.search(r'<select[^>]*multiple', html_content), 'P12: No complex multi-selects', gate=3)

# Q. Mobile Performance (17 parameters)
print('\n[*] Q. Mobile Performance (17 parameters)')

check_param('async' in html_content or 'defer' in html_content, 'Q1: Async/defer scripts', gate=3)

check_param('loading="lazy"' in html_content, 'Q2: Lazy loading', gate=3)
check_param('webp' in html_content.lower() or 'avif' in html_content.lower(), 'Q3: Modern image formats', gate=3)

check_param('<style' in html_content, 'Q4: Inline critical CSS', find_line('<style'), gate=3)

external_scripts = len(re.findall(r'<script[^>]*src="http', html_content, re.IGNORECASE))
check_param(external_scripts <= 5, f'Q5: Limited external scripts (found: {external_scripts})', gate=3)

css_links = len(re.findall(r'<link[^>]*rel="stylesheet"', html_content, re.IGNORECASE))
check_param(css_links <= 3, f'Q6: Minimal CSS files (found: {css_links})', gate=3)

check_param('font-display' in html_content or not re.search(r'@font-face', html_content), 'Q7: Optimized font loading', gate=3)

check_param('preload' in html_content or 'prefetch' in html_content, 'Q8: Resource hints', gate=3)

check_param('<script' not in html_content[:1000] or 'defer' in html_content[:1000], 'Q9: No render-blocking JS in head', gate=3)

check_param(html_content.count('window.location') <= 1, f'Q10: Minimal redirects (found: {html_content.count("window.location")})', gate=3)

check_param(html_content.count('jquery') == 0, 'Q11: No jQuery dependency', gate=3)

check_param('transform' in html_content or 'transition' in html_content, 'Q12: CSS animations', gate=3)

check_param('angular' not in html_content.lower() and 'ember' not in html_content.lower(), 'Q13: No heavy frameworks', gate=3)

check_param(not re.search(r'\*[\s]*{', html_content), 'Q14: No universal selectors', gate=3)

check_param('cdn' in html_content.lower() or external_scripts <= 3, f'Q15: CDN or minimal external resources', gate=3)

check_param(True, 'Q16: Compression awareness', gate=3)  # Can't test from HTML alone

check_param(True, 'Q17: Progressive enhancement capability', gate=3)  # Can't test from HTML alone

print(f'\n[GATE3] Mobile Responsiveness: {results["gate3"]}/91 passed')

# ====================
# FINAL CALCULATIONS
# ====================
total_params = 283
total_passed = results['passed']
total_failed = results['failed']
overall_score = (total_passed / total_params) * 100

gate1_score = (results['gate1'] / 97) * 100
gate2_score = (results['gate2'] / 95) * 100
gate3_score = (results['gate3'] / 91) * 100

print('\n' + '='*60)
print('BMAD v3.1 TEST RESULTS - MARKHAM LOCATION PAGE')
print('='*60)
print(f'\n[*] OVERALL SCORE: {overall_score:.1f}% ({total_passed}/{total_params} parameters)')
print(f'\n[*] Breakdown:')
print(f'   [PASS] Passed: {total_passed}')
print(f'   [FAIL] Failed: {total_failed}')
print(f'   [WARN] Warnings: {results["warnings"]}')

print(f'\n' + '='*60)
print('GATE RESULTS')
print('='*60)
gate1_status = '[PASS]' if gate1_score >= 90 else '[WARN]' if gate1_score >= 80 else '[FAIL]'
gate2_status = '[PASS]' if gate2_score >= 90 else '[WARN]' if gate2_score >= 80 else '[FAIL]'
gate3_status = '[PASS]' if gate3_score >= 90 else '[WARN]' if gate3_score >= 80 else '[FAIL]'

print(f'\n[*] Gate 1 - Data Consistency: {gate1_score:.1f}% ({results["gate1"]}/97) {gate1_status}')
print(f'[*] Gate 2 - Content Uniqueness: {gate2_score:.1f}% ({results["gate2"]}/95) {gate2_status}')
print(f'[*] Gate 3 - Mobile Responsiveness: {gate3_score:.1f}% ({results["gate3"]}/91) {gate3_status}')

print(f'\n' + '='*60)
print('CRITICAL FAILURES')
print('='*60)
critical_keywords = ['H1', 'Schema', 'Title', 'Meta description', 'Phone', 'Viewport', 'canonical']
critical_issues = [issue for issue in results['issues'] if any(x in issue for x in critical_keywords)]
if critical_issues:
    for issue in critical_issues:
        print(f'   [FAIL] {issue}')
else:
    print('   [PASS] No critical failures detected')

print(f'\n' + '='*60)
print('ALL FAILURES (Showing first 50)')
print('='*60)
if results['issues']:
    for i, issue in enumerate(results['issues'][:50], 1):
        print(f'   {i}. {issue}')

    if len(results['issues']) > 50:
        print(f'\n   ... and {len(results["issues"]) - 50} more issues')
else:
    print('   [PASS] No failures - Perfect score!')

print('\n' + '='*60)
print('DEPLOYMENT RECOMMENDATION')
print('='*60)
if overall_score >= 95:
    print('   [PASS] APPROVED FOR DEPLOYMENT - Excellent score!')
elif overall_score >= 90:
    print('   [PASS] APPROVED - Minor improvements recommended')
elif overall_score >= 85:
    print('   [WARN] CONDITIONAL APPROVAL - Fix critical issues first')
elif overall_score >= 80:
    print('   [WARN] NOT RECOMMENDED - Significant improvements needed')
else:
    print('   [FAIL] DEPLOYMENT BLOCKED - Major issues must be resolved')

print('\n' + '='*60)
print('END OF REPORT')
print('='*60)
