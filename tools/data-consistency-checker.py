#!/usr/bin/env python3
"""
BMAD Data Consistency Checker
Validates that all numbers across the page are consistent
Critical: Even 1 mismatch = FAIL

Version: 1.0 - October 2025
"""

import re
import sys
from collections import defaultdict

class DataConsistencyChecker:
    """Validates global data consistency across the page"""

    def __init__(self, html_file_path):
        self.html_file = html_file_path
        self.html_content = ""
        self.issues = []
        self.warnings = []
        self.pass_count = 0
        self.fail_count = 0

    def run_check(self):
        """Run all consistency checks"""
        print("\n" + "=" * 60)
        print("BMAD DATA CONSISTENCY CHECKER")
        print("=" * 60)

        # Load HTML
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            print(f"[OK] Loaded {self.html_file}")
        except Exception as e:
            print(f"[ERROR] {e}")
            return

        # Run checks
        self.check_phone_numbers()
        self.check_warranty_periods()
        self.check_pricing()
        self.check_ratings()
        self.check_review_counts()
        self.check_service_hours()
        self.check_years_in_business()
        self.check_response_times()

        # Print results
        self.print_report()

    def check_phone_numbers(self):
        """Check all phone numbers are identical"""
        print("\n--- PHONE NUMBER CONSISTENCY ---")

        # Extract all phone numbers
        phone_patterns = [
            r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})',  # 437-747-6737 or 437 747 6737
            r'\((\d{3})\)\s*(\d{3})[-\s]?(\d{4})',  # (437) 747-6737
            r'tel:(\d{10})',  # tel:4377476737
        ]

        phones = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, self.html_content)
            for match in matches:
                if isinstance(match, tuple):
                    # Clean and normalize
                    phone = ''.join(match).replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
                else:
                    phone = match.replace('-', '').replace(' ', '')
                if len(phone) == 10:
                    phones.append(phone)

        if not phones:
            print("[WARN] No phone numbers found")
            self.warnings.append("No phone numbers found on page")
            return

        # Check consistency
        unique_phones = list(set(phones))

        if len(unique_phones) == 1:
            print(f"[OK] Phone number consistent: {phones[0]}")
            print(f"[INFO] Found in {len(phones)} places")
            self.pass_count += 1
        else:
            print(f"[ERROR] Phone number MISMATCH detected!")
            for phone in unique_phones:
                count = phones.count(phone)
                print(f"  - {phone}: {count} occurrences")
            self.issues.append(f"Phone number inconsistent: {unique_phones}")
            self.fail_count += 1

    def check_warranty_periods(self):
        """Check warranty period consistency"""
        print("\n--- WARRANTY PERIOD CONSISTENCY ---")

        # Extract warranty mentions
        warranty_patterns = [
            r'(\d+)[-\s]?day\s+warranty',
            r'(\d+)[-\s]?month\s+warranty',
            r'(\d+)[-\s]?year\s+warranty',
        ]

        warranties = []
        for pattern in warranty_patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            for match in matches:
                warranties.append(match.lower())

        if not warranties:
            print("[WARN] No warranty period found")
            self.warnings.append("No warranty mentioned on page")
            return

        # Check consistency
        unique_warranties = list(set(warranties))

        if len(unique_warranties) == 1:
            print(f"[OK] Warranty period consistent")
            print(f"[INFO] Found in {len(warranties)} places")
            self.pass_count += 1
        else:
            print(f"[ERROR] Warranty period MISMATCH detected!")
            for warranty in unique_warranties:
                count = warranties.count(warranty)
                print(f"  - {warranty}: {count} occurrences")
            self.issues.append(f"Warranty inconsistent: {unique_warranties}")
            self.fail_count += 1

    def check_pricing(self):
        """Check pricing consistency"""
        print("\n--- PRICING CONSISTENCY ---")

        # Extract prices
        price_pattern = r'\$(\d+)'
        prices = re.findall(price_pattern, self.html_content)

        if not prices:
            print("[INFO] No prices found (optional)")
            return

        # Group by price value
        price_counts = defaultdict(int)
        for price in prices:
            price_counts[price] += 1

        # Check for diagnostic fee consistency
        diagnostic_prices = [p for p in prices if p in ['99', '119', '129', '149']]

        if diagnostic_prices:
            unique_diagnostic = list(set(diagnostic_prices))
            if len(unique_diagnostic) == 1:
                print(f"[OK] Diagnostic fee consistent: ${unique_diagnostic[0]}")
                self.pass_count += 1
            else:
                print(f"[ERROR] Diagnostic fee MISMATCH detected!")
                for price in unique_diagnostic:
                    count = diagnostic_prices.count(price)
                    print(f"  - ${price}: {count} occurrences")
                self.issues.append(f"Diagnostic fee inconsistent: ${unique_diagnostic}")
                self.fail_count += 1

    def check_ratings(self):
        """Check rating consistency"""
        print("\n--- RATING CONSISTENCY ---")

        # Extract ratings from specific contexts (avoid CSS line-height etc)
        rating_patterns = [
            r'ratingValue["\']:\s*["\'](\d\.\d)',  # Schema.org
            r'rating["\']:\s*(\d\.\d)',  # JSON
            r'(\d\.\d)\s*[★⭐]+',  # 4.9★
            r'[★⭐]+\s*(\d\.\d)',  # ★4.9
        ]

        ratings = []
        for pattern in rating_patterns:
            matches = re.findall(pattern, self.html_content)
            ratings.extend(matches)

        # Filter valid ratings (4.0-5.0 for business ratings)
        valid_ratings = [r for r in ratings if 4.0 <= float(r) <= 5.0]

        if not valid_ratings:
            print("[WARN] No ratings found")
            self.warnings.append("No ratings displayed on page")
            return

        unique_ratings = list(set(valid_ratings))

        if len(unique_ratings) == 1:
            print(f"[OK] Rating consistent: {unique_ratings[0]}")
            print(f"[INFO] Found in {len(valid_ratings)} places")
            self.pass_count += 1
        else:
            print(f"[ERROR] Rating MISMATCH detected!")
            for rating in unique_ratings:
                count = valid_ratings.count(rating)
                print(f"  - {rating}: {count} occurrences")
            self.issues.append(f"Rating inconsistent: {unique_ratings}")
            self.fail_count += 1

    def check_review_counts(self):
        """Check review count consistency"""
        print("\n--- REVIEW COUNT CONSISTENCY ---")

        # Extract review counts
        review_patterns = [
            r'([\d,]+)\+?\s+reviews?',
            r'([\d,]+)\+?\s+customers?',
            r'reviewCount["\']:\s*["\'](\d+)',
        ]

        review_counts = []
        for pattern in review_patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            # Remove commas for comparison
            review_counts.extend([m.replace(',', '') for m in matches])

        if not review_counts:
            print("[WARN] No review counts found")
            self.warnings.append("No review count displayed")
            return

        unique_counts = list(set(review_counts))

        if len(unique_counts) == 1:
            print(f"[OK] Review count consistent: {unique_counts[0]}")
            print(f"[INFO] Found in {len(review_counts)} places")
            self.pass_count += 1
        else:
            print(f"[ERROR] Review count MISMATCH detected!")
            for count in unique_counts:
                occurrences = review_counts.count(count)
                print(f"  - {count} reviews: {occurrences} occurrences")
            self.issues.append(f"Review count inconsistent: {unique_counts}")
            self.fail_count += 1

    def check_service_hours(self):
        """Check service hours consistency"""
        print("\n--- SERVICE HOURS CONSISTENCY ---")

        # Extract service hours
        hours_patterns = [
            r'(\d+\s*AM\s*-\s*\d+\s*PM)',
            r'(\d+:\d+\s*-\s*\d+:\d+)',
            r'(24/7)',
            r'(24-7)',
        ]

        hours = []
        for pattern in hours_patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            hours.extend([h.replace(' ', '') for h in matches])

        if not hours:
            print("[INFO] No service hours found (optional)")
            return

        unique_hours = list(set(hours))

        if len(unique_hours) == 1:
            print(f"[OK] Service hours consistent: {unique_hours[0]}")
            self.pass_count += 1
        else:
            print(f"[ERROR] Service hours MISMATCH detected!")
            for hour in unique_hours:
                count = hours.count(hour)
                print(f"  - {hour}: {count} occurrences")
            self.issues.append(f"Service hours inconsistent: {unique_hours}")
            self.fail_count += 1

    def check_years_in_business(self):
        """Check years in business consistency"""
        print("\n--- YEARS IN BUSINESS CONSISTENCY ---")

        # Extract years
        year_patterns = [
            r'[Ss]ince\s+(\d{4})',
            r'established\s+(\d{4})',
            r'(\d+)\+?\s+years?\s+(?:in\s+business|experience)',
        ]

        years = []
        for pattern in year_patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            years.extend(matches)

        if not years:
            print("[INFO] No years in business found (optional)")
            return

        unique_years = list(set(years))

        if len(unique_years) == 1:
            print(f"[OK] Years in business consistent: {unique_years[0]}")
            self.pass_count += 1
        else:
            print(f"[ERROR] Years in business MISMATCH detected!")
            for year in unique_years:
                count = years.count(year)
                print(f"  - {year}: {count} occurrences")
            self.issues.append(f"Years inconsistent: {unique_years}")
            self.fail_count += 1

    def check_response_times(self):
        """Check response time consistency"""
        print("\n--- RESPONSE TIME CONSISTENCY ---")

        # Extract response times
        response_patterns = [
            r'same[-\s]day',
            r'(\d+)[-\s]hour',
            r'(\d+)[-\s]minute',
            r'immediate',
            r'instant',
        ]

        responses = []
        for pattern in response_patterns:
            matches = re.findall(pattern, self.html_content, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str):
                    responses.append(pattern.replace(r'[-\s]', ' '))
                else:
                    responses.append(matches[0])

        if not responses:
            print("[INFO] No response times found (optional)")
            return

        # Normalize
        normalized = [r.lower().replace('-', ' ') for r in responses]
        unique_responses = list(set(normalized))

        if len(unique_responses) == 1:
            print(f"[OK] Response time consistent")
            self.pass_count += 1
        else:
            print(f"[WARN] Response time variations detected")
            for resp in unique_responses:
                count = normalized.count(resp)
                print(f"  - {resp}: {count} occurrences")
            self.warnings.append(f"Response time variations: {unique_responses}")

    def print_report(self):
        """Print final report"""
        print("\n" + "=" * 60)
        print("DATA CONSISTENCY REPORT")
        print("=" * 60)

        total_checks = self.pass_count + self.fail_count

        if self.fail_count == 0:
            print("\n[PASS] STATUS: PASS")
            print(f"All {self.pass_count} consistency checks passed!")
        else:
            print("\n[FAIL] STATUS: FAIL")
            print(f"Passed: {self.pass_count}/{total_checks}")
            print(f"Failed: {self.fail_count}/{total_checks}")

        if self.issues:
            print("\n[CRITICAL] CRITICAL ISSUES (Must fix before deployment):")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")

        if self.warnings:
            print("\n[WARN] WARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        print("\n" + "=" * 60)

        if self.fail_count > 0:
            print("[BLOCKED] DEPLOYMENT BLOCKED: Fix all inconsistencies!")
            print("=" * 60)
            return False
        else:
            print("[APPROVED] DEPLOYMENT APPROVED: All data consistent!")
            print("=" * 60)
            return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python data-consistency-checker.py <html-file>")
        sys.exit(1)

    checker = DataConsistencyChecker(sys.argv[1])
    success = checker.run_check()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
