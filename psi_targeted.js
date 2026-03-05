const https = require('https');

const KEY = 'REDACTED_PSI_KEY';
const URLS = [
  'https://nikaappliancerepair.com/services/dishwasher-repair',
  'https://nikaappliancerepair.com/services/washer-repair',
  'https://nikaappliancerepair.com/services/dryer-repair',
  'https://nikaappliancerepair.com/services/oven-repair',
  'https://nikaappliancerepair.com/services/microwave-repair',
  'https://nikaappliancerepair.com/locations/toronto',
  'https://nikaappliancerepair.com/locations/scarborough',
  'https://nikaappliancerepair.com/locations/north-york',
  'https://nikaappliancerepair.com/locations/mississauga',
  'https://nikaappliancerepair.com/brands/samsung-appliance-repair-toronto',
  'https://nikaappliancerepair.com/brands/lg-appliance-repair-toronto',
  'https://nikaappliancerepair.com/brands/bosch-appliance-repair-toronto',
];

function psi(url) {
  return new Promise((resolve) => {
    const apiUrl = `https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&strategy=mobile&key=${KEY}`;
    let data = '';
    https.get(apiUrl, res => {
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          const cats = j.lighthouseResult?.categories || {};
          resolve({
            url: url.replace('https://nikaappliancerepair.com',''),
            perf: Math.round((cats.performance?.score||0)*100),
            acc: Math.round((cats.accessibility?.score||0)*100),
            bp: Math.round((cats['best-practices']?.score||0)*100),
            seo: Math.round((cats.seo?.score||0)*100),
          });
        } catch(e) { resolve({ url: url.replace('https://nikaappliancerepair.com',''), perf:'ERR', acc:'', bp:'', seo:'' }); }
      });
    }).on('error', () => resolve({ url, perf:'ERR' }));
  });
}

async function main() {
  console.log('\nPageSpeed Audit — nikaappliancerepair.com (MOBILE)\n');
  console.log(' URL                                          Perf  SEO   Status');
  console.log(' ' + '─'.repeat(65));
  let ok=0, warn=0, bad=0;
  for (const url of URLS) {
    const r = await psi(url);
    const short = r.url.padEnd(45);
    const status = r.perf >= 90 ? '✅' : r.perf >= 50 ? '⚠️ ' : '❌';
    if (r.perf >= 90) ok++; else if (r.perf >= 50) warn++; else bad++;
    console.log(` ${short} ${String(r.perf).padEnd(5)} ${String(r.seo).padEnd(5)} ${status}`);
  }
  console.log('\n' + '─'.repeat(65));
  console.log(`✅ ${ok}  ⚠️  ${warn}  ❌ ${bad} / ${URLS.length} pages`);
}
main();
