#!/usr/bin/env python3
"""
BMAD V2 - TIER 2 FOOTER CONTACT FIX
Adds contact information to footer (Param 44)
"""

import json
from pathlib import Path


class FooterContactFixer:
    """Add contact info to footer"""

    def __init__(self, html_file, config_file):
        self.html_file = Path(html_file)
        self.config_file = Path(config_file)
        self.html_content = ""
        self.config = {}

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
            # Backup
            backup_path = self.html_file.with_suffix('.html.footer.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.html_content)

            # Save
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.html_content)

            print(f"\n[OK] Saved: {self.html_file}")
            print(f"[OK] Backup: {backup_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Saving: {e}")
            return False

    def fix_footer_contact(self):
        """Add contact block to footer"""
        # Check if already exists
        if 'footer-contact' in self.html_content or ('footer' in self.html_content.lower() and self.config['business_data']['phone_number'] in self.html_content[self.html_content.lower().rfind('footer'):]):
            print("[OK] Contact info already in footer")
            return False

        phone = self.config['business_data']['phone_number']
        hours = self.config['business_data']['service_hours']
        email = self.config['business_data'].get('email', 'info@nikaappliancerepair.ca')
        address = self.config['business_data']['service_area']

        contact_block = f'''
<div class="footer-contact" style="background: #1a1a1a; padding: 40px 20px; color: white; text-align: center;">
    <div class="footer-content" style="max-width: 1200px; margin: 0 auto;">
        <div class="footer-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; text-align: left;">

            <div class="footer-column">
                <h3 style="color: #fff; margin-bottom: 20px;">Contact Us</h3>
                <p style="margin: 10px 0;">
                    <strong>Phone:</strong><br/>
                    <a href="tel:{phone}" style="color: #fff; text-decoration: none; font-size: 18px;">
                        {phone}
                    </a>
                </p>
                <p style="margin: 10px 0;">
                    <strong>Email:</strong><br/>
                    <a href="mailto:{email}" style="color: #fff; text-decoration: none;">
                        {email}
                    </a>
                </p>
            </div>

            <div class="footer-column">
                <h3 style="color: #fff; margin-bottom: 20px;">Service Hours</h3>
                <p style="margin: 10px 0;">
                    <strong>{hours}</strong><br/>
                    Emergency service available
                </p>
                <p style="margin: 10px 0;">
                    <strong>Service Area:</strong><br/>
                    {address}
                </p>
            </div>

            <div class="footer-column">
                <h3 style="color: #fff; margin-bottom: 20px;">Quick Links</h3>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="margin: 8px 0;">
                        <a href="/services/" style="color: #fff; text-decoration: none;">All Services</a>
                    </li>
                    <li style="margin: 8px 0;">
                        <a href="/about/" style="color: #fff; text-decoration: none;">About Us</a>
                    </li>
                    <li style="margin: 8px 0;">
                        <a href="/contact/" style="color: #fff; text-decoration: none;">Contact</a>
                    </li>
                    <li style="margin: 8px 0;">
                        <a href="/privacy-policy/" style="color: #fff; text-decoration: none;">Privacy Policy</a>
                    </li>
                </ul>
            </div>

        </div>

        <div class="footer-bottom" style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #444; text-align: center;">
            <p style="margin: 0; color: #aaa; font-size: 14px;">
                &copy; 2024 Nika Appliance Repair. All rights reserved. | Licensed & Insured | 90-Day Warranty
            </p>
        </div>
    </div>
</div>
'''

        # Insert before closing footer or body
        if '</footer>' in self.html_content:
            # Insert inside footer, before closing tag
            self.html_content = self.html_content.replace('</footer>', contact_block + '</footer>', 1)
        elif '</body>' in self.html_content:
            # Insert before closing body
            self.html_content = self.html_content.replace('</body>', contact_block + '</body>', 1)
        else:
            print("[WARN] No footer or body closing tag found")
            return False

        print(f"[FIX] Added footer contact block with:")
        print(f"      - Phone: {phone}")
        print(f"      - Email: {email}")
        print(f"      - Hours: {hours}")
        print(f"      - Service Area: {address}")

        return True

    def run(self):
        """Execute the fix"""
        print("\n" + "=" * 70)
        print("TIER 2 - FOOTER CONTACT FIX (Param 44)")
        print("=" * 70)
        print(f"File: {self.html_file}\n")

        if not self.load_files():
            return False

        if self.fix_footer_contact():
            self.save_html()
            print("\n[SUCCESS] Footer contact information added")
        else:
            print("\n[OK] No changes needed")

        print("=" * 70)
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier2_footer_contact_fix.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    fixer = FooterContactFixer(html_file, config_file)
    fixer.run()
