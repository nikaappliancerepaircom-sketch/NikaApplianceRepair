#!/usr/bin/env python3
"""
Validate all pages by checking HTML content
"""

from pathlib import Path
import re

def validate_page(file_path):
    """Validate page HTML"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Check 1: $119 in pricing table
    if '<td' in content and 'Diagnostic Fee' in content:
        if '$119' not in content:
            issues.append("Missing $119 in pricing")

    # Check 2: Hero image path
    if '../assets/images/friendly-technician-character.png' not in content:
        if 'hero-section' in content:
            issues.append("Wrong hero image path")

    # Check 3: Check for $89 (should not exist)
    if '$89' in content and 'Waived' in content:
        issues.append("Still has $89 pricing")

    # Check 4: 4.9 rating with star
    if '4.9' in content:
        if '4.9 ★' not in content and '4.9 ⭐' not in content:
            issues.append("Missing star rating format")

    # Check 5: Review count 5,200+
    if '5,200+' not in content and '5200' not in content:
        issues.append("Missing review count")

    return issues

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("VALIDATING ALL PAGES")
    print("=" * 70)

    all_files = []

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        all_files.extend([f for f in services_dir.glob('*.html') if f.name != 'index.html'])

    # Location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        all_files.extend([f for f in locations_dir.glob('*.html') if f.name != 'index.html'])

    print(f"\nValidating {len(all_files)} pages...\n")

    passed = 0
    failed = 0
    all_issues = {}

    for file_path in all_files:
        issues = validate_page(file_path)

        if issues:
            failed += 1
            all_issues[file_path.name] = issues
            print(f"[FAIL] {file_path.name}: {', '.join(issues)}")
        else:
            passed += 1
            print(f"[PASS] {file_path.name}")

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} PASSED, {failed} FAILED")
    print("=" * 70)

    if all_issues:
        print("\nPages with issues:")
        for page, issues in all_issues.items():
            print(f"  {page}:")
            for issue in issues:
                print(f"    - {issue}")

if __name__ == '__main__':
    main()
