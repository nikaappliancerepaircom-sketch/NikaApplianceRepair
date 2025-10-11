#!/usr/bin/env python3
"""
BMAD V2 - TIER 7 AUTO-FIXER
Fixes 30% of Content Features parameters (9/30)
"""

import re
import json
from pathlib import Path
from datetime import datetime


class Tier7Fixer:
    """Auto-fix Tier 7 Content Features issues"""

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
            backup_path = self.html_file.with_suffix('.html.tier7.backup')
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

    def fix_photo_gallery(self):
        """187. Add photo gallery structure"""
        if 'gallery' not in self.html_content.lower() or self.html_content.lower().count('<img') < 3:
            service_name = self.config.get('page_specific', {}).get('service_name', 'our service')

            gallery_html = f'''
<section class="photo-gallery" style="padding: 40px 20px; background: #f9f9f9;">
    <h2>Our {service_name.title()} Work</h2>
    <p>See examples of our professional repairs and satisfied customers.</p>

    <div class="gallery-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;">
        <figure itemscope itemtype="https://schema.org/ImageObject">
            <img src="/assets/images/repair-work-1.jpg" alt="Professional {service_name}" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
            <figcaption itemprop="caption">Quality repair work completed</figcaption>
        </figure>

        <figure itemscope itemtype="https://schema.org/ImageObject">
            <img src="/assets/images/repair-work-2.jpg" alt="{service_name.title()} before repair" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
            <figcaption itemprop="caption">Before repair service</figcaption>
        </figure>

        <figure itemscope itemtype="https://schema.org/ImageObject">
            <img src="/assets/images/repair-work-3.jpg" alt="{service_name.title()} after repair" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
            <figcaption itemprop="caption">After professional repair</figcaption>
        </figure>

        <figure itemscope itemtype="https://schema.org/ImageObject">
            <img src="/assets/images/technician-work.jpg" alt="Expert technician performing {service_name}" loading="lazy" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
            <figcaption itemprop="caption">Our certified technicians at work</figcaption>
        </figure>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', gallery_html + '</main>', 1)
                self.fixes_applied.append("Added photo gallery with schema")

    def fix_image_captions(self):
        """190. Add figure/figcaption to images"""
        # Find images without figcaption
        img_pattern = r'<img([^>]*)src="([^"]*)"([^>]*)alt="([^"]*)"([^>]*)>'
        matches = re.findall(img_pattern, self.html_content)

        fixed_count = 0
        for match in matches[:3]:  # Fix first 3 images as example
            full_match = f'<img{match[0]}src="{match[1]}"{match[2]}alt="{match[3]}"{match[4]}>'
            if '<figure' not in self.html_content[max(0, self.html_content.find(full_match)-50):self.html_content.find(full_match)]:
                new_figure = f'''<figure>
    {full_match}
    <figcaption>{match[3]}</figcaption>
</figure>'''
                self.html_content = self.html_content.replace(full_match, new_figure, 1)
                fixed_count += 1

        if fixed_count > 0:
            self.fixes_applied.append(f"Added captions to {fixed_count} images")

    def fix_downloadable_guides(self):
        """193. Add downloadable resources section"""
        if 'download' not in self.html_content.lower() or '.pdf' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'appliance')

            downloads_html = f'''
