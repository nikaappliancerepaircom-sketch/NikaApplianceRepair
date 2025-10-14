#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMAD v3.1 STREAMLINED TEST - MILTON PAGE
Quick assessment of critical parameters
"""

import re
from pathlib import Path

def quick_test_milton():
    with open('locations/milton.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print("=" * 80)
    print("BMAD v3.1 STREAMLINED TEST - MILTON.HTML")
    print("=" * 80)

    # Critical Gate 1: Content Quality (Target: 98%+)
    print("\n[GATE 1] CONTENT QUALITY - Target: 98%+")
    print("-" * 80)

    # Word count
    words = len(content.split())
    print(f"Word count: {words}")

    # Location mentions
    milton_count = content.count('Milton')
    print(f"'Milton' mentions: {milton_count}")

    # Milton-specific unique content markers
    unique_markers = [
        'well water', 'Escarpment', 'Harrison', 'Mobility Hub',
        'Mattamy', 'Great Gulf', 'Branthaven', '400+ mg/L',
        'compact condo', 'Beaty', 'Dempsey', 'Scott'
    ]
    found_markers = sum(1 for m in unique_markers if m in content)
    print(f"Unique Milton markers: {found_markers}/{len(unique_markers)}")

    content_quality_score = min(100, (found_markers/len(unique_markers) * 100))
    print(f"Content Quality Estimate: {content_quality_score:.1f}%")

    # Critical Gate 2: Data Consistency (Target: 100%)
    print("\n[GATE 2] DATA CONSISTENCY - Target: 100%")
    print("-" * 80)

    # Phone consistency
    phone_variants = ['437-747-6737', '4377476737', '(437) 747-6737']
    phone_count = sum(content.count(p) for p in phone_variants)
    print(f"Phone number occurrences: {phone_count}")

    # Warranty consistency
    warranty_count = content.count('90-day') + content.count('90 days')
    print(f"Warranty (90-day) mentions: {warranty_count}")

    # Rating consistency
    rating_49 = content.count('4.9')
    review_count = content.count('5,200') + content.count('5200')
    print(f"Rating (4.9) mentions: {rating_49}")
    print(f"Review count mentions: {review_count}")

    # Data issues
    issues = []
    if phone_count < 8:
        issues.append(f"Phone count low ({phone_count}, need 8+)")
    if warranty_count < 5:
        issues.append(f"Warranty mentions low ({warranty_count}, need 5+)")
    if rating_49 < 3:
        issues.append(f"Rating mentions low ({rating_49}, need 3+)")

    data_consistency_score = 100 if len(issues) == 0 else max(0, 100 - len(issues) * 15)
    print(f"Data Consistency Score: {data_consistency_score:.1f}%")

    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")

    # Critical Gate 3: SEO Score
    print("\n[GATE 3] SEO OPTIMIZATION - Target: 85%+")
    print("-" * 80)

    # Title and meta
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        title = title_match.group(1)
        print(f"Title: {title}")
        print(f"Title length: {len(title)} chars (optimal: 50-60)")

    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    if desc_match:
        desc = desc_match.group(1)
        print(f"Meta description length: {len(desc)} chars (optimal: 150-160)")

    # Schema markup
    schema_types = ['LocalBusiness', 'FAQPage', 'BreadcrumbList', 'HowTo', 'WebPage']
    schemas_found = sum(1 for s in schema_types if s in content)
    print(f"Schema types: {schemas_found}/{len(schema_types)}")

    # H1 count
    h1_count = content.count('<h1')
    print(f"H1 tags: {h1_count} (should be 1)")

    # H2 count
    h2_count = content.count('<h2')
    print(f"H2 tags: {h2_count} (optimal: 8-12)")

    # Internal links
    internal_links = len(re.findall(r'href="\.\./', content))
    print(f"Internal links: {internal_links} (optimal: 20+)")

    seo_checks = 0
    if 50 <= len(title) <= 60: seo_checks += 1
    if 150 <= len(desc) <= 160: seo_checks += 1
    if schemas_found >= 4: seo_checks += 1
    if h1_count == 1: seo_checks += 1
    if h2_count >= 8: seo_checks += 1
    if internal_links >= 15: seo_checks += 1

    seo_score = (seo_checks / 6) * 100
    print(f"SEO Score Estimate: {seo_score:.1f}%")

    # Critical Gate 4: Factory-Authorized Claims Check
    print("\n[GATE 4] COMPLIANCE CHECK - No False Claims")
    print("-" * 80)

    false_claims = [
        'factory-authorized', 'factory-certified', 'manufacturer-approved',
        'official service center', 'authorized service center'
    ]

    found_false_claims = []
    for claim in false_claims:
        if claim.lower() in content.lower():
            found_false_claims.append(claim)

    if found_false_claims:
        print("[FAIL] False claims detected:")
        for claim in found_false_claims:
            print(f"  - {claim}")
        compliance_score = 0
    else:
        print("[PASS] No false claims detected")
        compliance_score = 100

    # Overall Assessment
    print("\n" + "=" * 80)
    print("OVERALL BMAD v3.1 ASSESSMENT")
    print("=" * 80)

    gates = [
        ("Content Quality", content_quality_score, 98),
        ("Data Consistency", data_consistency_score, 100),
        ("SEO Optimization", seo_score, 85),
        ("Compliance", compliance_score, 100)
    ]

    overall_score = sum(g[1] for g in gates) / len(gates)

    for name, score, target in gates:
        status = "PASS" if score >= target else "FAIL"
        print(f"{name:.<35} {score:.1f}% (target: {target}%) [{status}]")

    print("-" * 80)
    print(f"OVERALL SCORE: {overall_score:.1f}%")
    print("=" * 80)

    # Deployment recommendation
    print("\nDEPLOYMENT RECOMMENDATION:")
    print("-" * 80)

    all_pass = all(score >= target for name, score, target in gates)

    if all_pass and overall_score >= 90:
        print("[READY TO DEPLOY] All critical gates passed")
        print(f"✓ Content Quality: {content_quality_score:.1f}% (target: 98%)")
        print(f"✓ Data Consistency: {data_consistency_score:.1f}% (target: 100%)")
        print(f"✓ SEO Score: {seo_score:.1f}% (target: 85%)")
        print(f"✓ Compliance: {compliance_score:.1f}% (target: 100%)")
    else:
        print("[NEEDS WORK] Some gates failed")
        for name, score, target in gates:
            if score < target:
                print(f"✗ {name}: {score:.1f}% (need {target}%)")

    print("\n" + "=" * 80)

    return overall_score

if __name__ == "__main__":
    quick_test_milton()
