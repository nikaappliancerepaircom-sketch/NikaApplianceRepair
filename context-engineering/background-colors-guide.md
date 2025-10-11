# Background Colors Style Guide

## Standardized Background Colors

The website uses only these background colors for consistency:

### 1. **White Background** (`--bg-white: #FFFFFF`)
- Use for: Main content sections, cards, forms
- Class: `.bg-white`
- Example sections: Services, About, Booking

### 2. **Light Gray Background** (`--bg-light-gray: #F8F9FA`)
- Use for: Alternating sections to create visual separation
- Class: `.bg-light-gray`
- Example sections: FAQ, Areas, Testimonials, Brands

### 3. **Blue Gradient Background** (`--bg-blue-gradient`)
- Gradient: `linear-gradient(135deg, #1976D2 0%, #2196F3 50%, #1565C0 100%)`
- Use for: Hero sections, CTA sections, Why Choose Us
- Class: `.bg-blue-gradient`
- Automatically sets white text color

### 4. **Dark Blue Gradient Background** (`--bg-dark-blue`)
- Gradient: `linear-gradient(135deg, #1A237E 0%, #3949AB 100%)`
- Use for: Footer, special sections
- Class: `.bg-dark-blue`
- Automatically sets white text color

## Usage Pattern

Follow this pattern for consistent page layout:

1. **Header**: White background
2. **Hero Section**: Blue gradient or white
3. **Section 1**: White background
4. **Section 2**: Light gray background
5. **Section 3**: White background
6. **Section 4**: Light gray background
7. **CTA Section**: Blue gradient
8. **Footer**: Dark blue gradient

## Implementation

### CSS Classes
```css
.bg-white {
    background: var(--bg-white) !important;
}

.bg-light-gray {
    background: var(--bg-light-gray) !important;
}

.bg-blue-gradient {
    background: var(--bg-blue-gradient) !important;
    color: var(--white) !important;
}

.bg-dark-blue {
    background: var(--bg-dark-blue) !important;
    color: var(--white) !important;
}
```

### HTML Usage
```html
<!-- White section -->
<section class="services-section bg-white">
    <!-- Content -->
</section>

<!-- Light gray section -->
<section class="faq-section bg-light-gray">
    <!-- Content -->
</section>

<!-- Blue gradient section -->
<section class="hero-section bg-blue-gradient">
    <!-- Content -->
</section>
```

## Rules

1. **NO custom background colors** - Use only the 4 defined backgrounds
2. **Alternate between white and light gray** for content sections
3. **Use gradients sparingly** - Only for hero, CTA, and footer
4. **Test contrast** - Ensure text is readable on all backgrounds
5. **Be consistent** - Same type of content should use same background

## Examples

### Good ✅
```html
<section class="testimonials-section bg-light-gray">
<section class="services-section bg-white">
<section class="why-choose-section bg-blue-gradient">
```

### Bad ❌
```html
<section style="background: #e0e0e0;">
<section style="background: linear-gradient(...);">
<section style="background-color: rgb(240,240,240);">
```

## Accessibility

- White text on blue gradients must have sufficient contrast
- Use `color: #666` for body text on light backgrounds
- Use `color: #1A237E` for headings on light backgrounds
- Always test with contrast checkers