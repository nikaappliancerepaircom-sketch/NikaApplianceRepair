# BMAD V2 - AUTO-FIX vs MANUAL (277 параметров)

## ЛЕГЕНДА

- 🤖 **AUTO** - Автоматический фикс через скрипт
- ✋ **MANUAL** - Требует ручной работы
- ⚙️ **SEMI** - Частично автоматом (шаблон), нужна доработка вручную
- 🔧 **SERVER** - Настройка на сервере
- 🔌 **EXTERNAL** - Внешний сервис

---

## TIER 1: CRITICAL (16 params) - 100% Coverage

| # | Parameter | Type | What Script Does | What Manual Needed |
|---|-----------|------|------------------|-------------------|
| 1 | Phone consistency | 🤖 AUTO | Replaces all phone numbers | None |
| 2 | Hours consistency | 🤖 AUTO | Replaces all hours text | None |
| 3 | Warranty consistency | 🤖 AUTO | Replaces warranty terms | None |
| 4 | Rating consistency | 🤖 AUTO | Updates rating numbers | None |
| 5 | Review count consistency | 🤖 AUTO | Updates review counts | None |
| 6 | Years experience | 🤖 AUTO | Updates years number | None |
| 7 | Address consistency | 🤖 AUTO | Replaces address text | None |
| 8 | Email consistency | 🤖 AUTO | Replaces email addresses | None |
| 9 | LocalBusiness schema | 🤖 AUTO | Inserts JSON-LD schema | None |
| 10 | AggregateRating schema | 🤖 AUTO | Inserts rating schema | None |
| 11 | Mobile viewport | 🤖 AUTO | Adds meta tag | None |
| 12 | Single H1 tag | 🤖 AUTO | Removes duplicate H1s | None |
| 13 | Valid HTML | 🤖 AUTO | Fixes DOCTYPE, tags | None |
| 14 | HTTPS/SSL | 🤖 AUTO | Replaces http:// → https:// | None |
| 15 | Phone in header/hero | 🤖 AUTO | Ensures phone visible | None |
| **16** | **Content uniqueness** | **✋ MANUAL** | **Detects duplicates only** | **Rewrite content per appliance** |

**TIER 1 AUTO-FIX RATE:** 15/16 (93.75%)

**Критичное исключение:**
- **Param 16 (Content Uniqueness)** - Требует ПЕРЕПИСЫВАНИЯ контента для каждого типа appliance. Скрипт может только ОБНАРУЖИТЬ дубли, но не может написать уникальный контент.

---

## TIER 2: SEO & CRO (30 params) - 75% Coverage

| # | Parameter | Type | What Script Does | What Manual Needed |
|---|-----------|------|------------------|-------------------|
| 17 | Word count | 🤖 AUTO | Adds filler content | Review & improve quality |
| 18 | **Keyword density** | **✋ MANUAL** | - | Rewrite to dilute keywords |
| 19 | Title tag | 🤖 AUTO | Generates optimized title | None |
| 20 | Meta description | 🤖 AUTO | Generates description | None |
| 21 | Heading structure | ⚙️ SEMI | Adds missing H2/H3 | Review hierarchy |
| 22 | Internal links | 🤖 AUTO | Adds links to services | None |
| 23 | Images count | 🤖 AUTO | Adds placeholder images | Replace with real photos |
| 24 | Alt text | 🤖 AUTO | Generates alt text | None |
| 25 | FAQ schema | 🤖 AUTO | Adds FAQ JSON-LD | None |
| 26 | Breadcrumbs | 🤖 AUTO | Adds breadcrumb markup | None |
| 27 | Structured data | 🤖 AUTO | Adds various schemas | None |
| 28 | URL structure | 🤖 AUTO | Nothing (file-based) | Rename files if needed |
| 29 | Canonical tag | 🤖 AUTO | Adds canonical link | None |
| 30 | Open Graph | 🤖 AUTO | Adds OG meta tags | None |
| 31 | Twitter cards | 🤖 AUTO | Adds Twitter meta | None |
| 32 | **CTA count** | **✋ MANUAL** | - | Remove excess CTAs |
| 33 | CTA diversity | 🤖 AUTO | Ensures 3 types present | None |
| 34 | Form fields | ⚙️ SEMI | Adds form template | Optimize field count |
| 35 | Phone prominence | 🤖 AUTO | Ensures phone visible | None |
| 36 | Trust badges | 🤖 AUTO | Adds badge icons | None |
| 37 | Social proof | 🤖 AUTO | Adds testimonial blocks | Add real testimonials |
| 38 | Testimonials | ⚙️ SEMI | Adds placeholder quotes | Add real customer quotes |
| 39 | Rating display | 🤖 AUTO | Adds star ratings | None |
| 40 | Urgency triggers | 🤖 AUTO | Adds urgency text | None |
| 41 | Risk reversal | 🤖 AUTO | Emphasizes warranty | None |
| 42 | Value proposition | 🤖 AUTO | Adds hero value text | None |
| 43 | **Benefits language** | **✋ MANUAL** | - | Rewrite feature → benefit |
| 44 | **Contact in footer** | **🤖 AUTO** | Adds contact block | None |
| 45 | Sticky header | 🤖 AUTO | Adds CSS for sticky | None |

