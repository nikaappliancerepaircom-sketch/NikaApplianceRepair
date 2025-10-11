#!/usr/bin/env python3
"""
BMAD V2 - CTA OPTIMIZER
Reduces CTA count from 14-17 to optimal 3-8 by removing redundant CTAs
"""

import re
from pathlib import Path


class CTAOptimizer:
    """Optimize CTA count on service pages"""

    def __init__(self, html_file):
        self.html_file = Path(html_file)
        self.html_content = ""
        self.ctas_found = 0
        self.ctas_removed = 0

    def load_html(self):
        """Load HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            return True
        except Exception as e:
            print(f"[ERROR] Loading file: {e}")
            return False

    def save_html(self):
        """Save optimized HTML with backup"""
        try:
            # Backup
            backup_path = self.html_file.with_suffix('.html.cta.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                # Read original again for backup
                with open(self.html_file, 'r', encoding='utf-8') as orig:
                    f.write(orig.read())

            # Save optimized
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.html_content)

            print(f"\n[OK] Saved: {self.html_file}")
            print(f"[OK] Backup: {backup_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Saving: {e}")
            return False

    def count_ctas(self):
        """Count current CTA buttons"""
        # Look for common CTA patterns
        patterns = [
            r'<a[^>]*href=["\']#book["\'][^>]*>.*?</a>',
            r'<a[^>]*href=["\']tel:[^"\']*["\'][^>]*>.*?CALL.*?</a>',
            r'<button[^>]*class="[^"]*cta[^"]*"[^>]*>.*?</button>',
            r'BOOK\s+SERVICE\s+NOW',
            r'CALL\s+NOW',
            r'SCHEDULE\s+SERVICE',
            r'GET\s+A\s+QUOTE'
        ]

        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
            count += len(matches)

        self.ctas_found = count
        return count

    def optimize_ctas(self):
        """Remove redundant CTAs, keep strategic ones"""
        changes = []

        # Strategy: Keep CTAs in:
        # 1. Hero section (1 BOOK, 1 CALL)
        # 2. Mid-page (1 BOOK or CALL)
        # 3. Footer (1 BOOK, 1 CALL)
        # Remove: Excessive CTAs in FAQ, benefits, problems sections

        # Remove CTAs from FAQ section (keep the content, remove buttons)
        faq_pattern = r'(<section[^>]*class="[^"]*faq[^"]*"[^>]*>.*?)<a[^>]*class="[^"]*cta[^"]*"[^>]*>.*?</a>(.*?</section>)'
        if re.search(faq_pattern, self.html_content, re.IGNORECASE | re.DOTALL):
            self.html_content = re.sub(
                faq_pattern,
                r'\1\2',
                self.html_content,
                flags=re.IGNORECASE | re.DOTALL
            )
            changes.append("Removed CTA buttons from FAQ section")
            self.ctas_removed += 1

        # Remove duplicate "BOOK SERVICE NOW" buttons (keep only first 2)
        book_pattern = r'<a[^>]*href=["\']#book["\'][^>]*class="[^"]*cta[^"]*"[^>]*>.*?BOOK\s+SERVICE\s+NOW.*?</a>'
        book_matches = list(re.finditer(book_pattern, self.html_content, re.IGNORECASE | re.DOTALL))

        if len(book_matches) > 3:
            # Remove all but first 3 occurrences
            for match in reversed(book_matches[3:]):  # Keep first 3, remove rest
                start, end = match.span()
                self.html_content = self.html_content[:start] + self.html_content[end:]
                self.ctas_removed += 1

            changes.append(f"Removed {len(book_matches) - 3} redundant BOOK buttons")

        # Remove duplicate CALL buttons (keep only first 2)
        call_pattern = r'<a[^>]*href=["\']tel:[^"\']*["\'][^>]*>.*?CALL\s+NOW.*?</a>'
        call_matches = list(re.finditer(call_pattern, self.html_content, re.IGNORECASE | re.DOTALL))

        if len(call_matches) > 3:
            # Remove all but first 3
            for match in reversed(call_matches[3:]):
                start, end = match.span()
                self.html_content = self.html_content[:start] + self.html_content[end:]
                self.ctas_removed += 1

            changes.append(f"Removed {len(call_matches) - 3} redundant CALL buttons")

        # Remove CTAs from benefits/problems list items
        # Keep the list items, just remove inline CTA links
        list_cta_pattern = r'(<li[^>]*>.*?)</?\s*a[^>]*class="[^"]*cta[^"]*"[^>]*>.*?BOOK.*?</a>(.*?</li>)'
        if re.search(list_cta_pattern, self.html_content, re.IGNORECASE | re.DOTALL):
            self.html_content = re.sub(
                list_cta_pattern,
                r'\1\2',
                self.html_content,
                flags=re.IGNORECASE | re.DOTALL
            )
            changes.append("Removed inline CTA links from list items")
            self.ctas_removed += 1

        return changes

    def run(self):
        """Execute CTA optimization"""
        print("\n" + "="*70)
        print("BMAD V2 - CTA OPTIMIZER")
        print("="*70)
        print(f"File: {self.html_file}\n")

        if not self.load_html():
            return False

        initial_count = self.count_ctas()
        print(f"[INFO] Initial CTA count: {initial_count}")

        if initial_count <= 8:
            print("[OK] CTA count already optimal (≤8)")
            return True

        changes = self.optimize_ctas()

        if not changes:
            print("[OK] No CTA optimizations needed")
            return True

        final_count = self.count_ctas()

        print(f"\n[FIX] CTA Optimizations:")
        for i, change in enumerate(changes, 1):
            print(f"  {i}. {change}")

        print(f"\n[RESULT] CTAs reduced: {initial_count} -> ~{final_count} (removed {self.ctas_removed})")

        self.save_html()

        print("\n" + "="*70)
        print("[SUCCESS] CTA optimization complete")
        print("="*70 + "\n")

        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python cta-optimizer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    optimizer = CTAOptimizer(html_file)
    optimizer.run()