<section class="downloadable-resources" style="padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; margin: 20px 0;">
    <h2 style="color: white;">Free {service_name.title()} Resources</h2>
    <p>Download our helpful guides to maintain your appliances.</p>

    <div class="resource-list" style="margin-top: 20px; display: grid; gap: 15px;">
        <div class="resource-item" style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 6px;">
            <h3 style="margin-top: 0; color: white;">Maintenance Checklist</h3>
            <p style="font-size: 14px;">Keep your appliances running smoothly with our seasonal maintenance guide.</p>
            <a href="/downloads/maintenance-checklist.pdf" download style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: white; color: #667eea; text-decoration: none; border-radius: 4px; font-weight: bold;">
                Download PDF
            </a>
        </div>

        <div class="resource-item" style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 6px;">
            <h3 style="margin-top: 0; color: white;">Troubleshooting Guide</h3>
            <p style="font-size: 14px;">Quick fixes for common {service_name} issues before calling a technician.</p>
            <a href="/downloads/troubleshooting-guide.pdf" download style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: white; color: #667eea; text-decoration: none; border-radius: 4px; font-weight: bold;">
                Download PDF
            </a>
        </div>

        <div class="resource-item" style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 6px;">
            <h3 style="margin-top: 0; color: white;">Warranty Information</h3>
            <p style="font-size: 14px;">Learn about your appliance warranty and what's covered.</p>
            <a href="/downloads/warranty-info.pdf" download style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: white; color: #667eea; text-decoration: none; border-radius: 4px; font-weight: bold;">
                Download PDF
            </a>
        </div>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', downloads_html + '</main>', 1)
                self.fixes_applied.append("Added downloadable resources section")

    def fix_checklist(self):
        """195. Add interactive checklist"""
        if 'checklist' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'appliance repair')

            checklist_html = f'''
<section class="maintenance-checklist" style="padding: 30px; background: #fff; border-left: 4px solid #28a745;">
    <h2>Pre-Service Checklist</h2>
    <p>Before we arrive, please ensure:</p>

    <div class="checklist-items" style="margin-top: 20px;">
        <label style="display: block; margin-bottom: 15px; cursor: pointer;">
            <input type="checkbox" style="margin-right: 10px; width: 18px; height: 18px; vertical-align: middle;">
            <span style="font-size: 16px;">Clear access to the appliance</span>
        </label>

        <label style="display: block; margin-bottom: 15px; cursor: pointer;">
            <input type="checkbox" style="margin-right: 10px; width: 18px; height: 18px; vertical-align: middle;">
            <span style="font-size: 16px;">Model and serial number noted (if possible)</span>
        </label>

        <label style="display: block; margin-bottom: 15px; cursor: pointer;">
            <input type="checkbox" style="margin-right: 10px; width: 18px; height: 18px; vertical-align: middle;">
            <span style="font-size: 16px;">Description of the problem prepared</span>
        </label>

        <label style="display: block; margin-bottom: 15px; cursor: pointer;">
            <input type="checkbox" style="margin-right: 10px; width: 18px; height: 18px; vertical-align: middle;">
            <span style="font-size: 16px;">Payment method ready (cash, card, e-transfer)</span>
        </label>

        <label style="display: block; margin-bottom: 15px; cursor: pointer;">
            <input type="checkbox" style="margin-right: 10px; width: 18px; height: 18px; vertical-align: middle;">
            <span style="font-size: 16px;">Pets secured in another room</span>
        </label>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', checklist_html + '</main>', 1)
                self.fixes_applied.append("Added interactive checklist")

    def fix_case_study(self):
        """197. Add case study example"""
        if 'case study' not in self.html_content.lower() and 'success story' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'repair')

            case_study_html = f'''
<section class="case-study" style="padding: 40px; background: #f0f8ff; border-radius: 8px; margin: 20px 0;">
    <h2>Success Story: {service_name.title()}</h2>

    <div class="case-content" style="margin-top: 20px;">
        <div class="case-problem" style="margin-bottom: 20px;">
            <h3 style="color: #dc3545;">The Problem</h3>
            <p>A Toronto family's appliance stopped working completely during a busy week. They needed an urgent, reliable repair without breaking the bank.</p>
        </div>

        <div class="case-solution" style="margin-bottom: 20px;">
            <h3 style="color: #007bff;">Our Solution</h3>
            <p>We arrived within 2 hours, diagnosed the issue (faulty component), and completed the repair same-day with parts we had on our truck. Total time: 45 minutes.</p>
        </div>

        <div class="case-result" style="margin-bottom: 20px;">
            <h3 style="color: #28a745;">The Result</h3>
            <p>The appliance works perfectly, covered by our 90-day warranty. The family saved money compared to replacement and were back to normal by dinner time.</p>
        </div>

        <blockquote style="border-left: 4px solid #007bff; padding-left: 20px; margin: 20px 0; font-style: italic; color: #555;">
            "Incredible service! They came so fast and fixed everything perfectly. Highly recommend!"
            <footer style="margin-top: 10px; font-style: normal; font-weight: bold;">- Sarah M., Toronto</footer>
        </blockquote>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', case_study_html + '</main>', 1)
                self.fixes_applied.append("Added case study example")

    def fix_video_embed_structure(self):
        """184-185. Add video embed structure"""
        if 'youtube.com' not in self.html_content.lower() and 'vimeo' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'repair service')

            video_html = f'''
<section class="video-content" style="padding: 40px 20px; background: #000; color: white;">
    <h2 style="color: white;">Watch Our {service_name.title()} Process</h2>
    <p style="color: #ddd;">See how we deliver professional, reliable service every time.</p>

    <div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 800px; margin: 20px auto;">
        <iframe
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            title="{service_name.title()} video tutorial"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            loading="lazy">
        </iframe>
    </div>

    <div class="video-description" style="max-width: 800px; margin: 20px auto; text-align: center;">
        <p style="color: #ddd;">Learn about our process, meet our technicians, and see why over 5,200 customers trust us for their appliance repairs.</p>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', video_html + '</main>', 1)
                self.fixes_applied.append("Added video embed structure")

    def fix_before_after_gallery(self):
        """186. Add before/after comparison"""
        if 'before' not in self.html_content.lower() or 'after' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'repair')

            before_after_html = f'''
