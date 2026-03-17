/**
 * expand-blog-posts.js
 *
 * 1. Fixes malformed HTML bug: <section <div class="related-blog-posts"...
 * 2. Expands short blog posts (< 1400 words) with appliance-specific content
 *
 * Usage:
 *   node expand-blog-posts.js            -- fix + expand all 3 sites
 *   node expand-blog-posts.js --fix-only -- just fix HTML bug, no expansion
 *   node expand-blog-posts.js --dry-run  -- preview only
 */

const fs   = require('fs');
const path = require('path');

const DRY_RUN   = process.argv.includes('--dry-run');
const FIX_ONLY  = process.argv.includes('--fix-only');

const SITES = [
  { name: 'NAR',     dir: 'C:/nappliancerepair/blog',     author: 'Nick Petrenko' },
  { name: 'NEARY',   dir: 'C:/appliancerepairneary/blog', author: 'Mike Petrov' },
  { name: 'FIXLIFY', dir: 'C:/fixlifyservices/blog',      author: 'Alex Semenov' },
];

const TODAY = '2026-03-07';
const WORD_THRESHOLD = 1600;

// ── Appliance content templates ────────────────────────────────────────────

function getApplianceType(slug) {
  if (slug.includes('dishwasher'))                                          return 'dishwasher';
  if (slug.includes('dryer'))                                               return 'dryer';
  if (slug.includes('fridge') || slug.includes('freezer') || slug.includes('refrigerator')) return 'fridge';
  if (slug.includes('washer') || slug.includes('washing'))                  return 'washer';
  if (slug.includes('oven') || slug.includes('stove') || slug.includes('range') || slug.includes('burner')) return 'oven';
  if (slug.includes('microwave'))                                           return 'microwave';
  return 'general';
}

function getBrand(slug) {
  const brands = ['lg', 'samsung', 'whirlpool', 'bosch', 'miele', 'ge', 'frigidaire', 'kenmore', 'maytag', 'speed-queen'];
  for (const b of brands) {
    if (slug.includes(b)) return b.replace('-', ' ');
  }
  return null;
}

function getCity(slug) {
  const cities = ['toronto', 'brampton', 'mississauga', 'etobicoke', 'markham', 'scarborough', 'north-york', 'oakville', 'richmond-hill', 'vaughan'];
  for (const c of cities) {
    if (slug.includes(c)) return c.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ');
  }
  return 'Toronto';
}

