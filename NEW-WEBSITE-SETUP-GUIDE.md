# 🚀 Правильный Старт Нового Сайта
## Полный чек-лист для избежания SEO и технических проблем

**Дата создания:** November 2025
**Основано на опыте:** NikaApplianceRepair.com

---

## 📋 PHASE 1: Планирование (ДО написания кода)

### 1.1 Определи URL структуру СРАЗУ

**✅ ПРАВИЛЬНО:**
```
https://example.com/blog/category/post-name
https://example.com/services/service-name
https://example.com/locations/city-name
```

**❌ НЕПРАВИЛЬНО:**
```
https://example.com/blog/category/post-name.html
https://example.com/page.php?id=123
https://example.com/index.html
```

**Принципы clean URLs:**
- Без расширений файлов (.html, .php, .aspx)
- Используй `-` для разделения слов (не `_`)
- Только lowercase буквы
- Короткие, понятные, SEO-friendly
- Иерархическая структура

---

### 1.2 Выбери хостинг и платформу

**Рекомендуемые платформы:**

| Платформа | Плюсы | Минусы | Когда использовать |
|-----------|-------|--------|-------------------|
| **Vercel** | Auto clean URLs, CDN, GitHub интеграция | Только статика/Next.js | Static sites, Next.js |
| **Netlify** | Аналогично Vercel + forms | Дорого для больших | Static sites |
| **Cloudflare Pages** | Бесплатно, быстро | Меньше функций | Простые проекты |
| **VPS (DigitalOcean)** | Полный контроль | Нужна настройка | Сложные проекты |

**Что настроить СРАЗУ:**
- ✅ Clean URLs (в конфиге хостинга)
- ✅ HTTPS (SSL сертификат)
- ✅ WWW vs non-WWW (выбери один вариант)
- ✅ Trailing slash policy (с `/` или без)

---

## 📋 PHASE 2: Начальная Настройка

### 2.1 Создай конфигурационные файлы

