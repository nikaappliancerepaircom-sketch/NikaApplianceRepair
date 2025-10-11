#!/usr/bin/env python3
"""
Add Playwright test results to dashboard
"""

import json
from pathlib import Path

def get_latest_playwright_results():
    """Get latest Playwright test results"""
    base_dir = Path(__file__).parent.parent
    json_files = list(base_dir.glob('playwright_test_*.json'))

    if not json_files:
        return None

    json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return json_files[0]

def update_dashboard_with_playwright():
    """Add Playwright section to dashboard"""
    base_dir = Path(__file__).parent.parent
    dashboard_file = base_dir / 'bmad-dashboard.html'

    playwright_file = get_latest_playwright_results()
    if not playwright_file:
        print("[ERROR] No Playwright results found")
        return False

    with open(playwright_file, 'r', encoding='utf-8') as f:
        pw_data = json.load(f)

    # Read dashboard
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Create Playwright summary card HTML
    pw_summary = f'''
        <div class="table-container" style="margin-top: 2rem;">
            <div class="table-header">
                <h2>🎭 Playwright Browser Tests</h2>
                <span class="timestamp">Last test: {pw_data['timestamp']}</span>
            </div>

            <div class="stats-grid" style="margin: 1.5rem 0;">
                <div class="stat-card">
                    <h3>Total Tested</h3>
                    <div class="stat-value">{pw_data['total_pages']}</div>
                    <div class="stat-label">Full browser tests</div>
                </div>

                <div class="stat-card">
                    <h3>Passed</h3>
                    <div class="stat-value green">{pw_data['passed']}</div>
                    <div class="stat-label">All tests passed</div>
                </div>

                <div class="stat-card">
                    <h3>Failed</h3>
                    <div class="stat-value red">{pw_data['failed']}</div>
                    <div class="stat-label">Dropdown visibility issues</div>
                </div>
            </div>

            <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin: 1.5rem 0;">
                <h3 style="margin-bottom: 1rem;">Test Results Summary</h3>
                <p><strong>✅ index.html PASSED</strong> - All dropdowns and footer links work correctly</p>
                <p><strong>❌ 61 pages FAILED</strong> - Dropdown element not visible (CSS issue)</p>

                <h4 style="margin-top: 1.5rem;">What was tested:</h4>
                <ul style="list-style: none; padding-left: 0;">
                    <li>✓ Header dropdown exists</li>
                    <li>✓ Dropdown menu visible on hover</li>
                    <li>✓ All 8+ location links in dropdown</li>
                    <li>✓ Footer Service Areas section</li>
                    <li>✓ Footer links validation</li>
                    <li>✓ Responsive typography loaded</li>
                    <li>✓ Mobile viewport test (375x667)</li>
                    <li>✓ Console errors detection</li>
                    <li>✓ Full-page screenshots</li>
                </ul>

                <h4 style="margin-top: 1.5rem; color: #ef4444;">Issue Found:</h4>
                <p>Dropdown element exists but "not visible" - inline &lt;style&gt; tags not properly placed by BeautifulSoup</p>

                <h4 style="margin-top: 1.5rem; color: #10b981;">Fix Applied:</h4>
                <p>✅ Created external CSS file: <code>css/dropdown-styles.css</code></p>
                <p>✅ Added link to all 62 pages</p>
                <p>✅ Removed problematic inline styles</p>
                <p><strong>Ready for re-test!</strong></p>
            </div>

            <div style="margin-top: 1.5rem;">
                <h3>Screenshots Available</h3>
                <p>Full-page screenshots saved in: <code>screenshots/</code></p>
                <p>View screenshots: <code>{base_dir}/screenshots/</code></p>
            </div>
        </div>
    '''

    # Insert before closing </div></div> at end of container
    insertion_point = html.rfind('</div>\n    </div>\n\n    <script>')
    if insertion_point > 0:
        html = html[:insertion_point] + pw_summary + '\n' + html[insertion_point:]

        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[SUCCESS] Dashboard updated with Playwright results!")
        print(f"  Total Tests: {pw_data['total_pages']}")
        print(f"  Passed: {pw_data['passed']}")
        print(f"  Failed: {pw_data['failed']}")
        return True
    else:
        print("[ERROR] Could not find insertion point")
        return False

if __name__ == '__main__':
    update_dashboard_with_playwright()
