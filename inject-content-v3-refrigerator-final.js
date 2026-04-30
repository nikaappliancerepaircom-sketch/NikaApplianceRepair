const fs = require('fs');
const path = require('path');

const { data } = require('./inject-content-v3-refrigerator.js');
const { data2 } = require('./inject-content-v3-refrigerator-part2.js');
const { data3 } = require('./inject-content-v3-refrigerator-part3.js');

const allData = Object.assign({}, data, data2, data3);

const BASE = 'C:/NikaApplianceRepair/locations/services';
const MARKER = '<!-- CONTENT-v3 -->';
const SVC = 'refrigerator-repair';

function buildSection(d) {
  return `    <!-- CONTENT-v3 -->
    <section style="background: #f0f7ff; padding: 3rem 0; border-top: 1px solid #bbdefb;">
        <div class="container">
            <h2>Refrigerator Repair in ${d.loc} &#8212; Your Questions Answered</h2>
            <p>Nika Appliance Repair has served ${d.loc} since 2017. Here are the most common questions from ${d.loc} residents about refrigerator repair:</p>
            <div class="faq-item">
              <div class="faq-question">${d.q1}</div>
              <div class="faq-answer"><p>${d.a1}</p></div>
            </div>
            <div class="faq-item">
              <div class="faq-question">${d.q2}</div>
              <div class="faq-answer"><p>${d.a2}</p></div>
            </div>
            <div class="faq-item">
              <div class="faq-question">${d.q3}</div>
              <div class="faq-answer"><p>${d.a3}</p></div>
            </div>
            <div class="faq-item">
              <div class="faq-question">${d.q4}</div>
              <div class="faq-answer"><p>${d.a4}</p></div>
            </div>
            <div class="faq-item">
              <div class="faq-question">${d.q5}</div>
              <div class="faq-answer"><p>${d.a5}</p></div>
            </div>
        </div>
    </section>

`;
}

function trunc(s, n) {
  return s.substring(0, n).replace(/"/g, '\\"').replace(/\n/g, ' ');
}

function buildSchemaAdditions(d) {
  return [[d.q1, d.a1], [d.q2, d.a2], [d.q3, d.a3], [d.q4, d.a4], [d.q5, d.a5]]
    .map(([q, a]) => `    ,{\n      "@type": "Question",\n      "name": "${q.replace(/"/g, '\\"')}",\n      "acceptedAnswer": { "@type": "Answer", "text": "${trunc(a, 300)}" }\n    }`)
    .join('\n');
}

let done = 0, skip = 0, err = 0;

for (const [slug, d] of Object.entries(allData)) {
  const file = path.join(BASE, `${SVC}-${slug}.html`);
  if (!fs.existsSync(file)) {
    console.log(`MISSING: ${SVC}-${slug}.html`);
    err++;
    continue;
  }
  let html = fs.readFileSync(file, 'utf8');
  if (html.includes(MARKER)) {
    console.log(`SKIP (already done): ${slug}`);
    skip++;
    continue;
  }
  const CTA = '    <section class="cta-section">';
  if (!html.includes(CTA)) {
    console.log(`NO CTA SECTION: ${slug}`);
    err++;
    continue;
  }
  html = html.replace(CTA, buildSection(d) + CTA);

  // Inject into FAQPage schema
  const faqStart = html.indexOf('"@type": "FAQPage"');
  if (faqStart !== -1) {
    const scriptEnd = html.indexOf('</script>', faqStart);
    if (scriptEnd !== -1) {
      const faqSec = html.substring(faqStart, scriptEnd);
      const lastBracket = faqSec.lastIndexOf('\n        ]');
      if (lastBracket !== -1) {
        const insertPos = faqStart + lastBracket;
        html = html.substring(0, insertPos) + '\n' + buildSchemaAdditions(d) + html.substring(insertPos);
      }
    }
  }

  fs.writeFileSync(file, html, 'utf8');
  console.log(`OK: ${slug}`);
  done++;
}

console.log(`\nDone: ${done} processed, ${skip} skipped, ${err} errors`);
