#!/usr/bin/env node
/**
 * fix-phone-canonical-iframe.js
 * Fixes 3 types of issues found by full-check.js:
 * 1. Missing phone links (tel:) — add before </body>
 * 2. Wrong canonical domain (template placeholders) — fix to match site domain
 * 3. Missing booking iframe — add before </body>
 *
 * Usage:
 *   node fix-phone-canonical-iframe.js           # apply
 *   node fix-phone-canonical-iframe.js --dry-run  # preview
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');

// Pages to skip for phone link check
const SKIP_PHONE = new Set(['404.html', 'sitemap.html', 'privacy.html', 'terms.html', 'for-businesses.html']);

const BOOKING_IFRAME = `
<section class="booking-section" id="booking" style="padding:64px 0;background:#f0f4ff;">
  <div style="max-width:860px;margin:0 auto;padding:0 20px;text-align:center;">
    <span style="display:inline-block;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#4f46e5;margin-bottom:12px;">Online Booking</span>
    <h2 style="font-size:1.8rem;margin-bottom:8px;color:#111;">Book Your Repair Online</h2>
    <p style="color:#6b7280;margin-bottom:28px;font-size:15px;">Select a time that works — a certified technician will arrive and fix it right the first time.</p>
    <iframe id="fixlify-booking-nicks-appliance-repair-b8c8ce" src="https://hub.fixlify.app/book/nicks-appliance-repair-b8c8ce?embed=true" style="width:100%;height:600px;border:none;display:block;" title="Book a Service" loading="lazy" allowtransparency="true"></iframe>
<script>
window.addEventListener('message',function(e){if(e.data&&e.data.type==='fixlify-resize'){var el=document.getElementById('fixlify-booking-nicks-appliance-repair-b8c8ce');if(el)el.style.height=e.data.height+'px';}});
</script>
  </div>
</section>`;

const PHONE_LINK_BLOCK = `
<div style="text-align:center;padding:24px 0;background:#f0f4ff;">
  <a href="tel:4375241053" style="display:inline-flex;align-items:center;gap:8px;font-size:1.1rem;font-weight:600;color:#2563EB;text-decoration:none;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1.003 1.003 0 011.01-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.1.31.03.66-.25 1.02l-2.2 2.2z"/></svg>
    (437) 524-1053
  </a>
</div>`;

const stats = { phoneFix: 0, canonicalFix: 0, iframeFix: 0 };
const fixedPages = { phone: [], canonical: [], iframe: [] };

function processFile(filePath, domain) {
  const fileName = path.basename(filePath);
  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Fix 1: Missing phone link
  if (!SKIP_PHONE.has(fileName) && !html.includes('href="tel:') && !html.includes("href='tel:")) {
    // Also check if it has footer-loader (dynamic phone link)
    if (!html.includes('footer-loader') && !html.includes('footer-placeholder')) {
      // Add phone link block before </body>
      html = html.replace('</body>', PHONE_LINK_BLOCK + '\n</body>');
      changed = true;
      stats.phoneFix++;
      fixedPages.phone.push(filePath);
    }
  }

  // Fix 2: Wrong canonical — template placeholders
  if (html.includes('{{CANONICAL}}') || html.includes('{{canonical}}')) {
    // Build proper canonical from filename + domain
    const slug = fileName.replace('.html', '');
    const canonical = `https://${domain}/${slug}`;
    html = html.replace(/\{\{CANONICAL\}\}/g, canonical);
    html = html.replace(/\{\{canonical\}\}/g, canonical);
    changed = true;
    stats.canonicalFix++;
    fixedPages.canonical.push(filePath);
  }

  // Also check canonical pointing to wrong domain
  if (domain) {
    const canonicalMatch = html.match(/<link rel="canonical" href="https?:\/\/([^/"]+)/);
    if (canonicalMatch && canonicalMatch[1] !== domain && canonicalMatch[1] !== 'www.' + domain) {
      // Check it's a satellite domain mismatch (not an external link)
      const knownDomains = ['nappliancerepair.com', 'appliancerepairneary.com', 'fixlifyservices.com', 'nikaappliancerepair.com'];
      if (knownDomains.includes(canonicalMatch[1])) {
        const oldCanonical = canonicalMatch[0].replace('<link rel="canonical" href="', '');
        const newCanonical = oldCanonical.replace(canonicalMatch[1], domain);
        html = html.replace(oldCanonical, newCanonical);
        changed = true;
        stats.canonicalFix++;
        fixedPages.canonical.push(filePath + ' (domain fix)');
      }
    }
  }

  // Fix 3: Missing booking iframe (skip about, for-businesses, 404, privacy, terms, blog/, service-template)
  const skipIframe = new Set(['404.html', 'about.html', 'for-businesses.html', 'service-template.html',
    'sitemap.html', 'privacy.html', 'terms.html', 'index.html', 'book.html']);
  const isBlog = filePath.includes('/blog/') || filePath.includes('\\blog\\');

  if (!skipIframe.has(fileName) && !isBlog && !html.includes('fixlify-booking') && !html.includes('<iframe')) {
    // Only add if it has a booking-section CSS class defined (means it was intended)
    if (html.includes('booking-section') || html.includes('#booking')) {
      html = html.replace('</body>', BOOKING_IFRAME + '\n</body>');
      changed = true;
      stats.iframeFix++;
      fixedPages.iframe.push(filePath);
    }
  }

  if (changed && !DRY_RUN) {
    fs.writeFileSync(filePath, html, 'utf8');
  }

  return changed;
}

// Process each site
const SITES = [
  { dir: 'C:/NikaApplianceRepair', domain: 'nikaappliancerepair.com', label: 'NIKA' },
  { dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com', label: 'NAR' },
  { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com', label: 'NEARY' },
  { dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com', label: 'FIXLIFY' },
];

console.log(DRY_RUN ? '=== DRY RUN ===' : '=== APPLYING FIXES ===');

for (const site of SITES) {
  console.log(`\n--- ${site.label} (${site.domain}) ---`);
  const beforeStats = { ...stats };

  // Process root HTML files
  const rootFiles = fs.readdirSync(site.dir)
    .filter(f => f.endsWith('.html'))
    .map(f => path.join(site.dir, f));

  for (const f of rootFiles) {
    processFile(f, site.domain);
  }

  // Process blog files
  const blogDir = path.join(site.dir, 'blog');
  if (fs.existsSync(blogDir)) {
    const blogFiles = fs.readdirSync(blogDir)
      .filter(f => f.endsWith('.html'))
      .map(f => path.join(blogDir, f));
    for (const f of blogFiles) {
      processFile(f, site.domain);
    }
  }

  console.log(`  Phone links added: ${stats.phoneFix - beforeStats.phoneFix}`);
  console.log(`  Canonicals fixed: ${stats.canonicalFix - beforeStats.canonicalFix}`);
  console.log(`  Booking iframes added: ${stats.iframeFix - beforeStats.iframeFix}`);
}

console.log('\n=== TOTALS ===');
console.log(`Phone links added: ${stats.phoneFix}`);
console.log(`Canonicals fixed: ${stats.canonicalFix}`);
console.log(`Booking iframes added: ${stats.iframeFix}`);

if (fixedPages.phone.length > 0) {
  console.log('\nPages with phone links added:');
  fixedPages.phone.forEach(f => console.log('  ' + f));
}
if (fixedPages.canonical.length > 0) {
  console.log('\nPages with canonical fixed:');
  fixedPages.canonical.forEach(f => console.log('  ' + f));
}
if (fixedPages.iframe.length > 0) {
  console.log('\nPages with booking iframe added:');
  fixedPages.iframe.forEach(f => console.log('  ' + f));
}
