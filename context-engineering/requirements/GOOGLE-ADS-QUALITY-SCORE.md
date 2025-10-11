# GOOGLE ADS QUALITY SCORE OPTIMIZATION

## 🎯 Goal: Achieve 8-10/10 Quality Score = Lower CPC + Better Ad Position

### What is Quality Score?
Google rates your ads 1-10 based on:
- Landing page experience (33%)
- Ad relevance (33%)
- Expected CTR (33%)

**Higher score = Lower cost per click + Better positions**

## 1. LANDING PAGE EXPERIENCE OPTIMIZATION

### Page Speed Requirements
- [ ] Mobile load time < 2.5 seconds
- [ ] Desktop load time < 1.5 seconds
- [ ] Time to Interactive < 3.5 seconds
- [ ] First Contentful Paint < 1 second
- [ ] Cumulative Layout Shift < 0.1

### Speed Optimization Checklist
```html
<!-- Preload critical resources -->
<link rel="preload" href="fonts/Fredoka.woff2" as="font" crossorigin>
<link rel="preload" href="css/critical.css" as="style">

<!-- Async non-critical CSS -->
<link rel="preload" href="css/style.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- Lazy load images -->
<img src="placeholder.jpg" data-src="actual-image.jpg" loading="lazy" alt="Description">

<!-- Minify everything -->
<!-- Compress images to WebP -->
<!-- Enable GZIP compression -->
<!-- Use CDN for static assets -->
```

### Mobile Optimization (70% of clicks)
- [ ] Thumb-friendly CTAs (min 48px)
- [ ] No horizontal scrolling
- [ ] Text readable without zoom
- [ ] Forms easy to fill
- [ ] Click-to-call prominent

### Trust & Credibility
- [ ] SSL certificate active
- [ ] Business info visible
- [ ] Reviews/testimonials shown
- [ ] Security badges displayed
- [ ] Clear privacy policy

### Navigation & UX
- [ ] Relevant content above fold
- [ ] Clear value proposition
- [ ] Easy to find information
- [ ] Simple conversion path
- [ ] No intrusive popups

## 2. AD-TO-PAGE MESSAGE MATCH

### Exact Match Requirements
Your landing page MUST mirror your ad copy exactly:

**If Ad Says**: "Same-Day Refrigerator Repair Toronto - Save $40"
**Page Must Have**: 
- "Same-Day Refrigerator Repair" in H1
- "Toronto" mentioned prominently
- "$40 savings" visible above fold

### Message Match Template
```html
<!-- For Ad: "[Service] Repair Toronto - Same Day - Save $40" -->

<h1>[Service] Repair Toronto - Same Day Service Available</h1>
<div class="hero-offer">
    <span class="savings">Save $40</span>
    <span class="terms">New Customers - Today Only</span>
</div>
```

### Consistency Checklist
- [ ] Headline matches ad headline
- [ ] Offer matches exactly
- [ ] CTA matches ad CTA
- [ ] Pricing consistent
- [ ] Service area same
- [ ] Urgency level same

## 3. DYNAMIC KEYWORD INSERTION (DKI) READY

### URL Structure for DKI
```
/services/[appliance]-repair-[location]/
Example: /services/refrigerator-repair-toronto/
```

### Dynamic Content Blocks
```html
<!-- Dynamic Headline -->
<h1 class="dynamic-headline" data-default="Appliance Repair Toronto">
    <span class="service">{Keyword:Appliance}</span> Repair 
    <span class="location">{Location:Toronto}</span>
</h1>

<!-- Dynamic Meta Tags -->
<title>{Keyword:Appliance} Repair {Location:Toronto} | Save $40 - Nika</title>
<meta name="description" content="Professional {keyword:appliance} repair in {location:Toronto}. Same-day service, 90-day warranty. Save $40! Call 437-747-6737">

<!-- Dynamic Content -->
<script>
// Parse URL parameters for dynamic content
const urlParams = new URLSearchParams(window.location.search);
const service = urlParams.get('service') || 'appliance';
const location = urlParams.get('loc') || 'Toronto';

// Update content dynamically
document.querySelector('.service').textContent = service;
document.querySelector('.location').textContent = location;
</script>
```

### Landing Page Variations
Create specific pages for each ad group:
- `/refrigerator-repair-toronto/`
- `/washer-repair-north-york/`
- `/emergency-appliance-repair/`
- `/same-day-service-toronto/`

## 4. CONVERSION OPTIMIZATION FOR ADS