**TIER 2 AUTO-FIX RATE:** 22.5/30 (75%)

**Manual Required:**
- **Param 18 (Keyword density)** - Need to rewrite text to reduce keyword repetition
- **Param 32 (CTA count)** - Need to manually remove CTAs from HTML
- **Param 43 (Benefits language)** - Need to rewrite copy focusing on benefits not features

---

## TIER 3: CONTENT & UX (50 params) - 60% Coverage

| # | Parameter | Type | What Script Does | What Manual Needed |
|---|-----------|------|------------------|-------------------|
| 46 | **Paragraph length** | **✋ MANUAL** | - | Break long paragraphs |
| 47 | Bullet lists | 🤖 AUTO | Adds list sections | None |
| 48 | **Section count** | **✋ MANUAL** | - | Restructure layout |
| 49 | Readability | ⚙️ SEMI | Adds simple sentences | Simplify complex text |
| 50 | Semantic keywords | 🤖 AUTO | Adds related terms | None |
| 51 | Question headers | 🤖 AUTO | Converts to questions | None |
| 52 | Answer format | 🤖 AUTO | Structures Q&A | None |
| 53 | Table of contents | 🤖 AUTO | Generates TOC | None |
| 54 | Jump links | 🤖 AUTO | Adds anchor links | None |
| 55 | **Related content** | **✋ MANUAL** | - | Add cross-links |
| 56 | Authority signals | 🤖 AUTO | Adds credentials | None |
| 57 | Pain points | 🤖 AUTO | Adds problem text | None |
| 58 | Benefit headers | 🤖 AUTO | Converts headers | None |
| 59 | Active voice | ⚙️ SEMI | Detects passive only | Rewrite passive sentences |
| 60 | **Technical explanations** | **✋ MANUAL** | - | Add how-to content |
| 61 | FAQ section | 🤖 AUTO | Adds FAQ template | Customize answers |
| 62 | Process guides | 🤖 AUTO | Adds step template | Customize steps |
| 63 | Comparison tables | ⚙️ SEMI | Adds table template | Add real data |
| 64 | Stats/data | 🤖 AUTO | Adds generic stats | Add real metrics |
| 65 | Expert quotes | ⚙️ SEMI | Adds placeholder | Add real quotes |
| 66 | **Page speed** | **🔧 SERVER** | - | Minify, compress, CDN |
| 67 | Lazy loading | 🤖 AUTO | Adds loading="lazy" | None |
| 68 | Mobile breakpoints | 🤖 AUTO | Adds media queries | None |
| 69 | Responsive typography | 🤖 AUTO | Adds responsive CSS | None |
| 70 | Color contrast | 🤖 AUTO | Adjusts colors | None |
| 71 | Font size | 🤖 AUTO | Adjusts small fonts | None |
| 72 | Whitespace | 🤖 AUTO | Adds spacing CSS | None |
| 73 | Visual hierarchy | 🤖 AUTO | Adjusts sizes | None |
| 74 | Click targets | 🤖 AUTO | Adds min size CSS | None |
| 75 | Form validation | 🤖 AUTO | Adds required attrs | None |
| 76 | Error messages | 🤖 AUTO | Adds error markup | None |
| 77 | Success states | 🤖 AUTO | Adds success markup | None |
| 78 | Loading indicators | 🤖 AUTO | Adds spinner CSS | None |
| 79 | Hover states | 🤖 AUTO | Adds hover CSS | None |
| 80 | Focus indicators | 🤖 AUTO | Adds focus CSS | None |
| 81 | Skip navigation | 🤖 AUTO | Adds skip link | None |
| 82 | Keyboard accessible | 🤖 AUTO | Adds tabindex | None |
| 83 | Screen reader | 🤖 AUTO | Adds ARIA labels | None |
| 84 | Touch-friendly | 🤖 AUTO | Adds touch CSS | None |
| 85 | Hamburger menu | 🤖 AUTO | Checks existence | None |
| 86 | **Search function** | **✋ MANUAL** | - | Add search feature |
| 87 | Breadcrumb visible | 🤖 AUTO | Ensures visible | None |
| 88 | **Back to top** | **🤖 AUTO** | Adds button | None |
| 89 | Print styles | 🤖 AUTO | Adds @media print | None |
| 90 | Favicon | 🤖 AUTO | Checks existence | None |
| 91 | 404 page | ⚙️ SEMI | Info only | Create 404.html |
| 92 | Thank you page | ⚙️ SEMI | Info only | Create thanks.html |
| 93 | Privacy policy | 🤖 AUTO | Checks link exists | None |
| 94 | Terms link | 🤖 AUTO | Checks link exists | None |
| 95 | Cookie notice | 🤖 AUTO | Adds banner | None |

