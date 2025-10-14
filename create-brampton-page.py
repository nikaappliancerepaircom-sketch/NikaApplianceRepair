#!/usr/bin/env python3
"""
Create Brampton location page with 100% unique content
Based on Toronto template but completely customized for Brampton
"""

import re

# Read the Brampton file (copied from Toronto)
with open('locations/brampton.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================================
# STEP 1: META TAGS AND BASIC REPLACEMENTS
# ============================================================================

# Meta description
content = content.replace(
    'content="Appliance repair in Toronto, Ontario. Same-day service, 90-day warranty, all major brands. Save $40 on your first repair! Call 437-747-6737 for fast service"',
    'content="Appliance repair in Brampton, Ontario. Expert service for large families with heavy appliance usage. Same-day service, 90-day warranty. Call 437-747-6737"'
)

# Title
content = content.replace(
    '<title>Appliance Repair Toronto | Same Day Service | Save $40 | Nika</title>',
    '<title>Appliance Repair Brampton | Large Family Specialists | Save $40 | Nika</title>'
)

# Canonical URL
content = content.replace(
    'href="https://nikaappliancerepair.com/locations/toronto"',
    'href="https://nikaappliancerepair.com/locations/brampton"'
)

# Open Graph tags
content = content.replace(
    'content="Nika Appliance Repair Toronto | Same Day Service"',
    'content="Nika Appliance Repair Brampton | Large Family Specialists"'
)
content = content.replace(
    'content="Professional appliance repair in Toronto. Same-day service, 90-day warranty, all brands. Call 437-747-6737"',
    'content="Professional appliance repair in Brampton. Specialists in large family appliance challenges. Same-day service, 90-day warranty. Call 437-747-6737"'
)
content = content.replace(
    'property="og:url" content="https://nikaappliancerepair.com/locations/toronto"',
    'property="og:url" content="https://nikaappliancerepair.com/locations/brampton"'
)

# Twitter tags
content = content.replace(
    'name="twitter:title" content="Nika Appliance Repair Toronto | Same Day Service"',
    'name="twitter:title" content="Nika Appliance Repair Brampton | Large Family Specialists"'
)
content = content.replace(
    'name="twitter:description" content="Professional appliance repair in Toronto. Same-day service, 90-day warranty, all brands."',
    'name="twitter:description" content="Professional appliance repair in Brampton. Large family appliance specialists. Same-day service, 90-day warranty."'
)

# Schema addressLocality
content = content.replace(
    '"addressLocality": "Toronto"',
    '"addressLocality": "Brampton"'
)

# ============================================================================
# STEP 2: SCHEMA AREA SERVED - Update cities list
# ============================================================================

old_area_served = '''"areaServed": [
            {
                "@type": "City",
                "name": "Toronto"
            },
            {
                "@type": "City",
                "name": "North York"
            },
            {
                "@type": "City",
                "name": "Scarborough"
            },
            {
                "@type": "City",
                "name": "Mississauga"
            },
            {
                "@type": "City",
                "name": "Brampton"
            }
        ]'''

new_area_served = '''"areaServed": [
            {
                "@type": "City",
                "name": "Brampton"
            },
            {
                "@type": "City",
                "name": "Bramalea"
            },
            {
                "@type": "City",
                "name": "Springdale"
            },
            {
                "@type": "City",
                "name": "Heart Lake"
            },
            {
                "@type": "City",
                "name": "Mississauga"
            }
        ]'''

content = content.replace(old_area_served, new_area_served)

# ============================================================================
# STEP 3: SPEAKABLE SCHEMA
# ============================================================================

content = content.replace(
    '"name": "Nika Appliance Repair - Professional Same-Day Service in Toronto"',
    '"name": "Nika Appliance Repair - Large Family Appliance Specialists in Brampton"'
)
content = content.replace(
    '"description": "Expert appliance repair in Toronto and GTA. Same-day service, 90-day warranty, licensed technicians. Call 437-747-6737 for immediate help."',
    '"description": "Expert appliance repair in Brampton and GTA. Specialists in large family appliance challenges. Same-day service, 90-day warranty. Call 437-747-6737."'
)

# ============================================================================
# STEP 4: BREADCRUMB SCHEMA
# ============================================================================

content = content.replace(
    '"name": "Toronto",\n                "item": "https://nikaappliancerepair.com/locations/toronto"',
    '"name": "Brampton",\n                "item": "https://nikaappliancerepair.com/locations/brampton"'
)

print("✅ Step 1-4 complete: Meta tags, schemas, and basic replacements")
print("Now saving and continuing with content sections...")

# Save intermediate progress
with open('locations/brampton.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Basic replacements complete. File saved.")
print("Next: Run brampton-content-replacement.py for main content sections")
