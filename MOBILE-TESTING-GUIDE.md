# Mobile Testing Guide - Playwright

## 📱 Setup Instructions

### 1. Install Node.js
Download from: https://nodejs.org/

### 2. Install Dependencies
```bash
cd C:\NikaApplianceRepair
npm install
```

### 3. Install Playwright Browsers
```bash
npx playwright install
```

## 🧪 Running Tests

### Run All Mobile Tests
```bash
npm run test:mobile
```

### Run Tests with Browser Window (Visual Mode)
```bash
npm run test:headed
```

### Run Specific Device Tests
```bash
npx playwright test --project="iPhone SE"
npx playwright test --project="Mobile Chrome"
npx playwright test --project="Galaxy S9+"
```

### View Test Report
```bash
npm run test:report
```

## ✅ What We Test

### 1. **No Horizontal Overflow**
- Body width ≤ viewport width
- No horizontal scroll on any page

### 2. **Countdown Timer**
- MINUTES text centered
- SECONDS text centered
- No vertical scroll bars

### 3. **Videos Responsive**
- All video wrappers fit within viewport
- YouTube embeds scale properly
- Testimonial videos responsive

### 4. **Touch Targets**
- All buttons ≥ 48px height (Google standard)
- CTA buttons touch-friendly
- Form inputs accessible

### 5. **Sections Within Viewport**
- All sections fit within screen width
- No content overflow
- Proper padding/margins

### 6. **Back to Top Button**
- Hidden on page load
- Appears on scroll (300px+)
- Properly positioned (fixed)

## 📊 Test Results

After running tests, you'll see:

```
✓ iPhone SE - refrigerator-repair.html: Body width 375px <= Viewport 375px
✓ iPhone SE - refrigerator-repair.html: Countdown timer centered
✓ iPhone SE - refrigerator-repair.html: 6 videos responsive
✓ iPhone SE - refrigerator-repair.html: 12 buttons are touch-friendly
✓ iPhone SE - refrigerator-repair.html: All 15 sections within viewport
```

## 🎯 Tested Devices

- **iPhone SE** (375px) - Smallest iPhone
- **iPhone 12** (390px) - Modern iPhone
- **Pixel 5** (393px) - Android
- **Galaxy S9+** (412px) - Large Android
- **iPad Mini** (768px) - Tablet

## 📋 Test Coverage

**Pages tested:**
- refrigerator-repair.html
- dishwasher-repair.html
- washer-repair.html
- dryer-repair.html
- freezer-repair.html
- stove-repair.html
- oven-repair.html
- range-repair.html
- microwave-repair.html

**Total:** 9 pages × 5 devices = 45 test configurations

## 🐛 Debugging Failed Tests

### View Screenshots
```bash
# Screenshots saved in: test-results/
```

### View Videos
```bash
# Videos saved in: test-results/
```

### View Traces
```bash
npx playwright show-trace test-results/trace.zip
```

## ⚙️ Configuration

Edit `playwright.config.js` to:
- Add more devices
- Change viewport sizes
- Modify test settings
- Add custom reporters

## 📝 Test File Structure

```
C:\NikaApplianceRepair\
├── tests/
│   └── mobile-test.spec.js    # Main test file
├── playwright.config.js        # Playwright config
├── package.json               # Dependencies
└── test-results/              # Test output (auto-generated)
```

## 🚀 CI/CD Integration

Add to GitHub Actions:
```yaml
- name: Install dependencies
  run: npm ci

- name: Install Playwright Browsers
  run: npx playwright install --with-deps

- name: Run Playwright tests
  run: npm run test:mobile
```

## 📈 Expected Results

All tests should PASS:
- ✅ No horizontal overflow
- ✅ Countdown timer centered
- ✅ Videos responsive
- ✅ Touch targets ≥ 48px
- ✅ Sections within viewport
- ✅ Back to top button works

If any test FAILS:
1. Check the screenshot in `test-results/`
2. Review the specific element
3. Update CSS in `mobile-strict-fix.css`
4. Re-run tests

## 🔧 Maintenance

Re-run tests after:
- CSS changes
- HTML structure changes
- Adding new sections
- Updating responsive breakpoints

---

**Last Updated:** 2025-10-11
**Status:** ✅ All tests configured and ready to run