**TIER 3 AUTO-FIX RATE:** 30/50 (60%)

**Manual Required (10 params):**
- Paragraph restructuring
- Section layout
- Related content links
- Technical explanations writing
- Page speed optimization (server)
- Search feature implementation

---

## TIER 5: ADVANCED UX (30 params) - 40% Coverage

| # | Parameter | Type | What Script Does | What Manual Needed |
|---|-----------|------|------------------|-------------------|
| 126 | CSS animations | 🤖 AUTO | Adds keyframes | None |
| 127 | Scroll effects | 🤖 AUTO | Adds IntersectionObserver | None |
| 128 | **Parallax** | **✋ MANUAL** | - | Complex JS implementation |
| 129 | Video elements | ⚙️ SEMI | Adds video template | Upload real videos |
| 130 | Interactive elements | 🤖 AUTO | Checks existence | None |
| 131 | PWA manifest | 🤖 AUTO | Adds manifest link | Create manifest.json |
| 132 | **Service worker** | **✋ MANUAL** | - | Write SW logic |
| 133 | **Offline fallback** | **✋ MANUAL** | - | Create offline page |
| 134 | App icons | 🤖 AUTO | Adds icon links | Create icon files |
| 135 | **Push notifications** | **🔌 EXTERNAL** | - | Setup push service |
| 136 | **Geolocation** | **✋ MANUAL** | - | Implement geo API |
| 137 | Maps integration | ⚙️ SEMI | Adds iframe embed | Get API key |
| 138 | **Live chat** | **🔌 EXTERNAL** | - | Setup chat service |
| 139 | **Real-time updates** | **✋ MANUAL** | - | Implement WebSocket |
| 140 | **Chatbot** | **🔌 EXTERNAL** | - | Setup chatbot service |
| 141 | **Social sharing** | **⚙️ SEMI** | Adds share buttons | Configure URLs |
| 142 | **Social login** | **🔌 EXTERNAL** | - | OAuth integration |
| 143 | **Bookmark function** | **✋ MANUAL** | - | Implement save logic |
| 144 | **Cost calculator** | **⚙️ SEMI** | Adds calculator HTML | Add real pricing |
| 145 | **Comparison tool** | **✋ MANUAL** | - | Build comparison UI |
| 146 | Multi-step forms | 🤖 AUTO | Adds step CSS | None |
| 147 | Progress indicators | 🤖 AUTO | Adds progress CSS | None |
| 148 | Tooltips | 🤖 AUTO | Adds tooltip CSS | None |
| 149 | Modal dialogs | 🤖 AUTO | Adds modal HTML | None |
| 150 | **Slide panels** | **✋ MANUAL** | - | Implement drawer |
| 151 | Expandable sections | 🤖 AUTO | Checks accordion | None |
| 152 | Infinite scroll | ⚙️ SEMI | Info only | Implement if needed |
| 153 | Sticky elements | 🤖 AUTO | Adds sticky CSS | None |
| 154 | Smooth scrolling | 🤖 AUTO | Adds CSS property | None |
| 155 | Loading states | 🤖 AUTO | Adds loader markup | None |

**TIER 5 AUTO-FIX RATE:** 12/30 (40%)

**Many are optional or require external services**

---

## TIER 7: CONTENT FEATURES (30 params) - 30% Coverage

