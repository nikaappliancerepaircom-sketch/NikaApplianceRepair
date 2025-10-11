# Nika Appliance Repair - Local Development Setup

This setup allows you to run your website locally as a complete site, not just page by page.

## Quick Start

1. **Install Node.js** (if not already installed)
   - Download from: https://nodejs.org/
   - Choose the LTS version

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```
   This will:
   - Build all your pages
   - Start a local server at http://localhost:8080
   - Watch for changes and rebuild automatically

## Project Structure

```
NikaApplianceRepair/
├── src/                    # Source files
│   ├── components/         # Reusable components (header, footer)
│   ├── layouts/           # Page layouts
│   ├── pages/             # Individual pages
│   └── css/               # Stylesheets
├── dist/                  # Built website (generated)
├── assets/                # Images, fonts, etc.
└── build.js              # Build script
```

## Commands

- `npm run dev` - Start development server with auto-reload
- `npm run build` - Build the website
- `npm run serve` - Serve the built website

## Adding New Pages

1. Create a new HTML file in `src/pages/`
2. The build system will automatically process it
3. Access it via the local server

## How It Works

The build system:
- Combines layouts with page content
- Includes shared components (header/footer)
- Copies all assets
- Creates a complete website in the `dist/` folder