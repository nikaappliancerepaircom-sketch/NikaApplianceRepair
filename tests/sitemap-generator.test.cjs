const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const test = require('node:test');

const DOMAIN = 'https://nikaappliancerepair.com';

function page(canonical, extraHead = '') {
  const canonicalTag = canonical
    ? `<link rel="canonical" href="${DOMAIN}${canonical}">`
    : '';
  return `<!doctype html><html><head>${canonicalTag}${extraHead}</head><body><main><h1>Test</h1></main></body></html>`;
}

test('keeps only existing, indexable, self-canonical published URLs', () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'nika-sitemap-'));
  fs.copyFileSync(path.join(__dirname, '..', 'gen-sitemap-full.js'), path.join(fixture, 'gen-sitemap-full.js'));
  fs.mkdirSync(path.join(fixture, 'blog'));
  fs.mkdirSync(path.join(fixture, 'includes'));

  fs.writeFileSync(path.join(fixture, 'index.html'), page('/'));
  fs.writeFileSync(path.join(fixture, 'ajax.html'), page('/ajax'));
  fs.writeFileSync(path.join(fixture, 'blog', 'index.html'), page('/blog'));
  fs.writeFileSync(path.join(fixture, 'olds.html'), page('/olds'));
  fs.writeFileSync(path.join(fixture, 'alternate.html'), page('/ajax'));
  fs.writeFileSync(path.join(fixture, 'noindex.html'), page('/noindex', '<meta name="robots" content="noindex, follow">'));
  fs.writeFileSync(path.join(fixture, 'redirect.html'), page('/redirect', '<meta http-equiv="refresh" content="0; url=/ajax">'));
  fs.writeFileSync(path.join(fixture, 'missing.html'), page(null));
  fs.writeFileSync(path.join(fixture, 'duplicate.html'), `${page('/duplicate')}<link rel="canonical" href="${DOMAIN}/duplicate">`);
  fs.writeFileSync(path.join(fixture, 'unpublished.html'), page('/unpublished'));
  fs.writeFileSync(path.join(fixture, 'includes', 'fragment.html'), page('/fragment'));

  const published = ['/', '/ajax', '/blog', '/olds', '/alternate', '/noindex', '/redirect', '/missing', '/duplicate'];
  fs.writeFileSync(
    path.join(fixture, 'sitemap.xml'),
    `<urlset>${published.map((url) => `<url><loc>${DOMAIN}${url}</loc></url>`).join('')}</urlset>`,
  );

  const output = execFileSync(process.execPath, ['gen-sitemap-full.js'], { cwd: fixture, encoding: 'utf8' });
  const result = JSON.parse(output);
  const sitemap = fs.readFileSync(path.join(fixture, 'sitemap.xml'), 'utf8');
  const urls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);

  assert.deepEqual(urls, [`${DOMAIN}/`, `${DOMAIN}/ajax`, `${DOMAIN}/blog`, `${DOMAIN}/olds`]);
  assert.equal(result.urls, 4);
  assert.equal(result.skipped.alternateCanonical, 1);
  assert.equal(result.skipped.noindex, 1);
  assert.equal(result.skipped.redirect, 1);
  assert.equal(result.skipped.missingCanonical, 1);
  assert.equal(result.skipped.duplicateCanonical, 1);
  assert.equal(result.skipped.unpublished, 1);
  assert.doesNotMatch(sitemap, /<lastmod>/);
});
