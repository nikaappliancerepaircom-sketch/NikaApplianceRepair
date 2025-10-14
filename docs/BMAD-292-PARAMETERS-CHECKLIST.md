# 🎯 BMAD METHOD - 293 PARAMETERS MANDATORY CHECKLIST

## ⚠️ CRITICAL RULE: EVERY PAGE MUST PASS ALL 293 PARAMETERS BEFORE DEPLOYMENT

**Updated:** 2025-10-14 | **Version:** 3.2 (Excellence Standard) | **Total Parameters:** 293

---

## 📊 PARAMETER BREAKDOWN (293 TOTAL)

### 1️⃣ SEO OPTIMIZATION (46 parameters) - TARGET: **98+/100** ⭐

#### Content Optimization (9 parameters)
```bash
python seo-checker.py website/PAGE.html
```
- [ ] Word count: 2000-2500 words (use verify-all-location-pages.py for accurate count)
- [ ] Keyword density: 1.5-2.5%

**⚠️ CRITICAL: WORD COUNT METHODOLOGY**
```bash
# CORRECT METHOD - Count ONLY visible text content (no HTML, CSS, JS):
python verify-all-location-pages.py

# This script uses BeautifulSoup to extract ONLY visible text:
# - Auto-detects ALL .html files in locations/ folder
# - Removes <script>, <style>, <head> tags
# - Counts only user-visible words
# - Ignores HTML attributes, CSS, JavaScript code
# - Works with ANY number of location pages (10, 20, 50+)
```

**❌ WRONG METHODS - DO NOT USE:**
- `wc -w filename.html` - counts ALL words including HTML code (300-400% higher!)
- Simple text extraction without removing script/style tags
- Manual counting from HTML source
- grep/sed word counting without HTML parsing

**✅ CORRECT TOOLS:**
- `verify-all-location-pages.py` - Tests ALL location pages at once (UNIVERSAL)
- `verify_word_count.py` - Template for single page testing (uses BeautifulSoup)
- [ ] H1 tags: Exactly 1
- [ ] H2/H3 hierarchy: Proper structure (5-10 H2, 12-15 H3)
- [ ] Semantic coverage: 5+ semantic keywords
- [ ] Internal links: 10+ links total (location pages must link to 6+ service pages)
- [ ] Images: 10+ images
- [ ] Alt text: 100% coverage
- [ ] Trust signals: 4 types (warranty, rating, reviews, certifications)

**🔗 INTERNAL LINKING REQUIREMENTS:**
- **Location pages → Service pages:** Each location page MUST link to 6 service pages minimum
  - Refrigerator Repair → /services/refrigerator-repair
  - Dishwasher Repair → /services/dishwasher-repair
  - Dryer Repair → /services/dryer-repair
  - Stove Repair → /services/stove-repair
  - Oven Repair → /services/oven-repair
  - Washing Machine Repair → /services/washer-repair
- **Service pages → Location pages:** Each service page SHOULD link to 3-5 major location pages
- **Footer links:** All pages link to main service + location pages in footer
- **Link styling:** Use `color: inherit; text-decoration: none;` for seamless integration
- **Why this matters:** Internal linking passes SEO juice, improves crawlability, helps users navigate

#### Technical SEO (8 parameters)
- [ ] Title tag: 50-60 characters
- [ ] Meta description: 150-160 characters
- [ ] Schema markup: LocalBusiness, FAQPage, Service
- [ ] Mobile viewport: Configured
- [ ] HTTPS references: All secure
- [ ] JavaScript: Optimized/minified
- [ ] Critical CSS: Inline
- [ ] Clean URLs: No .html extensions in URLs (use vercel.json cleanUrls: true)

#### AI Optimization (5 parameters)
- [ ] Summary boxes: 1+ AI-friendly summary
- [ ] FAQ Schema: Structured data
- [ ] Question headers: 6+ H3 questions
- [ ] Voice search phrases: Natural language
- [ ] Lists/tables: Snippet-ready content

#### Local SEO (5 parameters)
- [ ] Location mentions: 15-40 (not oversaturated)
- [ ] LocalBusiness schema: Complete
- [ ] Phone number: 8+ mentions
- [ ] Neighborhoods: 4+ areas
- [ ] Local keywords: Service + location

