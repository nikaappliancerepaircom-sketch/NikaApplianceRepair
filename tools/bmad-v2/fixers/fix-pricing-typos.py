#!/usr/bin/env python3
"""
Fix typos in pricing tables on all pages
"""

from pathlib import Path


def fix_typos(html_file):
    """Fix pricing table typos"""
    html_path = Path(html_file)

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Reading {html_path.name}: {e}")
        return False

    # Fix 1: Diagnostic fee price
    content = content.replace(
        '$4.9  star(Waived if repaired)',
        '$80-$150 (Waived if repaired)'
    )

    # Also try without double space
    content = content.replace(
        '$4.9 star(Waived if repaired)',
        '$80-$150 (Waived if repaired)'
    )

    # Fix 2: Font size
    content = content.replace(
        'font-size: 4.9  starem',
        'font-size: 0.9rem'
    )

    content = content.replace(
        'font-size: 4.9 starem',
        'font-size: 0.9rem'
    )

    # Save
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed typos: {html_path.name}")
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
    print("FIXING PRICING TABLE TYPOS ON ALL PAGES")
    print("=" * 70 + "\n")

    for page in pages:
        page_path = services_dir / page
        if page_path.exists():
            fix_typos(page_path)

    print("\n" + "=" * 70)
    print("[SUCCESS] All typos fixed")
    print("=" * 70 + "\n")
