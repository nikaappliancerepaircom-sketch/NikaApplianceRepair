# BMAD 8-Tier Incremental Testing System

## Summary

**✅ NEW UNIFIED SYSTEM CREATED**

Combined the two previous BMAD systems (bmad-v2 and bmad-complete-test.py) into ONE unified 8-tier incremental testing system.

---

## Why 8 Tiers?

**Problem with Previous Approach:**
- Testing all 292 parameters at once caused errors and "hallucinations"
- Too much information to process simultaneously
- Hard to identify specific issues
- Difficult to track progress

**Solution: 8-Tier Incremental Testing**
- Test little by little (по чучуть), not all at once
- Each tier must pass before moving to next
- Clear, focused testing at each step
- Prevents errors and confusion

---

## 8-Tier Structure (292 Parameters Total)

```
TIER 1: Data Consistency        (15 params)  - 100% Required  [BLOCKING]
TIER 2: SEO Foundations         (30 params)  - 98% Required   [CRITICAL]
TIER 3: AI Search               (25 params)  - 98% Required   [CRITICAL]
TIER 4: Content Quality         (40 params)  - 98% Required   [CRITICAL]
TIER 5: Conversion (CRO)        (50 params)  - 85% Required   [HIGH]
TIER 6: Psychology              (45 params)  - 98% Required   [CRITICAL]
TIER 7: Design & UX             (60 params)  - 85% Required   [MEDIUM]
TIER 8: Performance             (27 params)  - 70% Target     [LOW]
```

---

## How It Works

### Incremental Testing Flow:

1. **Start with Tier 1** (Data Consistency)
   - Test ONLY 15 parameters
   - Must achieve 100/100
   - If FAIL → Stop, fix issues, re-test Tier 1
   - If PASS → Move to Tier 2

2. **Move to Tier 2** (SEO Foundations)
   - Test ONLY 30 parameters
   - Must achieve 98/100 (max 1 minor issue)
   - If FAIL → Stop, fix issues, re-test from Tier 2
   - If PASS → Move to Tier 3

3. **Continue through all 8 tiers**
   - Each tier tests specific, focused parameters
   - Each tier has clear pass/fail criteria
   - System stops at first failing critical tier
   - Fix issues incrementally

---

## Tier Descriptions

### TIER 1: Data Consistency (15 params) - 100% REQUIRED

**What it tests:**
- Phone: 437-747-6737 (identical everywhere)
- Reviews: 5,200+ (identical everywhere)
- Rating: 4.9/5 (identical everywhere)
- Warranty: 90-day (identical everywhere)
- Hours: 24/7 (identical everywhere)
- Pricing: $150-$450 (identical everywhere)

**Why critical:**
Inconsistent data confuses Google, hurts trust, and damages SEO.

**Pass criteria:** 100/100 (no exceptions)

---

### TIER 2: SEO Foundations (30 params) - 98% REQUIRED

**What it tests:**
- Title tag: 50-60 chars
- Meta description: 150-160 chars
- H1 tag: Exactly 1 per page
- H2 tags: 5-10 per page
- Canonical URL
- Mobile viewport
- LocalBusiness schema
- Open Graph tags

**Why critical:**
Without these, Google cannot properly index or rank the page.

**Pass criteria:** 98/100 (max 1 minor issue)

---

### TIER 3: AI Search Optimization (25 params) - 98% REQUIRED

**What it tests:**
- FAQPage schema (for Q&A)
- HowTo schema (for processes)
- WebPage schema (for context)
- Schema diversity (4+ types)
- Structured headings (H1 → H2 → H3)

**Why critical:**
AI search engines (ChatGPT, Perplexity, Google AI) are the future. Pages without AI optimization won't rank.

**Pass criteria:** 98/100

---

### TIER 4: Content Quality (40 params) - 98% REQUIRED [CRITICAL]

**What it tests:**
- Word count: 2,000-2,500
- Keyword density: 1.5-2.5%
- Semantic keywords: 8+
- Unique content (no duplication)
- Bullet lists: 3+
- Sections: 8-12
- Internal links: 10+
- Images with alt text: 10+

**Why critical:**
Content quality directly impacts rankings, time on page, and conversions. Google prioritizes high-quality, unique content.

**Pass criteria:** 98/100

---

### TIER 5: Conversion (CRO) (50 params) - 85% REQUIRED

**What it tests:**
- CTA count: 3-8 per page
- Phone tel: links: 8-12
- Phone in header (above fold)
- Workiz booking form
- Form fields: <7 (reduce friction)
- CTA diversity: Call, form, email

**Why important:**
Great SEO means nothing if visitors don't convert. This tier directly impacts revenue.

**Pass criteria:** 85/100

---

### TIER 6: Psychology (45 params) - 98% REQUIRED [CRITICAL]

**What it tests:**
- Rating displays: 3+ mentions
- Review mentions: 3+ mentions
- Authority signals: Licensed, insured, certified
- Urgency triggers: Same-day, 24/7, emergency
- Pain points: Problem identification

**Why critical:**
Psychology drives decision-making. These triggers are essential for converting visitors into customers. Without strong psychological triggers, conversion rates drop significantly.

**Pass criteria:** 98/100

---

### TIER 7: Design & UX (60 params) - 85% REQUIRED

**What it tests:**
- Mobile viewport
- Responsive typography (clamp)
- Mobile CSS breakpoints
- Lazy loading images
- Image alt text (80%+)
- Mobile menu

**Why important:**
60%+ of traffic is mobile. Poor UX = high bounce rate.