### Above-Fold Requirements
Users from ads want immediate answers:
1. **Headline** matching their search
2. **Offer** clearly visible ($40 OFF)
3. **Phone** number prominent
4. **Form** or booking CTA
5. **Trust** signals (reviews, licensed)
6. **Urgency** (same-day, limited)

### Conversion Elements Priority
```html
<section class="hero-ads">
    <!-- 1. Matching Headline -->
    <h1>Refrigerator Repair Toronto - Same Day Service</h1>
    
    <!-- 2. Offer Badge -->
    <div class="offer-badge">
        <span class="amount">$40 OFF</span>
        <span class="qualifier">First Time Customers</span>
    </div>
    
    <!-- 3. Trust Bar -->
    <div class="trust-bar">
        <span>✓ Licensed</span>
        <span>✓ 5,200+ Customers</span>
        <span>✓ 90-Day Warranty</span>
    </div>
    
    <!-- 4. Dual CTA -->
    <div class="cta-group">
        <a href="tel:4377476737" class="cta-call">Call Now: 437-747-6737</a>
        <a href="#book" class="cta-book">Book Online</a>
    </div>
    
    <!-- 5. Urgency -->
    <p class="urgency">⚡ Only 3 appointments left today</p>
</section>
```

## 5. QUALITY SCORE TRACKING

### Setup Tracking
1. **Google Ads Conversion Tracking**
   - Phone calls (60+ seconds)
   - Form submissions
   - Online bookings
   - Click-to-call

2. **UTM Parameters**
   ```
   ?utm_source=google
   &utm_medium=cpc
   &utm_campaign={campaign}
   &utm_term={keyword}
   &utm_content={adgroup}
   ```

3. **Landing Page Analytics**
   - Bounce rate by keyword
   - Time on page by ad group
   - Conversion rate by campaign
   - Page speed by device

### Quality Score Improvement Process
1. **Week 1**: Baseline measurement
2. **Week 2**: Speed optimization
3. **Week 3**: Message match refinement
4. **Week 4**: Conversion optimization
5. **Week 5+**: Continuous testing

## 6. AD GROUP LANDING PAGE MATRIX

### Service-Specific Pages
| Ad Group | Landing Page | Key Message |
|----------|-------------|-------------|
| Fridge Repair | /refrigerator-repair/ | "Fridge Repair Today" |
| Washer Repair | /washer-repair/ | "Washer Fixed Fast" |
| Emergency | /emergency-repair/ | "45-Min Response" |
| Same Day | /same-day-service/ | "Fixed Today Guaranteed" |

### Location-Specific Pages
| Ad Group | Landing Page | Local Focus |
|----------|-------------|-------------|
| Downtown | /downtown-toronto/ | "Serving Financial District" |
| North York | /north-york/ | "Your Local Experts" |
| Etobicoke | /etobicoke/ | "West End Specialists" |

## 7. COST REDUCTION STRATEGIES

### Lower CPC Through Quality
- 10/10 Quality Score = 50% discount on CPC
- 8/10 Quality Score = 25% discount
- 6/10 Quality Score = 0% discount
- 4/10 Quality Score = 25% penalty
- 2/10 Quality Score = 200% penalty

### Budget Optimization
1. **Focus budget on high QS keywords**
2. **Pause low QS keywords**
3. **Create specific landing pages**
4. **Test ad copy variations**
5. **Improve page experience**

## 8. TESTING FRAMEWORK

### A/B Tests for Quality Score
1. **Headlines**: Dynamic vs Static
2. **Forms**: Short vs Long
3. **CTAs**: Button vs Phone
4. **Trust**: Reviews vs Badges
5. **Layout**: Traditional vs Modern

### Measurement Period
- Run tests for 2 weeks minimum
- 1000+ impressions per variant
- Statistical significance required
- Monitor Quality Score changes

## 🎯 QUICK WINS CHECKLIST

### Immediate Improvements
- [ ] Compress all images
- [ ] Add lazy loading
- [ ] Match ad headlines exactly
- [ ] Add phone above fold
- [ ] Show offer prominently
- [ ] Add trust signals
- [ ] Optimize for mobile
- [ ] Track conversions

### Expected Results
- Quality Score: 6 → 8+ in 30 days
- CPC reduction: 20-40%
- Conversion rate: +15-25%
- Ad position: Improve 1-2 spots

Remember: Quality Score is updated daily. Consistent optimization = Compounding savings!