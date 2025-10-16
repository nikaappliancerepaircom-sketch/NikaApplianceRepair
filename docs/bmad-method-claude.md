# 🤖 BMAD METHOD FOR CLAUDE - COMPLETE 292 PARAMETER TEST

## 📋 PURPOSE
This document provides step-by-step instructions for Claude AI to test a webpage against ALL 292 BMAD parameters automatically.

**Company:** Nika Appliance Repair
**Domain:** https://nikaappliancerepair.com
**Last Updated:** 2025-10-16
**Version:** 1.1
**Total Parameters:** 292

---

## 🌐 COMPANY INFORMATION

**Domain:** nikaappliancerepair.com
**Business:** Appliance Repair Services
**Service Areas:** Toronto, Mississauga, Brampton, Markham, Vaughan, Richmond Hill, and GTA
**Founded:** 2017
**Experience:** 8+ years
**Phone:** 437-747-6737
**Rating:** 4.9★ (520+ reviews)

**Key Pages:**
- Homepage: https://nikaappliancerepair.com/
- About: https://nikaappliancerepair.com/about
- Online Booking: https://nikaappliancerepair.com/book
- Services: https://nikaappliancerepair.com/services
- Locations: https://nikaappliancerepair.com/locations

**Workiz CRM Integration:**
- All booking forms integrate with Workiz CRM
- Booking URL: https://online-booking.workiz.com/?ac=176dd5d1ce4f69e999d5930a80c1e0109e51c6c46573321e62fe8a71623f0ebb

---

## 🎯 WHEN TO USE THIS TEST

Run this COMPLETE test when user says:
- "test with BMAD method"
- "check all BMAD parameters"
- "run full BMAD test"
- "validate against 290+ parameters"
- "BMAD complete check"

---

## 🚀 AUTOMATIC TEST EXECUTION

### STEP 1: Initialize Test Report

Create a new markdown file: `BMAD-TEST-REPORT-[DATE].md`

```markdown
# BMAD 292 PARAMETER TEST REPORT
**Page Tested:** [URL/File]
**Date:** [Date]
**Tester:** Claude AI
**Status:** IN PROGRESS

## TEST SUMMARY
- Total Parameters: 292
- Passed: 0
- Failed: 0
- In Progress: 292
- Score: 0%

---
```

### STEP 2: Test Category 1 - SEO + AI OPTIMIZATION (45 parameters)

#### 2.1 Read HTML File
```bash
Read index.html or target page
```

#### 2.2 Content Optimization (9 parameters)

**Test 1: Word Count**
- Count all text content words
- ✅ PASS: 1500-2500 words
- ❌ FAIL: <1500 or >2500 words

**Test 2: H1 Tags**
- Use Grep tool: `<h1` pattern
- ✅ PASS: Exactly 1 H1 tag
- ❌ FAIL: 0 or 2+ H1 tags

**Test 3: H2/H3 Hierarchy**
- Grep: `<h2` (count should be 5-10)
- Grep: `<h3` (count should be 12-15)
- ✅ PASS: Proper structure
- ❌ FAIL: Out of range

**Test 4: Internal Links**
- Grep: `<a href="#` or `<a href="/`
- ✅ PASS: 10+ internal links
- ❌ FAIL: <10 links

**Test 5: Images Count**
- Grep: `<img`
- ✅ PASS: 10+ images
- ❌ FAIL: <10 images

**Test 6: Alt Text Coverage**
- Grep: `<img.*alt=""` (find empty alts)
- ✅ PASS: No empty alt tags
- ❌ FAIL: Any img without alt

**Test 7: Trust Signals**
- Search for: warranty, rating, review, certification
- ✅ PASS: 4+ types present
- ❌ FAIL: <4 types

**Test 8: Keyword Density**
- Count main keyword mentions / total words
- ✅ PASS: 1.5-2.5%
- ❌ FAIL: Outside range

**Test 9: Semantic Keywords**
- Check for related terms
- ✅ PASS: 5+ semantic variations
- ❌ FAIL: <5 variations

