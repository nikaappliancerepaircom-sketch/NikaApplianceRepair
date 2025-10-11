/**
 * Mobile Menu System
 * Responsive navigation with smooth animations
 */

class MobileMenu {
    constructor() {
        this.menuButton = document.querySelector('.mobile-menu-toggle');
        this.mobileMenu = document.querySelector('.mobile-menu');
        this.overlay = document.querySelector('.menu-overlay');
        this.menuItems = document.querySelectorAll('.mobile-menu a');
        this.body = document.body;
        
        this.isOpen = false;
        this.init();
    }
    
    init() {
        if (!this.menuButton || !this.mobileMenu) return;
        
        // Toggle button
        this.menuButton.addEventListener('click', () => this.toggle());
        
        // Close on overlay click
        if (this.overlay) {
            this.overlay.addEventListener('click', () => this.close());
        }
        
        // Close on menu item click
        this.menuItems.forEach(item => {
            item.addEventListener('click', () => {
                setTimeout(() => this.close(), 300);
            });
        });
        
        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }