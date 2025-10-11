import os

# All 9 files
files = [
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

# Pattern to remove
old_pattern = '''                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 15px; text-align: center;">Complex Repair</td>
                            <td style="padding: 15px; text-align: center;">$250 - $450</td>
                            <td style="padding: 15px; text-align: center;">90 Days</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px; text-align: center;">Emergency Service</td>
                            <td style="padding: 15px; text-align: center;">+$50 - $100</td>
                            <td style="padding: 15px; text-align: center;">90 Days</td>
                        </tr>'''

new_pattern = '''                        <tr>
                            <td style="padding: 15px; text-align: center;">Complex Repair</td>
                            <td style="padding: 15px; text-align: center;">$250 - $450</td>
                            <td style="padding: 15px; text-align: center;">90 Days</td>
                        </tr>'''

for filename in files:
    filepath = os.path.join(base_path, filename)
    print(f"Processing {filename}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove Emergency Service row
    content = content.replace(old_pattern, new_pattern)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] {filename} - Emergency Service row removed!")

print("\n[SUCCESS] All 8 files updated!")
