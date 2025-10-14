# 🔧 Unified Header & Footer System

## 📁 Files Structure

```
/includes/
  ├── header.html          - Unified header HTML
  ├── header-styles.css    - Header styling
  ├── footer.html          - Unified footer HTML
  ├── include-loader.js    - JavaScript loader with caching
  └── README.md            - This file
```

## 🎯 How It Works

Instead of copying header/footer to every page, we load them dynamically:

1. **header.html** - Contains urgency banner + header + mobile sticky bar
2. **footer.html** - Contains footer with 4 columns
3. **include-loader.js** - Fetches and caches header/footer (1 hour cache)

## 🚀 How to Use on Any Page

### Step 1: Add CSS in `<head>`
```html
<head>
    <!-- ... other meta tags ... -->

    <!-- Unified Header Styles -->
    <link rel="stylesheet" href="/includes/header-styles.css">

    <style>
        /* Your page-specific styles */
    </style>
</head>
```

### Step 2: Add Placeholders in `<body>`
```html
<body>
    <!-- Header Placeholder -->
    <div id="header-placeholder"></div>

    <!-- Your page content here -->
    <section class="hero-section">
        ...
    </section>

    <!-- Footer Placeholder -->
    <div id="footer-placeholder"></div>

    <!-- Load Header & Footer -->
    <script src="/includes/include-loader.js"></script>
</body>
```

## ✅ Benefits

1. **Single Source of Truth** - Change header/footer ONCE, updates everywhere
2. **Faster Updates** - No need to edit 12+ pages
3. **Performance** - Cached for 1 hour (fast subsequent loads)
4. **Clean Code** - Pages only contain content, not header/footer HTML
5. **Easy Maintenance** - Update phone number/CTA in one place

## 🔄 How to Update Header/Footer

### Update Phone Number
1. Edit `/includes/header.html`
2. Find `437-747-6737`
3. Replace all instances
4. Save - automatically updates all pages!

### Update Navigation Links
1. Edit `/includes/header.html`
2. Find `<nav class="main-nav-v2">`
3. Add/edit links
4. Save

### Update Footer Links
1. Edit `/includes/footer.html`
2. Find section (Services, Locations, Company, Contact)
3. Add/edit links
4. Save

## 🧹 Clear Cache (Development)

Open browser console and run:
```javascript
clearIncludesCache()
```

Then refresh page to see changes immediately.

## 📊 Implementation Status

### ✅ Completed:
- [x] Created header.html
- [x] Created header-styles.css
- [x] Created footer.html
- [x] Created include-loader.js
- [x] Updated Mississauga page (test)

### 🚧 TODO:
- [ ] Update remaining 11 location pages
- [ ] Update 9 service pages
- [ ] Update homepage
- [ ] Test all pages

## 🎨 Header Features

**Desktop:**
- Logo (left)
- Services dropdown (6 services)
- Locations dropdown (12 cities)
- 3 CTA buttons (Call, WhatsApp, Book)

**Mobile:**
- Sticky header with logo + hamburger
- Sticky bottom bar (Call, Chat, Book)
- Auto-hides urgency banner when closed

**Urgency Banner:**
- Orange gradient
- "SAVE $40" message
- Close button (X)
- Stores in localStorage (won't show again)

## 🦶 Footer Features

**4 Columns:**
1. **Our Services** - 6 service links
2. **Service Areas** - 12 location links
3. **Company** - About, Reviews, FAQ, Privacy, Terms, Sitemap
4. **Contact** - Phone, Email, Address, Hours

**Auto-updates:**
- Current year in copyright

## ⚠️ Important Notes

1. **Clean URLs** - All links use clean URLs (no .html)
2. **Absolute Paths** - All links start with `/` (not `../`)
3. **Cache Duration** - 1 hour (3600000 ms)
4. **LocalStorage** - Uses ~10KB for caching
5. **Fallback** - Shows error message if fetch fails

## 🔧 Troubleshooting

### Header/Footer not loading?
1. Check browser console for errors
2. Verify placeholders exist: `header-placeholder` and `footer-placeholder`
3. Verify include-loader.js is loaded
4. Clear cache: `clearIncludesCache()`

### Styles not applying?
1. Check if header-styles.css is linked in `<head>`
2. Check for CSS conflicts (use browser DevTools)
3. Verify file paths are correct

### Links not working?
1. Check Vercel configuration for clean URLs
2. Verify all links use absolute paths (`/services/...`)
3. Check if target pages exist

## 📝 Next Steps

1. Update all 12 location pages to use includes
2. Update 9 service pages to use includes
3. Update homepage to use includes
4. Test all pages (desktop + mobile)
5. Deploy to production
6. Monitor for issues

---

**Last Updated:** 2025-10-14
**Version:** 1.0
**Status:** Ready for deployment
