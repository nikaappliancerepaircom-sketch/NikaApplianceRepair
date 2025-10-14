#!/usr/bin/env python3
"""
Batch update location pages with new header, CSS, and JavaScript
"""

import os
import re

# Files to update (excluding ajax.html and brampton.html which are already done)
files_to_update = [
    "burlington.html",
    "markham.html",
    "milton.html",
    "mississauga.html",
    "oakville.html",
    "oshawa.html",
    "pickering.html",
    "richmond-hill.html",
    "toronto.html",
    "vaughan.html"
]

# Old header HTML to replace
old_header = '''    <header class="main-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../" style="text-decoration: none; color: inherit;">
                    <div class="logo-text">
                        <span class="logo-primary">NIKA</span>
                        <span class="logo-secondary">Appliance Repair</span>
                    </div>
                    </a>
                </div>
                <nav class="main-nav">
                    <ul>
                        <li><a href="../#services">Services</a></li>
                        <li><a href="../#about">About</a></li>
                        <li><a href="../#areas">Areas</a></li>
                        <li><a href="../#brands">Brands</a></li>
                        <li><a href="../#contact">Contact</a></li>
                    </ul>
                </nav>
                <a href="../#book" class="header-book-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="white" style="margin-right: 8px;">
                        <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                    </svg>
                    Book Online
                </a>
                <button class="mobile-menu-toggle" aria-label="Toggle mobile menu" aria-expanded="false">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </div>
    </header>'''

# New header HTML
new_header = '''    <!-- Urgency Banner (Top) -->
    <div class="urgency-banner">
        <div class="container">
            <p class="urgency-text">
                🔥 <strong>SAVE $40</strong> on any appliance repair service - Limited time offer!
                <a href="tel:4377476737" class="urgency-link">Call 437-747-6737</a>
            </p>
            <button class="urgency-close" aria-label="Close banner">&times;</button>
        </div>
    </div>

    <!-- Main Header -->
    <header class="main-header-v2">
        <div class="container">
            <div class="header-content-v2">
                <!-- Logo -->
                <div class="logo-v2">
                    <a href="../" style="text-decoration: none; color: inherit;">
                        <div class="logo-text-v2">
                            <span class="logo-primary-v2">NIKA</span>
                            <span class="logo-secondary-v2">Appliance Repair</span>
                        </div>
                    </a>
                </div>

                <!-- Navigation -->
                <nav class="main-nav-v2">
                    <ul>
                        <li class="nav-dropdown">
                            <a href="#services">Services ▼</a>
                            <ul class="dropdown-menu">
                                <li><a href="../services/refrigerator-repair">Refrigerator Repair</a></li>
                                <li><a href="../services/dishwasher-repair">Dishwasher Repair</a></li>
                                <li><a href="../services/dryer-repair">Dryer Repair</a></li>
                                <li><a href="../services/stove-repair">Stove Repair</a></li>
                                <li><a href="../services/oven-repair">Oven Repair</a></li>
                                <li><a href="../services/washer-repair">Washer Repair</a></li>
                            </ul>
                        </li>
                        <li class="nav-dropdown">
                            <a href="#locations">Locations ▼</a>
                            <ul class="dropdown-menu">
                                <li><a href="../locations/toronto">Toronto</a></li>
                                <li><a href="../locations/mississauga">Mississauga</a></li>
                                <li><a href="../locations/brampton">Brampton</a></li>
                                <li><a href="../locations/markham">Markham</a></li>
                                <li><a href="../locations/vaughan">Vaughan</a></li>
                                <li><a href="../locations/richmond-hill">Richmond Hill</a></li>
                            </ul>
                        </li>
                    </ul>
                </nav>

                <!-- CTA Buttons (Desktop) -->
                <div class="header-ctas-v2">
                    <a href="tel:4377476737" class="header-cta-call">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                        </svg>
                        <span>437-747-6737</span>
                    </a>
                    <a href="https://wa.me/14377476737?text=Hi%2C%20I%20need%20appliance%20repair" target="_blank" class="header-cta-chat">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                        </svg>
                        <span>Chat Now</span>
                    </a>
                    <a href="../#book" class="header-cta-book">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                            <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                        </svg>
                        <span>Book Now</span>
                    </a>
                </div>

                <!-- Mobile Menu Toggle -->
                <button class="mobile-menu-toggle-v2" aria-label="Toggle mobile menu" aria-expanded="false">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </div>
    </header>

    <!-- Mobile Sticky Bottom Bar -->
    <div class="mobile-sticky-bottom">
        <a href="tel:4377476737" class="mobile-cta-call">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
            </svg>
            <span>Call</span>
        </a>
        <a href="https://wa.me/14377476737?text=Hi%2C%20I%20need%20appliance%20repair" target="_blank" class="mobile-cta-chat">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
            </svg>
            <span>Chat</span>
        </a>
        <a href="../#book" class="mobile-cta-book">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
            </svg>
            <span>Book</span>
        </a>
    </div>'''

