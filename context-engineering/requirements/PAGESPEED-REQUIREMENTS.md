# 🚀 GOOGLE PAGESPEED INSIGHTS REQUIREMENTS

## 📊 PERFORMANCE TARGETS
**Minimum Score: 95+ on both Mobile and Desktop**

### 🎯 Core Web Vitals Requirements

#### 1. Largest Contentful Paint (LCP)
- **Target**: < 2.5 seconds
- **Good**: < 2.5s
- **Needs Improvement**: 2.5s - 4s
- **Poor**: > 4s

**Optimization Strategies:**
- Optimize hero images (WebP format)
- Preload critical resources
- Use responsive images with srcset
- Implement lazy loading
- Minimize render-blocking resources

#### 2. First Input Delay (FID) / Interaction to Next Paint (INP)
- **Target**: < 100 milliseconds
- **Good**: < 100ms
- **Needs Improvement**: 100ms - 300ms
- **Poor**: > 300ms

**Optimization Strategies:**
- Minimize JavaScript execution time
- Break up long tasks
- Use web workers for heavy computations
- Optimize third-party scripts

#### 3. Cumulative Layout Shift (CLS)
- **Target**: < 0.1
- **Good**: < 0.1
- **Needs Improvement**: 0.1 - 0.25
- **Poor**: > 0.25

**Optimization Strategies:**
- Set explicit dimensions for images/videos
- Reserve space for dynamic content
- Avoid inserting content above existing content
- Use CSS transforms for animations

### 🎨 ACCESSIBILITY REQUIREMENTS

#### Color Contrast (WCAG AA)
- **Normal Text**: Minimum contrast ratio 4.5:1
- **Large Text (18px+)**: Minimum contrast ratio 3:1
- **Interactive Elements**: Minimum contrast ratio 3:1

**Common Issues to Avoid:**
- Light text on light backgrounds
- Dark text on dark backgrounds
- Low contrast placeholders
- Insufficient focus indicators

### ⚡ PERFORMANCE CHECKLIST

#### Images
- [ ] Use WebP format with JPEG fallback
- [ ] Implement lazy loading (loading="lazy")
- [ ] Use srcset for responsive images
- [ ] Optimize image sizes (<100KB for heroes)
- [ ] Set explicit width and height attributes
- [ ] Use CSS aspect-ratio for consistency

#### CSS
- [ ] Inline critical CSS
- [ ] Defer non-critical CSS
- [ ] Minify all CSS files
- [ ] Remove unused CSS
- [ ] Use CSS containment where appropriate

#### JavaScript
- [ ] Minify and compress JS files
- [ ] Defer non-critical scripts
- [ ] Remove unused JavaScript
- [ ] Use async/defer attributes appropriately
- [ ] Implement code splitting

#### Fonts
- [ ] Use font-display: swap
- [ ] Preload critical fonts
- [ ] Subset fonts to required characters
- [ ] Use variable fonts where possible
- [ ] Limit font families (max 2-3)

#### Server/Hosting
- [ ] Enable Gzip/Brotli compression
- [ ] Set proper cache headers
- [ ] Use CDN for static assets
- [ ] Enable HTTP/2
- [ ] Implement resource hints (preconnect, prefetch)

### 📱 MOBILE-SPECIFIC OPTIMIZATIONS

#### Touch Targets
- Minimum size: 48x48px
- Adequate spacing between targets
- No overlapping clickable elements

#### Viewport
- Proper meta viewport tag
- No horizontal scrolling
- Content fits viewport width

#### Text Sizing
- Base font size ≥ 16px
- No text smaller than 12px
- Line height ≥ 1.5

### 🔍 COMMON PAGESPEED WARNINGS & FIXES

#### "Reduce unused CSS"
- Use PurgeCSS or similar tools
- Split CSS by page/component
- Inline critical CSS

#### "Eliminate render-blocking resources"
- Inline critical CSS
- Defer non-critical CSS/JS
- Use resource hints

#### "Serve images in next-gen formats"
- Convert to WebP
- Provide fallbacks for older browsers
- Use picture element

#### "Properly size images"
- Use responsive images
- Serve different sizes for different devices
- Implement art direction

### 📈 MONITORING & TESTING

#### Tools
1. **Google PageSpeed Insights**
   - Test both mobile and desktop
   - Check field data vs lab data
   - Monitor Core Web Vitals

2. **Lighthouse (Chrome DevTools)**
   - Run in incognito mode
   - Test with throttling
   - Check all categories

3. **WebPageTest**
   - Test from different locations
   - Check repeat view performance
   - Analyze waterfall charts

#### Testing Checklist
- [ ] Test on real devices (not just emulation)
- [ ] Test with slow 3G connection
- [ ] Test with CPU throttling
- [ ] Clear cache between tests
- [ ] Test at different times of day

### 🎯 SPECIFIC TARGETS FOR NIKA

#### Homepage (index.html)
- Mobile Score: 95+
- Desktop Score: 98+
- LCP: < 2.0s
- FID: < 50ms
- CLS: < 0.05

#### Landlords Page
- Mobile Score: 95+
- Desktop Score: 98+
- Fix color contrast in hero
- Optimize business images

#### Service Pages
- Mobile Score: 95+
- Desktop Score: 98+
- Lazy load testimonial videos
- Optimize form rendering

### ⚠️ CRITICAL ISSUES TO AVOID

1. **Text-Image Contrast**
   - Never put light text on light images
   - Add dark overlay for hero images
   - Test with different image loading states

2. **Font Loading**
   - Avoid FOIT (Flash of Invisible Text)
   - Use font-display: swap
   - Provide fallback fonts

3. **Animation Performance**
   - Use CSS transforms only
   - Avoid animating layout properties
   - Respect prefers-reduced-motion

### 📋 PRE-DEPLOYMENT CHECKLIST

- [ ] All pages score 95+ on mobile
- [ ] All pages score 98+ on desktop
- [ ] No accessibility errors
- [ ] All images optimized
- [ ] CSS/JS minified
- [ ] Caching configured
- [ ] No console errors
- [ ] Forms tested
- [ ] Analytics verified

---

**Remember**: Performance is a feature. Fast sites convert better, rank higher, and provide better user experience.
