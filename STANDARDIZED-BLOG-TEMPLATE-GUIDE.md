# Standardized Blog Template Guide
## Use `premium-blog-example.html` Design for ALL Blog Posts

**IMPORTANT:** All 40 new blog posts (Days 1-5) must follow the EXACT design template from `premium-blog-example.html`.

---

## Template Structure (Copy This For All Posts)

### 1. **Header Section**
```html
<!-- Reading Progress Bar -->
<div class="reading-progress" id="progressBar"></div>

<!-- Site Header with Navigation -->
<header class="site-header">
    <div class="header-container">
        <div class="header-logo">
            <a href="/">Nika Appliance Repair</a>
        </div>
        <nav class="header-nav" id="mainNav">
            <ul class="nav-list">
                <li><a href="/" class="nav-link">Home</a></li>
                <li><a href="/services" class="nav-link">Services</a></li>
                <li><a href="/locations" class="nav-link">Locations</a></li>
                <li><a href="/about" class="nav-link">About</a></li>
                <li><a href="/blog" class="nav-link">Blog</a></li>
            </ul>
        </nav>
        <div class="header-trust">
            <div class="trust-stars">⭐⭐⭐⭐⭐</div>
            <div class="trust-rating">4.9/5</div>
            <div class="trust-reviews">5,200+ Reviews</div>
        </div>
        <div class="header-cta">
            <a href="tel:4377476737" class="cta-phone">
                <i class="fas fa-phone"></i> (437) 747-6737
            </a>
            <a href="/book" class="cta-book">
                <i class="fas fa-calendar-check"></i> Book Now
            </a>
        </div>
        <button class="mobile-menu-btn" aria-label="Menu" aria-expanded="false">
            <span class="menu-bar"></span>
            <span class="menu-bar"></span>
            <span class="menu-bar"></span>
        </button>
    </div>
</header>
```

### 2. **CSS Links (In Head)**
```html
<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Premium Blog Styles -->
<link rel="stylesheet" href="../css/blog-premium.css">

<!-- Header Styles -->
<link rel="stylesheet" href="../css/header-optimized.css">
```

### 3. **Blog Header (Below Site Header)**
```html
<header class="blog-header">
    <div class="blog-meta-top">
        <span class="blog-category">
            <i class="fas fa-wrench"></i> Appliance Tips
        </span>
        <span class="reading-time">
            <i class="far fa-clock"></i> 8 min read
        </span>
    </div>

    <h1 class="blog-title">[INSERT POST TITLE HERE]</h1>

    <div class="blog-meta">
        <span class="meta-item">
            <i class="far fa-calendar"></i> October 30, 2025
        </span>
        <span class="meta-item">
            <i class="far fa-user"></i> Expert Team
        </span>
    </div>
</header>

<!-- Social Share -->
<div class="social-share">
    <a href="#" class="share-btn facebook" aria-label="Share on Facebook">
        <i class="fab fa-facebook-f"></i>
    </a>
    <a href="#" class="share-btn twitter" aria-label="Share on Twitter">
        <i class="fab fa-twitter"></i>
    </a>
    <a href="#" class="share-btn linkedin" aria-label="Share on LinkedIn">
        <i class="fab fa-linkedin-in"></i>
    </a>
    <a href="#" class="share-btn email" aria-label="Share via Email">
        <i class="far fa-envelope"></i>
    </a>
</div>
```

### 4. **Main Content Structure**
```html
<div class="blog-wrapper">
    <main class="blog-main">
        <article class="blog-content">
            <!-- All content goes here -->
            <!-- Use h2, h3, p, ul, ol, blockquote, etc. -->
        </article>
    </main>

    <!-- Sidebar -->
    <aside class="blog-sidebar">
        <!-- Table of Contents -->
        <div class="toc-widget">
            <h3>Table of Contents</h3>
            <ul class="toc-list">
                <li><a href="#section-1">Section 1</a></li>
                <li><a href="#section-2">Section 2</a></li>
                <li><a href="#section-3">Section 3</a></li>
            </ul>
        </div>

        <!-- Related Posts -->
        <div class="related-widget">
            <h3>Related Posts</h3>
            <div class="related-post">
                <a href="#">Related Post Title</a>
                <div class="related-post-meta">
                    <i class="far fa-calendar"></i> Oct 25, 2025
                </div>
            </div>
        </div>
    </aside>
</div>
```

