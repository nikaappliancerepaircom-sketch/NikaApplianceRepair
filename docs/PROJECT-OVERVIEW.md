# Nika Appliance Repair - Project Overview & Guidelines

## 🎯 Project Vision
Transform the appliance repair service website into a high-converting, SEO-optimized platform that dominates local search results and delivers exceptional ROI on Google Ads campaigns in Toronto and the Greater Toronto Area (GTA).

## 📍 Service Location
**Primary Market:** Toronto and Greater Toronto Area (GTA)
- Same coverage areas as nappliancerepair.ca
- Focus on all major Toronto neighborhoods and GTA municipalities

## 📁 Project Structure
```
NikaApplianceRepair/
├── index.html              # Homepage
├── assets/                 # All static assets
│   ├── css/
│   │   ├── main.css       # Main stylesheet
│   │   ├── mobile.css     # Mobile-specific styles
│   │   └── print.css      # Print styles
│   ├── js/
│   │   ├── main.js        # Main JavaScript
│   │   ├── forms.js       # Form handling
│   │   └── analytics.js   # Tracking code
│   └── images/
│       ├── icons/         # Service & UI icons
│       ├── hero/          # Hero images
│       └── brands/        # Brand logos
├── services/              # Service pages
│   ├── index.html         # Services overview
│   ├── refrigerator-repair.html
│   ├── washer-repair.html
│   ├── dryer-repair.html
│   ├── dishwasher-repair.html
│   ├── oven-repair.html
│   └── microwave-repair.html
├── locations/             # Location pages
│   ├── index.html         # Locations overview
│   ├── downtown.html
│   ├── north-side.html
│   ├── south-side.html
│   ├── east-side.html
│   └── west-side.html
├── brands/                # Brand pages
│   ├── index.html         # Brands overview
│   ├── samsung-repair.html
│   ├── lg-repair.html
│   ├── whirlpool-repair.html
│   ├── ge-repair.html
│   └── maytag-repair.html
├── templates/             # Page templates
│   ├── service-template.html
│   ├── location-template.html
│   └── brand-template.html
├── about.html
├── contact.html
├── emergency.html
├── pricing.html
├── reviews.html
├── sitemap.xml
├── robots.txt
└── docs/                  # Documentation
    ├── PROJECT-OVERVIEW.md
    ├── SEO-GUIDELINES.md
    ├── GOOGLE-ADS-GUIDE.md
    └── STYLE-GUIDE.md
```
## 🎨 Design System

### Color Palette
```css
:root {
  /* Primary Colors */
  --primary: #0ea5e9;        /* Sky Blue - Trust, reliability */
  --primary-dark: #0284c7;   /* Darker blue for hover states */
  --primary-light: #38bdf8;  /* Lighter blue for backgrounds */
  
  /* Secondary Colors */
  --secondary: #f59e0b;      /* Amber - CTAs, urgency */
  --secondary-dark: #d97706; /* Darker amber for hover */
  
  /* Status Colors */
  --success: #22c55e;        /* Green - Available, success */
  --warning: #f59e0b;        /* Orange - Attention */
  --danger: #ef4444;         /* Red - Emergency, urgent */
  
  /* Neutral Colors */
  --dark: #0f172a;           /* Near black - Text */
  --gray-900: #1e293b;       /* Headings */
  --gray-700: #334155;       /* Subheadings */
  --gray-500: #64748b;       /* Body text */
  --gray-300: #cbd5e1;       /* Borders */
  --gray-100: #f1f5f9;       /* Backgrounds */
  --light: #f8fafc;          /* Light backgrounds */
  --white: #ffffff;          /* Pure white */
}
```
### Typography System
```css
/* Font Stack */
--font-sans: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;

/* Font Sizes - Mobile First */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */

/* Responsive Typography */
@media (min-width: 768px) {
  --text-4xl: 2.5rem;
  --text-5xl: 3.5rem;
}

@media (min-width: 1024px) {
  --text-4xl: 3rem;
  --text-5xl: 4rem;
}
```
## 📄 Page Section Requirements

