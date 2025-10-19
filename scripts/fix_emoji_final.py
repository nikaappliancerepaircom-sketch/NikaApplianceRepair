#!/usr/bin/env python3
"""Fix remaining emoji encoding issues."""

filepath = r'C:\NikaApplianceRepair\locations\east-gwillimbury.html'

# Read as binary
with open(filepath, 'rb') as f:
    data = f.read()

# Decode as latin-1 to preserve all bytes
text = data.decode('latin-1')

print('Fixing emojis...')

# Count and fix
fixes = 0

# Trophy: bytes F0 9F 8F 86 displayed as ðŸ† in latin-1
if '\xf0\x9f\x8f\x86' in text:
    count = text.count('\xf0\x9f\x8f\x86')
    text = text.replace('\xf0\x9f\x8f\x86', '🏆')
    print(f'Fixed {count} trophy emojis')
    fixes += count

# House: F0 9F 8F A0
if '\xf0\x9f\x8f\xa0' in text:
    count = text.count('\xf0\x9f\x8f\xa0')
    text = text.replace('\xf0\x9f\x8f\xa0', '🏠')
    print(f'Fixed {count} house emojis')
    fixes += count

# Building: F0 9F 8F A2
if '\xf0\x9f\x8f\xa2' in text:
    count = text.count('\xf0\x9f\x8f\xa2')
    text = text.replace('\xf0\x9f\x8f\xa2', '🏢')
    print(f'Fixed {count} building emojis')
    fixes += count

# Technician (man technician): F0 9F 91 A8 E2 80 8D F0 9F 94 A7
# But wrench is already fixed, so just need man + ZWJ
if '\xf0\x9f\x91\xa8\xe2\x80\x8d' in text:
    count = text.count('\xf0\x9f\x91\xa8\xe2\x80\x8d')
    text = text.replace('\xf0\x9f\x91\xa8\xe2\x80\x8d', '👨\u200d')
    print(f'Fixed {count} technician emoji parts')
    fixes += count

print(f'\nTotal fixes: {fixes}')

# Write back as UTF-8
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('All emojis fixed!')
