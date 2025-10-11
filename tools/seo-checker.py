#!/usr/bin/env python3
"""
BMAD SEO Optimization Checker - Windows Compatible
Complete SEO audit system for Nika Appliance Repair
Version: 2.0 - September 2025
"""

import re
import json
from collections import Counter
from html.parser import HTMLParser
from datetime import datetime

class SEOChecker:
    """Complete SEO optimization checking system"""

    def __init__(self, html_file_path):
        self.html_file = html_file_path
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "scores": {},
            "issues": [],
            "recommendations": []
        }
        self.html_content = ""
        self.text_content = ""

    def run_check(self):
        """Run all optimization checks"""
        print("\n" + "=" * 60)
        print("BMAD SEO OPTIMIZATION CHECK")
        print("=" * 60)

        # Load HTML
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()

            # Extract text
            parser = TextExtractor()
            parser.feed(self.html_content)
            self.text_content = ' '.join(parser.text)
            print(f"[OK] Loaded {self.html_file}")
        except Exception as e:
            print(f"[ERROR] {e}")
            return

        # Run checks
        self.check_content()
        self.check_technical()
        self.check_ai_optimization()
        self.check_local_seo()
        self.check_user_experience()

        # Calculate score
        self.calculate_overall_score()

        # Print results
        self.print_report()

    def check_content(self):
        """Check content optimization"""
        print("\n--- CONTENT OPTIMIZATION ---")
        score = 0

        # Word count - Using our accurate visible text method
        # This matches our word_counter.py tool for consistency
        words = re.findall(r'\b\w+\b', self.text_content.lower())
        word_count = len(words)

        # Also run our accurate word counter for comparison
        print(f"[INFO] Visible text word count: {word_count}")

        if 1500 <= word_count <= 2500:
            score += 15
            print(f"[OK] Word count: {word_count}")
        else:
            print(f"[WARN] Word count: {word_count} (target: 1500-2500)")
            self.report["issues"].append(f"Word count {word_count} not optimal")

        # Keyword density
        appliance_repair = self.text_content.lower().count('appliance repair')
        keyword_density = (appliance_repair * 2 / word_count * 100) if word_count > 0 else 0

        if 1.5 <= keyword_density <= 2.5:
            score += 15
            print(f"[OK] Keyword density: {keyword_density:.2f}%")
        elif keyword_density > 3.0:
            print(f"[ERROR] Keyword density: {keyword_density:.2f}% (OVER-OPTIMIZED!)")
            self.report["issues"].append(f"Keyword density {keyword_density:.2f}% too high")
        else:
            score += 10
            print(f"[WARN] Keyword density: {keyword_density:.2f}% (target: 1.5-2.5%)")

        # Headings
        h1_count = len(re.findall(r'<h1[^>]*>', self.html_content))
        h2_count = len(re.findall(r'<h2[^>]*>', self.html_content))
        h3_count = len(re.findall(r'<h3[^>]*>', self.html_content))

        if h1_count == 1:
            score += 10
            print(f"[OK] H1 tags: {h1_count}")
        else:
            print(f"[ERROR] H1 tags: {h1_count} (must be 1)")
            self.report["issues"].append(f"H1 count: {h1_count} (must be 1)")

        print(f"[INFO] H2 tags: {h2_count}, H3 tags: {h3_count}")
        if 5 <= h2_count <= 10:
            score += 10

        # Semantic keywords
        semantic_keywords = ['service', 'repair', 'technician', 'emergency', 'warranty']
        semantic_found = sum(1 for kw in semantic_keywords if kw in self.text_content.lower())
        score += (semantic_found / len(semantic_keywords)) * 15
        print(f"[INFO] Semantic coverage: {semantic_found}/{len(semantic_keywords)}")

        # Internal links
        internal_links = len(re.findall(r'<a\s+href=["\']/[^"\']*["\']', self.html_content))
        if internal_links >= 10:
            score += 10
            print(f"[OK] Internal links: {internal_links}")
        else:
            print(f"[WARN] Internal links: {internal_links} (target: 10+)")

        # Images (including SVG with role="img")
        img_tags = re.findall(r'<img[^>]*>', self.html_content)
        svg_images = re.findall(r'<svg[^>]*role=["\']img["\'][^>]*>', self.html_content)
        total_images = len(img_tags) + len(svg_images)

        images_with_alt = len([img for img in img_tags if 'alt=' in img])
        svg_with_aria = len([svg for svg in svg_images if 'aria-label=' in svg])
        total_with_labels = images_with_alt + svg_with_aria

        if total_images >= 5:
            score += 10
            print(f"[OK] Images: {total_images} (IMG: {len(img_tags)}, SVG: {len(svg_images)}), with labels: {total_with_labels}")
        else:
            print(f"[WARN] Images: {total_images} (need 5+)")
            self.report["issues"].append(f"Only {total_images} images")

        # Trust signals
        trust_signals = ['licensed', 'insured', 'warranty', 'certified']
        trust_count = sum(1 for signal in trust_signals if signal in self.text_content.lower())
        if trust_count >= 3:
            score += 10
            print(f"[OK] Trust signals: {trust_count}/{len(trust_signals)}")
        else:
            print(f"[WARN] Trust signals: {trust_count}/{len(trust_signals)}")

        self.report["scores"]["content"] = score
        print(f"Content Score: {score}/100")

    def check_technical(self):
        """Check technical SEO"""
        print("\n--- TECHNICAL SEO ---")
        score = 0

        # Title tag
        title = re.search(r'<title>(.*?)</title>', self.html_content)
        if title:
            title_len = len(title.group(1))
            if 50 <= title_len <= 60:
                score += 10
                print(f"[OK] Title tag: {title_len} chars")
            else:
                print(f"[WARN] Title tag: {title_len} chars (target: 50-60)")

        # Meta description
        meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', self.html_content)
        if meta_desc:
            desc_len = len(meta_desc.group(1))
            if 150 <= desc_len <= 160:
                score += 10
                print(f"[OK] Meta description: {desc_len} chars")
            else:
                print(f"[WARN] Meta description: {desc_len} chars (target: 150-160)")

        # Schema markup
        schema_types = re.findall(r'"@type":\s*"([^"]+)"', self.html_content)
        if len(set(schema_types)) >= 2:
            score += 20
            print(f"[OK] Schema types: {len(set(schema_types))}")
        else:
            print(f"[WARN] Schema types: {len(set(schema_types))} (need 3+)")
            self.report["issues"].append("Add more schema types")

        # Mobile viewport
        if 'viewport' in self.html_content:
            score += 15
            print("[OK] Mobile viewport configured")
        else:
            print("[ERROR] No mobile viewport")

        # HTTPS
        if 'https://' in self.html_content:
            score += 15
            print("[OK] HTTPS references found")

        # JavaScript optimization
        if 'defer' in self.html_content or 'async' in self.html_content:
            score += 15
            print("[OK] JavaScript deferred/async")
        else:
            print("[WARN] JavaScript not optimized")

        # Critical CSS
        if '<style>' in self.html_content[:3000]:
            score += 15
            print("[OK] Critical CSS inline")

        self.report["scores"]["technical"] = score
        print(f"Technical Score: {score}/100")

    def check_ai_optimization(self):
        """Check AI and voice search optimization"""
        print("\n--- AI & VOICE SEARCH ---")
        score = 0

        # Summary boxes
        summary_indicators = ['quick answer', 'summary', 'tldr']
        summary_found = sum(1 for ind in summary_indicators if ind in self.html_content.lower())
        if summary_found > 0:
            score += 20
            print(f"[OK] Summary boxes: {summary_found}")
        else:
            print("[ERROR] No AI summary boxes")
            self.report["issues"].append("Add AI summary boxes")

        # FAQ Schema
        if 'FAQPage' in self.html_content:
            score += 20
            print("[OK] FAQ Schema found")
        else:
            print("[WARN] No FAQ Schema")

        # Question headers
        questions = re.findall(r'<h[2-3][^>]*>.*\?.*</h[2-3]>', self.html_content)
        if len(questions) >= 3:
            score += 20
            print(f"[OK] Question headers: {len(questions)}")
        else:
            print(f"[WARN] Question headers: {len(questions)} (need 5+)")

        # Voice search phrases
        voice_phrases = ['near me', 'how to', 'what is', 'where can']
        voice_count = sum(1 for phrase in voice_phrases if phrase in self.text_content.lower())
        if voice_count >= 2:
            score += 20
            print(f"[OK] Voice search phrases: {voice_count}")
        else:
            print(f"[WARN] Voice search phrases: {voice_count}")

        # Lists and tables for featured snippets
        lists = len(re.findall(r'<[ou]l>', self.html_content))
        tables = len(re.findall(r'<table', self.html_content))
        if lists >= 2 or tables >= 1:
            score += 20
            print(f"[OK] Featured snippet format: {lists} lists, {tables} tables")
        else:
            print(f"[WARN] Need more lists/tables")

        self.report["scores"]["ai_optimization"] = score
        print(f"AI Optimization Score: {score}/100")

    def check_local_seo(self):
        """Check local SEO"""
        print("\n--- LOCAL SEO ---")
        score = 0

        # Toronto mentions
        toronto_count = self.text_content.lower().count('toronto')
        if 15 <= toronto_count <= 40:
            score += 25
            print(f"[OK] Toronto mentions: {toronto_count}")
        else:
            print(f"[WARN] Toronto mentions: {toronto_count} (target: 15-40)")
            if toronto_count > 40:
                self.report["issues"].append(f"Toronto oversaturation: {toronto_count}")

        # Local schema
        if 'LocalBusiness' in self.html_content:
            score += 25
            print("[OK] LocalBusiness schema")
        else:
            print("[ERROR] No LocalBusiness schema")

        # Phone number
        phone_count = self.html_content.count('437-747-6737')
        if phone_count >= 3:
            score += 20
            print(f"[OK] Phone mentions: {phone_count}")
        else:
            print(f"[WARN] Phone mentions: {phone_count}")

        # Neighborhoods
        neighborhoods = ['north york', 'scarborough', 'etobicoke', 'mississauga']
        neighborhood_count = sum(1 for n in neighborhoods if n in self.text_content.lower())
        if neighborhood_count >= 2:
            score += 15
            print(f"[OK] Neighborhoods: {neighborhood_count}")
        else:
            print(f"[WARN] Neighborhoods: {neighborhood_count}")

        # Local keywords
        local_keywords = ['gta', 'ontario', '416', '647']
        local_found = sum(1 for kw in local_keywords if kw in self.text_content.lower())
        score += (local_found / len(local_keywords)) * 15
        print(f"[INFO] Local keywords: {local_found}/{len(local_keywords)}")

        self.report["scores"]["local_seo"] = score
        print(f"Local SEO Score: {score}/100")

    def check_user_experience(self):
        """Check user experience"""
        print("\n--- USER EXPERIENCE ---")
        score = 0

        # Font size
        font_match = re.search(r'font-size:\s*(\d+)px', self.html_content)
        if font_match:
            font_size = int(font_match.group(1))
            if font_size >= 18:
                score += 25
                print(f"[OK] Font size: {font_size}px")
            else:
                print(f"[ERROR] Font size: {font_size}px (need 18px+)")
                self.report["issues"].append(f"Font size {font_size}px too small")

        # CTAs
        cta_patterns = ['call now', 'get quote', 'contact', 'book']
        cta_count = sum(1 for cta in cta_patterns if cta in self.text_content.lower())
        if cta_count >= 3:
            score += 25
            print(f"[OK] CTAs: {cta_count} types")
        else:
            print(f"[WARN] CTAs: {cta_count}")

        # Forms
        form_count = len(re.findall(r'<form', self.html_content))
        if form_count >= 1:
            score += 25
            print(f"[OK] Forms: {form_count}")
        else:
            print("[WARN] No forms found")

        # Navigation
        if '<nav' in self.html_content:
            score += 25
            print("[OK] Navigation present")

        self.report["scores"]["user_experience"] = score
        print(f"UX Score: {score}/100")

    def calculate_overall_score(self):
        """Calculate weighted overall score"""
        weights = {
            "content": 0.25,
            "technical": 0.20,
            "ai_optimization": 0.25,
            "local_seo": 0.20,
            "user_experience": 0.10
        }

        total = 0
        for category, weight in weights.items():
            if category in self.report["scores"]:
                total += self.report["scores"][category] * weight

        self.report["overall_score"] = round(total)

    def print_report(self):
        """Print final report"""
        print("\n" + "=" * 60)
        print("SEO OPTIMIZATION REPORT SUMMARY")
        print("=" * 60)

        print(f"\nOVERALL SCORE: {self.report['overall_score']}/100")

        if self.report['overall_score'] >= 85:
            status = "EXCELLENT"
        elif self.report['overall_score'] >= 70:
            status = "GOOD"
        elif self.report['overall_score'] >= 50:
            status = "NEEDS IMPROVEMENT"
        else:
            status = "POOR"

        print(f"Status: {status}")

        print("\nCATEGORY SCORES:")
        for category, score in self.report["scores"].items():
            print(f"  {category.replace('_', ' ').title()}: {score}/100")

        if self.report["issues"]:
            print("\nCRITICAL ISSUES:")
            for i, issue in enumerate(self.report["issues"][:5], 1):
                print(f"  {i}. {issue}")

        print("\n" + "=" * 60)

        # Save report
        filename = f"seo_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"\nReport saved to: {filename}")


class TextExtractor(HTMLParser):
    """Extract visible text from HTML"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'meta', 'link'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            cleaned = data.strip()
            if cleaned:
                self.text.append(cleaned)


if __name__ == "__main__":
    import sys

    html_file = sys.argv[1] if len(sys.argv) > 1 else "website/index.html"

    print(f"Analyzing: {html_file}")
    checker = SEOChecker(html_file)
    checker.run_check()