### Homepage (12-14 Sections)
1. **Emergency Bar** - "24/7 Emergency Service Available"
2. **Navigation** - Sticky header with phone CTA
3. **Hero Section** - Headline + Form + Trust badges
4. **Trust Bar** - 4 key trust signals
5. **Services Grid** - 6 main services with icons
6. **Process Steps** - How it works (4 steps)
7. **Brands Section** - "We service all major brands"
8. **Why Choose Us** - Unique value propositions
9. **Testimonials Slider** - Recent reviews
10. **Service Areas** - Interactive map or list
11. **FAQ Section** - Common questions
12. **CTA Section** - Final conversion push
13. **Footer** - Complete sitemap + contact
14. **Floating Elements** - Phone + Chat buttons

### Service Pages (10-12 Sections)
1. **Navigation** - With emergency banner
2. **Service Hero** - H1 + Quick form + Image
3. **Problem Identifier** - "Common issues we fix"
4. **Trust Signals** - Certifications + Reviews
5. **Service Process** - Specific to appliance
6. **Pricing Guide** - Transparent pricing
7. **Brand Compatibility** - Brands we service
8. **FAQs** - Service-specific questions
9. **Related Services** - Cross-sell opportunities
10. **Local Reviews** - Service-specific testimonials
11. **Emergency CTA** - Urgency messaging
12. **Footer** - Navigation + trust
### Location Pages (8-10 Sections)
1. **Navigation** - Local phone number
2. **Local Hero** - "Appliance Repair in [Area]"
3. **Service Area Map** - Coverage visualization
4. **Available Services** - All 6 services
5. **Local Trust** - Area-specific reviews
6. **Response Times** - "Average arrival: X minutes"
7. **Local Team** - Technician profiles
8. **Parking/Access** - Location-specific info
9. **Recent Jobs** - "Recently completed in area"
10. **Footer** - Local-focused links

### Brand Pages (8-10 Sections)
1. **Navigation** - Brand-specific messaging
2. **Brand Hero** - "[Brand] Appliance Repair Experts"
3. **Authorization Badges** - Official certifications
4. **Model Coverage** - Supported models list
5. **Common Issues** - Brand-specific problems
6. **Repair Process** - Brand considerations
7. **Parts Availability** - Genuine parts info
8. **Brand Reviews** - Model-specific testimonials
9. **Other Brands** - Cross-linking
10. **Footer** - Standard navigation

### Emergency Page (6-8 Sections)
1. **Urgent Header** - Red emergency banner
2. **Hero** - Direct call + availability
3. **Common Emergencies** - Quick identifier
4. **Immediate Actions** - What to do now
5. **Live Availability** - Real-time slots
6. **Emergency Pricing** - Transparent costs
7. **Trust Urgency** - "Licensed for emergencies"
8. **Footer** - Emergency contact focus
## 🎨 Design Assets

### Logo System
- **Primary Logo**: Full horizontal version with icon + text
- **Compact Logo**: Icon only for mobile/favicon
- **Inverse Logo**: White version for dark backgrounds
- **Dimensions**: 300x80px (primary), 80x80px (icon only)
- **File Formats**: SVG (primary), PNG (backup), ICO (favicon)

### Service Icons (SVG)
- Refrigerator: Minimalist fridge with door line
- Washer: Front-load with circular window
- Dryer: Square with circular drum
- Dishwasher: Rack system visible
- Oven/Range: Burners on top
- Microwave: Rectangle with control panel

### Trust Badges
- Licensed & Insured: Star shield design
- BBB A+ Rating: Official style badge
- 90-Day Warranty: Hexagon seal
- Same Day Service: Clock emphasis
- 24/7 Emergency: Red urgent styling
- 5-Star Reviews: Rating display

## 📝 Unified Forms System

### Form Types
1. **Quick Quote Form** (3-4 fields)
   - Name, Phone, Appliance Type
   - Used in: Hero sections, sidebars, popups
   
2. **Detailed Booking Form** (Multi-step)
   - Contact Info → Address → Service Details → Schedule
   - Used in: Booking page, service pages
   
3. **Emergency Contact Form** (2 fields)
   - Phone + Issue (optional)
   - Used in: Emergency page, urgent popups

### Form Features
- Real-time validation
- Auto-formatting (phone numbers)
- Progress indicators
- Success animations
- Error handling
- Mobile optimized keyboards
## ⚡ Dynamic Elements

### Urgency Systems
1. **Live Availability Widget**
   - Real-time technician slots
   - Updates every 60 seconds
   - Color coding (red/yellow/green)
   
2. **Countdown Timers**
   - Offer expiration
   - Next available slot
   - Business hours closing
   
