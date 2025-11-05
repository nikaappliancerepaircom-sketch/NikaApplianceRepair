# Schema.org Article Author Linking Guide

## Overview
This guide explains how to properly link Article schema markup to Person schema profiles in the team.html page. This creates a connected knowledge graph that helps search engines understand author expertise and authority.

## Why This Matters

### SEO Benefits
1. **Author Authority**: Google can connect article content to verified expert profiles
2. **E-E-A-T Signals**: Strengthens Experience, Expertise, Authoritativeness, and Trust
3. **Rich Results Eligibility**: Proper author markup is required for article rich results
4. **Knowledge Graph**: Creates relationships between content and authors in Google's knowledge graph
5. **Author Bylines**: Can trigger author information in search results

### Technical Benefits
1. **Entity Resolution**: @id creates a unique identifier for each author
2. **Data Consistency**: Single source of truth for author information
3. **Schema Validation**: Properly linked entities pass Google's structured data testing
4. **Cross-Document Linking**: Multiple articles can reference the same author entity

---

## Team Member Schema Structure (team.html)

The `/team.html` page contains Person schema markup for all team members. Each person has:

```json
{
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chen",
    "name": "Sarah Chen",
    "jobTitle": "Master Appliance Technician",
    "url": "https://nikaappliancerepair.com/team/sarah-chen",
    "email": "sarah@nikaappliancerepair.com",
    "telephone": "647-557-6342",
    "worksFor": {
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair"
    },
    "knowsAbout": ["Refrigerator Repair", "Cooling Systems"],
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": "Samsung Certified Technician"},
        {"@type": "EducationalOccupationalCredential", "name": "LG Certified Technician"}
    ],
    "description": "Sarah has 12 years of experience..."
}
```

### Key Components
- **@id**: Unique identifier in format `https://nikaappliancerepair.com/team#author-name`
- **url**: Individual profile URL (can be team page with anchor or dedicated page)
- **Complete profile**: Includes credentials, expertise, and background

---

## Article Schema Author Linking Pattern

### Before (Basic Author - NOT Linked)
```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article Title",
    "author": {
        "@type": "Person",
        "name": "Sarah Chen",
        "jobTitle": "Master Appliance Technician"
    },
    ...
}
```

**Problems:**
- No connection to team profile
- Duplicate information (name, jobTitle repeated in every article)
- No way for Google to verify this is the same Sarah Chen across articles
- Missing author credentials and expertise

### After (Properly Linked Author - RECOMMENDED)
```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article Title",
    "author": {
        "@type": "Person",
        "@id": "https://nikaappliancerepair.com/team#sarah-chen",
        "name": "Sarah Chen",
        "jobTitle": "Master Appliance Technician",
        "url": "https://nikaappliancerepair.com/team/sarah-chen"
    },
    ...
}
```

**Benefits:**
- **@id matches team.html**: Creates explicit link to full profile
- **name + jobTitle**: Provides immediate context (required fields)
- **url**: Links to full profile page with credentials and experience
- **Single source of truth**: Full profile in team.html is referenced by all articles

---

## Available Authors (from team.html)

### 1. Sarah Chen (Refrigerator Specialist)
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chen",
    "name": "Sarah Chen",
    "jobTitle": "Master Appliance Technician",
    "url": "https://nikaappliancerepair.com/team/sarah-chen"
}
```
**Use for**: Refrigerator articles, cooling systems, Samsung/LG/Whirlpool content

---

### 2. Michael Toronto (Dishwasher Specialist)
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#michael-toronto",
    "name": "Michael Toronto",
    "jobTitle": "Senior Dishwasher Specialist",
    "url": "https://nikaappliancerepair.com/team/michael-toronto"
}
```
**Use for**: Dishwasher articles, hard water solutions, Bosch/KitchenAid content

---

### 3. James Wilson (Washer & Dryer Specialist)
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#james-wilson",
    "name": "James Wilson",
    "jobTitle": "Washer & Dryer Specialist",
    "url": "https://nikaappliancerepair.com/team/james-wilson"
}
```
**Use for**: Washing machine, dryer articles, laundry systems, Maytag/GE content

---

### 4. David Martinez (Oven & Stove Expert)
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#david-martinez",
    "name": "David Martinez",
    "jobTitle": "Oven & Stove Expert",
    "url": "https://nikaappliancerepair.com/team/david-martinez"
}
```
**Use for**: Oven, stove, range articles, Wolf/Viking/Thermador content

