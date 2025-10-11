# Popup Analytics & Optimization Guide

## 📊 Key Metrics to Track

### Primary KPIs
1. **Conversion Rate**: Popup shown → Action taken
2. **Engagement Rate**: Interactions with popup
3. **Bounce Rate Impact**: Before/after popup implementation
4. **Revenue Attribution**: Sales from popup interactions

### Tracking Implementation
```javascript
// Google Analytics 4 Events
const trackPopupEvent = (action, label, value = null) => {
    gtag('event', 'popup_interaction', {
        'popup_action': action,
        'popup_type': label,
        'popup_value': value,
        'time_on_page': Math.floor((Date.now() - pageLoadTime) / 1000),
        'scroll_depth': getCurrentScrollDepth(),
        'device_type': getDeviceType()
    });
};

// Track popup display
trackPopupEvent('display', 'exit_intent');

// Track popup interaction
trackPopupEvent('click', 'cta_button', 'call_now');

// Track popup dismissal
trackPopupEvent('dismiss', 'close_button');
```

### Conversion Tracking Setup
```javascript
// Phone call from popup
<a href="tel:5551234567" 
   onclick="trackPopupEvent('conversion', 'phone_call', 'exit_popup')">
   
// Form submission from popup
form.addEventListener('submit', () => {
    trackPopupEvent('conversion', 'form_submit', 'welcome_popup');
});
```