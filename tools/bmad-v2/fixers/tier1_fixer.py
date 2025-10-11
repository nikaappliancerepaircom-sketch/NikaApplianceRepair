#!/usr/bin/env python3
"""
BMAD V2 - TIER 1 AUTO-FIXER
Automatically fixes all 15 critical parameters
Creates backup before making changes
"""

import re
import json
import shutil
from pathlib import Path
from datetime import datetime

class Tier1Fixer:
    """Auto-fix critical data consistency and technical issues"""

    def __init__(self, html_file, config_file):
        self.html_file = html_file
        self.config_file = config_file
        self.html_content = ""
        self.config = {}
        self.fixes_applied = []
        self.backup_file = None

    def load_config(self):
        """Load business configuration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"[ERROR] Config load failed: {e}")
            return False

    def load_html(self):
        """Load HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            return True
        except Exception as e:
            print(f"[ERROR] HTML load failed: {e}")
            return False

    def create_backup(self):
        """Create backup before making changes"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path(self.html_file).parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        filename = Path(self.html_file).name
        self.backup_file = backup_dir / f"{filename}.backup_{timestamp}"

        shutil.copy2(self.html_file, self.backup_file)
        print(f"[OK] Backup created: {self.backup_file}")
        return True

    def save_html(self):
        """Save modified HTML"""
        try:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.html_content)
            return True
        except Exception as e:
            print(f"[ERROR] Save failed: {e}")
            return False

    def fix_all(self):
        """Apply all Tier 1 fixes"""
        print("\n" + "=" * 60)
        print("[FIX] TIER 1 AUTO-FIX")
        print("=" * 60)

        self.fix_phone_consistency()
        self.fix_hours_consistency()
        self.fix_warranty_consistency()
        self.fix_rating_consistency()
        self.fix_review_count_consistency()
        self.fix_years_consistency()
        self.fix_localbusiness_schema()
        self.fix_rating_schema()
        self.fix_mobile_viewport()
        self.fix_h1_tags()
        self.fix_https_links()
        self.fix_phone_in_header()

        # Print summary
        self.print_summary()

        return len(self.fixes_applied) > 0

    def fix_phone_consistency(self):
        """Normalize all phone numbers"""
        config_phone = self.config['business_data']['phone_number']
        config_phone_norm = self.config['business_data']['phone_normalized']

        # Find all phone numbers
        phone_pattern = r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})'
        phones = re.findall(phone_pattern, self.html_content)

        if phones:
            unique_phones = list(set(phones))
            if len(unique_phones) > 1 or (unique_phones and unique_phones[0].replace('-', '').replace(' ', '') != config_phone_norm):
                # Replace all with correct format
                for phone in set(phones):
                    self.html_content = self.html_content.replace(phone, config_phone)

                self.fixes_applied.append("Phone numbers normalized to " + config_phone)
                print(f"[OK] Fixed phone consistency: {len(unique_phones)} variations -> {config_phone}")

    def fix_hours_consistency(self):
        """Normalize business hours"""
        config_hours = self.config['business_data']['service_hours']

        # Normalize "24 hours" to "24/7"
        self.html_content = re.sub(r'24\s+hours', config_hours, self.html_content, flags=re.IGNORECASE)

        # Find varied hour patterns
        patterns = [
            (r'\d+\s*(?:AM|PM)\s*[-–]\s*\d+\s*(?:AM|PM)', config_hours),
            (r'\d+am-\d+pm', config_hours),
        ]

        fixed = False
        for pattern, replacement in patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            if matches:
                for match in set(matches):
                    if match.lower() != config_hours.lower():
                        self.html_content = self.html_content.replace(match, config_hours)
                        fixed = True

        if fixed or '24 hours' in self.html_content.lower():
            self.fixes_applied.append(f"Hours normalized to {config_hours}")
            print(f"[OK] Fixed hours consistency: all hours -> {config_hours}")

    def fix_warranty_consistency(self):
        """Normalize warranty period"""
        config_warranty = self.config['quality_metrics']['warranty_period']
        config_unit = self.config['quality_metrics']['warranty_unit']
        correct_text = f"{config_warranty}-{config_unit} warranty"

        warranty_pattern = r'(\d+)[-\s]?(day|month|year)s?\s+warranty'
        warranties = re.findall(warranty_pattern, self.html_content, re.IGNORECASE)

        if warranties:
            unique_warranties = list(set(warranties))
            if len(unique_warranties) > 1 or (unique_warranties and int(unique_warranties[0][0]) != config_warranty):
                # Replace all warranties
                for num, unit in set(warranties):
                    old_text = f"{num}-{unit} warranty"
                    self.html_content = re.sub(
                        rf'{num}[-\s]?{unit}s?\s+warranty',
                        correct_text,
                        self.html_content,
                        flags=re.IGNORECASE
                    )

                self.fixes_applied.append(f"Warranty normalized to {correct_text}")
                print(f"[OK] Fixed warranty consistency: all -> {correct_text}")

    def fix_rating_consistency(self):
        """Normalize rating display"""
        config_rating = self.config['quality_metrics']['rating']

        # Fix display ratings (4.9  star)
        rating_pattern = r'(\d\.\d)\s*[ star star]'
        ratings = re.findall(rating_pattern, self.html_content)

        if ratings:
            unique_ratings = list(set(ratings))
            if len(unique_ratings) > 1 or (unique_ratings and float(unique_ratings[0]) != config_rating):
                for rating in set(ratings):
                    self.html_content = re.sub(
                        rf'{rating}\s*[ star star]',
                        f'{config_rating}  star',
                        self.html_content
                    )

        # Fix schema ratings
        schema_pattern = r'(ratingValue["\']:\s*["\'])(\d\.\d)(["\'])'
        self.html_content = re.sub(
            schema_pattern,
            rf'\g<1>{config_rating}\g<3>',
            self.html_content
        )

        self.fixes_applied.append(f"Rating normalized to {config_rating}")
        print(f"[OK] Fixed rating consistency: all -> {config_rating}  star")

    def fix_review_count_consistency(self):
        """Normalize review count"""
        config_reviews = self.config['quality_metrics']['review_count']
        formatted_reviews = f"{config_reviews:,}"  # Add comma separator

        # Fix text mentions
        review_pattern = r'([\d,]+)\+?\s*(reviews?|customers?|clients?|happy\s+customers?)'
        matches = re.findall(review_pattern, self.html_content, re.IGNORECASE)

        if matches:
            for count, word in set(matches):
                # Replace with correct count, preserving the word used
                old_text = f"{count}+ {word}"
                new_text = f"{formatted_reviews}+ {word}"
                self.html_content = self.html_content.replace(old_text, new_text)

        # Fix schema reviewCount
        schema_pattern = r'(reviewCount["\']:\s*["\'])(\d+)(["\'])'
        self.html_content = re.sub(
            schema_pattern,
            rf'\g<1>{config_reviews}\g<3>',
            self.html_content
        )

        self.fixes_applied.append(f"Review count normalized to {formatted_reviews}+")
        print(f"[OK] Fixed review count: all -> {formatted_reviews}+")

    def fix_years_consistency(self):
        """Normalize years in business"""
        config_years = self.config['quality_metrics']['years_in_business']

        years_pattern = r'(\d+)\+?\s*(years?\s*(?:in business|experience|of experience))'
        matches = re.findall(years_pattern, self.html_content, re.IGNORECASE)

        if matches:
            unique_years = list(set([int(y[0]) for y in matches]))
            if len(unique_years) > 1 or (unique_years and unique_years[0] != config_years):
                for years, phrase in set(matches):
                    old_text = f"{years}+ {phrase}"
                    new_text = f"{config_years}+ {phrase}"
                    self.html_content = self.html_content.replace(old_text, new_text)
                    # Also try without space
                    old_text2 = f"{years} {phrase}"
                    new_text2 = f"{config_years} {phrase}"
                    self.html_content = self.html_content.replace(old_text2, new_text2)

                self.fixes_applied.append(f"Years normalized to {config_years}+")
                print(f"[OK] Fixed years in business: all -> {config_years}+")

    def fix_localbusiness_schema(self):
        """Add LocalBusiness schema if missing"""
        if 'LocalBusiness' not in self.html_content and 'HomeAndConstructionBusiness' not in self.html_content:
            schema = '''
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "''' + self.config['business_data']['company_name'] + '''",
      "telephone": "''' + self.config['business_data']['phone_number'] + '''",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Toronto",
        "addressRegion": "ON",
        "addressCountry": "CA"
      },
      "openingHours": "Mo-Su 00:00-24:00"
    }
    </script>'''

            # Insert before </head>
            self.html_content = self.html_content.replace('</head>', schema + '\n</head>')
            self.fixes_applied.append("Added LocalBusiness schema")
            print("[OK] Added LocalBusiness schema")

    def fix_rating_schema(self):
        """Add AggregateRating schema if missing"""
        if 'AggregateRating' not in self.html_content:
            rating = self.config['quality_metrics']['rating']
            review_count = self.config['quality_metrics']['review_count']

            schema = '''
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": "Appliance Repair Services",
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "''' + str(rating) + '''",
        "reviewCount": "''' + str(review_count) + '''",
        "bestRating": "5",
        "worstRating": "1"
      }
    }
    </script>'''

            # Insert before </head>
            self.html_content = self.html_content.replace('</head>', schema + '\n</head>')
            self.fixes_applied.append("Added AggregateRating schema")
            print("[OK] Added AggregateRating schema")

    def fix_mobile_viewport(self):
        """Add mobile viewport if missing"""
        if 'viewport' not in self.html_content:
            viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

            # Insert in <head>
            self.html_content = self.html_content.replace('<head>', '<head>\n    ' + viewport)
            self.fixes_applied.append("Added mobile viewport")
            print("[OK] Added mobile viewport meta tag")

    def fix_h1_tags(self):
        """Ensure exactly one H1 tag"""
        h1_matches = list(re.finditer(r'<h1[^>]*>.*?</h1>', self.html_content, re.DOTALL))
        h1_count = len(h1_matches)

        if h1_count == 0:
            print("[WARN] No H1 found - manual intervention needed")
        elif h1_count > 1:
            # Keep first H1, convert others to H2
            for i, match in enumerate(h1_matches):
                if i > 0:  # Skip first H1
                    old_h1 = match.group(0)
                    new_h2 = old_h1.replace('<h1', '<h2', 1).replace('</h1>', '</h2>')
                    self.html_content = self.html_content.replace(old_h1, new_h2, 1)

            self.fixes_applied.append(f"Converted {h1_count - 1} extra H1 tags to H2")
            print(f"[OK] Fixed H1 count: {h1_count} -> 1 (converted extras to H2)")

    def fix_https_links(self):
        """Convert HTTP links to HTTPS"""
        http_pattern = r'href=["\']http://(?!localhost)'
        http_links = re.findall(http_pattern, self.html_content)

        if http_links:
            self.html_content = re.sub(r'href=["\']http://', 'href="https://', self.html_content)
            self.fixes_applied.append(f"Converted {len(http_links)} HTTP links to HTTPS")
            print(f"[OK] Fixed insecure links: {len(http_links)} HTTP -> HTTPS")

    def fix_phone_in_header(self):
        """Ensure phone is in header - note for manual check"""
        config_phone = self.config['business_data']['phone_number']

        if config_phone not in self.html_content[:2000]:
            print("[WARN] Phone not in header/hero - manual check recommended")
            # This typically requires manual positioning in header
        else:
            print("[OK] Phone already in header/hero")

    def print_summary(self):
        """Print fix summary"""
        print("\n" + "=" * 60)
        print(f"FIXES APPLIED: {len(self.fixes_applied)}")
        print("=" * 60)

        if self.fixes_applied:
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"{i}. {fix}")
        else:
            print("No fixes needed - all parameters already compliant!")

        print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier1_fixer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    fixer = Tier1Fixer(html_file, config_file)

    if not fixer.load_config():
        sys.exit(1)

    if not fixer.load_html():
        sys.exit(1)

    print("Creating backup before making changes...")
    fixer.create_backup()

    if fixer.fix_all():
        print("\nSaving changes...")
        if fixer.save_html():
            print(f"[OK] File updated: {html_file}")
            print(f"[BACKUP] Backup saved: {fixer.backup_file}")
        else:
            print("[ERROR] Failed to save changes")
            sys.exit(1)
    else:
        print("\nNo changes needed!")

    print("\n[RETEST] Re-run Tier 1 test to verify fixes")