#### 2.3 Technical SEO (7 parameters)

**Test 10: Title Tag Length**
- Grep: `<title>` extract content
- ✅ PASS: 50-60 characters
- ❌ FAIL: Outside range

**Test 11: Meta Description**
- Grep: `<meta name="description"`
- ✅ PASS: 150-160 characters
- ❌ FAIL: Outside range

**Test 12: Schema Markup**
- Grep: `application/ld+json`
- Check for: LocalBusiness, FAQPage, Service
- ✅ PASS: All 3 present
- ❌ FAIL: Missing any

**Test 13: Mobile Viewport**
- Grep: `<meta name="viewport"`
- ✅ PASS: Present with width=device-width
- ❌ FAIL: Missing or incorrect

**Test 14: HTTPS References**
- Grep: `http://` (not https)
- ✅ PASS: No http:// found
- ❌ FAIL: http:// found

**Test 15: JavaScript Optimization**
- Check for: async, defer, minified
- ✅ PASS: Optimized
- ❌ FAIL: Blocking scripts

**Test 16: Critical CSS Inline**
- Check for: `<style>` in head
- ✅ PASS: Critical CSS inline
- ❌ FAIL: No inline CSS

#### 2.4 AI Optimization (15 parameters)

**Test 17-21: AI Crawler Access**
- Read robots.txt if exists
- Check allows for: GPTBot, Claude-Web, PerplexityBot, Google-Extended, Meta-ExternalAgent
- ✅ PASS: All 5 allowed
- ❌ FAIL: Any blocked

**Test 22: Direct Answer Box**
- Check first 100 words for summary
- ✅ PASS: Clear answer in first 100 words
- ❌ FAIL: No immediate answer

**Test 23: Question-Format H2s**
- Grep all H2 tags, count questions
- ✅ PASS: Most H2s are questions
- ❌ FAIL: <50% questions

**Test 24: HowTo Schema**
- Grep: `"@type": "HowTo"`
- ✅ PASS: Present
- ❌ FAIL: Missing

**Test 25: FAQ Schema**
- Grep: `"@type": "FAQPage"`
- ✅ PASS: Present
- ❌ FAIL: Missing

**Test 26-31: Voice Search Optimization**
- Check for: "near me", conversational tone, tel: links, natural language
- ✅ PASS: All elements present
- ❌ FAIL: Missing elements

#### 2.5 Local SEO (5 parameters)

**Test 32: Location Mentions**
- Count city name mentions
- ✅ PASS: 15-40 mentions
- ❌ FAIL: <15 or >40

**Test 33: LocalBusiness Schema**
- Grep: `"@type": "LocalBusiness"`
- ✅ PASS: Complete with address, phone, etc
- ❌ FAIL: Incomplete

**Test 34: Phone Number Frequency**
- Count phone number appearances
- ✅ PASS: 8+ mentions
- ❌ FAIL: <8 mentions

**Test 35: Neighborhoods**
- Count area/neighborhood mentions
- ✅ PASS: 4+ areas
- ❌ FAIL: <4 areas

**Test 36: Local Keywords**
- Check for: service + location combinations
- ✅ PASS: Present
- ❌ FAIL: Generic only

#### 2.6 User Experience SEO (4 parameters)

**Test 37: Font Sizes**
- Check CSS for base font-size
- ✅ PASS: 16px+ mobile, 18px+ desktop
- ❌ FAIL: Smaller fonts

**Test 38: CTA Diversity**
- Count different CTA types
- ✅ PASS: 3+ types (call, form, chat)
- ❌ FAIL: <3 types

**Test 39: Forms Present**
- Grep: `<form`
- ✅ PASS: Contact/callback form exists
- ❌ FAIL: No forms

**Test 40: Navigation Structure**
- Check nav menu
- ✅ PASS: Clear, logical structure
- ❌ FAIL: Confusing navigation

**✅ SEO + AI PASS CRITERIA: 40/45 parameters (88%+) AND AI crawler access enabled**

---

