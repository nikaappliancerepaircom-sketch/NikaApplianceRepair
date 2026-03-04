/**
 * Inject internal links from blog posts to relevant service pages.
 *
 * For each blog post in blog/_queue/:
 * 1. Detect which appliance/service is discussed
 * 2. Add a "Related Services" box before the FAQ section
 * 3. Link first text mention of the service to the service page (if not already linked)
 *
 * Usage: node inject-blog-links.js [--dry-run] [--site nar|neary|fixlify] [--published]
 *   --published  Also process already-published blog posts in blog/ (not just _queue)
 */
const fs = require('fs');
const path = require('path');

const SITES = {
  nar: {
    dir: 'C:/nappliancerepair',
    domain: 'https://nappliancerepair.com',
    name: 'N Appliance Repair',
    phone: '(437) 524-1053',
  },
  neary: {
    dir: 'C:/appliancerepairneary',
    domain: 'https://appliancerepairneary.com',
    name: 'Appliance Repair Near Me',
    phone: '(437) 524-1053',
  },
  fixlify: {
    dir: 'C:/fixlifyservices',
    domain: 'https://fixlifyservices.com',
    name: 'Fixlify Appliance Services',
    phone: '(437) 524-1053',
  },
};

// Service page mappings — slug → display name
const SERVICE_PAGES = {
  'dishwasher-repair': 'Dishwasher Repair',
  'dishwasher-installation': 'Dishwasher Installation',
  'fridge-repair': 'Refrigerator Repair',
  'washer-repair': 'Washing Machine Repair',
  'dryer-repair': 'Dryer Repair',
  'oven-repair': 'Oven Repair',
  'stove-repair': 'Stove Repair',
};

// Brand page mappings
const BRAND_PAGES = {
  'samsung': { slug: 'samsung-repair', name: 'Samsung Repair' },
  'lg': { slug: 'lg-repair', name: 'LG Repair' },
  'whirlpool': { slug: 'whirlpool-repair', name: 'Whirlpool Repair' },
  'bosch': { slug: 'bosch-repair', name: 'Bosch Repair' },
  'frigidaire': { slug: 'frigidaire-repair', name: 'Frigidaire Repair' },
  'kenmore': { slug: 'kenmore-repair', name: 'Kenmore Repair' },
  'ge': { slug: 'ge-repair', name: 'GE Repair' },
  'miele': { slug: 'miele-repair', name: 'Miele Repair' },
  'maytag': { slug: 'maytag-repair', name: 'Maytag Repair' },
  'kitchenaid': { slug: 'kitchenaid-repair', name: 'KitchenAid Repair' },
};

// Keyword → service slug mapping for detection (use regex for word boundaries)
const KEYWORDS = [
  { patterns: [/\bdishwasher\b/i, /\bdish washer\b/i], service: 'dishwasher-repair', install: 'dishwasher-installation' },
  { patterns: [/\bfridge\b/i, /\brefrigerator\b/i, /\bfreezer\b/i], service: 'fridge-repair' },
  { patterns: [/(?<!\w)washer\b/i, /\bwashing machine\b/i], service: 'washer-repair', exclude: /\bdishwasher\b/i },
  { patterns: [/\bdryer\b/i], service: 'dryer-repair' },
  { patterns: [/\boven\b/i], service: 'oven-repair' },
  { patterns: [/\bstove\b/i, /\bcooktop\b/i, /\bburner\b/i], service: 'stove-repair' },
];

function detectServices(html, filename) {
  const text = (html + ' ' + filename).toLowerCase();
  const title = (html.match(/<title[^>]*>([^<]+)<\/title>/i) || [])[1] || '';
  const h1 = (html.match(/<h1[^>]*>([^<]+)<\/h1>/i) || [])[1] || '';
  const primary = (title + ' ' + h1 + ' ' + filename).toLowerCase();
  const found = new Set();

  for (const kw of KEYWORDS) {
    // For washer: only match if "washer" appears WITHOUT "dish" before it in title/h1
    if (kw.exclude) {
      // Check primary text (title, h1, filename) for the service keyword
      let matched = false;
      for (const p of kw.patterns) {
        if (p.test(primary)) {
          // Make sure it's not just "dishwasher" triggering "washer"
          const stripped = primary.replace(/dishwasher/gi, '');
          if (p.test(stripped)) { matched = true; break; }
        }
      }
      if (matched) found.add(kw.service);
    } else {
      for (const p of kw.patterns) {
        if (p.test(primary)) {
          found.add(kw.service);
          if (kw.install && /\binstall/i.test(text)) {
            found.add(kw.install);
          }
          break;
        }
      }
    }
  }

  // Detect brands mentioned
  const brands = [];
  for (const [brand, info] of Object.entries(BRAND_PAGES)) {
    // Case-insensitive brand check
    const brandRegex = new RegExp('\\b' + brand + '\\b', 'i');
    if (brandRegex.test(text)) {
      brands.push(info);
    }
  }

  return { services: [...found], brands };
}

function pageExists(siteDir, slug) {
  return fs.existsSync(path.join(siteDir, slug + '.html'));
}

