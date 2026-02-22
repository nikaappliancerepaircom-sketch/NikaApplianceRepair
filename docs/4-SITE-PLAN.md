# 4-Site Appliance Repair Network — Full Plan
**Created:** 2026-02-22
**Status:** ✅ PLAN COMPLETE — READY TO BUILD

---

## ✅ CURRENT STATUS (2026-02-22) — READY TO BUILD

### All Decisions Made ✅
- Domains confirmed: nappliancerepair.com + appliancerepairneary.com + fixlifyservices.com
- Designs: nappliancerepair.com→V9, appliancerepairneary.com→V2, fixlifyservices.com→V8
- 130-150 pages per site (expanded with KD 0-40 keywords)
- KD threshold: 0-40 (low + medium competition, new domains)
- Milton REMOVED from all location lists
- Flat URL structure: /fridge-repair-ajax (not /locations/ajax/fridge)
- Template system: Golden Template per site + Node.js generator
- Internal linking: locations ↔ services ↔ brands matrix (same as nikaappliancerepair.com)
- Sites are INDEPENDENT — no aggressive cross-linking (avoid Google penalty)
- Only 1 natural footer link from each new site to nikaappliancerepair.com
- Fixlify booking iframe on every page
- Shared header.html + footer.html via loader.js per site
- Shared config.js per site (phone, rating, warranty, booking URL)
- BMAD v4 parameters checklist applies to ALL pages on all 3 sites
- PageSpeed target: 90+ mobile AND desktop
- Toronto location code: 1006984 (NOT Canada 2124) for keyword targeting
- AI SEO (GEO) is MOST IMPORTANT — llms.txt, FAQ schema, direct answers, AI crawlers

### BMAD v4 2026 Updates (vs v3.2 2025)
- **INP (Interaction to Next Paint)**: New Core Web Vitals metric. Target < 200ms. Use event delegation, avoid heavy JS on click handlers.
- **llms.txt**: New mandatory parameter. Every site must have /llms.txt with business facts, services, coverage.
- **AI crawlers in robots.txt**: Must explicitly Allow all AI bots (GPTBot, Claude-Web, PerplexityBot, Google-Extended, anthropic-ai, cohere-ai, you-bot, diffbot, bytespider, imagesiftbot, CCBot)
- **PageSpeed target raised**: 90+ both mobile AND desktop (was just mobile in v3.2)
- **AI Answer Box**: New required element on every page — 60-80 word direct answer at top of main content
- **E-E-A-T author block**: Required on all service/blog pages with technician name + credentials
- **Total parameters**: ~300+ (was 293)

### Data Findings ℹ️
- **Toronto city-level (1006984) Google Ads data = suppressed** — Google doesn't report volumes below threshold for city-level. Only 4 keywords returned data: "appliance repair near me" ($2.53 CPC, LOW competition index 32 — confirms low advertiser saturation), "appliance repair brampton", "appliance repair newmarket", "is it worth repairing washing machine" — all showing ~10/mo at city level.
- **Use Ontario-level (1009921) for volume estimates** — GTA dominates Ontario appliance searches so Ontario volume ≈ reliable proxy for GTA
- **KD is more important than volume for new domains** — "fridge repair ajax" KD=0 means we rank fast even if volume is low. Local intent = high conversion regardless.
- **Strategy confirmed**: Build all city+service pages — real people search for them, KD=0, competitors haven't built these pages yet.

## 🚀 EXECUTION STATUS (2026-02-22)

### ✅ DONE
- [x] Golden templates built for all 3 sites (index.html + service-template.html)
- [x] tokens.css added to all 3 sites
- [x] config.js + includes/ + data/ + llms.txt + robots.txt — all 3 sites
- [x] Fixlify iframe background fix (white bg on dark site)
- [x] Dev servers running: localhost:4001 / :4002 / :4003
- [x] Generators completed: 85 + 105 + 94 = 284 programmatic pages ✅
- [x] FAQPage schema added to all fixlifyservices problem pages ✅
- [x] All 295 pages pass quality check (0 issues) ✅
- [x] font-display:swap, lazy images, defer scripts — all 295 pages ✅
- [x] meta robots + og:title + og:description + twitter:card — all 295 pages ✅
- [x] robots.txt expanded: +7 AI crawlers (AmazonBot, Applebot, YouBot, DuckAssistBot, FacebookBot, Diffbot) ✅
- [x] llms.txt enriched with "Quick Answer for AI" section ✅
- [x] about.html + contact.html + pricing.html created for all 3 sites ✅
- [x] sitemap.xml generated for all 3 sites ✅
- [x] Blog posts 10x per site — in progress (agents running) ✅

### ⏳ IN PROGRESS
- [ ] Blog posts 10 per site (3 agents writing 30 total blog posts)
- [ ] appliancerepairneary about/contact/pricing agent (a6097f6)

### 📋 NEXT STEPS (in order, do NOT skip)

**STEP 1 — After generators finish:**
- Verify 0 unreplaced `{{VARIABLES}}` in generated pages: `grep -r "{{" C:/nappliancerepair/*.html | wc -l` (must = 0)
- Spot-check 3 pages per site in browser (localhost)
- Fix any rendering issues

