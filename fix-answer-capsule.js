#!/usr/bin/env node
/**
 * Fix pre-existing corruption in answer-capsule paragraphs across all v1 washer files.
 * The corruption pattern: "Typical cost </section>20–$320..." in itemprop="description" paragraph.
 */

const fs = require('fs');
const path = require('path');

const SITE_DIR = 'C:/appliancerepairneary';
const CONTENT_DIR = 'C:/NikaApplianceRepair';

function loadAllContent() {
  const merged = {};
  for (let i = 1; i <= 4; i++) {
    const fp = path.join(CONTENT_DIR, 'washer-content-batch' + i + '.json');
    const data = JSON.parse(fs.readFileSync(fp, 'utf8'));
    Object.assign(merged, data.cities);
  }
  return merged;
}

const allContent = loadAllContent();

const files = fs.readdirSync(SITE_DIR)
  .filter(f => f.startsWith('washer-repair-') && f.endsWith('.html') && !f.includes('near-me'));

let fixed = 0, skipped = 0, failed = 0;

files.forEach(file => {
  const city = file.replace('washer-repair-', '').replace('.html', '');
  const filePath = path.join(SITE_DIR, file);
  let html = fs.readFileSync(filePath, 'utf8');

  // Check if corrupted
  const isCorrupted = html.includes('Typical cost </section>') ||
                      html.includes('cost </section>') ||
                      html.includes('</section>20') ||
                      html.includes('</div>20') ||
                      html.includes('<\/p>20') ||
                      /itemprop="description"[^>]*>[\s\S]{0,200}<\/section>/.test(html);

  if (!isCorrupted) {
    skipped++;
    return;
  }

  const content = allContent[city];
  if (!content) {
    console.log('SKIP  ' + file + ' — no content data');
    failed++;
    return;
  }

  // Replace the corrupted itemprop description paragraph
  // The corruption is inside: <p style="..." itemprop="description">CORRUPTED TEXT</p>
  const fixed_html = html.replace(
    /(<div class="answer-capsule"[^>]*>[\s\S]*?<p[^>]*itemprop="description"[^>]*>)([\s\S]*?)(<\/p>\s*<\/div>)/,
    (match, open, inner, close) => {
      return open + content.answer_capsule + close;
    }
  );

  if (fixed_html !== html) {
    fs.writeFileSync(filePath, fixed_html, 'utf8');
    console.log('OK    ' + file);
    fixed++;
  } else {
    console.log('WARN  ' + file + ' — pattern not matched despite corruption detected');
    failed++;
  }
});

console.log('\n===== FIX SUMMARY =====');
console.log('Fixed:   ' + fixed);
console.log('Skipped: ' + skipped + ' (not corrupted)');
console.log('Failed:  ' + failed);
