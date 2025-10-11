#!/usr/bin/env python3
"""
BMAD V2 - TIER 7: CONTENT FEATURES (30 params)
Tests advanced content elements and media
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup


class Tier7Tester:
    """Test Content Features (params 184-213)"""

    def __init__(self, html_file, config_file):
        self.html_file = Path(html_file)
        self.config_file = Path(config_file)
        self.html_content = ""
        self.soup = None
        self.config = {}
        self.score = 0
        self.total_tests = 30
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"[ERROR] Loading config: {e}")
            return False

    def load_html(self):
        """Load and parse HTML"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            return True
        except Exception as e:
            print(f"[ERROR] Loading HTML: {e}")
            return False

    def test_video_tutorials(self):
        """184. Video tutorials/how-tos"""
        has_video = any([
            '<video' in self.html_content.lower(),
            'youtube.com' in self.html_content.lower(),
            'vimeo.com' in self.html_content.lower(),
            'tutorial' in self.html_content.lower() and 'video' in self.html_content.lower()
        ])

        if has_video:
            print("[PASS] 184. Video tutorials")
            self.passed += 1
        else:
            print("[WARN] 184. Video tutorials")
            print("   >> No video content")
            self.warnings += 1

    def test_video_testimonials(self):
        """185. Video testimonials"""
        has_video_testimonial = 'testimonial' in self.html_content.lower() and ('video' in self.html_content.lower() or 'youtube' in self.html_content.lower())

        if has_video_testimonial:
            print("[PASS] 185. Video testimonials")
            self.passed += 1
        else:
            print("[WARN] 185. Video testimonials")
            print("   >> Optional feature")
            self.warnings += 1

    def test_before_after_gallery(self):
        """186. Before/after galleries"""
        has_before_after = any([
            'before' in self.html_content.lower() and 'after' in self.html_content.lower() and 'gallery' in self.html_content.lower(),
            'before-after' in self.html_content.lower(),
            'transformation' in self.html_content.lower()
        ])

        if has_before_after:
            print("[PASS] 186. Before/after galleries")
            self.passed += 1
        else:
            print("[WARN] 186. Before/after galleries")
            print("   >> No visual proof")
            self.warnings += 1

    def test_photo_galleries(self):
        """187. Photo galleries"""
        images = self.soup.find_all('img')
        has_gallery = any([
            'gallery' in self.html_content.lower(),
            'slideshow' in self.html_content.lower(),
            'carousel' in self.html_content.lower(),
            len(images) >= 5
        ])

        if has_gallery:
            print(f"[PASS] 187. Photo galleries ({len(images)} images)")
            self.passed += 1
        else:
            print("[WARN] 187. Photo galleries")
            print(f"   >> Only {len(images)} images")
            self.warnings += 1

    def test_image_optimization(self):
        """188. Image format optimization (WebP, AVIF)"""
        has_modern_format = any([
            '.webp' in self.html_content.lower(),
            '.avif' in self.html_content.lower(),
            'image/webp' in self.html_content.lower()
        ])

        if has_modern_format:
            print("[PASS] 188. Image optimization")
            self.passed += 1
        else:
            print("[WARN] 188. Image optimization")
            print("   >> No WebP/AVIF format")
            self.warnings += 1

    def test_image_lazy_loading(self):
        """189. Image lazy loading"""
        images = self.soup.find_all('img')
        lazy_images = [img for img in images if img.get('loading') == 'lazy']

        if len(lazy_images) > 0:
            print(f"[PASS] 189. Image lazy loading {len(lazy_images)}/{len(images)}")
            self.passed += 1
        else:
            print("[FAIL] 189. Image lazy loading")
            print("   >> No lazy loading")
            self.failed += 1

    def test_image_captions(self):
        """190. Image captions/descriptions"""
        has_captions = any([
            '<figcaption' in self.html_content.lower(),
            'caption' in self.html_content.lower() and 'image' in self.html_content.lower()
        ])

        if has_captions:
            print("[PASS] 190. Image captions")
            self.passed += 1
        else:
            print("[WARN] 190. Image captions")
            print("   >> No captions found")
            self.warnings += 1

    def test_alt_text_quality(self):
        """191. Alt text quality"""
        images = self.soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]
        good_alt = [img for img in images_with_alt if len(img.get('alt', '')) > 10]

        if len(good_alt) >= len(images) * 0.8:
            print(f"[PASS] 191. Alt text quality {len(good_alt)}/{len(images)}")
            self.passed += 1
        else:
            print(f"[FAIL] 191. Alt text quality {len(good_alt)}/{len(images)}")
            print("   >> Insufficient alt text")
            self.failed += 1

    def test_infographics(self):
        """192. Infographics"""
        has_infographic = any([
            'infographic' in self.html_content.lower(),
            'data visualization' in self.html_content.lower(),
            'chart' in self.html_content.lower()
        ])

        if has_infographic:
            print("[PASS] 192. Infographics")
            self.passed += 1
        else:
            print("[WARN] 192. Infographics")
            print("   >> Optional feature")
            self.warnings += 1

    def test_downloadable_guides(self):
        """193. Downloadable guides/resources"""
        has_download = any([
            'download' in self.html_content.lower() and ('guide' in self.html_content.lower() or 'pdf' in self.html_content.lower()),
            '.pdf' in self.html_content.lower() and 'download' in self.html_content.lower()
        ])

        if has_download:
            print("[PASS] 193. Downloadable guides")
            self.passed += 1
        else:
            print("[WARN] 193. Downloadable guides")
            print("   >> No downloadable content")
            self.warnings += 1

    def test_pdf_resources(self):
        """194. PDF resources"""
        has_pdf = '.pdf' in self.html_content.lower()

        if has_pdf:
            print("[PASS] 194. PDF resources")
            self.passed += 1
        else:
            print("[WARN] 194. PDF resources")
            print("   >> No PDF files")
            self.warnings += 1

    def test_checklists(self):
        """195. Checklists"""
        has_checklist = any([
            'checklist' in self.html_content.lower(),
            'checkbox' in self.html_content.lower() and 'list' in self.html_content.lower(),
            'type="checkbox"' in self.html_content
        ])

        if has_checklist:
            print("[PASS] 195. Checklists")
            self.passed += 1
        else:
            print("[WARN] 195. Checklists")
            print("   >> No interactive checklists")
            self.warnings += 1

    def test_templates(self):
        """196. Templates/worksheets"""
        has_template = any([
            'template' in self.html_content.lower(),
            'worksheet' in self.html_content.lower(),
            'form' in self.html_content.lower() and 'download' in self.html_content.lower()
        ])

        if has_template:
            print("[PASS] 196. Templates")
            self.passed += 1
        else:
            print("[WARN] 196. Templates")
            print("   >> Optional feature")
            self.warnings += 1

    def test_case_studies(self):
        """197. Case studies"""
        has_case_study = any([
            'case study' in self.html_content.lower(),
            'case-study' in self.html_content.lower(),
            'success story' in self.html_content.lower()
        ])

        if has_case_study:
            print("[PASS] 197. Case studies")
            self.passed += 1
        else:
            print("[WARN] 197. Case studies")
            print("   >> No case studies")
            self.warnings += 1

    def test_customer_stories(self):
        """198. Customer success stories"""
        has_stories = any([
            'customer story' in self.html_content.lower(),
            'testimonial' in self.html_content.lower(),
            'review' in self.html_content.lower() and 'customer' in self.html_content.lower()
        ])

        if has_stories:
            print("[PASS] 198. Customer stories")
            self.passed += 1
        else:
            print("[WARN] 198. Customer stories")
            print("   >> Limited social proof")
            self.warnings += 1

    def test_review_display(self):
        """199. Customer reviews displayed"""
        has_reviews = any([
            'review' in self.html_content.lower(),
            'rating' in self.html_content.lower(),
            'testimonial' in self.html_content.lower()
        ])

        review_count = self.html_content.lower().count('review')
        if has_reviews and review_count >= 3:
            print(f"[PASS] 199. Review display ({review_count} mentions)")
            self.passed += 1
        else:
            print("[FAIL] 199. Review display")
            print("   >> Insufficient reviews shown")
            self.failed += 1

    def test_review_schema(self):
        """200. Review schema markup"""
        has_review_schema = any([
            'schema.org/Review' in self.html_content,
            'AggregateRating' in self.html_content,
            'reviewRating' in self.html_content
        ])

        if has_review_schema:
            print("[PASS] 200. Review schema")
            self.passed += 1
        else:
            print("[FAIL] 200. Review schema")
            print("   >> Missing review structured data")
            self.failed += 1

    def test_review_filtering(self):
        """201. Review filtering/sorting"""
        has_filter = any([
            'filter' in self.html_content.lower() and 'review' in self.html_content.lower(),
            'sort' in self.html_content.lower() and 'review' in self.html_content.lower()
        ])

        if has_filter:
            print("[PASS] 201. Review filtering")
            self.passed += 1
        else:
            print("[WARN] 201. Review filtering")
            print("   >> Optional for simple sites")
            self.warnings += 1

    def test_review_pagination(self):
        """202. Review pagination"""
        has_pagination = any([
            'pagination' in self.html_content.lower(),
            'load more' in self.html_content.lower(),
            'show more' in self.html_content.lower()
        ])

        if has_pagination:
            print("[PASS] 202. Review pagination")
            self.passed += 1
        else:
            print("[WARN] 202. Review pagination")
            print("   >> Optional feature")
            self.warnings += 1

    def test_video_reviews(self):
        """203. Video reviews/testimonials"""
        has_video_review = 'video' in self.html_content.lower() and ('review' in self.html_content.lower() or 'testimonial' in self.html_content.lower())

        if has_video_review:
            print("[PASS] 203. Video reviews")
            self.passed += 1
        else:
            print("[WARN] 203. Video reviews")
            print("   >> Optional feature")
            self.warnings += 1

    def test_photo_reviews(self):
        """204. Photo reviews from customers"""
        has_photo_review = any([
            'customer photo' in self.html_content.lower(),
            'photo review' in self.html_content.lower(),
            'gallery' in self.html_content.lower() and 'customer' in self.html_content.lower()
        ])

        if has_photo_review:
            print("[PASS] 204. Photo reviews")
            self.passed += 1
        else:
            print("[WARN] 204. Photo reviews")
            print("   >> No customer photos")
            self.warnings += 1

    def test_cost_calculator(self):
        """205. Cost/pricing calculators"""
        has_calculator = any([
            'calculator' in self.html_content.lower() and ('cost' in self.html_content.lower() or 'price' in self.html_content.lower()),
            'estimate' in self.html_content.lower() and 'calculate' in self.html_content.lower()
        ])

        if has_calculator:
            print("[PASS] 205. Cost calculator")
            self.passed += 1
        else:
            print("[WARN] 205. Cost calculator")
            print("   >> No pricing calculator")
            self.warnings += 1

    def test_roi_calculator(self):
        """206. ROI/savings calculators"""
        has_roi = any([
            'roi' in self.html_content.lower() and 'calculator' in self.html_content.lower(),
            'savings' in self.html_content.lower() and 'calculator' in self.html_content.lower()
        ])

        if has_roi:
            print("[PASS] 206. ROI calculator")
            self.passed += 1
        else:
            print("[WARN] 206. ROI calculator")
            print("   >> Optional feature")
            self.warnings += 1

    def test_interactive_diagrams(self):
        """207. Interactive diagrams"""
        has_diagram = any([
            'diagram' in self.html_content.lower(),
            'svg' in self.html_content.lower() and 'interactive' in self.html_content.lower(),
            'canvas' in self.html_content.lower()
        ])

        if has_diagram:
            print("[PASS] 207. Interactive diagrams")
            self.passed += 1
        else:
            print("[WARN] 207. Interactive diagrams")
            print("   >> Optional feature")
            self.warnings += 1

    def test_embedded_tools(self):
        """208. Embedded tools/widgets"""
        has_embed = any([
            '<iframe' in self.html_content.lower(),
            'embed' in self.html_content.lower(),
            'widget' in self.html_content.lower()
        ])

        if has_embed:
            print("[PASS] 208. Embedded tools")
            self.passed += 1
        else:
            print("[WARN] 208. Embedded tools")
            print("   >> No embedded content")
            self.warnings += 1

    def test_pricing_tables(self):
        """209. Pricing comparison tables"""
        has_pricing = any([
            'pricing' in self.html_content.lower() and '<table' in self.html_content.lower(),
            'price' in self.html_content.lower() and 'package' in self.html_content.lower()
        ])

        if has_pricing:
            print("[PASS] 209. Pricing tables")
            self.passed += 1
        else:
            print("[WARN] 209. Pricing tables")
            print("   >> No pricing comparison")
            self.warnings += 1

    def test_package_comparison(self):
        """210. Service package comparisons"""
        has_comparison = any([
            'package' in self.html_content.lower() and 'compare' in self.html_content.lower(),
            'plan' in self.html_content.lower() and '<table' in self.html_content.lower()
        ])

        if has_comparison:
            print("[PASS] 210. Package comparison")
            self.passed += 1
        else:
            print("[WARN] 210. Package comparison")
            print("   >> Optional feature")
            self.warnings += 1

    def test_service_bundles(self):
        """211. Service bundle offers"""
        has_bundle = any([
            'bundle' in self.html_content.lower(),
            'package deal' in self.html_content.lower(),
            'combo' in self.html_content.lower()
        ])

        if has_bundle:
            print("[PASS] 211. Service bundles")
            self.passed += 1
        else:
            print("[WARN] 211. Service bundles")
            print("   >> No bundle offers")
            self.warnings += 1

    def test_seasonal_content(self):
        """212. Seasonal/timely content"""
        has_seasonal = any([
            'seasonal' in self.html_content.lower(),
            'winter' in self.html_content.lower() or 'summer' in self.html_content.lower(),
            'holiday' in self.html_content.lower()
        ])

        if has_seasonal:
            print("[PASS] 212. Seasonal content")
            self.passed += 1
        else:
            print("[WARN] 212. Seasonal content")
            print("   >> No seasonal offers")
            self.warnings += 1

    def test_blog_integration(self):
        """213. Blog/news integration"""
        has_blog = any([
            'blog' in self.html_content.lower(),
            'article' in self.html_content.lower() and 'date' in self.html_content.lower(),
            'news' in self.html_content.lower()
        ])

        if has_blog:
            print("[PASS] 213. Blog integration")
            self.passed += 1
        else:
            print("[WARN] 213. Blog integration")
            print("   >> No blog content")
            self.warnings += 1

    def test_all(self):
        """Run all Tier 7 tests"""
        print("\n" + "=" * 60)
        print("TIER 7: CONTENT FEATURES (30 params)")
        print("=" * 60)
        print()

        # Run all tests
        self.test_video_tutorials()
        self.test_video_testimonials()
        self.test_before_after_gallery()
        self.test_photo_galleries()
        self.test_image_optimization()
        self.test_image_lazy_loading()
        self.test_image_captions()
        self.test_alt_text_quality()
        self.test_infographics()
        self.test_downloadable_guides()
        self.test_pdf_resources()
        self.test_checklists()
        self.test_templates()
        self.test_case_studies()
        self.test_customer_stories()
        self.test_review_display()
        self.test_review_schema()
        self.test_review_filtering()
        self.test_review_pagination()
        self.test_video_reviews()
        self.test_photo_reviews()
        self.test_cost_calculator()
        self.test_roi_calculator()
        self.test_interactive_diagrams()
        self.test_embedded_tools()
        self.test_pricing_tables()
        self.test_package_comparison()
        self.test_service_bundles()
        self.test_seasonal_content()
        self.test_blog_integration()

        # Calculate score
        self.score = (self.passed / self.total_tests) * 100

        # Print summary
        print()
        print("=" * 60)
        print(f"TIER 7 SCORE: {self.score:.1f}/100")
        print("=" * 60)

        if self.score >= 50:
            print("[SUCCESS] TIER 7 PASSED (many features optional)")
        else:
            print("[INFO] TIER 7 - Consider adding content features")
        print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier7_content_features.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier7Tester(html_file, config_file)
    if tester.load_config() and tester.load_html():
        tester.test_all()
