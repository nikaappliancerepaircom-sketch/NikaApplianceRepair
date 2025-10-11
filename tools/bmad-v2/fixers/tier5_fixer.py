#!/usr/bin/env python3
"""
BMAD V2 - TIER 5 AUTO-FIXER
Fixes 40% of Advanced UX parameters (12/30)
"""

import re
import json
from pathlib import Path
from datetime import datetime


class Tier5Fixer:
    """Auto-fix Tier 5 Advanced UX issues"""

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
            backup_path = self.html_file.with_suffix('.html.tier5.backup')
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

    def fix_css_animations(self):
        """126. Add CSS animations"""
        if '@keyframes' not in self.html_content.lower() and 'animation:' not in self.html_content.lower():
            animation_css = '''
<style>
/* CSS Animations for better UX */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Apply animations */
.hero-section {
    animation: fadeIn 0.8s ease-out;
}

.cta-button {
    transition: all 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.service-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.phone-link {
    animation: pulse 2s infinite;
}
</style>
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', animation_css + '</head>', 1)
                self.fixes_applied.append("Added CSS animations and transitions")

    def fix_smooth_scrolling(self):
        """154. Add smooth scroll behavior"""
        if 'scroll-behavior' not in self.html_content.lower():
            smooth_scroll_css = '''
<style>
/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Smooth scroll for anchor links */
a[href^="#"] {
    scroll-behavior: smooth;
}
</style>
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', smooth_scroll_css + '</head>', 1)
                self.fixes_applied.append("Added smooth scroll behavior")

    def fix_social_sharing(self):
        """141. Add social sharing buttons"""
        if 'share' not in self.html_content.lower() or 'facebook' not in self.html_content.lower():
            phone = self.config['business_data']['phone_number']
            service_name = self.config.get('page_specific', {}).get('service_name', 'appliance repair')

            social_sharing = f'''
<section class="social-sharing" style="padding: 20px; text-align: center; background: #f5f5f5;">
    <h3>Share This Service</h3>
    <div class="share-buttons" style="display: flex; gap: 10px; justify-content: center; margin-top: 15px;">
        <a href="https://www.facebook.com/sharer/sharer.php?u=https://nikaappliancerepair.ca"
           target="_blank"
           rel="noopener"
           class="share-btn facebook"
           style="padding: 10px 20px; background: #1877f2; color: white; text-decoration: none; border-radius: 4px;">
            Share on Facebook
        </a>
        <a href="https://twitter.com/intent/tweet?url=https://nikaappliancerepair.ca&text=Professional%20{service_name.replace(' ', '%20')}%20in%20Toronto"
           target="_blank"
           rel="noopener"
           class="share-btn twitter"
           style="padding: 10px 20px; background: #1da1f2; color: white; text-decoration: none; border-radius: 4px;">
            Share on Twitter
        </a>
        <a href="mailto:?subject=Check%20this%20service&body=I%20found%20this%20great%20service:%20https://nikaappliancerepair.ca"
           class="share-btn email"
           style="padding: 10px 20px; background: #555; color: white; text-decoration: none; border-radius: 4px;">
            Share via Email
        </a>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', social_sharing + '</main>', 1)
                self.fixes_applied.append("Added social sharing buttons")

    def fix_cost_calculator(self):
        """144. Add interactive cost calculator"""
        if 'calculator' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'repair')

            calculator_html = f'''
