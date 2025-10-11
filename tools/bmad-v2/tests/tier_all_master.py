#!/usr/bin/env python3
"""
BMAD V2 - MASTER TEST - ALL 277 PARAMETERS
Runs all 9 tiers in sequence
"""

import sys
from pathlib import Path

# Import all tier testers
sys.path.insert(0, str(Path(__file__).parent))

from tier1_critical import Tier1Tester
from tier2_high_priority import Tier2Tester
from tier3_content_ux import Tier3Tester
from tier4_cross_browser import Tier4Tester
from tier5_advanced_ux import Tier5Tester
from tier7_content_features import Tier7Tester
from tier8_integrations import Tier8Tester
from tier9_polish_performance import Tier9Tester

class MasterTester:
    """Run all 277 parameter tests"""

    def __init__(self, html_file, config_file):
        self.html_file = html_file
        self.config_file = config_file
        self.tier_results = {}
        self.total_score = 0

    def test_all_tiers(self):
        """Run all 9 tiers"""
        print("\n" + "=" * 70)
        print("BMAD V2 - MASTER TEST - ALL 277 PARAMETERS")
        print("=" * 70)
        print(f"Testing: {self.html_file}\n")

        # Tier 1: Critical (16 params)
        t1 = Tier1Tester(self.html_file, self.config_file)
        if t1.load_config() and t1.load_html():
            t1.test_all()
            self.tier_results['tier1'] = {
                'score': t1.score,
                'params': 16,
                'name': 'Critical'
            }

        # Tier 2: High Priority (30 params)
        t2 = Tier2Tester(self.html_file, self.config_file)
        if t2.load_config() and t2.load_html():
            t2.test_all()
            self.tier_results['tier2'] = {
                'score': t2.score,
                'params': 30,
                'name': 'SEO & CRO'
            }

        # Tier 3: Content & UX (50 params)
        t3 = Tier3Tester(self.html_file, self.config_file)
        if t3.load_config() and t3.load_html():
            t3.test_all()
            self.tier_results['tier3'] = {
                'score': t3.score,
                'params': 50,
                'name': 'Content & UX'
            }

        # Tier 4: Cross-Browser (30 params)
        t4 = Tier4Tester(self.html_file, self.config_file)
        if t4.load_config() and t4.load_html():
            t4.test_all()
            self.tier_results['tier4'] = {
                'score': t4.score,
                'params': 30,
                'name': 'Cross-Browser'
            }

        # Tier 5: Advanced UX (30 params)
        t5 = Tier5Tester(self.html_file, self.config_file)
        if t5.load_config() and t5.load_html():
            t5.test_all()
            self.tier_results['tier5'] = {
                'score': t5.score,
                'params': 30,
                'name': 'Advanced UX'
            }

        # Tier 6: Analytics (28 params) - EXTERNAL TOOLS REQUIRED
        self.tier_results['tier6'] = {'score': 0, 'params': 28, 'name': 'Analytics', 'status': 'INFO (external tools)'}

        # Tier 7: Content Features (30 params)
        t7 = Tier7Tester(self.html_file, self.config_file)
        if t7.load_config() and t7.load_html():
            t7.test_all()
            self.tier_results['tier7'] = {
                'score': t7.score,
                'params': 30,
                'name': 'Content Features'
            }

        # Tier 8: Integrations (29 params)
        t8 = Tier8Tester(self.html_file, self.config_file)
        if t8.load_config() and t8.load_html():
            t8.test_all()
            self.tier_results['tier8'] = {
                'score': t8.score,
                'params': 29,
                'name': 'Integrations'
            }

        # Tier 9: Polish & Performance (34 params)
        t9 = Tier9Tester(self.html_file, self.config_file)
        if t9.load_config() and t9.load_html():
            t9.test_all()
            self.tier_results['tier9'] = {
                'score': t9.score,
                'params': 34,
                'name': 'Polish & Perf'
            }

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print comprehensive summary"""
        print("\n" + "=" * 70)
        print("MASTER TEST SUMMARY - 249 PARAMETERS (no Tier 6 Analytics)")
        print("=" * 70)

        total_params_tested = 0
        total_params_info = 0
        total_score_weighted = 0

        for tier_name, data in self.tier_results.items():
            status = data.get('status', 'TESTED')

            if status == 'TESTED':
                score_display = f"{data['score']:.1f}%"
                print(f"\n{tier_name.upper()}: {data['name']} ({data['params']} params)")
                print(f"  Score: {score_display}")
                total_params_tested += data['params']
                total_score_weighted += (data['score'] / 100) * data['params']
            else:
                # INFO status
                print(f"\n{tier_name.upper()}: {data['name']} ({data['params']} params)")
                print(f"  Status: {status}")
                total_params_info += data['params']

        # Calculate overall score
        if total_params_tested > 0:
            overall_score = (total_score_weighted / total_params_tested) * 100
        else:
            overall_score = 0

        print("\n" + "=" * 70)
        print(f"OVERALL SCORE: {overall_score:.1f}/100")
        print(f"Parameters Tested: {total_params_tested}/249 ({total_params_tested/249*100:.1f}%)")
        print(f"Info-Only Parameters: {total_params_info}/249 ({total_params_info/249*100:.1f}%)")
        print(f"Total Coverage: {(total_params_tested + total_params_info)/249*100:.1f}%")
        print("=" * 70)

        # Deployment status
        tier1_score = self.tier_results.get('tier1', {}).get('score', 0)
        tier2_score = self.tier_results.get('tier2', {}).get('score', 0)
        tier3_score = self.tier_results.get('tier3', {}).get('score', 0)

        if tier1_score == 100 and tier2_score >= 85 and tier3_score >= 70:
            print("\n[OPTIMAL] Tier 1+2+3 targets met")
        elif tier1_score == 100 and tier2_score >= 85:
            print("\n[APPROVED] Ready for Production")
        elif tier1_score == 100:
            print("\n[APPROVED] Deployable (Tier 2 needs optimization)")
        else:
            print("\n[BLOCKED] Tier 1 must pass 100%")

        print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tier_all_master.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = MasterTester(html_file, config_file)
    tester.test_all_tiers()
