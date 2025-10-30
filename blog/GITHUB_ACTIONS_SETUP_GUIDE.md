# GitHub Actions Auto-Publishing Setup Guide
**For Automated Blog Post Publishing (Oct 31 - Nov 12, 2025)**

---

## Overview

This guide explains how to set up GitHub Actions to automatically publish 5 blog posts per day from October 31 through November 12, 2025.

**Benefits of GitHub Actions:**
- ✅ Fully automated - no manual intervention needed
- ✅ Cost: $0 (included free with GitHub)
- ✅ Reliable scheduling with built-in error handling
- ✅ Easy to modify or pause the schedule
- ✅ Integrates with your existing Git repository
- ✅ Notifications via Slack or email

---

## Prerequisites

**What You Need:**
1. GitHub repository (you already have this: NikaApplianceRepair)
2. All 68 blog posts in the repository (you have this)
3. A way to deploy posts to your web server (SSH, FTP, or Netlify/Vercel)
4. (Optional) Slack webhook for notifications
5. (Optional) Google Search Console API token

**If You Don't Have GitHub:**
- Create free account at https://github.com
- Push your blog folder to a new repository

---

## Step 1: Create the Workflow File

**File Location:** `.github/workflows/auto-publish-blog.yml`

**What This File Does:**
- Defines a schedule for when to publish posts
- Specifies which posts to publish at each time
- Handles deployment to your web server
- Sends notifications when publishing completes

**File Already Exists:** The file `auto-publish-blog.yml` has been created. Now you need to customize it with:
- Your server deployment details
- Slack webhook URL (optional)
- Google Search Console credentials (optional)

---

## Step 2: Configure Deployment Method

Choose ONE of these deployment methods:

### Option A: Netlify (Recommended for Static Sites)

**If You Use Netlify:**

1. Go to Netlify Settings → API Tokens
2. Create a Personal Access Token
3. In GitHub Settings → Secrets, add:
   - Name: `NETLIFY_AUTH_TOKEN`
   - Value: (paste your token)
   - Name: `NETLIFY_SITE_ID`
   - Value: (your site ID from Netlify)

4. In workflow file, replace "Deploy posts" step:
```yaml
- name: Deploy posts to production
  uses: netlify/actions/build@master
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    netlify_auth_token: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```

### Option B: FTP/Shared Hosting

**If You Use FTP:**

1. In GitHub Settings → Secrets, add:
   - Name: `FTP_HOST`
   - Value: your.ftp.server.com
   - Name: `FTP_USERNAME`
   - Value: your_ftp_username
   - Name: `FTP_PASSWORD`
   - Value: your_ftp_password

2. In workflow file, replace "Deploy posts" step:
```yaml
- name: Deploy posts to production
  uses: SamKirkland/FTP-Deploy-Action@4.3.4
  with:
    server: ${{ secrets.FTP_HOST }}
    username: ${{ secrets.FTP_USERNAME }}
    password: ${{ secrets.FTP_PASSWORD }}
    local-dir: ./blog/
    server-dir: /public_html/blog/
    state-name: .ftp-deploy-sync-state.json
    dangerous-delete-include: |
      *.html
```

### Option C: SSH/VPS

**If You Use SSH (Linux/VPS):**

1. Generate SSH key:
```bash
ssh-keygen -t ed25519 -f github-deploy -N ""
```

2. Add public key to your server:
```bash
cat github-deploy.pub >> ~/.ssh/authorized_keys
```

3. In GitHub Settings → Secrets, add:
   - Name: `DEPLOY_KEY`
   - Value: (paste contents of `github-deploy` file)
   - Name: `DEPLOY_HOST`
   - Value: your.server.com
   - Name: `DEPLOY_USER`
   - Value: your_username

