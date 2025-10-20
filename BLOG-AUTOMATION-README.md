# Blog Automation System - Complete Guide

## Overview

This automation system publishes 5 blog posts per day from your drafts folder, automatically updates the sitemap.xml, and refreshes the blog index page.

## 📁 Directory Structure

```
NikaApplianceRepair/
├── blog/
│   ├── _drafts/           ← Place unpublished posts here
│   ├── troubleshooting/   ← Auto-published posts go here
│   ├── maintenance/
│   ├── guides/
│   ├── seasonal/
│   ├── brands/
│   └── locations/
├── scripts/
│   ├── auto-publish-posts.py      ← Publishes 5 posts/day
│   ├── update-sitemap.py          ← Regenerates sitemap.xml
│   └── update-blog-index.py       ← Updates blog.html
└── .github/workflows/
    └── auto-publish-blog.yml      ← GitHub Actions (runs daily at 9 AM EST)
```

## 🚀 How It Works

### 1. GitHub Actions Workflow (Automated)

**When:** Runs automatically every day at 9:00 AM EST (2:00 PM UTC)

**What it does:**
1. Publishes 5 posts from `/blog/_drafts/` folder
2. Updates `sitemap.xml` with all pages and blog posts
3. Updates `blog.html` with new posts
4. Commits and pushes changes to GitHub
5. Vercel automatically deploys the changes

**Manual Trigger:**
You can also trigger the workflow manually from GitHub Actions tab.

### 2. Publishing Posts from Drafts

**Automatic (GitHub Actions):**
- GitHub Actions runs daily and publishes 5 posts automatically
- No manual intervention required

**Manual Publishing:**

```bash
# Publish 5 posts (default)
python scripts/auto-publish-posts.py

# Publish specific number of posts
python scripts/auto-publish-posts.py --count 10

# Dry run (preview without publishing)
python scripts/auto-publish-posts.py --dry-run --count 5

# Use custom drafts folder
python scripts/auto-publish-posts.py --drafts-folder blog/_custom_drafts
```

## 📝 Creating Blog Posts

### Step 1: Write Your Post

Use `BLOG-TEMPLATE.md` as your guide. Create an HTML file following the template structure.

**Required Elements:**
- Title, meta description, keywords
- Schema.org markup (Article, FAQPage, HowTo)
- Quick Answer Box (40-60 words)
- Table of Contents
- 5 DIY steps
- FAQ section (5-8 questions)
- Cost breakdown
- CTA buttons

### Step 2: Set Post Category

Add a meta tag or use the filename pattern to indicate category:

```html
<!-- Option 1: Meta tag -->
<meta name="category" content="troubleshooting">

<!-- Option 2: Filename pattern -->
<!-- Save as: 002-dishwasher-not-draining-toronto.html -->
```

**Available Categories:**
- `troubleshooting` - Problem-solving guides
- `maintenance` - Preventive care tips
- `guides` - How-to guides and tutorials
- `seasonal` - Seasonal maintenance
- `brands` - Brand-specific content
- `locations` - Location-specific content

### Step 3: Save to Drafts Folder

```bash
# Save your HTML file to:
blog/_drafts/your-post-name.html
```

**Naming Convention:**
- Use numbers for ordering: `001-post.html`, `002-post.html`
- Or use dates: `2025-01-20-post.html`
- Posts are published in alphabetical order

### Step 4: Publish

**Option A: Wait for automation** (recommended)
- GitHub Actions will publish 5 posts automatically every day at 9 AM EST
- Posts are published in alphabetical/numerical order

**Option B: Publish manually**
```bash
python scripts/auto-publish-posts.py --count 5
```

## 🗺️ Sitemap Updates

### Automatic Updates

The sitemap is automatically updated after publishing posts.

**What's included:**
- Homepage (priority: 1.0)
- Main pages (priority: 0.9)
- Location pages (priority: 0.8)
- Service pages (priority: 0.8)
- Brand pages (priority: 0.7)
- Blog posts (priority: 0.7)

### Manual Sitemap Generation

```bash
python scripts/update-sitemap.py
```

**Output:** `sitemap.xml` (53+ URLs)

### Submit to Search Engines

After publishing:
1. **Google Search Console:** Submit sitemap at `https://nikaappliancerepair.com/sitemap.xml`
2. **Bing Webmaster Tools:** Submit sitemap
3. **Yandex Webmaster:** Submit sitemap (optional)

## 📰 Blog Index Updates

### Automatic Updates

The blog index (`blog.html`) is automatically updated after publishing.

**Features:**
- Shows all published posts
- Newest posts first
- Category filtering
- Reading time estimate
- Featured post section

### Manual Index Update

```bash
python scripts/update-blog-index.py
```

## 🎯 Content Plan (100 Posts)

See `BLOG-CONTENT-PLAN-100.md` for the complete list of posts.

**Distribution:**
- 40 Troubleshooting posts
- 20 Maintenance posts
- 15 Cost & Pricing posts
- 15 Brand-specific posts
- 5 Seasonal posts
- 5 Location-specific posts

