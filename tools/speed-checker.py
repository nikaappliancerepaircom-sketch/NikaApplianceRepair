#!/usr/bin/env python3
"""
BMAD Speed Optimization Checker
Analyzes page load performance metrics
"""

import os
import re
from pathlib import Path

class SpeedChecker:
    """Check page speed optimization factors"""

    def __init__(self, html_file):
        self.html_file = html_file
        self.html_content = ""
        self.css_files = []
        self.js_files = []
        self.report = {
            "issues": [],
            "recommendations": [],
            "score": 0
        }

    def run_check(self):
        """Run all speed checks"""
        print("\n" + "="*60)
        print("BMAD SPEED OPTIMIZATION CHECK")
        print("="*60)

        # Load HTML
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            print(f"[OK] Loaded {self.html_file}")
        except Exception as e:
            print(f"[ERROR] {e}")
            return

        score = 0
        max_score = 100

        print("\n--- PERFORMANCE FACTORS ---")

        # 1. Critical CSS inline
        if '<style>' in self.html_content[:5000]:
            score += 10
            print("[OK] Critical CSS inline (Fast First Paint)")
        else:
            print("[WARN] No critical CSS inline")
            self.report["issues"].append("Add critical CSS inline")

        # 2. CSS files count
        css_links = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', self.html_content)
        css_count = len(css_links)
        if css_count <= 3:
            score += 10
            print(f"[OK] CSS files: {css_count} (optimal: ≤3)")
        elif css_count <= 5:
            score += 5
            print(f"[WARN] CSS files: {css_count} (consider combining)")
        else:
            print(f"[ERROR] CSS files: {css_count} (too many, combine them)")
            self.report["issues"].append(f"Reduce CSS files from {css_count}")

        # 3. JavaScript optimization
        js_scripts = re.findall(r'<script[^>]*src=[^>]*>', self.html_content)
        js_with_async = sum(1 for js in js_scripts if 'async' in js or 'defer' in js)
        js_count = len(js_scripts)

        if js_with_async == js_count and js_count > 0:
            score += 15
            print(f"[OK] All {js_count} external scripts optimized (async/defer)")
        elif js_with_async > 0:
            score += 8
            print(f"[WARN] {js_with_async}/{js_count} scripts optimized")
        else:
            print(f"[ERROR] No async/defer on {js_count} scripts")

        # 4. Font loading
        font_links = re.findall(r'fonts\.googleapis\.com', self.html_content)
        preconnect_fonts = re.findall(r'<link[^>]*preconnect[^>]*fonts', self.html_content)

        if len(font_links) > 0:
            if len(preconnect_fonts) >= 2:
                score += 10
                print(f"[OK] Font preconnect configured")
            else:
                score += 5
                print("[WARN] Add font preconnect for faster loading")

            # Check font-display
            if 'font-display' in self.html_content or 'display=swap' in self.html_content:
                score += 10
                print("[OK] Font-display: swap configured")
            else:
                print("[WARN] Add font-display: swap to Google Fonts URL")
                self.report["recommendations"].append("Add &display=swap to font URL")

        # 5. Image optimization
        images = re.findall(r'<img[^>]*>', self.html_content)
        img_with_loading = sum(1 for img in images if 'loading=' in img)

        if len(images) > 0:
            if img_with_loading > 0:
                score += 10
                print(f"[OK] {img_with_loading}/{len(images)} images with lazy loading")
            else:
                print(f"[WARN] Add loading='lazy' to images below fold")
                self.report["recommendations"].append("Add loading='lazy' to images")
        else:
            score += 10
            print("[OK] No heavy images (SVG/data URIs only)")

        # 6. Preload critical resources
        preload_count = len(re.findall(r'<link[^>]*rel=["\']preload["\']', self.html_content))
        if preload_count >= 1:
            score += 10
            print(f"[OK] {preload_count} resources preloaded")
        else:
            print("[INFO] Consider preloading critical fonts/CSS")

        # 7. DNS prefetch / preconnect
        prefetch_count = len(re.findall(r'<link[^>]*rel=["\'](?:dns-prefetch|preconnect)["\']', self.html_content))
        if prefetch_count >= 3:
            score += 10
            print(f"[OK] {prefetch_count} DNS optimizations")
        elif prefetch_count > 0:
            score += 5
            print(f"[INFO] {prefetch_count} DNS optimizations (good)")
        else:
            print("[WARN] Add preconnect for external resources")

        # 8. Minification check (rough estimate)
        html_size = len(self.html_content)
        whitespace_ratio = len(re.findall(r'\s{2,}', self.html_content)) / html_size if html_size > 0 else 0

        if whitespace_ratio < 0.1:
            score += 5
            print("[OK] HTML appears minified")
        else:
            print("[INFO] Consider minifying HTML for production")

        # 9. Render-blocking resources
        blocking_css = [css for css in css_links if 'media=' not in css or 'media="all"' in css]
        if len(blocking_css) <= 2:
            score += 10
            print(f"[OK] Minimal render-blocking CSS ({len(blocking_css)})")
        else:
            score += 5
            print(f"[WARN] {len(blocking_css)} render-blocking CSS files")

        # 10. Third-party scripts
        third_party = re.findall(r'<script[^>]*src=["\']https?://(?:unpkg|cdnjs|googleapis)[^"\']*["\']', self.html_content)
        if len(third_party) <= 3:
            score += 5
            print(f"[OK] Limited third-party scripts ({len(third_party)})")
        else:
            print(f"[INFO] {len(third_party)} third-party scripts (consider reducing)")

        self.report["score"] = score

        # Summary
        print("\n" + "="*60)
        print(f"SPEED OPTIMIZATION SCORE: {score}/100")

        if score >= 90:
            print("Status: EXCELLENT - Very fast loading")
        elif score >= 75:
            print("Status: GOOD - Fast with minor optimizations possible")
        elif score >= 60:
            print("Status: FAIR - Moderate speed, improvements recommended")
        else:
            print("Status: NEEDS WORK - Significant optimizations needed")

        print("="*60)

        # Recommendations
        if self.report["recommendations"]:
            print("\nRECOMMENDATIONS:")
            for rec in self.report["recommendations"]:
                print(f"  • {rec}")

        # Estimated load time
        print("\nESTIMATED METRICS:")
        print(f"  HTML Size: {html_size / 1024:.1f} KB")
        print(f"  CSS Files: {css_count}")
        print(f"  JS Files: {js_count}")
        print(f"  Images: {len(images)}")

        # Performance tips
        print("\nKEY OPTIMIZATIONS FOR 90+ MOBILE SCORE:")
        print("  1. ✓ Critical CSS inline (Fast First Paint)")
        print("  2. ✓ Async/defer JavaScript")
        print("  3. ✓ Font preconnect + display=swap")
        print("  4. → Lazy load images below fold")
        print("  5. → Minify CSS/JS files")
        print("  6. → Use modern image formats (WebP)")
        print("  7. → Reduce third-party scripts")
        print("  8. → Enable compression (gzip/brotli)")

        return self.report

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python speed-checker.py <html_file>")
        sys.exit(1)

    checker = SpeedChecker(sys.argv[1])
    checker.run_check()