#### **Для Vercel (`vercel.json`):**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "cleanUrls": true,
  "trailingSlash": false,

  "redirects": [
    {
      "source": "/:path*.html",
      "destination": "/:path*",
      "permanent": true
    },
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    }
  ],

  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    },
    {
      "source": "/(.*).(jpg|jpeg|png|webp|gif|svg|ico)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

#### **Для Nginx (`nginx.conf`):**

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect www to non-www
    if ($host = 'www.example.com') {
        return 301 https://example.com$request_uri;
    }

    # Force HTTPS
    return 301 https://example.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    root /var/www/html;
    index index.html;

    # Clean URLs - remove .html
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    # Redirect .html to clean URLs
    if ($request_uri ~ ^/(.*)\.html$) {
        return 301 /$1;
    }

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Caching
    location ~* \.(jpg|jpeg|png|webp|gif|svg|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### **Для Apache (`.htaccess`):**

```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Remove www
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Clean URLs - remove .html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^([^\.]+)$ $1.html [NC,L]

# Redirect .html to clean URLs
RewriteCond %{THE_REQUEST} ^[A-Z]{3,9}\ /([^.]+)\.html\ HTTP
RewriteRule ^([^.]+)\.html$ /$1 [R=301,L]

# Security headers
Header always set X-Frame-Options "DENY"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"

# Caching
<FilesMatch "\.(jpg|jpeg|png|webp|gif|svg|ico|css|js)$">
    Header set Cache-Control "max-age=31536000, public"
</FilesMatch>
```

---

### 2.2 HTML Шаблон с правильными мета-тегами

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- ВАЖНО: Canonical ВСЕГДА указывает на clean URL -->
    <link rel="canonical" href="https://example.com/page-path">

    <!-- SEO Meta Tags -->
    <title>Page Title - Your Brand Name</title>
    <meta name="description" content="Page description (150-160 characters)">
    <meta name="keywords" content="keyword1, keyword2, keyword3">
    <meta name="author" content="Your Name">

    <!-- Open Graph (Facebook, LinkedIn) -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://example.com/page-path">
    <meta property="og:title" content="Page Title">
    <meta property="og:description" content="Page description">
    <meta property="og:image" content="https://example.com/images/og-image.jpg">
    <meta property="og:site_name" content="Your Brand">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://example.com/page-path">
    <meta name="twitter:title" content="Page Title">
    <meta name="twitter:description" content="Page description">
    <meta name="twitter:image" content="https://example.com/images/twitter-image.jpg">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

    <!-- Preconnect for performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://cdn.example.com">

    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "Page Title",
      "description": "Page description",
      "url": "https://example.com/page-path",
      "publisher": {
        "@type": "Organization",
        "name": "Your Brand",
        "logo": {
          "@type": "ImageObject",
          "url": "https://example.com/logo.png"
        }
      }
    }
    </script>
</head>
<body>
    <!-- Your content -->
</body>
</html>
```

**Правила для canonical тегов:**
```html
<!-- ✅ ПРАВИЛЬНО - Absolute URL без .html -->
<link rel="canonical" href="https://example.com/blog/post-title">

<!-- ❌ НЕПРАВИЛЬНО - Relative URL -->
<link rel="canonical" href="/blog/post-title">

<!-- ❌ НЕПРАВИЛЬНО - С .html расширением -->
<link rel="canonical" href="https://example.com/blog/post-title.html">

<!-- ❌ НЕПРАВИЛЬНО - С параметрами -->
<link rel="canonical" href="https://example.com/blog/post-title?page=2">
```

---

## 📋 PHASE 3: SEO Инфраструктура

### 3.1 Создай sitemap.xml с первого дня

**Используй автоматический генератор:**

```python
# sitemap_generator.py
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_sitemap():
    base_url = "https://example.com"
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Static pages
    pages = [
        ('/', '1.0', 'weekly'),
        ('/about', '0.9', 'monthly'),
        ('/contact', '0.8', 'monthly'),
    ]

    for path, priority, changefreq in pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = base_url + path
        ET.SubElement(url, 'lastmod').text = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(url, 'changefreq').text = changefreq
        ET.SubElement(url, 'priority').text = priority

    # Auto-discover HTML files
    for html_file in Path('.').rglob('*.html'):
        if 'template' not in str(html_file):
            # Convert file path to clean URL
            path = str(html_file).replace('\\', '/').replace('.html', '')
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"{base_url}/{path}"
            ET.SubElement(url, 'lastmod').text = datetime.now().strftime("%Y-%m-%d")
            ET.SubElement(url, 'changefreq').text = 'weekly'
            ET.SubElement(url, 'priority').text = '0.8'

    # Pretty print and save
    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

if __name__ == "__main__":
    generate_sitemap()
```

**Запускай после каждого добавления страниц:**
```bash
python sitemap_generator.py
```

---

### 3.2 Создай robots.txt

```txt
# robots.txt
User-agent: *
Allow: /

# Sitemap location
Sitemap: https://example.com/sitemap.xml

# Disallow admin/private areas
Disallow: /admin/
Disallow: /private/
Disallow: /*.json$
Disallow: /*.xml$

# Crawl delay (optional, only if needed)
# Crawl-delay: 10
```

---

### 3.3 Настрой Google Search Console ДО запуска

**Шаги:**
1. Зайди на https://search.google.com/search-console
2. Add property → введи домен
3. Verify ownership (DNS или HTML file)
4. Submit sitemap.xml
5. Request indexing для главной страницы

---

## 📋 PHASE 4: Структура Проекта

### 4.1 Правильная файловая структура

```
my-website/
├── index.html                 # Главная страница
├── about.html                 # О нас
├── contact.html               # Контакты
├── sitemap.xml                # Sitemap
├── robots.txt                 # Robots.txt
├── favicon.ico                # Favicon
│
├── blog/
│   ├── index.html            # Список блог постов
│   ├── guides/
│   │   ├── post-1.html       # БЕЗ .html в URL!
│   │   └── post-2.html
│   └── news/
│       └── article-1.html
│
├── services/
│   ├── index.html
│   ├── service-1.html
│   └── service-2.html
│
├── locations/
│   ├── index.html
│   ├── city-1.html
│   └── city-2.html
│
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── logo.png
│
├── templates/               # Не индексировать!
│   └── page-template.html
│
└── scripts/
    ├── sitemap_generator.py
    └── deploy.sh
```

**Важно:**
- Файлы с `.html` расширением существуют физически
- НО в URL они доступны БЕЗ .html
- Redirectы настроены в `vercel.json` или `.htaccess`

---

## 📋 PHASE 5: Тестирование ПЕРЕД запуском

### 5.1 Чек-лист тестов

**SEO тесты:**
- [ ] Все страницы имеют уникальные `<title>` и `<meta description>`
- [ ] Canonical теги указывают на clean URLs
- [ ] Sitemap содержит только clean URLs (без .html)
- [ ] robots.txt правильно настроен
- [ ] Open Graph и Twitter Card теги присутствуют
- [ ] Structured data (JSON-LD) валидна

**Технические тесты:**
- [ ] HTTPS работает (без предупреждений)
- [ ] WWW редиректит на non-WWW (или наоборот)
- [ ] `.html` URLs редиректят на clean URLs (301)
- [ ] 404 страница существует и красиво оформлена
- [ ] Все изображения оптимизированы (WebP, сжатие)
- [ ] CSS и JS минифицированы

**Performance тесты:**
- [ ] Google PageSpeed Insights: 90+ баллов
- [ ] Lighthouse: все категории зелёные
- [ ] WebP images используются
- [ ] Lazy loading для изображений
- [ ] Critical CSS inline в `<head>`

**Инструменты для тестирования:**
```bash
# PageSpeed Insights
https://pagespeed.web.dev/

# Lighthouse
npx lighthouse https://example.com --view

# W3C Validator
https://validator.w3.org/

# Schema Markup Validator
https://validator.schema.org/

# Mobile-Friendly Test
https://search.google.com/test/mobile-friendly
```

---

## 📋 PHASE 6: Запуск и Мониторинг

### 6.1 День запуска чек-лист

**Утро запуска:**
- [ ] Final git commit и push
- [ ] Deploy на production
- [ ] Проверь что сайт доступен по домену
- [ ] Submit sitemap в Google Search Console
- [ ] Submit sitemap в Bing Webmaster Tools
- [ ] Создай Google Analytics property
- [ ] Настрой Google Tag Manager (опционально)

**Первая неделя:**
- [ ] Мониторь Google Search Console Coverage report
- [ ] Проверяй Index status ежедневно
- [ ] Фиксируй любые 404 ошибки
- [ ] Request indexing для важных страниц

**Первый месяц:**
- [ ] Анализируй Search Analytics
- [ ] Проверяй Mobile Usability
- [ ] Мониторь Core Web Vitals
- [ ] Исправляй найденные проблемы

---

### 6.2 Автоматизация мониторинга

**Создай скрипт для проверки:**

```bash
#!/bin/bash
# health_check.sh

DOMAIN="https://example.com"

# Check if site is up
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}\n" $DOMAIN)
if [ $HTTP_CODE -ne 200 ]; then
    echo "❌ Site is DOWN! HTTP Code: $HTTP_CODE"
    exit 1
fi

# Check if sitemap is accessible
SITEMAP_CODE=$(curl -o /dev/null -s -w "%{http_code}\n" $DOMAIN/sitemap.xml)
if [ $SITEMAP_CODE -ne 200 ]; then
    echo "⚠️ Sitemap not accessible!"
fi

# Check if .html redirects work
HTML_CODE=$(curl -o /dev/null -s -w "%{http_code}\n" -L $DOMAIN/about.html)
if [ $HTML_CODE -ne 200 ]; then
    echo "⚠️ .html redirect not working!"
fi

echo "✅ All checks passed!"
```

**Запускай ежедневно через cron:**
```cron
0 9 * * * /path/to/health_check.sh
```

---

## 📋 BONUS: Частые Ошибки и Как Их Избежать

### ❌ Ошибка 1: Дублирующиеся URLs

**Проблема:**
```
https://example.com/page
https://example.com/page.html
https://example.com/page/
https://www.example.com/page
```

**Решение:**
- Выбери ОДИН формат (рекомендую: без www, без .html, без trailing slash)
- Настрой 301 редиректы для всех остальных вариантов
- Используй canonical теги

---

### ❌ Ошибка 2: Плохие canonical теги

**Проблема:**
```html
<link rel="canonical" href="/blog/post">  <!-- Relative URL -->
<link rel="canonical" href="page.html">    <!-- С .html -->
```

**Решение:**
```html
<link rel="canonical" href="https://example.com/blog/post">
```

**Создай helper функцию:**
```javascript
function getCanonicalUrl() {
    const protocol = window.location.protocol;
    const host = window.location.host;
    const pathname = window.location.pathname.replace('.html', '');
    return `${protocol}//${host}${pathname}`;
}
```

---

### ❌ Ошибка 3: Забыли про mobile

**Проблема:**
- Сайт не адаптивный
- Мелкий текст
- Кнопки слишком маленькие

**Решение:**
```html
<!-- В <head> -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

```css
/* В CSS - Mobile-first подход */
/* Base styles для mobile */
body {
    font-size: 16px;
    line-height: 1.6;
}

/* Desktop стили в media queries */
@media (min-width: 768px) {
    body {
        font-size: 18px;
    }
}
```

---

### ❌ Ошибка 4: Медленная загрузка

**Проблема:**
- Большие изображения
- Нет кэширования
- Много JavaScript

**Решение:**

1. **Оптимизируй изображения:**
```bash
# Конвертируй в WebP
cwebp input.jpg -q 85 -o output.webp

# Или используй online:
# https://squoosh.app/
```

2. **Используй lazy loading:**
```html
<img src="image.jpg" loading="lazy" alt="Description">
```

3. **Настрой кэширование:**
```html
<!-- In vercel.json -->
{
  "headers": [
    {
      "source": "/(.*).(jpg|png|webp|css|js)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## 🎯 Итоговый Quick Start Checklist

### День 0: Планирование
- [ ] Определил URL структуру (clean URLs!)
- [ ] Выбрал хостинг (Vercel/Netlify/etc)
- [ ] Зарегистрировал домен
- [ ] Настроил DNS

### День 1: Настройка
- [ ] Создал `vercel.json` или `.htaccess`
- [ ] Настроил clean URLs
- [ ] Настроил 301 redirects
- [ ] Создал HTML template с правильными мета-тегами
- [ ] Создал `robots.txt`

### День 2-7: Разработка
- [ ] Создал страницы с уникальными title/description
- [ ] Добавил canonical теги (absolute URLs!)
- [ ] Оптимизировал изображения (WebP)
- [ ] Минифицировал CSS/JS
- [ ] Создал 404 страницу

### День 8: Pre-launch
- [ ] Создал sitemap.xml (автоматически)
- [ ] Проверил все страницы на mobile
- [ ] Запустил Lighthouse audit
- [ ] Проверил .html redirects
- [ ] Проверил canonical теги

### День 9: Launch!
- [ ] Deploy на production
- [ ] Проверил доступность сайта
- [ ] Submit sitemap в GSC
- [ ] Настроил Google Analytics
- [ ] Request indexing главной страницы

### Месяц 1: Мониторинг
- [ ] Проверяю GSC Coverage daily
- [ ] Исправляю найденные ошибки
- [ ] Анализирую Search Analytics
- [ ] Оптимизирую под Core Web Vitals

---

## 📚 Полезные Ресурсы

**Документация:**
- Vercel: https://vercel.com/docs
- Google Search Console: https://support.google.com/webmasters
- Schema.org: https://schema.org/

**Инструменты:**
- PageSpeed Insights: https://pagespeed.web.dev/
- Mobile-Friendly Test: https://search.google.com/test/mobile-friendly
- Structured Data Validator: https://validator.schema.org/
- SEO Checker: https://www.seobility.net/en/seocheck/

**Обучение:**
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Web.dev: https://web.dev/learn/

---

## ✅ Заключение

**Следуй этому гайду и у тебя будет:**
- ✅ Правильная URL структура с первого дня
- ✅ Никаких дублирующихся URLs
- ✅ Отличное SEO с момента запуска
- ✅ Быстрая загрузка страниц
- ✅ Мобильная адаптация
- ✅ Автоматизированный мониторинг

**Главное правило:** Делай правильно СРАЗУ, чтобы не исправлять потом!

---

**Created by:** Claude Code
**Based on:** Real-world experience fixing NikaApplianceRepair.com
**Last updated:** November 2025
