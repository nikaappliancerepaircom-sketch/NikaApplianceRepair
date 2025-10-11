import os
import re

# All 9 files
files = [
    'refrigerator-repair.html',
    'dishwasher-repair.html',
    'washer-repair.html',
    'dryer-repair.html',
    'freezer-repair.html',
    'stove-repair.html',
    'oven-repair.html',
    'range-repair.html',
    'microwave-repair.html'
]

base_path = 'C:\\NikaApplianceRepair\\services'

# CSS link to add (AFTER mobile-strict-fix.css - LAST!)
css_link = '    <link rel="stylesheet" href="../css/no-scrollbars-fix.css">\n'

for filename in files:
    filepath = os.path.join(base_path, filename)
    print(f"Processing {filename}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if no-scrollbars-fix.css is already included
    if 'no-scrollbars-fix.css' in content:
        print(f"  [SKIP] {filename} - no-scrollbars CSS already included")
        continue

    # Find mobile-strict-fix.css and insert AFTER it (LAST CSS FILE!)
    pattern = r'(    <link rel="stylesheet" href="../css/mobile-strict-fix\.css">)\n'

    if re.search(pattern, content):
        # Insert after mobile-strict-fix.css
        new_content = re.sub(
            pattern,
            r'\1\n' + css_link,
            content
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [OK] {filename} - no-scrollbars CSS added!")
    else:
        print(f"  [WARNING] {filename} - Could not find insertion point")

print("\n[SUCCESS] No-scrollbars CSS update completed!")
print("\nFINAL CSS loading order:")
print("1. style.css")
print("2. video-custom.css")
print("3. video-modern.css")
print("4. how-it-works-modern.css")
print("5. about-redesign.css")
print("6. responsive-comprehensive.css")
print("7. desktop-tablet-optimization.css")
print("8. mobile-strict-fix.css")
print("9. no-scrollbars-fix.css <- LAST (removes all scrollbars)")
