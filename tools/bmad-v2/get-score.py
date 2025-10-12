#!/usr/bin/env python3
"""
Get BMAD score for a specific tier from the last test run
"""

import sys
import json
from pathlib import Path

def get_score(file_path: str, tier: str) -> int:
    """Get score from last test run"""

    # Look for latest report
    reports_dir = Path(__file__).parent
    reports = sorted(reports_dir.glob("bmad-report-*.json"), reverse=True)

    if not reports:
        return 0

    # Read latest report
    with open(reports[0]) as f:
        data = json.load(f)

    # Extract tier score
    tier_num = int(tier)
    if 'results' in data:
        for result in data['results']:
            if result.get('tier') == tier_num:
                return int(result.get('score', 0))

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("0")
        sys.exit(0)

    file_path = sys.argv[1]
    tier = sys.argv[2]

    score = get_score(file_path, tier)
    print(score)