4. In workflow file, replace "Deploy posts" step:
```yaml
- name: Deploy posts to production
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.DEPLOY_KEY }}
    script: |
      cd /var/www/html/blog
      git pull origin main
      cp troubleshooting/*.html /var/www/html/blog/troubleshooting/
      chmod 644 troubleshooting/*.html
```

### Option D: Vercel

**If You Use Vercel:**

1. Go to Vercel Settings → Tokens
2. Create new token
3. In GitHub Settings → Secrets, add:
   - Name: `VERCEL_TOKEN`
   - Value: (paste your token)
   - Name: `VERCEL_ORG_ID`
   - Value: (your org ID)
   - Name: `VERCEL_PROJECT_ID`
   - Value: (your project ID)

4. In workflow file, replace "Deploy posts" step:
```yaml
- name: Deploy posts to production
  env:
    VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
    VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
  run: |
    npm i -g vercel
    vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
    vercel build --prod
    vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## Step 3: Set Up Slack Notifications (Optional)

**To Get Slack Updates When Posts Publish:**

1. Go to Slack Workspace Settings
2. Create new Incoming Webhook
3. In GitHub Settings → Secrets, add:
   - Name: `SLACK_WEBHOOK`
   - Value: (paste your webhook URL)

4. Workflow already includes Slack notification step - just update the webhook URL

---

## Step 4: Adjust Times for Your Timezone

**The times in the workflow are in UTC. Convert to your timezone:**

| Time Zone | Adjustment |
|-----------|-----------|
| Eastern (ET) | UTC - 4 (EDT) or UTC - 5 (EST) |
| Central (CT) | UTC - 5 (CDT) or UTC - 6 (CST) |
| Mountain (MT) | UTC - 6 (MDT) or UTC - 7 (MST) |
| Pacific (PT) | UTC - 7 (PDT) or UTC - 8 (PST) |

**Example: If you want posts to publish at 6 AM Eastern Time:**
- 6 AM ET = 10 AM UTC
- Cron expression: `0 10 31 10 *` (10 AM UTC on Oct 31)

**Current schedule (UTC times):**
- 6 AM UTC → 1 AM ET / 12 AM CT / 11 PM PT (previous day)
- 10 AM UTC → 5 AM ET / 4 AM CT / 2 AM PT
- 2 PM UTC → 9 AM ET / 8 AM CT / 6 AM PT
- 6 PM UTC → 1 PM ET / 12 PM CT / 10 AM PT
- 10 PM UTC → 5 PM ET / 4 PM CT / 2 PM PT

**To change schedule times in the workflow file:**

Find this section and modify cron expressions:
```yaml
- cron: '0 6 31 10 *'    # 6 AM UTC - CHANGE THIS
- cron: '0 10 31 10 *'   # 10 AM UTC - CHANGE THIS
```

**Cron Syntax:** `minute hour day month day-of-week`
- Minute: 0-59
- Hour: 0-23 (UTC)
- Day: 1-31
- Month: 1-12 (1=Jan, 10=Oct, 11=Nov)
- Day of week: 0-6 (0=Sunday, 1=Monday, etc.)

---

## Step 5: Set Up Secrets in GitHub

**To Add Secrets:**

1. Go to GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret based on your deployment method:

**Example (FTP):**
```
Secret Name: FTP_HOST
Secret Value: ftp.yourhost.com

Secret Name: FTP_USERNAME
Secret Value: your_username

