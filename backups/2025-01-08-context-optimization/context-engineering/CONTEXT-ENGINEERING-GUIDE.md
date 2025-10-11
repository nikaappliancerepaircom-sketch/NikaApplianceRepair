# Context Engineering Guide - Nika Appliance Repair Website

## 🎨 Design System & Colors
**Primary Colors**:
- Headers (h1, h2, h3): `#1A237E` (Dark Blue - matches nappliancerepair.ca style)
- Primary Blue: `#2196F3`
- Primary Yellow: `#FFD600`
- Bright Green: `#4CAF50`
- Dark Background: `#1A237E`

**Typography**:
- Heading Font: 'Fredoka' (playful, rounded)
- Body Font: 'Rubik' (clean, professional)
- All h1, h2, h3 tags use consistent dark blue color (#1A237E)

## 📞 Contact Information
**Primary Phone**: 437-747-6737 (Updated across all pages)
- Format in links: `tel:4377476737`
- Display format: `437-747-6737`
- Appears in: Header, Footer, CTAs, Meta descriptions, Hero sections

## 🎯 Universal Countdown Timer Section
**Purpose**: Drive urgency and conversions with a consistent countdown timer across all pages

### Implementation Details
The countdown timer appears after the hero section and shows:
- **Headline**: "Book Online & Save $40 on Any Appliance Repair"
- **Timer**: 15 minutes countdown (resets on page refresh)
- **CTA Button**: Green "BOOK SERVICE NOW" button

### HTML Structure
```html
<!-- Countdown Section -->
<section class="countdown-section" style="padding: 4rem 0; background: white;">
    <div style="max-width: 800px; margin: 0 auto; padding: 0 2rem; text-align: center;">
        <h2 style="color: var(--navy-blue); font-family: var(--font-heading); font-size: 2.5rem; font-weight: 700; margin-bottom: 1.5rem; line-height: 1.2;">
            Book Online & Save $40 on Any Appliance<br>Repair
        </h2>
        <p style="color: #666; font-size: 0.875rem; font-weight: 600; letter-spacing: 1px; margin-bottom: 1.5rem;">DEAL ENDS IN</p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem;">
            <div style="background: #dc3545; color: white; padding: 1.5rem 2rem; border-radius: 10px; min-width: 120px;">
                <div style="font-size: 3rem; font-weight: 700; line-height: 1;" id="minutes">15</div>
                <div style="font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Minutes</div>
            </div>
            <div style="background: #dc3545; color: white; padding: 1.5rem 2rem; border-radius: 10px; min-width: 120px;">
                <div style="font-size: 3rem; font-weight: 700; line-height: 1;" id="seconds">00</div>
                <div style="font-size: 0.75rem; text-transform: uppercase; margin-top: 0.25rem;">Seconds</div>
            </div>
        </div>
        <a href="#book" class="universal-book-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
            </svg>
            BOOK SERVICE NOW
        </a>
    </div>
</section>
```

### JavaScript Requirements
- Timer starts at 15:00 and counts down
- Uses IDs: `minutes` and `seconds` for display
- Resets on page refresh
- When timer reaches 0:00, the section should remain visible but show "OFFER EXPIRED"

### Styling Notes
- Background: Clean white (#ffffff)
- Timer boxes: Red (#dc3545) with white text
- Button: Green (var(--primary-green)) with hover effects
- Mobile responsive: Adjusts padding and font sizes

### Placement Guidelines
1. **Homepage**: 
   - After hero section, before services
   - Before "How It Works" section
2. **Service Pages**: After hero/intro, before main content
3. **Location Pages**: After hero, before service details
4. **Brand Pages**: After brand intro, before models section

**Note**: Can be used multiple times on longer pages for reinforcement

### Conversion Psychology
- Creates urgency with countdown
- Clear value proposition ($40 savings)
- Strong contrast colors (red timer, green CTA)
- Simple, focused message
- Mobile-optimized for quick conversions

## ✅ Page Quality Assurance System

### Quality Checklist
Located at: `PAGE-QUALITY-CHECKLIST.md`
- Comprehensive 252-point checklist
- Covers SEO, psychology, conversion, performance
- Scoring system for page readiness

### Interactive Validator Tool
Located at: `/tools/page-quality-validator.html`
- Visual checklist interface
- Real-time quality scoring
- Critical vs recommended items
- Use before launching any page

### Critical Page Requirements
Every page MUST have:
1. Phone number 437-747-6737 (header, footer, CTAs)
2. Mobile responsive design
3. Page load under 5 seconds
4. At least one CTA above fold
5. Primary keyword in title and H1

## 📚 Advanced Documentation System

### SEO Guide
Located at: `/docs/ADVANCED-SEO-GUIDE.md`
- Word count requirements by page type
- Keyword density formulas (1.5-2.5% primary)
- Interlinking hub & spoke model
- Schema markup templates
- Featured snippet optimization
- Local SEO requirements

### Marketing Psychology Guide  
Located at: `/docs/MARKETING-PSYCHOLOGY-GUIDE.md`
- Psychological triggers (urgency, FOLO, social proof)
- Color psychology mapping
- Marketing models (AIDA, PAS, BAB)
- Persuasion architecture
- Neuromarketing techniques
- A/B testing priorities

### Page Templates Created
1. **Service Page**: `/services/refrigerator-repair.html`
   - 1,400+ words, complete SEO optimization
   - All psychological triggers implemented
   - Booking form integrated
   
2. **Brand Page**: `/brands/lg-appliance-repair.html`
   - 1,000+ words, brand-focused content
   - Model-specific information
   - Brand color theming
   
3. **Location Page**: `/locations/downtown-toronto.html`
   - 1,200+ words, local SEO optimized
   - Neighborhood targeting
   - Local testimonials

### Quality Assurance Tools
1. **Manual Checklist**: `/PAGE-QUALITY-CHECKLIST.md`
   - 252-point comprehensive checklist
   - Covers SEO, psychology, conversion, technical

2. **Interactive Validator**: `/tools/page-quality-validator.html`
   - Visual checklist interface
   - Real-time scoring
   - Critical vs recommended items

3. **Automated Checker**: `/tools/automated-page-checker.html`
   - Paste HTML for instant analysis
   - References all guide documents
   - Checks 40+ quality factors
   - Provides score and recommendations

## 📋 Page Creation Workflow 2.0

1. **Choose Template**
   - Service: Use `/services/refrigerator-repair.html` as base
   - Brand: Use `/brands/lg-appliance-repair.html` as base  
   - Location: Use `/locations/downtown-toronto.html` as base

2. **Follow Guides**
   - SEO: Check `/docs/ADVANCED-SEO-GUIDE.md` for requirements
   - Marketing: Apply `/docs/MARKETING-PSYCHOLOGY-GUIDE.md` principles
   - Technical: Follow context engineering standards

3. **Quality Check**
   - Run through `/tools/automated-page-checker.html`
   - Score must be 90%+ before launch
   - Fix all critical issues
   - Address warnings if possible

4. **Final Validation**
   - Use `/tools/page-quality-validator.html` for manual check
   - Verify all phone numbers are 437-747-6737
   - Test all links and forms
   - Check mobile responsiveness

## 🎯 Project Overview

### Purpose
This guide provides comprehensive context for AI assistants, developers, and team members working on the Nika Appliance Repair website. It ensures consistency, efficiency, and proper understanding of the project structure and requirements.

### Project Goals
1. Create a professional, conversion-focused website for appliance repair services
2. Target Toronto and GTA market
3. Generate leads through online bookings and phone calls
4. Build trust through professional design and clear information
5. Optimize for local SEO and mobile users

### Business Context
- **Company**: Nika Appliance Repair
- **Industry**: Home appliance repair services
- **Service Area**: Toronto and Greater Toronto Area (GTA)
- **Target Audience**: Homeowners with broken appliances needing urgent repair
- **Key Differentiators**: Same-day service, 90-day warranty, all brands, no gas appliances

## 🏗️ Project Structure

```
NikaApplianceRepair/
├── assets/                 # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images and icons
├── services/              # Service-specific pages
├── locations/             # Location/area pages
├── brands/                # Brand-specific pages
├── src/                   # Source files for build system
│   ├── components/        # Reusable components
│   ├── layouts/           # Page layouts
│   └── pages/             # Page content
├── templates/             # Page templates
├── docs/                  # Documentation
└── dist/                  # Built website (generated)
```

## 🎨 Design System

### Color Palette
```css
/* Primary Colors */
--primary-blue: #2196F3;      /* Main brand color */
--primary-yellow: #FFD600;    /* Accent/highlight color */

/* Supporting Colors */
--bright-green: #4CAF50;      /* Success, CTAs, BOOKING BUTTONS */
--hot-pink: #E91E63;         /* Urgent notices, badges */
--orange: #FF6B35;           /* Secondary accent */
--purple: #7B1FA2;           /* Feature highlights, CALL BUTTONS */
--cyan: #00BCD4;             /* Additional accent */

/* Neutrals */
--dark: #1A237E;             /* Dark blue for contrast */
--gray-900: #212121;         /* Main text */
--gray-700: #616161;         /* Secondary text */
--gray-500: #9E9E9E;         /* Muted text */
--gray-300: #E0E0E0;         /* Borders */
--gray-100: #F5F5F5;         /* Light backgrounds */
--white: #FFFFFF;            /* Primary background */
```

### Button Color Standards
**IMPORTANT**: Use these colors consistently across all pages:
- **Book/Schedule Buttons**: Green (#4CAF50 / --bright-green)
  - Examples: "Book Now", "Schedule Service", "Book Appointment"
  - Icon: Calendar icon 📅
- **Call Buttons**: Purple (#7B1FA2 / --purple)
  - Examples: "Call Now", phone number CTAs
  - Icon: Phone icon 📞
- **Box Shadows**: Match the button color with appropriate opacity
  - Green buttons: `box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3)`
  - Purple buttons: `box-shadow: 0 5px 15px rgba(123, 31, 162, 0.3)`

### Typography
```css
/* Font Families */
--font-heading: 'Fredoka', cursive;    /* Playful, friendly headings */
--font-body: 'Rubik', sans-serif;      /* Clean, readable body text */

/* Font Sizes */
- Hero titles: 3.5rem
- Section headings: 2.5rem
- Subheadings: 1.5rem
- Body text: 1rem
- Small text: 0.875rem
```

### Design Principles
1. **Colorful & Approachable**: Use bright colors to appear friendly, not corporate
2. **Trust Building**: Professional layout with trust signals (warranty, reviews, badges)
3. **Action-Oriented**: Multiple CTAs, easy booking process
4. **Mobile-First**: Responsive design that works on all devices
5. **Fast Loading**: Optimized assets, minimal dependencies
6. **Consistent Blue Backgrounds**: Use `var(--primary-blue)` for major sections like Hero, "Why Our Service is Better", etc. This creates visual consistency and brand recognition

## 📋 Content Guidelines

### Tone of Voice
- **Friendly**: Approachable, not intimidating
- **Professional**: Competent and reliable
- **Urgent**: Emphasize same-day service
- **Clear**: No technical jargon
- **Local**: Reference Toronto/GTA frequently

### Key Messages
1. "Same-day service available"
2. "Licensed and insured technicians"
3. "90-day warranty on all repairs"
4. "$40 OFF for new customers"
5. "All major brands serviced"
6. "NO GAS APPLIANCES" (safety policy)

### Customer Statistics (Use Consistently)
**IMPORTANT**: Always use these exact numbers throughout the website:
- **Happy Clients**: 5,200+
- **Reviews**: 250+
- **Years in Business**: 5+
- **Service Areas**: 50+
- **Average Response Time**: 5 minutes
- **Customer Satisfaction**: 98%

These numbers should be consistent across all pages, sections, and marketing materials.

### SEO Keywords
- Primary: "appliance repair Toronto", "appliance repair near me"
- Service-specific: "[appliance] repair Toronto"
- Location-specific: "appliance repair [neighborhood]"
- Brand-specific: "[brand] appliance repair Toronto"

## 🔧 Technical Specifications

### Technology Stack
- **Frontend**: Pure HTML5, CSS3, Vanilla JavaScript ES6+ (no frameworks)
- **HTML**: Latest HTML5 semantic elements
- **CSS**: Modern CSS3 with Grid, Flexbox, Custom Properties, Animations
- **JavaScript**: Vanilla ES6+ with modern DOM APIs, no jQuery or libraries
- **Build System**: Node.js-based static site generator
- **Server**: Any static file server (Python, Node.js http-server)
- **Version Control**: Git

### Modern Web Standards
- **No Dependencies**: 100% vanilla code, no Bootstrap, no jQuery
- **Progressive Enhancement**: Works without JavaScript
- **Web APIs**: Using latest browser APIs (Intersection Observer, etc.)
- **CSS Features**: Using latest CSS features with fallbacks
- **ES6+ JavaScript**: Arrow functions, const/let, template literals, modern DOM methods

### Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Android)

### Performance Targets
- Page load: < 3 seconds
- First contentful paint: < 1.5 seconds
- Mobile score: > 90/100 (Google PageSpeed)

### Accessibility Requirements
- WCAG 2.1 Level AA compliance
- Semantic HTML structure
- Proper heading hierarchy
- Alt text for images
- Keyboard navigation support
- Color contrast ratios meeting standards

## 🧩 Component Structure

### Global Components
1. **Header** (`components/header.html`)
   - Logo
   - Navigation menu
   - Phone CTA button
   - Book Service button
   - Mobile menu toggle

2. **Footer** (`components/footer.html`)
   - Service links
   - Location links
   - Contact information
   - Business hours
   - Copyright notice

3. **Floating Elements**
   - Phone button (fixed position)
   - Chat widget (bottom right)

### Page Sections
1. **Hero Section**
   - Title with gradient text
   - Booking form (right side)
   - Trust indicators
   - Emergency notice

2. **Trust Bar**
   - 4 key benefits with icons
   - Responsive grid layout

3. **Services Grid**
   - 6 main services
   - Icon + title + description
   - Link to service page

4. **Testimonials**
   - Customer reviews
   - Star ratings
   - Name and location

5. **FAQ Section**
   - Expandable questions
   - Common concerns addressed

## 🚀 Development Workflow

### Adding New Pages
1. Create HTML file in appropriate directory
2. Use `page-template.html` as starting point
3. Include standard header/footer
4. Maintain consistent styling
5. Add to navigation if needed
6. Update sitemap.xml

### Code Standards
```javascript
// JavaScript
- Use ES6+ features
- Descriptive variable names
- Comment complex logic
- Handle errors gracefully

// CSS
- Use CSS variables for colors
- Mobile-first approach
- BEM naming convention where applicable
- Group related properties

// HTML
- Semantic elements
- Proper indentation
- Comments for sections
- Valid markup (W3C)
```

### Git Commit Messages
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

## 📊 Business Logic

### Service Areas
- **Primary**: Toronto (all districts)
- **Secondary**: GTA municipalities
- **Coverage**: ~30 cities/areas total
- **Response Time**: 45 minutes average

### Pricing Structure
- Diagnostic fee: $119 (waived with repair)
- $40 OFF promotion for new customers
- Transparent pricing before work begins
- 90-day warranty included

### Services Offered
1. Refrigerator Repair (electric only)
2. Washer Repair (all types)
3. Dryer Repair (electric only)
4. Dishwasher Repair (all types)
5. Oven Repair (electric only)
6. Stove/Cooktop Repair (electric only)
7. Freezer Repair (all types)

**IMPORTANT**: NO GAS APPLIANCES

### Booking Process
1. Customer fills form or calls
2. Service scheduled (same-day available)
3. Technician arrives with parts
4. Diagnosis and quote provided
5. Repair completed if approved
6. 90-day warranty begins

## 🔍 Common Tasks

### Update Phone Number
1. Search all files for: (555) 123-4567
2. Replace with new number
3. Update in:
   - Header component
   - Footer component
   - Hero section
   - Contact sections
   - CTAs

### Add New Service
1. Create page in `/services/`
2. Add to navigation menu
3. Update service grid on homepage
4. Add to footer links
5. Update sitemap

### Add New Location
1. Create page in `/locations/`
2. Add to areas grid
3. Update service area lists
4. Add local content/keywords

## 🔍 SEO Strategy

### Technical SEO
1. **Implemented**:
   - robots.txt with sitemap reference
   - XML sitemap with priority pages
   - Semantic HTML structure
   - Meta descriptions on all pages
   - Mobile-responsive design
   - Fast loading times

2. **Schema Markup** (To be added):
   ```json
   {
     "@type": "LocalBusiness",
     "name": "Nika Appliance Repair",
     "image": "logo.png",
     "telephone": "+15551234567",
     "address": {
       "@type": "PostalAddress",
       "addressLocality": "Toronto",
       "addressRegion": "ON",
       "addressCountry": "CA"
     },
     "geo": {
       "@type": "GeoCoordinates",
       "latitude": 43.653226,
       "longitude": -79.383184
     },
     "openingHours": "Mo-Fr 08:00-20:00,Sa 09:00-18:00,Su 10:00-17:00",
     "priceRange": "$$"
   }
   ```

3. **URL Structure**:
   - Services: `/services/[appliance]-repair`
   - Locations: `/locations/[area-name]`
   - Brands: `/brands/[brand-name]-repair`

### On-Page SEO
1. **Title Tags Formula**:
   - Homepage: "Appliance Repair Toronto | Same Day Service | $40 OFF - Nika"
   - Service: "[Appliance] Repair Toronto | Licensed & Insured - Nika"
   - Location: "Appliance Repair [Area] | Same Day Service - Nika"
   - Brand: "[Brand] Appliance Repair Toronto | Authorized Service - Nika"

2. **Meta Descriptions**:
   - Include: Service, area, urgency, phone number
   - Length: 150-160 characters
   - Call-to-action focused

3. **Header Structure**:
   - H1: One per page, keyword-rich
   - H2: Section headers
   - H3: Subsections

## 💰 Google Ads Strategy

### Campaign Structure
1. **Search Campaigns**:
   - Brand campaign (Nika Appliance Repair)
   - Service campaigns (per appliance type)
   - Competitor campaigns
   - Emergency/urgent campaigns

2. **Ad Copy Templates**:
   ```
   Headline 1: [Appliance] Repair Toronto
   Headline 2: Same Day Service - $40 OFF
   Headline 3: Licensed Technicians
   Description 1: 90-day warranty. All brands. 45min response.
   Description 2: Call now: (555) 123-4567
   ```

3. **Landing Page Requirements**:
   - Match ad copy exactly
   - Above-fold booking form
   - Trust signals visible
   - Mobile-optimized
   - Fast loading (< 3s)

4. **Conversion Tracking**:
   - Phone calls (duration > 60s)
   - Form submissions
   - Click-to-call buttons
   - Chat initiations

## 📈 Conversion Optimization

### Conversion Elements
1. **Trust Signals**:
   - "Licensed & Insured" badges
   - "90-day warranty" prominently displayed
   - Customer testimonials with locations
   - "10,000+ customers served"
   - Security badges near forms

2. **Urgency Creators**:
   - "Same-day service available"
   - "$40 OFF - Today Only"
   - Countdown timers
   - "Only 2 slots left today"
   - Emergency service messaging

3. **Friction Reducers**:
   - Simplified booking form
   - Auto-detect location
   - Multiple contact options
   - Clear pricing information
   - FAQ section

### Smart Popups
Located in: `/templates/popup-templates.html`

1. **Exit Intent Popup**:
   - Triggers when user moves to leave
   - Offers additional discount
   - Creates urgency with countdown

2. **Time-Based Popup**:
   - Shows after 30 seconds
   - Offers free diagnostic

3. **Scroll-Based Popup**:
   - Triggers at 70% scroll
   - Booking reminder

### A/B Testing Priorities
1. CTA button colors (Green vs Orange)
2. Headline variations
3. Form fields (minimal vs detailed)
4. Pricing display methods
5. Trust badge placements

## 📄 Templates System

### Available Templates

1. **Service Page Template** (`/templates/service-template.html`):
   - Hero with service-specific content
   - Common problems section
   - Brand compatibility list
   - Pricing table
   - FAQ specific to appliance
   - Booking form

2. **Location Page Template**:
   - Area-specific hero
   - Local testimonials
   - Service area map
   - Response time for area
   - Neighborhood list

3. **Pricing Components** (`/templates/pricing-components.html`):
   - Service pricing tables
   - Diagnostic fee explanation
   - Warranty information
   - Payment methods accepted

4. **Interlinking Components** (`/templates/interlinking-components.html`):
   - Related services widget
   - Popular brands carousel
   - Nearby areas list
   - Recent blog posts (future)

### Using Templates
```html
<!-- Example: Creating a new service page -->
1. Copy service-template.html
2. Replace placeholders:
   - {{APPLIANCE_NAME}}
   - {{SERVICE_DESCRIPTION}}
   - {{COMMON_ISSUES}}
   - {{PRICE_RANGE}}
3. Add to navigation
4. Update sitemap
```

## 📊 Analytics & Tracking

### Key Metrics
1. **Conversion Rate**: Form submissions / visitors
2. **Call Rate**: Phone clicks / visitors  
3. **Bounce Rate**: Target < 40%
4. **Page Load Time**: Target < 3s
5. **Mobile vs Desktop**: Track separately

### Event Tracking
- Form starts
- Form completions
- Phone number clicks
- CTA button clicks
- Popup interactions
- Chat widget opens

### Goal Setup
1. Primary: Form submission
2. Secondary: Phone call (60s+)
3. Micro: Email clicks
4. Engagement: Time on site > 2min

## 🚀 Growth Tactics

### Local SEO
1. Google My Business optimization
2. Local directory submissions
3. Review generation system
4. Location-specific content
5. Local backlink building

### Content Strategy
1. **Service Pages**: Detailed, problem-solving focused
2. **Location Pages**: Area guides, local testimonials
3. **Brand Pages**: Authorized service messaging
4. **Blog** (Future): How-to guides, maintenance tips

### Conversion Boosters
1. Live chat widget
2. SMS booking option
3. Online scheduling system
4. Review display widget
5. Price calculator tool

## 🎯 Performance Benchmarks

### Target Metrics
- **Organic Traffic**: 5,000+ monthly visitors
- **Conversion Rate**: 5-8% (form + calls)
- **Average Position**: Top 3 for main keywords
- **Page Speed**: 90+ mobile score
- **Quality Score**: 7+ for Google Ads

### Competitor Benchmarks
- Track top 3 competitors
- Monitor their ad copy
- Analyze their landing pages
- Track ranking changes
- Review their offers



### Design Decisions
- **Colorful Design**: Intentionally playful to stand out from corporate competitors
- **Multiple CTAs**: Maximize conversion opportunities
- **Booking Form in Hero**: Capture leads immediately
- **No Gas Appliances**: Safety/liability decision - clearly communicated

### Future Enhancements
1. Online payment integration
2. Customer portal for tracking
3. Live chat implementation
4. Review system integration
5. Email marketing automation
6. SMS notifications
7. Multi-language support (French)

### Known Limitations
1. Static site (no backend currently)
2. Form submissions need backend integration
3. No real-time availability checking
4. Manual content updates required

## 📞 Support & Resources

### Key Contacts
- Developer documentation: `/docs/`
- Design assets: `/assets/`
- Build instructions: `LOCAL-SETUP.md`
- Quick start: `RUN-WEBSITE.bat`

### External Resources
- Google Fonts: Fredoka, Rubik
- Icons: SVG inline icons
- Analytics: [To be added]
- Form handler: [To be configured]

---

## 🤖 AI Assistant Instructions

When working on this project:

1. **Maintain Consistency**
   - Use established color variables
   - Follow typography system
   - Keep playful but professional tone
   - Respect the no-gas-appliances policy

2. **Optimize for Conversion**
   - Add clear CTAs
   - Reduce friction in booking process
   - Build trust with badges/testimonials
   - Emphasize urgency (same-day service)

3. **Consider Local SEO**
   - Use Toronto/GTA references
   - Include neighborhood names
   - Add local schema markup
   - Create location-specific content

4. **Preserve Performance**
   - Minimize external dependencies
   - Optimize images
   - Use efficient CSS/JS
   - Test on mobile devices

5. **Follow Patterns**
   - Use existing components
   - Maintain file structure
   - Follow naming conventions
   - Document changes

This guide should be updated as the project evolves to maintain accuracy and usefulness.# CONTEXT ENGINEERING GUIDE

## Project Overview
Nika Appliance Repair is a professional appliance repair service website serving Toronto & GTA.

## Key Requirements

### Language
- **ALL content MUST be in English only**
- No mixed languages in any part of the website
- All UI elements, buttons, text, and labels in English

### Responsive Design Requirements
- **Desktop**: 1920px, 1440px, 1366px, 1280px
- **Laptop**: 1024px, 1366px
- **Tablet**: 768px (iPad), 834px (iPad Pro), 820px (iPad Air)
- **Mobile**: 375px (iPhone), 390px, 414px, 428px (Pro Max)

### Browser Compatibility
- Chrome (latest 3 versions)
- Firefox (latest 3 versions)
- Safari (latest 3 versions)
- Edge (latest 3 versions)

### Design Principles
1. **Mobile-First Approach**: Design for mobile, then scale up
2. **Flexible Grid System**: Use CSS Grid and Flexbox
3. **Fluid Typography**: Use rem/em units, clamp() for responsive text
4. **Responsive Images**: Use srcset, picture elements, and proper aspect ratios
5. **Touch-Friendly**: Minimum 44px touch targets on mobile
6. **Performance**: Optimize for fast loading on all devices

### CSS Best Practices
- Use CSS custom properties (variables) for consistent theming
- Implement proper media queries for all breakpoints
- Use min-width for mobile-first media queries
- Ensure proper viewport meta tag
- Test on real devices, not just browser dev tools

### Testing Checklist
- [ ] All text is in English
- [ ] Layout works on all screen sizes
- [ ] No horizontal scrolling on mobile
- [ ] Touch targets are appropriately sized
- [ ] Images scale properly
- [ ] Text is readable at all sizes
- [ ] Forms are usable on mobile
- [ ] Navigation works on all devices

## Page Structure Updates

### Current Homepage Layout (Top to Bottom)
1. **Top Banner** - Yellow background with special offer ($119 service call)
2. **Main Header** - Sticky navigation with logo, menu, and CTAs
3. **Appliances Banner** - Blue background with floating appliance icons and "WOW!" message
4. **Special Offer Banner** - Orange-pink gradient with repeated offer message
5. **Countdown Section** - White background with $40 savings offer and countdown timer
6. **Services Grid** - 6 main appliance repair services
7. **CTA Section** - Book and Call buttons
8. **Why Choose Us** - 6 benefit cards with blue icons
9. **Brands Section** - Licensed brands we service
10. **Additional sections** - Testimonials, footer, etc.

### Important Design Notes
- **Banner Colors**: Top banner uses yellow (#FFD600), special offer banner uses orange-pink gradient (#FF6B35 to #F72585)
- **Countdown Timer**: Red boxes (#DC2626) with white text
- **Floating Icons**: 8 unique appliance icons with chaotic animations
- **No Duplicate Content**: Each appliance type appears only once in floating icons
- **Responsive Design**: Header collapses to mobile menu, floating icons hide on mobile