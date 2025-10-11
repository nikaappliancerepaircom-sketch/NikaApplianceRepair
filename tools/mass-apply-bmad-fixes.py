#!/usr/bin/env python3
"""
Mass apply BMAD fixes to all pages:
1. Fix review counts (5,5,5,200+ -> 5,200+)
2. Add rating displays (4.9 ★ format)
3. Add RESPONSIVE TYPOGRAPHY SYSTEM marker
"""

from pathlib import Path
import re

def fix_page(file_path):
    """Apply BMAD fixes to a single page"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # Fix 1: Review count corruptions
    if re.search(r'5,\d,\d{2,3}\+\s*(reviews?|customers?|clients?)', content, re.I):
        content = re.sub(r'5,5,5,200\+\s*(reviews?|customers?|clients?)', r'5,200+ \1', content, flags=re.I)
        content = re.sub(r'5,5,200\+\s*(reviews?|customers?|clients?)', r'5,200+ \1', content, flags=re.I)
        content = re.sub(r'5,\d,\d{2,3}\+\s*(reviews?|customers?|clients?)', r'5,200+ \1', content, flags=re.I)
        changes.append("review counts")

    # Fix 2: Rating displays (4.9/5 -> 4.9 ★)
    if '4.9/5' in content:
        # In hero rating
        content = re.sub(r'4\.9/5 from 5,200\+', r'4.9 ★ from 5,200+', content)
        # In rating display sections
        content = re.sub(r'<div[^>]*>4\.9/5</div>', r'<div style="font-size: 2rem; font-weight: bold; margin-bottom: 10px;">4.9 ★</div>', content)
        changes.append("rating displays")

    # Fix 3: Add RESPONSIVE TYPOGRAPHY SYSTEM marker
    if 'id="responsive-typography"' in content and 'RESPONSIVE TYPOGRAPHY SYSTEM' not in content:
        content = content.replace(
            '<style id="responsive-typography">\n    /* Responsive Typography with clamp() */',
            '<style id="responsive-typography">\n    /* RESPONSIVE TYPOGRAPHY SYSTEM */\n    /* Responsive Typography with clamp() */'
        )
        changes.append("typography marker")

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("MASS APPLYING BMAD FIXES TO ALL PAGES")
    print("=" * 70)
    print("\nApplying:")
    print("  1. Review count fixes")
    print("  2. Rating display format (4.9 star)")
    print("  3. Responsive typography marker")
    print("=" * 70)

    all_files = []

    # Collect all HTML files
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html')])

    print(f"\nProcessing {len(all_files)} files...\n")

    fixed = 0
    for file_path in all_files:
        if not file_path.exists():
            continue

        changes = fix_page(file_path)
        if changes:
            print(f"[FIXED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 70)
    print("\nAll BMAD fixes applied!")

if __name__ == '__main__':
    main()
