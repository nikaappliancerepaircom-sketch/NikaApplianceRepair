/**
 * gen-og-images.js — Generate 4 visually distinct 1200x630 OG images using Sharp.
 *
 * Each brand gets a custom SVG layout (different colors, typography, layout) rendered to JPG.
 *
 * Requires: sharp (install with `npm install sharp` if not already available globally).
 *
 * Usage: node gen-og-images.js
 */
const fs = require('fs');
const path = require('path');

const sharp = require('sharp');

const W = 1200, H = 630;

// === BRAND 1: NIKA — Clean white minimalist ===
const nikaSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg1)"/>
  <rect x="0" y="0" width="14" height="${H}" fill="#2563eb"/>
  <circle cx="1100" cy="100" r="280" fill="#2563eb" opacity="0.06"/>
  <text x="80" y="170" font-family="Inter, Arial, sans-serif" font-weight="700" font-size="32" fill="#0f172a" letter-spacing="-1">🔧 NIKA</text>
  <text x="80" y="260" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="64" fill="#0f172a" letter-spacing="-2">Appliance Repair</text>
  <text x="80" y="328" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="64" fill="#2563eb" letter-spacing="-2">Toronto · Same-Day</text>
  <text x="80" y="400" font-family="Inter, Arial, sans-serif" font-weight="400" font-size="26" fill="#475569">Licensed technicians · 90-day warranty · Free diagnostic</text>
  <g transform="translate(80, 460)">
    <rect x="0" y="0" width="178" height="40" rx="20" fill="white" stroke="#e2e8f0" stroke-width="1"/>
    <text x="89" y="26" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="14" fill="#0f172a">🛡️ TSSA Licensed</text>
    <rect x="190" y="0" width="178" height="40" rx="20" fill="white" stroke="#e2e8f0" stroke-width="1"/>
    <text x="279" y="26" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="14" fill="#0f172a">⏱️ Same-Day</text>
    <rect x="380" y="0" width="220" height="40" rx="20" fill="white" stroke="#e2e8f0" stroke-width="1"/>
    <text x="490" y="26" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="14" fill="#0f172a">📞 (437) 524-1053</text>
  </g>
  <text x="80" y="585" font-family="Inter, Arial, sans-serif" font-weight="500" font-size="14" fill="#94a3b8">nikaappliancerepair.com · Trusted in the GTA since 2017</text>
</svg>`;

// === BRAND 2: NAR — Warm cream traditional ===
const narSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF7F2"/>
      <stop offset="100%" stop-color="#F0EBE0"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg2)"/>
  <circle cx="100" cy="${H-100}" r="180" fill="#F97316" opacity="0.10"/>
  <circle cx="${W-150}" cy="80" r="120" fill="#1E40AF" opacity="0.08"/>
  <text x="80" y="240" font-family="Georgia, 'Times New Roman', serif" font-weight="900" font-size="180" fill="#1E40AF" letter-spacing="-8">N</text>
  <text x="240" y="170" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="48" fill="#1E40AF">Appliance Repair</text>
  <text x="240" y="225" font-family="Georgia, 'Times New Roman', serif" font-weight="400" font-style="italic" font-size="28" fill="#92400E">Trusted in your neighbourhood</text>
  <text x="80" y="370" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="42" fill="#0c1929">Serving York Region:</text>
  <text x="80" y="420" font-family="Georgia, 'Times New Roman', serif" font-weight="400" font-size="32" fill="#475569">Richmond Hill · Newmarket · Markham · Vaughan · Bradford</text>
  <rect x="80" y="475" width="600" height="60" rx="6" fill="#1E40AF"/>
  <text x="380" y="514" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="26" fill="white">📞 (437) 524-1053 · Same-day service</text>
  <text x="80" y="595" font-family="Georgia, 'Times New Roman', serif" font-style="italic" font-size="14" fill="#92400E">nappliancerepair.com · Family-trusted since 2017 · TSSA Licensed · Insured · Bonded</text>
</svg>`;