3. **Recent Activity Feed**
   - "John in Lincoln Park booked 5 min ago"
   - Randomized but realistic
   - Location-aware
   
4. **Dynamic Pricing**
   - Time-of-day adjustments
   - Demand-based messaging
   - Seasonal variations

### Mobile Menu Features
- Slide-in from right
- Full-screen overlay
- Touch gestures support
- Accordion for submenus
- Click-to-call prominent
- Smooth animations
- Accessibility compliant

## 🔧 JavaScript Modules

### Core Modules Created
1. **main.js** - Core functionality
2. **form-system.js** - Unified form handling
3. **popup-system.js** - Smart popups
4. **urgency-system.js** - Dynamic urgency
5. **mobile-menu.js** - Mobile navigation

### Additional Modules Needed
- **analytics.js** - Event tracking
- **reviews.js** - Review display
- **booking.js** - Appointment system
- **chat.js** - Live chat integration
- **maps.js** - Service area maps
## 🎯 Smart Popup Strategy (Max 2 Per Session)

### Popup Logic Rules
- **Maximum 2 popups per session** (not per page)
- **Never show 2 popups simultaneously**
- **Minimum 30 seconds between popups**
- **Focus: Phone calls & online booking only**
- **No email capture or lead magnets**

### Primary Popup (1st Popup)
**Exit Intent Popup** - Highest conversion potential
- Triggers when mouse leaves viewport
- Shows discount or urgency message
- Direct CTA: "Call Now" or "Book Online"
- Suppressed if user already called/booked

### Secondary Popup (2nd Popup)
**Smart Contextual Popup** - Based on user behavior
Choose ONE based on context:

1. **Time-Based Helper** (30+ seconds on page)
   - "Need help? Technician available now"
   - Shows on service/pricing pages
   
2. **Scroll-Based Offer** (75% scroll on long pages)
   - "You made it this far - here's $30 off"
   - Shows on detailed content pages
   
3. **Mobile Touch-to-Call** (mobile only + engaged)
   - "Tap to call - Skip the reading"
   - Bottom sheet design

4. **Abandonment Preventer** (form started but not submitted)
   - "Having trouble? We'll call you!"
   - Reverse callback option
### Popup Session Management
```javascript
// Session tracking
sessionStorage.setItem('popupsShown', JSON.stringify([
    {type: 'exitIntent', timestamp: 1234567890},
    {type: 'timeHelper', timestamp: 1234567920}
]));

// Conversion tracking
sessionStorage.setItem('hasConverted', 'true');
```

### Popup Decision Flow
1. **Check eligibility**: Has user seen 2 popups? → Stop
2. **Check conversion**: Has user called/booked? → Stop
3. **Check timing**: 30+ seconds since last popup? → Continue
4. **Check context**: Which popup fits current behavior?
5. **Show popup**: Track in session, prevent overlap

### Popup Content Focus
- **NO email capture forms**
- **NO newsletter signups**
- **NO free guides/downloads**
- **ONLY phone calls and bookings**
- **Clear value proposition**
- **Single primary CTA**

### Analytics Tracking
```javascript
// Track popup performance
gtag('event', 'popup_display', {
    'popup_type': 'exit_intent',
    'popup_number': 1, // First or second
    'page': window.location.pathname,
    'time_on_page': 45
});

// Track conversions
gtag('event', 'popup_conversion', {
    'popup_type': 'exit_intent',
    'conversion_type': 'phone_call', // or 'booking'
    'popup_number': 1
});
```
## 💰 Pricing Structure

### Diagnostic Fees
- **Standard Diagnostic**: $119 (waived with repair)
- **Emergency Diagnostic**: $149 (waived with repair)
- **FREE Diagnostic**: With any repair service

### Special Offers
- **$40 OFF Any Repair Service** (new customers)
- **FREE Diagnostic** when you proceed with repair
- **90-Day Warranty** on all repairs
- **Same-Day Service** at no extra charge

### Service Pricing Ranges
- **Refrigerator Repair**: $150-$400
- **Washer Repair**: $120-$350
- **Dryer Repair**: $100-$300
- **Dishwasher Repair**: $120-$350
- **Oven/Range Repair**: $150-$400
- **Freezer Repair**: $150-$400

