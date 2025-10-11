# Countdown Timer Component - Context Engineering

## Overview
The countdown timer is a critical conversion element used to create urgency and encourage immediate bookings. It should be used strategically 1-2 times per page.

## Design Specifications

### Visual Design
- **Background**: Dark gradient (#1a1a2e to #16213e)
- **Timer Values**: White color (#FFFFFF) - IMPORTANT
- **Timer Boxes**: Semi-transparent with backdrop blur
- **Font Size**: 3rem for numbers, uppercase labels
- **CTA Button**: Green gradient with shadow effect

### Timer Settings
- **Default Time**: 14 minutes 45 seconds
- **Auto-Reset**: Timer resets to 14:45 when reaching 0:00
- **Format**: MM:SS with leading zeros

## Usage Guidelines

### Placement Options
1. **After Hero Section**: Primary placement for maximum visibility
2. **Before Booking Form**: Secondary placement to create final urgency
3. **Sticky Banner**: Optional inline version for persistent visibility

### Content Variations

#### Standard Version
```html
<h2>Book Online & Save $40 on Any Appliance Repair</h2>
```

#### Brand-Specific
```html
<h2>Book Online & Save $40 on Any {BRAND_NAME} Repair</h2>
```

#### Location-Specific
```html
<h2>{LOCATION_NAME} Residents: Save $40 on Any Appliance Repair</h2>
```

#### Service-Specific
```html
<h2>Book {SERVICE_TYPE} Repair & Save $40 Today</h2>
```

## Implementation Rules

### DO:
- ✅ Use white color for timer numbers
- ✅ Keep timer visible above the fold when possible
- ✅ Maintain consistent 14:45 starting time
- ✅ Include calendar icon in CTA button
- ✅ Use uppercase for "MINUTES" and "SECONDS"

### DON'T:
- ❌ Use more than 2 countdown timers per page
- ❌ Place timers too close together
- ❌ Change the core $40 offer amount
- ❌ Use different timer durations on same site

## Technical Implementation

### HTML Structure
```html
<section class="countdown-section">
    <div class="container">
        <h2 class="countdown-title">Book Online & Save $40 on Any Appliance Repair</h2>
        <p class="countdown-label">DEAL ENDS IN</p>
        <div class="countdown-timer">
            <div class="timer-box">
                <div class="timer-value" id="minutes">14</div>
                <div class="timer-label">MINUTES</div>
            </div>
            <div class="timer-box">
                <div class="timer-value" id="seconds">45</div>
                <div class="timer-label">SECONDS</div>
            </div>
        </div>
        <a href="#book" class="countdown-cta">
            <svg><!-- Calendar Icon --></svg>
            CLICK TO BOOK DIAGNOSTIC NOW
        </a>
    </div>
</section>
```

### Key CSS Classes
- `.countdown-section` - Main container
- `.timer-value` - White numbers (color: #FFFFFF)
- `.timer-box` - Semi-transparent background boxes
- `.countdown-cta` - Green CTA button

### JavaScript Behavior
- Counts down from 14:45 to 00:00
- Auto-resets when reaching zero
- Updates every second
- Maintains state during page session

## A/B Testing Opportunities

### Timer Duration
- Test: 14:45 vs 9:59 vs 29:59
- Hypothesis: Shorter times create more urgency

### CTA Text
- Control: "CLICK TO BOOK DIAGNOSTIC NOW"
- Variant A: "CLAIM YOUR $40 DISCOUNT"
- Variant B: "BOOK NOW - SAVE $40"

### Placement
- Test sticky header vs after hero vs before form
- Measure scroll depth and conversion correlation

## Performance Metrics

### Success Indicators
- Click-through rate on CTA button
- Conversion rate (bookings)
- Time to conversion
- Bounce rate reduction

### Target Benchmarks
- CTR: 15-20%
- Conversion lift: +25-35%
- Average time on page: +20%

## Mobile Considerations
- Smaller font sizes (2.5rem on mobile)
- Stacked layout for inline version
- Touch-friendly CTA button (min 44px height)
- Reduced padding for space efficiency

## Accessibility
- High contrast (white on dark)
- Large, readable numbers
- Semantic HTML structure
- ARIA labels for screen readers

## Brand Consistency
- Matches main site color scheme
- Uses consistent fonts (Fredoka/Rubik)
- Aligns with overall urgency messaging
- Complements $40 off value proposition