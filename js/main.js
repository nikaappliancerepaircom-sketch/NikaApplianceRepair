// Main JavaScript file for Nika Appliance Repair

document.addEventListener('DOMContentLoaded', function() {

    // Initialize all interactive elements immediately
    updateCurrentYear();
    initializeFAQ();
    initializeForms();
    initializeSmoothScrolling();

    // Update current year in copyright
    function updateCurrentYear() {
        const yearElement = document.getElementById('current-year');
        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    }
    
    // FAQ Functionality
    function initializeFAQ() {
        const faqItems = document.querySelectorAll('.faq-item');
        
        if (faqItems.length === 0) return;
        
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            const answer = item.querySelector('.faq-answer');
            const icon = item.querySelector('.faq-icon');
            
            if (question && answer) {
                // Set initial state
                answer.style.maxHeight = '0px';
                answer.style.opacity = '0';
                
                question.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const isActive = item.classList.contains('active');
                    
                    // Close all other FAQs
                    faqItems.forEach(otherItem => {
                        if (otherItem !== item && otherItem.classList.contains('active')) {
                            otherItem.classList.remove('active');
                            const otherAnswer = otherItem.querySelector('.faq-answer');
                            const otherIcon = otherItem.querySelector('.faq-icon');
                            
                            if (otherAnswer) {
                                otherAnswer.style.maxHeight = '0px';
                                otherAnswer.style.opacity = '0';
                            }
                            if (otherIcon) {
                                otherIcon.textContent = '+';
                                otherIcon.style.transform = 'rotate(0deg)';
                            }
                        }
                    });
                    
                    // Toggle current FAQ
                    if (!isActive) {
                        item.classList.add('active');
                        // Calculate the exact height needed
                        answer.style.maxHeight = answer.scrollHeight + 50 + 'px'; // Added extra 50px padding
                        answer.style.opacity = '1';
                        if (icon) {
                            icon.textContent = '−';
                            icon.style.transform = 'rotate(180deg)';
                        }
                    } else {
                        item.classList.remove('active');
                        answer.style.maxHeight = '0px';
                        answer.style.opacity = '0';
                        if (icon) {
                            icon.textContent = '+';
                            icon.style.transform = 'rotate(0deg)';
                        }
                    }
                });
                
                // Add keyboard accessibility
                question.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        question.click();
                    }
                });
            }
        });
    }
    
    // Form Submission Handling
    function initializeForms() {
        const bookingForm = document.querySelector('.booking-form');
        if (bookingForm) {
            bookingForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const brandName = window.location.pathname.includes('lg') ? 'LG' : 
                                window.location.pathname.includes('samsung') ? 'Samsung' :
                                window.location.pathname.includes('whirlpool') ? 'Whirlpool' :
                                window.location.pathname.includes('ge') ? 'GE' : '';
                const message = brandName 
                    ? `Thank you! We will contact you within 30 minutes to confirm your ${brandName} appliance repair appointment.`
                    : 'Thank you! We will contact you within 30 minutes to confirm your appliance repair appointment.';
                alert(message);
            });
        }

        // Property Manager Form
        const pmForm = document.querySelector('.pm-form');
        if (pmForm) {
            pmForm.addEventListener('submit', (e) => {
                e.preventDefault();
                alert('Thank you! Our property manager specialist will contact you within 24 hours.');
            });
        }
    }

    // Smooth Scrolling
    function initializeSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
});