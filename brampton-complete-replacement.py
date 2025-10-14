#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Brampton page content replacement
Reads Toronto template and creates 100% unique Brampton content
"""

# Read the current brampton.html
with open('locations/brampton.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary of all replacements
replacements = {
    # Open Graph
    'content="Nika Appliance Repair Toronto | Same Day Service"': 'content="Nika Appliance Repair Brampton | Large Family Specialists"',
    'content="Professional appliance repair in Toronto. Same-day service, 90-day warranty, all brands. Call 437-747-6737"': 'content="Professional appliance repair in Brampton. Large family appliance specialists. Same-day service, 90-day warranty. Call 437-747-6737"',
    'property="og:url" content="https://nikaappliancerepair.com/locations/toronto"': 'property="og:url" content="https://nikaappliancerepair.com/locations/brampton"',

    # Twitter
    'name="twitter:title" content="Nika Appliance Repair Toronto | Same Day Service"': 'name="twitter:title" content="Nika Appliance Repair Brampton | Large Family Specialists"',
    'name="twitter:description" content="Professional appliance repair in Toronto. Same-day service, 90-day warranty, all brands."': 'name="twitter:description" content="Professional appliance repair in Brampton. Large family appliance specialists. Same-day service, 90-day warranty."',

    # Schema
    '"addressLocality": "Toronto"': '"addressLocality": "Brampton"',
    '"name": "Nika Appliance Repair - Professional Same-Day Service in Toronto"': '"name": "Nika Appliance Repair - Large Family Appliance Specialists in Brampton"',
    '"description": "Expert appliance repair in Toronto and GTA. Same-day service, 90-day warranty, licensed technicians. Call 437-747-6737 for immediate help."': '"description": "Expert appliance repair in Brampton and GTA. Specialists in large family appliance challenges with heavy usage. Same-day service, 90-day warranty. Call 437-747-6737."',
}

# Apply all replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Hero Title - needs special handling
content = content.replace(
    '<span class="highlight-yellow">Toronto</span> Appliance<br>Repair <span class="highlight-yellow">Experts</span><br>Fast Response<br><span class="wow-text">Save $40 Today!</span>',
    '<span class="highlight-yellow">Brampton</span> Appliance<br>Repair <span class="highlight-yellow">Specialists</span><br>Large Family Experts<br><span class="wow-text">Save $40 Today!</span>'
)

# Hero subtitle
content = content.replace(
    '⭐ 4.9/5 from 5,200+ repairs • Licensed across 158 Toronto neighborhoods • Same-day appointments • 90-day parts warranty',
    '⭐ 4.9/5 from 5,200+ repairs • Brampton large family specialists • Bramalea, Springdale, Heart Lake • Same-day service • 90-day warranty'
)

# Save the file
with open('locations/brampton.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 1 complete: Basic meta and schema replacements done")
