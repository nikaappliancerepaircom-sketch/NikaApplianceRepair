# nappliancerepair.ca — Full Redesign Plan

## Project Overview

- **Domain:** nappliancerepair.ca (5 years old, domain authority established)
- **Current stack:** WordPress + Elementor Pro + 12 plugins
- **New stack:** Static HTML + Vanilla CSS/JS (same as nappliancerepair.com)
- **Hosting:** GitHub (nikaappliancerepaircom-sketch) + Vercel
- **Google account:** nappliancerepair.ca@gmail.com
- **GSC verified:** YES (nika-316 service account added as Owner)

## Critical Constraint: Preserve ALL indexed URLs

Every URL that currently gets impressions in Google MUST have a 1:1 match in the new site OR a 301 redirect.

---

## PHASE 1: Full Page Inventory (from GSC + Crawler)

### Total discovered: ~302 WordPress pages, ~130 with GSC impressions

---

## 1A. CORE PAGES (must recreate)

| Current URL | Clicks | Impressions | Position | Action |
|------------|--------|-------------|----------|--------|
| `/` | 231 | 48,194 | 16.1 | RECREATE — clone design, improve content |
| `/about-us/` | 1 | 128 | 18.2 | RECREATE |
| `/why-choose-us/` | 0 | 23 | 24.8 | RECREATE |
| `/our-working-process/` | 0 | 14 | 3.4 | RECREATE |
| `/frequently-asked-questions/` | 0 | 36 | 23.1 | RECREATE |
| `/testimonials/` | 2 | 132 | 16.0 | RECREATE |
| `/booking/` | 27 | 1,174 | 12.7 | RECREATE (Fixlify iframe) |
| `/blog/` | 0 | 1 | 2.0 | RECREATE |
| `/brands-we-service/` | 0 | 118 | 25.5 | RECREATE |
| `/services/` | — | — | — | RECREATE (hub page) |
| `/privacy-policy/` | 0 | 14 | 35.9 | RECREATE |
| `/terms-of-use/` | 0 | 3 | 19.0 | RECREATE |
| `/cancellation-policy/` | 0 | 7 | 13.4 | RECREATE |
| `/html-sitemap/` | 0 | 23 | 55.3 | RECREATE |
| `/appliance-repair-technician-jobs/` | 0 | 23 | 52.5 | RECREATE |

**Total core pages: 15**

---

## 1B. SERVICE PAGES (must recreate — NONE were in sitemap!)

| Current URL | Clicks | Impressions | Position | Action |
|------------|--------|-------------|----------|--------|
| `/appliance-repair/` | 1 | 403 | 35.6 | RECREATE + optimize |
| `/refrigerator-repair/` | 0 | 180 | 47.8 | RECREATE + optimize |
| `/washing-machine-repair/` | 0 | 939 | 63.1 | RECREATE + optimize |
| `/dishwasher-repair-service/` | 0 | 35 | 39.9 | RECREATE + optimize |
| `/dryer-repair-services/` | 0 | 104 | 55.0 | RECREATE + optimize |
| `/oven-repair-service/` | 0 | 110 | 58.1 | RECREATE + optimize |
| `/stove-repair-services/` | 0 | 79 | 65.5 | RECREATE + optimize |
| `/commercial-appliance-repair/` | 5 | 1,535 | 41.9 | RECREATE + optimize |
| `/gas-appliance-repair/` | 2 | 1,447 | 46.3 | RECREATE + optimize |
| `/appliance-installation-services/` | 0 | 965 | 62.3 | RECREATE + optimize |
| `/appliance-maintenance-services/` | 0 | 47 | 50.3 | RECREATE + optimize |
| `/appliance-repair/appliance-repair-cost/` | 1 | 1,071 | 53.7 | RECREATE + optimize |

**Total service pages: 12**

---

## 1C. BRAND PAGES (must recreate — NONE were in sitemap!)

