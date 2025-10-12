# BMAD v2 - Agent-Based Optimization System

## Overview

**BMAD v2** is a comprehensive website optimization framework with **277 parameters** across **9 Tiers**, featuring:

- ✅ **60% automation** via Python scripts and AI agents
- 🤖 **Agent-based testing** for complex validations
- 📊 **Tier-based prioritization** (critical → optional)
- 🚪 **Deployment gates** ensuring quality
- ⚡ **10-minute** quick optimization or **20-hour** complete audit

---

## Quick Start

### 1. Basic Optimization (Tiers 1-2, ~10 minutes)

```bash
# Optimize homepage with auto-fix
./tools/bmad-v2/bmad-optimize.sh index.html 2

# Output:
# ✅ Tier 1: 100/100 (Critical - PASSED)
# ✅ Tier 2: 87/100 (SEO+CRO - EXCELLENT)
# ✅ DEPLOYMENT: APPROVED
```

### 2. Production-Ready (Tiers 1-4, ~2 hours)

```bash
# Full production optimization
./tools/bmad-v2/bmad-optimize.sh index.html 4

# Output:
# ✅ Tier 1: 100/100 (Critical)
# ✅ Tier 2: 85/100 (SEO+CRO)
# ✅ Tier 3: 72/100 (Content+UX)
# ✅ Tier 4: 80/100 (Performance)
# ✅ DEPLOYMENT: APPROVED
```

### 3. Manual Testing (No Auto-Fix)

```bash
# Test only, don't modify file
./tools/bmad-v2/bmad-optimize.sh index.html 4 false

# Get report without changes
```

---

## Tier Structure

### 🔴 Tier 1: Critical Foundation (15 params) - **100% REQUIRED**
- **Blocks deployment** if < 100%
- Data consistency (phone, hours, warranty, rating)
- Core technical (schemas, H1, viewport, HTTPS)
- **Time:** 2 minutes (100% automated)
- **Script:** `tests/tier1_critical.py` + `fixers/tier1_fixer.py`

**Example issues fixed:**
- ❌ Phone: "437-747-6737" vs "4377476737" → ✅ Normalize to "437-747-6737"
- ❌ Rating: "4.9★" vs "4.9/5" vs "4.9 stars" → ✅ Normalize to "4.9/5"
- ❌ Missing LocalBusiness schema → ✅ Generate and inject

### ⭐ Tier 2: SEO + CRO Core (30 params) - **85% TARGET**
- **Warning** if < 85%
- SEO: Meta tags, schemas, keywords, images
- CRO: CTAs, forms, trust signals, social proof
- **Time:** 5 minutes (75% automated)
- **Scripts:** `tests/tier2_seo.py`, `tests/tier2_cro.py`

**Example fixes:**
- ✅ Generate meta description (160 chars)
- ✅ Add FAQPage schema from FAQ section
- ✅ Add ImageObject schemas for SEO
- ⚠️ Flag: Keyword density 3.8% (manual: add content)

### 🎨 Tier 3: Content + Basic UX (50 params) - **70% TARGET**
- **Recommended** but not blocking
- Content: Paragraphs, readability, authority, pain points
- UX: Responsive, accessibility, forms, navigation
- **Time:** 5 hours (40% automated, 60% manual)
- **Scripts:** `tests/tier3_content.py`, `tests/tier3_ux.py`

**Manual work required:**
- Break long paragraphs (≤5 sentences)
- Add authority signals ("Licensed", "Certified")
- Improve readability (Flesch 60+)
- Test responsive on multiple devices

### ⚡ Tier 4: Performance + Speed (25 params) - **80% TARGET**
- **High impact** on UX
- Core Web Vitals, image optimization, minification
- PageSpeed 85+ desktop, 75+ mobile
- **Time:** 2 hours (60% automated)
- **Script:** `tests/tier4_performance.py`

**Automated fixes:**
- ✅ Add `loading="lazy"` to images
- ✅ Add width/height to prevent CLS
- ✅ Minify CSS/JS
- ✅ Add preconnect/dns-prefetch
- ⚠️ Flag: LCP > 2.5s (manual: optimize hero image)

### 🌐 Tier 5-9: Advanced (157 params) - **OPTIONAL**
- **Tier 5:** Cross-browser + responsive (70% target)
- **Tier 6:** Advanced UX + features (60% target)
- **Tier 7:** Analytics + tracking (70% target)
- **Tier 8:** Content features (50% target)
- **Tier 9:** Integrations + polish (40% target)

---

## File Structure

```
tools/bmad-v2/
├── bmad-optimize.sh          # Main optimization script
├── agent-coordinator.py       # Agent execution manager
├── get-score.py              # Score extraction utility
│
├── config/
│   └── business-data.json    # Global data configuration
│
├── tests/                    # Test scripts per tier
│   ├── tier1_critical.py
│   ├── tier2_seo.py
│   ├── tier2_cro.py
│   ├── tier3_content.py
│   ├── tier3_ux.py
│   ├── tier4_performance.py
│   ├── tier5_browser.py
│   ├── tier5_responsive.py
│   └── ...
│
├── fixers/                   # Auto-fix scripts
│   ├── tier1_fixer.py
│   ├── tier2_fixer.py
│   ├── tier3_fixer.py
│   └── tier4_fixer.py
│
└── reports/                  # Generated reports
    └── bmad-report-*.json
```

