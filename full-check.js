/**
 * full-check.js — scans ALL published HTML pages across 4 sites
 *
 * Phase 1 (fast): reads each file from disk → checks canonical, title, H1,
 *                 booking iframe, phone link, og:image, meta description
 * Phase 2 (HTTP): batch-fetches all URLs to find 404s / redirects
 * Phase 3 (Playwright): full mobile render check on 60 sampled pages
 *
 * Usage:
 *   node full-check.js            — all 3 phases
 *   node full-check.js --fast     — phase 1 + 2 only (no Playwright)
 *   node full-check.js --site nar — one site only
 */

const fs   = require('fs');
const path = require('path');
const http  = require('http');
const https = require('https');

const FAST = process.argv.includes('--fast');
const siteIdx = process.argv.indexOf('--site');
const SITE_ARG = siteIdx !== -1 ? process.argv[siteIdx + 1] : null;

const SITES = {
  nar:     { dir: 'C:/nappliancerepair',     domain: 'nappliancerepair.com' },
  neary:   { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com' },
  fixlify: { dir: 'C:/fixlifyservices',      domain: 'fixlifyservices.com' },
  nika:    { dir: 'C:/NikaApplianceRepair',  domain: 'nikaappliancerepair.com' },
};

const SKIP_DIRS = ['_pages_queue', 'blog', 'node_modules', '.github'];
const SKIP_FILES = ['404', 'index', 'sitemap', 'robots', 'privacy', 'terms', 'thank-you'];

// ── PHASE 1: file-based checks ───────────────────────────────────────────────

function getHtmlFiles(dir) {
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.html'))
    .filter(f => !SKIP_FILES.some(s => {
      const b = path.basename(f, '.html').toLowerCase();
      return b === s || b.startsWith(s + '-') || b.endsWith('-' + s);
    }))
    .map(f => path.join(dir, f));
}

const BOOKING_ID = 'fixlify-booking-nicks-appliance-repair-b8c8ce';
const SKIP_IFRAME_SITES = ['nikaappliancerepair.com'];
const SKIP_IFRAME_SLUGS = ['services', 'locations', 'brands', 'for-businesses', '404'];

function checkFile(fpath, domain) {
  const html = fs.readFileSync(fpath, 'utf8');
  const slug = path.basename(fpath, '.html');
  const url  = 'https://' + domain + '/' + (slug === 'index' ? '' : slug);
  const issues = [];

  // Canonical
  const canonMatch = html.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']+)["']/i)
    || html.match(/<link[^>]*href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
  if (!canonMatch) {
    issues.push('no canonical');
  } else if (!canonMatch[1].includes(domain)) {
    issues.push('canonical wrong domain: ' + canonMatch[1].slice(0, 50));
  }

  // Title
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (!titleMatch || titleMatch[1].trim().length < 10) issues.push('title missing/short');
  else if (titleMatch[1].trim().length > 65) issues.push('title too long: ' + titleMatch[1].trim().length + ' chars');

  // Meta description
  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i)
    || html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*name=["']description["']/i);
  if (!descMatch) issues.push('no meta description');
  else if (descMatch[1].length < 100) issues.push('description short: ' + descMatch[1].length + ' chars');

  // H1
  const h1s = html.match(/<h1[^>]*>/gi) || [];
  if (h1s.length === 0) issues.push('no H1');
  else if (h1s.length > 1) issues.push(h1s.length + ' H1 tags (duplicate)');

  // og:image
  if (!html.includes('og:image')) issues.push('no og:image');

  // Phone link
  if (!html.includes('href="tel:') && !html.includes("href='tel:")) issues.push('no phone link');

  // Booking iframe (skip nika + certain page types)
  const skipIframe = SKIP_IFRAME_SITES.includes(domain)
    || SKIP_IFRAME_SLUGS.some(s => slug.includes(s));
  if (!skipIframe && !html.includes(BOOKING_ID)) issues.push('no booking iframe');

  return { url, slug, issues };
}

// ── PHASE 2: HTTP status check ───────────────────────────────────────────────

