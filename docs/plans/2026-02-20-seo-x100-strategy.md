# SEO x100 Growth Strategy — nikaappliancerepair.com

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Grow organic traffic 100x from ~250 clicks/90 days to 25,000+ clicks/90 days by dominating local appliance repair searches in Toronto GTA.

**Architecture:** 5-phase approach — Fix blockers → Optimize existing pages → Build authority → Create targeted content → Dominate AI search.

**Tech Stack:** Static HTML, Google Search Console API, DataForSEO API, Schema.org JSON-LD, llms.txt

---

## Current State Snapshot (Feb 2026)

| Metric | Now | Target (12 months) |
|--------|-----|-------------------|
| Clicks/90 days | ~250 | 25,000+ |
| Avg position | 18-20 | 5-8 |
| Indexed pages | 106/299 | 280+ |
| CTR | 0.4-1.2% | 4-8% |
| Brand pages CTR | 0.2-0.8% | 3-5% |
| Service pages clicks | ~5/month | 500+/month |

## Critical Issues Found

1. **193 pages NOT indexed** — 4 unknown reasons (must diagnose first)
2. **Service pages invisible** — oven repair: 584 impressions, 0 clicks, pos 14.9
3. **Brand pages waste** — LG: 2,772 impressions, 8 clicks, 0.3% CTR
4. **Blog CTR catastrophe** — compressor noise: 6,091 impressions, 0.4% CTR, pos 7
5. **"appliance repair toronto" not ranking** — main keyword absent
6. **No backlinks** — DA very low, new domain
7. **Two domains confusion** — nikaappliancerepair.com vs nappliancerepair.ca (verify canonicals)
8. **Sitemap** — 123 submitted, indexed showing 0 via sitemap

---

## PHASE 1 — Fix Critical Blockers (Week 1-2)

### Task 1: Diagnose 193 Not-Indexed Pages

**Why:** 193 pages stuck = half the site invisible to Google. Fix this first.

**Step 1: Check GSC Page Indexing → "Not indexed" → see 4 reasons**
Go to GSC → Indexing → Pages → click "193 Not indexed" → screenshot the 4 reason categories.

Common reasons to check:
- "Crawled - currently not indexed" (thin content or duplicate)
- "Discovered - currently not indexed" (crawl budget)
- "Duplicate without user-selected canonical" (canonical issues)
- "Page with redirect" (redirect problems)

**Step 2: Check for duplicate domain issue**
```bash
# Check if nappliancerepair.ca redirects to nikaappliancerepair.com
curl -I https://nappliancerepair.ca/
# Expected: 301 redirect to nikaappliancerepair.com
# If NOT redirecting: this is causing duplicate content → not indexed
```

**Step 3: Check canonical tags on non-indexed pages**
```bash
grep -r "canonical" C:/NikaApplianceRepair/locations/*.html | grep -v "nikaappliancerepair.com"
grep -r "canonical" C:/NikaApplianceRepair/blog/**/*.html | grep "nappliancerepair"
```
Any canonical pointing to wrong domain = fix immediately.

**Step 4: Check for noindex tags**
```bash
grep -rn "noindex" C:/NikaApplianceRepair/ --include="*.html" | grep -v ".git"
```

**Step 5: Check page speed — slow pages get dropped**
```bash
# Test key pages with PageSpeed API
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://nikaappliancerepair.com/locations/north-york&strategy=mobile" | node -e "const d=require('fs').readFileSync('/dev/stdin','utf8'); const j=JSON.parse(d); console.log('LCP:', j.lighthouseResult.audits['largest-contentful-paint'].displayValue, 'Score:', j.lighthouseResult.categories.performance.score*100)"
```

**Commit:** `fix: diagnose and document indexing blockers`

---

### Task 2: Fix Sitemap — 123 Submitted / 0 Indexed via Sitemap

**Step 1: Check current sitemap**
```bash
curl https://nikaappliancerepair.com/sitemap.xml | head -50
```

