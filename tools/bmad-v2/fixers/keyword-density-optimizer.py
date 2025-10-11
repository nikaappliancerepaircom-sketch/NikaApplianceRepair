#!/usr/bin/env python3
"""
BMAD V2 - KEYWORD DENSITY OPTIMIZER
Reduces keyword density from 3.3% to optimal 2.5% by diluting repetition
"""

import re
from pathlib import Path
from collections import Counter


class KeywordDensityOptimizer:
    """Optimize keyword density on service pages"""

    def __init__(self, html_file):
        self.html_file = Path(html_file)
        self.html_content = ""
        self.appliance_type = ""

    def load_html(self):
        """Load HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()

            # Detect appliance type from filename
            filename = self.html_file.name
            self.appliance_type = filename.replace('-repair.html', '').replace('-', ' ')

            return True
        except Exception as e:
            print(f"[ERROR] Loading file: {e}")
            return False

    def save_html(self):
        """Save optimized HTML with backup"""
        try:
            # Backup
            backup_path = self.html_file.with_suffix('.html.keyword.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
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

    def calculate_density(self, text, keyword):
        """Calculate keyword density percentage"""
        # Remove HTML tags for accurate count
        text_clean = re.sub(r'<[^>]+>', ' ', text)
        words = text_clean.lower().split()
        keyword_words = keyword.lower().split()

        # Count keyword occurrences
        keyword_count = 0
        for i in range(len(words) - len(keyword_words) + 1):
            if words[i:i+len(keyword_words)] == keyword_words:
                keyword_count += 1

        if len(words) == 0:
            return 0.0

        density = (keyword_count * len(keyword_words) / len(words)) * 100
        return density

    def dilute_keywords(self):
        """Dilute keyword repetition with semantic variations"""
        changes = []

        # Get main keyword (appliance + repair)
        main_keyword = f"{self.appliance_type} repair"

        # Calculate current density
        initial_density = self.calculate_density(self.html_content, main_keyword)

        if initial_density <= 2.5:
            print(f"[OK] Keyword density already optimal: {initial_density:.2f}%")
            return []

        print(f"[INFO] Current keyword density: {initial_density:.2f}%")
        print(f"[INFO] Target: ≤2.5%")

        # Semantic variations to use instead of exact keyword
        variations = {
            'dishwasher repair': ['appliance service', 'dishwasher technician', 'kitchen appliance fix', 'professional service'],
            'washer repair': ['washing machine service', 'laundry appliance fix', 'professional technician', 'appliance expert'],
            'dryer repair': ['laundry appliance service', 'dryer technician', 'professional fix', 'appliance expert'],
            'oven repair': ['cooking appliance service', 'oven technician', 'kitchen appliance fix', 'professional service'],
            'stove repair': ['cooktop service', 'stove technician', 'cooking appliance fix', 'professional expert'],
            'range repair': ['cooking appliance service', 'range technician', 'kitchen appliance fix', 'professional service'],
            'refrigerator repair': ['cooling appliance service', 'fridge technician', 'refrigeration expert', 'professional service'],
            'freezer repair': ['freezer service', 'cooling appliance fix', 'freezer technician', 'professional expert'],
            'microwave repair': ['microwave service', 'microwave technician', 'appliance fix', 'professional service'],
            'ice maker repair': ['ice machine service', 'ice maker technician', 'appliance fix', 'professional expert'],
            'garbage disposal repair': ['disposal service', 'disposal technician', 'kitchen appliance fix', 'professional service']
        }

        semantic_alts = variations.get(main_keyword, ['appliance service', 'professional technician', 'expert service'])

        # Find all exact keyword matches (case-insensitive, outside of tags)
        # Replace every 3rd occurrence with a semantic variation
        keyword_pattern = re.compile(
            rf'\b{re.escape(main_keyword)}\b',
            re.IGNORECASE
        )

        # Get text content only (not in tags)
        text_blocks = re.split(r'(<[^>]+>)', self.html_content)

        replacements_made = 0
        occurrence_count = 0

        for i, block in enumerate(text_blocks):
            # Skip HTML tags
            if block.startswith('<'):
                continue

            # Process text content
            matches = list(keyword_pattern.finditer(block))

            if not matches:
                continue

            # Replace every 3rd and 4th occurrence in this block
            new_block = block
            offset = 0

            for match in matches:
                occurrence_count += 1

                # Replace every 3rd and 4th occurrence
                if occurrence_count % 4 in [3, 0]:
                    alt = semantic_alts[replacements_made % len(semantic_alts)]

                    start = match.start() + offset
                    end = match.end() + offset

                    new_block = new_block[:start] + alt + new_block[end:]
                    offset += len(alt) - len(match.group())
                    replacements_made += 1

            text_blocks[i] = new_block

        self.html_content = ''.join(text_blocks)

        if replacements_made > 0:
            final_density = self.calculate_density(self.html_content, main_keyword)
            changes.append(f"Diluted {replacements_made} keyword instances with semantic variations")
            changes.append(f"Density reduced: {initial_density:.2f}% -> {final_density:.2f}%")

        return changes

    def run(self):
        """Execute keyword optimization"""
        print("\n" + "="*70)
        print("BMAD V2 - KEYWORD DENSITY OPTIMIZER")
        print("="*70)
        print(f"File: {self.html_file}")
        print(f"Appliance: {self.appliance_type}\n")

        if not self.load_html():
            return False

        changes = self.dilute_keywords()

        if not changes:
            print("[OK] No keyword optimization needed")
            return True

        print(f"\n[FIX] Keyword Optimizations:")
        for i, change in enumerate(changes, 1):
            print(f"  {i}. {change}")

        self.save_html()

        print("\n" + "="*70)
        print("[SUCCESS] Keyword density optimization complete")
        print("="*70 + "\n")

        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python keyword-density-optimizer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    optimizer = KeywordDensityOptimizer(html_file)
    optimizer.run()
