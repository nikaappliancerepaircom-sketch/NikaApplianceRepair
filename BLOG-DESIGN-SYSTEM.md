# BLOG DESIGN SYSTEM - Nika Appliance Repair

**Complete Design Specifications for Premium Blog Template**

---

## 📐 COLOR PALETTE

### Primary Colors
- **Primary Blue**: `#2196f3` (used for headers, links, accents)
- **Secondary Blue**: `#03a9f4` (gradient accent)
- **Tertiary Cyan**: `#00bcd4` (gradient accent)
- **Dark Gray**: `#1a202c` (footer background, dark text)
- **Medium Gray**: `#2d3748` (footer gradient)

### Text Colors
- **Primary Text**: `#333` (body text)
- **Light Text**: `#666` (secondary text, metadata)
- **White**: `#fff` (buttons, footer text)

### Background Colors
- **Main Background**: `#f9f9f9` (page background)
- **White**: `#fff` (content blocks)
- **Info Box Blue**: `#e3f2fd` (tip/info background)
- **Success Box Green**: `#e8f5e9` (info box background)
- **Warning Box Orange**: `#fff3e0` (warning background)

### Accent Colors (UI)
- **Phone Button Green**: `#10b981` (header CTA)
- **Book Button Amber**: `#f59e0b` (header CTA)
- **Facebook Blue**: `#1877f2` (social share)
- **Twitter Blue**: `#1da1f2` (social share)
- **LinkedIn Blue**: `#0077b5` (social share)
- **Email Gray**: `#666` (social share)
- **Gold Stars**: `#ffd700` (trust rating)

### Borders & Lines
- **Border Gray**: `#e0e0e0` (dividers, borders)
- **Light Border**: `rgba(255,255,255,0.1)` (footer borders)
- **Shadow**: `0 2px 8px rgba(0,0,0,0.1)` (box shadows)

---

## 🔤 TYPOGRAPHY

### Font Family
- **Headings**: `'Fredoka'` (sans-serif fallback)
- **Body Text**: `'Rubik'` (system fallbacks: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif)

### Font Weights
- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semi-bold**: 600
- **Bold**: 700

### Font Sizes (Responsive with clamp)

#### Blog Title (h1)
```
clamp(1.75rem, 4vw, 2.5rem)
Line height: 1.2
Font weight: 700 (bold)
Font family: Fredoka
Color: #1a202c (dark gray)
Margin bottom: 1rem
```

#### Section Headers (h2)
```
clamp(1.5rem, 3vw, 2rem)
Line height: default
Font weight: 700 (bold)
Font family: Fredoka
Color: #2196f3 (primary blue)
Margin: 2.5rem 0 1.5rem
Padding left: 1rem
Border left: 4px solid #2196f3
Scroll margin top: 80px (for anchor links)
```

#### Subsection Headers (h3)
```
clamp(1.25rem, 2.5vw, 1.5rem)
Font weight: 700 (bold)
Font family: Fredoka
Color: #1a202c (dark gray)
Margin: 2rem 0 1rem
```

#### Body Text (p)
```
Font size: 1.125rem (18px)
Line height: 1.8
Color: #333
Margin bottom: 1.5rem
```

#### Small Text (metadata, footer)
```
Font size: 0.95rem (15px)
Color: #666 (light gray)
```

#### Extra Small Text
```
Font size: 0.875rem (14px)
```

#### Tiny Text
```
Font size: 0.8rem (13px)
```

---

## 📏 SPACING & LAYOUT

### Blog Wrapper
```
Max width: 1400px
Margin: 2rem auto
Padding: 0 2rem
Display: grid
Grid columns: 1fr 350px (main content + 350px sidebar)
Gap: 3rem
Mobile (max-width: 1024px): grid-template-columns: 1fr (stacked)
```

### Main Content Area (.blog-main)
```
Background: #fff (white)
Border radius: 8px
Box shadow: 0 2px 8px rgba(0,0,0,0.1)
Padding: 3rem (desktop) / 1.5rem (mobile)
```

### Blog Header
```
Margin bottom: 2rem
Padding bottom: 2rem
Border bottom: 2px solid #e0e0e0
```

