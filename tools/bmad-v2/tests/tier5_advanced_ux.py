#!/usr/bin/env python3
"""
BMAD V2 - TIER 5: ADVANCED UX (30 params)
Tests enhanced features and interactivity
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup


class Tier5Tester:
    """Test Advanced UX features (params 126-155)"""

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

    def test_css_animations(self):
        """126. CSS animations/transitions present"""
        has_animations = any([
            '@keyframes' in self.html_content.lower(),
            'animation:' in self.html_content.lower(),
            'transition:' in self.html_content.lower(),
            '.animate' in self.html_content.lower()
        ])

        if has_animations:
            print("[PASS] 126. CSS animations/transitions")
            self.passed += 1
        else:
            print("[WARN] 126. CSS animations/transitions")
            print("   >> No animations found")
            self.warnings += 1

    def test_scroll_effects(self):
        """127. Scroll-triggered effects"""
        has_scroll_effects = any([
            'scroll' in self.html_content.lower() and 'animation' in self.html_content.lower(),
            'data-aos' in self.html_content.lower(),
            'intersection' in self.html_content.lower(),
            'scrollreveal' in self.html_content.lower()
        ])

        if has_scroll_effects:
            print("[PASS] 127. Scroll effects")
            self.passed += 1
        else:
            print("[WARN] 127. Scroll effects")
            print("   >> No scroll animations")
            self.warnings += 1

    def test_parallax(self):
        """128. Parallax scrolling (optional)"""
        has_parallax = 'parallax' in self.html_content.lower()

        if has_parallax:
            print("[PASS] 128. Parallax scrolling")
            self.passed += 1
        else:
            print("[WARN] 128. Parallax scrolling")
            print("   >> Optional feature")
            self.warnings += 1

    def test_video_background(self):
        """129. Video elements (background or content)"""
        has_video = '<video' in self.html_content.lower() or 'youtube.com' in self.html_content.lower() or 'vimeo.com' in self.html_content.lower()

        if has_video:
            print("[PASS] 129. Video elements")
            self.passed += 1
        else:
            print("[WARN] 129. Video elements")
            print("   >> No video content")
            self.warnings += 1

    def test_interactive_elements(self):
        """130. Interactive UI elements"""
        interactive_count = 0
        interactive_elements = [
            '<button', '<input', '<select', '<textarea',
            'onclick=', 'data-toggle', 'tabindex'
        ]

        for elem in interactive_elements:
            if elem in self.html_content.lower():
                interactive_count += 1

        if interactive_count >= 4:
            print(f"[PASS] 130. Interactive elements {interactive_count}")
            self.passed += 1
        else:
            print(f"[WARN] 130. Interactive elements {interactive_count}")
            print("   >> Limited interactivity")
            self.warnings += 1

    def test_pwa_manifest(self):
        """131. PWA manifest.json"""
        has_manifest = 'manifest.json' in self.html_content.lower() or '<link rel="manifest"' in self.html_content.lower()

        if has_manifest:
            print("[PASS] 131. PWA manifest")
            self.passed += 1
        else:
            print("[WARN] 131. PWA manifest")
            print("   >> No PWA manifest")
            self.warnings += 1

    def test_service_worker(self):
        """132. Service worker for offline support"""
        has_sw = any([
            'service-worker' in self.html_content.lower(),
            'serviceworker' in self.html_content.lower(),
            'sw.js' in self.html_content.lower()
        ])

        if has_sw:
            print("[PASS] 132. Service worker")
            self.passed += 1
        else:
            print("[WARN] 132. Service worker")
            print("   >> No offline support")
            self.warnings += 1

    def test_offline_fallback(self):
        """133. Offline page/fallback"""
        has_offline = 'offline' in self.html_content.lower() and ('fallback' in self.html_content.lower() or 'cache' in self.html_content.lower())

        if has_offline:
            print("[PASS] 133. Offline fallback")
            self.passed += 1
        else:
            print("[WARN] 133. Offline fallback")
            print("   >> No offline handling")
            self.warnings += 1

    def test_app_icons(self):
        """134. App icons for PWA"""
        has_icons = any([
            'apple-touch-icon' in self.html_content.lower(),
            'icon-192' in self.html_content.lower(),
            'icon-512' in self.html_content.lower()
        ])

        if has_icons:
            print("[PASS] 134. App icons")
            self.passed += 1
        else:
            print("[WARN] 134. App icons")
            print("   >> Missing PWA icons")
            self.warnings += 1

    def test_push_notifications(self):
        """135. Push notification support"""
        has_push = any([
            'push' in self.html_content.lower() and 'notification' in self.html_content.lower(),
            'onesignal' in self.html_content.lower(),
            'firebase' in self.html_content.lower() and 'messaging' in self.html_content.lower()
        ])

        if has_push:
            print("[PASS] 135. Push notifications")
            self.passed += 1
        else:
            print("[WARN] 135. Push notifications")
            print("   >> Optional feature")
            self.warnings += 1

    def test_geolocation(self):
        """136. Geolocation features"""
        has_geo = any([
            'geolocation' in self.html_content.lower(),
            'navigator.geolocation' in self.html_content.lower(),
            'detect location' in self.html_content.lower()
        ])

        if has_geo:
            print("[PASS] 136. Geolocation")
            self.passed += 1
        else:
            print("[WARN] 136. Geolocation")
            print("   >> No location detection")
            self.warnings += 1

    def test_maps_integration(self):
        """137. Maps integration (Google Maps, etc.)"""
        has_maps = any([
            'maps.google' in self.html_content.lower(),
            'maps.googleapis' in self.html_content.lower(),
            'mapbox' in self.html_content.lower(),
            '<iframe' in self.html_content and 'map' in self.html_content.lower()
        ])

        if has_maps:
            print("[PASS] 137. Maps integration")
            self.passed += 1
        else:
            print("[FAIL] 137. Maps integration")
            print("   >> No map for service area")
            self.failed += 1

    def test_live_chat(self):
        """138. Live chat widget"""
        has_chat = any([
            'livechat' in self.html_content.lower(),
            'tawk.to' in self.html_content.lower(),
            'intercom' in self.html_content.lower(),
            'drift' in self.html_content.lower(),
            'zendesk' in self.html_content.lower() and 'chat' in self.html_content.lower()
        ])

        if has_chat:
            print("[PASS] 138. Live chat")
            self.passed += 1
        else:
            print("[WARN] 138. Live chat")
            print("   >> No live chat widget")
            self.warnings += 1

    def test_realtime_updates(self):
        """139. Real-time data updates"""
        has_realtime = any([
            'websocket' in self.html_content.lower(),
            'socket.io' in self.html_content.lower(),
            'real-time' in self.html_content.lower(),
            'live update' in self.html_content.lower()
        ])

        if has_realtime:
            print("[PASS] 139. Real-time updates")
            self.passed += 1
        else:
            print("[WARN] 139. Real-time updates")
            print("   >> Optional feature")
            self.warnings += 1

    def test_chatbot(self):
        """140. Chatbot integration"""
        has_chatbot = any([
            'chatbot' in self.html_content.lower(),
            'bot' in self.html_content.lower() and 'chat' in self.html_content.lower(),
            'dialogflow' in self.html_content.lower()
        ])

        if has_chatbot:
            print("[PASS] 140. Chatbot")
            self.passed += 1
        else:
            print("[WARN] 140. Chatbot")
            print("   >> Optional feature")
            self.warnings += 1

    def test_social_sharing(self):
        """141. Social sharing buttons"""
        has_sharing = any([
            'share' in self.html_content.lower() and ('facebook' in self.html_content.lower() or 'twitter' in self.html_content.lower()),
            'addtoany' in self.html_content.lower(),
            'sharethis' in self.html_content.lower()
        ])

        if has_sharing:
            print("[PASS] 141. Social sharing")
            self.passed += 1
        else:
            print("[WARN] 141. Social sharing")
            print("   >> No sharing buttons")
            self.warnings += 1

    def test_social_login(self):
        """142. Social login options"""
        has_social_login = any([
            'login with facebook' in self.html_content.lower(),
            'login with google' in self.html_content.lower(),
            'oauth' in self.html_content.lower()
        ])

        if has_social_login:
            print("[PASS] 142. Social login")
            self.passed += 1
        else:
            print("[WARN] 142. Social login")
            print("   >> Optional for service sites")
            self.warnings += 1

    def test_bookmark_function(self):
        """143. Bookmark/save functionality"""
        has_bookmark = any([
            'bookmark' in self.html_content.lower(),
            'save' in self.html_content.lower() and 'later' in self.html_content.lower(),
            'favorite' in self.html_content.lower()
        ])

        if has_bookmark:
            print("[PASS] 143. Bookmark function")
            self.passed += 1
        else:
            print("[WARN] 143. Bookmark function")
            print("   >> Optional feature")
            self.warnings += 1

    def test_calculator_tools(self):
        """144. Interactive calculators"""
        has_calculator = any([
            'calculator' in self.html_content.lower(),
            'estimate' in self.html_content.lower() and 'cost' in self.html_content.lower(),
            'type="number"' in self.html_content and 'calculate' in self.html_content.lower()
        ])

        if has_calculator:
            print("[PASS] 144. Calculator tools")
            self.passed += 1
        else:
            print("[WARN] 144. Calculator tools")
            print("   >> No cost estimator")
            self.warnings += 1

    def test_comparison_tool(self):
        """145. Comparison features"""
        has_comparison = any([
            'compare' in self.html_content.lower() and 'vs' in self.html_content.lower(),
            'comparison' in self.html_content.lower(),
            '<table' in self.html_content and 'compare' in self.html_content.lower()
        ])

        if has_comparison:
            print("[PASS] 145. Comparison tool")
            self.passed += 1
        else:
            print("[WARN] 145. Comparison tool")
            print("   >> Optional feature")
            self.warnings += 1

    def test_multistep_forms(self):
        """146. Multi-step form process"""
        has_multistep = any([
            'step 1' in self.html_content.lower() or 'step 2' in self.html_content.lower(),
            'progress' in self.html_content.lower() and 'step' in self.html_content.lower(),
            'wizard' in self.html_content.lower()
        ])

        if has_multistep:
            print("[PASS] 146. Multi-step forms")
            self.passed += 1
        else:
            print("[WARN] 146. Multi-step forms")
            print("   >> Single-step forms only")
            self.warnings += 1

    def test_progress_indicators(self):
        """147. Progress bars/indicators"""
        has_progress = any([
            '<progress' in self.html_content.lower(),
            'progress-bar' in self.html_content.lower(),
            'loading' in self.html_content.lower() and 'percent' in self.html_content.lower()
        ])

        if has_progress:
            print("[PASS] 147. Progress indicators")
            self.passed += 1
        else:
            print("[WARN] 147. Progress indicators")
            print("   >> No visual progress")
            self.warnings += 1

    def test_tooltips(self):
        """148. Tooltips for help"""
        has_tooltips = any([
            'tooltip' in self.html_content.lower(),
            'title=' in self.html_content and 'help' in self.html_content.lower(),
            'data-tooltip' in self.html_content.lower()
        ])

        if has_tooltips:
            print("[PASS] 148. Tooltips")
            self.passed += 1
        else:
            print("[WARN] 148. Tooltips")
            print("   >> No contextual help")
            self.warnings += 1

    def test_modal_dialogs(self):
        """149. Modal dialogs"""
        has_modals = any([
            'modal' in self.html_content.lower(),
            'dialog' in self.html_content.lower(),
            'popup' in self.html_content.lower() and 'overlay' in self.html_content.lower()
        ])

        if has_modals:
            print("[PASS] 149. Modal dialogs")
            self.passed += 1
        else:
            print("[WARN] 149. Modal dialogs")
            print("   >> No modals found")
            self.warnings += 1

    def test_slide_panels(self):
        """150. Slide-out panels"""
        has_panels = any([
            'slide' in self.html_content.lower() and ('panel' in self.html_content.lower() or 'drawer' in self.html_content.lower()),
            'offcanvas' in self.html_content.lower(),
            'sidebar' in self.html_content.lower() and 'toggle' in self.html_content.lower()
        ])

        if has_panels:
            print("[PASS] 150. Slide-out panels")
            self.passed += 1
        else:
            print("[WARN] 150. Slide-out panels")
            print("   >> No slide panels")
            self.warnings += 1

    def test_expandable_sections(self):
        """151. Accordion/expandable sections"""
        has_accordion = any([
            'accordion' in self.html_content.lower(),
            'collapse' in self.html_content.lower() and 'expand' in self.html_content.lower(),
            'details' in self.html_content.lower() and 'summary' in self.html_content.lower()
        ])

        if has_accordion:
            print("[PASS] 151. Expandable sections")
            self.passed += 1
        else:
            print("[WARN] 151. Expandable sections")
            print("   >> No accordion found")
            self.warnings += 1

    def test_infinite_scroll(self):
        """152. Infinite scroll (optional)"""
        has_infinite = 'infinite' in self.html_content.lower() and 'scroll' in self.html_content.lower()

        if has_infinite:
            print("[PASS] 152. Infinite scroll")
            self.passed += 1
        else:
            print("[WARN] 152. Infinite scroll")
            print("   >> Not applicable")
            self.warnings += 1

    def test_sticky_elements(self):
        """153. Sticky navigation/CTA"""
        has_sticky = any([
            'position: sticky' in self.html_content.lower(),
            'position:sticky' in self.html_content.lower(),
            'fixed' in self.html_content.lower() and ('header' in self.html_content.lower() or 'nav' in self.html_content.lower())
        ])

        if has_sticky:
            print("[PASS] 153. Sticky elements")
            self.passed += 1
        else:
            print("[WARN] 153. Sticky elements")
            print("   >> No sticky navigation")
            self.warnings += 1

    def test_smooth_scrolling(self):
        """154. Smooth scroll behavior"""
        has_smooth = any([
            'scroll-behavior: smooth' in self.html_content.lower(),
            'scroll-behavior:smooth' in self.html_content.lower(),
            'smoothscroll' in self.html_content.lower()
        ])

        if has_smooth:
            print("[PASS] 154. Smooth scrolling")
            self.passed += 1
        else:
            print("[WARN] 154. Smooth scrolling")
            print("   >> No smooth scroll CSS")
            self.warnings += 1

    def test_loading_states(self):
        """155. Loading states/skeletons"""
        has_loading = any([
            'skeleton' in self.html_content.lower() and 'loader' in self.html_content.lower(),
            'spinner' in self.html_content.lower(),
            'loading' in self.html_content.lower() and ('state' in self.html_content.lower() or 'animation' in self.html_content.lower())
        ])

        if has_loading:
            print("[PASS] 155. Loading states")
            self.passed += 1
        else:
            print("[WARN] 155. Loading states")
            print("   >> No loading indicators")
            self.warnings += 1

    def test_all(self):
        """Run all Tier 5 tests"""
        print("\n" + "=" * 60)
        print("TIER 5: ADVANCED UX (30 params)")
        print("=" * 60)
        print()

        # Run all tests
        self.test_css_animations()
        self.test_scroll_effects()
        self.test_parallax()
        self.test_video_background()
        self.test_interactive_elements()
        self.test_pwa_manifest()
        self.test_service_worker()
        self.test_offline_fallback()
        self.test_app_icons()
        self.test_push_notifications()
        self.test_geolocation()
        self.test_maps_integration()
        self.test_live_chat()
        self.test_realtime_updates()
        self.test_chatbot()
        self.test_social_sharing()
        self.test_social_login()
        self.test_bookmark_function()
        self.test_calculator_tools()
        self.test_comparison_tool()
        self.test_multistep_forms()
        self.test_progress_indicators()
        self.test_tooltips()
        self.test_modal_dialogs()
        self.test_slide_panels()
        self.test_expandable_sections()
        self.test_infinite_scroll()
        self.test_sticky_elements()
        self.test_smooth_scrolling()
        self.test_loading_states()

        # Calculate score
        self.score = (self.passed / self.total_tests) * 100

        # Print summary
        print()
        print("=" * 60)
        print(f"TIER 5 SCORE: {self.score:.1f}/100")
        print("=" * 60)

        # Many Tier 5 features are optional for service sites
        if self.score >= 40:
            print("[SUCCESS] TIER 5 PASSED (many features optional)")
        else:
            print("[INFO] TIER 5 - Consider adding advanced features")
        print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier5_advanced_ux.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier5Tester(html_file, config_file)
    if tester.load_config() and tester.load_html():
        tester.test_all()