**Step 2: Check if sitemap URLs match canonical URLs exactly**
```bash
# Extract URLs from sitemap
curl https://nikaappliancerepair.com/sitemap.xml | grep "<loc>" | sed 's/.*<loc>//;s/<\/loc>//' > /tmp/sitemap-urls.txt

# Count
wc -l /tmp/sitemap-urls.txt

# Check for trailing slash inconsistency
grep "/$" /tmp/sitemap-urls.txt | head -10
grep -v "/$" /tmp/sitemap-urls.txt | grep -v ".xml" | head -10
```

**Step 3: Regenerate sitemap with correct format**

File to modify: `C:/NikaApplianceRepair/sitemap.xml`

Rules for Google to index via sitemap:
- Must match canonical URL EXACTLY (with/without trailing slash)
- Must include `<lastmod>` dates
- Priority: service pages 0.9, location pages 0.8, brand pages 0.7, blog 0.6

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Homepage -->
  <url>
    <loc>https://nikaappliancerepair.com/</loc>
    <lastmod>2026-02-20</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- Service pages - priority 0.9 -->
  <url>
    <loc>https://nikaappliancerepair.com/services/dryer-repair</loc>
    <lastmod>2026-02-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <!-- ... all service, location, brand, blog pages -->
</urlset>
```

**Step 4: Submit updated sitemap in GSC**
GSC → Sitemaps → Add new sitemap → `sitemap.xml` → Submit

**Commit:** `fix: regenerate sitemap with correct URLs and priorities`

---

### Task 3: CTR Fix — Top 10 High-Impression Pages

**Why:** These pages already rank, just need better titles to get clicks. Fastest ROI.

**Target pages (by impression volume):**

| Page | Impressions | Current CTR | Target CTR |
|------|------------|-------------|------------|
| /blog/.../refrigerator-compressor-noise-diagnosis | 6,091 | 0.4% | 4% |
| /brands/lg-appliance-repair-toronto | 2,772 | 0.3% | 3% |
| /brands/samsung-appliance-repair-toronto | 2,469 | 0.2% | 3% |
| /services/washer-repair | 773 | 0.1% | 3% |
| /services/oven-repair | 584 | 0% | 3% |
| /brands/bosch-appliance-repair-toronto | 1,885 | 0.7% | 3% |

**CTR Formula for local service pages:**
```
[Keyword] Toronto | Same-Day | [USP] | Nika Appliance Repair
```

**Step 1: Fix compressor noise blog post**

File: `C:/NikaApplianceRepair/blog/troubleshooting/refrigerator-compressor-noise-diagnosis.html`

Change `<title>` from:
```
Refrigerator Compressor Noise Diagnosis: Complete Troubleshooting Guide Toronto 2025
```
To:
```
Refrigerator Making Noise? Fix Compressor Sounds Today | Toronto Guide
```

Change `<meta name="description">` to:
```
Clicking, buzzing or grinding refrigerator? Toronto expert guide: 7 compressor noises diagnosed. Most fixed for $200-400. Same-day repair available. Call 437-524-1053.
```

**Step 2: Fix LG brand page**

File: `C:/NikaApplianceRepair/brands/lg-appliance-repair-toronto.html`

`<title>`:
```
LG Appliance Repair Toronto | Same-Day Service | 90-Day Warranty
```
`<meta description>`:
```
Certified LG repair in Toronto. Fridge, washer, dryer, dishwasher. Same-day booking, 90-day parts warranty. Save $40 on first repair. Call 437-524-1053.
```

**Step 3: Fix Samsung brand page**

File: `C:/NikaApplianceRepair/brands/samsung-appliance-repair-toronto.html`

`<title>`:
```
Samsung Appliance Repair Toronto | Certified Tech | Same-Day
```
`<meta description>`:
```
Samsung-certified repair in Toronto. All models: fridge, washer, oven. Same-day service, 90-day warranty. $40 off first repair. Book now: 437-524-1053.
```

**Step 4: Fix Bosch brand page**

File: `C:/NikaApplianceRepair/brands/bosch-appliance-repair-toronto.html`

`<title>`:
```
Bosch Appliance Repair Toronto | Authorized Service | $40 Off
```
`<meta description>`:
```
Bosch-authorized repair Toronto. Dishwasher, fridge, oven, washer. Certified techs. Same-day available. 90-day warranty. Save $40 first repair. 437-524-1053.
```

**Step 5: Fix service pages**

`/services/oven-repair`:
- Title: `Oven Repair Toronto | Same-Day Service | All Brands | Nika`
- Desc: `Oven not heating? Toronto's top-rated oven repair service. Gas & electric. All brands. Same-day. 90-day warranty. Certified techs. Call 437-524-1053.`

