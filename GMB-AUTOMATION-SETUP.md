# GMB Auto-Posting Setup Guide

Автоматизация постинга в Google Business Profile из блога.

---

## Архитектура

```
Blog Post Published
        ↓
  GitHub Actions
        ↓
  ┌─────────────────┐
  │ 1. Publish post │
  │ 2. Update RSS   │
  │ 3. Update site  │
  └─────────────────┘
        ↓
    RSS Feed (feed.xml)
        ↓
  ┌─────────────────────┐
  │ Automation Service  │
  │ (n8n / Zapier /     │
  │  Make / IFTTT)      │
  └─────────────────────┘
        ↓
  Google Business Profile Post
```

---

## Вариант 1: n8n (Бесплатно, Self-Hosted)

### Шаг 1: Установить n8n

```bash
# Docker (рекомендуется)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# или npm
npm install n8n -g
n8n start
```

### Шаг 2: Импортировать workflow

1. Открыть n8n: http://localhost:5678
2. Create New Workflow
3. Import from File → `scripts/n8n-gmb-workflow.json`

### Шаг 3: Настроить Google OAuth2

1. Google Cloud Console → Create Project
2. Enable "Google My Business API"
3. Create OAuth2 Credentials
4. В n8n: Credentials → Add → Google OAuth2
5. Указать Client ID и Secret

### Шаг 4: Получить GMB IDs

```bash
# После авторизации, получить account ID:
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"

# Получить location ID:
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://mybusinessbusinessinformation.googleapis.com/v1/accounts/ACCOUNT_ID/locations"
```

---

## Вариант 2: Zapier ($20-50/мес)

### Шаг 1: Создать Zap

1. Trigger: **RSS by Zapier** → New Item in Feed
2. Feed URL: `https://nikaappliancerepair.com/feed.xml`

### Шаг 2: Action

1. Action: **Google My Business** → Create Post
2. Авторизовать GMB аккаунт
3. Настроить пост:
   - **Summary**: `🔧 NEW: {{title}} - Read more!`
   - **Call to Action**: Learn More → `{{link}}`

---

## Вариант 3: Make.com (Integromat) ($9-16/мес)

### Сценарий

1. **RSS Module** → Watch RSS Feed Items
2. **Google My Business** → Create a Post
3. Настроить mapping полей

---

## Вариант 4: IFTTT (Бесплатно, ограничено)

IFTTT НЕ поддерживает GMB напрямую, но можно использовать:

1. RSS → Email (получать уведомление о новом посте)
2. Вручную копировать в GMB

---

## Вариант 5: Ручной постинг с помощью скрипта

Скрипт генерирует готовый текст для копирования:

```bash
cd scripts
python gmb-auto-post.py --manual --count 1
```

Вывод:
```
🔧 NEW: How to Fix Refrigerator Not Cooling

Read our latest appliance repair guide with expert tips for Toronto homeowners!

📖 Full article: https://nikaappliancerepair.com/blog/troubleshooting/refrigerator-not-cooling

#ApplianceRepair #Toronto #HomeMaintenance
```

Копируете в GMB → Create Post → Done!

---

## Рекомендуемый вариант

Для вашего случая рекомендую **n8n** потому что:

1. ✅ Бесплатно (self-hosted)
2. ✅ Полный контроль
3. ✅ Можно хостить на том же VPS
4. ✅ Поддержка GMB API
5. ✅ Визуальный редактор workflows

---

## Тестирование

### Проверить RSS feed:

```bash
python scripts/generate-rss-feed.py
```

Файл `feed.xml` появится в корне сайта.

### Проверить GMB пост:

```bash
python scripts/gmb-auto-post.py --dry-run
```

---

## Расписание постинга

| День | Время | Тип поста |
|------|-------|-----------|
| Пн | 9:00 | Новый блог-пост |
| Ср | 14:00 | Совет недели |
| Пт | 11:00 | Оффер/Акция |

---

## Формат GMB постов

### Для блог-постов:
```
🔧 NEW: [Заголовок статьи]

[2-3 предложения из description]

📖 Читать: [URL]

#ApplianceRepair #Toronto #[ApplicanceType]
```

### Для советов:
```
💡 TIP: [Быстрый совет]

[Развернутое объяснение]

📞 Нужна помощь? 437-747-6737

#ApplianceTips #TorontoHomes
```

### Для акций:
```
🎉 SPECIAL OFFER: [Название акции]

[Детали предложения]
⏰ Valid until: [Дата]

📞 Book now: 437-747-6737
🌐 nikaappliancerepair.com/book

#ApplianceRepairDeal #Toronto
```

---

## Мониторинг

После настройки проверяйте:

1. **Weekly**: GMB Insights → Post views
2. **Monthly**: Какие посты получают больше кликов
3. **Adjust**: Оптимизировать формат и время

---

*Setup guide created: December 7, 2025*
