# Context Engineering Framework - Nika Appliance Repair

## 🎯 Purpose
This document provides structured context templates and guidelines to ensure consistent, accurate content generation and development for the Nika Appliance Repair website.

## 📋 Master Context Template

### Project Identity Block
```
PROJECT: Nika Appliance Repair
MARKET: Toronto & Greater Toronto Area (GTA)
INDUSTRY: Residential Appliance Repair Services
COMPETITOR: nappliancerepair.ca (Nick's Appliance Repair)
PHONE: (555) 123-4567 [TO BE UPDATED]
WEBSITE: nikaappliancerepair.com
```

### Service Constraints Block
```
SERVICES WE OFFER:
✅ Refrigerator Repair (All electric models)
✅ Washer Repair (All types)
✅ Dryer Repair (ELECTRIC ONLY - NO GAS)
✅ Dishwasher Repair (All types)
✅ Oven Repair (ELECTRIC ONLY - NO GAS)
✅ Stove/Cooktop Repair (ELECTRIC ONLY - NO GAS)
✅ Freezer Repair (All types)

SERVICES WE DON'T OFFER:
❌ Gas Appliance Repair (Safety liability)
❌ Microwave Repair (Not cost-effective)
❌ Small Appliance Repair
❌ Commercial Equipment
❌ Window AC Units
```

### Brand Authority Block
```
BRANDS: 90+ including Samsung, LG, Whirlpool, GE, Maytag, Frigidaire, 
KitchenAid, Bosch, Sub-Zero, Viking, Wolf, Miele, Thermador, etc.
WARRANTY: 90-day on all repairs
RESPONSE: Same-day service available
HOURS: Mon-Sun 8AM-8PM, 24/7 Emergency
```

### Value Proposition Block
```
UNIQUE SELLING POINTS:
- $40 OFF any repair (competitive advantage)
- FREE diagnostic with repair ($119 value)
- Licensed & insured technicians
- Same-day service
- 90-day warranty
- NO hidden fees
- Toronto & GTA focus
```

## 🏗️ Page Generation Templates

### 1. Service Page Context Template
```
CONTEXT: Generate a service page for [APPLIANCE] repair
LOCATION: Toronto & GTA
CONSTRAINTS: 
- If oven/stove/dryer: Specify ELECTRIC ONLY, NO GAS
- Include common problems (3-5)
- Include brands we service
- Include pricing range
- Include emergency service mention
- Include $40 OFF promotion
- Include internal links to related services
- Target keywords: "[appliance] repair Toronto", "[appliance] repair near me"

TONE: Professional yet friendly, urgent but not pushy
LENGTH: 800-1200 words
SECTIONS REQUIRED:
1. Hero with headline and CTA
2. Common problems we fix
3. Our repair process
4. Brands we service
5. Pricing transparency
6. Why choose us
7. Service areas
8. FAQ (3-5 questions)
9. Final CTA
```

### 2. Location Page Context Template
```
CONTEXT: Generate location page for [CITY/AREA]
PARENT: Toronto & GTA
CONSTRAINTS:
- Mention specific neighborhoods if applicable
- Include "near me" and local keywords
- Reference actual local landmarks/areas
- Include all 7 services
- Mention same-day service
- Include testimonial from that area
- Link to nearby locations

TONE: Local, community-focused, trustworthy
LENGTH: 600-800 words
SECTIONS REQUIRED:
1. Hero: "Appliance Repair in [Location]"
2. Services available in area
3. Why choose local service
4. Response time for area
5. Recent jobs in area
6. All brands serviced
7. Book now CTA
```

### 3. Brand Page Context Template
```
CONTEXT: Generate brand page for [BRAND] appliance repair
EXPERTISE: Certified to repair all [BRAND] models
CONSTRAINTS:
- List specific model lines if premium brand
- Mention genuine parts
- Include brand-specific common issues
- Reference warranty compatibility
- Include all appliance types for brand
- NO gas models if applicable

TONE: Expert, authoritative, brand-aware
LENGTH: 700-900 words
SECTIONS REQUIRED:
1. Hero: "[BRAND] Appliance Repair Experts"
2. Models we service
3. Common [BRAND] issues
4. Genuine parts guarantee
5. Brand-specific expertise
6. Repair process
7. Service areas
8. Book repair CTA
```

## 🔧 Component Context Templates

