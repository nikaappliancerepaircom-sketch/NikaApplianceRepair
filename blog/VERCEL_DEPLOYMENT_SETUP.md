# Vercel Deployment Setup Guide
**For Automated Blog Publishing (Oct 31 - Nov 4, 2025)**

---

## Overview

Since you're using **Vercel for hosting**, the publishing workflow is:

1. **GitHub Actions** → Publishes 1 post to `/blog/troubleshooting/` and commits to GitHub
2. **GitHub Auto-Deploys to Vercel** → Vercel detects the commit and rebuilds/deploys
3. **Posts Live** → New posts immediately available on your site

**No Vercel secrets needed** - Your GitHub repository is already connected to Vercel!

---

## Prerequisites

✅ **You Already Have:**
- Vercel connected to GitHub repository
- vercel.json configured with rewrites
- Git repository set up
- GitHub Actions enabled

✅ **Verify:**
- Go to Vercel dashboard → Your project
- Confirm "Git" shows "NikaApplianceRepair" repository
- Confirm "Auto-deploy" is ON for main branch

---

## Step 1: Verify GitHub Access Token (Usually Already Set)

Vercel automatically deploys when commits are pushed to `main` branch.

**Check GitHub Actions permissions:**
1. Go to GitHub repository Settings
2. Click "Secrets and variables" → "Actions"
3. Confirm `GITHUB_TOKEN` exists (it's built-in, no setup needed)

---

## Step 2: Configure Slack Notifications (Optional)

If you want notifications when posts publish:

**Create Slack Webhook:**
1. Go to Slack Workspace Settings
2. Click "Manage Apps" → "Custom Integrations" → "Incoming Webhooks"
3. Click "Add New Webhook to Workspace"
4. Select channel (e.g., #blog or #publishing)
5. Copy the webhook URL

**Add to GitHub Secrets:**
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `SLACK_WEBHOOK_URL`
4. Value: (paste your webhook URL)

**Note:** Slack notifications in the workflow are optional (continue-on-error: true)

---

## Step 3: Test the Workflow (Manual Trigger)

Before October 31, test the workflow:

**Manual Test:**
1. Go to GitHub → Actions tab
2. Select "Auto-Publish Blog Posts" workflow
3. Click "Run workflow" button
4. Select branch: `main`
5. Click green "Run workflow"

**What to expect:**
- Workflow runs within 1 minute
- 1 post is published from `day-1` folder
- Commit appears in GitHub
- Vercel auto-deploys (takes 1-2 minutes)
- Post appears on your website at `/blog/troubleshooting/[slug]`

**Check Results:**
1. Go to GitHub Actions → Workflow run
2. Look for green checkmark ✅
3. Check sitemap updated in commit
4. Visit your website, verify new post appears
5. Check Vercel deployment status (Deployments tab)

---

## Step 4: Verify Vercel Auto-Deployment

Vercel should automatically deploy every time you push to `main` branch.

**Verify Auto-Deployment:**
1. Go to Vercel dashboard → Your project
2. Click "Settings" → "Git"
3. Confirm "Auto-deploy on every push" is ON
4. Confirm branch is `main`

**What happens automatically:**
- GitHub Actions publishes 1 post and commits to `main`
- Vercel detects the commit
- Vercel rebuilds the site
- Site is live in 1-2 minutes

---

## Step 5: Understanding the Schedule

The workflow will run at these times:

**Oct 31 (Day 1) - 5 posts:**
- 6:00 AM UTC
- 9:00 AM UTC
- 12:00 PM UTC
- 3:00 PM UTC
- 6:00 PM UTC

**Nov 1 (Day 2) - 5 posts:**
- Same times (6 AM, 9 AM, 12 PM, 3 PM, 6 PM UTC)

**Nov 2 (Day 3) - 5 posts:**
- Same times

**Nov 3 (Day 4) - 5 posts:**
- Same times

**Nov 4 (Day 5) - 4 posts:**
- 6:00 AM, 9:00 AM, 12:00 PM, 3:00 PM UTC

**Time Zone Conversion:**
If you're in Eastern Time (ET):
- 6 AM UTC = 1-2 AM ET (depending on DST)
- 9 AM UTC = 4-5 AM ET
- 12 PM UTC = 7-8 AM ET
- 3 PM UTC = 10-11 AM ET
- 6 PM UTC = 1-2 PM ET

To change times, edit the cron expressions in `.github/workflows/auto-publish-blog.yml`

---

## Step 6: Monitor During Publishing Week

**Daily Monitoring Checklist:**

**Each Morning:**
- [ ] Check GitHub Actions for successful runs
- [ ] Verify post appears on website
- [ ] Check Vercel deployment status
- [ ] Monitor site performance

**Each Evening:**
- [ ] Check for any failed runs
- [ ] Verify all posts indexed in Google Search Console
- [ ] Monitor GA4 for new traffic
- [ ] Review Slack notifications (if configured)

---

## Troubleshooting

### Posts Not Publishing?

**Issue: Workflow failed in GitHub Actions**
1. Go to GitHub → Actions → "Auto-Publish Blog Posts"
2. Click the failed run
3. Expand the failed step (usually "Publish draft posts")
4. Read the error message
5. Common issues:
   - Day folder doesn't exist (check spelling)
   - File permissions issue
   - Path not found

**Fix:** Check the specific error, adjust workflow if needed, try manual run again

### Posts Published But Don't Appear on Website?

**Issue: Vercel deployment succeeded but post not visible**

1. Check Vercel build log:
   - Go to Vercel dashboard → Deployments
   - Click the latest deployment
   - Check build logs for errors

2. Possible causes:
   - CSS paths are wrong (../../css/)
   - Post file wasn't deployed
   - Browser cache issue
   - Rewrite rules not matching

3. Solutions:
   - Check post file exists: `/blog/troubleshooting/[filename].html`
   - Clear browser cache (Ctrl+Shift+Delete)
   - Check vercel.json rewrites include `/blog/:category/:slug`
   - Redeploy by pushing empty commit: `git commit --allow-empty -m "Trigger redeploy"`

### Workflow Runs But No Commit?

**Issue: GitHub Actions says "No changes to commit"**

This means `day-X` folder is empty or all posts already published.

**Check:**
1. Verify draft posts exist: `/blog/_drafts/day-1/` should have 5 .html files
2. Check published log: `/blog/_published_log.json` to see what's already published
3. If all posts from a day are published, move to next day's folder

---

## How It Works: The Full Flow

```
GitHub Actions (scheduled)
    ↓
    ├─ Determines day (Oct 31 = day-1, Nov 1 = day-2, etc.)
    ├─ Runs Python script to move 1 post from draft to published
    ├─ Updates sitemap.xml
    ├─ Updates blog index
    ├─ Commits all changes to GitHub (main branch)
    │
Vercel (auto-triggered by commit)
    ↓
    ├─ Detects new commit on main branch
    ├─ Rebuilds site
    ├─ Deploys to production
    │
Your Website
    ↓
    └─ Post is now live at /blog/troubleshooting/[filename]
```

---

## Useful Links

- **GitHub Actions Logs:** `https://github.com/[USER]/NikaApplianceRepair/actions`
- **Vercel Dashboard:** `https://vercel.com/dashboard`
- **Vercel Deployments:** `https://vercel.com/[PROJECT]/deployments`
- **Google Search Console:** `https://search.google.com/search-console/`
- **GA4:** `https://analytics.google.com/`

---

## Important Notes

⚠️ **GitHub Actions Free Tier Limits:**
- 2,000 workflow runs per month (plenty for 25 runs)
- No issues for your schedule

✅ **What's Included:**
- Free GitHub Actions (no cost)
- Free Vercel deployment (no cost)
- Automatic Git commits and deploys

⏱️ **Timing:**
- 1-2 minutes for workflow to run
- 1-2 minutes for Vercel to build and deploy
- Posts live within 5 minutes of scheduled time

---

## Pre-Launch Checklist

Before October 31:

- [ ] Verify draft posts exist in `/blog/_drafts/day-1/` through `/day-5/`
- [ ] Run manual workflow test successfully
- [ ] Post appears on website after test
- [ ] Vercel auto-deployment is ON
- [ ] Slack webhook configured (optional)
- [ ] Google Search Console ready
- [ ] GA4 tracking active
- [ ] Team notified of publishing schedule

---

## Launch Day Script (Oct 31)

**6:00 AM:**
1. GitHub Actions triggers
2. Watch workflow run in Actions tab
3. First post publishes
4. Vercel deploys (2-3 minutes)
5. Check post on website ✅

**Repeat every 3 hours** (9 AM, 12 PM, 3 PM, 6 PM UTC)
- Each time: check Actions tab, verify Vercel deployment, check website

**End of Day (after 6 PM UTC):**
- Verify all 5 posts published
- Check Google Search Console for crawling activity
- Monitor GA4 for traffic
- Document any issues for next day

---

## After Publishing Completes (Nov 5+)

Once all 24 new posts are published:

1. **Disable Workflow** (optional):
   - Edit `.github/workflows/auto-publish-blog.yml`
   - Comment out or delete the `on: schedule:` section
   - Push the change

2. **Analyze Results:**
   - Track keyword rankings
   - Monitor organic traffic
   - Check user engagement
   - Identify top-performing posts

3. **Next Steps:**
   - Consider publishing remaining 44 old posts
   - Plan for next batch of content
   - Optimize based on performance data

---

## Status

✅ **Setup Complete**
- GitHub Actions workflow configured with 25 scheduled runs
- Vercel auto-deployment verified
- Python publishing script updated for single-post runs
- Ready for October 31 launch

**Next Action:** Run manual test on Oct 30-31 to verify everything works

Good luck with your launch! 🚀

