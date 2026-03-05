/**
 * inject-booking-form.js
 * Injects Fixlify booking iframe into all service pages that are missing it.
 * Skips: 404, about, privacy, terms, contact, sitemap, thank-you, for-businesses, blog pages
 *
 * Usage: node inject-booking-form.js [--dry-run] [--site nar|neary|fixlify|nika]
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const DRY = args.includes('--dry-run');
const siteIdx = args.indexOf('--site');
const SITE_ARG = siteIdx !== -1 ? args[siteIdx + 1] : null;

const SITES = {
  nar:    { dir: 'C:/nappliancerepair',      name: 'N Appliance Repair' },
  neary:  { dir: 'C:/appliancerepairneary',  name: 'Appliance Repair Near Me' },
  fixlify:{ dir: 'C:/fixlifyservices',       name: 'Fixlify Services' },
  nika:   { dir: 'C:/NikaApplianceRepair',   name: 'Nika Appliance Repair' },
};

const SKIP_PATTERNS = [
  '404', 'about', 'privacy', 'terms', 'contact', 'sitemap',
  'thank-you', 'for-businesses', 'index'
];

const BOOKING_IFRAME = `<iframe id="fixlify-booking-nicks-appliance-repair-b8c8ce" src="https://hub.fixlify.app/book/nicks-appliance-repair-b8c8ce?embed=true" style="width:100%;height:600px;border:none;display:block;" title="Book a Service" loading="lazy" allowtransparency="true"></iframe>
<script>
window.addEventListener('message',function(e){if(e.data&&e.data.type==='fixlify-resize'){var el=document.getElementById('fixlify-booking-nicks-appliance-repair-b8c8ce');if(el)el.style.height=e.data.height+'px';}});
</script>`;

const BOOKING_SECTION = `
<section style="padding:64px 0;background:#f0f4ff;" id="booking">
  <div style="max-width:860px;margin:0 auto;padding:0 20px;text-align:center;">
    <span style="display:inline-block;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#4f46e5;margin-bottom:12px;">Online Booking</span>
    <h2 style="font-size:1.8rem;margin-bottom:8px;color:#111;">Book Your Repair Online</h2>
    <p style="color:#6b7280;margin-bottom:28px;font-size:15px;">Select a time that works — a certified technician will arrive and fix it right the first time.</p>
    ${BOOKING_IFRAME}
  </div>
</section>
`;

function shouldSkip(filename) {
  const base = path.basename(filename, '.html').toLowerCase();
  return SKIP_PATTERNS.some(p => base === p || base.startsWith(p + '-') || base.endsWith('-' + p));
}

function processDir(dir, siteName) {
  const files = fs.readdirSync(dir)
    .filter(f => f.endsWith('.html'))
    .filter(f => !shouldSkip(f));

  let fixed = 0;
  let skipped = 0;
  let alreadyHas = 0;

  for (const file of files) {
    const fpath = path.join(dir, file);
    const html = fs.readFileSync(fpath, 'utf8');

    if (html.includes('fixlify-booking-nicks-appliance-repair-b8c8ce')) {
      alreadyHas++;
      continue;
    }

    // Insert before </footer> or before </body> if no footer
    const insertBefore = html.includes('<footer') ? '<footer' : '</body>';
    const idx = html.lastIndexOf(insertBefore);
    if (idx === -1) {
      skipped++;
      continue;
    }

    const newHtml = html.slice(0, idx) + BOOKING_SECTION + '\n' + html.slice(idx);

    if (DRY) {
      console.log(`  [DRY] Would fix: ${file}`);
    } else {
      fs.writeFileSync(fpath, newHtml, 'utf8');
    }
    fixed++;
  }

  console.log(`${siteName}: +${fixed} fixed | ${alreadyHas} already had form | ${skipped} skipped (no anchor)`);
  return fixed;
}

const sitesToProcess = SITE_ARG
  ? [[SITE_ARG, SITES[SITE_ARG]]]
  : Object.entries(SITES);

let total = 0;
for (const [key, site] of sitesToProcess) {
  if (!site) { console.error(`Unknown site: ${key}`); continue; }
  console.log(`\n=== ${site.name} (${key}) ===`);
  total += processDir(site.dir, site.name);
}

console.log(`\nTotal pages fixed: ${total}${DRY ? ' (DRY RUN)' : ''}`);
