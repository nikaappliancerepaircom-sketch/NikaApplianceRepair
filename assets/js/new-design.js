// Rotating Appliance Names Animation
document.addEventListener('DOMContentLoaded', function() {
    const rotateItems = document.querySelectorAll('.rotate-item');
    let currentIndex = 0;

    function rotateWords() {
        // Remove active class from all items
        rotateItems.forEach(item => item.classList.remove('active'));
        
        // Add active class to current item
        rotateItems[currentIndex].classList.add('active');
        
        // Move to next item
        currentIndex = (currentIndex + 1) % rotateItems.length;
    }

    // Start rotation
    if (rotateItems.length > 0) {
        rotateItems[0].classList.add('active');
        setInterval(rotateWords, 3000); // Change every 3 seconds
    }
});

// Phone Ring Animation Enhancement
document.addEventListener('DOMContentLoaded', function() {
    const phoneButtons = document.querySelectorAll('.phone-button, .cta-phone');
    
    phoneButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.phone-icon-animated');
            if (icon) {
                icon.style.animation = 'ring-bell 0.5s ease-in-out';
                setTimeout(() => {
                    icon.style.animation = 'ring-bell 2s ease-in-out infinite';
                }, 500);
            }
        });
    });
});

// Smooth Scroll for Navigation Links
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

// Header Scroll Effect
let lastScroll = 0;
const header = document.querySelector('.main-nav');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.08)';
    }
    
    lastScroll = currentScroll;
});