### STEP 3: Test Category 2 - RESPONSIVE DESIGN (80 parameters)

For EACH of 10 devices, run 8 checks:

#### 3.1 Test Devices (10 total)

**Mobile:**
1. iPhone SE (375×667)
2. iPhone 12 Pro (390×844)
3. Samsung Galaxy S21 (360×800)
4. iPhone 14 Pro Max (430×932)

**Tablet:**
5. iPad Mini (768×1024)
6. iPad Air (820×1180)
7. iPad Pro (1024×1366)

**Desktop:**
8. Laptop (1366×768)
9. Desktop HD (1920×1080)
10. Desktop 4K (2560×1440)

#### 3.2 8 Checks Per Device

**Test 41-48 (iPhone SE):**
1. Check CSS media queries for 375px
2. Verify no overflow-x in CSS
3. Check max-width constraints
4. Test button sizes ≥44px (mobile only)
5. Verify text is ≥16px
6. Check image max-width: 100%
7. Verify form inputs are usable
8. Check for horizontal scroll indicators

**Repeat for all 10 devices = 80 tests total**

**Automated Check:**
```bash
# Check CSS for responsive breakpoints
Grep: "@media.*max-width.*768px" in all CSS files
Grep: "@media.*max-width.*480px" in all CSS files
Grep: "overflow.*hidden" in CSS
Grep: "max-width.*100%" for images
```

**✅ RESPONSIVE PASS CRITERIA: 10/10 devices with 0px overflow, all 80 checks pass**

---

### STEP 4: Test Category 3 - SPEED PERFORMANCE (9 parameters)

**Test 121: CSS File Count**
- Count `<link rel="stylesheet"` tags
- ✅ PASS: ≤3 files or combined
- ❌ FAIL: >3 separate CSS files

**Test 122: JavaScript File Count**
- Count `<script src=` tags
- ✅ PASS: ≤3 files with async/defer
- ❌ FAIL: >3 or blocking scripts

**Test 123: Image Lazy Loading**
- Grep: `loading="lazy"` on images
- ✅ PASS: Most images lazy loaded
- ❌ FAIL: No lazy loading

**Test 124: Image Format**
- Check image extensions
- ✅ PASS: WebP format used
- ❌ FAIL: Only JPG/PNG

**Test 125: Font Families**
- Count different font families
- ✅ PASS: ≤2 font families
- ❌ FAIL: 3+ fonts

**Test 126: CSS Minification**
- Check CSS file names for .min.css
- ✅ PASS: Minified
- ❌ FAIL: Not minified

**Test 127: JS Minification**
- Check JS file names for .min.js
- ✅ PASS: Minified
- ❌ FAIL: Not minified

**Test 128: Resource Hints**
- Grep: `<link rel="preconnect"`
- ✅ PASS: Preconnect present
- ❌ FAIL: No resource hints

**Test 129: Font Optimization**
- Check for WOFF2 format
- ✅ PASS: WOFF2 used
- ❌ FAIL: Other formats only

**✅ SPEED PASS CRITERIA: 8/9 parameters (88%+) AND load time <3s**

---

### STEP 5: Test Category 4 - CROSS-BROWSER COMPATIBILITY (28 parameters)

**Note:** This requires manual browser testing or automated tools. Claude should document requirements:

**Test 130-136 (Chrome - 7 tests):**
1. Page loads without errors
2. Layout renders correctly
3. JavaScript executes properly
4. CSS applies correctly
5. Media queries work
6. Forms are functional
7. No horizontal scroll

**Repeat for:**
- Firefox (Tests 137-143)
- Safari (Tests 144-150)
- Edge (Tests 151-157)

**✅ CROSS-BROWSER PASS CRITERIA: 4/4 browsers fully functional (28/28 tests)**

---

### STEP 6: Test Category 5 - VISUAL DESIGN (30 parameters)

**Test 158: Element Overlap Check**
- Look for position: absolute/fixed conflicts
- ✅ PASS: No overlapping elements
- ❌ FAIL: Elements overlap

