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

# CSS link to add (AFTER responsive-comprehensive.css)
css_link = '    <link rel="stylesheet" href="../css/mobile-strict-fix.css">\n'

for filename in files:
    filepath = os.path.join(base_path, filename)
    print(f"Processing {filename}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if mobile-strict-fix.css is already included
    if 'mobile-strict-fix.css' in content:
        print(f"  [SKIP] {filename} - mobile strict CSS already included")
        continue

    # Find responsive-comprehensive.css and insert AFTER it
    pattern = r'(    <link rel="stylesheet" href="../css/responsive-comprehensive\.css">)\n'

    if re.search(pattern, content):
        # Insert after responsive-comprehensive.css
        new_content = re.sub(
            pattern,
            r'\1\n' + css_link,
            content
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [OK] {filename} - mobile strict CSS added!")
    else:
        print(f"  [WARNING] {filename} - Could not find insertion point")

print("\n[SUCCESS] Mobile strict CSS update completed!")
