#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMAD 8-Tier Incremental Testing System
Tests pages tier-by-tier to prevent errors and hallucinations

Version: 2.0 - October 2025
Author: BMAD Method Team
"""

import re
import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class BMAD8TierTester:
    """8-Tier incremental testing system - test little by little, not all at once"""

    def __init__(self, html_file, config_file="bmad-v2/config/business-data.json"):
        self.html_file = html_file
        self.config_file = config_file
        self.html_content = ""
        self.text_content = ""
        self.config = {}
        self.results = {}

    def load_config(self):
        """Load configuration"""
        config_path = Path(__file__).parent / self.config_file
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"[OK] Loaded config")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load config: {e}")
            return False

    def load_html(self):
        """Load HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()

            # Extract text content
            text = re.sub(r'<script[^>]*>.*?</script>', '', self.html_content, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            self.text_content = ' '.join(text.split())

            print(f"[OK] Loaded HTML: {self.html_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load HTML: {e}")
            return False

    def print_tier_header(self, tier_num, tier_name, param_count, threshold):
        """Print tier header"""
        print("\n" + "=" * 70)
        print(f"TIER {tier_num}: {tier_name.upper()} ({param_count} parameters)")
        print(f"Required Score: {threshold}")
        print("=" * 70)

    def tier1_data_consistency(self):
        """TIER 1: Data Consistency - 16 params - 100% REQUIRED [BLOCKING]"""
        self.print_tier_header(1, "Data Consistency", 16, "100%")

        score = 100
        issues = []

        # Phone number consistency
        phone_normalized = self.config['business_data']['phone_normalized']
        phone_pattern = r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})'
        phones_found = re.findall(phone_pattern, self.html_content)
        phones_normalized = [p.replace('-', '').replace(' ', '') for p in phones_found]

        if phones_normalized:
            unique_phones = list(set(phones_normalized))
            if len(unique_phones) > 1:
                score = 0
                issues.append(f"❌ Phone mismatch: {unique_phones}")
            elif unique_phones[0] != phone_normalized:
                score = 0
                issues.append(f"❌ Phone doesn't match config: {unique_phones[0]} vs {phone_normalized}")

        # Warranty consistency
        warranty_period = self.config['quality_metrics']['warranty_period']
        warranty_pattern = r'(\d+)[-\s]?(day|month|year)s?\s+warranty'
        warranties = re.findall(warranty_pattern, self.html_content, re.IGNORECASE)
        if warranties:
            unique_warranties = list(set([w[0] for w in warranties]))
            if len(unique_warranties) > 1:
                score = 0
                issues.append(f"❌ Warranty mismatch: {unique_warranties}")

        # Rating consistency
        rating = str(self.config['quality_metrics']['rating'])
        rating_pattern = r'ratingValue["\']:\s*["\'](\d\.\d)|(\d\.\d)\s*[★⭐]'
        ratings = re.findall(rating_pattern, self.html_content)
        ratings_flat = [r[0] or r[1] for r in ratings if r[0] or r[1]]
        if ratings_flat:
            unique_ratings = list(set(ratings_flat))
            if len(unique_ratings) > 1:
                score = 0
                issues.append(f"❌ Rating mismatch: {unique_ratings}")

        # Review count consistency
        review_count = str(self.config['quality_metrics']['review_count'])
        review_pattern = r'([\d,]+)\+?\s+(?:reviews?|customers?)|reviewCount["\']:\s*["\'](\d+)'
        reviews = re.findall(review_pattern, self.html_content, re.IGNORECASE)
        reviews_flat = [r[0].replace(',', '') if r[0] else r[1] for r in reviews if r[0] or r[1]]
        if reviews_flat:
            unique_reviews = list(set(reviews_flat))
            if len(unique_reviews) > 1:
                score = 0
                issues.append(f"❌ Review count mismatch: {unique_reviews}")

        # Diagnostic fee consistency
        diagnostic_fee = str(self.config['business_data']['diagnostic_fee'])
        diagnostic_pattern = r'[Dd]iagnostic\s+fee\s+is\s+\$(\d+)'
        diagnostic_fees = re.findall(diagnostic_pattern, self.html_content)
        if diagnostic_fees:
            unique_fees = list(set(diagnostic_fees))
            if len(unique_fees) > 1:
                score = 0
                issues.append(f"❌ Diagnostic fee mismatch: ${', $'.join(unique_fees)}")
            elif unique_fees[0] != diagnostic_fee:
                score = 0
                issues.append(f"❌ Diagnostic fee doesn't match config: ${unique_fees[0]} vs ${diagnostic_fee}")

        self.results['tier1'] = {
            'score': score,
            'issues': issues,
            'passed': score == 100
        }

        print(f"\n{'✅ PASS' if score == 100 else '❌ FAIL'} - Score: {score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return score == 100

    def tier2_seo_foundations(self):
        """TIER 2: SEO Foundations - 30 params - 98% REQUIRED [CRITICAL]"""
        self.print_tier_header(2, "SEO Foundations", 30, "98%")

        score = 0
        max_score = 100
        issues = []

        # Title tag (10 points)
        title_match = re.search(r'<title>(.*?)</title>', self.html_content)
        if title_match:
            title_len = len(title_match.group(1))
            if 50 <= title_len <= 60:
                score += 10
                print("  ✅ Title tag: Optimal length")
            else:
                issues.append(f"⚠️ Title tag: {title_len} chars (target: 50-60)")
        else:
            issues.append("❌ Title tag: Missing")

        # Meta description (10 points)
        meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', self.html_content)
        if meta_desc:
            desc_len = len(meta_desc.group(1))
            if 150 <= desc_len <= 160:
                score += 10
                print("  ✅ Meta description: Optimal length")
            else:
                issues.append(f"⚠️ Meta description: {desc_len} chars (target: 150-160)")
        else:
            issues.append("❌ Meta description: Missing")

        # H1 tag - must be exactly 1 (15 points)
        h1_count = len(re.findall(r'<h1[^>]*>', self.html_content))
        if h1_count == 1:
            score += 15
            print("  ✅ H1 tag: Exactly 1")
        else:
            issues.append(f"❌ H1 tag: {h1_count} found (must be 1)")

        # Canonical URL (10 points)
        canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', self.html_content)
        if canonical:
            score += 10
            print("  ✅ Canonical URL: Present")
        else:
            issues.append("❌ Canonical URL: Missing")

        # Mobile viewport (10 points)
        viewport = re.search(r'<meta\s+name=["\']viewport["\']', self.html_content)
        if viewport:
            score += 10
            print("  ✅ Mobile viewport: Present")
        else:
            issues.append("❌ Mobile viewport: Missing")

        # LocalBusiness schema (20 points)
        if 'LocalBusiness' in self.html_content:
            score += 20
            print("  ✅ LocalBusiness schema: Present")
        else:
            issues.append("❌ LocalBusiness schema: Missing")

        # Open Graph tags (15 points)
        og_count = len(re.findall(r'<meta\s+property=["\']og:', self.html_content))
        if og_count >= 4:
            score += 15
            print("  ✅ Open Graph tags: Present")
        else:
            issues.append(f"⚠️ Open Graph tags: {og_count}/4 (need 4+)")

        # H2 headings (10 points)
        h2_count = len(re.findall(r'<h2[^>]*>', self.html_content))
        if 5 <= h2_count <= 10:
            score += 10
            print("  ✅ H2 headings: Good count")
        else:
            issues.append(f"⚠️ H2 headings: {h2_count} (target: 5-10)")

        final_score = min(100, score)
        passed = final_score >= 98

        self.results['tier2'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def tier3_ai_search(self):
        """TIER 3: AI Search Optimization - 25 params - 98% REQUIRED [CRITICAL]"""
        self.print_tier_header(3, "AI Search Optimization", 25, "98%")

        score = 0
        issues = []

        # FAQPage schema (25 points)
        if 'FAQPage' in self.html_content:
            score += 25
            print("  ✅ FAQPage schema: Present")
        else:
            issues.append("❌ FAQPage schema: Missing")

        # HowTo schema (25 points)
        if re.search(r'"@type":\s*"HowTo"', self.html_content):
            score += 25
            print("  ✅ HowTo schema: Present")
        else:
            issues.append("⚠️ HowTo schema: Missing (recommended for AI)")

        # WebPage schema (20 points)
        if re.search(r'"@type":\s*"WebPage"', self.html_content):
            score += 20
            print("  ✅ WebPage schema: Present")
        else:
            issues.append("⚠️ WebPage schema: Missing")

        # Schema diversity - 4+ types (30 points)
        schema_types = re.findall(r'"@type":\s*"([^"]+)"', self.html_content)
        unique_schemas = len(set(schema_types))
        if unique_schemas >= 4:
            score += 30
            print(f"  ✅ Schema diversity: {unique_schemas} types")
        else:
            issues.append(f"⚠️ Schema diversity: {unique_schemas}/4 types (need 4+)")

        final_score = min(100, score)
        passed = final_score >= 98

        self.results['tier3'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def tier4_content_quality(self):
        """TIER 4: Content Quality - 40 params - 98% REQUIRED [CRITICAL]"""
        self.print_tier_header(4, "Content Quality", 40, "98%")

        score = 0
        issues = []

        # Word count (20 points)
        words = re.findall(r'\b\w+\b', self.text_content.lower())
        word_count = len(words)
        target_min = self.config['bmad_targets']['content_word_count_min']
        target_max = self.config['bmad_targets']['content_word_count_max']

        if target_min <= word_count <= target_max:
            score += 20
            print(f"  ✅ Word count: {word_count} (optimal)")
        else:
            issues.append(f"⚠️ Word count: {word_count} (target: {target_min}-{target_max})")

        # Keyword density (20 points)
        primary_keyword = self.config['keywords']['primary'].lower()
        keyword_count = self.text_content.lower().count(primary_keyword)
        keyword_density = (keyword_count * len(primary_keyword.split()) / word_count * 100) if word_count > 0 else 0

        if 1.5 <= keyword_density <= 3.0:
            score += 20
            print(f"  ✅ Keyword density: {keyword_density:.2f}%")
        else:
            issues.append(f"⚠️ Keyword density: {keyword_density:.2f}% (target: 1.5-3.0%)")

        # Bullet lists (15 points)
        lists = len(re.findall(r'<ul|<ol', self.html_content, re.IGNORECASE))
        if lists >= 3:
            score += 15
            print(f"  ✅ Bullet lists: {lists}")
        else:
            issues.append(f"⚠️ Bullet lists: {lists} (need 3+)")

        # Section structure (15 points)
        sections = len(re.findall(r'<section', self.html_content, re.IGNORECASE))
        if 8 <= sections <= 15:
            score += 15
            print(f"  ✅ Sections: {sections}")
        else:
            issues.append(f"⚠️ Sections: {sections} (target: 8-15)")

        # Internal links (15 points)
        internal_links = len(re.findall(r'<a\s+[^>]*href=["\'](?:/|#|[^h])[^"\']*["\']', self.html_content))
        if internal_links >= 10:
            score += 15
            print(f"  ✅ Internal links: {internal_links}")
        else:
            issues.append(f"⚠️ Internal links: {internal_links} (need 10+)")

        # Images with alt text (15 points)
        images = len(re.findall(r'<img[^>]*>', self.html_content))
        images_with_alt = len(re.findall(r'<img[^>]*alt=["\']', self.html_content))
        if images >= 10 and images_with_alt >= images * 0.8:
            score += 15
            print(f"  ✅ Images: {images} (80%+ have alt text)")
        else:
            issues.append(f"⚠️ Images: {images_with_alt}/{images} with alt text")

        final_score = min(100, score)
        passed = final_score >= 98

        self.results['tier4'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def tier5_conversion(self):
        """TIER 5: Conversion (CRO) - 50 params - 85% REQUIRED [HIGH]"""
        self.print_tier_header(5, "Conversion (CRO)", 50, "85%")

        score = 0
        issues = []

        # CTA count (25 points)
        ctas = len(re.findall(r'<a[^>]*(?:btn|button|cta)[^>]*>|<button', self.html_content, re.IGNORECASE))
        if 3 <= ctas <= 15:
            score += 25
            print(f"  ✅ CTA count: {ctas}")
        else:
            issues.append(f"⚠️ CTA count: {ctas} (target: 3-15)")

        # Phone tel: links (30 points)
        tel_links = len(re.findall(r'<a\s+[^>]*href=["\']tel:', self.html_content))
        if 8 <= tel_links <= 20:
            score += 30
            print(f"  ✅ Phone tel: links: {tel_links}")
        else:
            issues.append(f"⚠️ Phone tel: links: {tel_links} (target: 8-20)")

        # Form present (20 points)
        has_form = '<form' in self.html_content or 'workiz' in self.html_content.lower()
        if has_form:
            score += 20
            print("  ✅ Booking form: Present")
        else:
            issues.append("❌ Booking form: Missing")

        # Phone in header/hero (25 points)
        phone_number = self.config['business_data']['phone_number']
        phone_in_first_1000 = phone_number in self.html_content[:1000]
        if phone_in_first_1000:
            score += 25
            print("  ✅ Phone in header: Present")
        else:
            issues.append("⚠️ Phone in header: Not found in first 1000 chars")

        final_score = min(100, score)
        passed = final_score >= 85

        self.results['tier5'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def tier6_psychology(self):
        """TIER 6: Psychology - 45 params - 98% REQUIRED [CRITICAL]"""
        self.print_tier_header(6, "Psychology", 45, "98%")

        score = 0
        issues = []

        # Social proof - rating displays (20 points)
        rating_mentions = len(re.findall(r'\d\.\d\s*[★⭐]', self.html_content))
        if rating_mentions >= 3:
            score += 20
            print(f"  ✅ Rating displays: {rating_mentions}")
        else:
            issues.append(f"⚠️ Rating displays: {rating_mentions} (need 3+)")

        # Social proof - review mentions (20 points)
        review_mentions = len(re.findall(r'5,200|5200', self.html_content))
        if review_mentions >= 3:
            score += 20
            print(f"  ✅ Review mentions: {review_mentions}")
        else:
            issues.append(f"⚠️ Review mentions: {review_mentions} (need 3+)")

        # Authority signals (20 points)
        authority_keywords = ['licensed', 'insured', 'certified', 'professional', 'expert']
        authority_found = sum(1 for kw in authority_keywords if kw in self.text_content.lower())
        if authority_found >= 3:
            score += 20
            print(f"  ✅ Authority signals: {authority_found}/5")
        else:
            issues.append(f"⚠️ Authority signals: {authority_found}/5 (need 3+)")

        # Urgency triggers (20 points)
        urgency_keywords = ['same-day', 'today', 'now', 'emergency', '24/7', 'immediate']
        urgency_found = sum(1 for kw in urgency_keywords if kw in self.text_content.lower())
        if urgency_found >= 3:
            score += 20
            print(f"  ✅ Urgency triggers: {urgency_found}/6")
        else:
            issues.append(f"⚠️ Urgency triggers: {urgency_found}/6 (need 3+)")

        # Pain points (20 points)
        pain_keywords = ['problem', 'broken', 'not working', 'issue', 'trouble']
        pain_found = sum(1 for kw in pain_keywords if kw in self.text_content.lower())
        if pain_found >= 3:
            score += 20
            print(f"  ✅ Pain points: {pain_found}/5")
        else:
            issues.append(f"⚠️ Pain points: {pain_found}/5 (need 3+)")

        final_score = min(100, score)
        passed = final_score >= 98

        self.results['tier6'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def tier7_design_ux(self):
        """TIER 7: Design & UX - 60 params - 85% REQUIRED [MEDIUM]"""
        self.print_tier_header(7, "Design & UX", 60, "85%")

        score = 0
        issues = []

        # Mobile viewport (15 points)
        if 'viewport' in self.html_content:
            score += 15
            print("  ✅ Mobile viewport: Present")
        else:
            issues.append("❌ Mobile viewport: Missing")

        # Responsive typography (clamp) (20 points)
        clamp_usage = len(re.findall(r'clamp\s*\(', self.html_content, re.IGNORECASE))
        if clamp_usage >= 5:
            score += 20
            print(f"  ✅ Responsive typography: {clamp_usage} clamp() uses")
        else:
            issues.append(f"⚠️ Responsive typography: {clamp_usage} clamp() uses (need 5+)")

        # Mobile CSS breakpoints (15 points)
        mobile_css = len(re.findall(r'@media.*?max-width.*?768px', self.html_content, re.IGNORECASE))
        if mobile_css >= 1:
            score += 15
            print("  ✅ Mobile CSS: Breakpoints present")
        else:
            issues.append("⚠️ Mobile CSS: No breakpoints found")

        # Lazy loading images (20 points)
        lazy_images = len(re.findall(r'loading=["\']lazy["\']', self.html_content, re.IGNORECASE))
        total_images = len(re.findall(r'<img', self.html_content, re.IGNORECASE))
        if total_images > 0 and lazy_images / total_images >= 0.5:
            score += 20
            print(f"  ✅ Lazy loading: {lazy_images}/{total_images} images")
        else:
            issues.append(f"⚠️ Lazy loading: {lazy_images}/{total_images} images (need 50%+)")

        # Alt text on images (15 points)
        images_with_alt = len(re.findall(r'<img[^>]*alt=["\']', self.html_content))
        if total_images > 0 and images_with_alt / total_images >= 0.8:
            score += 15
            print(f"  ✅ Image alt text: {images_with_alt}/{total_images}")
        else:
            issues.append(f"⚠️ Image alt text: {images_with_alt}/{total_images} (need 80%+)")

        # Mobile menu (15 points)
        has_mobile_menu = 'hamburger' in self.html_content.lower() or 'menu-toggle' in self.html_content.lower()
        if has_mobile_menu:
            score += 15
            print("  ✅ Mobile menu: Present")
        else:
            issues.append("⚠️ Mobile menu: Not found")

        final_score = min(100, score)
        passed = final_score >= 85

        self.results['tier7'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def tier8_performance(self):
        """TIER 8: Performance - 27 params - 70% TARGET [LOW]"""
        self.print_tier_header(8, "Performance", 27, "70%")

        score = 0
        issues = []

        # Minified CSS (30 points)
        has_minified_css = bool(re.search(r'\.min\.css', self.html_content))
        if has_minified_css:
            score += 30
            print("  ✅ Minified CSS: Present")
        else:
            issues.append("⚠️ Minified CSS: Not found")

        # Lazy loading (30 points)
        lazy_images = len(re.findall(r'loading=["\']lazy["\']', self.html_content, re.IGNORECASE))
        if lazy_images >= 5:
            score += 30
            print(f"  ✅ Lazy loading: {lazy_images} images")
        else:
            issues.append(f"⚠️ Lazy loading: {lazy_images} images (recommended: 5+)")

        # Async scripts (20 points)
        async_scripts = len(re.findall(r'<script[^>]*(?:async|defer)', self.html_content))
        if async_scripts >= 1:
            score += 20
            print(f"  ✅ Async scripts: {async_scripts}")
        else:
            issues.append("⚠️ Async scripts: None found")

        # WebP images (20 points)
        webp_images = len(re.findall(r'\.webp', self.html_content, re.IGNORECASE))
        if webp_images >= 1:
            score += 20
            print(f"  ✅ WebP images: {webp_images}")
        else:
            issues.append("⚠️ WebP images: None found (optional)")

        final_score = min(100, score)
        passed = final_score >= 70

        self.results['tier8'] = {
            'score': final_score,
            'issues': issues,
            'passed': passed
        }

        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} - Score: {final_score}/100")
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")

        return passed

    def print_final_report(self):
        """Print final comprehensive report"""
        print("\n" + "=" * 70)
        print("FINAL REPORT - 8-TIER BMAD TEST")
        print("=" * 70)
        print(f"\nFile: {self.html_file}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n" + "-" * 70)
        print("TIER RESULTS:")
        print("-" * 70)

        tier_names = [
            "Tier 1: Data Consistency",
            "Tier 2: SEO Foundations",
            "Tier 3: AI Search",
            "Tier 4: Content Quality",
            "Tier 5: Conversion (CRO)",
            "Tier 6: Psychology",
            "Tier 7: Design & UX",
            "Tier 8: Performance"
        ]

        thresholds = [100, 98, 98, 98, 85, 98, 85, 70]

        all_passed = True
        total_score = 0

        for i, (tier_key, tier_name) in enumerate(zip(self.results.keys(), tier_names), 1):
            result = self.results[tier_key]
            score = result['score']
            passed = result['passed']
            threshold = thresholds[i-1]

            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{tier_name:35} {score:3}/100  {status}  (req: {threshold}%)")

            if not passed:
                all_passed = False

            total_score += score

        avg_score = total_score / len(self.results) if self.results else 0

        print("\n" + "-" * 70)
        print(f"OVERALL SCORE: {avg_score:.1f}/100")
        print("-" * 70)

        if all_passed and avg_score >= 85:
            print("\n🎉 DEPLOYMENT APPROVED")
            print("All tiers passed. Page is production-ready.")
        elif not all_passed:
            print("\n❌ DEPLOYMENT BLOCKED")
            print("Fix failing tiers before deployment.")
        else:
            print("\n⚠️ NEEDS IMPROVEMENT")
            print(f"Overall score {avg_score:.1f}/100 is below 85%.")

        print("\n" + "=" * 70)


def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("BMAD 8-TIER INCREMENTAL TESTING SYSTEM")
        print("=" * 70)
        print("\nUsage:")
        print("  python bmad-8tier-test.py <html-file> [--tier N] [--auto-run]")
        print("\nExamples:")
        print("  python bmad-8tier-test.py locations/toronto.html --tier 1")
        print("  python bmad-8tier-test.py locations/toronto.html --auto-run")
        print("\nOptions:")
        print("  --tier N     Test only tier N (1-8)")
        print("  --auto-run   Run all tiers sequentially")
        print("\n" + "=" * 70)
        sys.exit(1)

    html_file = sys.argv[1]

    if not os.path.exists(html_file):
        print(f"[ERROR] File not found: {html_file}")
        sys.exit(1)

    tester = BMAD8TierTester(html_file)

    if not tester.load_config():
        sys.exit(1)

    if not tester.load_html():
        sys.exit(1)

    print("\n" + "=" * 70)
    print("BMAD 8-TIER INCREMENTAL TESTING")
    print("=" * 70)
    print(f"File: {html_file}")
    print("Testing little by little to prevent errors...")

    # Check if specific tier requested
    if '--tier' in sys.argv:
        tier_idx = sys.argv.index('--tier')
        if tier_idx + 1 < len(sys.argv):
            tier_num = int(sys.argv[tier_idx + 1])

            tier_methods = [
                tester.tier1_data_consistency,
                tester.tier2_seo_foundations,
                tester.tier3_ai_search,
                tester.tier4_content_quality,
                tester.tier5_conversion,
                tester.tier6_psychology,
                tester.tier7_design_ux,
                tester.tier8_performance
            ]

            if 1 <= tier_num <= 8:
                tier_methods[tier_num - 1]()
            else:
                print(f"[ERROR] Invalid tier: {tier_num} (must be 1-8)")
                sys.exit(1)
    else:
        # Auto-run all tiers
        tier_methods = [
            tester.tier1_data_consistency,
            tester.tier2_seo_foundations,
            tester.tier3_ai_search,
            tester.tier4_content_quality,
            tester.tier5_conversion,
            tester.tier6_psychology,
            tester.tier7_design_ux,
            tester.tier8_performance
        ]

        for i, method in enumerate(tier_methods, 1):
            passed = method()

            # If critical tier fails, stop (Tiers 1-4 and 6 are critical)
            critical_tiers = [1, 2, 3, 4, 6]
            if not passed and i in critical_tiers:
                print(f"\n❌ CRITICAL TIER {i} FAILED - STOPPING")
                print("Fix issues and re-run from this tier")
                sys.exit(1)

        tester.print_final_report()


if __name__ == "__main__":
    main()
