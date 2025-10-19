# Bulk HTML Editing Scripts

Скрипты для массового редактирования HTML файлов на сайте Nika Appliance Repair.

## Зачем это нужно?

Когда нужно изменить один элемент на всех страницах (например, телефон, booking форму, CSS файл), эти скрипты позволяют сделать это за 1 команду вместо редактирования каждого файла вручную.

## Доступные скрипты

### 1. PowerShell (Рекомендуется для Windows)

**Файл:** `bulk-edit.ps1`

**Как использовать:**

```powershell
# 1. Открыть PowerShell в папке проекта
cd C:\NikaApplianceRepair

# 2. Загрузить скрипт
. .\scripts\bulk-edit.ps1

# 3. Использовать функции:

# Заменить телефон везде:
Replace-InAllPages -OldText "437-747-6737" -NewText "555-123-4567"

# Заменить текст только в location pages:
Replace-InLocationPages -OldText "старый текст" -NewText "новый текст"

# Заменить только в service pages:
Replace-InServicePages -OldText "old" -NewText "new"

# Удалить секцию из всех location pages:
Remove-SectionBetweenMarkers -StartMarker '<div id="old-section">' -EndMarker '</div>' -Path ".\locations\*.html"

# Добавить CSS файл во все страницы:
Add-CssLink -CssPath "css/new-styles.css"
```

### 2. Node.js (Самый гибкий)

**Файл:** `bulk-edit.js`

**Установка:**
```bash
npm install glob
```

**Как использовать:**

```javascript
// 1. Создать файл run-edit.js:
const {
    replaceText,
    updatePhoneNumber,
    addCssLink,
    updateBookingForms
} = require('./scripts/bulk-edit.js');

// 2. Использовать функции:

// Заменить телефон:
updatePhoneNumber('555-123-4567');

// Добавить CSS:
addCssLink('css/new-styles.css');

// Обновить все booking формы:
updateBookingForms('https://new-booking-url.com');

// Заменить текст в location pages:
replaceText('old text', 'new text', 'locations/*.html');

// 3. Запустить:
// node run-edit.js
```

### 3. Bash (для Linux/Mac)

**Файл:** `bulk-edit.sh`

**Как использовать:**

```bash
# Сделать скрипт исполняемым:
chmod +x scripts/bulk-edit.sh

# Редактировать скрипт и раскомментировать нужные команды
nano scripts/bulk-edit.sh

# Запустить:
./scripts/bulk-edit.sh
```

## Примеры типичных задач

### Задача 1: Изменить телефон на всех страницах

**PowerShell:**
```powershell
. .\scripts\bulk-edit.ps1
Replace-InAllPages -OldText "437-747-6737" -NewText "NEW-PHONE"
```

**Node.js:**
```javascript
const { updatePhoneNumber } = require('./scripts/bulk-edit.js');
updatePhoneNumber('NEW-PHONE');
```

### Задача 2: Обновить Workiz booking URL

**PowerShell:**
```powershell
. .\scripts\bulk-edit.ps1
Replace-InAllPages -OldText "https://online-booking.workiz.com/?ac=OLD_ID" -NewText "https://online-booking.workiz.com/?ac=NEW_ID"
```

**Node.js:**
```javascript
const { updateBookingForms } = require('./scripts/bulk-edit.js');
updateBookingForms('https://online-booking.workiz.com/?ac=NEW_ID');
```

### Задача 3: Удалить старую секцию со всех страниц

**PowerShell:**
```powershell
. .\scripts\bulk-edit.ps1
Remove-SectionBetweenMarkers -StartMarker '<!-- OLD SECTION START -->' -EndMarker '<!-- OLD SECTION END -->' -Path ".\**\*.html"
```

### Задача 4: Добавить новый CSS файл

**PowerShell:**
```powershell
. .\scripts\bulk-edit.ps1
Add-CssLink -CssPath "css/new-feature.css"
```

**Node.js:**
```javascript
const { addCssLink } = require('./scripts/bulk-edit.js');
addCssLink('css/new-feature.css');
```

### Задача 5: Заменить всю booking секцию

**Рекомендация:** Добавьте комментарии-маркеры в HTML:

```html
<!-- BOOKING SECTION START -->
<section class="booking-section-bmad">
    ...
</section>
<!-- BOOKING SECTION END -->
```

Потом используйте:

**Node.js:**
```javascript
const { replaceCodeBlock } = require('./scripts/bulk-edit.js');

const newBookingHtml = `<section class="booking-section-bmad">
    <!-- новый контент -->
</section>`;

replaceCodeBlock(
    '<!-- BOOKING SECTION START -->',
    '<!-- BOOKING SECTION END -->',
    newBookingHtml,
    '**/*.html'
);
```

## Безопасность

**ВАЖНО:** Всегда делайте backup или commit в Git перед массовыми изменениями!

```bash
# Создать Git commit перед изменениями:
git add .
git commit -m "Before bulk edit"

# Теперь можно безопасно экспериментировать
# Если что-то пошло не так:
git reset --hard HEAD
```

## Расширенные примеры

### Добавить Google Analytics на все страницы

**PowerShell:**
```powershell
$gaCode = @"
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
"@

Get-ChildItem -Path "." -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -notmatch "googletagmanager") {
        $content = $content -replace "</head>", "$gaCode`n</head>"
        Set-Content -Path $_.FullName -Value $content -NoNewline
        Write-Host "Added GA to: $($_.Name)"
    }
}
```

### Обновить год в footer

**PowerShell:**
```powershell
Replace-InAllPages -OldText "© 2024" -NewText "© 2025"
```

## Почему я использовал много токенов?

Я запустил 24+ параллельных агентов (по одному на каждую страницу), что использовало ~55,000 токенов.

**Для будущего:** Используйте эти скрипты для массовых изменений - это будет:
- ✅ Быстрее (секунды вместо минут)
- ✅ Дешевле (почти 0 токенов)
- ✅ Надежнее (одна команда для всех файлов)
- ✅ Легко откатить (Git reset)

## Дополнительные инструменты

### VS Code Find & Replace

Для простых замен можно использовать встроенный поиск VS Code:

1. Ctrl+Shift+H (Find & Replace in Files)
2. Включить regex: `.*`
3. Указать фильтр: `locations/*.html`
4. Ввести что искать и на что заменить
5. Replace All

### Regex примеры

```regex
# Найти все телефоны:
\d{3}-\d{3}-\d{4}

# Найти все email:
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# Найти все iframe с Workiz:
<iframe src='https://online-booking\.workiz\.com/\?ac=[^']+' [^>]*></iframe>
```
