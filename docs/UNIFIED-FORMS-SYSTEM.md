# Unified Forms System

## 📋 Form Types & Implementations

### 1. QUICK QUOTE FORM (Hero/Sidebar)
**Purpose**: Fast lead capture with minimal friction
**Fields**: 3-4 maximum

```html
<form class="quick-quote-form" id="quickQuoteForm">
    <h3>Get Free Quote in 30 Seconds</h3>
    
    <!-- Name -->
    <div class="form-group">
        <input type="text" 
               name="name" 
               placeholder="Your Name" 
               required
               autocomplete="name">
        <span class="error-message"></span>
    </div>
    
    <!-- Phone -->
    <div class="form-group">
        <input type="tel" 
               name="phone" 
               placeholder="(555) 123-4567" 
               required
               pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
               autocomplete="tel">
        <span class="error-message"></span>
    </div>
    
    <!-- Appliance Type -->
    <div class="form-group">
        <select name="appliance" required>
            <option value="">Select Appliance</option>
            <option value="refrigerator">Refrigerator</option>
            <option value="washer">Washer</option>
            <option value="dryer">Dryer</option>
            <option value="dishwasher">Dishwasher</option>
            <option value="oven">Oven/Range</option>
            <option value="microwave">Microwave</option>
        </select>
        <span class="error-message"></span>
    </div>
    
    <!-- Submit -->
    <button type="submit" class="form-submit">
        Get Free Quote →
        <span class="loader" style="display:none;"></span>
    </button>
    
    <p class="form-disclaimer">
        ✓ No obligation ✓ 30-second response ✓ Same-day service
    </p>
</form>
```
### 2. DETAILED BOOKING FORM (Booking Page)
**Purpose**: Complete appointment scheduling
**Fields**: 6-8 fields with smart defaults

```html
<form class="booking-form" id="bookingForm">
    <h2>Book Your Appliance Repair</h2>
    
    <!-- Progress Bar -->
    <div class="form-progress">
        <div class="progress-bar" style="width: 25%"></div>
        <span class="progress-text">Step 1 of 4</span>
    </div>
    
    <!-- Step 1: Contact Info -->
    <fieldset class="form-step active" data-step="1">
        <legend>Contact Information</legend>
        
        <div class="form-row">
            <div class="form-group">
                <label>First Name*</label>
                <input type="text" name="firstName" required>
            </div>
            <div class="form-group">
                <label>Last Name*</label>
                <input type="text" name="lastName" required>
            </div>
        </div>
        
        <div class="form-group">
            <label>Phone Number*</label>
            <input type="tel" name="phone" required>
        </div>
        
        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email">
        </div>
    </fieldset>
    
    <!-- Step 2: Address -->
    <fieldset class="form-step" data-step="2">
        <legend>Service Address</legend>
        
        <div class="form-group">
            <label>Street Address*</label>
            <input type="text" name="address" required autocomplete="street-address">
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label>City*</label>
                <input type="text" name="city" required autocomplete="address-level2">
            </div>
            <div class="form-group">
                <label>ZIP Code*</label>
                <input type="text" name="zip" required autocomplete="postal-code">
            </div>
        </div>
    </fieldset>
```