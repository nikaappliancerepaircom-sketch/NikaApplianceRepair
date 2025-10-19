#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix Samsung page Tier 2 issues: word count, keyword density, CTA count."""

import os
import sys
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fix_tier2_issues():
    """Fix Tier 2 BMAD issues."""

    print("Fixing Tier 2 issues...\n")

    file_path = 'brands/samsung-appliance-repair-toronto.html'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = []

    # ========================================
    # 1. FIX META DESCRIPTION (172 -> 156 chars)
    # ========================================
    old_meta = re.search(r'<meta name="description" content=".*?">', content)
    if old_meta and len(old_meta.group()) > 170:
        content = content.replace(
            old_meta.group(),
            '<meta name="description" content="Expert Samsung appliance repair Toronto & GTA. Same-day service. Licensed technicians. 90-day warranty. Call 437-747-6737 to book now.">'
        )
        changes.append("Meta description: 172 -> 154 chars")

    # ========================================
    # 2. REDUCE CTA COUNT (11 -> 6)
    # ========================================
    # Remove duplicate CTAs - keep only strategic ones
    # Find and remove extra "Book Service" buttons after hero

    # Remove CTA from About section
    about_cta_pattern = r'<div class="cta-container">\s*<a href="\.\./book\.html" class="btn-primary">\s*<i class="fas fa-calendar-check"></i>\s*BOOK SAMSUNG REPAIR NOW\s*</a>\s*</div>\s*</section>\s*<!-- End About Section -->'
    if re.search(about_cta_pattern, content, re.DOTALL):
        content = re.sub(
            r'<div class="cta-container">\s*<a href="\.\./book\.html" class="btn-primary">.*?BOOK SAMSUNG REPAIR NOW.*?</a>\s*</div>(\s*</section>\s*<!-- End About Section -->)',
            r'\1',
            content,
            flags=re.DOTALL,
            count=1
        )
        changes.append("Removed About section CTA")

    # Remove CTAs from service sections (keep only hero CTAs)
    service_cta_pattern = r'<div class="cta-container">\s*<a href="\.\./book\.html" class="btn-primary">.*?</a>\s*</div>\s*(?=</section>)'
    cta_removals = 0
    for _ in range(3):  # Remove up to 3 service CTAs
        if re.search(service_cta_pattern, content, re.DOTALL):
            content = re.sub(service_cta_pattern, '', content, flags=re.DOTALL, count=1)
            cta_removals += 1

    if cta_removals > 0:
        changes.append(f"Removed {cta_removals} service section CTAs")

    # ========================================
    # 3. REDUCE WORD COUNT (2640 -> ~2000)
    # ========================================
    # Remove redundant sections or shorten verbose descriptions

    # Shorten FAQ section - remove 2-3 less relevant questions
    # Find FAQ section and remove generic questions
    faq_questions_to_remove = [
        r'<button class="faq-question"[^>]*>.*?What is the best way to maintain my appliances\?.*?</button>\s*<div class="faq-answer">.*?</div>\s*</div>',
        r'<button class="faq-question"[^>]*>.*?Can I get same-day service\?.*?</button>\s*<div class="faq-answer">.*?</div>\s*</div>',
    ]

    for pattern in faq_questions_to_remove:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE, count=1)
            changes.append("Removed FAQ question")

    # ========================================
    # 4. OPTIMIZE KEYWORD DENSITY (2.7% -> 2.0%)
    # ========================================
    # Replace some "Samsung" mentions with pronouns or generic terms
    # Only in body content, not in headings/titles

    # Replace "Samsung appliances" -> "appliances" in some places
    samsung_appliances_count = len(re.findall(r'Samsung appliances', content))
    if samsung_appliances_count > 5:
        # Replace 2-3 instances with just "appliances"
        content = content.replace('Samsung appliances', 'appliances', 2)
        changes.append("Reduced 'Samsung appliances' mentions (2)")

    # Replace "Samsung repair" -> "repair" in some body text
    samsung_repair_pattern = r'(<p[^>]*>.*?)Samsung repair(.*?</p>)'
    matches = list(re.finditer(samsung_repair_pattern, content, re.DOTALL))
    if len(matches) > 3:
        # Replace in 1-2 instances
        for match in matches[:2]:
            old_p = match.group()
            new_p = old_p.replace('Samsung repair', 'repair', 1)
            content = content.replace(old_p, new_p, 1)
        changes.append("Reduced 'Samsung repair' mentions (2)")

    # ========================================
    # SAVE FIXED FILE
    # ========================================

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Count words and keyword density
        text_content = re.sub(r'<[^>]+>', ' ', content)
        words = len(text_content.split())
        samsung_count = len(re.findall(r'\bSamsung\b', content, re.IGNORECASE))
        keyword_density = (samsung_count / words) * 100 if words > 0 else 0

        # Count CTAs
        cta_pattern = r'<a[^>]*class="[^"]*btn-primary[^"]*"[^>]*>.*?</a>'
        cta_count = len(re.findall(cta_pattern, content, re.DOTALL))

        print(f"✓ Fixes applied: {len(changes)}")
        print(f"\nChanges made:")
        for i, change in enumerate(changes, 1):
            print(f"  {i}. {change}")

        print(f"\n{'='*60}")
        print(f"Updated Statistics:")
        print(f"  Total words: {words}")
        print(f"  'Samsung' mentions: {samsung_count}")
        print(f"  Keyword density: {keyword_density:.2f}%")
        print(f"  CTA count: {cta_count}")
        print(f"{'='*60}")

        return True
    else:
        print("No changes needed")
        return False

if __name__ == '__main__':
    print("="*60)
    print("Samsung Page - Tier 2 Fixes")
    print("="*60)
    print()

    fix_tier2_issues()

    print("\n" + "="*60)
    print("✓ Tier 2 fixes complete!")
    print("Next: Re-run BMAD test")
    print("="*60)