#### User Experience (4 parameters)
- [ ] Font size: 16px+ (mobile), 18px+ (desktop)
- [ ] CTAs: 3+ types (call, form, chat)
- [ ] Forms: Contact/callback form present
- [ ] Navigation: Clear structure

#### 🆕 AI Search Optimization (15 parameters) - **CRITICAL FOR 2025+**
```bash
python ai-search-checker.py website/PAGE.html
```

**AI Crawler Access (5 parameters):**
- [ ] robots.txt allows GPTBot (OpenAI/ChatGPT)
- [ ] robots.txt allows Claude-Web (Anthropic)
- [ ] robots.txt allows PerplexityBot (Perplexity AI)
- [ ] robots.txt allows Google-Extended (Google Gemini)
- [ ] robots.txt allows Meta-ExternalAgent (Meta AI)

**AI Content Structure (5 parameters):**
- [ ] Direct answer in first 100 words (AI summary box)
- [ ] All H2s formatted as natural questions
- [ ] Comparison tables present (AI citation format)
- [ ] HowTo schema for technical guides
- [ ] FAQ answers in standalone format (voice-ready)

**Voice Search & Conversational (5 parameters):**
- [ ] "Near me" query variations covered
- [ ] Voice-friendly question format (conversational)
- [ ] Natural language answers (no keyword stuffing)
- [ ] Location + intent combinations (e.g., "refrigerator repair Toronto today")
- [ ] Click-to-call enabled on all phone numbers (tel: links)

**SEO + AI PASS CRITERIA: 98+/100 score (45/46 minimum), AI crawler access enabled** ⭐

---

### 2️⃣ RESPONSIVE DESIGN (80 parameters) - TARGET: **95+/100** ⭐

#### Devices to Test (10 devices × 8 checks = 80 parameters)
```bash
python test-actual-scroll.py website/PAGE.html
```

**Mobile Devices (4):**
- [ ] iPhone SE (375×667) - 8 checks
- [ ] iPhone 12 Pro (390×844) - 8 checks
- [ ] Samsung Galaxy S21 (360×800) - 8 checks
- [ ] iPhone 14 Pro Max (430×932) - 8 checks

**Tablet Devices (3):**
- [ ] iPad Mini (768×1024) - 8 checks
- [ ] iPad Air (820×1180) - 8 checks
- [ ] iPad Pro (1024×1366) - 8 checks

**Desktop Devices (3):**
- [ ] Laptop (1366×768) - 8 checks
- [ ] Desktop HD (1920×1080) - 8 checks
- [ ] Desktop 4K (2560×1440) - 8 checks

**8 Checks Per Device:**
1. Document.scrollWidth ≤ Window.innerWidth
2. No document overflow
3. Body width correct
4. No horizontal scroll
5. Touch targets ≥44px (mobile)
6. Text readable without zoom
7. Images fit viewport
8. Forms usable

**RESPONSIVE PASS CRITERIA: 95+/100 score (76/80 minimum), 0px overflow** ⭐

---

### 3️⃣ SPEED PERFORMANCE (9 parameters) - TARGET: 85+/100

```bash
python speed-checker.py website/PAGE.html
```

#### Resource Loading (4 parameters)
- [ ] CSS files: ≤3 files, combined where possible
- [ ] JavaScript files: ≤3 files, async/defer
- [ ] Images: Lazy loading, WebP format
- [ ] Fonts: ≤2 font families, preloaded

#### Optimization (5 parameters)
- [ ] CSS minification: All CSS minified
- [ ] JS minification: All JS minified
- [ ] Image compression: 80-90% quality
- [ ] Font optimization: WOFF2 format
- [ ] Resource hints: preconnect, dns-prefetch

**SPEED PASS CRITERIA: Load time <3s, 85+/100 score**

---

### 4️⃣ CROSS-BROWSER COMPATIBILITY (28 parameters) - TARGET: 4/4 BROWSERS PASS

```bash
python complete-cross-browser-tester.py website/PAGE.html
```

#### Browsers to Test (4 browsers × 7 tests = 28 parameters)
- [ ] Chrome (7 tests): Load, Layout, JavaScript, CSS, Media queries, Forms, Scroll
- [ ] Firefox (7 tests): Same as Chrome
- [ ] Safari/WebKit (7 tests): Same as Chrome
- [ ] Edge (7 tests): Same as Chrome

