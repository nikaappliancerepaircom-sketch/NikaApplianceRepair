# Location Pages Optimization Plan

## Current State (32 pages total)

### Design Status
- ✅ **28 pages**: Full design (Header + Footer + FAQ + Workiz)
- ⚠️ **4 pages**: Missing header/footer (caledon, clarington, newmarket, whitby)

### Content Status
- ✅ **24 pages**: Good word count (1500-2500)
- ⚠️ **8 pages**: Over 2500 words (need trimming)

### BMAD Compliance
- ✅ **All pages**: Have LocalBusiness + AggregateRating schema
- ✅ **31/32 pages**: Correct review count (5,200+)
- ⚠️ **1 page**: Missing review count (whitby)

---

## Optimization Tasks

### Phase 1: Fix Missing Header/Footer (4 pages)
**Pages:** caledon, clarington, newmarket, whitby

**Tasks:**
1. Extract global header from index.html
2. Extract global footer from index.html
3. Insert into 4 pages with path fixes (/ → ../)
4. Verify through Chrome MCP

### Phase 2: Fix Review Count (1 page)
**Page:** whitby.html

**Tasks:**
1. Add missing review count (5,200+)
2. Verify consistency

### Phase 3: Trim Excessive Word Count (8 pages)
**Target:** Reduce from 2500+ to ~2000-2400 words

**Pages (priority order):**
1. toronto.html (4092 → ~2200)
2. stouffville.html (3471 → ~2200)
3. clarington.html (3226 → ~2200)
4. aurora.html (3153 → ~2200)
5. caledon.html (2964 → ~2200)
6. whitby.html (2623 → ~2200)
7. scarborough.html (2617 → ~2200)
8. etobicoke.html (2546 → ~2200)

**Method:**
- Remove redundant FAQ questions (keep 8-10 most relevant)
- Shorten verbose service descriptions
- Remove duplicate content
- Keep critical SEO content intact

### Phase 4: BMAD Testing
**Test all 32 pages:**
1. Run Tier 1 tests (must pass 100%)
2. Run Tier 2 tests (target 85%+)
3. Fix any critical failures
4. Document results

---

## Execution Plan

### Step 1: Fix 4 Pages Missing Header/Footer
```bash
python scripts/add-header-footer-to-locations.py
```
- Add global header/footer to: caledon, clarington, newmarket, whitby
- Test through Chrome MCP

### Step 2: Fix Whitby Review Count
```bash
python scripts/fix-whitby-review-count.py
```

### Step 3: Trim Word Counts
```bash
python scripts/trim-location-pages.py
```
- Target: Reduce 8 pages to ~2000-2400 words
- Method: Remove 2-3 FAQ questions, shorten descriptions

### Step 4: BMAD Batch Test
```bash
cd tools/bmad-v2
python auto-run.py --batch ../../locations/*.html --tier 1-2
```

### Step 5: Fix Any BMAD Failures
```bash
python auto-run.py <failed-page.html> --auto-fix
```

---

## Success Criteria

- ✅ All 32 pages have header + footer
- ✅ All 32 pages have 5,200+ reviews
- ✅ All 32 pages: 1500-2500 words
- ✅ All 32 pages: Tier 1 = 100%
- ✅ All 32 pages: Tier 2 = 85%+

---

## Timeline

1. **Fix header/footer (4 pages):** 10 minutes
2. **Fix review count (1 page):** 2 minutes
3. **Trim word counts (8 pages):** 15 minutes
4. **BMAD testing (32 pages):** 20 minutes
5. **Fix failures:** 10 minutes

**Total:** ~60 minutes
