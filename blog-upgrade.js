/**
 * blog-upgrade.js — Comprehensive blog fix for 3 satellite sites
 *
 * Phase 1: Fix author schema (Organization → Person), update dateModified,
 *          add related-posts links inside each blog post
 * Phase 2: Add "From Our Blog" section to service pages (creates internal links)
 * Phase 3: Expand short posts (<1400w) to 1600+ words via Claude API
 *
 * Usage:
 *   node blog-upgrade.js                    — all phases, all sites
 *   node blog-upgrade.js --phase 1          — structure fixes only
 *   node blog-upgrade.js --phase 2          — service page links only
 *   node blog-upgrade.js --phase 3          — expand short posts (Claude API)
 *   node blog-upgrade.js --site nar         — one site only
 *   node blog-upgrade.js --dry-run          — preview without writing
 */

const fs      = require('fs');
const path    = require('path');
const https   = require('https');
// Load .env manually
try {
  const envLines = fs.readFileSync('C:/NikaApplianceRepair/.env', 'utf8').split('\n');
  for (const line of envLines) {
    const m = line.match(/^([A-Z_]+)=(.+)$/);
    if (m) process.env[m[1]] = m[2].trim();
  }
} catch (e) {}

const PHASE   = (() => { const i = process.argv.indexOf('--phase'); return i !== -1 ? parseInt(process.argv[i+1]) : 0; })();
const SITE_ARG = (() => { const i = process.argv.indexOf('--site'); return i !== -1 ? process.argv[i+1] : null; })();
const DRY     = process.argv.includes('--dry-run');
const TODAY   = '2026-03-07';

const SITES = {
  nar: {
    dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com',
    name: 'N Appliance Repair', phone: '(437) 524-1053', phoneRaw: '+14375241053',
    author: { name: 'Nick Petrenko', title: 'Head Technician, N Appliance Repair', since: '2017', city: 'Toronto' },
  },
  neary: {
    dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com',
    name: 'Appliance Repair Near You', phone: '(437) 524-1053', phoneRaw: '+14375241053',
    author: { name: 'Mike Petrov', title: 'Certified Appliance Technician', since: '2015', city: 'Toronto GTA' },
  },
  fixlify: {
    dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com',
    name: 'Fixlify Appliance Repair', phone: '(437) 524-1053', phoneRaw: '+14375241053',
    author: { name: 'Alex Semenov', title: 'Senior Appliance Repair Technician', since: '2016', city: 'Toronto' },
  },
};

// ── HELPERS ───────────────────────────────────────────────────────────────────

function wordCount(html) {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().split(' ').filter(w => w.length > 2).length;
}

function getBlogPosts(site) {
  const blogDir = path.join(site.dir, 'blog');
  if (!fs.existsSync(blogDir)) return [];
  return fs.readdirSync(blogDir)
    .filter(f => f.endsWith('.html') && f !== 'index.html' && !f.startsWith('_'))
    .map(f => {
      const html = fs.readFileSync(path.join(blogDir, f), 'utf8');
      const titleM = html.match(/<title[^>]*>([^<]+)<\/title>/i);
      const h1M = html.match(/<h1[^>]*>([^<]+)<\/h1>/i);
      const title = (h1M ? h1M[1] : titleM ? titleM[1] : f).replace(/<[^>]+>/g, '').trim();
      const words = wordCount(html);
      const slug = f.replace('.html', '');
      // Detect topics from slug
      const topics = detectTopics(slug);
      return { f, slug, title, words, topics, html, fpath: path.join(blogDir, f) };
    });
}

function detectTopics(slug) {
  const s = slug.toLowerCase();
  const topics = [];
  const SERVICES = ['dishwasher','fridge','washer','dryer','oven','stove','freezer','microwave'];
  const BRANDS = ['samsung','lg','whirlpool','bosch','frigidaire','kenmore','ge','maytag','kitchenaid','miele','electrolux'];
  for (const svc of SERVICES) if (s.includes(svc)) topics.push(svc);
  for (const brand of BRANDS) if (s.includes(brand)) topics.push(brand);
  if (topics.length === 0) topics.push('general');
  return topics;
}

// ── PHASE 1: Fix author schema + inter-blog links ─────────────────────────────

