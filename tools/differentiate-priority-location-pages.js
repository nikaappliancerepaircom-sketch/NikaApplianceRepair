#!/usr/bin/env node

/**
 * Remove misplaced Richmond Hill copy from priority Ontario location pages and
 * replace it with truthful, city-specific diagnostic guidance.
 *
 * Usage:
 *   node tools/differentiate-priority-location-pages.js --check
 *   node tools/differentiate-priority-location-pages.js --write
 */

const fs = require('fs');
const path = require('path');

const mode = process.argv[2];
if (!['--check', '--write'].includes(mode)) {
  console.error('Usage: node tools/differentiate-priority-location-pages.js --check|--write');
  process.exit(2);
}

const ROOT = path.resolve(__dirname, '..');
const TARGETS = {
  ajax: {
    name: 'Ajax',
    neighborhoods: "Central West, Pickering Village, South Ajax, Audley, and Nottingham",
    description: 'Residential appliance repair in Ajax for cooling, draining, heating, and control faults. Same-day appointments when available. Call 437-524-1053.',
    problemSummary: 'Use the checks below to narrow down drainage, cooling, heating, and vibration problems before booking appliance repair in Ajax.',
    dishwasher: 'Ajax dishwasher repair for built-in, portable, double, and countertop models. We diagnose poor cleaning, standing water, leaks, and noisy circulation pumps.',
    washer: "Ajax washer repair for front-load, top-load, and high-efficiency models. We diagnose drain faults, spin-cycle vibration, leaks, and machines that will not start.",
    range: 'Ajax stove repair for residential gas and electric models. We diagnose burners that will not heat, ignition faults, uneven temperatures, and control errors.',
    serviceFocus: 'Residential diagnosis for drainage, cooling, heating, and vibration faults across Ajax. Same-day appointments when available, with a 90-day repair warranty.',
  },
  brampton: {
    name: 'Brampton',
    neighborhoods: "Bramalea, Heart Lake, Fletcher's Meadow, Mount Pleasant, and Springdale",
    description: 'Residential appliance repair in Brampton for busy kitchens and laundry rooms. Clear diagnosis, written quote, and same-day appointments when available.',
    problemSummary: 'Use the checks below to narrow down laundry, drainage, cooling, and cooking-appliance faults before booking repair in Brampton.',
    dishwasher: 'Brampton dishwasher repair for built-in, portable, double, and countertop models. We diagnose poor cleaning, standing water, leaks, and heater faults.',
    washer: "Brampton washer repair for front-load, top-load, and high-efficiency models. We diagnose drain faults, repeated imbalance errors, leaks, and machines that will not spin.",
    range: 'Brampton stove repair for residential gas and electric models. We diagnose ignition faults, burners that will not heat, uneven temperatures, and control errors.',
    serviceFocus: 'Residential diagnosis for high-use laundry, kitchen drainage, cooling, and cooking faults across Brampton. Same-day appointments when available, with a 90-day repair warranty.',
  },
  markham: {
    name: 'Markham',
    neighborhoods: 'Unionville, Cornell, Berczy Village, Thornhill, and Markham Village',
    description: 'Residential appliance repair in Markham for standard, built-in, and premium household appliances. Written quote and 90-day repair warranty.',
    problemSummary: 'Use the checks below to narrow down built-in appliance, refrigeration, drainage, and cooking faults before booking repair in Markham.',
    dishwasher: 'Markham dishwasher repair for standard and built-in models. We diagnose poor cleaning, drainage faults, leaks, heater errors, and cabinet-access constraints.',
    washer: "Markham washer repair for front-load, top-load, compact, and stacked models. We diagnose drain faults, imbalance errors, leaks, and machines that will not spin.",
    range: 'Markham stove repair for residential gas, electric, and induction models. We diagnose ignition faults, heating errors, temperature problems, and control failures.',
    serviceFocus: 'Residential diagnosis for built-in appliances, refrigeration, drainage, and cooking faults across Markham. Same-day appointments when available, with a 90-day repair warranty.',
  },
  mississauga: {
    name: 'Mississauga',
    neighborhoods: 'Port Credit, Square One, Streetsville, Meadowvale, and Clarkson',
    description: 'Residential appliance repair in Mississauga for condo, townhouse, and detached-home appliances. Clear diagnosis and same-day appointments when available.',
    problemSummary: 'Use the checks below to narrow down condo access, drainage, cooling, and laundry faults before booking appliance repair in Mississauga.',
    dishwasher: 'Mississauga dishwasher repair for built-in, portable, double, and countertop models. We diagnose standing water, poor cleaning, leaks, and heater faults.',
    washer: "Mississauga washer repair for full-size, compact, and stacked laundry units. We diagnose drain faults, vibration, leaks, and machines that will not spin.",
    range: 'Mississauga stove repair for residential gas, electric, and induction models. We diagnose ignition faults, burners that will not heat, uneven temperatures, and control errors.',
    serviceFocus: 'Residential diagnosis for condo-access, drainage, cooling, and laundry faults across Mississauga. Same-day appointments when available, with a 90-day repair warranty.',
  },
  oshawa: {
    name: 'Oshawa',
    neighborhoods: "Windfields, Taunton, O'Neill, Donevan, and Eastdale",
    description: 'Residential appliance repair in Oshawa for cooling, laundry, drainage, and cooking faults. Written quote and same-day appointments when available.',
    problemSummary: 'Use the checks below to narrow down cooling, laundry, drainage, and cooking-appliance faults before booking repair in Oshawa.',
    dishwasher: 'Oshawa dishwasher repair for built-in, portable, double, and countertop models. We diagnose standing water, poor cleaning, leaks, and noisy pumps.',
    washer: "Oshawa washer repair for front-load, top-load, and high-efficiency models. We diagnose drain faults, imbalance errors, leaks, and machines that will not spin.",
    range: 'Oshawa stove repair for residential gas and electric models. We diagnose ignition faults, burners that will not heat, temperature problems, and control errors.',
    serviceFocus: 'Residential diagnosis for cooling, laundry, drainage, and cooking faults across Oshawa. Same-day appointments when available, with a 90-day repair warranty.',
  },
};