const CONTENT_TEMPLATES = {
  washer: (brand, city) => `
<h2>What to Expect During a${brand ? ' ' + capitalize(brand) : ''} Washer Repair Visit in ${city}</h2>
<p>When our technician arrives for a${brand ? ' ' + capitalize(brand) : ''} washer repair, the process begins with a full diagnostic &mdash; not a guess. We run the machine through a test cycle while monitoring water intake, drum rotation, drainage timing and spin speed. For front-load models, we also check the door latch switch, boot seal condition and control board error logs.</p>
<p>The diagnostic phase takes 15&ndash;20 minutes and tells us exactly what failed. We'll show you the fault and quote the repair before touching anything. Most common washer repairs &mdash; pump replacements, lid switches, control board modules, belt and motor couplers &mdash; are stocked on our vans, so completion happens in the same visit. After the repair, we run a full wash-and-spin cycle before leaving to confirm the fix held.</p>
<p>All${brand ? ' ' + capitalize(brand) : ''} washer repairs include a 90-day parts and labour warranty. If the same fault returns within 90 days, we come back at no charge.</p>

<h2>Washer Maintenance Tips That Prevent Costly Repairs</h2>
<p>After years of servicing washers in ${city} and surrounding areas, our technicians see the same preventable failures time after time. Here are the habits that keep repair bills away.</p>
<h3>Clean the Drain Filter Monthly</h3>
<p>Front-load washers have a drain filter behind the small access panel at the bottom front. This filter catches lint, coins, buttons and small debris before they reach the pump. A clogged filter is the leading cause of drain errors and pump failures. Cleaning it takes three minutes and costs nothing &mdash; ignoring it can lead to a $150&ndash;$220 pump replacement. On top-load models, run a cleaning cycle with a washing machine tablet monthly.</p>
<h3>Always Use HE Detergent</h3>
<p>High-efficiency washers require HE-labelled, low-sudsing detergent. Regular detergent creates excessive suds that the machine cannot rinse away properly, leading to residue buildup on the drum, hoses and door gasket. Over time this residue harbours bacteria, causes musty odours and accelerates gasket deterioration. Use liquid HE detergent in the amount printed on the cap &mdash; typically far less than you'd expect.</p>
<h3>Check the Hoses Annually</h3>
<p>Washer inlet hoses (hot and cold water supply) are the leading cause of household flooding. Rubber hoses develop micro-cracks over time and can fail catastrophically. Inspect both hoses annually for bulging, cracking or corrosion at the fittings. Braided stainless steel hoses are a worthwhile upgrade &mdash; they rarely fail and cost about $25 at any hardware store. Replace rubber hoses every 5 years regardless of appearance.</p>
<p>Following these three steps can easily extend your washer's service life by several years. When problems do arise, call us for same-day diagnosis in ${city}.</p>`,

  dishwasher: (brand, city) => `
<h2>What Happens During a${brand ? ' ' + capitalize(brand) : ''} Dishwasher Repair in ${city}</h2>
<p>A professional dishwasher repair visit starts with the door &mdash; we check the latch, gasket seal, and door switches before the diagnostic cycle begins. Dishwasher problems are often mechanical (spray arm blockage, float switch, wash pump) rather than electronic, so hands-on inspection yields faster diagnoses than error code reading alone.</p>
<p>We run the machine through a full cycle while checking water temperature (should reach 60&deg;C for effective cleaning), spray arm pressure, water intake volume and drainage. If the unit throws a fault code, we pull the full error log from the control board. Most${brand ? ' ' + capitalize(brand) : ''} dishwasher repairs &mdash; drain pumps, wash motor assemblies, door latches, water inlet valves and spray arms &mdash; are carried on our vans and repaired same-day.</p>
<p>All repairs come with a 90-day warranty. We serve ${city} and surrounding areas Monday to Saturday, 8 am&ndash;8 pm.</p>

<h2>Dishwasher Maintenance Tips to Prevent Breakdowns</h2>
<p>Dishwashers are the most-used appliance in most kitchens, running daily or near-daily. Proper maintenance dramatically extends service life and preserves cleaning performance.</p>
<h3>Clean the Filter Weekly</h3>
<p>Most modern dishwashers (especially${brand ? ' ' + capitalize(brand) : ''} models) have a removable filter at the base of the tub. Unlike older models with self-cleaning grinders, these manual filters trap food debris that must be rinsed out. A clogged filter reduces spray pressure, leaves dishes dirty and forces the pump to work harder, shortening its life. Twist the filter counterclockwise, rinse under warm water with a soft brush, and replace &mdash; takes 60 seconds.</p>
<h3>Check and Clean Spray Arms</h3>
<p>Spray arm holes clog with mineral deposits and food particles, reducing wash pressure and leaving dishes spotty. Remove the spray arms every two months and use a toothpick or skewer to clear each hole. Soak the arms in white vinegar for 20 minutes to dissolve mineral buildup. In ${city}'s moderately hard water, this prevents uneven cleaning patterns and extends the life of the wash pump.</p>
<h3>Run a Cleaning Cycle Monthly</h3>
<p>Place a dishwasher cleaning tablet or a cup of white vinegar in the bottom rack and run an empty hot cycle. This removes grease, limescale and detergent residue from the spray system and interior. Follow with a short empty cycle using baking soda to neutralise odours. Monthly cleaning cycles visibly improve wash results and prevent the internal buildup that triggers pump and valve failures.</p>
<p>When your dishwasher isn't cleaning properly, draining slowly or leaking, call our ${city} team for same-day diagnosis.</p>`,

  dryer: (brand, city) => `
<h2>What to Expect During a${brand ? ' ' + capitalize(brand) : ''} Dryer Repair in ${city}</h2>
<p>Dryer repairs begin with a safety check &mdash; we test the thermal fuse (the most commonly replaced dryer component) and check that the exhaust temperature is within safe range. An overheating dryer is a fire risk, so our technicians always measure exhaust heat before running a full diagnostic cycle.</p>
<p>After the safety check, we inspect the heating element (electric) or burner assembly and igniter (gas), the drum seals, drive belt, idler pulley and drum bearings. We listen for the noise that prompted the call &mdash; squealing (worn drum seals or rear bearing), thumping (worn drum support rollers), or grinding (idler pulley failure) each points to a specific component. Most${brand ? ' ' + capitalize(brand) : ''} dryer repairs complete in a single visit using OEM parts from our van stock.</p>
<p>All dryer repairs include a 90-day parts and labour warranty. Same-day service is available in ${city} Mon&ndash;Sat.</p>

<h2>Dryer Maintenance Tips: Reduce Fire Risk and Extend Appliance Life</h2>
<p>Dryers cause approximately 15,000 house fires per year in North America, nearly all from lint buildup. These tips protect your home and extend your dryer's service life significantly.</p>
<h3>Clean the Lint Trap After Every Load</h3>
<p>This is the most important habit. A clogged lint trap reduces airflow, forces the heating element to work harder, extends drying times and creates a fire hazard. Beyond the trap itself, lint accumulates in the duct system over time. Wash the lint screen with soap and water monthly to remove the invisible film left by dryer sheets, which restricts airflow even when the trap looks clean.</p>
<h3>Vent Cleaning Annually (or Every Six Months for Heavy Use)</h3>
<p>The dryer exhaust duct collects lint that bypasses the trap. A blocked duct is the primary cause of dryer fires and dramatically reduces efficiency. Signs of a blocked duct: clothes take two cycles to dry, the dryer exterior is unusually hot, or you smell burning during operation. Professional vent cleaning costs $80&ndash;$120 in ${city} and should be done annually. Use only rigid or semi-rigid metal duct &mdash; flexible plastic duct crushes easily and collects lint at every bend.</p>
<h3>Keep the Area Around the Dryer Clear</h3>
<p>Combustible materials (clothing, lint-covered surfaces, cleaning supplies) should not be stored near dryers. Ensure at least 30&nbsp;cm of clearance on all sides for proper ventilation. Gas dryers require an approved gas line installation &mdash; never use flexible connectors longer than 1.8 metres or run them through walls. If you smell gas at any point, leave the home and call your gas utility immediately.</p>
<p>When your${brand ? ' ' + capitalize(brand) : ''} dryer is taking too long, making noise or not heating at all, call our ${city} team for same-day diagnosis and repair.</p>`,

  fridge: (brand, city) => `
<h2>What Happens During a${brand ? ' ' + capitalize(brand) : ''} Fridge Repair in ${city}</h2>
<p>A refrigerator service call begins with temperature verification. We bring a calibrated thermometer to confirm actual fridge and freezer temperatures before opening the unit &mdash; this tells us whether we're dealing with a sealed system problem (compressor, refrigerant, condenser) or an airflow problem (evaporator fan, defrost heater, damper).</p>
<p>We then check the compressor start relay, evaporator coil for ice buildup, condenser coils for dust accumulation, and door seal integrity. Modern${brand ? ' ' + capitalize(brand) : ''} refrigerators have diagnostic modes accessible via button combinations on the control panel &mdash; we pull the full error log before disassembling anything. Most airflow and defrost failures are repaired same-day. Sealed system repairs (compressor, refrigerant recharge) take longer and are assessed for cost-effectiveness relative to the unit's age.</p>
<p>We serve ${city} and the GTA, Monday to Saturday, 8 am&ndash;8 pm. All repairs carry a 90-day warranty.</p>

<h2>Refrigerator Maintenance Tips to Keep Food Safe and Reduce Repairs</h2>
<p>Refrigerators run 24 hours a day, 365 days a year. Simple maintenance habits reduce power consumption, prevent breakdowns and extend the unit's life by years.</p>
<h3>Clean Condenser Coils Twice a Year</h3>
<p>Condenser coils release the heat extracted from your fridge. When coated with dust and pet hair, they can't dissipate heat efficiently &mdash; the compressor runs longer and hotter, wearing out sooner. Unplug the fridge, pull it away from the wall (or remove the front grille for bottom-mount coils), and vacuum the coils with a brush attachment. This 10-minute task twice a year is one of the highest-impact maintenance steps you can do.</p>
<h3>Check the Door Seals Annually</h3>
<p>A worn door gasket lets cold air escape continuously, forcing the compressor to compensate. Test the seal by closing the door on a piece of paper &mdash; you should feel resistance pulling it out. If the paper slides freely, the gasket is failing. Replacement gaskets cost $40&ndash;$80 and are straightforward to install, or our technicians can handle it during any service call. Damaged seals also cause frost buildup and moisture inside the cabinet.</p>
<h3>Set Temperatures Correctly</h3>
<p>The refrigerator section should run at 3&deg;C&ndash;4&deg;C; the freezer at -18&deg;C. Higher temperatures allow bacterial growth in food; lower temperatures waste energy and can partially freeze fresh produce. Keep the fridge at 75&ndash;80% capacity &mdash; a full fridge maintains temperature better than an empty one, but overpacking blocks airflow from the evaporator fan. Leave at least 2.5&nbsp;cm between items and the rear wall.</p>
<p>When your${brand ? ' ' + capitalize(brand) : ''} fridge is running warm, making unusual noise or forming excessive frost, call our ${city} team for same-day diagnosis.</p>`,

  oven: (brand, city) => `
<h2>What Happens During a${brand ? ' ' + capitalize(brand) : ''} Oven or Range Repair in ${city}</h2>
<p>Range and oven repairs begin with a safety inspection &mdash; particularly important for gas models. We test for gas leaks at the supply line and burner valves, check igniter spark strength, and verify the oven igniter resistance (a failing oven igniter is the most common cause of "oven not heating" on gas ranges). For electric models, we test element continuity, bake and broil element resistance, and the electronic control board.</p>
<p>Surface burner problems (gas: no ignition, weak flame, continuous clicking; electric: element not glowing) are usually diagnosed and repaired in under an hour. Oven temperature calibration issues &mdash; where the oven runs hot or cold relative to its setting &mdash; are addressed by testing the temperature sensor and recalibrating the control board. Most common${brand ? ' ' + capitalize(brand) : ''} range repairs complete same-day with OEM parts from our van.</p>
<p>We serve ${city} Mon&ndash;Sat, 8 am&ndash;8 pm, with a 90-day warranty on all repairs.</p>

<h2>Oven and Range Maintenance Tips From Our Technicians</h2>
<p>Ranges are built to last, but neglected maintenance shortens their life and creates safety hazards. Here's what our technicians recommend after years of service calls in ${city}.</p>
<h3>Clean the Burner Grates and Caps Regularly (Gas Ranges)</h3>
<p>Food spills clog gas burner ports, causing uneven flames, weak heat output and constant re-ignition problems. Remove the burner caps and grates after each cooking session (once cooled) and wipe them down. Monthly, soak the caps in warm soapy water and use a toothpick to clear any clogged burner ports. Never put gas burner components in the dishwasher &mdash; the harsh detergent and high heat degrade the finish and can warp lighter components.</p>
<h3>Use Self-Clean Carefully</h3>
<p>Self-cleaning cycles run at 480&deg;C&ndash;540&deg;C, burning off food residue. This intense heat is hard on door gaskets, oven igniter contacts and control electronics. Use self-clean cycles no more than two or three times per year, and never immediately after heavy cooking when the oven is already hot. Remove oven racks before running self-clean &mdash; the extreme heat discolours and warps standard chrome racks. After the cycle, wipe out ash with a damp cloth once the oven cools completely.</p>
<h3>Test the Oven Temperature Annually</h3>
<p>Oven thermostats drift over time. Purchase an oven thermometer ($10&ndash;$15) and set it at 175&deg;C &mdash; if the reading differs by more than 15&deg;, the temperature sensor or control board calibration needs adjustment. Consistently miscalibrated temperatures ruin baked goods and can char food at higher settings. Our technicians can test and recalibrate oven temperature during any service call.</p>
<p>When your${brand ? ' ' + capitalize(brand) : ''} oven isn't heating evenly, a burner won't light, or the oven won't reach temperature, call our ${city} team for same-day service.</p>`,

  microwave: (brand, city) => `
<h2>What Happens During a Microwave Repair in ${city}</h2>
<p>Microwave repairs require specific safety protocols &mdash; the high-voltage capacitor can store a lethal charge even after the unit is unplugged. Our technicians always discharge the capacitor before working inside any microwave, using a safety discharge tool. If you're experiencing a microwave that stopped heating, sparking, or making unusual noises, do not attempt to open the cabinet yourself.</p>
<p>The most common microwave failure is a blown high-voltage diode ($30&ndash;$50 part) or a failed magnetron ($100&ndash;$180 part), which is the component that actually generates microwaves. Door switch failures (preventing the unit from starting when the door is closed) are also very common and inexpensive to fix. We diagnose and repair all OTR (over-the-range) and countertop models in ${city}.</p>
<p>If repair cost exceeds 50% of replacement cost for a countertop model, we'll let you know &mdash; it's often better value to replace a low-cost countertop unit. OTR models almost always warrant repair given their higher replacement cost and installation complexity.</p>

<h2>Microwave Safety and Maintenance Tips</h2>
<p>Microwaves are the most frequently used kitchen appliance in most homes, yet they receive almost no maintenance attention. These simple habits keep them running safely.</p>
<h3>Clean the Interior After Every Use</h3>
<p>Food splatters inside the microwave absorb microwave energy during subsequent uses, causing hot spots and premature magnetron wear. Wipe the interior after each use with a damp cloth. For stubborn buildup, microwave a cup of water for three minutes to create steam, then wipe down &mdash; the steam loosens debris without harsh chemicals. Never use abrasive pads on the interior walls, which can damage the interior coating.</p>
<h3>Inspect the Door Seal Regularly</h3>
<p>The door seal prevents microwave radiation from escaping during operation. Inspect the rubber gasket around the door for cracks, tears or compression. The choke seal &mdash; the metal channel around the door cavity &mdash; should fit flush with no warping. If you notice the door doesn't close smoothly, latches inconsistently, or the unit runs but door switches arc, have it inspected immediately. A damaged door seal is a safety issue, not just a maintenance concern.</p>
<h3>Never Run the Microwave Empty</h3>
<p>Running a microwave with nothing inside causes the magnetron to absorb its own microwave energy, leading to overheating and potentially permanent damage. Always place a microwave-safe container with at least 100&nbsp;mL of water inside before running a test cycle. This applies to self-cleaning cycles if your microwave has a steam clean feature.</p>
<p>For microwave repairs in ${city}, call our team for a same-day appointment. We carry common door switch sets, diodes and fuses on every van.</p>`,

  general: (brand, city) => `
<h2>What Our Appliance Repair Process Looks Like in ${city}</h2>
<p>When our technician arrives, the diagnostic process takes priority before any repair work begins. We use a structured approach: visual inspection, fault code retrieval from the appliance's control board, and a functional test cycle to observe the failure directly. This gives us certainty about the cause before we quote the repair &mdash; no guessing, no replacing parts that don't need replacing.</p>
<p>Our vans are stocked with the most common OEM parts for all major brands &mdash; motors, control boards, pumps, valves, heating elements, belts, sensors and seals. The majority of repairs complete in a single two-hour visit. When a specialized part isn't on the van, we provide a firm timeline and schedule a return visit, typically within 24&ndash;48 hours. All repairs carry a 90-day parts and labour warranty.</p>
<p>We serve ${city} and the surrounding GTA Monday through Saturday, 8 am to 8 pm, with same-day availability for calls before 2 pm.</p>

<h2>Appliance Maintenance Tips From Our ${city} Technicians</h2>
<p>The most expensive appliance repair is always the one that was preventable. After years of service calls across ${city}, our technicians see the same neglected maintenance items causing premature failures. Here's a simple checklist that applies across all major home appliances.</p>
<h3>Keep Air Circulation Clear</h3>
<p>Every major appliance &mdash; fridge, washer, dryer, dishwasher &mdash; needs adequate clearance on all sides for heat dissipation and ventilation. Blocked airflow makes compressors, motors and heating elements work harder and run hotter, significantly shortening their service life. Ensure at least 2.5&nbsp;cm on sides and 5&nbsp;cm at the back for built-in clearance. Never stack items on top of washers, dryers or dishwashers &mdash; this restricts ventilation and can damage the top panel.</p>
<h3>Inspect Hoses, Seals and Gaskets Annually</h3>
<p>Water-connected appliances (washers, dishwashers) rely on rubber hoses and door gaskets. These components harden and crack over time, especially in Toronto's temperature-variable climate. Inspect supply hoses for bulging or cracking at the fittings; inspect door gaskets for tears or compression failure. Replacing a $15 hose or $40 gasket prevents the flood damage and mould remediation costs that follow a hose burst or persistent leak.</p>
<h3>Don't Ignore Error Codes and Warning Signs</h3>
<p>Modern appliances display error codes, flash indicator lights or make specific noises when something is wrong. Ignoring these early warning signs consistently leads to more expensive failures &mdash; a motor that starts making noise runs hot and eventually seizes; a clogged filter that causes drain errors eventually burns out the pump. When an appliance shows an error or behaves unusually, book a diagnostic visit. Early intervention is almost always less expensive than emergency repair after a complete failure.</p>
<p>For appliance repair in ${city}, call our team for same-day diagnosis. We fix all major brands and most models in a single visit.</p>`,
};