---

### 5. Expert Team (General Content)
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#expert-team",
    "name": "Nika Expert Team",
    "jobTitle": "Certified Appliance Repair Specialists",
    "url": "https://nikaappliancerepair.com/team"
}
```
**Use for**: Multi-appliance guides, general repair tips, location pages, brand overview articles

---

## Implementation Steps

### Step 1: Identify Article Topic
Determine which expert should author the article based on appliance type.

### Step 2: Locate Existing Schema
Find the Article schema block (typically around lines 190-220 in blog posts):
```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",
    ...
}
</script>
```

### Step 3: Update Author Object
Replace the basic author object with the properly linked version:

**Find:**
```json
"author": {
    "@type": "Person",
    "name": "Author Name",
    "jobTitle": "Job Title"
},
```

**Replace with:**
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#author-slug",
    "name": "Author Name",
    "jobTitle": "Job Title",
    "url": "https://nikaappliancerepair.com/team/author-slug"
},
```

### Step 4: Verify Match
Ensure the `@id` and author details EXACTLY match what's in `/team.html` (lines 20-134).

### Critical: The @id MUST match between:
- Article schema author `@id`
- Person schema `@id` in team.html
- If they don't match, the link won't work!

---

## Example: Complete Article Schema

Here's the complete updated schema from `how-to-maintain-refrigerator.html`:

```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "How to Maintain Your Refrigerator: Toronto Hard Water Coil Cleaning Guide",
    "author": {
        "@type": "Person",
        "@id": "https://nikaappliancerepair.com/team#sarah-chen",
        "name": "Sarah Chen",
        "jobTitle": "Master Appliance Technician",
        "url": "https://nikaappliancerepair.com/team/sarah-chen"
    },
    "publisher": {
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair",
        "logo": {
            "@type": "ImageObject",
            "url": "https://nikaappliancerepair.com/images/logo.png"
        }
    },
    "datePublished": "2025-10-25",
    "dateModified": "2025-10-25",
    "image": "https://nikaappliancerepair.com/images/blog-default.jpg",
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://nikaappliancerepair.com/blog/maintenance/how-to-maintain-refrigerator.html"
    }
}
```

**Changes made:**
1. Added `@id` property pointing to team.html anchor
2. Added `url` property linking to author profile
3. Kept `name` and `jobTitle` for immediate context

---

## Content Assignment Matrix

Use this table to assign the correct author to each article type:

| Article Topic | Recommended Author | @id |
|--------------|-------------------|-----|
| Refrigerator repair/maintenance | Sarah Chen | `#sarah-chen` |
| Freezer issues | Sarah Chen | `#sarah-chen` |
| Ice maker problems | Sarah Chen | `#sarah-chen` |
| Dishwasher repair/maintenance | Michael Toronto | `#michael-toronto` |
| Hard water issues (dishwasher) | Michael Toronto | `#michael-toronto` |
| Washing machine repair | James Wilson | `#james-wilson` |
| Dryer repair/maintenance | James Wilson | `#james-wilson` |
| Laundry appliance issues | James Wilson | `#james-wilson` |
| Oven repair/maintenance | David Martinez | `#david-martinez` |
| Stove/range issues | David Martinez | `#david-martinez` |
| Gas appliance repair | David Martinez | `#david-martinez` |
| General appliance tips | Expert Team | `#expert-team` |
| Multi-appliance guides | Expert Team | `#expert-team` |
| Location/service area pages | Expert Team | `#expert-team` |
| Brand-specific guides (multi) | Expert Team | `#expert-team` |

---

## Validation & Testing

### 1. Google Rich Results Test
URL: https://search.google.com/test/rich-results

**Steps:**
1. Enter blog post URL
2. Check for "Article" detection
3. Verify author property shows linked Person
4. Ensure no errors or warnings

### 2. Schema.org Validator
URL: https://validator.schema.org/

**Steps:**
1. Paste article HTML
2. Look for connected entities
3. Verify @id references resolve
4. Check for warnings about missing properties

### 3. Manual Verification Checklist