`/services/washer-repair`:
- Title: `Washer Repair Toronto | Same-Day | All Brands | Nika`
- Desc: `Washing machine not spinning or leaking? Same-day washer repair in Toronto. All brands: LG, Samsung, Bosch. 90-day warranty. Save $40. Call 437-524-1053.`

**Step 6: Verify in browser**
Open each page → Ctrl+U → check title/meta updated correctly

**Commit:** `seo: fix title and meta for top 6 high-impression pages`

---

### Task 4: Add AggregateRating Schema to All Service Pages

**Why:** Star ratings in search results → CTR jumps 15-30%.

**Prerequisite:** Need real reviews. Add after collecting reviews from GBP/Homestars.

**Template to add to each service page** (after getting reviews):

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Dryer Repair Toronto",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "47",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

Files to modify: All 9 in `C:/NikaApplianceRepair/services/*.html`

**Commit:** `schema: add AggregateRating to all service pages`

---

## PHASE 2 — Service Page Domination (Week 2-4)

### Task 5: Create Service+Location Pages (Programmatic SEO)

**Why:** "dryer repair brampton" has volume but no dedicated page. Each combo = a ranking opportunity.

**Target combinations — 45 new pages:**

```
[service] repair [city] where:
- services: dryer, washer, refrigerator, oven, dishwasher (top 5)
- cities: toronto, mississauga, brampton, north-york, vaughan, scarborough,
         markham, richmond-hill, oakville, etobicoke (top 10)
```

**Example URL structure:**
```
/services/dryer-repair-toronto        (exists, optimize)
/services/dryer-repair-mississauga    (CREATE)
/services/dryer-repair-brampton       (CREATE)
/services/washer-repair-mississauga   (CREATE)
/services/refrigerator-repair-toronto (exists, optimize)
```

**Page template** (each page must have):
- Unique H1: `Dryer Repair in Mississauga — Same-Day Service`
- 300-500 words unique content mentioning city-specific neighborhoods
- LocalBusiness schema with city address area
- FAQPage schema with 3-4 city-specific questions
- Internal links to: main dryer-repair page, Mississauga location page
- CTA with phone number

**Priority order** (by GSC impressions):
1. dryer-repair-toronto (41 impressions, 0 clicks, pos 36 — needs urgently)
2. oven-repair-toronto (584 impressions, 0 clicks!)
3. washer-repair-mississauga
4. dishwasher-repair-toronto
5. refrigerator-repair-toronto

**Step 1: Check if dryer-repair-toronto page exists separately**
```bash
ls C:/NikaApplianceRepair/services/dryer*
```

**Step 2: Create template script for service+location pages**

File to create: `C:/NikaApplianceRepair/generate-service-location-pages.py`

**Step 3: Generate top priority pages first**

**Step 4: Add to sitemap**

**Commit:** `feat: add service+location combination pages for top 45 combos`

---

### Task 6: Fix Internal Linking — Blog → Service Pages

**Why:** Blog gets impressions but doesn't pass authority to service pages. Need bridges.

**Current state:** 111 blog posts, most NOT linking to service pages.

**Target internal links to add:**

```
refrigerator-compressor-noise-diagnosis → /services/refrigerator-repair
                                        → /brands/lg-appliance-repair-toronto
                                        → /brands/samsung-appliance-repair-toronto

washer-not-agitating → /services/washer-repair
dryer-not-heating → /services/dryer-repair
dishwasher-not-draining → /services/dishwasher-repair
oven-temperature-calibration → /services/oven-repair
```