**CROSS-BROWSER PASS CRITERIA: 4/4 browsers fully functional**

---

### 5️⃣ VISUAL DESIGN (30 parameters) - TARGET: **95+/100** ⭐

```bash
python visual-design-checker-real.py website/PAGE.html
```

#### Layout & Spacing (8 parameters)
- [ ] No overlapping elements
- [ ] Consistent spacing (multiples of 8px)
- [ ] Proper padding/margins
- [ ] Grid alignment
- [ ] Responsive breakpoints work
- [ ] No content cutoff
- [ ] Proper aspect ratios
- [ ] White space balance

#### Typography (6 parameters)
- [ ] Font hierarchy clear (H1 > H2 > H3 > p)
- [ ] Line height: 1.5-1.8 for body text
- [ ] Letter spacing appropriate
- [ ] Font weights consistent
- [ ] Text color contrast ≥4.5:1
- [ ] Readable font sizes

#### Colors & Contrast (6 parameters)
- [ ] Brand colors consistent
- [ ] Contrast ratios WCAG compliant
- [ ] Color palette harmony
- [ ] Hover states visible
- [ ] Focus states clear
- [ ] Error states distinct

#### Images & Media (5 parameters)
- [ ] All images load correctly
- [ ] Proper image compression
- [ ] Alt text present
- [ ] Responsive images (srcset)
- [ ] Loading states/placeholders

#### Interactive Elements (5 parameters)
- [ ] Buttons have hover states
- [ ] Links distinguishable
- [ ] Forms have validation
- [ ] CTAs stand out
- [ ] Loading indicators present

**VISUAL PASS CRITERIA: 95+/100 score (29/30 minimum), no critical issues** ⭐

---

### 6️⃣ ACCESSIBILITY (15 parameters) - TARGET: WCAG 2.1 AA COMPLIANT

#### Keyboard Navigation (4 parameters)
- [ ] All interactive elements reachable via Tab
- [ ] Focus indicators visible
- [ ] Logical tab order
- [ ] Skip navigation link present

#### Screen Reader Support (4 parameters)
- [ ] All images have alt text
- [ ] ARIA labels where needed
- [ ] Semantic HTML used
- [ ] Form labels associated

#### Color & Contrast (3 parameters)
- [ ] Text contrast ≥4.5:1
- [ ] Large text contrast ≥3:1
- [ ] Color not sole indicator

#### Content Accessibility (4 parameters)
- [ ] Headings in logical order
- [ ] Links descriptive
- [ ] Language declared
- [ ] Error messages clear

**ACCESSIBILITY PASS CRITERIA: No critical violations, WCAG AA compliant**

---

### 🆕 7️⃣ CONTENT QUALITY (15 parameters) - TARGET: **98+/100** ⭐

```bash
python content-quality-checker.py website/PAGE.html
```

**⚠️ CRITICAL: Content Quality must be 98%+ (14.5/15 minimum)**

**WHY 98% MINIMUM:**
- Content uniqueness = competitive advantage
- AI search visibility depends on quality
- Google E-E-A-T scoring requires excellence
- Users trust high-quality content more
- Conversion rates directly tied to content quality

#### Uniqueness & Value (5 parameters) - **MUST BE 5/5** ✅
- [ ] Content originality: **100% unique content** (CRITICAL - not copied from competitors)
- [ ] Expertise demonstration: Shows real expertise (technical details, experience)
- [ ] User value: Solves real user problems (how to fix, what to do)
- [ ] Fresh information: Current information (2025 prices, new models)
- [ ] Depth of coverage: Deep topic coverage (not superficial)

**⚠️ Content originality is NON-NEGOTIABLE - must be 100% unique**

**🚨 CRITICAL RULE FOR LOCATION PAGES:**
- **Each location page MUST have 100% unique content**
- **NO duplicate content across location pages** (Google penalty)
- **Write content manually, quality over speed**
- **Research each location before writing** (neighborhoods, demographics, local issues)
- **Include location-specific details** (known areas, local landmarks, climate issues)
- **Unique FAQs for each location** (3-5 location-specific questions)
- **Do NOT rush** - take time to write quality content
- **Tokens are NOT important** - quality is everything

