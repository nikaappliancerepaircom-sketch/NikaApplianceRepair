# Smart Popup System Guide

## 🎯 High-Converting Popup Strategy for Appliance Repair

### POPUP TYPES & THEIR PURPOSES

#### 1. EXIT INTENT POPUP
**Trigger**: Mouse moves to close tab/back button
**Psychology**: Loss aversion + Last chance urgency
**Message**: "Wait! Your appliance still needs repair!"

```javascript
// Exit Intent Detection
document.addEventListener('mouseout', (e) => {
    if (e.clientY <= 0 && !hasShownExitPopup) {
        showExitPopup();
    }
});
```

**Content Formula**:
```
HEADLINE: "Before You Go! 🛑"
SUBHEAD: "Get $50 OFF Same-Day Repair"
BODY: "Your [detected appliance] problem won't fix itself. 
       We have a technician available in [user location] right now."
CTA: "Claim $50 Discount → [Phone Icon]"
SECONDARY: "Maybe later" (small text)
```

#### 2. TIME-BASED ENGAGEMENT POPUP
**Trigger**: User on page for 30+ seconds
**Psychology**: Reciprocity + Helpful intervention
**Message**: "Need help deciding?"

```javascript
// Time-based trigger
setTimeout(() => {
    if (scrollDepth > 25 && !hasEngaged) {
        showHelpPopup();
    }
}, 30000);
```
#### 3. SCROLL-TRIGGERED VALUE POPUP
**Trigger**: 50% scroll depth on service pages
**Psychology**: Pattern interrupt + Value proposition
**Message**: "Most people don't know this..."

**Content Options**:
- "Fun Fact: 73% of appliance 'breakdowns' are simple fixes"
- "Did you know? Repair costs 80% less than replacement"
- "Secret: Calling before 2PM gets same-day service"

#### 4. ABANDONMENT PREVENTION POPUP
**Trigger**: Form started but not submitted after 10 seconds
**Psychology**: Completion bias + Assistance
**Message**: "Having trouble? We can help!"

```javascript
// Form abandonment detection
formField.addEventListener('focus', startFormTimer);
formField.addEventListener('blur', () => {
    if (!formSubmitted && timeOnForm > 10) {
        showAssistancePopup();
    }
});
```

#### 5. MOBILE-SPECIFIC CLICK-TO-CALL POPUP
**Trigger**: Mobile user + scrolled 25% + not called
**Psychology**: Convenience + Urgency
**Message**: "Tap to Call Now - Tech Available!"

```html
<div class="mobile-call-popup">
    <div class="tech-available-badge">🟢 Tech Available Now</div>
    <h3>Skip the Forms - Call Directly!</h3>
    <a href="tel:5551234567" class="pulse-button">
        📞 (555) 123-4567
    </a>
    <p class="arrival-time">Average arrival: 67 minutes</p>
</div>
```
### 🧠 PSYCHOLOGICAL TRIGGERS FOR POPUPS

#### 1. SOCIAL PROOF POPUP
**Trigger**: 15 seconds on pricing page
**Content**: "17 people in [City] booked repair in last 2 hours"

```javascript
const socialProofPopup = {
    headline: "You're Not Alone!",
    body: `${recentBookings} neighbors in ${userCity} chose us today`,
    reviews: showRecentReview(),
    cta: "Join Them →"
};
```

#### 2. SCARCITY POPUP
**Trigger**: Viewing emergency service page
**Content**: Real-time technician availability

```html
<div class="scarcity-popup">
    <div class="live-indicator">🔴 LIVE UPDATE</div>
    <h3>Only 2 Emergency Slots Left Today</h3>
    <div class="tech-grid">
        <div class="tech-slot booked">9:00 AM ❌</div>
        <div class="tech-slot booked">11:00 AM ❌</div>
        <div class="tech-slot available">1:00 PM ✅</div>
        <div class="tech-slot available">3:00 PM ✅</div>
        <div class="tech-slot booked">5:00 PM ❌</div>
    </div>
    <button class="cta-urgent">Claim Your Slot →</button>
</div>
```

#### 3. PROBLEM AGITATION POPUP
**Trigger**: Reading about specific appliance issue
**Psychology**: Pain point amplification + Solution

```javascript
// Dynamic problem-specific popup
if (pageContent.includes('refrigerator not cooling')) {
    showPopup({
        icon: '⚠️',
        headline: 'Food Spoils in Just 4 Hours!',
        body: 'FDA warns: Food above 40°F becomes unsafe quickly',
        cost: 'Average family loses $250 in groceries',
        cta: 'Prevent Food Loss - Call Now'
    });
}
```
### 📊 SMART TARGETING RULES

#### Behavioral Targeting Matrix
```javascript
const popupRules = {
    // New visitors
    firstTimeVisitor: {
        delay: 45000, // 45 seconds
        popup: 'welcomeDiscount',
        message: 'First-Time Customer? Save $30!'
    },
    
    // Returning visitors
    returningVisitor: {
        condition: 'visitCount > 2 && !converted',
        popup: 'urgencyReminder',
        message: 'Still having appliance trouble?'
    },
    
    // High-intent behavior
    highIntent: {
        condition: 'viewedPricing && viewedServices',
        popup: 'closeTheDeal',
        message: 'Ready to book? Here\'s $50 off!'
    },
    
    // Mobile users
    mobileUser: {
        condition: 'isMobile && scrollDepth > 30',
        popup: 'clickToCall',
        showAfter: 20000
    }
};
```

#### Smart Suppression Rules
- Never show popups on thank you pages
- Max 1 popup per page visit
- 7-day cookie for dismissed popups
- Respect user's "Don't show again" choice
- No popups during form filling
- Disable on slow connections

### 🎨 POPUP DESIGN BEST PRACTICES

#### Visual Hierarchy
```css
.smart-popup {
    /* Attention-grabbing but not annoying */
    max-width: 480px;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    animation: slideInUp 0.4s ease;
}

.popup-headline {
    font-size: 28px;
    font-weight: 800;
    color: var(--urgent-red);
    margin-bottom: 12px;
}

.popup-cta {
    background: var(--primary);
    font-size: 20px;
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 700;
    animation: pulse 2s infinite;
}
```# Smart Popup System - 2 Popup Maximum Strategy

## 🎯 Conversion-Focused Popup Strategy

### Core Rules
1. **Maximum 2 popups per user session** (stored in sessionStorage)
2. **Never overlap** - One popup at a time
3. **30-second minimum gap** between popups
4. **Goal: Phone call or online booking** (no email capture)
5. **Smart suppression** - No popups if already converted

### Popup Priority System

```javascript
const popupPriority = {
    // First Popup - Highest Impact
    exitIntent: {
        priority: 1,
        trigger: 'mouseout',
        message: 'Wait! Get $50 OFF Right Now',
        cta: ['Call Now', 'Book Online'],
        suppressIf: ['hasBooked', 'hasCalled', 'onThankYouPage']
    },
    
    // Second Popup - Contextual
    contextual: {
        priority: 2,
        trigger: determineSecondPopup(),
        delay: 30000, // 30 seconds after first popup closes
        options: [
            'timeBasedHelper',
            'scrollBasedOffer',
            'mobileCallPrompt',
            'formAbandonment'
        ]
    }
};
```

### Implementation Logic

```javascript
class SmartPopupManager {
    constructor() {
        this.maxPopups = 2;
        this.popupsShown = this.getPopupHistory();
        this.lastPopupTime = null;
        this.minimumGap = 30000; // 30 seconds
        this.hasConverted = this.checkConversion();
    }