const FORBIDDEN = [
  'RICHMOND HILL-SPECIFIC ISSUES',
  'Oak Ridges well water',
  'Yonge Corridor compact',
  'Yonge Corridor condos',
  'Persian/Chinese cooking',
  'Persian (10.1%',
  'Chinese (28.5%',
];

function replaceExact(html, from, to, file, label) {
  const count = html.split(from).length - 1;
  if (count !== 1) {
    throw new Error(`${file}: expected one ${label}, found ${count}`);
  }
  return html.replace(from, to);
}

function removeFaqItem(html, questionFragment, file) {
  const marker = `<span>${questionFragment}`;
  const markerIndex = html.indexOf(marker);
  if (markerIndex === -1) {
    throw new Error(`${file}: FAQ not found: ${questionFragment}`);
  }
  const start = html.lastIndexOf('<div class="faq-item">', markerIndex);
  if (start === -1) {
    throw new Error(`${file}: FAQ wrapper not found: ${questionFragment}`);
  }

  const tokenPattern = /<div\b[^>]*>|<\/div>/g;
  tokenPattern.lastIndex = start;
  let depth = 0;
  let end = -1;
  for (let match = tokenPattern.exec(html); match; match = tokenPattern.exec(html)) {
    depth += match[0].startsWith('</') ? -1 : 1;
    if (depth === 0) {
      end = match.index + match[0].length;
      break;
    }
  }
  if (end === -1) {
    throw new Error(`${file}: unterminated FAQ wrapper: ${questionFragment}`);
  }
  const lineStart = html.lastIndexOf('\n', start) + 1;
  const nextNewline = html.indexOf('\n', end);
  const lineEnd = nextNewline === -1 ? end : nextNewline + 1;
  return html.slice(0, lineStart) + html.slice(lineEnd);
}