**WHY THIS MATTERS:**
- Google penalizes duplicate content severely (-50% to -90% ranking)
- Users can tell generic vs location-specific content
- Conversion rates 3x higher with localized content
- AI search engines (ChatGPT, Perplexity) prefer unique local content
- Competitors with generic location pages = easy to beat

**MINIMUM UNIQUE CONTENT PER LOCATION PAGE:**
- Hero section: 100% unique (mention local neighborhoods)
- Services: 70% unique (adapt to local needs/issues)
- Common Problems: 80% unique (climate-specific, building age issues)
- FAQ: 100% unique (5+ local questions)
- Testimonials: Can reuse, but add local customer references
- Overall page uniqueness: 75%+ unique content minimum

#### Readability & Structure (5 parameters) - **MUST BE 4.5/5+**
- [ ] Reading level: Grade 8-10 (understandable to average person)
- [ ] Sentence length: Average 15-20 words
- [ ] Paragraph length: 3-5 sentences maximum
- [ ] Bullet points/lists: 3+ lists on page (easy to scan)
- [ ] Content hierarchy: Logical information flow (general to specific)

#### Content Structure (5 parameters) - **MUST BE 4.5/5+**
- [ ] Sections count: 7-12 sections optimal
- [ ] Required sections present: Hero, Services, FAQ, Contact, Social Proof
- [ ] Each section has H2: 100% sections with headings
- [ ] Section length balance: No more than 500 words per section
- [ ] Visual breaks: Images/icons between text blocks

**CONTENT QUALITY PASS CRITERIA: 98+/100 score (14.5/15 minimum) ⭐**

**FAIL IF:**
- Content originality < 100%
- Overall score < 98%
- Copied content from competitors found

---

### 🆕 8️⃣ CONVERSION RATE OPTIMIZATION (20 parameters) - TARGET: **95+/100** ⭐

```bash
python cro-checker.py website/PAGE.html
```

#### Above The Fold (5 parameters)
- [ ] Clear value proposition: Understand offer in first 3 seconds
- [ ] Primary CTA visible: "Call" button visible without scrolling
- [ ] Phone number prominent: Phone in header + hero (minimum 2 places)
- [ ] Trust signal immediate: Warranty/rating/reviews visible immediately
- [ ] Hero image/video: Visual proof of service (technician, van, work)

#### Call-to-Actions (CTAs) (5 parameters)
- [ ] CTA count: 5-8 CTAs on page (each section has action)
- [ ] CTA types diversity: Minimum 3 types (call, form, chat/whatsapp)
- [ ] CTA copy action-oriented: "Call Now", "Get Quote", "Book Today" (not "Learn More")
- [ ] CTA color contrast: Buttons contrast well (stand out from background)
- [ ] Mobile CTA sticky: On mobile sticky "Call Now" button at bottom

#### Forms Optimization (5 parameters)
- [ ] Form fields minimal: 3-5 fields maximum (name, phone, appliance, problem)
- [ ] Form above fold: At least one form visible without scrolling
- [ ] Form validation clear: Real-time validation with clear messages
- [ ] Submit button prominent: Submit button bright, large
- [ ] Privacy assurance: "We don't spam" / "Your data is secure" near form

#### Friction Reduction (5 parameters)
- [ ] No popups on entry: No popups when page loads
- [ ] Click-to-call direct: Phone with href="tel:" (direct call)
- [ ] No registration required: Don't require registration to contact
- [ ] Loading speed fast: <3 seconds load (otherwise 50% leave)
- [ ] Navigation simple: Maximum 5-7 menu items

**CRO PASS CRITERIA: 95+/100 score (19/20 minimum), 5+ conversion points** ⭐

---

### 🆕 9️⃣ PSYCHOLOGICAL TRIGGERS (25 parameters) - TARGET: **98+/100** ⭐

```bash
python psychology-checker.py website/PAGE.html
```

#### Pain-Solve Framework (5 parameters)
- [ ] Pain points identified: 3+ specific problems mentioned ("fridge not cooling", "water leaking")
- [ ] Emotional pain amplified: Describe consequences ("food spoiling", "kitchen flooding")
- [ ] Solution immediate: Show we can solve TODAY
- [ ] Before/After contrast: "From broken to fixed in 2 hours"
- [ ] Problem → Solution structure: Each problem = solution

