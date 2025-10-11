# Conversion-Focused Popup Templates

## 📞 Call-Focused Popups

### Exit Intent - Call Version
```html
<div class="popup-content call-focused">
    <h2>🛑 Your Appliance Won't Fix Itself!</h2>
    <div class="urgency-message">
        <p><strong>Leave now = Another day without [appliance]</strong></p>
        <p>Call us now = Fixed TODAY!</p>
    </div>
    
    <div class="offer-box">
        <span class="discount">$50 OFF</span>
        <span class="condition">When You Call Now</span>
    </div>
    
    <a href="tel:5551234567" class="cta-call">
        📞 (555) 123-4567
        <span class="sub-text">Technician Standing By</span>
    </a>
    
    <button class="secondary-option" onclick="showBookingForm()">
        Prefer to Book Online?
    </button>
</div>
```

### Mobile Touch-to-Call Popup
```html
<div class="mobile-call-popup bottom-sheet">
    <div class="drag-handle"></div>
    <div class="tech-availability">
        <div class="live-dot"></div>
        <span>Technician Available Now!</span>
    </div>
    
    <h3>Why Keep Reading?</h3>
    <p>Get answers in 30 seconds with a quick call</p>
    
    <a href="tel:5551234567" class="big-call-button">
        <div class="phone-icon">📞</div>
        <div class="call-text">
            <span class="main">Tap to Call</span>
            <span class="number">(555) 123-4567</span>
        </div>
    </a>
    
    <div class="trust-points">
        ✓ Free Quote ✓ No Obligation ✓ 90-Day Warranty
    </div>
</div>
```
## 📅 Booking-Focused Popups

### Time-Based Helper - Booking Version
```html
<div class="popup-content booking-focused">
    <div class="helper-header">
        <img src="/assets/images/technician-avatar.png" alt="Mike" class="tech-avatar">
        <div class="helper-text">
            <h3>Need Help Deciding?</h3>
            <p>Hi, I'm Mike. I can get your [appliance] fixed today!</p>
        </div>
    </div>
    
    <div class="quick-booking">
        <h4>Book Your Repair in 60 Seconds</h4>
        <form class="mini-booking-form">
            <input type="text" placeholder="Your Name" required>
            <input type="tel" placeholder="Phone Number" required>
            <select required>
                <option>Select Time</option>
                <option>Next Available (1-2 hours)</option>
                <option>This Afternoon</option>
                <option>Tomorrow Morning</option>
            </select>
            <button type="submit">Book Now →</button>
        </form>
    </div>
    
    <a href="tel:5551234567" class="alternative-cta">
        Prefer to call? (555) 123-4567
    </a>
</div>
```

### Form Abandonment - Callback Version
```html
<div class="popup-content callback-focused">
    <h3>Having Trouble With The Form?</h3>
    <p>No problem! We'll call you instead.</p>
    
    <div class="callback-form">
        <input type="tel" 
               placeholder="Your Phone Number" 
               class="callback-phone"
               autofocus>
        
        <button class="callback-button">
            Call Me Back in 5 Minutes →
        </button>
    </div>
    
    <div class="callback-benefits">
        <div class="benefit">⚡ Faster than filling forms</div>
        <div class="benefit">💬 Speak to a real person</div>
        <div class="benefit">📋 We'll handle the details</div>
    </div>
</div>
```