function updatedHtml(file, data) {
  let html = fs.readFileSync(file, 'utf8');
  const city = data.name;

  html = replaceExact(
    html,
    `"description": "Expert appliance repair in ${city}. Oak Ridges well water solutions. Serving Persian & Chinese communities. Same-day service. Call 437-524-1053.",`,
    `"description": "${data.description}",`,
    file,
    'WebPage description'
  );
  html = replaceExact(
    html,
    `${city} dishwasher repair for built-in, portable, double, and countertop models. Leaking, flooding, not draining, not cleaning. Oak Ridges well water damage fix.`,
    data.dishwasher,
    file,
    'dishwasher summary'
  );
  html = replaceExact(
    html,
    `${city} stove repair for gas and electric models including residential ranges for Persian and Chinese cooking. Burners not igniting, uneven heat, control issues.`,
    data.range,
    file,
    'stove summary'
  );
  html = replaceExact(
    html,
    `${city} washer repair for front-load, top-load, and high-efficiency models. Won't drain, won't spin, loud noises, leaking, flooding. Oak Ridges well water damage fix.`,
    data.washer,
    file,
    'washer summary'
  );
  html = replaceExact(
    html,
    'RICHMOND HILL-SPECIFIC ISSUES',
    `${city.toUpperCase()} APPLIANCE ISSUES`,
    file,
    'problem badge'
  );
  html = replaceExact(
    html,
    'Learn how to fix urgent issues: Oak Ridges well water damage, Yonge Corridor compact appliances, Persian/Chinese cooking equipment, and European appliance parts.',
    data.problemSummary,
    file,
    'problem summary'
  );
  html = replaceExact(
    html,
    'Samsung, LG, Whirlpool, GE, and all major brands, well water solutions, Persian/Chinese cooking. Same-day service available, 90-day warranty.',
    data.serviceFocus,
    file,
    'service focus'
  );

  const coveragePattern = /<p><strong>Complete coverage:<\/strong> Oak Ridges \(well water specialists\), Yonge Corridor \(European compact appliances\), Bayview Hill, Westbrook, Elgin Mills\. Serving Persian \(10\.1%, 20,400\+\) and Chinese \(28\.5%, 57,600\+\) communities with residential cooking expertise\. Fast response time\.<\/p>/g;
  const coverageMatches = html.match(coveragePattern) || [];
  if (coverageMatches.length !== 1) {
    throw new Error(`${file}: expected one coverage answer, found ${coverageMatches.length}`);
  }
  html = html.replace(
    coveragePattern,
    `<p><strong>City-wide coverage:</strong> We serve ${data.neighborhoods}, plus nearby ${city} communities. Include your postal code, appliance type, and access details when booking so dispatch can confirm the available appointment window.</p>`
  );

  html = removeFaqItem(html, 'Can you repair Oak Ridges well water damage to appliances?', file);
  html = removeFaqItem(html, 'Do you stock parts for European compact appliances in Yonge Corridor condos?', file);
  html = removeFaqItem(html, 'Do you service residential ranges and stoves for Chinese and Persian cooking?', file);

  const brandAnswer = '<p><strong>Experienced with major residential brands.</strong> We service Samsung, LG, Whirlpool, GE, Bosch, KitchenAid, Maytag, Frigidaire, Amana, Electrolux, and Kenmore appliances. Share the full model number when booking so the technician can check service information and likely parts before the visit.</p>';
  html = replaceExact(
    html,
    `<p><strong>Experienced with 90+ brands.</strong> Major residential brands: Samsung, LG, Whirlpool, GE, Bosch, KitchenAid, Maytag, Frigidaire. European compact: Bosch, Blomberg, Asko (18-24"). Asian brands: Midea, Haier. Residential cooking equipment for Persian/Chinese communities. OEM parts direct from manufacturers.</p>`,
    brandAnswer,
    file,
    'brand answer'
  );

  const sameDayPattern = /<p><strong>Yes — same-day service available 7 days\/week, fast response time\.<\/strong> Call <a href="tel:4375241053" style="color: #2196F3; text-decoration: underline;">437-524-1053<\/a> before 2 PM or book online before noon\. Emergency 24\/7 \(\+\$75-150\)\. Licensed technicians for residential appliances, well water priority, culturally-aware service for Persian\/Chinese cooking equipment\. Peak seasons: Winter \(ranges\), Summer \(refrigerators\), December \(holiday cooking\)\.<\/p>/g;
  const sameDayMatches = html.match(sameDayPattern) || [];
  if (sameDayMatches.length !== 1) {
    throw new Error(`${file}: expected one same-day answer, found ${sameDayMatches.length}`);
  }
  html = html.replace(
    sameDayPattern,
    `<p><strong>Same-day appointments are available when the route has capacity.</strong> Call <a href="tel:4375241053" style="color: #2196F3; text-decoration: underline;">437-524-1053</a> or book online with the appliance type, model number, symptoms, postal code, and any condo or parking instructions. Dispatch will confirm the appointment window before the visit.</p>`
  );

  return html;
}

let changed = 0;
for (const [slug, data] of Object.entries(TARGETS)) {
  const file = path.join(ROOT, 'locations', `${slug}.html`);
  const original = fs.readFileSync(file, 'utf8');
  const currentForbidden = FORBIDDEN.filter((phrase) => original.includes(phrase));

  if (mode === '--check') {
    if (currentForbidden.length) {
      console.error(`${path.relative(ROOT, file)}: forbidden copy: ${currentForbidden.join(', ')}`);
      process.exitCode = 1;
    } else {
      console.log(`OK ${path.relative(ROOT, file)}`);
    }
    continue;
  }

  const updated = updatedHtml(file, data);
  const remainingForbidden = FORBIDDEN.filter((phrase) => updated.includes(phrase));
  if (remainingForbidden.length) {
    throw new Error(`${file}: forbidden copy remains: ${remainingForbidden.join(', ')}`);
  }
  if (updated === original) {
    throw new Error(`${file}: no changes produced`);
  }
  fs.writeFileSync(file, updated, 'utf8');
  changed += 1;
  console.log(`UPDATED ${path.relative(ROOT, file)}`);
}

if (mode === '--write') {
  console.log(`Updated ${changed} priority location pages.`);
}