function fetchStatus(url) {
  return new Promise(resolve => {
    const lib = url.startsWith('https') ? https : http;
    try {
      const req = lib.get(url, { timeout: 10000 }, res => {
        resolve({ url, status: res.statusCode });
        res.resume();
      });
      req.on('error', () => resolve({ url, status: 0 }));
      req.on('timeout', () => { req.destroy(); resolve({ url, status: -1 }); });
    } catch (e) {
      resolve({ url, status: 0 });
    }
  });
}

async function checkHttpBatch(urls, concurrency = 20) {
  const results = [];
  for (let i = 0; i < urls.length; i += concurrency) {
    const batch = urls.slice(i, i + concurrency);
    const res = await Promise.all(batch.map(fetchStatus));
    results.push(...res);
    if ((i + concurrency) % 100 === 0 || i + concurrency >= urls.length) {
      process.stdout.write('  HTTP checked ' + Math.min(i + concurrency, urls.length) + '/' + urls.length + '...\n');
    }
  }
  return results;
}

// ── PHASE 3: Playwright mobile check ────────────────────────────────────────

async function playwrightCheck(urls) {
  let chromium;
  try {
    ({ chromium } = require('playwright'));
  } catch (e) {
    console.log('  [SKIP] Playwright not available: ' + e.message);
    return [];
  }

  const MOBILE = {
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    isMobile: true,
  };

  const browser = await chromium.launch({ headless: true });
  const results = [];

  const BATCH = 8;
  for (let i = 0; i < urls.length; i += BATCH) {
    const batch = urls.slice(i, i + BATCH);
    const batchRes = await Promise.all(batch.map(async url => {
      const ctx  = await browser.newContext({ ...MOBILE });
      const page = await ctx.newPage();
      const jsErrors = [];
      page.on('pageerror', e => jsErrors.push(e.message.slice(0, 80)));
      try {
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 12000 });
        const status = resp ? resp.status() : 0;
        if (status >= 400) return { url, issue: 'HTTP ' + status };
        await page.waitForTimeout(1200);
        const scrollW = await page.evaluate(() => document.documentElement.scrollWidth);
        const viewW  = await page.evaluate(() => window.innerWidth);
        const issues = [];
        if (scrollW > viewW + 5) issues.push('overflow ' + scrollW + '>' + viewW);
        if (jsErrors.length > 0) issues.push('JS: ' + jsErrors[0].slice(0, 60));
        return { url, issues };
      } catch (e) {
        return { url, issue: e.message.slice(0, 60) };
      } finally {
        await ctx.close();
      }
    }));
    results.push(...batchRes);
    process.stdout.write('  Playwright ' + Math.min(i + BATCH, urls.length) + '/' + urls.length + '...\n');
  }

  await browser.close();
  return results;
}

// ── MAIN ─────────────────────────────────────────────────────────────────────