function phase1AuthorAndInterlinks(site, posts) {
  console.log('\n[PHASE 1] ' + site.dir.split('/').pop() + ' — fix author schema + inter-blog links');
  let fixed = 0;

  for (const post of posts) {
    let html = post.html;

    // 1a. Fix author schema: Organization → Person
    const personSchema = JSON.stringify({
      '@type': 'Person',
      name: site.author.name,
      jobTitle: site.author.title,
      description: `Appliance repair technician in ${site.author.city} since ${site.author.since}. Specializes in all major brands.`,
    });
    html = html.replace(/"author":\{"@type":"Organization"[^}]+\}/, '"author":' + personSchema);
    html = html.replace(/"author":\s*\{\s*"@type":\s*"Organization"[^}]+\}/, '"author":' + personSchema);

    // 1b. Update dateModified
    html = html.replace(/"dateModified":"[^"]*"/, '"dateModified":"' + TODAY + '"');

    // 1c. Add author E-E-A-T bio box after article-meta if not present
    if (!html.includes('author-bio') && html.includes('article-meta')) {
      const bioCss = `<style>.author-bio{display:flex;align-items:flex-start;gap:16px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:16px 20px;margin:0 0 32px;}.author-bio .avatar{width:48px;height:48px;border-radius:50%;background:#2563EB;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:1.125rem;flex-shrink:0;}.author-bio .bio-text p{margin:0;font-size:0.875rem;color:#475569;line-height:1.5;}.author-bio .bio-text strong{color:#0F172A;font-size:0.9375rem;display:block;margin-bottom:2px;}</style>`;
      const bioHtml = `<div class="author-bio"><div class="avatar">${site.author.name.charAt(0)}</div><div class="bio-text"><strong>${site.author.name} — ${site.author.title}</strong><p>Appliance repair technician in ${site.author.city} since ${site.author.since}. Trained on all major brands — Samsung, LG, Whirlpool, Bosch, GE and more. 4.9★ rated across 300+ reviews.</p></div></div>`;
      html = html.replace(/(<\/header>)/, '$1\n' + bioCss + '\n' + bioHtml);
    }

    // 1d. Add related blog posts section (before FAQ or before </article>)
    if (!html.includes('related-blog-posts')) {
      const related = posts
        .filter(p => p.slug !== post.slug && p.topics.some(t => post.topics.includes(t)))
        .slice(0, 3);

      if (related.length >= 2) {
        const relatedHtml = `<div class="related-blog-posts" style="background:#F0F7FF;border:1px solid #BFDBFE;border-radius:8px;padding:20px 24px;margin:40px 0;">
<p style="font-size:0.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#2563EB;margin:0 0 12px;">Related Articles</p>
<ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
${related.map(r => `<li><a href="/blog/${r.slug}" style="color:#1D4ED8;font-weight:600;font-size:0.9375rem;">→ ${r.title}</a></li>`).join('\n')}
</ul>
</div>`;
        // Insert before FAQ section or before </article>
        if (html.includes('class="faq-section"')) {
          html = html.replace('class="faq-section"', 'RELATED_INSERTED class="faq-section"');
          html = html.replace('RELATED_INSERTED ', relatedHtml + '\n');
        } else {
          html = html.replace('</article>', relatedHtml + '\n</article>');
        }
      }
    }

    if (!DRY && html !== post.html) {
      fs.writeFileSync(post.fpath, html, 'utf8');
      fixed++;
    } else if (DRY && html !== post.html) {
      console.log('  [DRY] Would fix: ' + post.slug);
      fixed++;
    }
  }

  console.log('  Fixed: ' + fixed + ' posts');
  return fixed;
}

// ── PHASE 2: Add "From Our Blog" section to service pages ─────────────────────

