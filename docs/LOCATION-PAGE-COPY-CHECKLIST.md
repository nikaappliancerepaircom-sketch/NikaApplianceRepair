# Location Page Copy Checklist

**When copying index.html to locations/ subfolder**

## ✅ Steps to Follow

### 1. Copy File
```bash
cp index.html locations/city-name.html
```

### 2. Update Content
- [ ] Meta title (change city name)
- [ ] Meta description (add local details)
- [ ] Canonical URL (`/locations/city-name`)
- [ ] Open Graph title & description
- [ ] H1 hero title (city name)
- [ ] Hero subtitle (local specializations if applicable)
- [ ] Schema.org address (city, postal code)

### 3. Fix Paths (CRITICAL!)
**Must fix all relative paths because file is in subfolder:**

```bash
# CSS paths
sed -i 's|href="css/|href="../css/|g' locations/city-name.html

# Asset paths
sed -i 's|src="assets/|src="../assets/|g' locations/city-name.html

# JS paths
sed -i 's|src="js/|src="../js/|g' locations/city-name.html
```

### 4. Run BMAD Tests
```bash
python tools/bmad-8tier-test.py locations/city-name.html
```

**Expected Results:**
- Tier 1-8: All pass
- Overall score: 90+ / 100

### 5. Visual Testing (REQUIRED!)
Use Playwright MCP to verify design:

1. Navigate to `file:///C:/NikaApplianceRepair/locations/city-name.html`
2. Take full page screenshot
3. Verify:
   - ✅ CSS loaded (page has colors, styling)
   - ✅ Images display (not broken boxes)
   - ✅ Layout matches index.html
   - ✅ No console errors

### 6. Remove Community References
If applicable, remove specific community accent mentions:
- ❌ "Persian & Chinese community experts"
- ❌ "Serving [ethnicity] communities"
- ✅ Use generic: "Same-day service available"

## ⚠️ Common Mistakes

### Mistake 1: Forgetting to Fix Paths
**Symptom:** Page looks broken, no CSS, black squares instead of images

**Fix:**
```bash
sed -i 's|href="css/|href="../css/|g; s|src="assets/|src="../assets/|g; s|src="js/|src="../js/|g' locations/city-name.html
```

### Mistake 2: Not Testing Visually
**Symptom:** BMAD tests pass but page looks wrong

**Fix:** Always take screenshot after changes!

### Mistake 3: Copying Content Without Localization
**Symptom:** Page says "Toronto" but it's for "Vaughan"

**Fix:** Update ALL city references (title, H1, meta, schema)

## 📊 Success Criteria

- [ ] BMAD Score: 90+/100
- [ ] All 8 tiers pass
- [ ] Visual test: Design perfect
- [ ] No console errors
- [ ] City name correct everywhere
- [ ] Paths work (CSS, images, JS)

## 🚀 Automation Script (Future)

```bash
# Example automation script (to be created)
./tools/copy-location-page.sh richmond-hill vaughan
# Would automatically:
# 1. Copy file
# 2. Update city name
# 3. Fix paths
# 4. Run tests
# 5. Take screenshot
```

---

**Last Updated:** 2025-10-18
**Status:** Richmond Hill Golden Template Complete ✅
