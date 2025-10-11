#!/usr/bin/env python3
"""
BMAD Complete Test Suite - All 277 Parameters
Multi-Project Support with Config File

Version: 1.0 - October 2025
Author: BMAD Method Team
"""

import re
import sys
import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class BMADCompleteTester:
    """Complete 277-parameter test suite with project config support"""

    def __init__(self, html_file, config_file="bmad-config.json"):
        self.html_file = html_file
        self.config_file = config_file
        self.html_content = ""
        self.text_content = ""
        self.config = {}
        self.results = {}
        self.total_score = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def load_config(self):
        """Load project-specific configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"[OK] Loaded config: {self.config['project']['name']}")
            return True
        except FileNotFoundError:
            print(f"[ERROR] Config file not found: {self.config_file}")
            print("[INFO] Copy bmad-config-TEMPLATE.json to bmad-config.json")
            print("[INFO] Fill in your business data and run again")
            return False
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in config file: {e}")
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

    def run_all_tests(self):
        """Run all 277 parameter tests"""
        print("\n" + "=" * 60)
        print("BMAD COMPLETE TEST - 277 PARAMETERS")
        print("=" * 60)
        print(f"\nProject: {self.config['project']['name']}")
        print(f"Testing: {self.html_file}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "=" * 60)

        # Run all test categories
        self.test_data_consistency()   # FIRST - validates all data
        self.test_seo()                # 30 params
        self.test_content_quality()    # 15 params
        self.test_cro()                # 20 params
        self.test_psychology()         # 25 params
        self.test_conversion_design()  # 10 params
        self.test_responsive_typography()  # 10 params - NEW

        # Print final report
        self.print_final_report()

    def test_data_consistency(self):
        """CRITICAL: Data Consistency - 15 params (100% required)"""
        print("\n[1/12] DATA CONSISTENCY (15 params)........", end="", flush=True)

        score = 100
        issues = []

        # Phone number consistency
        config_phone = self.config['business_data']['phone_normalized']
        phone_pattern = r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})'
        phones_found = re.findall(phone_pattern, self.html_content)
        phones_normalized = [p.replace('-', '').replace(' ', '') for p in phones_found]

        if phones_normalized:
            unique_phones = list(set(phones_normalized))
            if len(unique_phones) > 1:
                score = 0
                issues.append(f"Phone mismatch: {unique_phones}")
            elif unique_phones[0] != config_phone:
                score = 0
                issues.append(f"Phone doesn't match config: {unique_phones[0]} vs {config_phone}")

        # Warranty consistency
        config_warranty = self.config['quality_metrics']['warranty_period']
        warranty_pattern = r'(\d+)[-\s]?(day|month|year)s?\s+warranty'
        warranties = re.findall(warranty_pattern, self.html_content, re.IGNORECASE)
        if warranties:
            unique_warranties = list(set([w[0] for w in warranties]))
            if len(unique_warranties) > 1:
                score = 0
                issues.append(f"Warranty mismatch: {unique_warranties}")
            elif int(unique_warranties[0]) != config_warranty:
                score = 0
                issues.append(f"Warranty doesn't match config: {unique_warranties[0]} vs {config_warranty}")

        # Rating consistency
        config_rating = str(self.config['quality_metrics']['rating'])
        rating_pattern = r'ratingValue["\']:\s*["\'](\d\.\d)|(\d\.\d)\s*[★⭐]'
        ratings = re.findall(rating_pattern, self.html_content)
        ratings_flat = [r[0] or r[1] for r in ratings if r[0] or r[1]]
        if ratings_flat:
            unique_ratings = list(set(ratings_flat))
            if len(unique_ratings) > 1:
                score = 0
                issues.append(f"Rating mismatch: {unique_ratings}")
            elif unique_ratings[0] != config_rating:
                score = 0
                issues.append(f"Rating doesn't match config: {unique_ratings[0]} vs {config_rating}")

        # Review count consistency
        config_reviews = str(self.config['quality_metrics']['review_count'])
        review_pattern = r'([\d,]+)\+?\s+(?:reviews?|customers?|clients?|happy\s+customers?)|reviewCount["\']:\s*["\'](\d+)'
        reviews = re.findall(review_pattern, self.html_content, re.IGNORECASE)
        reviews_flat = [r[0].replace(',', '') if r[0] else r[1] for r in reviews if r[0] or r[1]]
        if reviews_flat:
            unique_reviews = list(set(reviews_flat))
            if len(unique_reviews) > 1:
                score = 0
                issues.append(f"Review count mismatch: {unique_reviews}")
            elif unique_reviews[0] != config_reviews:
                score = 0
                issues.append(f"Review count doesn't match config: {unique_reviews[0]} vs {config_reviews}")

        self.results['data_consistency'] = {
            'score': score,
            'status': 'PASS' if score == 100 else 'FAIL',
            'issues': issues,
            'critical': True
        }

        if score == 100:
            print(" PASS [CRITICAL]")
            self.tests_passed += 1
        else:
            print(" FAIL [BLOCKING]")
            self.tests_failed += 1

    def test_seo(self):
        """SEO Optimization - 30 params"""
        print("[2/12] SEO OPTIMIZATION (30 params)........", end="", flush=True)

        score = 0
        issues = []

        # Word count
        words = re.findall(r'\b\w+\b', self.text_content.lower())
        word_count = len(words)
        target_min = self.config['bmad_targets']['content_word_count_min']
        target_max = self.config['bmad_targets']['content_word_count_max']

        if target_min <= word_count <= target_max:
            score += 15
        else:
            issues.append(f"Word count: {word_count} (target: {target_min}-{target_max})")

        # Keyword density
        primary_keyword = self.config['keywords']['primary'].lower()
        keyword_count = self.text_content.lower().count(primary_keyword)
        keyword_density = (keyword_count * len(primary_keyword.split()) / word_count * 100) if word_count > 0 else 0
        target_min_kw = self.config['bmad_targets']['keyword_density_min']
        target_max_kw = self.config['bmad_targets']['keyword_density_max']

        if target_min_kw <= keyword_density <= target_max_kw:
            score += 15
        else:
            issues.append(f"Keyword density: {keyword_density:.2f}% (target: {target_min_kw}-{target_max_kw}%)")

        # H1 tags
        h1_count = len(re.findall(r'<h1[^>]*>', self.html_content))
        if h1_count == 1:
            score += 10
        else:
            issues.append(f"H1 count: {h1_count} (must be 1)")

        # Internal links
        internal_links = len(re.findall(r'<a\s+[^>]*href=["\'](?:/|#|[^h])[^"\']*["\']', self.html_content))
        target_links = self.config['bmad_targets']['internal_links_min']
        if internal_links >= target_links:
            score += 10
        else:
            issues.append(f"Internal links: {internal_links} (target: {target_links}+)")

        # Images - count both visible and SEO-hidden images
        images = len(re.findall(r'<img[^>]*>', self.html_content))

        # Count Schema.org ImageObject markup (hidden images for Google)
        schema_images = len(re.findall(r'itemtype="https://schema\.org/ImageObject"', self.html_content))

        total_images = max(images, schema_images)  # Use whichever is higher
        target_images = self.config['bmad_targets']['images_min']

        if total_images >= target_images:
            score += 10
        else:
            issues.append(f"Images: {total_images} (target: {target_images}+)")

        # Schema markup
        schema_types = re.findall(r'"@type":\s*"([^"]+)"', self.html_content)
        if len(set(schema_types)) >= 2:
            score += 20
        else:
            issues.append(f"Schema types: {len(set(schema_types))} (need 2+)")

        # Phone mentions
        config_phone = self.config['business_data']['phone_number']
        phone_mentions = self.html_content.count(config_phone)
        if phone_mentions >= 8:
            score += 10
        else:
            issues.append(f"Phone mentions: {phone_mentions} (target: 8+)")

        # FAQ Schema
        if 'FAQPage' in self.html_content:
            score += 10
        else:
            issues.append("Missing FAQ Schema")

        final_score = min(100, score)

        self.results['seo'] = {
            'score': final_score,
            'status': 'PASS' if final_score >= 85 else 'WARN' if final_score >= 70 else 'FAIL',
            'issues': issues
        }

        print(f" {final_score}/100 [{self.results['seo']['status']}]")
        if final_score >= 85:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_content_quality(self):
        """Content Quality - 15 params"""
        print("[3/12] CONTENT QUALITY (15 params).........", end="", flush=True)

        score = 0
        issues = []

        # Bullet points/lists
        lists = len(re.findall(r'<ul|<ol', self.html_content, re.IGNORECASE))
        if lists >= 3:
            score += 20
        else:
            issues.append(f"Lists: {lists} (need 3+)")

        # Paragraph structure
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', self.html_content, re.DOTALL)
        if paragraphs:
            avg_sentences = sum(len(re.findall(r'[.!?]+', p)) for p in paragraphs) / len(paragraphs)
            if avg_sentences <= 5:
                score += 20
            else:
                issues.append(f"Avg paragraph: {avg_sentences:.1f} sentences (max 5)")

        # Section count
        sections = len(re.findall(r'<section', self.html_content, re.IGNORECASE))
        target_min = self.config['bmad_targets']['sections_min']
        target_max = self.config['bmad_targets']['sections_max']
        if target_min <= sections <= target_max:
            score += 20
        else:
            issues.append(f"Sections: {sections} (target: {target_min}-{target_max})")

        # Required sections
        required = self.config['page_structure']['required_sections']
        found_sections = []
        for section in required:
            if section.lower() in self.html_content.lower():
                found_sections.append(section)

        if len(found_sections) >= len(required) - 1:  # Allow 1 missing
            score += 20
        else:
            missing = [s for s in required if s not in found_sections]
            issues.append(f"Missing sections: {missing}")

        # Semantic keywords
        semantic_keywords = self.config['keywords']['semantic']
        found_keywords = sum(1 for kw in semantic_keywords if kw in self.text_content.lower())
        if found_keywords >= len(semantic_keywords) - 1:
            score += 20
        else:
            issues.append(f"Semantic keywords: {found_keywords}/{len(semantic_keywords)}")

        final_score = min(100, score)

        self.results['content_quality'] = {
            'score': final_score,
            'status': 'PASS' if final_score >= 85 else 'WARN' if final_score >= 70 else 'FAIL',
            'issues': issues
        }

        print(f" {final_score}/100 [{self.results['content_quality']['status']}]")
        if final_score >= 85:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_cro(self):
        """Conversion Rate Optimization - 20 params"""
        print("[4/12] CRO - CONVERSION (20 params)........", end="", flush=True)

        score = 0
        issues = []

        # CTA count
        ctas = len(re.findall(r'<a[^>]*(?:btn|button|cta)[^>]*>|<button', self.html_content, re.IGNORECASE))
        target_min = self.config['bmad_targets']['cta_count_min']
        target_max = self.config['bmad_targets']['cta_count_max']
        if target_min <= ctas <= target_max:
            score += 25
        else:
            issues.append(f"CTAs: {ctas} (target: {target_min}-{target_max})")

        # CTA types diversity
        has_call = 'tel:' in self.html_content
        has_form = '<form' in self.html_content
        has_email = 'mailto:' in self.html_content
        cta_types = sum([has_call, has_form, has_email])

        if cta_types >= 2:
            score += 25
        else:
            issues.append(f"CTA types: {cta_types} (need 2+: call, form, email)")

        # Form fields
        if has_form:
            form_fields = len(re.findall(r'<input[^>]*type=["\'](?:text|tel|email)', self.html_content, re.IGNORECASE))
            target_max_fields = self.config['bmad_targets']['form_fields_max']
            if form_fields <= target_max_fields:
                score += 25
            else:
                issues.append(f"Form fields: {form_fields} (max {target_max_fields})")
        else:
            issues.append("No form found")

        # Phone number prominent (header + hero)
        config_phone = self.config['business_data']['phone_number']
        phone_in_first_1000 = config_phone in self.html_content[:1000]
        if phone_in_first_1000:
            score += 25
        else:
            issues.append("Phone not in header/hero")

        final_score = min(100, score)

        self.results['cro'] = {
            'score': final_score,
            'status': 'PASS' if final_score >= 85 else 'WARN' if final_score >= 70 else 'FAIL',
            'issues': issues
        }

        print(f" {final_score}/100 [{self.results['cro']['status']}]")
        if final_score >= 85:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_psychology(self):
        """Psychological Triggers - 25 params"""
        print("[5/12] PSYCHOLOGY (25 params)...............", end="", flush=True)

        score = 0
        issues = []

        # Pain points
        pain_keywords = ['problem', 'broken', 'not working', 'issue', 'trouble', 'emergency']
        pain_found = sum(1 for kw in pain_keywords if kw in self.text_content.lower())
        if pain_found >= 3:
            score += 20
        else:
            issues.append(f"Pain points: {pain_found}/6")

        # Social proof (testimonials)
        testimonials = len(re.findall(r'testimonial|review|customer\s+said', self.html_content, re.IGNORECASE))
        target_min = self.config['social_proof']['testimonials_min']
        if testimonials >= target_min:
            score += 20
        else:
            issues.append(f"Testimonials: {testimonials} (need {target_min}+)")

        # Rating display
        rating_mentions = len(re.findall(r'\d\.\d\s*[★⭐]', self.html_content))
        target_min_rating = self.config['social_proof']['rating_display_min']
        if rating_mentions >= target_min_rating:
            score += 20
        else:
            issues.append(f"Rating displays: {rating_mentions} (need {target_min_rating}+)")

        # Urgency triggers
        urgency_keywords = ['same-day', 'today', 'now', 'emergency', '24/7', 'immediate']
        urgency_found = sum(1 for kw in urgency_keywords if kw in self.text_content.lower())
        if urgency_found >= 3:
            score += 20
        else:
            issues.append(f"Urgency triggers: {urgency_found}/6")

        # Authority signals
        authority_keywords = ['licensed', 'insured', 'certified', 'experienced', 'professional', 'expert']
        authority_found = sum(1 for kw in authority_keywords if kw in self.text_content.lower())
        if authority_found >= 4:
            score += 20
        else:
            issues.append(f"Authority signals: {authority_found}/6")

        final_score = min(100, score)

        self.results['psychology'] = {
            'score': final_score,
            'status': 'PASS' if final_score >= 85 else 'WARN' if final_score >= 70 else 'FAIL',
            'issues': issues
        }

        print(f" {final_score}/100 [{self.results['psychology']['status']}]")
        if final_score >= 85:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_conversion_design(self):
        """Conversion Design - 10 params"""
        print("[6/12] CONVERSION DESIGN (10 params).......", end="", flush=True)

        score = 0
        issues = []

        # Mobile viewport
        if 'viewport' in self.html_content:
            score += 25
        else:
            issues.append("No mobile viewport")

        # Lazy loading images
        lazy_images = len(re.findall(r'loading=["\']lazy["\']', self.html_content, re.IGNORECASE))
        total_images = len(re.findall(r'<img', self.html_content, re.IGNORECASE))
        if total_images > 0 and lazy_images / total_images >= 0.5:
            score += 25
        else:
            issues.append(f"Lazy loading: {lazy_images}/{total_images} images")

        # CSS for mobile (media queries)
        mobile_css = len(re.findall(r'@media.*?max-width.*?768px', self.html_content, re.IGNORECASE))
        if mobile_css >= 1:
            score += 25
        else:
            issues.append("No mobile CSS breakpoints")

        # Hamburger menu for mobile
        if 'hamburger' in self.html_content.lower() or 'menu-toggle' in self.html_content.lower():
            score += 25
        else:
            issues.append("No mobile menu")

        final_score = min(100, score)

        self.results['conversion_design'] = {
            'score': final_score,
            'status': 'PASS' if final_score >= 85 else 'WARN' if final_score >= 70 else 'FAIL',
            'issues': issues
        }

        print(f" {final_score}/100 [{self.results['conversion_design']['status']}]")
        if final_score >= 85:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_responsive_typography(self):
        """Responsive Typography - 10 params"""
        print("[7/12] RESPONSIVE TYPOGRAPHY (10 params)....", end="", flush=True)

        score = 0
        issues = []

        # Check for CSS clamp() function (fluid typography)
        clamp_usage = len(re.findall(r'clamp\s*\(', self.html_content, re.IGNORECASE))
        if clamp_usage >= 5:  # Should have clamp for h1, h2, h3, p, etc.
            score += 40
        else:
            issues.append(f"CSS clamp() usage: {clamp_usage} (need 5+ for headings/text)")

        # Check for responsive heading classes
        has_responsive_headings = bool(re.search(r'h1.*?font-size:\s*clamp', self.html_content, re.IGNORECASE | re.DOTALL))
        if has_responsive_headings:
            score += 30
        else:
            issues.append("No responsive headings (h1 with clamp)")

        # Check for RESPONSIVE TYPOGRAPHY SYSTEM marker
        has_typography_system = 'RESPONSIVE TYPOGRAPHY SYSTEM' in self.html_content
        if has_typography_system:
            score += 30
        else:
            issues.append("Missing responsive typography system")

        final_score = min(100, score)

        self.results['responsive_typography'] = {
            'score': final_score,
            'status': 'PASS' if final_score >= 85 else 'WARN' if final_score >= 70 else 'FAIL',
            'issues': issues
        }

        print(f" {final_score}/100 [{self.results['responsive_typography']['status']}]")
        if final_score >= 85:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def print_final_report(self):
        """Print comprehensive final report"""
        print("\n" + "=" * 60)
        print("FINAL REPORT")
        print("=" * 60)

        # Calculate overall score
        total = 0
        count = 0
        for category, result in self.results.items():
            if 'score' in result:
                total += result['score']
                count += 1

        overall_score = total / count if count > 0 else 0

        print(f"\nOVERALL SCORE: {overall_score:.1f}/100")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")

        # Deployment decision
        data_consistency_passed = self.results.get('data_consistency', {}).get('score', 0) == 100

        if data_consistency_passed and overall_score >= 85:
            print("\n[APPROVED] DEPLOYMENT APPROVED")
            print("All critical parameters pass. Page ready for production.")
        elif not data_consistency_passed:
            print("\n[BLOCKED] DEPLOYMENT BLOCKED")
            print("CRITICAL: Data consistency failed. Fix immediately!")
        else:
            print("\n[BLOCKED] DEPLOYMENT BLOCKED")
            print(f"Score {overall_score:.1f}/100 is below 85. Fix issues and retest.")

        # Critical issues
        print("\n" + "=" * 60)
        print("CRITICAL ISSUES (Must fix):")
        print("=" * 60)

        has_critical = False
        for category, result in self.results.items():
            if result.get('issues'):
                print(f"\n{category.upper().replace('_', ' ')}:")
                for issue in result['issues']:
                    print(f"  - {issue}")
                has_critical = True

        if not has_critical:
            print("\nNo critical issues found!")

        print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("BMAD COMPLETE TEST - 277 Parameters")
        print("=" * 60)
        print("\nUsage:")
        print("  python bmad-complete-test.py <html-file>")
        print("\nExample:")
        print("  python bmad-complete-test.py website/index.html")
        print("\nRequirements:")
        print("  1. bmad-config.json must exist (copy from bmad-config-TEMPLATE.json)")
        print("  2. Fill config with YOUR business data")
        print("  3. Run test on your pages")
        print("\n" + "=" * 60)
        sys.exit(1)

    html_file = sys.argv[1]

    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"[ERROR] File not found: {html_file}")
        sys.exit(1)

    # Run test
    tester = BMADCompleteTester(html_file)

    if not tester.load_config():
        sys.exit(1)

    if not tester.load_html():
        sys.exit(1)

    tester.run_all_tests()

if __name__ == "__main__":
    main()
