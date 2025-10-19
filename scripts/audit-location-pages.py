#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit all location pages to understand current state: design, content, BMAD status."""

import os
import sys
import glob
import re
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_page(file_path):
    """Analyze a single location page."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    page_name = os.path.basename(file_path)

    # Extract key data
    analysis = {
        'name': page_name,
        'path': file_path,
        'file_size_kb': round(len(content) / 1024, 1),
    }

    # Check for design elements
    analysis['has_header'] = bool(re.search(r'<header class="site-header"', content))
    analysis['has_footer'] = bool(re.search(r'<footer class="seo-footer', content))
    analysis['has_hero'] = bool(re.search(r'class="hero', content, re.IGNORECASE))

    # Check for CSS links
    css_count = len(re.findall(r'<link rel="stylesheet"', content))
    analysis['css_files'] = css_count

    # Check for JS scripts
    js_count = len(re.findall(r'<script src=', content))
    analysis['js_files'] = js_count

    # Check for schema
    analysis['has_local_business_schema'] = bool(re.search(r'"@type":\s*"LocalBusiness"', content))
    analysis['has_aggregate_rating'] = bool(re.search(r'"@type":\s*"AggregateRating"', content))

    # Check for H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    analysis['h1'] = h1_match.group(1).strip()[:80] if h1_match else 'NO H1'

    # Check title
    title_match = re.search(r'<title>(.*?)</title>', content)
    analysis['title'] = title_match.group(1)[:80] if title_match else 'NO TITLE'

    # Count H2 and H3
    analysis['h2_count'] = len(re.findall(r'<h2[^>]*>', content))
    analysis['h3_count'] = len(re.findall(r'<h3[^>]*>', content))

    # Check for FAQ section
    analysis['has_faq'] = bool(re.search(r'Frequently Asked Questions|FAQ', content, re.IGNORECASE))

    # Check for location section (60+ SERVICE AREAS)
    analysis['has_location_section'] = bool(re.search(r'60\+ SERVICE AREAS|SERVICE AREAS', content))

    # Check for Workiz booking form
    analysis['has_workiz'] = bool(re.search(r'workiz\.com', content))

    # Estimate word count (rough - visible text only)
    text_content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
    text_content = re.sub(r'<style.*?</style>', '', text_content, flags=re.DOTALL)
    text_content = re.sub(r'<[^>]+>', ' ', text_content)
    words = len(text_content.split())
    analysis['word_count_estimate'] = words

    # Check for review count
    review_match = re.search(r'(520\+|5,200\+)', content)
    analysis['review_count'] = review_match.group(1) if review_match else 'NOT FOUND'

    # Check canonical URL
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)">', content)
    analysis['canonical'] = canonical_match.group(1) if canonical_match else 'NO CANONICAL'

    # Check paths (relative vs absolute)
    css_href_sample = re.search(r'<link rel="stylesheet" href="([^"]+)"', content)
    analysis['css_path_type'] = 'relative (../)' if css_href_sample and '../' in css_href_sample.group(1) else 'other'

    return analysis

def main():
    """Main function."""
    print("="*80)
    print("LOCATION PAGES AUDIT")
    print("="*80)
    print()

    # Find all location pages
    location_files = glob.glob('locations/*.html')

    if not location_files:
        print("ERROR: No location pages found in locations/")
        return

    print(f"Found {len(location_files)} location pages\n")
    print("="*80)

    results = []
    for file_path in sorted(location_files):
        try:
            analysis = analyze_page(file_path)
            results.append(analysis)
        except Exception as e:
            print(f"ERROR analyzing {file_path}: {e}")

    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY TABLE")
    print(f"{'='*80}\n")

    # Header
    print(f"{'Page':<25} {'Size':<8} {'CSS':<5} {'H1':<6} {'Words':<8} {'Review':<10} {'Design Status':<30}")
    print("-" * 80)

    for r in results:
        page_name = r['name'].replace('.html', '')
        size = f"{r['file_size_kb']}KB"
        css = str(r['css_files'])
        h1_status = '✓' if r['h1'] != 'NO H1' else '✗'
        words = str(r['word_count_estimate'])
        review = r['review_count']

        # Design status
        design_parts = []
        if r['has_header']: design_parts.append('Hdr')
        if r['has_footer']: design_parts.append('Ftr')
        if r['has_faq']: design_parts.append('FAQ')
        if r['has_workiz']: design_parts.append('Wrkz')
        design_status = '+'.join(design_parts) if design_parts else 'MINIMAL'

        print(f"{page_name:<25} {size:<8} {css:<5} {h1_status:<6} {words:<8} {review:<10} {design_status:<30}")

    # Categorize pages
    print(f"\n{'='*80}")
    print("CATEGORIZATION")
    print(f"{'='*80}\n")

    full_design = [r for r in results if r['has_header'] and r['has_footer'] and r['has_faq']]
    partial_design = [r for r in results if (r['has_header'] or r['has_footer']) and not (r['has_header'] and r['has_footer'] and r['has_faq'])]
    minimal_design = [r for r in results if not r['has_header'] and not r['has_footer']]

    print(f"✓ FULL DESIGN ({len(full_design)}): Header + Footer + FAQ + Location section")
    for r in full_design:
        print(f"  - {r['name']}")

    print(f"\n⚠ PARTIAL DESIGN ({len(partial_design)}): Missing some elements")
    for r in partial_design:
        print(f"  - {r['name']}")

    print(f"\n✗ MINIMAL DESIGN ({len(minimal_design)}): No header/footer")
    for r in minimal_design:
        print(f"  - {r['name']}")

    # Review count check
    print(f"\n{'='*80}")
    print("REVIEW COUNT CHECK")
    print(f"{'='*80}\n")

    correct_review = [r for r in results if '5,200+' in r['review_count']]
    wrong_review = [r for r in results if '520+' in r['review_count']]
    no_review = [r for r in results if 'NOT FOUND' in r['review_count']]

    print(f"✓ Correct (5,200+): {len(correct_review)} pages")
    print(f"✗ Wrong (520+): {len(wrong_review)} pages")
    print(f"⚠ Missing: {len(no_review)} pages")

    # Schema check
    print(f"\n{'='*80}")
    print("SCHEMA CHECK")
    print(f"{'='*80}\n")

    has_schema = [r for r in results if r['has_local_business_schema'] and r['has_aggregate_rating']]
    partial_schema = [r for r in results if r['has_local_business_schema'] or r['has_aggregate_rating']]
    no_schema = [r for r in results if not r['has_local_business_schema'] and not r['has_aggregate_rating']]

    print(f"✓ Full schema (LocalBusiness + AggregateRating): {len(has_schema)} pages")
    print(f"⚠ Partial schema: {len(partial_schema) - len(has_schema)} pages")
    print(f"✗ No schema: {len(no_schema)} pages")

    # Word count distribution
    print(f"\n{'='*80}")
    print("WORD COUNT DISTRIBUTION")
    print(f"{'='*80}\n")

    under_1500 = [r for r in results if r['word_count_estimate'] < 1500]
    good_range = [r for r in results if 1500 <= r['word_count_estimate'] <= 2500]
    over_2500 = [r for r in results if r['word_count_estimate'] > 2500]

    print(f"⚠ Under 1500 words: {len(under_1500)} pages")
    print(f"✓ Good (1500-2500): {len(good_range)} pages")
    print(f"⚠ Over 2500 words: {len(over_2500)} pages")

    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print(f"{'='*80}\n")

    print("PRIORITY 1 - Fix Critical Issues:")
    print(f"  1. {len(wrong_review)} pages with wrong review count (520+ → 5,200+)")
    print(f"  2. {len(minimal_design)} pages with no header/footer (need global design)")
    print(f"  3. {len(no_schema)} pages with no schema (need LocalBusiness + AggregateRating)")

    print("\nPRIORITY 2 - Content Optimization:")
    print(f"  1. {len(under_1500)} pages under 1500 words (need more content)")
    print(f"  2. {len(over_2500)} pages over 2500 words (may need trimming)")

    print("\nPRIORITY 3 - Design Consistency:")
    print(f"  1. {len(partial_design)} pages with partial design (standardize)")
    print(f"  2. All pages should have: Header, Footer, FAQ, Location section, Workiz")

    print(f"\n{'='*80}")
    print("✓ Audit complete!")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
