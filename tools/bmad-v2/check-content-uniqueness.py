#!/usr/bin/env python3
"""
Check content uniqueness across all service pages
Detects duplicate content between pages
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


def extract_main_content(html_file):
    """Extract main text content from HTML"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Remove scripts and styles
        text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Extract text
        soup = BeautifulSoup(text, 'html.parser')

        # Get main content (skip header/footer)
        main = soup.find('main')
        if main:
            content = main.get_text(separator=' ', strip=True)
        else:
            content = soup.get_text(separator=' ', strip=True)

        # Clean up whitespace
        content = ' '.join(content.split())

        return content
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return ""


def calculate_similarity(text1, text2):
    """Calculate similarity percentage between two texts"""
    return SequenceMatcher(None, text1, text2).ratio() * 100


def find_duplicate_phrases(text1, text2, min_length=100):
    """Find duplicate phrases between two texts"""
    duplicates = []

    # Split into sentences
    sentences1 = re.split(r'[.!?]+', text1)
    sentences2 = re.split(r'[.!?]+', text2)

    for s1 in sentences1:
        s1 = s1.strip()
        if len(s1) < min_length:
            continue

        for s2 in sentences2:
            s2 = s2.strip()
            if len(s2) < min_length:
                continue

            # Check if highly similar
            similarity = SequenceMatcher(None, s1, s2).ratio()
            if similarity > 0.8:  # 80% similar
                duplicates.append((s1[:100] + '...' if len(s1) > 100 else s1, similarity * 100))

    return duplicates


def main():
    """Check content uniqueness"""
    print("\n" + "=" * 80)
    print("CONTENT UNIQUENESS CHECK - ALL SERVICE PAGES")
    print("=" * 80)
    print()

    services_dir = Path(__file__).parent.parent.parent / "services"
    service_pages = [
        "refrigerator-repair.html",
        "dishwasher-repair.html",
        "washer-repair.html",
        "dryer-repair.html",
        "oven-repair.html",
        "freezer-repair.html"
    ]

    # Extract content from all pages
    pages_content = {}

    for page in service_pages:
        page_path = services_dir / page
        if page_path.exists():
            content = extract_main_content(page_path)
            if content:
                pages_content[page] = content
                print(f"[OK] {page} - {len(content)} characters")

    print()
    print("=" * 80)
    print("SIMILARITY MATRIX")
    print("=" * 80)
    print()

    # Compare all pages
    pages_list = list(pages_content.keys())

    # Print header
    print(f"{'Page':<30}", end='')
    for p in pages_list:
        print(f"{p[:15]:<16}", end='')
    print()
    print("-" * 80)

    # Print similarity matrix
    issues_found = []

    for i, page1 in enumerate(pages_list):
        print(f"{page1:<30}", end='')

        for j, page2 in enumerate(pages_list):
            if i == j:
                print(f"{'100.0%':<16}", end='')
            else:
                similarity = calculate_similarity(pages_content[page1], pages_content[page2])
                print(f"{similarity:.1f}%{' ':11}", end='')

                # Flag high similarity
                if similarity > 70 and i < j:  # Only check upper triangle
                    issues_found.append({
                        'page1': page1,
                        'page2': page2,
                        'similarity': similarity
                    })
        print()

    print()

    # Report issues
    if issues_found:
        print("=" * 80)
        print("DUPLICATE CONTENT DETECTED")
        print("=" * 80)
        print()

        for issue in sorted(issues_found, key=lambda x: x['similarity'], reverse=True):
            print(f"[WARNING] {issue['page1']} <-> {issue['page2']}")
            print(f"          Similarity: {issue['similarity']:.1f}%")

            # Find specific duplicate phrases
            duplicates = find_duplicate_phrases(
                pages_content[issue['page1']],
                pages_content[issue['page2']]
            )

            if duplicates:
                print(f"          Found {len(duplicates)} duplicate phrases:")
                for dup, sim in duplicates[:3]:  # Show first 3
                    print(f"            - \"{dup}\" ({sim:.0f}% match)")
            print()
    else:
        print("=" * 80)
        print("[SUCCESS] All pages have unique content!")
        print("=" * 80)

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Pages checked: {len(pages_content)}")

    if issues_found:
        print(f"Issues found: {len(issues_found)}")
        print("\n[ACTION REQUIRED] Content needs differentiation")
        print("Recommendation: Rewrite duplicate sections to be unique for each appliance type")
    else:
        print("Issues found: 0")
        print("\n[SUCCESS] All content is unique")

    print("=" * 80)


if __name__ == "__main__":
    main()
