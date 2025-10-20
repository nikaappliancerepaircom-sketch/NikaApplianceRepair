#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix FAQ Questions in All Location Pages
Adds 6th FAQ question to reach BMAD compliance
"""

import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# All locations except richmond-hill (already has 6 FAQs)
locations = [
    "ajax", "aurora", "brampton", "burlington", "caledon",
    "east-gwillimbury", "etobicoke", "halton-hills", "markham", "milton",
    "mississauga", "newmarket", "north-york", "oakville", "oshawa",
    "pickering", "scarborough", "stouffville", "toronto",
    "vaughan", "whitby"
]

def fix_faq(location_name):
    """Add 6th FAQ question to location page"""
    html_file = f"locations/{location_name}.html"

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Count existing FAQs
    faq_count = html.count('"@type": "Question"')

    if faq_count >= 6:
        print(f"✅ {location_name}: Already has {faq_count} FAQs")
        return False

    # Location display name
    location_display = location_name.replace('-', ' ').title()

    # Find the last FAQ closing and add new question before it
    old_pattern = '''                }
            }
        ]
    }
    </script>'''

    new_text = f'''                }}
            }},
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

    if old_pattern in html:
        html = html.replace(old_pattern, new_text, 1)  # Replace only first occurrence

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ {location_name}: Added 6th FAQ ({faq_count}→6)")
        return True
    else:
        print(f"❌ {location_name}: Pattern not found (has {faq_count} FAQs)")
        return False

# Main execution
print("=" * 70)
print("🎯 FIX FAQ QUESTIONS - ALL LOCATION PAGES")
print("=" * 70)

fixed_count = 0
for location in locations:
    if fix_faq(location):
        fixed_count += 1

print()
print("=" * 70)
print(f"✅ Fixed: {fixed_count}/{len(locations)} location pages")
print("=" * 70)
