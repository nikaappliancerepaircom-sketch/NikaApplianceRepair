# BMAD 2026 Fixes — appliancerepairneary.com

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix top BMAD 2026 audit failures across 729 pages of appliancerepairneary.com: answer capsule (369 pages), LocalBusiness schema in blog (8 pages), robots meta (146 pages), preconnect (120 pages).

**Architecture:** Node.js scripts per fix category. Each script reads HTML, injects the fix, writes back. Run sequentially. No framework needed — pure fs + regex.

**Tech Stack:** Node.js, fs, path. Site: `/c/appliancerepairneary/`. Git push to deploy via GitHub Actions.

---

## Priority Order (by impact)

| # | Fix | Pages | Impact |
|---|-----|-------|--------|
| 1 | Answer capsule | 369 | AI search citations +40% |
| 2 | LocalBusiness schema in blog | 8 | Critical BMAD fail |
| 3 | Robots meta tag | 146 | Indexation signal |
| 4 | Preconnect hints | 120 | Page speed |
| 5 | Git commit + deploy | all | Live |

---

### Task 1: Answer Capsule — 369 pages

**What:** Inject phone number into the first `<p>` tag after the H1 if it doesn't already contain the phone number.

**Target format:** Wrap existing first paragraph OR prepend a sentence:
`"Need [service] in [city]? Call <a href="tel:+14375241053">(437) 524-1053</a> — same-day service, 90-day warranty."`

**Files:**
- Create: `/c/appliancerepairneary/fix-answer-capsule.js`
- Modifies: all `.html` in root + `_pages_queue/` + `blog/`

**Step 1: Write the script**

```js
// /c/appliancerepairneary/fix-answer-capsule.js
const fs = require('fs');
const path = require('path');

const PHONE_HTML = '<a href="tel:+14375241053">(437) 524-1053</a>';
const PHONE_PATTERN = /437|524-1053/;

const FOLDERS = [
  __dirname,
  path.join(__dirname, '_pages_queue'),
  path.join(__dirname, 'blog'),
];

// Extract city and service from filename
function getCityService(filename) {
  const base = filename.replace('.html', '');
  // e.g. washer-repair-toronto -> service=washer repair, city=Toronto
  const repairIdx = base.indexOf('-repair-');
  if (repairIdx === -1) return null;
  const service = base.slice(0, repairIdx).replace(/-/g, ' ') + ' repair';
  const city = base.slice(repairIdx + 8).replace(/-/g, ' ')
    .split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  return { service, city };
}

let fixed = 0, skipped = 0, errors = 0;

for (const folder of FOLDERS) {
  if (!fs.existsSync(folder)) continue;
  const files = fs.readdirSync(folder).filter(f => f.endsWith('.html'));

  for (const file of files) {
    const filepath = path.join(folder, file);
    let html = fs.readFileSync(filepath, 'utf8');

    // Skip if already has phone in first <p>
    const firstParaMatch = html.match(/<p[^>]*>([\s\S]{0,600}?)<\/p>/i);
    if (!firstParaMatch) { skipped++; continue; }
    if (PHONE_PATTERN.test(firstParaMatch[1])) { skipped++; continue; }

    // Skip non-service pages
    const sc = getCityService(file);
    if (!sc) { skipped++; continue; }

    // Build capsule sentence
    const capsule = `Need ${sc.service} in ${sc.city}? Call ${PHONE_HTML} — same-day service, 90-day parts &amp; labour warranty.`;

    // Prepend capsule to first <p> content
    html = html.replace(
      firstParaMatch[0],
      firstParaMatch[0].replace(
        /(<p[^>]*>)/i,
        `$1${capsule} `
      )
    );

    fs.writeFileSync(filepath, html);
    fixed++;
  }
}

console.log(`Answer capsule: fixed ${fixed} | skipped ${skipped} | errors ${errors}`);
```

**Step 2: Run and verify**

```bash
cd /c/appliancerepairneary && node fix-answer-capsule.js
```

