// Mobile Menu and Responsive Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn, .mobile-menu-toggle, .menu-toggle');
    const navMenu = document.querySelector('.nav-menu, .nav-links, nav ul');
    const body = document.body;
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            body.classList.toggle('menu-open');
            
            // Change icon
            if (navMenu.classList.contains('active')) {
                mobileMenuBtn.innerHTML = '✕';
            } else {
                mobileMenuBtn.innerHTML = '☰';
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('nav') && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                body.classList.remove('menu-open');
                mobileMenuBtn.innerHTML = '☰';
            }
        });
        
        // Close menu when clicking on a link
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                body.classList.remove('menu-open');
                mobileMenuBtn.innerHTML = '☰';
            });
        });
    }
    
    // Smooth scroll for anchor links
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
    
    // Fix viewport height on mobile (for browsers with URL bar)
    function setViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    setViewportHeight();
    window.addEventListener('resize', setViewportHeight);
    window.addEventListener('orientationchange', setViewportHeight);
    
    // Disable floating icons on touch devices
    if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
        document.querySelectorAll('.floating-icon, .hero-floating-icon, [class*="float-icon"]').forEach(icon => {
            icon.style.display = 'none';
        });
    }
    
    // Ensure forms work properly on mobile
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add your form handling logic here
            console.log('Form submitted');
        });
    });
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 6) {
                value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 10);
            } else if (value.length >= 3) {
                value = value.slice(0, 3) + '-' + value.slice(3);
            }
            e.target.value = value;
        });
    });
});

// Add CSS for mobile menu
const style = document.createElement('style');
style.textContent = `
    /* Mobile Menu Styles */
    @media (max-width: 767px) {
        .nav-menu,
        .nav-links,
        nav ul {
            position: fixed;
            top: 0;
            right: -100%;
            width: 80%;
            max-width: 300px;
            height: 100vh;
            background: white;
            box-shadow: -5px 0 15px rgba(0,0,0,0.1);
            flex-direction: column;
            padding: 80px 20px 20px;
            transition: right 0.3s ease;
            z-index: 1000;
            overflow-y: auto;
        }
        
        .nav-menu.active,
        .nav-links.active,
        nav ul.active {
            right: 0;
        }
        
        .nav-menu li,
        .nav-links li,
        nav ul li {
            margin: 15px 0;
            width: 100%;
        }
        
        .nav-menu a,
        .nav-links a,
        nav ul a {
            display: block;
            padding: 10px 0;
            font-size: 18px;
        }
        
        body.menu-open {
            overflow: hidden;
        }
        
        body.menu-open::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 999;
        }
        
        .mobile-menu-btn,
        .mobile-menu-toggle,
        .menu-toggle {
            position: relative;
            z-index: 1001;
        }
    }
    
    /* Viewport height fix */
    .hero,
    .hero-section {
        min-height: 100vh;
        min-height: calc(var(--vh, 1vh) * 100);
    }
`;
document.head.appendChild(style);
