#!/usr/bin/env python3
"""
Unify Countdown Timer Component Across All Pages
This script standardizes the countdown timer HTML across all pages of the website.

Author: Claude Code
Date: 2025-10-20
"""

import os
import re
from pathlib import Path

# Define the unified countdown timer HTML
# This is the ONE consistent timer that will be used everywhere
UNIFIED_TIMER = '''    <!-- Unified Countdown Timer -->
    <section class="countdown-section">
        <div class="container">
            <h2 class="countdown-title">Book Online & Save $40 on Any Service</h2>
            <p class="countdown-label">DEAL ENDS IN</p>
            <div class="countdown-timer">
                <div class="timer-box">
                    <div class="timer-value countdown-minutes" id="timer-minutes">14</div>
                    <div class="timer-label">MINUTES</div>
                </div>
                <div class="timer-box">
                    <div class="timer-value countdown-seconds" id="timer-seconds">45</div>
                    <div class="timer-label">SECONDS</div>
                </div>
            </div>
            <a href="LINK_PLACEHOLDER" class="countdown-cta">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                </svg>
                CLICK TO BOOK DIAGNOSTIC NOW
            </a>
        </div>
    </section>
'''

def find_countdown_section(content):
    """Find the countdown section in HTML content."""
    # Pattern to match the entire countdown section
    pattern = r'<!-- .*?[Cc]ountdown.*?-->\s*<section class="countdown-section">.*?</section>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(0), match.start(), match.end()

    # Try without comment
    pattern = r'<section class="countdown-section">.*?</section>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(0), match.start(), match.end()

    return None, None, None

def determine_link(file_path):
    """Determine the correct link for the CTA button based on file location."""
    file_path = Path(file_path)

    # Homepage
    if file_path.name == 'index.html' and file_path.parent.name == 'NikaApplianceRepair':
        return '#book'

    # Subdirectory pages (services, locations, brands)
    if file_path.parent.name in ['services', 'locations', 'brands']:
        return '../book.html'

    # Default
    return '../book.html'

def unify_timer(file_path):
    """Replace the countdown timer in a file with the unified version."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find existing countdown section
        old_timer, start, end = find_countdown_section(content)

        if old_timer is None:
            return False, "No countdown timer found"

        # Determine the correct link
        link = determine_link(file_path)
        unified_timer = UNIFIED_TIMER.replace('LINK_PLACEHOLDER', link)

        # Replace the old timer with unified timer
        new_content = content[:start] + unified_timer + content[end:]

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, "Timer unified successfully"

    except Exception as e:
        return False, f"Error: {str(e)}"

def process_directory(directory):
    """Process all HTML files in a directory."""
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }

    directory = Path(directory)

    for html_file in directory.glob('*.html'):
        success, message = unify_timer(html_file)

        if success:
            results['success'].append((str(html_file), message))
            print(f"[OK] {html_file.name}: {message}")
        elif "No countdown timer found" in message:
            results['skipped'].append((str(html_file), message))
            print(f"[SKIP] {html_file.name}: {message}")
        else:
            results['failed'].append((str(html_file), message))
            print(f"[FAIL] {html_file.name}: {message}")

    return results

def main():
    """Main function to unify timers across all pages."""
    base_dir = Path(__file__).parent

    print("=" * 80)
    print("UNIFIED COUNTDOWN TIMER DEPLOYMENT")
    print("=" * 80)
    print()
    print("This script will replace ALL countdown timers with ONE consistent design:")
    print("  - Timer: 14:45 (synced across all pages)")
    print("  - Title: 'Book Online & Save $40 on Any Service'")
    print("  - Labels: UPPERCASE (MINUTES, SECONDS)")
    print("  - CTA: Consistent button with calendar icon")
    print()

    all_results = {
        'success': [],
        'failed': [],
        'skipped': []
    }

    # Process homepage
    print("\n" + "=" * 80)
    print("PROCESSING: Homepage")
    print("=" * 80)
    homepage = base_dir / 'index.html'
    if homepage.exists():
        success, message = unify_timer(homepage)
        if success:
            all_results['success'].append((str(homepage), message))
            print(f"[OK] index.html: {message}")
        else:
            print(f"[FAIL] index.html: {message}")

    # Process services pages
    print("\n" + "=" * 80)
    print("PROCESSING: Services Pages")
    print("=" * 80)
    services_dir = base_dir / 'services'
    if services_dir.exists():
        results = process_directory(services_dir)
        all_results['success'].extend(results['success'])
        all_results['failed'].extend(results['failed'])
        all_results['skipped'].extend(results['skipped'])

    # Process location pages
    print("\n" + "=" * 80)
    print("PROCESSING: Location Pages")
    print("=" * 80)
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        results = process_directory(locations_dir)
        all_results['success'].extend(results['success'])
        all_results['failed'].extend(results['failed'])
        all_results['skipped'].extend(results['skipped'])

    # Process brand pages
    print("\n" + "=" * 80)
    print("PROCESSING: Brand Pages")
    print("=" * 80)
    brands_dir = base_dir / 'brands'
    if brands_dir.exists():
        results = process_directory(brands_dir)
        all_results['success'].extend(results['success'])
        all_results['failed'].extend(results['failed'])
        all_results['skipped'].extend(results['skipped'])

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"[OK] Successfully unified: {len(all_results['success'])} files")
    print(f"[FAIL] Failed: {len(all_results['failed'])} files")
    print(f"[SKIP] Skipped (no timer): {len(all_results['skipped'])} files")
    print()

    if all_results['failed']:
        print("\nFailed files:")
        for file_path, message in all_results['failed']:
            print(f"  - {file_path}: {message}")

    print("\n" + "=" * 80)
    print("TIMER UNIFICATION COMPLETE!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Test the timer on different pages")
    print("2. Verify timer syncs across pages (uses localStorage)")
    print("3. Check mobile responsiveness")
    print("4. Ensure countdown-timer.js is loaded on all pages")
    print()

if __name__ == '__main__':
    main()
