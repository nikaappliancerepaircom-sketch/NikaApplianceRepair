# DAY 1 BLOG POST REWRITE INSTRUCTIONS

## CRITICAL ISSUE
All 4 existing Day 1 blog posts use EMBEDDED CSS instead of external CSS references.
They need to be completely rewritten using the EXACT structure from premium-blog-example.html.

## REQUIRED CHANGES

### 1. Replace ALL Embedded CSS
**Current (WRONG):**
```html
<style>
    body { font-family: -apple-system... }
    .container { max-width: 800px... }
    /* hundreds of lines of CSS */
</style>
```

**Required (CORRECT):**
```html
<!-- External CSS -->
<link rel="stylesheet" href="../css/blog-premium.css">
<link rel="stylesheet" href="../css/header-optimized.css">
```

### 2. Use Premium Template Structure
**Copy EXACTLY from premium-blog-example.html:**
- Lines 190-227: Header with Nika logo, nav, trust signals, CTAs
- Lines 233-253: Blog header (category, reading time, date, author)
- Lines 256-269: Social share buttons
- Lines 494-527: Sidebar with TOC + related posts
- Lines 531-642: Footer with trust badges + links + contact
- Lines 645-672: JavaScript (progress bar + mobile menu)

### 3. Content Requirements for Each Post
- **Word count:** 2,750 words (not including HTML/schemas)
- **FAQs:** 10-12 questions minimum
- **Schemas:** All 7 required (Article, FAQ, LocalBusiness, HowTo, Breadcrumb, Organization, Rating)
- **Hard water data:** Toronto's 200-300 ppm mentioned in context
- **CTAs:** Multiple phone/booking buttons throughout
- **Related posts:** Link to same-day-appliance-repair.html, emergency-appliance-repair-24-7.html

### 4. Design Elements to Include
```html
<div class="tip-box">
    <strong>Pro Tip:</strong> Content here
</div>

<div class="info-box">
    <h3>Heading</h3>
    <p>Content here</p>
</div>

<div class="cta-box">
    <h3>CTA Heading</h3>
    <p>Description</p>
    <a href="tel:4377476737" class="btn">
        <i class="fas fa-phone"></i> Call (437) 747-6737
    </a>
</div>

<div class="comparison-grid">
    <div class="comparison-card safe">
        <h3>Safe for DIY</h3>
        <ul>...</ul>
    </div>
    <div class="comparison-card danger">
        <h3>Requires Professional</h3>
        <ul>...</ul>
    </div>
</div>
```

### 5. Sidebar TOC Structure
```html
<div class="toc-widget">
    <h3>Table of Contents</h3>
    <ul class="toc-list">
        <li><a href="#section1">Section Name</a></li>
        <li><a href="#section2">Section Name</a></li>
        ...
    </ul>
</div>
```

## FILES TO REWRITE

### 1. refrigerator-ice-maker-not-working.html
- **Focus:** Ice maker failures, hard water as PRIMARY cause
- **Keywords:** "ice maker not working toronto"
- **Cost range:** $200-400
- **Unique angle:** Toronto hard water (200-300 ppm) causes 60% of failures
- **Current status:** Has embedded CSS, needs complete rewrite

### 2. washing-machine-leaking-water.html
- **Focus:** Water leak diagnosis and repair
- **Keywords:** "washing machine leaking repair"
- **Cost range:** $150-500
- **Unique angle:** Door seal failures in Toronto's humid summers
- **Current status:** Has embedded CSS, needs complete rewrite

### 3. dryer-not-drying-clothes.html
- **Focus:** Heating element and lint issues
- **Keywords:** "dryer not drying toronto"
- **Cost range:** $100-450
- **Unique angle:** Winter venting challenges (ice buildup in external vents)
- **Current status:** Has embedded CSS, needs complete rewrite

### 4. dishwasher-leaving-food-spots.html
- **Focus:** Hard water spotting (UNIQUE ANGLE for this post)
- **Keywords:** "dishwasher spots hard water"
- **Cost range:** $80-300
- **Unique angle:** Toronto hard water creates spots - descaling guide
- **Current status:** Has embedded CSS, needs complete rewrite

## VERIFICATION CHECKLIST

For each file, verify:
- [ ] External CSS links present (blog-premium.css + header-optimized.css)
- [ ] NO embedded <style> tags anywhere
- [ ] Header structure matches lines 190-227 of premium template
- [ ] Footer structure matches lines 531-642 of premium template
- [ ] Sidebar present with TOC and related posts
- [ ] Progress bar JavaScript included
- [ ] Mobile menu JavaScript included
- [ ] All 7 schemas present and valid
- [ ] 10-12 FAQs included
- [ ] 2,750+ words of content
- [ ] Multiple CTA boxes with phone number
- [ ] Toronto hard water data mentioned where relevant

## NEXT STEPS

1. Delete current files or rename to .old
2. Create NEW files using premium-blog-example.html as BASE
3. Copy entire header, footer, sidebar, scripts sections
4. Write custom content for each topic (2,750 words)
5. Add topic-specific schemas and FAQs
6. Test in browser to ensure CSS loads correctly
7. Validate HTML and schema markup
