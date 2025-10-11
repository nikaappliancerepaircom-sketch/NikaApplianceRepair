# 🚀 How to Run Your Website Locally

## Quick Start (Easiest Method)

### Option 1: Simple HTTP Server (No Installation Required)

1. **Open Command Prompt** in your project folder
   - Press `Win + R`, type `cmd`, press Enter
   - Navigate to: `cd C:\Users\petru\Documents\NikaApplianceRepair`

2. **Use Python** (if you have Python installed):
   ```
   python -m http.server 8080
   ```
   Then open: http://localhost:8080/homepage-complete.html

3. **OR Use Node.js** (if you have Node.js):
   ```
   npx http-server -p 8080
   ```
   Then open: http://localhost:8080/homepage-complete.html

### Option 2: Professional Development Setup

1. **Install Node.js** from https://nodejs.org/ (if not installed)

2. **Double-click** `start-dev-server.bat`
   - This will install everything needed
   - Opens your website automatically
   - Watches for changes

## Converting to a Multi-Page Website

Your website structure is already set up for multiple pages:

```
NikaApplianceRepair/
├── homepage-complete.html    (Your main design)
├── services/                 (Service pages)
├── locations/               (Location pages)
├── brands/                  (Brand pages)
└── assets/                  (CSS, JS, images)
```

### To Add New Pages:

1. **Copy** `homepage-complete.html` to a new file
2. **Edit** the content (keep header/footer)
3. **Save** in the appropriate folder:
   - Service pages → `/services/`
   - Location pages → `/locations/`
   - Brand pages → `/brands/`

### Example - Creating a Service Page:

1. Copy `homepage-complete.html` → `services/refrigerator-repair.html`
2. Change the title and content
3. Keep the same header, footer, and styles
4. Update internal links to use relative paths

## Making It Work Like a Real Website

The key is using a local web server (like we set up above) instead of opening files directly. This makes:
- Links work properly
- No "file:///" URLs
- Behaves like a real website
- Can test on multiple devices on your network

## Next Steps

1. Start with the simple HTTP server to test
2. Create your service pages
3. Update all internal links
4. Test navigation between pages

## Tips

- Always use relative URLs (`/services/refrigerator-repair` not `file:///...`)
- Keep consistent header/footer across all pages
- Test on different browsers
- Use the browser's developer tools (F12) to debug

## Need Help?

If the automated setup doesn't work, you can manually:
1. Copy the CSS from `<style>` tags to `/assets/css/main.css`
2. Copy the JS from `<script>` tags to `/assets/js/main.js`
3. Update the HTML files to link to these external files
4. Use any local web server to run the site