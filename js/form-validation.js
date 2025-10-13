/**
 * Form Validation Script
 * BMAD Method Compliant - Client-side validation with clear error messages
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.booking-form-bmad form');

    if (!form) return;

    // Add novalidate to use custom validation
    form.setAttribute('novalidate', 'true');

    // Validation patterns
    const patterns = {
        name: /^[a-zA-Z\s]{2,50}$/,
        phone: /^[\d\s\-\(\)]{10,15}$/,
        postal: /^[A-Za-z]\d[A-Za-z][\s]?\d[A-Za-z]\d$/
    };

    // Error messages
    const messages = {
        name: 'Please enter a valid name (2-50 characters, letters only)',
        phone: 'Please enter a valid phone number (10-15 digits)',
        postal: 'Please enter a valid postal code (e.g., M5V 3A8)',
        appliance: 'Please select an appliance type'
    };

    // Get form inputs
    const nameInput = form.querySelector('input[name="name"]');
    const phoneInput = form.querySelector('input[name="phone"]');
    const postalInput = form.querySelector('input[name="postal"]');
    const applianceSelect = form.querySelector('select[name="appliance"]');

    // Create error display function
    function showError(input, message) {
        // Remove existing error
        clearError(input);

        // Create error element
        const error = document.createElement('div');
        error.className = 'form-error';
        error.style.color = '#e74c3c';
        error.style.fontSize = '14px';
        error.style.marginTop = '5px';
        error.style.marginBottom = '10px';
        error.textContent = message;

        // Add error styling to input
        input.style.borderColor = '#e74c3c';
        input.style.borderWidth = '2px';

        // Insert error after input
        input.parentNode.insertBefore(error, input.nextSibling);
    }

    function clearError(input) {
        const error = input.parentNode.querySelector('.form-error');
        if (error) {
            error.remove();
        }
        input.style.borderColor = '';
        input.style.borderWidth = '';
    }

    // Real-time validation on blur
    nameInput.addEventListener('blur', function() {
        if (!this.value.trim()) {
            showError(this, 'Name is required');
        } else if (!patterns.name.test(this.value.trim())) {
            showError(this, messages.name);
        } else {
            clearError(this);
        }
    });

    phoneInput.addEventListener('blur', function() {
        if (!this.value.trim()) {
            showError(this, 'Phone number is required');
        } else if (!patterns.phone.test(this.value.trim())) {
            showError(this, messages.phone);
        } else {
            clearError(this);
        }
    });

    postalInput.addEventListener('blur', function() {
        if (!this.value.trim()) {
            showError(this, 'Postal code is required');
        } else if (!patterns.postal.test(this.value.trim())) {
            showError(this, messages.postal);
        } else {
            clearError(this);
        }
    });

    applianceSelect.addEventListener('change', function() {
        if (!this.value) {
            showError(this, messages.appliance);
        } else {
            clearError(this);
        }
    });

    // Clear error on focus
    [nameInput, phoneInput, postalInput, applianceSelect].forEach(input => {
        input.addEventListener('focus', function() {
            clearError(this);
        });
    });

    // Form submission validation
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        let isValid = true;

        // Validate name
        if (!nameInput.value.trim()) {
            showError(nameInput, 'Name is required');
            isValid = false;
        } else if (!patterns.name.test(nameInput.value.trim())) {
            showError(nameInput, messages.name);
            isValid = false;
        }

        // Validate phone
        if (!phoneInput.value.trim()) {
            showError(phoneInput, 'Phone number is required');
            isValid = false;
        } else if (!patterns.phone.test(phoneInput.value.trim())) {
            showError(phoneInput, messages.phone);
            isValid = false;
        }

        // Validate postal
        if (!postalInput.value.trim()) {
            showError(postalInput, 'Postal code is required');
            isValid = false;
        } else if (!patterns.postal.test(postalInput.value.trim())) {
            showError(postalInput, messages.postal);
            isValid = false;
        }

        // Validate appliance
        if (!applianceSelect.value) {
            showError(applianceSelect, messages.appliance);
            isValid = false;
        }

        // If valid, submit form
        if (isValid) {
            // Show success message
            const submitBtn = form.querySelector('.submit-btn');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '✓ Form Submitted!';
            submitBtn.style.background = '#27AE60';
            submitBtn.disabled = true;

            // In production, actually submit the form
            // form.submit(); or use AJAX

            // For demo, reset after 2 seconds
            setTimeout(function() {
                submitBtn.innerHTML = originalText;
                submitBtn.style.background = '';
                submitBtn.disabled = false;
                form.reset();
            }, 2000);
        } else {
            // Scroll to first error
            const firstError = form.querySelector('.form-error');
            if (firstError) {
                firstError.previousElementSibling.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
                firstError.previousElementSibling.focus();
            }
        }
    });

    // Auto-format phone number
    phoneInput.addEventListener('input', function(e) {
        let value = this.value.replace(/\D/g, '');
        if (value.length > 0) {
            if (value.length <= 3) {
                this.value = value;
            } else if (value.length <= 6) {
                this.value = value.slice(0, 3) + '-' + value.slice(3);
            } else {
                this.value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 10);
            }
        }
    });

    // Auto-format postal code (Canadian format)
    postalInput.addEventListener('input', function(e) {
        let value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        if (value.length > 3) {
            this.value = value.slice(0, 3) + ' ' + value.slice(3, 6);
        } else {
            this.value = value;
        }
    });
});