- [ ] `@id` format: `https://nikaappliancerepair.com/team#author-slug`
- [ ] `@id` matches team.html exactly (case-sensitive)
- [ ] `url` property included
- [ ] `name` property matches team.html
- [ ] `jobTitle` property matches team.html
- [ ] No extra properties that don't exist in team.html
- [ ] Proper JSON formatting (commas, quotes)

---

## Common Mistakes to Avoid

### ❌ Wrong: Missing @id
```json
"author": {
    "@type": "Person",
    "name": "Sarah Chen",
    "url": "https://nikaappliancerepair.com/team/sarah-chen"
}
```
**Problem**: No unique identifier, can't be linked to team profile

---

### ❌ Wrong: Different @id than team.html
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/authors/sarah-chen",
    "name": "Sarah Chen"
}
```
**Problem**: @id doesn't match team.html (#sarah-chen vs /authors/sarah-chen)

---

### ❌ Wrong: Typo in author slug
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chan",
    "name": "Sarah Chen"
}
```
**Problem**: Slug is "sarah-chan" but should be "sarah-chen"

---

### ❌ Wrong: Including full profile data in article
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chen",
    "name": "Sarah Chen",
    "email": "sarah@...",
    "telephone": "647-...",
    "hasCredential": [...]
}
```
**Problem**: Duplicating team.html data defeats purpose of linking. Keep article author minimal.

---

### ✅ Correct: Minimal linked author
```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chen",
    "name": "Sarah Chen",
    "jobTitle": "Master Appliance Technician",
    "url": "https://nikaappliancerepair.com/team/sarah-chen"
}
```
**Why it works**:
- @id creates the link
- name + jobTitle provide context
- url allows direct navigation
- Full profile details remain in team.html

---

## Bulk Update Process

### For all 57 blog posts:

1. **Categorize articles** by appliance type using the Content Assignment Matrix
2. **Find Article schema** in each file (search for `"@type": "Article"`)
3. **Replace author object** with appropriate linked version
4. **Verify @id match** with team.html
5. **Test one article** from each author to confirm
6. **Batch update** remaining articles

### Search & Replace Pattern

For refrigerator articles (Sarah Chen):
```
FIND:
"author": {
      "@type": "Person",
      "name": "Sarah Chen",
      "jobTitle": "Master Appliance Technician"
},

REPLACE:
"author": {
      "@type": "Person",
      "@id": "https://nikaappliancerepair.com/team#sarah-chen",
      "name": "Sarah Chen",
      "jobTitle": "Master Appliance Technician",
      "url": "https://nikaappliancerepair.com/team/sarah-chen"
},
```

Repeat for each author type.

---

## Benefits Summary

### For Search Engines
- ✅ Unified author identity across all articles
- ✅ Verifiable credentials and expertise
- ✅ Clear relationship between author and organization
- ✅ Enhanced E-E-A-T signals

### For Users
- ✅ Click through to author bio and credentials
- ✅ Find other articles by same expert
- ✅ Trust content from certified technicians
- ✅ Contact specific experts directly

### For Site Maintenance
- ✅ Single source of truth for author data
- ✅ Easy to update author info in one place
- ✅ Consistent author presentation
- ✅ Reduced data duplication

---

## Next Steps

1. ✅ **Sample completed**: how-to-maintain-refrigerator.html updated with Sarah Chen linking
2. **Categorize remaining 56 posts** using Content Assignment Matrix
3. **Bulk update** articles in batches by author
4. **Validate** updated schemas using Google Rich Results Test
5. **Monitor** search console for improved author attribution

---

## Reference Files

- **Team schema source**: `/team.html` (lines 20-134)
- **Sample implementation**: `/blog/maintenance/how-to-maintain-refrigerator.html` (lines 193-221)
- **This guide**: `/blog/SCHEMA-AUTHOR-LINKING-GUIDE.md`

---

## Questions & Support

If you encounter issues:
1. Verify @id matches exactly (case-sensitive, including #)
2. Check JSON syntax (commas, quotes)
3. Test with Google Rich Results Test
4. Review team.html to confirm Person schema exists
5. Ensure no typos in author slugs

---

**Last Updated**: 2025-11-05
**Status**: Pattern established, ready for bulk implementation
**Next Action**: Apply to remaining 56 blog posts
