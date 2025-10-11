#!/usr/bin/env python3
"""
Fix location paths on index.html
Should be /locations/ not ../locations/
"""

import re
from pathlib import Path

def fix_index_paths():
    index_file = Path(__file__).parent.parent / 'index.html'

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix header dropdown paths
    content = content.replace('href="../locations/', 'href="/locations/')

    # Fix footer paths
    content = re.sub(r'href="\.\./locations/', 'href="/locations/', content)

    if content != original:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("[FIXED] index.html - Updated location paths from ../locations/ to /locations/")
        return True
    else:
        print("[OK] index.html - Paths already correct")
        return False

if __name__ == '__main__':
    fix_index_paths()
