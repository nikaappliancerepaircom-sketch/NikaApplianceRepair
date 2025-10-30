# Launch Day Quick Guide - October 31, 2025

**Status: ✅ System Ready to Auto-Publish**

---

## What Will Happen (Automatically)

**6:00 AM UTC (Oct 31)**
- GitHub Actions triggers
- Posts 1 post from `day-1` to production
- Commits to GitHub
- Vercel auto-deploys
- **Post live in 3-5 minutes ✅**

**9:00 AM UTC**
- Repeat: 1 more post published
- Deployed automatically

**12:00 PM, 3:00 PM, 6:00 PM UTC**
- Same thing: 1 post each time
- All automatic

**By 6:00 PM UTC:**
- 5 posts published
- 5 posts live on website
- All posts on their way to Google

---

## Your Role (Monitoring)

### 6:00 AM Check
```
□ Go to GitHub Actions
  → github.com/[user]/NikaApplianceRepair/actions
□ Look for the workflow run
□ Should show ✅ green checkmark
□ Check Vercel dashboard
  → vercel.com/dashboard
□ Latest deployment should be "production"
□ Visit website and verify new post appears
```

### 9:00 AM, 12:00 PM, 3:00 PM, 6:00 PM Checks
- Repeat the same process
- Each time: verify workflow ran and post appears
- Takes 2 minutes per check

### Evening Check
- Count total posts published (should be 5)
- All have correct styling?
- Any errors in logs?
- Document for next day

---

## If Something Goes Wrong

### Workflow Failed?
1. Go to GitHub Actions
2. Click on the failed run
3. Expand the failed step
4. Read the error
5. Common fixes:
   - Check draft folder exists
   - Check files aren't locked
   - Manually run: `python scripts/auto-publish-posts.py --day day-1`

### Post Didn't Appear?
1. Check Vercel deployment succeeded
   - Go to Vercel → Deployments
   - Look for latest deployment
   - Should show "Ready"
2. Clear browser cache (Ctrl+Shift+Delete)
3. Check file permissions
4. Visit direct URL: `/blog/troubleshooting/[filename]`

### CSS Styling Broken?
1. Check paths in HTML: should be `../../css/blog-premium.css`
2. Verify CSS files deployed to Vercel
3. Check browser console for 404 errors
4. May need to manually verify CSS was deployed

---

## Emergency Actions

**If Automated System Fails:**

1. **Manually publish 1 post:**
```bash
cd C:\NikaApplianceRepair
python scripts/auto-publish-posts.py --count 1 --day day-1
```

2. **Commit to GitHub:**
```bash
git add -A
git commit -m "Manual publish: Blog post added"
git push
```

3. **Vercel will auto-deploy** within 1-2 minutes

---

## Timeline (October 31)

```
6:00 AM UTC
  └─ GitHub Actions: Publish post 1
  └─ Vercel deploys (2-3 min)
  └─ Post live ✅

9:00 AM UTC
  └─ GitHub Actions: Publish post 2
  └─ Post live ✅

12:00 PM UTC
  └─ GitHub Actions: Publish post 3
  └─ Post live ✅

3:00 PM UTC
  └─ GitHub Actions: Publish post 4
  └─ Post live ✅

6:00 PM UTC
  └─ GitHub Actions: Publish post 5
  └─ Post live ✅

Evening
  └─ All 5 posts published and live
  └─ Ready for Nov 1
```

---

## Timezone Conversion

**If 6:00 AM UTC doesn't match your schedule:**

| Your Time Zone | 6 AM UTC | 9 AM UTC | 12 PM UTC | 3 PM UTC | 6 PM UTC |
|---|---|---|---|---|---|
| **ET** | 1-2 AM | 4-5 AM | 8 AM | 11 AM | 2 PM |
| **CT** | 12-1 AM | 3-4 AM | 7 AM | 10 AM | 1 PM |
| **MT** | 11 PM* | 2-3 AM | 6 AM | 9 AM | 12 PM |
| **PT** | 10 PM* | 1-2 AM | 5 AM | 8 AM | 11 AM |

*previous day

---

## Success Signs

✅ **Everything is Working If:**
- GitHub Actions shows ✅ green checkmark
- Vercel shows "Ready" status
- Post appears on website within 5 minutes
- Page has correct styling (blue headers, footer)
- Post has all sections (intro, body, FAQ, related posts)

❌ **Something is Wrong If:**
- GitHub Actions shows red ✗
- Post doesn't appear after 10 minutes
- Page looks broken (no CSS, no formatting)
- Browser console shows 404 errors
- Vercel shows "Failed"

---

## What NOT to Do

❌ **Don't:**
- Manually publish posts while automation runs (will create duplicates)
- Edit draft files during publishing (will cause conflicts)
- Push changes to GitHub manually (will interfere with automation)
- Restart GitHub Actions while it's running (will create incomplete commits)
- Force push to main branch (will break Vercel deployment)

✅ **Do:**
- Monitor and verify
- Let automation do its job
- Only manually publish if automation fails
- Check logs if something seems wrong
- Ask for help if confused

---

## Important Links

**GitHub Actions:**
`https://github.com/[USER]/NikaApplianceRepair/actions`

**Vercel Dashboard:**
`https://vercel.com/dashboard`

**Vercel Deployments:**
`https://vercel.com/[PROJECT]/deployments`

**Your Website:**
`https://www.nikaappliancerepair.ca/blog/`

**Google Search Console:**
`https://search.google.com/search-console/`

---

## Notes for Nov 1-4

- Same process repeats each day
- GitHub Actions runs 5 times per day automatically
- Verify morning, afternoon, evening
- By Nov 5: all 24 posts live
- By Nov 12: all posts indexed by Google

---

## Post-Launch (Nov 5+)

1. **Check Google Search Console**
   - See which posts are indexed
   - Monitor crawl activity

2. **Check GA4**
   - New traffic to blog posts
   - User engagement metrics

3. **Track Rankings**
   - Monitor keyword positions
   - New rankings appearing

4. **Celebrate! 🎉**
   - You've successfully automated 24 post launches
   - Organic traffic will grow for months

---

## Questions?

**If Workflow Questions:**
→ See `VERCEL_DEPLOYMENT_SETUP.md`

**If Publishing Questions:**
→ See `PRE_LAUNCH_CHECKLIST.md`

**If Content Questions:**
→ See `FINAL_LAUNCH_SUMMARY.md`

**If Technical Issues:**
→ Check GitHub Actions logs or Vercel logs

---

## Summary

| Time | Action | Status |
|------|--------|--------|
| **Before 6 AM** | System Ready | ✅ Go |
| **6 AM** | Post 1 Published | Watch & Verify |
| **9 AM** | Post 2 Published | Watch & Verify |
| **12 PM** | Post 3 Published | Watch & Verify |
| **3 PM** | Post 4 Published | Watch & Verify |
| **6 PM** | Post 5 Published | Watch & Verify |
| **Evening** | 5 Posts Live | Celebrate! |
| **Next Day** | Repeat (Nov 1) | Same Process |

---

**Everything is automated. Your job is just to monitor and make sure it's working. Good luck! 🚀**

