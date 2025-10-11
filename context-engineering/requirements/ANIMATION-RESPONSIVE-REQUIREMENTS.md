# 🎯 ANIMATION & RESPONSIVE DESIGN REQUIREMENTS

## FLOATING ICONS ANIMATION SYSTEM

### Core Requirements
- **All animations MUST work seamlessly on ALL devices**: PC, tablets, mobile
- **Performance first**: Animations should not impact page performance
- **Accessibility**: Respect prefers-reduced-motion settings
- **Safe boundaries**: Icons must never overlap important content or go off-screen

### Animation Amplitudes by Device

#### 🖥️ Desktop (>1400px)
- **Maximum movement**: 30px translation
- **Rotation**: up to 25 degrees
- **Scale**: 1.0 to 1.15
- **Full animation complexity**

#### 💻 Laptop/Small Desktop (1024px - 1400px)
- **Maximum movement**: 20px translation
- **Rotation**: up to 20 degrees
- **Scale**: 1.0 to 1.10
- **Slightly reduced complexity**

#### 📱 Tablet (768px - 1024px)
- **Maximum movement**: 12px translation
- **Rotation**: up to 12 degrees
- **Scale**: 1.0 to 1.08
- **Moderate animation complexity**
- **Icon size**: 40px

#### 📱 Mobile (<768px)
- **Maximum movement**: 6px translation
- **Rotation**: up to 6 degrees
- **Scale**: 1.0 to 1.04
- **Minimal animation complexity**
- **Icon size**: 32px
- **Consider hiding some icons**

#### 📱 Small Mobile (<480px)
- **Maximum movement**: 3px translation
- **Rotation**: up to 3 degrees
- **Scale**: 1.0 to 1.02
- **Very subtle animations only**
- **Icon size**: 24px
- **Show only 2-3 essential icons**

### Icon Positioning Rules

#### Vertical Distribution
- **Left side icons**: All aligned at `left: 5%`
  - Icon 1: `top: 20%`
  - Icon 3: `top: 50%`
  - Icon 5: `top: 80%`

- **Right side icons**: All aligned at `right: 8%`
  - Icon 2: `top: 20%`
  - Icon 4: `top: 50%`
  - Icon 6: `top: 80%`

#### Safe Zones
- Never position icons closer than 5% from any edge
- Maintain at least 30% vertical spacing between icons
- Keep icons away from interactive elements (buttons, forms)

### Animation Types

#### 1. floatDiagonal
- Diagonal movement pattern
- Combines X and Y translation
- Includes rotation for dynamic feel

#### 2. floatCircular
- Circular/elliptical movement
- Full 360-degree rotation through animation
- Smooth scaling transitions

#### 3. floatWave
- Wave-like movement pattern
- Multiple keyframes for complex motion
- Varying rotation directions

### Performance Guidelines

1. **Use CSS transforms only** (no position animations)
2. **GPU acceleration**: Use `transform: translateZ(0)` or `will-change: transform`
3. **Limit simultaneous animations**: Max 6 icons animating at once
4. **Stagger animation delays**: Prevent all icons moving in sync
5. **Duration range**: 25-32 seconds for smooth, non-distracting movement

### Accessibility Considerations

```css
@media (prefers-reduced-motion: reduce) {
    .floating-icon {
        animation: none !important;
        transform: none !important;
    }
}
```

### Testing Checklist

- [ ] Test on real devices, not just browser DevTools
- [ ] Verify no horizontal scroll on any device
- [ ] Check animation performance (60fps target)
- [ ] Ensure icons don't overlap text on any breakpoint
- [ ] Validate touch targets aren't obscured
- [ ] Test with slow network conditions
- [ ] Verify animations work in all major browsers

### Browser Support

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (check -webkit prefixes)
- Mobile browsers: Optimized for reduced complexity

### Common Issues to Avoid

1. **Don't use percentage-based translations** - they scale differently
2. **Avoid fixed pixel positions** for responsive layouts
3. **Don't animate position properties** - use transform only
4. **Prevent z-index conflicts** with navigation or CTAs
5. **Test overflow hidden** doesn't cut off animations unexpectedly

### Implementation Example

```css
/* Base animation with responsive scaling */
.floating-icon {
    --movement-scale: 1; /* Default for desktop */
}

@media (max-width: 1400px) {
    .floating-icon { --movement-scale: 0.7; }
}

@media (max-width: 1024px) {
    .floating-icon { --movement-scale: 0.4; }
}

@media (max-width: 768px) {
    .floating-icon { --movement-scale: 0.2; }
}

/* Use CSS custom property in animations */
@keyframes float {
    25% {
        transform: translate(
            calc(30px * var(--movement-scale)),
            calc(-30px * var(--movement-scale))
        );
    }
}
```

---

**Remember**: The goal is subtle, professional movement that enhances the design without distracting from content or impacting performance.