Expected output: `Answer capsule: fixed ~360 | skipped ~370 | errors 0`

**Step 3: Spot-check a fixed page**

```bash
grep -m1 "Need.*repair\|524-1053" /c/appliancerepairneary/dryer-repair-brampton.html | head -c 200
```

Expected: line starts with "Need dryer repair in Brampton? Call..."

**Step 4: Re-run BMAD audit to confirm improvement**

```bash
cd /c/appliancerepairneary && node bmad-audit-all.js 2>&1 | grep "answer capsule"
```

Expected: number drops from 369 to <20

**Step 5: Commit**

```bash
cd /c/appliancerepairneary && git add -A && git commit -m "fix: inject answer capsule into first paragraph (BMAD 2026)"
```

---

### Task 2: LocalBusiness Schema in Blog — 8 pages

**What:** Blog pages missing `"@type": "LocalBusiness"` schema. Inject a minimal LocalBusiness JSON-LD block into `<head>`.

**Files:**
- Create: `/c/appliancerepairneary/fix-blog-schema.js`
- Modifies: files in `blog/` missing LocalBusiness schema

**Step 1: Write the script**

```js
// /c/appliancerepairneary/fix-blog-schema.js
const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');
const LOCAL_BUSINESS_SCHEMA = `
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Appliance Repair Near Me — Toronto & GTA",
    "telephone": "+14375241053",
    "url": "https://appliancerepairneary.com",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Toronto",
      "addressRegion": "Ontario",
      "addressCountry": "CA"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "287"
    },
    "areaServed": "Toronto & GTA",
    "openingHours": ["Mo-Sa 08:00-20:00", "Su 09:00-18:00"]
  }
  </script>`;

let fixed = 0;
const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));

for (const file of files) {
  const filepath = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(filepath, 'utf8');

  if (/"@type"\s*:\s*"LocalBusiness"/.test(html)) continue; // already has it

  // Inject before </head>
  html = html.replace('</head>', LOCAL_BUSINESS_SCHEMA + '\n</head>');
  fs.writeFileSync(filepath, html);
  fixed++;
  console.log(`  Fixed: ${file}`);
}

console.log(`LocalBusiness schema: fixed ${fixed} blog pages`);
```

**Step 2: Run**

```bash
cd /c/appliancerepairneary && node fix-blog-schema.js
```

Expected: `fixed 8 blog pages` (list of filenames)

**Step 3: Verify**

```bash
grep -L '"@type": "LocalBusiness"' /c/appliancerepairneary/blog/*.html | wc -l
```

Expected: `0`

**Step 4: Commit**

```bash
cd /c/appliancerepairneary && git add blog/ && git commit -m "fix: add LocalBusiness schema to blog pages (BMAD 2026)"
```

---

### Task 3: Robots Meta Tag — 146 pages

**What:** Add `<meta name="robots" content="index, follow">` to pages missing it. Inject into `<head>` after `<meta charset>`.

**Files:**
- Create: `/c/appliancerepairneary/fix-robots-meta.js`
- Modifies: root + `_pages_queue/` + `blog/` pages missing robots meta

**Step 1: Write the script**

```js
// /c/appliancerepairneary/fix-robots-meta.js
const fs = require('fs');
const path = require('path');

const FOLDERS = [
  __dirname,
  path.join(__dirname, '_pages_queue'),
  path.join(__dirname, 'blog'),
];

const ROBOTS_TAG = '  <meta name="robots" content="index, follow">';

let fixed = 0, skipped = 0;

for (const folder of FOLDERS) {
  if (!fs.existsSync(folder)) continue;
  const files = fs.readdirSync(folder).filter(f => f.endsWith('.html'));

  for (const file of files) {
    const filepath = path.join(folder, file);
    let html = fs.readFileSync(filepath, 'utf8');

    if (/name="robots"/i.test(html)) { skipped++; continue; }

    // Inject after <meta charset> line
    html = html.replace(
      /(<meta\s+charset[^>]*>)/i,
      `$1\n${ROBOTS_TAG}`
    );
    fs.writeFileSync(filepath, html);
    fixed++;
  }
}

console.log(`Robots meta: fixed ${fixed} | already had it: ${skipped}`);
```

