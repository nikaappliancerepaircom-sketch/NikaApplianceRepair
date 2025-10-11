# Mobile Popup Optimization Guide

## 📱 Mobile-First Popup Strategy

### Mobile-Specific Triggers
```javascript
const mobilePopupRules = {
    // Thumb-zone interaction
    scrollThreshold: 150, // pixels - one thumb swipe
    
    // Shorter attention span
    timeDelay: 15000, // 15 seconds vs 30 on desktop
    
    // Touch-specific events
    swipeUp: showBottomSheetPopup,
    swipeDown: dismissPopup,
    
    // Network-aware
    slowConnection: disableAnimations
};
```

### Mobile Popup Types

#### 1. BOTTOM SHEET POPUP
```css
.mobile-bottom-sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    transform: translateY(100%);
    border-radius: 20px 20px 0 0;
    padding-bottom: env(safe-area-inset-bottom);
    max-height: 70vh;
    animation: slideUp 0.3s ease;
}
```

#### 2. FLOATING ACTION POPUP
```html
<div class="fab-popup">
    <div class="fab-badge">Tech Available!</div>
    <button class="fab-main">
        📞
    </button>
    <div class="fab-options">
        <button class="fab-option">Call Now</button>
        <button class="fab-option">Text Us</button>
    </div>
</div>
```