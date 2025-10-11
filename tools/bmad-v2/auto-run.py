#!/usr/bin/env python3
"""
BMAD V2 - AUTO-RUN PIPELINE
Runs tests and fixes incrementally: Tier 1 → Tier 2 → Tier 3
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tests.tier1_critical import Tier1Tester
from fixers.tier1_fixer import Tier1Fixer
from tests.tier2_high_priority import Tier2Tester
from fixers.tier2_fixer import Tier2Fixer

def print_banner(text):
    """Print banner (Windows compatible)"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def run_tier1(html_file, config_file, auto_fix=False):
    """Run Tier 1: Critical Parameters"""
    print_banner("[TIER 1] CRITICAL PARAMETERS (15)")

    # Test
    tester = Tier1Tester(html_file, config_file)

    if not tester.load_config():
        return False

    if not tester.load_html():
        return False

    passed = tester.test_all()

    # Auto-fix if requested and not passed
    if not passed and auto_fix:
        print("\n[AUTO-FIX] Applying fixes...")

        fixer = Tier1Fixer(html_file, config_file)
        if not fixer.load_config():
            return False

        if not fixer.load_html():
            return False

        fixer.create_backup()

        if fixer.fix_all():
            fixer.save_html()

            # Re-test
            print("\n[RE-TEST] Verifying fixes...")
            tester2 = Tier1Tester(html_file, config_file)
            tester2.load_config()
            tester2.load_html()
            passed = tester2.test_all()

    return passed

def run_tier2(html_file, config_file, auto_fix=False):
    """Run Tier 2: High Priority (SEO & CRO)"""
    print_banner("[TIER 2] HIGH PRIORITY - SEO & CRO (30)")

    # Test
    tester = Tier2Tester(html_file, config_file)

    if not tester.load_config():
        return False

    if not tester.load_html():
        return False

    passed = tester.test_all()

    # Auto-fix if requested and not passed
    if not passed and auto_fix:
        print("\n[AUTO-FIX] Applying Tier 2 fixes...")

        fixer = Tier2Fixer(html_file, config_file)
        if not fixer.load_config():
            return False

        if not fixer.load_html():
            return False

        fixer.create_backup()

        if fixer.fix_all():
            fixer.save_html()

            # Re-test
            print("\n[RE-TEST] Verifying fixes...")
            tester2 = Tier2Tester(html_file, config_file)
            tester2.load_config()
            tester2.load_html()
            passed = tester2.test_all()

    return passed

def main():
    if len(sys.argv) < 2:
        print("BMAD V2 - Auto-Run Pipeline")
        print("\nUsage:")
        print("  python auto-run.py <html_file> [--auto-fix]")
        print("\nExample:")
        print("  python auto-run.py services/refrigerator-repair.html --auto-fix")
        sys.exit(1)

    html_file = sys.argv[1]
    auto_fix = '--auto-fix' in sys.argv

    # Check if file exists
    if not os.path.exists(html_file):
        print(f"Error: File not found: {html_file}")
        sys.exit(1)

    config_file = Path(__file__).parent / "config" / "business-data.json"

    print_banner(f"BMAD V2 - TESTING: {html_file}")
    print(f"Auto-fix: {'ENABLED' if auto_fix else 'DISABLED'}")

    # Run Tier 1
    tier1_passed = run_tier1(html_file, config_file, auto_fix)

    if not tier1_passed:
        print("\n[BLOCKED] Tier 1 must pass before proceeding to Tier 2")
        print("Run with --auto-fix to automatically fix issues")
        sys.exit(1)

    print("\n[SUCCESS] Tier 1 passed! Ready for Tier 2")

    # Run Tier 2
    tier2_passed = run_tier2(html_file, config_file, auto_fix)

    if not tier2_passed:
        print("\n[WARNING] Tier 2 score below 85% - page needs optimization")
        print("Page is deployable but not optimal")
    else:
        print("\n[SUCCESS] Tier 2 passed! Page is well-optimized")

    # Print final summary
    print_banner("OPTIMIZATION COMPLETE")
    t1_status = 'PASS' if tier1_passed else 'FAIL'
    t2_status = 'PASS' if tier2_passed else 'NEEDS WORK'
    page_status = 'APPROVED' if tier1_passed else 'BLOCKED'
    print(f"Tier 1 (Critical): {t1_status}")
    print(f"Tier 2 (High Priority): {t2_status}")
    print(f"\nPage Status: {page_status}")

if __name__ == "__main__":
    main()