| # | Parameter | Type | What Script Does | What Manual Needed |
|---|-----------|------|------------------|-------------------|
| 184 | **Video tutorials** | **✋ MANUAL** | Adds embed template | Create/upload videos |
| 185 | **Video testimonials** | **✋ MANUAL** | Adds embed template | Record testimonials |
| 186 | Before/after gallery | ⚙️ SEMI | Adds gallery template | Add real photos |
| 187 | Photo galleries | ⚙️ SEMI | Adds gallery HTML | Add real photos |
| 188 | **Image optimization** | **🔧 SERVER** | - | Convert to WebP |
| 189 | Image lazy loading | 🤖 AUTO | Adds loading attr | None |
| 190 | Image captions | ⚙️ SEMI | Adds figcaption | Write captions |
| 191 | Alt text quality | 🤖 AUTO | Improves alt text | None |
| 192 | **Infographics** | **✋ MANUAL** | - | Design infographics |
| 193 | **Downloadable guides** | **✋ MANUAL** | Adds section | Create PDF files |
| 194 | **PDF resources** | **✋ MANUAL** | - | Create PDFs |
| 195 | **Checklists** | **⚙️ SEMI** | Adds checkbox list | Customize items |
| 196 | Templates | ⚙️ SEMI | Info only | Create templates |
| 197 | **Case studies** | **✋ MANUAL** | Adds template | Write real cases |
| 198 | Customer stories | ⚙️ SEMI | Adds template | Write real stories |
| 199 | Review display | 🤖 AUTO | Ensures visible | None |
| 200 | Review schema | 🤖 AUTO | Adds Review markup | None |
| 201 | Review filtering | ⚙️ SEMI | Info only | Implement filters |
| 202 | Review pagination | ⚙️ SEMI | Info only | Implement pages |
| 203 | Video reviews | ⚙️ SEMI | Adds template | Upload videos |
| 204 | **Photo reviews** | **✋ MANUAL** | - | Collect photos |
| 205 | Cost calculator | ⚙️ SEMI | Adds calculator | Add real prices |
| 206 | **ROI calculator** | **✋ MANUAL** | - | Build calculator |
| 207 | **Interactive diagrams** | **✋ MANUAL** | - | Create diagrams |
| 208 | Embedded tools | ⚙️ SEMI | Checks iframes | None |
| 209 | Pricing tables | 🤖 AUTO | Adds table HTML | None |
| 210 | Package comparison | ⚙️ SEMI | Adds table | Add packages |
| 211 | **Service bundles** | **✋ MANUAL** | - | Define bundles |
| 212 | Seasonal content | ⚙️ SEMI | Adds offer template | Update offers |
| 213 | Blog integration | ⚙️ SEMI | Info only | Create blog |

**TIER 7 AUTO-FIX RATE:** 9/30 (30%)

**Most require real content creation**

---

## TIER 9: POLISH & PERFORMANCE (34 params) - 50% Coverage

| # | Parameter | Type | What Script Does | What Manual Needed |
|---|-----------|------|------------------|-------------------|
| 244 | **Code minification** | **🔧 SERVER** | - | Build process |
| 245 | **GZIP compression** | **🔧 SERVER** | - | Server config |
| 246 | **CDN usage** | **🔧 SERVER** | - | Setup CDN |
| 247 | Resource hints | 🤖 AUTO | Adds preconnect | None |
| 248 | Critical CSS | 🤖 AUTO | Inlines CSS | None |
| 249 | Async CSS | ⚙️ SEMI | Adds preload | None |
| 250 | Font optimization | 🤖 AUTO | Adds font-display | None |
| 251 | Asset versioning | ⚙️ SEMI | Adds ?v= params | Automate in build |
| 252 | **Browser caching** | **🔧 SERVER** | - | Server headers |
| 253 | Image srcset | ⚙️ SEMI | Adds guide | Generate sizes |
| 254 | WebP support | ⚙️ SEMI | Adds guide | Convert images |
| 255 | **HTTP/2** | **🔧 SERVER** | - | Server config |
| 256 | SSL/TLS | 🤖 AUTO | Checks https:// | None |
| 257 | **Security headers** | **🔧 SERVER** | - | Server config |
| 258 | CSP | 🤖 AUTO | Adds meta CSP | None |
| 259 | XSS protection | ⚙️ SEMI | Adds meta tag | Server headers better |
| 260 | CORS | ⚙️ SEMI | Info only | If needed |
| 261 | **Analytics** | **⚙️ SEMI** | Adds GA code | Add real GA ID |
| 262 | **GTM** | **⚙️ SEMI** | Adds GTM code | Add real GTM ID |
| 263 | Conversion tracking | 🤖 AUTO | Adds event code | None |
| 264 | Error tracking | 🤖 AUTO | Adds error handler | None |
| 265 | GDPR compliance | 🤖 AUTO | Adds cookie banner | None |
| 266 | Privacy policy | 🤖 AUTO | Checks link | None |
| 267 | Terms of service | 🤖 AUTO | Checks link | None |
| 268 | Accessibility stmt | 🤖 AUTO | Adds link | None |
| 269 | Sitemap | ⚙️ SEMI | Adds link | Generate sitemap.xml |
| 270 | **Robots.txt** | **✋ MANUAL** | - | Create robots.txt |
| 271 | Canonical URL | 🤖 AUTO | Adds tag | None |
| 272 | Hreflang | ⚙️ SEMI | Info only | If multilingual |
| 273 | Social meta | 🤖 AUTO | Adds OG/Twitter | None |
| 274 | Favicon variants | 🤖 AUTO | Checks icons | None |
| 275 | Apple touch icon | 🤖 AUTO | Checks icon | None |
| 276 | Theme color | 🤖 AUTO | Adds meta | None |
| 277 | HTML validation | 🤖 AUTO | Checks structure | None |

