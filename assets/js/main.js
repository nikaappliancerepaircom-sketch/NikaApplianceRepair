/**
 * Nika Appliance Repair - Main JavaScript
 * Version: 1.0
 * Dependencies: None (Vanilla JS)
 */

// === Configuration === //
const CONFIG = {
    phoneNumber: '5551234567',
    businessHours: {
        open: 7,  // 7 AM
        close: 21, // 9 PM
        timezone: 'America/Chicago'
    },
    emergencyAvailable: true,
    animationDuration: 300
};

// === Utility Functions === //
const utils = {
    // Smooth scroll to element
    smoothScroll: (target) => {
        const element = document.querySelector(target);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    },