# CSS to add after <style> tag
css_to_add = '''        /* ========== NEW HEADER V2 STYLES ========== */

        /* Urgency Banner */
        .urgency-banner {
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            padding: 12px 0;
            position: relative;
            z-index: 1001;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .urgency-banner .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
        }
        .urgency-text {
            margin: 0;
            font-size: 16px;
            font-weight: 500;
            text-align: center;
            flex: 1;
        }
        .urgency-text strong {
            font-size: 18px;
            font-weight: 700;
        }
        .urgency-link {
            color: white;
            text-decoration: underline;
            font-weight: 700;
            margin-left: 10px;
        }
        .urgency-close {
            background: transparent;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            line-height: 1;
            opacity: 0.8;
            transition: opacity 0.3s;
        }
        .urgency-close:hover {
            opacity: 1;
        }

        /* Main Header V2 */
        .main-header-v2 {
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 15px 0;
        }
        .header-content-v2 {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 30px;
        }

        /* Logo V2 */
        .logo-v2 {
            flex-shrink: 0;
        }
        .logo-text-v2 {
            display: flex;
            flex-direction: column;
            line-height: 1.2;
        }
        .logo-primary-v2 {
            font-size: 28px;
            font-weight: 800;
            color: #2196F3;
            letter-spacing: 1px;
        }
        .logo-secondary-v2 {
            font-size: 14px;
            font-weight: 500;
            color: #666;
        }

        /* Navigation V2 */
        .main-nav-v2 ul {
            list-style: none;
            display: flex;
            gap: 30px;
            margin: 0;
            padding: 0;
        }
        .main-nav-v2 a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            font-size: 15px;
            transition: color 0.3s;
        }
        .main-nav-v2 a:hover {
            color: #2196F3;
        }
        .nav-dropdown {
            position: relative;
        }
        .dropdown-menu {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-radius: 8px;
            padding: 10px 0;
            min-width: 220px;
            z-index: 1002;
            margin-top: 10px;
        }
        .nav-dropdown:hover .dropdown-menu {
            display: block;
        }
        .dropdown-menu li {
            margin: 0;
        }
        .dropdown-menu a {
            display: block;
            padding: 10px 20px;
            font-size: 14px;
            color: #333;
        }
        .dropdown-menu a:hover {
            background: #f5f5f5;
            color: #2196F3;
        }

        /* Header CTAs V2 */
        .header-ctas-v2 {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        .header-cta-call,
        .header-cta-chat,
        .header-cta-book {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
            white-space: nowrap;
        }
        .header-cta-call {
            background: #4CAF50;
            color: white;
            border: 2px solid #4CAF50;
        }
        .header-cta-call:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76,175,80,0.3);
        }
        .header-cta-chat {
            background: #25D366;
            color: white;
            border: 2px solid #25D366;
        }
        .header-cta-chat:hover {
            background: #20bd5a;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37,211,102,0.3);
        }
        .header-cta-book {
            background: #2196F3;
            color: white;
            border: 2px solid #2196F3;
        }
        .header-cta-book:hover {
            background: #1976D2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(33,150,243,0.3);
        }

        /* Mobile Menu Toggle V2 */
        .mobile-menu-toggle-v2 {
            display: none;
            flex-direction: column;
            gap: 5px;
            background: transparent;
            border: none;
            cursor: pointer;
            padding: 8px;
        }
        .mobile-menu-toggle-v2 span {
            width: 25px;
            height: 3px;
            background: #333;
            border-radius: 2px;
            transition: all 0.3s;
        }

        /* Mobile Sticky Bottom Bar */
        .mobile-sticky-bottom {
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            z-index: 999;
            padding: 10px;
        }
        .mobile-sticky-bottom {
            display: none;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }
        .mobile-cta-call,
        .mobile-cta-chat,
        .mobile-cta-book {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 5px;
            padding: 12px 8px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.3s;
        }
        .mobile-cta-call {
            background: #4CAF50;
            color: white;
        }
        .mobile-cta-chat {
            background: #25D366;
            color: white;
        }
        .mobile-cta-book {
            background: #2196F3;
            color: white;
        }
        .mobile-cta-call:active,
        .mobile-cta-chat:active,
        .mobile-cta-book:active {
            transform: scale(0.95);
        }

        /* Mobile Responsive */
        @media (max-width: 968px) {
            .main-nav-v2,
            .header-ctas-v2 {
                display: none;
            }
            .mobile-menu-toggle-v2 {
                display: flex;
            }
            .mobile-sticky-bottom {
                display: grid;
            }
            .urgency-text {
                font-size: 14px;
            }
            .urgency-text strong {
                font-size: 16px;
            }
            body {
                padding-bottom: 70px; /* Space for sticky bottom bar */
            }
        }

        @media (max-width: 768px) {
            .header-content-v2 {
                gap: 15px;
            }
            .logo-primary-v2 {
                font-size: 24px;
            }
            .logo-secondary-v2 {
                font-size: 12px;
            }
            .urgency-text {
                font-size: 13px;
            }
            .urgency-link {
                display: block;
                margin-left: 0;
                margin-top: 5px;
            }
        }

'''

