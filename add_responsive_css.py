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

# CSS link to add
css_link = '    <link rel="stylesheet" href="../css/responsive-comprehensive.css">\n'

# Find where to insert (after other CSS links, before </head>)
for filename in files:
    filepath = os.path.join(base_path, filename)
    print(f"Processing {filename}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if responsive-comprehensive.css is already included
    if 'responsive-comprehensive.css' in content:
        print(f"  [SKIP] {filename} - responsive CSS already included")
        continue

    # Find the last CSS link before </head>
    # Insert after about-redesign.css or the last CSS file
    pattern = r'(    <link rel="stylesheet" href="../css/about-redesign\.css">)\n'

    if re.search(pattern, content):
        # Insert after about-redesign.css
        new_content = re.sub(
            pattern,
            r'\1\n' + css_link,
            content
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [OK] {filename} - responsive CSS added!")
    else:
        print(f"  [WARNING] {filename} - Could not find insertion point")

print("\n[SUCCESS] Responsive CSS update completed!")
