# 🎨 UNIFIED DESIGN SYSTEM
**Nika Appliance Repair - Single Source of Truth**

**Quick Summary:** 2 fonts • 2 button types • 3 backgrounds • Unified grays

---

## 📋 QUICK REFERENCE

| Element | Rule | Value |
|---------|------|-------|
| **Heading Font** | Fredoka only | `var(--font-heading)` |
| **Body Font** | Rubik only | `var(--font-body)` |
| **Booking Buttons** | Green gradient | `#27AE60 → #2ECC71` |
| **Call Buttons** | Purple gradient | `#7c3aed → #8b5cf6` |
| **Backgrounds** | 3 options only | White, Light Gray, Blue Gradient |
| **Body Text** | Unified grays | `#495057` on white, `#ffffff` on blue |

---

## 📝 TYPOGRAPHY

### Fonts (2 Only)
```css
--font-heading: 'Fredoka', cursive;    /* H1-H6 */
--font-body: 'Rubik', sans-serif;      /* Body text */
```

✅ **USE:** Only Fredoka + Rubik
❌ **AVOID:** Any other fonts (Arial, Georgia, Times New Roman, etc.)

### Heading Colors by Background
```css
/* White background → Blue gradient headings */
h1, h2, h3 {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Blue background → White headings */
.section-blue h2 {
    color: white !important;
    background: none !important;
}
```

### Font Sizes
| Variable | Size | Usage |
|----------|------|-------|
| `--text-xs` | 12px | Labels |
| `--text-sm` | 14px | Small text |
| `--text-base` | 16px | Body text |
| `--text-lg` | 18px | Emphasis |
| `--text-xl` | 20px | Subheadings |
| `--text-2xl` | 24px | H4 |
| `--text-3xl` | 30px | H3 |
| `--text-4xl` | 36px | H2 |
| `--text-5xl` | 48px | H1 |

✅ **USE:** `font-size: var(--text-xl)`
❌ **AVOID:** `font-size: 1.5rem` (hardcoded)

### Text Colors
| Variable | Color | Usage |
|----------|-------|-------|
| `--text-primary` | #212529 | Headings on white |
| `--text-body` | #495057 | Paragraphs |
| `--text-muted` | #6c757d | Secondary info |
| `--text-on-blue` | #ffffff | Text on blue backgrounds |

---

## 🎨 COLORS

### Brand Colors
| Color | Variable | Hex | Usage |
|-------|----------|-----|-------|
| **Blue** | `--primary-blue` | #2196F3 | Main brand |
| **Blue Dark** | `--primary-blue-dark` | #1976D2 | Gradients |
| **Yellow** | `--primary-yellow` | #FFD600 | Accents |
| **Green** | `--bright-green` | #28a745 | Booking buttons |
| **Purple** | `--purple` | #7c3aed | Call buttons |

### Unified Grays
| Variable | Hex | Usage |
|----------|-----|-------|
| `--gray-900` | #212529 | Headings |
| `--gray-700` | #495057 | Body text |
| `--gray-500` | #6c757d | Muted text |
| `--gray-300` | #dee2e6 | Borders |
| `--gray-100` | #f8f9fa | Light backgrounds |

### Backgrounds (3 Only)
```css
--bg-white: #ffffff;              /* White sections */
--bg-light: #f8f9fa;              /* Light gray alternating */
--bg-blue-gradient: linear-gradient(135deg, #1976D2 0%, #2196F3 50%, #1565C0 100%);
```

✅ **USE:** Only these 3 background options
❌ **AVOID:** Any other background colors

---

## 🔘 BUTTONS (2 Types Only)

### Type 1: Booking (Green)
**Gradient:** `#27AE60 → #2ECC71`

**Classes:**
- `.cta-primary`
- `.countdown-cta`
- `.header-book-btn`
- `.submit-btn`

**Use for:** "Book Service", "Book Now", "Schedule Service", "Submit"

### Type 2: Call (Purple)
**Gradient:** `#7c3aed → #8b5cf6`

**Classes:**
- `.cta-secondary`
- `.emergency-phone-btn`
- `.footer-cta-btn`

**Use for:** "Call Now", "Call 437-747-6737", phone links

