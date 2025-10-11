# UNIVERSAL FORMS GUIDE

## 📋 Two Universal Forms for Entire Website

### 1. QUICK CONTACT FORM (Simple)
Used for: Quick inquiries, general contact

```html
<form class="quick-contact-form">
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="tel" name="phone" placeholder="Phone Number" required>
    <input type="email" name="email" placeholder="Email (Optional)">
    <textarea name="message" placeholder="How can we help?" rows="3"></textarea>
    <button type="submit" class="cta-primary">Send Message</button>
</form>
```

### 2. BOOKING FORM (Detailed)
Used for: Service bookings, appointments

```html
<form class="booking-form">
    <!-- Contact Info -->
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="tel" name="phone" placeholder="Phone Number" required>
    <input type="email" name="email" placeholder="Email Address">
    
    <!-- Service Details -->
    <select name="appliance" required>
        <option value="">Select Appliance Type</option>
        <option value="refrigerator">Refrigerator</option>
        <option value="washer">Washing Machine</option>
        <option value="dryer">Dryer</option>
        <option value="dishwasher">Dishwasher</option>
        <option value="oven">Oven</option>
        <option value="stove">Stove/Cooktop</option>
        <option value="other">Other</option>
    </select>
    
    <!-- Appliance Type - This is where gas/electric is handled -->
    <div class="appliance-type-field">
        <select name="appliance_type" required>
            <option value="">Is your appliance Gas or Electric?</option>
            <option value="electric">Electric</option>
            <option value="gas" disabled>Gas (We don't service gas appliances)</option>
        </select>
        <p class="form-note">⚡ We specialize in electric appliances only for safety reasons</p>
    </div>
    
    <!-- Location -->
    <input type="text" name="address" placeholder="Street Address">
    <input type="text" name="postal" placeholder="Postal Code" required>
    
    <!-- Problem Description -->
    <textarea name="problem" placeholder="Describe the issue (Optional)" rows="3"></textarea>
    
    <!-- Preferred Time -->
    <select name="preferred_time">
        <option value="">Preferred Time</option>
        <option value="asap">As Soon As Possible</option>
        <option value="morning">Morning (8AM-12PM)</option>
        <option value="afternoon">Afternoon (12PM-5PM)</option>
        <option value="evening">Evening (5PM-8PM)</option>
    </select>
    
    <button type="submit" class="cta-primary">Book Service</button>
</form>
```

## 🎯 Form Placement Strategy

### Quick Contact Form
Place on:
- Contact page
- Footer (every page)
- Service pages (sidebar)
- About page

### Booking Form
Place on:
- Homepage (hero section)
- Dedicated booking page
- Service pages (main CTA)
- After testimonials section
- Pop-up (exit intent)

## 💡 Form Features

### Both Forms Should Have:
1. **Validation**
   - Phone number format
   - Required fields marked
   - Email format (if provided)
   
2. **User Experience**
   - Auto-format phone numbers
   - Clear error messages
   - Success confirmation
   - Loading states
   
3. **Mobile Optimization**
   - Large touch targets
   - Proper input types (tel, email)
   - Auto-complete enabled
   - Single column layout

## 🚫 Gas Appliance Handling

### Visual Indicators in Form:
1. **Disabled Option**: Gas option is visible but disabled
2. **Clear Message**: "We don't service gas appliances"
3. **Safety Note**: "We specialize in electric appliances only for safety reasons"

### Alternative Approach - Radio Buttons:
```html
<div class="appliance-type-selection">
    <label>Is your appliance gas or electric?</label>
    <div class="radio-group">
        <label>
            <input type="radio" name="appliance_type" value="electric" required>
            <span>✓ Electric (We can help!)</span>
        </label>
        <label class="disabled-option">
            <input type="radio" name="appliance_type" value="gas" disabled>
            <span>✗ Gas (We don't service gas appliances)</span>
        </label>
    </div>
</div>
```

### JavaScript Enhancement:
```javascript
// Show message when user tries to select gas
document.querySelector('select[name="appliance_type"]').addEventListener('change', function(e) {
    if (e.target.value === 'gas') {
        alert('Sorry, we only service electric appliances for safety reasons. Please contact a certified gas technician.');
        e.target.value = ''; // Reset selection
    }
});
```

## 📊 Form Analytics to Track

### Metrics:
- Form starts vs completions
- Field abandonment rates
- Most common appliance types
- Peak booking times
- Gas vs electric ratio

### A/B Test:
- Number of fields
- Field order
- Button text
- Form headlines
- Required vs optional fields

## 🔧 Technical Implementation

### Form Handling:
```javascript
// Both forms can use same endpoint
const handleFormSubmit = async (formData) => {
    // Determine form type
    const formType = formData.has('appliance') ? 'booking' : 'contact';
    
    // If gas appliance selected
    if (formData.get('appliance_type') === 'gas') {
        // Special handling for gas referrals
        formData.append('referral_needed', 'true');
    }
    
    // Submit to backend
    await submitForm(formData, formType);
};
```

### Success Messages:
- **Quick Contact**: "Thanks! We'll call you within 2 hours."
- **Booking (Electric)**: "Booking confirmed! We'll call to schedule."
- **Booking (Gas)**: "Thanks! We'll help you find the right specialist."

## ✅ Best Practices

1. **Keep It Simple**
   - Minimum required fields
   - Clear labels
   - Logical flow
   
2. **Build Trust**
   - "Your info is secure" near submit
   - No spam promise
   - Clear what happens next
   
3. **Make It Fast**
   - Optimize for speed
   - Show progress
   - Confirm success quickly

Remember: Forms should help customers, not create barriers!