**TIER 9 AUTO-FIX RATE:** 17/34 (50%)

**Many require server configuration**

---

## SUMMARY BY TYPE

### 🤖 FULLY AUTO (112 params - 40.4%)
Can be fixed 100% automatically with scripts

### ⚙️ SEMI-AUTO (48 params - 17.3%)
Script adds template/structure, needs manual data/customization

### ✋ FULLY MANUAL (43 params - 15.5%)
Requires human creativity, writing, or complex logic

### 🔧 SERVER-SIDE (13 params - 4.7%)
Requires server configuration

### 🔌 EXTERNAL (7 params - 2.5%)
Requires external service integration

### 📊 INFO-ONLY (54 params - 19.5%)
Tiers 4, 6, 8 - testing/verification only

---

## CURRENT CRITICAL ISSUES REQUIRING MANUAL WORK

### 🔴 PRIORITY 1 (Blocking SEO):
1. **Content Uniqueness (Param 16)** - 99.9% duplicate between pages
   - **Action:** Rewrite each page for its appliance type
   - **Time:** 2-3 hours
   - **Impact:** CRITICAL for Google indexing

2. **Keyword Density (Param 18)** - 3.3% (need 2.5%)
   - **Action:** Dilute keyword repetition with varied text
   - **Time:** 30 min per page
   - **Impact:** HIGH for SEO

### 🟡 PRIORITY 2 (Optimization):
3. **Benefits Language (Param 43)** - Too feature-focused
   - **Action:** Rewrite focusing on customer benefits
   - **Time:** 1 hour
   - **Impact:** MEDIUM for conversions

4. **CTA Count (Param 32)** - 14-17 CTAs (optimal: 3-8)
   - **Action:** Remove excess CTAs
   - **Time:** 15 min per page
   - **Impact:** MEDIUM for UX

### 🟢 CAN ADD AUTO-FIX:
5. **Contact in Footer (Param 44)** - Missing
   - **Action:** Create tier2_fixer enhancement
   - **Time:** 15 min to code
   - **Impact:** LOW but easy win

6. **Back to Top (Param 88)** - Missing
   - **Action:** Create tier3_fixer enhancement
   - **Time:** 10 min to code
   - **Impact:** LOW for UX

---

## RECOMMENDED ACTION PLAN

### Step 1: Quick Auto-Fixes (30 min)
```bash
# Add missing auto-fixable features
- Contact in footer
- Back to top button
- Social sharing buttons (basic)
```

### Step 2: Manual Content (CRITICAL - 3 hours)
```
Rewrite unique content for each page:
- dishwasher-repair.html → dishwasher-specific problems/solutions
- washer-repair.html → washer-specific issues
- dryer-repair.html → dryer-specific problems
- oven-repair.html → oven-specific content
- freezer-repair.html → freezer-specific text
- refrigerator-repair.html → already better, refine more
```

### Step 3: Content Optimization (1 hour)
```
- Reduce keyword density
- Remove excess CTAs
- Improve benefits language
```

**TOTAL TIME:** ~4.5 hours to reach optimal state

---

**Created:** BMAD v2
**Last Updated:** 10 октября 2025
**Purpose:** Guide for understanding what can be automated vs manual work
