// Validates Alberta footer + schema templates.
// Run: node _validate.js
const fs = require('fs');
const path = require('path');

const dir = __dirname;
let pass = 0, fail = 0;
const out = [];
const ok  = (msg) => { pass++; out.push(`PASS  ${msg}`); };
const bad = (msg) => { fail++; out.push(`FAIL  ${msg}`); };

// 1) JSON validity + no telephone field
for (const f of ['schema-edmonton.json', 'schema-calgary.json']) {
  const p = path.join(dir, f);
  let data;
  try {
    data = JSON.parse(fs.readFileSync(p, 'utf8'));
    ok(`${f} — JSON.parse succeeded`);
  } catch (e) {
    bad(`${f} — JSON.parse error: ${e.message}`);
    continue;
  }
  // Required fields
  for (const k of ['@context','@type','name','address','geo','areaServed','openingHoursSpecification']) {
    if (data[k] !== undefined) ok(`${f} — has "${k}"`);
    else bad(`${f} — missing "${k}"`);
  }
  // Forbidden fields
  if (data.telephone !== undefined) bad(`${f} — has telephone (FORBIDDEN Phase 1)`);
  else ok(`${f} — no telephone field`);
  if (data.aggregateRating !== undefined) bad(`${f} — has aggregateRating (FORBIDDEN Phase 1)`);
  else ok(`${f} — no aggregateRating field`);
  // Type must be ProfessionalService
  if (data['@type'] === 'ProfessionalService') ok(`${f} — @type is ProfessionalService`);
  else bad(`${f} — @type is "${data['@type']}", expected ProfessionalService`);
  // Address sanity
  const addr = data.address || {};
  if (addr.addressRegion === 'AB') ok(`${f} — addressRegion AB`);
  else bad(`${f} — addressRegion is "${addr.addressRegion}", expected AB`);
  if (addr.addressCountry === 'CA') ok(`${f} — addressCountry CA`);
  else bad(`${f} — addressCountry is "${addr.addressCountry}"`);
}

// 2) HTML footers — must have well-balanced tags + no Toronto refs
const footerFiles = [
  { f: 'footer-edmonton.html', forbidden: /toronto|ontario|\bGTA\b|\(437\)|\(416\)|\(647\)|tel:/i, mustHave: ['10025 102A Avenue', 'Edmonton', 'edmonton@fixlifyservices.com', 'Sherwood Park'] },
  { f: 'footer-calgary.html',  forbidden: /toronto|ontario|\bGTA\b|\(437\)|\(416\)|\(647\)|tel:/i, mustHave: ['700 6th Avenue', 'Calgary', 'calgary@appliancerepairneary.com', 'Airdrie'] },
];

for (const { f, forbidden, mustHave } of footerFiles) {
  const p = path.join(dir, f);
  const html = fs.readFileSync(p, 'utf8');

  // Tag balance — count opening vs closing for key tags
  const tagBalance = (tag) => {
    const open = (html.match(new RegExp(`<${tag}\\b[^>]*>`, 'gi')) || []).length;
    const close = (html.match(new RegExp(`</${tag}>`, 'gi')) || []).length;
    return [open, close];
  };
  for (const tag of ['footer','div','ul','li','p','span','a','address','h4']) {
    const [o, c] = tagBalance(tag);
    if (o === c) ok(`${f} — <${tag}> balanced (${o})`);
    else bad(`${f} — <${tag}> imbalanced: open=${o}, close=${c}`);
  }

  // No forbidden Toronto/phone strings
  if (forbidden.test(html)) {
    const m = html.match(forbidden);
    bad(`${f} — contains forbidden token: "${m[0]}"`);
  } else {
    ok(`${f} — no forbidden Toronto/phone tokens`);
  }

  // Required strings
  for (const s of mustHave) {
    if (html.includes(s)) ok(`${f} — contains required "${s}"`);
    else bad(`${f} — missing required "${s}"`);
  }

  // Microdata present
  if (/itemscope[^>]*itemtype="https:\/\/schema\.org\/PostalAddress"/.test(html)) {
    ok(`${f} — has PostalAddress microdata`);
  } else {
    bad(`${f} — missing PostalAddress microdata`);
  }
}

// 3) Schema files must not contain Toronto strings either
for (const f of ['schema-edmonton.json', 'schema-calgary.json']) {
  const p = path.join(dir, f);
  const txt = fs.readFileSync(p, 'utf8');
  if (/toronto|ontario|\bGTA\b|\(437\)|\(416\)/i.test(txt)) {
    const m = txt.match(/toronto|ontario|\bGTA\b|\(437\)|\(416\)/i);
    bad(`${f} — contains forbidden Toronto token: "${m[0]}"`);
  } else {
    ok(`${f} — no forbidden Toronto tokens`);
  }
}

// 4) Default footer SHOULD still contain Toronto refs (it's the Toronto footer)
{
  const p = path.join(dir, 'footer-default.html');
  const html = fs.readFileSync(p, 'utf8');
  if (/Toronto|GTA|East Gwillimbury/i.test(html)) ok('footer-default.html — still contains Toronto/GTA references (expected)');
  else bad('footer-default.html — missing Toronto references (it should keep them)');
}

console.log(out.join('\n'));
console.log(`\n=== ${pass} pass / ${fail} fail ===`);
process.exit(fail === 0 ? 0 : 1);
