# SEO URL Consolidation Plan
## Fix Duplicate Content Issue: .html vs Clean URLs

**Date:** November 13, 2025
**Issue:** Google Search Console shows duplicate URLs (with and without .html)
**Impact:** Duplicate content penalty, split SEO authority, wasted crawl budget

---

## 🔴 Current Problems

### 1. Vercel Configuration (`vercel.json`)
- ✅ `cleanUrls: true` - Allows access without .html
- ❌ `rewrites` section - Also allows access WITH .html
- **Result:** Both URLs are accessible (200 status)

### 2. Canonical Tags in Blog Posts
- ❌ Point to `.html` URLs
- ❌ Mix of relative and absolute URLs
- **Examples:**
  ```html
  <link rel="canonical" href="/blog/bosch-dishwasher-repair.html">
  <link rel="canonical" href="https://nikaappliancerepair.com/blog/guides/dishwasher-hard-water-solutions-toronto.html">
  ```
- **Should be:**
  ```html
  <link rel="canonical" href="https://nikaappliancerepair.com/blog/guides/bosch-dishwasher-repair">
  ```

### 3. Sitemap (`sitemap.xml`)
- ❌ Contains `.html` URLs for blog posts
- **Example:**
  ```xml
  <loc>https://nikaappliancerepair.com/blog/guides/bosch-dishwasher-repair.html</loc>
  ```
- **Should be:**
  ```xml
  <loc>https://nikaappliancerepair.com/blog/guides/bosch-dishwasher-repair</loc>
  ```

### 4. Google Search Console
- Shows 2x URLs indexed (duplicate content)
- Both versions compete for rankings
- SEO authority is split between duplicates

---

## ✅ SOLUTION: 5-Step Fix

### Step 1: Update `vercel.json` Configuration

**Add 301 redirects** to force .html URLs → clean URLs:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [
    {
      "source": "/blog/:category/:slug.html",
      "destination": "/blog/:category/:slug",
      "permanent": true
    },
    {
      "source": "/services/:slug.html",
      "destination": "/services/:slug",
      "permanent": true
    },
    {
      "source": "/locations/:slug.html",
      "destination": "/locations/:slug",
      "permanent": true
    },
    {
      "source": "/brands/:slug.html",
      "destination": "/brands/:slug",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/services/:slug",
      "destination": "/services/:slug.html"
    },
    {
      "source": "/locations/:slug",
      "destination": "/locations/:slug.html"
    },
    {
      "source": "/brands/:slug",
      "destination": "/brands/:slug.html"
    },
    {
      "source": "/blog/:category/:slug",
      "destination": "/blog/:category/:slug.html"
    }
  ]
}
```

**How it works:**
- Rewrites: Internal mapping (user sees clean URL, server serves .html file)
- Redirects: If someone accesses .html URL directly → 301 redirect to clean URL
- Result: Only clean URLs are accessible from outside

---

### Step 2: Fix Canonical Tags in ALL Blog Posts

**Current (WRONG):**
```html
<link rel="canonical" href="/blog/bosch-dishwasher-repair.html">
```

**Correct (CLEAN URL):**
```html
<link rel="canonical" href="https://nikaappliancerepair.com/blog/guides/bosch-dishwasher-repair">
```

**Requirements:**
- ✅ Always use absolute URLs (with https://)
- ✅ Always use clean URLs (no .html)
- ✅ Match exact path structure

**Files to update:** ~109 blog post HTML files

---

### Step 3: Update Blog Template

Update `/blog/templates/blog-template-optimized.html`:

```html
<link rel="canonical" href="https://nikaappliancerepair.com{{CANONICAL_PATH}}">
```

Where `{{CANONICAL_PATH}}` = `/blog/category/slug` (no .html)

---

### Step 4: Regenerate Sitemap with Clean URLs Only

**Current sitemap has:**
```xml
<loc>https://nikaappliancerepair.com/blog/guides/bosch-dishwasher-repair.html</loc>
```

**Must change to:**
```xml
<loc>https://nikaappliancerepair.com/blog/guides/bosch-dishwasher-repair</loc>
```

**Action:** Create Python script to regenerate sitemap with clean URLs

---

### Step 5: Google Search Console Actions

After deployment:

1. **Submit Updated Sitemap**
   - Remove old sitemap (if exists)
   - Submit new sitemap with clean URLs only

2. **Request URL Removals**
   - Submit removal requests for all .html URLs
   - Use bulk removal tool (pattern: `*/blog/*/*.html`)

3. **Force Re-indexing**
   - Use URL Inspection tool
   - Request indexing for top 20-30 blog posts with clean URLs

4. **Monitor for 2-4 weeks**
   - Check index coverage report
   - Verify .html URLs are removed
   - Verify clean URLs are indexed

---

## 📊 Expected Results

### Before Fix:
- ❌ 218 URLs indexed (109 clean + 109 .html)
- ❌ Duplicate content warnings
- ❌ Split SEO authority
- ❌ Confusing user experience

### After Fix:
- ✅ 109 URLs indexed (clean only)
- ✅ No duplicate content
- ✅ Consolidated SEO authority
- ✅ Better rankings
- ✅ Improved crawl budget efficiency

---

## ⚠️ Important Notes

1. **301 Redirects are permanent** - They tell Google:
   - Old URL (.html) has permanently moved to new URL (clean)
   - Transfer all SEO value to new URL
   - Don't index old URL anymore

2. **Canonical tags** - Backup signal to Google:
   - "This is the preferred version of this page"
   - Helps consolidate duplicate signals

3. **Sitemap** - Tells Google which URLs to index:
   - Only include clean URLs
   - Exclude .html versions entirely

4. **Timeline:**
   - Deploy fixes: 1-2 hours
   - Google detection: 1-3 days
   - Full re-indexing: 2-4 weeks
   - SEO recovery: 4-8 weeks

---

## 🚀 Implementation Order

1. ✅ Create this plan
2. ⏳ Update vercel.json with redirects
3. ⏳ Fix canonical tags in all blog posts
4. ⏳ Regenerate sitemap
5. ⏳ Deploy to production
6. ⏳ Submit to Google Search Console
7. ⏳ Monitor and track progress

---

## 📝 Scripts Needed

1. **fix_canonical_tags.py** - Update all blog post canonical tags
2. **generate_sitemap.py** - Regenerate sitemap with clean URLs
3. **verify_redirects.sh** - Test that redirects work correctly

---

## Success Metrics

- [ ] All .html URLs return 301 redirect
- [ ] All canonical tags point to clean URLs
- [ ] Sitemap contains only clean URLs
- [ ] Google Search Console shows only clean URLs indexed
- [ ] No duplicate content warnings
- [ ] Improved average position for target keywords

---

**Status:** Ready for implementation
**Priority:** 🔴 HIGH (SEO critical)
**Estimated Time:** 2-3 hours implementation + 2-4 weeks Google re-indexing
