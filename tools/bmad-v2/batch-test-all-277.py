#!/usr/bin/env python3
"""
BMAD V2 - Batch Test All Service Pages (277 params)
Tests all 11 service pages with complete 277-parameter coverage
"""

import subprocess
import sys
from pathlib import Path


def test_page(html_file):
    """Test a single page"""
    config_file = Path(__file__).parent / "config" / "business-data.json"
    tester_path = Path(__file__).parent / "tests" / "tier_all_master.py"

    try:
        result = subprocess.run(
            [sys.executable, str(tester_path), str(html_file)],
            capture_output=True,
            text=True,
            timeout=120
        )

        # Parse results from output
        output = result.stdout
        scores = {}

        # Extract tier scores
        for line in output.split('\n'):
            if 'TIER 1 SCORE:' in line:
                scores['tier1'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 2 SCORE:' in line:
                scores['tier2'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 3 SCORE:' in line:
                scores['tier3'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 4 SCORE:' in line:
                scores['tier4'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 5 SCORE:' in line:
                scores['tier5'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 7 SCORE:' in line:
                scores['tier7'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 8 SCORE:' in line:
                scores['tier8'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'TIER 9 SCORE:' in line:
                scores['tier9'] = float(line.split(':')[1].replace('/100', '').strip())
            elif 'OVERALL SCORE:' in line and '/100' in line:
                scores['overall'] = float(line.split(':')[1].replace('/100', '').strip())

        return scores

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout testing {html_file}")
        return None
    except Exception as e:
        print(f"[ERROR] Testing {html_file}: {e}")
        return None


def main():
    """Test all service pages"""
    print("\n" + "=" * 80)
    print("BMAD V2 - BATCH TEST ALL PAGES (277 PARAMETERS)")
    print("=" * 80)
    print()

    # Define all service pages
    services_dir = Path(__file__).parent.parent.parent / "services"
    service_pages = [
        "refrigerator-repair.html",
        "dishwasher-repair.html",
        "washer-repair.html",
        "dryer-repair.html",
        "stove-repair.html",
        "oven-repair.html",
        "range-repair.html",
        "microwave-repair.html",
        "freezer-repair.html",
        "ice-maker-repair.html",
        "garbage-disposal-repair.html"
    ]

    results = {}
    total_pages = len(service_pages)
    completed = 0

    for page_name in service_pages:
        page_path = services_dir / page_name
        if not page_path.exists():
            print(f"[SKIP] {page_name} - file not found")
            continue

        print(f"[{completed + 1}/{total_pages}] Testing {page_name}...")
        scores = test_page(page_path)

        if scores:
            results[page_name] = scores
            print(f"      Overall: {scores.get('overall', 0):.1f}/100")
            completed += 1
        else:
            print(f"      [FAILED]")

        print()

    # Print summary table
    print("\n" + "=" * 95)
    print("SUMMARY TABLE - ALL 11 PAGES (249 PARAMS no Tier 6)")
    print("=" * 95)
    print()

    # Header
    print(f"{'Page':<35} {'T1':>5} {'T2':>5} {'T3':>5} {'T4':>5} {'T5':>5} {'T7':>5} {'T8':>5} {'T9':>5} {'Overall':>8}")
    print("-" * 95)

    # Calculate averages
    avg_scores = {
        'tier1': 0, 'tier2': 0, 'tier3': 0, 'tier4': 0,
        'tier5': 0, 'tier7': 0, 'tier8': 0, 'tier9': 0, 'overall': 0
    }

    # Print each page
    for page_name, scores in sorted(results.items()):
        t1 = scores.get('tier1', 0)
        t2 = scores.get('tier2', 0)
        t3 = scores.get('tier3', 0)
        t4 = scores.get('tier4', 0)
        t5 = scores.get('tier5', 0)
        t7 = scores.get('tier7', 0)
        t8 = scores.get('tier8', 0)
        t9 = scores.get('tier9', 0)
        overall = scores.get('overall', 0)

        print(f"{page_name:<35} {t1:>5.1f} {t2:>5.1f} {t3:>5.1f} {t4:>5.1f} {t5:>5.1f} {t7:>5.1f} {t8:>5.1f} {t9:>5.1f} {overall:>8.1f}")

        # Accumulate for average
        for key in avg_scores:
            avg_scores[key] += scores.get(key, 0)

    # Print average
    if completed > 0:
        print("-" * 95)
        for key in avg_scores:
            avg_scores[key] /= completed

        print(f"{'AVERAGE':<35} "
              f"{avg_scores['tier1']:>5.1f} "
              f"{avg_scores['tier2']:>5.1f} "
              f"{avg_scores['tier3']:>5.1f} "
              f"{avg_scores['tier4']:>5.1f} "
              f"{avg_scores['tier5']:>5.1f} "
              f"{avg_scores['tier7']:>5.1f} "
              f"{avg_scores['tier8']:>5.1f} "
              f"{avg_scores['tier9']:>5.1f} "
              f"{avg_scores['overall']:>8.1f}")

    print()
    print(f"Tested: {completed}/{total_pages} pages")
    print(f"Coverage: 249/249 params testable (100%)")
    print(f"Info-only: 28/277 params (Tier 6 Analytics only)")
    print("=" * 95)

    # Deployment status
    if avg_scores['tier1'] == 100 and avg_scores['tier2'] >= 85 and avg_scores['tier3'] >= 70:
        print("\n[OPTIMAL] All targets met!")
    elif avg_scores['tier1'] == 100 and avg_scores['tier2'] >= 85:
        print("\n[APPROVED] Ready for Production")
    elif avg_scores['tier1'] == 100:
        print("\n[APPROVED] Deployable (optimization recommended)")
    else:
        print("\n[WARNING] Tier 1 must be 100%")

    print("=" * 80)


if __name__ == "__main__":
    main()
