#!/usr/bin/env python3
"""
BMAD V2 - TIER 2 HIGH PRIORITY TESTS
30 parameters: SEO Core (15) + CRO Essentials (15)
Target: 85% score
"""

import re
import json
from pathlib import Path

class Tier2Tester:
    """Test 30 high-priority parameters - SEO & CRO"""

    def __init__(self, html_file, config_file):
        self.html_file = html_file
        self.config_file = config_file
        self.html_content = ""
        self.text_content = ""
        self.config = {}
        self.results = []
        self.score = 0
        self.total_tests = 30

    def load_config(self):
        """Load business configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"[ERROR] Config load failed: {e}")
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

            return True
        except Exception as e:
            print(f"[ERROR] HTML load failed: {e}")
            return False

    def test_all(self):
        """Run all 30 Tier 2 tests"""
        print("\n" + "=" * 60)
        print("TIER 2: HIGH PRIORITY (30 params)")
        print("=" * 60)

        # SEO Core (15 params)
        self.test_word_count()           # 16
        self.test_keyword_density()      # 17
        self.test_title_tag()            # 18
        self.test_meta_description()     # 19
        self.test_heading_structure()    # 20
        self.test_internal_links()       # 21
        self.test_images()               # 22
        self.test_alt_text()             # 23
        self.test_faq_schema()           # 24
        self.test_breadcrumbs()          # 25
        self.test_structured_data()      # 26
        self.test_url_structure()        # 27
        self.test_canonical_tag()        # 28
        self.test_open_graph()           # 29
        self.test_twitter_cards()        # 30

        # CRO Essentials (15 params)
        self.test_cta_count()            # 31
        self.test_cta_diversity()        # 32
        self.test_form_fields()          # 33
        self.test_phone_prominence()     # 34
        self.test_trust_badges()         # 35
        self.test_social_proof()         # 36
        self.test_testimonials()         # 37
        self.test_rating_display()       # 38
        self.test_urgency_triggers()     # 39
        self.test_risk_reversal()        # 40
        self.test_value_proposition()    # 41
        self.test_benefits_vs_features() # 42
        self.test_price_transparency()   # 43
        self.test_contact_in_footer()    # 44
        self.test_sticky_header()        # 45

        # Calculate score
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        self.score = (passed / self.total_tests) * 100

        # Print summary
        self.print_summary()

        return self.score >= 85

    # SEO CORE TESTS (16-30)

    def test_word_count(self):
        """16. Word count: 1500-2500"""
        words = re.findall(r'\b\w+\b', self.text_content.lower())
        word_count = len(words)
        target_min = self.config['bmad_targets']['content_word_count_min']
        target_max = self.config['bmad_targets']['content_word_count_max']

        if target_min <= word_count <= target_max:
            self.results.append({'param': '16. Word count', 'status': 'PASS', 'value': word_count})
        else:
            self.results.append({'param': '16. Word count', 'status': 'FAIL',
                               'issue': f'{word_count} words (target: {target_min}-{target_max})'})

    def test_keyword_density(self):
        """17. Keyword density: 1.5-2.5%"""
        primary_keyword = self.config['keywords']['primary'].lower()
        words = re.findall(r'\b\w+\b', self.text_content.lower())
        word_count = len(words)

        keyword_count = self.text_content.lower().count(primary_keyword)
        keyword_density = (keyword_count * len(primary_keyword.split()) / word_count * 100) if word_count > 0 else 0

        target_min = self.config['bmad_targets']['keyword_density_min']
        target_max = self.config['bmad_targets']['keyword_density_max']

        if target_min <= keyword_density <= target_max:
            self.results.append({'param': '17. Keyword density', 'status': 'PASS', 'value': f'{keyword_density:.1f}%'})
        else:
            self.results.append({'param': '17. Keyword density', 'status': 'FAIL',
                               'issue': f'{keyword_density:.1f}% (target: {target_min}-{target_max}%)'})

    def test_title_tag(self):
        """18. Title tag optimized (50-60 chars)"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', self.html_content, re.IGNORECASE)

        if title_match:
            title = title_match.group(1).strip()
            title_len = len(title)

            if 50 <= title_len <= 60:
                self.results.append({'param': '18. Title tag', 'status': 'PASS', 'value': f'{title_len} chars'})
            else:
                self.results.append({'param': '18. Title tag', 'status': 'WARN',
                                   'issue': f'{title_len} chars (optimal: 50-60)'})
        else:
            self.results.append({'param': '18. Title tag', 'status': 'FAIL', 'issue': 'Missing title tag'})

    def test_meta_description(self):
        """19. Meta description (150-160 chars)"""
        meta_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', self.html_content, re.IGNORECASE)

        if meta_match:
            desc = meta_match.group(1).strip()
            desc_len = len(desc)

            if 150 <= desc_len <= 160:
                self.results.append({'param': '19. Meta description', 'status': 'PASS', 'value': f'{desc_len} chars'})
            else:
                self.results.append({'param': '19. Meta description', 'status': 'WARN',
                                   'issue': f'{desc_len} chars (optimal: 150-160)'})
        else:
            self.results.append({'param': '19. Meta description', 'status': 'FAIL', 'issue': 'Missing meta description'})

    def test_heading_structure(self):
        """20. H2-H6 heading structure"""
        h2_count = len(re.findall(r'<h2[^>]*>', self.html_content))
        h3_count = len(re.findall(r'<h3[^>]*>', self.html_content))

        if h2_count >= 3 and h3_count >= 2:
            self.results.append({'param': '20. Heading structure', 'status': 'PASS',
                               'value': f'{h2_count} H2s, {h3_count} H3s'})
        else:
            self.results.append({'param': '20. Heading structure', 'status': 'FAIL',
                               'issue': f'Only {h2_count} H2s, {h3_count} H3s (need 3+ H2s, 2+ H3s)'})

    def test_internal_links(self):
        """21. Internal links: 10+"""
        internal_links = len(re.findall(r'<a\s+[^>]*href=["\'](?:/|#|[^h])[^"\']*["\']', self.html_content))
        target = self.config['bmad_targets']['internal_links_min']

        if internal_links >= target:
            self.results.append({'param': '21. Internal links', 'status': 'PASS', 'value': internal_links})
        else:
            self.results.append({'param': '21. Internal links', 'status': 'FAIL',
                               'issue': f'{internal_links} links (need {target}+)'})

    def test_images(self):
        """22. Images: 10+"""
        visible_images = len(re.findall(r'<img[^>]*>', self.html_content))
        schema_images = len(re.findall(r'itemtype="https://schema\.org/ImageObject"', self.html_content))
        total_images = max(visible_images, schema_images)
        target = self.config['bmad_targets']['images_min']

        if total_images >= target:
            self.results.append({'param': '22. Images', 'status': 'PASS', 'value': total_images})
        else:
            self.results.append({'param': '22. Images', 'status': 'FAIL',
                               'issue': f'{total_images} images (need {target}+)'})

    def test_alt_text(self):
        """23. Alt text on all images"""
        all_imgs = re.findall(r'<img[^>]*>', self.html_content)
        imgs_with_alt = [img for img in all_imgs if 'alt=' in img]

        if len(all_imgs) == 0:
            self.results.append({'param': '23. Alt text', 'status': 'WARN', 'issue': 'No images found'})
        elif len(imgs_with_alt) == len(all_imgs):
            self.results.append({'param': '23. Alt text', 'status': 'PASS', 'value': 'All images have alt'})
        else:
            self.results.append({'param': '23. Alt text', 'status': 'FAIL',
                               'issue': f'{len(imgs_with_alt)}/{len(all_imgs)} images have alt text'})

    def test_faq_schema(self):
        """24. FAQPage schema"""
        if 'FAQPage' in self.html_content:
            self.results.append({'param': '24. FAQ schema', 'status': 'PASS', 'value': 'Present'})
        else:
            self.results.append({'param': '24. FAQ schema', 'status': 'FAIL', 'issue': 'Missing FAQPage schema'})

    def test_breadcrumbs(self):
        """25. Breadcrumb navigation"""
        if 'breadcrumb' in self.html_content.lower() or 'BreadcrumbList' in self.html_content:
            self.results.append({'param': '25. Breadcrumbs', 'status': 'PASS', 'value': 'Present'})
        else:
            self.results.append({'param': '25. Breadcrumbs', 'status': 'WARN', 'issue': 'No breadcrumbs found'})

    def test_structured_data(self):
        """26. Structured data: 3+ types"""
        schema_types = re.findall(r'"@type":\s*"([^"]+)"', self.html_content)
        unique_types = list(set(schema_types))

        if len(unique_types) >= 3:
            self.results.append({'param': '26. Structured data', 'status': 'PASS',
                               'value': f'{len(unique_types)} types'})
        else:
            self.results.append({'param': '26. Structured data', 'status': 'FAIL',
                               'issue': f'Only {len(unique_types)} schema types (need 3+)'})

    def test_url_structure(self):
        """27. URL structure (clean, descriptive)"""
        # Check if filename is descriptive (has hyphens, not numbers)
        filename = Path(self.html_file).stem

        if '-' in filename and not filename[0].isdigit():
            self.results.append({'param': '27. URL structure', 'status': 'PASS', 'value': 'Clean URL'})
        else:
            self.results.append({'param': '27. URL structure', 'status': 'WARN',
                               'issue': 'URL could be more descriptive'})

    def test_canonical_tag(self):
        """28. Canonical tag present"""
        if 'rel="canonical"' in self.html_content or 'rel=\'canonical\'' in self.html_content:
            self.results.append({'param': '28. Canonical tag', 'status': 'PASS', 'value': 'Present'})
        else:
            self.results.append({'param': '28. Canonical tag', 'status': 'WARN', 'issue': 'Missing canonical tag'})

    def test_open_graph(self):
        """29. Open Graph tags (Facebook)"""
        og_tags = len(re.findall(r'property=["\']og:', self.html_content))

        if og_tags >= 4:
            self.results.append({'param': '29. Open Graph', 'status': 'PASS', 'value': f'{og_tags} tags'})
        else:
            self.results.append({'param': '29. Open Graph', 'status': 'WARN',
                               'issue': f'Only {og_tags} OG tags (need 4+)'})

    def test_twitter_cards(self):
        """30. Twitter Card tags"""
        twitter_tags = len(re.findall(r'name=["\']twitter:', self.html_content))

        if twitter_tags >= 3:
            self.results.append({'param': '30. Twitter cards', 'status': 'PASS', 'value': f'{twitter_tags} tags'})
        else:
            self.results.append({'param': '30. Twitter cards', 'status': 'WARN',
                               'issue': f'Only {twitter_tags} Twitter tags (need 3+)'})

    # CRO ESSENTIALS TESTS (31-45)

    def test_cta_count(self):
        """31. CTA count: 3-8"""
        ctas = len(re.findall(r'<a[^>]*(?:btn|button|cta)[^>]*>|<button', self.html_content, re.IGNORECASE))
        target_min = self.config['bmad_targets']['cta_count_min']
        target_max = self.config['bmad_targets']['cta_count_max']

        if target_min <= ctas <= target_max:
            self.results.append({'param': '31. CTA count', 'status': 'PASS', 'value': ctas})
        else:
            self.results.append({'param': '31. CTA count', 'status': 'FAIL',
                               'issue': f'{ctas} CTAs (optimal: {target_min}-{target_max})'})

    def test_cta_diversity(self):
        """32. CTA diversity (call + form + email)"""
        has_call = 'tel:' in self.html_content
        has_form = '<form' in self.html_content
        has_email = 'mailto:' in self.html_content
        cta_types = sum([has_call, has_form, has_email])

        if cta_types >= 2:
            self.results.append({'param': '32. CTA diversity', 'status': 'PASS', 'value': f'{cta_types} types'})
        else:
            self.results.append({'param': '32. CTA diversity', 'status': 'FAIL',
                               'issue': f'Only {cta_types} CTA type(s) (need 2+: call, form, email)'})

    def test_form_fields(self):
        """33. Form fields: <=5"""
        form_fields = len(re.findall(r'<input[^>]*type=["\'](?:text|tel|email)', self.html_content, re.IGNORECASE))
        target_max = self.config['bmad_targets']['form_fields_max']

        if '<form' not in self.html_content:
            self.results.append({'param': '33. Form fields', 'status': 'WARN', 'issue': 'No form found'})
        elif form_fields <= target_max:
            self.results.append({'param': '33. Form fields', 'status': 'PASS', 'value': form_fields})
        else:
            self.results.append({'param': '33. Form fields', 'status': 'FAIL',
                               'issue': f'{form_fields} fields (max {target_max} for low friction)'})

    def test_phone_prominence(self):
        """34. Phone prominence (above fold)"""
        config_phone = self.config['business_data']['phone_number']

        if config_phone in self.html_content[:2000]:
            self.results.append({'param': '34. Phone prominence', 'status': 'PASS', 'value': 'Above fold'})
        else:
            self.results.append({'param': '34. Phone prominence', 'status': 'FAIL',
                               'issue': 'Phone not in header/hero'})

    def test_trust_badges(self):
        """35. Trust badges: 3+"""
        trust_keywords = ['licensed', 'insured', 'certified', 'warranty', 'guarantee', 'bonded', 'approved']
        found_badges = sum(1 for kw in trust_keywords if kw in self.text_content.lower())
        target = self.config['social_proof']['trust_badges_min']

        if found_badges >= target:
            self.results.append({'param': '35. Trust badges', 'status': 'PASS', 'value': found_badges})
        else:
            self.results.append({'param': '35. Trust badges', 'status': 'FAIL',
                               'issue': f'{found_badges} badges (need {target}+)'})

    def test_social_proof(self):
        """36. Social proof visible"""
        has_reviews = 'review' in self.text_content.lower()
        has_testimonials = 'testimonial' in self.text_content.lower()
        has_rating = bool(re.search(r'\d\.\d\s*star', self.html_content))

        social_proof_count = sum([has_reviews, has_testimonials, has_rating])

        if social_proof_count >= 2:
            self.results.append({'param': '36. Social proof', 'status': 'PASS', 'value': 'Visible'})
        else:
            self.results.append({'param': '36. Social proof', 'status': 'FAIL',
                               'issue': 'Need more social proof (reviews, testimonials, ratings)'})

    def test_testimonials(self):
        """37. Testimonials: 3+"""
        testimonials = len(re.findall(r'testimonial|review|customer\s+said', self.html_content, re.IGNORECASE))
        target = self.config['social_proof']['testimonials_min']

        if testimonials >= target:
            self.results.append({'param': '37. Testimonials', 'status': 'PASS', 'value': testimonials})
        else:
            self.results.append({'param': '37. Testimonials', 'status': 'FAIL',
                               'issue': f'{testimonials} testimonials (need {target}+)'})

    def test_rating_display(self):
        """38. Rating display: 3+ instances"""
        rating_mentions = len(re.findall(r'\d\.\d\s*star', self.html_content))
        target = self.config['social_proof']['rating_display_min']

        if rating_mentions >= target:
            self.results.append({'param': '38. Rating display', 'status': 'PASS', 'value': rating_mentions})
        else:
            self.results.append({'param': '38. Rating display', 'status': 'FAIL',
                               'issue': f'{rating_mentions} displays (need {target}+)'})

    def test_urgency_triggers(self):
        """39. Urgency triggers: 3+"""
        urgency_keywords = ['same-day', 'today', 'now', 'emergency', '24/7', 'immediate', 'fast', 'quick']
        found_urgency = sum(1 for kw in urgency_keywords if kw in self.text_content.lower())

        if found_urgency >= 3:
            self.results.append({'param': '39. Urgency triggers', 'status': 'PASS', 'value': found_urgency})
        else:
            self.results.append({'param': '39. Urgency triggers', 'status': 'FAIL',
                               'issue': f'{found_urgency} triggers (need 3+)'})

    def test_risk_reversal(self):
        """40. Risk reversal (warranty visible)"""
        warranty_pattern = r'\d+[-\s]?(?:day|month|year)s?\s+warranty'

        if re.search(warranty_pattern, self.html_content, re.IGNORECASE):
            self.results.append({'param': '40. Risk reversal', 'status': 'PASS', 'value': 'Warranty visible'})
        else:
            self.results.append({'param': '40. Risk reversal', 'status': 'WARN', 'issue': 'Warranty not prominent'})

    def test_value_proposition(self):
        """41. Clear value proposition in hero"""
        # Check for value keywords in first 1500 chars (hero section)
        hero = self.html_content[:1500]
        value_keywords = ['expert', 'professional', 'reliable', 'trusted', 'quality', 'best', 'affordable']
        found_value = sum(1 for kw in value_keywords if kw in hero.lower())

        if found_value >= 2:
            self.results.append({'param': '41. Value proposition', 'status': 'PASS', 'value': 'Clear in hero'})
        else:
            self.results.append({'param': '41. Value proposition', 'status': 'WARN',
                               'issue': 'Value prop not clear in hero'})

    def test_benefits_vs_features(self):
        """42. Benefits vs features (benefit-led)"""
        # Look for benefit words (you, your) vs feature words (we, our)
        benefit_count = len(re.findall(r'\b(you|your)\b', self.text_content.lower()))
        feature_count = len(re.findall(r'\b(we|our)\b', self.text_content.lower()))

        if benefit_count > feature_count:
            self.results.append({'param': '42. Benefits vs features', 'status': 'PASS',
                               'value': 'Benefit-led'})
        else:
            self.results.append({'param': '42. Benefits vs features', 'status': 'WARN',
                               'issue': 'Too feature-focused, not enough benefit language'})

    def test_price_transparency(self):
        """43. Price transparency or 'free quote'"""
        has_pricing = bool(re.search(r'\$\d+', self.html_content))
        has_free_quote = 'free quote' in self.text_content.lower() or 'free estimate' in self.text_content.lower()

        if has_pricing or has_free_quote:
            self.results.append({'param': '43. Price transparency', 'status': 'PASS', 'value': 'Present'})
        else:
            self.results.append({'param': '43. Price transparency', 'status': 'WARN',
                               'issue': 'No pricing or free quote mention'})

    def test_contact_in_footer(self):
        """44. Contact info in footer"""
        # Check last 2000 chars for contact info
        footer = self.html_content[-2000:]
        config_phone = self.config['business_data']['phone_number']

        if config_phone in footer:
            self.results.append({'param': '44. Contact in footer', 'status': 'PASS', 'value': 'Present'})
        else:
            self.results.append({'param': '44. Contact in footer', 'status': 'WARN',
                               'issue': 'Contact info not in footer'})

    def test_sticky_header(self):
        """45. Sticky header on scroll"""
        has_sticky = bool(re.search(r'position:\s*(?:fixed|sticky)', self.html_content, re.IGNORECASE))
        has_sticky_class = 'sticky' in self.html_content.lower()

        if has_sticky or has_sticky_class:
            self.results.append({'param': '45. Sticky header', 'status': 'PASS', 'value': 'Implemented'})
        else:
            self.results.append({'param': '45. Sticky header', 'status': 'WARN',
                               'issue': 'No sticky header detected'})

    def print_summary(self):
        """Print test summary"""
        print("\n" + "-" * 60)
        print("TEST RESULTS:")
        print("-" * 60)

        for result in self.results:
            if result['status'] == 'PASS':
                status_icon = "[PASS]"
                value = result.get('value', '')
                print(f"{status_icon} {result['param']} ({value})")
            else:
                status_icon = "[FAIL]" if result['status'] == 'FAIL' else "[WARN]"
                print(f"{status_icon} {result['param']}")
                if result.get('issue'):
                    print(f"   >> {result['issue']}")

        print("\n" + "=" * 60)
        print(f"TIER 2 SCORE: {self.score:.1f}/100")
        print("=" * 60)

        if self.score >= 85:
            print("[SUCCESS] TIER 2 PASSED - Ready for Tier 3")
        elif self.score >= 70:
            print("[WARNING] TIER 2 needs improvement")
        else:
            print("[FAIL] TIER 2 needs major improvements")

        print("=" * 60)

    def get_fixes_needed(self):
        """Return list of parameters that need fixing"""
        return [r for r in self.results if r['status'] in ['FAIL', 'WARN']]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier2_high_priority.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier2Tester(html_file, config_file)

    if not tester.load_config():
        sys.exit(1)

    if not tester.load_html():
        sys.exit(1)

    passed = tester.test_all()

    sys.exit(0 if passed else 1)