**Publishing Schedule:**
- 5 posts/day = 20 days to publish all 100 posts
- Consistent daily publishing signals freshness to Google

## 🔧 Scripts Reference

### 1. auto-publish-posts.py

Moves posts from drafts to category folders.

```bash
# Basic usage
python scripts/auto-publish-posts.py

# Options
--count 5              # Number of posts to publish (default: 5)
--dry-run             # Preview without publishing
--drafts-folder PATH  # Custom drafts folder (default: blog/_drafts)
```

**Output:**
- Moves HTML files from `blog/_drafts/` to appropriate category folders
- Logs published posts to `blog/_published_log.json`
- Prints summary of published posts

### 2. update-sitemap.py

Generates complete sitemap.xml for all pages.

```bash
python scripts/update-sitemap.py
```

**Output:**
- Creates/updates `sitemap.xml`
- Includes all pages and blog posts
- Sets appropriate priorities and changefreq

### 3. update-blog-index.py

Updates blog.html with all published posts.

```bash
python scripts/update-blog-index.py
```

**Output:**
- Updates `blog.html` posts grid
- Maintains category filters
- Preserves featured post section

## 📊 Monitoring & Logs

### Published Posts Log

Location: `blog/_published_log.json`

```json
[
  {
    "filename": "refrigerator-not-cooling-toronto.html",
    "title": "Why Is My Refrigerator Not Cooling?",
    "category": "troubleshooting",
    "date": "2025-01-20",
    "url": "/blog/troubleshooting/refrigerator-not-cooling-toronto"
  }
]
```

### GitHub Actions Log

1. Go to GitHub repository
2. Click "Actions" tab
3. Select "Auto-Publish Blog Posts" workflow
4. View execution logs

## 🎨 AI Optimization Features

All blog posts are optimized for:

### AI Search Platforms
- **ChatGPT:** Schema markup, clear Q&A format
- **Gemini:** Entity recognition (brands + locations)
- **Perplexity:** Citation-friendly structure
- **Google AI Overview:** Featured snippet optimization

### Voice Search
- **Siri/Alexa/Google Assistant:** Natural language questions
- **Quick Answer Box:** 40-60 word direct answers
- **FAQ Schema:** Structured Q&A for voice results

### Traditional SEO
- **Featured Snippets:** Quick Answer Boxes
- **People Also Ask:** FAQ section with schema
- **Rich Results:** Article, HowTo, FAQPage schemas
- **Internal Linking:** Cross-linking to services/locations

## 🚨 Troubleshooting

### No posts being published

**Check:**
1. Are there files in `blog/_drafts/`?
2. Are files named as `.html` files?
3. Run with `--dry-run` to see what would be published

```bash
python scripts/auto-publish-posts.py --dry-run
```

### Sitemap not updating

**Solution:**
```bash
# Manually regenerate sitemap
python scripts/update-sitemap.py

# Check if sitemap.xml was created
ls -la sitemap.xml
```

### Blog index not updating

**Solution:**
```bash
# Manually update blog index
python scripts/update-blog-index.py

# Verify blog.html has posts-grid section
grep "posts-grid" blog.html
```

### GitHub Actions failing

**Check:**
1. Repository permissions (Settings → Actions → General)
2. Workflow file syntax (`.github/workflows/auto-publish-blog.yml`)
3. Python version compatibility (script requires Python 3.11+)

## 📈 Performance Tips

### Batch Writing

**Write all 100 posts upfront:**
1. Create 100 HTML files using `BLOG-TEMPLATE.md`
2. Save all to `blog/_drafts/`
3. Name sequentially: `001-post.html` to `100-post.html`
4. Automation publishes 5/day for 20 days

**Benefits:**
- Consistent publishing schedule
- No manual intervention for 20 days
- Strong freshness signal to Google

### Content Quality

**Use AI to assist:**
1. ChatGPT/Claude for initial drafts
2. Human editing for accuracy
3. Local expertise (Toronto-specific details)
4. Brand-specific troubleshooting (real issues)

### SEO Optimization

**Key elements:**
- Focus keyword in title, H1, first paragraph
- Voice search queries in headings
- Local keywords (Toronto, GTA, specific cities)
- Brand names (Samsung, LG, Whirlpool, etc.)
- Problem + Location + Brand combinations

## 🎯 Next Steps

1. **Create 100 blog posts** using `BLOG-CONTENT-PLAN-100.md`
2. **Save to drafts folder:** `blog/_drafts/`
3. **Let automation run:** 5 posts/day for 20 days
4. **Monitor rankings:** Google Search Console, AI platforms
5. **Adjust strategy:** Based on performance data

## 📞 Support

- **GitHub Issues:** Report bugs or request features
- **Template:** Use `BLOG-TEMPLATE.md` for all posts
- **Content Plan:** Follow `BLOG-CONTENT-PLAN-100.md` for topics

---

**Last Updated:** January 20, 2025
**Version:** 1.0.0
**Automation Status:** ✅ Active (Daily at 9:00 AM EST)
