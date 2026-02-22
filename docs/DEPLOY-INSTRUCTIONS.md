# Deploy Instructions — 3 New Sites
**Date:** 2026-02-22

## Quick Reference
| Site | Local Path | Domain | GitHub Repo |
|------|-----------|--------|-------------|
| Site 1 | C:/nappliancerepair | nappliancerepair.com | TBD |
| Site 2 | C:/appliancerepairneary | appliancerepairneary.com | TBD |
| Site 3 | C:/fixlifyservices | fixlifyservices.com | TBD |

---

## Step 1 — Create GitHub Repos

Run these 3 commands in terminal (requires `gh` CLI logged in):

```bash
# Site 1
cd /c/nappliancerepair
gh repo create nappliancerepair --public --source=. --push

# Site 2
cd /c/appliancerepairneary
gh repo create appliancerepairneary --public --source=. --push

# Site 3
cd /c/fixlifyservices
gh repo create fixlifyservices --public --source=. --push
```

Or create manually on GitHub.com then:
```bash
cd /c/nappliancerepair && git remote add origin https://github.com/YOUR_USER/nappliancerepair.git && git push -u origin main
cd /c/appliancerepairneary && git remote add origin https://github.com/YOUR_USER/appliancerepairneary.git && git push -u origin main
cd /c/fixlifyservices && git remote add origin https://github.com/YOUR_USER/fixlifyservices.git && git push -u origin main
```

---

## Step 2 — Deploy to Vercel

For each site, go to: https://vercel.com/new

1. Click "Import Git Repository"
2. Select the repo (nappliancerepair / appliancerepairneary / fixlifyservices)
3. Framework: **Other** (static HTML)
4. Root directory: `/` (leave default)
5. Click Deploy

OR use Vercel CLI:
```bash
npm i -g vercel
cd /c/nappliancerepair && vercel --prod
cd /c/appliancerepairneary && vercel --prod
cd /c/fixlifyservices && vercel --prod
```

---

## Step 3 — Connect Custom Domains

In Vercel dashboard → Project Settings → Domains:

1. nappliancerepair → Add `nappliancerepair.com` + `www.nappliancerepair.com`
2. appliancerepairneary → Add `appliancerepairneary.com` + `www.appliancerepairneary.com`
3. fixlifyservices → Add `fixlifyservices.com` + `www.fixlifyservices.com`

Then update DNS at your registrar:
- `A` record: `@` → `76.76.21.21` (Vercel IP)
- `CNAME` record: `www` → `cname.vercel-dns.com`

Or use Vercel nameservers for automatic DNS management.

---

## Step 4 — Google Search Console

For EACH site:
1. Go to https://search.google.com/search-console
2. Add property → URL prefix → `https://nappliancerepair.com`
3. Verify via HTML file method (Vercel makes this easy — just add the verification file and push)
4. Submit sitemap: Settings → Sitemaps → `https://nappliancerepair.com/sitemap.xml`

---

## Step 5 — Google Indexing API (Priority URLs)

After GSC verified, submit these priority URLs for fast indexing:

### nappliancerepair.com (top 15)
- /index.html
- /fridge-repair-toronto.html
- /washer-repair-toronto.html
- /appliance-repair-toronto.html
- /fridge-repair-mississauga.html
- /washer-repair-mississauga.html
- /lg-repair.html
- /samsung-repair.html
- /whirlpool-repair.html
- /bosch-repair.html
- /about.html
- /pricing.html
- /fridge-repair-brampton.html
- /fridge-repair-vaughan.html
- /fridge-repair-markham.html

### appliancerepairneary.com (top 15)
- /index.html
- /fridge-repair-near-me.html
- /washer-repair-near-me.html
- /appliance-repair-near-me.html
- /dryer-repair-near-me.html
- /fridge-not-cooling-near-me.html
- /washer-not-draining-near-me.html
- /fridge-repair-toronto.html
- /fridge-repair-mississauga.html
- /washer-repair-toronto.html
- /about.html
- /contact.html
- /fridge-repair-brampton.html
- /fridge-repair-markham.html
- /oven-not-heating-near-me.html

### fixlifyservices.com (top 15)
- /index.html
- /fridge-repair-toronto.html
- /washer-repair-toronto.html
- /emergency-fridge-repair-toronto.html
- /fridge-not-cooling.html
- /washer-not-draining.html
- /fridge-repair-mississauga.html
- /fridge-repair-brampton.html
- /same-day-appliance-repair-scarborough.html
- /appliance-repair-cost-toronto.html
- /is-it-worth-repairing-appliance.html
- /samsung-appliance-repair.html
- /lg-appliance-repair.html
- /about.html
- /fridge-repair-markham.html

---

## Step 6 — Google Business Profile

**ONE shared GBP** for all 4 sites (do NOT create multiple):
- Business name: Nick's Appliance Repair
- Phone: (437) 524-1053
- Website: https://nikaappliancerepair.com (main site)
- Secondary website field: n/a (GBP only allows one)
- Service area: Greater Toronto Area
- Category: Appliance Repair Service

Link the 3 new sites via:
- Footer mention: "Also serving customers via [nappliancerepair.com]"
- About pages mention: part of the same licensed operation

---

## NAP Consistency Checklist

All 4 sites must use IDENTICAL:
- Phone: **(437) 524-1053**
- Schema name: varies per site (but same phone/address)
- Address: Toronto, ON (no street needed for mobile service)

---

## Post-Launch Monitoring

- GSC: check index coverage weekly for first month
- Ahrefs/Semrush: track keyword rankings starting week 2
- Google Analytics: add GA4 tag to all pages
- CRV: check Fixlify booking completions in Fixlify dashboard

### GA4 tag to add to all pages (after creating property):
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```
Replace `G-XXXXXXXXXX` with your GA4 measurement ID.
