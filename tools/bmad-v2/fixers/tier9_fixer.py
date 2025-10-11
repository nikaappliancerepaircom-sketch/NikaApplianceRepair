#!/usr/bin/env python3
"""
BMAD V2 - TIER 9 AUTO-FIXER
Fixes 50% of Polish & Performance parameters (17/34)
"""

import re
import json
from pathlib import Path
from datetime import datetime


class Tier9Fixer:
    """Auto-fix Tier 9 Polish & Performance issues"""

    def __init__(self, html_file, config_file):
        self.html_file = Path(html_file)
        self.config_file = Path(config_file)
        self.html_content = ""
        self.config = {}
        self.fixes_applied = []

    def load_files(self):
        """Load HTML and config"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"[ERROR] Loading files: {e}")
            return False

    def save_html(self):
        """Save fixed HTML with backup"""
        try:
            # Backup original
            backup_path = self.html_file.with_suffix('.html.tier9.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.html_content)

            # Save fixed version
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.html_content)

            print(f"\n[OK] Saved: {self.html_file}")
            print(f"[OK] Backup: {backup_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Saving: {e}")
            return False

    def fix_resource_hints(self):
        """247. Add resource hints"""
        if 'rel="preconnect"' not in self.html_content or 'dns-prefetch' not in self.html_content:
            hints = '''
<!-- Resource Hints for Performance -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
'''
            if '</head>' in self.html_content and 'preconnect' not in self.html_content:
                self.html_content = self.html_content.replace('</head>', hints + '</head>', 1)
                self.fixes_applied.append("Added resource hints (preconnect, dns-prefetch)")

    def fix_font_optimization(self):
        """250. Add font-display optimization"""
        if 'font-display' not in self.html_content.lower():
            font_css = '''
<style>
/* Font optimization */
@font-face {
    font-display: swap;
}

/* Ensure system fonts fallback quickly */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', font_css + '</head>', 1)
                self.fixes_applied.append("Added font-display optimization")

    def fix_image_srcset(self):
        """253. Add responsive image hints"""
        responsive_img_comment = '''
<!-- Image Optimization Guide:
     Convert images to WebP format for better compression
     Use srcset for responsive images:
     <img src="image.jpg"
          srcset="image-320.webp 320w, image-640.webp 640w, image-1024.webp 1024w"
          sizes="(max-width: 320px) 280px, (max-width: 640px) 600px, 1024px"
          alt="description">
-->
'''
        if 'srcset' not in self.html_content and '<!-- Image Optimization' not in self.html_content:
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', responsive_img_comment + '</head>', 1)
                self.fixes_applied.append("Added image optimization guide")

    def fix_security_headers_meta(self):
        """258-259. Add security meta tags"""
        if 'x-frame-options' not in self.html_content.lower():
            security_meta = '''
<!-- Security Headers -->
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=()">
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', security_meta + '</head>', 1)
                self.fixes_applied.append("Added security meta headers")

    def fix_csp_meta(self):
        """258. Add Content Security Policy"""
        if 'content-security-policy' not in self.html_content.lower():
            csp_meta = '''<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com;">'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', csp_meta + '\n</head>', 1)
                self.fixes_applied.append("Added Content Security Policy")

    def fix_analytics_placeholder(self):
        """261. Add Google Analytics placeholder"""
        if 'google-analytics' not in self.html_content.lower() and 'gtag' not in self.html_content.lower():
            analytics_script = '''
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
<!-- End Google Analytics -->
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', analytics_script + '</head>', 1)
                self.fixes_applied.append("Added Google Analytics placeholder")

    def fix_gtm_placeholder(self):
        """262. Add Google Tag Manager placeholder"""
        if 'googletagmanager' not in self.html_content.lower():
            gtm_head = '''
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXX');</script>
<!-- End Google Tag Manager -->
'''
            gtm_body = '''
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', gtm_head + '</head>', 1)
            if '<body>' in self.html_content:
                self.html_content = self.html_content.replace('<body>', '<body>\n' + gtm_body, 1)
                self.fixes_applied.append("Added Google Tag Manager placeholder")

    def fix_conversion_tracking(self):
        """263. Add conversion tracking events"""
        if 'gtag' in self.html_content and 'event' not in self.html_content:
            conversion_script = '''
<script>
// Conversion tracking
document.addEventListener('DOMContentLoaded', function() {
    // Track phone clicks
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    phoneLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'phone_click', {
                    'event_category': 'contact',
                    'event_label': 'Phone Number Click'
                });
            }
        });
    });

    // Track form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'form_submit', {
                    'event_category': 'lead',
                    'event_label': 'Contact Form Submission'
                });
            }
        });
    });
});
</script>
'''
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', conversion_script + '</body>', 1)
                self.fixes_applied.append("Added conversion tracking events")

    def fix_gdpr_cookie_consent(self):
        """265. Add GDPR cookie consent banner"""
        if 'cookie' not in self.html_content.lower() or 'consent' not in self.html_content.lower():
            cookie_banner = '''
<div id="cookieConsent" style="display: none; position: fixed; bottom: 0; left: 0; right: 0; background: #2c3e50; color: white; padding: 20px; z-index: 9999; box-shadow: 0 -2px 10px rgba(0,0,0,0.2);">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div style="flex: 1; min-width: 300px;">
            <p style="margin: 0; font-size: 14px;">
                We use cookies to enhance your experience, analyze site traffic, and for marketing purposes.
                By continuing to browse, you consent to our use of cookies.
                <a href="/privacy-policy" style="color: #3498db; text-decoration: underline;">Learn more</a>
            </p>
        </div>
        <div style="display: flex; gap: 10px;">
            <button onclick="acceptCookies()" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
                Accept
            </button>
            <button onclick="declineCookies()" style="padding: 10px 20px; background: transparent; color: white; border: 1px solid white; border-radius: 4px; cursor: pointer;">
                Decline
            </button>
        </div>
    </div>
</div>

<script>
// Cookie Consent Management
function showCookieBanner() {
    if (!localStorage.getItem('cookieConsent')) {
        document.getElementById('cookieConsent').style.display = 'block';
    }
}

function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    document.getElementById('cookieConsent').style.display = 'none';
    // Enable analytics/tracking here
}

function declineCookies() {
    localStorage.setItem('cookieConsent', 'declined');
    document.getElementById('cookieConsent').style.display = 'none';
}

// Show banner on page load
document.addEventListener('DOMContentLoaded', showCookieBanner);
</script>
'''
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', cookie_banner + '</body>', 1)
                self.fixes_applied.append("Added GDPR cookie consent banner")

    def fix_sitemap_reference(self):
        """269. Add sitemap reference"""
        if 'sitemap' not in self.html_content.lower():
            sitemap_link = '<link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">'
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', sitemap_link + '\n</head>', 1)
                self.fixes_applied.append("Added sitemap reference")

    def fix_robots_meta(self):
        """270. Add robots meta tag"""
        if 'robots' not in self.html_content.lower() or '<meta name="robots"' not in self.html_content:
            robots_meta = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', robots_meta + '\n</head>', 1)
                self.fixes_applied.append("Added robots meta tag")

    def fix_performance_monitoring(self):
        """Add performance monitoring"""
        if 'PerformanceObserver' not in self.html_content:
            perf_script = '''
<script>
// Performance Monitoring
if ('PerformanceObserver' in window) {
    // Monitor Largest Contentful Paint (LCP)
    const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
    });
    lcpObserver.observe({entryTypes: ['largest-contentful-paint']});

    // Monitor First Input Delay (FID)
    const fidObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
            console.log('FID:', entry.processingStart - entry.startTime);
        });
    });
    fidObserver.observe({entryTypes: ['first-input']});

    // Monitor Cumulative Layout Shift (CLS)
    let clsScore = 0;
    const clsObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
            if (!entry.hadRecentInput) {
                clsScore += entry.value;
                console.log('CLS:', clsScore);
            }
        });
    });
    clsObserver.observe({entryTypes: ['layout-shift']});
}
</script>
'''
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', perf_script + '</body>', 1)
                self.fixes_applied.append("Added performance monitoring")

    def fix_error_tracking(self):
        """264. Add basic error tracking"""
        if 'window.onerror' not in self.html_content:
            error_tracking = '''
<script>
// Basic Error Tracking
window.onerror = function(message, source, lineno, colno, error) {
    console.error('Error caught:', {
        message: message,
        source: source,
        lineno: lineno,
        colno: colno,
        error: error
    });

    // Send to analytics if available
    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            'description': message,
            'fatal': false
        });
    }

    return false;
};

// Track unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);

    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            'description': 'Unhandled Promise: ' + event.reason,
            'fatal': false
        });
    }
});
</script>
'''
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', error_tracking + '</body>', 1)
                self.fixes_applied.append("Added error tracking")

    def fix_async_css(self):
        """249. Add async CSS loading hint"""
        async_css_comment = '''
<!-- CSS Optimization Guide:
     Load non-critical CSS asynchronously:
     <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
     <noscript><link rel="stylesheet" href="styles.css"></noscript>
-->
'''
        if 'preload' not in self.html_content or '<!-- CSS Optimization' not in self.html_content:
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', async_css_comment + '</head>', 1)
                self.fixes_applied.append("Added async CSS loading guide")

    def fix_asset_versioning_hint(self):
        """251. Add asset versioning comment"""
        versioning_comment = '''
<!-- Asset Versioning Guide:
     Add version numbers to CSS/JS for cache busting:
     <link rel="stylesheet" href="/styles.css?v=1.2.3">
     <script src="/script.js?v=1.2.3"></script>
-->
'''
        if '<!-- Asset Versioning' not in self.html_content:
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', versioning_comment + '</head>', 1)
                self.fixes_applied.append("Added asset versioning guide")

    def fix_accessibility_statement(self):
        """268. Add accessibility statement link"""
        if 'accessibility' not in self.html_content.lower() or 'statement' not in self.html_content.lower():
            # Add to footer if exists
            if '</footer>' in self.html_content:
                accessibility_link = '<li><a href="/accessibility-statement">Accessibility Statement</a></li>'
                # Try to add to footer nav
                if '<nav' in self.html_content and '</footer>' in self.html_content:
                    footer_section = self.html_content[self.html_content.rfind('<footer'):self.html_content.rfind('</footer>')]
                    if '<ul' in footer_section and '</ul>' in footer_section:
                        self.html_content = self.html_content.replace('</ul></footer>', accessibility_link + '\n</ul></footer>', 1)
                        self.fixes_applied.append("Added accessibility statement link to footer")

    def fix_all(self):
        """Apply all Tier 9 auto-fixes"""
        print("\n" + "=" * 70)
        print("TIER 9 AUTO-FIXER - Polish & Performance (17/34 params)")
        print("=" * 70)
        print(f"File: {self.html_file}\n")

        if not self.load_files():
            return False

        # Apply all fixes
        self.fix_resource_hints()
        self.fix_font_optimization()
        self.fix_image_srcset()
        self.fix_security_headers_meta()
        self.fix_csp_meta()
        self.fix_analytics_placeholder()
        self.fix_gtm_placeholder()
        self.fix_conversion_tracking()
        self.fix_gdpr_cookie_consent()
        self.fix_sitemap_reference()
        self.fix_robots_meta()
        self.fix_performance_monitoring()
        self.fix_error_tracking()
        self.fix_async_css()
        self.fix_asset_versioning_hint()
        self.fix_accessibility_statement()

        # Save results
        if self.fixes_applied:
            print("\n[FIX] Applied fixes:")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"  {i}. {fix}")

            self.save_html()
            print(f"\n[OK] Total fixes: {len(self.fixes_applied)}/17 possible")
        else:
            print("\n[OK] No fixes needed - page already optimized")

        print("=" * 70)
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier9_fixer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    fixer = Tier9Fixer(html_file, config_file)
    fixer.fix_all()