### 5. **Special Content Boxes**

**Tip Box (Green):**
```html
<div class="tip-box">
    <strong>💡 Pro Tip:</strong> Your tip content here.
</div>
```

**Info Box (Blue):**
```html
<div class="info-box">
    <h3>Box Title</h3>
    <p>Content here</p>
</div>
```

**CTA Box (Gradient):**
```html
<div class="cta-box">
    <h3>Ready for Service?</h3>
    <p>Description here</p>
    <a href="tel:4377476737" class="btn">
        <i class="fas fa-phone"></i> Call (437) 747-6737
    </a>
</div>
```

**Comparison Grid:**
```html
<div class="comparison-grid">
    <div class="comparison-card safe">
        <h3>✅ Safe Option</h3>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <div class="card-footer">Footer text</div>
    </div>

    <div class="comparison-card danger">
        <h3>⚠️ Requires Professional</h3>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <div class="card-footer">Footer text</div>
    </div>
</div>
```

### 6. **Footer (Identical for All Posts)**
```html
<footer class="seo-footer-premium">
    <div class="container">
        <!-- Trust Badges Row -->
        <div class="footer-trust-badges">
            <div class="trust-badge-item">
                <div class="badge-icon">⭐</div>
                <div class="badge-text">
                    <strong>4.9/5 Rating</strong>
                    <span>5,200+ Reviews</span>
                </div>
            </div>
            <div class="trust-badge-item">
                <div class="badge-icon">🏆</div>
                <div class="badge-text">
                    <strong>Licensed & Insured</strong>
                    <span>Since 2017</span>
                </div>
            </div>
            <div class="trust-badge-item">
                <div class="badge-icon">🛡️</div>
                <div class="badge-text">
                    <strong>90-Day Warranty</strong>
                    <span>Parts & Labor</span>
                </div>
            </div>
            <div class="trust-badge-item">
                <div class="badge-icon">⚡</div>
                <div class="badge-text">
                    <strong>Same-Day Service</strong>
                    <span>7 Days a Week</span>
                </div>
            </div>
        </div>

        <!-- Main Footer Content -->
        <div class="footer-main-content">
            <!-- Column 1: Services -->
            <div class="footer-column">
                <h4 class="footer-heading">Our Services</h4>
                <ul class="footer-links">
                    <li><a href="/services/refrigerator-repair">Refrigerator Repair</a></li>
                    <li><a href="/services/dishwasher-repair">Dishwasher Repair</a></li>
                    <li><a href="/services/washer-repair">Washer Repair</a></li>
                    <li><a href="/services/dryer-repair">Dryer Repair</a></li>
                    <li><a href="/services/oven-repair">Oven Repair</a></li>
                </ul>
            </div>

            <!-- Column 2: Locations -->
            <div class="footer-column">
                <h4 class="footer-heading">Service Areas</h4>
                <ul class="footer-links">
                    <li><a href="/locations/mississauga">Mississauga</a></li>
                    <li><a href="/locations/brampton">Brampton</a></li>
                    <li><a href="/locations/markham">Markham</a></li>
                    <li><a href="/locations/vaughan">Vaughan</a></li>
                    <li><a href="/locations/oakville">Oakville</a></li>
                </ul>
            </div>

            <!-- Column 3: Company -->
            <div class="footer-column">
                <h4 class="footer-heading">Company</h4>
                <ul class="footer-links">
                    <li><a href="/about">About Us</a></li>
                    <li><a href="/reviews">Customer Reviews</a></li>
                    <li><a href="/faq">FAQ</a></li>
                    <li><a href="/book">Book Online</a></li>
                    <li><a href="/privacy">Privacy Policy</a></li>
                </ul>
            </div>

            <!-- Column 4: Contact -->
            <div class="footer-column footer-column-contact">
                <h4 class="footer-heading">Contact Us</h4>
                <div class="footer-contact-box">
                    <p class="contact-item">
                        <i class="fas fa-phone"></i>
                        <a href="tel:4377476737" class="contact-link">(437) 747-6737</a>
                    </p>
                    <p class="contact-item">
                        <i class="far fa-envelope"></i>
                        <a href="mailto:care@niappliancerepair.ca" class="contact-link">care@niappliancerepair.ca</a>
                    </p>
                    <p class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>Serving Toronto & GTA</span>
                    </p>
                </div>

                <a href="tel:4377476737" class="footer-cta-button">
                    <i class="fas fa-phone"></i>
                    Call for Same-Day Service
                </a>
            </div>
        </div>

        <!-- Footer Bottom -->
        <div class="footer-bottom">
            <div class="footer-bottom-content">
                <p class="copyright">
                    © 2025 Nika Appliance Repair. All Rights Reserved.
                    <span class="separator">|</span>
                    Licensed & Insured
                </p>
                <div class="footer-social-links">
                    <span class="footer-tagline">Trusted by 5,200+ Happy Customers</span>
                </div>
            </div>
        </div>
    </div>
</footer>
```

