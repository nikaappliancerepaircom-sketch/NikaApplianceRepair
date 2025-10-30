#!/usr/bin/env python3
"""
Check for multiple H1 tags on each page
"""
import re
from pathlib import Path

def count_h1_tags(filepath):
    """Count H1 tags in a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(re.findall(r'<h1', content))

blog_base = Path("blog")
issues = []

for folder in ["maintenance", "troubleshooting", "guides"]:
    folder_path = blog_base / folder
    if not folder_path.exists():
        continue

    for filepath in sorted(folder_path.glob('*.html')):
        h1_count = count_h1_tags(filepath)
        if h1_count > 1:
            issues.append((filepath.name, h1_count))
        elif h1_count == 0:
            issues.append((filepath.name, 0))

print("\n" + "="*80)
print("H1 TAG COUNT CHECK")
print("="*80 + "\n")

if not issues:
    print("All posts have exactly 1 H1 tag. Good!\n")
else:
    print("Issues found:\n")
    for filename, count in issues:
        if count == 0:
            print(f"  {filename}: NO H1 TAGS")
        else:
            print(f"  {filename}: {count} H1 TAGS (should be 1)")
    print()

print("="*80 + "\n")