function phase2ServicePageLinks(site, posts) {
  console.log('\n[PHASE 2] ' + site.dir.split('/').pop() + ' — add blog links to service pages');

  // Build topic → posts map
  const topicPosts = {};
  for (const post of posts) {
    for (const topic of post.topics) {
      if (!topicPosts[topic]) topicPosts[topic] = [];
      topicPosts[topic].push(post);
    }
  }

  // Get main service pages (not city pages, not brand pages)
  const SERVICES = ['dishwasher','fridge','washer','dryer','oven','stove'];
  const BRANDS = ['samsung','lg','whirlpool','bosch','frigidaire','kenmore','ge','maytag','kitchenaid','miele'];

  const serviceFiles = fs.readdirSync(site.dir)
    .filter(f => f.endsWith('.html'))
    .filter(f => {
      const s = f.replace('.html','').toLowerCase();
      // Include: main service pages + brand pages + brand-service pages
      const hasSvc = SERVICES.some(svc => s === svc + '-repair');
      const hasBrand = BRANDS.some(b => s === b + '-repair' || s === b);
      const hasBrandSvc = BRANDS.some(b => SERVICES.some(svc => s === b + '-' + svc + '-repair'));
      // Also include service+city pages for major cities only
      const isMajorCity = ['toronto','scarborough','north-york','etobicoke','mississauga','brampton'].some(c => s.endsWith('-' + c));
      const isSvcCity = SERVICES.some(svc => s.startsWith(svc + '-repair-')) && isMajorCity;
      return hasSvc || hasBrand || hasBrandSvc || isSvcCity;
    });

  let pagesFixed = 0, linksAdded = 0;

  for (const f of serviceFiles) {
    const fpath = path.join(site.dir, f);
    let html = fs.readFileSync(fpath, 'utf8');

    // Skip if already has blog links
    if (html.includes('href="/blog/') || html.includes("href='/blog/")) continue;

    const slug = f.replace('.html', '').toLowerCase();

    // Find relevant blog posts
    const topics = detectTopics(slug);
    let relevant = [];
    for (const t of topics) {
      if (topicPosts[t]) relevant.push(...topicPosts[t]);
    }
    // Add 1-2 general posts if needed
    if (topicPosts['general']) relevant.push(...topicPosts['general'].slice(0,1));

    // Deduplicate and limit to 3
    const seen = new Set();
    relevant = relevant.filter(p => { if (seen.has(p.slug)) return false; seen.add(p.slug); return true; }).slice(0, 3);

    if (relevant.length < 2) continue;

    const blogSection = `
<section class="from-our-blog" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:24px 28px;margin:32px auto;max-width:900px;">
  <p style="font-size:0.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#2563EB;margin:0 0 14px;">From Our Blog</p>
  <div style="display:flex;flex-direction:column;gap:10px;">
${relevant.map(p => `    <a href="/blog/${p.slug}" style="color:#1D4ED8;font-weight:600;font-size:0.9375rem;text-decoration:none;display:flex;align-items:center;gap:8px;"><span style="color:#2563EB">→</span> ${p.title}</a>`).join('\n')}
  </div>
</section>`;

    // Insert before FAQ section or before </main>
    if (html.includes('class="faq-section"') || html.includes('id="faq"')) {
      html = html.replace(/(<(?:section|div)[^>]*(?:class|id)="faq[^"]*"[^>]*>)/, blogSection + '\n$1');
    } else if (html.includes('</main>')) {
      html = html.replace('</main>', blogSection + '\n</main>');
    } else {
      html = html.replace('</body>', blogSection + '\n</body>');
    }

    if (!DRY) {
      fs.writeFileSync(fpath, html, 'utf8');
    }
    pagesFixed++;
    linksAdded += relevant.length;
  }

  console.log('  Service pages updated: ' + pagesFixed);
  console.log('  Blog links added: ' + linksAdded);
  return pagesFixed;
}

// ── PHASE 3: Expand short posts via Claude API ────────────────────────────────

function callClaude(prompt, maxTokens = 1200) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: maxTokens,
      messages: [{ role: 'user', content: prompt }],
    });

    const req = https.request({
      hostname: 'api.anthropic.com',
      path: '/v1/messages',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Length': Buffer.byteLength(body),
      },
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          if (j.content && j.content[0]) resolve(j.content[0].text);
          else reject(new Error('No content: ' + data.slice(0, 200)));
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function expandPost(post, site) {
  const currentWords = post.words;
  const needed = Math.max(400, 1600 - currentWords);

  // Extract existing H2 headings to avoid duplication
  const existingH2 = (post.html.match(/<h2[^>]*>([^<]+)<\/h2>/gi) || [])
    .map(h => h.replace(/<[^>]+>/g, '').trim());

  const prompt = `You are a certified appliance repair technician writing for a local service business blog.

Write a new H2 section (~${needed} words) for this blog post. Add REAL, practical value.

POST TOPIC: ${post.title}
BUSINESS: ${site.name} — ${site.author.city}, since ${site.author.since}
AUTHOR: ${site.author.name}, ${site.author.title}

EXISTING H2 sections (DO NOT repeat these topics):
${existingH2.map(h => '- ' + h).join('\n')}

Requirements:
- Write exactly ONE new H2 section with 3-4 sub-points or H3 subsections
- Use real technician experience: "In our experience...", "We've seen...", "When we repaired..."
- Include specific, helpful technical details (symptoms, causes, costs, DIY tips)
- Mention Toronto/GTA if relevant
- End with a brief CTA (call (437) 524-1053)
- Format: start with <h2>Heading</h2> then content paragraphs
- NO markdown, only clean HTML tags (h2, h3, p, ul, li, strong)
- Target: ${needed} words of useful content

Write the HTML section now (no explanation, just the HTML):`;

  const content = await callClaude(prompt, 1500);
  return content.trim();
}

async function phase3ExpandPosts(site, posts) {
  console.log('\n[PHASE 3] ' + site.dir.split('/').pop() + ' — expand short posts via Claude API');

  const shortPosts = posts.filter(p => p.words < 1450).sort((a, b) => a.words - b.words);
  console.log('  Short posts to expand: ' + shortPosts.length);

  if (!process.env.ANTHROPIC_API_KEY) {
    console.log('  ERROR: ANTHROPIC_API_KEY not set in .env');
    return 0;
  }

  let expanded = 0;

  for (const post of shortPosts) {
    process.stdout.write('  [' + post.slug.slice(0, 40) + '] ' + post.words + 'w → ');

    let newSection;
    try {
      newSection = await expandPost(post, site);
    } catch (e) {
      console.log('ERROR: ' + e.message.slice(0, 60));
      continue;
    }

    // Insert before FAQ section or before </article>
    let html = post.html;
    const insertBefore = html.includes('class="faq-section"') ? 'class="faq-section"' :
                         html.includes('class="related-blog-posts"') ? 'class="related-blog-posts"' :
                         '</article>';

    html = html.replace(insertBefore, newSection + '\n' + insertBefore);

    const newWords = wordCount(html);
    console.log(newWords + 'w (+' + (newWords - post.words) + ')');

    if (!DRY) {
      fs.writeFileSync(post.fpath, html, 'utf8');
      expanded++;
    }

    // Small delay to avoid rate limits
    await new Promise(r => setTimeout(r, 500));
  }

  console.log('  Expanded: ' + expanded + ' posts');
  return expanded;
}

// ── ALSO: Fix blog/index.html to show all posts ───────────────────────────────

function fixBlogIndex(site, posts) {
  const indexPath = path.join(site.dir, 'blog', 'index.html');
  if (!fs.existsSync(indexPath)) return;

  let html = fs.readFileSync(indexPath, 'utf8');

  // Check if links are extensionless (missing .html)
  const hasExtensionlessLinks = posts.some(p => html.includes('href="/blog/' + p.slug + '"'));
  const hasHtmlLinks = posts.some(p => html.includes('href="/blog/' + p.slug + '.html"'));

  // Add missing posts to blog index
  const missingPosts = posts.filter(p => !html.includes(p.slug));
  if (missingPosts.length > 0) {
    console.log('  Blog index missing ' + missingPosts.length + ' posts — adding cards');
    const newCards = missingPosts.map(p => {
      const topics = p.topics.filter(t => t !== 'general');
      const tag = topics.length > 0 ? topics[0].charAt(0).toUpperCase() + topics[0].slice(1) + ' Repair' : 'Appliance Repair';
      const excerpt = p.title; // Simple excerpt from title
      return `<article class="post-card">
  <div class="post-card-stripe"></div>
  <div class="post-card-header">
    <div class="post-tag">${tag}</div>
    <h2><a href="/blog/${p.slug}">${p.title}</a></h2>
  </div>
  <div class="post-card-body">
    <p class="post-excerpt">Read our complete guide on ${p.title.toLowerCase()}.</p>
  </div>
  <div class="post-card-footer">
    <span class="post-date">${TODAY}</span>
    <a href="/blog/${p.slug}" class="read-more">Read More →</a>
  </div>
</article>`;
    }).join('\n');

    // Insert before closing </div> of posts-grid
    html = html.replace('</div>\n</section>', newCards + '\n</div>\n</section>');
  }

  if (!DRY) fs.writeFileSync(indexPath, html, 'utf8');
}

// ── MAIN ──────────────────────────────────────────────────────────────────────

(async () => {
  const sitesToProcess = SITE_ARG ? [[SITE_ARG, SITES[SITE_ARG]]] : Object.entries(SITES);

  for (const [key, site] of sitesToProcess) {
    if (!site) { console.log('Unknown site: ' + key); continue; }
    console.log('\n' + '═'.repeat(50));
    console.log(key.toUpperCase() + ' — ' + site.domain);
    console.log('═'.repeat(50));

    const posts = getBlogPosts(site);
    console.log('Blog posts found: ' + posts.length);
    if (posts.length === 0) continue;

    // Fix blog index
    if (!PHASE || PHASE === 1) {
      fixBlogIndex(site, posts);
    }

    // Phase 1: Author + inter-blog links
    if (!PHASE || PHASE === 1) {
      phase1AuthorAndInterlinks(site, posts);
    }

    // Phase 2: Service page → blog links
    if (!PHASE || PHASE === 2) {
      phase2ServicePageLinks(site, posts);
    }

    // Phase 3: Expand short posts (async, Claude API)
    if (!PHASE || PHASE === 3) {
      await phase3ExpandPosts(site, posts);
    }
  }

  console.log('\n✓ Done. Review changes and commit.');
})();
