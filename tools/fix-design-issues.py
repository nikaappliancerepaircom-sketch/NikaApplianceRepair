#!/usr/bin/env python3
"""
Fix Design Issues:
1. Remove sections that don't match design (sliding left, bad colors)
2. Fix blue text on blue background
3. Remove added sections that break layout
"""

from pathlib import Path
from bs4 import BeautifulSoup

def fix_design_issues(file_path):
    """Remove poorly designed sections and fix color issues"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    changes = []

    # 1. Remove voice-optimized-qa (yellow box with bad contrast)
    voice_qa = soup.find('div', class_='voice-optimized-qa')
    if voice_qa:
        voice_qa.decompose()
        changes.append("removed voice-qa yellow box")

    # 2. Remove conversational-content (extra text)
    conv_content = soup.find('div', class_='conversational-content')
    if conv_content:
        conv_content.decompose()
        changes.append("removed conversational text")

    # 3. Remove enhanced-local-info (blue box on blue background)
    local_info = soup.find('div', class_='enhanced-local-info')
    if local_info:
        local_info.decompose()
        changes.append("removed local info blue box")

    # 4. Remove location-specific-content (extra content)
    loc_specific = soup.find('div', class_='location-specific-content')
    if loc_specific:
        loc_specific.decompose()
        changes.append("removed location-specific content")

    # 5. Remove service-benefits-list (may be causing issues)
    benefits_list = soup.find('div', class_='service-benefits-list')
    if benefits_list:
        benefits_list.decompose()
        changes.append("removed benefits list")

    # 6. Fix pricing table background
    pricing_table = soup.find('table', class_='pricing-table')
    if pricing_table:
        # Change table background to white
        table_div = pricing_table.parent
        if table_div and 'margin: 40px 0' in str(table_div.get('style', '')):
            # Add proper background
            current_style = table_div.get('style', '')
            if 'background' not in current_style:
                table_div['style'] = current_style + '; background: white; padding: 20px; border-radius: 12px;'
                changes.append("fixed pricing table background")

    # 7. Remove service images that may not exist
    service_images = soup.find('div', class_='service-images')
    if service_images:
        service_images.decompose()
        changes.append("removed service images placeholder")

    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes

    return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("FIXING DESIGN ISSUES")
    print("=" * 70)
    print("\nRemoving sections that break design:")
    print("  - Yellow box with bad contrast")
    print("  - Blue text on blue background")
    print("  - Extra content sections")
    print("  - Non-existent image placeholders")
    print("=" * 70)

    all_files = []
    for subdir in ['services', 'locations']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html')])

    print(f"\nProcessing {len(all_files)} pages...\n")

    fixed = 0
    for file_path in all_files:
        changes = fix_design_issues(file_path)
        if changes:
            print(f"[FIXED] {file_path.name}: {', '.join(changes)}")
            fixed += 1

    print("\n" + "=" * 70)
    print(f"FIXED: {fixed}/{len(all_files)} pages")
    print("=" * 70)
    print("\nDesign issues resolved!")

if __name__ == '__main__':
    main()
