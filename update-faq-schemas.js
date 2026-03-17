/**
 * update-faq-schemas.js
 * Replaces generic FAQPage schemas with page-specific questions
 * for brand, brand-service, service, and problem pages.
 *
 * Usage:
 *   node update-faq-schemas.js                  — all 3 sites
 *   node update-faq-schemas.js --site nar        — one site
 *   node update-faq-schemas.js --dry-run         — preview only
 */

const fs   = require('fs');
const path = require('path');

const DRY  = process.argv.includes('--dry-run');
const siteArg = process.argv.indexOf('--site') !== -1 ? process.argv[process.argv.indexOf('--site')+1] : null;

const SITES = {
  nar:     { dir: 'C:/nappliancerepair',     name: 'N Appliance Repair', phone: '(437) 524-1053', area: 'Toronto & GTA' },
  neary:   { dir: 'C:/appliancerepairneary', name: 'Appliance Repair Near You', phone: '(437) 524-1053', area: 'Toronto & GTA' },
  fixlify: { dir: 'C:/fixlifyservices',      name: 'Fixlify Appliance Repair', phone: '(437) 524-1053', area: 'Toronto & GTA' },
};

// ── DATA TABLES ───────────────────────────────────────────────────────────────

const SERVICE_DATA = {
  dishwasher: {
    cost: '$120–$350',
    time: '1–2 hours',
    problems: 'not draining, not cleaning dishes, leaking, won\'t start, broken door latch, error codes, noisy operation',
    worth: 'If the repair cost is under 50% of a new dishwasher price, repair is almost always worth it. Most dishwasher issues—pumps, valves, heating elements—cost $120–$250 to fix vs $600+ for a new unit.',
    parts: 'drain pumps, wash pumps, door latches, control boards, water inlet valves, spray arms, heating elements',
  },
  fridge: {
    cost: '$150–$450',
    time: '1–3 hours',
    problems: 'not cooling, not making ice, leaking water, making loud noise, freezer frosting over, compressor issues, temperature fluctuations',
    worth: 'Fridges are worth repairing if they\'re under 10 years old and the repair is under $400. Common fixes like evaporator fan motors, thermostats, or water valves are very cost-effective.',
    parts: 'compressors, evaporator fans, condenser fans, thermostats, water inlet valves, ice maker assemblies, door gaskets, control boards',
  },
  washer: {
    cost: '$120–$380',
    time: '1–2 hours',
    problems: 'not spinning, not draining, shaking violently, won\'t start, door won\'t lock, making noise, leaking',
    worth: 'Washers under 8 years old are almost always worth repairing. Common issues like lid switches, pumps, or bearings cost far less than replacing the machine.',
    parts: 'door lid switches, drain pumps, motor couplings, bearings, drive belts, control boards, water inlet valves, door seals',
  },
  dryer: {
    cost: '$100–$320',
    time: '1–2 hours',
    problems: 'not heating, taking too long to dry, making squealing or thumping noise, won\'t start, overheating, drum not spinning',
    worth: 'Dryers are the most cost-effective appliance to repair. A heating element or thermal fuse replacement costs $80–$180 vs $500+ for a new dryer.',
    parts: 'heating elements, thermal fuses, thermostats, drum belts, idler pulleys, drum bearings, igniters (gas), control boards',
  },
  oven: {
    cost: '$100–$350',
    time: '1–2 hours',
    problems: 'not heating, uneven baking, burner not working, door won\'t close properly, control board errors, self-clean issues, igniter problems',
    worth: 'Ovens are worth repairing in most cases. Igniter replacements ($100–$180), control board repairs ($150–$300), and element replacements are all cost-effective.',
    parts: 'bake elements, broil elements, igniters, control boards, door hinges, door gaskets, temperature sensors, surface burner switches',
  },
  stove: {
    cost: '$100–$320',
    time: '1–2 hours',
    problems: 'burner not lighting, burner not heating, uneven heat, control knob issues, igniter clicking constantly, element not working',
    worth: 'Stove repairs are almost always worth it. Surface burner repairs and igniter fixes cost $80–$200 vs $400–$800 for a new range.',
    parts: 'surface burners, igniters, spark modules, control boards, burner switches, oven elements, door hinges',
  },
  freezer: {
    cost: '$130–$380',
    time: '1–2 hours',
    problems: 'not freezing, frosting up, making noise, ice buildup, temperature fluctuations, compressor issues',
    worth: 'Freezers are worth repairing if under 10 years old. Defrost heater, thermostat, and evaporator fan replacements are very cost-effective.',
    parts: 'defrost heaters, evaporator fans, thermostats, compressors, door gaskets, temperature controls',
  },
  microwave: {
    cost: '$80–$250',
    time: '1 hour',
    problems: 'not heating, sparking, turntable not spinning, display not working, door not closing, fan not working',
    worth: 'Microwaves over $300 are worth repairing. Common issues like magnetrons or control boards can be fixed for $100–$200.',
    parts: 'magnetrons, diodes, capacitors, door switches, turntable motors, control boards, high-voltage transformers',
  },
};

