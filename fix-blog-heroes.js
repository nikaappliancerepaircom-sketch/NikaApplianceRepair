#!/usr/bin/env node
/**
 * fix-blog-heroes.js
 * Replaces broken solid-color hero images with CSS gradient + SVG icon hero blocks.
 * Keeps <img> tag hidden for Google alt-text signal.
 * Usage: node fix-blog-heroes.js [--dry-run]
 */

const fs   = require('fs');
const path = require('path');

const BLOG_DIR = 'C:/NikaApplianceRepair/blog';
const DRY_RUN  = process.argv.includes('--dry-run');
const MAX_BROKEN_SIZE = 5000; // bytes — anything under 5KB is a placeholder

// ── Service type → gradient + icon ──────────────────────────────────────────
const SERVICE_THEMES = {
  dishwasher:   { grad: ['#1e3a8a','#3b82f6'], label: 'Dishwasher Repair',  icon: 'dishwasher'   },
  washer:       { grad: ['#134e4a','#14b8a6'], label: 'Washer Repair',      icon: 'washer'       },
  washing:      { grad: ['#134e4a','#14b8a6'], label: 'Washer Repair',      icon: 'washer'       },
  dryer:        { grad: ['#7c2d12','#f97316'], label: 'Dryer Repair',       icon: 'dryer'        },
  refrigerator: { grad: ['#0c4a6e','#0ea5e9'], label: 'Fridge Repair',      icon: 'fridge'       },
  fridge:       { grad: ['#0c4a6e','#0ea5e9'], label: 'Fridge Repair',      icon: 'fridge'       },
  freezer:      { grad: ['#0c4a6e','#38bdf8'], label: 'Freezer Repair',     icon: 'fridge'       },
  'ice-maker':  { grad: ['#0e7490','#67e8f9'], label: 'Ice Maker Repair',   icon: 'fridge'       },
  ice:          { grad: ['#0e7490','#67e8f9'], label: 'Ice Maker Repair',   icon: 'fridge'       },
  oven:         { grad: ['#7f1d1d','#ef4444'], label: 'Oven Repair',        icon: 'oven'         },
  stove:        { grad: ['#7f1d1d','#f87171'], label: 'Stove Repair',       icon: 'oven'         },
  range:        { grad: ['#78350f','#f59e0b'], label: 'Range Repair',       icon: 'oven'         },
  burner:       { grad: ['#78350f','#fbbf24'], label: 'Stove Burner Repair',icon: 'oven'         },
  microwave:    { grad: ['#4c1d95','#a78bfa'], label: 'Microwave Repair',   icon: 'microwave'    },
  garbage:      { grad: ['#14532d','#22c55e'], label: 'Garbage Disposal',   icon: 'tools'        },
  disposal:     { grad: ['#14532d','#4ade80'], label: 'Disposal Repair',    icon: 'tools'        },
  'water-heater':{ grad: ['#1e3a8a','#6366f1'], label: 'Water Heater',     icon: 'tools'        },
  water:        { grad: ['#1e3a8a','#818cf8'], label: 'Water Heater Repair',icon: 'tools'        },
  gas:          { grad: ['#78350f','#fb923c'], label: 'Gas Appliance Repair',icon:'oven'         },
  appliance:    { grad: ['#1e3a5f','#2563eb'], label: 'Appliance Repair',   icon: 'wrench'       },
  default:      { grad: ['#1e3a5f','#2563eb'], label: 'Appliance Repair',   icon: 'wrench'       },
};