**STEP 2 — Manual pages (write these by hand, NOT generated):**
Each site needs:
- `about.html` — team story, 6+ years, 5200+ repairs, licensed
- `contact.html` — phone, booking, hours, service area map
- `pricing.html` — repair cost table by appliance
- `blog/index.html` — blog listing page
- Site 1 extra: brand guide pages (lg-warranty-canada.html, frigidaire-vs-whirlpool.html etc.)
- Site 3 extra: `same-day.html`, `emergency.html`, `book-online.html`

**STEP 3 — Blog posts (10 per site, use subagent):**
- Site 1: brand comparisons, warranty guides, repair tips
- Site 2: "near me" local guides, GTA city profiles
- Site 3: booking guides, cost breakdowns, repair vs replace

**STEP 4 — sitemap.xml for each site:**
Generate from all .html files in root folder:
```javascript
// sitemap-generator.js
const files = fs.readdirSync('./').filter(f => f.endsWith('.html') && !f.includes('template'));
const urls = files.map(f => `<url><loc>https://{domain}/${f}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>`);
```

**STEP 5 — BMAD Critical Parameters Check (ALL pages must pass 100%):**
Critical parameters to verify on EVERY page:
- [ ] `<title>` present, unique, 50-60 chars, contains keyword + phone or brand
- [ ] `<meta name="description">` present, 140-160 chars
- [ ] `<link rel="canonical">` present and correct
- [ ] One `<h1>` per page (not zero, not two)
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] NO `<meta name="robots" content="noindex">` anywhere
- [ ] LocalBusiness JSON-LD with aggregateRating
- [ ] FAQPage JSON-LD with min 5 questions
- [ ] Phone number as `<a href="tel:+14375241053">`
- [ ] Fixlify iframe present with exact URL
- [ ] All images have `alt` attribute
- [ ] `font-display: swap` on Google Fonts
- [ ] `loading="lazy"` on below-fold images
- [ ] `defer` on scripts
- [ ] Answer box (60-80 word direct answer) present
- [ ] llms.txt exists at site root
- [ ] robots.txt exists, allows all AI bots
- [ ] Breadcrumb nav with schema markup
- [ ] Internal links: related services + related cities

Run BMAD check script:
```bash
# Quick critical params check:
node bmad-check.js C:/nappliancerepair/
node bmad-check.js C:/appliancerepairneary/
node bmad-check.js C:/fixlifyservices/
```

**STEP 6 — PageSpeed check (BEFORE deploy):**
Use browser Lighthouse (DevTools → Lighthouse tab):
- Test each index.html via localhost:4001/4002/4003
- Target: 90+ mobile AND desktop
- Common fixes if <90:
  - Unused CSS: move non-critical styles to async load
  - Render-blocking resources: ensure all scripts have defer
  - Image sizing: add explicit width/height to all images
  - CLS: ensure iframes have fixed height

**STEP 7 — GitHub repos (create 3 new repos):**
```bash
cd C:/nappliancerepair && git init && git add . && git commit -m "Initial: N Appliance Repair site"
gh repo create nappliancerepair --public --source=. --push

cd C:/appliancerepairneary && git init && git add . && git commit -m "Initial: Appliance Repair Near Me site"
gh repo create appliancerepairneary --public --source=. --push

cd C:/fixlifyservices && git init && git add . && git commit -m "Initial: Fixlify Services site"
gh repo create fixlifyservices --public --source=. --push
```

**STEP 8 — Vercel deploy:**
```bash
cd C:/nappliancerepair && npx vercel --prod
cd C:/appliancerepairneary && npx vercel --prod
cd C:/fixlifyservices && npx vercel --prod
```
Then in Vercel dashboard: add custom domain for each site.

**STEP 9 — DNS at registrar:**
For each domain, add:
```
Type: CNAME
Name: @  (or www)
Value: cname.vercel-dns.com
```

**STEP 10 — Google Search Console:**
- Add all 3 properties
- Submit sitemaps: https://{domain}/sitemap.xml
- Verify via HTML file or DNS TXT record

**STEP 11 — Google Indexing API (fast indexing):**
Use existing indexing script from nikaappliancerepair.com.
Submit top 20 priority URLs per site:
- Site 1: index, 6 service pages, 9 brand pages, top 5 city pages
- Site 2: index, 6 near-me pages, top 10 service×city (brampton, mississauga, markham)
- Site 3: index, same-day, emergency, fridge-not-cooling, appliance-repair-mississauga, cost guides

---

## FILE INVENTORY (current state)

### C:/nappliancerepair/ ✅ templates done
- index.html, service-template.html, config.js, tokens.css
- includes/ (header, footer, loaders)
- data/ (cities, services, brands)
- llms.txt, robots.txt
- generator.js + ~74 generated pages (in progress)
- MISSING: about.html, contact.html, pricing.html, blog/, sitemap.xml

### C:/appliancerepairneary/ ✅ templates done
- index.html, service-template.html, config.js, tokens.css
- includes/ + data/
- llms.txt, robots.txt
- generator.js + ~104 generated pages (in progress)
- MISSING: about.html, contact.html, pricing.html, blog/, sitemap.xml

### C:/fixlifyservices/ ✅ templates done (iframe bg fixed)
- index.html, service-template.html, config.js, tokens.css
- includes/ + data/
- llms.txt, robots.txt
- generator.js + ~94 generated pages (in progress)
- MISSING: about.html, contact.html, same-day.html, emergency.html, book-online.html, blog/, sitemap.xml

---

---

## Network Overview

| # | Domain | Design | SEO Strategy | Priority |
|---|--------|--------|--------------|----------|
| 0 | nikaappliancerepair.com | V9 upgrade | Brand Authority | Upgrade |
| 1 | nappliancerepair.com | V9 Swiss Minimal | Main GTA Brand | HIGH |
| 2 | appliancerepairneary.com | V2 White Pro | "Near Me" Programmatic | HIGH |
| 3 | fixlifyservices.com | V8 Cinematic Dark | Conversion/Booking | HIGH |

All 4 sites: same business (Nika Appliance Repair), different keyword angles, all pointing to Fixlify booking.

---

## Site 0 — nikaappliancerepair.com (UPGRADE)

**What changes:**
- Replace landing.html with V9 Swiss Minimal design
- PageSpeed audit → target 95+
- Add missing AI SEO signals (FAQ schema, direct answers, llms.txt update)
- No structural changes to other pages

**Effort:** 1 agent, ~2 hours

---

## Site 1 — nappliancerepair.com

**Theme:** "N Appliance Repair" — professional GTA-wide brand
**Design:** V9 Swiss Minimal (clean, fast, trustworthy)
**Target keywords:**
- "appliance repair Toronto"
- "appliance repair GTA"
- "appliance repair service Ontario"
- "fridge repair Toronto", "washer repair Toronto" (etc.)

### Site Structure
```
/                          ← V9 landing (main CTA: book online)
/services/
  fridge-repair.html
  washer-repair.html
  dryer-repair.html
  dishwasher-repair.html
  oven-repair.html
  stove-repair.html
