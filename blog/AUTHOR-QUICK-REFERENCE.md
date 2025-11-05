# Author Schema Quick Reference Card

## Copy-Paste Templates for Each Author

### Sarah Chen (Refrigerator Specialist)
**Use for**: Refrigerator, freezer, ice maker, cooling system articles

```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#sarah-chen",
    "name": "Sarah Chen",
    "jobTitle": "Master Appliance Technician",
    "url": "https://nikaappliancerepair.com/team/sarah-chen"
}
```

---

### Michael Toronto (Dishwasher Specialist)
**Use for**: Dishwasher, hard water, drainage articles

```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#michael-toronto",
    "name": "Michael Toronto",
    "jobTitle": "Senior Dishwasher Specialist",
    "url": "https://nikaappliancerepair.com/team/michael-toronto"
}
```

---

### James Wilson (Washer & Dryer Specialist)
**Use for**: Washing machine, dryer, laundry articles

```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#james-wilson",
    "name": "James Wilson",
    "jobTitle": "Washer & Dryer Specialist",
    "url": "https://nikaappliancerepair.com/team/james-wilson"
}
```

---

### David Martinez (Oven & Stove Expert)
**Use for**: Oven, stove, range, cooktop articles

```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#david-martinez",
    "name": "David Martinez",
    "jobTitle": "Oven & Stove Expert",
    "url": "https://nikaappliancerepair.com/team/david-martinez"
}
```

---

### Expert Team (General)
**Use for**: Multi-appliance, location, brand overview, general tips

```json
"author": {
    "@type": "Person",
    "@id": "https://nikaappliancerepair.com/team#expert-team",
    "name": "Nika Expert Team",
    "jobTitle": "Certified Appliance Repair Specialists",
    "url": "https://nikaappliancerepair.com/team"
}
```

---

## Critical Rules

1. ✅ **ALWAYS include**: `@type`, `@id`, `name`, `jobTitle`, `url`
2. ✅ **@id MUST match** what's in `/team.html` exactly
3. ✅ **Include comma** after closing `}` if not last property
4. ❌ **DON'T add** email, telephone, or other details (they're in team.html)
5. ❌ **DON'T change** the @id format or structure

---

## Validation Checklist

Before saving:
- [ ] `@id` starts with `https://nikaappliancerepair.com/team#`
- [ ] Author name matches article topic
- [ ] JSON syntax valid (check commas and quotes)
- [ ] All 5 properties present: @type, @id, name, jobTitle, url

Test after saving:
- [ ] Google Rich Results Test shows valid Article
- [ ] No schema errors in console
- [ ] Author appears correctly in preview

---

## Location in Blog Files

Find the Article schema around **lines 190-220** in most blog posts:

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "...",
    "author": {
        <!-- REPLACE THIS SECTION -->
    },
    "publisher": {...},
    ...
}
</script>
```

Replace only the `author: {...}` object, leave everything else unchanged.
