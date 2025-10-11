# SEO Guidelines - Nika Appliance Repair

## 📋 SEO Checklist for Every Page

### Title Tags
- **Length**: 50-60 characters
- **Format**: [Primary Keyword] | [Secondary Keyword] | Nika Appliance
- **Include**: Location, service type, unique value prop

#### Title Tag Formulas:

**Service Pages:**
```
[Appliance] Repair in [City] | Same Day Service | Nika Appliance
Example: Refrigerator Repair in Chicago | Same Day Service | Nika Appliance
```

**Location Pages:**
```
Appliance Repair in [Location] | Fast Local Service | Nika
Example: Appliance Repair in Downtown Chicago | Fast Local Service | Nika
```

**Brand Pages:**
```
[Brand] Appliance Repair | Authorized Service | Nika Appliance
Example: Samsung Appliance Repair | Authorized Service | Nika Appliance
```

### Meta Descriptions
- **Length**: 150-160 characters
- **Include**: Call to action, phone number, key benefits
- **Format**: Problem/Solution + Benefits + CTA
## 📊 CORE WEB VITALS & USER EXPERIENCE

### Performance Metrics That Matter
1. **LCP (Largest Contentful Paint)**: < 2.5s
2. **INP (Interaction to Next Paint)**: < 200ms
3. **CLS (Cumulative Layout Shift)**: < 0.1

### Page Experience Signals
- Mobile-friendly (100% score)
- HTTPS secure
- No intrusive interstitials
- Safe browsing (no malware)

## 🔍 SEMANTIC SEO & ENTITY OPTIMIZATION

### Entity Building for Your Business
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://nikaappliancerepair.com/#organization",
  "name": "Nika Appliance Repair",
  "alternateName": ["Nika Repair", "Nika Appliance Service"],
  "description": "Professional appliance repair service in Chicago",
  "knowsAbout": [
    "Refrigerator Repair",
    "Washer Repair",
    "Dryer Repair",
    "Appliance Diagnostics",
    "Emergency Appliance Service"
  ],
  "areaServed": {
    "@type": "City",
    "name": "Chicago",
    "containsPlace": ["Downtown", "North Side", "South Side"]
  }
}
```

### Topic Clustering Strategy
Build topical authority through interconnected content:
```
Hub Page: /appliance-repair/
├── /refrigerator-repair/
│   ├── /refrigerator-not-cooling/
│   ├── /ice-maker-repair/
│   └── /refrigerator-leaking-water/
├── /washer-repair/
│   ├── /washer-wont-drain/
│   ├── /washer-not-spinning/
│   └── /washer-leaking/
```
## 🔗 ADVANCED INTERNAL LINKING STRATEGY

### Semantic Internal Linking
Create topical relevance through smart linking:

```html
<!-- In refrigerator repair page -->
<p>If your refrigerator isn't cooling, it might be related to 
<a href="/services/ice-maker-repair">ice maker problems</a> or require 
<a href="/emergency-repair">emergency service</a> to prevent food spoilage.</p>
```

### Link Equity Distribution
**Priority Pages** (most internal links):
1. Main service pages (refrigerator, washer, etc.)
2. Emergency repair page
3. Service area pages for main neighborhoods

**Support Pages** (moderate links):
- Brand repair pages
- How-to guides
- Pricing pages

**Link Anchor Text Variation**:
- Exact match (20%): "refrigerator repair"
- Partial match (40%): "fridge repair service"
- Branded (20%): "Nika refrigerator experts"
- Natural (20%): "fix your fridge today"

## 🌐 INTERNATIONAL SEO (Multi-location)

### Location-Specific Optimization
```html
<!-- Unique content for each location -->
<h1>Appliance Repair in Downtown Chicago</h1>
<p>Serving the Loop area including Willis Tower, Millennium Park, 
and the Financial District. Our technicians know the parking 
restrictions and building access requirements unique to high-rise 
living.</p>
```

### Local Schema Implementation
```json
{
  "@type": "LocalBusiness",
  "areaServed": [
    {"@type": "City", "name": "Chicago"},
    {"@type": "Place", "name": "Downtown Chicago"},
    {"@type": "Place", "name": "Chicago Loop"}
  ],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 41.8781,
    "longitude": -87.6298
  }
}
```