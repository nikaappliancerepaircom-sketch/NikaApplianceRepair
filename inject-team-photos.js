#!/usr/bin/env node
// Injects branded team photos into about.html and index.html for each site.
// Run: node inject-team-photos.js

const fs = require('fs');
const path = require('path');

const SITES = [
  {
    dir: 'C:/fixlifyservices',
    domain: 'fixlifyservices.com',
    brand: 'Fixlify',
    heroPhoto: 'tech-hero-fixlify.webp',
    teamPhoto: 'tech-van-fixlify.webp',
    femalePhoto: 'tech-female-fixlify.webp',
    customerPhoto: 'tech-customer-fixlify.webp',
    city: 'Edmonton',
  },
  {
    dir: 'C:/appliancerepairneary',
    domain: 'appliancerepairneary.com',
    brand: 'Neary',
    heroPhoto: 'tech-hero-neary.webp',
    teamPhoto: 'tech-van-neary.webp',
    femalePhoto: 'tech-female-neary.webp',
    customerPhoto: 'tech-customer-neary.webp',
    city: 'Calgary',
  },
  {
    dir: 'C:/NikaApplianceRepair',
    domain: 'nikaappliancerepair.com',
    brand: 'Nika',
    heroPhoto: 'tech-hero-nika.webp',
    teamPhoto: 'tech-van-nika.webp',
    femalePhoto: 'tech-female-nika.webp',
    customerPhoto: 'tech-customer-nika.webp',
    city: 'Toronto',
  },
  {
    dir: 'C:/nappliancerepair',
    domain: 'nappliancerepair.com',
    brand: 'N Appliance',
    heroPhoto: 'tech-hero-nar.webp',
    teamPhoto: 'tech-van-nar.webp',
    femalePhoto: 'tech-female-nar.webp',
    customerPhoto: 'tech-customer-nar.webp',
    city: 'Richmond Hill',
  },
];

function injectAfterTag(html, tag, injection) {
  const idx = html.indexOf(tag);
  if (idx === -1) return null;
  const end = idx + tag.length;
  return html.slice(0, end) + '\n' + injection + html.slice(end);
}

function injectBeforeTag(html, tag, injection) {
  const idx = html.lastIndexOf(tag);
  if (idx === -1) return null;
  return html.slice(0, idx) + injection + '\n' + html.slice(idx);
}

function buildTeamBlock(site) {
  return `
<!-- Team photos — E-E-A-T signals -->
<section class="team-photos-section" style="padding:2.5rem 1rem;background:#f8f9fa;margin:2rem 0;border-radius:12px;">
  <h2 style="text-align:center;margin-bottom:1.5rem;font-size:1.5rem;">Meet Our ${site.city} Technicians</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;max-width:960px;margin:0 auto;">
    <figure style="margin:0;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.1);">
      <img src="/img/${site.heroPhoto}" alt="${site.brand} lead technician repairing appliance in ${site.city}" width="800" height="600" loading="lazy" style="width:100%;height:220px;object-fit:cover;display:block;" />
      <figcaption style="padding:0.75rem 1rem;background:#fff;font-size:0.9rem;color:#444;">Certified appliance repair — ${site.city}</figcaption>
    </figure>
    <figure style="margin:0;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.1);">
      <img src="/img/${site.femalePhoto}" alt="${site.brand} technician on the job in ${site.city}" width="800" height="600" loading="lazy" style="width:100%;height:220px;object-fit:cover;display:block;" />
      <figcaption style="padding:0.75rem 1rem;background:#fff;font-size:0.9rem;color:#444;">Our team serves all ${site.city} neighbourhoods</figcaption>
    </figure>
    <figure style="margin:0;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.1);">
      <img src="/img/${site.customerPhoto}" alt="${site.brand} customer satisfaction in ${site.city}" width="800" height="600" loading="lazy" style="width:100%;height:220px;object-fit:cover;display:block;" />
      <figcaption style="padding:0.75rem 1rem;background:#fff;font-size:0.9rem;color:#444;">Happy customers across ${site.city}</figcaption>
    </figure>
  </div>
</section>`;
}

function buildHeroPhoto(site) {
  return `
<div class="hero-team-photo" style="margin:1.5rem 0;border-radius:12px;overflow:hidden;max-height:380px;">
  <img src="/img/${site.teamPhoto}" alt="${site.brand} appliance repair team in ${site.city}" width="1200" height="900" loading="eager" style="width:100%;height:auto;object-fit:cover;display:block;" />
</div>`;
}

for (const site of SITES) {
  console.log(`\n=== ${site.brand} (${site.dir}) ===`);

  // --- about.html ---
  const aboutPath = path.join(site.dir, 'about.html');
  if (fs.existsSync(aboutPath)) {
    let html = fs.readFileSync(aboutPath, 'utf8');
    if (html.includes('team-photos-section')) {
      console.log('  about.html — already has team photos, skipping');
    } else {
      const teamBlock = buildTeamBlock(site);
      // Inject before </main> or before <footer
      let updated = injectBeforeTag(html, '</main>', teamBlock);
      if (!updated) updated = injectBeforeTag(html, '<footer', teamBlock);
      if (updated) {
        fs.writeFileSync(aboutPath, updated, 'utf8');
        console.log('  about.html — team photo block injected ✓');
      } else {
        console.log('  about.html — could not find injection point');
      }
    }
  } else {
    console.log('  about.html — not found');
  }

  // --- index.html ---
  const indexPath = path.join(site.dir, 'index.html');
  if (fs.existsSync(indexPath)) {
    let html = fs.readFileSync(indexPath, 'utf8');
    if (html.includes('hero-team-photo')) {
      console.log('  index.html — already has hero photo, skipping');
    } else {
      const heroBlock = buildHeroPhoto(site);
      // Inject after </h1> in the hero section
      let updated = injectAfterTag(html, '</h1>', heroBlock);
      if (!updated) {
        // fallback: after first </section>
        updated = injectAfterTag(html, '</section>', heroBlock);
      }
      if (updated) {
        fs.writeFileSync(indexPath, updated, 'utf8');
        console.log('  index.html — hero team photo injected ✓');
      } else {
        console.log('  index.html — could not find injection point');
      }
    }
  } else {
    console.log('  index.html — not found');
  }
}

console.log('\nAll done.');
