#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick BMAD Full Test - All Tiers Without Stopping
Richmond Hill Location Page
"""

import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

html_file = "locations/richmond-hill.html"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Strip tags for text analysis
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text_clean = ' '.join(text.split())

print("="*70)
print("BMAD FULL TEST - RICHMOND HILL")
print("All 8 Tiers - Complete Report")
print("="*70)

# TIER 1: DATA CONSISTENCY
print("\n📊 TIER 1: DATA CONSISTENCY (15 params)")
print("-"*70)
tier1_score = 100
tier1_issues = []

# Phone
if html.count('437-747-6737') >= 8 or html.count('4377476737') >= 8:
    print("✅ Phone: 437-747-6737 (8+ mentions)")
else:
    tier1_score -= 20
    tier1_issues.append("❌ Phone mentions < 8")

# Reviews
if '5,200' in html or '5200' in html:
    print("✅ Reviews: 5,200+")
else:
    tier1_score -= 20
    tier1_issues.append("❌ Reviews not 5,200+")

# Rating
if '4.9' in html:
    print("✅ Rating: 4.9/5")
else:
    tier1_score -= 20
    tier1_issues.append("❌ Rating not 4.9")

# Warranty
if '90-day' in html.lower() or '90 day' in html.lower():
    print("✅ Warranty: 90-day")
else:
    tier1_score -= 20
    tier1_issues.append("❌ Warranty not 90-day")

print(f"\n{'✅ PASS' if tier1_score >= 100 else '❌ FAIL'} - Score: {tier1_score}/100")
if tier1_issues:
    for issue in tier1_issues:
        print(f"  {issue}")

# TIER 2: SEO FOUNDATIONS
print("\n🔍 TIER 2: SEO FOUNDATIONS (30 params)")
print("-"*70)
tier2_score = 100
tier2_issues = []

# Title tag
title_match = re.search(r'<title>(.*?)</title>', html)
if title_match:
    title = title_match.group(1)
    title_len = len(title)
    if 50 <= title_len <= 60:
        print(f"✅ Title: {title_len} chars (50-60 target)")
    else:
        tier2_score -= 10
        tier2_issues.append(f"⚠️ Title: {title_len} chars (target 50-60)")
        print(f"⚠️ Title: {title_len} chars - '{title}'")

# Meta description
meta_match = re.search(r'<meta name="description" content="(.*?)"', html)
if meta_match:
    meta = meta_match.group(1)
    meta_len = len(meta)
    if 150 <= meta_len <= 160:
        print(f"✅ Meta description: {meta_len} chars (150-160 target)")
    else:
        tier2_score -= 10
        tier2_issues.append(f"⚠️ Meta: {meta_len} chars (target 150-160)")
        print(f"⚠️ Meta description: {meta_len} chars")

# H1
h1_count = len(re.findall(r'<h1[^>]*>', html))
if h1_count == 1:
    print(f"✅ H1 tags: {h1_count} (exactly 1)")
else:
    tier2_score -= 15
    tier2_issues.append(f"❌ H1 tags: {h1_count} (need exactly 1)")

# H2
h2_count = len(re.findall(r'<h2[^>]*>', html))
if 5 <= h2_count <= 10:
    print(f"✅ H2 tags: {h2_count} (5-10 target)")
else:
    tier2_score -= 10
    tier2_issues.append(f"⚠️ H2 tags: {h2_count} (target 5-10)")
    print(f"⚠️ H2 tags: {h2_count}")

# Canonical
if 'rel="canonical"' in html:
    print("✅ Canonical URL: Present")
else:
    tier2_score -= 10
    tier2_issues.append("❌ Canonical URL: Missing")

# LocalBusiness schema
if '"@type": "LocalBusiness"' in html or '"@type":"LocalBusiness"' in html:
    print("✅ LocalBusiness schema: Present")
else:
    tier2_score -= 15
    tier2_issues.append("❌ LocalBusiness schema: Missing")

print(f"\n{'✅ PASS' if tier2_score >= 98 else '❌ FAIL'} - Score: {tier2_score}/100 (need 98+)")
if tier2_issues:
    for issue in tier2_issues:
        print(f"  {issue}")

# TIER 3: AI SEARCH
print("\n🤖 TIER 3: AI SEARCH OPTIMIZATION (25 params)")
print("-"*70)
tier3_score = 100
tier3_issues = []

# FAQPage schema
if '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html:
    print("✅ FAQPage schema: Present")
else:
    tier3_score -= 20
    tier3_issues.append("❌ FAQPage schema: Missing")

# FAQ count
faq_count = html.count('"@type": "Question"') + html.count('"@type":"Question"')
if faq_count >= 6:
    print(f"✅ FAQ questions: {faq_count} (6+ target)")
else:
    tier3_score -= 15
    tier3_issues.append(f"⚠️ FAQ questions: {faq_count} (need 6+)")

# H3 headings
h3_count = len(re.findall(r'<h3[^>]*>', html))
if 12 <= h3_count <= 20:
    print(f"✅ H3 tags: {h3_count} (12-20 target)")
else:
    tier3_score -= 10
    tier3_issues.append(f"⚠️ H3 tags: {h3_count} (target 12-20)")

print(f"\n{'✅ PASS' if tier3_score >= 98 else '❌ FAIL'} - Score: {tier3_score}/100 (need 98+)")
if tier3_issues:
    for issue in tier3_issues:
        print(f"  {issue}")

# TIER 4: CONTENT QUALITY
print("\n📝 TIER 4: CONTENT QUALITY (40 params)")
print("-"*70)
tier4_score = 100
tier4_issues = []

# Word count (visible)
word_count = len(text_clean.split())
if 2000 <= word_count <= 2500:
    print(f"✅ Word count: {word_count} (2000-2500 target)")
elif 1800 <= word_count < 2000:
    tier4_score -= 5
    tier4_issues.append(f"⚠️ Word count: {word_count} (slightly low)")
    print(f"⚠️ Word count: {word_count} (target 2000-2500)")
elif word_count > 2500:
    tier4_score -= 5
    tier4_issues.append(f"⚠️ Word count: {word_count} (slightly high)")
    print(f"⚠️ Word count: {word_count} (over 2500)")
else:
    tier4_score -= 15
    tier4_issues.append(f"❌ Word count: {word_count} (too low)")
    print(f"❌ Word count: {word_count} (need 2000-2500)")

# Internal links
internal_links = html.count('href="../') + html.count('href="/')
if internal_links >= 10:
    print(f"✅ Internal links: {internal_links} (10+ target)")
else:
    tier4_score -= 10
    tier4_issues.append(f"⚠️ Internal links: {internal_links} (need 10+)")

# Images with alt
img_total = len(re.findall(r'<img[^>]*>', html))
img_with_alt = len(re.findall(r'<img[^>]*alt="[^"]+', html))
alt_percent = (img_with_alt / img_total * 100) if img_total > 0 else 0
if alt_percent >= 90:
    print(f"✅ Images with alt: {img_with_alt}/{img_total} ({alt_percent:.0f}%)")
else:
    tier4_score -= 10
    tier4_issues.append(f"⚠️ Images with alt: {img_with_alt}/{img_total} ({alt_percent:.0f}%)")

print(f"\n{'✅ PASS' if tier4_score >= 98 else '❌ FAIL'} - Score: {tier4_score}/100 (need 98+)")
if tier4_issues:
    for issue in tier4_issues:
        print(f"  {issue}")

# TIER 5: CONVERSION (CRO)
print("\n💰 TIER 5: CONVERSION/CRO (50 params)")
print("-"*70)
tier5_score = 100
tier5_issues = []

# CTA buttons
cta_count = html.count('cta-') + html.count('CTA')
if 5 <= cta_count <= 12:
    print(f"✅ CTAs: {cta_count} (5-12 target)")
else:
    tier5_score -= 10
    tier5_issues.append(f"⚠️ CTAs: {cta_count} (target 5-12)")

# Phone clickable (tel:)
tel_links = html.count('href="tel:')
if tel_links >= 8:
    print(f"✅ Phone tel: links: {tel_links} (8+ target)")
else:
    tier5_score -= 15
    tier5_issues.append(f"⚠️ Phone tel: links: {tel_links} (need 8+)")
    print(f"⚠️ Phone tel: links: {tel_links}")

# Booking form
if 'workiz' in html.lower() or 'booking' in html.lower():
    print("✅ Booking integration: Present")
else:
    tier5_score -= 10
    tier5_issues.append("⚠️ Booking form: Check integration")

print(f"\n{'✅ PASS' if tier5_score >= 85 else '❌ FAIL'} - Score: {tier5_score}/100 (need 85+)")
if tier5_issues:
    for issue in tier5_issues:
        print(f"  {issue}")

# TIER 6: PSYCHOLOGY
print("\n🧠 TIER 6: PSYCHOLOGY (45 params)")
print("-"*70)
tier6_score = 100
tier6_issues = []

# Social proof - rating mentions
rating_mentions = text_clean.lower().count('4.9')
if rating_mentions >= 3:
    print(f"✅ Rating mentions: {rating_mentions} (3+ target)")
else:
    tier6_score -= 10
    tier6_issues.append(f"⚠️ Rating mentions: {rating_mentions} (need 3+)")

# Social proof - review mentions
review_mentions = text_clean.lower().count('5,200') + text_clean.lower().count('5200')
if review_mentions >= 3:
    print(f"✅ Review mentions: {review_mentions} (3+ target)")
else:
    tier6_score -= 10
    tier6_issues.append(f"⚠️ Review mentions: {review_mentions} (need 3+)")

# Urgency triggers
urgency_count = text_clean.lower().count('same-day') + text_clean.lower().count('24/7') + text_clean.lower().count('emergency')
if urgency_count >= 3:
    print(f"✅ Urgency triggers: {urgency_count} (3+ target)")
else:
    tier6_score -= 10
    tier6_issues.append(f"⚠️ Urgency triggers: {urgency_count} (need 3+)")

# Trust signals
trust_count = text_clean.lower().count('licensed') + text_clean.lower().count('insured') + text_clean.lower().count('certified')
if trust_count >= 2:
    print(f"✅ Trust signals: {trust_count} (2+ target)")
else:
    tier6_score -= 10
    tier6_issues.append(f"⚠️ Trust signals: {trust_count} (need 2+)")

print(f"\n{'✅ PASS' if tier6_score >= 98 else '❌ FAIL'} - Score: {tier6_score}/100 (need 98+)")
if tier6_issues:
    for issue in tier6_issues:
        print(f"  {issue}")

# TIER 7: DESIGN & UX
print("\n🎨 TIER 7: DESIGN & UX (60 params)")
print("-"*70)
tier7_score = 100
tier7_issues = []

# Mobile viewport
if 'viewport' in html and 'width=device-width' in html:
    print("✅ Mobile viewport: Present")
else:
    tier7_score -= 15
    tier7_issues.append("❌ Mobile viewport: Missing")

# Responsive typography
clamp_count = html.count('clamp(')
if clamp_count >= 3:
    print(f"✅ CSS clamp(): {clamp_count} (3+ target)")
else:
    tier7_score -= 10
    tier7_issues.append(f"⚠️ CSS clamp(): {clamp_count} (need 3+ for responsive)")
    print(f"⚠️ CSS clamp(): {clamp_count}")

# Image lazy loading
lazy_count = html.count('loading="lazy"')
if lazy_count >= 5:
    print(f"✅ Lazy loading: {lazy_count} images (5+ target)")
else:
    tier7_score -= 5
    tier7_issues.append(f"⚠️ Lazy loading: {lazy_count} (target 5+)")

print(f"\n{'✅ PASS' if tier7_score >= 85 else '❌ FAIL'} - Score: {tier7_score}/100 (need 85+)")
if tier7_issues:
    for issue in tier7_issues:
        print(f"  {issue}")

# TIER 8: PERFORMANCE
print("\n⚡ TIER 8: PERFORMANCE (27 params)")
print("-"*70)
tier8_score = 100
tier8_issues = []

# Minified CSS/JS
if '.min.css' in html or '.min.js' in html:
    print("✅ Minified files: Present")
else:
    tier8_score -= 10
    tier8_issues.append("⚠️ Minified files: Check optimization")

# WebP images
webp_count = html.count('.webp')
if webp_count >= 3:
    print(f"✅ WebP images: {webp_count} (3+ target)")
else:
    tier8_score -= 10
    tier8_issues.append(f"⚠️ WebP images: {webp_count} (target 3+)")

print(f"\n{'✅ PASS' if tier8_score >= 70 else '❌ FAIL'} - Score: {tier8_score}/100 (need 70+)")
if tier8_issues:
    for issue in tier8_issues:
        print(f"  {issue}")

# FINAL SUMMARY
print("\n" + "="*70)
print("FINAL SUMMARY - ALL 8 TIERS")
print("="*70)

tiers = {
    'Tier 1 (Data Consistency)': {'score': tier1_score, 'required': 100, 'critical': True},
    'Tier 2 (SEO Foundations)': {'score': tier2_score, 'required': 98, 'critical': True},
    'Tier 3 (AI Search)': {'score': tier3_score, 'required': 98, 'critical': True},
    'Tier 4 (Content Quality)': {'score': tier4_score, 'required': 98, 'critical': True},
    'Tier 5 (Conversion/CRO)': {'score': tier5_score, 'required': 85, 'critical': False},
    'Tier 6 (Psychology)': {'score': tier6_score, 'required': 98, 'critical': True},
    'Tier 7 (Design & UX)': {'score': tier7_score, 'required': 85, 'critical': False},
    'Tier 8 (Performance)': {'score': tier8_score, 'required': 70, 'critical': False}
}

total_score = sum(t['score'] for t in tiers.values()) / len(tiers)
passed = sum(1 for t in tiers.values() if t['score'] >= t['required'])
failed = len(tiers) - passed

print(f"\n📊 OVERALL SCORE: {total_score:.1f}/100")
print(f"✅ Passed: {passed}/8 tiers")
print(f"❌ Failed: {failed}/8 tiers\n")

for name, data in tiers.items():
    status = "✅ PASS" if data['score'] >= data['required'] else "❌ FAIL"
    critical = " [CRITICAL]" if data['critical'] else ""
    print(f"{status:10} {name:30} {data['score']:3}/100 (need {data['required']}+){critical}")

# Production ready?
critical_failed = sum(1 for t in tiers.values() if t['critical'] and t['score'] < t['required'])
if critical_failed == 0 and total_score >= 90:
    print("\n✅ PRODUCTION READY - All critical tiers passed")
elif critical_failed == 0:
    print(f"\n⚠️ ACCEPTABLE - Critical tiers pass but overall score {total_score:.1f}% (target 90%)")
else:
    print(f"\n❌ NOT PRODUCTION READY - {critical_failed} critical tier(s) failed")

print("="*70)