/locations/
  toronto.html
  scarborough.html
  north-york.html
  etobicoke.html
  mississauga.html
  brampton.html
  vaughan.html
  richmond-hill.html
  markham.html
  oakville.html
/about.html
/contact.html
/blog/
  index.html
  how-much-does-appliance-repair-cost-toronto.html
  signs-your-fridge-needs-repair.html
  diy-vs-professional-appliance-repair.html
/llms.txt
/robots.txt
/sitemap.xml
```

### Page count: ~25 pages

### Schema per page:
- LocalBusiness + AggregateRating (all pages)
- Service (service pages)
- FAQPage (12-15 Q&A, all pages)
- HowTo (blog posts)
- BreadcrumbList (all pages)

### AI SEO signals:
- Direct answer box at top of each page (60-80 words)
- Conversational H2/H3 headings ("How much does fridge repair cost in Toronto?")
- E-E-A-T: technician credentials, 5200+ repairs stat, 90-day warranty
- llms.txt with brand facts, services, coverage area

---

## Site 2 — appliancerepairneary.com

**Theme:** "Appliance Repair Near Me" — programmatic local SEO
**Design:** V2 White Professional (clean, trustworthy, easy to scan)
**Target keywords:**
- "appliance repair near me [city]"
- "[appliance] repair near me"
- "[appliance] repair [city]"
- "best appliance repair [city]"

### Programmatic Matrix: 6 × 15 = 90 pages

**Appliances (6):**
1. Refrigerator / Fridge
2. Washer / Washing Machine
3. Dryer
4. Dishwasher
5. Oven
6. Stove / Range

**GTA Locations (15):**
1. Toronto
2. Scarborough
3. North York
4. Etobicoke
5. Mississauga
6. Brampton
7. Vaughan
8. Richmond Hill
9. Markham
10. Oakville
11. Burlington
12. Pickering
13. Ajax
14. Whitby
15. Oshawa
❌ Milton — REMOVED (no service)

### URL pattern: `/[appliance]-repair-[city].html`
Examples:
- `/fridge-repair-toronto.html`
- `/washer-repair-mississauga.html`
- `/dryer-repair-brampton.html`

### Site Structure
```
/                          ← V2 landing ("Find appliance repair near you")
/fridge-repair-toronto.html
/fridge-repair-scarborough.html
... (6 × 15 = 90 pages)
/about.html
/contact.html
/llms.txt
/robots.txt
/sitemap.xml               ← All 90 pages
```

### Page count: ~95 pages (90 programmatic + 5 core)

### Each programmatic page includes:
- H1: "[Appliance] Repair in [City] — Same-Day Service"
- Direct answer: "Need [appliance] repair in [city]? We service all of [city] and surrounding areas..."
- Price range table for that appliance
- Common problems for that appliance (5-7 items)
- Why choose us section
- FAQ (8-10 Q&A specific to appliance+city)
- Fixlify booking iframe
- LocalBusiness schema with city
- Service schema

### Generator approach:
- Node.js script using template + data arrays
- Gemini API for unique intro paragraph per page (avoid duplicate content)
- Run once to generate all 90 pages
- Part of fixlify-agents as `programmatic-site-agent.ts`

---

## Site 3 — fixlifyservices.com

**Theme:** "Book Appliance Repair Online — Fast" — conversion machine
**Design:** V8 Cinematic Dark (dramatic, urgent, memorable)
**Target keywords:**
- "book appliance repair Toronto"
- "same-day appliance repair"
- "online appliance repair booking GTA"
- "appliance repair service Toronto"
- "24 hour appliance repair Toronto"

### Site Structure
```
/                          ← V8 landing (Fixlify booking front and center)
/same-day.html
/emergency.html
/services/
  refrigerator.html
  washing-machine.html
  dryer.html
  dishwasher.html
  oven.html