---

## Configuration

Edit global business data in `config/business-data.json`:

```json
{
  "phone": "437-747-6737",
  "hours": "Mon-Fri 8-20, Sat 9-18, Sun 10-17",
  "warranty": "90-day",
  "rating": "4.9",
  "reviews": "5200",
  "since": "2019",
  "address": {
    "street": "60 Walter Tunny Cresent",
    "city": "East Gwillimbury",
    "province": "ON",
    "postal": "L9N 0R3"
  },
  "email": "care@niappliancerepair.ca"
}
```

All Tier 1 tests validate against this config.

---

## Deployment Gates

### Gate 1: Tier 1 = 100% (BLOCKING)
```bash
IF Tier 1 < 100%:
  🔴 BLOCK deployment
  → Fix data inconsistencies manually
  → Re-run until 100%
```

**Why blocking:**
- Inconsistent phone numbers = lost leads
- Missing schemas = poor Google rankings
- Wrong data = customer confusion

### Gate 2: Tier 2 ≥ 85% (WARNING)
```bash
IF Tier 2 ≥ 85%:
  ✅ APPROVED - Excellent SEO+CRO

IF Tier 2 = 80-84%:
  ⚠️ APPROVED WITH WARNING
  → Consider improving before deployment

IF Tier 2 < 80%:
  ⚠️ NOT RECOMMENDED
  → Improve SEO/CRO parameters
```

### Gate 3: Tier 3-4 ≥ 70% (INFORMATIONAL)
```bash
IF Tier 3-4 ≥ 70%:
  ✅ GOOD QUALITY
  → High-quality user experience

IF Tier 3-4 < 70%:
  ℹ️ ACCEPTABLE
  → Not blocking, but improvement recommended
```

---

## Command Reference

### Basic Commands

```bash
# Optimize single tier
./bmad-optimize.sh index.html 1          # Tier 1 only
./bmad-optimize.sh index.html 2          # Tiers 1-2
./bmad-optimize.sh index.html 4          # Tiers 1-4 (recommended)

# Test without modifications
./bmad-optimize.sh index.html 4 false    # No auto-fix

# Run Python coordinator directly
python agent-coordinator.py index.html 1       # Tier 1
python agent-coordinator.py index.html all     # All tiers
python agent-coordinator.py index.html all --no-fix  # Test only
```

### Batch Operations

```bash
# Optimize all service pages
for file in services/*.html; do
  ./bmad-optimize.sh "$file" 4
done

# Generate reports for all pages
for file in *.html; do
  python agent-coordinator.py "$file" all --no-fix
done
```

---

## Understanding Scores

### Score Interpretation

| Tier | Score | Meaning | Action |
|------|-------|---------|--------|
| **1** | 100% | ✅ Perfect | Deploy |
| **1** | < 100% | 🔴 Critical issues | BLOCK - Fix immediately |
| **2** | 85-100% | ✅ Excellent | Deploy |
| **2** | 80-84% | ⚠️ Good | Deploy with warning |
| **2** | < 80% | ⚠️ Needs work | Improve before deploy |
| **3-4** | 70-100% | ✅ Good quality | Continue |
| **3-4** | < 70% | ℹ️ Acceptable | Optional improvements |

### What Each Score Means

**Tier 1: 95/100**
- 1 of 15 critical parameters failed
- Likely: Phone inconsistency or missing schema
- **Impact:** High - blocks deployment
- **Fix time:** 2-5 minutes

**Tier 2: 82/100**
- 5-6 of 30 SEO/CRO parameters need work
- Likely: Keyword density high, too many CTAs
- **Impact:** Medium - approved but with warning
- **Fix time:** 1-2 hours (content work)

**Tier 3: 68/100**
- 16 of 50 content/UX parameters below target
- Likely: Long paragraphs, missing accessibility
- **Impact:** Low - informational only
- **Fix time:** 3-5 hours (manual work)

---

## Automation Breakdown

### What Gets Auto-Fixed (60% of 277 params)