| Current URL | Clicks | Impressions | Position | Action |
|------------|--------|-------------|----------|--------|
| `/blomberg-appliance-repair/` | 20 | 3,798 | 14.7 | CRITICAL — top performer |
| `/frigidaire-appliance-repair/` | 5 | 2,900 | 24.4 | HIGH |
| `/kitchenaid-appliance-repair/` | 5 | 1,518 | 36.9 | HIGH |
| `/lg-appliance-repair/` | 3 | 2,786 | 43.9 | HIGH |
| `/liebherr-appliance-repair/` | 3 | 344 | 18.6 | MEDIUM |
| `/viking-appliance-repair/` | 3 | 647 | 37.2 | MEDIUM |
| `/fulgor-milano-appliance-repair/` | 4 | 1,279 | 11.7 | HIGH (good position!) |
| `/cyclone-appliance-repair-service/` | 2 | 196 | 12.8 | MEDIUM |
| `/sub-zero-appliance-repair/` | 2 | 736 | 36.9 | MEDIUM |
| `/bosch-appliance-repair/` | 1 | 2,678 | 40.8 | HIGH |
| `/electrolux-appliance-repair/` | 1 | 748 | 43.9 | MEDIUM |
| `/fisher-paykel-appliance-repair/` | 1 | 596 | 37.1 | MEDIUM |
| `/huebsch-appliance-repair/` | 1 | 278 | 32.6 | LOW |
| `/jennair-appliance-repair/` | 1 | 683 | 46.3 | MEDIUM |
| `/panasonic-appliance-repair/` | 1 | 512 | 33.3 | MEDIUM |
| `/samsung-appliance-repair/` | 0 | 2,037 | 47.4 | HIGH |
| `/whirlpool-appliance-repair/` | 0 | 2,367 | 39.5 | HIGH |
| `/ge-appliance-repair/` | 0 | 1,765 | 37.2 | HIGH |
| `/maytag-appliance-repair/` | 0 | 2,180 | 46.8 | HIGH |
| `/kenmore-sears-appliance-repair/` | 0 | 1,634 | 30.3 | HIGH |
| `/dacor-appliance-repair/` | 0 | 465 | 23.2 | MEDIUM |
| `/amana-appliance-repair/` | 0 | 314 | 45.3 | LOW |
| `/bertazzoni-appliance-repair/` | 0 | 470 | 34.9 | MEDIUM |
| `/inglis-appliance-repair/` | 0 | 456 | 38.4 | MEDIUM |

**Total brand pages: 24**

---

## 1D. LOCATION PAGES — Major Cities

| Current URL | Clicks | Impressions | Position | Action |
|------------|--------|-------------|----------|--------|
| `/appliance-repair-richmond-hill/` | 50 | 9,394 | 12.0 | CRITICAL — #1 city performer |
| `/appliance-repair-uxbridge/` | 10 | 1,512 | 13.6 | HIGH |
| `/appliance-repair-brampton/` | 8 | 15,533 | 53.9 | HUGE opportunity |
| `/appliance-repair-gwillimbury/` | 4 | 652 | 29.2 | MEDIUM |
| `/appliance-repair-east-york/` | 3 | 1,806 | 13.9 | HIGH |
| `/appliance-repair-markham/` | 3 | 4,932 | 39.4 | HIGH opportunity |
| `/appliance-repair-north-york/` | 0 | 7,295 | 56.1 | HUGE opportunity |
| `/appliance-repair-mississauga/` | 1 | 6,264 | 59.4 | HUGE opportunity |
| `/appliance-repair-hamilton/` | 0 | 5,512 | 51.4 | MEDIUM (far from Toronto) |
| `/appliance-repair-vaughan/` | 1 | 4,189 | 54.6 | HIGH opportunity |
| `/appliance-repair-oshawa/` | 0 | 3,801 | 48.5 | MEDIUM |
| `/appliance-repair-greater-toronto-area/` | 1 | 3,697 | 53.9 | HIGH (hub page) |
| `/appliance-repair-scarborough/` | 0 | 2,685 | 35.8 | HIGH |
| `/appliance-repair-whitby/` | 0 | 2,213 | 57.7 | MEDIUM |
| `/appliance-repair-toronto/` | 1 | 2,191 | 64.9 | CRITICAL — main city! |
| `/appliance-repair-newmarket/` | 0 | 1,704 | 45.8 | MEDIUM |
| `/appliance-repair-burlington/` | 0 | 1,402 | 54.4 | MEDIUM |
| `/appliance-repair-oakville/` | 0 | 1,371 | 63.9 | MEDIUM |
| `/appliance-repair-etobicoke/` | 0 | 1,104 | 51.0 | MEDIUM |
| `/appliance-repair-ajax/` | 0 | 1,076 | 39.6 | MEDIUM |
| `/appliance-repair-aurora/` | 0 | 1,012 | 35.6 | MEDIUM |
| `/appliance-repair-mount-albert/` | 1 | 1,561 | 64.9 | LOW |
| `/appliance-repair-king-city/` | 0 | 492 | 32.2 | LOW |
| `/appliance-repair-bradford/` | 0 | 517 | 64.5 | LOW |
| `/appliance-repair-pickering/` | 0 | 518 | 37.9 | MEDIUM |
| `/appliance-repair-unionville/` | 0 | 513 | 40.3 | LOW |
| `/appliance-repair-innisfil/` | 0 | 254 | 43.0 | LOW |
| `/appliance-repair-woodbridge/` | 0 | 400 | 28.7 | LOW |
| `/appliance-repair-concord/` | 0 | 187 | 36.4 | LOW |
| `/appliance-repair-thornhill/` | 0 | 356 | 24.8 | MEDIUM |
| `/appliance-repair-stouffville/` | 0 | 267 | 25.0 | LOW |
| `/appliance-repair-schomberg/` | 1 | 128 | 25.2 | LOW |
| `/appliance-repair-maple/` | 0 | 119 | 47.9 | LOW |
| `/appliance-repair-kleinburg/` | 0 | 102 | 35.2 | LOW |
| `/holland-landing-appliance-repair/` | 1 | 166 | 20.3 | LOW |
| `/appliance-repair-edmonton/` | 0 | 17,561 | 63.7 | OUT-OF-AREA — 301 redirect to / |
| `/appliance-repair-calgary/` | 0 | 6,317 | 67.1 | OUT-OF-AREA — 301 redirect to / |