function capitalize(s) {
  return s.replace(/\b\w/g, c => c.toUpperCase());
}

// ── Word count (rough) ─────────────────────────────────────────────────────
function wordCount(html) {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().split(' ').length;
}

// ── Fix malformed HTML bug ─────────────────────────────────────────────────
function fixMalformedHtml(html) {
  // Fix: <section <div class="related-blog-posts"  →  <div class="related-blog-posts"
  html = html.replace(/<section\s+<div(\s+class="related-blog-posts")/g, '<div$1');
  // Fix orphan class="faq-section"> (after </div> with optional spaces + CRLF or LF)
  html = html.replace(/(<\/div>)[ \t]*\r?\nclass="faq-section">/g, '$1\n<section class="faq-section">');
  // Handle inline variant (no newline between </div> and class=)
  html = html.replace(/(<\/div>)class="faq-section">/g, '$1\n<section class="faq-section">');
  return html;
}

// ── Update dateModified ────────────────────────────────────────────────────
function updateDateModified(html) {
  return html.replace(/"dateModified"\s*:\s*"[^"]+"/g, `"dateModified": "${TODAY}"`);
}

// ── Build the new content block ─────────────────────────────────────────────
function buildExpandContent(slug, brand, city) {
  const type = getApplianceType(slug);
  const templateFn = CONTENT_TEMPLATES[type] || CONTENT_TEMPLATES.general;
  const content = templateFn(brand, city);
  return content.trim();
}

