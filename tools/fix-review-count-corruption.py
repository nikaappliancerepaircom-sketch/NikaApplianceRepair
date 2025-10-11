#!/usr/bin/env python3
"""
Fix corrupted review counts from 5,5,5,200+ or 5,5,200+ to 5,200+
This fixes the data consistency BMAD test failure.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def fix_corrupted_review_counts(file_path):
    """Fix malformed review counts like 5,5,5,200+ to 5,200+"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix corrupted patterns
    original = content

    # Pattern 1: 5,5,5,200+ reviews/customers/clients
    content = re.sub(r'\b5,5,5,200\+\s*(reviews?|customers?|clients?)', r'5,200+ \1', content, flags=re.I)

    # Pattern 2: 5,5,200+ reviews/customers/clients
    content = re.sub(r'\b5,5,200\+\s*(reviews?|customers?|clients?)', r'5,200+ \1', content, flags=re.I)

    # Pattern 3: Any other malformed 5,x,xxx+ patterns
    content = re.sub(r'\b5,\d,\d{2,3}\+\s*(reviews?|customers?|clients?)', r'5,200+ \1', content, flags=re.I)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING CORRUPTED REVIEW COUNTS")
    print("=" * 70)
    print("\nFixing patterns like:")
    print("  - 5,5,5,200+ to 5,200+")
    print("  - 5,5,200+ to 5,200+")
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

        if fix_corrupted_review_counts(file_path):
            print(f"[FIXED] {file_path.name}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} files")
    print("=" * 70)
    print("\nData consistency issue resolved!")

if __name__ == '__main__':
    main()
