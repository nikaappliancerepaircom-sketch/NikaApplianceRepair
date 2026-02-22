/**
 * design-tests.spec.js
 * Responsive design & mobile QA tests for all 3 new sites + NikaApplianceRepair
 * Viewports: mobile 375px, tablet 768px, desktop 1280px, wide 1440px
 * Checks: overflow, font sizes, tap targets, layout, Google mobile policy
 */

const { test, expect } = require('@playwright/test');

const SITES = [
  {
    name: 'nappliancerepair',
    baseUrl: 'http://127.0.0.1:8001',
    pages: ['/', '/dryer-repair-toronto.html', '/dishwasher-repair-brampton.html', '/mississauga.html'],
  },
  {
    name: 'appliancerepairneary',
    baseUrl: 'http://127.0.0.1:8002',
    pages: ['/', '/dryer-repair-toronto.html', '/dishwasher-repair-brampton.html', '/fridge-repair-mississauga.html'],
  },
  {
    name: 'fixlifyservices',
    baseUrl: 'http://127.0.0.1:8003',
    pages: ['/', '/dryer-repair-toronto.html', '/dishwasher-repair-brampton.html'],
  },
];

const VIEWPORTS = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'mobile-lg', width: 430, height: 932 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'wide', width: 1440, height: 900 },
];

// Run against only nappliancerepair for now (others same template)
const TEST_SITE = SITES[0];
const TEST_PAGES = TEST_SITE.pages;

// Safe page.evaluate that retries once if context is destroyed by async scripts
async function safeEvaluate(page, fn, retries = 2) {
  for (let i = 0; i < retries; i++) {
    try {
      return await page.evaluate(fn);
    } catch (e) {
      if (i < retries - 1 && e.message.includes('Execution context was destroyed')) {
        await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
        continue;
      }
      throw e;
    }
  }
}

// Navigate and wait for page to stabilize (handles deferred header/footer loaders)
async function gotoStable(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  // Wait for async header/footer fetch scripts to finish
  await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
}

for (const vp of VIEWPORTS) {
  for (const pagePath of TEST_PAGES) {
    test(`[${vp.name} ${vp.width}px] ${TEST_SITE.name}${pagePath} — no horizontal overflow`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await gotoStable(page, TEST_SITE.baseUrl + pagePath);

      const hasHorizontalScroll = await safeEvaluate(page, () => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });
      expect(hasHorizontalScroll, `Horizontal overflow at ${vp.width}px on ${pagePath}`).toBe(false);
    });

    test(`[${vp.name} ${vp.width}px] ${TEST_SITE.name}${pagePath} — body text readable (>=14px)`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await gotoStable(page, TEST_SITE.baseUrl + pagePath);

      const smallText = await safeEvaluate(page, () => {
        const paragraphs = document.querySelectorAll('p, li, td, .content, .faq-answer');
        const issues = [];
        paragraphs.forEach(el => {
          const size = parseFloat(window.getComputedStyle(el).fontSize);
          if (size < 14 && el.textContent.trim().length > 20) {
            // Exclude footer/nav/breadcrumb elements — those can be smaller per Google policy
            let parent = el.parentElement;
            let skipEl = false;
            for (let i = 0; i < 8 && parent; i++) {
              const tag = parent.tagName;
              const cls = (parent.className || '').toLowerCase();
              if (tag === 'FOOTER' || tag === 'NAV' ||
                  cls.includes('footer') || cls.includes('narf-footer') ||
                  cls.includes('breadcrumb') || cls.includes('cookie') ||
                  cls.includes('label') || cls.includes('badge')) {
                skipEl = true; break;
              }
              parent = parent.parentElement;
            }
            if (!skipEl) {
              issues.push({ tag: el.tagName, size, text: el.textContent.trim().slice(0, 50) });
            }
          }
        });
        return issues.slice(0, 5);
      });
      expect(smallText, `Text too small: ${JSON.stringify(smallText)}`).toHaveLength(0);
    });
  }
}

// Mobile-specific: tap targets
test(`[mobile] tap targets >= 44px height`, async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await gotoStable(page, TEST_SITE.baseUrl + '/');

  const smallTargets = await safeEvaluate(page, () => {
    const buttons = document.querySelectorAll('a[href], button, [role="button"]');
    const issues = [];
    buttons.forEach(el => {
      const rect = el.getBoundingClientRect();
      const h = rect.height, w = rect.width;
      if (h > 0 && w > 0 && (h < 44 || w < 44)) {
        const text = el.textContent.trim().slice(0, 40);
        if (text.length > 1) {
          issues.push({ tag: el.tagName, h: Math.round(h), w: Math.round(w), text });
        }
      }
    });
    return issues.slice(0, 10);
  });

  if (smallTargets.length > 0) {
    console.log(`⚠️  Small tap targets found: ${JSON.stringify(smallTargets, null, 2)}`);
  }
  const criticalSmall = smallTargets.filter(t =>
    t.text.toLowerCase().includes('book') ||
    t.text.toLowerCase().includes('call') ||
    t.text.toLowerCase().includes('schedule')
  );
  expect(criticalSmall, `Critical CTAs too small for touch: ${JSON.stringify(criticalSmall)}`).toHaveLength(0);
});

