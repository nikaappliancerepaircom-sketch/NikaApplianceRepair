# Smart Template System for Nika Appliance Repair

## Overview
This template system uses context engineering to create unique, SEO-optimized content for each page while maintaining consistent design.

## Template Types

### 1. Brand Pages Template
- **Variables**: {{BRAND_NAME}}, {{BRAND_COLOR}}, {{BRAND_SPECIALTIES}}
- **Unique Content Blocks**:
  - Hero content specific to brand's technology
  - Brand-specific repair expertise
  - Common problems for that brand
  - Brand-specific FAQs

### 2. Service Pages Template  
- **Variables**: {{SERVICE_TYPE}}, {{SERVICE_ICON}}, {{COMMON_ISSUES}}
- **Unique Content Blocks**:
  - Service-specific benefits
  - Common problems and solutions
  - Service-specific pricing info
  - Maintenance tips

### 3. Location Pages Template
- **Variables**: {{LOCATION_NAME}}, {{NEARBY_AREAS}}, {{LOCAL_STATS}}
- **Unique Content Blocks**:
  - Local testimonials
  - Area-specific response times
  - Local service statistics
  - Nearby landmarks/areas served

## Context Engineering Rules

### For Brand Pages:
1. **LG Context**:
   - Emphasize: Smart ThinQ, Linear Compressor, Energy Efficiency
   - Common issues: Compressor failures, WiFi connectivity
   - Certifications: LG authorized service
   
2. **Samsung Context**:
   - Emphasize: Digital Inverter, FlexWash/FlexDry, Smart Home
   - Common issues: Error codes, ice maker problems
   - Certifications: Samsung certified technicians

3. **Whirlpool Context**:
   - Emphasize: American reliability, 6th Sense technology
   - Common issues: Control board, heating elements
   - Certifications: Whirlpool factory trained

### For Service Pages:
1. **Refrigerator Repair Context**:
   - Keywords: cooling, ice maker, compressor, thermostat
   - Common issues: Not cooling, leaking, strange noises
   - Urgency: Food spoilage risk, 24/7 emergency service
   
2. **Washer Repair Context**:
   - Keywords: spinning, draining, leaking, agitator
   - Common issues: Won't drain, unbalanced load, error codes
   - Urgency: Laundry piling up, water damage risk

### For Location Pages:
1. **Toronto Context**:
   - Mention: Downtown core, rapid response, high-rise service
   - Local proof: "Serving Toronto since 2019"
   - Areas: Yorkville, Financial District, Entertainment District
   
2. **Mississauga Context**:
   - Mention: Square One area, suburban homes, same-day service
   - Local proof: "Your Mississauga neighbors trust us"
   - Areas: Port Credit, Streetsville, Erin Mills

## Implementation Example

```javascript
// Context engine function
function generatePageContent(type, context) {
  switch(type) {
    case 'brand':
      return {
        hero: generateBrandHero(context.brand),
        about: generateBrandAbout(context.brand),
        services: generateBrandServices(context.brand),
        faqs: generateBrandFAQs(context.brand)
      };
    case 'service':
      return {
        hero: generateServiceHero(context.service),
        benefits: generateServiceBenefits(context.service),
        process: generateServiceProcess(context.service),
        faqs: generateServiceFAQs(context.service)
      };
    case 'location':
      return {
        hero: generateLocationHero(context.location),
        areas: generateLocationAreas(context.location),
        testimonials: generateLocationTestimonials(context.location),
        stats: generateLocationStats(context.location)
      };
  }
}
```

## Content Generation Rules

1. **Never duplicate content** - Each page must have unique text
2. **Include semantic variations** - Use synonyms and related terms
3. **Maintain brand voice** - Friendly, professional, trustworthy
4. **Include local/specific details** - Makes content authentic
5. **Natural keyword integration** - No keyword stuffing

## Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <!-- SEO Meta - Dynamically Generated -->
    <title>{{GENERATED_TITLE}}</title>
    <meta name="description" content="{{GENERATED_DESCRIPTION}}">
</head>
<body>
    <!-- Universal Header -->
    {{UNIVERSAL_HEADER}}
    
    <!-- Dynamic Hero Section -->
    <section class="hero">
        {{UNIQUE_HERO_CONTENT}}
    </section>
    
    <!-- Dynamic Services/Benefits -->
    <section class="services">
        {{UNIQUE_SERVICES_CONTENT}}
    </section>
    
    <!-- Dynamic About -->
    <section class="about">
        {{UNIQUE_ABOUT_CONTENT}}
    </section>
    
    <!-- Dynamic Testimonials -->
    <section class="testimonials">
        {{UNIQUE_TESTIMONIALS}}
    </section>
    
    <!-- Dynamic FAQ -->
    <section class="faq">
        {{UNIQUE_FAQ_CONTENT}}
    </section>
    
    <!-- Universal Footer -->
    {{UNIVERSAL_FOOTER}}
</body>
</html>
```