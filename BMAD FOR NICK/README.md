# 📚 BMAD REFERENCE FOLDER - FOR NICK

**Purpose:** All essential documents for understanding and maintaining the Nika Appliance Repair website

**Created:** 2025-10-17
**Status:** ✅ Complete Reference Library

---

## 🎯 READ THESE DOCUMENTS IN THIS ORDER:

### 1. CLAUDE-PROJECT-RULES.md ⭐ START HERE
**What it covers:**
- Project overview and structure
- Business contact data (phone, hours, reviews)
- Tech stack (HTML/CSS/JS, no framework)
- BMAD method introduction
- Word count tools and commands
- SEO strategy basics

**When to read:** Before doing ANYTHING on this project

**Time to read:** 5 minutes

---

### 2. BRAND-AND-SERVICE-FOCUS.md ⭐⭐ CRITICAL
**What it covers:**
- Brand strategy (standard vs luxury positioning)
- Which brands to mention on which pages
- Service focus (9 core residential appliance types)
- Messaging tone by location type
- Geographic rules for luxury brand mentions
- Examples of correct vs incorrect messaging

**When to read:** Before creating OR editing ANY page

**Time to read:** 10 minutes

**⚠️ WARNING:** If you don't read this, you will:
- Put luxury brands (Sub-Zero, Wolf, Miele) on standard area pages (WRONG)
- Use "affordable" messaging in luxury areas like Oakville (WRONG)
- Create inconsistent brand positioning across the site (WRONG)

---

### 3. BMAD-METHOD-OVERVIEW.md ⭐⭐ CRITICAL
**What it covers:**
- BMAD 292-parameter testing methodology
- All 11 categories explained
- Category 1 (SEO-AI) - 45 parameters
- Category 10 (Data Consistency) - 15 parameters
- Scoring system and thresholds
- Common BMAD failures and fixes
- Production readiness checklist

**When to read:** Before creating new pages, or when fixing BMAD issues

**Time to read:** 15 minutes

**Why critical:** This explains HOW to make pages that rank in Google and convert visitors to customers.

---

### 4. BMAD-FINAL-COMPLIANCE-REPORT.md
**What it covers:**
- Complete audit results for all 32 location pages
- Category 1 (SEO-AI): 100% ✅
- Category 10 (Data Consistency): 100% ✅
- All fixes applied (review count, title tags, tel: links)
- Before/after comparison
- Verification commands

**When to read:** To understand what has already been fixed and verified

**Time to read:** 10 minutes

**Use case:** Reference document showing the project is production-ready

---

### 5. PROJECT-COMPLETION-SUMMARY.md
**What it covers:**
- 20 new location pages created
- All 32 pages now BMAD-compliant
- Scripts created (reusable)
- Documentation updates
- Word count verification results
- Deployment approval status

**When to read:** To see the full project scope and deliverables

**Time to read:** 8 minutes

**Use case:** Project history and completion metrics

---

## 🚨 QUICK REFERENCE: WHAT TO CHECK BEFORE PUBLISHING ANY PAGE

### Critical Checklist (Must Be 100%)

**Data Consistency:**
- [ ] Phone: 437-747-6737 (8-12 mentions, all clickable)
- [ ] Reviews: 5,200+ Reviews (not 520+)
- [ ] Rating: 4.9/5
- [ ] Warranty: 90-day
- [ ] Pricing: $150-$450

**Brand Consistency:**
- [ ] Standard areas (28 cities): Samsung, LG, Whirlpool, GE ONLY
- [ ] Luxury areas (4 cities): Sub-Zero, Wolf, Miele + Samsung, LG
- [ ] NO luxury brands in Oshawa, Ajax, Brampton, etc.

**SEO Requirements:**
- [ ] Title tag: 50-60 characters
- [ ] Meta description: 150-160 characters
- [ ] Word count: 2,000-2,500 (check with `node tools/count-visible-words.js`)
- [ ] Schema: LocalBusiness + FAQPage
- [ ] H1: Exactly 1
- [ ] H2: 5-10
- [ ] H3: 12-15
- [ ] Images: 10+ with alt text

