# BMAD v2 - COMPLETE OPTIMIZATION METHOD
## Єдина система тестування та оптимізації по 277+ параметрам

**Version:** 2.0
**Date:** 2025-10-12
**Status:** Production Ready

---

## 📋 TABLE OF CONTENTS

1. [Method Overview](#method-overview)
2. [Tier Structure](#tier-structure)
3. [Tier 1: Critical Foundation](#tier-1-critical-foundation)
4. [Tier 2: SEO + CRO Core](#tier-2-seo--cro-core)
5. [Tier 3: Content + Basic UX](#tier-3-content--basic-ux)
6. [Tier 4: Performance + Speed](#tier-4-performance--speed)
7. [Tier 5: Cross-Browser + Responsive](#tier-5-cross-browser--responsive)
8. [Tier 6: Advanced UX + Features](#tier-6-advanced-ux--features)
9. [Tier 7: Analytics + Tracking](#tier-7-analytics--tracking)
10. [Tier 8: Content Features](#tier-8-content-features)
11. [Tier 9: Integrations + Polish](#tier-9-integrations--polish)
12. [Agent-Based Testing System](#agent-based-testing-system)
13. [Optimization Workflow](#optimization-workflow)
14. [Deployment Gates](#deployment-gates)

---

## 🎯 METHOD OVERVIEW

### What is BMAD v2?

**BMAD (Best Method for Appliance Documentation)** - це комплексна система оптимізації веб-сторінок по 277 параметрам, розділених на 9 рівнів (Tiers) за критичністю.

### Core Principles:

1. **Tier-based prioritization** - не все одразу, а поступово
2. **Automation first** - 60%+ параметрів фіксяться скриптами/агентами
3. **Quality gates** - чіткі критерії для deployment
4. **Agent-driven testing** - використання AI агентів для складних перевірок
5. **Data-driven decisions** - metrics та scores для кожного tier

### Key Metrics:

- **Total parameters:** 277
- **Auto-fixable:** ~165 (60%)
- **Manual optimization:** ~112 (40%)
- **Deployment blockers:** Tier 1 only (15 params)
- **Recommended for production:** Tier 1-4 (120 params)

---

## 📊 TIER STRUCTURE

```
┌────────────────────────────────────────────────────────────────┐
│                      BMAD v2 TIER PYRAMID                      │
└────────────────────────────────────────────────────────────────┘

                         ┌─────────┐
                         │ Tier 9  │ Integrations (29) - 40%
                    ┌────┴─────────┴────┐
                    │      Tier 8        │ Content Features (30) - 50%
               ┌────┴────────────────────┴────┐
               │         Tier 7               │ Analytics (28) - 70%
          ┌────┴──────────────────────────────┴────┐
          │            Tier 6                      │ Advanced UX (35) - 60%
     ┌────┴────────────────────────────────────────┴────┐
     │               Tier 5                             │ Cross-Browser (30) - 70%
┌────┴──────────────────────────────────────────────────┴────┐
│                   Tier 4                                    │ Performance (25) - 80%
├─────────────────────────────────────────────────────────────┤
│                   Tier 3                                    │ Content+UX (50) - 70%
├─────────────────────────────────────────────────────────────┤
│                   Tier 2                                    │ SEO+CRO (30) - 85%
├─────────────────────────────────────────────────────────────┤
│                   Tier 1                                    │ Critical (15) - 100%
└─────────────────────────────────────────────────────────────┘
       🔴 BLOCKS DEPLOYMENT         ⚠️ WARNING         ✅ RECOMMENDED
```

### Tier Summary Table:

| Tier | Name | Params | Target | Auto-fix | Blocks Deploy | Time |
|------|------|--------|--------|----------|---------------|------|
| **1** | Critical Foundation | 15 | 100% | 100% | 🔴 YES | 2 min |
| **2** | SEO + CRO Core | 30 | 85% | 75% | ⚠️ Warn | 5 min |
| **3** | Content + Basic UX | 50 | 70% | 40% | ❌ No | 5 hrs |
| **4** | Performance + Speed | 25 | 80% | 60% | ❌ No | 2 hrs |
| **5** | Cross-Browser | 30 | 70% | 20% | ❌ No | 3 hrs |
| **6** | Advanced UX | 35 | 60% | 30% | ❌ No | 4 hrs |
| **7** | Analytics + Tracking | 28 | 70% | 80% | ❌ No | 1 hr |
| **8** | Content Features | 30 | 50% | 10% | ❌ No | varies |
| **9** | Integrations + Polish | 34 | 40% | 40% | ❌ No | varies |
| **TOTAL** | | **277** | | **60%** | | **~20 hrs** |

---

## 🔴 TIER 1: CRITICAL FOUNDATION (15 параметрів)

### 🎯 Target: 100% (BLOCKS DEPLOYMENT IF FAIL)

### Category: Data Consistency (8 params)

**CRITICAL: 0 discrepancies allowed**

1. **Phone number consistency**
   - Value: 437-747-6737
   - Check: SAME number everywhere (header, footer, body, schema)
   - Auto-fix: ✅ Normalize to single format
   - Agent: `data-consistency-agent`

2. **Business hours consistency**
   - Value: Mon-Fri 8-20, Sat 9-18, Sun 10-17 (or 24/7)
   - Check: SAME hours everywhere
   - Auto-fix: ✅ Normalize to config value
   - Agent: `data-consistency-agent`

3. **Warranty period consistency**
   - Value: 90-day
   - Check: "90-day" everywhere (not "3-month" or "90 days")
   - Auto-fix: ✅ Replace variations
   - Agent: `data-consistency-agent`

4. **Rating consistency**
   - Value: 4.9
   - Check: 4.9/5 or 4.9★ everywhere (not 4.8 or 5.0)
   - Auto-fix: ✅ Normalize to config
   - Agent: `data-consistency-agent`

5. **Review count consistency**
   - Value: 5,200+
   - Check: "5,200+" everywhere (not "5000" or "5200")
   - Auto-fix: ✅ Normalize format
   - Agent: `data-consistency-agent`

6. **Years in business consistency**
   - Value: Since 2019 = 6+ years (2025)
   - Check: Math correct everywhere
   - Auto-fix: ✅ Calculate from founding year
   - Agent: `data-consistency-agent`

7. **Address consistency**
   - Value: 60 Walter Tunny Cresent, East Gwillimbury, ON L9N 0R3
   - Check: Exact same everywhere
   - Auto-fix: ✅ Normalize
   - Agent: `data-consistency-agent`

8. **Email consistency**
   - Value: care@niappliancerepair.ca
   - Check: Same email everywhere
   - Auto-fix: ✅ Normalize
   - Agent: `data-consistency-agent`

### Category: Core Technical (7 params)

9. **LocalBusiness schema present**
   - Required: Valid JSON-LD schema in <head>
   - Auto-fix: ✅ Generate and inject
   - Agent: `schema-agent`

10. **AggregateRating schema present**
    - Required: Inside LocalBusiness schema
    - Auto-fix: ✅ Generate and inject
    - Agent: `schema-agent`

11. **Mobile viewport meta tag**
    - Required: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
    - Auto-fix: ✅ Add if missing
    - Agent: `technical-agent`

12. **Single H1 tag**
    - Required: EXACTLY 1 H1 per page
    - Auto-fix: ✅ Convert extra H1s to H2
    - Agent: `technical-agent`

13. **Valid HTML structure**
    - Required: No critical errors (unclosed tags, invalid nesting)
    - Auto-fix: ⚠️ Report only (manual fix)
    - Agent: `html-validator-agent`

14. **HTTPS/SSL enabled**
    - Required: All links https://, no http://
    - Auto-fix: ✅ Replace http:// → https://
    - Agent: `security-agent`

15. **Phone visible in header/hero**
    - Required: Phone number above fold
    - Auto-fix: ⚠️ Check only (manual placement)
    - Agent: `visibility-agent`

### Testing Command:

```bash
python tools/bmad-v2/tests/tier1_critical.py [file.html]
python tools/bmad-v2/fixers/tier1_fixer.py [file.html]
```

### Agent Command:

```bash
# Launch data consistency agent
claude-agent run data-consistency-agent [file.html]

# Launch schema agent
claude-agent run schema-agent [file.html]

# Launch technical agent
claude-agent run technical-agent [file.html]
```

### Success Criteria:

- ✅ Score: 15/15 = 100%
- ✅ All data values match config
- ✅ All schemas valid
- ✅ No critical HTML errors

### Failure Action:

- 🔴 **BLOCK DEPLOYMENT**
- Fix manually if auto-fix fails
- Re-run tests until 100%

---

## ⭐ TIER 2: SEO + CRO CORE (30 параметрів)

### 🎯 Target: 85%+ (WARNING IF < 85%)

### Category A: SEO Core (15 params)

16. **Word count: 1500-2500**
    - Check: Total words on page
    - Auto-fix: ⚠️ Report (manual content needed)
    - Agent: `seo-content-agent`

17. **Keyword density: 1.5-2.5%**
    - Check: Primary keyword frequency
    - Auto-fix: ⚠️ Suggest semantic content
    - Agent: `seo-content-agent`

18. **Title tag: 50-60 chars**
    - Check: `<title>` length
    - Auto-fix: ✅ Generate optimized title
    - Agent: `seo-meta-agent`

19. **Meta description: 150-160 chars**
    - Check: `<meta name="description">` length
    - Auto-fix: ✅ Generate from page content
    - Agent: `seo-meta-agent`

20. **H2-H6 heading structure**
    - Check: Proper hierarchy (H2 → H3 → H4)
    - Auto-fix: ⚠️ Report structure issues
    - Agent: `seo-structure-agent`

21. **Internal links: 10+**
    - Check: Count `<a href="/...">` links
    - Auto-fix: ⚠️ Suggest linking opportunities
    - Agent: `link-agent`

22. **Images: 10+ with optimization**
    - Check: Count `<img>` tags
    - Auto-fix: ✅ Add ImageObject schemas
    - Agent: `image-seo-agent`

23. **Alt text: all images**
    - Check: Every `<img>` has alt attribute
    - Auto-fix: ✅ Generate descriptive alt text
    - Agent: `image-seo-agent`

24. **FAQPage schema**
    - Check: FAQ section exists + schema
    - Auto-fix: ✅ Generate schema from FAQ HTML
    - Agent: `schema-agent`

25. **Breadcrumb navigation**
    - Check: BreadcrumbList schema present
    - Auto-fix: ✅ Generate from URL structure
    - Agent: `schema-agent`

26. **Structured data: 3+ types**
    - Check: LocalBusiness, FAQ, Breadcrumb, etc.
    - Auto-fix: ✅ Generate missing schemas
    - Agent: `schema-agent`

27. **URL structure clean**
    - Check: No ?id=123, use /service-name
    - Auto-fix: ⚠️ Report (requires routing changes)
    - Agent: `seo-structure-agent`

28. **Canonical tag**
    - Check: `<link rel="canonical">`
    - Auto-fix: ✅ Add with current URL
    - Agent: `seo-meta-agent`

29. **Open Graph tags**
    - Check: og:title, og:description, og:image, etc.
    - Auto-fix: ✅ Generate 10 OG tags
    - Agent: `social-meta-agent`

30. **Twitter Card tags**
    - Check: twitter:card, twitter:title, etc.
    - Auto-fix: ✅ Generate 6 Twitter tags
    - Agent: `social-meta-agent`

### Category B: CRO Essentials (15 params)

31. **CTA count: 3-8 (optimal 5-7)**
    - Check: Count call-to-action buttons
    - Auto-fix: ⚠️ Report if too many (> 8)
    - Agent: `cro-agent`

32. **CTA diversity**
    - Check: Mix of call, form, email CTAs
    - Auto-fix: ⚠️ Report missing types
    - Agent: `cro-agent`

33. **Form fields: ≤5**
    - Check: Count input fields in main form
    - Auto-fix: ⚠️ Suggest field reduction
    - Agent: `form-optimization-agent`

34. **Phone prominence above fold**
    - Check: Phone visible without scroll
    - Auto-fix: ⚠️ Report position
    - Agent: `visibility-agent`

35. **Trust badges: 3+**
    - Check: Licensed, Insured, Certified, etc.
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `trust-agent`

36. **Social proof visible**
    - Check: Reviews/testimonials above fold
    - Auto-fix: ⚠️ Report visibility
    - Agent: `cro-agent`

37. **Testimonials: 3+**
    - Check: Count testimonial elements
    - Auto-fix: ⚠️ Report count
    - Agent: `content-audit-agent`

38. **Rating display: 3+ instances**
    - Check: "4.9/5" or "★★★★★" mentions
    - Auto-fix: ⚠️ Suggest placements
    - Agent: `cro-agent`

39. **Urgency triggers: 3+**
    - Check: "same-day", "now", "today", "24/7"
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `psychology-agent`

40. **Risk reversal visible**
    - Check: Warranty mentioned prominently
    - Auto-fix: ⚠️ Report visibility
    - Agent: `cro-agent`

41. **Clear value proposition**
    - Check: Hero section has clear benefit
    - Auto-fix: ⚠️ Analyze and suggest
    - Agent: `copywriting-agent`

42. **Benefits vs features**
    - Check: "you/your" vs "we/our" ratio
    - Auto-fix: ⚠️ Report % and suggest rewrites
    - Agent: `copywriting-agent`

43. **Price transparency**
    - Check: Pricing visible or "free quote"
    - Auto-fix: ⚠️ Report presence
    - Agent: `cro-agent`

44. **Contact info in footer**
    - Check: Phone/email in footer
    - Auto-fix: ✅ Add if missing
    - Agent: `structure-agent`

45. **Sticky header with phone**
    - Check: Header sticks on scroll + phone visible
    - Auto-fix: ⚠️ Report (requires CSS/JS)
    - Agent: `ux-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier2_seo.py [file.html]
python tools/bmad-v2/tests/tier2_cro.py [file.html]
python tools/bmad-v2/fixers/tier2_fixer.py [file.html]
```

### Agent Commands:

```bash
# SEO optimization
claude-agent run seo-optimization-agent [file.html]

# CRO optimization
claude-agent run cro-optimization-agent [file.html]

# Full Tier 2
claude-agent run tier2-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 26+/30 = 85%+
- ✅ SEO fundamentals solid
- ✅ CRO elements present
- ⚠️ Warning if 80-84%

---

## 🎨 TIER 3: CONTENT + BASIC UX (50 параметрів)

### 🎯 Target: 70%+ (RECOMMENDED)

### Category A: Content Quality (20 params)

46. **Paragraph length: ≤5 sentences**
    - Check: Count sentences per `<p>`
    - Auto-fix: ⚠️ Report long paragraphs
    - Agent: `content-quality-agent`

47. **Bullet lists: 3+**
    - Check: Count `<ul>` and `<ol>` elements
    - Auto-fix: ⚠️ Suggest conversions
    - Agent: `content-quality-agent`

48. **Sections: 6-12**
    - Check: Count major `<section>` elements
    - Auto-fix: ⚠️ Report structure
    - Agent: `structure-agent`

49. **Readability score: Flesch 60+**
    - Check: Calculate Flesch Reading Ease
    - Auto-fix: ⚠️ Suggest simplifications
    - Agent: `readability-agent`

50. **Semantic keywords: 5+**
    - Check: LSI keywords present
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `seo-content-agent`

51. **Question headers**
    - Check: H2/H3 as questions (?)
    - Auto-fix: ⚠️ Suggest conversions
    - Agent: `content-quality-agent`

52. **Answer format**
    - Check: Direct answers after questions
    - Auto-fix: ⚠️ Analyze structure
    - Agent: `content-quality-agent`

53. **Table of contents (if long)**
    - Check: TOC for pages > 2000 words
    - Auto-fix: ✅ Generate from headers
    - Agent: `structure-agent`

54. **Jump links**
    - Check: Anchor links for navigation
    - Auto-fix: ✅ Add id attributes
    - Agent: `structure-agent`

55. **Related content links**
    - Check: "See also" or related links
    - Auto-fix: ⚠️ Suggest linking
    - Agent: `link-agent`

56. **Authority signals: 4+**
    - Check: "Licensed", "Certified", "Insured", "Years"
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `trust-agent`

57. **Pain point mentions: 3+**
    - Check: Problem statements/questions
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `psychology-agent`

58. **Benefit-driven headers**
    - Check: Headers focus on benefits
    - Auto-fix: ⚠️ Suggest rewrites
    - Agent: `copywriting-agent`

59. **Active voice: 80%+**
    - Check: Passive voice detection
    - Auto-fix: ⚠️ Suggest active rewrites
    - Agent: `writing-quality-agent`

60. **Technical terms explained**
    - Check: Jargon has parenthetical explanations
    - Auto-fix: ⚠️ Flag unexplained terms
    - Agent: `content-quality-agent`

61. **FAQ section present**
    - Check: FAQ HTML exists
    - Auto-fix: ⚠️ Report presence
    - Agent: `structure-agent`

62. **Step-by-step guides**
    - Check: "How it works" or process sections
    - Auto-fix: ⚠️ Report presence
    - Agent: `content-audit-agent`

63. **Comparison tables**
    - Check: `<table>` elements present
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `content-audit-agent`

64. **Stats/data points: 3+**
    - Check: Numbers with context (%, years, etc.)
    - Auto-fix: ⚠️ Count and suggest
    - Agent: `content-audit-agent`

65. **Expert credentials**
    - Check: Certifications, licenses mentioned
    - Auto-fix: ⚠️ Suggest additions
    - Agent: `trust-agent`

### Category B: Basic UX (30 params)

66. **Page load speed: <3s**
    - Check: PageSpeed Insights score
    - Auto-fix: ⚠️ Report + suggestions
    - Agent: `performance-agent`

67. **Lazy loading images**
    - Check: `<img loading="lazy">`
    - Auto-fix: ✅ Add to all images
    - Agent: `performance-agent`

68. **Mobile breakpoints: 3+**
    - Check: @media queries in CSS
    - Auto-fix: ⚠️ Report responsive coverage
    - Agent: `responsive-agent`

69. **Responsive typography**
    - Check: CSS clamp() or breakpoint font sizes
    - Auto-fix: ⚠️ Report
    - Agent: `responsive-agent`

70. **Color contrast: WCAG AA**
    - Check: 4.5:1 text, 3:1 UI elements
    - Auto-fix: ⚠️ Report violations
    - Agent: `accessibility-agent`

71. **Font size: 16px+ body**
    - Check: Base font-size ≥ 16px
    - Auto-fix: ✅ Set to 16px if smaller
    - Agent: `accessibility-agent`

72. **Whitespace optimization**
    - Check: margin/padding not cramped
    - Auto-fix: ⚠️ Report density
    - Agent: `design-agent`

73. **Visual hierarchy clear**
    - Check: H1 > H2 > H3 > p sizing
    - Auto-fix: ⚠️ Report inconsistencies
    - Agent: `design-agent`

74. **Click targets: 44px+**
    - Check: Button/link height
    - Auto-fix: ✅ Set min-height: 44px
    - Agent: `accessibility-agent`

75. **Form validation client-side**
    - Check: JavaScript validation present
    - Auto-fix: ⚠️ Report presence
    - Agent: `form-agent`

76. **Error messages helpful**
    - Check: Form errors descriptive
    - Auto-fix: ⚠️ Review messages
    - Agent: `ux-agent`

77. **Success states**
    - Check: Form submission feedback
    - Auto-fix: ⚠️ Report presence
    - Agent: `ux-agent`

78. **Loading indicators**
    - Check: Spinner or skeleton screens
    - Auto-fix: ⚠️ Report presence
    - Agent: `ux-agent`

79. **Hover states on CTAs**
    - Check: :hover CSS on buttons
    - Auto-fix: ✅ Add if missing
    - Agent: `interaction-agent`

80. **Focus indicators**
    - Check: :focus CSS visible
    - Auto-fix: ✅ Add outline if missing
    - Agent: `accessibility-agent`

81. **Skip navigation link**
    - Check: "Skip to content" link
    - Auto-fix: ✅ Add before header
    - Agent: `accessibility-agent`

82. **Keyboard accessible**
    - Check: Tab order logical
    - Auto-fix: ⚠️ Test and report
    - Agent: `accessibility-agent`

83. **Screen reader support**
    - Check: ARIA labels present
    - Auto-fix: ✅ Add aria-label to icons
    - Agent: `accessibility-agent`

84. **Touch-friendly**
    - Check: No hover-only interactions
    - Auto-fix: ⚠️ Report violations
    - Agent: `mobile-ux-agent`

85. **Hamburger menu mobile**
    - Check: Mobile nav collapses
    - Auto-fix: ⚠️ Report presence
    - Agent: `responsive-agent`

86. **Search function**
    - Check: Search input present
    - Auto-fix: ⚠️ Report presence
    - Agent: `feature-audit-agent`

87. **Breadcrumb trail visible**
    - Check: Breadcrumbs display (not just schema)
    - Auto-fix: ⚠️ Report visibility
    - Agent: `navigation-agent`

88. **Back to top button**
    - Check: Button appears on scroll
    - Auto-fix: ✅ Add JavaScript implementation
    - Agent: `ux-agent`

89. **Print-friendly styles**
    - Check: @media print CSS
    - Auto-fix: ✅ Add basic print styles
    - Agent: `design-agent`

90. **Favicon present**
    - Check: `<link rel="icon">`
    - Auto-fix: ✅ Add if missing
    - Agent: `technical-agent`

91. **Custom 404 page**
    - Check: 404.html exists
    - Auto-fix: ⚠️ Report presence
    - Agent: `technical-agent`

92. **Thank you page**
    - Check: Form submission redirect page
    - Auto-fix: ⚠️ Report presence
    - Agent: `technical-agent`

93. **Privacy policy linked**
    - Check: Link in footer
    - Auto-fix: ✅ Add link if missing
    - Agent: `legal-agent`

94. **Terms of service linked**
    - Check: Link in footer
    - Auto-fix: ✅ Add link if missing
    - Agent: `legal-agent`

95. **Cookie notice**
    - Check: GDPR compliance banner
    - Auto-fix: ⚠️ Report presence
    - Agent: `legal-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier3_content.py [file.html]
python tools/bmad-v2/tests/tier3_ux.py [file.html]
python tools/bmad-v2/fixers/tier3_fixer.py [file.html]
```

### Agent Commands:

```bash
# Content quality
claude-agent run content-optimization-agent [file.html]

# UX audit
claude-agent run ux-audit-agent [file.html]

# Full Tier 3
claude-agent run tier3-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 35+/50 = 70%+
- ✅ Content readable and structured
- ✅ Basic UX solid
- ℹ️ Not blocking, but quality indicator

---

## ⚡ TIER 4: PERFORMANCE + SPEED (25 параметрів)

### 🎯 Target: 80%+ (HIGH IMPACT ON UX)

### Category: Speed Optimization

96. **PageSpeed score: 85+ desktop**
    - Check: Google PageSpeed Insights
    - Auto-fix: ⚠️ Generate recommendations
    - Agent: `performance-agent`

97. **PageSpeed score: 75+ mobile**
    - Check: Mobile PageSpeed score
    - Auto-fix: ⚠️ Generate recommendations
    - Agent: `performance-agent`

98. **First Contentful Paint: <1.8s**
    - Check: FCP metric
    - Auto-fix: ⚠️ Analyze and suggest
    - Agent: `performance-agent`

99. **Largest Contentful Paint: <2.5s**
    - Check: LCP metric
    - Auto-fix: ⚠️ Analyze and suggest
    - Agent: `performance-agent`

100. **Total Blocking Time: <200ms**
     - Check: TBT metric
     - Auto-fix: ⚠️ Analyze JS
     - Agent: `performance-agent`

101. **Cumulative Layout Shift: <0.1**
     - Check: CLS metric
     - Auto-fix: ✅ Add width/height to images
     - Agent: `performance-agent`

102. **Image optimization: WebP format**
     - Check: Images use .webp or optimized
     - Auto-fix: ⚠️ Suggest conversion
     - Agent: `image-optimization-agent`

103. **Image compression**
     - Check: File sizes reasonable
     - Auto-fix: ⚠️ Suggest tools
     - Agent: `image-optimization-agent`

104. **Images have width/height**
     - Check: `<img>` has dimensions
     - Auto-fix: ✅ Add from actual size
     - Agent: `performance-agent`

105. **CSS minified**
     - Check: .min.css or minified
     - Auto-fix: ✅ Minify CSS
     - Agent: `optimization-agent`

106. **JavaScript minified**
     - Check: .min.js or minified
     - Auto-fix: ✅ Minify JS
     - Agent: `optimization-agent`

107. **HTML minified (production)**
     - Check: Whitespace removed
     - Auto-fix: ✅ Minify for production
     - Agent: `optimization-agent`

108. **Gzip compression enabled**
     - Check: Server sends gzip
     - Auto-fix: ⚠️ Report (server config)
     - Agent: `server-agent`

109. **Brotli compression**
     - Check: Server supports br
     - Auto-fix: ⚠️ Report (server config)
     - Agent: `server-agent`

110. **HTTP/2 enabled**
     - Check: Server uses HTTP/2
     - Auto-fix: ⚠️ Report (server config)
     - Agent: `server-agent`

111. **Critical CSS inlined**
     - Check: Above-fold CSS in <head>
     - Auto-fix: ✅ Extract and inline
     - Agent: `performance-agent`

112. **Defer non-critical JS**
     - Check: `<script defer>` or async
     - Auto-fix: ✅ Add defer attribute
     - Agent: `performance-agent`

113. **Preconnect to external domains**
     - Check: `<link rel="preconnect">`
     - Auto-fix: ✅ Add for fonts, APIs
     - Agent: `performance-agent`

114. **DNS prefetch**
     - Check: `<link rel="dns-prefetch">`
     - Auto-fix: ✅ Add for third-party
     - Agent: `performance-agent`

115. **Prefetch next page**
     - Check: `<link rel="prefetch">` for likely next page
     - Auto-fix: ✅ Add for main CTA destination
     - Agent: `performance-agent`

116. **Font preloading**
     - Check: `<link rel="preload">` for fonts
     - Auto-fix: ✅ Add for critical fonts
     - Agent: `performance-agent`

117. **Font subsetting**
     - Check: Fonts only include used glyphs
     - Auto-fix: ⚠️ Suggest tools
     - Agent: `font-optimization-agent`

118. **Reduce unused CSS**
     - Check: Coverage report
     - Auto-fix: ⚠️ Identify unused rules
     - Agent: `css-optimization-agent`

119. **Reduce unused JS**
     - Check: Coverage report
     - Auto-fix: ⚠️ Identify unused code
     - Agent: `js-optimization-agent`

120. **Eliminate render-blocking resources**
     - Check: No blocking CSS/JS
     - Auto-fix: ✅ Move to footer or defer
     - Agent: `performance-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier4_performance.py [file.html]
npm run lighthouse [url] --output=json
```

### Agent Commands:

```bash
# Performance audit
claude-agent run performance-audit-agent [file.html]

# Image optimization
claude-agent run image-optimization-agent [directory]

# Full Tier 4
claude-agent run tier4-performance-agent [file.html]
```

### Success Criteria:

- ✅ Score: 20+/25 = 80%+
- ✅ PageSpeed 85+ desktop, 75+ mobile
- ✅ Core Web Vitals pass
- ⚠️ High impact on user experience

---

## 🌐 TIER 5: CROSS-BROWSER + RESPONSIVE (30 параметрів)

### 🎯 Target: 70%+ (QUALITY ASSURANCE)

### Category: Browser Compatibility (15 params)

121. **Chrome desktop latest**
     - Check: Manual testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

122. **Chrome mobile latest**
     - Check: Mobile Chrome testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

123. **Firefox desktop latest**
     - Check: Manual testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

124. **Firefox mobile latest**
     - Check: Mobile Firefox testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

125. **Safari desktop latest**
     - Check: Manual testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

126. **Safari iOS latest**
     - Check: iPhone/iPad testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

127. **Edge latest**
     - Check: Manual testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

128. **Samsung Internet**
     - Check: Android device testing
     - Auto-fix: ❌ Manual
     - Agent: `browser-test-agent`

129. **Layout consistency across browsers**
     - Check: Screenshots comparison
     - Auto-fix: ⚠️ Report differences
     - Agent: `visual-regression-agent`

130. **Font rendering consistent**
     - Check: Font display across browsers
     - Auto-fix: ⚠️ Report issues
     - Agent: `visual-regression-agent`

131. **Image rendering consistent**
     - Check: Images display correctly
     - Auto-fix: ⚠️ Report issues
     - Agent: `visual-regression-agent`

132. **CSS Grid support + fallback**
     - Check: @supports (display: grid)
     - Auto-fix: ✅ Add flexbox fallback
     - Agent: `compatibility-agent`

133. **Flexbox support + fallback**
     - Check: Flexbox works everywhere
     - Auto-fix: ✅ Add float fallback if needed
     - Agent: `compatibility-agent`

134. **JavaScript features detection**
     - Check: Polyfills for old browsers
     - Auto-fix: ✅ Add feature detection
     - Agent: `compatibility-agent`

135. **Modal/popup functionality**
     - Check: Works on all browsers
     - Auto-fix: ⚠️ Report issues
     - Agent: `interaction-test-agent`

### Category: Responsive Design (15 params)

136. **Mobile (375px) - iPhone SE**
     - Check: Layout works at 375px
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

137. **Mobile (390px) - iPhone 12**
     - Check: Layout works at 390px
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

138. **Mobile (412px) - Android**
     - Check: Layout works at 412px
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

139. **Tablet (768px) - iPad**
     - Check: 2-column layout works
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

140. **Tablet (1024px) - iPad Pro**
     - Check: 3-column layout works
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

141. **Laptop (1366px)**
     - Check: Full layout displays
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

142. **Desktop (1920px)**
     - Check: Content centered, not stretched
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

143. **4K (2560px)**
     - Check: Max-width prevents stretch
     - Auto-fix: ✅ Add max-width
     - Agent: `responsive-test-agent`

144. **No horizontal scroll (any device)**
     - Check: overflow-x: hidden works
     - Auto-fix: ✅ Add to html/body
     - Agent: `responsive-test-agent`

145. **Images responsive**
     - Check: max-width: 100% on all images
     - Auto-fix: ✅ Add to CSS
     - Agent: `responsive-agent`

146. **Text readable (no tiny fonts)**
     - Check: Mobile fonts ≥ 14px
     - Auto-fix: ✅ Increase if smaller
     - Agent: `responsive-agent`

147. **Touch targets adequate**
     - Check: 44px+ on mobile
     - Auto-fix: ✅ Increase if smaller
     - Agent: `mobile-ux-agent`

148. **Orientation support**
     - Check: Works portrait + landscape
     - Auto-fix: ⚠️ Report issues
     - Agent: `responsive-test-agent`

149. **Zoom works (no max-scale)**
     - Check: user-scalable=yes
     - Auto-fix: ✅ Remove max-scale=1
     - Agent: `accessibility-agent`

150. **Print layout functional**
     - Check: @media print works
     - Auto-fix: ✅ Add basic print styles
     - Agent: `design-agent`

### Testing Commands:

```bash
# Cross-browser testing
npm run playwright-test
npm run browserstack-test

# Responsive testing
python tools/bmad-v2/tests/tier5_responsive.py [file.html]
```

### Agent Commands:

```bash
# Browser compatibility
claude-agent run browser-compatibility-agent [file.html]

# Responsive testing
claude-agent run responsive-test-agent [file.html]

# Full Tier 5
claude-agent run tier5-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 21+/30 = 70%+
- ✅ Works on Chrome, Firefox, Safari, Edge
- ✅ Responsive on mobile, tablet, desktop
- ℹ️ Quality assurance tier

---

## 🎨 TIER 6: ADVANCED UX + FEATURES (35 параметрів)

### 🎯 Target: 60%+ (ENHANCEMENT)

### Category: Advanced UX (20 params)

151. **Smooth scroll animations**
     - Check: scroll-behavior: smooth
     - Auto-fix: ✅ Add to CSS
     - Agent: `animation-agent`

152. **Fade-in animations on scroll**
     - Check: Elements animate on viewport enter
     - Auto-fix: ✅ Add Intersection Observer
     - Agent: `animation-agent`

153. **Parallax effects (if applicable)**
     - Check: Background parallax scrolling
     - Auto-fix: ⚠️ Not recommended (performance)
     - Agent: `animation-agent`

154. **Micro-interactions on buttons**
     - Check: Scale/pulse on hover/click
     - Auto-fix: ✅ Add CSS animations
     - Agent: `interaction-agent`

155. **Loading skeleton screens**
     - Check: Skeleton UI while loading
     - Auto-fix: ⚠️ Requires implementation
     - Agent: `ux-agent`

156. **Progressive image loading**
     - Check: Blur-up or placeholder images
     - Auto-fix: ⚠️ Requires image pipeline
     - Agent: `image-agent`

157. **Infinite scroll (if applicable)**
     - Check: Auto-load more content
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

158. **Lazy load below-fold content**
     - Check: Defer non-critical content
     - Auto-fix: ✅ Add loading="lazy"
     - Agent: `performance-agent`

159. **Prefetch next page links**
     - Check: Prefetch on hover/visible
     - Auto-fix: ✅ Add prefetch logic
     - Agent: `performance-agent`

160. **Service worker (PWA)**
     - Check: service-worker.js registered
     - Auto-fix: ⚠️ Requires setup
     - Agent: `pwa-agent`

161. **Offline functionality**
     - Check: Cache API for offline
     - Auto-fix: ⚠️ Requires PWA setup
     - Agent: `pwa-agent`

162. **App install prompt**
     - Check: PWA installable
     - Auto-fix: ⚠️ Requires manifest.json
     - Agent: `pwa-agent`

163. **Push notification support**
     - Check: Notifications API
     - Auto-fix: ⚠️ Requires backend
     - Agent: `feature-agent`

164. **Geolocation features**
     - Check: Location-based services
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

165. **Click-to-call functional**
     - Check: tel: links work
     - Auto-fix: ✅ Verify all phone links
     - Agent: `mobile-agent`

166. **Click-to-email functional**
     - Check: mailto: links work
     - Auto-fix: ✅ Verify email links
     - Agent: `mobile-agent`

167. **Click-to-SMS functional**
     - Check: sms: links present (if needed)
     - Auto-fix: ✅ Add if applicable
     - Agent: `mobile-agent`

168. **Map integration**
     - Check: Google Maps embedded
     - Auto-fix: ⚠️ Report presence
     - Agent: `feature-audit-agent`

169. **Directions link functional**
     - Check: Link to Maps directions
     - Auto-fix: ✅ Generate from address
     - Agent: `location-agent`

170. **Hours display (open/closed)**
     - Check: Real-time open status
     - Auto-fix: ⚠️ Requires JavaScript
     - Agent: `business-logic-agent`

### Category: Interactive Features (15 params)

171. **Holiday hours noted**
     - Check: Special hours mentioned
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

172. **Appointment scheduler widget**
     - Check: Booking form/calendar
     - Auto-fix: ⚠️ Report presence
     - Agent: `feature-audit-agent`

173. **Live availability display**
     - Check: Real-time slot availability
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

174. **Live chat widget**
     - Check: Chat integration present
     - Auto-fix: ⚠️ Report presence
     - Agent: `feature-audit-agent`

175. **Chatbot integration**
     - Check: AI chat functionality
     - Auto-fix: ⚠️ Report presence
     - Agent: `feature-audit-agent`

176. **FAQ search functionality**
     - Check: Search within FAQ
     - Auto-fix: ⚠️ Requires implementation
     - Agent: `feature-agent`

177. **Autocomplete in search**
     - Check: Search suggestions
     - Auto-fix: ⚠️ Requires implementation
     - Agent: `feature-agent`

178. **Filters for services/locations**
     - Check: Filtering UI present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

179. **Sort options (if listings)**
     - Check: Sort by price/rating/etc
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

180. **Pagination (if needed)**
     - Check: Page navigation present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

181. **Video backgrounds (hero section)**
     - Check: Video element in hero
     - Auto-fix: ⚠️ Not recommended (performance)
     - Agent: `media-agent`

182. **Video testimonials**
     - Check: Video testimonials present
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

183. **Image gallery/slider**
     - Check: Gallery functionality
     - Auto-fix: ⚠️ Report presence
     - Agent: `feature-audit-agent`

184. **Before/after image slider**
     - Check: Comparison slider present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

185. **360-degree image viewer**
     - Check: 360° product view
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier6_advanced_ux.py [file.html]
npm run feature-audit
```

### Agent Commands:

```bash
# Advanced UX audit
claude-agent run advanced-ux-agent [file.html]

# Feature audit
claude-agent run feature-audit-agent [file.html]

# Full Tier 6
claude-agent run tier6-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 21+/35 = 60%+
- ✅ Nice-to-have features present
- ✅ Enhanced user experience
- ℹ️ Enhancement tier (not critical)

---

## 📊 TIER 7: ANALYTICS + TRACKING (28 параметрів)

### 🎯 Target: 70%+ (BUSINESS INTELLIGENCE)

### Category: Core Analytics (15 params)

186. **Google Analytics 4 installed**
     - Check: GA4 gtag.js present
     - Auto-fix: ✅ Add GA4 code
     - Agent: `analytics-agent`

187. **Google Tag Manager setup**
     - Check: GTM container loaded
     - Auto-fix: ✅ Add GTM code
     - Agent: `analytics-agent`

188. **Conversion tracking: calls**
     - Check: tel: click events tracked
     - Auto-fix: ✅ Add GTM event
     - Agent: `analytics-agent`

189. **Conversion tracking: forms**
     - Check: Form submissions tracked
     - Auto-fix: ✅ Add GTM event
     - Agent: `analytics-agent`

190. **Event tracking: CTA clicks**
     - Check: Button clicks tracked
     - Auto-fix: ✅ Add GTM events
     - Agent: `analytics-agent`

191. **Scroll depth tracking**
     - Check: 25%, 50%, 75%, 100% tracked
     - Auto-fix: ✅ Add GTM trigger
     - Agent: `analytics-agent`

192. **Exit intent tracking**
     - Check: Mouse-out events tracked
     - Auto-fix: ✅ Add exit intent logic
     - Agent: `analytics-agent`

193. **Heat map tracking (Hotjar/etc)**
     - Check: Heatmap tool installed
     - Auto-fix: ⚠️ Requires account
     - Agent: `analytics-agent`

194. **Session recording enabled**
     - Check: Session replay tool active
     - Auto-fix: ⚠️ Requires tool
     - Agent: `analytics-agent`

195. **A/B testing platform**
     - Check: Google Optimize or similar
     - Auto-fix: ⚠️ Requires setup
     - Agent: `testing-agent`

196. **User flow tracking**
     - Check: Navigation paths tracked
     - Auto-fix: ✅ Enable in GA4
     - Agent: `analytics-agent`

197. **Funnel visualization**
     - Check: Conversion funnels defined
     - Auto-fix: ⚠️ Configure in GA4
     - Agent: `analytics-agent`

198. **Goal completions tracked**
     - Check: Key goals defined in GA4
     - Auto-fix: ⚠️ Configure in GA4
     - Agent: `analytics-agent`

199. **Custom dimensions set**
     - Check: Custom GA4 dimensions
     - Auto-fix: ⚠️ Configure in GA4
     - Agent: `analytics-agent`

200. **User ID tracking**
     - Check: Logged-in user tracking
     - Auto-fix: ⚠️ Requires backend
     - Agent: `analytics-agent`

### Category: Advanced Tracking (13 params)

201. **Cross-domain tracking**
     - Check: Linker parameter present
     - Auto-fix: ⚠️ Configure if multi-domain
     - Agent: `analytics-agent`

202. **Referral source tracking**
     - Check: Traffic sources tracked
     - Auto-fix: ✅ Default in GA4
     - Agent: `analytics-agent`

203. **Campaign parameter tracking (UTM)**
     - Check: UTM parameters recognized
     - Auto-fix: ✅ Default in GA4
     - Agent: `analytics-agent`

204. **Phone call tracking numbers**
     - Check: Dynamic number insertion
     - Auto-fix: ⚠️ Requires call tracking service
     - Agent: `call-tracking-agent`

205. **Form field tracking**
     - Check: Field-level interactions tracked
     - Auto-fix: ✅ Add GTM events
     - Agent: `analytics-agent`

206. **Error tracking (JavaScript)**
     - Check: window.onerror or Sentry
     - Auto-fix: ✅ Add error handler
     - Agent: `error-tracking-agent`

207. **Performance monitoring**
     - Check: Web Vitals sent to analytics
     - Auto-fix: ✅ Add web-vitals.js
     - Agent: `performance-agent`

208. **Core Web Vitals tracking**
     - Check: LCP, FID, CLS tracked
     - Auto-fix: ✅ Add CWV events
     - Agent: `performance-agent`

209. **Video engagement tracking**
     - Check: Video plays/completions tracked
     - Auto-fix: ✅ Add YouTube API events
     - Agent: `media-agent`

210. **PDF download tracking**
     - Check: PDF link clicks tracked
     - Auto-fix: ✅ Add GTM trigger
     - Agent: `analytics-agent`

211. **Outbound link tracking**
     - Check: External links tracked
     - Auto-fix: ✅ Add GTM trigger
     - Agent: `analytics-agent`

212. **File download tracking**
     - Check: Downloads tracked
     - Auto-fix: ✅ Add GTM trigger
     - Agent: `analytics-agent`

213. **Social sharing tracking**
     - Check: Share button clicks tracked
     - Auto-fix: ✅ Add events
     - Agent: `analytics-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier7_analytics.py [file.html]
npm run analytics-audit
```

### Agent Commands:

```bash
# Analytics setup
claude-agent run analytics-setup-agent [file.html]

# Tracking audit
claude-agent run tracking-audit-agent [file.html]

# Full Tier 7
claude-agent run tier7-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 20+/28 = 70%+
- ✅ GA4 + GTM installed
- ✅ Key conversions tracked
- ⚠️ Important for business insights

---

## 🎬 TIER 8: CONTENT FEATURES (30 параметрів)

### 🎯 Target: 50%+ (NICE TO HAVE)

### Category: Media & Interactive Content (30 params)

214. **Video content embedded**
     - Check: YouTube/Vimeo videos present
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

215. **Video auto-play (muted)**
     - Check: Background videos auto-play
     - Auto-fix: ⚠️ Not recommended
     - Agent: `media-agent`

216. **Video captions/subtitles**
     - Check: CC available on videos
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `accessibility-agent`

217. **YouTube/Vimeo integration**
     - Check: Properly embedded
     - Auto-fix: ⚠️ Verify embeds
     - Agent: `media-agent`

218. **Image gallery/slider**
     - Check: Gallery functionality
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

219. **Before/after image slider**
     - Check: Comparison tool
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

220. **360-degree image viewer**
     - Check: 360° product view
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

221. **Product/service catalog**
     - Check: Structured listings
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

222. **Pricing calculator**
     - Check: Interactive calculator
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

223. **Cost estimator tool**
     - Check: Estimate tool present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

224. **ROI calculator**
     - Check: ROI tool present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

225. **Savings calculator**
     - Check: Savings tool present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

226. **Interactive checklist**
     - Check: Checkable items
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

227. **Downloadable PDF guides**
     - Check: PDFs available
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

228. **Printable checklists**
     - Check: Print-friendly documents
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

229. **Email-gated content**
     - Check: Lead magnets present
     - Auto-fix: ⚠️ Marketing strategy
     - Agent: `content-audit-agent`

230. **Newsletter signup form**
     - Check: Email opt-in present
     - Auto-fix: ⚠️ Requires email service
     - Agent: `form-agent`

231. **Blog integration**
     - Check: Blog section exists
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

232. **Blog post schema**
     - Check: Article schema present
     - Auto-fix: ✅ Add if blog exists
     - Agent: `schema-agent`

233. **Related posts widget**
     - Check: "Related articles" present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

234. **Popular posts widget**
     - Check: "Most popular" present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

235. **Recent posts widget**
     - Check: "Latest articles" present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

236. **Category/tag filtering**
     - Check: Content filters present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

237. **Author bios**
     - Check: Author profiles present
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

238. **Social sharing buttons**
     - Check: Share buttons present
     - Auto-fix: ✅ Add if missing
     - Agent: `social-agent`

239. **Comments system (if blog)**
     - Check: Comments functionality
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

240. **Rating/review system**
     - Check: User reviews present
     - Auto-fix: ⚠️ Feature-dependent
     - Agent: `feature-audit-agent`

241. **User-generated content display**
     - Check: UGC showcased
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

242. **Case studies published**
     - Check: Success stories present
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

243. **Portfolio/work examples**
     - Check: Examples showcased
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `content-audit-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier8_content_features.py [file.html]
```

### Agent Commands:

```bash
# Content features audit
claude-agent run content-features-agent [file.html]

# Full Tier 8
claude-agent run tier8-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 15+/30 = 50%+
- ℹ️ Optional features
- ℹ️ Content-dependent
- ℹ️ Nice to have for engagement

---

## 🔗 TIER 9: INTEGRATIONS + POLISH (34 параметрів)

### 🎯 Target: 40%+ (OPTIONAL)

### Category: Third-Party Integrations (20 params)

244. **CRM integration**
     - Check: Salesforce/HubSpot connected
     - Auto-fix: ⚠️ Requires accounts
     - Agent: `integration-agent`

245. **Email marketing integration**
     - Check: MailChimp/ConvertKit connected
     - Auto-fix: ⚠️ Requires accounts
     - Agent: `integration-agent`

246. **SMS marketing platform**
     - Check: Twilio/similar integrated
     - Auto-fix: ⚠️ Requires account
     - Agent: `integration-agent`

247. **Appointment booking system**
     - Check: Calendly/Acuity integrated
     - Auto-fix: ⚠️ Requires account
     - Agent: `integration-agent`

248. **Payment gateway (if needed)**
     - Check: Stripe/PayPal integrated
     - Auto-fix: ⚠️ Business-dependent
     - Agent: `integration-agent`

249. **Invoice system integration**
     - Check: Billing system connected
     - Auto-fix: ⚠️ Business-dependent
     - Agent: `integration-agent`

250. **Scheduling software**
     - Check: Calendar integration
     - Auto-fix: ⚠️ Requires service
     - Agent: `integration-agent`

251. **Live chat software**
     - Check: Intercom/Drift/etc installed
     - Auto-fix: ⚠️ Requires account
     - Agent: `integration-agent`

252. **Help desk integration**
     - Check: Zendesk/Freshdesk connected
     - Auto-fix: ⚠️ Requires account
     - Agent: `integration-agent`

253. **Knowledge base integration**
     - Check: Help center connected
     - Auto-fix: ⚠️ Requires setup
     - Agent: `integration-agent`

254. **Review platform integration**
     - Check: Trustpilot/Yelp/Google reviews
     - Auto-fix: ⚠️ Requires API
     - Agent: `integration-agent`

255. **Google My Business sync**
     - Check: GMB data pulling
     - Auto-fix: ⚠️ Requires API
     - Agent: `integration-agent`

256. **Facebook page integration**
     - Check: Facebook feed/reviews
     - Auto-fix: ⚠️ Requires API
     - Agent: `integration-agent`

257. **Instagram feed integration**
     - Check: Instagram posts displayed
     - Auto-fix: ⚠️ Requires API
     - Agent: `integration-agent`

258. **Twitter feed integration**
     - Check: Twitter timeline embedded
     - Auto-fix: ⚠️ Requires widget
     - Agent: `integration-agent`

259. **LinkedIn integration**
     - Check: LinkedIn content present
     - Auto-fix: ⚠️ Requires API
     - Agent: `integration-agent`

260. **YouTube channel integration**
     - Check: Latest videos displayed
     - Auto-fix: ⚠️ Requires API
     - Agent: `integration-agent`

261. **Zapier integrations**
     - Check: Zapier webhooks connected
     - Auto-fix: ⚠️ Requires account
     - Agent: `integration-agent`

262. **Webhook endpoints**
     - Check: API webhooks functional
     - Auto-fix: ⚠️ Requires backend
     - Agent: `integration-agent`

263. **API documentation**
     - Check: API docs published
     - Auto-fix: ⚠️ Content-dependent
     - Agent: `documentation-agent`

### Category: Final Polish (14 params)

264. **Custom logo design**
     - Check: Professional logo present
     - Auto-fix: ⚠️ Design work
     - Agent: `design-audit-agent`

265. **Logo variations (light/dark)**
     - Check: Multiple logo versions
     - Auto-fix: ⚠️ Design work
     - Agent: `design-audit-agent`

266. **Brand colors documented**
     - Check: Style guide exists
     - Auto-fix: ⚠️ Documentation work
     - Agent: `documentation-agent`

267. **Typography system documented**
     - Check: Font system defined
     - Auto-fix: ⚠️ Documentation work
     - Agent: `documentation-agent`

268. **Design system/style guide**
     - Check: Complete style guide
     - Auto-fix: ⚠️ Design work
     - Agent: `documentation-agent`

269. **Component library**
     - Check: Reusable components documented
     - Auto-fix: ⚠️ Development work
     - Agent: `documentation-agent`

270. **Icon system consistent**
     - Check: Icons from single system
     - Auto-fix: ⚠️ Design work
     - Agent: `design-audit-agent`

271. **Illustrations custom**
     - Check: Custom graphics present
     - Auto-fix: ⚠️ Design work
     - Agent: `design-audit-agent`

272. **Photography professional**
     - Check: High-quality photos
     - Auto-fix: ⚠️ Content work
     - Agent: `content-audit-agent`

273. **Sitemap XML updated**
     - Check: sitemap.xml current
     - Auto-fix: ✅ Generate sitemap
     - Agent: `seo-agent`

274. **Robots.txt optimized**
     - Check: robots.txt configured
     - Auto-fix: ✅ Generate robots.txt
     - Agent: `seo-agent`

275. **Security headers configured**
     - Check: CSP, X-Frame-Options, etc.
     - Auto-fix: ⚠️ Server configuration
     - Agent: `security-agent`

276. **CORS configured properly**
     - Check: CORS headers set
     - Auto-fix: ⚠️ Server configuration
     - Agent: `security-agent`

277. **Performance budget defined**
     - Check: Budget rules documented
     - Auto-fix: ⚠️ Team decision
     - Agent: `documentation-agent`

### Testing Commands:

```bash
python tools/bmad-v2/tests/tier9_integrations.py [file.html]
python tools/bmad-v2/tests/tier9_polish.py [file.html]
```

### Agent Commands:

```bash
# Integrations audit
claude-agent run integrations-agent [file.html]

# Polish audit
claude-agent run polish-agent [file.html]

# Full Tier 9
claude-agent run tier9-full-agent [file.html]
```

### Success Criteria:

- ✅ Score: 14+/34 = 40%+
- ℹ️ Fully optional
- ℹ️ For advanced sites only
- ℹ️ Business/feature-dependent

---

## 🤖 AGENT-BASED TESTING SYSTEM

### Agent Architecture:

```
┌─────────────────────────────────────────────────────────┐
│              BMAD v2 AGENT COORDINATOR                  │
│                                                          │
│  Manages execution of specialized testing agents        │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌───────▼──────┐  ┌──────▼───────┐
│  Tier 1-3    │  │  Tier 4-6    │  │  Tier 7-9    │
│   Agents     │  │   Agents     │  │   Agents     │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Available Agents:

**Tier 1 Agents:**
- `data-consistency-agent` - Validates all global data
- `schema-agent` - Manages JSON-LD schemas
- `technical-agent` - HTML/technical validation
- `security-agent` - HTTPS and security checks

**Tier 2 Agents:**
- `seo-optimization-agent` - Full SEO audit + fixes
- `cro-optimization-agent` - CRO audit + suggestions
- `seo-meta-agent` - Meta tags optimization
- `image-seo-agent` - Image SEO + alt text

**Tier 3 Agents:**
- `content-quality-agent` - Content structure and quality
- `ux-audit-agent` - UX and usability audit
- `accessibility-agent` - WCAG compliance
- `readability-agent` - Reading level analysis

**Tier 4 Agents:**
- `performance-agent` - Speed and Core Web Vitals
- `image-optimization-agent` - Image compression/format
- `optimization-agent` - Minification and bundling

**Tier 5 Agents:**
- `browser-test-agent` - Cross-browser testing
- `responsive-test-agent` - Multi-device testing
- `visual-regression-agent` - Screenshot comparison

**Tier 6 Agents:**
- `advanced-ux-agent` - Advanced UX features
- `feature-audit-agent` - Feature presence audit
- `pwa-agent` - PWA capabilities

**Tier 7 Agents:**
- `analytics-agent` - Analytics setup and tracking
- `tracking-audit-agent` - Event tracking verification

**Tier 8-9 Agents:**
- `content-features-agent` - Content features audit
- `integration-agent` - Third-party integrations
- `documentation-agent` - Documentation completeness

### Agent Execution:

```bash
# Run single tier with agents
claude-agent tier1 index.html

# Run specific agent
claude-agent run seo-optimization-agent index.html

# Run all tiers sequentially
claude-agent full-audit index.html

# Run parallel (Tiers 1-4 together)
claude-agent parallel-audit index.html
```

### Agent Output Format:

```json
{
  "agent": "data-consistency-agent",
  "tier": 1,
  "file": "index.html",
  "timestamp": "2025-10-12T14:30:00Z",
  "results": {
    "passed": 8,
    "failed": 0,
    "warnings": 0,
    "score": "100%"
  },
  "details": [
    {
      "param": "phone_consistency",
      "status": "pass",
      "value": "437-747-6737",
      "occurrences": 12,
      "message": "All phone numbers consistent"
    }
  ],
  "fixes_applied": [
    {
      "param": "rating_consistency",
      "action": "normalized",
      "before": "4.9★, 4.9/5, 4.9 stars",
      "after": "4.9/5 (all instances)"
    }
  ],
  "recommendations": []
}
```

---

## 🔄 OPTIMIZATION WORKFLOW

### Complete Optimization Process:

```bash
#!/bin/bash
# bmad-v2-optimize.sh - Complete optimization workflow

FILE=$1

echo "🚀 Starting BMAD v2 Optimization: $FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: Backup
echo "📦 Creating backup..."
cp "$FILE" "$FILE.backup_$(date +%Y%m%d_%H%M%S)"

# Step 2: Tier 1 - CRITICAL (MUST PASS)
echo ""
echo "🔴 TIER 1: Critical Foundation (15 params)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
claude-agent tier1 "$FILE"

TIER1_SCORE=$(python tools/bmad-v2/get-score.py "$FILE" tier1)
if [ "$TIER1_SCORE" != "100" ]; then
    echo "❌ TIER 1 FAILED: Score $TIER1_SCORE/100"
    echo "🔴 BLOCKING DEPLOYMENT"
    exit 1
fi
echo "✅ TIER 1 PASSED: 100/100"

# Step 3: Tier 2 - SEO + CRO (TARGET 85%)
echo ""
echo "⭐ TIER 2: SEO + CRO Core (30 params)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
claude-agent tier2 "$FILE"

TIER2_SCORE=$(python tools/bmad-v2/get-score.py "$FILE" tier2)
echo "⭐ TIER 2 SCORE: $TIER2_SCORE/100"
if [ "$TIER2_SCORE" -lt 85 ]; then
    echo "⚠️  WARNING: Below 85% target"
fi

# Step 4: Tier 3 - Content + UX (TARGET 70%)
echo ""
echo "🎨 TIER 3: Content + Basic UX (50 params)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
claude-agent tier3 "$FILE"

TIER3_SCORE=$(python tools/bmad-v2/get-score.py "$FILE" tier3)
echo "🎨 TIER 3 SCORE: $TIER3_SCORE/100"

# Step 5: Tier 4 - Performance (TARGET 80%)
echo ""
echo "⚡ TIER 4: Performance + Speed (25 params)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
claude-agent tier4 "$FILE"

TIER4_SCORE=$(python tools/bmad-v2/get-score.py "$FILE" tier4)
echo "⚡ TIER 4 SCORE: $TIER4_SCORE/100"

# Step 6: Generate final report
echo ""
echo "📊 Generating final report..."
python tools/bmad-v2/generate-report.py "$FILE" --output="bmad-report-$(date +%Y%m%d).html"

# Step 7: Deployment decision
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 FINAL SCORES:"
echo "   Tier 1: $TIER1_SCORE/100 (Required: 100%)"
echo "   Tier 2: $TIER2_SCORE/100 (Target: 85%)"
echo "   Tier 3: $TIER3_SCORE/100 (Target: 70%)"
echo "   Tier 4: $TIER4_SCORE/100 (Target: 80%)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$TIER1_SCORE" == "100" ] && [ "$TIER2_SCORE" -ge 85 ]; then
    echo "✅ DEPLOYMENT: APPROVED"
    exit 0
elif [ "$TIER1_SCORE" == "100" ] && [ "$TIER2_SCORE" -ge 80 ]; then
    echo "⚠️  DEPLOYMENT: APPROVED WITH WARNING"
    echo "   Consider improving Tier 2 to 85%+"
    exit 0
else
    echo "🔴 DEPLOYMENT: NOT RECOMMENDED"
    echo "   Review failed parameters and re-optimize"
    exit 1
fi
```

---

## 🚪 DEPLOYMENT GATES

### Gate System:

```
┌──────────────────────────────────────────────────────┐
│ GATE 1: TIER 1 = 100%                                │
│ ─────────────────────                                │
│ Status: BLOCKING                                      │
│ Action: STOP deployment if < 100%                    │
│ Reason: Data consistency critical                    │
│                                                       │
│ IF PASS → Continue to Gate 2                         │
│ IF FAIL → Fix manually, re-run, repeat until pass    │
└──────────────────────────────────────────────────────┘
                     │ PASS
                     ▼
┌──────────────────────────────────────────────────────┐
│ GATE 2: TIER 2 ≥ 85%                                │
│ ─────────────────────                                │
│ Status: WARNING                                       │
│ Action: Can deploy but warn if < 85%                 │
│ Reason: SEO + CRO important for visibility           │
│                                                       │
│ IF ≥ 85% → APPROVED                                  │
│ IF 80-84% → APPROVED WITH WARNING                    │
│ IF < 80% → NOT RECOMMENDED (but not blocked)         │
└──────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│ GATE 3: TIER 3-4 ≥ 70%                              │
│ ─────────────────────────                            │
│ Status: INFORMATIONAL                                 │
│ Action: Quality indicator only                       │
│ Reason: UX + Performance nice to have                │
│                                                       │
│ IF ≥ 70% → GOOD QUALITY                             │
│ IF < 70% → ACCEPTABLE (no action required)           │
└──────────────────────────────────────────────────────┘
```

### Deployment Decision Matrix:

| Tier 1 | Tier 2 | Tier 3 | Tier 4 | Decision | Action |
|--------|--------|--------|--------|----------|--------|
| 100% | 90% | 80% | 85% | ✅ APPROVED | Deploy immediately |
| 100% | 87% | 75% | 70% | ✅ APPROVED | Deploy immediately |
| 100% | 82% | 65% | 60% | ⚠️ WARNING | Can deploy, note improvements |
| 100% | 78% | 50% | 55% | ⚠️ WARNING | Consider improving Tier 2 |
| 95% | 90% | 85% | 90% | 🔴 BLOCKED | Fix Tier 1 first |
| 87% | 95% | 90% | 95% | 🔴 BLOCKED | Tier 1 must be 100% |

---

## 📚 SUMMARY

### BMAD v2 Method = 9 Tiers, 277 Parameters

**Production Requirements:**
- ✅ Tier 1: 100% (BLOCKS deployment)
- ⭐ Tier 2: 85%+ (WARNING if fail)
- 🎨 Tier 3: 70%+ (Recommended)
- ⚡ Tier 4: 80%+ (High impact)

**Quality Enhancements:**
- 🌐 Tier 5: 70%+ (Cross-browser + responsive)
- 🎨 Tier 6: 60%+ (Advanced UX)
- 📊 Tier 7: 70%+ (Analytics)

**Optional:**
- 🎬 Tier 8: 50%+ (Content features)
- 🔗 Tier 9: 40%+ (Integrations + polish)

### Automation:
- **60% parameters** auto-fixable with scripts/agents
- **40% parameters** require manual work
- **Agent-driven** testing for complex validations

### Time Investment:
- **Tier 1-2:** 10 minutes (mostly automated)
- **Tier 3:** 5 hours (content work)
- **Tier 4:** 2 hours (performance tuning)
- **Tier 5-9:** Varies (optional enhancements)

**Total:** ~20 hours for complete optimization (Tiers 1-9)
**Minimum:** ~7 hours for production-ready (Tiers 1-4)

---

**Version:** 2.0
**Last Updated:** 2025-10-12
**Status:** ✅ PRODUCTION READY
**Methodology:** BMAD (Best Method for Appliance Documentation)