### Reading Progress Bar
```
Position: fixed
Top: 0
Left: 0
Width: 100%
Height: 4px
Background: #e0e0e0
Z-index: 9999
Gradient: linear-gradient(to right, #2196f3, #03a9f4, #00bcd4)
```

### Sections
```
Margin top/bottom: 1.5rem to 2.5rem
Padding: varies per section type
```

---

## 🎨 COMPONENT STYLES

### Blog Meta (Top)
```
Display: flex
Gap: 1.5rem
Margin bottom: 1rem
Font size: 0.95rem

Category:
  Color: #2196f3 (primary blue)
  Font weight: 600

Reading time:
  Color: #666 (light gray)
```

### Blog Meta (Bottom)
```
Display: flex
Gap: 1.5rem
Color: #666
Font size: 0.95rem

Meta items:
  Display: flex
  Gap: 0.5rem (icon + text)
```

### Social Share Buttons
```
Display: flex
Gap: 1rem
Margin bottom: 2rem
Padding bottom: 2rem
Border bottom: 1px solid #e0e0e0

Button style:
  Width: 40px
  Height: 40px
  Border radius: 50% (circle)
  Display: flex
  Align items: center
  Justify content: center
  Text decoration: none
  Color: white
  Transition: transform 0.2s
  Hover: transform translateY(-2px)
```

### Tip Box (.tip-box)
```
Background: #e3f2fd (light blue)
Border left: 4px solid #2196f3
Padding: 1.5rem
Border radius: 8px
Margin: 2rem 0
```

### Info Box (.info-box)
```
Background: #e8f5e9 (light green)
Border left: 4px solid #4caf50
Padding: 1.5rem
Border radius: 8px
Margin: 2rem 0
```

### Warning Box (.warning-box)
```
Background: #fff3e0 (light orange)
Border left: 4px solid #ff9800
Padding: 1.5rem
Border radius: 8px
Margin: 2rem 0
```

### CTA Box (.cta-box)
```
Background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Color: white
Padding: 2.5rem
Border radius: 8px
Margin: 3rem 0
Text align: center
Position: relative
Overflow: hidden

Animated pattern:
  Background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 30%, rgba(255,255,255,0.1) 70%, transparent 70%)
  Background size: 20px 20px
  Animation: movePattern 20s linear infinite

Button (.btn inside):
  Display: inline-flex
  Align items: center
  Gap: 0.75rem
  Background: #fff (white)
  Color: #667eea (purple)
  Padding: 1rem 2rem
  Border radius: 8px
  Font weight: 600
  Transition: transform 0.2s
  Hover: transform translateY(-2px)
```

### Comparison Grid
```
Display: grid
Grid columns: repeat(auto-fit, minmax(280px, 1fr))
Gap: 2rem
Margin: 2rem 0

Comparison Card:
  Background: white
  Border radius: 8px
  Padding: 2rem
  Border: 2px solid #e0e0e0
  Transition: transform 0.2s, box-shadow 0.2s
  Hover: transform translateY(-4px), box-shadow: 0 4px 12px rgba(0,0,0,0.15)

Safe variant (.safe):
  Border color: #4caf50 (green)
  Background: linear-gradient(to bottom, #f1f8f1 0%, white 100%)

Danger variant (.danger):
  Border color: #f44336 (red)
  Background: linear-gradient(to bottom, #fff5f5 0%, white 100%)

Card heading:
  Font size: 1.25rem
  Margin bottom: 1rem

Card lists:
  List style: none
  Padding: 0

Card items:
  Padding: 0.5rem 0
  Border bottom: 1px solid #f0f0f0

Last item:
  Border bottom: none

Card footer:
  Margin top: 1.5rem
  Padding top: 1rem
  Border top: 2px solid #e0e0e0
  Font weight: 600
  Color: #2196f3
```

### Lists
```
Unordered & Ordered:
  Margin: 1.5rem 0
  Padding left: 2rem

List items:
  Margin bottom: 0.75rem
```

