# 📍 ПЛАН: 20 Новых Location Pages с BMAD Оптимизацией

**Дата:** 2025-10-17
**Базовая страница:** Richmond Hill (лучший BMAD score)
**Метод:** Дупликация + Уникализация критических параметров
**Цель:** Покрыть весь GTA по популяции

---

## 🎯 СТРАТЕГИЯ

### Основной подход:
1. **Дупликация Richmond Hill** - берем как template (уже оптимизирована по BMAD)
2. **Уникализация ключевых элементов** - SEO + локальный контент
3. **Автоматизация** - PowerShell + AI агенты для массового создания
4. **BMAD Tier 1-2 обязательно** - критические параметры для каждой страницы

### Что будет уникальным:

✅ **Tier 1 - Data Consistency (100% обязательно):**
- Location name (город)
- H1 title
- Meta title
- Meta description
- Schema.org addressLocality + geo coordinates
- URL canonical
- OG tags (title, description, url)

✅ **Tier 2 - SEO Content (85%+ цель):**
- Уникальный hero paragraph (150-200 слов)
- Local keywords (город + appliance repair)
- Neighborhoods served (3-5 районов в городе)
- Common problems section (3-5 локальных проблем) - САМОЕ ГЛАВНОЕ
- FAQ (5-7 вопросов специфичных для локации)
- Internal links к другим location pages

✅ **AI Search Optimization (98% обязательно):**
- Speakable schema с местным контентом
- HowTo schema ("How to get appliance repair in [город]")
- FAQ schema с местными вопросами
- WebPage schema with mainEntity

### Что остается одинаковым:
- Phone: 437-524-1053
- Booking form (Workiz iframe)
- Trust sidebar ("Why Choose Nika?")
- Warranty: 90-day
- Rating: 4.9/5
- Service list (refrigerator, washer, dryer, etc.)
- CSS/JS файлы

---

## 📊 20 НОВЫХ ЛОКАЦИЙ (По Популяции GTA)

### Критерии выбора:
1. Население 20,000+
2. В радиусе 80km от Toronto
3. Search volume для "[city] appliance repair"
4. Покрытие всего GTA + York Region + Durham Region

### Финальный список:

| # | Город | Население | Район | Приоритет | Ключевые районы |
|---|-------|-----------|-------|-----------|-----------------|
| 1 | **Etobicoke** | 365,000 | Toronto | 🔴 CRITICAL | Long Branch, Islington, Kingsway |
| 2 | **North York** | 672,000 | Toronto | 🔴 CRITICAL | Willowdale, Don Mills, Sheppard |
| 3 | **Scarborough** | 632,000 | Toronto | 🔴 CRITICAL | Agincourt, Wexford, Malvern |
| 4 | **Newmarket** | 87,000 | York | 🟠 HIGH | Stonehaven, Bristol, Armitage |
| 5 | **Aurora** | 62,000 | York | 🟠 HIGH | Town Centre, Oak Ridges Moraine |
| 6 | **Whitby** | 138,000 | Durham | 🟠 HIGH | Brooklin, Downtown, Pringle Creek |
| 7 | **Stouffville** | 49,000 | York | 🟠 HIGH | Old Stouffville, Ballantrae |
| 8 | **Caledon** | 76,000 | Peel | 🟠 HIGH | Bolton, Caledon East, Inglewood |
| 9 | **Clarington** | 100,000 | Durham | 🟠 HIGH | Bowmanville, Courtice, Newcastle |
| 10 | **Halton Hills** | 62,000 | Halton | 🟢 MEDIUM | Georgetown, Acton |
| 11 | **Bradford** | 36,000 | Simcoe | 🟢 MEDIUM | Bradford West, Gwillimbury |
| 12 | **East Gwillimbury** | 24,000 | York | 🟢 MEDIUM | Mount Albert, Holland Landing |
| 13 | **King** | 27,000 | York | 🟢 MEDIUM | King City, Nobleton, Schomberg |
| 14 | **Georgina** | 48,000 | York | 🟢 MEDIUM | Keswick, Sutton, Pefferlaw |
| 15 | **Innisfil** | 43,000 | Simcoe | 🟢 MEDIUM | Alcona, Stroud, Lefroy |
| 16 | **Orangeville** | 30,000 | Dufferin | 🟢 MEDIUM | Downtown, Mono Mills |
| 17 | **Uxbridge** | 21,000 | Durham | 🟢 MEDIUM | Downtown, Goodwood |
| 18 | **Scugog** | 22,000 | Durham | 🟢 MEDIUM | Port Perry, Seagrave |
| 19 | **Brock** | 12,000 | Durham | 🟡 LOW | Cannington, Beaverton |
| 20 | **Mono** | 9,000 | Dufferin | 🟡 LOW | Mono Centre, Camilla |