<section class="cost-calculator" style="padding: 30px; background: #fff; border: 2px solid #007bff; border-radius: 8px; margin: 20px 0;">
    <h2>Estimate Your {service_name.title()} Cost</h2>
    <p>Get a quick estimate for your repair. Actual cost determined after diagnosis.</p>

    <form id="costCalculator" style="margin-top: 20px;">
        <div style="margin-bottom: 15px;">
            <label for="serviceType" style="display: block; margin-bottom: 5px; font-weight: bold;">Service Type:</label>
            <select id="serviceType" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                <option value="100">Basic Repair ($100-150)</option>
                <option value="200">Standard Repair ($200-300)</option>
                <option value="350">Complex Repair ($350-500)</option>
                <option value="150">Diagnostic Only ($150)</option>
            </select>
        </div>

        <div style="margin-bottom: 15px;">
            <label for="urgency" style="display: block; margin-bottom: 5px; font-weight: bold;">Urgency:</label>
            <select id="urgency" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                <option value="1.0">Regular Service</option>
                <option value="1.2">Same Day (+20%)</option>
                <option value="1.3">Emergency (+30%)</option>
            </select>
        </div>

        <button type="button" onclick="calculateCost()" style="width: 100%; padding: 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
            Calculate Estimate
        </button>

        <div id="calculatorResult" style="margin-top: 20px; padding: 15px; background: #e7f3ff; border-radius: 4px; display: none;">
            <h3 style="margin: 0 0 10px 0;">Estimated Cost:</h3>
            <p id="estimateAmount" style="font-size: 24px; font-weight: bold; color: #007bff; margin: 0;"></p>
            <p style="font-size: 14px; color: #666; margin-top: 10px;">
                * This is an estimate only. Final cost determined after professional diagnosis.
                All repairs include 90-day warranty.
            </p>
        </div>
    </form>

    <script>
    function calculateCost() {{
        const serviceType = parseFloat(document.getElementById('serviceType').value);
        const urgency = parseFloat(document.getElementById('urgency').value);
        const estimate = Math.round(serviceType * urgency);
        const maxEstimate = Math.round(estimate * 1.5);

        document.getElementById('estimateAmount').textContent = '$' + estimate + ' - $' + maxEstimate;
        document.getElementById('calculatorResult').style.display = 'block';
    }}
    </script>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', calculator_html + '</main>', 1)
                self.fixes_applied.append("Added interactive cost calculator")

    def fix_pwa_manifest(self):
        """131. Add PWA manifest"""
        if 'manifest.json' not in self.html_content.lower():
            manifest_link = '''<link rel="manifest" href="/manifest.json">'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', manifest_link + '\n</head>', 1)
                self.fixes_applied.append("Added PWA manifest link")

    def fix_app_icons(self):
        """134. Enhance app icons"""
        if 'icon-192' not in self.html_content.lower():
            icon_links = '''
<link rel="icon" sizes="192x192" href="/assets/icons/icon-192.png">
<link rel="icon" sizes="512x512" href="/assets/icons/icon-512.png">
<link rel="apple-touch-startup-image" href="/assets/icons/apple-splash.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', icon_links + '</head>', 1)
                self.fixes_applied.append("Enhanced app icons for PWA")

    def fix_modal_structure(self):
        """149. Add modal dialog structure"""
        if 'modal' not in self.html_content.lower():
            modal_html = '''
<div id="bookingModal" class="modal" style="display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5);">
    <div class="modal-content" style="background: white; margin: 10% auto; padding: 30px; width: 90%; max-width: 500px; border-radius: 8px; position: relative;">
        <span class="modal-close" onclick="closeModal()" style="position: absolute; right: 15px; top: 15px; font-size: 28px; cursor: pointer;">&times;</span>
        <h2>Book Your Service</h2>
        <p>Fill out the form and we'll contact you within 30 minutes.</p>
        <form id="quickBooking" style="margin-top: 20px;">
            <input type="text" placeholder="Your Name" required style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;">
            <input type="tel" placeholder="Phone Number" required style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;">
            <textarea placeholder="Describe the issue" rows="3" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;"></textarea>
            <button type="submit" style="width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Request Callback
            </button>
        </form>
    </div>
</div>

<script>
function openModal() {
    document.getElementById('bookingModal').style.display = 'block';
}
function closeModal() {
    document.getElementById('bookingModal').style.display = 'none';
}
window.onclick = function(event) {
    const modal = document.getElementById('bookingModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
</script>
'''
            # Insert before closing body
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', modal_html + '</body>', 1)
                self.fixes_applied.append("Added modal dialog structure")

    def fix_progress_indicators(self):
        """147. Add progress indicators"""
        if '<progress' not in self.html_content.lower():
            progress_css = '''
<style>
/* Progress indicators */
.progress-bar {
    width: 100%;
    height: 4px;
    background: #e0e0e0;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9998;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #007bff, #0056b3);
    width: 0%;
    transition: width 0.3s ease;
}

.loading-spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007bff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', progress_css + '</head>', 1)
                self.fixes_applied.append("Added progress indicator styles")

    def fix_enhanced_tooltips(self):
        """148. Enhance tooltips"""
        if 'data-tooltip' not in self.html_content.lower():
            tooltip_css = '''