(async () => {
  const sitesToCheck = SITE_ARG
    ? (SITES[SITE_ARG] ? [[SITE_ARG, SITES[SITE_ARG]]] : [])
    : Object.entries(SITES);

  console.log('\n' + '═'.repeat(60));
  console.log('FULL SITE CHECK — ' + new Date().toISOString().slice(0, 16));
  console.log('Sites: ' + sitesToCheck.map(([k]) => k.toUpperCase()).join(', '));
  console.log('═'.repeat(60));

  // ── Phase 1: file scan ────────────────────────────────────────
  console.log('\n▶ PHASE 1: File-based checks (canonical, title, H1, OG, phone, iframe)');
  const allFileResults = [];
  const allUrls = [];

  for (const [key, site] of sitesToCheck) {
    const files = getHtmlFiles(site.dir);
    console.log('  ' + key.toUpperCase() + ': ' + files.length + ' pages');
    for (const fpath of files) {
      const r = checkFile(fpath, site.domain);
      allUrls.push(r.url);
      if (r.issues.length > 0) allFileResults.push({ site: key, ...r });
    }
  }

  const fileOk  = allUrls.length - allFileResults.length;
  const fileWarn = allFileResults.length;
  console.log('\n  Total pages scanned: ' + allUrls.length);
  console.log('  Clean: ' + fileOk + '  Issues: ' + fileWarn);

  // Group issues by type
  const issueTypes = {};
  for (const r of allFileResults) {
    for (const iss of r.issues) {
      const key2 = iss.split(':')[0];
      issueTypes[key2] = (issueTypes[key2] || 0) + 1;
    }
  }
  if (Object.keys(issueTypes).length > 0) {
    console.log('\n  Issue breakdown:');
    for (const [t, n] of Object.entries(issueTypes).sort((a,b) => b[1]-a[1])) {
      console.log('    ' + n + 'x  ' + t);
    }
  }

  // Show worst offenders (pages with 3+ issues)
  const worst = allFileResults.filter(r => r.issues.length >= 3);
  if (worst.length > 0) {
    console.log('\n  Pages with 3+ issues (' + worst.length + '):');
    worst.slice(0, 20).forEach(r => {
      console.log('    [' + r.site + '] ' + r.slug + ': ' + r.issues.join(', '));
    });
    if (worst.length > 20) console.log('    ... and ' + (worst.length - 20) + ' more');
  }

  // ── Phase 2: HTTP status ──────────────────────────────────────
  console.log('\n▶ PHASE 2: HTTP status check (' + allUrls.length + ' URLs)');
  const httpResults = await checkHttpBatch(allUrls, 25);
  const http404 = httpResults.filter(r => r.status === 404);
  const httpErr  = httpResults.filter(r => r.status !== 200 && r.status !== 404 && r.status !== 301 && r.status !== 302);
  const http3xx  = httpResults.filter(r => r.status === 301 || r.status === 302);
  console.log('  200 OK: ' + httpResults.filter(r => r.status === 200).length);
  console.log('  404:    ' + http404.length);
  console.log('  3xx:    ' + http3xx.length);
  console.log('  Error:  ' + httpErr.length);

  if (http404.length > 0) {
    console.log('\n  404 pages:');
    http404.forEach(r => console.log('    ' + r.url));
  }
  if (http3xx.length > 0) {
    console.log('\n  Redirects (may need canonical update):');
    http3xx.slice(0, 10).forEach(r => console.log('    ' + r.status + ' ' + r.url));
  }

  // ── Phase 3: Playwright ────────────────────────────────────────
  if (!FAST) {
    // Sample 60 pages: all 404s + a spread across sites/types
    const sample = [...http404.map(r => r.url)];
    const byDomain = {};
    for (const url of allUrls) {
      const d = new URL(url).hostname;
      if (!byDomain[d]) byDomain[d] = [];
      byDomain[d].push(url);
    }
    for (const [, urls] of Object.entries(byDomain)) {
      const step = Math.max(1, Math.floor(urls.length / 15));
      for (let i = 0; i < urls.length; i += step) {
        if (!sample.includes(urls[i])) sample.push(urls[i]);
      }
    }
    const pwUrls = sample.slice(0, 80);
    console.log('\n▶ PHASE 3: Playwright mobile check (' + pwUrls.length + ' sampled pages)');
    const pwResults = await playwrightCheck(pwUrls);
    const pwIssues  = pwResults.filter(r => (r.issues && r.issues.length > 0) || r.issue);

    if (pwIssues.length === 0) {
      console.log('  All clean — no JS errors or horizontal overflow found');
    } else {
      console.log('\n  Playwright issues (' + pwIssues.length + '):');
      pwIssues.forEach(r => {
        const iss = r.issue || (r.issues && r.issues.join(', ')) || '';
        console.log('    ' + r.url.replace('https://', '').slice(0, 60) + ' → ' + iss);
      });
    }
  }

  // ── Final summary ─────────────────────────────────────────────
  console.log('\n' + '═'.repeat(60));
  console.log('SUMMARY');
  console.log('  Pages scanned:  ' + allUrls.length);
  console.log('  File issues:    ' + fileWarn + ' pages have SEO problems');
  console.log('  404 errors:     ' + http404.length);
  if (!FAST) console.log('  Mobile issues:  see Playwright section above');
  console.log('═'.repeat(60) + '\n');

  // Detailed file issues for review
  if (fileWarn > 0) {
    console.log('FILE ISSUES DETAIL (first 50):');
    allFileResults.slice(0, 50).forEach(r => {
      console.log('  [' + r.site.toUpperCase() + '] ' + r.slug);
      r.issues.forEach(i => console.log('    - ' + i));
    });
    if (allFileResults.length > 50) {
      console.log('  ... and ' + (allFileResults.length - 50) + ' more pages with issues');
    }
  }
})();
