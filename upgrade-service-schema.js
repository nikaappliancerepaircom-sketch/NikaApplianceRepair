/**
 * Upgrade Service + ServiceArea schema on all service pages across satellite sites.
 *
 * Enhances existing Service schema with:
 * - serviceType
 * - areaServed as proper GeoShape/AdministrativeArea
 * - offers with price range
 * - serviceOutput
 *
 * Usage: node upgrade-service-schema.js [--dry-run] [--site nar|neary|fixlify]
 */
const fs = require('fs');
const path = require('path');

const SITES = {
  nar: {
    dir: 'C:/nappliancerepair',
    domain: 'https://nappliancerepair.com',
    name: 'N Appliance Repair',
    phone: '+14375241053',
  },
  neary: {
    dir: 'C:/appliancerepairneary',
    domain: 'https://appliancerepairneary.com',
    name: 'Appliance Repair Near Me',
    phone: '+14375241053',
  },
  fixlify: {
    dir: 'C:/fixlifyservices',
    domain: 'https://fixlifyservices.com',
    name: 'Fixlify Appliance Services',
    phone: '+14375241053',
  },
};

// Map service slug prefixes to service info
const SERVICE_MAP = {
  'dishwasher-repair': { type: 'Dishwasher Repair', price: '$120–$350', low: 120, high: 350 },
  'dishwasher-installation': { type: 'Dishwasher Installation', price: '$150–$400', low: 150, high: 400 },
  'fridge-repair': { type: 'Refrigerator Repair', price: '$150–$450', low: 150, high: 450 },
  'washer-repair': { type: 'Washing Machine Repair', price: '$130–$380', low: 130, high: 380 },
  'dryer-repair': { type: 'Dryer Repair', price: '$120–$350', low: 120, high: 350 },
  'oven-repair': { type: 'Oven Repair', price: '$130–$400', low: 130, high: 400 },
  'stove-repair': { type: 'Stove Repair', price: '$130–$400', low: 130, high: 400 },
  'gas-appliance-repair': { type: 'Gas Appliance Repair', price: '$150–$450', low: 150, high: 450 },
  'gas-dryer-repair': { type: 'Gas Dryer Repair', price: '$150–$400', low: 150, high: 400 },
  'gas-oven-repair': { type: 'Gas Oven Repair', price: '$160–$450', low: 160, high: 450 },
  'gas-stove-repair': { type: 'Gas Stove Repair', price: '$160–$450', low: 160, high: 450 },
};

// Brand-specific pages
const BRAND_SERVICES = {
  'samsung': 'Samsung',
  'lg': 'LG',
  'whirlpool': 'Whirlpool',
  'bosch': 'Bosch',
  'frigidaire': 'Frigidaire',
  'kenmore': 'Kenmore',
  'ge': 'GE',
  'miele': 'Miele',
  'maytag': 'Maytag',
  'kitchenaid': 'KitchenAid',
};

const APPLIANCE_FROM_SLUG = {
  'dishwasher-repair': 'Dishwasher',
  'fridge-repair': 'Refrigerator',
  'washer-repair': 'Washing Machine',
  'dryer-repair': 'Dryer',
  'oven-repair': 'Oven',
  'stove-repair': 'Stove',
  'repair': 'Appliance',
};

// Toronto GTA areas for ServiceArea
const GTA_AREAS = [
  'Toronto', 'North York', 'Scarborough', 'Etobicoke', 'Mississauga',
  'Brampton', 'Markham', 'Vaughan', 'Richmond Hill', 'Oakville',
  'Burlington', 'Ajax', 'Pickering', 'Whitby', 'Oshawa',
];

function getServiceInfo(filename) {
  const slug = filename.replace('.html', '');

  // Brand-specific pages (e.g., samsung-dishwasher-repair, lg-repair)
  for (const [prefix, brand] of Object.entries(BRAND_SERVICES)) {
    if (slug.startsWith(prefix + '-')) {
      const rest = slug.slice(prefix.length + 1);
      // e.g., samsung-dishwasher-repair → Dishwasher Repair
      for (const [svcSlug, svcInfo] of Object.entries(SERVICE_MAP)) {
        if (rest.startsWith(svcSlug.split('-')[0])) {
          return { ...svcInfo, type: `${brand} ${svcInfo.type}`, brand };
        }
      }
      // e.g., samsung-repair → Samsung Appliance Repair
      if (rest === 'repair') {
        return { type: `${brand} Appliance Repair`, price: '$120–$450', low: 120, high: 450, brand };
      }
    }
  }

  // Service + city pages (e.g., dishwasher-repair-north-york)
  for (const [svcSlug, svcInfo] of Object.entries(SERVICE_MAP)) {
    if (slug.startsWith(svcSlug)) {
      return svcInfo;
    }
  }

  return null;
}

function getAreaFromFilename(filename) {
  const slug = filename.replace('.html', '');

  // Check if it's a city-only page
  const cityPages = ['toronto', 'scarborough', 'north-york', 'etobicoke', 'mississauga',
    'brampton', 'markham', 'vaughan', 'richmond-hill', 'oakville', 'burlington',
    'ajax', 'pickering', 'whitby', 'oshawa'];
  if (cityPages.includes(slug)) return titleCase(slug);

  // Extract area from service-city pattern
  for (const svcSlug of Object.keys(SERVICE_MAP)) {
    if (slug.startsWith(svcSlug + '-')) {
      const area = slug.slice(svcSlug.length + 1);
      return titleCase(area);
    }
  }

  return null;
}

