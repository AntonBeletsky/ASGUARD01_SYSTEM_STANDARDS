# 🔬 DESIGN CHECK PROTOCOL GUIDE
### Полный системный протокол выявления и устранения дизайн-багов в HTML/CSS/JS проектах

> **Назначение:** Данный гайд — пошаговый протокол для ИИ-ассистента. На входе — исходный код (HTML/CSS/JS). На выходе — полный отчёт о всех дизайн-багах с конкретными путями решения.

---

## 📋 ОГЛАВЛЕНИЕ

1. [Методология анализа](#1-методология)
2. [Блок A — Разметка и структура HTML](#2-блок-a--разметка-и-структура-html)
3. [Блок B — Типографика](#3-блок-b--типографика)
4. [Блок C — Spacing: отступы и поля](#4-блок-c--spacing-отступы-и-поля)
5. [Блок D — Выравнивание и симметрия](#5-блок-d--выравнивание-и-симметрия)
6. [Блок E — Цвет и контраст](#6-блок-e--цвет-и-контраст)
7. [Блок F — Размеры и пропорции элементов](#7-блок-f--размеры-и-пропорции-элементов)
8. [Блок G — Flexbox и Grid баги](#8-блок-g--flexbox-и-grid-баги)
9. [Блок H — Адаптивность (Responsive)](#9-блок-h--адаптивность-responsive)
10. [Блок I — Переполнение и обрезка контента (Overflow)](#10-блок-i--переполнение-и-обрезка-контента-overflow)
11. [Блок J — Z-index и слои](#11-блок-j--z-index-и-слои)
12. [Блок K — Изображения и медиа](#12-блок-k--изображения-и-медиа)
13. [Блок L — Анимации и переходы](#13-блок-l--анимации-и-переходы)
14. [Блок M — Формы и интерактивные элементы](#14-блок-m--формы-и-интерактивные-элементы)
15. [Блок N — Визуальная иерархия](#15-блок-n--визуальная-иерархия)
16. [Блок O — Консистентность системы](#16-блок-o--консистентность-системы)
17. [Блок P — JavaScript-влияние на UI](#17-блок-p--javascript-влияние-на-ui)
18. [Шаблон финального отчёта](#18-шаблон-финального-отчёта)
19. [Быстрый чеклист (Quick Scan)](#19-быстрый-чеклист-quick-scan)

---

## 1. МЕТОДОЛОГИЯ

### Как ИИ должен работать с кодом

**Шаг 1 — Первичный скан**
Перед детальным анализом — беглый просмотр кода для понимания:
- Тип проекта (лендинг / дашборд / форма / портфолио / e-commerce)
- CSS-методология (BEM, Tailwind, CSS Modules, plain CSS)
- Используемые фреймворки (Bootstrap, CSS Grid, Flexbox, кастом)
- Объём и сложность

**Шаг 2 — Блочный анализ**
Пройти каждый блок протокола (A→P) и зафиксировать все найденные проблемы.

**Шаг 3 — Классификация багов**

| Severity | Обозначение | Описание |
|----------|------------|---------|
| Критический | 🔴 CRITICAL | Ломает layout, контент недоступен или нечитаем |
| Высокий | 🟠 HIGH | Заметные визуальные проблемы, нарушают восприятие |
| Средний | 🟡 MEDIUM | Несимметричность, непоследовательность, неточности |
| Низкий | 🟢 LOW | Небольшие отклонения, polish-правки |

**Шаг 4 — Формирование решений**
Для каждого бага — конкретный CSS/HTML/JS-фикс, не абстрактный совет.

**Шаг 5 — Итоговый отчёт**
Структурированный вывод по шаблону из раздела 18.

---

## 2. БЛОК A — РАЗМЕТКА И СТРУКТУРА HTML

### A1. Семантическая вложенность

**Что проверять:**
```
❌ <div> внутри <p>
❌ <h3> без предшествующего <h2>
❌ <button> внутри <a> или наоборот
❌ <ul> с дочерними элементами не <li>
❌ <table> для layout (не для данных)
```

**Диагностика:** Поиск по коду вложенностей, нарушающих модель блочных/инлайн элементов.

**Решение:**
```html
<!-- ❌ Баг: блочный элемент внутри инлайн -->
<span><div>Текст</div></span>

<!-- ✅ Фикс -->
<div><span>Текст</span></div>
```

---

### A2. Дублирование ID

**Что проверять:** Наличие одинаковых `id` на нескольких элементах.

**Диагностика:** Извлечь все `id="..."` из HTML, проверить уникальность.

**Решение:**
```html
<!-- ❌ Баг -->
<div id="header">...</div>
<div id="header">...</div>

<!-- ✅ Фикс — использовать class для повторяющихся паттернов -->
<div class="header-block">...</div>
<div class="header-block">...</div>
```

---

### A3. Пустые/избыточные контейнеры

**Что проверять:** `<div>` без контента и без функциональной цели, многоуровневая вложенность без смысла (div soup).

**Решение:** Удалить или заменить семантическим тегом.

---

## 3. БЛОК B — ТИПОГРАФИКА

### B1. Нечитаемые размеры шрифта

**Что проверять:**
```css
/* 🔴 Критично: размер меньше 12px для основного контента */
font-size: 10px;

/* 🟠 Высокий: размер меньше 14px для body text */
font-size: 12px;
```

**Диагностика:** Найти все `font-size` значения. Построить таблицу scale.

**Фикс — минимальные требования:**
```css
body          { font-size: 16px; }      /* минимум */
caption, hint { font-size: 12px; }      /* абсолютный минимум */
h1            { font-size: clamp(28px, 5vw, 56px); }
h2            { font-size: clamp(22px, 4vw, 40px); }
```

---

### B2. Неконсистентный type scale

**Что проверять:** Произвольные размеры без системы (12, 13, 15, 17, 23px вместо scale).

**Решение — внедрить Modular Scale:**
```css
:root {
  --text-xs:   0.75rem;   /* 12px */
  --text-sm:   0.875rem;  /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg:   1.25rem;   /* 20px */
  --text-xl:   1.5rem;    /* 24px */
  --text-2xl:  2rem;      /* 32px */
  --text-3xl:  2.5rem;    /* 40px */
  --text-4xl:  3rem;      /* 48px */
}
```

---

### B3. Проблемы line-height

**Что проверять:**
```css
/* 🔴 Критично: line-height меньше 1 или больше 2 */
line-height: 0.8;
line-height: 3;

/* 🟠 Высокий: для body text — не в диапазоне 1.4–1.7 */
line-height: 1.1;
```

**Фикс:**
```css
body           { line-height: 1.6; }
h1, h2, h3    { line-height: 1.2; }
.caption       { line-height: 1.4; }
```

---

### B4. Слишком длинные строки

**Что проверять:** Ширина текстового блока > 75 символов (примерно > 700px без ограничений).

**Фикс:**
```css
.prose, article, .text-block {
  max-width: 65ch;   /* ch = ширина символа "0" */
}
```

---

### B5. Orphans и widows (одиноко висящие слова)

**Что проверять:** Последняя строка параграфа — одно слово.

**Фикс:**
```css
p {
  orphans: 3;
  widows: 3;
  /* или для заголовков: */
  text-wrap: balance; /* современный CSS */
}
```

---

### B6. Смешение шрифтовых семейств без системы

**Что проверять:** Более 2-3 разных font-family без дизайн-логики.

**Диагностика:** Извлечь все `font-family` значения из CSS.

---

## 4. БЛОК C — SPACING: ОТСТУПЫ И ПОЛЯ

### C1. Магические числа в отступах

**Что проверять:** Отступы типа `margin: 13px`, `padding: 7px`, `gap: 11px` — произвольные значения без системы.

**Решение — Space Scale (8px grid):**
```css
:root {
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  24px;
  --space-6:  32px;
  --space-7:  48px;
  --space-8:  64px;
  --space-9:  96px;
  --space-10: 128px;
}
```

---

### C2. Несимметричные внутренние отступы в схожих элементах

**Что проверять:**
```css
/* 🟡 Баг: одна кнопка */
.btn-primary { padding: 12px 24px; }
/* другая кнопка — разные значения */
.btn-secondary { padding: 10px 20px; }
```

**Диагностика:** Сравнить padding/margin у однотипных компонентов (кнопки, карточки, инпуты).

**Фикс:** Унифицировать через переменные или общий класс.

---

### C3. Отсутствие отступов между секциями

**Что проверять:** Секции страницы "слипаются" — нет вертикального ритма.

**Фикс:**
```css
section + section { margin-top: var(--space-9); }
/* или через gap в flex/grid родителе */
```

---

### C4. Padding vs Margin путаница

**Что проверять:** `margin` используется для внутреннего отступа от края блока, `padding` — для внешнего расстояния между блоками (характерная ошибка).

**Правило:**
- `padding` — внутри элемента (фон/граница включают padding)
- `margin` — снаружи элемента (расстояние между элементами)

---

### C5. Коллапс margin (margin collapse)

**Что проверять:** Вертикальные margin между блочными элементами коллапсируют — ожидаемый суммарный отступ не соблюдается.

**Диагностика:** Если `margin-bottom: 32px` + `margin-top: 32px` дают итого `32px` (не `64px`) — это коллапс.

**Фикс:**
```css
/* Вариант 1: Использовать padding вместо margin */
/* Вариант 2: Добавить border или padding родителю */
/* Вариант 3: Использовать flexbox (не коллапсирует) */
.container { display: flex; flex-direction: column; gap: var(--space-6); }
```

---

## 5. БЛОК D — ВЫРАВНИВАНИЕ И СИММЕТРИЯ

### D1. Смешанное выравнивание контента

**Что проверять:** В одном блоке часть контента `text-align: left`, часть — `center`, без логики.

**Диагностика:** Извлечь все `text-align`, `align-items`, `justify-content` — сравнить со структурой страницы.

---

### D2. Визуальное несоответствие краёв (edge misalignment)

**Что проверять:** Разные элементы в одной колонке имеют разные левые/правые края.

**Решение — единая сетка:**
```css
.page-wrapper {
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: clamp(16px, 5vw, 80px);
}
/* ВСЕ секции используют .page-wrapper */
```

---

### D3. Несимметричные карточки / grid-элементы

**Что проверять:**
```css
/* 🟠 Баг: карточки разной высоты в одном ряду */
.card { height: auto; } /* при разном контенте — разная высота */
```

**Фикс:**
```css
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  align-items: stretch; /* все карточки одной высоты */
}
.card {
  display: flex;
  flex-direction: column;
}
.card__body { flex: 1; } /* растягивает тело карточки */
```

---

### D4. Иконки не выровнены с текстом по вертикали

**Что проверять:**
```css
/* 🟡 Баг: иконка сдвинута относительно baseline */
.icon { display: inline; }
```

**Фикс:**
```css
.icon-text {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.icon-text svg {
  width: 1em;
  height: 1em;
  flex-shrink: 0;
}
```

---

### D5. Непоследовательное выравнивание label и input

**Что проверять:** В форме label расположен по-разному — где-то сверху, где-то слева, где-то inline.

**Фикс:** Определить одну систему и применить ко всем полям.

---

## 6. БЛОК E — ЦВЕТ И КОНТРАСТ

### E1. Недостаточный контраст текста (WCAG)

**Что проверять:**

| Тип текста | Минимум (AA) | Идеал (AAA) |
|-----------|-------------|-------------|
| Основной (≥18px или bold ≥14px) | 3:1 | 4.5:1 |
| Мелкий текст | 4.5:1 | 7:1 |
| UI-компоненты, иконки | 3:1 | — |

**Диагностика:** Извлечь пары `color` + `background-color`, рассчитать ratio по формуле WCAG.

**Формула яркости:**
```
L = 0.2126R + 0.7152G + 0.0722B
Contrast = (L1 + 0.05) / (L2 + 0.05)
```

**Типичные проблемные пары:**
```css
/* 🔴 Критично: серый на белом */
color: #aaaaaa; background: #ffffff; /* ratio ~2.3:1 — недостаточно */

/* 🔴 Критично: жёлтый текст на белом */
color: #ffcc00; background: #ffffff;
```

---

### E2. Отсутствие Dark Mode поддержки (если задумывался)

**Что проверять:** Жёстко заданные `color: #000` и `background: #fff` без `@media (prefers-color-scheme: dark)`.

**Фикс:**
```css
:root {
  --color-bg: #ffffff;
  --color-text: #1a1a1a;
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #121212;
    --color-text: #e5e5e5;
  }
}
```

---

### E3. Неконсистентная цветовая палитра

**Что проверять:** Оттенки одного цвета с незначительными различиями (`#3498db`, `#3399dd`, `#3492db` в одном проекте).

**Диагностика:** Извлечь все hex/rgb значения из CSS, сгруппировать похожие.

**Решение — CSS Custom Properties палитра:**
```css
:root {
  --color-primary-100: #e8f4fd;
  --color-primary-300: #85c1e9;
  --color-primary-500: #3498db;  /* основной */
  --color-primary-700: #1f6f9f;
  --color-primary-900: #0d3b56;
}
```

---

### E4. Использование цвета как единственного индикатора

**Что проверять:** Статус ошибки/успеха передаётся только цветом (без иконки, текста, паттерна).

**Фикс:**
```html
<!-- ❌ Только цвет -->
<div class="status-error">Ошибка</div>

<!-- ✅ Цвет + иконка + текст -->
<div class="status-error" role="alert">
  <span aria-hidden="true">✕</span> Ошибка подключения
</div>
```

---

## 7. БЛОК F — РАЗМЕРЫ И ПРОПОРЦИИ ЭЛЕМЕНТОВ

### F1. Кнопки слишком маленькие для касания

**Что проверять:** Интерактивные элементы меньше 44×44px (Apple HIG) / 48×48px (Material Design).

**Фикс:**
```css
button, a, [role="button"] {
  min-height: 44px;
  min-width: 44px;
  /* или через padding: */
  padding: 12px 24px;
}
```

---

### F2. Фиксированные размеры ломающие layout

**Что проверять:**
```css
/* 🔴 Критично: фиксированная ширина больше viewport */
.container { width: 1400px; } /* без max-width */

/* 🟠 Высокий: фиксированная высота блока с текстом */
.card { height: 200px; } /* текст будет overflow при масштабировании */
```

**Фикс:**
```css
.container {
  width: 100%;
  max-width: 1400px;
  margin-inline: auto;
}
.card {
  min-height: 200px; /* минимум, но может расти */
  height: auto;
}
```

---

### F3. Пропорции изображений нарушены

**Что проверять:**
```css
/* 🔴 Баг: изображение деформировано */
img { width: 100%; height: 300px; } /* без object-fit */
```

**Фикс:**
```css
.image-container {
  width: 100%;
  aspect-ratio: 16 / 9; /* или 4/3, 1/1 */
  overflow: hidden;
}
.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
```

---

### F4. Несоответствие размеров иконок

**Что проверять:** Иконки разных размеров (16px, 18px, 20px, 24px) используются вперемешку без логики.

**Решение — Icon Scale:**
```css
:root {
  --icon-sm: 16px;
  --icon-md: 20px;
  --icon-lg: 24px;
  --icon-xl: 32px;
}
```

---

## 8. БЛОК G — FLEXBOX И GRID БАГИ

### G1. Flex-items сжимаются/растягиваются неожиданно

**Что проверять:**
```css
/* 🟠 Баг: элементы сжимаются ниже min-content */
.flex-child { /* нет flex-shrink: 0 на элементах с фиксированным размером */ }
```

**Диагностика:** Найти все `display: flex` контейнеры. Проверить `flex` свойства дочерних.

**Фикс:**
```css
/* Иконки, аватары, логотипы — не сжимать */
.icon, .avatar, .logo { flex-shrink: 0; }

/* Текстовый контент — сжимать, но не ниже min-content */
.text-content {
  flex: 1 1 auto;
  min-width: 0; /* ВАЖНО: без этого текст не truncate */
}
```

---

### G2. Text overflow в flex-контейнерах

**Что проверять:** Текст выходит за границы flex-item или не обрезается.

**Фикс:**
```css
.flex-text-item {
  min-width: 0;  /* ключевой фикс для flex */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

---

### G3. Неправильное использование `justify-content: space-between` при одном элементе

**Что проверять:** `space-between` при одном flex-child — элемент прижимается к краю.

**Фикс:**
```css
/* Использовать gap вместо space-between для равномерных отступов */
.flex-container {
  display: flex;
  gap: var(--space-4);
  /* вместо justify-content: space-between */
}
```

---

### G4. Grid gap/column несоответствие

**Что проверять:**
```css
/* 🟡 Баг: grid-template-columns не учитывает gap */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 33.33%); /* 3 × 33.33% + 2 × gap = overflow */
  gap: 20px;
}
```

**Фикс:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* fr учитывает gap автоматически */
  gap: 20px;
}
```

---

### G5. Auto-fill vs Auto-fit путаница

**Что проверять:**
```css
/* auto-fill создаёт пустые колонки, auto-fit — коллапсирует их */
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
```

**Правило:**
- `auto-fill` — сохраняет пустые треки (для выравнивания по правому краю)
- `auto-fit` — коллапсирует пустые треки (элементы занимают всю ширину)

---

### G6. Align-items vs Align-content путаница

**Что проверять:** Неправильное свойство для однострочного/многострочного flex.

**Правило:**
- `align-items` — выравнивает элементы на текущей строке
- `align-content` — выравнивает строки (работает только при `flex-wrap: wrap` и нескольких строках)

---

## 9. БЛОК H — АДАПТИВНОСТЬ (RESPONSIVE)

### H1. Горизонтальный скролл на мобильных

**Что проверять:**
```css
/* 🔴 Критично: элементы шире viewport */
.element { width: 600px; } /* без медиа-запроса */
```

**Диагностика:** Найти все фиксированные ширины `> 320px` без responsive обёртки.

**Фикс:**
```css
/* Глобальный предохранитель */
*, *::before, *::after {
  box-sizing: border-box;
}
body {
  overflow-x: hidden; /* крайний случай — скрыть, но лучше фиксить причину */
}
.element {
  width: min(600px, 100%);
}
```

---

### H2. Текст не масштабируется на мобильных

**Что проверять:** Фиксированные `px` размеры без `clamp()` или `vw` единиц.

**Фикс:**
```css
h1 { font-size: clamp(24px, 5vw, 64px); }
h2 { font-size: clamp(20px, 4vw, 48px); }
p  { font-size: clamp(14px, 2vw, 18px); }
```

---

### H3. Брейкпоинты не охватывают все состояния

**Что проверять:** Только один брейкпоинт (например, `@media (max-width: 768px)`) без промежуточных.

**Рекомендуемая система:**
```css
/* Mobile-first подход */
/* Base: 0–599px (mobile) — базовые стили */

@media (min-width: 600px)  { /* small tablets */ }
@media (min-width: 768px)  { /* tablets */ }
@media (min-width: 1024px) { /* desktop */ }
@media (min-width: 1280px) { /* large desktop */ }
@media (min-width: 1536px) { /* XL screens */ }
```

---

### H4. Touch-цели слишком близко друг к другу

**Что проверять:** Расстояние между кликабельными элементами < 8px на мобильных.

**Фикс:**
```css
@media (pointer: coarse) { /* тач-устройства */
  .nav-item { padding: 12px 16px; }
  .btn + .btn { margin-left: 8px; }
}
```

---

### H5. Viewport meta отсутствует или неправильный

**Что проверять в HTML:**
```html
<!-- 🔴 Отсутствует или неправильный -->
<meta name="viewport" content="width=1200"> <!-- фиксированная ширина -->

<!-- ✅ Правильный -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## 10. БЛОК I — ПЕРЕПОЛНЕНИЕ И ОБРЕЗКА КОНТЕНТА (OVERFLOW)

### I1. Контент выходит за границы родителя

**Что проверять:**
```css
/* 🔴 Баг: дочерний абсолютно спозиционированный элемент */
.parent { position: relative; }
.child  { position: absolute; right: -20px; } /* выходит за край */
```

**Диагностика:** Все `position: absolute/fixed` элементы — проверить, не выходят ли за bounds.

---

### I2. `overflow: hidden` обрезает box-shadow/outline

**Что проверять:**
```css
/* 🟡 Баг: shadow обрезается */
.card {
  overflow: hidden; /* обрезает shadow */
  box-shadow: 0 4px 20px rgba(0,0,0,0.15); /* не видна полностью */
}
```

**Фикс:** Применить `overflow: hidden` к внутреннему элементу, shadow — к внешнему:
```css
.card-wrapper { box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
.card-inner   { overflow: hidden; border-radius: inherit; }
```

---

### I3. Текстовый overflow без ellipsis

**Что проверять:** Длинные строки рвут layout или уходят за границы.

**Фикс:**
```css
/* Однострочный */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Многострочный (webkit) */
.truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

---

### I4. Скролл без скрытия scrollbar

**Что проверять:** Кастомные scroll-контейнеры с уродливым системным scrollbar.

**Фикс:**
```css
.scroll-container {
  overflow-y: auto;
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: #888 transparent;
}
.scroll-container::-webkit-scrollbar { width: 4px; }
.scroll-container::-webkit-scrollbar-thumb { background: #888; border-radius: 4px; }
```

---

## 11. БЛОК J — Z-INDEX И СЛОИ

### J1. Z-index война (z-index escalation)

**Что проверять:**
```css
/* 🟠 Баг: бесконтрольный z-index */
.header   { z-index: 9999; }
.modal    { z-index: 99999; }
.tooltip  { z-index: 999999; }
```

**Решение — Z-index Scale через переменные:**
```css
:root {
  --z-base:    0;
  --z-raised:  10;
  --z-dropdown: 100;
  --z-sticky:  200;
  --z-overlay: 300;
  --z-modal:   400;
  --z-toast:   500;
  --z-tooltip: 600;
}
```

---

### J2. Stacking context непредсказуемый

**Что проверять:** Элемент с `z-index` не работает ожидаемо — он находится внутри stacking context родителя с `transform`, `opacity`, `will-change`, `filter`.

**Диагностика:** Найти все:
```css
transform: ...
opacity: < 1
will-change: transform
filter: ...
isolation: isolate
```
Эти свойства создают новый stacking context.

**Фикс:** Добавить `isolation: isolate` к нужному контейнеру для явного создания контекста.

---

### J3. Dropdown/tooltip перекрыт другими элементами

**Что проверять:** Выпадающие меню под соседними секциями.

**Фикс:**
```css
.section-with-dropdown {
  position: relative;
  z-index: var(--z-raised); /* поднять секцию */
}
```

---

## 12. БЛОК K — ИЗОБРАЖЕНИЯ И МЕДИА

### K1. Изображения без размеров — Layout Shift

**Что проверять:**
```html
<!-- 🔴 Баг: нет width/height — CLS (Cumulative Layout Shift) -->
<img src="photo.jpg" alt="Фото">
```

**Фикс:**
```html
<img src="photo.jpg" alt="Фото" width="800" height="600" loading="lazy">
```

---

### K2. Retina-незаметные изображения

**Что проверять:** Одиночный `src` без `srcset` — размытость на Retina экранах.

**Фикс:**
```html
<img
  src="photo-800.jpg"
  srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="Фото"
>
```

---

### K3. SVG без viewBox

**Что проверять:**
```html
<!-- 🟠 Баг: SVG без viewBox не масштабируется правильно -->
<svg width="24" height="24"> <!-- без viewBox -->
```

**Фикс:**
```html
<svg viewBox="0 0 24 24" width="24" height="24">
```

---

### K4. Фоновые изображения без fallback

**Что проверять:**
```css
/* 🟡 Баг: нет fallback цвета */
.hero {
  background-image: url('hero.jpg');
  /* нет background-color */
}
```

**Фикс:**
```css
.hero {
  background-color: #1a1a2e; /* fallback пока грузится/если не загрузилось */
  background-image: url('hero.jpg');
  background-size: cover;
  background-position: center;
}
```

---

## 13. БЛОК L — АНИМАЦИИ И ПЕРЕХОДЫ

### L1. Анимации без `prefers-reduced-motion`

**Что проверять:** Все анимации запускаются у пользователей с вестибулярными нарушениями.

**Фикс:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

### L2. Анимируются свойства вызывающие reflow

**Что проверять:** Анимация `width`, `height`, `margin`, `padding`, `top`, `left` — дорогостоящие reflow.

**Правило:** Анимировать только:
```css
/* ✅ Дешёво (только composite) */
transform: translateX() / scale() / rotate()
opacity: 0 → 1
```

**Фикс:**
```css
/* ❌ Дорого */
.el { transition: width 0.3s, left 0.3s; }

/* ✅ Дёшево */
.el { transition: transform 0.3s, opacity 0.3s; }
/* Заменить left: 100px → transform: translateX(100px) */
```

---

### L3. Отсутствие/неправильные timing functions

**Что проверять:** Все переходы с `linear` — выглядят механически.

**Рекомендуемые easing:**
```css
:root {
  --ease-in:      cubic-bezier(0.4, 0, 1, 1);
  --ease-out:     cubic-bezier(0, 0, 0.2, 1);  /* для элементов появляющихся */
  --ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1); /* для большинства UI */
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1); /* пружинный эффект */
}
```

---

### L4. Flash of Unstyled Content (FOUC)

**Что проверять:** Элементы мигают при загрузке страницы.

**Диагностика:** JS добавляет классы после DOMContentLoaded — элементы видны до стилизации.

**Фикс:**
```html
<!-- Скрыть до инициализации -->
<html class="no-js">
<script>document.documentElement.classList.replace('no-js','js');</script>
```
```css
.no-js .animated-element { visibility: hidden; }
```

---

## 14. БЛОК M — ФОРМЫ И ИНТЕРАКТИВНЫЕ ЭЛЕМЕНТЫ

### M1. Отсутствие focus-visible стилей

**Что проверять:**
```css
/* 🔴 Критично для доступности */
:focus { outline: none; } /* убрали outline без замены */
```

**Фикс:**
```css
/* Убрать для мыши, оставить для клавиатуры */
:focus:not(:focus-visible) { outline: none; }
:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 3px;
  border-radius: 3px;
}
```

---

### M2. Placeholder вместо Label

**Что проверять:**
```html
<!-- 🟠 Баг: нет label, только placeholder -->
<input type="email" placeholder="Введите email">
```

**Фикс:**
```html
<label for="email">Email</label>
<input type="email" id="email" placeholder="example@mail.com">
```

---

### M3. Состояния hover/active/disabled не стилизованы

**Что проверять:** Интерактивные элементы без визуального feedback.

**Минимум состояний:**
```css
.btn {
  /* default */
  background: var(--color-primary-500);
  transition: all 0.2s var(--ease-out);
}
.btn:hover    { background: var(--color-primary-700); transform: translateY(-1px); }
.btn:active   { background: var(--color-primary-900); transform: translateY(0); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; pointer-events: none; }
.btn:focus-visible { /* см. M1 */ }
```

---

### M4. Checkbox/Radio не кастомизированы, но нужны

**Что проверять:** Системные чекбоксы в контексте кастомного дизайна.

**Фикс (CSS-only):**
```css
input[type="checkbox"] {
  appearance: none;
  width: 18px; height: 18px;
  border: 2px solid var(--color-border);
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}
input[type="checkbox"]:checked {
  background: var(--color-primary-500);
  border-color: var(--color-primary-500);
}
input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
}
```

---

## 15. БЛОК N — ВИЗУАЛЬНАЯ ИЕРАРХИЯ

### N1. Все элементы одинакового визуального веса

**Что проверять:** Нет явного главного акцента — глаз не знает куда смотреть первым.

**Диагностика:** Определить Primary CTA и проверить, выделяется ли он визуально (размером, цветом, пространством).

**Правило:** Максимум 1 primary action per view.

---

### N2. Заголовки не создают иерархию

**Что проверять:**
```css
/* 🟡 Баг: H1 и H2 почти одинаковые */
h1 { font-size: 24px; font-weight: 600; }
h2 { font-size: 22px; font-weight: 600; }
```

**Фикс — минимальный ratio 1.25x между уровнями:**
```css
h1 { font-size: 3rem;   font-weight: 800; }
h2 { font-size: 2rem;   font-weight: 700; }
h3 { font-size: 1.5rem; font-weight: 600; }
h4 { font-size: 1.25rem;font-weight: 600; }
```

---

### N3. Недостаточное использование пространства для акцента

**Что проверять:** Важные элементы зажаты среди других без breathing room.

**Принцип:** Пространство вокруг элемента повышает его важность.

```css
.hero-headline {
  margin-bottom: var(--space-8); /* больше пространства = больше веса */
}
```

---

## 16. БЛОК O — КОНСИСТЕНТНОСТЬ СИСТЕМЫ

### O1. Отсутствие Design Tokens

**Что проверять:** Значения цветов, отступов, размеров повторяются хардкодом по всему коду.

**Диагностика:** Поиск одинаковых значений (например, `#3498db` встречается 15 раз).

**Фикс:** Вынести в CSS Custom Properties (см. примеры выше в блоках B, C, E, F).

---

### O2. Несогласованные border-radius

**Что проверять:** Карточки с `border-radius: 4px`, кнопки с `border-radius: 12px`, инпуты с `border-radius: 8px` — разные радиусы без логики.

**Фикс — Radius Scale:**
```css
:root {
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:  12px;
  --radius-xl:  16px;
  --radius-2xl: 24px;
  --radius-full: 9999px; /* pills */
}
```

---

### O3. Несогласованные тени

**Что проверять:** Разные `box-shadow` значения без системы.

**Фикс — Shadow Scale:**
```css
:root {
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.12);
  --shadow-md:  0 4px 12px rgba(0,0,0,0.15);
  --shadow-lg:  0 8px 24px rgba(0,0,0,0.18);
  --shadow-xl:  0 16px 48px rgba(0,0,0,0.22);
}
```

---

### O4. Разные стили одного и того же компонента

**Что проверять:** Кнопки с одной функцией имеют разный вид в разных частях сайта.

**Диагностика:** Найти все `<button>`, `<a class="btn">` и сравнить их стили.

---

## 17. БЛОК P — JAVASCRIPT-ВЛИЯНИЕ НА UI

### P1. FOUC от JS-управляемых стилей

**Что проверять:** Классы для стилизации добавляются через JS после рендера.

**Диагностика:** Все `classList.add()` в `DOMContentLoaded` / `onload`.

**Фикс:** CSS-first подход — базовые стили без JS, JS только модифицирует.

---

### P2. Динамический контент без резервных размеров

**Что проверять:** Контейнеры для данных загружаемых через fetch имеют `height: 0` до загрузки.

**Фикс — Skeleton screens:**
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: var(--radius-sm);
}
@keyframes skeleton-loading {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

### P3. Event handlers вызывающие layout thrashing

**Что проверять:** В scroll/resize обработчиках — чтение и запись DOM вперемешку.

**Диагностика:** Поиск паттернов в JS:
```javascript
// 🔴 Layout thrashing
element.style.height = element.offsetHeight + 'px'; // read → write → read → write
```

**Фикс:**
```javascript
// ✅ Батчинг через requestAnimationFrame
requestAnimationFrame(() => {
  const height = element.offsetHeight; // все reads
  element.style.height = height + 'px'; // все writes
});
```

---

### P4. Классы состояний не отражают реальное состояние

**Что проверять:** `is-active`, `is-open`, `is-loading` — классы не удаляются после смены состояния.

**Диагностика:** Проверить все toggle/add/remove логику.

---

## 18. ШАБЛОН ФИНАЛЬНОГО ОТЧЁТА

```
═══════════════════════════════════════════════════════
          DESIGN CHECK REPORT — [Название проекта]
═══════════════════════════════════════════════════════

СВОДКА
──────
Дата проверки:     [дата]
Файлов проверено:  [кол-во]
Багов найдено:     [общее]
  🔴 CRITICAL:  [кол-во]
  🟠 HIGH:      [кол-во]
  🟡 MEDIUM:    [кол-во]
  🟢 LOW:       [кол-во]

КРИТИЧЕСКИЕ БАГИ (требуют немедленного исправления)
────────────────────────────────────────────────────
[ID: C-001]
Блок:       E1 — Контраст
Файл:       style.css, строка 234
Проблема:   Цвет текста #aaaaaa на фоне #ffffff — ratio 2.3:1 (минимум 4.5:1)
Решение:    Изменить на color: #767676 (ratio 4.54:1) или color: #595959 (ratio 7:1)
До:         color: #aaaaaa;
После:      color: #595959;

ВЫСОКИЕ БАГИ
────────────────────────────────────────────────────
[ID: H-001]
...

СРЕДНИЕ БАГИ
────────────────────────────────────────────────────
[ID: M-001]
...

НИЗКИЕ ПРИОРИТЕТЫ / POLISH
────────────────────────────────────────────────────
[ID: L-001]
...

СИСТЕМНЫЕ РЕКОМЕНДАЦИИ
────────────────────────────────────────────────────
1. Внедрить CSS Custom Properties для всех повторяющихся значений
2. Перейти на 8px spacing grid
3. Добавить type scale систему
4. Создать единый компонент .btn с полными состояниями
5. Добавить @media (prefers-reduced-motion)

═══════════════════════════════════════════════════════
```

---

## 19. БЫСТРЫЙ ЧЕКЛИСТ (QUICK SCAN)

Для быстрой первичной проверки — пройти каждый пункт:

### HTML
- [ ] Нет дублирующихся `id`
- [ ] Нет `<div>` внутри `<p>` или `<span>` внутри `<div>`
- [ ] Viewport meta присутствует и корректен
- [ ] У всех `<img>` есть `alt`, `width`, `height`

### Типографика и цвет
- [ ] Минимальный размер шрифта ≥ 14px (body), ≥ 12px (captions)
- [ ] `line-height` для body: 1.4–1.7
- [ ] Контраст текста ≥ 4.5:1 (основной), ≥ 3:1 (крупный)
- [ ] Не более 3 font-family в проекте

### Spacing и выравнивание
- [ ] Все отступы кратны 4px или 8px
- [ ] Схожие элементы имеют одинаковые padding/margin
- [ ] Нет "магических чисел" (13px, 17px, 23px)

### Layout
- [ ] Нет фиксированных ширин без `max-width` и `width: 100%`
- [ ] Все `display: flex` контейнеры имеют корректные `flex-shrink`
- [ ] Grid использует `fr` единицы (не `%` с gap)
- [ ] `min-width: 0` у flex-детей с текстом

### Адаптивность
- [ ] Нет горизонтального скролла на 320px ширине
- [ ] Брейкпоинты есть для: 600px, 768px, 1024px
- [ ] Touch-цели ≥ 44×44px

### Изображения
- [ ] Все изображения с `object-fit: cover/contain`
- [ ] SVG имеют `viewBox`
- [ ] Фоновые изображения имеют `background-color` fallback

### Интерактивность
- [ ] Кнопки/ссылки стилизованы для: default, hover, active, disabled, focus
- [ ] Нет `outline: none` без `focus-visible` замены
- [ ] Анимации отключаются при `prefers-reduced-motion`

### Консистентность
- [ ] Все цвета через CSS Custom Properties
- [ ] Единый `border-radius` scale
- [ ] Единый `box-shadow` scale
- [ ] Z-index управляется через переменные

---

*Design Check Protocol Guide v1.0*
*Охват: HTML структура, CSS layout, типографика, цвет, адаптивность, доступность, JS-влияние на UI*
