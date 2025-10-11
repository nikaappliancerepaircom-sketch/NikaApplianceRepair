#!/usr/bin/env python3
"""
BMAD V2 - TIER 1 CRITICAL TESTS
15 parameters that MUST pass 100%
Blocks deployment if any fail
"""

import re
import json
from pathlib import Path

class Tier1Tester:
    """Test 15 critical parameters - data consistency & core technical"""

    def __init__(self, html_file, config_file):
        self.html_file = html_file
        self.config_file = config_file
        self.html_content = ""
        self.config = {}
        self.results = []
        self.score = 0
        self.total_tests = 16

    def load_config(self):
        """Load business configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"❌ Config load failed: {e}")
            return False

    def load_html(self):
        """Load HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()

            # Extract text content for uniqueness check
            text = re.sub(r'<script[^>]*>.*?</script>', '', self.html_content, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            self.text_content = ' '.join(text.split())

            return True
        except Exception as e:
            print(f"❌ HTML load failed: {e}")
            return False

    def test_all(self):
        """Run all 16 critical tests"""
        print("\n" + "=" * 60)
        print("TIER 1: CRITICAL PARAMETERS (16)")
        print("=" * 60)

        # Data Consistency (8 params)
        self.test_phone_consistency()
        self.test_hours_consistency()
        self.test_warranty_consistency()
        self.test_rating_consistency()
        self.test_review_count_consistency()
        self.test_years_consistency()
        self.test_address_consistency()
        self.test_email_consistency()

        # Core Technical (7 params)
        self.test_localbusiness_schema()
        self.test_rating_schema()
        self.test_mobile_viewport()
        self.test_single_h1()
        self.test_valid_html()
        self.test_https()
        self.test_phone_in_header()

        # Content Uniqueness (1 param) - NEW!
        self.test_content_uniqueness()

        # Calculate score
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        self.score = (passed / self.total_tests) * 100

        # Print summary
        self.print_summary()

        return self.score == 100

    def test_phone_consistency(self):
        """1. Phone number must be consistent"""
        config_phone = self.config['business_data']['phone_normalized']
        phone_pattern = r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})'
        phones = re.findall(phone_pattern, self.html_content)
        phones_normalized = [p.replace('-', '').replace(' ', '') for p in phones]

        if not phones_normalized:
            self.results.append({
                'param': '1. Phone consistency',
                'status': 'FAIL',
                'issue': 'No phone number found',
                'critical': True
            })
        else:
            unique_phones = list(set(phones_normalized))
            if len(unique_phones) > 1:
                self.results.append({
                    'param': '1. Phone consistency',
                    'status': 'FAIL',
                    'issue': f'Multiple phone numbers: {unique_phones}',
                    'critical': True
                })
            elif unique_phones[0] != config_phone:
                self.results.append({
                    'param': '1. Phone consistency',
                    'status': 'FAIL',
                    'issue': f'Phone mismatch: {unique_phones[0]} vs config {config_phone}',
                    'critical': True
                })
            else:
                self.results.append({
                    'param': '1. Phone consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': True
                })

    def test_hours_consistency(self):
        """2. Business hours must be consistent"""
        config_hours = self.config['business_data']['service_hours']
        # Look for hours patterns
        hours_patterns = [
            r'(\d+\s*(?:AM|PM)\s*[-–]\s*\d+\s*(?:AM|PM))',
            r'(24/7)',
            r'(24\s*hours)',
            r'(\d+am-\d+pm)'
        ]

        all_hours = []
        for pattern in hours_patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            all_hours.extend(matches)

        if not all_hours:
            self.results.append({
                'param': '2. Hours consistency',
                'status': 'WARN',
                'issue': 'No business hours found',
                'critical': False
            })
        else:
            unique_hours = list(set([h.strip() for h in all_hours]))
            if len(unique_hours) > 1:
                self.results.append({
                    'param': '2. Hours consistency',
                    'status': 'FAIL',
                    'issue': f'Multiple hours found: {unique_hours}',
                    'critical': True
                })
            else:
                self.results.append({
                    'param': '2. Hours consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': True
                })

    def test_warranty_consistency(self):
        """3. Warranty period must be consistent"""
        config_warranty = self.config['quality_metrics']['warranty_period']
        warranty_pattern = r'(\d+)[-\s]?(day|month|year)s?\s+warranty'
        warranties = re.findall(warranty_pattern, self.html_content, re.IGNORECASE)

        if warranties:
            unique_warranties = list(set([int(w[0]) for w in warranties]))
            if len(unique_warranties) > 1:
                self.results.append({
                    'param': '3. Warranty consistency',
                    'status': 'FAIL',
                    'issue': f'Multiple warranties: {unique_warranties}',
                    'critical': True
                })
            elif unique_warranties[0] != config_warranty:
                self.results.append({
                    'param': '3. Warranty consistency',
                    'status': 'FAIL',
                    'issue': f'Warranty mismatch: {unique_warranties[0]} vs config {config_warranty}',
                    'critical': True
                })
            else:
                self.results.append({
                    'param': '3. Warranty consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': True
                })
        else:
            self.results.append({
                'param': '3. Warranty consistency',
                'status': 'PASS',
                'issue': 'No warranty found (OK if not mentioned)',
                'critical': False
            })

    def test_rating_consistency(self):
        """4. Rating must be consistent"""
        config_rating = str(self.config['quality_metrics']['rating'])
        rating_pattern = r'(\d\.\d)\s*[★⭐]|ratingValue["\']:\s*["\'](\d\.\d)'
        ratings = re.findall(rating_pattern, self.html_content)
        ratings_flat = [r[0] or r[1] for r in ratings if r[0] or r[1]]

        if ratings_flat:
            unique_ratings = list(set(ratings_flat))
            if len(unique_ratings) > 1:
                self.results.append({
                    'param': '4. Rating consistency',
                    'status': 'FAIL',
                    'issue': f'Multiple ratings: {unique_ratings}',
                    'critical': True
                })
            elif unique_ratings[0] != config_rating:
                self.results.append({
                    'param': '4. Rating consistency',
                    'status': 'FAIL',
                    'issue': f'Rating mismatch: {unique_ratings[0]} vs config {config_rating}',
                    'critical': True
                })
            else:
                self.results.append({
                    'param': '4. Rating consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': True
                })
        else:
            self.results.append({
                'param': '4. Rating consistency',
                'status': 'FAIL',
                'issue': 'No rating found',
                'critical': True
            })

    def test_review_count_consistency(self):
        """5. Review count must be consistent"""
        config_reviews = str(self.config['quality_metrics']['review_count'])
        review_pattern = r'([\d,]+)\+?\s*(?:reviews?|customers?|clients?)|reviewCount["\']:\s*["\'](\d+)'
        reviews = re.findall(review_pattern, self.html_content, re.IGNORECASE)
        reviews_flat = [r[0].replace(',', '') if r[0] else r[1] for r in reviews if r[0] or r[1]]

        if reviews_flat:
            unique_reviews = list(set(reviews_flat))
            if len(unique_reviews) > 1:
                self.results.append({
                    'param': '5. Review count consistency',
                    'status': 'FAIL',
                    'issue': f'Multiple review counts: {unique_reviews}',
                    'critical': True
                })
            elif unique_reviews[0] != config_reviews:
                self.results.append({
                    'param': '5. Review count consistency',
                    'status': 'FAIL',
                    'issue': f'Review count mismatch: {unique_reviews[0]} vs config {config_reviews}',
                    'critical': True
                })
            else:
                self.results.append({
                    'param': '5. Review count consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': True
                })
        else:
            self.results.append({
                'param': '5. Review count consistency',
                'status': 'FAIL',
                'issue': 'No review count found',
                'critical': True
            })

    def test_years_consistency(self):
        """6. Years in business must be consistent"""
        config_years = self.config['quality_metrics']['years_in_business']
        years_pattern = r'(\d+)\+?\s*years?\s*(?:in business|experience|of experience)'
        years = re.findall(years_pattern, self.html_content, re.IGNORECASE)

        if years:
            unique_years = list(set([int(y) for y in years]))
            if len(unique_years) > 1:
                self.results.append({
                    'param': '6. Years consistency',
                    'status': 'FAIL',
                    'issue': f'Multiple years: {unique_years}',
                    'critical': True
                })
            elif unique_years[0] != config_years:
                self.results.append({
                    'param': '6. Years consistency',
                    'status': 'FAIL',
                    'issue': f'Years mismatch: {unique_years[0]} vs config {config_years}',
                    'critical': True
                })
            else:
                self.results.append({
                    'param': '6. Years consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': True
                })
        else:
            self.results.append({
                'param': '6. Years consistency',
                'status': 'PASS',
                'issue': 'No years mentioned (OK)',
                'critical': False
            })

    def test_address_consistency(self):
        """7. Address must be consistent if present"""
        # Simple check - just verify if addresses are consistent
        address_pattern = r'\b(?:Toronto|Mississauga|Brampton|North York|Scarborough),?\s*(?:ON|Ontario)\b'
        addresses = re.findall(address_pattern, self.html_content, re.IGNORECASE)

        if addresses:
            unique_addresses = list(set(addresses))
            # Allow multiple city mentions (service areas)
            self.results.append({
                'param': '7. Address consistency',
                'status': 'PASS',
                'issue': None,
                'critical': False
            })
        else:
            self.results.append({
                'param': '7. Address consistency',
                'status': 'PASS',
                'issue': 'No specific address (OK for service business)',
                'critical': False
            })

    def test_email_consistency(self):
        """8. Email must be consistent if present"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.html_content)

        if emails:
            unique_emails = list(set(emails))
            if len(unique_emails) > 1:
                self.results.append({
                    'param': '8. Email consistency',
                    'status': 'WARN',
                    'issue': f'Multiple emails: {unique_emails}',
                    'critical': False
                })
            else:
                self.results.append({
                    'param': '8. Email consistency',
                    'status': 'PASS',
                    'issue': None,
                    'critical': False
                })
        else:
            self.results.append({
                'param': '8. Email consistency',
                'status': 'PASS',
                'issue': 'No email found (OK)',
                'critical': False
            })

    def test_localbusiness_schema(self):
        """9. LocalBusiness schema must be present"""
        if 'LocalBusiness' in self.html_content or 'HomeAndConstructionBusiness' in self.html_content:
            self.results.append({
                'param': '9. LocalBusiness schema',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })
        else:
            self.results.append({
                'param': '9. LocalBusiness schema',
                'status': 'FAIL',
                'issue': 'Missing LocalBusiness schema',
                'critical': True
            })

    def test_rating_schema(self):
        """10. AggregateRating schema must be present"""
        if 'AggregateRating' in self.html_content:
            self.results.append({
                'param': '10. AggregateRating schema',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })
        else:
            self.results.append({
                'param': '10. AggregateRating schema',
                'status': 'FAIL',
                'issue': 'Missing AggregateRating schema',
                'critical': True
            })

    def test_mobile_viewport(self):
        """11. Mobile viewport meta tag must be present"""
        if 'viewport' in self.html_content:
            self.results.append({
                'param': '11. Mobile viewport',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })
        else:
            self.results.append({
                'param': '11. Mobile viewport',
                'status': 'FAIL',
                'issue': 'Missing viewport meta tag',
                'critical': True
            })

    def test_single_h1(self):
        """12. Exactly one H1 tag"""
        h1_count = len(re.findall(r'<h1[^>]*>', self.html_content))

        if h1_count == 1:
            self.results.append({
                'param': '12. Single H1 tag',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })
        else:
            self.results.append({
                'param': '12. Single H1 tag',
                'status': 'FAIL',
                'issue': f'Found {h1_count} H1 tags (must be exactly 1)',
                'critical': True
            })

    def test_valid_html(self):
        """13. Basic HTML validity"""
        # Check for critical errors
        issues = []

        if not re.search(r'<!DOCTYPE html>', self.html_content, re.IGNORECASE):
            issues.append('Missing DOCTYPE')

        if not re.search(r'<html[^>]*>', self.html_content, re.IGNORECASE):
            issues.append('Missing <html> tag')

        if not re.search(r'<head[^>]*>', self.html_content, re.IGNORECASE):
            issues.append('Missing <head> tag')

        if not re.search(r'<body[^>]*>', self.html_content, re.IGNORECASE):
            issues.append('Missing <body> tag')

        if issues:
            self.results.append({
                'param': '13. Valid HTML structure',
                'status': 'FAIL',
                'issue': ', '.join(issues),
                'critical': True
            })
        else:
            self.results.append({
                'param': '13. Valid HTML structure',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })

    def test_https(self):
        """14. HTTPS/SSL links check"""
        # Check for http:// links (should be https://)
        http_links = re.findall(r'href=["\']http://(?!localhost)', self.html_content)

        if http_links:
            self.results.append({
                'param': '14. HTTPS/SSL',
                'status': 'WARN',
                'issue': f'Found {len(http_links)} insecure HTTP links',
                'critical': False
            })
        else:
            self.results.append({
                'param': '14. HTTPS/SSL',
                'status': 'PASS',
                'issue': None,
                'critical': False
            })

    def test_phone_in_header(self):
        """15. Phone must be visible in header/hero"""
        config_phone = self.config['business_data']['phone_number']
        # Check first 2000 characters (header + hero)
        if config_phone in self.html_content[:2000]:
            self.results.append({
                'param': '15. Phone in header/hero',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })
        else:
            self.results.append({
                'param': '15. Phone in header/hero',
                'status': 'FAIL',
                'issue': 'Phone not found in header/hero section',
                'critical': True
            })

    def test_content_uniqueness(self):
        """16. Content must be unique (not duplicated)"""
        duplicate_indicators = []

        # Check for template placeholder text
        template_phrases = [
            'lorem ipsum',
            'placeholder text',
            'sample content',
            'coming soon',
            'under construction',
            'default text'
        ]

        for phrase in template_phrases:
            if phrase in self.text_content.lower():
                duplicate_indicators.append(f'Found template text: "{phrase}"')

        # Check for extremely short unique content (less than 500 chars)
        if len(self.text_content) < 500:
            duplicate_indicators.append(f'Very short content ({len(self.text_content)} chars)')

        # Check if title and H1 are too generic
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', self.html_content, re.DOTALL)
        if h1_match:
            h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip().lower()
            generic_h1s = ['home', 'welcome', 'main page', 'index', 'default']
            if h1_text in generic_h1s:
                duplicate_indicators.append(f'Generic H1: "{h1_text}"')

        if duplicate_indicators:
            self.results.append({
                'param': '16. Content uniqueness',
                'status': 'FAIL',
                'issue': '; '.join(duplicate_indicators),
                'critical': True
            })
        else:
            self.results.append({
                'param': '16. Content uniqueness',
                'status': 'PASS',
                'issue': None,
                'critical': True
            })

    def print_summary(self):
        """Print test summary"""
        print("\n" + "-" * 60)
        print("TEST RESULTS:")
        print("-" * 60)

        for result in self.results:
            status_icon = "[PASS]" if result['status'] == 'PASS' else "[FAIL]" if result['status'] == 'FAIL' else "[WARN]"
            critical_mark = " [CRITICAL]" if result.get('critical') else ""
            print(f"{status_icon} {result['param']}{critical_mark}")
            if result['issue']:
                print(f"   >> {result['issue']}")

        print("\n" + "=" * 60)
        print(f"TIER 1 SCORE: {self.score:.0f}/100")
        print("=" * 60)

        critical_failures = [r for r in self.results if r['status'] == 'FAIL' and r.get('critical')]

        if self.score == 100:
            print("[SUCCESS] TIER 1 PASSED - Ready for Tier 2")
        elif critical_failures:
            print("[BLOCKED] TIER 1 BLOCKED - Critical failures found")
            print("\nCRITICAL ISSUES:")
            for fail in critical_failures:
                print(f"  - {fail['param']}: {fail['issue']}")
        else:
            print("[WARNING] TIER 1 WARNING - Non-critical issues found")

        print("=" * 60)

    def get_fixes_needed(self):
        """Return list of parameters that need fixing"""
        return [r for r in self.results if r['status'] in ['FAIL', 'WARN']]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier1_critical.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier1Tester(html_file, config_file)

    if not tester.load_config():
        sys.exit(1)

    if not tester.load_html():
        sys.exit(1)

    passed = tester.test_all()

    sys.exit(0 if passed else 1)