**Test 159: Spacing Consistency**
- Check padding/margin values
- ✅ PASS: Multiples of 8px
- ❌ FAIL: Inconsistent spacing

**Test 160-167: Layout Checks**
- Grid alignment, no cutoff, aspect ratios, white space
- ✅ PASS: All layout elements proper
- ❌ FAIL: Layout issues

**Test 168-173: Typography**
- Font hierarchy, line height (1.5-1.8), letter spacing, weights, contrast
- ✅ PASS: Typography properly structured
- ❌ FAIL: Typography issues

**Test 174-179: Colors & Contrast**
- Brand consistency, WCAG contrast ratios
- ✅ PASS: All contrast ≥4.5:1
- ❌ FAIL: Contrast failures

**Test 180-184: Images & Media**
- All load, compressed, alt text, responsive
- ✅ PASS: Images optimized
- ❌ FAIL: Image issues

**Test 185-187: Interactive Elements**
- Hover states, link distinction, validation
- ✅ PASS: All interactive elements clear
- ❌ FAIL: Missing states

**✅ VISUAL PASS CRITERIA: 26/30 parameters (85%+), no critical issues**

---

### STEP 7: Test Category 6 - ACCESSIBILITY (15 parameters)

**Test 188-191: Keyboard Navigation**
- All elements reachable via Tab
- Focus indicators visible
- Logical tab order
- Skip link present

**Test 192-195: Screen Reader**
- All images have alt
- ARIA labels present
- Semantic HTML used
- Form labels associated

**Test 196-198: Color & Contrast**
- Text contrast ≥4.5:1
- Large text ≥3:1
- Color not sole indicator

**Test 199-202: Content Accessibility**
- Heading order logical
- Links descriptive
- Language declared
- Error messages clear

**✅ ACCESSIBILITY PASS CRITERIA: WCAG 2.1 AA compliant, no critical violations**

---

### STEP 8: Test Category 7 - CONTENT QUALITY (15 parameters)

**Test 203-207: Uniqueness & Value**
- Content originality (not copied)
- Expertise demonstration
- Solves user problems
- Fresh information (2025)
- Deep coverage

**Test 208-212: Readability & Structure**
- Reading level Grade 8-10
- Sentence length 15-20 words
- Paragraphs 3-5 sentences
- 3+ lists present
- Logical flow

**Test 213-217: Content Structure**
- 7-12 sections
- Required sections present
- All sections have H2
- Section length ≤500 words
- Visual breaks present

**✅ CONTENT QUALITY PASS CRITERIA: 13/15 parameters (85%+)**

---

### STEP 9: Test Category 8 - CONVERSION RATE OPTIMIZATION (20 parameters)

**Test 218-222: Above The Fold**
- Value proposition clear
- Primary CTA visible
- Phone number prominent (2+ places)
- Trust signal immediate
- Hero image/video present

**Test 223-227: Call-to-Actions**
- 5-8 CTAs on page
- 3+ CTA types
- Action-oriented copy
- High contrast buttons
- Mobile sticky CTA

**Test 228-232: Forms Optimization**
- 3-5 fields maximum
- Form above fold
- Validation clear
- Submit button prominent
- Privacy assurance

**Test 233-237: Friction Reduction**
- No entry popups
- Click-to-call direct
- No registration required
- Fast loading (<3s)
- Simple navigation (5-7 items)

**✅ CRO PASS CRITERIA: 17/20 parameters (85%+), 5+ conversion points**

---

### STEP 10: Test Category 9 - PSYCHOLOGICAL TRIGGERS (25 parameters)

**Test 238-242: Pain-Solve Framework**
- 3+ pain points mentioned
- Emotional pain amplified
- Solution immediate
- Before/After contrast
- Problem→Solution structure

**Test 243-247: AIDA Framework**
- Attention: Headline hooks
- Interest: First paragraph intrigues
- Desire: Benefits > Features
- Action: Multiple CTAs
- AIDA flow present