### Services We Offer
✅ **Refrigerator Repair** - All types and models
✅ **Washer/Washing Machine Repair** - Top-load, front-load, stackable
✅ **Dryer Repair** - Electric dryers only
✅ **Dishwasher Repair** - Built-in, portable, countertop
✅ **Oven Repair** - Electric ovens only
✅ **Stove/Cooktop Repair** - Electric only
✅ **Freezer Repair** - Standalone and chest freezers

### Services We DON'T Offer
- ❌ **Gas Appliance Repair** (NO gas stoves, ovens, or dryers - safety liability)
- ❌ **Microwave Repair** (not cost-effective)
- ❌ **Small Appliance Repair** (toasters, blenders, etc.)
- ❌ **Window AC Units** (specialized service)
- ❌ **Commercial Equipment** (focus on residential only)

### Transparent Pricing Policy
- Upfront pricing before work begins
- No hidden fees or charges
- Price includes parts and labor
- Payment due upon completion
- Accept: Cash, Check, Credit Cards

### Price Comparison Advantage
- Average competitor diagnostic: $150-200
- Our diagnostic: $119 (FREE with repair)
- Competitor repair discount: $20-25
- Our repair discount: $40 OFF
- Total savings: Up to $120
### Pricing Psychology Implementation

#### Price Anchoring Display
```
❌ Replacement Cost: $1,299
❌ Other Companies: $350 + $150 diagnostic
✅ Our Price: $279 (includes FREE diagnostic)
💰 You Save: $1,020 vs replacement!
```

#### Value Stacking
1. Expert Repair Service ($279 value)
2. FREE Diagnostic ($119 value)
3. $40 OFF Discount (limited time)
4. 90-Day Warranty ($99 value)
5. Same-Day Service ($75 value)
Total Value: $612
Your Price: $239 ✨

#### Urgency Pricing Messages
- "Today Only: FREE Diagnostic (Save $119)"
- "Book Now: Lock in $40 OFF discount"
- "Price increases tomorrow at midnight"
- "Only 2 slots left at this price"

#### Trust Through Transparency
- Show price breakdown (labor + parts)
- Compare to competitor pricing
- Highlight savings vs replacement
- Display warranty value
- No surprise fees guarantee

## 🎯 Competitor Differentiation

### vs. Nick's Appliance Repair (nappliancerepair.ca)
**Our Advantages:**
- Lower diagnostic fee ($119 vs $150+)
- Bigger discount ($40 vs $20-30)
- Clearer pricing structure
- Better online booking system
- More trust signals

### Service Advantages
- Same-day service standard
- 90-day warranty (vs 30-60 days)
- Licensed & insured techs
- No gas appliance liability
- Focus on major appliances only

## 📍 Service Areas (Toronto & GTA)

### Toronto Neighborhoods
- Downtown Toronto
- North York
- Etobicoke
- Scarborough
- East York
- York

### Primary GTA Cities
- **Ajax** - Eastern coverage
- **Aurora** - Northern service area
- **Brampton** - Western region
- **Burlington** - Southwest coverage
- **Markham** - Northeast sector
- **Mississauga** - Major western hub
- **Newmarket** - Northern boundary
- **Oakville** - Southwest luxury market
- **Oshawa** - Eastern boundary
- **Pickering** - Eastern coverage
- **Richmond Hill** - Northern sector
- **Vaughan** - Northwest region
- **Whitby** - Eastern service area

### Extended Service Areas
- Bradford, Stouffville, Thornhill, Unionville
- Uxbridge, Woodbridge, Hamilton, Orangeville
- East Gwillimbury, Georgina, Halton Hills, King
- Milton, Caledon, Gormley, Holland Landing
- Innisfil, Langstaff, Oak Ridges

### Contact Information
- **Phone:** (555) 123-4567 (to be updated)
- **Email:** info@nikaappliancerepair.com
- **Service Hours:** Mon-Sun 8AM-8PM
- **Emergency Service:** 24/7

## 🏷️ Brands We Service
We repair all major appliance brands including but not limited to:

### Premium Brands
- **Sub-Zero** - High-end refrigeration
- **Viking** - Professional-grade appliances
- **Wolf** - Luxury cooking appliances
- **Thermador** - Premium kitchen appliances
- **Miele** - German engineering
- **Bosch** - European quality
- **Gaggenau** - Ultra-luxury appliances

### Popular Brands
- **Samsung** - Korean innovation
- **LG** - Smart appliances
- **Whirlpool** - American reliability
- **GE (General Electric)** - Trusted household name
- **Maytag** - Dependable performance
- **KitchenAid** - Professional style
- **Frigidaire** - Affordable quality
- **Electrolux** - Swedish design