### Tables
```
Width: 100%
Border collapse: collapse
Margin: 2rem 0
Background: white
Box shadow: 0 2px 8px rgba(0,0,0,0.1)
Border radius: 8px
Overflow: hidden

Thead:
  Background: #2196f3 (primary blue)
  Color: white

Tbody rows (alternate):
  Even rows: #f9f9f9 (light gray)
  Odd rows: white

Cells:
  Padding: varies
  Border: varies
```

### Sidebar (.blog-sidebar)
```
Width: 350px (desktop)
Hidden: (mobile/tablet)

Table of Contents Widget:
  H3 font size: varies
  List: unstyled
  Links: color varies

Related Posts Widget:
  Related post: padding, margin varies
  Related post meta: font-size 0.95rem, color #666
```

---

## 🔼 HEADER (.site-header)

```
Background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%)
Color: white
Padding: 1rem 0
Box shadow: 0 2px 10px rgba(0,0,0,0.1)
Position: sticky
Top: 0
Z-index: 1000

Container:
  Max width: 1400px
  Margin: 0 auto
  Padding: 0 2rem
  Display: flex
  Align items: center
  Justify content: space-between
  Gap: 2rem

Logo:
  Font family: Fredoka
  Font size: 1.5rem
  Font weight: 700
  Color: white
  Text decoration: none

Navigation:
  Flex: 1
  List: display flex, gap 2rem
  Links:
    Color: rgba(255,255,255,0.9)
    Text decoration: none
    Font weight: 500
    Transition: color 0.2s
    Hover: color white

Trust Section:
  Display: flex
  Flex direction: column
  Align items: center
  Gap: 0.25rem

  Stars: color #ffd700, font-size 0.9rem
  Rating: font-weight 600, font-size 1.1rem
  Reviews: font-size 0.8rem, opacity 0.8

CTA Buttons:
  Display: flex
  Gap: 1rem

  Phone button (.cta-phone):
    Display: flex
    Align items: center
    Gap: 0.5rem
    Padding: 0.75rem 1.5rem
    Border radius: 6px
    Text decoration: none
    Font weight: 600
    Background: #10b981 (green)
    Color: white
    Transition: transform 0.2s
    Hover: transform translateY(-2px)

  Book button (.cta-book):
    Display: flex
    Align items: center
    Gap: 0.5rem
    Padding: 0.75rem 1.5rem
    Border radius: 6px
    Text decoration: none
    Font weight: 600
    Background: #f59e0b (amber)
    Color: white
    Transition: transform 0.2s
    Hover: transform translateY(-2px)

Mobile Menu Button:
  Display: none (desktop)
  Display: flex (mobile, max-width: 1024px)
  Flex direction: column
  Gap: 4px
  Background: none
  Border: none
  Cursor: pointer
  Padding: 0.5rem

  Menu bars:
    Width: 25px
    Height: 3px
    Background: white
    Transition: all 0.3s
```

---

## 🔽 FOOTER (.seo-footer-premium)

```
Background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%)
Color: white
Padding: 3rem 0 1.5rem (60px 0 24px)
Margin top: 4rem

Container:
  Max width: 1400px
  Margin: 0 auto
  Padding: 0 2rem
```

### Trust Badges Section
```
Display: grid
Grid columns: repeat(auto-fit, minmax(250px, 1fr))
Gap: 2rem
Margin bottom: 3rem
Padding bottom: 2rem
Border bottom: 1px solid rgba(255,255,255,0.1)

Badge item:
  Display: flex
  Align items: center
  Gap: 1rem

Badge icon:
  Font size: 2rem

Badge text strong:
  Display: block
  Font size: 1rem
  Margin bottom: 0.25rem

Badge text span:
  Font size: 0.875rem
  Opacity: 0.8
```

### Main Footer Content
```
Display: grid
Grid columns: repeat(auto-fit, minmax(200px, 1fr))
Gap: 2rem
Margin bottom: 2rem

Column:
  Heading:
    Font size: 1.125rem
    Margin bottom: 1rem
    Font weight: 600

  Links list:
    List style: none
    Padding: 0
    Margin: 0

  Links li:
    Margin bottom: 0.5rem

  Links a:
    Color: rgba(255,255,255,0.8)
    Text decoration: none
    Font size: 0.95rem
    Transition: color 0.2s
    Hover: color white
```

