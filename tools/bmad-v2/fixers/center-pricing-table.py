#!/usr/bin/env python3
"""
Fix pricing table centering on all pages
"""

import re
from pathlib import Path


def fix_pricing_table(html_file):
    """Center pricing table and fix text alignment"""
    html_path = Path(html_file)

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Reading {html_path.name}: {e}")
        return False

    # Backup
    backup_path = html_path.with_suffix('.html.pricing-center.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Fix 1: Change table width from 100% to max-width and center it
    content = re.sub(
        r'<table class="pricing-table" style="width: 100%;',
        r'<table class="pricing-table" style="max-width: 800px; margin: 0 auto;',
        content
    )

    # Fix 2: Center align table cells
    content = re.sub(
        r'<th style="padding: 15px; text-align: left;">',
        r'<th style="padding: 15px; text-align: center;">',
        content
    )

    content = re.sub(
        r'<td style="padding: 15px;">',
        r'<td style="padding: 15px; text-align: center;">',
        content
    )

    # Save
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed pricing table centering: {html_path.name}")
    return True


if __name__ == "__main__":
    import sys
    from pathlib import Path

    services_dir = Path(__file__).parent.parent.parent / "services"
    pages = [
        "refrigerator-repair.html",
        "dishwasher-repair.html",
        "washer-repair.html",
        "dryer-repair.html",
        "stove-repair.html",
        "oven-repair.html",
        "range-repair.html",
        "microwave-repair.html",
        "freezer-repair.html",
        "ice-maker-repair.html",
        "garbage-disposal-repair.html"
    ]

    print("\n" + "=" * 70)
    print("CENTERING PRICING TABLES ON ALL PAGES")
    print("=" * 70 + "\n")

    for page in pages:
        page_path = services_dir / page
        if page_path.exists():
            fix_pricing_table(page_path)

    print("\n" + "=" * 70)
    print("[SUCCESS] All pricing tables centered")
    print("=" * 70 + "\n")