### Required Button Styles
```css
/* All buttons must have: */
border-radius: 50px;           /* Rounded */
text-transform: uppercase;      /* UPPERCASE */
font-weight: 700;              /* Bold */
padding: 1.25rem 2.5rem;       /* Consistent spacing */
box-shadow: 0 8px 20px rgba(); /* Shadow */
```

✅ **DO:** Green for booking, Purple for calls, rounded corners
❌ **NEVER:** Blue buttons, red buttons, square corners, lowercase text

---

## 📏 SPACING

### Spacing Scale
| Variable | Size | Pixels |
|----------|------|--------|
| `--space-1` | 0.25rem | 4px |
| `--space-2` | 0.5rem | 8px |
| `--space-3` | 0.75rem | 12px |
| `--space-4` | 1rem | 16px |
| `--space-6` | 1.5rem | 24px |
| `--space-8` | 2rem | 32px |
| `--space-12` | 3rem | 48px |
| `--space-16` | 4rem | 64px |

### Semantic Spacing
- `--section-padding: 3rem` (sections)
- `--card-padding: 1.5rem` (cards)
- `--button-padding: 0.75rem 1.5rem` (buttons)

✅ **USE:** `padding: var(--space-4)`
❌ **AVOID:** `padding: 1rem` (hardcoded)

---

## ✅ DO'S & ❌ DON'TS

| Category | ✅ DO | ❌ DON'T |
|----------|-------|----------|
| **Fonts** | Fredoka + Rubik only | Arial, Georgia, Times New Roman |
| **Font Sizes** | Use CSS variables | Hardcoded values |
| **Headings** | Blue gradient on white, white on blue | Black headings, random colors |
| **Backgrounds** | 3 options: white, light gray, blue gradient | Random background colors |
| **Buttons** | 2 types: green (booking), purple (call) | Blue, red, orange buttons |
| **Button Shape** | Rounded (50px border-radius) | Square corners |
| **Button Text** | UPPERCASE, bold (700) | lowercase, different styles |
| **Spacing** | CSS variables | Hardcoded values (13px, 27px) |
| **Colors** | Use design system palette | Colors outside palette |

---

## 📂 FILE STRUCTURE

### CSS Load Order (Critical!)
```html
1. design-system.css  ← MUST load first (variables)
2. style.css          ← General styles
3. cta-buttons.css    ← Button styles
4. All other CSS files
```

✅ **design-system.css** = Single source of truth for all variables
✅ **All other files** = Reference variables only
❌ **NEVER** define colors/fonts directly in other CSS files

---

## 🔧 HOW TO ADD NEW STYLES

### ✅ CORRECT
```css
/* 1. Add variable in design-system.css */
:root {
    --new-blue-light: #42A5F5;
}

/* 2. Use variable in other CSS files */
.my-class {
    color: var(--new-blue-light);
}
```

### ❌ WRONG
```css
/* Hardcoded color - BAD! */
.my-class {
    color: #42A5F5;  /* ❌ */
}
```

---

## 🎯 CHECKLIST: Adding New Styles

Before adding anything new, ask:

- [ ] Does it use Fredoka or Rubik?
- [ ] Does it use colors from design-system.css?
- [ ] Is it a green or purple button?
- [ ] Does it use spacing variables?

**If NO to any:** Modify design-system.css first, then use variables.

---

## 📊 IMPLEMENTATION STATUS

| Area | Status | Details |
|------|--------|---------|
| **Typography** | ✅ Complete | 2 fonts, size variables, unified headings |
| **Colors** | ✅ Complete | 3 backgrounds, unified grays, 2 button colors |
| **Buttons** | ✅ Complete | 6 CTA buttons (BMAD optimal), 2 types only |
| **Spacing** | ✅ Complete | Variables defined, semantic spacing |
| **CSS Files** | ✅ Complete | design-system.css loads first |

---

## 🚀 MAINTENANCE

### When Making Changes:
1. **Check design-system.css first** - does variable exist?
2. **Add variable if needed** - don't hardcode
3. **Use variable in component** - reference, don't duplicate
4. **Test on both backgrounds** - white and blue
5. **Verify button colors** - green or purple only

### Periodic Audits:
- [ ] Remove hardcoded colors from CSS files
- [ ] Replace hardcoded spacing with variables
- [ ] Remove duplicate button styles
- [ ] Verify CSS load order

---

**Version:** 1.0 | **Updated:** 2025-01-13 | **Status:** ✅ Active
