# DNS Setup for 3 New Sites

## Vercel Deployment URLs (live now)
- nappliancerepair: https://nappliancerepair-j7ghhu8bz-heyboomys-projects.vercel.app
- appliancerepairneary: https://appliancerepairneary-3o5eltlch-heyboomys-projects.vercel.app
- fixlifyservices: https://fixlifyservices-cgnd6mh1m-heyboomys-projects.vercel.app

## DNS Records to Add (in your domain registrar)

### nappliancerepair.com
```
Type  Name   Value           TTL
A     @      76.76.21.21     3600
CNAME www    cname.vercel-dns.com  3600
```

### appliancerepairneary.com
```
Type  Name   Value           TTL
A     @      76.76.21.21     3600
CNAME www    cname.vercel-dns.com  3600
```

### fixlifyservices.com
```
Type  Name   Value           TTL
A     @      76.76.21.21     3600
CNAME www    cname.vercel-dns.com  3600
```

## After DNS Propagates (24-48h)

### Step 1: Google Search Console
1. Go to https://search.google.com/search-console
2. Add property → URL prefix → https://nappliancerepair.com
3. Verify via HTML file method OR DNS TXT record
4. Repeat for all 3 sites
5. Submit sitemap: https://nappliancerepair.com/sitemap.xml

### Step 2: Google Indexing API (fast crawl)
```bash
# After GSC verification:
GOOGLE_INDEXING_SA="$(cat service-account.json)" node C:/nappliancerepair/fast-index.js
```
This will submit 15 priority URLs per site (45 total) to Google's Indexing API.

### Step 3: Google Business Profile
- Add all 3 sites as website URLs in your GBP
- Or create 1 GBP listing with nappliancerepair.com as primary website

## Vercel Domain Status
All 3 domains are added to Vercel projects. Once DNS points to 76.76.21.21,
Vercel will automatically issue SSL certificates (Let's Encrypt).
