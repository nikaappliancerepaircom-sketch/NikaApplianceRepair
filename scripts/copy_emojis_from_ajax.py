#!/usr/bin/env python3
"""Copy correct emojis from ajax.html to east-gwillimbury.html"""

import os

os.chdir(r'C:\NikaApplianceRepair\locations')

# Read ajax.html (known good)
with open('ajax.html', 'rb') as f:
    ajax_bytes = f.read()

ajax_text = ajax_bytes.decode('utf-8')

# Read east-gwillimbury.html
with open('east-gwillimbury.html', 'r', encoding='utf-8') as f:
    egwill = f.read()

# Extract correct emojis from ajax
import re

# Get trophy emoji
match = re.search(r'<div class="cert-icon">([🏆]+)</div>', ajax_text)
if match:
    trophy = match.group(1)

    # Replace all trophy instances
    egwill = re.sub(r'<div class="benefit-icon">[^<>]*?[ðŸ†]+[^<>]*?</div>',
                    '<div class="benefit-icon">🏆</div>', egwill)
    egwill = re.sub(r'<div class="cert-icon">[^<>]*?[ðŸ†]+[^<>]*?</div>',
                    '<div class="cert-icon">🏆</div>', egwill)
    egwill = re.sub(r'<div class="feature-icon-premium">[^<>]*?[ðŸ†]+[^<>]*?</div>',
                    '<div class="feature-icon-premium">🏆</div>', egwill)
    egwill = re.sub(r'<div class="badge-icon">[^<>]*?[ðŸ†]+[^<>]*?</div>',
                    '<div class="badge-icon">🏆</div>', egwill)

# Get house emoji
match = re.search(r'(<div class="benefit-icon">)([🏠])(</div>)', ajax_text)
if match:
    house = match.group(2)
    egwill = re.sub(r'<div class="benefit-icon">[ðŸ\s]*</div>',
                    '<div class="benefit-icon">🏠</div>', egwill, count=1)

# Get building emoji
building_pattern = r'<div class="problem-icon">🏢</div>'
if building_pattern in ajax_text:
    egwill = re.sub(r'<div class="problem-icon">[ðŸ¢]+</div>',
                    '<div class="problem-icon">🏢</div>', egwill)

# Fix any remaining broken emojis with generic replacements
egwill = egwill.replace('ðŸ†', '🏆')
egwill = egwill.replace('ðŸ ', '🏠')
egwill = egwill.replace('ðŸ¢', '🏢')
egwill = egwill.replace('âœ"', '✓')

# Write fixed version
with open('east-gwillimbury.html', 'w', encoding='utf-8') as f:
    f.write(egwill)

# Return success code
exit(0)
