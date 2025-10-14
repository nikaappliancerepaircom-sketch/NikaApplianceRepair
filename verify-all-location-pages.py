#!/usr/bin/env python3
"""Verify actual content word count for ALL location pages (auto-detects)"""

import re
from bs4 import BeautifulSoup
import os
import glob

def count_content_words(html_file):
    """Count words in visible content only"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style', 'head']):
        script.decompose()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading/trailing space
    lines = (line.strip() for line in text.splitlines())

    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # Remove blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)

    # Count words
    words = text.split()
    return len(words)

def count_location_mentions(html_file, location_name):
    """Count location mentions"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(re.findall(rf'\b{location_name}\b', content, re.IGNORECASE))

def extract_location_name(filename):
    """Extract location name from filename (e.g. 'richmond-hill.html' -> 'Richmond Hill')"""
    # Remove .html extension
    name = filename.replace('.html', '')

    # Convert hyphens to spaces and title case
    location = name.replace('-', ' ').title()

    return location

if __name__ == '__main__':
    base_path = r'C:\NikaApplianceRepair\locations'

    # Auto-detect ALL .html files in locations folder
    all_files = glob.glob(os.path.join(base_path, '*.html'))

    # Filter out backup files
    location_files = [f for f in all_files if 'backup' not in f.lower() and 'test' not in f.lower()]

    # Sort alphabetically
    location_files.sort()

    if not location_files:
        print("ERROR: No location pages found in locations folder!")
        exit(1)

    print("=" * 80)
    print(f"WORD COUNT VERIFICATION - ALL LOCATION PAGES ({len(location_files)} found)")
    print("=" * 80)
    print(f"\n{'Location':<25} {'Words':<10} {'Status':<20} {'Mentions':<10}")
    print("-" * 80)

    total_words = 0
    results = []

    for file_path in location_files:
        filename = os.path.basename(file_path)
        location_name = extract_location_name(filename)

        try:
            word_count = count_content_words(file_path)
            mentions = count_location_mentions(file_path, location_name)
            total_words += word_count

            if 2000 <= word_count <= 2500:
                status = "OPTIMAL"
            elif word_count < 2000:
                status = f"{2000 - word_count} below"
            else:
                status = f"{word_count - 2500} above"

            print(f"{location_name:<25} {word_count:>6,}    {status:<20} {mentions:>4}")
            results.append((location_name, word_count, mentions))
        except Exception as e:
            print(f"{location_name:<25} ERROR: {str(e)}")

    print("-" * 80)
    if results:
        print(f"{'AVERAGE':<25} {total_words // len(results):>6,}")
    print("=" * 80)

    # Summary
    if results:
        print("\nSUMMARY:")
        total_pages = len(results)
        optimal = sum(1 for _, wc, _ in results if 2000 <= wc <= 2500)
        below = sum(1 for _, wc, _ in results if wc < 2000)
        above = sum(1 for _, wc, _ in results if wc > 2500)

        print(f"  Optimal (2000-2500): {optimal}/{total_pages} pages")
        print(f"  Below target (<2000): {below}/{total_pages} pages")
        print(f"  Above target (>2500): {above}/{total_pages} pages")

        if optimal == total_pages:
            print(f"\nSUCCESS: ALL {total_pages} PAGES WITHIN TARGET RANGE!")
        else:
            print(f"\nWARNING: {total_pages - optimal} pages need adjustment")
    else:
        print("\nERROR: No pages were successfully analyzed")

    print("=" * 80)
