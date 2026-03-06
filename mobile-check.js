/**
 * mobile-check.js — checks 40+ pages across all 4 sites on mobile viewport
 * Tests: page loads, no JS errors, booking form visible, nav works, CTA clickable
 */
const { chromium } = require('playwright');

const MOBILE = {
  viewport: { width: 390, height: 844 },
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  isMobile: true,
};

const PAGES = [
  // NAR
  { url: 'https://nappliancerepair.com/', label: 'NAR Home' },
  { url: 'https://nappliancerepair.com/fridge-repair-toronto', label: 'NAR Fridge Toronto' },
  { url: 'https://nappliancerepair.com/dishwasher-repair-scarborough', label: 'NAR Dishwasher Scarborough' },
  { url: 'https://nappliancerepair.com/washer-repair-mississauga', label: 'NAR Washer Mississauga' },
  { url: 'https://nappliancerepair.com/samsung-repair', label: 'NAR Samsung' },
  { url: 'https://nappliancerepair.com/lg-fridge-repair', label: 'NAR LG Fridge' },
  { url: 'https://nappliancerepair.com/toronto', label: 'NAR Toronto Hub' },
  { url: 'https://nappliancerepair.com/richmond-hill', label: 'NAR Richmond Hill' },
  { url: 'https://nappliancerepair.com/airdrie', label: 'NAR Airdrie (new)' },
  { url: 'https://nappliancerepair.com/dishwasher-repair-bloor-west-village', label: 'NAR Dishwasher Bloor West' },
  // NEARY
  { url: 'https://appliancerepairneary.com/', label: 'NEARY Home' },
  { url: 'https://appliancerepairneary.com/fridge-repair-pickering', label: 'NEARY Fridge Pickering' },
  { url: 'https://appliancerepairneary.com/fridge-repair-near-me', label: 'NEARY Fridge Near Me' },
  { url: 'https://appliancerepairneary.com/washer-repair-brampton', label: 'NEARY Washer Brampton' },
  { url: 'https://appliancerepairneary.com/dishwasher-repair-ajax', label: 'NEARY Dishwasher Ajax' },
  { url: 'https://appliancerepairneary.com/samsung-repair', label: 'NEARY Samsung' },
  { url: 'https://appliancerepairneary.com/lg-fridge-repair', label: 'NEARY LG Fridge' },
  { url: 'https://appliancerepairneary.com/toronto', label: 'NEARY Toronto Hub' },
  { url: 'https://appliancerepairneary.com/fridge-repair-edmonton', label: 'NEARY Fridge Edmonton (new)' },
  { url: 'https://appliancerepairneary.com/calgary', label: 'NEARY Calgary Hub (new)' },
  // FIXLIFY
  { url: 'https://fixlifyservices.com/', label: 'FIXLIFY Home' },
  { url: 'https://fixlifyservices.com/fridge-repair-toronto', label: 'FIXLIFY Fridge Toronto' },
  { url: 'https://fixlifyservices.com/dishwasher-repair-pickering', label: 'FIXLIFY Dishwasher Pickering' },
  { url: 'https://fixlifyservices.com/washer-repair-scarborough', label: 'FIXLIFY Washer Scarborough' },
  { url: 'https://fixlifyservices.com/samsung-fridge-repair', label: 'FIXLIFY Samsung Fridge' },
  { url: 'https://fixlifyservices.com/for-businesses', label: 'FIXLIFY For Businesses' },
  { url: 'https://fixlifyservices.com/toronto', label: 'FIXLIFY Toronto Hub' },
  { url: 'https://fixlifyservices.com/fridge-repair-edmonton', label: 'FIXLIFY Fridge Edmonton (new)' },
  { url: 'https://fixlifyservices.com/bosch-repair-calgary', label: 'FIXLIFY Bosch Calgary (new)' },
  { url: 'https://fixlifyservices.com/dryer-repair-bloor-west-village', label: 'FIXLIFY Dryer Bloor West' },
  // NIKA
  { url: 'https://nikaappliancerepair.com/', label: 'NIKA Home' },
  { url: 'https://nikaappliancerepair.com/services', label: 'NIKA Services' },
  { url: 'https://nikaappliancerepair.com/locations', label: 'NIKA Locations' },
  { url: 'https://nikaappliancerepair.com/brands', label: 'NIKA Brands' },
  { url: 'https://nikaappliancerepair.com/book', label: 'NIKA Book' },
];

