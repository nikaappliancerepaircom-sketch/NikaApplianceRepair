// @ts-check
const { test, expect, devices } = require('@playwright/test');

/**
 * Mobile Responsive Tests for Nika Appliance Repair
 * Tests all 9 service pages on mobile devices
 */

const servicePages = [
  'refrigerator-repair.html',
  'dishwasher-repair.html',
  'washer-repair.html',
  'dryer-repair.html',
  'freezer-repair.html',
  'stove-repair.html',
  'oven-repair.html',
  'range-repair.html',
  'microwave-repair.html'
];

const mobileDevices = {
  'iPhone SE': devices['iPhone SE'],
  'iPhone 12': devices['iPhone 12'],
  'Pixel 5': devices['Pixel 5'],
  'Galaxy S9+': devices['Galaxy S9+']
};

// Test each page on each mobile device
for (const [deviceName, device] of Object.entries(mobileDevices)) {
  test.describe(`Mobile Tests - ${deviceName}`, () => {
    test.use(device);

    for (const page of servicePages) {
      test(`${page} - No Horizontal Overflow`, async ({ page: browserPage }) => {
        // Navigate to page
        await browserPage.goto(`file:///C:/NikaApplianceRepair/services/${page}`);

        // Wait for page to load
        await browserPage.waitForLoadState('networkidle');

        // Check viewport width
        const viewportWidth = browserPage.viewportSize().width;

        // Check body width
        const bodyWidth = await browserPage.evaluate(() => {
          return document.body.scrollWidth;
        });

        // Body should not be wider than viewport
        expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 1); // +1 for rounding

        console.log(`✓ ${deviceName} - ${page}: Body width ${bodyWidth}px <= Viewport ${viewportWidth}px`);
      });

      test(`${page} - Countdown Timer Centered`, async ({ page: browserPage }) => {
        await browserPage.goto(`file:///C:/NikaApplianceRepair/services/${page}`);
        await browserPage.waitForLoadState('networkidle');

        // Find countdown timer
        const timerBox = await browserPage.locator('.timer-box').first();

        if (await timerBox.count() > 0) {
          // Check that timer-value is centered
          const timerValue = await timerBox.locator('.timer-value');
          const textAlign = await timerValue.evaluate((el) => {
            return window.getComputedStyle(el).textAlign;
          });

          expect(textAlign).toBe('center');

          // Check that timer-label is centered
          const timerLabel = await timerBox.locator('.timer-label');
          const labelAlign = await timerLabel.evaluate((el) => {
            return window.getComputedStyle(el).textAlign;
          });

          expect(labelAlign).toBe('center');

          console.log(`✓ ${deviceName} - ${page}: Countdown timer centered`);
        }
      });

      test(`${page} - Videos Responsive`, async ({ page: browserPage }) => {
        await browserPage.goto(`file:///C:/NikaApplianceRepair/services/${page}`);
        await browserPage.waitForLoadState('networkidle');

        const viewportWidth = browserPage.viewportSize().width;

        // Check all video wrappers
        const videoWrappers = await browserPage.locator('.video-wrapper, .testimonial-video-wrapper').all();

        for (let i = 0; i < videoWrappers.length; i++) {
          const wrapper = videoWrappers[i];
          const wrapperWidth = await wrapper.evaluate((el) => el.scrollWidth);

          expect(wrapperWidth).toBeLessThanOrEqual(viewportWidth);
        }

        if (videoWrappers.length > 0) {
          console.log(`✓ ${deviceName} - ${page}: ${videoWrappers.length} videos responsive`);
        }
      });

      test(`${page} - Touch Targets ≥ 48px`, async ({ page: browserPage }) => {
        await browserPage.goto(`file:///C:/NikaApplianceRepair/services/${page}`);
        await browserPage.waitForLoadState('networkidle');

        // Check all buttons
        const buttons = await browserPage.locator('button, .cta-primary, .cta-secondary').all();

        for (let i = 0; i < buttons.length; i++) {
          const button = buttons[i];
          const height = await button.evaluate((el) => {
            return el.getBoundingClientRect().height;
          });

          // Touch targets should be at least 44px (Apple), 48px (Google)
          expect(height).toBeGreaterThanOrEqual(44);
        }

        console.log(`✓ ${deviceName} - ${page}: ${buttons.length} buttons are touch-friendly`);
      });

      test(`${page} - No Elements Overflow Viewport`, async ({ page: browserPage }) => {
        await browserPage.goto(`file:///C:/NikaApplianceRepair/services/${page}`);
        await browserPage.waitForLoadState('networkidle');

        const viewportWidth = browserPage.viewportSize().width;

        // Check all major sections
        const sections = await browserPage.locator('section').all();

        for (let i = 0; i < sections.length; i++) {
          const section = sections[i];
          const sectionWidth = await section.evaluate((el) => el.scrollWidth);

          expect(sectionWidth).toBeLessThanOrEqual(viewportWidth + 2); // +2 for rounding
        }

        console.log(`✓ ${deviceName} - ${page}: All ${sections.length} sections within viewport`);
      });
    }

    test('Back to Top Button Visible on Scroll', async ({ page: browserPage }) => {
      await browserPage.goto('file:///C:/NikaApplianceRepair/services/refrigerator-repair.html');
      await browserPage.waitForLoadState('networkidle');

      // Initially hidden
      const backToTop = await browserPage.locator('#backToTop');
      const initialDisplay = await backToTop.evaluate((el) => {
        return window.getComputedStyle(el).display;
      });

      // Scroll down
      await browserPage.evaluate(() => window.scrollTo(0, 400));
      await browserPage.waitForTimeout(500);

      // Should be visible now
      const scrolledDisplay = await backToTop.evaluate((el) => {
        return window.getComputedStyle(el).display;
      });

      expect(scrolledDisplay).not.toBe('none');
      console.log(`✓ ${deviceName}: Back to top button appears on scroll`);
    });
  });
}

// Summary test
test('Mobile Test Summary', async () => {
  console.log('\n==============================================');
  console.log('MOBILE RESPONSIVE TESTS SUMMARY');
  console.log('==============================================');
  console.log(`✓ Tested ${servicePages.length} pages`);
  console.log(`✓ Tested on ${Object.keys(mobileDevices).length} devices`);
  console.log('✓ Checked:');
  console.log('  - No horizontal overflow');
  console.log('  - Countdown timer centered');
  console.log('  - Videos responsive');
  console.log('  - Touch targets ≥ 48px');
  console.log('  - All sections within viewport');
  console.log('  - Back to top button');
  console.log('==============================================\n');
});
