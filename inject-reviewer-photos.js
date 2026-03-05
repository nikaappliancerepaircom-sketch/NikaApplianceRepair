/**
 * Inject reviewer photos into all 3 satellite site homepages.
 *
 * 1. Resize photos from reviewer-photos/ to 200x200 JPEG (~15-25KB)
 * 2. Copy to each site's img/reviewers/ directory
 * 3. Replace <div class="review-avatar">XX</div> with <img> tags in index.html
 *
 * Usage: node inject-reviewer-photos.js [--dry-run]
 */
const fs = require('fs');
const path = require('path');

const PHOTOS_DIR = path.join(__dirname, 'reviewer-photos');

const SITES = {
  nar: {
    dir: 'C:/nappliancerepair',
    name: 'N Appliance Repair',
    reviewers: {
      'PR': 'PR.jpg',
      'MT': 'MT.jpg',
      'SK': 'SK.jpg',
      'JC': 'JC.jpg',
      'LW': 'LW.jpg',
      'AN': 'AN_ahmed.jpg',
    },
  },
  neary: {
    dir: 'C:/appliancerepairneary',
    name: 'Appliance Repair Near Me',
    reviewers: {
      'JT': 'JT.jpg',
      'RK': 'RK.jpg',
      'SP': 'SP.jpg',
      'MG': 'MG.jpg',
      'AL': 'AL.jpg',
      'DW': 'DW.jpg',
    },
  },
  fixlify: {
    dir: 'C:/fixlifyservices',
    name: 'Fixlify Appliance Services',
    reviewers: {
      'JR': 'JR.jpg',
      'PK': 'PK.jpg',
      'MT': 'MT.jpg',
      'SL': 'SL.jpg',
      'DW': 'DW.jpg',
      'AN': 'AN_amira.jpg',
    },
  },
};

async function resizePhoto(srcPath, destPath) {
  try {
    const sharp = require('sharp');
    await sharp(srcPath)
      .resize(200, 200, { fit: 'cover' })
      .jpeg({ quality: 80 })
      .toFile(destPath);
    return true;
  } catch (e) {
    // Fallback: just copy the original
    fs.copyFileSync(srcPath, destPath);
    return true;
  }
}

function updateHtml(html, reviewers) {
  let modified = html;

  // Update CSS for review-avatar to support images
  if (!modified.includes('.review-avatar img')) {
    const avatarCssMatch = modified.match(/\.review-avatar\s*\{[^}]+\}/);
    if (avatarCssMatch) {
      const newCss = avatarCssMatch[0] + '\n.review-avatar img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block; }';
      modified = modified.replace(avatarCssMatch[0], newCss);
    }
  }

  // Replace each reviewer's initials div with an img tag
  for (const [initials] of Object.entries(reviewers)) {
    const outputName = initials.toLowerCase() + '.jpg';
    const pattern = new RegExp(
      `<div class="review-avatar">${initials}</div>`,
      'g'
    );
    const replacement = `<div class="review-avatar"><img src="/img/reviewers/${outputName}" alt="Reviewer photo" width="200" height="200" loading="lazy"></div>`;
    modified = modified.replace(pattern, replacement);
  }

  return modified;
}

async function main() {
  const dryRun = process.argv.includes('--dry-run');

  for (const [siteKey, site] of Object.entries(SITES)) {
    console.log(`\n=== ${site.name} ===`);

    const reviewersDir = path.join(site.dir, 'img', 'reviewers');

    if (!dryRun) {
      fs.mkdirSync(reviewersDir, { recursive: true });
    }
    console.log(`  Directory: ${reviewersDir}`);

    for (const [initials, photoFile] of Object.entries(site.reviewers)) {
      const srcPath = path.join(PHOTOS_DIR, photoFile);
      const outputName = initials.toLowerCase() + '.jpg';
      const destPath = path.join(reviewersDir, outputName);

      if (!fs.existsSync(srcPath)) {
        console.log(`  SKIP: ${photoFile} not found`);
        continue;
      }

      if (dryRun) {
        const srcSize = (fs.statSync(srcPath).size / 1024).toFixed(0);
        console.log(`  [DRY] ${photoFile} (${srcSize}KB) → img/reviewers/${outputName}`);
      } else {
        await resizePhoto(srcPath, destPath);
        const destSize = (fs.statSync(destPath).size / 1024).toFixed(0);
        console.log(`  ${photoFile} → img/reviewers/${outputName} (${destSize}KB)`);
      }
    }

    const indexPath = path.join(site.dir, 'index.html');
    if (!fs.existsSync(indexPath)) {
      console.log(`  SKIP: index.html not found`);
      continue;
    }

    const html = fs.readFileSync(indexPath, 'utf8');
    const newHtml = updateHtml(html, site.reviewers);

    if (newHtml !== html) {
      if (dryRun) {
        console.log(`  [DRY] Would update ${Object.keys(site.reviewers).length} reviewer avatars in index.html`);
      } else {
        fs.writeFileSync(indexPath, newHtml);
        console.log(`  Updated index.html with photo avatars`);
      }
    } else {
      console.log(`  No changes needed in index.html`);
    }
  }

  console.log(dryRun ? '\n[DRY RUN] No files changed.' : '\nDone! All reviewer photos injected.');
}

main().catch(e => { console.error(e); process.exit(1); });