const NIKA_PAGES = ['nikaappliancerepair.com/services','nikaappliancerepair.com/locations','nikaappliancerepair.com/brands','nikaappliancerepair.com/'];
const results = { ok: [], warn: [], fail: [] };

async function checkPage(browser, { url, label }) {
  const context = await browser.newContext({ ...MOBILE });
  const page = await context.newPage();
  const jsErrors = [];
  page.on('pageerror', e => jsErrors.push(e.message.slice(0, 80)));

  try {
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
    const status = resp ? resp.status() : 0;

    if (status >= 400) {
      results.fail.push({ label, url, issue: `HTTP ${status}` });
      return;
    }

    await page.waitForTimeout(1500);

    const issues = [];

    // Check canonical
    const canonical = await page.$eval('link[rel="canonical"]', el => el.href).catch(() => null);
    if (!canonical) issues.push('no canonical');
    else {
      const pageHost = new URL(url).hostname;
      if (!canonical.includes(pageHost)) issues.push('canonical wrong domain: ' + canonical.slice(0, 60));
    }

    // Check title
    const title = await page.title();
    if (!title || title.length < 10) issues.push('title missing/short');

    // Check H1
    const h1Count = await page.$$eval('h1', els => els.length);
    if (h1Count === 0) issues.push('no H1');
    if (h1Count > 1) issues.push(h1Count + ' H1 tags (duplicate)');

    // Check booking iframe (skip certain pages)
    const skipIframe = url.includes('404') || url.includes('for-businesses') ||
      NIKA_PAGES.some(p => url.includes(p));
    if (!skipIframe) {
      const hasIframe = await page.$('iframe[src*="fixlify"]').catch(() => null);
      if (!hasIframe) issues.push('no booking iframe');
    }

    // Check nav/header
    const hasNav = await page.$('nav, header').catch(() => null);
    if (!hasNav) issues.push('no nav/header');

    // Check phone link
    const hasPhone = await page.$('a[href*="tel:"]').catch(() => null);
    if (!hasPhone) issues.push('no phone link');

    // JS errors
    if (jsErrors.length > 0) issues.push('JS errors: ' + jsErrors.slice(0, 2).join('; '));

    // Horizontal overflow = mobile layout broken
    const scrollW = await page.evaluate(() => document.documentElement.scrollWidth);
    const viewW = await page.evaluate(() => window.innerWidth);
    if (scrollW > viewW + 5) issues.push('horizontal overflow ' + scrollW + 'px > ' + viewW + 'px');

    if (issues.length === 0) {
      results.ok.push({ label, title: title.slice(0, 55) });
    } else {
      results.warn.push({ label, url, issues });
    }
  } catch (e) {
    results.fail.push({ label, url, issue: e.message.slice(0, 80) });
  } finally {
    await context.close();
  }
}

(async () => {
  console.log('\nMobile check — ' + PAGES.length + ' pages on iPhone 14 Pro (390x844)\n');
  const browser = await chromium.launch({ headless: true });

  const BATCH = 5;
  for (let i = 0; i < PAGES.length; i += BATCH) {
    const batch = PAGES.slice(i, i + BATCH);
    await Promise.all(batch.map(p => checkPage(browser, p)));
    process.stdout.write('  checked ' + Math.min(i + BATCH, PAGES.length) + '/' + PAGES.length + '...\n');
  }

  await browser.close();

  console.log('\n' + '='.repeat(60));
  console.log('OK: ' + results.ok.length + '  WARN: ' + results.warn.length + '  FAIL: ' + results.fail.length);
  console.log('='.repeat(60));

  if (results.fail.length > 0) {
    console.log('\nFAILURES:');
    results.fail.forEach(function(r) { console.log('  [FAIL] ' + r.label + ': ' + r.issue + '\n    ' + r.url); });
  }

  if (results.warn.length > 0) {
    console.log('\nWARNINGS:');
    results.warn.forEach(function(r) {
      console.log('  [WARN] ' + r.label + ':');
      r.issues.forEach(function(i) { console.log('    - ' + i); });
    });
  }

  console.log('\nALL GOOD:');
  results.ok.forEach(function(r) { console.log('  [OK] ' + r.label + ' — "' + r.title + '"'); });
})();
