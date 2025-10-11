#!/usr/bin/env python3
"""
Generate HTML SEO Report Page
Creates a visual dashboard for SEO analysis results
"""

from pathlib import Path
import json
from datetime import datetime

def generate_html_report(json_data):
    """Generate HTML dashboard from JSON data"""

    avg_scores = json_data['average_scores']
    page_results = json_data['page_results']

    # Determine status color
    overall = avg_scores['overall']
    if overall >= 80:
        status_color = '#10b981'
        status_text = 'EXCELLENT'
    elif overall >= 70:
        status_color = '#f59e0b'
        status_text = 'GOOD'
    elif overall >= 60:
        status_color = '#f59e0b'
        status_text = 'NEEDS IMPROVEMENT'
    else:
        status_color = '#ef4444'
        status_text = 'POOR'

    # Generate category cards
    category_cards = ""
    for category, score in avg_scores['categories'].items():
        color_class = 'green' if score >= 75 else ('yellow' if score >= 60 else 'red')
        category_cards += f'''
        <div class="stat-card">
            <h3>{category.replace('_', ' ').title()}</h3>
            <div class="stat-value {color_class}">{score:.1f}</div>
            <div class="stat-label">out of 100</div>
        </div>
        '''

    # Generate top performers table
    top_performers = sorted(page_results, key=lambda x: x['overall_score'], reverse=True)[:10]
    top_table_rows = ""

    for i, page in enumerate(top_performers, 1):
        score = page['overall_score']
        color_class = 'green' if score >= 75 else ('yellow' if score >= 60 else 'red')
        top_table_rows += f'''
        <tr>
            <td>{i}</td>
            <td>{page['file']}</td>
            <td><span class="score-badge {color_class}">{score:.1f}</span></td>
            <td>{page['category_scores']['content']:.0f}</td>
            <td>{page['category_scores']['technical']:.0f}</td>
            <td>{page['category_scores']['local_seo']:.0f}</td>
        </tr>
        '''

    # Generate needs improvement table
    needs_improvement = sorted(page_results, key=lambda x: x['overall_score'])[:10]
    needs_table_rows = ""

    for i, page in enumerate(needs_improvement, 1):
        score = page['overall_score']
        color_class = 'red' if score < 60 else 'yellow'

        # Get top 3 issues
        all_issues = []
        for category, issues in page['issues'].items():
            all_issues.extend(issues)

        top_issues = ', '.join(all_issues[:3]) if all_issues else 'No critical issues'

        needs_table_rows += f'''
        <tr>
            <td>{i}</td>
            <td>{page['file']}</td>
            <td><span class="score-badge {color_class}">{score:.1f}</span></td>
            <td>{top_issues[:100]}{'...' if len(top_issues) > 100 else ''}</td>
        </tr>
        '''

    # Generate detailed issues section
    detailed_issues = ""
    service_pages = [p for p in page_results if 'services/' in str(p.get('file', ''))][:5]

    for page in service_pages:
        issues_html = ""
        for category, issues in page['issues'].items():
            if issues:
                issues_html += f"<strong>{category.replace('_', ' ').title()}:</strong> "
                issues_html += '; '.join(issues) + "<br>"

        if issues_html:
            detailed_issues += f'''
            <div class="issue-card">
                <h4>{page['file']}</h4>
                <div class="issue-list">{issues_html}</div>
            </div>
            '''

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analysis Report - Nika Appliance Repair</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header h1 {{
            color: #1a202c;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            color: #718096;
            font-size: 1.1rem;
        }}

        .overall-score {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .score-circle {{
            display: inline-block;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: conic-gradient({status_color} {overall*3.6}deg, #e5e7eb {overall*3.6}deg);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 1rem 0;
        }}

        .score-inner {{
            width: 170px;
            height: 170px;
            border-radius: 50%;
            background: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .score-number {{
            font-size: 3.5rem;
            font-weight: bold;
            color: {status_color};
        }}

        .score-status {{
            font-size: 1.2rem;
            color: #718096;
            margin-top: 0.5rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stat-card h3 {{
            color: #718096;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #1a202c;
            margin-bottom: 0.5rem;
        }}

        .stat-value.green {{ color: #10b981; }}
        .stat-value.yellow {{ color: #f59e0b; }}
        .stat-value.red {{ color: #ef4444; }}

        .stat-label {{
            color: #a0aec0;
            font-size: 0.875rem;
        }}

        .table-container {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow-x: auto;
            margin-bottom: 2rem;
        }}

        .table-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}

        .table-header h2 {{
            color: #1a202c;
            font-size: 1.5rem;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            background: #f7fafc;
            color: #4a5568;
            font-weight: 600;
            text-align: left;
            padding: 1rem;
            border-bottom: 2px solid #e2e8f0;
        }}

        td {{
            padding: 1rem;
            border-bottom: 1px solid #e2e8f0;
            color: #4a5568;
        }}

        tr:hover {{
            background: #f7fafc;
        }}

        .score-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.875rem;
        }}

        .score-badge.green {{
            background: #d1fae5;
            color: #065f46;
        }}

        .score-badge.yellow {{
            background: #fef3c7;
            color: #92400e;
        }}

        .score-badge.red {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .issues-section {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .issues-section h2 {{
            color: #1a202c;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .issue-card {{
            background: #f7fafc;
            border-left: 4px solid #ef4444;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 4px;
        }}

        .issue-card h4 {{
            color: #1a202c;
            margin-bottom: 0.5rem;
        }}

        .issue-list {{
            color: #4a5568;
            line-height: 1.6;
        }}

        .timestamp {{
            text-align: center;
            color: white;
            margin-top: 2rem;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Comprehensive SEO Analysis Report</h1>
            <p>270+ Parameter Analysis | Nika Appliance Repair Website</p>
        </div>

        <div class="overall-score">
            <h2>Overall SEO Score</h2>
            <div class="score-circle">
                <div class="score-inner">
                    <div class="score-number">{overall:.0f}</div>
                    <div class="score-status">{status_text}</div>
                </div>
            </div>
            <p style="color: #718096; margin-top: 1rem;">
                Based on {json_data['total_pages']} pages analyzed
            </p>
        </div>

        <div class="stats-grid">
{category_cards}
        </div>

        <div class="table-container">
            <div class="table-header">
                <h2>🏆 Top Performing Pages</h2>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Page</th>
                        <th>Overall Score</th>
                        <th>Content</th>
                        <th>Technical</th>
                        <th>Local SEO</th>
                    </tr>
                </thead>
                <tbody>
{top_table_rows}
                </tbody>
            </table>
        </div>

        <div class="table-container">
            <div class="table-header">
                <h2>⚠️ Pages Needing Improvement</h2>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Page</th>
                        <th>Score</th>
                        <th>Top Issues</th>
                    </tr>
                </thead>
                <tbody>
{needs_table_rows}
                </tbody>
            </table>
        </div>

        <div class="issues-section">
            <h2>🔍 Detailed Issues (Sample Pages)</h2>
{detailed_issues}
        </div>

        <div class="timestamp">
            <p>Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>Analysis Date: {json_data['analysis_date'][:10]}</p>
        </div>
    </div>
</body>
</html>'''

    return html_content

def main():
    base_dir = Path(__file__).parent.parent

    # Load JSON report
    json_file = base_dir / 'reports' / 'comprehensive_seo_analysis.json'

    if not json_file.exists():
        print("[ERROR] comprehensive_seo_analysis.json not found!")
        print("Run full-seo-analysis.py first")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Generate HTML
    html_content = generate_html_report(json_data)

    # Save HTML report
    html_file = base_dir / 'seo-report.html'

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("=" * 70)
    print("SEO REPORT HTML GENERATED")
    print("=" * 70)
    print(f"\nReport saved to: {html_file}")
    print(f"\nOverall Score: {json_data['average_scores']['overall']:.2f}/100")
    print("\nOpen seo-report.html in your browser to view the full report!")

if __name__ == '__main__':
    main()
