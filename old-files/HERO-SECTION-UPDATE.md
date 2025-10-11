## Hero Section Updates Summary

The following updates have been completed:

### 1. Word Color Changes
- The word "appliance" in the hero title now has yellow color (#FFD600) with a subtle text shadow

### 2. Floating Icons Updates
- All floating emoji icons have been replaced with custom SVG appliance icons:
  - Icon 1: Refrigerator
  - Icon 2: Washing Machine  
  - Icon 3: Dishwasher
  - Icon 4: Dryer
  - Icon 5: Stove
  - Icon 6: Oven

### 3. Icon Styling
- Icons are now white color (using currentColor with white from CSS)
- Opacity increased from 0.2 to 0.3 for better visibility
- Added drop shadow for better visual depth
- Icons use proper SVG format with varying opacity layers for depth

### CSS Changes Made:
1. Added `color: var(--white)` to `.floating-icon` class
2. Added drop shadow filter to floating icons
3. Added specific styling for `.hero-title .highlight-yellow`
4. Increased icon opacity from 0.2 to 0.3

### HTML Changes Made:
1. Replaced all emoji icons with custom SVG appliance service icons
2. Each icon represents a specific appliance service offered

The hero section now properly displays white appliance service icons floating in the background with the word "appliance" highlighted in yellow color.