// === BRAND 3: NEARY — Light grey diagonal geometric ===
const nearySvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F1F5F9"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg3)"/>
  <polygon points="0,0 700,0 500,${H} 0,${H}" fill="#42A5F5" opacity="0.10"/>
  <polygon points="0,0 350,0 250,${H} 0,${H}" fill="#42A5F5" opacity="0.15"/>
  <rect x="0" y="0" width="8" height="${H}" fill="#42A5F5"/>
  <rect x="80" y="80" width="170" height="46" rx="4" fill="#42A5F5"/>
  <text x="165" y="111" text-anchor="middle" font-family="'Arial Narrow', sans-serif" font-weight="800" font-size="22" letter-spacing="3" fill="white">NEAR ME</text>
  <text x="80" y="220" font-family="'Arial Narrow', Impact, sans-serif" font-weight="900" font-size="72" letter-spacing="-1" fill="#0c1929">APPLIANCE REPAIR</text>
  <text x="80" y="290" font-family="'Arial Narrow', Impact, sans-serif" font-weight="900" font-size="72" letter-spacing="-1" fill="#0c1929">NEAR ME</text>
  <text x="80" y="360" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="28" letter-spacing="2" fill="#42A5F5">SAME-DAY · WEST GTA</text>
  <text x="80" y="400" font-family="Arial, Helvetica, sans-serif" font-weight="400" font-size="22" fill="#475569">Mississauga · Brampton · Oakville · Burlington</text>
  <g transform="translate(80, 460)">
    <rect x="0" y="0" width="180" height="80" rx="6" fill="white"/>
    <text x="90" y="40" text-anchor="middle" font-family="Arial, sans-serif" font-weight="900" font-size="34" fill="#42A5F5">90</text>
    <text x="90" y="60" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="11" letter-spacing="2" fill="#475569">DAY WARRANTY</text>
    <rect x="200" y="0" width="180" height="80" rx="6" fill="white"/>
    <text x="290" y="40" text-anchor="middle" font-family="Arial, sans-serif" font-weight="900" font-size="34" fill="#42A5F5">4.9★</text>
    <text x="290" y="60" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="11" letter-spacing="2" fill="#475569">150+ REVIEWS</text>
    <rect x="400" y="0" width="290" height="80" rx="6" fill="#0c1929"/>
    <text x="545" y="35" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="13" letter-spacing="2" fill="#94a3b8">CALL NOW</text>
    <text x="545" y="62" text-anchor="middle" font-family="Arial, sans-serif" font-weight="900" font-size="20" fill="white">(437) 524-1053</text>
  </g>
  <text x="80" y="595" font-family="Arial, sans-serif" font-weight="500" font-size="13" letter-spacing="1" fill="#475569">APPLIANCEREPAIRNEARY.COM · TSSA LICENSED · SINCE 2017</text>
</svg>`;

// === BRAND 4: FIXLIFY — Dark cinematic ===
const fixlifySvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#030810"/>
      <stop offset="50%" stop-color="#0D1B2A"/>
      <stop offset="100%" stop-color="#091422"/>
    </linearGradient>
    <radialGradient id="glow1" cx="20%" cy="80%" r="50%">
      <stop offset="0%" stop-color="#FF6B35" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#FF6B35" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="80%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#00C2FF" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#00C2FF" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg4)"/>
  <rect width="100%" height="100%" fill="url(#glow1)"/>
  <rect width="100%" height="100%" fill="url(#glow2)"/>
  <rect x="80" y="80" width="200" height="36" rx="18" fill="rgba(255,107,53,0.12)" stroke="#FF6B35" stroke-width="1" stroke-opacity="0.3"/>
  <text x="180" y="104" text-anchor="middle" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="700" font-size="13" letter-spacing="3" fill="#FF6B35">SAME-DAY · GTA</text>
  <text x="80" y="225" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="800" font-size="92" fill="#E8F4FD" letter-spacing="-3">Fixlify</text>
  <text x="80" y="295" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="700" font-size="42" fill="#00C2FF" letter-spacing="-1">Appliance Services</text>
  <text x="80" y="370" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="600" font-size="28" fill="#E8F4FD" opacity="0.85">Fast repair. Transparent pricing. East GTA.</text>
  <text x="80" y="410" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="400" font-size="22" fill="#E8F4FD" opacity="0.55">Scarborough · Pickering · Ajax · Whitby · Oshawa</text>
  <rect x="80" y="465" width="280" height="72" rx="36" fill="#FF6B35"/>
  <text x="220" y="510" text-anchor="middle" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="800" font-size="22" fill="#000">Book Online →</text>
  <rect x="380" y="465" width="320" height="72" rx="36" fill="rgba(0,194,255,0.12)" stroke="#00C2FF" stroke-width="2" stroke-opacity="0.4"/>
  <text x="540" y="510" text-anchor="middle" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="800" font-size="22" fill="#00C2FF">📞 (437) 524-1053</text>
  <text x="80" y="595" font-family="'Outfit', Inter, Arial, sans-serif" font-weight="500" font-size="13" letter-spacing="2" fill="#E8F4FD" opacity="0.35">FIXLIFYSERVICES.COM · TSSA LICENSED · INSURED · SINCE 2017</text>
</svg>`;

const targets = [
  { svg: nikaSvg,    outs: ['C:/NikaApplianceRepair/og-default.jpg', 'C:/NikaApplianceRepair/og-image.jpg'] },
  { svg: narSvg,     outs: ['C:/nappliancerepair/og-image.jpg', 'C:/nappliancerepair/og-default.jpg'] },
  { svg: nearySvg,   outs: ['C:/appliancerepairneary/og-image.jpg', 'C:/appliancerepairneary/og-default.jpg'] },
  { svg: fixlifySvg, outs: ['C:/fixlifyservices/og-image.jpg', 'C:/fixlifyservices/og-default.jpg'] },
];

(async () => {
  for (const t of targets) {
    const buf = Buffer.from(t.svg);
    const img = await sharp(buf, { density: 144 }).resize(W, H).jpeg({ quality: 90, mozjpeg: true }).toBuffer();
    for (const out of t.outs) {
      fs.writeFileSync(out, img);
      console.log('Wrote:', out, `(${img.length} bytes)`);
    }
  }
})().catch(e => { console.error(e); process.exit(1); });
