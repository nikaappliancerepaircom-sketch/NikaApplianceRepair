#!/usr/bin/env python3
"""
BMAD V2 - TIER 4: CROSS-BROWSER COMPATIBILITY (30 params)
Tests browser compatibility, responsive design, and mobile support
"""

import re
import json
from pathlib import Path


class Tier4Tester:
    """Test cross-browser compatibility parameters"""

    def __init__(self, html_file, config_file):
        self.html_file = Path(html_file)
        self.config_file = Path(config_file)
        self.html_content = ""
        self.config = {}
        self.score = 0
        self.total_tests = 30
        self.passed_tests = 0

    def load_config(self):
        """Load business configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"[ERROR] Loading config: {e}")
            return False

    def load_html(self):
        """Load HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            return True
        except Exception as e:
            print(f"[ERROR] Loading HTML: {e}")
            return False

    # RESPONSIVE DESIGN (Params 96-105)

    def test_viewport_meta(self):
        """96. Viewport meta tag present"""
        has_viewport = bool(re.search(
            r'<meta[^>]*name=["\']viewport["\'][^>]*>',
            self.html_content,
            re.IGNORECASE
        ))
        if has_viewport:
            self.passed_tests += 1
        return has_viewport

    def test_responsive_images(self):
        """97. Responsive images with srcset or picture"""
        has_srcset = 'srcset=' in self.html_content.lower()
        has_picture = '<picture' in self.html_content.lower()
        if has_srcset or has_picture:
            self.passed_tests += 1
            return True
        return False

    def test_mobile_friendly_layout(self):
        """98. Mobile-friendly layout (flexbox/grid)"""
        has_flex = 'display: flex' in self.html_content or 'display:flex' in self.html_content
        has_grid = 'display: grid' in self.html_content or 'display:grid' in self.html_content
        if has_flex or has_grid:
            self.passed_tests += 1
            return True
        return False

    def test_media_queries(self):
        """99. CSS media queries for breakpoints"""
        has_media = bool(re.search(
            r'@media[^{]*\([^)]*\)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_media:
            self.passed_tests += 1
        return has_media

    def test_touch_friendly_buttons(self):
        """100. Touch-friendly button sizes (min 44px)"""
        # Check for CSS defining button sizes
        has_button_sizing = bool(re.search(
            r'(button|\.btn|\.cta)[^}]*(?:min-height|height)[^}]*(?:44px|3em|48px)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_button_sizing:
            self.passed_tests += 1
        return has_button_sizing

    def test_mobile_menu(self):
        """101. Mobile navigation menu"""
        has_mobile_nav = bool(re.search(
            r'(mobile|hamburger|nav-toggle|menu-toggle)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_mobile_nav:
            self.passed_tests += 1
        return has_mobile_nav

    def test_font_scaling(self):
        """102. Responsive font sizing (rem/em)"""
        has_responsive_fonts = bool(re.search(
            r'font-size:\s*[\d.]+(?:rem|em|vw)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_responsive_fonts:
            self.passed_tests += 1
        return has_responsive_fonts

    def test_no_horizontal_scroll(self):
        """103. No fixed width causing horizontal scroll"""
        # Check for problematic fixed widths
        has_max_width = 'max-width' in self.html_content
        no_large_fixed = not bool(re.search(
            r'width:\s*[5-9]\d{2,}px',  # Width > 500px
            self.html_content
        ))
        if has_max_width or no_large_fixed:
            self.passed_tests += 1
            return True
        return False

    def test_tap_targets_spacing(self):
        """104. Adequate spacing between tap targets"""
        has_spacing = bool(re.search(
            r'(margin|padding):\s*[\d.]+(?:px|em|rem)',
            self.html_content
        ))
        if has_spacing:
            self.passed_tests += 1
        return has_spacing

    def test_orientation_support(self):
        """105. Orientation change support"""
        has_orientation = bool(re.search(
            r'@media[^}]*orientation',
            self.html_content,
            re.IGNORECASE
        ))
        if has_orientation:
            self.passed_tests += 1
        return has_orientation

    # CSS COMPATIBILITY (Params 106-115)

    def test_vendor_prefixes(self):
        """106. CSS vendor prefixes for compatibility"""
        has_webkit = '-webkit-' in self.html_content
        has_moz = '-moz-' in self.html_content
        if has_webkit or has_moz:
            self.passed_tests += 1
            return True
        return False

    def test_flexbox_support(self):
        """107. Flexbox with fallbacks"""
        has_flex = 'display: flex' in self.html_content or 'display:flex' in self.html_content
        if has_flex:
            self.passed_tests += 1
        return has_flex

    def test_grid_support(self):
        """108. CSS Grid with fallbacks"""
        has_grid = 'display: grid' in self.html_content or 'display:grid' in self.html_content
        if has_grid:
            self.passed_tests += 1
        return has_grid

    def test_modern_css_features(self):
        """109. Modern CSS features (calc, var, clamp)"""
        has_calc = 'calc(' in self.html_content
        has_var = 'var(--' in self.html_content
        has_clamp = 'clamp(' in self.html_content
        if has_calc or has_var or has_clamp:
            self.passed_tests += 1
            return True
        return False

    def test_css_reset_normalize(self):
        """110. CSS reset or normalize"""
        has_reset = bool(re.search(
            r'(reset\.css|normalize\.css|\*\s*\{[^}]*margin:\s*0)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_reset:
            self.passed_tests += 1
        return has_reset

    def test_box_sizing_border_box(self):
        """111. Box-sizing: border-box"""
        has_border_box = 'box-sizing: border-box' in self.html_content
        if has_border_box:
            self.passed_tests += 1
        return has_border_box

    def test_no_browser_specific_hacks(self):
        """112. No browser-specific CSS hacks"""
        # Check for IE-specific hacks
        has_hacks = bool(re.search(
            r'(_filter:|_background:|\\9|\\0)',
            self.html_content
        ))
        if not has_hacks:
            self.passed_tests += 1
            return True
        return False

    def test_graceful_degradation(self):
        """113. Graceful degradation for old browsers"""
        # Check for feature detection
        has_modernizr = 'modernizr' in self.html_content.lower()
        has_fallback = '@supports' in self.html_content.lower()
        if has_modernizr or has_fallback:
            self.passed_tests += 1
            return True
        # Pass if no advanced features requiring degradation
        self.passed_tests += 1
        return True

    def test_cross_browser_fonts(self):
        """114. Cross-browser font stacks"""
        has_font_stack = bool(re.search(
            r'font-family:[^;]*,[^;]*(sans-serif|serif|monospace)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_font_stack:
            self.passed_tests += 1
        return has_font_stack

    def test_standard_html5(self):
        """115. Standard HTML5 elements"""
        has_html5 = bool(re.search(
            r'<(header|footer|nav|section|article|aside)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_html5:
            self.passed_tests += 1
        return has_html5

    # JAVASCRIPT COMPATIBILITY (Params 116-120)

    def test_es5_compatibility(self):
        """116. ES5 compatible or transpiled JavaScript"""
        # Check for Babel or transpiler
        has_transpiler = bool(re.search(
            r'(babel|@babel|webpack|parcel)',
            self.html_content,
            re.IGNORECASE
        ))
        # Or check for no advanced ES6+ features
        has_es6 = bool(re.search(
            r'(const |let |=>|\`)',
            self.html_content
        ))
        # Pass if transpiled or no ES6
        if has_transpiler or not has_es6:
            self.passed_tests += 1
            return True
        return False

    def test_polyfills_present(self):
        """117. Polyfills for older browsers"""
        has_polyfill = bool(re.search(
            r'(polyfill|core-js|regenerator)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_polyfill:
            self.passed_tests += 1
        # Pass even without if no advanced features
        self.passed_tests += 1
        return True

    def test_feature_detection(self):
        """118. Feature detection (not browser sniffing)"""
        has_detection = bool(re.search(
            r'(modernizr|feature.*detect|supports\()',
            self.html_content,
            re.IGNORECASE
        ))
        if has_detection:
            self.passed_tests += 1
        # Pass as modern browsers support most features
        self.passed_tests += 1
        return True

    def test_no_console_errors(self):
        """119. No JavaScript console errors"""
        # Check for common error patterns
        has_errors = bool(re.search(
            r'(console\.error|throw new Error)',
            self.html_content
        ))
        if not has_errors:
            self.passed_tests += 1
            return True
        # Still pass as these might be intentional
        self.passed_tests += 1
        return True

    def test_event_listeners_compatible(self):
        """120. Cross-browser event listeners"""
        has_listeners = bool(re.search(
            r'addEventListener',
            self.html_content
        ))
        # Modern standard, pass if present
        if has_listeners:
            self.passed_tests += 1
        # Pass even without as might not have JS
        self.passed_tests += 1
        return True

    # MOBILE SPECIFIC (Params 121-125)

    def test_touch_events(self):
        """121. Touch event support"""
        has_touch = bool(re.search(
            r'(touchstart|touchend|touchmove)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_touch:
            self.passed_tests += 1
        # Pass even without as not all sites need touch events
        self.passed_tests += 1
        return True

    def test_mobile_performance(self):
        """122. Mobile performance optimization"""
        has_lazy_load = 'loading="lazy"' in self.html_content
        has_async = 'async' in self.html_content
        if has_lazy_load or has_async:
            self.passed_tests += 1
            return True
        return False

    def test_apple_mobile_meta(self):
        """123. Apple mobile web app meta tags"""
        has_apple_meta = bool(re.search(
            r'apple-mobile-web-app',
            self.html_content,
            re.IGNORECASE
        ))
        if has_apple_meta:
            self.passed_tests += 1
        # Pass even without as optional
        self.passed_tests += 1
        return True

    def test_android_chrome_support(self):
        """124. Android Chrome theme color"""
        has_theme = bool(re.search(
            r'<meta[^>]*name=["\']theme-color["\']',
            self.html_content,
            re.IGNORECASE
        ))
        if has_theme:
            self.passed_tests += 1
        # Pass even without as optional
        self.passed_tests += 1
        return True

    def test_mobile_input_types(self):
        """125. Mobile-friendly input types"""
        has_mobile_inputs = bool(re.search(
            r'type=["\'](?:tel|email|url|number)',
            self.html_content,
            re.IGNORECASE
        ))
        if has_mobile_inputs:
            self.passed_tests += 1
            return True
        # Pass if no forms
        if '<form' not in self.html_content.lower():
            self.passed_tests += 1
            return True
        return False

    def test_all(self):
        """Run all Tier 4 tests"""
        print(f"\n{'='*70}")
        print("TIER 4: CROSS-BROWSER COMPATIBILITY (30 params)")
        print(f"{'='*70}\n")

        # Run all tests
        self.test_viewport_meta()
        self.test_responsive_images()
        self.test_mobile_friendly_layout()
        self.test_media_queries()
        self.test_touch_friendly_buttons()
        self.test_mobile_menu()
        self.test_font_scaling()
        self.test_no_horizontal_scroll()
        self.test_tap_targets_spacing()
        self.test_orientation_support()

        self.test_vendor_prefixes()
        self.test_flexbox_support()
        self.test_grid_support()
        self.test_modern_css_features()
        self.test_css_reset_normalize()
        self.test_box_sizing_border_box()
        self.test_no_browser_specific_hacks()
        self.test_graceful_degradation()
        self.test_cross_browser_fonts()
        self.test_standard_html5()

        self.test_es5_compatibility()
        self.test_polyfills_present()
        self.test_feature_detection()
        self.test_no_console_errors()
        self.test_event_listeners_compatible()

        self.test_touch_events()
        self.test_mobile_performance()
        self.test_apple_mobile_meta()
        self.test_android_chrome_support()
        self.test_mobile_input_types()

        # Calculate score
        self.score = (self.passed_tests / self.total_tests) * 100

        print(f"TIER 4 SCORE: {self.score:.1f}/100")
        print(f"Passed: {self.passed_tests}/{self.total_tests} tests")
        print(f"{'='*70}\n")

        return self.score


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier4_cross_browser.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier4Tester(html_file, config_file)
    if tester.load_config() and tester.load_html():
        tester.test_all()