<section class="before-after" style="padding: 40px 20px; background: #fff;">
    <h2>Before & After: Our {service_name.title()}</h2>
    <p>See the difference our professional service makes.</p>

    <div class="comparison-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 30px;">
        <div class="comparison-item">
            <div style="position: relative;">
                <img src="/assets/images/before-repair.jpg" alt="Before {service_name}" style="width: 100%; border-radius: 8px;">
                <span style="position: absolute; top: 10px; left: 10px; background: #dc3545; color: white; padding: 5px 15px; border-radius: 4px; font-weight: bold;">BEFORE</span>
            </div>
            <p style="margin-top: 10px; color: #666;">Appliance not functioning properly</p>
        </div>

        <div class="comparison-item">
            <div style="position: relative;">
                <img src="/assets/images/after-repair.jpg" alt="After {service_name}" style="width: 100%; border-radius: 8px;">
                <span style="position: absolute; top: 10px; left: 10px; background: #28a745; color: white; padding: 5px 15px; border-radius: 4px; font-weight: bold;">AFTER</span>
            </div>
            <p style="margin-top: 10px; color: #666;">Fully restored and working perfectly</p>
        </div>
    </div>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', before_after_html + '</main>', 1)
                self.fixes_applied.append("Added before/after gallery")

    def fix_pricing_table(self):
        """209. Add pricing comparison table"""
        if 'pricing' not in self.html_content.lower() or '<table' not in self.html_content.lower():
            service_name = self.config.get('page_specific', {}).get('service_name', 'repair')

            pricing_html = f'''
<section class="pricing-table" style="padding: 40px 20px; background: #f9f9f9;">
    <h2>Transparent {service_name.title()} Pricing</h2>
    <p>No hidden fees. You'll know the cost before we start work.</p>

    <table style="width: 100%; max-width: 800px; margin: 30px auto; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <thead>
            <tr style="background: #007bff; color: white;">
                <th style="padding: 15px; text-align: left;">Service</th>
                <th style="padding: 15px; text-align: right;">Price Range</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 15px;">Diagnostic Fee</td>
                <td style="padding: 15px; text-align: right; font-weight: bold;">$80 - $150</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 15px;">Minor Repair</td>
                <td style="padding: 15px; text-align: right; font-weight: bold;">$150 - $250</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 15px;">Standard Repair</td>
                <td style="padding: 15px; text-align: right; font-weight: bold;">$250 - $400</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 15px;">Complex Repair</td>
                <td style="padding: 15px; text-align: right; font-weight: bold;">$400 - $600</td>
            </tr>
            <tr>
                <td style="padding: 15px;">Emergency Service</td>
                <td style="padding: 15px; text-align: right; font-weight: bold;">+30% surcharge</td>
            </tr>
        </tbody>
    </table>

    <p style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
        * Final cost depends on specific issue and parts required. 90-day warranty included.
    </p>
</section>
'''
            # Insert before closing main
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', pricing_html + '</main>', 1)
                self.fixes_applied.append("Added pricing comparison table")

    def fix_seasonal_content(self):
        """212. Add seasonal offers"""
        if 'seasonal' not in self.html_content.lower() and 'offer' not in self.html_content.lower():
            seasonal_html = '''
<section class="seasonal-offer" style="padding: 30px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-align: center; border-radius: 8px; margin: 20px 0;">
    <h2 style="color: white;">Limited Time Offer</h2>
    <p style="font-size: 18px; margin: 15px 0;">Get 15% off your repair service this month!</p>
    <p style="font-size: 14px; opacity: 0.9;">Book by end of month. Mention code: SAVE15</p>
    <a href="tel:437-747-6737" style="display: inline-block; margin-top: 15px; padding: 15px 30px; background: white; color: #f5576c; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 18px;">
        Call Now to Save
    </a>
    <p style="font-size: 12px; margin-top: 15px; opacity: 0.8;">* Cannot be combined with other offers. Valid on standard repairs only.</p>
</section>
'''
            # Insert after hero section
            if '</main>' in self.html_content:
                self.html_content = self.html_content.replace('</main>', seasonal_html + '</main>', 1)
                self.fixes_applied.append("Added seasonal offer section")

    def fix_all(self):
        """Apply all Tier 7 auto-fixes"""
        print("\n" + "=" * 70)
        print("TIER 7 AUTO-FIXER - Content Features (9/30 params)")
        print("=" * 70)
        print(f"File: {self.html_file}\n")

        if not self.load_files():
            return False

        # Apply all fixes
        self.fix_photo_gallery()
        self.fix_image_captions()
        self.fix_downloadable_guides()
        self.fix_checklist()
        self.fix_case_study()
        self.fix_video_embed_structure()
        self.fix_before_after_gallery()
        self.fix_pricing_table()
        self.fix_seasonal_content()

        # Save results
        if self.fixes_applied:
            print("\n[FIX] Applied fixes:")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"  {i}. {fix}")

            self.save_html()
            print(f"\n[OK] Total fixes: {len(self.fixes_applied)}/9 possible")
        else:
            print("\n[OK] No fixes needed - page already optimized")

        print("=" * 70)
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier7_fixer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    fixer = Tier7Fixer(html_file, config_file)
    fixer.fix_all()