---

## 🤖 АВТОМАТИЧЕСКИЙ WORKFLOW

### Phase 1: Создание базовых файлов (PowerShell)

```powershell
# create-location-pages.ps1

$locations = @(
    @{Name="Etobicoke"; Slug="etobicoke"; Lat="43.6205"; Lon="-79.5132"; Neighborhoods="Long Branch, Islington, Kingsway"},
    @{Name="North York"; Slug="north-york"; Lat="43.7615"; Lon="-79.4111"; Neighborhoods="Willowdale, Don Mills, Sheppard"},
    @{Name="Scarborough"; Slug="scarborough"; Lat="43.7731"; Lon="-79.2578"; Neighborhoods="Agincourt, Wexford, Malvern"},
    # ... all 20 locations
)

foreach ($loc in $locations) {
    # Copy Richmond Hill template
    Copy-Item "locations\richmond-hill.html" "locations\$($loc.Slug).html"

    # Replace basic placeholders
    $content = Get-Content "locations\$($loc.Slug).html" -Raw

    # Replace city name
    $content = $content -replace "Richmond Hill", $loc.Name
    $content = $content -replace "richmond-hill", $loc.Slug

    # Replace coordinates
    $content = $content -replace '"latitude": "44.0389"', "`"latitude`": `"$($loc.Lat)`""
    $content = $content -replace '"longitude": "-79.4537"', "`"longitude`": `"$($loc.Lon)`""

    Set-Content -Path "locations\$($loc.Slug).html" -Value $content -NoNewline

    Write-Host "✓ Created: $($loc.Name)"
}
```

### Phase 2: AI Content Generation (Агенты)

Для каждой локации нужно сгенерировать:

**1. Hero Section (150-200 слов):**
```
Example for Etobicoke:
"Looking for fast, reliable appliance repair in Etobicoke? Nika Appliance Repair
serves all neighborhoods including Long Branch, Islington, and Kingsway with same-day
service 7 days a week. Our licensed technicians specialize in repairing all major
appliance brands right in your home..."
```

**2. Common Problems (3-5 local issues):**
```
Example for Etobicoke (well water issues):
- Hard water buildup in dishwashers (common in older Etobicoke homes)
- Washer drainage issues in basement installations
- Refrigerator condensation from lake humidity
```

**3. FAQ (5-7 questions):**
```
Example for Etobicoke:
Q: Do you service all Etobicoke neighborhoods?
A: Yes! We serve Long Branch, Islington, Kingsway, Humber Bay, and all Etobicoke areas.

Q: Same-day service in Etobicoke?
A: Absolutely. We typically arrive within 2-3 hours of your call in Etobicoke.

Q: Do you repair appliances near Lake Ontario (waterfront condos)?
A: Yes, we specialize in high-rise appliance repair in waterfront buildings.
```

**4. Neighborhoods Section:**
```
We proudly serve all Etobicoke communities:
- Long Branch
- Islington Village
- Kingsway
- Humber Bay Shores
- The Queensway
```

### Phase 3: BMAD Validation

Запустить для каждой страницы:

```bash
# Tier 1 - MUST PASS (100%)
python tools/bmad-v2/tests/tier1_critical.py locations/etobicoke.html