**Test 248-252: Social Proof**
- 3+ real reviews
- Rating visible (2+ places)
- Specific review count
- Customer photos
- Case studies

**Test 253-257: Scarcity & Urgency**
- Time urgency present
- Limited availability (if true)
- Seasonal urgency
- Emergency framing
- NO false scarcity

**Test 258-262: Authority & Trust**
- Credentials displayed
- Years in business
- Completion stats
- Certifications visible
- Guarantee prominent (3+ mentions)

**✅ PSYCHOLOGY PASS CRITERIA: 21/25 parameters (85%+), all triggers ethical & truthful**

---

### STEP 11: Test Category 10 - DATA CONSISTENCY (15 parameters) ⚠️ CRITICAL

**Test 263-272: Global Numbers Validation**
- Phone number SAME everywhere
- Warranty period consistent
- Service areas consistent
- Pricing consistent
- Years in business consistent
- Review count consistent
- Rating consistent
- Service hours consistent
- Response time consistent
- Brand count consistent

**Test 273-277: Factual Accuracy**
- No fake statistics
- No stock photos as "real customers"
- No fake urgency timers
- No false "#1" claims
- All claims verifiable

**⚠️ CRITICAL: DATA CONSISTENCY = 100% OR ENTIRE TEST FAILS**

**✅ DATA CONSISTENCY PASS CRITERIA: 15/15 parameters (100%), 0 discrepancies**

---

### STEP 12: Test Category 11 - CONVERSION DESIGN (10 parameters)

**Test 278-282: Visual Hierarchy for Conversion**
- F-pattern layout
- Visual flow to CTA
- Color psychology
- White space generous
- Icons meaningful

**Test 283-287: Mobile Conversion Optimization**
- Mobile CTA 44px+, thumb-friendly
- Mobile forms simplified
- Mobile number one-tap
- Mobile images fast
- Mobile menu accessible

**✅ CONVERSION DESIGN PASS CRITERIA: 8/10 parameters (85%+)**

---

## 📊 FINAL REPORT GENERATION

After completing ALL 292 tests, generate final report:

```markdown
# BMAD 292 PARAMETER TEST - FINAL REPORT

**Page:** [URL/File]
**Date:** [Date]
**Tester:** Claude AI

## ✅ OVERALL SCORE

**Total Tests:** 292
**Passed:** [X]
**Failed:** [Y]
**Pass Rate:** [X/292 = Z%]

**DEPLOYMENT STATUS:**
- ✅ APPROVED FOR DEPLOYMENT (if 85%+ all categories)
- ❌ FAILED - REQUIRES FIXES (if <85% any category)

---

## 📊 CATEGORY BREAKDOWN

| Category | Parameters | Passed | Failed | Score | Status |
|----------|------------|--------|--------|-------|--------|
| 1. SEO + AI | 45 | X | Y | Z% | ✅/❌ |
| 2. Responsive | 80 | X | Y | Z% | ✅/❌ |
| 3. Speed | 9 | X | Y | Z% | ✅/❌ |
| 4. Cross-Browser | 28 | X | Y | Z% | ✅/❌ |
| 5. Visual Design | 30 | X | Y | Z% | ✅/❌ |
| 6. Accessibility | 15 | X | Y | Z% | ✅/❌ |
| 7. Content Quality | 15 | X | Y | Z% | ✅/❌ |
| 8. CRO | 20 | X | Y | Z% | ✅/❌ |
| 9. Psychology | 25 | X | Y | Z% | ✅/❌ |
| 10. Data Consistency | 15 | X | Y | Z% | ✅/❌ |
| 11. Conversion Design | 10 | X | Y | Z% | ✅/❌ |

---

## 🚨 CRITICAL ISSUES (Must Fix Before Deployment)

[List all FAILED tests with parameter numbers]

Example:
- ❌ Test 10: Title tag too long (65 chars, should be 50-60)
- ❌ Test 45: Horizontal scroll on iPhone SE (375px width)
- ❌ Test 263: Phone number inconsistent (437-747-6737 in header, 4377476737 in footer)

---

## ⚠️ WARNINGS (Should Fix)

[List tests that passed but are borderline]

---

## ✅ STRENGTHS

[List categories with 90%+ pass rate]

---

## 📋 NEXT STEPS

1. Fix all CRITICAL issues (❌ failures)
2. Address WARNINGS
3. Re-test failed categories
4. Verify data consistency is 100%
5. Run final verification test
6. Deploy only if ALL categories ≥85%

---

## 📞 RECOMMENDATION

**DEPLOY:** Yes/No
**CONFIDENCE:** High/Medium/Low
**ESTIMATED FIX TIME:** [X hours]

---

**Test Completed:** [Timestamp]
**Report Generated By:** Claude AI (BMAD Method v3.0)
```