#### AIDA Framework (5 parameters)
- [ ] **Attention**: Headline hooks (statistic, question, promise)
- [ ] **Interest**: First paragraph intrigues (how we do it)
- [ ] **Desire**: Benefits > Features (not "we use OEM parts", but "your appliance lasts 5+ years")
- [ ] **Action**: Multiple CTAs (each section = call to action)
- [ ] AIDA flow present: Page follows this structure top to bottom

#### Social Proof (5 parameters)
- [ ] Reviews/testimonials: 3+ real reviews with names
- [ ] Rating visible: 4.9★ or higher, shown minimum 2 places
- [ ] Review count: "127 reviews" (specific number)
- [ ] Customer photos: Real customer/work photos (not stock images)
- [ ] Case studies: 1+ story "how we saved the situation"

#### Scarcity & Urgency (5 parameters)
- [ ] Time urgency: "Same-day service" / "Call before noon"
- [ ] Limited availability: "Only 3 slots left today" (IF TRUE)
- [ ] Seasonal urgency: "Don't wait until summer rush"
- [ ] Emergency framing: "24/7 emergency service available"
- [ ] No false scarcity: ALL urgency triggers = TRUTH (no fake timers)

#### Authority & Trust (5 parameters)
- [ ] Credentials displayed: "Licensed", "Insured" (with numbers if available)
- [ ] Years in business: "Since 2015" (specific date)
- [ ] Completion stats: "5000+ repairs completed" (real number)
- [ ] Certifications visible: BBB, local business certifications (NO manufacturer claims)
- [ ] Guarantee prominent: "90-day warranty" mentioned 3+ times

**⚠️ CRITICAL: NO FALSE CLAIMS**
- ❌ NO "Factory-authorized", "Factory-certified", "Manufacturer-approved"
- ❌ NO "Official service center" or similar manufacturer claims
- ❌ NO brand partnerships unless you have written agreements
- ✅ YES: "We repair [brand]", "Experienced with [brand]", "We service [brand]"

**🚨 CRITICAL: ONLY REPAIR 6 MAJOR APPLIANCES**
We ONLY repair these 6 appliances - NEVER mention others:
- ✅ Refrigerator (fridge, freezer)
- ✅ Dishwasher
- ✅ Dryer
- ✅ Stove (cooktop, range, gas/electric)
- ✅ Oven (wall oven, range oven)
- ✅ Washing Machine (washer, laundry machine)

**❌ DO NOT MENTION - WE DO NOT SERVICE:**
- ❌ Rice cookers, pressure cookers, slow cookers
- ❌ Microwaves
- ❌ Range hoods, ventilation fans
- ❌ Wine fridges, beverage centers, kegerators
- ❌ Espresso machines, coffee makers
- ❌ Ice makers (standalone)
- ❌ Trash compactors
- ❌ Garbage disposals
- ❌ Water heaters
- ❌ HVAC (air conditioning, heating, furnaces)
- ❌ Any small appliances
- ❌ Any specialty cooking equipment (wok ranges, steamers, etc.)
- ❌ **COMMERCIAL APPLIANCES** - We ONLY service residential appliances

**🚨 NO COMMERCIAL APPLIANCES:**
- ❌ NO commercial refrigerators, freezers, walk-ins
- ❌ NO commercial ovens, ranges, convection ovens
- ❌ NO commercial dishwashers
- ❌ NO restaurant equipment
- ❌ NO industrial laundry machines
- ❌ NO any commercial-grade appliances
- ✅ YES: ONLY residential home appliances

