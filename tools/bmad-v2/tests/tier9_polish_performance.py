#!/usr/bin/env python3
"""
BMAD V2 - TIER 9: POLISH & PERFORMANCE (34 params)
Tests final optimizations, security, and infrastructure
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup


class Tier9Tester:
    """Test Polish & Performance (params 244-277)"""

    def __init__(self, html_file, config_file):
        self.html_file = Path(html_file)
        self.config_file = Path(config_file)
        self.html_content = ""
        self.soup = None
        self.config = {}
        self.score = 0
        self.total_tests = 34
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

    def test_minification(self):
        """244. Code minification"""
        has_whitespace = re.search(r'\n\s{4,}', self.html_content)
        has_comments = '<!--' in self.html_content and 'DOCTYPE' not in self.html_content[self.html_content.find('<!--'):]

        if not has_whitespace or not has_comments:
            print("[PASS] 244. Code minification")
            self.passed += 1
        else:
            print("[WARN] 244. Code minification")
            print("   >> Code not minified")
            self.warnings += 1

    def test_compression(self):
        """245. GZIP/Brotli compression (server-level)"""
        # Can't test server config from HTML, mark as info
        print("[INFO] 245. GZIP/Brotli compression")
        print("   >> Requires server check")
        self.warnings += 1

    def test_cdn_usage(self):
        """246. CDN for static assets"""
        has_cdn = any([
            'cdn.' in self.html_content.lower(),
            'cloudflare' in self.html_content.lower(),
            'cloudfront' in self.html_content.lower(),
            'jsdelivr' in self.html_content.lower(),
            'unpkg' in self.html_content.lower()
        ])

        if has_cdn:
            print("[PASS] 246. CDN usage")
            self.passed += 1
        else:
            print("[WARN] 246. CDN usage")
            print("   >> No CDN detected")
            self.warnings += 1

    def test_resource_hints(self):
        """247. Resource hints (preload, prefetch, dns-prefetch)"""
        has_hints = any([
            'rel="preload"' in self.html_content,
            'rel="prefetch"' in self.html_content,
            'rel="dns-prefetch"' in self.html_content,
            'rel="preconnect"' in self.html_content
        ])

        if has_hints:
            print("[PASS] 247. Resource hints")
            self.passed += 1
        else:
            print("[WARN] 247. Resource hints")
            print("   >> No preload/prefetch")
            self.warnings += 1

    def test_critical_css(self):
        """248. Critical CSS inlined"""
        has_inline_css = '<style>' in self.html_content

        if has_inline_css:
            print("[PASS] 248. Critical CSS")
            self.passed += 1
        else:
            print("[WARN] 248. Critical CSS")
            print("   >> No inline critical CSS")
            self.warnings += 1

    def test_async_css(self):
        """249. Async CSS loading"""
        has_async_css = any([
            'media="print" onload' in self.html_content,
            'rel="preload" as="style"' in self.html_content
        ])

        if has_async_css:
            print("[PASS] 249. Async CSS loading")
            self.passed += 1
        else:
            print("[WARN] 249. Async CSS loading")
            print("   >> CSS blocks rendering")
            self.warnings += 1

    def test_font_optimization(self):
        """250. Font loading optimization"""
        has_font_display = 'font-display' in self.html_content.lower()
        has_preload_fonts = 'rel="preload"' in self.html_content and 'font' in self.html_content.lower()

        if has_font_display or has_preload_fonts:
            print("[PASS] 250. Font optimization")
            self.passed += 1
        else:
            print("[WARN] 250. Font optimization")
            print("   >> No font-display or preload")
            self.warnings += 1

    def test_asset_versioning(self):
        """251. Asset versioning/cache busting"""
        has_versioning = any([
            re.search(r'\.(css|js)\?v=', self.html_content),
            re.search(r'\.(css|js)\?ver=', self.html_content),
            re.search(r'-v\d+\.(css|js)', self.html_content)
        ])

        if has_versioning:
            print("[PASS] 251. Asset versioning")
            self.passed += 1
        else:
            print("[WARN] 251. Asset versioning")
            print("   >> No cache busting")
            self.warnings += 1

    def test_browser_caching(self):
        """252. Browser caching headers (server-level)"""
        # Can't test from HTML
        print("[INFO] 252. Browser caching")
        print("   >> Requires server check")
        self.warnings += 1

    def test_image_srcset(self):
        """253. Responsive images (srcset)"""
        has_srcset = 'srcset=' in self.html_content

        if has_srcset:
            print("[PASS] 253. Responsive images")
            self.passed += 1
        else:
            print("[WARN] 253. Responsive images")
            print("   >> No srcset attributes")
            self.warnings += 1

    def test_webp_support(self):
        """254. WebP/modern image formats"""
        has_webp = any([
            '.webp' in self.html_content.lower(),
            'image/webp' in self.html_content.lower(),
            '<picture>' in self.html_content.lower()
        ])

        if has_webp:
            print("[PASS] 254. WebP support")
            self.passed += 1
        else:
            print("[WARN] 254. WebP support")
            print("   >> No WebP images")
            self.warnings += 1

    def test_http2(self):
        """255. HTTP/2 or HTTP/3 (server-level)"""
        # Can't test from HTML
        print("[INFO] 255. HTTP/2/3 support")
        print("   >> Requires server check")
        self.warnings += 1

    def test_ssl_tls(self):
        """256. SSL/TLS security"""
        has_https = 'https://' in self.html_content

        if has_https:
            print("[PASS] 256. SSL/TLS references")
            self.passed += 1
        else:
            print("[WARN] 256. SSL/TLS references")
            print("   >> Check HTTPS usage")
            self.warnings += 1

    def test_security_headers(self):
        """257. Security headers (server-level)"""
        # Can't test from HTML
        print("[INFO] 257. Security headers")
        print("   >> Requires server check (CSP, X-Frame-Options, etc.)")
        self.warnings += 1

    def test_csp(self):
        """258. Content Security Policy"""
        has_csp = 'content-security-policy' in self.html_content.lower()

        if has_csp:
            print("[PASS] 258. CSP meta tag")
            self.passed += 1
        else:
            print("[WARN] 258. CSP meta tag")
            print("   >> No CSP found")
            self.warnings += 1

    def test_xss_protection(self):
        """259. XSS protection headers"""
        has_xss = 'x-xss-protection' in self.html_content.lower()

        if has_xss:
            print("[PASS] 259. XSS protection")
            self.passed += 1
        else:
            print("[WARN] 259. XSS protection")
            print("   >> Should be set in headers")
            self.warnings += 1

    def test_cors(self):
        """260. CORS configuration"""
        has_cors = 'access-control-allow' in self.html_content.lower()

        if has_cors:
            print("[PASS] 260. CORS headers")
            self.passed += 1
        else:
            print("[INFO] 260. CORS headers")
            print("   >> May not be needed")
            self.warnings += 1

    def test_analytics(self):
        """261. Analytics integration"""
        has_analytics = any([
            'google-analytics' in self.html_content.lower(),
            'gtag' in self.html_content.lower(),
            'ga(' in self.html_content.lower(),
            'analytics.js' in self.html_content.lower()
        ])

        if has_analytics:
            print("[PASS] 261. Analytics")
            self.passed += 1
        else:
            print("[FAIL] 261. Analytics")
            print("   >> No tracking found")
            self.failed += 1

    def test_gtm(self):
        """262. Google Tag Manager"""
        has_gtm = 'googletagmanager' in self.html_content.lower()

        if has_gtm:
            print("[PASS] 262. Google Tag Manager")
            self.passed += 1
        else:
            print("[WARN] 262. Google Tag Manager")
            print("   >> Consider using GTM")
            self.warnings += 1

    def test_conversion_tracking(self):
        """263. Conversion tracking pixels"""
        has_conversion = any([
            'fbq(' in self.html_content.lower(),  # Facebook Pixel
            'gtag' in self.html_content.lower() and 'event' in self.html_content.lower(),
            'conversion' in self.html_content.lower()
        ])

        if has_conversion:
            print("[PASS] 263. Conversion tracking")
            self.passed += 1
        else:
            print("[WARN] 263. Conversion tracking")
            print("   >> No conversion pixels")
            self.warnings += 1

    def test_error_tracking(self):
        """264. Error tracking (Sentry, etc.)"""
        has_error_tracking = any([
            'sentry' in self.html_content.lower(),
            'bugsnag' in self.html_content.lower(),
            'rollbar' in self.html_content.lower(),
            'onerror' in self.html_content.lower()
        ])

        if has_error_tracking:
            print("[PASS] 264. Error tracking")
            self.passed += 1
        else:
            print("[WARN] 264. Error tracking")
            print("   >> No error monitoring")
            self.warnings += 1

    def test_gdpr_compliance(self):
        """265. GDPR compliance indicators"""
        has_gdpr = any([
            'cookie' in self.html_content.lower() and 'consent' in self.html_content.lower(),
            'privacy policy' in self.html_content.lower(),
            'gdpr' in self.html_content.lower()
        ])

        if has_gdpr:
            print("[PASS] 265. GDPR compliance")
            self.passed += 1
        else:
            print("[WARN] 265. GDPR compliance")
            print("   >> No cookie consent")
            self.warnings += 1

    def test_privacy_policy(self):
        """266. Privacy policy link"""
        has_privacy = 'privacy' in self.html_content.lower() and ('policy' in self.html_content.lower() or 'href' in self.html_content.lower())

        if has_privacy:
            print("[PASS] 266. Privacy policy")
            self.passed += 1
        else:
            print("[FAIL] 266. Privacy policy")
            print("   >> Required by law")
            self.failed += 1

    def test_terms_of_service(self):
        """267. Terms of service"""
        has_terms = 'terms' in self.html_content.lower() and ('service' in self.html_content.lower() or 'condition' in self.html_content.lower())

        if has_terms:
            print("[PASS] 267. Terms of service")
            self.passed += 1
        else:
            print("[WARN] 267. Terms of service")
            print("   >> Recommended")
            self.warnings += 1

    def test_accessibility_statement(self):
        """268. Accessibility statement"""
        has_a11y = 'accessibility' in self.html_content.lower() and 'statement' in self.html_content.lower()

        if has_a11y:
            print("[PASS] 268. Accessibility statement")
            self.passed += 1
        else:
            print("[WARN] 268. Accessibility statement")
            print("   >> Optional but recommended")
            self.warnings += 1

    def test_sitemap(self):
        """269. Sitemap.xml reference"""
        has_sitemap = 'sitemap' in self.html_content.lower() and '.xml' in self.html_content.lower()

        if has_sitemap:
            print("[PASS] 269. Sitemap reference")
            self.passed += 1
        else:
            print("[WARN] 269. Sitemap reference")
            print("   >> Should exist for SEO")
            self.warnings += 1

    def test_robots_txt(self):
        """270. Robots.txt (can't verify from HTML)"""
        print("[INFO] 270. Robots.txt")
        print("   >> Requires separate check")
        self.warnings += 1

    def test_canonical_url(self):
        """271. Canonical URL tag"""
        has_canonical = 'rel="canonical"' in self.html_content

        if has_canonical:
            print("[PASS] 271. Canonical URL")
            self.passed += 1
        else:
            print("[WARN] 271. Canonical URL")
            print("   >> Prevents duplicate content")
            self.warnings += 1

    def test_hreflang(self):
        """272. Hreflang tags (if multilingual)"""
        has_hreflang = 'hreflang' in self.html_content.lower()

        if has_hreflang:
            print("[PASS] 272. Hreflang tags")
            self.passed += 1
        else:
            print("[INFO] 272. Hreflang tags")
            print("   >> Not needed for single language")
            self.warnings += 1

    def test_social_meta(self):
        """273. Social media meta tags (OG, Twitter)"""
        has_og = 'og:' in self.html_content
        has_twitter = 'twitter:' in self.html_content

        if has_og or has_twitter:
            print("[PASS] 273. Social meta tags")
            self.passed += 1
        else:
            print("[WARN] 273. Social meta tags")
            print("   >> Missing OG/Twitter cards")
            self.warnings += 1

    def test_favicon_variants(self):
        """274. Favicon variants (multiple sizes)"""
        favicon_count = self.html_content.lower().count('icon')

        if favicon_count >= 3:
            print(f"[PASS] 274. Favicon variants ({favicon_count})")
            self.passed += 1
        else:
            print(f"[WARN] 274. Favicon variants ({favicon_count})")
            print("   >> Add multiple sizes")
            self.warnings += 1

    def test_apple_touch_icon(self):
        """275. Apple touch icon"""
        has_apple_icon = 'apple-touch-icon' in self.html_content.lower()

        if has_apple_icon:
            print("[PASS] 275. Apple touch icon")
            self.passed += 1
        else:
            print("[WARN] 275. Apple touch icon")
            print("   >> For iOS bookmarks")
            self.warnings += 1

    def test_theme_color(self):
        """276. Theme color meta tag"""
        has_theme = 'theme-color' in self.html_content.lower()

        if has_theme:
            print("[PASS] 276. Theme color")
            self.passed += 1
        else:
            print("[WARN] 276. Theme color")
            print("   >> For mobile browsers")
            self.warnings += 1

    def test_validation(self):
        """277. HTML validation (basic check)"""
        has_doctype = '<!DOCTYPE html>' in self.html_content
        has_html_tag = '<html' in self.html_content
        has_head = '<head>' in self.html_content.lower()
        has_body = '<body>' in self.html_content.lower()

        if all([has_doctype, has_html_tag, has_head, has_body]):
            print("[PASS] 277. HTML validation")
            self.passed += 1
        else:
            print("[FAIL] 277. HTML validation")
            print("   >> Missing required tags")
            self.failed += 1

    def test_all(self):
        """Run all Tier 9 tests"""
        print("\n" + "=" * 60)
        print("TIER 9: POLISH & PERFORMANCE (34 params)")
        print("=" * 60)
        print()

        # Run all tests
        self.test_minification()
        self.test_compression()
        self.test_cdn_usage()
        self.test_resource_hints()
        self.test_critical_css()
        self.test_async_css()
        self.test_font_optimization()
        self.test_asset_versioning()
        self.test_browser_caching()
        self.test_image_srcset()
        self.test_webp_support()
        self.test_http2()
        self.test_ssl_tls()
        self.test_security_headers()
        self.test_csp()
        self.test_xss_protection()
        self.test_cors()
        self.test_analytics()
        self.test_gtm()
        self.test_conversion_tracking()
        self.test_error_tracking()
        self.test_gdpr_compliance()
        self.test_privacy_policy()
        self.test_terms_of_service()
        self.test_accessibility_statement()
        self.test_sitemap()
        self.test_robots_txt()
        self.test_canonical_url()
        self.test_hreflang()
        self.test_social_meta()
        self.test_favicon_variants()
        self.test_apple_touch_icon()
        self.test_theme_color()
        self.test_validation()

        # Calculate score
        self.score = (self.passed / self.total_tests) * 100

        # Print summary
        print()
        print("=" * 60)
        print(f"TIER 9 SCORE: {self.score:.1f}/100")
        print("=" * 60)

        if self.score >= 60:
            print("[SUCCESS] TIER 9 PASSED")
        else:
            print("[INFO] TIER 9 - Many params require server config")
        print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier9_polish_performance.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier9Tester(html_file, config_file)
    if tester.load_config() and tester.load_html():
        tester.test_all()