**Step 1: Find posts missing service page links**
```bash
grep -rL "services/refrigerator-repair" C:/NikaApplianceRepair/blog/troubleshooting/*refrigerator*.html
grep -rL "services/dryer-repair" C:/NikaApplianceRepair/blog/troubleshooting/*dryer*.html
```

**Step 2: Add contextual CTA to each post**
Pattern: within content, after diagnosing a problem, add:
```html
<div class="repair-cta">
  <p>Need professional help? <a href="/services/dryer-repair">Our Toronto dryer repair technicians</a>
  can diagnose and fix this same-day. <a href="tel:4375241053">Call 437-524-1053</a>.</p>
</div>
```

**Step 3: Add "Related Services" section to blog posts**

**Commit:** `seo: add internal links from blog posts to service pages`

---

### Task 7: Service Pages Content Expansion

**Why:** Most service pages are thin. More depth = better E-E-A-T = better rankings.

**Target pages** (by impressions, worst performing):
- `/services/oven-repair` — 584 impressions, 0 clicks, pos 14.9
- `/services/refrigerator-repair` — 672 impressions, 0 clicks, pos 33

**Each service page needs:**
- 1,200-1,500 words minimum
- "Common Problems" section with 5-7 specific issues
- "Brands We Service" with links to brand pages
- "Service Areas" with links to location pages
- "Cost Guide" section (people search "dryer repair cost")
- "DIY vs Professional" section
- FAQ schema (already have, but expand to 6-8 questions)
- HowTo schema for 1 common fix

**Cost sections to add** (these rank for "repair cost" queries):
```
Dryer Repair Toronto: $150-$450
- Heating element: $150-$250
- Drum belt: $100-$200
- Control board: $250-$450
- Motor: $200-$350
```

**Commit:** `content: expand service pages to 1200+ words with cost guides`

---

## PHASE 3 — Domain Authority Building (Month 2)

### Task 8: Local Citations — 20 Essential Directories

**Why:** Citations = NAP (Name, Address, Phone) mentions. Google uses them to verify legitimacy.

**Priority directories:**

```
FREE (do immediately):
1. Google Business Profile — MOST IMPORTANT
2. Bing Places
3. Apple Maps Connect
4. Yelp Canada (yelp.ca)
5. HomeStars.com — #1 for home services in Canada
6. Houzz.com
7. BBB (Better Business Bureau)
8. YellowPages.ca
9. Canada411.ca
10. Canpages.ca
11. Cylex.ca
12. LocalBusiness.ca
13. Fyple.ca
14. Hotfrog.ca
15. Tupalo.com

PAID (worth it):
16. Angi.com (Canada)
17. Thumbtack.com
18. HomeAdvisor.com
```

**NAP format to use CONSISTENTLY everywhere:**
```
Name: Nika Appliance Repair
Address: [actual address - ask client]
Phone: (437) 524-1053
Website: https://nikaappliancerepair.com
Email: care@nikaappliancerepair.com
```

⚠️ **Note:** Found `care@niappliancerepair.ca` in code — verify which is correct email and fix all instances.

**Step 1: Create citations spreadsheet**

File to create: `docs/citations-tracker.md`
Track: directory name, URL, submitted date, live date, login info

**Step 2: Submit to all 18 directories**

**Step 3: Fix any existing inconsistent NAP**
```bash
grep -r "niappliancerepair.ca\|@nika\|437-747\|4377476" C:/NikaApplianceRepair/ --include="*.html" | head -20
```

**Commit:** `docs: add citations tracker with submission status`

---

### Task 9: Google Business Profile Optimization

**If GBP doesn't exist — CREATE IMMEDIATELY** (this is #1 local ranking factor).

**If GBP exists — optimize:**

1. **Posts:** Add weekly Google Post (offer, update, event)
2. **Photos:**
   - Add 10+ interior/work photos
   - Add technician photos
   - Label photos with keywords
3. **Services:** Add all 9 services with descriptions and prices
4. **Q&A:** Add 10 common Q&As yourself before customers ask
5. **Reviews:**
   - Create review request template SMS/email
   - Get minimum 25 reviews (target 50+)
   - Respond to every review within 24h