### Contact Box
```
Margin bottom: 1.5rem

Contact item:
  Margin bottom: 1rem
  Font size: 0.95rem
  Line height: 1.6

Contact link:
  Color: #93c5fd (light blue)
  Text decoration: none
  Hover: color #60a5fa, text-decoration underline
```

### Footer CTA Button
```
Display: inline-flex
Align items: center
Gap: 0.75rem
Background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Color: white
Padding: 1rem 2rem
Border radius: 8px
Text decoration: none
Font weight: 600
Transition: transform 0.2s
Hover: transform translateY(-2px)
```

### Footer Bottom
```
Margin top: 2rem
Padding top: 1.5rem
Border top: 1px solid rgba(255,255,255,0.1)

Bottom content:
  Display: flex
  Justify content: space-between
  Align items: center
  Flex wrap: wrap
  Gap: 1rem

Copyright:
  Font size: 0.875rem
  Opacity: 0.8
  Margin: 0

Separator:
  Margin: 0 0.5rem

Tagline:
  Font size: 0.875rem
  Opacity: 0.8
```

---

## 📱 RESPONSIVE BREAKPOINTS

### Desktop
```
Max width: 1400px
Header: full visible nav, trust, CTA
Sidebar: 350px visible
Grid gap: 3rem
Blog main padding: 3rem
```

### Tablet (max-width: 1024px)
```
Blog wrapper: single column (sidebar hidden or stacked)
Header nav: hidden (mobile menu shows)
Header trust: hidden
Header CTA: flex-direction column, gap 0.5rem
Header CTA buttons: padding 0.5rem 1rem, font-size 0.9rem
Mobile menu button: display flex
```

### Mobile (max-width: 768px)
```
Blog main padding: 1.5rem
Footer trust badges: grid-template-columns 1fr
Footer main content: grid-template-columns 1fr
Footer bottom content: flex-direction column, text-align center
Header container gap: 1rem
Header logo font size: smaller
All paddings/margins: reduced
```

---

## 🎬 ANIMATIONS & TRANSITIONS

### Hover Effects
```
Default transition: transform 0.2s, color 0.2s
Transform on hover: translateY(-2px) (slight lift)
Color transition: smooth 0.2s ease
```

### CTA Box Pattern Animation
```
Animation name: movePattern
Duration: 20s
Timing: linear
Iteration: infinite
Background shift: 40px horizontal
```

### Progress Bar
```
Position: fixed, top 0
Height: 4px
Background: gradient (#2196f3 → #03a9f4 → #00bcd4)
Updates: on scroll event
Width: percentage of page scrolled
```

---

## 🔗 Z-INDEX HIERARCHY

- **9999**: Reading progress bar (top layer)
- **1000**: Sticky header (below progress)
- **1**: Default stacking context
- **0**: Background elements

---

## 📊 SIZING CONSTANTS

- **Border radius**: 8px (standard), 6px (buttons)
- **Shadow**: `0 2px 8px rgba(0,0,0,0.1)` (standard)
- **Line height**: 1.8 (body), 1.2 (headings)
- **Max content width**: 1400px
- **Sidebar width**: 350px
- **Mobile menu bar height**: 3px
- **Mobile menu bar width**: 25px
- **Mobile menu gap**: 4px

---

## ⚠️ CRITICAL IMPLEMENTATION RULES

1. **CSS Files Referenced**: Use EXTERNAL CSS files only (no embedded styles except footer)
   - `../../css/blog-premium.css` (from _drafts/day-X/)
   - `../../css/header-optimized.css` (from _drafts/day-X/)

2. **Relative Paths**: Files in `blog/_drafts/day-X/` need TWO levels up (`../../`)

3. **Footer Exception**: Inline `<style>` tag ONLY for footer-specific overrides

4. **Header HTML**: Copy EXACTLY from premium-blog-example.html (no modifications)

5. **Fonts**: Must include both Fredoka and Rubik from Google Fonts CDN

6. **Responsive**: Mobile first, then enhance with max-width media queries

7. **Accessibility**: Proper heading hierarchy (h1→h2→h3), semantic HTML

---

**Design System Version**: 1.0
**Last Updated**: November 10, 2025
**Compatible with**: premium-blog-example.html template
