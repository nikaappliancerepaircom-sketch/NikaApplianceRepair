#!/usr/bin/env node
/**
 * Fix Alberta city pages where title/meta still says "Toronto".
 *
 * Bug: publish-next-page.js generated pages with correct body/schema/H1
 * for Alberta cities, but failed to swap "Toronto" -> city name in the
 * <title>, <meta description>, and OG/Twitter tags.
 *
 * This script targets only those head meta tags. Body text mentions of
 * "Toronto" (e.g. "30% faster than in Toronto" comparison in Calgary
 * pages) are intentionally preserved.
 */

const fs = require('fs');
const path = require('path');

const ALBERTA_CITIES = [
  'edmonton', 'calgary', 'airdrie', 'leduc', 'fort-saskatchewan',
  'sherwood-park', 'spruce-grove', 'st-albert', 'stony-plain', 'strathmore',
  'okotoks', 'cochrane', 'chestermere', 'canmore', 'beaumont',
  'devon', 'langdon', 'high-river'
];

const SERVICES = new Set([
  'dishwasher', 'dryer', 'freezer', 'fridge', 'microwave', 'oven',
  'stove', 'washer', 'range'
]);

const BRANDS = new Set([
  'bosch', 'electrolux', 'frigidaire', 'ge', 'kenmore', 'kitchenaid',
  'lg', 'maytag', 'samsung', 'whirlpool', 'miele'
]);

function citySlugToName(slug) {
  if (slug === 'st-albert') return 'St. Albert';
  return slug.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ');
}

function titleCase(word) {
  return word[0].toUpperCase() + word.slice(1);
}

function parseFilename(filename) {
  // Pattern: <token>-repair-<city>.html where city may contain hyphens
  const base = filename.replace(/\.html$/, '');
  const m = base.match(/^([a-z]+)-repair-(.+)$/);
  if (!m) return null;
  const token = m[1];
  const citySlug = m[2];
  if (!ALBERTA_CITIES.includes(citySlug)) return null;

  let serviceLabel; // for title (e.g. "Oven Repair", "Bosch Appliance Repair")
  let serviceLower; // for description (e.g. "oven repair", "Bosch appliance repair")
  if (BRANDS.has(token)) {
    const BRAND_DISPLAY = {
      lg: 'LG', ge: 'GE', kitchenaid: 'KitchenAid',
    };
    const brand = BRAND_DISPLAY[token] || titleCase(token);
    serviceLabel = `${brand} Appliance Repair`;
    serviceLower = `${brand} appliance repair`;
  } else if (SERVICES.has(token)) {
    serviceLabel = `${titleCase(token)} Repair`;
    serviceLower = `${token} repair`;
  } else {
    return null;
  }

  return {
    token,
    citySlug,
    cityName: citySlugToName(citySlug),
    serviceLabel,
    serviceLower,
  };
}

function fixFile(filepath) {
  const filename = path.basename(filepath);
  const info = parseFilename(filename);
  if (!info) return { filename, skipped: true, reason: 'unparseable' };

  const original = fs.readFileSync(filepath, 'utf8');
  let content = original;
  let replacements = 0;

  const cityName = info.cityName;
  const svcTitle = info.serviceLabel;       // "Oven Repair" or "Bosch Appliance Repair"
  const svcLower = info.serviceLower;       // "oven repair" or "Bosch appliance repair"

  // Build expected buggy strings (these came verbatim from the Toronto template)
  // and their replacements.
  const replaceLiteral = (oldStr, newStr) => {
    if (oldStr === newStr) return;
    if (content.includes(oldStr)) {
      const before = content;
      content = content.split(oldStr).join(newStr);
      // count occurrences replaced
      const occ = (before.length - content.length) / (oldStr.length - newStr.length || 1);
      replacements += Math.max(1, Math.round(occ));
    }
  };

  // 1. <title>Oven Repair Toronto | ... -> Oven Repair <City> | ...
  //    <title>Bosch Appliance Repair Toronto | ... -> Bosch Appliance Repair <City> | ...
  replaceLiteral(`<title>${svcTitle} Toronto |`, `<title>${svcTitle} ${cityName} |`);

  // 2. <meta name="description" content="Certified <svc> in Toronto since 2017...
  replaceLiteral(
    `<meta name="description" content="Certified ${svcLower} in Toronto since 2017`,
    `<meta name="description" content="Certified ${svcLower} in ${cityName} since 2017`
  );

  // 3. og:title - same template as <title>
  replaceLiteral(
    `<meta property="og:title" content="${svcTitle} Toronto |`,
    `<meta property="og:title" content="${svcTitle} ${cityName} |`
  );

  // 4. og:description - same as description
  replaceLiteral(
    `<meta property="og:description" content="Certified ${svcLower} in Toronto since 2017`,
    `<meta property="og:description" content="Certified ${svcLower} in ${cityName} since 2017`
  );

  // 5. twitter:title
  replaceLiteral(
    `<meta name="twitter:title" content="${svcTitle} Toronto |`,
    `<meta name="twitter:title" content="${svcTitle} ${cityName} |`
  );

  // 6. twitter:description
  replaceLiteral(
    `<meta name="twitter:description" content="Certified ${svcLower} in Toronto since 2017`,
    `<meta name="twitter:description" content="Certified ${svcLower} in ${cityName} since 2017`
  );

  if (content === original) {
    return { filename, changed: false, replacements: 0 };
  }

  fs.writeFileSync(filepath, content, 'utf8');
  return { filename, changed: true, replacements, cityName, serviceLabel: svcTitle };
}

function main() {
  const dirs = [__dirname, path.join(__dirname, '_pages_queue')];
  const targets = [];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir).filter(f => /^[a-z]+-repair-[a-z-]+\.html$/.test(f));
    for (const f of files) {
      if (parseFilename(f) !== null) {
        targets.push({ dir, file: f });
      }
    }
  }

  console.log(`Found ${targets.length} Alberta target files (root + _pages_queue)`);

  let changed = 0;
  let unchanged = 0;
  let totalReps = 0;
  const failed = [];
  const cities = new Set();

  for (const t of targets) {
    const f = t.file;
    try {
      const r = fixFile(path.join(t.dir, f));
      if (r.changed) {
        changed++;
        totalReps += r.replacements;
        cities.add(r.cityName);
        console.log(`  fixed ${f}: ${r.replacements} replacements (city=${r.cityName}, svc=${r.serviceLabel})`);
      } else if (r.skipped) {
        failed.push(`${f} skipped: ${r.reason}`);
      } else {
        unchanged++;
        console.log(`  unchanged ${f} (no Toronto template found)`);
      }
    } catch (e) {
      failed.push(`${f}: ${e.message}`);
    }
  }

  console.log('\n=== SUMMARY ===');
  console.log(`Files changed:       ${changed}`);
  console.log(`Files unchanged:     ${unchanged}`);
  console.log(`Files failed:        ${failed.length}`);
  console.log(`Total replacements:  ${totalReps}`);
  console.log(`Cities processed:    ${[...cities].sort().join(', ')}`);
  if (failed.length) {
    console.log('Failures:');
    failed.forEach(f => console.log(`  ${f}`));
  }
}

main();
