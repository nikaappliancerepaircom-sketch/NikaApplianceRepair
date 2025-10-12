#!/usr/bin/env python3
"""
BMAD v2 Agent Coordinator
Manages execution of specialized AI agents for testing and optimization
"""

import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class AgentCoordinator:
    """Coordinates execution of BMAD v2 testing agents"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.results = {}
        self.start_time = datetime.now()

        # Agent definitions with tier mappings
        self.agents = {
            # Tier 1 agents
            "data-consistency": {
                "tier": 1,
                "params": 8,
                "description": "Validates global data consistency",
                "auto_fix": True,
                "script": "tests/tier1_critical.py"
            },
            "schema": {
                "tier": 1,
                "params": 2,
                "description": "Manages JSON-LD schema markup",
                "auto_fix": True,
                "script": "tests/tier1_critical.py"
            },
            "technical": {
                "tier": 1,
                "params": 3,
                "description": "HTML and technical validation",
                "auto_fix": True,
                "script": "tests/tier1_critical.py"
            },
            "security": {
                "tier": 1,
                "params": 2,
                "description": "HTTPS and security checks",
                "auto_fix": True,
                "script": "tests/tier1_critical.py"
            },

            # Tier 2 agents
            "seo-optimization": {
                "tier": 2,
                "params": 15,
                "description": "Complete SEO audit and optimization",
                "auto_fix": True,
                "script": "tests/tier2_seo.py"
            },
            "cro-optimization": {
                "tier": 2,
                "params": 15,
                "description": "CRO elements audit",
                "auto_fix": False,
                "script": "tests/tier2_cro.py"
            },

            # Tier 3 agents
            "content-quality": {
                "tier": 3,
                "params": 20,
                "description": "Content structure and quality",
                "auto_fix": False,
                "script": "tests/tier3_content.py"
            },
            "ux-audit": {
                "tier": 3,
                "params": 30,
                "description": "UX and usability audit",
                "auto_fix": True,
                "script": "tests/tier3_ux.py"
            },

            # Tier 4 agents
            "performance": {
                "tier": 4,
                "params": 25,
                "description": "Speed and Core Web Vitals",
                "auto_fix": True,
                "script": "tests/tier4_performance.py"
            },

            # Tier 5 agents
            "cross-browser": {
                "tier": 5,
                "params": 15,
                "description": "Cross-browser compatibility",
                "auto_fix": False,
                "script": "tests/tier5_browser.py"
            },
            "responsive": {
                "tier": 5,
                "params": 15,
                "description": "Responsive design testing",
                "auto_fix": True,
                "script": "tests/tier5_responsive.py"
            },

            # Tier 6 agents
            "advanced-ux": {
                "tier": 6,
                "params": 35,
                "description": "Advanced UX features",
                "auto_fix": False,
                "script": "tests/tier6_advanced_ux.py"
            },

            # Tier 7 agents
            "analytics": {
                "tier": 7,
                "params": 28,
                "description": "Analytics and tracking setup",
                "auto_fix": True,
                "script": "tests/tier7_analytics.py"
            }
        }

    def run_agent(self, agent_name: str, auto_fix: bool = True) -> Dict[str, Any]:
        """Run a single agent"""

        if agent_name not in self.agents:
            return {"error": f"Unknown agent: {agent_name}"}

        agent = self.agents[agent_name]
        print(f"\n🤖 Running: {agent_name}")
        print(f"   Tier {agent['tier']} | {agent['params']} params | {agent['description']}")
        print("   " + "─" * 70)

        # Run test script
        script_path = Path(__file__).parent / agent['script']

        if not script_path.exists():
            print(f"   ⚠️  Script not found: {script_path}")
            return {
                "agent": agent_name,
                "status": "skipped",
                "message": "Script not implemented yet"
            }

        try:
            # Run test
            test_result = subprocess.run(
                [sys.executable, str(script_path), str(self.file_path)],
                capture_output=True,
                text=True,
                timeout=120
            )

            # Parse output
            output_lines = test_result.stdout.strip().split('\n')

            # Extract score (last line usually contains score)
            score_line = [l for l in output_lines if 'SCORE:' in l or '/100' in l]
            score = 0
            if score_line:
                # Extract numeric score
                import re
                match = re.search(r'(\d+)/100', score_line[-1])
                if match:
                    score = int(match.group(1))

            print(f"   ✅ Test complete: {score}%")

            # Run auto-fix if available and enabled
            if auto_fix and agent['auto_fix']:
                fixer_script = script_path.parent / f"../fixers/tier{agent['tier']}_fixer.py"
                if fixer_script.exists():
                    print(f"   🔧 Running auto-fix...")

                    fix_result = subprocess.run(
                        [sys.executable, str(fixer_script), str(self.file_path)],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )

                    if fix_result.returncode == 0:
                        print(f"   ✅ Auto-fix complete")
                    else:
                        print(f"   ⚠️  Auto-fix had issues")

            return {
                "agent": agent_name,
                "tier": agent['tier'],
                "status": "completed",
                "score": score,
                "output": test_result.stdout
            }

        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Timeout (> 120s)")
            return {
                "agent": agent_name,
                "status": "timeout",
                "message": "Execution exceeded 120 seconds"
            }
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {
                "agent": agent_name,
                "status": "error",
                "message": str(e)
            }

    def run_tier(self, tier_number: int, auto_fix: bool = True) -> Dict[str, Any]:
        """Run all agents for a specific tier"""

        tier_agents = [name for name, agent in self.agents.items() if agent['tier'] == tier_number]

        if not tier_agents:
            return {"error": f"No agents defined for Tier {tier_number}"}

        print(f"\n{'='*80}")
        print(f"🎯 TIER {tier_number} OPTIMIZATION")
        print(f"{'='*80}")

        tier_results = []
        for agent_name in tier_agents:
            result = self.run_agent(agent_name, auto_fix)
            tier_results.append(result)

        # Calculate tier score
        scores = [r['score'] for r in tier_results if 'score' in r]
        tier_score = sum(scores) / len(scores) if scores else 0

        print(f"\n   📊 TIER {tier_number} SCORE: {tier_score:.1f}%")

        return {
            "tier": tier_number,
            "agents_run": len(tier_results),
            "score": tier_score,
            "results": tier_results
        }

    def run_all_tiers(self, max_tier: int = 4, auto_fix: bool = True) -> Dict[str, Any]:
        """Run all tiers up to max_tier"""

        print(f"\n{'='*80}")
        print(f"🚀 BMAD v2 FULL OPTIMIZATION")
        print(f"   File: {self.file_path}")
        print(f"   Tiers: 1-{max_tier}")
        print(f"   Auto-fix: {'Enabled' if auto_fix else 'Disabled'}")
        print(f"{'='*80}")

        all_results = []
        gate_passed = True

        for tier in range(1, max_tier + 1):
            tier_result = self.run_tier(tier, auto_fix)
            all_results.append(tier_result)

            # Check deployment gates
            if tier == 1 and tier_result['score'] < 100:
                print(f"\n   🔴 GATE 1 FAILED: Tier 1 must be 100%")
                print(f"   🔴 BLOCKING DEPLOYMENT")
                gate_passed = False
                break

            if tier == 2 and tier_result['score'] < 80:
                print(f"\n   ⚠️  GATE 2 WARNING: Tier 2 below 80%")

        # Final summary
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        print(f"\n{'='*80}")
        print(f"📊 FINAL SUMMARY")
        print(f"{'='*80}")

        for result in all_results:
            tier = result['tier']
            score = result['score']

            if tier == 1:
                status = "✅ PASS" if score == 100 else "🔴 FAIL"
            elif tier == 2:
                if score >= 85:
                    status = "✅ EXCELLENT"
                elif score >= 80:
                    status = "⚠️  ACCEPTABLE"
                else:
                    status = "⚠️  NEEDS WORK"
            else:
                status = "ℹ️  INFO"

            print(f"   Tier {tier}: {score:.1f}% {status}")

        print(f"\n   ⏱️  Duration: {duration:.1f} seconds")

        if gate_passed:
            if all_results[1]['score'] >= 85 if len(all_results) > 1 else False:
                print(f"   ✅ DEPLOYMENT: APPROVED")
            else:
                print(f"   ⚠️  DEPLOYMENT: APPROVED WITH WARNING")
        else:
            print(f"   🔴 DEPLOYMENT: BLOCKED")

        print(f"{'='*80}\n")

        return {
            "file": str(self.file_path),
            "tiers_completed": len(all_results),
            "total_duration": duration,
            "gate_passed": gate_passed,
            "results": all_results
        }

    def save_report(self, results: Dict[str, Any], output_file: str = None):
        """Save results to JSON report"""

        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"bmad-report-{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"📄 Report saved: {output_file}")


def main():
    """CLI entry point"""

    if len(sys.argv) < 2:
        print("Usage: python agent-coordinator.py <file.html> [tier|all] [--no-fix]")
        print("\nExamples:")
        print("  python agent-coordinator.py index.html 1")
        print("  python agent-coordinator.py index.html all")
        print("  python agent-coordinator.py index.html all --no-fix")
        sys.exit(1)

    file_path = sys.argv[1]
    tier_arg = sys.argv[2] if len(sys.argv) > 2 else "all"
    auto_fix = "--no-fix" not in sys.argv

    coordinator = AgentCoordinator(file_path)

    if tier_arg == "all":
        results = coordinator.run_all_tiers(max_tier=4, auto_fix=auto_fix)
    elif tier_arg.isdigit():
        tier_num = int(tier_arg)
        results = coordinator.run_tier(tier_num, auto_fix=auto_fix)
    else:
        # Run specific agent
        results = coordinator.run_agent(tier_arg, auto_fix=auto_fix)

    # Save report
    coordinator.save_report(results)


if __name__ == "__main__":
    main()
