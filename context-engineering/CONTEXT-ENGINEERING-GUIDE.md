# Context Engineering Master Guide - Nika Appliance Repair

## 🎯 Overview
This guide contains all design decisions, patterns, and requirements for the Nika Appliance Repair website. All new pages and features MUST follow these guidelines.

## 📁 Project Structure
```
NikaApplianceRepair/
├── index.html              # Homepage
├── css/                    # Stylesheets
│   ├── style.css          # Main styles
│   └── [other].css        # Component styles
├── js/                     # JavaScript
│   ├── main.js            # Core functionality
│   └── [other].js         # Module scripts
├── brands/                 # Brand-specific pages
├── services/              # Service pages
├── locations/             # Location pages
└── context-engineering/   # Documentation
```

## 🎨 Design System

### Color Palette (MANDATORY - Use Only These)
```css
/* Primary Colors */
--primary-blue: #2196F3;
--primary-yellow: #FFD600;
--bright-green: #4CAF50;
--dark: #1A237E;

/* Background Colors - ONLY USE THESE */
--bg-white: #FFFFFF;                    /* White sections */
--bg-light-gray: #F8F9FA;              /* Alternating sections */
--bg-blue-gradient: linear-gradient(135deg, #1976D2 0%, #2196F3 50%, #1565C0 100%);
--bg-dark-blue: linear-gradient(135deg, #1A237E 0%, #3949AB 100%);
```

### Background Pattern Rules
1. **Header**: White background
2. **Hero**: Blue gradient or white
3. **Content sections**: Alternate white → light gray → white
4. **CTA sections**: Blue gradient
5. **Footer**: Dark blue gradient

### Typography
- **Headings**: Fredoka font, dark blue (#1A237E)
- **Body**: Rubik font, gray (#666)
- **Base size**: 18px (1rem)

## 🔧 Component Standards

### 1. FAQ Section
- Use accordion pattern (one open at a time)
- Dark navy color (#1A237E) for questions
- Smooth animations with max-height
- Include FAQ schema markup
- See: `faq-implementation-guide.md`

### 2. Video Testimonials
- YouTube embeds with modestbranding
- Blue gradient background for section
- White cards with video + info
- Verified badges and star ratings
- Counter animations for stats

### 3. Service Cards
- Equal height using flexbox
- Centered text alignment
- Balanced content (~35-40 words each)
- Include technology keywords
- Links to service/location pages

### 4. Psychological Triggers
**Animations:**
- urgencyPulse - urgent messages
- attentionShake - badges
- trustGlow - trust elements
- scarcityBlink - limited offers
- socialProof - testimonials
- valueHighlight - discounts

**Features:**
- Live booking notifications
- Dynamic slot availability
- Countdown timers
- Number counter animations

## 📋 Page Requirements

### All Pages Must Include:
1. **Navigation** - Sticky header with phone CTA
2. **Hero Section** - Clear H1 + trust signals
3. **Services Grid** - 6 main services
4. **Video Testimonials** - Real customer reviews
5. **FAQ Section** - Common questions
6. **Trust Elements** - Badges, warranty, certifications
7. **CTAs** - Phone and booking buttons
8. **Footer** - Complete sitemap

### Content Guidelines:
- **NO gas appliances** - Electric only
- $119 diagnostic (FREE with repair)
- $40 OFF new customers
- 90-day warranty
- Same-day service standard
- 24/7 emergency availability

## 🚀 Implementation Checklist

### For New Pages:
- [ ] Use standard background colors only
- [ ] Include all required sections
- [ ] Add FAQ with proper structure
- [ ] Include video testimonials
- [ ] Add psychological triggers
- [ ] Balance service card content
- [ ] Test all animations
- [ ] Verify mobile responsiveness
- [ ] Check FAQ functionality
- [ ] Add schema markup

### JavaScript Requirements:
- Initialize FAQs on page load
- Add counter animations for stats
- Include live notifications
- Update dynamic content (slots, time)
- Smooth scroll navigation

## 🎯 Conversion Optimization

### Key Elements:
1. **Urgency** - Limited slots, countdown timers
2. **Social Proof** - Live notifications, video reviews
3. **Trust** - Badges, warranties, certifications
4. **Value** - Highlight savings, discounts
5. **Ease** - Simple forms, clear CTAs

### Popup Strategy:
- Max 2 popups per session
- Focus on phone calls/bookings
- No email capture
- Exit intent + contextual

## 📱 Mobile Optimization
- Touch-friendly buttons (min 48px)
- Readable text (min 16px)
- Compressed images
- Fast load times
- Click-to-call buttons

## 🔗 Internal Linking
- Every page → Emergency (max 2 clicks)
- Service pages → Related services + locations
- Location pages → All services
- Brand pages → Service pages
- Breadcrumb navigation

## ⚠️ Important Notes
1. **Always check context-engineering folder before creating new features**
2. **Follow established patterns - don't create new ones**
3. **Test on mobile first**
4. **Maintain consistency across all pages**
5. **Use only approved background colors**

## 📄 Related Guides
- `background-colors-guide.md` - Color usage
- `faq-implementation-guide.md` - FAQ setup
- `PROJECT-OVERVIEW.md` - Full project details
- `SEO-GUIDELINES.md` - SEO requirements
- `STYLE-GUIDE.md` - Design standards

Last Updated: December 2024