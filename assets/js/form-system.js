/**
 * Unified Form Validation & Submission System
 * Handles all forms across the site with consistent validation
 */

class FormSystem {
    constructor() {
        this.forms = {
            quickQuote: document.querySelectorAll('.quick-quote-form'),
            booking: document.querySelector('#bookingForm'),
            contact: document.querySelector('#contactForm')
        };
        
        this.validators = {
            phone: /^[\d\s\-\(\)]+$/,
            email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            zip: /^\d{5}(-\d{4})?$/
        };
        
        this.initializeForms();
    }
    
    initializeForms() {
        // Quick Quote Forms (multiple per page)
        this.forms.quickQuote.forEach(form => {
            this.setupQuickQuoteForm(form);
        });
        
        // Booking Form (single)
        if (this.forms.booking) {
            this.setupBookingForm(this.forms.booking);
        }
    }