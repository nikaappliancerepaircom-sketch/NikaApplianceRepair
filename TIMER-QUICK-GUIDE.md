# Countdown Timer Quick Reference Guide

## The ONE Timer to Rule Them All

Every page on the site now uses the SAME timer. No exceptions.

---

## Quick Facts

- **Timer Value:** 14 minutes 45 seconds (always)
- **Title:** "Book Online & Save $40 on Any Service" (always)
- **Labels:** "MINUTES" and "SECONDS" in uppercase (always)
- **Layout:** Horizontal (always, even on mobile)
- **Color:** Red background (#dc2626)
- **Synced:** Timer state persists across pages (localStorage)

---

## The Unified Timer HTML

```html
<!-- Unified Countdown Timer -->
<section class="countdown-section">
    <div class="container">
        <h2 class="countdown-title">Book Online & Save $40 on Any Service</h2>
        <p class="countdown-label">DEAL ENDS IN</p>
        <div class="countdown-timer">
            <div class="timer-box">
                <div class="timer-value countdown-minutes" id="timer-minutes">14</div>
                <div class="timer-label">MINUTES</div>
            </div>
            <div class="timer-box">
                <div class="timer-value countdown-seconds" id="timer-seconds">45</div>
                <div class="timer-label">SECONDS</div>
            </div>
        </div>
        <a href="[LINK]" class="countdown-cta">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
            </svg>
            CLICK TO BOOK DIAGNOSTIC NOW
        </a>
    </div>
</section>
```

**[LINK] should be:**
- Homepage: `#book`
- All other pages: `../book.html`

---

## Required Files

Make sure these are loaded on EVERY page with a timer:

```html
<!-- CSS -->
<link rel="stylesheet" href="css/countdown-horizontal.css">

<!-- JavaScript -->
<script src="js/countdown-timer.js" defer></script>
```

For pages in subdirectories (services, locations, brands):
```html
<link rel="stylesheet" href="../css/countdown-horizontal.css">
<script src="../js/countdown-timer.js" defer></script>
```

---

## Adding Timer to New Page

1. Copy HTML from `includes/countdown-timer.html`
2. Update the link href:
   - Homepage: `#book`
   - Other pages: `../book.html`
3. Load required CSS and JS files (see above)
4. Test that timer counts down

---

## DO NOT:

❌ Change timer initial values (14, 45)
❌ Change label casing (must be UPPERCASE)
❌ Change title text
❌ Create different timer designs
❌ Use different colors
❌ Make timer vertical on mobile

The JavaScript automatically controls the timer. HTML values are just for initial display.

---

## Common Issues & Fixes

### Timer Not Counting
- **Fix:** Ensure `js/countdown-timer.js` is loaded
- **Check:** Look for JavaScript errors in console

### Timer Looks Wrong
- **Fix:** Ensure `css/countdown-horizontal.css` is loaded
- **Check:** Verify CSS path is correct for page location

### Timer Not Syncing
- **Fix:** Check localStorage is enabled in browser
- **Check:** All pages use the same storage key (`nikaCountdownEndTime`)

### Need to Re-unify All Timers
```bash
python unify_countdown_timers.py
```

---

## How It Works

1. **HTML** shows initial state (14:45)
2. **JavaScript** takes over immediately on page load
3. **JavaScript** checks localStorage for existing timer
4. **If timer exists:** Continue counting from stored time
5. **If no timer:** Create new timer starting at 14:45
6. **Every second:** Update display, save to localStorage
7. **When reaches 0:** Reset to 14:45 and continue

---

## Customization Points

### Change Timer Duration
Edit `js/countdown-timer.js`:
```javascript
const TIMER_DURATION = 14 * 60 + 45; // Change numbers here
```

### Change Timer Colors
Edit `css/countdown-horizontal.css`:
```css
.timer-box {
    background: #dc2626 !important; /* Red - change to your color */
}
```

### Change Timer Text
Edit HTML on each page (or use Python script to batch update):
```html
<h2 class="countdown-title">Your New Title Here</h2>
```

---

## File Locations

- **Template:** `includes/countdown-timer.html`
- **JavaScript:** `js/countdown-timer.js`
- **CSS:** `css/countdown-horizontal.css`
- **Update Script:** `unify_countdown_timers.py`
- **Documentation:** `COUNTDOWN-TIMER-UNIFICATION-REPORT.md`

---

## Testing Checklist

After making any changes, test:

- [ ] Timer displays correctly on desktop
- [ ] Timer displays correctly on mobile
- [ ] Timer counts down every second
- [ ] Timer resets when reaching 0
- [ ] Timer syncs across page navigation
- [ ] Timer link works correctly
- [ ] No JavaScript errors in console
- [ ] Timer stays horizontal on mobile

---

## Emergency: Revert to Original

If something goes wrong:

1. Check git history
2. Find last working commit
3. Restore timer HTML from that commit
4. Or run: `git checkout HEAD~1 -- [file-path]`

Better: Always test in development first!

---

## Summary

**Remember:** ONE timer design, used everywhere, no exceptions.

This makes the site look professional and makes your life easier.

Questions? Read the full report: `COUNTDOWN-TIMER-UNIFICATION-REPORT.md`