const BRAND_DATA = {
  samsung: {
    known_for: 'smart home integration, French door fridges, front-load washers, and innovative dishwasher features',
    common_issues: 'Samsung appliances can experience ice maker problems (fridges), SE/5E error codes (dishwashers), UE spin errors (washers), and control board failures',
    reliability: 'Samsung is a premium brand with generally good reliability. Most issues appear after 5–8 years of use.',
    parts: 'genuine Samsung OEM parts',
    warranty_note: 'Samsung offers a 1-year manufacturer warranty. We provide an additional 90-day warranty on all repairs.',
  },
  lg: {
    known_for: 'inverter technology, front-load washers, French door fridges, and ThinQ smart connectivity',
    common_issues: 'LG appliances can experience LE motor errors (washers), OE drain errors (dishwashers), compressor failures (fridges), and linear compressor issues',
    reliability: 'LG is known for innovative technology. Linear compressor fridges may need compressor replacement after 5–7 years — covered under LG\'s extended warranty.',
    parts: 'genuine LG OEM parts',
    warranty_note: 'LG offers manufacturer warranty on parts. We provide 90-day warranty on all repairs.',
  },
  whirlpool: {
    known_for: 'reliability, top-load washers, built-in dishwashers, and American-style fridges',
    common_issues: 'Whirlpool appliances commonly have pump failures (washers), control board issues, heating element failures (dryers), and ice maker problems (fridges)',
    reliability: 'Whirlpool is one of the most reliable appliance brands. Most issues are straightforward repairs with widely available parts.',
    parts: 'genuine Whirlpool OEM parts',
    warranty_note: 'Whirlpool offers 1-year manufacturer warranty. We provide 90-day warranty on our repairs.',
  },
  bosch: {
    known_for: 'ultra-quiet dishwashers, European-style washers and dryers, and premium build quality',
    common_issues: 'Bosch appliances may experience drain pump failures, E15 error codes (dishwashers), bearing wear (washers/dryers), and control board issues',
    reliability: 'Bosch is a premium German brand known for durability. With proper maintenance, Bosch appliances last 15+ years.',
    parts: 'genuine Bosch OEM parts',
    warranty_note: 'Bosch offers a standard manufacturer warranty. We provide 90-day warranty on all our repairs.',
  },
  frigidaire: {
    known_for: 'affordable reliable refrigerators, built-in dishwashers, and classic American appliances',
    common_issues: 'Frigidaire appliances commonly experience ice maker failures, compressor issues in older fridges, control board errors, and door gasket wear',
    reliability: 'Frigidaire (owned by Electrolux) offers solid mid-range reliability. Parts are widely available and affordable.',
    parts: 'genuine Frigidaire/Electrolux OEM parts',
    warranty_note: 'Frigidaire offers 1-year manufacturer warranty. We add a 90-day warranty on all repairs.',
  },
  kenmore: {
    known_for: 'top-load washers, dryers, side-by-side fridges, and built through major manufacturers',
    common_issues: 'Kenmore appliances can experience control board failures, lid switch issues (washers), icemaker problems, and heating element failures (dryers)',
    reliability: 'Kenmore appliances are manufactured by Whirlpool, LG, or Electrolux. Reliability and parts depend on the manufacturer.',
    parts: 'OEM parts specific to the Kenmore manufacturer (Whirlpool or LG)',
    warranty_note: 'Kenmore has brand warranty support. We provide a 90-day repair warranty.',
  },
  ge: {
    known_for: 'built-in refrigerators, Profile and Café series, dishwashers, and cooking appliances',
    common_issues: 'GE appliances commonly experience ice maker failures, control board issues, igniter problems (ovens/stoves), and door seal wear',
    reliability: 'GE (now owned by Haier) has strong reliability, especially in refrigerators and ovens. Parts are widely available.',
    parts: 'genuine GE OEM parts',
    warranty_note: 'GE offers 1-year manufacturer warranty. We provide 90-day warranty on all our repairs.',
  },
  maytag: {
    known_for: 'heavy-duty washers and dryers, commercial-grade durability, and long-lasting appliances',
    common_issues: 'Maytag appliances may experience agitator issues (top-load washers), control board failures, bearing wear (dryers), and heating element problems',
    reliability: 'Maytag is known for rugged reliability. Many Maytag appliances last 15–20 years with proper maintenance.',
    parts: 'genuine Maytag/Whirlpool OEM parts',
    warranty_note: 'Maytag offers extended manufacturer warranty on some models. We add 90-day warranty on repairs.',
  },
  kitchenaid: {
    known_for: 'premium dishwashers, stand mixers, refrigerators, and professional-grade cooking appliances',
    common_issues: 'KitchenAid dishwashers may experience control board errors, pump failures, and spray arm clogs. Fridges can have ice maker and compressor issues.',
    reliability: 'KitchenAid is a premium brand (owned by Whirlpool) built for heavy use. Parts availability is excellent.',
    parts: 'genuine KitchenAid/Whirlpool OEM parts',
    warranty_note: 'KitchenAid offers manufacturer warranty. We provide 90-day warranty on all repairs.',
  },
  electrolux: {
    known_for: 'front-load washers, built-in dishwashers, and premium European-style appliances',
    common_issues: 'Electrolux appliances may have control board failures, door seal issues, pump problems (washers), and drainage errors (dishwashers)',
    reliability: 'Electrolux is a premium brand with generally good reliability. European-designed components can be specific to source.',
    parts: 'genuine Electrolux OEM parts',
    warranty_note: 'Electrolux offers manufacturer warranty. We add 90-day warranty on all our repairs.',
  },
  miele: {
    known_for: 'ultra-premium dishwashers, front-load washers, and exceptional build quality and longevity',
    common_issues: 'Miele appliances are highly reliable but can experience control board issues, pump failures after heavy use, and door seal wear over time',
    reliability: 'Miele is the most reliable appliance brand — tested to last 20+ years. Repairs are always worth it given the appliance value.',
    parts: 'genuine Miele OEM parts — sourced directly from Miele Canada',
    warranty_note: 'Miele offers extended manufacturer warranty on most models. We provide 90-day warranty on all repairs.',
  },
};

