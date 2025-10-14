#!/usr/bin/env python3
"""Verify Brampton-specific content is preserved"""

with open(r'C:\NikaApplianceRepair\locations\brampton.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('3.6 people', 'Large family specialists (3.6 people/household)'),
    ('60-amp panel', '1960s electrical specialists (60-amp panels)'),
    ('150-180 mg/L', 'Hard water experts (Peel Region data)'),
    ('WiFi Samsung/LG', 'Smart home appliance experts'),
    ('2000-2015 construction', 'Builder-grade expertise'),
    ('Tarion', 'Warranty expiration support'),
    ('Bramalea', 'Bramalea neighborhood coverage'),
    ('Springdale', 'Springdale luxury homes'),
    ('Heart Lake', 'Heart Lake area coverage'),
    ('8-12+ loads', 'Heavy usage patterns'),
]

print('='*70)
print('BRAMPTON-SPECIFIC CONTENT VERIFICATION')
print('='*70)
print()

all_found = True
for term, description in checks:
    found = term in content
    status = 'FOUND' if found else 'MISSING'
    symbol = '✓' if found else '✗'
    print(f'{symbol} {description}: {status}')
    if not found:
        all_found = False

print()
print('='*70)
if all_found:
    print('SUCCESS: All Brampton-specific content preserved!')
else:
    print('WARNING: Some content may be missing!')
print('='*70)