/locations/
  toronto.html
  gta.html
  mississauga.html
  brampton.html
  scarborough.html
/pricing.html
/about.html
/llms.txt
/robots.txt
/sitemap.xml
```

### Page count: ~18 pages

### Unique features vs other sites:
- Fixlify booking iframe above the fold (primary CTA)
- Price transparency page (repair costs by appliance)
- "Emergency" and "Same-Day" dedicated pages
- Urgency messaging throughout ("Available Today", "Book in 2 Minutes")
- Dark dramatic design creates urgency feeling

### Schema per page:
- LocalBusiness + AggregateRating
- Service with pricing (priceRange)
- FAQPage
- EmergencyService type
- Offer (discounts/promotions)

---

## REAL KEYWORD DATA (DataForSEO, Feb 2026)

### STRATEGY: Why low volume is fine
- Low volume × KD=0 × 130 pages = big combined traffic
- CPC = proxy for commercial intent (washing machine repair free estimate = $13.37 CPC → people who search this WANT to book)
- Problem pages ("dryer not heating" KD=0, 590/mo) = homeowner's first search before calling → capture them
- AI Search doesn't care about volume — cares about content quality
- Launch ALL pages day 1 — not gradually
- Featured Snippets possible for new domains on FAQ/cost/problem pages

### Site 1 — nappliancerepair.com keyword targets

| Keyword | Vol/mo | KD | Priority |
|---------|--------|----|----------|
| washer repair markham | 390 | 0 | 🔥 |
| lg canada parts | 720 | 17 | 🔥 |
| dryer parts canada | 260 | 1 | 🔥 |
| frigidaire vs whirlpool | 210 | 0 | 🔥 |
| lg repair service | 110 | 4 | 🔥 |
| lg warranty check | 140 | 0 | 🔥 |
| ge appliances warranty canada | 70 | 0 | 🔥 |
| kenmore washer canada | 50 | 2 | 🔥 |
| samsung fridge repair toronto | <10 | 19 | MEDIUM |
| bosch dishwasher repair toronto | <10 | 0 | EASY |
| appliance repair north york | <10 | 0 | EASY |
| appliance repair etobicoke | <10 | 0 | EASY |
| appliance repair scarborough | <10 | 0 | EASY |

**Strategy:** Brand authority — Samsung/LG/Whirlpool/GE/Bosch specific repair pages + brand comparisons + GTA neighborhoods

### Site 2 — appliancerepairneary.com keyword targets

| Keyword | Vol/mo | KD | Priority |
|---------|--------|----|----------|
| washer dryer repair near me | 2,900 | 1 | 🔥🔥🔥 |
| dishwasher repair service near me | 1,600 | 3 | 🔥🔥🔥 |
| stove repair near me | 1,000 | 5 | 🔥🔥 |
| appliance repair brampton | 880 | 0 | 🔥🔥 |
| appliance repair service near me | 480 | 4 | 🔥🔥 |
| lg fridge repair near me | 320 | 0 | 🔥🔥 |
| appliance repair shop near me | 320 | 0 | 🔥 |
| bosch dishwasher repair near me | 170 | 0 | 🔥 |
| fridge repair ajax | N/A | 0 | EASY WIN |
| washer repair whitby | N/A | 0 | EASY WIN |
| dryer repair oshawa | N/A | 0 | EASY WIN |
| dryer repair burlington | N/A | 0 | EASY WIN |

**Strategy:** "Near me" + small GTA cities — 6 × 14 matrix, all KD=0

### Site 3 — fixlifyservices.com keyword targets

| Keyword | Vol/mo | KD | Priority |
|---------|--------|----|----------|
| appliance repair mississauga | 1,900 | 4 | 🔥🔥🔥 |
| appliance repair brampton | 880 | 0 | 🔥🔥🔥 |
| appliance repair etobicoke | 720 | 0 | 🔥🔥 |
| same day appliance repair | 480 | 0 | 🔥🔥 |
| appliance repair north york | 480 | 0 | 🔥🔥 |
| appliance repair scarborough | 480 | 0 | 🔥🔥 |
| lg appliance repair | 590 | 0 | 🔥🔥 |
| samsung appliance repair | 480 | 20 | MEDIUM |
| washer machine repair cost | 140 | 0 | 🔥 |
| dishwasher repair cost | 110 | 0 | 🔥 |
| dryer repair cost | 110 | 0 | 🔥 |

**Strategy:** Booking + same-day + cost guides + GTA neighborhoods

---

## 100-PAGE STRUCTURE PER SITE

### Site 1: nappliancerepair.com — 135 pages
```
Core pages (5):            index, about, contact, pricing, blog-index
Service pages (6):         fridge, washer, dryer, dishwasher, oven, stove
Brand pages (9):           Samsung, LG, Whirlpool, GE, Bosch, Frigidaire, Kenmore, Maytag, KitchenAid
Brand×Appliance (30):      LG/Samsung/Whirlpool/GE/Bosch × 6 appliances
                           e.g. lg-fridge-repair, samsung-washer-repair, bosch-dishwasher-repair
