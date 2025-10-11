# FAQ Section Implementation Guide

## Overview
The FAQ section uses an accordion-style dropdown with smooth animations and consistent styling across all pages.

## Color Scheme
- **Primary Color**: `#1A237E` (Dark Navy) - Matches section titles
- **Hover Background**: `rgba(26, 35, 126, 0.03)` - Very subtle navy
- **Active Background**: `rgba(26, 35, 126, 0.05)` - Light navy
- **Active Border**: `#1A237E` - Dark navy
- **Text Color**: `#555` - Dark gray for answers

## HTML Structure
```html
<!-- FAQ Section -->
<section class="faq-section" id="faq">
    <div class="container">
        <h2 class="section-title">Frequently Asked Questions</h2>
        
        <div class="faq-grid">
            <div class="faq-item">
                <button class="faq-question">
                    <span>Your question here?</span>
                    <span class="faq-icon">+</span>
                </button>
                <div class="faq-answer">
                    <p>Your detailed answer here.</p>
                </div>
            </div>
            <!-- More FAQ items -->
        </div>
    </div>
</section>
```

## CSS Styles (Required)
```css
/* FAQ Section */
.faq-section {
    padding: 4rem 0;
    background: #f8f9fa;
}

.faq-grid {
    max-width: 800px;
    margin: 0 auto;
}

.faq-item {
    background: white;
    border-radius: 15px;
    margin-bottom: 1rem;
    overflow: visible;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.faq-item:hover {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
}

.faq-item.active {
    border-color: #1A237E;
    box-shadow: 0 5px 20px rgba(26, 35, 126, 0.15);
    background: #F8F9FF;
}

.faq-question {
    width: 100%;
    padding: 1.5rem 2rem;
    background: none;
    border: none;
    text-align: left;
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
    position: relative;
}

.faq-question span:first-child {
    color: #1A237E;
    flex: 1;
    padding-right: 1rem;
}

.faq-question::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 2rem;
    right: 2rem;
    height: 1px;
    background: #e0e0e0;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.faq-item.active .faq-question::after {
    opacity: 1;
}

.faq-question:hover {
    background: rgba(26, 35, 126, 0.03);
    padding-left: 2.25rem;
}

.faq-item.active .faq-question {
    background: rgba(26, 35, 126, 0.05);
}

.faq-icon {
    font-size: 1.75rem;
    color: #1A237E;
    transition: all 0.3s ease;
    font-weight: 300;
    min-width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.faq-item.active .faq-icon {
    transform: rotate(180deg);
}

.faq-answer {
    padding: 0 2rem;
    color: #555;
    line-height: 1.8;
    max-height: 0;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 0;
}

.faq-item.active .faq-answer {
    max-height: 1000px;
    padding: 1rem 2rem 1.5rem;
    opacity: 1;
}

.faq-answer p {
    margin: 0;
    font-size: 1rem;
}
```

## JavaScript Implementation
The FAQ functionality is initialized automatically in `main.js`:

```javascript
// FAQ Functionality (in main.js)
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
                    answer.style.maxHeight = answer.scrollHeight + 50 + 'px';
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
        }
    });
}
```

## Features
1. **Accordion behavior** - Only one FAQ open at a time
2. **Smooth animations** - Cubic bezier transitions
3. **Keyboard accessible** - Enter/Space key support
4. **Visual feedback** - Hover effects, active states
5. **Icon rotation** - + changes to − with 180° rotation
6. **Max height calculation** - Dynamic height with extra padding

## Best Practices
1. Keep questions concise and clear
2. Use consistent formatting across all FAQs
3. Ensure answers are complete but not too long
4. Group related questions together
5. Use schema markup for SEO benefits

## Common Issues & Solutions
1. **Text cut off**: Set `overflow: visible` on `.faq-item`
2. **Animation jerky**: Use `cubic-bezier` timing function
3. **Icon not changing**: Ensure JavaScript is loaded
4. **Multiple FAQs open**: Check JavaScript logic for closing others

## Implementation Checklist
- [ ] Add FAQ HTML structure
- [ ] Include CSS styles
- [ ] Ensure main.js is loaded
- [ ] Test accordion functionality
- [ ] Verify color scheme matches site
- [ ] Check mobile responsiveness
- [ ] Add schema markup for SEO