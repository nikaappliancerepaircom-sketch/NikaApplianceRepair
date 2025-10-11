#!/usr/bin/env python3
"""
Remove ALL junk content between <!-- Footer --> comment and <footer> tag
This is the content I added without section wrappers
"""

from pathlib import Path
import re

def remove_junk_between_comment_and_footer(file_path):
    """Remove all content between <!-- Footer --> and <footer>"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Pattern: <!-- Footer --> ... <footer
        # Remove everything in between
        pattern = r'(<!--\s*Footer\s*-->)(.*?)(<footer)'

        def replacement(match):
            # Keep Footer comment and footer tag, remove junk in between
            return match.group(1) + '\n' + match.group(3)

        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

        if new_content != original:
            # Calculate removed characters
            removed = len(original) - len(new_content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"[CLEANED] {file_path.name} - Removed {removed:,} chars of junk")
            return True
        else:
            print(f"[OK] {file_path.name} - No junk found")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("REMOVING JUNK CONTENT BETWEEN FAQ AND FOOTER")
    print("=" * 70)
    print("\nRemoving ALL content I added between <!-- Footer --> and <footer>")
    print("This will restore ORIGINAL template: FAQ -> Footer (no junk!)")
    print("=" * 70)

    # Get all HTML files
    all_files = []

    for subdir in ['services', 'locations', 'blog']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

    if not all_files:
        print("\n[ERROR] No files found!")
        return

    cleaned = 0
    total_removed = 0

    print(f"\nProcessing {len(all_files)} files...\n")

    for file_path in all_files:
        result = remove_junk_between_comment_and_footer(file_path)
        if result:
            cleaned += 1

    print("\n" + "=" * 70)
    print(f"CLEANED: {cleaned}/{len(all_files)} files")
    print("=" * 70)
    print("\nStructure now: Hero -> ... -> FAQ -> FOOTER")
    print("(No junk content!)")

if __name__ == '__main__':
    main()