**Pass criteria:** 85/100

---

### TIER 8: Performance (27 params) - 70% TARGET

**What it tests:**
- Minified CSS
- Lazy loading images
- Async scripts
- WebP images

**Why lower priority:**
Performance is important but not blocking. A slow page that converts is better than a fast page that doesn't.

**Pass criteria:** 70/100 (target, not required)

---

## How to Use

### Test Single Tier:
```bash
python tools/bmad-8tier-test.py <html-file> --tier N
```

**Example:**
```bash
python tools/bmad-8tier-test.py brands/samsung-appliance-repair-toronto.html --tier 1
python tools/bmad-8tier-test.py brands/samsung-appliance-repair-toronto.html --tier 2
```

### Test All Tiers (Auto-Run):
```bash
python tools/bmad-8tier-test.py <html-file> --auto-run
```

**Example:**
```bash
python tools/bmad-8tier-test.py locations/toronto.html --auto-run
```

**What happens:**
- Runs Tier 1 → Tier 2 → Tier 3 → ... → Tier 8
- Stops at first failing critical tier (Tiers 1-4 and 6)
- Shows detailed report with all issues
- Gives clear next steps

---

## Example Output

```
======================================================================
TIER 1: DATA CONSISTENCY (15 parameters)
Required Score: 100%
======================================================================

✅ PASS - Score: 100/100

======================================================================
TIER 2: SEO FOUNDATIONS (30 parameters)
Required Score: 98%
======================================================================
  ✅ Title tag: Optimal length
  ✅ H1 tag: Exactly 1
  ✅ Canonical URL: Present
  ✅ Mobile viewport: Present
  ✅ LocalBusiness schema: Present
  ✅ Open Graph tags: Present

❌ FAIL - Score: 80/100

Issues:
  ⚠️ Meta description: 134 chars (target: 150-160)
  ⚠️ H2 headings: 15 (target: 5-10)

❌ CRITICAL TIER 2 FAILED - STOPPING
Fix issues and re-run from this tier
```

---

## Deployment Requirements

**For page to be PRODUCTION READY, ALL must pass:**

- ✅ Tier 1: 100% (BLOCKING - no exceptions)
- ✅ Tier 2: 98%+ (CRITICAL - max 1 minor issue)
- ✅ Tier 3: 98%+ (CRITICAL - AI is future)
- ✅ Tier 4: 98%+ (CRITICAL - content is king)
- ✅ Tier 5: 85%+ (HIGH - must convert)
- ✅ Tier 6: 98%+ (CRITICAL - psychology matters)
- ✅ Tier 7: 85%+ (MEDIUM - UX crucial)
- ⚠️ Tier 8: 70%+ (LOW - nice to have, not blocking)

**Overall Score:** Should be 85%+ (90%+ ideal)

---

## Files Created

### New Unified Testing Script:
- `tools/bmad-8tier-test.py` - Main 8-tier testing system

### Documentation:
- `PROJECT-OVERVIEW.md` - Updated with 8-tier methodology
- `docs/BMAD-8TIER-SYSTEM-OVERVIEW.md` - This document

### Old Files (Keep for Reference):
- `tools/bmad-v2/auto-run.py` - Old 4-tier system
- `tools/bmad-complete-test.py` - Old 11-category system

---

## Benefits of 8-Tier System

### ✅ Prevents Errors
- Small, focused tests
- Easy to identify issues
- Clear pass/fail at each step

### ✅ Prevents "Hallucinations"
- Not testing 292 parameters at once
- Incremental, step-by-step approach
- Clear, focused feedback

### ✅ Clear Progress Tracking
- See exactly which tier needs work
- Fix one tier at a time
- Track improvement incrementally

### ✅ Organized by Criticality
- Critical tiers (1-4, 6) must pass 98-100%
- High priority tier (5) must pass 85%
- Medium/Low tiers (7-8) are 70-85%

---

## Samsung Brand Page Example

**Current Status (October 18, 2025):**

```
✅ Tier 1: 100/100 - PASS (Data Consistency)
❌ Tier 2: 80/100 - FAIL (SEO Foundations)
   - Meta description: 134 chars (need 150-160)
   - H2 headings: 15 (need 5-10)

Next Steps:
1. Fix meta description (add 16-26 chars)
2. Reduce H2 headings from 15 to 5-10
3. Re-test Tier 2
4. Once Tier 2 passes, move to Tier 3
```

---

## Workflow

**When optimizing ANY page:**

1. **Test Tier 1 first**
   ```bash
   python tools/bmad-8tier-test.py <page>.html --tier 1
   ```

2. **If Tier 1 fails, fix and re-test Tier 1**
   - Fix data consistency issues
   - Re-run Tier 1
   - Must achieve 100/100

3. **Once Tier 1 passes, move to Tier 2**
   ```bash
   python tools/bmad-8tier-test.py <page>.html --tier 2
   ```

4. **Continue through all 8 tiers incrementally**

5. **OR use auto-run to test all at once:**
   ```bash
   python tools/bmad-8tier-test.py <page>.html --auto-run
   ```
   - Will stop at first failing critical tier
   - Fix issues
   - Re-run from failing tier

---

## Next Steps

1. ✅ Fix Samsung brand page Tier 2 issues
2. Test Samsung through all 8 tiers
3. Use 8-tier system for all future page optimization
4. Update 30 location pages with duplicate content using 8-tier testing

---

**Last Updated:** 2025-10-18
**Version:** 1.0