**Total location pages: 37 (keep 35, redirect 2 out-of-area)**

---

## 1E. NEIGHBOURHOOD PAGES (micro-locations)

| Current URL | Impressions | Position | Action |
|------------|-------------|----------|--------|
| `/appliance-repair-steeles/` | 46 | 27.5 | KEEP (3 clicks) |
| `/appliance-repair-richvale/` | 62 | 24.2 | KEEP |
| `/appliance-repair-berczy-village/` | 54 | 34.8 | KEEP |
| `/get-reliable-home-appliance-repairs-in-milliken/` | 70 | 41.9 | KEEP |
| `/appliance-repair-greensborough/` | 59 | 42.9 | KEEP |
| `/appliance-repair-bayview-glen/` | 24 | 29.1 | KEEP |
| `/appliance-repair-oak-ridges/` | 53 | 44.4 | KEEP |
| `/appliance-repair-raymerville-markville-east/` | 25 | 49.6 | KEEP |
| `/appliance-repair-hillcrest-village/` | 37 | 44.5 | KEEP |
| `/appliance-repair-don-valley-village/` | 87 | 67.1 | KEEP |
| `/appliance-repair-gormley/` | 31 | 46.0 | KEEP |
| `/appliance-repair-agincourt/` | 19 | 23.7 | KEEP |
| `/appliance-repair-cachet/` | 18 | 29.9 | KEEP |
| `/appliance-repair-cathedraltown/` | 20 | 74.5 | KEEP |
| `/appliance-repair-beverley-acres/` | 19 | 43.7 | KEEP |
| `/appliance-repair-beverley-glen/` | 19 | 63.2 | KEEP |
| `/appliance-repair-yongehurst/` | 19 | 63.5 | KEEP |
| `/appliance-repair-lamoreaux/` | 16 | 65.0 | KEEP |
| `/appliance-repair-langstaff/` | 10 | 61.2 | KEEP |
| `/appliance-repair-unionville/` | 513 | 40.3 | KEEP |
| `/appliance-repair-wismer-commons/` | 14 | 61.4 | KEEP |
| `/appliance-repairs-in-elgin-mills/` | 7 | 17.6 | KEEP |

**Total neighbourhood pages: 22**

---

## 1F. BLOG / ARTICLE POSTS (from post-sitemap.xml — 157 total)

### TOP blog posts by GSC performance:

| URL | Clicks | Impressions | Position | Action |
|-----|--------|-------------|----------|--------|
| `/washing-machine-repair/speed-queen-washer-error-codes/` | 95 | 11,991 | 10.8 | CRITICAL |
| `/refrigerator-repair/ge-refrigerator-not-cooling/` | 19 | 8,593 | 13.5 | HIGH |
| `/blog/dryer-not-heating-heres-how-to-solve-it/` | 2 | 7,775 | 36.6 | HIGH opportunity |
| `/samsung-appliance-repair/samsung-washer-sud-code/` | 3 | 3,242 | 24.9 | HIGH |
| `/dishwasher-repair/dishwasher-is-leaking/` | 0 | 3,062 | 75.1 | MEDIUM |
| `/dishwasher-repair/whirlpool-dishwasher-not-washing/` | 1 | 3,133 | 11.1 | HIGH (good position!) |
| `/oven-repair/frigidaire-oven-self-clean/` | 6 | 2,989 | 38.2 | MEDIUM |
| `/dryer-repair/lg-dryer-cl-code/` | 5 | 2,050 | 11.8 | HIGH (good position!) |
| `/oven-repair/whirlpool-oven-not-heating/` | 2 | 2,454 | 23.2 | MEDIUM |
| `/oven-repair/how-to-use-a-ge-self-cleaning-oven/` | 0 | 2,262 | 38.5 | MEDIUM |
| `/dishwasher-repair/samsung-dishwasher-lc-code/` | 1 | 2,144 | 24.8 | MEDIUM |
| `/refrigerator-repair/samsung-refrigerator-not-making-ice/` | 0 | 2,106 | 58.2 | MEDIUM |
| `/dryer-repair/dryer-wont-start/` | 1 | 2,618 | 45.4 | MEDIUM |
| `/samsung-appliance-repair/how-to-fix-samsung-washer-ur-code/` | 5 | 1,681 | 15.8 | HIGH |
| `/dishwasher-repair/dishwasher-leaking-from-bottom-of-door/` | 4 | 1,984 | 31.7 | MEDIUM |
| `/dryer-repair/samsung-dryer-not-heating/` | 1 | 1,937 | 51.5 | MEDIUM |
| `/blog/how-long-do-eggs-last-in-the-fridge/` | 0 | 1,741 | 66.3 | MEDIUM |
| `/kitchenaid-appliance-repair/kitchenaid-dishwasher-troubleshooting/` | 1 | 1,550 | 22.2 | MEDIUM |
| `/whirlpool-appliance-repair/whirlpool-refrigerator-not-cooling/` | 0 | 1,480 | 34.3 | MEDIUM |
| `/dishwasher-repair/dishwasher-not-getting-water/` | 0 | 1,394 | 55.5 | MEDIUM |
| `/dryer-repair/dryer-not-spinning/` | 0 | 1,156 | 69.8 | MEDIUM |
| `/appliance-repair/appliance-repair-cost/` | 1 | 1,071 | 53.7 | MEDIUM |
| `/refrigerator-repair/ge-fridge-not-cooling/` | 5 | 1,049 | 15.9 | HIGH |
| `/oven-repair/ge-oven-self-clean/` | 3 | 1,088 | 41.5 | MEDIUM |
| `/blog/how-long-does-a-dishwasher-run-and-why/` | 0 | 1,010 | 64.1 | MEDIUM |
| `/dryer-repair/ge-dryer-not-starting/` | 1 | 1,010 | 37.4 | MEDIUM |
| `/dishwasher-repair/lg-dishwasher-error-codes/` | 3 | 879 | 38.3 | MEDIUM |
| `/dishwasher-repair/ge-dishwasher-not-draining/` | 1 | 505 | 33.1 | LOW |
| `/dishwasher-repair/how-long-does-a-dishwasher-take/` | 1 | 3,870 | 61.8 | MEDIUM |
| `/washing-machine-repair/washer-not-spinning/` | 1 | 697 | 75.7 | MEDIUM |
| `/dishwasher-repair/dishwasher-air-gap-leaking/` | 0 | 780 | 41.9 | MEDIUM |
| `/refrigerator-repair/refrigerator-not-cooling-or-refrigerator-not-getting-cold/` | 0 | 583 | 47.4 | MEDIUM |
| `/refrigerator-repair/smeg-fridge/` | 0 | 319 | 19.5 | LOW |
| `/refrigerator-repair/counter-depth-fridge/` | 0 | 245 | 58.4 | LOW |
| `/blog/speed-queen-appliances/` | 1 | 149 | 40.6 | LOW |
| `/oven-repair/self-cleaning-oven/` | — | — | — | KEEP |
| `/oven-repair/convection-oven/` | — | — | — | KEEP |
| `/dryer-repair/squeaky-dryer/` | 0 | 31 | 37.7 | LOW |
| `/dryer-repair/dryer-not-heating/` | 0 | 92 | 74.3 | LOW |
| `/dishwasher-repair/bosch-dishwasher-e24-faulty-code/` | 0 | 43 | 27.4 | LOW |
| `/samsung-appliance-repair/samsung-dishwasher-error-codes/` | — | — | — | KEEP |

