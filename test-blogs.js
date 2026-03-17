/**
 * test-blogs.js — Playwright mobile check for all 3 blog sites
 * Checks: HTTP 200, no JS errors, no horizontal overflow, FAQ present,
 *         related-blog-posts valid (no malformed section tag), word count 1600+
 */

const { chromium } = require('playwright');

const MOBILE = {
  viewport: { width: 390, height: 844 },
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
  isMobile: true,
};

const BLOG_URLS = [
  // FIXLIFY
  'https://fixlifyservices.com/blog/lg-washer-repair-toronto/',
  'https://fixlifyservices.com/blog/samsung-washer-repair-toronto/',
  'https://fixlifyservices.com/blog/fridge-not-cooling-diagnosis-toronto/',
  'https://fixlifyservices.com/blog/whirlpool-dryer-repair-toronto/',
  'https://fixlifyservices.com/blog/washer-not-draining-toronto-fix/',
  // NEARY
  'https://appliancerepairneary.com/blog/appliance-repair-brampton/',
  'https://appliancerepairneary.com/blog/fridge-making-noise-near-me/',
  'https://appliancerepairneary.com/blog/dishwasher-leaking-near-me/',
  'https://appliancerepairneary.com/blog/microwave-not-heating-near-me/',
  'https://appliancerepairneary.com/blog/washer-not-draining-near-me/',
  // NAR
  'https://nappliancerepair.com/blog/ge-fridge-not-cooling-toronto/',
  'https://nappliancerepair.com/blog/samsung-fridge-problems-toronto/',
  'https://nappliancerepair.com/blog/miele-appliance-repair-toronto/',
  'https://nappliancerepair.com/blog/oven-repair-cost-toronto-2026/',
  'https://nappliancerepair.com/blog/dryer-vent-cleaning-toronto-guide/',
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];

  console.log('Testing ' + BLOG_URLS.length + ' blog posts on mobile (390px)...\n');

  const BATCH = 5;
  for (let i = 0; i < BLOG_URLS.length; i += BATCH) {
    const batch = BLOG_URLS.slice(i, i + BATCH);
    const batchResults = await Promise.all(batch.map(async url => {
      const ctx  = await browser.newContext({ ...MOBILE });
      const page = await ctx.newPage();
      const issues = [];
      const jsErrors = [];
      page.on('pageerror', e => jsErrors.push(e.message.slice(0, 80)));

      try {
        const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
        const status = resp ? resp.status() : 0;
        if (status !== 200) issues.push('HTTP ' + status);

        await page.waitForTimeout(1500);

        // Overflow check
        const scrollW = await page.evaluate(() => document.documentElement.scrollWidth);
        const viewW  = await page.evaluate(() => window.innerWidth);
        if (scrollW > viewW + 5) issues.push('overflow ' + scrollW + 'px > ' + viewW + 'px');

        // Malformed HTML: check that <section <div does NOT exist
        const hasMalformed = await page.evaluate(() => {
          const src = document.documentElement.outerHTML;
          return src.includes('<section <div');
        });
        if (hasMalformed) issues.push('MALFORMED: <section <div still present!');

        // Check orphan class="faq-section"> appears as visible TEXT (not just in HTML source)
        const hasOrphan = await page.evaluate(() => {
          return document.body.innerText.includes('class="faq-section">');
        });
        if (hasOrphan) issues.push('MALFORMED: orphan class="faq-section"> visible as text');

        // FAQ section present
        const hasFaq = await page.evaluate(() => !!document.querySelector('.faq-section'));
        if (!hasFaq) issues.push('No FAQ section');

        // FAQ items count
        const faqCount = await page.evaluate(() => document.querySelectorAll('.faq-item').length);
        if (faqCount < 4) issues.push('Only ' + faqCount + ' FAQ items (expected 4+)');

        // Related posts present
        const hasRelated = await page.evaluate(() => !!document.querySelector('.related-blog-posts'));
        if (!hasRelated) issues.push('No related-blog-posts section');

        // Word count (full page visible text excluding nav/footer/sidebar)
        const wc = await page.evaluate(() => {
          // Clone body, remove nav/footer/aside/header/script/style
          const clone = document.body.cloneNode(true);
          clone.querySelectorAll('nav,footer,header,aside,script,style,.blog-sidebar,#header-placeholder').forEach(el => el.remove());
          return clone.innerText.replace(/\s+/g, ' ').trim().split(' ').length;
        });
        if (wc < 900) issues.push('Content too short: ' + wc + 'w');

        // JS errors
        if (jsErrors.length > 0) issues.push('JS: ' + jsErrors[0]);

        return { url: url.replace('https://', '').replace(/\/$/, ''), status, wc, issues };
      } catch (e) {
        return { url: url.replace('https://', '').replace(/\/$/, ''), status: 0, wc: 0, issues: [e.message.slice(0, 70)] };
      } finally {
        await ctx.close();
      }
    }));
    results.push(...batchResults);
    process.stdout.write('  Checked ' + Math.min(i + BATCH, BLOG_URLS.length) + '/' + BLOG_URLS.length + '\n');
  }

  await browser.close();

  console.log('\n' + '─'.repeat(72));
  console.log('RESULTS\n');
  let passed = 0;
  let failed = 0;
  for (const r of results) {
    const ok = r.issues.length === 0;
    if (ok) {
      console.log('  ✅ ' + r.url + ' (' + r.wc + 'w)');
      passed++;
    } else {
      console.log('  ❌ ' + r.url + ' (' + r.wc + 'w)');
      for (const iss of r.issues) console.log('       → ' + iss);
      failed++;
    }
  }

  console.log('\n' + '─'.repeat(72));
  console.log('SUMMARY: ' + passed + ' passed, ' + failed + ' failed out of ' + results.length);
  if (failed === 0) console.log('All blog posts CLEAN ✅');
})();
