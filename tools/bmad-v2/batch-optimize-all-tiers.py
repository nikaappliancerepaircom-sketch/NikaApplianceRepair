#!/usr/bin/env python3
"""
BMAD V2 - Batch All Tiers Optimizer
Processes multiple HTML files with full Tier 1+2 optimization
"""

import sys
import subprocess
from pathlib import Path

def optimize_file(html_file):
    """Run full optimization on a single file"""
    print(f"\n{'=' * 70}")
    print(f"Processing: {html_file}")
    print('=' * 70)

    script = Path(__file__).parent / "auto-run.py"
    cmd = [sys.executable, str(script), html_file, "--auto-fix"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extract scores from output
    tier1_score = "N/A"
    tier2_score = "N/A"

    for line in result.stdout.split('\n'):
        if "TIER 1 SCORE:" in line:
            tier1_score = line.split("TIER 1 SCORE:")[1].split("/")[0].strip()
        elif "TIER 2 SCORE:" in line:
            tier2_score = line.split("TIER 2 SCORE:")[1].split("/")[0].strip()

    return {
        'file': Path(html_file).name,
        'tier1': tier1_score,
        'tier2': tier2_score,
        'success': result.returncode == 0
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch-optimize-all-tiers.py <pattern>")
        print("Example: python batch-optimize-all-tiers.py 'services/*.html'")
        sys.exit(1)

    pattern = sys.argv[1]

    # Find files
    if '*' in pattern:
        parts = pattern.split('/')
        if len(parts) == 2:
            directory = Path(parts[0])
            glob_pattern = parts[1]
            files = list(directory.glob(glob_pattern))
        else:
            files = list(Path('.').glob(pattern))
    else:
        files = [Path(pattern)]

    # Filter out index.html
    files = [f for f in files if f.name != 'index.html']

    if not files:
        print(f"No files found matching: {pattern}")
        sys.exit(1)

    print(f"\nBMAD V2 - Full Optimization (Tier 1 + Tier 2)")
    print(f"Found {len(files)} files to optimize")
    print("=" * 70)

    results = []
    for file in files:
        result = optimize_file(str(file))
        results.append(result)

    # Print summary
    print("\n" + "=" * 70)
    print("BATCH OPTIMIZATION SUMMARY")
    print("=" * 70)

    print(f"\n{'File':<35} {'Tier 1':>10} {'Tier 2':>10} {'Status':>12}")
    print("-" * 70)

    for result in results:
        status = "OK" if result['success'] else "FAILED"
        print(f"{result['file']:<35} {result['tier1']:>10} {result['tier2']:>10} {status:>12}")

    # Calculate averages
    tier1_scores = [float(r['tier1']) for r in results if r['tier1'] != 'N/A']
    tier2_scores = [float(r['tier2']) for r in results if r['tier2'] != 'N/A']

    if tier1_scores:
        avg_tier1 = sum(tier1_scores) / len(tier1_scores)
        print("\n" + "=" * 70)
        print(f"AVERAGE TIER 1 SCORE: {avg_tier1:.1f}/100")

    if tier2_scores:
        avg_tier2 = sum(tier2_scores) / len(tier2_scores)
        print(f"AVERAGE TIER 2 SCORE: {avg_tier2:.1f}/100")

    print("=" * 70)

    passed = sum(1 for r in results if r['success'])
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {len(results) - passed}")

if __name__ == "__main__":
    main()