### Location sub-posts (city-specific blog articles, 72 total):

These are posts like `/appliance-repair-toronto/5-best-appliance-repair-services-in-toronto/` — they provide supporting content for city pages.

**Decision: KEEP all that have impressions, 301 redirect the rest to parent city page.**

### Posts with 0 impressions or not in GSC:

301 redirect to parent page or closest relevant page.

**Total posts to recreate: ~50 (those with impressions)**
**Total posts to 301 redirect: ~107 (no impressions)**

---

## 1G. QUICK WIN KEYWORDS (position 4-20, optimize these pages first!)

| Keyword | Impressions | Position | Page | Action |
|---------|-------------|----------|------|--------|
| appliance repair east gwillimbury | 412 | **1.1** | /appliance-repair-gwillimbury/ | PROTECT — #1! |
| fridge is not cooling | 290 | **1.2** | /refrigerator-repair/ | PROTECT |
| breville toaster oven repair near me | 10 | **1.0** | / | PROTECT |
| dishwasher repair richmond hill | 507 | **1.7** | / | PROTECT |
| nick's appliance repair | 332 | **3.4** | / | PROTECT brand |
| appliance repair bradford | 548 | **4.8** | /appliance-repair-bradford/ | BOOST to #1 |
| sr code on speed queen washer | 137 | **4.8** | /speed-queen-error-codes/ | BOOST |
| speed queen sr code | 98 | **5.0** | /speed-queen-error-codes/ | BOOST |
| ge refrigerator not cooling or freezing | 583 | **6.4** | /ge-refrigerator-not-cooling/ | BOOST |
| washing machine repair newmarket | 169 | **6.8** | various | BOOST |
| blomberg appliance repair toronto | 124 | **6.8** | /blomberg/ | BOOST |
| appliance repair uxbridge | 56 | **8.9** | /appliance-repair-uxbridge/ | BOOST to TOP 5 |
| dryer repair richmond hill | 190 | **8.8** | /appliance-repair-richmond-hill/ | BOOST |
| washing machine repair richmond hill | 126 | **9.0** | various | BOOST |
| speed queen washer error codes | 11,991 | **10.8** | /speed-queen/ | BOOST to TOP 5 |
| appliance repair richmond hill | 1,762 | **12.0** | /appliance-repair-richmond-hill/ | PUSH to page 1 |
| appliance repair north york | 1,461 | **16.8** | /appliance-repair-north-york/ | PUSH to page 1 |
| appliance repair newmarket | 1,256 | **16.5** | /appliance-repair-newmarket/ | PUSH to page 1 |
| dishwasher repair north york | 1,191 | **18.5** | various | PUSH to page 1 |
| appliance repair | 1,102 | **13.3** | / | PUSH to page 1 |

---

## PHASE 2: Design Specification

### Source Design: nappliancerepair.ca (WordPress/Elementor)

**Visual Identity:**
- Primary color: `#18256D` (navy blue) — headings
- Accent green: `#1EC651` — CTA buttons
- Accent pink: `#F52A85` — highlights
- Orange: `#F5962A` — section accents
- Cyan: `#1ECBEA` — gradient endpoint
- Heading font: **Fredoka One** (playful, rounded)
- Body font: **Rubik** (clean sans-serif)
- Script font: **Mrs Saint Delafield** (decorative accents)