Location pages (14):       All 14 GTA cities (no Milton)
Blog posts (30):           Brand comparisons, warranty guides, cost guides, repair tips
Location+Appliance (20):   washer-repair-markham, washer-repair-scarborough, washer-repair-north-york,
                           washer-repair-etobicoke, washer-repair-brampton, washer-repair-vaughan,
                           fridge-repair-mississauga, fridge-repair-scarborough, fridge-repair-north-york,
                           fridge-repair-vaughan, dryer-repair-toronto, dryer-repair-mississauga,
                           dryer-repair-brampton, dryer-repair-markham, dishwasher-repair-toronto,
                           dishwasher-repair-mississauga, oven-repair-toronto, oven-repair-mississauga,
                           stove-repair-toronto, stove-repair-scarborough
Brand guides (6):          lg-appliance-warranty-canada, samsung-warranty-canada,
                           whirlpool-parts-canada, ge-warranty-canada, bosch-parts-canada, frigidaire-vs-whirlpool
Brand×City (5):            lg-repair-toronto, samsung-repair-toronto, lg-repair-mississauga,
                           samsung-repair-mississauga, bosch-repair-toronto
─────────────────────────────────────────────
TOTAL: 5+6+9+30+14+30+20+6+5 = 125 pages + blog expandable to 135

KEY URLs (examples):
/lg-fridge-repair.html              ← KD=0, brand authority
/samsung-washer-repair.html         ← KD=0, brand authority
/bosch-dishwasher-repair.html       ← KD=0, local monopoly
/washer-repair-markham.html         ← KD=0, 390/mo Ontario
/frigidaire-vs-whirlpool.html       ← KD=0, 210/mo, featured snippet target
/lg-warranty-canada.html            ← KD=0, 140/mo, info intent
```

### Site 2: appliancerepairneary.com — 129 pages
```
Core pages (5):       index, about, contact, pricing, blog-index
"Near me" pages (6):  fridge/washer/dryer/dishwasher/oven/stove + near me
Brand near me (9):    LG/Samsung/Bosch/Whirlpool/GE/Frigidaire/KitchenAid/Maytag/Kenmore + near me
App×City matrix (84): 6 appliances × 14 GTA cities (all KD=0)
                      e.g. fridge-repair-ajax, washer-repair-whitby, dryer-repair-oshawa
Problem near me (8):  dryer-not-heating-near-me, fridge-not-cooling-near-me,
                      washer-not-draining-near-me, dishwasher-not-draining-near-me,
                      oven-not-heating-near-me, washer-making-noise-near-me,
                      fridge-leaking-near-me, freezer-not-working-near-me
Service combo (4):    washer-dryer-repair-near-me, kitchen-appliance-repair-near-me,
                      all-appliance-repair-near-me, home-appliance-repair-near-me
Intent pages (3):     best-appliance-repair-near-me, top-rated-near-me, affordable-near-me
Blog (10):            Local guides, near me tips, city profiles
─────────────────────────────────────────────
TOTAL: 5+6+9+84+8+4+3+10 = 129 pages

KEY URLs (examples):
/washer-dryer-repair-near-me.html   ← KD=1, 2,900/mo — #1 priority
/dishwasher-repair-near-me.html     ← KD=3, 1,600/mo
/fridge-repair-ajax.html            ← KD=0, small city monopoly
/washer-repair-whitby.html          ← KD=0, small city monopoly
/dryer-not-heating-near-me.html     ← KD=0, problem intent, converts well
/lg-fridge-repair-near-me.html      ← KD=0, 320/mo brand near me
```

### Site 3: fixlifyservices.com — 135 pages
```
Core pages (5):           index, about, contact, book-online, blog-index
Service pages (6):        fridge, washer, dryer, dishwasher, oven, stove
Emergency pages (3):      same-day, emergency, asap-repair
Cost guides (10):         fridge-repair-cost, washer-repair-cost, dryer-repair-cost,
                          dishwasher-repair-cost, oven-repair-cost, stove-repair-cost,
                          appliance-repair-cost-toronto, is-it-worth-repairing-appliance,
                          washer-machine-repair-cost, average-appliance-repair-cost
Problem diagnosis (10):   fridge-not-cooling, fridge-not-cooling-toronto,
                          washer-not-draining, washer-not-spinning,
                          dryer-not-heating, dryer-not-spinning,
                          dishwasher-not-draining, oven-not-heating,
                          stove-burner-not-working, fridge-making-noise
Brand pages (6):          LG, Samsung, Whirlpool, GE, Bosch, Frigidaire
Location pages (14):      All 14 GTA cities
Service×Location (60):    6 appliances × 10 top cities
                          e.g. fridge-repair-mississauga, washer-repair-brampton
Emergency×City (8):       emergency-fridge-repair-toronto, emergency-fridge-repair-mississauga,
                          emergency-washer-repair-toronto, emergency-washer-repair-mississauga,
                          same-day-appliance-repair-brampton, same-day-appliance-repair-markham,
                          same-day-appliance-repair-scarborough, same-day-appliance-repair-north-york
Blog (10):                Booking guides, cost tips, same-day guides, repair vs replace
Bonus pages (3):          warranty-repairs, brands-we-repair, service-area-map
─────────────────────────────────────────────
TOTAL: 5+6+3+10+10+6+14+60+8+10+3 = 135 pages

