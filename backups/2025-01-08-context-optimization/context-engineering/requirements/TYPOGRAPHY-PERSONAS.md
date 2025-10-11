# 📐 TYPOGRAPHY GUIDELINES FOR CUSTOMER PERSONAS

## 🎯 FONT SIZE RECOMMENDATIONS BY PERSONA

### 👩 FOR "BUSY SARAH" (35-45 years)
**Mobile-first, quick scanning, efficiency**

#### Base Font Sizes
```css
/* Body text */
body {
    font-size: 16px; /* Base size - comfortable mobile reading */
    line-height: 1.6;
}

/* Headings */
h1 { font-size: 2.5rem; }  /* 40px - Bold but not overwhelming */
h2 { font-size: 2rem; }    /* 32px */
h3 { font-size: 1.5rem; }  /* 24px */
h4 { font-size: 1.25rem; } /* 20px */

/* CTAs - Make them obvious! */
.cta-primary, .cta-secondary {
    font-size: 1.125rem; /* 18px - Easy to tap on mobile */
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* Mobile (her primary device) */
@media (max-width: 768px) {
    body { font-size: 16px; } /* Keep readable */
    h1 { font-size: 2rem; }   /* 32px */
    h2 { font-size: 1.75rem; } /* 28px */
    .cta-primary { font-size: 1rem; } /* 16px but bold */
}
```

#### Key Points for Sarah:
- ✅ **16px minimum** body text (she's multitasking)
- ✅ **Large tap targets** (48px minimum height)
- ✅ **Bold CTAs** that stand out
- ✅ **Good contrast** for quick reading
- ✅ **Short paragraphs** with 1.6 line height

---

### 👴 FOR "CAUTIOUS ROBERT" (55-70 years)
**Larger text, high contrast, clear hierarchy**

#### Base Font Sizes
```css
/* Body text - LARGER for aging eyes */
body {
    font-size: 18px; /* Increased base size */
    line-height: 1.8; /* More spacing */
}

/* Headings - Clear hierarchy */
h1 { font-size: 3.5rem; }  /* 56px - Very clear */
h2 { font-size: 2.5rem; }  /* 40px */
h3 { font-size: 1.75rem; } /* 28px */
h4 { font-size: 1.5rem; }  /* 24px */

/* Important info */
.phone-number {
    font-size: 1.5rem; /* 24px - MUST be easy to read */
    font-weight: 700;
}

/* Pricing */
.price {
    font-size: 1.75rem; /* 28px - No squinting! */
    font-weight: 700;
    color: #2ECC71; /* High contrast green */
}

/* Desktop (his primary device) */
@media (min-width: 1024px) {
    body { font-size: 20px; } /* Even larger on desktop */
    .main-nav a { font-size: 1.125rem; } /* 18px nav links */
}
```

#### Key Points for Robert:
- ✅ **18-20px minimum** body text
- ✅ **High contrast** (WCAG AAA if possible)
- ✅ **Larger phone numbers** (24px+)
- ✅ **Clear pricing** (28px+)
- ✅ **Sans-serif fonts** (easier to read)

---

### 🏠 FOR "INVESTMENT IVAN" (40-55 years)
**Professional, scannable, data-focused**

#### Base Font Sizes
```css
/* Body text - Professional */
body {
    font-size: 16px;
    line-height: 1.6;
}

/* Headings - Business-like */
h1 { font-size: 2.75rem; } /* 44px */
h2 { font-size: 2.25rem; } /* 36px */
h3 { font-size: 1.5rem; }  /* 24px */
h4 { font-size: 1.25rem; } /* 20px */

/* Data/Stats */
.stat-number {
    font-size: 2.5rem; /* 40px - Impact */
    font-weight: 700;
}

/* Tables/Lists */
table {
    font-size: 0.875rem; /* 14px - Compact data */
}

.property-list {
    font-size: 0.9375rem; /* 15px */
}

/* Business CTAs */
.business-cta {
    font-size: 1rem; /* 16px */
    text-transform: none; /* Professional, not shouty */
}
```

#### Key Points for Ivan:
- ✅ **16px standard** body text
- ✅ **Compact data views** (14-15px for tables)
- ✅ **Large numbers** for stats (40px+)
- ✅ **Professional tone** (no all-caps)
- ✅ **Efficient layout** (more content visible)

---

## 🎨 UNIVERSAL ACCESSIBILITY RULES

### Minimum Sizes (WCAG Compliant)
```css
/* Never go below these */
body { font-size: 16px; } /* Absolute minimum */
.small-text { font-size: 0.875rem; } /* 14px minimum */
.fine-print { font-size: 0.75rem; } /* 12px only for legal */

/* Touch targets */
button, .cta {
    min-height: 48px; /* Touch friendly */
    min-width: 48px;
}
```

### Responsive Scaling
```css
/* Fluid typography */
html {
    font-size: clamp(16px, 2.5vw, 20px);
}

h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);
}
```

---

## 📱 IMPLEMENTATION STRATEGY

### 1. **CSS Variables for Easy Adjustment**
```css
:root {
    /* Base sizes */
    --font-size-base: 16px;
    --font-size-large: 18px;
    --font-size-xl: 20px;
    
    /* Scale for different personas */
    --scale-sarah: 1;
    --scale-robert: 1.125; /* 12.5% larger */
    --scale-ivan: 1;
}

/* Apply based on user preference */
body.prefer-larger-text {
    font-size: calc(var(--font-size-base) * var(--scale-robert));
}
```

### 2. **JavaScript Font Size Toggle**
```javascript
// Let users adjust font size
function adjustFontSize(persona) {
    const root = document.documentElement;
    switch(persona) {
        case 'sarah':
            root.style.fontSize = '16px';
            break;
        case 'robert':
            root.style.fontSize = '18px';
            break;
        case 'ivan':
            root.style.fontSize = '16px';
            break;
    }
}
```

### 3. **Testing Checklist**
- [ ] Test at 200% browser zoom (for Robert)
- [ ] Test on iPhone SE (small screen for Sarah)
- [ ] Test data tables at various sizes (for Ivan)
- [ ] Verify all text passes WCAG AA contrast
- [ ] Check touch target sizes on mobile

---

## 🎯 QUICK REFERENCE

| Element | Sarah (Mobile) | Robert (Desktop) | Ivan (Business) |
|---------|---------------|------------------|-----------------|
| Body | 16px | 18-20px | 16px |
| H1 | 32-40px | 56px | 44px |
| H2 | 28-32px | 40px | 36px |
| CTA | 16-18px bold | 18-20px bold | 16px medium |
| Phone # | 18px | 24px+ | 18px |
| Price | 20px | 28px | 24px |
| Nav | 16px | 18px | 16px |
| Tables | 14px | 16px | 14px |

---

**Remember**: These are starting points. Always test with real users and be ready to adjust based on feedback!