### Navigation Context
```
PRIMARY NAV ITEMS:
- Services (Dropdown: All 7 services)
- Brands (Dropdown: Top 8 brands)
- Service Areas (Dropdown: Toronto neighborhoods + GTA cities)
- About Us
- Reviews
- Contact

CTA BUTTONS:
- Phone: (555) 123-4567
- Book Online (Green button)
```

### Form Context
```
FORM TYPES:
1. Quick Quote (Name, Phone, Appliance, Zip)
2. Detailed Booking (Multi-step)
3. Emergency Contact (Phone + Issue)

VALIDATION RULES:
- Phone: Canadian format
- Postal Code: Canadian format (A1A 1A1)
- Required fields marked with *
- Success message includes $40 OFF reminder
```

### Footer Context
```
FOOTER SECTIONS:
1. Services (All 7 with electric-only notation)
2. Top Locations (Toronto + 5 major GTA)
3. Popular Brands (Top 6)
4. Company (About, Reviews, Warranty, Contact)
5. Legal (Privacy, Terms, Sitemap)
```

## 🎨 Content Style Context

### Voice & Tone
```
BRAND VOICE:
- Professional but approachable
- Urgent without being pushy
- Local and community-focused
- Expert but not condescending
- Helpful and solution-oriented

AVOID:
- Technical jargon
- Pressure tactics
- Mentioning gas services
- Comparing directly to competitors
- Making unrealistic promises
```

### SEO Context
```
PRIMARY KEYWORDS:
- appliance repair Toronto
- [appliance] repair near me
- same day appliance repair GTA
- emergency appliance repair Toronto

LOCAL MODIFIERS:
- in Toronto
- near me
- GTA
- [specific neighborhood/city]
- same day
- emergency
- 24/7
```

## 🚀 Implementation Workflow

### Step 1: Context Loading
Before generating any content, load:
1. Master Context Template
2. Specific Page Template
3. SEO Requirements
4. Brand Voice Guidelines

### Step 2: Generation Process
1. **Input**: "Create a [PAGE TYPE] for [SPECIFIC ITEM]"
2. **Context Application**: Apply all relevant templates
3. **Constraint Check**: Verify all rules followed
4. **Output**: Complete page following structure

### Step 3: Quality Checks
- ✓ Electric-only for applicable appliances
- ✓ $40 OFF mentioned
- ✓ Local keywords included
- ✓ Internal links present
- ✓ CTA placement correct
- ✓ Brand voice consistent

## 📊 Context Hierarchy

```
Level 1: Project Identity (Always active)
    ↓
Level 2: Service Constraints (Always active)
    ↓
Level 3: Page Type Template (Specific to task)
    ↓
Level 4: SEO & Local Context (Adjust per page)
    ↓
Level 5: Component Details (As needed)
```

## 💡 Usage Examples

### Example 1: Service Page Request
```
REQUEST: "Create a washer repair service page"

CONTEXT LOADED:
- Master Context ✓
- Service Page Template ✓
- Washer-specific constraints ✓
- Toronto & GTA keywords ✓

OUTPUT: Complete washer repair page with all sections, proper keywords, 
internal links, and following brand guidelines
```

### Example 2: Location Page Request
```
REQUEST: "Create Mississauga location page"

CONTEXT LOADED:
- Master Context ✓
- Location Page Template ✓
- Mississauga neighborhoods ✓
- Local keywords ✓
- Nearby areas (Oakville, Brampton) ✓

OUTPUT: Mississauga-focused page with local relevance and area-specific content
```

## 🔄 Continuous Improvement

### Feedback Loop
1. Generate content using context
2. Review for accuracy and completeness
3. Update context templates if gaps found
4. Regenerate with improved context

### Version Control
- Current Version: 1.0
- Last Updated: January 2025
- Next Review: After first 10 pages created

## ✅ Benefits of This Framework

1. **Consistency**: Every page follows same quality standards
2. **Efficiency**: No need to re-explain requirements
3. **Accuracy**: Constraints prevent errors (no gas services)
4. **Scalability**: Easy to generate 50+ pages quickly
5. **SEO Optimization**: Built-in keyword strategy
6. **Brand Cohesion**: Unified voice across all content

---

This context engineering framework ensures that every piece of content created for Nika Appliance Repair is accurate, consistent, and optimized for both users and search engines.