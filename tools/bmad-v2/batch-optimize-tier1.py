#!/usr/bin/env python3
"""
BMAD V2 - Batch Tier 1 Optimizer
Processes multiple HTML files with Tier 1 test & fix
"""

import sys
import subprocess
from pathlib import Path

def optimize_file(html_file):
    """Run Tier 1 optimization on a single file"""
    print(f"\n{'=' * 70}")
    print(f"Processing: {html_file}")
    print('=' * 70)

    script = Path(__file__).parent / "auto-run.py"
    cmd = [sys.executable, str(script), html_file, "--auto-fix"]

    result = subprocess.run(cmd, capture_output=False)

    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch-optimize-tier1.py <pattern>")
        print("Example: python batch-optimize-tier1.py 'services/*.html'")
        sys.exit(1)

    pattern = sys.argv[1]

    # Find files
    if '*' in pattern:
        # Glob pattern
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

    print(f"\nFound {len(files)} files to optimize")
    print("=" * 70)

    results = []
    for file in files:
        success = optimize_file(str(file))
        results.append((file.name, success))

    # Print summary
    print("\n" + "=" * 70)
    print("BATCH OPTIMIZATION SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed

    for filename, success in results:
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"{status} {filename}")

    print("\n" + "=" * 70)
    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
    print("=" * 70)

if __name__ == "__main__":
    main()
