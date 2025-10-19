# Nika Appliance Repair - Project Context

## Project Overview
Appliance repair business website serving Toronto and GTA. Focus on residential appliance repair services (refrigerators, dishwashers, washers, dryers, ovens, stoves, microwaves, etc.).

## Business Data
- **Company**: Nika Appliance Repair
- **Phone**: 437-747-6737
- **Service Area**: Toronto, Mississauga, Brampton, North York, Scarborough, Etobicoke, Markham, Vaughan, Richmond Hill
- **Hours**: 24/7 Emergency Service
- **Rating**: 4.9 ★
- **Reviews**: 5,200+
- **Warranty**: 90-day warranty on all repairs
- **Experience**: 6+ years

## Tech Stack
- HTML5, CSS3, JavaScript
- No framework (vanilla)
- Schema.org structured data
- Mobile-first responsive design

## Project Structure
```
/
├── index.html                 # Homepage
├── services/                  # Service pages (11 pages)
│   ├── refrigerator-repair.html
│   ├── dishwasher-repair.html
│   ├── washer-repair.html
│   └── ... (8 more)
├── locations/                 # Location pages (9 pages)
│   ├── toronto.html
│   ├── mississauga.html
│   └── ... (7 more)
├── brands/                    # Brand pages (40+ pages)
├── blog/                      # Blog articles
├── css/                       # Stylesheets
├── js/                        # JavaScript files
├── assets/                    # Images, icons
└── tools/                     # BMAD testing & optimization tools

Total pages: 64+
```

## BMAD Method
**Business Marketing Acquisition Development** - 277 parameters for testing and optimizing web pages.

### BMAD v2 Structure (New)
Testing organized in 4 priority tiers:
- **Tier 1**: 15 critical parameters (data consistency, core schema) - Must pass 100%
- **Tier 2**: 30 high priority (SEO, CRO essentials) - Target 85%
- **Tier 3**: 50 medium priority (UX, psychology) - Target 70%
- **Tier 4**: 182 low priority (polish, advanced features) - Target 50%

### Tools Location
- `tools/bmad-v2/` - New modular testing system
- `tools/bmad-complete-test.py` - Legacy 277-param test (being replaced)

## Optimization Goals
1. All pages pass Tier 1 (100% data consistency)
2. Homepage + Service pages score 85+ overall
3. Location pages score 80+ overall
4. Maintain mobile-first responsive design
5. Keep page load under 3 seconds

## Key Features
- LocalBusiness schema on all pages
- AggregateRating schema
- Responsive typography with CSS clamp()
- Mobile hamburger menu
- Trust signals (licensed, insured, warranty)
- Multiple CTAs (call, form, email)
- Emergency service messaging
- Same-day service availability

## Brand & Service Focus
**⚠️ CRITICAL: Read `BMAD FOR NICK/BRAND-AND-SERVICE-FOCUS.md` before creating/editing any page**

### Brand Strategy (Dual-Tier Positioning)
- **Primary (70%):** Standard brands - Samsung, LG, Whirlpool, GE, Maytag, Frigidaire
- **Secondary (30%):** Luxury brands - Sub-Zero, Wolf, Miele, Thermador (Oakville/Markham/Richmond Hill/Vaughan ONLY)
- **Geographic Rule:** Luxury brands ONLY in 4 affluent cities, standard brands in all 28 other cities
- **Brand Mentions:** 8-12 popular brands per page, 0 luxury brands in standard areas

### Service Focus (Residential Only)
- **9 Core Services:** Refrigerator, Washer, Dryer, Dishwasher, Oven, Stove, Range, Microwave, Freezer
- **NO Commercial:** Residential appliances only, no restaurant/industrial equipment
- **Positioning:** Affordable repair alternative (save 50-70% vs replacement)

### Tone by Location Type
- **Standard Areas (28 cities):** "Affordable rates", "transparent pricing", "honest service"
- **Luxury Areas (4 cities):** "White-glove service", "premium brands", "discreet appointments"

## Content Strategy
- Pain point focus (broken appliances, emergency repairs)
- Social proof emphasis (reviews, ratings, testimonials)
- Urgency triggers (same-day, 24/7, now)
- Authority signals (licensed, certified, experienced)
- Clear value propositions
- Service area coverage
- **Brand consistency:** Popular brands on all pages, luxury brands only in designated cities

## SEO Strategy
- **Target word count: 2,000-2,500 per page** (visible content only, excluding HTML/CSS/JS)
- Keyword density: 1.5-2.5%
- Internal linking: 10+ links per page
- Images: 10+ with alt text
- FAQ sections with schema
- Location-specific content
- Service-specific content

## Word Count Tool
- **Count visible words:** `node tools/count-visible-words.js <file.html>`
- **Python alternative:** `python verify_word_count.py` (edit file path inside script)
- **Important:** Word count = visible text only (no HTML tags, CSS, JavaScript, or meta tags)

## Commands
- Test page: `python tools/bmad-v2/auto-run.py <page.html> --tier <1-4>`
- Fix page: `python tools/bmad-v2/auto-run.py <page.html> --auto-fix`
- Batch test: `python tools/bmad-v2/auto-run.py --batch services/*.html`
- Generate report: `python tools/bmad-v2/dashboard/generate-report.py`
- **Check word count:** `node tools/count-visible-words.js locations/<page.html>`

## Notes
- Always backup before mass changes
- Test fixes on 3 pages before batch operations
- Maintain data consistency across all pages
- Use rollback if needed: `python tools/bmad-v2/utils/rollback.py <page.html>`
