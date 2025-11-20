"""Fix picture tag mismatches - make srcset and img src both use slug-based WebP"""
import re
from pathlib import Path

blog_dir = Path('C:/NikaApplianceRepair/blog')
fixed_count = 0

for category in ['guides', 'maintenance', 'troubleshooting']:
    category_path = blog_dir / category
    if not category_path.exists():
        continue

    for html_file in category_path.glob('*.html'):
        if html_file.name == 'index.html':
            continue

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Find all picture elements and fix them
        def fix_picture(match):
            picture_block = match.group(0)

            # Extract img src (the correct slug-based filename)
            img_match = re.search(r'<img[^>]+src="([^"]+)"', picture_block)
            if img_match:
                correct_image = img_match.group(1)

                # Update srcset to match img src
                fixed_block = re.sub(
                    r'srcset="[^"]+"',
                    f'srcset="{correct_image}"',
                    picture_block
                )
                return fixed_block

            return picture_block

        # Fix all picture blocks
        content = re.sub(
            r'<picture>.*?</picture>',
            fix_picture,
            content,
            flags=re.DOTALL
        )

        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Fixed: {category}/{html_file.name}")
            fixed_count += 1
        else:
            print(f"  Skipped: {category}/{html_file.name}")

print(f"\n[DONE] Fixed {fixed_count} blog posts")
