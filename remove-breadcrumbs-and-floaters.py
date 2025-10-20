#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove Breadcrumbs and Floating Icons from Service Pages
"""

import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# All service pages
services = [
    "refrigerator-repair", "washer-repair", "dryer-repair", "dishwasher-repair",
    "stove-repair", "freezer-repair", "range-repair", "oven-repair", "microwave-repair"
]

def remove_elements(service_name):
    """Remove breadcrumbs and floating icons from a service page"""
    html_file = f"services/{service_name}.html"

    print(f"\n{'='*70}")
    print(f"🔧 PROCESSING: {service_name}")
    print(f"{'='*70}")

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    original_html = html
    changes = []

    # ============================================
    # REMOVE 1: Breadcrumb Navigation
    # ============================================
    breadcrumb_pattern = r'    <!-- Breadcrumb Navigation -->\s*<nav class="breadcrumb".*?</nav>\s*\n'

    if re.search(breadcrumb_pattern, html, re.DOTALL):
        html = re.sub(breadcrumb_pattern, '', html, flags=re.DOTALL)
        changes.append("✓ Removed breadcrumb navigation")

    # ============================================
    # REMOVE 2: Floating Icons (hero-bg-animation)
    # ============================================
    floating_pattern = r'        <div class="hero-bg-animation">.*?</div>\s*<div class="container">'

    if re.search(floating_pattern, html, re.DOTALL):
        # Replace with just the container div
        html = re.sub(floating_pattern, '        <div class="container">', html, flags=re.DOTALL)
        changes.append("✓ Removed floating animated icons")

    # ============================================
    # WRITE UPDATED FILE
    # ============================================
    if html != original_html:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print("Changes applied:")
        for change in changes:
            print(f"  {change}")
        print(f"✅ {service_name} updated successfully")
        return True
    else:
        print(f"⚠️  No changes needed for {service_name}")
        return False

# Main execution
print("=" * 70)
print("🎯 REMOVE BREADCRUMBS & FLOATING ICONS - ALL SERVICE PAGES")
print("=" * 70)

updated_count = 0
for service in services:
    if remove_elements(service):
        updated_count += 1

print()
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Updated: {updated_count}/{len(services)} service pages")
print("=" * 70)