**Tier 1 (100% automated):**
- ✅ Data normalization (phone, hours, warranty)
- ✅ Schema generation (LocalBusiness, Rating, FAQ)
- ✅ H1 validation (convert extras to H2)
- ✅ HTTPS links (http:// → https://)

**Tier 2 (75% automated):**
- ✅ Meta tags (title, description, OG, Twitter)
- ✅ Image SEO (ImageObject schemas, alt text)
- ✅ Canonical tags
- ✅ Breadcrumb schemas
- ⚠️ Manual: Keyword density, CTA optimization

**Tier 3 (40% automated):**
- ✅ Lazy loading images
- ✅ ARIA labels for icons
- ✅ Focus indicators
- ✅ Skip navigation link
- ⚠️ Manual: Content structure, readability

**Tier 4 (60% automated):**
- ✅ Image dimensions (width/height)
- ✅ CSS/JS minification
- ✅ Preconnect/prefetch tags
- ✅ Defer non-critical JS
- ⚠️ Manual: Image compression, LCP optimization

### What Requires Manual Work (40%)

- 📝 **Content writing** (paragraphs, FAQ expansion)
- 🎨 **Design decisions** (CTA placement, hierarchy)
- 🔧 **Complex optimizations** (LCP, TBT, CLS fixes)
- 🧪 **Testing** (cross-browser, responsive, user testing)

---

## Real-World Results

### Homepage Optimization (Our Experience)

**Before BMAD:**
- Tier 1: 87% (data inconsistencies)
- Tier 2: 65% (missing schemas, poor meta tags)
- Tier 3: 50% (long paragraphs, no accessibility)
- Tier 4: 60% (slow PageSpeed, no lazy loading)

**After BMAD v2 (7 hours work):**
- Tier 1: 100% ✅ (all data consistent)
- Tier 2: 88% ✅ (excellent SEO+CRO)
- Tier 3: 74% ✅ (good content quality)
- Tier 4: 82% ✅ (fast page load)

**Issues Fixed:**
1. ✅ Response time inconsistency (5-min → 45-min) - CRITICAL
2. ✅ Fake countdown timer removed - BMAD violation
3. ✅ 12 data inconsistencies normalized
4. ✅ 8 missing schemas added
5. ✅ Meta description generated (160 chars)
6. ✅ 15+ images optimized (SEO schemas + lazy loading)

**Deployment:** ✅ APPROVED

### Service Pages (11 Pages Optimized)

**Average Scores:**
- Tier 1: 100% (all pages)
- Tier 2: 80.9% (range: 76-83%)
- Tier 3: ~75% (estimated)

**Time per page:**
- Automation: 5 minutes
- Manual content: 2-4 hours
- **Total:** ~5 hours per page

**Deployment:** ✅ ALL APPROVED

---

## Troubleshooting

### Issue: "Tier 1 stuck at 93%"

**Diagnosis:**
```bash
# Run verbose test
python tests/tier1_critical.py index.html --verbose

# Look for failed params
```

**Common causes:**
- Phone number inconsistent (e.g., "437-747-6737" vs "4377476737")
- Rating varies (e.g., "4.9★" vs "4.8/5")
- Missing LocalBusiness or AggregateRating schema

**Fix:**
```bash
# Run fixer
python fixers/tier1_fixer.py index.html

# If still failing, manual grep:
grep -n "437" index.html  # Check all phone occurrences
grep -n "4\." index.html  # Check all ratings
```

### Issue: "Tier 2 at 78%, can't reach 85%"

**Common blockers:**
- Keyword density too high (3.5%+ vs target 1.5-2.5%)
- Too many CTAs (12+ vs optimal 5-7)
- Value proposition unclear

**Manual fixes:**
1. Add 300-500 words of semantic content (dilute keywords)
2. Remove duplicate CTAs
3. Rewrite hero section with clear benefit

---

## Advanced Usage

### Custom Agent Development

Create your own specialized agent:

```python
# tools/bmad-v2/tests/tier_custom.py

class CustomAgent:
    def __init__(self, file_path):
        self.file_path = file_path

    def test_custom_param(self):
        # Your logic here
        return {"status": "pass", "score": 100}

    def run(self):
        results = []
        results.append(self.test_custom_param())
        return results
```

Register in `agent-coordinator.py`:

```python
self.agents["custom-agent"] = {
    "tier": 10,
    "params": 5,
    "description": "My custom checks",
    "auto_fix": False,
    "script": "tests/tier_custom.py"
}
```

---

## Support

### Documentation
- **Full method:** `docs/BMAD-V2-COMPLETE-METHOD.md`
- **Strategy:** `HOMEPAGE-OPTIMIZATION-STRATEGY.md`
- **Quick reference:** `QUICK-REFERENCE-CARD.md`

### Common Questions

**Q: Can I skip Tier 1?**
**A:** No. Tier 1 is mandatory and blocks deployment if < 100%.

**Q: How long does full optimization take?**
**A:**
- Quick (Tier 1-2): ~10 minutes
- Production (Tier 1-4): ~7 hours
- Complete (Tier 1-9): ~20 hours

**Q: Can I run tests without modifying files?**
**A:** Yes: `./bmad-optimize.sh file.html 4 false`

**Q: What if I disagree with a parameter?**
**A:** Tiers 3-9 are informational. Tier 1-2 are based on proven best practices, but you can customize `config/business-data.json`.

---

## Version History

### v2.0 (2025-10-12)
- ✅ Restructured to 9 Tiers (was 4)
- ✅ Added agent-based testing system
- ✅ Increased automation to 60%
- ✅ Added deployment gates
- ✅ Comprehensive documentation

### v1.0 (2025-10-10)
- Initial BMAD framework
- 4 Tiers, 277 parameters
- Basic automation

---

**Created by:** Nika Appliance Repair + Claude Code
**Methodology:** BMAD (Best Method for Appliance Documentation)
**License:** Proprietary
**Status:** ✅ Production Ready
