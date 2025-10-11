#!/usr/bin/env python3
"""
Full BMAD Mass Test - All Pages with Playwright Screenshots
Tests all 62 pages with comprehensive BMAD scoring
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

class FullBMADTester:
    def __init__(self, html_file):
        self.html_file = html_file
        self.html_content = ""
        self.text_content = ""
        self.score = 0
        self.issues = []

    def load_html(self):
        with open(self.html_file, 'r', encoding='utf-8') as f:
            self.html_content = f.read()

        # Extract visible text
        text = re.sub(r'<script[^>]*>.*?</script>', '', self.html_content, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        self.text_content = ' '.join(text.split())

    def test_all(self):
        """Run comprehensive BMAD test"""
        self.load_html()
        self.score = 100
        self.issues = []

        # 1. Word Count (target: 2500-3000)
        words = re.findall(r'\b\w+\b', self.text_content.lower())
        word_count = len(words)
        if not (2500 <= word_count <= 3000):
            self.score -= 5
            self.issues.append(f"Word count {word_count} not optimal (2500-3000)")

        # 2. Keyword Density (target: 2.0-2.5%)
        keyword_count = self.text_content.lower().count('appliance repair')
        keyword_density = (keyword_count * 2 / word_count * 100) if word_count > 0 else 0
        if not (2.0 <= keyword_density <= 2.5):
            self.score -= 5
            if keyword_density > 3.0:
                self.issues.append(f"Keyword density {keyword_density:.2f}% too high (over-optimization)")
            else:
                self.issues.append(f"Keyword density {keyword_density:.2f}% (target: 2.0-2.5%)")

        # 3. H1 Tags (must be exactly 1)
        h1_count = len(re.findall(r'<h1[^>]*>', self.html_content))
        if h1_count != 1:
            self.score -= 10
            self.issues.append(f"H1 count {h1_count} (must be 1)")

        # 4. Internal Links (target: 10+)
        internal_links = len(re.findall(r'<a\s+[^>]*href=["\'](?:/|\.\.\/|#)[^"\']*["\']', self.html_content))
        if internal_links < 10:
            self.score -= 5
            self.issues.append(f"Internal links {internal_links} (need 10+)")

        # 5. Images (target: 5+)
        img_tags = len(re.findall(r'<img[^>]*>', self.html_content))
        svg_images = len(re.findall(r'<svg[^>]*role=["\']img["\'][^>]*>', self.html_content))
        total_images = img_tags + svg_images
        if total_images < 5:
            self.score -= 5
            self.issues.append(f"Images {total_images} (need 5+)")

        # 6. Schema Markup (need 2+ types)
        schema_types = set(re.findall(r'"@type":\s*"([^"]+)"', self.html_content))
        if len(schema_types) < 2:
            self.score -= 10
            self.issues.append(f"Schema types {len(schema_types)} (need 2+)")

        # 7. Phone Mentions (target: 8+)
        phone_mentions = self.html_content.count('437-747-6737') + self.html_content.count('4377476737')
        if phone_mentions < 8:
            self.score -= 5
            self.issues.append(f"Phone mentions {phone_mentions} (need 8+)")

        # 8. Meta Description (120-160 chars) - relaxed range
        meta_desc = re.search(r'<meta\s+[^>]*name=["\']description["\']\s+content=["\'](.*?)["\']', self.html_content)
        if not meta_desc:
            # Try reverse order: content then name
            meta_desc = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', self.html_content)

        if meta_desc:
            desc_len = len(meta_desc.group(1))
            if not (120 <= desc_len <= 160):
                self.score -= 3
                self.issues.append(f"Meta description {desc_len} chars (target: 120-160)")
        else:
            self.score -= 10
            self.issues.append("Missing meta description")

        # 9. Title Tag (50-60 chars)
        title = re.search(r'<title>(.*?)</title>', self.html_content)
        if title:
            title_len = len(title.group(1))
            if not (50 <= title_len <= 60):
                self.score -= 3
                self.issues.append(f"Title {title_len} chars (target: 50-60)")
        else:
            self.score -= 10
            self.issues.append("Missing title tag")

        # 10. CTA Buttons (need 3+)
        cta_buttons = len(re.findall(r'(Call|Book|Get|Contact|Schedule)', self.html_content, re.IGNORECASE))
        if cta_buttons < 3:
            self.score -= 5
            self.issues.append(f"CTA buttons {cta_buttons} (need 3+)")

        # 11. Trust Signals
        trust_signals = ['licensed', 'insured', 'warranty', 'certified', 'professional']
        trust_count = sum(1 for signal in trust_signals if signal in self.text_content.lower())
        if trust_count < 4:
            self.score -= 5
            self.issues.append(f"Trust signals {trust_count}/5")

        # 12. Lists/Bullets (need 3+)
        lists = len(re.findall(r'<ul|<ol', self.html_content, re.IGNORECASE))
        if lists < 3:
            self.score -= 3
            self.issues.append(f"Lists {lists} (need 3+)")

        # 13. Sections (6-12)
        sections = len(re.findall(r'<section', self.html_content, re.IGNORECASE))
        if not (6 <= sections <= 12):
            self.score -= 3
            self.issues.append(f"Sections {sections} (target: 6-12)")

        # 14. FAQ Schema
        if 'FAQPage' not in self.html_content and 'Question' not in self.html_content:
            self.score -= 5
            self.issues.append("Missing FAQ schema or questions")

        # 15. Mobile Viewport
        if 'viewport' not in self.html_content or 'width=device-width' not in self.html_content:
            self.score -= 10
            self.issues.append("Missing or incorrect mobile viewport")

        return {
            'score': max(0, self.score),
            'issues': self.issues,
            'word_count': word_count,
            'keyword_density': round(keyword_density, 2),
            'internal_links': internal_links,
            'images': total_images,
            'schema_types': len(schema_types),
            'phone_mentions': phone_mentions
        }

def main():
    base_dir = Path(__file__).parent.parent

    # All pages to test
    pages = []

    # Index
    pages.append(('main', 'index.html', base_dir / 'index.html'))

    # Services
    services_dir = base_dir / 'services'
    for f in sorted(services_dir.glob('*.html')):
        if f.name != 'index.html':
            pages.append(('services', f.name, f))

    # Locations
    locations_dir = base_dir / 'locations'
    for f in sorted(locations_dir.glob('*.html')):
        if f.name != 'index.html':
            pages.append(('locations', f.name, f))

    # Blogs
    blog_dir = base_dir / 'blog'
    for f in sorted(blog_dir.glob('*.html')):
        if f.name != 'index.html':
            pages.append(('blog', f.name, f))

    print("=" * 70)
    print("FULL BMAD MASS TEST - ALL PARAMETERS")
    print(f"Testing {len(pages)} pages")
    print("=" * 70)

    results = {}
    category_scores = {'services': [], 'locations': [], 'blog': [], 'main': []}

    for category, filename, filepath in pages:
        print(f"\nTesting: {category}/{filename}...", end="", flush=True)

        tester = FullBMADTester(filepath)
        result = tester.test_all()

        results[f"{category}/{filename}"] = result
        category_scores[category].append(result['score'])

        print(f" {result['score']}/100")

        if result['issues']:
            for issue in result['issues'][:3]:  # Show top 3 issues
                print(f"  - {issue}")

    # Calculate averages
    print("\n" + "=" * 70)
    print("SUMMARY BY CATEGORY")
    print("=" * 70)

    for category in ['main', 'services', 'locations', 'blog']:
        if category_scores[category]:
            avg = sum(category_scores[category]) / len(category_scores[category])
            print(f"{category.upper():12} {avg:.1f}/100 (n={len(category_scores[category])})")

    all_scores = [s for scores in category_scores.values() for s in scores]
    overall_avg = sum(all_scores) / len(all_scores)

    print(f"\nOVERALL:     {overall_avg:.1f}/100")
    print(f"Pages 85+:   {sum(1 for s in all_scores if s >= 85)}/{len(all_scores)}")
    print(f"Pages 70+:   {sum(1 for s in all_scores if s >= 70)}/{len(all_scores)}")

    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = base_dir / f"full_bmad_test_{timestamp}.json"

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'overall_average': round(overall_avg, 1),
            'category_averages': {cat: round(sum(scores)/len(scores), 1) if scores else 0
                                  for cat, scores in category_scores.items()},
            'pages': results
        }, f, indent=2)

    print(f"\nDetailed report: {report_file.name}")
    print("=" * 70)

if __name__ == '__main__':
    main()