// ── Inject content before the CTA block ───────────────────────────────────
function injectContentBeforeCta(html, newContent) {
  // Try to find CTA block
  const ctaIdx = html.indexOf('<div class="cta-block">');
  if (ctaIdx === -1) {
    // Fallback: insert before the related-blog-posts or faq-section
    const fallbackIdx = html.indexOf('<div class="related-blog-posts"');
    if (fallbackIdx !== -1) {
      return html.slice(0, fallbackIdx) + '\n' + newContent + '\n' + html.slice(fallbackIdx);
    }
    const faqIdx = html.indexOf('class="faq-section"');
    if (faqIdx !== -1) {
      return html.slice(0, faqIdx - 9) + '\n' + newContent + '\n' + html.slice(faqIdx - 9);
    }
    return html; // can't inject
  }
  return html.slice(0, ctaIdx) + '\n' + newContent + '\n' + html.slice(ctaIdx);
}

// ── Main ───────────────────────────────────────────────────────────────────
let totalFixed = 0;
let totalExpanded = 0;
let totalSkipped = 0;

for (const site of SITES) {
  if (!fs.existsSync(site.dir)) {
    console.log(`SKIP ${site.name}: ${site.dir} not found`);
    continue;
  }

  const files = fs.readdirSync(site.dir)
    .filter(f => f.endsWith('.html'))
    .map(f => path.join(site.dir, f));

  let siteFixed = 0;
  let siteExpanded = 0;

  for (const fpath of files) {
    let html = fs.readFileSync(fpath, 'utf8');
    const slug = path.basename(fpath, '.html');
    let changed = false;

    // 1. Fix malformed HTML
    const fixedHtml = fixMalformedHtml(html);
    if (fixedHtml !== html) {
      html = fixedHtml;
      changed = true;
      siteFixed++;
    }

    // 2. Update dateModified
    const datedHtml = updateDateModified(html);
    if (datedHtml !== html) {
      html = datedHtml;
      changed = true;
    }

    // 3. Expand short posts (skip if FIX_ONLY)
    if (!FIX_ONLY) {
      const wc = wordCount(html);
      if (wc < WORD_THRESHOLD) {
        const brand = getBrand(slug);
        const city  = getCity(slug);
        const newContent = buildExpandContent(slug, brand, city);
        const expandedHtml = injectContentBeforeCta(html, newContent);
        if (expandedHtml !== html) {
          const newWc = wordCount(expandedHtml);
          if (DRY_RUN) {
            console.log(`  [EXPAND] [${site.name}] ${slug}: ${wc} → ~${newWc} words`);
          }
          html = expandedHtml;
          changed = true;
          siteExpanded++;
        } else {
          console.log(`  [WARN] could not inject content into ${slug} (no CTA/FAQ anchor found)`);
        }
      }
    }

    if (changed) {
      if (!DRY_RUN) {
        fs.writeFileSync(fpath, html, 'utf8');
      }
    }
  }

  console.log(`${site.name}: ${files.length} posts | HTML fixes: ${siteFixed} | Expanded: ${siteExpanded}`);
  totalFixed    += siteFixed;
  totalExpanded += siteExpanded;
}

console.log(`\nTotal HTML fixes: ${totalFixed}`);
console.log(`Total expanded:   ${totalExpanded}`);
if (DRY_RUN) console.log('(DRY RUN — no files written)');
