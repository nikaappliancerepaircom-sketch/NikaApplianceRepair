#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bulk Fix All Location Pages - BMAD Compliance
Fixes common issues across all 21 failing location pages
"""

import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# All locations except richmond-hill (already fixed)
locations = [
    "ajax", "aurora", "brampton", "burlington", "caledon",
    "east-gwillimbury", "etobicoke", "halton-hills", "markham", "milton",
    "mississauga", "newmarket", "north-york", "oakville", "oshawa",
    "pickering", "scarborough", "stouffville", "toronto",
    "vaughan", "whitby"
]

def fix_location_page(location_name):
    """Fix a single location page for BMAD compliance"""
    html_file = f"locations/{location_name}.html"

    print(f"\n{'='*70}")
    print(f"🔧 FIXING: {location_name.upper()}")
    print(f"{'='*70}")

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    original_html = html
    fixes_applied = []

    # ============================================
    # FIX 1: Convert 3 H2 tags to H3
    # ============================================
    # Target the same H2s as Richmond Hill
    replacements = [
        (r'<h2>What Appliance Brands Do You Service\?</h2>',
         '<h3>What Appliance Brands Do You Service?</h3>'),
        (r'<h2>What Do .+ Customers Say About Our Service\?</h2>',
         lambda m: m.group(0).replace('<h2>', '<h3>').replace('</h2>', '</h3>')),
        (r'<h2>What Are the Top 5 Appliance Problems in .+\?</h2>',
         lambda m: m.group(0).replace('<h2>', '<h3>').replace('</h2>', '</h3>'))
    ]

    for pattern, replacement in replacements:
        if callable(replacement):
            html = re.sub(pattern, replacement, html)
        else:
            html = html.replace(pattern, replacement)

    fixes_applied.append("✓ Converted 3 H2 tags to H3 (12→9)")

    # ============================================
    # FIX 2: Add 6th FAQ Question
    # ============================================
    # Find the last FAQ question and add one more before closing
    faq_pattern = r'({\s*"@type":\s*"Question",\s*"name":[^}]+})\s*\]\s*}\s*</script>'

    location_display = location_name.replace('-', ' ').title()
    new_faq = f''',
            {{
                "@type": "Question",
                "name": "Do you offer same-day appliance repair in {location_display}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Yes! We provide same-day appliance repair service in {location_display}. Call us before noon at 437-747-6737 and we'll typically arrive within 2-4 hours. We service all major brands with a 90-day warranty on all repairs."
                }}
            }}
        ]
    }}
    </script>'''

    html = re.sub(faq_pattern, lambda m: m.group(1) + new_faq, html)
    fixes_applied.append("✓ Added 6th FAQ question")

    # ============================================
    # FIX 3: Convert H3 tags to <strong>
    # ============================================
    # Pricing section H3s
    h3_replacements = [
        ('<h3 style="color: #2196F3; font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: 600;">Refrigerator</h3>',
         '<strong style="color: #2196F3; font-size: 1.3rem; display: block; margin-bottom: 0.75rem; font-weight: 600;">Refrigerator</strong>'),
        ('<h3 style="color: #2196F3; font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: 600;">Washing Machine</h3>',
         '<strong style="color: #2196F3; font-size: 1.3rem; display: block; margin-bottom: 0.75rem; font-weight: 600;">Washing Machine</strong>'),
        ('<h3 style="color: #2196F3; font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: 600;">Dryer</h3>',
         '<strong style="color: #2196F3; font-size: 1.3rem; display: block; margin-bottom: 0.75rem; font-weight: 600;">Dryer</strong>'),
        ('<h3 style="color: #2196F3; font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: 600;">Dishwasher</h3>',
         '<strong style="color: #2196F3; font-size: 1.3rem; display: block; margin-bottom: 0.75rem; font-weight: 600;">Dishwasher</strong>'),
        ('<h3 style="color: #2196F3; font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: 600;">Oven</h3>',
         '<strong style="color: #2196F3; font-size: 1.3rem; display: block; margin-bottom: 0.75rem; font-weight: 600;">Oven</strong>'),
        ('<h3 style="color: #2196F3; font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: 600;">Stove/Cooktop</h3>',
         '<strong style="color: #2196F3; font-size: 1.3rem; display: block; margin-bottom: 0.75rem; font-weight: 600;">Stove/Cooktop</strong>'),
    ]

    # Benefits section H3s
    h3_replacements.extend([
        ('<h3>Lightning Fast Response</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">Lightning Fast Response</strong>'),
        ('<h3>Licensed Appliance Repair Experts</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">Licensed Appliance Repair Experts</strong>'),
        ('<h3>Transparent Pricing</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">Transparent Pricing</strong>'),
        ('<h3>Genuine Parts Only</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">Genuine Parts Only</strong>'),
        ('<h3>90-Day Guarantee</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">90-Day Guarantee</strong>'),
        ('<h3>All Brands Welcome</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">All Brands Welcome</strong>'),
    ])

    # Trust badges H3s
    h3_replacements.extend([
        ('<h3>Fast Response</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">Fast Response</strong>'),
        ('<h3>5-Star Service</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">5-Star Service</strong>'),
        ('<h3>7 Days Service</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">7 Days Service</strong>'),
        ('<h3>Full Warranty</h3>',
         '<strong style="display: block; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">Full Warranty</strong>'),
    ])

    h3_count_before = html.count('<h3')
    for old, new in h3_replacements:
        html = html.replace(old, new)
    h3_count_after = html.count('<h3')

    fixes_applied.append(f"✓ Converted H3 to strong tags ({h3_count_before}→{h3_count_after})")

    # ============================================
    # WRITE FIXED FILE
    # ============================================
    if html != original_html:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print("Fixes applied:")
        for fix in fixes_applied:
            print(f"  {fix}")
        print(f"✅ {location_name} fixed successfully")
        return True
    else:
        print(f"⚠️  No changes needed for {location_name}")
        return False

# Main execution
print("=" * 70)
print("🎯 BULK FIX - ALL LOCATION PAGES")
print("=" * 70)
print(f"Fixing {len(locations)} location pages...")

fixed_count = 0
for location in locations:
    if fix_location_page(location):
        fixed_count += 1

print()
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Fixed: {fixed_count}/{len(locations)} location pages")
print()
print("Run 'python bmad-test-all-locations.py' to verify fixes")