**🚨 NO LUXURY BRANDS EMPHASIS:**
- ❌ DO NOT emphasize luxury brands (Sub-Zero, Wolf, Miele, Thermador, Gaggenau)
- ❌ DO NOT mention "luxury appliance specialists" or "certified for ultra-luxury"
- ❌ DO NOT claim "factory-certified" for ANY brand (we don't have certifications)
- ❌ DO NOT claim "manufacturer-certified" or "authorized service center"
- ❌ Parts for luxury brands are difficult to source
- ✅ YES: **STRONG EMPHASIS on standard residential brands** (Samsung, LG, Whirlpool, GE, Bosch, KitchenAid, Maytag, Frigidaire)
- ✅ YES: Can mention we service luxury brands, but NO special emphasis
- ✅ YES: Lead with Samsung, LG, Whirlpool, GE in all brand lists

**🚨 NO DISPOSAL/REMOVAL SERVICES:**
- ❌ DO NOT mention appliance disposal service
- ❌ DO NOT mention appliance removal service
- ❌ DO NOT mention recycling services
- ❌ DO NOT mention eco-certified disposal
- ❌ We do NOT provide haul-away or disposal services
- ✅ YES: We ONLY repair existing appliances

**🚨 NO COMMERCIAL SERVICES:**
- ❌ DO NOT service high-BTU commercial ranges (this is commercial equipment)
- ❌ DO NOT mention commercial-grade stoves or ranges
- ❌ DO NOT mention restaurant-style cooking equipment
- ❌ High-BTU ranges = commercial service, we don't do this
- ✅ YES: Standard residential ranges only (up to 18,000 BTU max)

**🚨 NO REFRIGERANT SERVICES:**
- ❌ DO NOT mention refrigerant recovery service
- ❌ DO NOT mention refrigerant refill/recharge service
- ❌ DO NOT mention Freon service
- ❌ We do NOT handle refrigerant (requires EPA certification)
- ✅ YES: We diagnose cooling issues, but refer refrigerant work to specialists

**🚨 ARRIVAL TIME - BE FLEXIBLE:**
- ❌ DO NOT promise exact times like "30-45 minutes"
- ❌ DO NOT promise "same-day" if not guaranteed
- ❌ Sometimes service is next day, not same day
- ✅ YES: "Fast response time" or "Quick service"
- ✅ YES: "Same-day service available" (not guaranteed)
- ✅ YES: "We'll arrive as soon as possible"

**🎯 TARGET AUDIENCE: RESIDENTIAL HOMEOWNERS**
- ✅ **STRONG FOCUS** on everyday residential homeowners
- ✅ **EMPHASIS** on standard appliances in typical homes
- ✅ Affordable, reliable repair service
- ✅ NOT targeting luxury/high-end market
- ✅ Middle-class families, average homes
- ✅ Lead with Samsung, LG, Whirlpool, GE (most common brands)

**WHY THIS MATTERS:**
- Promising services we don't provide = legal liability
- Customer disappointment = negative reviews
- Wasted service calls = lost revenue
- False advertising = potential lawsuits
- Luxury parts = hard to source, delays, customer frustration

**PSYCHOLOGY PASS CRITERIA: 98+/100 score (24.5/25 minimum), all triggers ethical & truthful** ⭐

---

### 🆕 🔟 DATA CONSISTENCY (15 parameters) - TARGET: 100% MATCH

```bash
python data-consistency-checker.py website/PAGE.html
```

#### Global Numbers Validation (10 parameters)
- [ ] Phone number consistent: SAME number everywhere (header, footer, hero, contact)
- [ ] Warranty period consistent: If "90-day" → everywhere 90-day (not "3 month" elsewhere)
- [ ] Service areas consistent: Same list of areas (not "Toronto, Mississauga" here and "GTA" there)
- [ ] Pricing consistent: Diagnostic fee everywhere $119 (not $99 in one place)
- [ ] Years in business consistent: "Since 2015" everywhere (not "10 years" and "9 years" in different places)
- [ ] Review count consistent: "127 reviews" same everywhere
- [ ] Rating consistent: 4.9★ everywhere (not 4.8★ elsewhere)
- [ ] Service hours consistent: "8 AM - 8 PM" same everywhere
- [ ] Response time consistent: "Same-day" everywhere (not "2-hour" elsewhere)
- [ ] Brand count consistent: "All major brands" or "6 brands" - same everywhere

#### Factual Accuracy (5 parameters)
- [ ] No fake statistics: All numbers real (not "95% satisfaction" if not measured)
- [ ] No stock photos passed as real: Don't use stock images as "our customers"
- [ ] No fake urgency: No countdown timers if not real deadline
- [ ] No false claims: Not "fastest" or "#1" without proof
- [ ] Verifiable claims: All statements can be verified

**⚠️ CRITICAL: DATA CONSISTENCY = 100% OR FAIL. No exceptions.**

**DATA CONSISTENCY PASS CRITERIA: 100% match across all numbers, 0 discrepancies**

---

### 🆕 1️⃣1️⃣ CONVERSION DESIGN (10 parameters) - TARGET: **98+/100** ⭐

```bash
python conversion-design-checker.py website/PAGE.html
```

#### Visual Hierarchy for Conversion (5 parameters)
- [ ] F-pattern layout: Important info top-left (how eyes read)
- [ ] Visual flow to CTA: Eye directed to buttons (arrows, colors, whitespace)
- [ ] Color psychology: Green/blue for trust, red/orange for action
- [ ] White space generous: Not cluttered (breathable design)
- [ ] Icons meaningful: Icons help understand meaning (not decoration)

#### Mobile Conversion Optimization (5 parameters)
- [ ] Mobile CTA thumb-friendly: Buttons 44px+ height, in thumb zone
- [ ] Mobile forms simplified: Minimum fields on mobile
- [ ] Mobile number one-tap: Click-to-call works
- [ ] Mobile images fast: Lazy loading + compressed
- [ ] Mobile menu accessible: Hamburger menu obvious, working

**CONVERSION DESIGN PASS CRITERIA: 98+/100 score (9.8/10 minimum)** ⭐

---

## 📊 COMPLETE PARAMETER SUMMARY

```
┌────────────────────────────────────────────────────────┐
│  BMAD METHOD - 293 TOTAL PARAMETERS (v3.2)            │
├────────────────────────────────────────────────────────┤
│  1.  SEO + AI Optimization:   46 params → 98+/100  ⭐│
│  2.  Responsive Design:       80 params → 95+/100  ⭐│
│  3.  Speed Performance:        9 params → 85+/100     │
│  4.  Cross-Browser:           28 params → 4/4         │
│  5.  Visual Design:           30 params → 95+/100  ⭐│
│  6.  Accessibility:           15 params → WCAG AA     │
│  7.  Content Quality:         15 params → 98+/100  ⭐│
│  8.  CRO (Conversion):        20 params → 95+/100  ⭐│
│  9.  Psychology:              25 params → 98+/100  ⭐│
│  10. Data Consistency:        15 params → 100%     ⭐│
│  11. Conversion Design:       10 params → 98+/100  ⭐│
├────────────────────────────────────────────────────────┤
│  TOTAL:                      293 PARAMETERS        🚀 │
│  NEW STANDARDS (v3.2):       8 categories at 95-98%  │
│  CRITICAL GATES:             7 categories (marked ⭐) │
│  DEPLOYMENT GATE:            ALL CATEGORIES PASS      │
│  EXCELLENCE STANDARD:        Near-perfect execution   │
└────────────────────────────────────────────────────────┘
```

---

## 🚨 CRITICAL DEPLOYMENT GATES (v3.2 - EXCELLENCE STANDARD)

### Gate 1-6: Technical Foundation (208 params)
```
✅ SEO + AI: 98+/100 (45/46 minimum) ⭐ CRITICAL - RAISED FROM 85%
✅ Responsive: 95+/100 (76/80 minimum) ⭐ CRITICAL - RAISED FROM 85%
✅ Speed: 85+/100
✅ Cross-Browser: 4/4 browsers
✅ Visual: 95+/100 (29/30 minimum) ⭐ CRITICAL - RAISED FROM 85%
✅ Accessibility: WCAG AA
```

### Gate 7-11: Conversion & Trust (85 params)
```
✅ Content Quality: 98+/100 (14.5/15 minimum) ⭐ CRITICAL
✅ CRO: 95+/100 (19/20 minimum) ⭐ CRITICAL - RAISED FROM 85%
✅ Psychology: 98+/100 (24.5/25 minimum) ⭐ CRITICAL - RAISED FROM 85%
✅ Data Consistency: 100% (15/15) ⭐ CRITICAL
✅ Conversion Design: 98+/100 (9.8/10 minimum) ⭐ CRITICAL - RAISED FROM 85%
```

**⚠️ ALL 11 GATES MUST PASS BEFORE DEPLOYMENT**

**🚨 NEW v3.2 STANDARDS:**
- **7 CRITICAL categories** require 95-98% (near-perfection)
- Only 4 categories remain at 85% threshold (Speed, Cross-Browser, Accessibility, old baseline)
- This raises the bar to EXCELLENCE level - only best-in-class pages will pass

---

## 🔥 MANDATORY TESTING WORKFLOW

### Complete Test Suite
```bash
# Run all 11 category tests
python bmad-complete-test.py website/PAGE.html

# Or run individually:
python seo-checker.py website/PAGE.html                   # 30 params (traditional SEO)
python ai-search-checker.py website/PAGE.html             # 15 params (AI Search) 🆕
python test-actual-scroll.py website/PAGE.html            # 80 params
python speed-checker.py website/PAGE.html                 # 9 params
python complete-cross-browser-tester.py website/PAGE.html # 28 params
python visual-design-checker-real.py website/PAGE.html    # 30 params
# (Accessibility manual check)                            # 15 params
python content-quality-checker.py website/PAGE.html       # 15 params
python cro-checker.py website/PAGE.html                   # 20 params
python psychology-checker.py website/PAGE.html            # 25 params
python data-consistency-checker.py website/PAGE.html      # 15 params - CRITICAL!
python conversion-design-checker.py website/PAGE.html     # 10 params
```

### If Any Test Fails (<85/100 or FAIL):
1. Identify EVERY failing parameter
2. Fix ONE parameter at a time
3. Retest immediately
4. Document the fix
5. Move to next parameter
6. Repeat until ALL categories 85+/100

**NO DEPLOYMENT until all 292 parameters pass!**

---

## 💡 TIPS FOR AI AGENTS

1. **Always check this file FIRST** before starting page work
2. **AI Search is NOW CRITICAL** - 50%+ traffic will come from AI by 2026 🆕
3. **Data Consistency is CRITICAL** - even 1 mismatch = FAIL entire page
4. **Psychology triggers must be TRUE** - no fake urgency or false claims
5. **Test after EVERY change** - don't batch fixes
6. **Document all numbers** - maintain global consistency sheet
7. **CRO before prettiness** - conversion > visual appeal
8. **Mobile-first testing** - most traffic is mobile
9. **Test in ChatGPT/Perplexity weekly** - monitor AI visibility 🆕

---

## 📄 Related Documentation

- [BMAD-METHOD-COMPLETE.md](BMAD-METHOD-COMPLETE.md) - Full methodology
- [AI-SEARCH-DOMINATION-2025-2030.md](AI-SEARCH-DOMINATION-2025-2030.md) - AI Search Strategy 🆕
- [SEO-AI-OPTIMIZATION.md](SEO-AI-OPTIMIZATION.md) - AI & E-E-A-T Optimization
- [AI-VISIBILITY-AUDIT.md](AI-VISIBILITY-AUDIT.md) - 90-Day AI Strategy
- [README-FOR-AI-AGENTS.md](README-FOR-AI-AGENTS.md) - AI agent onboarding
- [BMAD-CONTENT-QUALITY-GUIDE.md](BMAD-CONTENT-QUALITY-GUIDE.md) - Content best practices
- [BMAD-CRO-GUIDE.md](BMAD-CRO-GUIDE.md) - Conversion optimization
- [BMAD-PSYCHOLOGY-GUIDE.md](BMAD-PSYCHOLOGY-GUIDE.md) - Psychological triggers
- [BMAD-DATA-CONSISTENCY-GUIDE.md](BMAD-DATA-CONSISTENCY-GUIDE.md) - Numbers validation

---

**Last Updated:** 2025-10-14
**Version:** 3.2 (Excellence Standard Update + Clean URLs)
**Total Parameters:** 293
**Status:** Production Ready ✅
**Key Changes (v3.2):**
- **RAISED STANDARDS:** 7 categories now require 95-98% (near-perfection)
- SEO + AI: 85% → 98% ⭐ (46 params, added clean URLs requirement)
- Responsive Design: 85% → 95% ⭐
- Visual Design: 85% → 95% ⭐
- CRO: 85% → 95% ⭐
- Psychology: 85% → 98% ⭐
- Conversion Design: 85% → 98% ⭐
- Content Quality: 98% (maintained) ⭐
- Data Consistency: 100% (maintained) ⭐
- **Excellence Standard:** Only best-in-class pages will pass all gates
- **Clean URLs:** All URLs must be without .html extension (vercel.json cleanUrls: true)