**Layout:**
- Special offer top bar (red)
- Transparent header with sticky scroll
- Hero with dark overlay + countdown timer
- 6 service cards (colored texture backgrounds)
- Why Choose Us (6 icon boxes)
- Brand logos gallery (20+ brands)
- Video testimonials (YouTube embed)
- Gradient feature section (navy → cyan)
- Stats counter
- Long-form SEO content
- Locations list with green checkmarks
- Working process (3 steps)
- FAQ accordion
- Payment methods
- 3-column footer

**Key Elements to Clone:**
1. Countdown timer for "$40 OFF" deal
2. Service cards with colored texture backgrounds
3. Green pill-shaped CTA buttons (border-radius: 24px)
4. Fredoka One headings (friendly feel)
5. Stats counter animation
6. Brand logo gallery
7. YouTube video embed with overlay
8. Location list with checkmark icons

### New Stack (matching nappliancerepair.com architecture):

```
nappliancerepair.ca/
├── index.html                     (homepage)
├── tokens.css                     (design tokens — adapted from WP design)
├── config.js                      (business config)
├── _redirects                     (301 redirects)
├── robots.txt                     (allow all + AI crawlers)
├── llms.txt                       (AI search optimization)
├── sitemap.xml                    (all pages!)
├── includes/
│   ├── header.html                (global header)
│   ├── header-loader.js
│   ├── footer.html                (global footer)
│   └── footer-loader.js
├── assets/
│   ├── images/                    (icons, hero, textures)
│   └── reviewers/                 (testimonial photos)
├── about.html
├── booking.html
├── contact.html
├── faq.html
├── testimonials.html
├── why-choose-us.html
├── our-working-process.html
├── privacy-policy.html
├── terms-of-use.html
├── cancellation-policy.html
├── careers.html
├── brands-we-service.html
├── [service]-repair.html          (6 base service pages)
├── commercial-appliance-repair.html
├── gas-appliance-repair.html
├── appliance-installation.html
├── appliance-maintenance.html
├── appliance-repair-cost.html
├── [brand]-appliance-repair.html  (24 brand pages)
├── appliance-repair-[city].html   (35 city pages)
├── appliance-repair-[hood].html   (22 neighbourhood pages)
├── blog/
│   ├── index.html
│   └── [slug].html                (~50 blog posts with impressions)
├── [category]/[article].html      (article posts in service/brand paths)
└── data/
    ├── services.js
    ├── cities.js
    └── brands.js
```

---

## PHASE 3: Content Strategy

### Per page type:

**Service pages** (12 pages):
- 800+ words unique content per page
- Answer capsule in first paragraph (phone + city + service)
- 4 unique FAQs with FAQPage schema
- LocalBusiness + Service schema
- Internal links to related blog posts
- Brand mentions (which brands we repair for this appliance)
- Pricing section
- CTA every 2-3 sections

**Brand pages** (24 pages):
- 600+ words unique content per brand
- Common error codes for that brand
- "Why choose us for [Brand] repair"
- LocalBusiness schema
- Links to service pages

**City pages** (35 pages):
- 800+ words unique content per city
- Specific neighborhood mentions
- Local landmarks/context
- "Appliance Repair [City]" as H1
- Service area map or description
- All 6 services listed
- LocalBusiness schema with city address

**Blog posts** (~50 pages):
- Keep existing content, expand if under 400 words
- Add answer capsule
- Add FAQ section
- Article + FAQPage schema

---

## PHASE 4: 301 Redirects

### Must redirect (URL structure changes):

| Old URL | New URL | Reason |
|---------|---------|--------|
| `/appliance-repair-edmonton/` | `/` | Out of area |
| `/appliance-repair-calgary/` | `/` | Out of area |
| `/thank-you/` | `/booking/` | Merge |
| `/home-demo/` | `/` | Test page |
| `/disquiz/` | `/` | Not needed |
| `/author/shadowdancer1988/` | `/about-us/` | Security |

### Blog posts with 0 impressions → redirect to parent:

~107 blog posts with 0 GSC impressions → 301 to closest parent page.

Example:
- `/appliance-repair-brampton/common-misconceptions-appliance-repair-brampton/` → `/appliance-repair-brampton/`
- `/appliance-repair-concord/understanding-concords-appliance-repair-regulations/` → `/appliance-repair-concord/`