**Review request template:**
```
Hi [Name], thank you for choosing Nika Appliance Repair!
We'd really appreciate if you could leave us a quick review on Google:
[short.link/gsc-review]
Your feedback helps others find us! — Nika Team
```

---

### Task 10: Backlink Strategy

**Target: 50 quality backlinks in 3 months**

**Tier 1 — Local/Industry (easiest, most valuable):**
- HomeStars profile + reviews (DA 50+)
- Local Toronto blogs / news
- Appliance manufacturer sites (authorized dealer/service page)
- Toronto neighbourhood associations
- Property management companies (referral partnerships)

**Tier 2 — Content-based:**
- Guest posts on home improvement blogs
- Answer HARO (Help A Reporter Out) queries for home/appliance topics
- Create "Appliance Repair Cost Guide Toronto" → pitch to local news

**Tier 3 — Competitor analysis:**
```bash
# Use DataForSEO to find competitor backlinks
POST https://api.dataforseo.com/v3/backlinks/backlinks/live
{
  "target": "appliancerepair.ca",
  "limit": 50
}
# Then replicate their best links
```

---

## PHASE 4 — Content Strategy (Months 2-6)

### Task 11: Commercial-Intent Blog Posts (Priority Content)

**Why:** Current blog is mostly "how to fix" (informational). Need "should I hire" (commercial) content.

**Missing commercial keywords to target:**

```
High priority (high intent, good volume):
- "dryer repair cost toronto" — nobody searching "how to fix dryer" pays for repair
- "oven repair vs replace toronto"
- "how much does appliance repair cost toronto"
- "same day appliance repair toronto"
- "emergency appliance repair toronto"  (we rank pos 4.6 but 0 clicks!)
- "best appliance repair toronto"
- "appliance repair near me toronto"
- "refrigerator repair cost toronto"
- "washer repair cost toronto"

Brand-specific commercial:
- "lg refrigerator repair toronto cost"
- "samsung washer repair toronto"
- "bosch dishwasher repair cost toronto"
- "miele appliance repair toronto"
```

**Content calendar — 16 posts over 8 weeks:**

| Week | Post Title | Target Keyword | Intent |
|------|-----------|----------------|--------|
| 1 | Dryer Repair Cost Toronto: 2026 Price Guide | dryer repair cost toronto | Commercial |
| 1 | Emergency Appliance Repair Toronto: Same-Day Guide | emergency appliance repair toronto | Commercial |
| 2 | LG Refrigerator Repair Toronto: What to Expect | lg refrigerator repair toronto | Commercial |
| 2 | Samsung Washer Repair Toronto: Cost & Service | samsung washer repair toronto | Commercial |
| 3 | Bosch Dishwasher Repair Toronto: Certified Service | bosch dishwasher repair toronto | Commercial |
| 3 | Appliance Repair vs Replace: 2026 Toronto Guide | appliance repair vs replace toronto | Commercial |
| 4 | How Much Does Appliance Repair Cost in Toronto? | appliance repair cost toronto | Commercial |
| 4 | Miele Appliance Repair Toronto: Expert Service | miele appliance repair toronto | Commercial |
| 5 | Oven Not Heating Toronto: Repair or Replace? | oven repair toronto | Commercial |
| 5 | Washer Repair Cost Toronto: 2026 Price Guide | washer repair cost toronto | Commercial |
| 6 | Refrigerator Repair Toronto: When to Call a Pro | refrigerator repair toronto | Commercial |
| 6 | Same-Day Appliance Repair Toronto: How It Works | same day appliance repair toronto | Commercial |
| 7 | Dishwasher Repair Toronto: Cost & Common Issues | dishwasher repair toronto | Commercial |
| 7 | KitchenAid Appliance Repair Toronto | kitchenaid repair toronto | Commercial |
| 8 | Best Appliance Repair Toronto: What to Look For | best appliance repair toronto | Commercial |
| 8 | Freezer Repair Toronto: Diagnosis & Repair | freezer repair toronto | Commercial |