# Tier 2 - TARGET 85%+
python tools/bmad-v2/tests/tier2_seo.py locations/etobicoke.html
python tools/bmad-v2/tests/tier2_ai_search.py locations/etobicoke.html
python tools/bmad-v2/tests/tier2_cro.py locations/etobicoke.html
```

---

## 📝 УНИКАЛЬНЫЙ КОНТЕНТ - ПРИОРИТЕТЫ

### 🔴 CRITICAL (Обязательно уникально):

1. **Meta Title** (50-60 chars):
   ```
   [City] Appliance Repair | Same-Day Fix | Nika
   Etobicoke Appliance Repair | Same-Day Service
   ```

2. **Meta Description** (150-160 chars):
   ```
   Fast appliance repair in [City]. [Neighborhoods]. Same-day service.
   Licensed technicians. 90-day warranty. Call 437-524-1053.
   ```

3. **H1 Tag**:
   ```
   [City] Appliance Repair - Same-Day Service
   Professional Appliance Repair in [City]
   ```

4. **Hero Paragraph** (150-200 words):
   - Mention city name 3-4 times
   - Include 2-3 main neighborhoods
   - Emphasize same-day service
   - Include phone number
   - Mention "licensed and insured"

5. **Common Problems** (3-5 bullets):
   - Research local issues (well water, basement flooding, older homes, condo restrictions)
   - Make it specific to area demographics
   - Example: Scarborough = many high-rise condos → elevator issues, building restrictions

6. **FAQ Section** (5-7 Q&A):
   - First question ALWAYS: "Do you service [neighborhood 1], [neighborhood 2], and [neighborhood 3]?"
   - "How quickly can you get to [City]?"
   - "Do you repair appliances in [specific area type, e.g., condos, townhomes]?"
   - Local-specific questions

### 🟠 HIGH Priority (Желательно уникально):

7. **Neighborhoods List** (5-8 районов):
   - Research actual neighborhoods
   - List in bullet points
   - Include nearby cities

8. **Service Areas Mention** (в тексте):
   - "Serving [City] and surrounding areas including [3 nearby cities]"

9. **Schema.org areaServed**:
   - Add city + 3-5 nearby areas

### 🟢 MEDIUM Priority (Можно стандартное):

10. **Services List** - одинаковое для всех
11. **Why Choose Nika** - одинаковое
12. **Booking Form** - одинаковое (Workiz iframe)
13. **Trust Badges** - одинаковое
14. **Testimonials** - можно 1-2 локальных добавить

---

## 🎨 WORKFLOW EXECUTION PLAN

### Step 1: Подготовка данных (30 мин)

Создать CSV файл с данными для всех 20 локаций:

```csv
city,slug,lat,lon,neighborhoods,search_keywords,common_problems
Etobicoke,etobicoke,43.6205,-79.5132,"Long Branch,Islington,Kingsway","etobicoke appliance repair,appliance repair etobicoke","Hard water buildup,Basement drainage,Lake humidity"
...
```

### Step 2: Массовое создание (PowerShell - 10 мин)

```powershell
# Запустить скрипт создания
.\scripts\create-20-location-pages.ps1