### 7. **JavaScript (Identical for All Posts)**
```html
<script>
    // Reading Progress Bar
    window.addEventListener('scroll', function() {
        const progressBar = document.getElementById('progressBar');
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight - windowHeight;
        const scrolled = (window.scrollY / documentHeight) * 100;
        progressBar.style.width = scrolled + '%';
    });

    // Mobile Menu Toggle
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const mainNav = document.getElementById('mainNav');

    if (menuBtn) {
        menuBtn.addEventListener('click', function() {
            const isOpen = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isOpen);
            mainNav.classList.toggle('menu-open');
        });
    }

    // Update year
    const yearElement = document.getElementById('current-year-footer');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
</script>
```

---

## Key Points for All Posts

✅ **CSS Files Referenced (NOT Embedded):**
- `../css/blog-premium.css` - Main blog styling
- `../css/header-optimized.css` - Header styling
- Font Awesome CDN for icons
- Google Fonts (Fredoka + Rubik)

✅ **No Embedded CSS:** All styling comes from external files (matches production setup)

✅ **Consistent Structure:**
- Header with navigation (same for all)
- Blog header with metadata
- Social sharing buttons
- Main content + sidebar
- Professional footer (same for all)
- JavaScript for progress bar (same for all)

✅ **Content Areas That Differ by Post:**
- Blog title
- Blog category (can vary)
- Reading time (update based on word count)
- Publication date
- Main article content
- Table of Contents in sidebar
- Related Posts in sidebar
- Schema markup JSON-LD (customize per post)

✅ **Design Elements to Use:**
- `<div class="tip-box">` for tips (green)
- `<div class="info-box">` for information (blue)
- `<div class="cta-box">` for calls-to-action (gradient)
- `<div class="comparison-grid">` for comparisons
- Font Awesome icons for visual interest

---

## Regeneration Priority

**IMMEDIATE ACTION NEEDED:**
Days 1-5 posts created in previous batch need to be **regenerated with this template structure**.

Current posts use:
- ❌ Embedded CSS (unnecessary weight)
- ❌ Inconsistent header/footer
- ❌ No sidebar widget structure
- ❌ Different design approach per post

Should use:
- ✅ External CSS references
- ✅ Consistent header/footer (from template)
- ✅ Sidebar with TOC + related posts
- ✅ Standardized design boxes and elements

---

## Commands for Regeneration

```bash
# Delete draft folders with old design
rm -rf blog/_drafts/day-1
rm -rf blog/_drafts/day-2
rm -rf blog/_drafts/day-3
rm -rf blog/_drafts/day-4
rm -rf blog/_drafts/day-5

# Then regenerate with new template (following this guide)
```

---

**Status:** Template guide ready
**Next Step:** Regenerate 20 posts (Days 1-5) with this standardized template