**Each post structure:**
1. H1 with main keyword
2. "Quick Answer" box (gets featured snippet)
3. Problem/symptom list (gets "People Also Ask")
4. Cost table (people love this, high CTR)
5. DIY check vs call professional
6. CTA to book service
7. FAQ schema (5+ questions)
8. Internal links to: service page, location page, related brands

---

### Task 12: Featured Snippet Optimization

**Why:** Featured snippets = position 0 = free massive CTR boost.

**Pages to optimize for featured snippets:**

Target "Quick Answer" boxes for these queries:
- "how much does dryer repair cost" → cost table
- "refrigerator compressor noise" → already ranking, add definition list
- "is it worth repairing an appliance" → direct answer paragraph
- "how long does appliance repair take" → numbered list

**Format for featured snippet:**

```html
<!-- Add "Quick Answer" box near top of content -->
<div class="quick-answer" itemscope itemtype="https://schema.org/FAQPage">
  <h2>Quick Answer</h2>
  <div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
    <p itemprop="name"><strong>How much does dryer repair cost in Toronto?</strong></p>
    <div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
      <p itemprop="text">Dryer repair in Toronto costs <strong>$150-$450</strong> depending on the part. Heating element: $150-250. Drum belt: $100-200. Motor: $200-350. Most repairs are completed same-day.</p>
    </div>
  </div>
</div>
```

**HowTo Schema for blog posts:**
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Diagnose Refrigerator Compressor Noise",
  "step": [
    {"@type": "HowToStep", "name": "Listen to the noise type", "text": "Clicking = relay. Humming = condenser. Grinding = compressor failure."},
    {"@type": "HowToStep", "name": "Check condenser coils", "text": "Unplug fridge, pull away from wall, check if coils are dusty."}
  ]
}
```

---

## PHASE 5 — AI Search / 2026 (Week 2+, Ongoing)

### Task 13: Create llms.txt (AI Crawler Optimization)

**Why:** AI Overviews, ChatGPT, Perplexity read llms.txt to understand your site. New in 2025-2026.

File to create: `C:/NikaApplianceRepair/llms.txt`

```markdown
# Nika Appliance Repair

> Professional appliance repair service in Toronto, Ontario, Canada.
> Same-day service, 90-day warranty, all major brands.

## About
Nika Appliance Repair serves the Greater Toronto Area with certified appliance repair technicians. We repair refrigerators, washers, dryers, dishwashers, ovens, stoves, and microwaves from all major brands.

