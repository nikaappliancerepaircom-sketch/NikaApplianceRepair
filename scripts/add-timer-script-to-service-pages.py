#!/usr/bin/env python3
"""
Add countdown-timer.js script to all service pages
"""
import os
import re

# Service pages to update
service_pages = [
    'dishwasher-repair.html',
    'dryer-repair.html',
    'freezer-repair.html',
    'microwave-repair.html',
    'oven-repair.html',
    'range-repair.html',
    'refrigerator-repair.html',
    'stove-repair.html',
    'washer-repair.html',
]

def add_countdown_script(filepath):
    """Add countdown-timer.js script to the service page"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if script is already added
    if 'countdown-timer.js' in content:
        print(f"[OK] {os.path.basename(filepath)} - Already has countdown-timer.js")
        return False

    # Pattern to find the closing year script before </body>
    pattern = r'(<script>\s*//\s*Set current year in footer\s*\n\s*document\.getElementById\([\'"]current-year-footer[\'"]\)\.textContent = new Date\(\)\.getFullYear\(\);\s*\n\s*</script>\s*\n</body>)'

    # Replacement with countdown script added
    replacement = r'''<!-- JavaScript -->
    <script src="../js/countdown-timer.js" defer></script>

    \1'''

    # Replace
    new_content = re.sub(pattern, replacement, content)

    if new_content == content:
        print(f"[ERROR] {os.path.basename(filepath)} - Pattern not found!")
        return False

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] {os.path.basename(filepath)} - Added countdown-timer.js script")
    return True

def main():
    """Main function"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    services_dir = os.path.join(base_dir, 'services')

    print("Adding countdown-timer.js script to service pages...\n")

    updated_count = 0
    for page in service_pages:
        filepath = os.path.join(services_dir, page)
        if os.path.exists(filepath):
            if add_countdown_script(filepath):
                updated_count += 1
        else:
            print(f"[ERROR] {page} - File not found!")

    print(f"\n{updated_count} pages updated successfully!")

if __name__ == '__main__':
    main()
