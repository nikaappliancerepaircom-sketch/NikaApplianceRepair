#!/usr/bin/env python3
"""
Remove Workiz booking form sections from all pages except book.html
"""
import os
import re
from pathlib import Path

def remove_workiz_section(filepath):
    """Remove the Workiz booking form section from a page"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if Workiz iframe exists
    if 'workiz.com' not in content and 'booking-section-bmad' not in content:
        print(f"[SKIP] {filepath.name} - No booking form found")
        return False

    original_content = content

    # Pattern to match the entire booking section
    # Matches from <section class="booking-section-bmad"> to its closing </section>
    pattern = r'<section[^>]*class="booking-section-bmad"[^>]*>.*?</section>'

    # Remove the section
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Also try to match sections with id="book" that contain workiz
    if 'workiz' in content.lower():
        pattern2 = r'<section[^>]*id="book"[^>]*>.*?workiz\.com.*?</section>'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)

    # Clean up extra whitespace/newlines left behind
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    # Check if anything was removed
    if content == original_content:
        print(f"[WARN] {filepath.name} - Has booking form but couldn't remove it automatically")
        # Show where workiz appears for manual inspection
        for i, line in enumerate(content.split('\n'), 1):
            if 'workiz' in line.lower() or 'booking-section-bmad' in line.lower():
                print(f"  Line {i}: {line[:80]}...")
        return False

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] {filepath.name} - Removed booking form section")
    return True

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("Removing Workiz booking forms from all pages except book.html")
    print("=" * 70)
    print()

    # Files to process
    files_to_process = []

    # Root page
    index_file = base_dir / 'index.html'
    if index_file.exists():
        files_to_process.append(index_file)

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        for file in sorted(services_dir.glob('*.html')):
            files_to_process.append(file)

    # Brand pages
    brands_dir = base_dir / 'brands'
    if brands_dir.exists():
        for file in sorted(brands_dir.glob('*.html')):
            files_to_process.append(file)

    # Location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        for file in sorted(locations_dir.glob('*.html')):
            files_to_process.append(file)

    print(f"Processing {len(files_to_process)} pages...\n")

    removed_count = 0
    skipped_count = 0
    warning_count = 0

    for filepath in files_to_process:
        result = remove_workiz_section(filepath)
        if result:
            removed_count += 1
        elif 'SKIP' in str(result):
            skipped_count += 1
        else:
            warning_count += 1

    print()
    print("=" * 70)
    print(f"✓ COMPLETED: Removed booking forms from {removed_count} pages")
    print(f"  Skipped: {skipped_count} (no form found)")
    if warning_count > 0:
        print(f"  Warnings: {warning_count} (manual inspection needed)")
    print()
    print("  Booking form now ONLY available on /book page")
    print("=" * 70)

if __name__ == '__main__':
    main()
