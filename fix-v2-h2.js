#!/usr/bin/env node
const fs = require('fs');

function loadAllContent() {
  const merged = {};
  for (let i = 1; i <= 4; i++) {
    const fp = 'C:/NikaApplianceRepair/washer-content-batch' + i + '.json';
    const data = JSON.parse(fs.readFileSync(fp, 'utf8'));
    Object.assign(merged, data.cities);
  }
  return merged;
}

const allContent = loadAllContent();
const V2_CITIES = [
  'bloor-west-village', 'chinatown', 'corso-italia', 'dufferin-grove', 'east-york',
  'etobicoke-village', 'greektown', 'high-park', 'king-west', 'little-italy',
  'little-portugal', 'midtown', 'ossington', 'roncesvalles', 'st-lawrence',
  'swansea', 'the-beaches', 'thorncliffe-park', 'trinity-bellwoods', 'wychwood'
];

let ok = 0, warn = 0;

V2_CITIES.forEach(function(citySlug) {
  const filePath = 'C:/appliancerepairneary/washer-repair-' + citySlug + '.html';
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;
  const content = allContent[citySlug];

  const cityTitle = citySlug.split('-').map(function(w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(' ');
  const searchStr = '<h2>About ' + cityTitle + '</h2>';
  const replaceStr = '<h2>' + content.content_h2 + '</h2>';

  if (html.indexOf(searchStr) >= 0) {
    html = html.replace(searchStr, replaceStr);
    fs.writeFileSync(filePath, html, 'utf8');
    console.log('OK    ' + citySlug);
    ok++;
  } else {
    // Check if already replaced
    if (html.indexOf(content.content_h2) >= 0) {
      console.log('SKIP  ' + citySlug + ' (already correct)');
    } else {
      // Try alternate patterns - some cities have hyphenated names
      const altTitle = citySlug.split('-').map(function(w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join('-');
      const searchStr2 = '<h2>About ' + altTitle + '</h2>';
      if (html.indexOf(searchStr2) >= 0) {
        html = html.replace(searchStr2, replaceStr);
        fs.writeFileSync(filePath, html, 'utf8');
        console.log('OK    ' + citySlug + ' (alt pattern)');
        ok++;
      } else {
        console.log('WARN  ' + citySlug + ' - no About h2 found');
        warn++;
      }
    }
  }
});

console.log('Done. OK: ' + ok + ' Warn: ' + warn);