KEY URLs (examples):
/appliance-repair-mississauga.html  ← KD=4, 1,900/mo — #1 priority
/same-day-appliance-repair.html     ← KD=0, 480/mo booking intent
/fridge-not-cooling.html            ← KD=23, 1,600/mo problem diagnosis
/fridge-repair-cost.html            ← KD=0, featured snippet target
/washer-not-draining.html           ← KD=7, 880/mo problem intent
/emergency-fridge-repair-toronto.html ← KD=0, urgent buyer
```

---

## Technical Standards (ALL 4 SITES)

### PageSpeed 90+ Requirements
```html
<!-- Critical CSS inline in <head> (first 200 lines) -->
<style>/* critical above-fold CSS here */</style>

<!-- Fonts: preconnect + font-display: swap -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<style>@font-face { font-display: swap; }</style>

<!-- Images: WebP + lazy + explicit dimensions -->
<img src="image.webp" width="800" height="600" loading="lazy" alt="...">

<!-- JS: async/defer only, no render-blocking -->
<script src="app.js" defer></script>

<!-- No external CSS in <head> except fonts -->
```

### Mobile Standards
- Viewport: `width=device-width, initial-scale=1`
- Test breakpoints: 320px, 375px, 390px, 414px, 768px, 1024px
- Font size: minimum 16px body text
- Touch targets: minimum 48×48px
- No horizontal scroll at any width
- CTA buttons full-width on mobile

### AI SEO / GEO (Most Important)
```
1. llms.txt on every site:
   - Business name, phone, address
   - Services offered
   - Coverage area (all 15 GTA cities)
   - Booking URL (Fixlify)
   - Key facts (5200+ repairs, 90-day warranty, licensed)

2. robots.txt — allow all AI crawlers:
   User-agent: GPTBot
   Allow: /
   User-agent: Claude-Web
   Allow: /
   User-agent: PerplexityBot
   Allow: /
   User-agent: Google-Extended
   Allow: /
   (+ all other AI bots)

3. Direct answer boxes (every page):
   <div class="answer-box">
     [Appliance] repair in [City]: We offer same-day service across GTA.
     Cost typically $150-$400. Call (437) 524-1053 or book online.
     Licensed technicians, 90-day warranty.
   </div>

4. FAQ Schema (12-15 per page):
   - Conversational questions AI systems get asked
   - "How much does fridge repair cost in Toronto?"
   - "Is it worth repairing a 10-year-old washing machine?"
   - "What brands do you repair?"
   - "Do you offer same-day service in Mississauga?"

5. E-E-A-T signals:
   - Author: "Nika Appliance Repair Team — Licensed Technicians"
   - Experience: "5,200+ appliances repaired in GTA since 2018"
   - Authority: "Licensed & insured, member of Ontario trades association"
   - Trust: "4.9★ rating from 1,200+ verified reviews"
```

### Schema Markup Stack
```json
// Every page:
LocalBusiness + AggregateRating

// Service pages:
Service + Offer + FAQPage

// Blog/guides:
Article + FAQPage + HowTo + BreadcrumbList

// Home page:
WebSite + LocalBusiness + FAQPage + Review
```

### Clean Code Standards
- Valid HTML5 (W3C validator pass)
- Semantic tags: header, main, section, article, nav, footer, aside
- No inline styles (except critical CSS)
- No deprecated tags
- ARIA labels on all interactive elements
- Alt text on all images (descriptive + keyword)
- Proper heading hierarchy (one H1 per page)

---

## fixlify-agents Integration

### New agents to add: `C:/fixlify-agents/src/agents/`

**1. `programmatic-site-agent.ts`**
- Generates all 90 pages for appliancerepairneary.com
- Uses template HTML + data arrays (appliances × cities)
- Calls Gemini for unique 100-word intro per page
- Writes HTML files to output directory
- Run: `npm run agent -- programmatic-site`

**2. `appliance-seo-agent.ts`**
- Adapted from existing `seo-agent.ts`
- Keywords: appliance repair Toronto/GTA specific
- BMAD format (already in BMAD-AI-STRATEGY.md)
- Generates blog posts for all 4 sites
- Saves to appropriate site's /blog/ directory

**3. Update `soul.yaml`:**
```yaml
# Add Nika Appliance Repair context:
business:
  name: "Nika Appliance Repair"
  phone: "(437) 524-1053"
  area: "Toronto & GTA"
  reviews: "4.9★ from 5,200+ repairs"
  warranty: "90-day parts & labor"
  booking: "https://hub.fixlify.app/book/nicks-appliance-repair-b8c8ce"
```

---

## TEMPLATE SYSTEM (confirmed approach)

### Per-site file structure:
```
/config.js              ← shared business data (phone, rating, warranty, booking URL, cities, services)
/header.html            ← shared header (loaded via header-loader.js)
/footer.html            ← shared footer (ALL internal links: locations, services, brands)
/includes/
  header-loader.js
  footer-loader.js
/template.html          ← Golden Template (tested to 293 BMAD params before copy)
/generator.js           ← Node.js script: reads config.js → generates all pages
/data/
  cities.js             ← 14 GTA cities list (NO Milton)
  services.js           ← 6 appliances list
  brands.js             ← 9 brands list
  keywords.js           ← per-page keyword targets
