'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..');
const domain = 'https://nikaappliancerepair.com';
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const urls = [...read('sitemap.xml').matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
const inheritedEntries = JSON.parse(read('tests/fixtures/inherited-sitemap-entries.json'));
// The owner requires preserving legacy main entries as well as the audited canonical set.
const canonicalUrls = urls.filter(url => !Object.hasOwn(inheritedEntries, url));
const contactUrls = ['/team', '/team/michael-toronto', '/team/sarah-chen', '/team/david-martinez', '/team/james-wilson'].map(route => domain + route);
function source(url) {
  let rel = new URL(url).pathname.slice(1);
  if (!rel) rel = 'index.html';
  else if (fs.existsSync(path.join(root, rel + '.html'))) rel += '.html';
  else if (fs.statSync(path.join(root, rel)).isDirectory()) rel += '/index.html';
  return read(rel);
}
function attrs(tag) {
  return Object.fromEntries([...tag.matchAll(/([\w:-]+)\s*=\s*(["'])(.*?)\2/gs)].map(m => [m[1].toLowerCase(), m[3]]));
}
function* schemaObjects(value) {
  if (!value || typeof value !== 'object') return;
  yield value;
  for (const child of Object.values(value)) yield* schemaObjects(child);
}

test('every audited sitemap URL is a served canonical page with useful head metadata', () => {
  assert.equal(new Set(urls).size, urls.length);
  assert.ok(urls.length > 2000);
  for (const url of canonicalUrls) {
    const head = source(url).split(/<\/head>/i)[0];
    assert.match(head, /<title\b[^>]*>\s*[^<\s][^<]*<\/title>/i, url + ': title');
    const links = [...head.matchAll(/<link\b[^>]*>/gi)].map(m => attrs(m[0]));
    assert.deepEqual(links.filter(a => a.rel === 'canonical').map(a => a.href), [url], url);
    const metas = [...head.matchAll(/<meta\b[^>]*>/gi)].map(m => attrs(m[0]));
    assert.ok(metas.some(a => a.name === 'description' && a.content), url + ': description');
    assert.ok(!metas.some(a => /^(robots|googlebot)$/i.test(a.name || '') && /noindex/i.test(a.content || '')), url + ': noindex');
    for (const property of ['og:title', 'og:description', 'og:url', 'og:image']) {
      assert.ok(metas.some(a => a.property === property && a.content), url + ': ' + property);
    }
    assert.ok(!/\*\s*\{[^}]*overflow-x:\s*hidden\s*!important/.test(head), url + ': nested-scroll regression');
  }
});

test('sitemap preserves inherited main entries with their existing canonical and noindex values', () => {
  for (const [url, expected] of Object.entries(inheritedEntries)) {
    assert.ok(urls.includes(url), url + ': inherited main entry was removed');
    const head = source(url).split(/<\/head>/i)[0];
    const links = [...head.matchAll(/<link\b[^>]*>/gi)].map(m => attrs(m[0]));
    assert.deepEqual(links.filter(a => a.rel === 'canonical').map(a => a.href), expected.canonical, url);
    const metas = [...head.matchAll(/<meta\b[^>]*>/gi)].map(m => attrs(m[0]));
    const noindex = metas.some(a => /^(robots|googlebot)$/i.test(a.name || '') && /noindex/i.test(a.content || ''));
    assert.equal(noindex, expected.noindex, url + ': inherited indexing setting changed');
  }
});

test('schema parses and Nika business facts do not invent founder, staff, address or ratings', () => {
  for (const url of [...canonicalUrls, ...contactUrls, domain + '/book']) {
    const text = source(url);
    const alberta = /"addressRegion"\s*:\s*"(?:AB|Alberta)"/.test(text);
    if (!alberta) {
      assert.ok(!text.includes('founder Ron'), url + ': unsupported founder in visible copy');
      assert.ok(!/class=["']lz-trust-author["']/.test(text), url + ': unsupported reviewer in visible copy');
    }
    for (const match of text.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>(.*?)<\/script>/gis)) {
      const schema = JSON.parse(match[1]);
      for (const business of schemaObjects(schema)) {
        if (!alberta && business['@type'] === 'Organization') {
          if (url === domain + '/book') assert.equal('priceRange' in business, false, url + ': Organization priceRange');
          for (const field of ['founder', 'numberOfEmployees', 'aggregateRating', 'review', 'address', 'geo']) {
            assert.equal(field in business, false, url + ': ' + field);
          }
        }
      }
    }
  }
});

test('North York repair pages have separate visible answers, service schema and city links', () => {
  const city = read('locations/north-york.html');
  const guide = read('llms.txt');
  for (const appliance of ['refrigerator', 'washer']) {
    const url = domain + '/locations/services/' + appliance + '-repair-north-york';
    assert.ok(urls.includes(url), url);
    const text = source(url);
    assert.match(text, /<h1\b/);
    assert.match(text, /<details>/);
    assert.ok(city.includes(new URL(url).pathname));
    assert.ok(guide.includes(url));
    const schema = JSON.parse(text.match(/type="application\/ld\+json">\s*(.*?)<\/script>/s)[1]);
    assert.ok(schema['@graph'].some(item => item['@type'] === 'Service' && item.url === url));
    assert.ok(!/"(?:aggregateRating|founder|numberOfEmployees|address|price)"/.test(text));
    assert.ok(text.includes('tel:+14375241053'));
    assert.ok(text.includes('href="/book"'));
  }
});

test('shared promotion styles stay still and reduced-motion remains usable', () => {
  for (const file of ['style.css', 'cta-buttons.css', 'styles.css', 'areas-premium.css', 'brands-premium.css', 'common-problems-premium.css']) {
    assert.ok(!/animation:\s*(?:pulse(?:-shadow(?:-purple)?)?|shimmer)\b/.test(read('css/' + file)), file);
  }
  assert.match(read('css/responsive-comprehensive.css'), /prefers-reduced-motion:\s*reduce/);
  assert.match(read('css/responsive-comprehensive.css'), /scroll-behavior:\s*auto\s*!important/);
});

test('Toronto call links use the confirmed Nika business number', () => {
  for (const url of [...canonicalUrls, ...contactUrls]) {
    const text = source(url);
    if (/"addressRegion"\s*:\s*"(?:AB|Alberta)"/.test(text)) continue;
    for (const match of text.matchAll(/href=["']tel:([^"']+)["']/gi)) {
      const number = match[1].replace(/\D/g, '');
      assert.ok(['4375241053', '14375241053'].includes(number), url + ': ' + match[1]);
    }
  }
});
