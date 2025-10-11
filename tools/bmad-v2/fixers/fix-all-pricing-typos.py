#!/usr/bin/env python3
"""
Fix ALL pricing table typo variations on all pages
"""

import re
from pathlib import Path


def fix_all_typos(html_file):
    """Fix all pricing typo variations"""
    html_path = Path(html_file)

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Reading {html_path.name}: {e}")
        return False

    original_content = content

    # Fix 1: Diagnostic fee price - handle ANY variation after "star"
    content = re.sub(
        r'\$4\.9\s+star[a-z]*\(Waived if repaired\)',
        r'\$80-\$150 (Waived if repaired)',
        content,
        flags=re.IGNORECASE
    )

    # Fix 2: Font size - handle ANY variation after "star"
    content = re.sub(
        r'font-size:\s*4\.9\s+star[a-z]*em',
        'font-size: 0.9rem',
        content,
        flags=re.IGNORECASE
    )

    # Check if anything changed
    if content == original_content:
        print(f"[SKIP] No typos found: {html_path.name}")
        return True

    # Save
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed all typo variations: {html_path.name}")
    return True


if __name__ == "__main__":
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
    print("FIXING ALL PRICING TABLE TYPO VARIATIONS")
    print("=" * 70 + "\n")

    for page in pages:
        page_path = services_dir / page
        if page_path.exists():
            fix_all_typos(page_path)

    print("\n" + "=" * 70)
    print("[SUCCESS] All typo variations fixed")
    print("=" * 70 + "\n")
