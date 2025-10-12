# 🚀 План оптимизации производительности Homepage

## 📊 Текущие проблемы (PageSpeed Insights - Mobile)

### 🔴 КРИТИЧЕСКИЕ (влияют на LCP/FCP):
1. **Render-blocking CSS** - экономия 750ms
   - 9 CSS файлов блокируют первый рендер
   - Общий размер: 30.0 KiB, время загрузки: 3,870ms

2. **YouTube iframes** - экономия 4.4 KiB JS
   - 6.8 KiB неиспользуемого JavaScript
   - Блокировка main-thread на 4.7s
   - 6 iframe embeds загружаются сразу

3. **JavaScript execution time** - 6.8s
   - YouTube scripts: 7.6s CPU time
   - Собственные скрипты: 928ms

4. **Main-thread work** - 9.1s
   - Script Evaluation: 3.9s
   - Script Parsing: 2.9s
   - Style & Layout: 602ms

### 🟡 ВАЖНЫЕ (мобильная версия):
5. **Mobile overflow** - секции вылезают справа
6. **Mobile centering** - контент не центрирован

---

## ✅ ПЛАН ИСПРАВЛЕНИЯ (БЕЗ ПОЛОМКИ ДИЗАЙНА)

### Этап 1: Оптимизация CSS (⏱️ 15 мин)
**Цель**: Устранить render-blocking CSS без изменения дизайна

**Действия**:
```html
<!-- БЫЛО: Все CSS в <head> блокируют рендер -->
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/video-custom.css">
... (9 файлов)

<!-- СТАНЕТ: Critical CSS inline + async остальные -->
<style>/* Critical CSS inline - только для above-the-fold */</style>
<link rel="preload" href="css/style.css" as="style">
<link rel="stylesheet" href="css/style.css" media="print" onload="this.media='all'">
```

**Безопасность**:
- ✅ Дизайн не изменится (все стили остаются)
- ✅ Только меняется порядок загрузки
- ✅ Above-the-fold контент рендерится мгновенно

**Результат**: -750ms LCP

---

### Этап 2: YouTube Facade (⏱️ 20 мин)
**Цель**: Отложить загрузку YouTube до клика пользователя

**Действия**:
```html
<!-- БЫЛО: iframe загружается сразу -->
<iframe src="https://www.youtube.com/embed/..."></iframe>

<!-- СТАНЕТ: Легкая картинка-заглушка -->
<div class="youtube-facade" data-video-id="Nk1ab2OskJ4">
  <img src="https://i.ytimg.com/vi/Nk1ab2OskJ4/hqdefault.jpg" alt="Video">
  <button class="play-btn">▶</button>
</div>
```

**Безопасность**:
- ✅ Визуально выглядит идентично
- ✅ Видео загружается только при клике
- ✅ Работает на всех устройствах

**Результат**: -4.4 KiB JS, -4.7s main-thread, -6.8s execution time

---

### Этап 3: JavaScript оптимизация (⏱️ 10 мин)
**Цель**: Отложить неважные скрипты

**Действия**:
```html
<!-- БЫЛО: Все скрипты в <body> -->
<script src="js/main.js"></script>
<script src="js/countdown-timer.js"></script>

<!-- СТАНЕТ: Defer для несрочных -->
<script src="js/main.js" defer></script>
<script src="js/countdown-timer.js" defer></script>
```

**Безопасность**:
- ✅ Функционал не изменится
- ✅ Скрипты выполнятся после парсинга HTML
- ✅ Не блокируют рендер

**Результат**: -1-2s main-thread work

---

### Этап 4: Mobile Overflow Fix (⏱️ 10 мин)
**Цель**: Исправить горизонтальный скролл на мобильных

**Проблема**: Скорее всего `overflow-x` или элементы с `width > 100vw`

**Действия**:
```css
/* Добавить в css/mobile-strict-fix.css */
html, body {
  overflow-x: hidden;
  max-width: 100vw;
}

.container,
.section {
  max-width: 100%;
  overflow-x: hidden;
}

/* Проверить все элементы с фиксированной шириной */
@media (max-width: 768px) {
  * {
    max-width: 100vw !important;
  }
}
```

