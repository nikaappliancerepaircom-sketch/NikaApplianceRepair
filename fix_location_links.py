#!/usr/bin/env python3
"""
Fix location links on service pages - convert DIVs to A tags for locations with pages
"""

import os
import re

# List of service pages (excluding refrigerator-repair.html which is already fixed)
service_pages = [
    'dishwasher-repair.html',
    'dryer-repair.html',
    'freezer-repair.html',
    'microwave-repair.html',
    'oven-repair.html',
    'range-repair.html',
    'stove-repair.html',
    'washer-repair.html'
]

# Location mappings: display name -> URL slug
location_mappings = {
    'Ajax': 'ajax',
    'Aurora': 'aurora',
    'Brampton': 'brampton',
    'Burlington': 'burlington',
    'Caledon': 'caledon',
    'East Gwillimbury': 'east-gwillimbury',
    'Etobicoke': 'etobicoke',
    'Halton Hills': 'halton-hills',
    'Markham': 'markham',
    'Milton': 'milton',
    'Mississauga': 'mississauga',
    'Newmarket': 'newmarket',
    'North York': 'north-york',
    'Oakville': 'oakville',
    'Oshawa': 'oshawa',
    'Pickering': 'pickering',
    'Richmond Hill': 'richmond-hill',
    'Scarborough': 'scarborough',
    'Stouffville': 'stouffville',
    'Toronto': 'toronto',
    'Vaughan': 'vaughan',
    'Whitby': 'whitby'
}

def fix_location_links(filepath):
    """Fix location DIVs to A tags in a service page"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track changes
    changes_made = 0

    # Replace each location DIV with A tag
    for location_name, url_slug in location_mappings.items():
        old_pattern = f'<div class="area-item">📍 {location_name}</div>'
        new_pattern = f'<a href="../locations/{url_slug}" class="area-item">📍 {location_name}</a>'

        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            changes_made += 1
            print(f"  OK Fixed: {location_name}")

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Total changes: {changes_made}\n")
    return changes_made

# Process all service pages
total_changes = 0
for page in service_pages:
    filepath = os.path.join('services', page)
    if os.path.exists(filepath):
        changes = fix_location_links(filepath)
        total_changes += changes
    else:
        print(f"WARNING File not found: {filepath}")

print(f"\nComplete! Total location links fixed: {total_changes}")