### URL normalization:

Some WP URLs have different patterns than expected:
- `/dishwasher-repair-service/` (WP) → keep as-is (or redirect to `/dishwasher-repair/`)
- `/dryer-repair-services/` (WP) → keep as-is

**Decision:** Keep exact same URLs as WordPress to preserve all backlinks and rankings.

---

## PHASE 5: Technical SEO (new site must have)

### Schema per page:
- LocalBusiness (every page)
- Service (service pages)
- FAQPage (pages with FAQ)
- Article (blog posts)
- BreadcrumbList (every page)
- AggregateRating (homepage + service pages)

### Robots.txt:
```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: https://nappliancerepair.ca/sitemap.xml
```

### GEO (AI Search Optimization):
- llms.txt at root
- Answer capsule on every page
- TL;DR box for AI extraction
- Deep content (800+ words)
- FAQ visible on page (not just schema)

### Security Headers (Vercel):
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {"key": "X-Content-Type-Options", "value": "nosniff"},
        {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
        {"key": "Strict-Transport-Security", "value": "max-age=31536000"},
        {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
        {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}
      ]
    }
  ]
}
```

---

## PHASE 6: Migration Steps

1. **Create GitHub repo** under nikaappliancerepaircom-sketch/nappliancerepairca
2. **Clone design** — recreate homepage in static HTML matching WP visual design
3. **Create template system** — header/footer includes, tokens.css with WP colors
4. **Build all pages** — core → service → brand → city → neighbourhood → blog
5. **Extract content** from WP (API: wp-json/wp/v2/pages and posts)
6. **Rewrite content** — expand thin pages, add answer capsules, FAQs
7. **Add schema** — LocalBusiness + Service + FAQPage on every page
8. **Generate sitemap** — ALL pages (not just 22 like current WP!)
9. **Set up 301 redirects** — _redirects file for removed pages
10. **Deploy to Vercel** under nappliancerepair.ca domain
11. **Verify in GSC** — add DNS TXT record, verify property
12. **Submit sitemap** — new complete sitemap to GSC
13. **Monitor** — track position changes for 4-8 weeks
14. **Auto-publish workflow** — GitHub Actions for blog auto-publish

---

## PHASE 7: Page Count Summary

| Type | Count |
|------|-------|
| Core pages | 15 |
| Service pages | 12 |
| Brand pages | 24 |
| City pages | 35 |
| Neighbourhood pages | 22 |
| Blog/article posts | ~50 |
| **TOTAL pages to build** | **~158** |
| Pages to 301 redirect | ~107 |
| Pages to remove (out of area) | 2 |

---

## Business Config

```javascript
const BUSINESS = {
  name: "Nick's Appliance Repair Service",
  shortName: "Nick's Appliance Repair",
  phone: "(437) 524-1053",
  tel: "tel:+14375241053",
  email: "care@nappliancerepair.ca",
  booking: "https://hub.fixlify.app/book/nicks-appliance-repair-b8c8ce",
  rating: "4.9",
  reviews: "5,200+",
  warranty: "90-day",
  experience: "5+",
  hours: "Mon-Sat 8am-8pm, Sun 9am-6pm",
  domain: "nappliancerepair.ca",
  addresses: [
    "60 Walter Tunny Crescent, East Gwillimbury, ON L9N 0R4",
    "755 Steeles Ave W #311, North York, ON M2R 3W9",
    "Marshall St, Richmond Hill, ON L4C 0A5"
  ],
  social: {
    facebook: true,
    instagram: true,
    youtube: true,
    yelp: true
  }
};
```

---

## Expected Outcomes After Redesign

| Metric | Current | Expected (8 weeks) |
|--------|---------|-------------------|
| Page load (HTML) | 1,486 KB | ~50-80 KB |
| PageSpeed Mobile | ~30-40 | 90+ |
| Pages in sitemap | 180 | 302+ |
| Average position | 40+ | 20-30 |
| Monthly clicks | ~660 | 2,000+ |
| Quick win keywords (pos 4-20) | 30 | 30 in TOP 5 |
| Schema types | Product (wrong!) | LocalBusiness+Service+FAQ |
| Security headers | 0 | 5+ |
| AI search ready | No | Yes (llms.txt, answer capsule) |