---

## 🤖 CLAUDE EXECUTION INSTRUCTIONS

### When User Says "BMAD test" or "test 290+ parameters":

1. **Start TodoWrite**:
```json
[
  {"content": "Initialize BMAD 292 test report", "status": "in_progress", "activeForm": "Initializing test"},
  {"content": "Test Category 1: SEO + AI (45 params)", "status": "pending", "activeForm": "Testing SEO"},
  {"content": "Test Category 2: Responsive (80 params)", "status": "pending", "activeForm": "Testing responsive"},
  {"content": "Test Category 3: Speed (9 params)", "status": "pending", "activeForm": "Testing speed"},
  {"content": "Test Category 4: Cross-Browser (28 params)", "status": "pending", "activeForm": "Testing browsers"},
  {"content": "Test Category 5: Visual Design (30 params)", "status": "pending", "activeForm": "Testing design"},
  {"content": "Test Category 6: Accessibility (15 params)", "status": "pending", "activeForm": "Testing accessibility"},
  {"content": "Test Category 7: Content Quality (15 params)", "status": "pending", "activeForm": "Testing content"},
  {"content": "Test Category 8: CRO (20 params)", "status": "pending", "activeForm": "Testing CRO"},
  {"content": "Test Category 9: Psychology (25 params)", "status": "pending", "activeForm": "Testing psychology"},
  {"content": "Test Category 10: Data Consistency (15 params)", "status": "pending", "activeForm": "Testing consistency"},
  {"content": "Test Category 11: Conversion Design (10 params)", "status": "pending", "activeForm": "Testing conversion design"},
  {"content": "Generate final BMAD report", "status": "pending", "activeForm": "Generating report"}
]
```

2. **Read Target File**: `Read index.html` or specified page

3. **Execute Each Category Test**: Use Read, Grep, Bash tools to check parameters

4. **Document Results**: Update TodoWrite as each category completes

5. **Generate Final Report**: Create markdown file with complete results

6. **Present to User**: Show summary + link to full report

---

## 🎯 SUCCESS CRITERIA

**Page PASSES BMAD if:**
- ✅ Overall score ≥ 85% (249+ of 292 parameters pass)
- ✅ Each category ≥ 85% (no weak spots)
- ✅ Data Consistency = 100% (CRITICAL)
- ✅ Responsive works on 10/10 devices
- ✅ No critical accessibility violations

**Page FAILS BMAD if:**
- ❌ Any category < 85%
- ❌ Data Consistency < 100%
- ❌ Horizontal scroll on any device
- ❌ Critical accessibility violations
- ❌ False/fake claims present

---

## 📚 REFERENCE DOCUMENTS

- [BMAD-292-PARAMETERS-CHECKLIST.md](BMAD-292-PARAMETERS-CHECKLIST.md) - Full parameter list
- [BMAD-V2-COMPLETE-METHOD.md](BMAD-V2-COMPLETE-METHOD.md) - Complete methodology
- [BMAD-SCORING-TIERS-EXPLANATION.md](BMAD-SCORING-TIERS-EXPLANATION.md) - Scoring system

---

**Document Version:** 1.0
**Created:** 2025-10-13
**For:** Claude AI (Anthropic)
**Purpose:** Automate 292-parameter BMAD testing
**Status:** Production Ready ✅