function titleCase(str) {
  return str.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function buildServiceSchema(svcInfo, area, siteName) {
  const areaServed = area ? {
    '@type': 'AdministrativeArea',
    'name': area,
    'containedInPlace': {
      '@type': 'AdministrativeArea',
      'name': 'Greater Toronto Area, Ontario, Canada',
    }
  } : GTA_AREAS.map(a => ({
    '@type': 'AdministrativeArea',
    'name': a,
    'containedInPlace': {
      '@type': 'AdministrativeArea',
      'name': 'Ontario, Canada',
    }
  }));

  const schema = {
    '@type': 'Service',
    'serviceType': svcInfo.type,
    'name': area ? `${svcInfo.type} in ${area}` : svcInfo.type,
    'provider': {
      '@type': 'LocalBusiness',
      'name': siteName,
    },
    'areaServed': areaServed,
    'description': area
      ? `Professional ${svcInfo.type.toLowerCase()} service in ${area}. Same-day appointments available.`
      : `Professional ${svcInfo.type.toLowerCase()} service across the Greater Toronto Area. Same-day appointments available.`,
    'offers': {
      '@type': 'AggregateOffer',
      'priceCurrency': 'CAD',
      'lowPrice': String(svcInfo.low),
      'highPrice': String(svcInfo.high),
    },
    'termsOfService': 'https://nappliancerepair.com/pricing',
    'serviceOutput': 'Repaired appliance with 90-day warranty on parts and labour',
  };

  if (svcInfo.brand) {
    schema.brand = {
      '@type': 'Brand',
      'name': svcInfo.brand,
    };
  }

  return schema;
}

function upgradeSchema(html, svcInfo, area, site) {
  // Find the existing JSON-LD script with @graph
  const graphRegex = /<script type="application\/ld\+json">\s*\{[\s\S]*?"@graph"\s*:\s*\[([\s\S]*?)\]\s*\}\s*<\/script>/;
  const match = html.match(graphRegex);

  if (!match) return null; // No @graph schema found

  try {
    // Extract the full JSON-LD block
    const fullMatch = match[0];
    const jsonStart = fullMatch.indexOf('{');
    const jsonEnd = fullMatch.lastIndexOf('}');
    const jsonStr = fullMatch.slice(jsonStart, jsonEnd + 1);
    const data = JSON.parse(jsonStr);

    // Find and replace the Service entry in @graph
    let replaced = false;
    for (let i = 0; i < data['@graph'].length; i++) {
      if (data['@graph'][i]['@type'] === 'Service') {
        data['@graph'][i] = buildServiceSchema(svcInfo, area, site.name);
        replaced = true;
        break;
      }
    }

    if (!replaced) {
      // No Service in graph yet — add one
      data['@graph'].push(buildServiceSchema(svcInfo, area, site.name));
    }

    const newJsonLd = '<script type="application/ld+json">' + JSON.stringify(data, null, 2) + '</script>';
    return html.replace(fullMatch, newJsonLd);
  } catch (e) {
    return null; // JSON parse error, skip
  }
}

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const siteArg = args.find(a => a.startsWith('--site='));
  const targetSite = siteArg ? siteArg.split('=')[1] : null;

  const sitesToProcess = targetSite ? { [targetSite]: SITES[targetSite] } : SITES;
  let totalUpdated = 0;
  let totalSkipped = 0;

  for (const [siteKey, site] of Object.entries(sitesToProcess)) {
    if (!site) { console.log(`Unknown site: ${siteKey}`); continue; }
    console.log(`\n=== ${site.name} (${site.domain}) ===`);

    const files = fs.readdirSync(site.dir).filter(f => f.endsWith('.html'));
    let updated = 0;
    let skipped = 0;

    for (const file of files) {
      const svcInfo = getServiceInfo(file);
      if (!svcInfo) { skipped++; continue; }

      const area = getAreaFromFilename(file);
      const filePath = path.join(site.dir, file);
      const html = fs.readFileSync(filePath, 'utf8');

      // Check if already upgraded (has AggregateOffer)
      if (html.includes('"AggregateOffer"') && html.includes('"serviceType"')) {
        skipped++;
        continue;
      }

      const newHtml = upgradeSchema(html, svcInfo, area, site);
      if (!newHtml) { skipped++; continue; }

      if (dryRun) {
        console.log(`  [DRY] ${file} → ${svcInfo.type}${area ? ' in ' + area : ''}`);
      } else {
        fs.writeFileSync(filePath, newHtml);
      }
      updated++;
    }

    console.log(`  Updated: ${updated} | Skipped: ${skipped}`);
    totalUpdated += updated;
    totalSkipped += skipped;
  }

  console.log(`\nTotal: ${totalUpdated} updated, ${totalSkipped} skipped`);
  if (dryRun) console.log('[DRY RUN] No files changed.');
}

main();
