# 🎯 BMAD METHOD - 277 PARAMETERS MANDATORY CHECKLIST

## ⚠️ CRITICAL RULE: EVERY PAGE MUST PASS ALL 277 PARAMETERS BEFORE DEPLOYMENT

**Updated:** 2025-10-01 | **Version:** 2.0 | **Total Parameters:** 277

---

## 📊 PARAMETER BREAKDOWN (277 TOTAL)

### 1️⃣ SEO OPTIMIZATION (30 parameters) - TARGET: 85+/100

#### Content Optimization (9 parameters)
```bash
python seo-checker.py website/PAGE.html
```
- [ ] Word count: 1500-2500 words
- [ ] Keyword density: 1.5-2.5%
- [ ] H1 tags: Exactly 1
- [ ] H2/H3 hierarchy: Proper structure (5-10 H2, 12-15 H3)
- [ ] Semantic coverage: 5+ semantic keywords
- [ ] Internal links: 10+ links
- [ ] Images: 10+ images
- [ ] Alt text: 100% coverage
- [ ] Trust signals: 4 types (warranty, rating, reviews, certifications)

#### Technical SEO (7 parameters)
- [ ] Title tag: 50-60 characters
- [ ] Meta description: 150-160 characters
- [ ] Schema markup: LocalBusiness, FAQPage, Service
- [ ] Mobile viewport: Configured
- [ ] HTTPS references: All secure
- [ ] JavaScript: Optimized/minified
- [ ] Critical CSS: Inline

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

**SEO PASS CRITERIA: 85+/100 score**

---

### 2️⃣ RESPONSIVE DESIGN (80 parameters) - TARGET: 10/10 DEVICES PASS

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

**RESPONSIVE PASS CRITERIA: 10/10 devices with 0px overflow**

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

### 5️⃣ VISUAL DESIGN (30 parameters) - TARGET: 85+/100

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

**VISUAL PASS CRITERIA: 85+/100 score, no critical issues**

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

### 🆕 7️⃣ CONTENT QUALITY (15 parameters) - TARGET: 85+/100

```bash
python content-quality-checker.py website/PAGE.html
```

#### Uniqueness & Value (5 parameters)
- [ ] Content originality: 100% unique content (not copied from competitors)
- [ ] Expertise demonstration: Shows real expertise (technical details, experience)
- [ ] User value: Solves real user problems (how to fix, what to do)
- [ ] Fresh information: Current information (2025 prices, new models)
- [ ] Depth of coverage: Deep topic coverage (not superficial)

#### Readability & Structure (5 parameters)
- [ ] Reading level: Grade 8-10 (understandable to average person)
- [ ] Sentence length: Average 15-20 words
- [ ] Paragraph length: 3-5 sentences maximum
- [ ] Bullet points/lists: 3+ lists on page (easy to scan)
- [ ] Content hierarchy: Logical information flow (general to specific)

#### Content Structure (5 parameters)
- [ ] Sections count: 7-12 sections optimal
- [ ] Required sections present: Hero, Services, FAQ, Contact, Social Proof
- [ ] Each section has H2: 100% sections with headings
- [ ] Section length balance: No more than 500 words per section
- [ ] Visual breaks: Images/icons between text blocks

**CONTENT QUALITY PASS CRITERIA: 85+/100 score**

---

### 🆕 8️⃣ CONVERSION RATE OPTIMIZATION (20 parameters) - TARGET: 85+/100

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

**CRO PASS CRITERIA: 85+/100 score, 5+ conversion points**

---

### 🆕 9️⃣ PSYCHOLOGICAL TRIGGERS (25 parameters) - TARGET: 85+/100

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
- [ ] Credentials displayed: "Licensed", "Insured", "Certified" (with numbers if available)
- [ ] Years in business: "Since 2015" (specific date)
- [ ] Completion stats: "5000+ repairs completed" (real number)
- [ ] Certifications visible: BBB, manufacturer certifications
- [ ] Guarantee prominent: "90-day warranty" mentioned 3+ times

