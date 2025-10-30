#!/usr/bin/env python3
"""
Verify all blog posts use the premium blog template
"""
import os
from pathlib import Path

def check_post_template(filepath):
    """
    Check if a post uses premium blog template
    Returns: (status, has_css, has_wrapper)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        has_css = 'blog-premium.css' in content
        has_wrapper = 'blog-wrapper' in content

        if has_css and has_wrapper:
            return "OK", True, True
        elif has_css or has_wrapper:
            return "PARTIAL", has_css, has_wrapper
        else:
            return "MISSING", False, False
    except Exception as e:
        return "ERROR", False, False

def main():
    base_dir = Path(__file__).parent.parent / "blog" / "troubleshooting"

    if not base_dir.exists():
        print(f"[ERROR] Directory not found: {base_dir}")
        return

    # Get all HTML files
    html_files = sorted([f for f in base_dir.glob('*.html')])

    print("\n" + "="*80)
    print("BLOG POST TEMPLATE VERIFICATION REPORT")
    print("="*80 + "\n")

    ok_count = 0
    partial_count = 0
    missing_count = 0
    error_count = 0

    ok_posts = []
    partial_posts = []
    missing_posts = []
    error_posts = []

    for filepath in html_files:
        filename = filepath.name
        status, has_css, has_wrapper = check_post_template(filepath)

        if status == "OK":
            print(f"[OK] {filename}")
            ok_count += 1
            ok_posts.append(filename)
        elif status == "PARTIAL":
            css_str = "CSS: Yes" if has_css else "CSS: No"
            wrapper_str = "Wrapper: Yes" if has_wrapper else "Wrapper: No"
            print(f"[PARTIAL] {filename} - {css_str}, {wrapper_str}")
            partial_count += 1
            partial_posts.append((filename, has_css, has_wrapper))
        elif status == "MISSING":
            print(f"[MISSING] {filename}")
            missing_count += 1
            missing_posts.append(filename)
        else:
            print(f"[ERROR] {filename} - Could not read file")
            error_count += 1
            error_posts.append(filename)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total posts checked: {len(html_files)}")
    print(f"  - Complete (CSS + Wrapper): {ok_count}")
    print(f"  - Partial (missing one): {partial_count}")
    print(f"  - Missing (no template): {missing_count}")
    print(f"  - Errors: {error_count}")

    compliance_rate = (ok_count / len(html_files) * 100) if html_files else 0
    print(f"\nTemplate Compliance: {compliance_rate:.1f}%")

    if partial_count > 0:
        print(f"\n[ATTENTION] {partial_count} posts missing either CSS or wrapper:")
        for filename, has_css, has_wrapper in partial_posts:
            missing = []
            if not has_css:
                missing.append("CSS")
            if not has_wrapper:
                missing.append("Wrapper")
            print(f"  - {filename}: Missing {', '.join(missing)}")

    if missing_count > 0:
        print(f"\n[ERROR] {missing_count} posts missing all template elements:")
        for filename in missing_posts:
            print(f"  - {filename}")

    if error_count > 0:
        print(f"\n[ERROR] {error_count} posts could not be read:")
        for filename in error_posts:
            print(f"  - {filename}")

    print("\n" + "="*80)
    if ok_count == len(html_files):
        print("STATUS: ALL POSTS COMPLIANT [100% COMPLIANCE]")
        print("="*80 + "\n")
        return True
    else:
        print("STATUS: ISSUES FOUND - MANUAL REVIEW REQUIRED")
        print("="*80 + "\n")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