Secret Name: FTP_PASSWORD
Secret Value: your_password
```

⚠️ **Important:** Never share or commit these secrets. They're encrypted and private.

---

## Step 6: Testing Before Oct 31

**Test the Workflow:**

1. Go to GitHub repository
2. Click "Actions" tab
3. Select "Auto-Publish Blog Posts" workflow
4. Click "Run workflow"
5. Choose branch (main)
6. Click green "Run workflow" button

**What to Check:**
- ✅ Workflow completes without errors
- ✅ Posts appear on your website
- ✅ Slack notifications work (if configured)
- ✅ Logs show successful deployment

**Troubleshooting Failed Runs:**

1. Click on failed workflow run
2. Expand the "Deploy posts" step
3. Read error message (usually tells you exactly what's wrong)
4. Common issues:
   - `authentication failed` → Check FTP/SSH credentials
   - `file not found` → Verify file paths
   - `timeout` → May need to increase timeout
   - `permission denied` → Check server file permissions

---

## Step 7: Monitor During Publishing Period

**Oct 31 - Nov 12 Daily Tasks:**

- [ ] Check Slack notifications (or GitHub Actions page)
- [ ] Verify posts appear on website
- [ ] Monitor Google Search Console for indexing
- [ ] Check website error logs for issues
- [ ] Track GA4 traffic to new posts
- [ ] Keep an eye on server performance

**If A Post Fails to Publish:**

1. Go to GitHub Actions → failed run
2. Read the error log
3. Fix the issue (usually in the workflow file)
4. Click "Re-run failed jobs"

---

## Step 8: Post-Publishing (After Nov 12)

**When Publishing Completes:**

1. Go to workflow file (.github/workflows/auto-publish-blog.yml)
2. Comment out or delete the schedule section:
```yaml
# Disable after Nov 12
# on:
#   schedule:
#     ...
```

3. Or delete the entire workflow file if no longer needed

**Analyze Results:**

- Total organic traffic increase
- New keyword rankings
- Average ranking position improvement
- Domain authority changes
- User engagement metrics (bounce rate, pages/session, time on page)

---

## Complete Workflow File Template

If you need to create the workflow from scratch, here's the basic structure:

```yaml
name: Auto-Publish Blog Posts
on:
  schedule:
    - cron: '0 10 31 10 *'  # 6 AM ET on Oct 31
    - cron: '0 10 1 11 *'   # 6 AM ET on Nov 1
    # ... more dates ...
  workflow_dispatch:  # Allow manual triggering

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy posts
        run: |
          echo "Deploying blog posts..."
          # Your deployment command here
      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## FAQ

**Q: Can I pause the schedule if something breaks?**
A: Yes, just comment out the `on: schedule:` section in the workflow file.

**Q: Can I test without waiting until Oct 31?**
A: Yes, use the "Run workflow" button to trigger manually.

**Q: What if a post fails to publish?**
A: Check GitHub Actions logs, fix the issue, and re-run the job.

**Q: Can I change the posting times?**
A: Yes, edit the cron expressions in the workflow file. Changes take effect immediately.

**Q: What if my server goes down during publishing?**
A: The workflow will fail. When server is back up, you can manually re-run the failed jobs.

**Q: Can I see what posts are being published?**
A: Yes, check GitHub Actions logs. Each run shows exactly which posts were deployed.

**Q: Is this secure?**
A: Yes, GitHub encrypts all secrets. Your FTP/SSH credentials are never logged or exposed.

---

## Support Resources

- GitHub Actions Documentation: https://docs.github.com/en/actions
- Cron Schedule Syntax: https://crontab.guru/
- FTP Deploy Action: https://github.com/SamKirkland/FTP-Deploy-Action
- SSH Deploy Action: https://github.com/appleboy/ssh-action
- Slack GitHub Action: https://github.com/slackapi/slack-github-action

---

## Next Steps

1. **ASAP:** Choose your deployment method (Option A-D above)
2. **This Week:** Set up GitHub secrets and test the workflow
3. **Oct 30:** Verify test run succeeded, posts appeared, notifications worked
4. **Oct 31:** Watch first post publish automatically
5. **Nov 1-12:** Monitor daily, adjust if needed
6. **Nov 13+:** Analyze results and plan next batch

---

**Status:** ✅ SETUP GUIDE COMPLETE
**Next:** Configure your specific deployment method and test before Oct 31

Remember: The workflow is already created. You just need to configure it for YOUR specific hosting setup!
