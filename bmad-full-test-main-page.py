#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick BMAD Full Test - All Tiers Without Stopping
Main Page (index.html)
"""

import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

html_file = "index.html"

# Load and parse HTML
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Count visible words (exclude HTML tags, scripts, styles)
text_only = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
text_only = re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=re.DOTALL | re.IGNORECASE)
text_only = re.sub(r'<[^>]+>', ' ', text_only)
text_only = re.sub(r'\s+', ' ', text_only)
words = text_only.split()
word_count = len(words)

print("=" * 70)
print("🎯 BMAD FULL TEST - MAIN PAGE (index.html)")
print("=" * 70)
print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 1: DATA CONSISTENCY (15 params) - 100% required [CRITICAL]
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 1: DATA CONSISTENCY [CRITICAL]")
print("-" * 70)
tier1_score = 100

# Phone number consistency
phone_count = html.count('437-747-6737')
if phone_count >= 8:
    print(f"✅ Phone: 437-747-6737 ({phone_count} mentions, 8+ target)")
else:
    tier1_score -= 25
    print(f"❌ Phone: 437-747-6737 ({phone_count} mentions, need 8+)")

# Review count consistency
review_patterns = ['5,200+', '5200', '5,200']
review_found = any(pattern in html for pattern in review_patterns)
if review_found:
    print(f"✅ Reviews: 5,200+ mentions found")
else:
    tier1_score -= 25
    print(f"❌ Reviews: 5,200+ not found consistently")

# Rating consistency
rating_count = html.count('4.9')
if rating_count >= 3:
    print(f"✅ Rating: 4.9/5 ({rating_count} mentions, 3+ target)")
else:
    tier1_score -= 25
    print(f"❌ Rating: 4.9/5 ({rating_count} mentions, need 3+)")

# Warranty consistency
warranty_count = html.count('90-day')
if warranty_count >= 3:
    print(f"✅ Warranty: 90-day ({warranty_count} mentions, 3+ target)")
else:
    tier1_score -= 25
    print(f"❌ Warranty: 90-day ({warranty_count} mentions, need 3+)")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 2: SEO FOUNDATIONS (30 params) - 98% required [CRITICAL]
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 2: SEO FOUNDATIONS [CRITICAL]")
print("-" * 70)
tier2_score = 100

# Title tag
title_match = re.search(r'<title>(.*?)</title>', html)
if title_match:
    title = title_match.group(1)
    title_len = len(title)
    if 50 <= title_len <= 60:
        print(f"✅ Title: {title_len} chars (50-60 target)")
        print(f"   '{title}'")
    else:
        tier2_score -= 10
        print(f"❌ Title: {title_len} chars (need 50-60)")
        print(f"   '{title}'")
else:
    tier2_score -= 15
    print("❌ Title: No title tag found")

# Meta description
meta_match = re.search(r'<meta name="description" content="([^"]*)"', html)
if meta_match:
    meta = meta_match.group(1)
    meta_len = len(meta)
    if 150 <= meta_len <= 160:
        print(f"✅ Meta: {meta_len} chars (150-160 target)")
    else:
        tier2_score -= 10
        print(f"❌ Meta: {meta_len} chars (need 150-160)")
        print(f"   '{meta}'")
else:
    tier2_score -= 15
    print("❌ Meta: No meta description found")

# H1 tags
h1_count = len(re.findall(r'<h1[^>]*>.*?</h1>', html, re.DOTALL))
if h1_count == 1:
    print(f"✅ H1 tags: {h1_count} (exactly 1 required)")
else:
    tier2_score -= 15
    print(f"❌ H1 tags: {h1_count} (need exactly 1)")

# H2 tags
h2_count = len(re.findall(r'<h2[^>]*>.*?</h2>', html, re.DOTALL))
if 5 <= h2_count <= 10:
    print(f"✅ H2 tags: {h2_count} (5-10 target)")
else:
    tier2_score -= 10
    print(f"❌ H2 tags: {h2_count} (need 5-10)")

# Canonical URL
if '<link rel="canonical"' in html:
    print(f"✅ Canonical: Present")
else:
    tier2_score -= 10
    print(f"❌ Canonical: Missing")

# Schema markup
if '"@type": "LocalBusiness"' in html or '"@type": "Organization"' in html:
    print(f"✅ Schema: LocalBusiness/Organization present")
else:
    tier2_score -= 10
    print(f"❌ Schema: LocalBusiness/Organization missing")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 3: AI SEARCH OPTIMIZATION (25 params) - 98% required [CRITICAL]
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 3: AI SEARCH OPTIMIZATION [CRITICAL]")
print("-" * 70)
tier3_score = 100

# FAQ schema
faq_count = html.count('"@type": "Question"')
if faq_count >= 6:
    print(f"✅ FAQ questions: {faq_count} (6+ target)")
else:
    tier3_score -= 25
    print(f"❌ FAQ questions: {faq_count} (need 6+)")

# H3 tags (should be 12-20)
h3_count = len(re.findall(r'<h3[^>]*>.*?</h3>', html, re.DOTALL))
if 12 <= h3_count <= 20:
    print(f"✅ H3 tags: {h3_count} (12-20 target)")
else:
    tier3_score -= 25
    print(f"❌ H3 tags: {h3_count} (need 12-20)")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 4: CONTENT QUALITY (40 params) - 98% required [CRITICAL]
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 4: CONTENT QUALITY [CRITICAL]")
print("-" * 70)
tier4_score = 100

# Word count
if 2000 <= word_count <= 2500:
    print(f"✅ Word count: {word_count} (2000-2500 target)")
elif 1800 <= word_count < 2000:
    tier4_score -= 5
    print(f"⚠️  Word count: {word_count} (slightly under 2000)")
elif 2500 < word_count <= 2700:
    tier4_score -= 5
    print(f"⚠️  Word count: {word_count} (slightly over 2500)")
else:
    tier4_score -= 15
    print(f"❌ Word count: {word_count} (need 2000-2500)")

# Internal links
internal_link_count = html.count('href="/') + html.count('href="./') + html.count('href="../')
if internal_link_count >= 10:
    print(f"✅ Internal links: {internal_link_count} (10+ target)")
else:
    tier4_score -= 10
    print(f"❌ Internal links: {internal_link_count} (need 10+)")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 5: CONVERSION/CRO (50 params) - 85% required
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 5: CONVERSION/CRO")
print("-" * 70)
tier5_score = 100

# CTA buttons
cta_patterns = ['call now', 'book now', 'schedule', 'contact', 'call 437-747-6737']
cta_count = sum(html.lower().count(pattern) for pattern in cta_patterns)
if cta_count >= 5:
    print(f"✅ CTA buttons: {cta_count} CTAs found (5+ target)")
else:
    tier5_score -= 15
    print(f"❌ CTA buttons: {cta_count} CTAs (need 5+)")

# Urgency elements
urgency_patterns = ['same-day', 'same day', 'today', 'now', 'emergency', '24/7']
urgency_count = sum(html.lower().count(pattern) for pattern in urgency_patterns)
if urgency_count >= 3:
    print(f"✅ Urgency: {urgency_count} urgency phrases (3+ target)")
else:
    tier5_score -= 10
    print(f"⚠️  Urgency: {urgency_count} urgency phrases (3+ recommended)")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 6: PSYCHOLOGY (45 params) - 98% required [CRITICAL]
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 6: PSYCHOLOGY [CRITICAL]")
print("-" * 70)
tier6_score = 100

# Social proof
if '5,200+' in html or '5200' in html:
    print(f"✅ Social proof: Review count visible")
else:
    tier6_score -= 10
    print(f"❌ Social proof: Review count not visible")

# Trust signals
trust_patterns = ['licensed', 'insured', 'certified', 'warranty', 'guarantee']
trust_count = sum(html.lower().count(pattern) for pattern in trust_patterns)
if trust_count >= 5:
    print(f"✅ Trust signals: {trust_count} found (5+ target)")
else:
    tier6_score -= 10
    print(f"❌ Trust signals: {trust_count} (need 5+)")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 7: DESIGN & UX (60 params) - 85% required
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 7: DESIGN & UX")
print("-" * 70)
tier7_score = 100

# Mobile viewport
if 'name="viewport"' in html:
    print(f"✅ Mobile: Viewport meta tag present")
else:
    tier7_score -= 15
    print(f"❌ Mobile: Viewport meta tag missing")

# Images with alt text
img_tags = len(re.findall(r'<img[^>]+>', html))
img_with_alt = len(re.findall(r'<img[^>]+alt="[^"]*"[^>]*>', html))
if img_tags > 0:
    alt_ratio = (img_with_alt / img_tags) * 100
    if alt_ratio >= 90:
        print(f"✅ Images: {img_with_alt}/{img_tags} have alt text ({alt_ratio:.0f}%)")
    else:
        tier7_score -= 10
        print(f"⚠️  Images: {img_with_alt}/{img_tags} have alt text ({alt_ratio:.0f}%, 90%+ target)")

print()

# ═══════════════════════════════════════════════════════════════════════
# TIER 8: PERFORMANCE (27 params) - 70% target
# ═══════════════════════════════════════════════════════════════════════
print("🔍 TIER 8: PERFORMANCE")
print("-" * 70)
tier8_score = 100

# Lazy loading
lazy_count = html.count('loading="lazy"')
if lazy_count >= 3:
    print(f"✅ Lazy loading: {lazy_count} images (3+ target)")
else:
    tier8_score -= 10
    print(f"⚠️  Lazy loading: {lazy_count} images (3+ recommended)")

# WebP images
webp_count = html.count('.webp')
if webp_count >= 3:
    print(f"✅ WebP format: {webp_count} images (3+ target)")
else:
    tier8_score -= 10
    print(f"⚠️  WebP format: {webp_count} images (3+ recommended)")

print()

# ═══════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("📊 TIER SUMMARY")
print("=" * 70)

tiers = {
    'Tier 1 (Data Consistency)': {
        'score': tier1_score,
        'required': 100,
        'critical': True
    },
    'Tier 2 (SEO Foundations)': {
        'score': tier2_score,
        'required': 98,
        'critical': True
    },
    'Tier 3 (AI Search)': {
        'score': tier3_score,
        'required': 98,
        'critical': True
    },
    'Tier 4 (Content Quality)': {
        'score': tier4_score,
        'required': 98,
        'critical': True
    },
    'Tier 5 (Conversion/CRO)': {
        'score': tier5_score,
        'required': 85,
        'critical': False
    },
    'Tier 6 (Psychology)': {
        'score': tier6_score,
        'required': 98,
        'critical': True
    },
    'Tier 7 (Design & UX)': {
        'score': tier7_score,
        'required': 85,
        'critical': False
    },
    'Tier 8 (Performance)': {
        'score': tier8_score,
        'required': 70,
        'critical': False
    }
}

passed = 0
failed = 0
critical_failed = 0

for tier_name, tier_data in tiers.items():
    score = tier_data['score']
    required = tier_data['required']
    is_critical = tier_data['critical']

    if score >= required:
        status = "✅ PASS"
        passed += 1
    else:
        status = "❌ FAIL"
        failed += 1
        if is_critical:
            critical_failed += 1

    critical_badge = " [CRITICAL]" if is_critical else ""

    print(f"{status:8}   {tier_name:30}  {score:3}/100 (need {required}+){critical_badge}")

total_score = sum(t['score'] for t in tiers.values()) / len(tiers)

print()
print("=" * 70)
print(f"📊 OVERALL SCORE: {total_score:.1f}/100")
print(f"✅ Passed: {passed}/{len(tiers)} tiers")
print(f"❌ Failed: {failed}/{len(tiers)} tiers")
print("=" * 70)
print()

if critical_failed > 0:
    print(f"❌ NOT PRODUCTION READY - {critical_failed} critical tier(s) failed")
    print()
    print("Critical tiers that failed:")
    for tier_name, tier_data in tiers.items():
        if tier_data['critical'] and tier_data['score'] < tier_data['required']:
            print(f"  • {tier_name}: {tier_data['score']}/100 (need {tier_data['required']}+)")
elif total_score >= 90:
    print("✅ PRODUCTION READY - All critical tiers passed")
else:
    print(f"⚠️  REVIEW NEEDED - Total score {total_score:.1f}/100 (90+ recommended)")

print()
