#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMAD Test - All Location Pages
Tests all 22 location pages and generates summary report
"""

import re
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# List of all location pages
locations = [
    "ajax", "aurora", "brampton", "burlington", "caledon",
    "east-gwillimbury", "etobicoke", "halton-hills", "markham", "milton",
    "mississauga", "newmarket", "north-york", "oakville", "oshawa",
    "pickering", "richmond-hill", "scarborough", "stouffville", "toronto",
    "vaughan", "whitby"
]

def test_location(location_name):
    """Test a single location page and return tier scores"""
    html_file = f"locations/{location_name}.html"

    if not os.path.exists(html_file):
        return None

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Count visible words
    text_only = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text_only = re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=re.DOTALL | re.IGNORECASE)
    text_only = re.sub(r'<[^>]+>', ' ', text_only)
    text_only = re.sub(r'\s+', ' ', text_only)
    words = text_only.split()
    word_count = len(words)

    # TIER 1: DATA CONSISTENCY
    tier1_score = 100
    phone_count = html.count('437-747-6737')
    if phone_count < 8:
        tier1_score -= 25
    review_patterns = ['5,200+', '5200', '5,200']
    review_found = any(pattern in html for pattern in review_patterns)
    if not review_found:
        tier1_score -= 25
    rating_count = html.count('4.9')
    if rating_count < 3:
        tier1_score -= 25
    warranty_count = html.count('90-day')
    if warranty_count < 3:
        tier1_score -= 25

    # TIER 2: SEO FOUNDATIONS
    tier2_score = 100
    title_match = re.search(r'<title>(.*?)</title>', html)
    if title_match:
        title_len = len(title_match.group(1))
        if not (50 <= title_len <= 60):
            tier2_score -= 10
    else:
        tier2_score -= 15

    meta_match = re.search(r'<meta name="description" content="([^"]*)"', html)
    if meta_match:
        meta_len = len(meta_match.group(1))
        if not (150 <= meta_len <= 160):
            tier2_score -= 10
    else:
        tier2_score -= 15

    h1_count = len(re.findall(r'<h1[^>]*>.*?</h1>', html, re.DOTALL))
    if h1_count != 1:
        tier2_score -= 15

    h2_count = len(re.findall(r'<h2[^>]*>.*?</h2>', html, re.DOTALL))
    if not (5 <= h2_count <= 10):
        tier2_score -= 10

    if '<link rel="canonical"' not in html:
        tier2_score -= 10

    if '"@type": "LocalBusiness"' not in html and '"@type": "Organization"' not in html:
        tier2_score -= 10

    # TIER 3: AI SEARCH
    tier3_score = 100
    faq_count = html.count('"@type": "Question"')
    if faq_count < 6:
        tier3_score -= 25

    h3_count = len(re.findall(r'<h3[^>]*>.*?</h3>', html, re.DOTALL))
    if not (12 <= h3_count <= 20):
        tier3_score -= 25

    # TIER 4: CONTENT QUALITY
    tier4_score = 100
    if 2000 <= word_count <= 2500:
        pass
    elif 1800 <= word_count < 2000:
        tier4_score -= 5
    elif 2500 < word_count <= 2700:
        tier4_score -= 5
    else:
        tier4_score -= 15

    internal_link_count = html.count('href="/') + html.count('href="./') + html.count('href="../')
    if internal_link_count < 10:
        tier4_score -= 10

    # TIER 5: CONVERSION/CRO
    tier5_score = 100
    cta_patterns = ['call now', 'book now', 'schedule', 'contact', 'call 437-747-6737']
    cta_count = sum(html.lower().count(pattern) for pattern in cta_patterns)
    if cta_count < 5:
        tier5_score -= 15

    urgency_patterns = ['same-day', 'same day', 'today', 'now', 'emergency', '24/7']
    urgency_count = sum(html.lower().count(pattern) for pattern in urgency_patterns)
    if urgency_count < 3:
        tier5_score -= 10

    # TIER 6: PSYCHOLOGY
    tier6_score = 100
    if '5,200+' not in html and '5200' not in html:
        tier6_score -= 10

    trust_patterns = ['licensed', 'insured', 'certified', 'warranty', 'guarantee']
    trust_count = sum(html.lower().count(pattern) for pattern in trust_patterns)
    if trust_count < 5:
        tier6_score -= 10

    # TIER 7: DESIGN & UX
    tier7_score = 100
    if 'name="viewport"' not in html:
        tier7_score -= 15

    img_tags = len(re.findall(r'<img[^>]+>', html))
    img_with_alt = len(re.findall(r'<img[^>]+alt="[^"]*"[^>]*>', html))
    if img_tags > 0:
        alt_ratio = (img_with_alt / img_tags) * 100
        if alt_ratio < 90:
            tier7_score -= 10

    # TIER 8: PERFORMANCE
    tier8_score = 100
    lazy_count = html.count('loading="lazy"')
    if lazy_count < 3:
        tier8_score -= 10

    webp_count = html.count('.webp')
    if webp_count < 3:
        tier8_score -= 10

    # Calculate overall score and status
    tiers = {
        'tier1': {'score': tier1_score, 'required': 100, 'critical': True},
        'tier2': {'score': tier2_score, 'required': 98, 'critical': True},
        'tier3': {'score': tier3_score, 'required': 98, 'critical': True},
        'tier4': {'score': tier4_score, 'required': 98, 'critical': True},
        'tier5': {'score': tier5_score, 'required': 85, 'critical': False},
        'tier6': {'score': tier6_score, 'required': 98, 'critical': True},
        'tier7': {'score': tier7_score, 'required': 85, 'critical': False},
        'tier8': {'score': tier8_score, 'required': 70, 'critical': False}
    }

    total_score = sum(t['score'] for t in tiers.values()) / len(tiers)

    passed = sum(1 for t in tiers.values() if t['score'] >= t['required'])
    failed = len(tiers) - passed
    critical_failed = sum(1 for t in tiers.values() if t['critical'] and t['score'] < t['required'])

    status = "✅ PASS" if critical_failed == 0 and total_score >= 90 else "❌ FAIL"

    return {
        'location': location_name,
        'total_score': total_score,
        'passed': passed,
        'failed': failed,
        'critical_failed': critical_failed,
        'status': status,
        'tier1': tier1_score,
        'tier2': tier2_score,
        'tier3': tier3_score,
        'tier4': tier4_score,
        'tier5': tier5_score,
        'tier6': tier6_score,
        'tier7': tier7_score,
        'tier8': tier8_score,
        'word_count': word_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'faq_count': faq_count,
        'internal_links': internal_link_count,
        'title_len': title_len if title_match else 0,
        'meta_len': meta_len if meta_match else 0
    }

# Main execution
print("=" * 100)
print("🎯 BMAD TEST - ALL LOCATION PAGES")
print("=" * 100)
print()

results = []
for location in locations:
    print(f"Testing {location}...", end=" ")
    result = test_location(location)
    if result:
        results.append(result)
        print(f"{result['status']} ({result['total_score']:.1f}/100)")
    else:
        print("❌ File not found")

print()
print("=" * 100)
print("📊 SUMMARY TABLE")
print("=" * 100)
print()

# Header
print(f"{'Location':<20} {'Score':>7} {'Status':>8} {'T1':>4} {'T2':>4} {'T3':>4} {'T4':>4} {'T5':>4} {'T6':>4} {'T7':>4} {'T8':>4} {'Pass':>5}")
print("-" * 100)

# Sort by score (lowest first to show problems first)
results.sort(key=lambda x: x['total_score'])

for r in results:
    status_icon = "✅" if r['status'] == "✅ PASS" else "❌"
    print(f"{r['location']:<20} {r['total_score']:>6.1f}% {status_icon:>7} "
          f"{r['tier1']:>4} {r['tier2']:>4} {r['tier3']:>4} {r['tier4']:>4} "
          f"{r['tier5']:>4} {r['tier6']:>4} {r['tier7']:>4} {r['tier8']:>4} "
          f"{r['passed']:>2}/{len([r['tier1'], r['tier2'], r['tier3'], r['tier4'], r['tier5'], r['tier6'], r['tier7'], r['tier8']])}")

print()
print("=" * 100)
print("📈 STATISTICS")
print("=" * 100)

passing = sum(1 for r in results if r['status'] == "✅ PASS")
failing = len(results) - passing
avg_score = sum(r['total_score'] for r in results) / len(results)

print(f"✅ Passing: {passing}/{len(results)} locations ({passing/len(results)*100:.1f}%)")
print(f"❌ Failing: {failing}/{len(results)} locations ({failing/len(results)*100:.1f}%)")
print(f"📊 Average Score: {avg_score:.1f}/100")
print()

if failing > 0:
    print("=" * 100)
    print("🔍 DETAILED ISSUES (Failing Locations Only)")
    print("=" * 100)
    print()

    for r in results:
        if r['status'] == "❌ FAIL":
            print(f"📍 {r['location'].upper()} - {r['total_score']:.1f}/100")
            print("-" * 50)

            issues = []
            if r['tier2'] < 98:
                if r['title_len'] < 50 or r['title_len'] > 60:
                    issues.append(f"  • Title: {r['title_len']} chars (need 50-60)")
                if r['meta_len'] < 150 or r['meta_len'] > 160:
                    issues.append(f"  • Meta: {r['meta_len']} chars (need 150-160)")
                if r['h2_count'] < 5 or r['h2_count'] > 10:
                    issues.append(f"  • H2 tags: {r['h2_count']} (need 5-10)")

            if r['tier3'] < 98:
                if r['faq_count'] < 6:
                    issues.append(f"  • FAQ questions: {r['faq_count']} (need 6+)")
                if r['h3_count'] < 12 or r['h3_count'] > 20:
                    issues.append(f"  • H3 tags: {r['h3_count']} (need 12-20)")

            if r['tier4'] < 98:
                if r['word_count'] < 2000 or r['word_count'] > 2500:
                    issues.append(f"  • Word count: {r['word_count']} (need 2000-2500)")
                if r['internal_links'] < 10:
                    issues.append(f"  • Internal links: {r['internal_links']} (need 10+)")

            for issue in issues:
                print(issue)
            print()

print("=" * 100)