function buildRelatedServicesBox(services, brands, siteDir) {
  const links = [];

  for (const svc of services) {
    if (pageExists(siteDir, svc) && SERVICE_PAGES[svc]) {
      links.push(`<a href="/${svc}">${SERVICE_PAGES[svc]} Toronto & GTA</a>`);
    }
  }

  // Add up to 2 brand links
  let brandCount = 0;
  for (const brand of brands) {
    if (brandCount >= 2) break;
    if (pageExists(siteDir, brand.slug)) {
      links.push(`<a href="/${brand.slug}">${brand.name} Toronto</a>`);
      brandCount++;
    }
  }

  if (links.length === 0) return null;

  return `
<div class="related-services" style="background:#F0F7FF;border:1px solid #D0E3FF;border-radius:8px;padding:20px 24px;margin:40px 0;">
<h3 style="font-size:1.125rem;font-weight:700;margin:0 0 12px;color:#0A0A0A;">Related Services</h3>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
${links.map(l => l.replace('<a ', '<a style="display:inline-block;background:#2563EB;color:#fff;padding:8px 16px;border-radius:6px;font-size:0.875rem;font-weight:600;text-decoration:none;" ')).join('\n')}
</div>
</div>`;
}

function addInlineLink(html, services, siteDir) {
  // For the primary service, link the first text mention in a <p> tag
  // Avoid double-linking (skip if already inside <a>)
  let modified = html;

  for (const svc of services.slice(0, 1)) { // Only primary service
    if (!pageExists(siteDir, svc) || !SERVICE_PAGES[svc]) continue;

    const displayName = SERVICE_PAGES[svc].toLowerCase();
    // Match first occurrence in article body text (not in tags, not already linked)
    // Look for pattern like "dishwasher repair" in a <p> that isn't already a link
    const words = displayName.split(' ');
    const firstWord = words[0]; // e.g., "dishwasher"

    // Build regex to find "dishwasher repair" in body text (case-insensitive)
    const pattern = new RegExp(
      `(<article[^>]*class="article-body"[^>]*>[\\s\\S]*?<p[^>]*>[^<]*?)\\b(${firstWord}\\s+repair)\\b`,
      'i'
    );

    if (pattern.test(modified)) {
      // Check it's not already linked
      const match = modified.match(pattern);
      if (match && !match[0].includes(`href="/${svc}"`)) {
        modified = modified.replace(pattern, (full, before, term) => {
          return `${before}<a href="/${svc}">${term}</a>`;
        });
      }
    }
  }

  return modified;
}

function injectLinks(html, filename, siteDir) {
  const { services, brands } = detectServices(html, filename);

  if (services.length === 0 && brands.length === 0) return null;

  let modified = html;

  // 1. Add Related Services box before FAQ section
  const relatedBox = buildRelatedServicesBox(services, brands, siteDir);
  if (relatedBox) {
    // Try to inject before FAQ section
    if (modified.includes('<div class="faq-section">')) {
      modified = modified.replace(
        '<div class="faq-section">',
        relatedBox + '\n\n<div class="faq-section">'
      );
    } else if (modified.includes('class="cta-box"')) {
      // Inject before the last CTA box
      const lastCtaIdx = modified.lastIndexOf('class="cta-box"');
      const divStart = modified.lastIndexOf('<div', lastCtaIdx);
      if (divStart > 0) {
        modified = modified.slice(0, divStart) + relatedBox + '\n\n' + modified.slice(divStart);
      }
    }
  }

  // 2. Add inline link to first mention of primary service
  modified = addInlineLink(modified, services, siteDir);

  return modified === html ? null : modified;
}

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const includePublished = args.includes('--published');
  const siteArg = args.find(a => a.startsWith('--site='));
  const targetSite = siteArg ? siteArg.split('=')[1] : null;

  const sitesToProcess = targetSite ? { [targetSite]: SITES[targetSite] } : SITES;
  let totalUpdated = 0;

  for (const [siteKey, site] of Object.entries(sitesToProcess)) {
    if (!site) { console.log(`Unknown site: ${siteKey}`); continue; }
    console.log(`\n=== ${site.name} (${site.domain}) ===`);

    const blogDir = path.join(site.dir, 'blog');
    const queueDir = path.join(blogDir, '_queue');
    const dirs = [queueDir];
    if (includePublished) dirs.push(blogDir);

    let updated = 0;
    let skipped = 0;

    for (const dir of dirs) {
      if (!fs.existsSync(dir)) continue;
      const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');
      const label = dir.endsWith('_queue') ? '_queue' : 'published';

      for (const file of files) {
        const filePath = path.join(dir, file);
        const html = fs.readFileSync(filePath, 'utf8');

        // Skip if already has related-services box
        if (html.includes('class="related-services"')) { skipped++; continue; }

        const newHtml = injectLinks(html, file, site.dir);
        if (!newHtml) { skipped++; continue; }

        if (dryRun) {
          const { services, brands } = detectServices(html, file);
          console.log(`  [DRY] ${label}/${file} → ${services.join(', ')}${brands.length ? ' + ' + brands.map(b => b.name).join(', ') : ''}`);
        } else {
          fs.writeFileSync(filePath, newHtml);
        }
        updated++;
      }
    }

    console.log(`  Updated: ${updated} | Skipped: ${skipped}`);
    totalUpdated += updated;
  }

  console.log(`\nTotal: ${totalUpdated} blog posts updated`);
  if (dryRun) console.log('[DRY RUN] No files changed.');
}

main();