# JavaScript to add before </body> tag
js_to_add = '''
    <script>
        // Close urgency banner
        document.addEventListener('DOMContentLoaded', function() {
            const closeBtn = document.querySelector('.urgency-close');
            const banner = document.querySelector('.urgency-banner');

            if (closeBtn && banner) {
                closeBtn.addEventListener('click', function() {
                    banner.style.display = 'none';
                    // Save to localStorage so it doesn't show again this session
                    localStorage.setItem('urgencyBannerClosed', 'true');
                });

                // Check if banner was closed before
                if (localStorage.getItem('urgencyBannerClosed') === 'true') {
                    banner.style.display = 'none';
                }
            }
        });
    </script>'''

def update_file(filename):
    """Update a single location file"""
    filepath = f"C:\\NikaApplianceRepair\\locations\\{filename}"

    if not os.path.exists(filepath):
        print(f"[FAIL] {filename}: File not found")
        return False

    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Replace header
        if old_header in content:
            content = content.replace(old_header, new_header)
            print(f"[OK] {filename}: Header replaced")
        else:
            print(f"[WARN] {filename}: Old header not found")
            return False

        # 2. Add CSS after <style> tag
        if '    <style>\n        /* Fluid typography' in content:
            content = content.replace(
                '    <style>\n        /* Fluid typography',
                '    <style>\n' + css_to_add + '        /* Fluid typography'
            )
            print(f"[OK] {filename}: CSS added")
        else:
            print(f"[WARN] {filename}: <style> tag not found in expected format")
            return False

        # 3. Add JavaScript before </body> tag
        old_js_section = '''    <!-- JavaScript -->
    <script src="../js/youtube-facade.js" defer></script>
    <script src="../js/main.js" defer></script>
    <script src="../js/countdown-timer.js" defer></script>
    <script src="../js/form-validation.js" defer></script>
</body>'''

        new_js_section = '''    <!-- JavaScript -->
    <script src="../js/youtube-facade.js" defer></script>
    <script src="../js/main.js" defer></script>
    <script src="../js/countdown-timer.js" defer></script>
    <script src="../js/form-validation.js" defer></script>''' + js_to_add + '''
</body>'''

        if old_js_section in content:
            content = content.replace(old_js_section, new_js_section)
            print(f"[OK] {filename}: JavaScript added")
        else:
            print(f"[WARN] {filename}: JavaScript section not found")
            return False

        # Write file back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[SUCCESS] {filename}: Successfully updated\n")
        return True

    except Exception as e:
        print(f"[ERROR] {filename}: Error - {str(e)}\n")
        return False

def main():
    """Main function to update all files"""
    print("=" * 60)
    print("Updating Location Pages with New Header")
    print("=" * 60)
    print()

    success_count = 0
    fail_count = 0

    for filename in files_to_update:
        if update_file(filename):
            success_count += 1
        else:
            fail_count += 1

    print("=" * 60)
    print(f"SUMMARY: {success_count} successful, {fail_count} failed")
    print("=" * 60)

if __name__ == "__main__":
    main()