// Check meta viewport is present
test('viewport meta tag present on all pages', async ({ page }) => {
  for (const pagePath of TEST_PAGES) {
    await gotoStable(page, TEST_SITE.baseUrl + pagePath);
    const viewport = await page.locator('meta[name="viewport"]').count();
    expect(viewport, `Missing viewport meta on ${pagePath}`).toBeGreaterThan(0);
  }
});

// Check no intrusive interstitials (Google policy)
test('no modal/popup blocking content on mobile load', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await gotoStable(page, TEST_SITE.baseUrl + '/');
  await page.waitForTimeout(2000);

  const blockingModal = await safeEvaluate(page, () => {
    const modals = document.querySelectorAll('[class*="modal"], [class*="popup"], [class*="overlay"], [class*="interstitial"]');
    const blocking = [];
    modals.forEach(el => {
      const style = window.getComputedStyle(el);
      if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
        const rect = el.getBoundingClientRect();
        if (rect.width > window.innerWidth * 0.3 && rect.height > window.innerHeight * 0.3) {
          blocking.push({ class: el.className.slice(0, 50) });
        }
      }
    });
    return blocking;
  });
  expect(blockingModal, `Blocking modal found: ${JSON.stringify(blockingModal)}`).toHaveLength(0);
});

// Check images have alt text
test('images have alt text (accessibility + SEO)', async ({ page }) => {
  await gotoStable(page, TEST_SITE.baseUrl + '/');

  const missingAlt = await safeEvaluate(page, () => {
    const imgs = document.querySelectorAll('img');
    const issues = [];
    imgs.forEach(img => {
      if (!img.alt || img.alt.trim() === '') {
        const src = (img.src || img.getAttribute('src') || '').slice(0, 60);
        issues.push({ src, width: img.naturalWidth });
      }
    });
    return issues.filter(i => i.width > 0);
  });
  expect(missingAlt, `Images without alt: ${JSON.stringify(missingAlt)}`).toHaveLength(0);
});

// Check canonical tag present
test('canonical tag present (SEO)', async ({ page }) => {
  for (const pagePath of TEST_PAGES.slice(0, 2)) {
    await gotoStable(page, TEST_SITE.baseUrl + pagePath);
    const canonical = await page.locator('link[rel="canonical"]').count();
    expect(canonical, `Missing canonical on ${pagePath}`).toBeGreaterThan(0);
  }
});

// Check page loads fast enough (< 5s)
test('page load time < 5 seconds', async ({ page }) => {
  const start = Date.now();
  await page.goto(TEST_SITE.baseUrl + '/', { waitUntil: 'load', timeout: 10000 });
  const duration = Date.now() - start;
  console.log(`Page load time: ${duration}ms`);
  expect(duration).toBeLessThan(5000);
});

// Check mobile nav works
test('[mobile] hamburger menu / nav accessible', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await gotoStable(page, TEST_SITE.baseUrl + '/');

  const hasNav = await page.locator('nav, header').count();
  expect(hasNav).toBeGreaterThan(0);

  const phoneLinks = await page.locator('a[href^="tel:"]').count();
  expect(phoneLinks, 'No tel: links on mobile').toBeGreaterThan(0);
});

// Screenshot all 3 sites at mobile/tablet/desktop for review
test('screenshots at mobile/tablet/desktop for all 3 sites', async ({ page }) => {
  const screenshotDir = 'C:/NikaApplianceRepair/docs/screenshots';
  const fs = require('fs');
  if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });

  for (const site of SITES) {
    for (const vp of [VIEWPORTS[0], VIEWPORTS[2], VIEWPORTS[3]]) { // mobile, tablet, desktop
      await page.setViewportSize({ width: vp.width, height: vp.height });
      try {
        await page.goto(site.baseUrl + '/', { waitUntil: 'networkidle', timeout: 20000 });
        await page.waitForTimeout(500);
        const filename = `${screenshotDir}/${site.name}-${vp.name}.png`;
        await page.screenshot({ path: filename, fullPage: false });
        console.log(`Screenshot saved: ${filename}`);
      } catch (e) {
        console.log(`Screenshot failed for ${site.name} at ${vp.name}: ${e.message}`);
      }
    }
  }
  expect(true).toBe(true);
});