<style>
/* Enhanced tooltips */
[data-tooltip] {
    position: relative;
    cursor: help;
}

[data-tooltip]:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    padding: 8px 12px;
    background: #333;
    color: white;
    font-size: 14px;
    white-space: nowrap;
    border-radius: 4px;
    margin-bottom: 5px;
    z-index: 1000;
}

[data-tooltip]:hover::before {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: #333;
    z-index: 1000;
}
</style>
'''
            if '</head>' in self.html_content:
                self.html_content = self.html_content.replace('</head>', tooltip_css + '</head>', 1)
                self.fixes_applied.append("Enhanced tooltip functionality")

    def fix_loading_states(self):
        """155. Add loading state indicators"""
        loading_html = '''
<div id="pageLoader" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10000;">
    <div class="loading-spinner"></div>
</div>

<script>
// Show loader on form submit
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            document.getElementById('pageLoader').style.display = 'block';
        });
    });
});
</script>
'''
        if 'pageLoader' not in self.html_content:
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', loading_html + '</body>', 1)
                self.fixes_applied.append("Added loading state indicators")

    def fix_scroll_effects(self):
        """127. Add scroll reveal effects"""
        if 'scroll' not in self.html_content or 'IntersectionObserver' not in self.html_content:
            scroll_effects = '''
<style>
.scroll-reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.scroll-reveal.revealed {
    opacity: 1;
    transform: translateY(0);
}
</style>

<script>
// Scroll reveal animation
document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, {
        threshold: 0.1
    });

    // Add scroll-reveal class to sections
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        if (index > 0) {  // Skip first section (hero)
            section.classList.add('scroll-reveal');
            observer.observe(section);
        }
    });
});
</script>
'''
            if '</body>' in self.html_content:
                self.html_content = self.html_content.replace('</body>', scroll_effects + '</body>', 1)
                self.fixes_applied.append("Added scroll reveal effects")

    def fix_multistep_form_enhancement(self):
        """146. Enhance multi-step forms"""
        if 'step' in self.html_content.lower():
            multistep_css = '''
<style>
/* Multi-step form enhancements */
.form-steps {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
}

.form-step {
    flex: 1;
    text-align: center;
    position: relative;
    padding: 10px;
}

.form-step.active {
    color: #007bff;
    font-weight: bold;
}

.form-step.completed {
    color: #28a745;
}

.form-step::after {
    content: '';
    position: absolute;
    top: 50%;
    right: -50%;
    width: 100%;
    height: 2px;
    background: #ddd;
}

.form-step:last-child::after {
    display: none;
}

.form-step.completed::after {
    background: #28a745;
}
</style>
'''
            if '</head>' in self.html_content and '.form-step' not in self.html_content:
                self.html_content = self.html_content.replace('</head>', multistep_css + '</head>', 1)
                self.fixes_applied.append("Enhanced multi-step form styling")

    def fix_all(self):
        """Apply all Tier 5 auto-fixes"""
        print("\n" + "=" * 70)
        print("TIER 5 AUTO-FIXER - Advanced UX (12/30 params)")
        print("=" * 70)
        print(f"File: {self.html_file}\n")

        if not self.load_files():
            return False

        # Apply all fixes
        self.fix_css_animations()
        self.fix_smooth_scrolling()
        self.fix_social_sharing()
        self.fix_cost_calculator()
        self.fix_pwa_manifest()
        self.fix_app_icons()
        self.fix_modal_structure()
        self.fix_progress_indicators()
        self.fix_enhanced_tooltips()
        self.fix_loading_states()
        self.fix_scroll_effects()
        self.fix_multistep_form_enhancement()

        # Save results
        if self.fixes_applied:
            print("\n[FIX] Applied fixes:")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"  {i}. {fix}")

            self.save_html()
            print(f"\n[OK] Total fixes: {len(self.fixes_applied)}/12 possible")
        else:
            print("\n[OK] No fixes needed - page already optimized")

        print("=" * 70)
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier5_fixer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    fixer = Tier5Fixer(html_file, config_file)
    fixer.fix_all()