# Результат: 20 HTML файлов в /locations/
```

### Step 3: AI Content Generation (Агенты - 2 часа)

Запустить параллельно агентов для генерации уникального контента:

```bash
# Parallel execution
claude-agent run location-content-generator etobicoke
claude-agent run location-content-generator north-york
claude-agent run location-content-generator scarborough
# ... all 20 в параллель
```

**Что делает агент:**
1. Читает CSV с данными локации
2. Генерирует hero paragraph (150-200 слов)
3. Генерирует 3-5 common problems на базе local research
4. Генерирует 5-7 FAQ вопросов
5. Генерирует neighborhoods section
6. Обновляет все schema.org данные
7. Проверяет keyword density (город упоминается 15-40 раз)

### Step 4: BMAD Validation (Автомат - 30 мин)

```bash
# Batch testing
for file in locations/*.html; do
    python tools/bmad-v2/tests/tier1_critical.py "$file"
    python tools/bmad-v2/tests/tier2_seo.py "$file"
done
```

### Step 5: Manual Review (1 час)

Проверить вручную для CRITICAL pages (Etobicoke, North York, Scarborough):
- Hero text читается естественно?
- Common problems релевантные?
- FAQ отвечают на реальные вопросы?
- Нет keyword stuffing?

### Step 6: Internal Linking (15 мин)

Добавить cross-links между location pages:

```html
<!-- В footer или sidebar -->
<div class="nearby-locations">
    <h3>Nearby Service Areas</h3>
    <ul>
        <li><a href="/locations/etobicoke">Etobicoke</a></li>
        <li><a href="/locations/north-york">North York</a></li>
        <li><a href="/locations/scarborough">Scarborough</a></li>
    </ul>
</div>
```

---

## 📊 BMAD REQUIREMENTS (Tier 1-2)

### Tier 1: Critical Foundation (100% REQUIRED)

✅ **Data Consistency:**
1. Phone: 437-524-1053 (везде одинаково)
2. Warranty: 90-day (везде одинаково)
3. Rating: 4.9/5 (везде одинаково)
4. Business hours: Mon-Fri 8-20, Sat 9-18, Sun 10-17
5. Address: (head office - одинаковый)
6. Email: care@niappliancerepair.ca

✅ **Technical:**
7. LocalBusiness schema ✅
8. AggregateRating schema ✅
9. Mobile viewport meta ✅
10. Single H1 tag ✅
11. Valid HTML ✅
12. HTTPS only ✅
13. Phone in header ✅

### Tier 2: SEO + AI + CRO (85%+ TARGET)

✅ **SEO Core:**
14. Word count: 1500-2500 ✅
15. Title tag: 50-60 chars ✅ (уникально!)
16. Meta description: 150-160 chars ✅ (уникально!)
17. H1: уникально ✅
18. H2-H6 structure ✅
19. Internal links: 10+ ✅
20. Images: 10+ ✅
21. Alt text: 100% ✅
22. FAQPage schema ✅
23. Canonical tag ✅
24. Open Graph tags ✅

✅ **AI Search (98% REQUIRED):**
25. Speakable schema ✅
26. HowTo schema ✅
27. FAQ schema ✅
28. WebPage schema ✅
29. Schema diversity: 4+ types ✅

✅ **CRO:**
30. CTA count: 5-8 ✅
31. Form above fold ✅
32. Phone prominence ✅
33. Trust badges: 3+ ✅
34. Social proof ✅
35. Testimonials: 3+ ✅
36. Urgency triggers ✅

---

## 🚀 EXECUTION TIMELINE

| Day | Task | Time | Output |
|-----|------|------|--------|
| **Day 1** | Подготовка CSV данных | 1h | locations-data.csv |
| | PowerShell: создание 20 files | 15m | 20 HTML files |
| | AI Agents: content gen (parallel) | 3h | Уникальный контент |
| **Day 2** | BMAD Tier 1 validation | 30m | 100% pass rate |
| | BMAD Tier 2 validation | 1h | 85%+ pass rate |
| | Manual review (top 3) | 1h | Quality check |
| | Internal linking | 30m | Cross-links added |
| **Day 3** | Final QA | 1h | Ready for deploy |
| | Deploy to site | 30m | Live! |
| **Total** | | **~8 hours** | **20 new location pages** |

---

## 💰 EXPECTED RESULTS

### SEO Impact:
- **+20 location pages** = 20x увеличение local footprint
- Each page targets "[city] appliance repair" (high intent keyword)
- Internal linking boost для main site
- Google My Business signals (areaServed expansion)

### Traffic Projection:
- Each page: 50-200 visits/month (low competition keywords)
- Total: **1,000-4,000 visits/month** from new pages
- Conversion rate: 3-5% (same-day service, local)
- Expected leads: **30-200/month** additional

### Timeline to Results:
- Week 1-2: Google indexing
- Month 1: Появление в results
- Month 2-3: Ranking improvements
- Month 4+: Stable traffic flow

---

## 📋 NEXT STEPS

1. ✅ Approve этот план
2. 🔨 Создать PowerShell script для массового создания
3. 🤖 Настроить AI агенты для content generation
4. 📊 Подготовить CSV с данными локаций
5. 🚀 Запустить execution (Day 1-3)

**Готов начать?** Скажи "go" и я создам все необходимые скрипты и начну генерацию!