---

## 📊 LOCATION TYPE QUICK REFERENCE

### LUXURY AREAS (4 cities) - Use Premium Messaging
- Oakville
- Markham
- Richmond Hill
- Vaughan

**Brands:** Sub-Zero, Wolf, Miele, Thermador + Samsung, LG
**Tone:** "White-glove service", "luxury appliance specialists", "discreet appointments"

---

### STANDARD AREAS (28 cities) - Use Affordable Messaging
- Toronto, Mississauga, Brampton
- Etobicoke, North York, Scarborough
- Ajax, Pickering, Oshawa, Whitby, Clarington, Scugog, Brock
- Aurora, Newmarket, Bradford, Stouffville, King, East Gwillimbury, Georgina
- Milton, Burlington, Oakville, Halton Hills
- Caledon, Orangeville, Mono, Uxbridge, Innisfil

**Brands:** Samsung, LG, Whirlpool, GE, Maytag, Frigidaire ONLY
**Tone:** "Affordable rates", "transparent pricing", "honest service", "quick turnaround"

---

## 🔧 TOOLS & COMMANDS

### Word Count Check:
```bash
node tools/count-visible-words.js locations/city.html
```
**Target:** 2,000-2,500 words (visible content only, no HTML/CSS/JS)

### BMAD Audit:
```bash
python tools/bmad-v2/auto-run.py locations/city.html
```

### Find Review Count Issues:
```powershell
Get-ChildItem -Path "C:\NikaApplianceRepair\locations" -Filter "*.html" |
    ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -match '520\+ Reviews') {
            Write-Host "FAIL: $($_.Name)"
        }
    }
```

### Find Unlinked Phone Numbers:
```powershell
Get-ChildItem -Path "C:\NikaApplianceRepair\locations" -Filter "*.html" |
    ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $plainPhones = ([regex]::Matches($content, '(?<!href="tel:)\(437\)\s*747-6737') | Measure-Object).Count
        if ($plainPhones -gt 0) {
            Write-Host "FAIL: $($_.Name) has $plainPhones unlinked phones"
        }
    }
```

---

## 🚀 SCRIPTS AVAILABLE

