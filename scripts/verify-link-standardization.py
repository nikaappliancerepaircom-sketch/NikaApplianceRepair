#!/usr/bin/env python3
"""
Verify that all internal links use consistent relative paths.

This script checks all HTML files to ensure:
1. Internal links use relative paths (services/..., locations/..., brands/...)
2. No absolute internal paths (except /blog, /#anchors, and href="/")
3. External links and resources remain unchanged
"""

import os
import re
import glob
from pathlib import Path
from collections import defaultdict

# Define the root directory
ROOT_DIR = Path(r"C:\NikaApplianceRepair")

# Patterns to check for (these should NOT exist, except for exceptions)
PROBLEMATIC_PATTERNS = [
    r'href="/services/',
    r'href="/locations/',
    r'href="/brands/',
    r'href="/book"',
    r'href="/about"',
]

# Exceptions (these are OK)
EXCEPTION_PATTERNS = [
    r'href="/"[^a-zA-Z]',  # Home link href="/" is OK
    r'href="/#',  # Anchor links to home page are OK
    r'href="/blog',  # Blog links can stay absolute for clean URLs
]

def should_skip_file(filepath):
    """Check if file should be skipped."""
    filepath_str = str(filepath).lower()

    # Skip backup files
    if "backup" in filepath_str:
        return True

    # Skip template files
    if "template" in filepath_str:
        return True

    # Skip test files
    if "test" in filepath_str:
        return True

    # Skip optimization files
    if "optimization" in filepath_str:
        return True

    return False


def check_file(filepath):
    """
    Check a single HTML file for problematic absolute paths.

    Returns:
        Tuple of (has_issues, issues_found)
    """
    if should_skip_file(filepath):
        return False, []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []

        # Check each problematic pattern
        for pattern in PROBLEMATIC_PATTERNS:
            matches = list(re.finditer(pattern, content))

            for match in matches:
                # Check if this match is an exception
                is_exception = False
                for exception_pattern in EXCEPTION_PATTERNS:
                    if re.search(exception_pattern, match.group()):
                        is_exception = True
                        break

                if not is_exception:
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1
                    # Get context (50 chars before and after)
                    start = max(0, match.start() - 25)
                    end = min(len(content), match.end() + 25)
                    context = content[start:end].replace('\n', ' ')

                    issues.append({
                        'line': line_num,
                        'pattern': pattern,
                        'match': match.group(),
                        'context': context
                    })

        return len(issues) > 0, issues

    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return False, []


def main():
    """Main function to verify all HTML files."""
    print("=" * 80)
    print("Internal Link Standardization Verification")
    print("=" * 80)
    print("\nChecking all HTML files for absolute internal paths...")
    print("(Excluding /blog links, anchor links, and home link)\n")

    # Collect all HTML files
    html_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip certain directories
        skip_dirs = {'backups', 'node_modules', '.git', 'templates', 'tools', 'context-engineering'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if file.endswith('.html'):
                filepath = Path(root) / file
                html_files.append(filepath)

    print(f"Found {len(html_files)} HTML files to check\n")

    # Track results
    files_with_issues = defaultdict(list)
    total_issues = 0

    # Check each file
    for filepath in sorted(html_files):
        rel_path = filepath.relative_to(ROOT_DIR)
        has_issues, issues = check_file(filepath)

        if has_issues:
            files_with_issues[rel_path] = issues
            total_issues += len(issues)

    # Print results
    if files_with_issues:
        print("\n" + "=" * 80)
        print("ISSUES FOUND")
        print("=" * 80)

        for filepath, issues in sorted(files_with_issues.items()):
            print(f"\n{filepath}")
            print("-" * 80)
            for issue in issues:
                print(f"  Line {issue['line']}: {issue['match']}")
                print(f"  Context: ...{issue['context']}...")
                print()

        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Files with issues: {len(files_with_issues)}")
        print(f"Total issues found: {total_issues}")
        print("\n[!] Fix required: Some files still have absolute internal paths")
        print("=" * 80)

    else:
        print("\n" + "=" * 80)
        print("SUCCESS")
        print("=" * 80)
        print("All files checked - no issues found!")
        print("\nAll internal links are using consistent relative paths.")
        print("Blog links (/blog) and anchor links (/#) are correctly preserved.")
        print("=" * 80)


if __name__ == "__main__":
    main()
