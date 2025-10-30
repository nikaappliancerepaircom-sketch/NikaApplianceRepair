#!/usr/bin/env python3
"""
Upgrade blog posts to premium template
Converts posts with inline styles to use external CSS files
"""
import os
import re
from pathlib import Path

def upgrade_post_to_premium_template(filepath):
    """
    Upgrade a single post to use premium blog template
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has premium template
    if 'blog-premium.css' in content and 'blog-wrapper' in content:
        return "SKIP", "Already using premium template"

    # Check if it has external CSS links
    if '<link rel="stylesheet" href="../../css/blog-premium.css">' in content:
        return "SKIP", "Already has external CSS"

    # Add external CSS links if not present
    if '<link rel="stylesheet" href="../../css/blog-premium.css">' not in content:
        # Find where to insert - after Font Awesome link or at end of head
        css_link = '    <!-- Premium Blog Styles -->\n    <link rel="stylesheet" href="../../css/blog-premium.css">\n\n    <!-- Header Styles -->\n    <link rel="stylesheet" href="../../css/header-optimized.css">\n'

        # Try to insert after Font Awesome
        if 'cdnjs.cloudflare.com/ajax/libs/font-awesome' in content:
            pattern = r'(<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+">)'
            content = re.sub(pattern, r'\1\n\n' + css_link, content)
        else:
            # Insert before closing </head>
            content = content.replace('</head>', css_link + '</head>')

    # Wrap body content in blog-wrapper structure if not already wrapped
    if 'blog-wrapper' not in content:
        # Find body and main content
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1)

            # Create wrapper structure
            wrapper_start = '\n    <div class="blog-wrapper">\n        '
            wrapper_end = '\n    </div>\n'

            # Insert wrapper
            new_body = '<body>' + wrapper_start + body_content.strip() + wrapper_end + '</body>'
            content = content[:body_match.start()] + new_body + content[body_match.end():]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return "OK", "Upgraded to premium template"

def main():
    # Posts that need upgrading
    posts_to_upgrade = [
        "appliance-repair-distillery-district.html",
        "appliance-repair-grande-prairie.html",
        "appliance-repair-king-west.html",
        "appliance-repair-peterborough.html",
        "appliance-repair-queen-west.html",
        "appliance-repair-yorkville.html",
        "best-appliance-repair-near-me.html",
        "dishwasher-repair-toronto.html",
        "dryer-repair-toronto.html",
        "emergency-appliance-repair-24-7.html",
        "freezer-repair-guide.html",
        "garbage-disposal-repair.html",
        "ice-maker-repair.html",
        "lg-appliance-repair-service.html",
        "microwave-not-heating.html",
        "microwave-repair-toronto.html",
        "mobile-appliance-repair-whitehorse.html",
        "oven-repair-toronto.html",
        "same-day-appliance-repair.html",
        "samsung-appliance-repair.html",
        "stove-repair-toronto.html",
        "washing-machine-repair-complete-guide.html",
        "water-heater-repair-toronto.html",
        "whirlpool-customer-service-repair.html",
    ]

    base_dir = Path(__file__).parent.parent / "blog" / "troubleshooting"

    print("\n" + "="*70)
    print("UPGRADING BLOG POSTS TO PREMIUM TEMPLATE")
    print("="*70 + "\n")

    success_count = 0
    skip_count = 0

    for filename in posts_to_upgrade:
        filepath = base_dir / filename

        if not filepath.exists():
            print(f"[NOT FOUND] {filename}")
            continue

        try:
            status, message = upgrade_post_to_premium_template(filepath)
            if status == "OK":
                print(f"[OK] {filename}")
                success_count += 1
            else:
                print(f"[SKIP] {filename} - {message}")
                skip_count += 1
        except Exception as e:
            print(f"[ERROR] {filename} - {str(e)}")

    print("\n" + "="*70)
    print(f"Upgraded: {success_count} posts")
    print(f"Skipped: {skip_count} posts")
    print(f"Total: {success_count + skip_count} posts processed")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