// ── SVG Icons ────────────────────────────────────────────────────────────────
function getIcon(type) {
  const icons = {
    wrench: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
    </svg>`,
    dishwasher: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="3" width="20" height="18" rx="2"/>
      <line x1="2" y1="9" x2="22" y2="9"/>
      <circle cx="12" cy="15" r="3"/>
      <path d="M12 12v1M12 18v1M9 15H8M16 15h-1"/>
    </svg>`,
    washer: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="2" width="20" height="20" rx="2"/>
      <circle cx="12" cy="13" r="5"/>
      <circle cx="12" cy="13" r="2"/>
      <line x1="6" y1="6" x2="6.01" y2="6"/>
      <line x1="10" y1="6" x2="14" y2="6"/>
    </svg>`,
    dryer: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="2" width="20" height="20" rx="2"/>
      <circle cx="12" cy="13" r="5"/>
      <path d="M9.5 10.5l5 5M14.5 10.5l-5 5"/>
      <line x1="6" y1="6" x2="6.01" y2="6"/>
    </svg>`,
    fridge: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <rect x="4" y="2" width="16" height="20" rx="2"/>
      <line x1="4" y1="10" x2="20" y2="10"/>
      <line x1="9" y1="6" x2="9" y2="9"/>
      <line x1="9" y1="14" x2="9" y2="19"/>
    </svg>`,
    oven: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="4" width="20" height="18" rx="2"/>
      <rect x="6" y="9" width="12" height="9" rx="1"/>
      <circle cx="7" cy="6.5" r="0.5" fill="rgba(255,255,255,0.9)"/>
      <circle cx="10" cy="6.5" r="0.5" fill="rgba(255,255,255,0.9)"/>
      <circle cx="14" cy="6.5" r="0.5" fill="rgba(255,255,255,0.9)"/>
      <circle cx="17" cy="6.5" r="0.5" fill="rgba(255,255,255,0.9)"/>
    </svg>`,
    microwave: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="6" width="20" height="14" rx="2"/>
      <rect x="5" y="9" width="11" height="8" rx="1"/>
      <line x1="18" y1="9" x2="18" y2="10"/>
      <line x1="18" y1="13" x2="18" y2="14"/>
    </svg>`,
    tools: `<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 21l9-9"/>
      <path d="M12.22 6.22A6.01 6.01 0 0 0 6 5c-.36.87-.54 1.8-.54 2.74C5.46 10.12 7.46 12 9.87 12c.98 0 1.9-.28 2.7-.78"/>
      <path d="M20.97 7.77A10 10 0 0 0 12 2c-.56 0-1.11.05-1.65.14"/>
      <path d="M20.97 7.77l-3.1 3.1a2 2 0 0 1-2.82 0L13.2 9.03a2 2 0 0 1 0-2.83l3.1-3.1"/>
    </svg>`,
  };
  return icons[type] || icons.wrench;
}

// ── Detect service from filename ─────────────────────────────────────────────
function detectTheme(filename) {
  const base = filename.toLowerCase().replace(/-hero\.webp$/, '').replace(/\.html$/, '');
  for (const [key, theme] of Object.entries(SERVICE_THEMES)) {
    if (key === 'default') continue;
    if (base.includes(key.replace('-', '-'))) return theme;
  }
  return SERVICE_THEMES.default;
}

// ── Build CSS hero replacement HTML ─────────────────────────────────────────
function buildHero(theme, altText, imgRelPath) {
  const [c1, c2] = theme.grad;
  const icon = getIcon(theme.icon);
  return `<div class="blog-hero-image" style="background:linear-gradient(135deg,${c1} 0%,${c2} 100%);height:380px;display:flex;align-items:center;justify-content:center;border-radius:12px;margin:1.5rem 0 2rem;overflow:hidden;position:relative;">
  <div style="text-align:center;color:white;padding:2rem;position:relative;z-index:1;">
    ${icon}
    <div style="font-size:1.4rem;font-weight:700;margin-top:1rem;text-shadow:0 2px 4px rgba(0,0,0,0.3);">${theme.label}</div>
    <div style="font-size:0.95rem;margin-top:0.5rem;opacity:0.85;">Toronto &amp; GTA — Same-Day Service</div>
  </div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 50%,rgba(255,255,255,0.08) 0%,transparent 60%);pointer-events:none;"></div>
  <!-- img kept for Google image signal -->
  <img src="${imgRelPath}" alt="${altText}" width="1" height="1" style="position:absolute;bottom:0;right:0;opacity:0.01;" loading="lazy" aria-hidden="true">
</div>`;
}

// ── Get broken image files list ──────────────────────────────────────────────
function getBrokenImages() {
  const imgDir = path.join(BLOG_DIR, 'images');
  const broken = new Set();
  try {
    for (const f of fs.readdirSync(imgDir)) {
      if (!f.endsWith('.webp')) continue;
      const size = fs.statSync(path.join(imgDir, f)).size;
      if (size < MAX_BROKEN_SIZE) broken.add(f);
    }
  } catch {}
  return broken;
}

// ── Walk blog HTML files ─────────────────────────────────────────────────────
function walkHtml(dir) {
  const out = [];
  try {
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      if (item.isDirectory() && !['css','images','_queue','node_modules'].includes(item.name)) {
        out.push(...walkHtml(path.join(dir, item.name)));
      } else if (item.name.endsWith('.html') && item.name !== 'index.html') {
        out.push(path.join(dir, item.name));
      }
    }
  } catch {}
  return out;
}

// ── Main ─────────────────────────────────────────────────────────────────────
const broken = getBrokenImages();
console.log(`\nBroken images found: ${broken.size}`);
console.log(`Mode: ${DRY_RUN ? '🔍 DRY RUN' : '✏️  LIVE'}\n`);

const htmlFiles = walkHtml(BLOG_DIR);
let fixed = 0, skipped = 0, alreadyFixed = 0;

// Regex to match the full hero block: <div class="blog-hero-image">...<picture>...</picture>...</div>
const HERO_RE = /<div class="blog-hero-image">\s*<picture>\s*<source[^>]+srcset="([^"]+)"[^>]*>\s*<img[^>]+alt="([^"]*)"[^>]*>\s*<\/picture>\s*<\/div>/s;

for (const filePath of htmlFiles) {
  const html = fs.readFileSync(filePath, 'utf8');

  // Skip if already CSS hero (no <picture> inside blog-hero-image)
  if (html.includes('blog-hero-image') && !html.includes('<picture>')) {
    alreadyFixed++; continue;
  }

  const match = html.match(HERO_RE);
  if (!match) { skipped++; continue; }

  const [fullMatch, srcset, altText] = match;
  // srcset is like "../images/foo-hero.webp" — extract filename
  const imgFile = path.basename(srcset);

  if (!broken.has(imgFile)) { skipped++; continue; }

  // Determine theme from filename (no extension)
  const theme = detectTheme(path.basename(filePath));
  const heroHtml = buildHero(theme, altText || 'Appliance repair technician in Toronto', srcset);

  console.log(`[FIX] ${path.relative(BLOG_DIR, filePath)}`);
  console.log(`      img: ${imgFile} (broken) → CSS hero (${theme.label})`);

  if (!DRY_RUN) {
    fs.writeFileSync(filePath, html.replace(fullMatch, heroHtml), 'utf8');
  }
  fixed++;
}

console.log(`\n${'─'.repeat(60)}`);
console.log(`Fixed: ${fixed} | Already OK: ${alreadyFixed} | Skipped (no broken img): ${skipped}`);
if (DRY_RUN) console.log('[DRY RUN] No files changed.');
else if (fixed > 0) console.log('\n✅ Done! Commit and push to deploy.');