```

### Generator logic:
```javascript
// Creates 84 service×city pages automatically:
for (city of cities) {
  for (service of services) {
    generatePage(`/${service}-repair-${city}`, template, {city, service, keywords})
  }
}
// Uses Gemini API for unique 150-word intro per page (avoids duplicate content penalty)
```

### Internal linking matrix (per page):
- Location page → links to: all 6 services on-page + 3 nearby cities + top 3 brands
- Service page → links to: all 14 location pages + 5 brands + 3 blog posts
- Brand page → links to: 6 services + top 5 locations + 2 blog posts
- Blog post → links to: 2-3 services + 1-2 locations + related post
- Footer → links to: ALL locations + ALL services + ALL brands (sitemap-style)
- Home → hero links to top 5 cities + 6 services + booking

### Fast indexing (Day 1):
1. Submit sitemap.xml to GSC immediately after deploy
2. Google Indexing API call for top 20 priority pages
3. Footer contains links to ALL pages → Google crawls everything in 1 visit
4. llms.txt at root (AI crawlers indexed from day 1)

---

## BUSINESS DATA (same across all 3 sites)
```javascript
// config.js (copy to each site, update domain)
const BUSINESS = {
  name: "Nika Appliance Repair",
  phone: "(437) 524-1053",
  tel: "tel:+14375241053",
  booking: "https://hub.fixlify.app/book/nicks-appliance-repair-b8c8ce",
  rating: "4.9",
  reviews: "5,200+",
  warranty: "90-day",
  experience: "6+ years",
  hours: "Mon-Sat 8am-8pm, Sun 9am-6pm",
  services: ["Refrigerator","Washer","Dryer","Dishwasher","Oven","Stove"],
  cities: ["Toronto","Scarborough","North York","Etobicoke","Mississauga",
           "Brampton","Vaughan","Richmond Hill","Markham","Oakville",
           "Burlington","Pickering","Ajax","Whitby","Oshawa"],  // NO Milton
  brands: ["Samsung","LG","Whirlpool","GE","Bosch","Frigidaire","Kenmore","Maytag","KitchenAid"]
}
```

---

## DESIGN SYSTEM PER SITE

### Site 1: nappliancerepair.com → V9 Swiss Minimal
- Font: Instrument Sans
- Colors: #2563EB (blue), #111 (dark), white
- Tone: Professional, expert, authoritative
- Hero: "GTA Appliance Repair — All Brands, All Models"
- Unique angle: brand expertise (Samsung, LG, Whirlpool specialists)

### Site 2: appliancerepairneary.com → V2 White Professional
- Font: DM Sans + Rubik
- Colors: White bg, #1976D2 blue, clean
- Tone: Local, convenient, "we're nearby"
- Hero: "Appliance Repair Near You — Toronto & GTA"
- Unique angle: hyper-local "near me" + every GTA city covered

### Site 3: fixlifyservices.com → V8 Cinematic Dark
- Font: Outfit + Plus Jakarta
- Colors: Dark bg, accent color, glassmorphism
- Tone: Urgent, fast, book-now
- Hero: "Book Appliance Repair Online — Available Today"
- Unique angle: same-day booking, online-first, cost transparency

---

## Execution Plan — Agent Assignments

### Parallel execution (3 main build agents + 1 support):

**Agent 1: nappliancerepair.com** → 135 pages, V9 Swiss Minimal
- Step 1: Create Golden Template (index.html) with V9 design
- Step 2: Verify BMAD v4 compliance on template (300+ params)
- Step 3: Build config.js + header.html + footer.html + loader scripts
- Step 4: Generate all service pages (6) + brand pages (9) + brand×appliance (30)
- Step 5: Generate all location pages (14) + location+appliance (20)
- Step 6: Build brand guides (6) + brand×city (5)
- Step 7: Build blog posts (30) — use Gemini for unique content
- Step 8: Build core pages (about, contact, pricing)
- Step 9: llms.txt + robots.txt + sitemap.xml
- Step 10: Final PageSpeed check (must be 90+)

**Agent 2: appliancerepairneary.com** → 129 pages, V2 White Professional
- Step 1: Create Golden Template with V2 design
- Step 2: BMAD v4 compliance check
- Step 3: Build config.js + shared includes
- Step 4: Build generator.js (Node.js) for 84 service×city pages
- Step 5: Run generator → 84 pages with unique Gemini intros
- Step 6: Build "near me" pages (6) + brand near me (9)
- Step 7: Build problem near me (8) + combo pages (4) + intent pages (3)
- Step 8: Blog posts (10) + core pages (5)
- Step 9: llms.txt + robots.txt + sitemap.xml (all 129 URLs)
- Step 10: PageSpeed check

**Agent 3: fixlifyservices.com** → 135 pages, V8 Cinematic Dark
- Step 1: Create Golden Template with V8 design
- Step 2: BMAD v4 compliance check
- Step 3: Build config.js + shared includes
- Step 4: Build service×location generator (60 pages)
- Step 5: Build cost guides (10) + problem diagnosis (10)
- Step 6: Build emergency pages (3) + emergency×city (8)
- Step 7: Build brand pages (6) + location pages (14)
- Step 8: Blog posts (10) + core pages (5) + bonus pages (3)
- Step 9: llms.txt + robots.txt + sitemap.xml
- Step 10: PageSpeed check

**Agent 4: GitHub + Vercel setup** (after agents 1-3 complete)
- Create 3 GitHub repos: nappliancerepair, appliancerepairneary, fixlifyservices
- Connect each to Vercel
- Set custom domains in Vercel
- Update DNS at registrar (CNAME to Vercel)
- Submit all 3 sitemaps to Google Search Console
- Run Google Indexing API for top 20 pages on each site

### Output directories:
```
C:/nappliancerepair/          ← Site 1 (new GitHub repo)
C:/appliancerepairneary/      ← Site 2 (new GitHub repo)
C:/fixlifyservices/           ← Site 3 (new GitHub repo)
C:/NikaApplianceRepair/       ← Site 0 (existing, updated)
C:/fixlify-agents/src/agents/ ← 2 new agents added
```

### Deployment per site:
1. Create GitHub repo
2. Push code
3. Connect to Vercel
4. Point domain in Vercel → DNS at registrar

---

## Shared Assets (copy from nikaappliancerepair.com)

- Phone: (437) 524-1053
- Booking URL: https://hub.fixlify.app/book/nicks-appliance-repair-b8c8ce
- Rating: 4.9★, 5,200+ repairs
- Warranty: 90-day parts & labor
- Hours: Mon-Sat 8am-8pm, Sun 9am-6pm
- Service area: Toronto, Scarborough, North York, Etobicoke, Mississauga, Brampton, Vaughan, Richmond Hill, Markham, Oakville, Burlington, Pickering, Ajax, Whitby, Oshawa
- Images: /assets/images/ from nikaappliancerepair.com (copy)
- Header/footer: new shared includes per site

---

## ANTI-SPAM & GOOGLE POLICY

### Is 3 sites for 1 business allowed? ✅ YES — with conditions
Google doesn't ban multiple sites for one business. BUT will penalize "doorway pages":
- ❌ BAD: thin pages, same text just city swapped, no real value
- ✅ GOOD: each site has unique angle, real content, genuine user value

Our 3 sites have different purposes:
- nappliancerepair.com = brand expertise (Samsung/LG specialists)
- appliancerepairneary.com = hyper-local convenience (near me, every GTA city)
- fixlifyservices.com = online booking & cost transparency

### Anti-Spam Checklist (ALL sites)

**Content uniqueness:**
- [ ] Gemini API for unique 150-word intro per generated page (NOT template rotation)
- [ ] Different H2 structure per page type (not identical section order)
- [ ] Rotate FAQ questions — pull from pool of 20+, not same 8 every time
- [ ] Each page has page-specific data (price table, issues list, city details)

**Trust signals (add to all pages):**
- [ ] 3-4 real customer reviews per page (take from nikaappliancerepair.com reviews)
  - Include: first name + city, star rating, specific appliance, date
  - Example: "Maria K., Scarborough — Samsung fridge repair, March 2025 ★★★★★"
- [ ] Technician author block on service pages: "Reviewed by Nika Appliance Repair Team — Licensed Technicians"
- [ ] Real photos from main site (technician photos, appliance photos)

**NAP Consistency (CRITICAL for Google):**
- Phone: (437) 524-1053 — IDENTICAL on all 4 sites
- Business name in LocalBusiness schema: "Nika Appliance Repair" (same on all)
- Display names can differ (N Appliance Repair / Appliance Repair Near Me / Fixlify Services)
- Do NOT create separate Google Business Profile for new sites → use main one

**Social media links (YES, safe to add):**
- Footer of each new site: link to Facebook/Instagram/YouTube of nikaappliancerepair.com
- This reinforces entity signals (same business across multiple web properties)
- Natural, not spam

**Internal structure signals:**
- [ ] About page on each site — real business story (not copy of main site)
- [ ] Contact page with same phone (NAP)
- [ ] Privacy Policy + Terms (even simple ones)
- [ ] Sitemap.xml submitted to GSC

**What NOT to do:**
- ❌ Don't use identical intro paragraphs across sites
- ❌ Don't interlink sites aggressively (max 1 footer link per site)
- ❌ Don't submit all 3 sites as same property in GSC
- ❌ Don't create 3 Google Business Profiles

## Content Differentiation (avoid duplicate penalties)

Each site must have unique content despite same business:

| Site | Unique Angle | Tone | H1 Example |
|------|-------------|------|------------|
| nikaappliancerepair.com | Brand story, team, reviews | Warm, personal | "Toronto's Trusted Appliance Repair" |
| nappliancerepair.com | Professional, comprehensive | Expert, authoritative | "GTA Appliance Repair — All Brands, All Models" |
| appliancerepairneary.com | Location convenience, "near me" | Local, nearby | "Appliance Repair Near You in Toronto & GTA" |
| fixlifyservices.com | Speed, booking, online-first | Urgent, modern | "Book Appliance Repair Online — Available Today" |

---

## Timeline

| Phase | What | When |
|-------|------|------|
| 1 | Launch 5 agents in parallel | NOW |
| 2 | Review output, fix issues | After agents complete |
| 3 | Create GitHub repos | After review |
| 4 | Deploy to Vercel | After repos |
| 5 | Point domains in DNS | After Vercel |
| 6 | Submit all 4 sitemaps to GSC | After DNS |
| 7 | Request indexing (Google Indexing API) | After GSC |

---

## Success Metrics (30 days)

- All 4 sites: PageSpeed 90+ mobile + desktop
- Schema validation: 100% pass (Google Rich Results Test)
- All pages indexed by Google
- AI citation: appear in ChatGPT/Perplexity for "appliance repair Toronto"
- Combined organic impressions: 5,000+/month
