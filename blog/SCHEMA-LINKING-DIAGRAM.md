# Schema.org Entity Linking - Visual Diagram

## How @id Creates the Connection

```
┌─────────────────────────────────────────────────────────────────┐
│                        /team.html                                │
│                   (Single Source of Truth)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Contains full Person schema:
                              │
    ┌─────────────────────────▼──────────────────────────┐
    │  {                                                  │
    │    "@type": "Person",                              │
    │    "@id": "...team#sarah-chen", ◄─────┐            │
    │    "name": "Sarah Chen",               │            │
    │    "jobTitle": "Master Technician",    │            │
    │    "url": "...team/sarah-chen",        │            │
    │    "email": "sarah@...",               │            │
    │    "telephone": "647-...",             │  UNIQUE    │
    │    "worksFor": {...},                  │  IDENTIFIER│
    │    "knowsAbout": [...],                │            │
    │    "hasCredential": [                  │            │
    │      "Samsung Certified",              │            │
    │      "LG Certified",                   │            │
    │      "Whirlpool Certified"             │            │
    │    ],                                  │            │
    │    "description": "12 years..."        │            │
    │  }                                     │            │
    └────────────────────────────────────────┘            │
                              │                           │
                              │ Referenced by:            │
                              │                           │
        ┌─────────────────────┼───────────────────┐       │
        │                     │                   │       │
        ▼                     ▼                   ▼       │
                                                          │
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Article #1      │  │  Article #2      │  │  Article #3      │
│  refrigerator    │  │  ice-maker       │  │  freezer         │
│  maintenance     │  │  repair          │  │  troubleshooting │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                     │                   │
        │ Minimal reference:  │                   │
        │                     │                   │
        ▼                     ▼                   ▼
                                                          │
    ┌───────────────────────────────────────────┐         │
    │  "author": {                              │         │
    │    "@type": "Person",                     │         │
    │    "@id": "...team#sarah-chen", ──────────┼─────────┘
    │    "name": "Sarah Chen",                  │  LINKS BACK
    │    "jobTitle": "Master Technician",       │  TO FULL
    │    "url": "...team/sarah-chen"            │  PROFILE
    │  }                                        │
    └───────────────────────────────────────────┘
```

## The Power of @id

When Google sees the same `@id` in multiple places:

```
Article A → @id: "team#sarah-chen" ──┐
                                      │
Article B → @id: "team#sarah-chen" ──┼──► Google: "These all reference
                                      │           the SAME person!"
Article C → @id: "team#sarah-chen" ──┘
```

Google then:
1. Fetches the full Person schema from `/team.html`
2. Associates all articles with that person
3. Builds knowledge graph connections
4. Verifies credentials and expertise
5. Attributes authority to the content

## Without @id Linking (Before)

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Article #1      │  │  Article #2      │  │  Article #3      │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                     │                   │
        ▼                     ▼                   ▼
    ┌───────────┐       ┌───────────┐       ┌───────────┐
    │  "author":│       │  "author":│       │  "author":│
    │  {        │       │  {        │       │  {        │
    │   "name": │       │   "name": │       │   "name": │
    │   "Sarah" │       │   "Sarah" │       │   "Sarah" │
    │  }        │       │  }        │       │  }        │
    └───────────┘       └───────────┘       └───────────┘
         ❌                  ❌                  ❌
    Isolated            Isolated            Isolated
```

**Problems:**
- Google doesn't know these are the same person
- No connection to credentials
- No authority building
- Duplicate data in every article
- Can't verify expertise

## With @id Linking (After)

```
                    ┌────────────────────┐
                    │   /team.html       │
                    │   Full Profile     │
                    │   + Credentials    │
                    └────────────────────┘
                             ▲
                             │
                    All articles link here
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Article #1  │     │  Article #2  │     │  Article #3  │
│  @id: #sarah │     │  @id: #sarah │     │  @id: #sarah │
└──────────────┘     └──────────────┘     └──────────────┘
        ✅                  ✅                  ✅
    Connected           Connected           Connected
```

**Benefits:**
- Google knows same expert across all articles
- Credentials flow to all content
- Authority compounds
- Single source of truth
- Verifiable expertise

## Entity Resolution Flow

```
User searches: "refrigerator not cooling toronto"
                    ↓
         Google finds article
                    ↓
    Article has author with @id
                    ↓
    Google follows @id to /team.html
                    ↓
       Finds Sarah Chen's profile
                    ↓
        Checks credentials:
        ✓ Samsung Certified
        ✓ LG Certified
        ✓ 12 years experience
                    ↓
      Verifies expertise in:
      ✓ Refrigerator Repair
      ✓ Cooling Systems
                    ↓
    Finds 13 other articles by same author
                    ↓
      BOOSTS RANKING:
      ✓ Verified expert
      ✓ Consistent authority
      ✓ Multiple quality articles
      ✓ E-E-A-T signals strong