// ── FAQ GENERATORS ─────────────────────────────────────────────────────────────

function toTitleCase(s) {
  return s.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function getBrandLabel(brand) {
  const labels = { ge: 'GE', lg: 'LG', kitchenaid: 'KitchenAid' };
  return labels[brand] || toTitleCase(brand);
}

function getServiceLabel(svc) {
  const labels = { dishwasher: 'Dishwasher', fridge: 'Fridge', washer: 'Washer', dryer: 'Dryer', oven: 'Oven', stove: 'Stove' };
  return labels[svc] || toTitleCase(svc);
}

function faqBrandService(brand, service, phone, name) {
  const B = getBrandLabel(brand);
  const S = getServiceLabel(service);
  const bd = BRAND_DATA[brand] || BRAND_DATA.whirlpool;
  const sd = SERVICE_DATA[service] || SERVICE_DATA.dishwasher;
  return [
    {
      q: `What are common ${B} ${S.toLowerCase()} problems you repair?`,
      a: `${bd.common_issues}. Our technicians are trained specifically on ${B} appliances and carry ${bd.parts} for faster same-day repairs. Call ${phone} to describe the issue and we\'ll confirm availability.`,
    },
    {
      q: `How much does ${B} ${S.toLowerCase()} repair cost in Toronto?`,
      a: `${B} ${S.toLowerCase()} repair in Toronto typically costs ${sd.cost} depending on the fault and parts required. We charge a $65 diagnostic fee (waived when you proceed with repair). All ${B} repairs include a 90-day parts and labour warranty.`,
    },
    {
      q: `Is my ${B} ${S.toLowerCase()} worth repairing?`,
      a: `${sd.worth} For ${B} specifically: ${bd.reliability} ${name} will give you an honest assessment — if repair isn\'t cost-effective, we\'ll tell you.`,
    },
    {
      q: `Do you use genuine ${B} parts?`,
      a: `Yes — we use ${bd.parts} to ensure the repair lasts. Aftermarket parts can void remaining manufacturer warranty and cause premature failure. ${bd.warranty_note}`,
    },
    {
      q: `How quickly can you repair my ${B} ${S.toLowerCase()}?`,
      a: `Most ${B} ${S.toLowerCase()} repairs are completed same-day when you call before 2 PM. We stock the most common ${B} ${S.toLowerCase()} parts — ${sd.parts}. Call ${phone} to check availability in your area.`,
    },
  ];
}

function faqBrandOnly(brand, phone, name, area) {
  const B = getBrandLabel(brand);
  const bd = BRAND_DATA[brand] || BRAND_DATA.whirlpool;
  const svcs = ['refrigerators', 'washers', 'dryers', 'dishwashers', 'ovens', 'stoves'];
  return [
    {
      q: `What ${B} appliances do you repair in ${area}?`,
      a: `${name} repairs all ${B} appliances including ${svcs.slice(0,5).join(', ')}, and more. ${B} is ${bd.known_for}. We are familiar with the full ${B} lineup and carry ${bd.parts}.`,
    },
    {
      q: `What are the most common ${B} appliance problems?`,
      a: `${bd.common_issues}. Our technicians are ${B}-trained and carry common ${B} parts on every service call for faster first-visit repairs.`,
    },
    {
      q: `How much does ${B} appliance repair cost in ${area}?`,
      a: `${B} appliance repair in ${area} typically costs $100–$450 depending on the appliance and issue. We charge a $65 flat diagnostic fee, waived when you proceed with the repair. All repairs include a 90-day parts and labour warranty.`,
    },
    {
      q: `Is my ${B} appliance worth repairing?`,
      a: `${bd.reliability} As a general rule, if the repair cost is under 50% of a replacement, repair is the better choice — especially for premium brands like ${B}. ${name} gives honest repair-vs-replace advice at no charge.`,
    },
    {
      q: `Do you offer same-day ${B} repair in ${area}?`,
      a: `Yes — same-day ${B} appliance repair is available across ${area} when you call before 2 PM. Call ${phone} to schedule. ${bd.warranty_note}`,
    },
  ];
}

function faqService(service, phone, name, area) {
  const S = getServiceLabel(service);
  const sd = SERVICE_DATA[service] || SERVICE_DATA.dishwasher;
  return [
    {
      q: `What ${S.toLowerCase()} problems do you fix in ${area}?`,
      a: `${name} repairs all common ${S.toLowerCase()} issues: ${sd.problems}. We service all major brands — Samsung, LG, Whirlpool, Bosch, GE, Frigidaire, Maytag, KitchenAid and more. Call ${phone} to describe the problem.`,
    },
    {
      q: `How much does ${S.toLowerCase()} repair cost in ${area}?`,
      a: `${S} repair in ${area} typically costs ${sd.cost} depending on the fault, brand, and parts. We charge a $65 flat diagnostic fee, waived when you proceed with the repair. You receive an exact quote before we start any work.`,
    },
    {
      q: `Is my ${S.toLowerCase()} worth repairing?`,
      a: `${sd.worth} ${name} provides an honest repair-vs-replace assessment at no charge. If repair is not cost-effective, we\'ll tell you before doing any work.`,
    },
    {
      q: `How long does ${S.toLowerCase()} repair take in ${area}?`,
      a: `Most ${S.toLowerCase()} repairs are completed in ${sd.time} on the first visit. We stock the most commonly needed parts — ${sd.parts}. Same-day service is available across ${area} when you book before 2 PM.`,
    },
    {
      q: `Do you offer a warranty on ${S.toLowerCase()} repairs?`,
      a: `Yes — all ${S.toLowerCase()} repairs include a 90-day parts and labour warranty. If the same issue recurs within 90 days, we return and fix it at no charge. Call ${phone} to book.`,
    },
  ];
}

function faqToSchema(faqs) {
  return faqs.map(f => ({
    '@type': 'Question',
    name: f.q,
    acceptedAnswer: { '@type': 'Answer', text: f.a },
  }));
}

// ── PAGE CLASSIFIER ────────────────────────────────────────────────────────────

const SERVICES = ['dishwasher','fridge','washer','dryer','oven','stove','freezer','microwave'];
const BRANDS   = ['samsung','lg','whirlpool','bosch','frigidaire','kenmore','ge','maytag','kitchenaid','electrolux','miele','aeg','danby','amana','hotpoint','speed-queen','blomberg'];
const SKIP_FILES = ['404','index','sitemap','robots','privacy','terms','thank-you','service-template','landing','compare','preview','services','locations','brands','about','for-businesses'];

function classifyPage(slug) {
  const s = slug.toLowerCase();
  if (SKIP_FILES.some(x => s === x || s.startsWith(x+'-') || s.endsWith('-'+x))) return null;

  // Pure service page only: exactly "[service]-repair"
  const svcExact = SERVICES.find(svc => s === svc + '-repair');
  if (svcExact) return { type: 'service', service: svcExact };

  // Brand+service page: exactly "[brand]-[service]-repair"
  for (const b of BRANDS) {
    for (const svc of SERVICES) {
      if (s === b + '-' + svc + '-repair') return { type: 'brand-service', brand: b, service: svc };
    }
  }

  // Pure brand page: "[brand]-repair" or "[brand]-repair-[city]" or "[brand]"
  const brandOnly = BRANDS.find(b => s === b + '-repair' || s.startsWith(b + '-repair-') || s === b);
  if (brandOnly) return { type: 'brand', brand: brandOnly };

  return null;
}

// ── SCHEMA REPLACER ────────────────────────────────────────────────────────────

function replaceFAQInScript(scriptContent, newMainEntity) {
  try {
    const data = JSON.parse(scriptContent);
    const graph = data['@graph'];
    if (!graph) return null;
    const faqIdx = graph.findIndex(n => n['@type'] === 'FAQPage');
    if (faqIdx === -1) return null;
    graph[faqIdx].mainEntity = newMainEntity;
    return JSON.stringify(data, null, 6);
  } catch (e) {
    return null;
  }
}

function updateFAQ(html, newMainEntity) {
  // Match the JSON-LD script that contains FAQPage
  const re = /(<script type="application\/ld\+json">\s*)([\s\S]*?FAQPage[\s\S]*?)(<\/script>)/;
  const m = html.match(re);
  if (!m) return null;

  const updated = replaceFAQInScript(m[2], newMainEntity);
  if (!updated) return null;

  return html.replace(re, m[1] + updated + m[3]);
}

// ── MAIN ──────────────────────────────────────────────────────────────────────

const sitesToProcess = siteArg ? [[siteArg, SITES[siteArg]]] : Object.entries(SITES);

let totalUpdated = 0;

for (const [key, site] of sitesToProcess) {
  if (!site) { console.log('Unknown site: ' + key); continue; }

  const files = fs.readdirSync(site.dir).filter(f => f.endsWith('.html'));
  let updated = 0, skipped = 0;

  for (const f of files) {
    const slug = path.basename(f, '.html');
    const info = classifyPage(slug);
    if (!info) { skipped++; continue; }

    let faqs;
    if (info.type === 'brand-service') {
      faqs = faqBrandService(info.brand, info.service, site.phone, site.name);
    } else if (info.type === 'brand') {
      faqs = faqBrandOnly(info.brand, site.phone, site.name, site.area);
    } else if (info.type === 'service') {
      faqs = faqService(info.service, site.phone, site.name, site.area);
    } else {
      skipped++;
      continue;
    }

    const fpath = path.join(site.dir, f);
    const html = fs.readFileSync(fpath, 'utf8');
    const newMainEntity = faqToSchema(faqs);
    const newHtml = updateFAQ(html, newMainEntity);

    if (!newHtml) { skipped++; continue; }

    if (DRY) {
      console.log('[' + key.toUpperCase() + '] ' + slug + ' (' + info.type + ')');
      console.log('  Q1: ' + faqs[0].q);
    } else {
      fs.writeFileSync(fpath, newHtml, 'utf8');
    }
    updated++;
  }

  console.log(key.toUpperCase() + ': updated=' + updated + ' skipped=' + skipped + (DRY ? ' (DRY)' : ''));
  totalUpdated += updated;
}

console.log('\nTotal pages updated: ' + totalUpdated + (DRY ? ' (dry run)' : ''));
