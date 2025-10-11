#!/usr/bin/env python3
"""
Update BMAD dashboard with latest test results
"""

import json
from pathlib import Path
from datetime import datetime

def get_latest_json():
    """Find the latest test results JSON file"""
    base_dir = Path(__file__).parent.parent
    json_files = list(base_dir.glob('bmad_mass_test_*.json'))

    if not json_files:
        return None

    # Sort by modification time, newest first
    json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return json_files[0]

def calculate_stats(data):
    """Calculate statistics from test data"""
    details = data.get('details', {})

    stats = {
        'total_pages': len(details),
        'passing': 0,      # 85+
        'needs_work': 0,   # 50-84
        'failing': 0,      # <50
        'scores': []
    }

    for page_data in details.values():
        score = page_data.get('seo_score', 0)
        stats['scores'].append(score)

        if score >= 85:
            stats['passing'] += 1
        elif score >= 50:
            stats['needs_work'] += 1
        else:
            stats['failing'] += 1

    stats['avg_score'] = sum(stats['scores']) / len(stats['scores']) if stats['scores'] else 0

    return stats

def generate_table_rows(data):
    """Generate HTML table rows from test data"""
    details = data.get('details', {})
    rows = []

    for page_name, page_data in details.items():
        score = page_data.get('seo_score', 0)
        category = page_data.get('category', 'unknown')
        data_consistency = page_data.get('data_consistency', 'UNKNOWN')

        # Determine score class and status
        if score >= 85:
            score_class = 'green'
            status = 'pass'
            status_text = 'Passing'
        elif score >= 50:
            score_class = 'yellow'
            status = 'pending'
            status_text = 'Needs Work'
        else:
            score_class = 'red'
            status = 'fail'
            status_text = 'Failing'

        # Data consistency badge
        dc_badge = 'pass' if data_consistency == 'PASS' else 'fail'

        row = f'''                    <tr data-category="{category}" data-status="{status}">
                        <td class="page-name">{page_name}</td>
                        <td><span class="category">{category.capitalize()}</span></td>
                        <td><span class="score {score_class}">{score}</span>/100</td>
                        <td><span class="badge {dc_badge}">{data_consistency}</span></td>
                        <td><span class="badge {status}">{status_text}</span></td>
                        <td class="timestamp">Just now</td>
                        <td><button class="btn" style="padding: 0.5rem 1rem; font-size: 0.875rem;" onclick="testPage('{page_name}')">Test</button></td>
                    </tr>'''

        rows.append(row)

    return '\n'.join(rows)

def update_dashboard():
    """Update the dashboard HTML with latest data"""
    base_dir = Path(__file__).parent.parent
    dashboard_file = base_dir / 'bmad-dashboard.html'

    # Get latest test results
    latest_json = get_latest_json()
    if not latest_json:
        print("[ERROR] No test results found")
        return False

    print(f"[INFO] Using test results from: {latest_json.name}")

    with open(latest_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Calculate stats
    stats = calculate_stats(data)

    # Generate table rows
    table_rows = generate_table_rows(data)

    # Read dashboard template
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update stats
    html = html.replace(
        '<div class="stat-value green" id="passingPages">0</div>',
        f'<div class="stat-value green" id="passingPages">{stats["passing"]}</div>'
    )

    html = html.replace(
        '<div class="stat-value yellow" id="needsWork">0</div>',
        f'<div class="stat-value yellow" id="needsWork">{stats["needs_work"]}</div>'
    )

    html = html.replace(
        '<div class="stat-value red" id="failingPages">0</div>',
        f'<div class="stat-value red" id="failingPages">{stats["failing"]}</div>'
    )

    # Update average score
    avg = int(stats['avg_score'])
    avg_class = 'green' if avg >= 85 else 'yellow' if avg >= 50 else 'red'
    html = html.replace(
        '<div class="stat-value" id="avgScore">--</div>',
        f'<div class="stat-value {avg_class}" id="avgScore">{avg}</div>'
    )

    # Update table rows
    import re
    table_pattern = r'<tbody id="tableBody">.*?</tbody>'
    new_tbody = f'<tbody id="tableBody">\n{table_rows}\n                </tbody>'
    html = re.sub(table_pattern, new_tbody, html, flags=re.DOTALL)

    # Update timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Write updated dashboard
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n[SUCCESS] Dashboard updated!")
    print(f"  Total Pages: {stats['total_pages']}")
    print(f"  Passing (85+): {stats['passing']}")
    print(f"  Needs Work (50-84): {stats['needs_work']}")
    print(f"  Failing (<50): {stats['failing']}")
    print(f"  Average Score: {avg}/100")
    print(f"\nOpen file:///{dashboard_file.absolute()} to view")

    return True

if __name__ == '__main__':
    update_dashboard()
