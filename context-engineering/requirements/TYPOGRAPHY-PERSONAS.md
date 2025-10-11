# 📐 TYPOGRAPHY GUIDELINES FOR CUSTOMER PERSONAS

## 🎯 UPDATED: LARGER TEXT BY DEFAULT

### Important Change (January 2025)
We've made larger text the default for ALL users. This ensures:
- Better readability for everyone
- No need for toggle buttons
- Consistent experience
- Better accessibility out of the box

## 🎯 NEW DEFAULT FONT SIZES

### Base Settings
```css
/* Default for all users */
html {
    font-size: 18px; /* Increased from 16px */
}

body {
    font-size: 1rem; /* 18px */
    line-height: 1.7; /* Increased for readability */
}

/* Headings */
h1 { font-size: 3.5rem; }  /* 63px */
h2 { font-size: 2.5rem; }  /* 45px */
h3 { font-size: 2rem; }    /* 36px */
h4 { font-size: 1.5rem; }  /* 27px */

/* CTAs */
.cta-primary, .cta-secondary {
    font-size: 1.25rem; /* 22.5px */
    min-height: 56px;
    padding: 1.25rem 2.5rem;
}

/* Phone numbers */
.phone-large {
    font-size: 1.5rem; /* 27px */
}
```

### Benefits for Each Persona

#### 👩 Busy Sarah (35-45)
- 18px base is still fast to scan
- Larger touch targets (56px buttons)
- Clear hierarchy with bigger headings
- Mobile-friendly sizing

#### 👴 Cautious Robert (55-70)  
- No need to find toggle button
- 18px base comfortable for aging eyes
- 27px phone numbers easy to read
- High contrast maintained

#### 🏠 Investment Ivan (40-55)
- Professional appearance maintained
- Data tables still compact
- Clear headings for scanning
- Business-appropriate sizing

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
