#!/usr/bin/env python3
"""
BMAD Mass Testing Script
Tests all pages in the project and generates comprehensive report
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
PAGES = {
    "main": ["index.html"],
    "services": [
        "services/refrigerator-repair.html",
        "services/washer-repair.html",
        "services/dryer-repair.html",
        "services/oven-repair.html",
        "services/stove-cooktop-repair.html",
        "services/freezer-repair.html",
        "services/dishwasher-repair.html",
        "services/refrigerator-freezer-repair.html",
        "services/washer-dryer-repair.html",
        "services/oven-stove-repair.html",
        "services/dishwasher-installation.html"
    ],
    "locations": [
        "locations/ajax.html",
        "locations/aurora.html",
        "locations/barrie.html",
        "locations/bolton.html",
        "locations/brampton.html",
        "locations/burlington.html",
        "locations/caledon.html",
        "locations/concord.html",
        "locations/east-gwillimbury.html",
        "locations/etobicoke.html",
        "locations/georgetown.html",
        "locations/king-city.html",
        "locations/maple.html",
        "locations/markham.html",
        "locations/milton.html",
        "locations/mississauga.html",
        "locations/newmarket.html",
        "locations/north-york.html",
        "locations/oakville.html",
        "locations/oshawa.html",
        "locations/pickering.html",
        "locations/richmond-hill.html",
        "locations/scarborough.html",
        "locations/stouffville.html",
        "locations/thornhill.html",
        "locations/toronto.html",
        "locations/uxbridge.html",
        "locations/vaughan.html",
        "locations/whitby.html",
        "locations/woodbridge.html"
    ],
    "blog": [
        "blog/how-to-fix-refrigerator-not-cooling.html",
        "blog/washer-not-draining-solutions.html",
        "blog/dryer-not-heating-troubleshooting.html",
        "blog/dishwasher-not-cleaning-solutions.html",
        "blog/oven-temperature-calibration-guide.html",
        "blog/appliance-maintenance-schedule.html",
        "blog/signs-appliance-needs-repair.html",
        "blog/diy-vs-professional-appliance-repair.html",
        "blog/best-appliance-brands-2025.html",
        "blog/repair-vs-replace-appliances.html",
        "blog/energy-efficient-appliances-worth-it.html",
        "blog/buying-used-appliances-toronto.html",
        "blog/appliance-warranties-explained.html",
        "blog/appliance-repair-costs-toronto-2025.html",
        "blog/reliable-appliance-repair-gta.html",
        "blog/toronto-appliance-disposal-recycling.html",
        "blog/buy-appliance-parts-toronto.html",
        "blog/prepare-appliances-winter-toronto.html",
        "blog/spring-appliance-maintenance-gta.html",
        "blog/emergency-appliance-repair-fridge.html"
    ]
}

def run_test(test_script, page_path):
    """Run a single test and capture output"""
    try:
        result = subprocess.run(
            ["python", test_script, page_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=PROJECT_ROOT
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Test timeout after 60 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

def extract_seo_score(output):
    """Extract SEO score from output"""
    for line in output.split('\n'):
        if "OVERALL SCORE:" in line:
            try:
                score = line.split(':')[1].strip().split('/')[0]
                return int(score)
            except:
                return 0
    return 0

def extract_data_consistency(error_output):
    """Extract data consistency status"""
    if "[PASS]" in error_output or "DEPLOYMENT APPROVED" in error_output:
        return "PASS"
    elif "[FAIL]" in error_output or "DEPLOYMENT BLOCKED" in error_output:
        return "FAIL"
    return "UNKNOWN"

def extract_critical_issues(output):
    """Extract critical issues from output"""
    issues = []
    in_critical = False
    for line in output.split('\n'):
        if "CRITICAL ISSUES:" in line:
            in_critical = True
            continue
        if in_critical and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            issues.append(line.strip())
        if in_critical and line.strip() == "":
            break
    return issues

def main():
    print("=" * 70)
    print("BMAD MASS TESTING - ALL PAGES")
    print("=" * 70)
    print()

    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pages": 0,
        "pages_tested": 0,
        "pages_passed": 0,
        "pages_failed": 0,
        "details": {}
    }

    all_pages = []
    for category, pages in PAGES.items():
        all_pages.extend([(category, page) for page in pages])

    results["total_pages"] = len(all_pages)

    for category, page_path in all_pages:
        print(f"\n{'='*70}")
        print(f"Testing: {page_path}")
        print('='*70)

        page_results = {
            "category": category,
            "path": page_path,
            "seo_score": 0,
            "data_consistency": "UNKNOWN",
            "critical_issues": [],
            "status": "FAIL"
        }

        # Test 1: SEO Check
        print("  [1/2] Running SEO check...")
        seo_result = run_test("tools/seo-checker.py", page_path)
        if seo_result["success"]:
            page_results["seo_score"] = extract_seo_score(seo_result["output"])
            page_results["critical_issues"].extend(extract_critical_issues(seo_result["output"]))
            print(f"  [OK] SEO Score: {page_results['seo_score']}/100")
        else:
            print(f"  [FAIL] SEO test failed")

        # Test 2: Data Consistency
        print("  [2/2] Running data consistency check...")
        data_result = run_test("tools/data-consistency-checker.py", page_path)
        combined_output = data_result["output"] + data_result["error"]
        page_results["data_consistency"] = extract_data_consistency(combined_output)
        if page_results["data_consistency"] == "PASS":
            print(f"  [OK] Data Consistency: PASS")
        else:
            print(f"  [FAIL] Data Consistency: FAIL")
            # Extract issues from error output
            for line in data_result["error"].split('\n'):
                if "inconsistent:" in line.lower() or "mismatch" in line.lower():
                    page_results["critical_issues"].append(line.strip())

        # Determine overall status
        if page_results["seo_score"] >= 85 and page_results["data_consistency"] == "PASS":
            page_results["status"] = "PASS"
            results["pages_passed"] += 1
        else:
            page_results["status"] = "FAIL"
            results["pages_failed"] += 1

        results["pages_tested"] += 1
        results["details"][page_path] = page_results

        # Print status
        status_icon = "[OK]" if page_results["status"] == "PASS" else "[FAIL]"
        print(f"\n  {status_icon} Status: {page_results['status']}")

    # Generate summary report
    print("\n" + "=" * 70)
    print("TESTING COMPLETE - SUMMARY REPORT")
    print("=" * 70)
    print(f"\nTotal Pages: {results['total_pages']}")
    print(f"Pages Tested: {results['pages_tested']}")
    print(f"Pages Passed (85+/100): {results['pages_passed']}")
    print(f"Pages Failed: {results['pages_failed']}")
    print(f"\nPass Rate: {(results['pages_passed']/results['pages_tested']*100):.1f}%")

    # Print failures
    if results["pages_failed"] > 0:
        print("\n" + "=" * 70)
        print("FAILED PAGES - NEED ATTENTION")
        print("=" * 70)
        for page_path, details in results["details"].items():
            if details["status"] == "FAIL":
                print(f"\n{page_path}")
                print(f"  SEO Score: {details['seo_score']}/100")
                print(f"  Data Consistency: {details['data_consistency']}")
                if details["critical_issues"]:
                    print(f"  Critical Issues ({len(details['critical_issues'])}):")
                    for issue in details["critical_issues"][:3]:  # Show first 3
                        print(f"    - {issue}")

    # Save results
    report_file = PROJECT_ROOT / f"bmad_mass_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n\nDetailed report saved to: {report_file}")
    print("=" * 70)

    return 0 if results["pages_failed"] == 0 else 1

if __name__ == "__main__":
    exit(main())