**Step 2: Run**

```bash
cd /c/appliancerepairneary && node fix-robots-meta.js
```

Expected: `fixed ~146 | already had it: ~583`

**Step 3: Verify**

```bash
grep -rL 'name="robots"' /c/appliancerepairneary/*.html /c/appliancerepairneary/blog/*.html | wc -l
```

Expected: `0` or just `404.html`

**Step 4: Commit**

```bash
cd /c/appliancerepairneary && git add -A && git commit -m "fix: add robots meta index,follow to all pages (BMAD 2026)"
```

---

### Task 4: Preconnect Hints — 120 pages

**What:** Pages missing `<link rel="preconnect">` for Google Fonts. Inject standard preconnect tags.

**Files:**
- Create: `/c/appliancerepairneary/fix-preconnect.js`
- Modifies: pages in all folders missing preconnect

**Step 1: Write the script**

```js
// /c/appliancerepairneary/fix-preconnect.js
const fs = require('fs');
const path = require('path');

const FOLDERS = [
  __dirname,
  path.join(__dirname, '_pages_queue'),
  path.join(__dirname, 'blog'),
];

const PRECONNECT = `  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`;

let fixed = 0, skipped = 0;

for (const folder of FOLDERS) {
  if (!fs.existsSync(folder)) continue;
  const files = fs.readdirSync(folder).filter(f => f.endsWith('.html'));

  for (const file of files) {
    const filepath = path.join(folder, file);
    let html = fs.readFileSync(filepath, 'utf8');

    if (/rel="preconnect"/i.test(html)) { skipped++; continue; }

    // Inject before first <link rel="stylesheet">
    const target = html.match(/<link\s+rel="stylesheet"/i);
    if (target) {
      html = html.replace('<link rel="stylesheet"', `${PRECONNECT}\n  <link rel="stylesheet"`);
    } else {
      // Fallback: inject before </head>
      html = html.replace('</head>', `${PRECONNECT}\n</head>`);
    }

    fs.writeFileSync(filepath, html);
    fixed++;
  }
}

console.log(`Preconnect: fixed ${fixed} | already had it: ${skipped}`);
```

**Step 2: Run**

```bash
cd /c/appliancerepairneary && node fix-preconnect.js
```

Expected: `fixed ~120 | already had it: ~609`

**Step 3: Verify**

```bash
grep -rL 'rel="preconnect"' /c/appliancerepairneary/*.html | wc -l
```

Expected: `1` (just 404.html)

**Step 4: Commit**

```bash
cd /c/appliancerepairneary && git add -A && git commit -m "fix: add preconnect hints to all pages (BMAD 2026)"
```

---

### Task 5: Final Audit + Deploy

**Step 1: Run full BMAD audit**

```bash
cd /c/appliancerepairneary && node bmad-audit-all.js 2>&1
```

Expected:
- Overall pass rate: **≥92%** (up from 86%)
- Answer capsule issues: **<20**
- LocalBusiness schema issues: **0**
- Robots meta warnings: **0**
- Preconnect warnings: **0**

**Step 2: Push to GitHub (triggers Vercel deploy)**

```bash
cd /c/appliancerepairneary && git push origin main
```

**Step 3: Verify deploy**

Check GitHub Actions tab for `nikaappliancerepaircom-sketch/appliancerepairneary-com` — green checkmark.

---

## Success Criteria

| Metric | Before | Target After |
|--------|--------|-------------|
| Overall BMAD pass | 86% | ≥92% |
| Answer capsule missing | 369 | <20 |
| LocalBusiness schema missing | 8 | 0 |
| Robots meta missing | 146 | 0 |
| Preconnect missing | 120 | 0 |
