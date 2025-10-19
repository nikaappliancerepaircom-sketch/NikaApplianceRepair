#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch BMAD auto-fix for all location pages."""

import os
import sys
import glob
import subprocess

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    """Run BMAD auto-fix on all location pages."""

    print("="*60)
    print("BMAD Batch Auto-Fix - All Location Pages")
    print("="*60)
    print()

    location_files = glob.glob('locations/*.html')

    if not location_files:
        print("ERROR: No location pages found")
        return

    print(f"Found {len(location_files)} location pages\n")
    print("="*60)

    passed = []
    failed = []

    for i, file_path in enumerate(sorted(location_files), 1):
        page_name = os.path.basename(file_path)
        print(f"\n[{i}/{len(location_files)}] Testing: {page_name}")

        try:
            # Run BMAD auto-fix
            result = subprocess.run(
                ['python', 'tools/bmad-v2/auto-run.py', file_path, '--auto-fix', '--tier', '1'],
                capture_output=True,
                text=True,
                timeout=60
            )

            # Check if Tier 1 passed
            if 'TIER 1 SCORE: 100/100' in result.stdout:
                print(f"  ✓ PASS - Tier 1: 100/100")
                passed.append(page_name)
            elif 'TIER 1 SCORE:' in result.stdout:
                # Extract score
                import re
                score_match = re.search(r'TIER 1 SCORE: (\d+)/100', result.stdout)
                if score_match:
                    score = score_match.group(1)
                    print(f"  ⚠ WARN - Tier 1: {score}/100")
                    failed.append(page_name)
                else:
                    print(f"  ✗ FAIL - Could not parse score")
                    failed.append(page_name)
            else:
                print(f"  ✗ FAIL - No score found")
                failed.append(page_name)

        except subprocess.TimeoutExpired:
            print(f"  ✗ TIMEOUT")
            failed.append(page_name)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed.append(page_name)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}\n")
    print(f"✓ Passed Tier 1 (100/100): {len(passed)}/{len(location_files)}")
    print(f"✗ Failed/Warned: {len(failed)}/{len(location_files)}")

    if failed:
        print(f"\nFailed pages:")
        for page in failed:
            print(f"  - {page}")

    print(f"\n{'='*60}")
    print("✓ Batch auto-fix complete!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