```

## All Authors Connected

```
                    ┌─────────────────────────┐
                    │      /team.html         │
                    │   (Authority Source)    │
                    └─────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │   Sarah     │  │  Michael    │  │   James     │
    │   Chen      │  │  Toronto    │  │  Wilson     │
    │             │  │             │  │             │
    │ #sarah-chen │  │#michael-... │  │#james-...   │
    └─────────────┘  └─────────────┘  └─────────────┘
          │                │                │
          ├─13 articles    ├─7 articles     ├─13 articles
          │                │                │
          ▼                ▼                ▼
    Refrigerator    Dishwasher       Washer/Dryer
     Articles        Articles          Articles
```

## Data Flow Direction

```
┌──────────────────────────────────────────────────────────┐
│                    DATA HIERARCHY                         │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  1. MASTER SOURCE (team.html)                            │
│     ↓                                                     │
│     Contains: Full Person schema with credentials        │
│     Purpose: Single source of truth                      │
│                                                           │
│  2. ARTICLE REFERENCE (blog posts)                       │
│     ↓                                                     │
│     Contains: Minimal author with @id link              │
│     Purpose: Reference master source                     │
│                                                           │
│  3. GOOGLE KNOWLEDGE GRAPH                               │
│     ↓                                                     │
│     Resolves: @id → Full profile → All articles         │
│     Purpose: Build entity relationships                  │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## The @id Format

```
https://nikaappliancerepair.com/team#sarah-chen
│                                 │    │         │
│                                 │    │         └─ Author slug
│                                 │    └─────────── Fragment identifier
│                                 └──────────────── Page path
└────────────────────────────────────────────────── Domain
```

**Critical Components:**
1. **Domain**: Must match your site
2. **Path**: Points to team page
3. **# Fragment**: Creates unique ID on that page
4. **Slug**: Matches author identifier

**Why fragment (#)?**
- Creates unique identifier WITHIN a page
- Same page can have multiple Person schemas
- Each person gets unique @id with different #slug
- Browser can jump to #anchor on page

## Implementation Pattern

```
STEP 1: Verify team.html has Person schema
        ↓
   ┌────────────────────┐
   │ Check lines 20-134 │
   │ Find author's @id  │
   └────────────────────┘
        ↓
STEP 2: Copy exact @id value
        ↓
   ┌────────────────────┐
   │ Copy full URL with │
   │ #fragment          │
   └────────────────────┘
        ↓
STEP 3: Update article author
        ↓
   ┌────────────────────┐
   │ Find author object │
   │ Add @id property   │
   │ Add url property   │
   └────────────────────┘
        ↓
STEP 4: Validate
        ↓
   ┌────────────────────┐
   │ Google Rich Results│
   │ Check Article type │
   │ Verify author link │
   └────────────────────┘
```

## Complete Example

### team.html (Source)
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    {
      "@type": "Person",
      "@id": "https://nikaappliancerepair.com/team#sarah-chen",  ← SOURCE
      "name": "Sarah Chen",
      "jobTitle": "Master Appliance Technician",
      "url": "https://nikaappliancerepair.com/team/sarah-chen",
      "email": "sarah@nikaappliancerepair.com",
      "knowsAbout": ["Refrigerator Repair", "Cooling Systems"],
      "hasCredential": [
        {"name": "Samsung Certified Technician"},
        {"name": "LG Certified Technician"}
      ]
    }
  ]
}
```

### Blog Article (Reference)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Maintain Your Refrigerator",
  "author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chen",  ← REFERENCE
    "name": "Sarah Chen",
    "jobTitle": "Master Appliance Technician",
    "url": "https://nikaappliancerepair.com/team/sarah-chen"
  },
  "publisher": {...},
  "datePublished": "2025-10-25"
}
```

### Google's Understanding
```
"Oh, this article about refrigerator maintenance is by
sarah-chen. Let me look up her full profile..."

[Fetches team.html]

"I see! Sarah Chen is a Master Appliance Technician with:
- Samsung Certification
- LG Certification
- Whirlpool Certification
- 12 years experience
- Specializes in refrigerator repair and cooling systems

This gives her article more authority for refrigerator topics.
I'll rank it higher for refrigerator searches."
```

---

## Key Takeaways

1. **@id is the magic** - It's what creates the connection
2. **@id must match exactly** - Case-sensitive, character-for-character
3. **team.html is source** - Full profile with credentials lives here
4. **Articles reference** - Minimal data with link back to full profile
5. **Google connects** - Resolves @id to build knowledge graph
6. **Authority compounds** - Each article strengthens the author's expertise

---

**Visual Summary**: One expert profile → Multiple linked articles → Compounding authority
