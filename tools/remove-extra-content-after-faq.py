#!/usr/bin/env python3
"""
Remove ALL extra content that was added between FAQ section and Footer
Keep only original template design
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

def remove_content_between_faq_and_footer(file_path):
    """Remove all content between FAQ section closing tag and Footer opening tag"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the pattern: </section><!-- FAQ --> ... <!-- Footer -->
        # We want to remove everything between these two markers

        # Pattern to match:
        # 1. Closing FAQ section tag
        # 2. Any content (including comments)
        # 3. Footer comment (but keep it)

        # Use regex to find and remove content between FAQ and Footer
        pattern = r'(</section>\s*(?:<!--\s*FAQ.*?-->\s*)?)(.*?)(<!--\s*Footer\s*-->)'

        def replacement(match):
            # Keep the FAQ section closing, remove middle content, keep Footer comment
            return match.group(1) + '\n' + match.group(3)

        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

        # Check if anything was removed
        if new_content != content and len(new_content) < len(content):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            removed = len(content) - len(new_content)
            print(f"[CLEANED] {file_path.name} - Removed {removed} chars")
            return True
        else:
            print(f"[OK] {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("REMOVING EXTRA CONTENT AFTER FAQ")
    print("=" * 60)
    print("\nRemoving all added content between FAQ and Footer...")
    print("Keeping only original template design")
    print("=" * 60)

    # Get all HTML files
    all_files = []

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    cleaned = 0
    total_removed = 0

    for file_path in all_files:
        if remove_content_between_faq_and_footer(file_path):
            cleaned += 1

    print("\n" + "=" * 60)
    print(f"CLEANED: {cleaned}/{len(all_files)} files")
    print("=" * 60)
    print("\nNow pages have only ORIGINAL template design!")
    print("FAQ -> Footer (no extra content)")

if __name__ == '__main__':
    main()
