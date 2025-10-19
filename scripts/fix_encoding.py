#!/usr/bin/env python3
"""Fix UTF-8 encoding issues (hieroglyphs) in HTML files."""

import sys
import codecs

def fix_encoding(filepath):
    """Fix double-encoded UTF-8 characters."""

    print(f"\n{'='*50}")
    print("FIX ENCODING ISSUES (HIEROGLYPHS)")
    print(f"{'='*50}\n")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes = []

    # Map of broken encodings to correct characters
    replacements = {
        'â€¢': '•',      # bullet
        'âš¡': '⚡',     # lightning
        'â­': '⭐',      # star
        'Â©': '©',       # copyright
        'ðŸ"§': '🔧',    # wrench
        'ðŸ†': '🏆',     # trophy
        'ðŸ'°': '💰',    # money bag
        'ðŸ›¡ï¸': '🛡️',  # shield
        'ðŸ ': '🏠',     # house
        'ðŸ'¨â€ðŸ"§': '👨‍🔧',  # technician
        'ðŸ'µ': '💵',    # dollar bill
        'ðŸ"…': '📅',    # calendar
        'ðŸ'§': '💧',    # water droplet
        'ðŸ¢': '🏢',     # office building
        'ðŸ¥˜': '🥘',    # shallow pan of food
        'âœ"': '✓',      # checkmark
        'âœ…': '✅',     # check mark button
    }

    # Apply fixes
    for broken, correct in replacements.items():
        if broken in content:
            count = content.count(broken)
            content = content.replace(broken, correct)
            fixes.append(f"[FIXED] {count} instances: {broken} → {correct}")
            print(f"✓ Fixed {count} instances: {repr(broken)} → {correct}")

    # Save if changes were made
    if content != original_content:
        # Write as UTF-8 without BOM
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n{'='*50}")
        print(f"[SUCCESS] Fixed {len(fixes)} encoding issue types")
        print(f"[SAVED] {filepath}")
        print(f"{'='*50}\n")
        return True
    else:
        print(f"\n{'='*50}")
        print("[INFO] No encoding issues found!")
        print(f"{'='*50}\n")
        return False

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else r'C:\NikaApplianceRepair\locations\east-gwillimbury.html'
    fix_encoding(filepath)
