#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all relative paths in brand pages for subfolder location."""

import os
import sys
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fix_paths(file_path):
    """Fix all relative paths in a brand page."""
    print(f"\nFixing paths in: {os.path.basename(file_path)}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = []

    # Fix CSS paths
    old = 'href="css/'
    new = 'href="../css/'
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        changes.append(f"CSS paths: {count}")

    # Fix asset image paths
    old = 'src="assets/'
    new = 'src="../assets/'
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        changes.append(f"Asset paths: {count}")

    # Fix JS paths
    old = 'src="js/'
    new = 'src="../js/'
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        changes.append(f"JS paths: {count}")

    # Fix navigation links to other pages
    patterns = [
        ('href="services/', 'href="../services/'),
        ('href="locations/', 'href="../locations/'),
        ('href="about.html"', 'href="../about.html"'),
        ('href="book.html"', 'href="../book.html"'),
        ('href="index.html"', 'href="../index.html"'),
        ('action="submit-form"', 'action="../submit-form"'),
    ]

    for old, new in patterns:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f"{old}: {count}")

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {', '.join(changes)}")
        return True
    else:
        print(f"- No changes needed")
        return False

if __name__ == '__main__':
    file_path = 'brands/samsung-appliance-repair-toronto.html'

    if not os.path.exists(file_path):
        print(f"ERROR: {file_path} not found")
        sys.exit(1)

    print("="*60)
    print("Fixing relative paths in Samsung brand page")
    print("="*60)

    if fix_paths(file_path):
        print("\n" + "="*60)
        print("✓ All paths fixed successfully!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("All paths already correct")
        print("="*60)