### Value Brands
- **Kenmore** (Sears) - Store brand quality
- **Amana** - Basic reliability
- **Hotpoint** - Budget-friendly
- **Inglis** - Canadian brand
- **Danby** - Compact specialists

### Other Brands
- Fisher & Paykel, Blomberg, Bertazzoni, Dacor, Fulgor Milano
- Jenn-Air, Liebherr, Panasonic, Asco, Brava, Cyclone
- Fhiaba, Falmec, Huebsch, Moffat, White Westinghouse
- Zephyr, and many more (90+ brands total)
## 🔗 Advanced Interlinking System

### Interlinking Architecture
**Hub & Spoke Model** - Strategic link flow for maximum authority
```
HOME → Service Hubs → Problem Pages → Solutions
     → Location Hubs → Neighborhood Pages → Local Services  
     → Brand Hubs → Model Pages → Specific Repairs
```

### Link Distribution Strategy
- **Service Pages**: 8-12 internal links per page
- **Location Pages**: 6-10 internal links per page
- **Support Pages**: 10-15 internal links per page
- **Homepage**: 20-30 strategic links to main hubs

### Anchor Text Rules
- Exact Match: 15-20% ("refrigerator repair")
- Partial Match: 30-35% ("expert refrigerator repair")
- Branded: 10-15% ("Nika appliance experts")
- Natural: 30-40% ("fix your appliance today")

### Automated Link Components
1. **Related Services Widget** - On every service page
2. **Location Breadcrumbs** - Dynamic navigation
3. **Smart Footer** - Contextual links based on current page
4. **Problem/Solution Links** - Auto-link related issues
5. **Brand Cross-Links** - Connect brands to services

### Priority Link Paths
1. **Emergency Path**: Every page → Emergency service (max 2 clicks)
2. **Conversion Path**: Problem → Service → Location → Contact
3. **Trust Path**: Service → Reviews → About → Contact
4. **Local Path**: Location → Services in Area → Book Now

### Link Equity Flow
- Tier 1 (Most links): Homepage, main services, primary locations
- Tier 2 (Moderate): Brand pages, sub-locations, common problems
- Tier 3 (Fewer): Blog posts, FAQs, about pages

### Implementation Phases
1. **Week 1**: Build core structure and templates
2. **Week 2**: Create 30+ interlinked content pages
3. **Week 3**: Add contextual links throughout
4. **Week 4**: Optimize and audit link distribution
## 🔗 Critical Interlinking Requirements

### Must-Have Link Structure
Every page MUST include these essential links:

#### 1. Navigation Links (Header/Footer)
- Homepage
- All 6 main services
- Emergency service
- Primary locations (5)
- Phone number (clickable)

#### 2. Contextual Links (In Content)
**Service Pages Must Link To:**
- 2-3 related services
- 2 location pages
- 2-3 common problems
- 1 emergency page
- 1-2 relevant brands

**Location Pages Must Link To:**
- All 6 services (with location modifier)
- Neighboring locations
- Emergency service
- Recent reviews

**Problem Pages Must Link To:**
- Parent service page
- Related problems (2-3)
- Relevant brand if applicable
- Emergency service if urgent

#### 3. Automated Link Blocks
```html
<!-- Required on EVERY page -->
<nav class="breadcrumbs">[Dynamic breadcrumb trail]</nav>

<!-- Required on SERVICE pages -->
<div class="related-services">[3 related services]</div>

<!-- Required on LOCATION pages -->
<div class="services-in-area">[All 6 services for this area]</div>

<!-- Required in FOOTER -->
<div class="footer-links">[Contextual links based on current page]</div>
```

### Link Rules
- **Max Click Depth**: 3 clicks from homepage
- **Emergency Access**: 2 clicks maximum from any page
- **Orphan Pages**: ZERO (every page must have incoming links)
- **Link Density**: 8-12 internal links per 1000 words
- **Anchor Text**: Vary between exact, partial, and natural

### Priority Linking Paths
1. **Money Path**: Problem → Service → Location → Contact
2. **Trust Path**: Service → Reviews → About → Contact  
3. **Emergency Path**: Any Page → Emergency (max 2 clicks)
4. **Local Path**: Location → Local Services → Book Now