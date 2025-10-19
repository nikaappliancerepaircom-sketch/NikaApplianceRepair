#!/usr/bin/env python3
"""
Fix ALL encoding issues across multiple HTML files.
This script fixes double UTF-8 encoding systematically.
"""

import os
import sys

def fix_double_encoding(filepath):
    """Fix double UTF-8 encoding in a file."""

    print(f"\n{'='*60}")
    print(f"Processing: {filepath}")
    print(f"{'='*60}")

    # Read as binary
    with open(filepath, 'rb') as f:
        data = f.read()

    original_size = len(data)

    # Map of double-encoded bytes to correct UTF-8
    # These are the most common emoji corruptions
    replacements = {
        # Lightning ⚡ (e2 9a a1)
        b'\xc3\xa2\xc5\xa1\xc2\xa1': b'\xe2\x9a\xa1',

        # Trophy 🏆 (f0 9f 8f 86)
        b'\xc3\xb0\xc5\xb8\xc2\x8f\xe2\x80\xa0': b'\xf0\x9f\x8f\x86',

        # House 🏠 (f0 9f 8f a0)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xb0': b'\xf0\x9f\x8f\xa0',

        # Star ⭐ (e2 ad 90)
        b'\xc3\xa2\xc2\xad\xc2\x90': b'\xe2\xad\x90',

        # Shield 🛡️ (f0 9f 9b a1 ef b8 8f)
        b'\xc3\xb0\xc5\xb8\xe2\x80\xba\xc2\xa1\xc3\xaf\xc2\xb8\xc2\x8f': b'\xf0\x9f\x9b\xa1\xef\xb8\x8f',

        # Wrench 🔧 (f0 9f 94 a7)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xa7': b'\xf0\x9f\x94\xa7',

        # Building 🏢 (f0 9f 8f a2)
        b'\xc3\xb0\xc5\xb8\xc2\x8f\xc2\xa2': b'\xf0\x9f\x8f\xa2',

        # Cooking pot 🥘 (f0 9f a5 98)
        b'\xc3\xb0\xc5\xb8\xc2\xa5\xcb\x9c': b'\xf0\x9f\xa5\x98',

        # Money bag 💰 (f0 9f 92 b0)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xb0': b'\xf0\x9f\x92\xb0',

        # Water drop 💧 (f0 9f 92 a7)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xa7': b'\xf0\x9f\x92\xa7',

        # Checkmark ✓ (e2 9c 93)
        b'\xc3\xa2\xc5\x93\xe2\x80\x9c': b'\xe2\x9c\x93',

        # Dollar 💵 (f0 9f 92 b5)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xb5': b'\xf0\x9f\x92\xb5',

        # Calendar 📅 (f0 9f 93 85)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\x85': b'\xf0\x9f\x93\x85',

        # Technician 👨‍🔧 (f0 9f 91 a8 e2 80 8d f0 9f 94 a7)
        b'\xc3\xb0\xc5\xb8\xe2\x80\x98\xc2\xa8\xc3\xa2\xe2\x82\xac\xc2\x8d\xf0\x9f\x94\xa7':
            b'\xf0\x9f\x91\xa8\xe2\x80\x8d\xf0\x9f\x94\xa7',
    }

    fixes_applied = []

    # Apply each fix
    for garbled, correct in replacements.items():
        if garbled in data:
            count = data.count(garbled)
            data = data.replace(garbled, correct)

            # Decode to get emoji name for display
            try:
                emoji_display = correct.decode('utf-8')
            except:
                emoji_display = correct.hex()

            fixes_applied.append((emoji_display, count))
            print(f"  [OK] Fixed {count}x instances")

    # Write the fixed file
    if fixes_applied:
        with open(filepath, 'wb') as f:
            f.write(data)

        print(f"\n  Total fixes: {len(fixes_applied)} types")
        print(f"  Status: [FIXED]")
        return True
    else:
        print(f"  Status: [Already clean]")
        return False

def main():
    """Fix all broken pages."""

    # Pages with encoding issues
    broken_pages = [
        'king.html',
        'east-gwillimbury.html',
        'scugog.html',
        'brock.html',
        'halton-hills.html',
        'bradford.html',
        'innisfil.html',
        'georgina.html',
        'orangeville.html',
        'uxbridge.html',
        'mono.html',
    ]

    os.chdir('C:\\NikaApplianceRepair\\locations')

    print("\n" + "="*60)
    print("FIXING ALL ENCODING ISSUES - BATCH OPERATION")
    print("="*60)

    fixed_count = 0
    for page in broken_pages:
        if os.path.exists(page):
            if fix_double_encoding(page):
                fixed_count += 1
        else:
            print(f"\n{'='*60}")
            print(f"WARNING: {page} not found!")
            print(f"{'='*60}")

    print("\n" + "="*60)
    print(f"BATCH FIX COMPLETE")
    print(f"  Files processed: {len(broken_pages)}")
    print(f"  Files fixed: {fixed_count}")
    print(f"  Files already clean: {len(broken_pages) - fixed_count}")
    print("="*60)

if __name__ == '__main__':
    main()
