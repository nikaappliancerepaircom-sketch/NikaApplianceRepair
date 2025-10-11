#!/usr/bin/env python3
"""
Run BMAD test on all pages and generate dashboard
"""

from pathlib import Path
import json
import subprocess
from datetime import datetime

def run_bmad_test(file_path):
    """Run BMAD test on a single file and capture results"""
    try:
        result = subprocess.run(
            ['python', 'tools/bmad-complete-test.py', str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout

        # Parse score from output
        score_line = [line for line in output.split('\n') if 'OVERALL SCORE:' in line]
        if score_line:
            score = float(score_line[0].split(':')[1].split('/')[0].strip())
        else:
            score = 0

        # Parse status
        if 'DEPLOYMENT APPROVED' in output:
            status = 'APPROVED'
        elif 'DEPLOYMENT BLOCKED' in output:
            status = 'BLOCKED'
        else:
            status = 'UNKNOWN'

        # Parse category scores
        categories = {}
        for line in output.split('\n'):
            if 'DATA CONSISTENCY' in line and 'PASS' in line:
                categories['data_consistency'] = 100
            elif 'DATA CONSISTENCY' in line and 'FAIL' in line:
                categories['data_consistency'] = 0
            elif 'SEO OPTIMIZATION' in line:
                parts = line.split('.')
                if len(parts) > 1:
                    score_part = parts[-1].strip()
                    if '/' in score_part:
                        categories['seo'] = int(score_part.split('/')[0].strip())
            elif 'PSYCHOLOGY' in line:
                parts = line.split('.')
                if len(parts) > 1:
                    score_part = parts[-1].strip()
                    if '/' in score_part:
                        categories['psychology'] = int(score_part.split('/')[0].strip())
            elif 'RESPONSIVE TYPOGRAPHY' in line:
                parts = line.split('.')
                if len(parts) > 1:
                    score_part = parts[-1].strip()
                    if '/' in score_part:
                        categories['responsive_typography'] = int(score_part.split('/')[0].strip())

        return {
            'file': file_path.name,
            'score': score,
            'status': status,
            'categories': categories
        }

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return None

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("MASS BMAD TESTING - ALL PAGES")
    print("=" * 70)

    all_files = []

    # Collect all HTML files
    all_files.append(base_dir / 'index.html')

    for subdir in ['services', 'locations']:
        dir_path = base_dir / subdir
        if dir_path.exists():
            all_files.extend([f for f in dir_path.glob('*.html')])

    print(f"\nTesting {len(all_files)} pages...\n")

    results = []
    approved = 0
    blocked = 0

    for i, file_path in enumerate(all_files, 1):
        if not file_path.exists():
            continue

        print(f"[{i}/{len(all_files)}] Testing {file_path.name}...", end=" ", flush=True)

        result = run_bmad_test(file_path)
        if result:
            results.append(result)
            if result['status'] == 'APPROVED':
                approved += 1
                print(f"✓ {result['score']}/100 APPROVED")
            elif result['status'] == 'BLOCKED':
                blocked += 1
                print(f"✗ {result['score']}/100 BLOCKED")
            else:
                print(f"? {result['score']}/100")

    # Save results
    output_file = base_dir / f'bmad_mass_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_pages': len(results),
            'approved': approved,
            'blocked': blocked,
            'average_score': sum(r['score'] for r in results) / len(results) if results else 0,
            'results': results
        }, f, indent=2)

    print("\n" + "=" * 70)
    print("MASS TEST COMPLETE")
    print("=" * 70)
    print(f"\nTotal Pages: {len(results)}")
    print(f"Approved: {approved}")
    print(f"Blocked: {blocked}")
    print(f"Average Score: {sum(r['score'] for r in results) / len(results) if results else 0:.1f}/100")
    print(f"\nResults saved: {output_file}")
    print("=" * 70)

if __name__ == '__main__':
    main()