**PSYCHOLOGY PASS CRITERIA: 85+/100 score, all triggers ethical & truthful**

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

### 🆕 1️⃣1️⃣ CONVERSION DESIGN (10 parameters) - TARGET: 85+/100

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

**CONVERSION DESIGN PASS CRITERIA: 85+/100 score**

---

## 📊 COMPLETE PARAMETER SUMMARY

```
┌────────────────────────────────────────────────────────┐
│  BMAD METHOD - 277 TOTAL PARAMETERS                    │
├────────────────────────────────────────────────────────┤
│  1.  SEO Optimization:        30 params → 85+/100     │
│  2.  Responsive Design:       80 params → 10/10       │
│  3.  Speed Performance:        9 params → 85+/100     │
│  4.  Cross-Browser:           28 params → 4/4         │
│  5.  Visual Design:           30 params → 85+/100     │
│  6.  Accessibility:           15 params → WCAG AA     │
│  7.  Content Quality:         15 params → 85+/100     │
│  8.  CRO (Conversion):        20 params → 85+/100     │
│  9.  Psychology:              25 params → 85+/100     │
│  10. Data Consistency:        15 params → 100%        │
│  11. Conversion Design:       10 params → 85+/100     │
├────────────────────────────────────────────────────────┤
│  TOTAL:                      277 PARAMETERS           │
│  TARGET:                     85+/100 on ALL           │
│  DEPLOYMENT GATE:            ALL CATEGORIES PASS      │
└────────────────────────────────────────────────────────┘
```

---

## 🚨 CRITICAL DEPLOYMENT GATES

### Gate 1-6: Technical Foundation (192 params)
```
✅ SEO: 85+/100
✅ Responsive: 10/10 devices
✅ Speed: 85+/100
✅ Cross-Browser: 4/4 browsers
✅ Visual: 85+/100
✅ Accessibility: WCAG AA
```

### Gate 7-11: Conversion & Trust (85 params)
```
✅ Content Quality: 85+/100
✅ CRO: 85+/100
✅ Psychology: 85+/100
✅ Data Consistency: 100% (CRITICAL!)
✅ Conversion Design: 85+/100
```

**⚠️ ALL 11 GATES MUST PASS BEFORE DEPLOYMENT**

---

## 🔥 MANDATORY TESTING WORKFLOW

### Complete Test Suite
```bash
# Run all 11 category tests
python bmad-complete-test.py website/PAGE.html

# Or run individually:
python seo-checker.py website/PAGE.html                   # 30 params
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

**NO DEPLOYMENT until all 277 parameters pass!**

---

## 💡 TIPS FOR AI AGENTS

1. **Always check this file FIRST** before starting page work
2. **Data Consistency is CRITICAL** - even 1 mismatch = FAIL entire page
3. **Psychology triggers must be TRUE** - no fake urgency or false claims
4. **Test after EVERY change** - don't batch fixes
5. **Document all numbers** - maintain global consistency sheet
6. **CRO before prettiness** - conversion > visual appeal
7. **Mobile-first testing** - most traffic is mobile

---

## 📄 Related Documentation

- [BMAD-METHOD-COMPLETE.md](BMAD-METHOD-COMPLETE.md) - Full methodology
- [README-FOR-AI-AGENTS.md](README-FOR-AI-AGENTS.md) - AI agent onboarding
- [BMAD-CONTENT-QUALITY-GUIDE.md](BMAD-CONTENT-QUALITY-GUIDE.md) - Content best practices
- [BMAD-CRO-GUIDE.md](BMAD-CRO-GUIDE.md) - Conversion optimization
- [BMAD-PSYCHOLOGY-GUIDE.md](BMAD-PSYCHOLOGY-GUIDE.md) - Psychological triggers
- [BMAD-DATA-CONSISTENCY-GUIDE.md](BMAD-DATA-CONSISTENCY-GUIDE.md) - Numbers validation

---

**Last Updated:** 2025-10-01
**Version:** 2.0
**Total Parameters:** 277
**Status:** Production Ready ✅