## Services
- [Dryer Repair Toronto](https://nikaappliancerepair.com/services/dryer-repair)
- [Washer Repair Toronto](https://nikaappliancerepair.com/services/washer-repair)
- [Refrigerator Repair Toronto](https://nikaappliancerepair.com/services/refrigerator-repair)
- [Oven Repair Toronto](https://nikaappliancerepair.com/services/oven-repair)
- [Dishwasher Repair Toronto](https://nikaappliancerepair.com/services/dishwasher-repair)

## Service Areas
Toronto, Mississauga, Brampton, Vaughan, Markham, Richmond Hill, Oakville, North York, Scarborough

## Contact
Phone: (437) 524-1053
Email: care@nikaappliancerepair.com
Website: https://nikaappliancerepair.com

## Pricing
Service call/diagnosis: $89 (waived if repair done)
Most repairs: $150-$450
90-day parts and labour warranty
```

**Step 2: Allow AI crawlers in robots.txt**
```bash
# Check current robots.txt
curl https://nikaappliancerepair.com/robots.txt
```

File to modify: `C:/NikaApplianceRepair/robots.txt`

Ensure these are NOT blocked:
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GoogleBot
Allow: /
```

**Commit:** `feat: add llms.txt and allow AI crawlers`

---

### Task 14: Optimize for AI Overviews (Google GEO)

**Why:** Google AI Overviews show up for informational queries. Get cited = massive brand exposure.

**Pages most likely to get AI Overview citations:**
- Cost guides (structured data + direct answers)
- "Is it worth repairing" guides
- Brand-specific repair guides

**Optimization checklist per page:**
- [ ] Add "Quick Answer" box at top with direct answer
- [ ] Use structured headings (H2/H3) for each section
- [ ] Add statistics and specific numbers
- [ ] Include local context (Toronto-specific info)
- [ ] Add author bio with credentials (E-E-A-T)
- [ ] Include "Last Updated" date

**Author bio template to add to blog posts:**
```html
<div class="author-bio">
  <img src="/assets/images/technician.webp" alt="Nika technician">
  <div>
    <strong>Written by Nika Appliance Repair Team</strong>
    <p>Our team has 10+ years repairing appliances in Toronto.
    All technical content reviewed by certified technicians.</p>
  </div>
</div>
```

---

## PHASE 6 — Location Page Enhancement (Month 2-3)

### Task 15: Optimize Top Location Pages

**Current top location pages by impressions:**
- north-york: 1,571 impressions, 2 clicks, pos 36 → fix urgently
- vaughan: 1,261 impressions, 2 clicks, pos 26 → fix
- brampton: 840 impressions, 5 clicks, pos 35 → fix

**Each location page needs:**
- City-specific H1: `Appliance Repair in North York — Same-Day Service`
- Neighbourhood mentions (North York: Willowdale, Newtonbrook, Bathurst Manor)
- Local landmarks/references
- City-specific schema with proper `areaServed`
- Links to service pages WITH city context
- Local phone number if different
- "Areas we cover in [City]" with postal codes
- 800-1000 words

**North York example improvements:**

File: `C:/NikaApplianceRepair/locations/north-york.html`

Title change: `Appliance Repair North York | Same-Day | All Brands | Nika`
Description: `North York appliance repair — same-day service in Willowdale, Newtonbrook, Don Mills. All brands. 90-day warranty. Licensed techs. Call 437-524-1053.`

**Commit:** `seo: optimize top 5 location pages with city-specific content`

---

## Quick Wins Checklist (Do in First 48 Hours)

- [ ] Screenshot and share the 4 "not indexed" reasons from GSC
- [ ] Verify nappliancerepair.ca → 301 redirect to nikaappliancerepair.com
- [ ] Fix title on refrigerator-compressor-noise-diagnosis (6,091 impressions, 0.4% CTR)
- [ ] Fix title on LG, Samsung, Bosch brand pages
- [ ] Check robots.txt for accidental blocking
- [ ] Confirm Google Business Profile exists (or create)
- [ ] Submit to HomeStars.com (top Canadian home services directory)
- [ ] Create llms.txt file

---

## KPI Tracking (Check Monthly via GSC)

| KPI | Month 1 Target | Month 3 Target | Month 6 Target |
|-----|---------------|----------------|----------------|
| Total clicks/month | 100 | 500 | 2,000 |
| Avg position | 15 | 10 | 7 |
| Indexed pages | 200 | 260 | 299 |
| Service page clicks | 20 | 100 | 400 |
| CTR (overall) | 0.8% | 2% | 4% |
| GBP reviews | 10 | 30 | 75 |

---

## Questions Needing Answers

1. **Google Business Profile** — Does it exist? How many reviews?
2. **Two domains** — nikaappliancerepair.com vs nappliancerepair.ca — which is primary? Is .ca redirecting to .com?
3. **193 not indexed — 4 reasons** — Need screenshot from GSC → Pages → Not indexed
4. **Physical address** — Needed for Local Business schema and citations
5. **Budget for paid directories** — HomeStars Pro (~$50/month) vs free listing

---

## CSS Рефакторинг (после SEO спринта)

**Проблема:** 40+ CSS файлов в /css/ — накопленный технический долг
- design-system.css, style.css, styles.css, combined-fixes.css, centering-fixes.css, mobile-strict-fix.css, и ещё 35+
- Много визуальных багов из-за конфликтующих стилей
- Тяжёлая загрузка страниц (много HTTP запросов)

**Задача:** CSS аудит + консолидация
1. Аудит: найти все баги (мобильные, десктоп, выравнивание)
2. Консолидация: объединить всё в один main.css + отдельный critical.css
3. Удалить мусорные CSS файлы
4. Проверить Core Web Vitals после

**Приоритет:** После завершения SEO quick wins (service+location страницы, blog improvements)