**Безопасность**:
- ✅ Только мобильная версия
- ✅ Десктоп не затронут
- ✅ Контент остается читаемым

**Результат**: Нет горизонтального скролла

---

### Этап 5: Mobile Centering (⏱️ 5 мин)
**Цель**: Центрировать контент на мобильных

**Действия**:
```css
@media (max-width: 768px) {
  .section,
  .container {
    margin-left: auto;
    margin-right: auto;
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .about-section,
  .testimonials-modern,
  .video-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
```

**Безопасность**:
- ✅ Только мобильная версия
- ✅ Симметричные отступы
- ✅ Контент по центру экрана

**Результат**: Все секции центрированы и responsive

---

## 📝 ПОРЯДОК ВЫПОЛНЕНИЯ

### Шаг 1: Mobile Fixes (СНАЧАЛА - самое безопасное)
1. ✅ Исправить overflow
2. ✅ Центрировать секции
3. ✅ Тестировать на мобильном

### Шаг 2: JavaScript оптимизация (безопасно)
1. ✅ Добавить defer к скриптам
2. ✅ Тестировать функционал

### Шаг 3: YouTube Facade (средний риск)
1. ✅ Создать facade компонент
2. ✅ Заменить 6 iframes на facade
3. ✅ Тестировать воспроизведение видео

### Шаг 4: CSS оптимизация (ПОСЛЕДНЕЕ - нужна аккуратность)
1. ✅ Извлечь critical CSS
2. ✅ Добавить preload + async
3. ✅ Тестировать рендеринг

---

## 🎯 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ

### Performance Metrics:
- **LCP**: -750ms (CSS) + -2s (YouTube) = **-2.75s improvement**
- **TBT**: -4.7s (YouTube) + -2s (JS defer) = **-6.7s improvement**
- **FCP**: -750ms (CSS) = **-0.75s improvement**

### PageSpeed Score:
- **Текущий**: ~40-50 (mobile)
- **Ожидаемый**: ~75-85 (mobile) ✅

### User Experience:
- ✅ Страница загружается мгновенно
- ✅ Видео не тормозят загрузку
- ✅ Мобильная версия идеальна
- ✅ Дизайн не изменен

---

## ⚠️ РИСКИ И МЕРЫ БЕЗОПАСНОСТИ

### Низкий риск:
- ✅ Mobile overflow/centering - чистый CSS
- ✅ JavaScript defer - стандартная практика

### Средний риск:
- ⚠️ YouTube facade - нужно тестировать клик
- ✅ Митигация: Оставить 1 iframe для теста

### Высокий риск:
- ⚠️ CSS async - может вызвать FOUC (Flash of Unstyled Content)
- ✅ Митигация: Critical CSS inline предотвратит FOUC

---

## 🧪 ТЕСТИРОВАНИЕ

### Обязательные проверки:
1. ✅ Десктоп - визуальный чек всех секций
2. ✅ Мобильный - нет overflow, все центрировано
3. ✅ Видео - воспроизведение работает
4. ✅ Формы - работают корректно
5. ✅ Таймер - отсчитывает правильно
6. ✅ FAQ - accordion работает

### Критерии успеха:
- ✅ PageSpeed Mobile > 75
- ✅ Нет визуальных изменений дизайна
- ✅ Все функции работают
- ✅ Мобильная версия responsive

---

## 🚀 НАЧАТЬ С:

**Приоритет 1**: Mobile fixes (overflow + centering) - 15 минут, 0 рисков
**Приоритет 2**: JavaScript defer - 10 минут, низкий риск
**Приоритет 3**: YouTube facade - 20 минут, средний риск
**Приоритет 4**: CSS optimization - 15 минут, требует тестирования

**ОБЩЕЕ ВРЕМЯ**: ~1 час
**РИСК ПОЛОМКИ**: Минимальный при пошаговом подходе