All scripts in `C:\NikaApplianceRepair\scripts\`:

1. **fix-critical-bmad-issues.ps1** - Fix data consistency (reviews, phone, warranty)
2. **fix-category1-seo-ai.ps1** - Add tel: links to phone numbers
3. **fix-title-tags.ps1** - Optimize title tags to 50-60 chars
4. **fix-double-tel-links.ps1** - Fix nested tel: links that break colors
5. **check-all-20-word-counts.ps1** - Check word counts on all pages
6. **generate-remaining-locations.ps1** - Generate new location pages from template

---

## ❓ COMMON QUESTIONS

### Q: How do I know if a city is "luxury" or "standard"?
**A:** Only 4 cities are luxury: Oakville, Markham, Richmond Hill, Vaughan. All others are standard.

### Q: Can I mention Sub-Zero in a standard area like Ajax?
**A:** NO. Only mention Sub-Zero, Wolf, Miele, Viking, Thermador in the 4 luxury cities.

### Q: What if the word count is 1,800 (below 2,000)?
**A:** Add more content:
- More neighborhood descriptions
- More FAQs (aim for 6-8)
- More service details
- More appliance brand mentions

### Q: What if the word count is 3,200 (above 2,500)?
**A:** Generally OK. More content = better SEO. Only reduce if over 3,500 words.

### Q: How do I check if a page is BMAD compliant?
**A:** Run: `python tools/bmad-v2/auto-run.py locations/city.html`
- Category 1 (SEO-AI) must be 100%
- Category 10 (Data Consistency) must be 100%

### Q: Can I change the phone number?
**A:** NO. It must be 437-747-6737 everywhere. Changing it breaks Category 10 (Data Consistency).

### Q: Can I change the review count?
**A:** NO. It must be "5,200+ Reviews" everywhere. Changing it breaks Category 10.

### Q: What's the difference between "word count" and "file size"?
**A:**
- **Word count:** Visible text only (what users read) - Target: 2,000-2,500
- **File size:** Entire HTML file including all HTML tags, CSS, JavaScript - Ignore this

Use `node tools/count-visible-words.js` to check word count (not file size).

---

## 🎯 YOUR GOAL AS NICK

**When creating or editing pages:**

1. ✅ Read BRAND-AND-SERVICE-FOCUS.md first
2. ✅ Check if city is luxury or standard
3. ✅ Use correct brand mentions
4. ✅ Use correct messaging tone
5. ✅ Verify phone: 437-747-6737 (8-12 clickable mentions)
6. ✅ Verify reviews: 5,200+ Reviews
7. ✅ Verify warranty: 90-day
8. ✅ Check word count: 2,000-2,500
9. ✅ Run BMAD audit to verify 100% on Category 1 & 10
10. ✅ Deploy with confidence

**Your pages should score:**
- Category 1 (SEO-AI): 100%
- Category 10 (Data Consistency): 100%
- Overall: 90%+ minimum

---

## 📞 DATA TO MEMORIZE

**Phone:** 437-747-6737
**Reviews:** 5,200+ Reviews
**Rating:** 4.9/5
**Warranty:** 90-day
**Pricing:** $150-$450
**Years:** Since 2017
**Schema Price Range:** $$

**Popular Brands (Standard Areas):** Samsung, LG, Whirlpool, GE, Maytag, Frigidaire
**Luxury Brands (4 Cities Only):** Sub-Zero, Wolf, Miele, Thermador

**Luxury Cities (ONLY 4):** Oakville, Markham, Richmond Hill, Vaughan

**Word Count Target:** 2,000-2,500 visible words

---

## ✅ PROJECT STATUS

**Total Location Pages:** 32
- 20 new pages created (2025-10-17)
- 12 existing pages updated (2025-10-17)

**BMAD Compliance:**
- Category 1 (SEO-AI): 100% ✅ (all 32 pages)
- Category 10 (Data Consistency): 100% ✅ (all 32 pages)

**Production Status:** ✅ READY FOR DEPLOYMENT

**Next Steps:**
1. Deploy to production
2. Submit sitemap to Google Search Console
3. Monitor SEO rankings
4. Monitor AI search appearances (ChatGPT, Perplexity)
5. Track conversion rates per city

---

## 📖 FOLDER CONTENTS

```
BMAD FOR NICK/
├── README.md (this file)
├── CLAUDE-PROJECT-RULES.md (project overview)
├── BRAND-AND-SERVICE-FOCUS.md ⭐ (brand/service positioning)
├── BMAD-METHOD-OVERVIEW.md ⭐ (292-parameter methodology)
├── BMAD-FINAL-COMPLIANCE-REPORT.md (audit results)
└── PROJECT-COMPLETION-SUMMARY.md (project deliverables)
```

**Total Reading Time:** ~50 minutes to read all documents

**Recommended Order:**
1. CLAUDE-PROJECT-RULES.md (5 min)
2. BRAND-AND-SERVICE-FOCUS.md (10 min) ⭐ CRITICAL
3. BMAD-METHOD-OVERVIEW.md (15 min) ⭐ CRITICAL
4. BMAD-FINAL-COMPLIANCE-REPORT.md (10 min)
5. PROJECT-COMPLETION-SUMMARY.md (8 min)

---

**This folder contains EVERYTHING you need to maintain and expand the Nika Appliance Repair website.**

**Questions? Read BRAND-AND-SERVICE-FOCUS.md and BMAD-METHOD-OVERVIEW.md again. 95% of questions are answered there.**

---

**Created:** 2025-10-17
**Status:** ✅ Complete Reference Library
**Version:** 1.0

**Happy building! 🚀**
