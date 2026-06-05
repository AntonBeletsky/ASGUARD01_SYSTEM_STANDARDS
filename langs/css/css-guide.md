# МОНУМЕНТАЛЬНОЕ РУКОВОДСТВО ПО СОВРЕМЕННОМУ CSS
## Полное самодостаточное руководство для ИИ-агентов и разработчиков

> **Версия**: 2025 Edition  
> **Охват**: CSS3, CSS4, Living Standard — всё актуальное на сегодняшний день  
> **Принцип**: Только рабочий, современный, производительный код. Никаких устаревших паттернов.

---

## СОДЕРЖАНИЕ

1. [Философия и принципы современного CSS](#1-философия-и-принципы)
2. [Архитектура CSS и организация кода](#2-архитектура-css)
3. [Каскад, специфичность и наследование](#3-каскад-специфичность-наследование)
4. [CSS Custom Properties (переменные)](#4-css-custom-properties)
5. [Блочная модель (Box Model)](#5-блочная-модель)
6. [Flexbox — полное руководство](#6-flexbox)
7. [CSS Grid — полное руководство](#7-css-grid)
8. [Subgrid](#8-subgrid)
9. [Позиционирование](#9-позиционирование)
10. [Типографика](#10-типографика)
11. [Цвет и градиенты](#11-цвет-и-градиенты)
12. [Фоны, границы, тени](#12-фоны-границы-тени)
13. [Трансформации](#13-трансформации)
14. [Переходы (Transitions)](#14-переходы)
15. [Анимации (Animations)](#15-анимации)
16. [Адаптивный дизайн и Media Queries](#16-адаптивный-дизайн)
17. [Container Queries](#17-container-queries)
18. [CSS Functions](#18-css-functions)
19. [Псевдоклассы и псевдоэлементы](#19-псевдоклассы-и-псевдоэлементы)
20. [Логические свойства (Logical Properties)](#20-логические-свойства)
21. [CSS Layers (@layer)](#21-css-layers)
22. [CSS Nesting](#22-css-nesting)
23. [Scroll Behavior и Scroll Snap](#23-scroll)
24. [CSS Shapes и clip-path](#24-shapes-и-clip-path)
25. [Фильтры и режимы смешивания](#25-фильтры-и-blend-modes)
26. [CSS Grid — продвинутые техники](#26-grid-advanced)
27. [Производительность CSS](#27-производительность)
28. [Доступность (Accessibility) в CSS](#28-доступность)
29. [Тёмная тема (Dark Mode)](#29-тёмная-тема)
30. [CSS Reset и нормализация](#30-css-reset)
31. [Именование: BEM, CUBE CSS, Utility-first](#31-именование)
32. [Компонентные паттерны](#32-компонентные-паттерны)
33. [Антипаттерны и частые ошибки](#33-антипаттерны)
34. [Отладка CSS](#34-отладка)
35. [Полная библиотека сниппетов](#35-библиотека-сниппетов)
36. [Справочник свойств по категориям](#36-справочник)

---

## 1. ФИЛОСОФИЯ И ПРИНЦИПЫ

### 1.1 Современный подход к CSS

CSS в 2024–2025 — это мощный, самодостаточный язык. Больше не нужны:
- `float` для раскладки (используй Grid/Flexbox)
- Хаки для вертикального центрирования
- JavaScript для простых анимаций
- Вендорные префиксы для большинства свойств
- Препроцессоры для вложенности и переменных

```css
/* ❌ СТАРЫЙ подход */
.container {
  width: 960px;
  margin: 0 auto;
}
.column {
  float: left;
  width: 33.333%;
}
.clearfix::after {
  content: '';
  display: table;
  clear: both;
}

/* ✅ СОВРЕМЕННЫЙ подход */
.container {
  max-width: 60rem;
  margin-inline: auto;
  padding-inline: clamp(1rem, 5vw, 3rem);
}
.columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 20rem), 1fr));
}
```

### 1.2 Принципы, которым должен следовать ИИ

**P1: CSS-first** — решай задачи средствами CSS, не JavaScript  
**P2: Прогрессивное улучшение** — базовые стили работают везде, улучшения — там, где поддерживается  
**P3: Логические свойства** — используй `margin-inline`, `padding-block` вместо `margin-left/right`  
**P4: Fluid всё** — типографика, отступы, размеры через `clamp()` и относительные единицы  
**P5: Переменные для всего** — все токены дизайна — в Custom Properties  
**P6: Слои (Layers)** — контролируй специфичность через `@layer`  
**P7: Нулевая специфичность где возможно** — используй `:where()` и `@layer`  

### 1.3 Что проверять перед использованием свойства

```css
/* Проверь поддержку через @supports */
@supports (display: grid) {
  .layout { display: grid; }
}

@supports (container-type: inline-size) {
  .card { container-type: inline-size; }
}

@supports not (gap: 1rem) {
  /* Фолбэк для старых браузеров */
}
```

---

## 2. АРХИТЕКТУРА CSS

### 2.1 Структура файлов (рекомендуемая)

```
styles/
├── base/
│   ├── reset.css          # CSS Reset/Normalize
│   ├── tokens.css         # Design tokens (CSS variables)
│   └── typography.css     # Базовые стили текста
├── layout/
│   ├── grid.css           # Глобальные сетки
│   └── containers.css     # Контейнеры, обёртки
├── components/
│   ├── button.css
│   ├── card.css
│   └── ...
├── utilities/
│   └── utilities.css      # Вспомогательные классы
└── main.css               # Точка входа с @layer и @import
```

### 2.2 Точка входа с @layer

```css
/* main.css */
@layer reset, tokens, base, layout, components, utilities, overrides;

@import url('base/reset.css') layer(reset);
@import url('base/tokens.css') layer(tokens);
@import url('base/typography.css') layer(base);
@import url('layout/grid.css') layer(layout);
@import url('components/button.css') layer(components);
@import url('utilities/utilities.css') layer(utilities);
```

### 2.3 Design Tokens — основа системы

```css
/* tokens.css */
:root {
  /* ─── Цветовая палитра ─── */
  --color-neutral-0:   #ffffff;
  --color-neutral-100: #f8f9fa;
  --color-neutral-200: #e9ecef;
  --color-neutral-300: #dee2e6;
  --color-neutral-400: #ced4da;
  --color-neutral-500: #adb5bd;
  --color-neutral-600: #6c757d;
  --color-neutral-700: #495057;
  --color-neutral-800: #343a40;
  --color-neutral-900: #212529;
  --color-neutral-1000: #000000;

  --color-brand-100: #e0f2fe;
  --color-brand-300: #7dd3fc;
  --color-brand-500: #0ea5e9;
  --color-brand-700: #0369a1;
  --color-brand-900: #0c4a6e;

  --color-success-100: #dcfce7;
  --color-success-500: #22c55e;
  --color-success-900: #14532d;

  --color-warning-100: #fef9c3;
  --color-warning-500: #eab308;
  --color-warning-900: #713f12;

  --color-danger-100: #fee2e2;
  --color-danger-500: #ef4444;
  --color-danger-900: #7f1d1d;

  /* ─── Семантические цвета ─── */
  --color-bg:           var(--color-neutral-0);
  --color-bg-subtle:    var(--color-neutral-100);
  --color-bg-muted:     var(--color-neutral-200);
  --color-surface:      var(--color-neutral-0);
  --color-border:       var(--color-neutral-200);
  --color-border-strong: var(--color-neutral-300);
  --color-text:         var(--color-neutral-900);
  --color-text-muted:   var(--color-neutral-600);
  --color-text-subtle:  var(--color-neutral-500);
  --color-accent:       var(--color-brand-500);
  --color-accent-hover: var(--color-brand-700);

  /* ─── Типографика ─── */
  --font-sans:   system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-serif:  Georgia, 'Times New Roman', serif;
  --font-mono:   'Fira Code', 'Cascadia Code', Consolas, monospace;

  --font-size-xs:   0.75rem;    /* 12px */
  --font-size-sm:   0.875rem;   /* 14px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-md:   1.125rem;   /* 18px */
  --font-size-lg:   1.25rem;    /* 20px */
  --font-size-xl:   1.5rem;     /* 24px */
  --font-size-2xl:  1.875rem;   /* 30px */
  --font-size-3xl:  2.25rem;    /* 36px */
  --font-size-4xl:  3rem;       /* 48px */
  --font-size-5xl:  3.75rem;    /* 60px */

  /* Fluid типографика */
  --font-size-fluid-sm:  clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-size-fluid-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-fluid-lg:  clamp(1.25rem, 1rem + 1.25vw, 1.875rem);
  --font-size-fluid-xl:  clamp(1.5rem, 1rem + 2.5vw, 3rem);
  --font-size-fluid-2xl: clamp(2rem, 1rem + 5vw, 5rem);

  --font-weight-light:   300;
  --font-weight-normal:  400;
  --font-weight-medium:  500;
  --font-weight-semibold: 600;
  --font-weight-bold:    700;
  --font-weight-black:   900;

  --line-height-tight:   1.2;
  --line-height-snug:    1.35;
  --line-height-normal:  1.5;
  --line-height-relaxed: 1.65;
  --line-height-loose:   2;

  --letter-spacing-tight: -0.05em;
  --letter-spacing-normal: 0em;
  --letter-spacing-wide:   0.05em;
  --letter-spacing-wider:  0.1em;
  --letter-spacing-widest: 0.25em;

  /* ─── Отступы ─── */
  --space-1:  0.25rem;   /* 4px  */
  --space-2:  0.5rem;    /* 8px  */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.25rem;   /* 20px */
  --space-6:  1.5rem;    /* 24px */
  --space-8:  2rem;      /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */
  --space-32: 8rem;      /* 128px */

  /* Fluid отступы */
  --space-fluid-sm:  clamp(0.75rem, 2vw, 1.5rem);
  --space-fluid-md:  clamp(1.5rem, 4vw, 3rem);
  --space-fluid-lg:  clamp(2rem, 8vw, 6rem);
  --space-fluid-xl:  clamp(3rem, 10vw, 8rem);

  /* ─── Размеры ─── */
  --size-container-sm:  36rem;   /* 576px */
  --size-container-md:  48rem;   /* 768px */
  --size-container-lg:  64rem;   /* 1024px */
  --size-container-xl:  80rem;   /* 1280px */
  --size-container-2xl: 96rem;   /* 1536px */

  /* ─── Радиусы ─── */
  --radius-sm:   0.125rem;  /* 2px  */
  --radius-md:   0.375rem;  /* 6px  */
  --radius-lg:   0.5rem;    /* 8px  */
  --radius-xl:   0.75rem;   /* 12px */
  --radius-2xl:  1rem;      /* 16px */
  --radius-3xl:  1.5rem;    /* 24px */
  --radius-full: 9999px;

  /* ─── Тени ─── */
  --shadow-sm:   0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md:   0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg:   0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl:   0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl:  0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);

  /* ─── Переходы ─── */
  --duration-fast:    100ms;
  --duration-normal:  200ms;
  --duration-slow:    300ms;
  --duration-slower:  500ms;

  --ease-default:  cubic-bezier(0.4, 0, 0.2, 1);   /* ease-in-out */
  --ease-in:       cubic-bezier(0.4, 0, 1, 1);
  --ease-out:      cubic-bezier(0, 0, 0.2, 1);
  --ease-bounce:   cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-spring:   cubic-bezier(0.5, 0, 0.5, 1.5);

  /* ─── z-index шкала ─── */
  --z-hide:      -1;
  --z-base:       0;
  --z-raised:     1;
  --z-dropdown:   10;
  --z-sticky:     20;
  --z-fixed:      30;
  --z-overlay:    40;
  --z-modal:      50;
  --z-popover:    60;
  --z-toast:      70;
  --z-tooltip:    80;
  --z-top:        90;

  /* ─── Breakpoints (для использования в JS/data-атрибутах) ─── */
  --bp-sm:  640px;
  --bp-md:  768px;
  --bp-lg:  1024px;
  --bp-xl:  1280px;
  --bp-2xl: 1536px;
}
```

---

## 3. КАСКАД, СПЕЦИФИЧНОСТЬ И НАСЛЕДОВАНИЕ

### 3.1 Порядок каскада (от наименьшего к наибольшему приоритету)

```
1. Стили браузера (user-agent styles)
2. Пользовательские стили браузера
3. Авторские стили:
   a. @layer (в порядке объявления слоёв)
   b. Обычные стили (не в @layer)
   c. !important в @layer (обратный порядок)
   d. !important в обычных стилях
4. Встроенные стили (style="")
5. !important встроенные
```

### 3.2 Специфичность — таблица

| Селектор | Специфичность | Числовое значение |
|----------|---------------|-------------------|
| `*` | 0-0-0 | 0 |
| `div`, `p`, `h1` | 0-0-1 | 1 |
| `.class`, `[attr]`, `:hover` | 0-1-0 | 10 |
| `#id` | 1-0-0 | 100 |
| `style=""` | 1-0-0-0 | 1000 |
| `!important` | Перекрывает всё | ∞ |
| `:is()`, `:not()`, `:has()` | Наибольшая из аргументов | varies |
| `:where()` | 0-0-0 | 0 |

```css
/* Примеры специфичности */
div               /* 0-0-1 */
.card             /* 0-1-0 */
div.card          /* 0-1-1 */
#main             /* 1-0-0 */
#main .card       /* 1-1-0 */
#main .card:hover /* 1-1-1 */

/* :where() = 0 специфичность — идеально для утилит */
:where(.text-center) { text-align: center; }

/* :is() = специфичность наибольшего аргумента */
:is(h1, h2, h3)  /* 0-0-1 (тег) */
:is(.title, #hero) { }  /* 1-0-0 (из-за #hero!) */
```

### 3.3 Управление специфичностью

```css
/* ✅ Увеличение специфичности без ID */
.component.component { /* 0-2-0 */ }

/* ✅ Нулевая специфичность */
:where(.utility-class) { display: flex; }

/* ✅ Специфичность через :not() */
.btn:not(.btn-custom) { color: blue; }

/* ✅ :has() для родительской специфичности */
.card:has(> .featured) { border: 2px solid gold; }

/* ❌ Избегай !important кроме reset и utility */
.text-red { color: red !important; } /* только для utility */
```

### 3.4 Наследуемые свойства (важно знать)

```css
/* НАСЛЕДУЮТСЯ автоматически: */
color, font-*, line-height, letter-spacing, word-spacing,
text-align, text-transform, text-indent, text-shadow,
visibility, cursor, pointer-events,
list-style-*, quotes, direction,
border-collapse, border-spacing (таблицы),
caption-side, empty-cells (таблицы)

/* НЕ НАСЛЕДУЮТСЯ (нужно явно указывать или использовать inherit): */
display, position, top/right/bottom/left, z-index,
width, height, margin, padding, border,
background-*, overflow, opacity,
transform, animation, transition,
box-shadow, outline
```

```css
/* Явное наследование */
.child {
  border: inherit;        /* принять значение родителя */
  color: initial;         /* сбросить до начального */
  padding: unset;         /* inherit для наследуемых, initial для остальных */
  margin: revert;         /* до стиля браузера */
  border-radius: revert-layer; /* до предыдущего @layer */
}
```

---

## 4. CSS CUSTOM PROPERTIES

### 4.1 Базовый синтаксис

```css
/* Объявление */
:root {
  --color-primary: #0ea5e9;
  --spacing-unit: 0.5rem;
  --grid-columns: 12;
}

/* Использование */
.element {
  color: var(--color-primary);
  margin: calc(var(--spacing-unit) * 4);
}

/* Фолбэк значение */
.element {
  color: var(--color-primary, blue);
  margin: var(--spacing, 1rem);
  /* Цепочка фолбэков */
  font-size: var(--size-custom, var(--font-size-base, 1rem));
}
```

### 4.2 Область видимости (Scope)

```css
/* Глобальные — на :root */
:root { --color: blue; }

/* Компонентные — на элементе */
.card {
  --card-padding: 1.5rem;
  --card-radius: 0.75rem;
  padding: var(--card-padding);
  border-radius: var(--card-radius);
}

/* Переопределение в контексте */
.sidebar .card {
  --card-padding: 1rem; /* только для карточек в сайдбаре */
}

/* Медиазапросы изменяют переменные */
:root {
  --columns: 1;
  --font-scale: 1;
}

@media (min-width: 768px) {
  :root {
    --columns: 2;
    --font-scale: 1.1;
  }
}
```

### 4.3 Продвинутые паттерны

```css
/* ─── Пространства имён ─── */
.btn {
  /* Приватные переменные компонента */
  --_btn-bg: var(--btn-bg, var(--color-accent));
  --_btn-color: var(--btn-color, white);
  --_btn-padding: var(--btn-padding, 0.5rem 1rem);
  --_btn-radius: var(--btn-radius, var(--radius-md));

  background: var(--_btn-bg);
  color: var(--_btn-color);
  padding: var(--_btn-padding);
  border-radius: var(--_btn-radius);
}

/* Пользователь настраивает через публичное API */
.btn-custom {
  --btn-bg: purple;
  --btn-padding: 1rem 2rem;
}

/* ─── Числовые переменные для вычислений ─── */
:root {
  --ratio: 1.618;           /* Golden ratio */
  --base-size: 1rem;
  --size-sm:   calc(var(--base-size) / var(--ratio));
  --size-lg:   calc(var(--base-size) * var(--ratio));
  --size-xl:   calc(var(--size-lg) * var(--ratio));
}

/* ─── Булевые переменные ─── */
/* Техника: 0 = false, 1 = true */
.element {
  --is-active: 0;
  opacity: calc(0.5 + var(--is-active) * 0.5); /* 0.5 или 1 */
}
.element.active {
  --is-active: 1;
}

/* ─── CSS Variable как множитель состояний ─── */
.button {
  --hover: 0;
  --pressed: 0;
  
  background: rgb(
    calc(59 - var(--hover) * 10),
    calc(130 - var(--hover) * 10),
    calc(246 - var(--hover) * 10)
  );
}
.button:hover  { --hover: 1; }
.button:active { --pressed: 1; }

/* ─── Анимация переменных ─── */
@property --progress {
  syntax: '<number>';
  initial-value: 0;
  inherits: false;
}

.progress-bar {
  --progress: 0;
  width: calc(var(--progress) * 100%);
  transition: --progress 0.5s var(--ease-out);
}
```

### 4.4 @property — типизированные переменные

```css
/* Объявление типизированной переменной */
@property --hue {
  syntax: '<number>';        /* Тип: number, color, length, percentage, angle... */
  initial-value: 220;
  inherits: true;            /* наследуется ли */
}

@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@property --card-color {
  syntax: '<color>';
  initial-value: #0ea5e9;
  inherits: false;
}

/* Теперь можно анимировать! */
.spinning-gradient {
  background: conic-gradient(from var(--gradient-angle), red, blue, red);
  animation: spin 4s linear infinite;
}

@keyframes spin {
  to { --gradient-angle: 360deg; }
}

/* Анимация цвета */
.color-shift {
  background: var(--card-color);
  transition: --card-color 0.3s;
}
.color-shift:hover {
  --card-color: #ef4444;
}
```

---

## 5. БЛОЧНАЯ МОДЕЛЬ

### 5.1 box-sizing — всегда border-box

```css
/* ОБЯЗАТЕЛЬНО в каждом проекте */
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

### 5.2 Модели отображения (display)

```css
/* Внешний тип (как элемент ведёт себя в потоке) */
display: block;        /* блочный — занимает всю ширину */
display: inline;       /* строчный — по содержимому */
display: inline-block; /* строчно-блочный */
display: none;         /* скрыт (удалён из потока) */

/* Внутренний тип (как организованы дети) */
display: flex;
display: inline-flex;
display: grid;
display: inline-grid;
display: flow-root;    /* BFC без overflow:hidden */
display: contents;     /* элемент невидим, дети — в потоке родителя */
display: table;        /* и все table-* значения */

/* Новый синтаксис (пока меньше поддержки) */
display: block flow;
display: inline flow-root;
display: block flex;
```

### 5.3 Размеры — современный подход

```css
/* Абсолютные */
width: 300px;
height: 200px;

/* Относительные */
width: 50%;           /* от родителя */
width: 50vw;          /* от viewport */
height: 50vh;
height: 50dvh;        /* dynamic viewport height (мобильные) */
height: 50svh;        /* small viewport height */
height: 50lvh;        /* large viewport height */

/* Содержимое */
width: fit-content;   /* по содержимому, но не > родителя */
width: max-content;   /* максимальная ширина содержимого */
width: min-content;   /* минимальная ширина (по длиннейшему слову) */

/* Ограничения */
min-width: 200px;
max-width: 60rem;
min-height: 400px;

/* Логические свойства (предпочтительны) */
inline-size: 50%;         /* width для ltr/rtl */
block-size: 200px;        /* height для ltr/rtl */
min-inline-size: 200px;
max-inline-size: 60rem;

/* aspect-ratio */
.square    { aspect-ratio: 1; }
.video     { aspect-ratio: 16 / 9; }
.portrait  { aspect-ratio: 3 / 4; }
.golden    { aspect-ratio: 1.618; }

/* Изображение в контейнере */
.hero-img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  object-position: center top;
}
```

### 5.4 Отступы — логические свойства

```css
/* Физические → Логические */
margin-top     → margin-block-start
margin-bottom  → margin-block-end
margin-left    → margin-inline-start
margin-right   → margin-inline-end

padding-top    → padding-block-start
padding-bottom → padding-block-end
padding-left   → padding-inline-start
padding-right  → padding-inline-end

/* Шортхенды */
margin-block: 1rem;           /* top и bottom */
margin-inline: auto;          /* left и right — центрирование! */
padding-block: 0.5rem 1rem;   /* top=0.5rem, bottom=1rem */
padding-inline: 1rem 2rem;    /* left=1rem, right=2rem */

/* Пример современного контейнера */
.container {
  max-inline-size: var(--size-container-lg);
  margin-inline: auto;
  padding-inline: clamp(1rem, 5vw, 3rem);
}
```

### 5.5 overflow

```css
/* Базовые значения */
overflow: visible;   /* По умолчанию */
overflow: hidden;    /* Обрезать */
overflow: scroll;    /* Всегда показывать скроллбар */
overflow: auto;      /* Скроллбар только при необходимости */
overflow: clip;      /* Как hidden, но без BFC, без программного скролла */

/* Раздельно по осям */
overflow-x: hidden;
overflow-y: auto;

/* Современный скролл */
.scroll-container {
  overflow-y: auto;
  overscroll-behavior: contain;    /* предотвратить scroll chaining */
  scroll-padding-top: var(--header-height); /* отступ при якорных ссылках */
  -webkit-overflow-scrolling: touch;  /* плавный скролл iOS */
}

/* Скрыть скроллбар но оставить скролл */
.no-scrollbar {
  overflow: auto;
  scrollbar-width: none;        /* Firefox */
}
.no-scrollbar::-webkit-scrollbar {
  display: none;                /* Chrome/Safari */
}

/* Кастомный скроллбар */
.custom-scroll::-webkit-scrollbar { width: 6px; }
.custom-scroll::-webkit-scrollbar-track { background: var(--color-bg-subtle); }
.custom-scroll::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: var(--radius-full);
}
.custom-scroll::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }

/* Firefox */
.custom-scroll {
  scrollbar-width: thin;
  scrollbar-color: var(--color-border-strong) var(--color-bg-subtle);
}
```

---

## 6. FLEXBOX

### 6.1 Полный справочник свойств

```css
/* ─── КОНТЕЙНЕР (flex container) ─── */
.flex-container {
  display: flex;                /* или inline-flex */

  /* Направление главной оси */
  flex-direction: row;          /* → (по умолчанию) */
  flex-direction: row-reverse;  /* ← */
  flex-direction: column;       /* ↓ */
  flex-direction: column-reverse; /* ↑ */

  /* Перенос */
  flex-wrap: nowrap;            /* без переноса (по умолчанию) */
  flex-wrap: wrap;              /* перенос */
  flex-wrap: wrap-reverse;      /* перенос в обратном направлении */

  /* Шортхенд для direction + wrap */
  flex-flow: row wrap;

  /* Выравнивание на главной оси */
  justify-content: flex-start;     /* |○ ○ ○    | */
  justify-content: flex-end;       /* |    ○ ○ ○| */
  justify-content: center;         /* |  ○ ○ ○  | */
  justify-content: space-between;  /* |○    ○    ○| */
  justify-content: space-around;   /* | ○   ○   ○ | */
  justify-content: space-evenly;   /* |  ○   ○   ○  | */
  justify-content: start;
  justify-content: end;

  /* Выравнивание на поперечной оси */
  align-items: stretch;         /* растянуть (по умолчанию) */
  align-items: flex-start;      /* к началу */
  align-items: flex-end;        /* к концу */
  align-items: center;          /* по центру */
  align-items: baseline;        /* по базовой линии текста */

  /* Выравнивание рядов (при flex-wrap) */
  align-content: flex-start;
  align-content: flex-end;
  align-content: center;
  align-content: space-between;
  align-content: space-around;
  align-content: stretch;

  /* Отступы между элементами */
  gap: 1rem;                    /* row-gap и column-gap */
  gap: 1rem 2rem;               /* row-gap column-gap */
  row-gap: 1rem;
  column-gap: 2rem;
}

/* ─── ЭЛЕМЕНТ (flex item) ─── */
.flex-item {
  /* Порядок */
  order: 0;                     /* по умолчанию; меньше = раньше */
  order: -1;                    /* переместить в начало */
  order: 999;                   /* переместить в конец */

  /* Рост */
  flex-grow: 0;                 /* не расти (по умолчанию) */
  flex-grow: 1;                 /* занять доступное пространство */

  /* Сжатие */
  flex-shrink: 1;               /* сжиматься (по умолчанию) */
  flex-shrink: 0;               /* не сжиматься */

  /* Базовый размер */
  flex-basis: auto;             /* по содержимому (по умолчанию) */
  flex-basis: 0;                /* игнорировать содержимое */
  flex-basis: 200px;
  flex-basis: 30%;

  /* Шортхенд flex: grow shrink basis */
  flex: 0 1 auto;               /* по умолчанию */
  flex: 1;                      /* flex: 1 1 0 — равные колонки */
  flex: auto;                   /* flex: 1 1 auto */
  flex: none;                   /* flex: 0 0 auto — жёсткий размер */
  flex: 2;                      /* в два раза больше, чем flex: 1 */

  /* Индивидуальное выравнивание (переопределяет align-items) */
  align-self: auto;
  align-self: flex-start;
  align-self: flex-end;
  align-self: center;
  align-self: stretch;
  align-self: baseline;
}
```

### 6.2 Рецепты Flexbox

```css
/* ─── Центрирование (классическое) ─── */
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ─── Прилипающий футер ─── */
body {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}
main { flex: 1; }

/* ─── Навигационная панель ─── */
.navbar {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}
.navbar .logo { margin-inline-end: auto; } /* или: */
.navbar .spacer { flex: 1; }

/* ─── Карточка с футером внизу ─── */
.card {
  display: flex;
  flex-direction: column;
}
.card__body { flex: 1; }
/* .card__footer всегда внизу */

/* ─── Равные колонки любой ширины ─── */
.columns {
  display: flex;
  gap: var(--space-4);
}
.columns > * { flex: 1 1 0; }

/* ─── Ряд с переносом (auto-fill поведение) ─── */
.wrap-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.wrap-row > * {
  flex: 1 1 200px;  /* grow shrink basis: минимум 200px */
}

/* ─── Иконка + текст ─── */
.icon-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
}

/* ─── Медиа-объект ─── */
.media {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
}
.media__image { flex-shrink: 0; }
.media__body  { flex: 1; min-width: 0; } /* min-width: 0 важно! */
```

### 6.3 Частые ошибки Flexbox

```css
/* ❌ Текст не обрезается в flex-item */
.flex-item { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
/* ✅ Нужен min-width: 0 на родителе! */
.flex-parent { display: flex; }
.flex-item   { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* ❌ Все элементы одинаковой высоты неожиданно */
/* Причина: align-items: stretch (по умолчанию) */
/* ✅ Если не нужно: */
.flex { align-items: flex-start; }

/* ❌ flex: 1 не работает как ожидается */
/* flex: 1 = flex: 1 1 0 (basis=0, игнорирует содержимое) */
/* flex: auto = flex: 1 1 auto (basis=auto, учитывает содержимое) */
```

---

## 7. CSS GRID

### 7.1 Полный справочник свойств

```css
/* ─── КОНТЕЙНЕР (grid container) ─── */
.grid-container {
  display: grid;                /* или inline-grid */

  /* Определение колонок */
  grid-template-columns: 200px 1fr 200px;
  grid-template-columns: repeat(3, 1fr);
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-template-columns: [start] 1fr [middle] 2fr [end];  /* именованные линии */

  /* Определение рядов */
  grid-template-rows: auto 1fr auto;
  grid-template-rows: repeat(3, minmax(100px, auto));

  /* Именованные области */
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";

  /* Шортхенд: rows / columns */
  grid-template: auto 1fr auto / 200px 1fr;

  /* Неявные треки (для элементов вне grid-template) */
  grid-auto-rows: minmax(100px, auto);
  grid-auto-columns: 200px;
  grid-auto-flow: row;          /* куда помещать новые элементы */
  grid-auto-flow: column;
  grid-auto-flow: row dense;    /* плотная упаковка */

  /* Полный шортхенд grid */
  grid: "header" auto
        "main"   1fr
        "footer" auto
        / 1fr;

  /* Отступы */
  gap: 1rem;
  gap: 1rem 2rem;
  row-gap: 1rem;
  column-gap: 2rem;

  /* Выравнивание треков в контейнере */
  justify-content: start | end | center | stretch | space-between | space-around | space-evenly;
  align-content: start | end | center | stretch | space-between | space-around | space-evenly;
  place-content: center;        /* align-content justify-content */

  /* Выравнивание элементов внутри ячеек */
  justify-items: start | end | center | stretch;
  align-items: start | end | center | stretch | baseline;
  place-items: center;          /* align-items justify-items */
}

/* ─── ЭЛЕМЕНТ (grid item) ─── */
.grid-item {
  /* Размещение по линиям */
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row-start: 1;
  grid-row-end: 2;

  /* Шортхенды */
  grid-column: 1 / 3;          /* start / end */
  grid-column: 1 / span 2;     /* start / через сколько */
  grid-column: span 2;          /* через сколько (auto start) */
  grid-column: 1 / -1;         /* на всю ширину */
  grid-row: 1 / 3;

  /* По именованным областям */
  grid-area: header;
  grid-area: 1 / 1 / 2 / 4;   /* row-start col-start row-end col-end */

  /* Индивидуальное выравнивание */
  justify-self: start | end | center | stretch;
  align-self: start | end | center | stretch;
  place-self: center;
}
```

### 7.2 Ключевые функции Grid

```css
/* ─── repeat() ─── */
grid-template-columns: repeat(4, 1fr);
grid-template-columns: repeat(4, 200px 1fr);      /* чередование */
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));

/* auto-fit vs auto-fill:
   auto-fill: создаёт пустые треки, если элементов мало
   auto-fit: сжимает пустые треки до 0, элементы растягиваются */

/* ─── minmax() ─── */
minmax(100px, 1fr)       /* min=100px, max=1fr */
minmax(auto, 200px)      /* min=auto(содержимое), max=200px */
minmax(min-content, 1fr) /* min по содержимому */
minmax(0, 1fr)           /* явный 0 для равного деления */

/* ─── fit-content() ─── */
grid-template-columns: fit-content(200px) 1fr;
/* Колонка растёт по содержимому, но не больше 200px */

/* ─── Именованные линии ─── */
.grid {
  grid-template-columns:
    [full-start] minmax(1rem, 1fr)
    [content-start] minmax(0, 60rem) [content-end]
    minmax(1rem, 1fr) [full-end];
}
.full-width { grid-column: full-start / full-end; }
.content    { grid-column: content-start / content-end; }
```

### 7.3 Рецепты Grid

```css
/* ─── Holy Grail Layout ─── */
.holy-grail {
  display: grid;
  grid-template:
    "header"  auto
    "nav"     auto
    "main"    1fr
    "sidebar" auto
    "footer"  auto
    / 1fr;
  min-height: 100dvh;
}

@media (min-width: 768px) {
  .holy-grail {
    grid-template:
      "header  header  header"  auto
      "nav     main    sidebar" 1fr
      "footer  footer  footer"  auto
      / 200px  1fr     200px;
  }
}

header  { grid-area: header;  }
nav     { grid-area: nav;     }
main    { grid-area: main;    }
aside   { grid-area: sidebar; }
footer  { grid-area: footer;  }

/* ─── Адаптивная карточная сетка ─── */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: var(--space-6);
}

/* ─── Маснори-подобная сетка ─── */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-rows: 10px;
  gap: 10px;
}
/* JS устанавливает grid-row-end для каждой карточки */
/* CSS masonry (экспериментально, пока в Firefox флаг) */
.masonry-native {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: masonry;
}

/* ─── Рамка-сетка (magazine layout) ─── */
.magazine {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
}
.featured  { grid-column: span 4; grid-row: span 2; }
.secondary { grid-column: span 2; }

/* ─── Центрирование через Grid ─── */
.grid-center {
  display: grid;
  place-items: center;
  /* или */
  align-items: center;
  justify-items: center;
}

/* ─── Полноэкранный раздел с контентом по центру ─── */
.section {
  display: grid;
  place-content: center;
  min-height: 100dvh;
  padding: var(--space-8);
}
```

---

## 8. SUBGRID

### 8.1 Что такое Subgrid и зачем нужен

```css
/* Проблема без subgrid: дети не выровнены по родительской сетке */
.grid-parent {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
.card {
  /* Карточка занимает 1 колонку родителя.
     Внутри карточки своя сетка, не связанная с родителем. */
  display: grid;
  grid-template-rows: auto 1fr auto; /* header, body, footer */
}
/* Проблема: разные карточки имеют разную высоту header/body/footer */

/* ✅ Решение: subgrid */
.grid-parent {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr auto;  /* строки для subgrid */
  gap: 1rem;
}
.card {
  grid-row: span 3;           /* занять 3 строки */
  display: grid;
  grid-template-rows: subgrid; /* наследовать строки родителя */
}
/* Теперь header/body/footer всех карточек выровнены! */
```

### 8.2 Примеры использования Subgrid

```css
/* ─── Карточки с выровненными секциями ─── */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-template-rows: auto;
  gap: 1.5rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;             /* header + body + footer */
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.card__header { padding: 1rem; background: var(--color-bg-subtle); }
.card__body   { padding: 1rem; }
.card__footer { padding: 1rem; border-top: 1px solid var(--color-border); }

/* ─── Subgrid по колонкам ─── */
.form-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem 1rem;
}
.form-row {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
}
```

---

## 9. ПОЗИЦИОНИРОВАНИЕ

### 9.1 Значения position

```css
/* static — нормальный поток (по умолчанию) */
.static { position: static; } /* top/left/z-index не работают */

/* relative — смещение от нормального места (место сохраняется) */
.relative {
  position: relative;
  top: 10px;     /* смещение вниз */
  left: 20px;    /* смещение вправо */
  z-index: 1;    /* работает */
}

/* absolute — вырван из потока, позиция от ближайшего positioned предка */
.absolute {
  position: absolute;
  top: 0;
  right: 0;
  /* Если нет positioned предка — от <html> */
}

/* fixed — фиксированный относительно viewport */
.fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  /* Проблема: fixed внутри transform/filter/perspective ломается */
}

/* sticky — гибридное: relative пока не достигнет threshold, потом fixed */
.sticky {
  position: sticky;
  top: 0;          /* пороговое значение */
  /* Работает только если родитель выше viewport */
  /* Требует overflow: visible на всех предках */
}
```

### 9.2 Частые паттерны позиционирования

```css
/* ─── Оверлей поверх элемента ─── */
.parent { position: relative; }
.overlay {
  position: absolute;
  inset: 0;                /* top:0 right:0 bottom:0 left:0 */
  background: rgb(0 0 0 / 0.5);
}

/* inset — логический шортхенд */
inset: 0              /* все стороны 0 */
inset: 1rem           /* все стороны 1rem */
inset: 1rem 2rem      /* block: 1rem, inline: 2rem */
inset-block: 1rem;    /* top и bottom */
inset-inline: 1rem;   /* left и right */

/* ─── Бейдж/нотификация ─── */
.parent {
  position: relative;
  display: inline-block;
}
.badge {
  position: absolute;
  top: -0.5rem;
  right: -0.5rem;
  min-width: 1.25rem;
  height: 1.25rem;
  background: red;
  border-radius: 9999px;
  font-size: 0.75rem;
  display: grid;
  place-items: center;
}

/* ─── Абсолютное центрирование ─── */
/* Способ 1: transform */
.centered-absolute {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
/* Способ 2: inset + margin */
.centered-absolute {
  position: absolute;
  inset: 0;
  width: fit-content;
  height: fit-content;
  margin: auto;
}

/* ─── Sticky заголовок ─── */
.header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: var(--color-bg);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-sm);
}

/* ─── Sticky боковая панель ─── */
.sidebar-sticky {
  position: sticky;
  top: calc(var(--header-height) + 1rem);
  max-height: calc(100vh - var(--header-height) - 2rem);
  overflow-y: auto;
}
```

### 9.3 z-index и stacking contexts

```css
/* Stacking context создаётся при:
   - position: relative/absolute/fixed/sticky + z-index не auto
   - opacity < 1
   - transform (любое значение кроме none)
   - filter, backdrop-filter
   - will-change
   - isolation: isolate ← явное создание
   - mix-blend-mode (не normal)
*/

/* ✅ Изолировать stacking context */
.modal-container {
  isolation: isolate; /* Всё внутри имеет свой stacking context */
}

/* ✅ Избегай произвольных z-index */
/* Используй переменные из системы токенов */
.dropdown { z-index: var(--z-dropdown); }
.modal    { z-index: var(--z-modal); }
.tooltip  { z-index: var(--z-tooltip); }
```

---

## 10. ТИПОГРАФИКА

### 10.1 Шрифты

```css
/* ─── Подключение шрифтов ─── */
@font-face {
  font-family: 'CustomFont';
  src:
    url('font.woff2') format('woff2'),     /* только woff2 нужен в 2024 */
    url('font.woff') format('woff');       /* фолбэк для IE11 (если нужен) */
  font-weight: 400;
  font-style: normal;
  font-display: swap;                      /* ОБЯЗАТЕЛЬНО для производительности */
  unicode-range: U+0000-00FF, U+0131;     /* Подмножество символов */
}

/* Вариативные шрифты */
@font-face {
  font-family: 'VariableFont';
  src: url('font-variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal oblique 0deg 20deg;
  font-display: swap;
}

/* Использование вариативных шрифтов */
.text {
  font-family: 'VariableFont', sans-serif;
  font-weight: 350;                        /* Любое значение 100-900 */
  font-variation-settings:
    'wght' 350,                            /* weight */
    'wdth' 100,                            /* width */
    'slnt' -10,                            /* slant */
    'opsz' 16;                             /* optical size */
}
```

### 10.2 Типографические свойства

```css
.typography {
  /* Гарнитура */
  font-family: var(--font-sans);

  /* Размер */
  font-size: var(--font-size-base);
  font-size: clamp(1rem, 2.5vw, 1.5rem);  /* fluid */

  /* Насыщенность */
  font-weight: 400;
  font-weight: var(--font-weight-bold);

  /* Начертание */
  font-style: normal;
  font-style: italic;
  font-style: oblique 15deg;

  /* Межстрочный интервал */
  line-height: 1.5;
  line-height: var(--line-height-relaxed);

  /* Межбуквенный интервал */
  letter-spacing: 0.05em;      /* em = относительно font-size */
  letter-spacing: -0.02em;     /* для больших заголовков */

  /* Межсловный интервал */
  word-spacing: 0.1em;

  /* Трансформация */
  text-transform: uppercase;
  text-transform: lowercase;
  text-transform: capitalize;
  text-transform: none;

  /* Декорация */
  text-decoration: none;
  text-decoration: underline;
  text-decoration: underline dotted;
  text-decoration: underline wavy var(--color-danger-500);
  text-decoration-thickness: 2px;
  text-underline-offset: 0.2em;  /* Отступ подчёркивания от текста */

  /* Выравнивание */
  text-align: left | right | center | justify | start | end;

  /* Отступ первой строки */
  text-indent: 2em;

  /* Переносы и пробелы */
  white-space: normal | nowrap | pre | pre-wrap | pre-line | break-spaces;
  word-break: normal | break-all | keep-all | break-word;
  overflow-wrap: normal | break-word | anywhere;
  hyphens: none | manual | auto;
  -webkit-hyphens: auto; /* Safari */

  /* Оптимизация рендеринга */
  text-rendering: optimizeLegibility;   /* kerning и лигатуры */
  -webkit-font-smoothing: antialiased;  /* macOS/iOS */
  -moz-osx-font-smoothing: grayscale;   /* Firefox macOS */
  font-smooth: always;

  /* OpenType фичи */
  font-feature-settings: 'liga' 1, 'kern' 1, 'tnum' 1;
  font-variant-numeric: tabular-nums;   /* цифры одинаковой ширины */
  font-variant-numeric: oldstyle-nums;  /* старостильные цифры */
  font-variant-ligatures: common-ligatures;
  font-variant-caps: small-caps;

  /* Тень */
  text-shadow: 2px 2px 4px rgb(0 0 0 / 0.3);
  text-shadow:
    0 0 10px var(--color-accent),
    0 0 20px var(--color-accent);  /* Glow эффект */

  /* Выделение (selection) */
  user-select: none | text | auto | all;
}
```

### 10.3 Обрезка текста

```css
/* ─── Однострочное обрезание ─── */
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  /* Работает ТОЛЬКО с известной шириной! */
}

/* ─── Многострочное обрезание ─── */
.clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* Стандарт (пока draft): */
  line-clamp: 3;
}

/* ─── Обрезание с градиентом ─── */
.fade-out {
  max-height: 4.5em;          /* 3 строки */
  overflow: hidden;
  position: relative;
}
.fade-out::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2em;
  background: linear-gradient(to bottom, transparent, var(--color-bg));
}
```

### 10.4 Система типографики (Type Scale)

```css
/* Модульная шкала (Major Third = 1.25) */
:root {
  --step--2: clamp(0.56rem,   calc(0.54rem + 0.11vw), 0.64rem);
  --step--1: clamp(0.70rem,   calc(0.66rem + 0.21vw), 0.80rem);
  --step-0:  clamp(0.88rem,   calc(0.82rem + 0.32vw), 1.00rem);
  --step-1:  clamp(1.09rem,   calc(1.01rem + 0.42vw), 1.25rem);
  --step-2:  clamp(1.37rem,   calc(1.24rem + 0.65vw), 1.56rem);
  --step-3:  clamp(1.71rem,   calc(1.52rem + 0.97vw), 1.95rem);
  --step-4:  clamp(2.14rem,   calc(1.86rem + 1.41vw), 2.44rem);
  --step-5:  clamp(2.67rem,   calc(2.27rem + 2.02vw), 3.05rem);
}

/* Применение */
h1 { font-size: var(--step-5); line-height: var(--line-height-tight); }
h2 { font-size: var(--step-4); line-height: var(--line-height-tight); }
h3 { font-size: var(--step-3); line-height: var(--line-height-snug); }
h4 { font-size: var(--step-2); line-height: var(--line-height-snug); }
h5 { font-size: var(--step-1); }
h6 { font-size: var(--step-0); }
small { font-size: var(--step--1); }
```

### 10.5 Ширина текста и читабельность

```css
/* ─── Оптимальная длина строки ─── */
.prose {
  max-width: 65ch;          /* ch = ширина '0' */
  /* 45-75 символов в строке — оптимально */
}

/* ─── Колонки текста ─── */
.multi-column {
  column-count: 3;
  column-width: 200px;       /* auto-fill */
  column-gap: 2rem;
  column-rule: 1px solid var(--color-border);
  orphans: 3;                /* минимум строк внизу страницы */
  widows: 3;                 /* минимум строк вверху страницы */
}
.no-break { break-inside: avoid; } /* не разрывать элемент */

/* ─── balance и pretty (новые) ─── */
h1, h2, h3 {
  text-wrap: balance;        /* Равномерно распределить строки заголовка */
}
p {
  text-wrap: pretty;         /* Избежать висячих слов (orphan) */
}
```

---

## 11. ЦВЕТ И ГРАДИЕНТЫ

### 11.1 Современные цветовые пространства

```css
/* ─── RGB / RGBA (старый, но надёжный) ─── */
color: rgb(255 0 0);                /* без запятых — новый синтаксис */
color: rgb(255 0 0 / 0.5);         /* с прозрачностью */
color: rgba(255, 0, 0, 0.5);       /* старый синтаксис */

/* ─── HEX ─── */
color: #ff0000;
color: #ff0000aa;  /* с прозрачностью */
color: #f00;       /* короткая форма */

/* ─── HSL — лучший для человека ─── */
color: hsl(0 100% 50%);             /* красный */
color: hsl(220 90% 56%);            /* синий */
color: hsl(220 90% 56% / 0.5);     /* с прозрачностью */

/* ─── HWB (Hue White Black) ─── */
color: hwb(0 0% 0%);               /* красный */

/* ─── oklch — лучший для программной работы ─── */
color: oklch(0.7 0.15 250);        /* L C H */
/* L: яркость 0-1, C: насыщенность 0-0.4, H: оттенок 0-360 */
color: oklch(0.7 0.15 250 / 0.5); /* с прозрачностью */

/* oklch для последовательной палитры */
:root {
  --brand-hue: 250;
  --brand-chroma: 0.15;

  --color-50:  oklch(0.97 calc(var(--brand-chroma) * 0.3) var(--brand-hue));
  --color-100: oklch(0.93 calc(var(--brand-chroma) * 0.5) var(--brand-hue));
  --color-200: oklch(0.87 calc(var(--brand-chroma) * 0.7) var(--brand-hue));
  --color-500: oklch(0.65 var(--brand-chroma) var(--brand-hue));
  --color-700: oklch(0.50 var(--brand-chroma) var(--brand-hue));
  --color-900: oklch(0.25 calc(var(--brand-chroma) * 0.6) var(--brand-hue));
}

/* ─── color() — профессиональные пространства ─── */
color: color(display-p3 0.5 0.3 0.8);      /* P3 цветовое пространство */
color: color(rec2020 0.5 0.3 0.8);
color: color(sRGB 0.5 0.3 0.8);

/* ─── Wide gamut с фолбэком ─── */
.vivid {
  color: oklch(0.7 0.35 140);  /* яркий зелёный */
}
@supports (color: color(display-p3 0 0 0)) {
  .vivid { color: color(display-p3 0.1 0.8 0.2); }
}

/* ─── currentColor — наследование цвета ─── */
.icon {
  color: currentColor;           /* = цвет текста родителя */
  fill: currentColor;            /* для SVG */
  border-color: currentColor;
}

/* ─── color-mix() ─── */
color: color-mix(in oklch, var(--color-primary) 70%, white);
color: color-mix(in srgb, blue, red 30%);
color: color-mix(in hsl, hsl(200 50% 50%) 50%, hsl(300 50% 50%));
```

### 11.2 Градиенты

```css
/* ─── linear-gradient ─── */
background: linear-gradient(to right, red, blue);
background: linear-gradient(90deg, red, blue);
background: linear-gradient(45deg, red 0%, orange 25%, yellow 50%, green 75%, blue 100%);

/* Повторяющийся */
background: repeating-linear-gradient(
  45deg,
  transparent 0px, transparent 10px,
  var(--color-border) 10px, var(--color-border) 11px
);

/* ─── radial-gradient ─── */
background: radial-gradient(circle, red, blue);
background: radial-gradient(ellipse at center, red, blue);
background: radial-gradient(circle at 20% 80%, #12c2e9, #c471ed, #f64f59);
background: radial-gradient(farthest-corner at 40px 40px, red, blue);

/* ─── conic-gradient ─── */
background: conic-gradient(red, orange, yellow, green, blue, red);
background: conic-gradient(from 0deg at 50% 50%, red 0%, blue 50%, red 100%);

/* Pie chart */
.pie {
  background: conic-gradient(
    var(--color-brand-500) 0%   40%,
    var(--color-success-500) 40% 70%,
    var(--color-warning-500) 70% 100%
  );
  border-radius: 50%;
}

/* ─── Mesh градиент ─── */
.mesh-gradient {
  background:
    radial-gradient(at 40% 20%, hsla(28, 100%, 74%, 1)  0px, transparent 50%),
    radial-gradient(at 80% 0%,  hsla(189, 100%, 56%, 1) 0px, transparent 50%),
    radial-gradient(at 0% 50%,  hsla(355, 100%, 93%, 1) 0px, transparent 50%),
    radial-gradient(at 80% 50%, hsla(340, 100%, 76%, 1) 0px, transparent 50%),
    radial-gradient(at 0% 100%, hsla(22, 100%, 77%, 1)  0px, transparent 50%),
    radial-gradient(at 80% 100%,hsla(242, 100%, 70%, 1) 0px, transparent 50%),
    radial-gradient(at 0% 0%,   hsla(343, 100%, 76%, 1) 0px, transparent 50%);
}

/* ─── Многослойные фоны ─── */
.layered {
  background:
    linear-gradient(to right, transparent 70%, white),  /* 1-й слой (сверху) */
    url('noise.png') repeat,                             /* 2-й слой */
    radial-gradient(circle at top right, blue, transparent 60%), /* 3-й */
    #f0f0f0;                                            /* фоновый цвет */
}
```

---

## 12. ФОНЫ, ГРАНИЦЫ, ТЕНИ

### 12.1 Background

```css
.bg {
  background-color: var(--color-bg);
  background-image: url('image.jpg');
  background-size: cover | contain | auto | 100% | 50px 100px;
  background-position: center | top right | 50% 25% | left 20px bottom 10px;
  background-repeat: no-repeat | repeat | repeat-x | repeat-y | space | round;
  background-attachment: scroll | fixed | local;
  background-origin: border-box | padding-box | content-box;
  background-clip: border-box | padding-box | content-box | text;

  /* Шортхенд: color image position/size repeat attachment origin clip */
  background: url('img.jpg') center/cover no-repeat;
}

/* ─── Текстурные паттерны на CSS ─── */
/* Точечная сетка */
.dot-grid {
  background-image: radial-gradient(circle, #d0d0d0 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Линейная сетка */
.line-grid {
  background-image:
    linear-gradient(var(--color-border) 1px, transparent 1px),
    linear-gradient(to right, var(--color-border) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Диагональные полосы */
.diagonal-stripes {
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    rgb(0 0 0 / 0.05) 10px,
    rgb(0 0 0 / 0.05) 20px
  );
}

/* ─── background-clip: text ─── */
.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
```

### 12.2 Border и Outline

```css
.bordered {
  /* Полный синтаксис */
  border: 2px solid var(--color-border);
  border-width: 1px 2px 1px 2px;       /* top right bottom left */
  border-style: solid | dashed | dotted | double | groove | ridge | inset | outset | none;
  border-color: red blue green yellow;

  /* По сторонам */
  border-top: 1px solid red;
  border-block: 1px solid var(--color-border);    /* логические */
  border-inline: 1px solid var(--color-border);
  border-block-start: 2px solid var(--color-accent);

  /* Радиус */
  border-radius: 8px;
  border-radius: 8px 4px 8px 4px;        /* TL TR BR BL */
  border-radius: 8px / 4px;              /* горизонтальный / вертикальный */
  border-top-left-radius: 8px 4px;
  border-start-start-radius: 8px;        /* логические */

  /* Логические свойства */
  border-start-start-radius: var(--radius-lg);
  border-start-end-radius: var(--radius-lg);
  border-end-start-radius: var(--radius-sm);
  border-end-end-radius: var(--radius-sm);

  /* border-image */
  border-image-source: linear-gradient(to right, red, blue);
  border-image-slice: 1;
  border-image: linear-gradient(to right, red, blue) 1;
}

/* Outline (не занимает место, не влияет на layout) */
.outlined {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;   /* отступ от края элемента */
}

/* ─── Продвинутые border-radius ─── */
.blob {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
}
.squircle {
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}
```

### 12.3 Тени

```css
/* box-shadow: x y blur spread color */
.shadow {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  
  /* Многослойные тени */
  box-shadow:
    0 1px 2px rgb(0 0 0 / 0.04),
    0 4px 8px rgb(0 0 0 / 0.04),
    0 16px 32px rgb(0 0 0 / 0.08);
  
  /* Внутренняя тень */
  box-shadow: inset 0 2px 4px rgb(0 0 0 / 0.1);
  
  /* Тени от нескольких сторон */
  box-shadow:
    inset 0 2px 0 rgb(255 255 255 / 0.1),
    inset 0 -2px 0 rgb(0 0 0 / 0.1);

  /* Цветная тень */
  box-shadow: 0 0 20px var(--color-accent);
  
  /* Нейморфизм */
  box-shadow:
    5px 5px 10px #bebebe,
    -5px -5px 10px #ffffff;
}

/* drop-shadow для filter (работает для SVG и clip-path) */
.svg-shadow {
  filter: drop-shadow(0 4px 6px rgb(0 0 0 / 0.3));
}

/* Убрать тень при hover (плавно) */
.card {
  box-shadow: var(--shadow-md);
  transition: box-shadow var(--duration-normal) var(--ease-out);
}
.card:hover {
  box-shadow: var(--shadow-xl);
}
```

---

## 13. ТРАНСФОРМАЦИИ

### 13.1 transform — все функции

```css
.transform {
  /* 2D трансформации */
  transform: translate(50px, 100px);
  transform: translateX(50px);
  transform: translateY(-20px);
  transform: scale(1.2);
  transform: scale(1.5, 0.8);         /* X, Y */
  transform: scaleX(2);
  transform: rotate(45deg);
  transform: rotateZ(45deg);
  transform: skew(10deg, 5deg);
  transform: skewX(10deg);
  transform: matrix(a, b, c, d, tx, ty);

  /* 3D трансформации */
  transform: translate3d(50px, 0, 0);
  transform: translateZ(100px);
  transform: scale3d(1.2, 1.2, 1);
  transform: rotateX(45deg);
  transform: rotateY(45deg);
  transform: rotateZ(45deg);
  transform: rotate3d(1, 1, 0, 45deg);
  transform: perspective(500px) rotateY(30deg);
  transform: matrix3d(/* 16 значений */);

  /* Множественные трансформации (порядок важен!) */
  transform: translateX(50px) rotate(45deg) scale(1.2);
  /* Применяются справа налево: сначала scale, потом rotate, потом translate */

  /* Точка трансформации */
  transform-origin: center;            /* по умолчанию */
  transform-origin: top left;
  transform-origin: 50px 20px;
  transform-origin: 50% 100%;

  /* 3D перспектива */
  perspective: 800px;                  /* на родителе */
  perspective-origin: 50% 50%;
  transform-style: preserve-3d;        /* сохранить 3D для детей */
  backface-visibility: hidden;         /* скрыть обратную сторону */
}

/* Отдельные свойства трансформации (новые) */
.modern-transform {
  translate: 50px 100px;   /* вместо transform: translate() */
  rotate: 45deg;
  scale: 1.2;
  /* Можно анимировать независимо и комбинировать */
}
```

### 13.2 Паттерны трансформаций

```css
/* ─── 3D карточка (переворот) ─── */
.card-3d {
  perspective: 1000px;
}
.card-3d__inner {
  transform-style: preserve-3d;
  transition: transform 0.6s;
  position: relative;
}
.card-3d:hover .card-3d__inner {
  transform: rotateY(180deg);
}
.card-3d__front,
.card-3d__back {
  backface-visibility: hidden;
}
.card-3d__back {
  transform: rotateY(180deg);
  position: absolute;
  inset: 0;
}

/* ─── Параллакс элемент ─── */
.parallax-layer {
  transform: translateZ(calc(var(--depth, 0) * 1px)) scale(calc(1 + var(--depth, 0) * 0.001));
}

/* ─── Эффект наклона (tilt) ─── */
/* Управляется через CSS переменные из JS */
.tilt {
  transform: perspective(500px)
    rotateX(calc(var(--rx, 0) * 1deg))
    rotateY(calc(var(--ry, 0) * 1deg));
  transition: transform 0.1s;
}
```

---

## 14. ПЕРЕХОДЫ (TRANSITIONS)

### 14.1 Синтаксис и свойства

```css
.element {
  /* transition: property duration timing-function delay */
  transition: all 0.2s ease;

  /* Конкретные свойства (ПРЕДПОЧТИТЕЛЬНО — лучше производительность) */
  transition: 
    transform   0.2s var(--ease-out),
    opacity     0.2s var(--ease-out),
    box-shadow  0.2s var(--ease-out);

  /* Раздельно */
  transition-property: transform, opacity;
  transition-duration: 200ms, 300ms;
  transition-timing-function: ease-out, ease-in;
  transition-delay: 0ms, 50ms;
}

/* ─── Функции плавности ─── */
transition-timing-function:
  ease,                               /* slow-fast-slow */
  linear,
  ease-in,                            /* медленное начало */
  ease-out,                           /* медленный конец */
  ease-in-out,
  cubic-bezier(0.34, 1.56, 0.64, 1), /* bounce */
  steps(4, end),                      /* ступенчатый */
  step-start,
  step-end;
```

### 14.2 Что можно и нельзя анимировать

```css
/* ✅ Производительные (GPU) — предпочтительно */
transform: translate(), scale(), rotate()
opacity
filter (частично)
backdrop-filter (частично)

/* ⚠️ Вызывают repaint (но не reflow) */
color, background-color, border-color, outline, box-shadow, text-shadow

/* ❌ Вызывают reflow (перерасчёт layout) — избегать */
width, height, margin, padding, top, left, right, bottom
font-size, line-height

/* ─── Оптимальный hover эффект ─── */
/* ❌ Неоптимально */
.btn:hover { width: 120%; }

/* ✅ Оптимально */
.btn {
  transform: scaleX(1);
  transition: transform 0.2s var(--ease-out);
}
.btn:hover { transform: scaleX(1.1); }
```

### 14.3 Паттерны переходов

```css
/* ─── Появление элемента ─── */
.fade-in {
  opacity: 0;
  transition: opacity 0.3s var(--ease-out);
}
.fade-in.visible { opacity: 1; }

/* ─── Slide + Fade ─── */
.slide-in {
  opacity: 0;
  transform: translateY(20px);
  transition: 
    opacity   0.3s var(--ease-out),
    transform 0.3s var(--ease-out);
}
.slide-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ─── Staggered (ступенчатое) появление ─── */
.item:nth-child(1) { transition-delay: 0ms; }
.item:nth-child(2) { transition-delay: 50ms; }
.item:nth-child(3) { transition-delay: 100ms; }
/* Или через переменную */
.item { transition-delay: calc(var(--index, 0) * 50ms); }

/* ─── Переход View Transition API ─── */
/* CSS для View Transitions */
::view-transition-old(root) {
  animation: fade-out 0.3s ease-out;
}
::view-transition-new(root) {
  animation: fade-in 0.3s ease-in;
}
.hero-image {
  view-transition-name: hero;  /* именованный transition */
}
::view-transition-old(hero),
::view-transition-new(hero) {
  height: 100%;
  object-fit: cover;
}
```

---

## 15. АНИМАЦИИ

### 15.1 @keyframes и animation

```css
/* ─── Определение ─── */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-20px); }
}

/* Сложные кейфреймы с процентами */
@keyframes spinner {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse-scale {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

/* ─── Применение ─── */
.animated {
  /* animation: name duration timing delay iteration direction fill-mode */
  animation: fadeIn 0.3s ease-out;
  
  /* Раздельно */
  animation-name:            fadeIn;
  animation-duration:        0.3s;
  animation-timing-function: ease-out;
  animation-delay:           0ms;
  animation-iteration-count: 1;         /* число или infinite */
  animation-direction:       normal;    /* normal | reverse | alternate | alternate-reverse */
  animation-fill-mode:       both;      /* none | forwards | backwards | both */
  animation-play-state:      running;   /* running | paused */
}

/* ─── Множественные анимации ─── */
.multi-animated {
  animation:
    fadeIn    0.3s ease-out,
    slideUp   0.3s ease-out,
    float     3s ease-in-out infinite;
}
```

### 15.2 Коллекция готовых анимаций

```css
/* ─── Spinner ─── */
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--color-bg-muted);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* ─── Skeleton Loading ─── */
@keyframes skeleton-shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-subtle) 25%,
    var(--color-bg-muted) 50%,
    var(--color-bg-subtle) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
}

/* ─── Pulse ─── */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
.pulse { animation: pulse 2s ease-in-out infinite; }

/* ─── Bounce ─── */
@keyframes bounce {
  0%, 100% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

/* ─── Typewriter ─── */
@keyframes typewriter {
  from { width: 0; }
  to   { width: 100%; }
}
@keyframes blink-cursor {
  50% { border-color: transparent; }
}
.typewriter {
  overflow: hidden;
  border-right: 2px solid var(--color-text);
  white-space: nowrap;
  animation:
    typewriter     3s steps(30) 1 forwards,
    blink-cursor   0.75s step-end infinite;
}

/* ─── Float ─── */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-10px); }
}
.floating { animation: float 3s ease-in-out infinite; }

/* ─── Shake ─── */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
  20%, 40%, 60%, 80%       { transform: translateX(4px); }
}
.shake { animation: shake 0.6s ease-in-out; }

/* ─── Ripple (Material) ─── */
@keyframes ripple {
  to { transform: scale(4); opacity: 0; }
}
.ripple-container { position: relative; overflow: hidden; }
.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgb(255 255 255 / 0.3);
  transform: scale(0);
  animation: ripple 0.6s linear;
  pointer-events: none;
}
```

### 15.3 Анимация с учётом доступности

```css
/* ОБЯЗАТЕЛЬНО: уважай настройки пользователя */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Альтернативный подход — проверка перед применением */
@media (prefers-reduced-motion: no-preference) {
  .animated {
    animation: fadeIn 0.3s ease-out;
  }
}

/* JavaScript для проверки */
/* const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; */
```

---

## 16. АДАПТИВНЫЙ ДИЗАЙН

### 16.1 Mobile-first подход

```css
/* ─── Базовые стили (mobile) ─── */
.component {
  padding: var(--space-4);
  font-size: var(--font-size-base);
}

/* ─── Расширение для больших экранов ─── */
@media (min-width: 640px) {  /* sm */
  .component {
    padding: var(--space-6);
  }
}

@media (min-width: 768px) {  /* md */
  .component {
    display: flex;
    gap: var(--space-6);
  }
}

@media (min-width: 1024px) { /* lg */
  .component {
    padding: var(--space-8);
    font-size: var(--font-size-md);
  }
}

@media (min-width: 1280px) { /* xl */
  /* ... */
}

@media (min-width: 1536px) { /* 2xl */
  /* ... */
}
```

### 16.2 Полный справочник Media Features

```css
/* ─── Размер viewport ─── */
@media (min-width: 768px) { }
@media (max-width: 767px) { }      /* ⚠️ max-width — desktop-first (избегай) */
@media (768px <= width <= 1024px) { } /* Новый диапазонный синтаксис */
@media (width >= 768px) { }

/* ─── Ориентация ─── */
@media (orientation: portrait) { }
@media (orientation: landscape) { }

/* ─── Разрешение / DPR ─── */
@media (min-resolution: 2dppx) { }       /* Retina */
@media (-webkit-min-device-pixel-ratio: 2) { } /* Safari фолбэк */
@media (resolution >= 2dppx) { }

/* ─── Устройство ввода ─── */
@media (hover: hover) { }         /* есть ли мышь (hover) */
@media (hover: none) { }          /* touch-only */
@media (pointer: fine) { }        /* точный указатель (мышь) */
@media (pointer: coarse) { }      /* грубый (палец) */
@media (any-hover: hover) { }     /* есть хоть один hover-девайс */

/* ─── Системные предпочтения ─── */
@media (prefers-color-scheme: dark) { }
@media (prefers-color-scheme: light) { }
@media (prefers-reduced-motion: reduce) { }
@media (prefers-reduced-motion: no-preference) { }
@media (prefers-contrast: more) { }
@media (prefers-contrast: less) { }
@media (prefers-contrast: forced) { }
@media (forced-colors: active) { }      /* Windows High Contrast */
@media (prefers-reduced-data: reduce) { }  /* Экономия трафика (draft) */
@media (prefers-reduced-transparency: reduce) { }

/* ─── Форм-фактор ─── */
@media (display-mode: standalone) { }    /* PWA */
@media (display-mode: fullscreen) { }
@media screen { }
@media print { }

/* ─── Логические операторы ─── */
@media (min-width: 768px) and (max-width: 1024px) { }
@media (max-width: 767px), (min-width: 1280px) { }  /* OR */
@media not (min-width: 768px) { }

/* ─── Диапазонный синтаксис (новый, предпочтительный) ─── */
@media (width >= 768px) { }
@media (768px <= width < 1024px) { }
@media (height > 600px) { }
```

### 16.3 Fluid Design без Media Queries

```css
/* ─── Fluid Typography ─── */
/* clamp(MIN, PREFERRED, MAX) */
html {
  font-size: clamp(100%, 90% + 0.5vw, 125%);
}
h1 { font-size: clamp(2rem, 5vw + 1rem, 5rem); }

/* ─── Fluid Spacing ─── */
.section {
  padding-block: clamp(3rem, 8vw, 8rem);
  padding-inline: clamp(1rem, 5vw, 4rem);
}

/* ─── Fluid Grid без breakpoints ─── */
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 20rem), 1fr));
  gap: clamp(1rem, 3vw, 2rem);
}

/* ─── Адаптивный размер шрифта через viewport ─── */
/* Формула: font-size = minSize + (maxSize - minSize) * ((100vw - minWidth) / (maxWidth - minWidth)) */
p {
  font-size: clamp(
    1rem,
    calc(1rem + (1.25 - 1) * ((100vw - 20rem) / (80 - 20))),
    1.25rem
  );
}
```

### 16.4 Responsive Images

```css
/* ─── Адаптивные изображения ─── */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Изображение-обложка */
.cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  object-position: center;
}

/* Адаптивное соотношение сторон */
.responsive-video {
  aspect-ratio: 16 / 9;
  width: 100%;
}
.responsive-video iframe {
  width: 100%;
  height: 100%;
}

/* ─── Retina изображения через CSS ─── */
.logo {
  background-image: url('logo.png');
  background-size: 100px 50px;
}
@media (min-resolution: 2dppx) {
  .logo { background-image: url('logo@2x.png'); }
}
```

---

## 17. CONTAINER QUERIES

### 17.1 Синтаксис и использование

```css
/* ─── Объявление контейнера ─── */
.card-wrapper {
  container-type: inline-size;  /* только ширина */
  /* container-type: size;       ширина и высота */
  /* container-type: normal;     для style queries */
  container-name: card;          /* необязательное имя */
  
  /* Шортхенд */
  container: card / inline-size;
}

/* ─── Container Query ─── */
@container (min-width: 400px) {
  .card { flex-direction: row; }
}

@container (width >= 600px) {
  .card__image { width: 40%; }
  .card__body  { width: 60%; }
}

/* ─── Именованные контейнеры ─── */
@container card (min-width: 500px) {
  .card__title { font-size: 1.5rem; }
}

/* ─── Диапазоны ─── */
@container (400px <= width < 800px) {
  .card { grid-template-columns: 1fr 1fr; }
}

/* ─── Единицы container ─── */
.card__title {
  font-size: 5cqi;    /* 5% от inline-size контейнера */
  /* cqw: ширина, cqh: высота, cqi: inline, cqb: block */
  /* cqmin: меньшее, cqmax: большее */
  margin: 2cqw;
}
```

### 17.2 Style Container Queries

```css
/* ─── Style Queries (новые, частичная поддержка) ─── */
.theme-wrapper {
  container-type: normal;
  --theme: dark;
}

@container style(--theme: dark) {
  .card {
    background: var(--color-neutral-800);
    color: var(--color-neutral-100);
  }
}

/* Полный пример адаптивного компонента */
.card-container {
  container: card / inline-size;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}

@container card (width >= 400px) {
  .card {
    flex-direction: row;
    padding: 1.5rem;
  }
  .card__image {
    width: 200px;
    flex-shrink: 0;
  }
}

@container card (width >= 700px) {
  .card {
    gap: 2rem;
    padding: 2rem;
  }
  .card__title {
    font-size: 1.5rem;
  }
}
```

---

## 18. CSS FUNCTIONS

### 18.1 Математические функции

```css
/* ─── calc() ─── */
.element {
  width: calc(100% - 2rem);
  height: calc(100vh - 60px);
  padding: calc(var(--space-4) * 2);
  font-size: calc(1rem + 0.5vw);
  /* Вложенные calc */
  margin: calc(calc(var(--space-4) + 10px) * 2);
}

/* ─── clamp(min, preferred, max) ─── */
.fluid {
  font-size: clamp(1rem, 2.5vw, 2rem);
  width: clamp(200px, 50%, 600px);
  padding: clamp(1rem, 5vw, 4rem);
}

/* ─── min() и max() ─── */
.element {
  width: min(100%, 600px);           /* не шире 600px */
  width: max(200px, 50%);            /* не уже 200px */
  font-size: min(5vw, 3rem);
  padding: max(1rem, 3vw);
  
  /* Комбинирование */
  width: min(max(200px, 50%), 800px); /* как clamp(200px, 50%, 800px) */
}

/* ─── round(), rem(), mod() (новые) ─── */
.element {
  width: round(var(--width), 4px);    /* округлить до ближайших 4px */
  padding: rem(17px, 5px);           /* остаток от деления */
  margin: mod(17px, 5px);            /* как rem но сохраняет знак */
}

/* ─── abs() и sign() ─── */
.element {
  width: calc(abs(var(--offset)) * 2);
  transform: translateX(calc(sign(var(--x)) * 10px));
}
```

### 18.2 Функции для форм и путей

```css
/* ─── shape() (будущее, пока не поддерживается) ─── */

/* ─── path() ─── */
.clip {
  clip-path: path('M 0 0 L 100 0 L 100 100 Z');
  offset-path: path('M 0 100 C 50 0 100 200 200 100');
}

/* ─── polygon(), circle(), ellipse() ─── */
.clipped {
  clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
  clip-path: circle(50% at center);
  clip-path: ellipse(60% 40% at 50% 50%);
  clip-path: inset(10px 20px round 10px);
}
```

### 18.3 Функции для цвета

```css
/* ─── color-mix() ─── */
color: color-mix(in oklch, blue 30%, white);
background: color-mix(in srgb, var(--color-accent), transparent 80%);

/* ─── oklch() ─── */
color: oklch(0.7 0.2 250);
/* L: 0-1, C: 0-0.4+, H: 0-360 */

/* ─── light-dark() ─── */
.element {
  color: light-dark(black, white);              /* автоматически по color-scheme */
  background: light-dark(#ffffff, #1a1a1a);
}

/* ─── relative color syntax (новый) ─── */
.element {
  --base: oklch(0.7 0.2 250);
  
  /* Создать осветлённую версию */
  color: oklch(from var(--base) calc(l + 0.1) c h);
  
  /* Изменить насыщенность */
  background: oklch(from var(--base) l calc(c * 0.5) h);
  
  /* Изменить оттенок */
  border-color: oklch(from var(--base) l c calc(h + 30));
  
  /* Из любого формата */
  color: rgb(from var(--base) r calc(g * 0.8) b);
}
```

### 18.4 Прочие функции

```css
/* ─── env() — переменные окружения ─── */
.notched {
  padding-top: env(safe-area-inset-top);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  
  /* С фолбэком */
  padding-bottom: env(safe-area-inset-bottom, 20px);
}

/* ─── var() — уже описана в разделе 4 ─── */

/* ─── attr() ─── */
/* Стандартно — только в content */
.tooltip::after {
  content: attr(data-tooltip);
}
/* В будущем — в любом свойстве (draft) */
.element {
  width: attr(data-width px);
}

/* ─── counter() и counters() ─── */
ol {
  counter-reset: item;
}
ol li {
  counter-increment: item;
}
ol li::before {
  content: counter(item) '. ';
  content: counters(item, '.') ' '; /* вложенные: 1.2.3 */
}

/* ─── url() ─── */
background-image: url('image.jpg');
background-image: url("data:image/svg+xml,...");

/* ─── image-set() — адаптивные фоны ─── */
background-image: image-set(
  url('image.avif') type('image/avif'),
  url('image.webp') type('image/webp'),
  url('image.jpg')  1x,
  url('image@2x.jpg') 2x
);
```

---

## 19. ПСЕВДОКЛАССЫ И ПСЕВДОЭЛЕМЕНТЫ

### 19.1 Псевдоклассы — полный список

```css
/* ─── Ссылки и взаимодействие ─── */
:link     { }  /* непосещённые ссылки */
:visited  { }  /* посещённые */
:hover    { }  /* при наведении */
:active   { }  /* при нажатии */
:focus    { }  /* фокус (клавиатура/кнопка) */
:focus-visible { }  /* фокус ТОЛЬКО от клавиатуры (не мыши) */
:focus-within  { }  /* имеет потомка в фокусе */

/* ПОРЯДОК для ссылок: LVHA (или LVFHA) */
a:link, a:visited, a:focus, a:hover, a:active { }

/* ─── Структурные ─── */
:root              { }  /* <html> */
:empty             { }  /* нет детей */
:first-child       { }  /* первый ребёнок родителя */
:last-child        { }  /* последний */
:only-child        { }  /* единственный */
:nth-child(n)      { }
:nth-last-child(n) { }
:first-of-type     { }  /* первый своего типа тега */
:last-of-type      { }
:only-of-type      { }
:nth-of-type(n)    { }
:nth-last-of-type(n){ }

/* nth-child паттерны */
:nth-child(odd)     { }  /* нечётные */
:nth-child(even)    { }  /* чётные */
:nth-child(3n)      { }  /* каждый 3-й */
:nth-child(3n+1)    { }  /* 1-й, 4-й, 7-й... */
:nth-child(-n+3)    { }  /* первые 3 */
:nth-child(n+4)     { }  /* начиная с 4-го */

/* Новый синтаксис с аргументом (Selectors Level 4) */
:nth-child(2n of .featured) { }  /* каждый 2-й .featured */

/* ─── Формы ─── */
:checked        { }  /* checkbox/radio отмечен */
:indeterminate  { }  /* checkbox в промежуточном состоянии */
:valid          { }  /* валидное поле */
:invalid        { }  /* невалидное */
:in-range       { }  /* в диапазоне min/max */
:out-of-range   { }
:required       { }  /* обязательное */
:optional       { }  /* необязательное */
:disabled       { }  /* отключённое */
:enabled        { }
:read-only      { }  /* readonly */
:read-write     { }  /* редактируемое */
:placeholder-shown { } /* placeholder отображается */
:default        { }  /* дефолтный submit/option */
:autofill       { }  /* заполнено автозаполнением */
:user-valid     { }  /* валидное ПОСЛЕ взаимодействия (новое) */
:user-invalid   { }  /* невалидное после взаимодействия */

/* ─── Функциональные ─── */
:is(h1, h2, h3)         { }  /* любой из списка */
:not(.excluded)         { }  /* исключение */
:not(:first-child, .special) { }  /* сложное исключение */
:where(.class, #id)     { }  /* как :is() но нулевая специфичность */
:has(img)               { }  /* содержит img */
:has(+ .next)           { }  /* есть следующий сиблинг .next */
:has(~ .later)          { }  /* есть последующий сиблинг */

/* ─── Состояния ─── */
:target         { }  /* якорный элемент (из URL #id) */
:scope          { }  /* элемент применения (в компонентах) */
:any-link       { }  /* все ссылки (с href) */
:local-link     { }  /* ссылки на текущий домен */
:global         { }

/* ─── Специальные ─── */
:fullscreen     { }  /* в режиме fullscreen */
:modal          { }  /* элемент <dialog> */
:popover-open   { }  /* открытый popover */
:playing        { }  /* воспроизводится (media) */
:paused         { }  /* на паузе */
:lang(ru)       { }  /* по языку */
:dir(ltr)       { }  /* по направлению текста */
:defined        { }  /* зарегистрированный Web Component */
:host           { }  /* Shadow DOM хост */
:host(.theme-dark) { }
```

### 19.2 Псевдоэлементы

```css
/* ─── Классические ─── */
::before        { content: ''; }   /* до содержимого */
::after         { content: ''; }   /* после содержимого */
::first-line    { }                /* первая строка */
::first-letter  { }                /* первая буква */
::selection     { }                /* выделенный текст */
::marker        { }                /* маркер списка */
::placeholder   { }                /* плейсхолдер input */

/* ─── Новые ─── */
::backdrop          { }  /* фон за <dialog> и fullscreen */
::cue               { }  /* субтитры WebVTT */
::part(name)        { }  /* Shadow DOM части */
::slotted(selector) { }  /* слотированное содержимое */
::file-selector-button { } /* кнопка input[type=file] */
::spelling-error    { }  /* орфографическая ошибка */
::grammar-error     { }  /* грамматическая ошибка */
::target-text       { }  /* прокруткой к тексту */
::view-transition   { }  /* контейнер перехода */
::view-transition-old(name) { }
::view-transition-new(name) { }
::scroll-marker     { }  /* (draft) */
::column            { }  /* (draft) */

/* ─── Скроллбар (нестандартные WebKit) ─── */
::-webkit-scrollbar           { width: 8px; }
::-webkit-scrollbar-track     { background: transparent; }
::-webkit-scrollbar-thumb     { background: var(--color-border-strong); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
::-webkit-scrollbar-corner    { background: transparent; }
```

### 19.3 Практические примеры

```css
/* ─── Декоративный ::before / ::after ─── */
.section-title {
  position: relative;
  padding-block-end: 0.5rem;
}
.section-title::after {
  content: '';
  position: absolute;
  inset-inline-start: 0;
  inset-block-end: 0;
  width: 3rem;
  height: 3px;
  background: var(--color-accent);
  border-radius: 9999px;
}

/* ─── Счётчик ─── */
.numbered-list {
  counter-reset: my-counter;
}
.numbered-list__item {
  counter-increment: my-counter;
}
.numbered-list__item::before {
  content: counter(my-counter, decimal-leading-zero);
  font-size: 0.75em;
  font-weight: bold;
  color: var(--color-accent);
}

/* ─── Кавычки ─── */
blockquote::before { content: '\201C'; }  /* " */
blockquote::after  { content: '\201D'; }  /* " */

/* ─── Маркер списка ─── */
li::marker {
  color: var(--color-accent);
  font-size: 0.8em;
}

/* ─── :has() — Родительский селектор ─── */
/* Форма с ошибкой */
.field:has(input:invalid) .field__label { color: var(--color-danger-500); }
.field:has(input:focus) .field__label   { color: var(--color-accent); }

/* Карточка с изображением (другой layout) */
.card:has(> .card__image) {
  grid-template-columns: 200px 1fr;
}

/* Навигация — активный пункт */
.nav:has(.nav__link[aria-current="page"]) { /* nav содержит активную ссылку */ }

/* ─── :focus-visible (предпочтительный) ─── */
/* Убрать outline для мыши, оставить для клавиатуры */
:focus { outline: none; }             /* убрать всем */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* ─── :user-valid / :user-invalid ─── */
input:user-invalid {
  border-color: var(--color-danger-500);
  background: var(--color-danger-100);
}
input:user-valid {
  border-color: var(--color-success-500);
}
```

---

## 20. ЛОГИЧЕСКИЕ СВОЙСТВА

### 20.1 Таблица соответствия физических → логических

```css
/* ─── Физическое → Логическое ─── */

/* Размеры */
width         → inline-size
height        → block-size
min-width     → min-inline-size
max-width     → max-inline-size
min-height    → min-block-size
max-height    → max-block-size

/* Отступы */
margin-top    → margin-block-start
margin-bottom → margin-block-end
margin-left   → margin-inline-start
margin-right  → margin-inline-end
margin-top + margin-bottom  → margin-block
margin-left + margin-right  → margin-inline

padding-top    → padding-block-start
padding-bottom → padding-block-end
padding-left   → padding-inline-start
padding-right  → padding-inline-end
padding-top + padding-bottom  → padding-block
padding-left + padding-right  → padding-inline

/* Позиционирование */
top    → inset-block-start
bottom → inset-block-end
left   → inset-inline-start
right  → inset-inline-end

/* Границы */
border-top    → border-block-start
border-bottom → border-block-end
border-left   → border-inline-start
border-right  → border-inline-end

border-top-left-radius     → border-start-start-radius
border-top-right-radius    → border-start-end-radius
border-bottom-left-radius  → border-end-start-radius
border-bottom-right-radius → border-end-end-radius

/* Прочее */
float: left   → float: inline-start
float: right  → float: inline-end
text-align: left  → text-align: start
text-align: right → text-align: end
resize: horizontal → resize: inline
resize: vertical   → resize: block
```

### 20.2 Когда использовать логические свойства

```css
/* ВСЕГДА используй логические для: */
/* - Блочных отступов (вертикальных в ltr) */
.spacing {
  margin-block: var(--space-4);
  padding-block: var(--space-6);
}

/* - Центрирования по горизонтали */
.centered {
  margin-inline: auto;
}

/* - Компонентов, которые могут быть в RTL */
.component {
  padding-inline: var(--space-4);
  border-inline-start: 2px solid var(--color-accent);
  text-align: start;
}

/* Физические свойства OK для: */
/* - Декоративных эффектов без семантики направления */
/* - Когда direction точно ltr */
.decorative {
  border-bottom: 2px solid red;  /* OK: декоративный низ */
  border-left: 5px solid green;  /* Лучше: border-inline-start */
}
```

---

## 21. CSS LAYERS

### 21.1 Синтаксис @layer

```css
/* ─── Объявление порядка слоёв (ВНАЧАЛЕ файла) ─── */
@layer reset, tokens, base, components, utilities;

/* Правила внутри слоёв */
@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  * { margin: 0; padding: 0; }
}

@layer base {
  body { font-family: var(--font-sans); }
  a { color: var(--color-accent); }
}

@layer components {
  .btn { /* стили кнопки */ }
}

@layer utilities {
  .sr-only { /* утилиты */ }
}

/* ─── Вложенные слои ─── */
@layer components {
  @layer base {
    .btn { padding: 0.5rem 1rem; }
  }
  @layer theme {
    .btn { background: var(--color-accent); }
  }
  /* components.base < components.theme < components (без слоя) */
}

/* ─── Безымянный слой ─── */
@layer {
  /* Анонимный слой — нельзя добавить позже */
  .anon { color: red; }
}

/* ─── Импорт в слой ─── */
@import url('reset.css') layer(reset);
@import url('components.css') layer(components);
```

### 21.2 Стратегия слоёв для проекта

```css
/* Порядок от низшего к высшему приоритету */
@layer
  reset,       /* CSS Reset, normalize */
  tokens,      /* CSS переменные */
  base,        /* базовые HTML стили */
  layout,      /* сетки, контейнеры */
  components,  /* UI компоненты */
  patterns,    /* комбинации компонентов */
  utilities,   /* утилитарные классы */
  overrides;   /* специальные переопределения */

/* Важное: styles вне @layer ВСЕГДА выше любого @layer */
/* Поэтому помещай всё в @layer */

@layer overrides {
  /* Специфические исправления — высший приоритет среди слоёв */
  .dark-theme .btn { background: #333; }
}
```

---

## 22. CSS NESTING

### 22.1 Нативный CSS Nesting (не SASS)

```css
/* ─── Базовый нестинг ─── */
.card {
  padding: 1rem;
  border-radius: var(--radius-lg);

  /* Вложенный потомок (НУЖЕН & или пространство имён) */
  .card__header {
    font-size: 1.25rem;
    font-weight: bold;
  }

  .card__body {
    color: var(--color-text-muted);
  }

  /* Псевдоклассы */
  &:hover {
    box-shadow: var(--shadow-lg);
  }

  &:focus-within {
    outline: 2px solid var(--color-accent);
  }

  /* Псевдоэлементы */
  &::before {
    content: '';
  }

  /* Медиазапросы внутри! */
  @media (min-width: 768px) {
    padding: 2rem;
    display: flex;
  }

  /* Container query внутри */
  @container (width >= 400px) {
    flex-direction: row;
  }

  /* Модификаторы (как BEM модификаторы) */
  &.card--featured {
    border: 2px solid var(--color-accent);
  }

  /* Сиблинги */
  & + & {
    margin-block-start: 1rem;
  }

  /* Родительский контекст */
  .dark-theme & {
    background: var(--color-neutral-800);
  }
}
```

### 22.2 Нюансы нативного нестинга

```css
/* ─── & всегда обязателен для элементных селекторов ─── */
.parent {
  /* ✅ Работает (с &) */
  & span { color: red; }
  & p { margin: 0; }

  /* ✅ Работает (с именем класса без &) */
  .child { color: blue; }

  /* ❌ НЕ работает без & для тегов (в старых реализациях) */
  span { color: red; } /* может не работать */
}

/* ─── Вложенность @supports ─── */
.feature {
  display: flex;

  @supports (display: grid) {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ─── Ограничения нестинга ─── */
/* Нельзя вкладывать @font-face, @keyframes, @layer вне @layer */
/* Можно вкладывать только @media, @supports, @container, @layer */
```

---

## 23. SCROLL

### 23.1 Scroll Snap

```css
/* ─── Контейнер прокрутки ─── */
.scroll-container {
  overflow-x: scroll;             /* или auto */
  scroll-snap-type: x mandatory;  /* ось snap + строгость */
  /* x: горизонтальный, y: вертикальный, both: оба */
  /* mandatory: строгий snap, proximity: мягкий */
  
  scroll-behavior: smooth;        /* плавная прокрутка */
  overscroll-behavior-x: contain; /* не передавать прокрутку родителю */
}

/* ─── Элементы внутри ─── */
.scroll-item {
  scroll-snap-align: start;    /* start | center | end */
  scroll-snap-stop: always;    /* normal | always — нельзя пропустить */
  scroll-margin: 1rem;         /* отступ при snap */
  scroll-margin-block-start: 80px; /* отступ для sticky header */
}

/* ─── Горизонтальный слайдер ─── */
.slider {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding: 1rem;        /* отступ snap-point от края контейнера */
  gap: 1rem;
  padding: 1rem;
  -webkit-overflow-scrolling: touch;
}
.slide {
  flex: 0 0 80%;
  scroll-snap-align: start;
}

/* ─── Вертикальный пейджинг ─── */
.pages {
  height: 100dvh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
}
.page {
  height: 100dvh;
  scroll-snap-align: start;
}
```

### 23.2 Scroll Timeline (анимация по прокрутке)

```css
/* ─── Scroll-Driven Animations (новые!) ─── */

/* Анимация прогресс-бара чтения */
@keyframes progress {
  from { width: 0; }
  to   { width: 100%; }
}

.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: var(--color-accent);
  animation: progress linear;
  animation-timeline: scroll();          /* привязать к прокрутке страницы */
  animation-range: 0% 100%;
}

/* Появление элемента при скролле */
@keyframes reveal {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

.reveal-on-scroll {
  animation: reveal linear both;
  animation-timeline: view();            /* привязать к видимости элемента */
  animation-range: entry 0% entry 30%;  /* только при входе в view */
}

/* Именованная scroll timeline */
.scroll-parent {
  overflow-y: scroll;
  scroll-timeline: --my-timeline y;     /* имя и ось */
}

.parallax-child {
  animation: parallax linear;
  animation-timeline: --my-timeline;
}

/* Именованная view timeline */
.sticky-section {
  view-timeline: --section-progress y;
}
.progress-indicator {
  animation: fill-progress linear;
  animation-timeline: --section-progress;
  animation-range: contain;             /* пока section полностью в viewport */
}
```

---

## 24. SHAPES И CLIP-PATH

### 24.1 clip-path

```css
/* ─── Базовые фигуры ─── */
.clipped {
  /* Прямоугольник */
  clip-path: inset(10px);                   /* все стороны */
  clip-path: inset(10px 20px);             /* вертикаль горизонталь */
  clip-path: inset(10px 20px 30px 40px round 8px);

  /* Круг */
  clip-path: circle(50%);
  clip-path: circle(100px at 50% 50%);
  clip-path: circle(50% at center);

  /* Эллипс */
  clip-path: ellipse(50% 30% at 50% 50%);

  /* Полигон */
  clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
  clip-path: polygon(50% 0%, 100% 100%, 0 100%);  /* треугольник */
  clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);  /* шестиугольник */

  /* SVG путь */
  clip-path: path('M 0 0 L 100 0 L 100 75 Q 50 100 0 75 Z');
}

/* ─── Переходы между clip-path ─── */
.reveal {
  clip-path: circle(0% at 50% 50%);
  transition: clip-path 0.5s var(--ease-out);
}
.reveal:hover {
  clip-path: circle(100% at 50% 50%);
}

/* Диагональный reveal */
.diagonal {
  clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);
  transition: clip-path 0.5s;
}
.diagonal.visible {
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}

/* ─── Фигурные разделители секций ─── */
.wave-section {
  clip-path: polygon(
    0 0,
    100% 0,
    100% 90%,
    80% 95%,
    60% 90%,
    40% 95%,
    20% 90%,
    0 95%
  );
  padding-block-end: 5%;
}
```

### 24.2 CSS Shapes (обтекание)

```css
/* ─── shape-outside (обтекание текстом) ─── */
.float-shape {
  float: left;
  shape-outside: circle(50%);
  shape-outside: polygon(0 0, 100% 50%, 0 100%);
  shape-outside: url('mask.png');       /* по прозрачности */
  
  shape-margin: 1rem;                   /* отступ текста от формы */
  shape-image-threshold: 0.5;          /* порог прозрачности */
}

/* ─── Пример: круглое изображение с обтеканием ─── */
.avatar {
  float: left;
  width: 200px;
  height: 200px;
  shape-outside: circle(50%);
  clip-path: circle(50%);
  margin-inline-end: 1rem;
}
```

---

## 25. ФИЛЬТРЫ И BLEND MODES

### 25.1 filter

```css
.filtered {
  /* Базовые фильтры */
  filter: blur(4px);
  filter: brightness(1.2);           /* > 1 ярче, < 1 темнее */
  filter: contrast(1.5);
  filter: grayscale(100%);
  filter: hue-rotate(90deg);
  filter: invert(100%);
  filter: opacity(50%);
  filter: saturate(200%);
  filter: sepia(100%);

  /* Тень (работает с clip-path и SVG, в отличие от box-shadow) */
  filter: drop-shadow(2px 4px 6px rgb(0 0 0 / 0.3));

  /* Множественные фильтры */
  filter: 
    contrast(1.2) 
    saturate(1.3) 
    brightness(1.1);

  /* url() — SVG фильтр */
  filter: url('#svgFilter');

  /* Переходы фильтров */
  transition: filter 0.3s;
}

/* Эффект при hover */
.image-hover {
  transition: filter 0.3s;
}
.image-hover:hover {
  filter: brightness(1.1) saturate(1.2);
}

/* Размытие фона */
.frosted-glass {
  backdrop-filter: blur(10px) brightness(1.1);
  background: rgb(255 255 255 / 0.2);
  -webkit-backdrop-filter: blur(10px) brightness(1.1);
}
```

### 25.2 mix-blend-mode и background-blend-mode

```css
/* ─── mix-blend-mode (элемент с фоном под ним) ─── */
.blend {
  mix-blend-mode: multiply;      /* умножение — темнит */
  mix-blend-mode: screen;        /* экран — осветляет */
  mix-blend-mode: overlay;       /* оверлей — усиливает контраст */
  mix-blend-mode: darken;        /* тёмнее из двух */
  mix-blend-mode: lighten;       /* светлее из двух */
  mix-blend-mode: color-dodge;   /* осветление цвета */
  mix-blend-mode: color-burn;    /* затемнение цвета */
  mix-blend-mode: hard-light;
  mix-blend-mode: soft-light;
  mix-blend-mode: difference;    /* разница — инвертирует */
  mix-blend-mode: exclusion;
  mix-blend-mode: hue;
  mix-blend-mode: saturation;
  mix-blend-mode: color;
  mix-blend-mode: luminosity;
}

/* ─── background-blend-mode (слои фона между собой) ─── */
.bg-blend {
  background-image: url('texture.png'), linear-gradient(blue, purple);
  background-blend-mode: multiply;
}

/* ─── Популярный эффект: текст через изображение ─── */
.text-on-image {
  background-image: url('photo.jpg');
  background-size: cover;
  background-attachment: fixed;
}
.text-on-image h1 {
  color: white;
  mix-blend-mode: overlay;
}

/* ─── Эффект duotone ─── */
.duotone {
  position: relative;
}
.duotone img {
  filter: grayscale(100%);
}
.duotone::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom right,
    var(--color-brand-700),
    var(--color-brand-300)
  );
  mix-blend-mode: color;
}
```

---

## 26. GRID ADVANCED

### 26.1 Продвинутые паттерны Grid

```css
/* ─── RAM паттерн (Repeat, Auto, Minmax) ─── */
.ram {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  /* Магический однострочник: адаптивная сетка без media queries */
}

/* ─── Asymmetric Grid ─── */
.asymmetric {
  display: grid;
  grid-template-columns: 2fr 3fr 1fr;
  grid-template-rows: repeat(3, auto);
}

/* ─── Overlapping Grid ─── */
.overlap-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}
.overlap-grid .item-1 {
  grid-column: 1 / 3;
  grid-row: 1 / 2;
  z-index: 1;
}
.overlap-grid .item-2 {
  grid-column: 2 / 3;
  grid-row: 1 / 3;  /* перекрывается с item-1 */
}

/* ─── Full-bleed layout ─── */
.full-bleed-layout {
  display: grid;
  grid-template-columns:
    [full-start] minmax(var(--space-4), 1fr)
    [content-start] min(100% - 2 * var(--space-4), var(--size-container-lg))
    [content-end]
    minmax(var(--space-4), 1fr) [full-end];
}
.full-bleed-layout > * {
  grid-column: content;
}
.full-bleed-layout > .full-bleed {
  grid-column: full;
}

/* ─── Sticky в grid ─── */
.grid-with-sticky {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2rem;
  align-items: start;         /* ВАЖНО: иначе sticky не работает */
}
.sidebar {
  position: sticky;
  top: 1rem;
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
}
```

### 26.2 Dense и Auto Placement

```css
/* ─── Auto-fill vs Auto-fit ─── */
/* auto-fill: создаёт пустые колонки */
.auto-fill {
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  /* При 400px контейнере: 4 колонки по 100px */
}

/* auto-fit: схлопывает пустые колонки */
.auto-fit {
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  /* При 400px и 2 элементах: 2 колонки по 200px */
}

/* ─── Dense packing ─── */
.mosaic {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 100px;
  gap: 1rem;
  grid-auto-flow: dense;  /* заполнять пустоты */
}
.mosaic .wide { grid-column: span 2; }
.mosaic .tall { grid-row: span 2; }
.mosaic .big  { grid-column: span 2; grid-row: span 2; }
```

---

## 27. ПРОИЗВОДИТЕЛЬНОСТЬ CSS

### 27.1 Принципы производительности

```css
/* ─── will-change — подсказка браузеру ─── */
/* Использовать непосредственно перед анимацией, не постоянно */
.will-animate {
  will-change: transform, opacity;
  /* Только для трансформирующихся элементов */
  /* Не на *: — это убьёт производительность */
}
/* После анимации: */
.animation-done {
  will-change: auto;  /* сбросить */
}

/* ─── Изолировать дорогостоящие операции ─── */
.heavy-element {
  contain: layout paint;    /* изолировать layout и paint */
  contain: strict;          /* all — изолировать всё */
  content-visibility: auto; /* пропустить рендеринг невидимого */
  contain-intrinsic-size: 0 300px; /* placeholder высота */
}

/* ─── Ускорение GPU через transform ─── */
/* ✅ Используй transform вместо top/left для анимации */
.fast-animation {
  transform: translateX(var(--x, 0));
  /* НЕ: left: var(--x, 0px); — вызывает reflow */
}

/* ─── Переходы только на GPU-ускоренных свойствах ─── */
.performant {
  /* ✅ Хорошо */
  transition: transform 0.2s, opacity 0.2s;
  /* ❌ Избегай в анимациях */
  /* transition: width 0.2s, height 0.2s, margin 0.2s; */
}
```

### 27.2 Критический CSS

```css
/* Встроенный (inlined) критический CSS должен включать: */
/* 1. Базовые reset-стили */
/* 2. Шрифты для контента above the fold */
/* 3. Раскладку header */
/* 4. Hero section */
/* 5. Не более ~14KB gzipped */

/* ─── Асинхронная загрузка некритического CSS ─── */
/*
<link rel="preload" href="non-critical.css" as="style" 
      onload="this.onload=null;this.rel='stylesheet'">
<noscript>
  <link rel="stylesheet" href="non-critical.css">
</noscript>
*/

/* ─── Font loading optimization ─── */
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;      /* FOUT (flash of unstyled text) — приемлемо */
  /* font-display: optional; — без FOUT, может не загрузиться */
  /* font-display: block;    — FOIT (flash of invisible text) — плохо */
}
```

### 27.3 content-visibility и contain

```css
/* ─── content-visibility ─── */
.lazy-section {
  content-visibility: auto;          /* skip rendering если off-screen */
  contain-intrinsic-size: auto 500px; /* резервировать место */
}

/* ─── contain ─── */
.isolated {
  contain: none;            /* нет изоляции */
  contain: size;            /* размер не зависит от детей */
  contain: layout;          /* layout детей изолирован */
  contain: paint;           /* paint изолирован (как overflow:hidden) */
  contain: style;           /* CSS counters изолированы */
  contain: strict;          /* size + layout + paint + style */
  contain: content;         /* layout + paint + style */
}
```

---

## 28. ДОСТУПНОСТЬ В CSS

### 28.1 Визуальная доступность

```css
/* ─── Focus индикатор ─── */
/* Никогда не убирай outline без замены! */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-radius: 2px;
}

/* Кастомный фокус */
.btn:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--color-bg),
    0 0 0 4px var(--color-accent);
}

/* ─── Skip link (перейти к содержимому) ─── */
.skip-link {
  position: absolute;
  top: -100%;
  left: 1rem;
  background: var(--color-accent);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  z-index: var(--z-top);
  transition: top 0.2s;
}
.skip-link:focus {
  top: 0;
}

/* ─── Screen reader only (sr-only) ─── */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
/* Показать при фокусе */
.sr-only:not(:focus):not(:focus-within) {
  /* применяй sr-only только в этом состоянии */
}
```

### 28.2 Цветовой контраст и читабельность

```css
/* Минимум WCAG 2.1:
   AA: 4.5:1 для текста, 3:1 для крупного текста (18pt+)
   AAA: 7:1 для текста, 4.5:1 для крупного
*/

/* ─── Проверенные пары цветов ─── */
/* Тёмный текст на светлом фоне — безопаснее */
.good-contrast {
  background: #ffffff;
  color: #212529;           /* 16:1 */
}

/* ─── prefers-contrast ─── */
@media (prefers-contrast: more) {
  :root {
    --color-border: var(--color-neutral-700);
    --color-text-muted: var(--color-neutral-700);
  }
  .btn {
    border: 2px solid currentColor;
  }
}

/* ─── Размер текста ─── */
body { font-size: 1rem; }    /* Не задавай в px! Уважай настройки браузера */

/* ─── Минимальная область клика ─── */
.clickable {
  min-height: 44px;           /* iOS HIG: 44pt */
  min-width: 44px;            /* WCAG 2.5.5: 24px минимум */
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

### 28.3 Системы анимации и motion

```css
/* ─── Уважение к настройкам пользователя ─── */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ─── Режим принудительных цветов (Windows HC) ─── */
@media (forced-colors: active) {
  .btn {
    border: 2px solid ButtonText;
    color: ButtonText;
    background: ButtonFace;
  }
  .icon { forced-color-adjust: none; } /* сохранить цвет иконки */
}
```

---

## 29. ТЁМНАЯ ТЕМА

### 29.1 Автоматическая тёмная тема

```css
/* ─── Через CSS переменные ─── */
:root {
  color-scheme: light dark;  /* поддержка обеих схем */
  
  /* Светлые значения по умолчанию */
  --color-bg:     #ffffff;
  --color-surface: #f8f9fa;
  --color-text:   #212529;
  --color-border: #dee2e6;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:     #0a0a0a;
    --color-surface: #141414;
    --color-text:   #f0f0f0;
    --color-border: #333333;
  }
}

/* ─── Через data-атрибут (JS переключение) ─── */
:root,
[data-theme="light"] {
  --color-bg:   #ffffff;
  --color-text: #212529;
}

[data-theme="dark"] {
  --color-bg:   #0a0a0a;
  --color-text: #f0f0f0;
}

/* ─── Через light-dark() ─── */
:root { color-scheme: light dark; }

.element {
  background: light-dark(#ffffff, #0a0a0a);
  color:       light-dark(#212529, #f0f0f0);
}
```

### 29.2 Компонентные токены для тёмной темы

```css
:root {
  /* Светлая тема */
  --bg-primary:        #ffffff;
  --bg-secondary:      #f8f9fa;
  --bg-elevated:       #ffffff;
  --bg-overlay:        rgb(0 0 0 / 0.5);
  
  --text-primary:      #0f172a;
  --text-secondary:    #475569;
  --text-disabled:     #94a3b8;
  --text-on-accent:    #ffffff;
  
  --border-default:    #e2e8f0;
  --border-strong:     #cbd5e1;
  
  --shadow-color:      0deg 0% 0%;
  --shadow-strength:   1%;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary:      #0f172a;
    --bg-secondary:    #1e293b;
    --bg-elevated:     #1e293b;
    --bg-overlay:      rgb(0 0 0 / 0.7);
    
    --text-primary:    #f1f5f9;
    --text-secondary:  #94a3b8;
    --text-disabled:   #475569;
    
    --border-default:  #1e293b;
    --border-strong:   #334155;
    
    --shadow-color:    0deg 0% 0%;
    --shadow-strength: 30%;
  }
}

/* Использование */
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  box-shadow: 0 4px 16px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 5%));
}
```

### 29.3 Изображения в тёмной теме

```css
/* Снизить яркость изображений */
@media (prefers-color-scheme: dark) {
  img:not([src*=".svg"]) {
    filter: brightness(0.85) contrast(1.05);
  }
  
  /* Исключения */
  img.no-dimming,
  .logo img {
    filter: none;
  }
}

/* ─── color-scheme для системных элементов ─── */
:root { color-scheme: light dark; }
/* Автоматически стилизует: scrollbars, form controls,
   input backgrounds, select, checkboxes, dialog backgrounds */
```

---

## 30. CSS RESET

### 30.1 Современный CSS Reset

```css
/* ─── Modern CSS Reset (2024) ─── */

/* Базовые */
*,
*::before,
*::after {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
}

/* Документ */
html {
  /* Предотвратить автоувеличение шрифта на iOS */
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
  
  /* Плавный скролл */
  scroll-behavior: smooth;
  
  /* Уважать настройки OS */
  @media (prefers-reduced-motion: reduce) {
    scroll-behavior: auto;
  }
  
  /* Повесить font-size на html для rem */
  font-size: 100%;  /* = 16px, но уважает настройки браузера */
  
  /* Поддержка тёмной темы */
  color-scheme: light dark;
  
  /* Интерполяция шрифтов */
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100dvh;
  line-height: 1.5;
  font-family: var(--font-sans, system-ui, sans-serif);
  color: var(--color-text, currentColor);
  background: var(--color-bg, transparent);
}

/* Медиа */
img,
picture,
video,
canvas,
svg {
  display: block;
  max-width: 100%;
}

img,
video {
  height: auto;  /* сохранить пропорции */
}

/* Типографика */
h1, h2, h3, h4, h5, h6 {
  font-size: inherit;
  font-weight: inherit;
  overflow-wrap: break-word;
}

p,
li,
figcaption {
  overflow-wrap: break-word;
  max-width: var(--prose-width, 70ch);
}

/* Формы */
input,
button,
textarea,
select {
  font: inherit;  /* по умолчанию формы не наследуют шрифт */
  color: inherit;
}

button {
  cursor: pointer;
  background: none;
  border: none;
}

textarea {
  resize: vertical;  /* только по вертикали */
}

/* Списки */
ul,
ol {
  list-style: none;
}
/* Восстановить семантику для VoiceOver (Safari баг) */
ul[role="list"],
ol[role="list"] {
  list-style: none;
}

/* Ссылки */
a {
  color: inherit;
  text-decoration-skip-ink: auto;  /* подчёркивание огибает буквы */
}

/* Таблицы */
table {
  border-collapse: collapse;
  border-spacing: 0;
}

/* Скрытые элементы */
[hidden] { display: none !important; }
[disabled] { cursor: not-allowed; }

/* SVG */
svg {
  overflow: hidden;  /* IE баг */
}
[fill="none"] {
  fill: none;
}

/* Диалог */
dialog {
  max-width: 90vw;
  max-height: 90vh;
}

/* Монospace */
code,
kbd,
samp,
pre {
  font-family: var(--font-mono, monospace);
  font-size: 0.875em;
}

/* Вкладки */
:focus-visible {
  outline: 2px solid var(--color-accent, currentColor);
  outline-offset: 2px;
}

/* Избегать overflow при изменении размеров контента */
.wrapper,
.container {
  overflow-x: clip;
}
```

---

## 31. ИМЕНОВАНИЕ: BEM, CUBE CSS, UTILITY-FIRST

### 31.1 BEM (Block Element Modifier)

```css
/* ─── Синтаксис ─── */
.block { }                        /* Блок */
.block__element { }               /* Элемент (двойное подчёркивание) */
.block--modifier { }              /* Модификатор блока (двойной дефис) */
.block__element--modifier { }     /* Модификатор элемента */

/* ─── Пример: карточка ─── */
.card { }
.card__header { }
.card__body { }
.card__footer { }
.card__title { }
.card__thumbnail { }

.card--featured { }
.card--horizontal { }
.card--loading { }
.card__title--large { }

/* ─── Пример: форма ─── */
.form { }
.form__group { }
.form__label { }
.form__input { }
.form__helper { }
.form__error { }

.form__input--error { }
.form__input--success { }
.form--compact { }

/* ─── Антипаттерны BEM ─── */
/* ❌ Глубокая вложенность */
.card__header__title__link { }  /* слишком глубоко */

/* ✅ Флаттен */
.card__header-link { }  /* или переименовать */

/* ❌ HTML в классе */
.div__span { }  /* привязка к тегам */

/* ✅ Семантические имена */
.card__action { }
```

### 31.2 CUBE CSS (Composition Utility Block Exception)

```css
/* CUBE CSS — методология Энди Белла */

/* C - Composition (Раскладка) */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}
.stack > * + * {
  margin-block-start: var(--stack-space, var(--space-4));
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(var(--grid-min, 250px), 1fr));
}

/* U - Utilities (Утилиты) */
.text-center { text-align: center; }
.sr-only { /* ... screen reader only ... */ }
.flow > * + * { margin-block-start: var(--flow-space, 1em); }

/* B - Block (Блок) */
.card {
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

/* E - Exception (Исключение, через data-) */
.card[data-size="large"] {
  padding: var(--space-8);
}
.card[data-variant="featured"] {
  border: 2px solid var(--color-accent);
}
```

### 31.3 Utility-First подход

```css
/* Минимальная утилитарная система */
@layer utilities {
  /* ─── Display ─── */
  .flex        { display: flex; }
  .inline-flex { display: inline-flex; }
  .grid        { display: grid; }
  .block       { display: block; }
  .hidden      { display: none; }
  .contents    { display: contents; }

  /* ─── Flexbox утилиты ─── */
  .flex-col   { flex-direction: column; }
  .flex-wrap  { flex-wrap: wrap; }
  .items-center   { align-items: center; }
  .items-start    { align-items: flex-start; }
  .items-end      { align-items: flex-end; }
  .items-stretch  { align-items: stretch; }
  .justify-center  { justify-content: center; }
  .justify-between { justify-content: space-between; }
  .justify-end     { justify-content: flex-end; }
  .flex-1   { flex: 1 1 0%; }
  .flex-auto { flex: 1 1 auto; }
  .flex-none { flex: none; }
  .shrink-0 { flex-shrink: 0; }

  /* ─── Grid утилиты ─── */
  .place-center { place-items: center; }
  .col-span-2   { grid-column: span 2; }
  .col-full     { grid-column: 1 / -1; }

  /* ─── Gap ─── */
  .gap-1 { gap: var(--space-1); }
  .gap-2 { gap: var(--space-2); }
  .gap-4 { gap: var(--space-4); }
  .gap-6 { gap: var(--space-6); }
  .gap-8 { gap: var(--space-8); }

  /* ─── Типографика ─── */
  .text-xs    { font-size: var(--font-size-xs); }
  .text-sm    { font-size: var(--font-size-sm); }
  .text-base  { font-size: var(--font-size-base); }
  .text-lg    { font-size: var(--font-size-lg); }
  .text-xl    { font-size: var(--font-size-xl); }
  .font-bold  { font-weight: var(--font-weight-bold); }
  .font-medium { font-weight: var(--font-weight-medium); }
  .text-center { text-align: center; }
  .truncate   { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .uppercase  { text-transform: uppercase; }
  .leading-tight { line-height: var(--line-height-tight); }

  /* ─── Цвет ─── */
  .text-muted   { color: var(--color-text-muted); }
  .text-accent  { color: var(--color-accent); }
  .text-danger  { color: var(--color-danger-500); }
  .text-success { color: var(--color-success-500); }

  /* ─── Spacing ─── */
  .p-4  { padding: var(--space-4); }
  .p-6  { padding: var(--space-6); }
  .px-4 { padding-inline: var(--space-4); }
  .py-4 { padding-block: var(--space-4); }
  .m-auto { margin: auto; }
  .mx-auto { margin-inline: auto; }
  .mt-4 { margin-block-start: var(--space-4); }
  .mb-4 { margin-block-end: var(--space-4); }

  /* ─── Border ─── */
  .rounded    { border-radius: var(--radius-md); }
  .rounded-lg { border-radius: var(--radius-lg); }
  .rounded-full { border-radius: var(--radius-full); }
  .border     { border: 1px solid var(--color-border); }
  .border-t   { border-block-start: 1px solid var(--color-border); }

  /* ─── Тени ─── */
  .shadow-sm { box-shadow: var(--shadow-sm); }
  .shadow    { box-shadow: var(--shadow-md); }
  .shadow-lg { box-shadow: var(--shadow-lg); }

  /* ─── Прочее ─── */
  .overflow-hidden { overflow: hidden; }
  .relative { position: relative; }
  .absolute { position: absolute; }
  .inset-0  { inset: 0; }
  .w-full   { width: 100%; }
  .h-full   { height: 100%; }
  .min-h-screen { min-height: 100dvh; }
  .cursor-pointer { cursor: pointer; }
  .select-none { user-select: none; }
  .pointer-events-none { pointer-events: none; }
  .opacity-0    { opacity: 0; }
  .opacity-50   { opacity: 0.5; }
  .opacity-100  { opacity: 1; }
  .transition   { transition: all var(--duration-normal) var(--ease-default); }
  .transition-transform { transition: transform var(--duration-normal) var(--ease-out); }
  .transition-opacity   { transition: opacity var(--duration-normal) var(--ease-out); }
}
```

---

## 32. КОМПОНЕНТНЫЕ ПАТТЕРНЫ

### 32.1 Кнопки

```css
/* ─── Базовая кнопка ─── */
.btn {
  /* Сброс */
  appearance: none;
  border: none;
  background: none;

  /* Размеры */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  padding: 0.5em 1em;
  min-height: 2.5rem;

  /* Типографика */
  font-family: inherit;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  line-height: 1.25;
  letter-spacing: 0.025em;
  white-space: nowrap;
  text-decoration: none;

  /* Визуал */
  border-radius: var(--radius-md);
  cursor: pointer;
  user-select: none;
  outline-offset: 2px;
  position: relative;
  overflow: hidden;

  /* Переход */
  transition:
    background-color var(--duration-fast) var(--ease-out),
    border-color     var(--duration-fast) var(--ease-out),
    box-shadow       var(--duration-fast) var(--ease-out),
    transform        var(--duration-fast) var(--ease-out),
    opacity          var(--duration-fast) var(--ease-out);

  /* Токены компонента */
  --btn-bg:        transparent;
  --btn-color:     var(--color-text);
  --btn-border:    transparent;
  --btn-shadow:    none;
  --btn-hover-bg:  transparent;

  background: var(--btn-bg);
  color:      var(--btn-color);
  border:     1px solid var(--btn-border);
  box-shadow: var(--btn-shadow);
}

.btn:hover {
  background: var(--btn-hover-bg);
}

.btn:active {
  transform: scale(0.98);
}

.btn:disabled,
.btn[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Варианты */
.btn-primary {
  --btn-bg:       var(--color-accent);
  --btn-color:    white;
  --btn-hover-bg: var(--color-accent-hover);
}
.btn-secondary {
  --btn-bg:       var(--color-bg-subtle);
  --btn-color:    var(--color-text);
  --btn-border:   var(--color-border);
  --btn-hover-bg: var(--color-bg-muted);
}
.btn-ghost {
  --btn-hover-bg: var(--color-bg-subtle);
}
.btn-danger {
  --btn-bg:       var(--color-danger-500);
  --btn-color:    white;
  --btn-hover-bg: var(--color-danger-900);
}
.btn-outline {
  --btn-border:   var(--color-accent);
  --btn-color:    var(--color-accent);
  --btn-hover-bg: var(--color-brand-100);
}

/* Размеры */
.btn-sm { font-size: var(--font-size-xs); padding: 0.375em 0.75em; min-height: 2rem; }
.btn-lg { font-size: var(--font-size-md); padding: 0.625em 1.25em; min-height: 3rem; }
.btn-xl { font-size: var(--font-size-lg); padding: 0.75em 1.5em;  min-height: 3.5rem; }
.btn-icon { padding: 0.5em; aspect-ratio: 1; border-radius: var(--radius-md); }
.btn-full { width: 100%; }
```

### 32.2 Карточки

```css
/* ─── Базовая карточка ─── */
.card {
  --card-padding: var(--space-6);
  --card-radius:  var(--radius-xl);
  --card-shadow:  var(--shadow-md);
  --card-border:  var(--color-border);

  display: flex;
  flex-direction: column;
  
  background:    var(--color-surface);
  border:        1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow:    var(--card-shadow);
  overflow:      hidden;
  
  transition:
    box-shadow var(--duration-normal) var(--ease-out),
    transform  var(--duration-normal) var(--ease-out);
}

.card:where([href], [role="button"]) {
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}

.card:where([href], [role="button"]):hover {
  box-shadow: var(--shadow-xl);
  transform: translateY(-2px);
}

.card__image {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}
.card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--duration-slow) var(--ease-out);
}
.card:hover .card__image img {
  transform: scale(1.05);
}

.card__body  { padding: var(--card-padding); flex: 1; }
.card__footer {
  padding: var(--card-padding);
  padding-block-start: 0;
  margin-block-start: auto;
}

.card__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  margin-block-end: var(--space-2);
}

.card__description {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Варианты */
.card--horizontal {
  flex-direction: row;
}
.card--horizontal .card__image {
  width: 200px;
  flex-shrink: 0;
  aspect-ratio: auto;
}

.card--flat {
  --card-shadow: none;
  --card-border: var(--color-border);
}

.card--featured {
  --card-border: var(--color-accent);
  border-width: 2px;
}
```

### 32.3 Формы

```css
/* ─── Группа поля ─── */
.field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.field__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  transition: color var(--duration-fast);
}

.field__label .required {
  color: var(--color-danger-500);
  margin-inline-start: 0.25em;
}

/* ─── Базовый input ─── */
.input {
  appearance: none;
  width: 100%;
  padding: 0.5rem 0.75rem;
  min-height: 2.5rem;

  font: inherit;
  font-size: var(--font-size-base);
  color: var(--color-text);

  background: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  outline: none;

  transition:
    border-color var(--duration-fast),
    box-shadow   var(--duration-fast);
}

.input::placeholder { color: var(--color-text-subtle); }

.input:hover {
  border-color: var(--color-neutral-400);
}

.input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

.input:user-invalid,
.input[aria-invalid="true"] {
  border-color: var(--color-danger-500);
}
.input:user-invalid:focus,
.input[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-danger-500) 15%, transparent);
}

.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--color-bg-subtle);
}

/* ─── Обёртка с иконкой ─── */
.input-wrapper {
  position: relative;
}
.input-wrapper .icon-start {
  position: absolute;
  inset-inline-start: 0.75rem;
  inset-block: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  pointer-events: none;
}
.input-wrapper .input {
  padding-inline-start: 2.5rem;
}

/* ─── Сообщения ─── */
.field__helper {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.field__error {
  font-size: var(--font-size-xs);
  color: var(--color-danger-500);
  display: flex;
  align-items: center;
  gap: 0.25em;
}

/* ─── Контекстные состояния ─── */
.field:has(.input:focus) .field__label { color: var(--color-accent); }
.field:has(.input:user-invalid) .field__label { color: var(--color-danger-500); }
.field:has(.input:user-valid) .field__label { color: var(--color-success-500); }

/* ─── Checkbox / Radio ─── */
.checkbox,
.radio {
  appearance: none;
  width: 1rem;
  height: 1rem;
  border: 1.5px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
  transition:
    background   var(--duration-fast),
    border-color var(--duration-fast),
    box-shadow   var(--duration-fast);
}

.radio { border-radius: 50%; }

.checkbox:checked,
.radio:checked {
  background:    var(--color-accent);
  border-color:  var(--color-accent);
}

.checkbox:checked::after {
  content: '';
  position: absolute;
  inset: 2px;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 12 10' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 5l3.5 3.5L11 1' stroke='white' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E") center/contain no-repeat;
}

.radio:checked::after {
  content: '';
  position: absolute;
  inset: 3px;
  background: white;
  border-radius: 50%;
}

.checkbox:focus-visible,
.radio:focus-visible {
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 25%, transparent);
}

/* ─── Toggle / Switch ─── */
.toggle {
  appearance: none;
  width: 2.5rem;
  height: 1.375rem;
  background: var(--color-neutral-300);
  border-radius: 9999px;
  cursor: pointer;
  position: relative;
  transition: background var(--duration-fast);
}
.toggle::after {
  content: '';
  position: absolute;
  width: 1rem;
  height: 1rem;
  background: white;
  border-radius: 50%;
  top: 3px;
  left: 3px;
  box-shadow: var(--shadow-sm);
  transition: transform var(--duration-fast) var(--ease-bounce);
}
.toggle:checked {
  background: var(--color-accent);
}
.toggle:checked::after {
  transform: translateX(1.125rem);
}
```

### 32.4 Модальное окно и Диалог

```css
/* ─── Нативный <dialog> ─── */
dialog {
  position: fixed;
  inset: 0;
  margin: auto;
  
  max-width: min(90vw, 560px);
  max-height: min(90dvh, 600px);
  width: 100%;
  
  padding: 0;
  border: none;
  border-radius: var(--radius-xl);
  background: var(--color-surface);
  box-shadow: var(--shadow-2xl);
  
  overflow: hidden;
  
  /* Анимация открытия */
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
  transition:
    opacity   var(--duration-normal) var(--ease-out),
    transform var(--duration-normal) var(--ease-out),
    display   var(--duration-normal) allow-discrete,
    overlay   var(--duration-normal) allow-discrete;
}

dialog[open] {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* starting-style для открытия */
@starting-style {
  dialog[open] {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
}

/* Фон/бэкдроп */
dialog::backdrop {
  background: rgb(0 0 0 / 0);
  backdrop-filter: blur(0px);
  transition:
    background var(--duration-normal),
    backdrop-filter var(--duration-normal),
    display var(--duration-normal) allow-discrete,
    overlay var(--duration-normal) allow-discrete;
}

dialog[open]::backdrop {
  background: rgb(0 0 0 / 0.5);
  backdrop-filter: blur(4px);
}

@starting-style {
  dialog[open]::backdrop {
    background: rgb(0 0 0 / 0);
    backdrop-filter: blur(0px);
  }
}

/* Контент диалога */
.dialog__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-6);
  border-block-end: 1px solid var(--color-border);
}

.dialog__body {
  padding: var(--space-6);
  overflow-y: auto;
  max-height: calc(90dvh - 140px);
}

.dialog__footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-6);
  border-block-start: 1px solid var(--color-border);
}
```

### 32.5 Навигация

```css
/* ─── Основная навигация ─── */
.nav {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.nav__link {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  text-decoration: none;
  transition:
    background var(--duration-fast),
    color var(--duration-fast);
}

.nav__link:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.nav__link[aria-current="page"],
.nav__link.active {
  background: var(--color-brand-100);
  color: var(--color-accent);
}

/* ─── Breadcrumbs ─── */
.breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.breadcrumbs__item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumbs__item:not(:last-child)::after {
  content: '/';
  color: var(--color-border-strong);
}

.breadcrumbs__link {
  color: inherit;
  text-decoration: none;
  transition: color var(--duration-fast);
}

.breadcrumbs__link:hover { color: var(--color-accent); }
.breadcrumbs__item:last-child { color: var(--color-text); }

/* ─── Tabs ─── */
.tabs {
  border-block-end: 1px solid var(--color-border);
  display: flex;
  gap: var(--space-1);
  overflow-x: auto;
  scrollbar-width: none;
}

.tab {
  padding: 0.625rem 1rem;
  border: none;
  background: none;
  font: inherit;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  cursor: pointer;
  white-space: nowrap;
  position: relative;
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  transition: color var(--duration-fast);
}

.tab::after {
  content: '';
  position: absolute;
  inset-inline: 0;
  inset-block-end: -1px;
  height: 2px;
  background: var(--color-accent);
  border-radius: 2px 2px 0 0;
  transform: scaleX(0);
  transition: transform var(--duration-fast) var(--ease-out);
}

.tab:hover { color: var(--color-text); }
.tab:hover::after { transform: scaleX(0.5); }

.tab[aria-selected="true"] {
  color: var(--color-accent);
}
.tab[aria-selected="true"]::after {
  transform: scaleX(1);
}
```

### 32.6 Skeleton Loading и Loading States

```css
/* ─── Skeleton ─── */
@keyframes skeleton {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-subtle) 0%,
    var(--color-bg-muted) 50%,
    var(--color-bg-subtle) 100%
  );
  background-size: 200% 100%;
  animation: skeleton 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
  color: transparent;
  user-select: none;
}

/* Skeleton для карточки */
.skeleton-card {
  border-radius: var(--radius-xl);
  overflow: hidden;
}
.skeleton-card .skeleton-image {
  aspect-ratio: 16/9;
  border-radius: 0;
}
.skeleton-card .skeleton-content {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.skeleton-line {
  height: 1em;
  border-radius: var(--radius-full);
}
.skeleton-line.short { width: 60%; }
.skeleton-line.medium { width: 80%; }
.skeleton-line.full { width: 100%; }

/* ─── Spinner ─── */
.spinner {
  --size: 1.5rem;
  --border: 2px;
  
  width: var(--size);
  height: var(--size);
  border: var(--border) solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  opacity: 0.7;
}

/* ─── Dots loader ─── */
@keyframes dot-pulse {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40%           { transform: scale(1);   opacity: 1; }
}
.dots-loader {
  display: flex;
  gap: 0.375rem;
  align-items: center;
}
.dots-loader span {
  width: 0.5rem;
  height: 0.5rem;
  background: currentColor;
  border-radius: 50%;
  animation: dot-pulse 1.2s ease-in-out infinite;
}
.dots-loader span:nth-child(2) { animation-delay: 0.2s; }
.dots-loader span:nth-child(3) { animation-delay: 0.4s; }
```

### 32.7 Тосты / Уведомления

```css
/* ─── Toast Container ─── */
.toast-container {
  position: fixed;
  inset-block-end: var(--space-4);
  inset-inline-end: var(--space-4);
  z-index: var(--z-toast);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 360px;
  width: calc(100% - var(--space-8));
  pointer-events: none;
}

/* ─── Toast ─── */
.toast {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-neutral-800);
  color: var(--color-neutral-100);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  pointer-events: auto;

  animation: toast-in var(--duration-slow) var(--ease-bounce);
}

@keyframes toast-in {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}

.toast.toast-success { background: var(--color-success-900); }
.toast.toast-error   { background: var(--color-danger-900); }
.toast.toast-warning { background: var(--color-warning-900); color: var(--color-neutral-900); }
.toast.toast-info    { background: var(--color-brand-900); }
```

### 32.8 Tooltip / Popover

```css
/* ─── Нативный CSS Tooltip ─── */
[data-tooltip] {
  position: relative;
}
[data-tooltip]::after {
  content: attr(data-tooltip);
  position: absolute;
  inset-block-end: calc(100% + 8px);
  inset-inline-start: 50%;
  transform: translateX(-50%);
  
  padding: 0.375rem 0.625rem;
  background: var(--color-neutral-800);
  color: var(--color-neutral-100);
  font-size: var(--font-size-xs);
  white-space: nowrap;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  pointer-events: none;
  
  opacity: 0;
  transform: translateX(-50%) translateY(4px);
  transition:
    opacity   var(--duration-fast),
    transform var(--duration-fast);
}

[data-tooltip]:hover::after,
[data-tooltip]:focus::after {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* ─── Нативный <popover> ─── */
.popover {
  position: absolute;
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  max-width: 280px;
  
  /* Анимация открытия */
  opacity: 0;
  transform: scale(0.95);
  transition:
    opacity   var(--duration-fast) var(--ease-out),
    transform var(--duration-fast) var(--ease-out),
    display   var(--duration-fast) allow-discrete,
    overlay   var(--duration-fast) allow-discrete;
}

.popover:popover-open {
  opacity: 1;
  transform: scale(1);
}

@starting-style {
  .popover:popover-open {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

---

## 33. АНТИПАТТЕРНЫ И ЧАСТЫЕ ОШИБКИ

### 33.1 Антипаттерны раскладки

```css
/* ❌ Float для раскладки */
.col { float: left; width: 33%; }
/* ✅ Grid или Flex */
.cols { display: grid; grid-template-columns: repeat(3, 1fr); }

/* ❌ Абсолютные пиксели для всего */
.container { width: 960px; }
/* ✅ Fluid с max */
.container { max-inline-size: 60rem; margin-inline: auto; }

/* ❌ Hacks для вертикального центрирования */
.centered { position: absolute; top: 50%; transform: translateY(-50%); }
/* ✅ Flexbox или Grid */
.centered { display: flex; align-items: center; }
.centered { display: grid; place-items: center; }

/* ❌ Magic numbers */
.element { margin-top: 37px; }
/* ✅ Токены и смысловые значения */
.element { margin-block-start: var(--space-8); }

/* ❌ !important везде */
.red { color: red !important; }
/* ✅ Использовать @layer и правильную специфичность */
```

### 33.2 Антипаттерны типографики

```css
/* ❌ Размер шрифта в px для body */
body { font-size: 16px; } /* игнорирует настройки браузера */
/* ✅ rem или % */
body { font-size: 100%; }

/* ❌ Слишком малый размер */
.caption { font-size: 10px; }
/* ✅ Минимум 12px / 0.75rem */
.caption { font-size: var(--font-size-xs); }

/* ❌ Слишком длинные строки */
p { max-width: 100%; }
/* ✅ Ограничить для читабельности */
p { max-width: 65ch; }

/* ❌ Высота строки в px */
.text { line-height: 24px; }
/* ✅ Безразмерное значение */
.text { line-height: 1.5; }

/* ❌ Отключённое сглаживание на тёмном фоне */
/* (не отключать -webkit-font-smoothing: antialiased на светлом) */
body { -webkit-font-smoothing: antialiased; } /* OK на тёмном, спорно на светлом */
```

### 33.3 Антипаттерны производительности

```css
/* ❌ Дорогие универсальные селекторы */
* { box-shadow: 0 0 10px black; }  /* применяется ко всем */

/* ❌ Анимация layout-вызывающих свойств */
@keyframes bad {
  from { width: 0; height: 0; }
  to   { width: 200px; height: 200px; }
}
/* ✅ Только transform и opacity */
@keyframes good {
  from { transform: scale(0); }
  to   { transform: scale(1); }
}

/* ❌ will-change везде */
* { will-change: transform; } /* убивает производительность */
/* ✅ Точечно, только когда нужно */
.animated-element { will-change: transform; }

/* ❌ Тяжёлые фильтры на частоанимируемых элементах */
.scroll-element { filter: blur(20px); } /* пересчёт при каждом скролле */

/* ❌ Импорт CSS внутри CSS без оптимизации */
@import url('a.css');
@import url('b.css'); /* блокирующие последовательные запросы */
/* ✅ Использовать HTTP/2 или бандлер */
```

### 33.4 Антипаттерны специфичности

```css
/* ❌ Чрезмерно специфичные селекторы */
body div.container ul li.item a.link { color: blue; }
/* ✅ Один класс */
.nav-link { color: blue; }

/* ❌ ID в CSS (высокая специфичность, сложно переопределить) */
#header { background: blue; }
/* ✅ Классы */
.site-header { background: blue; }

/* ❌ Инлайн стили (трудно переопределить) */
/* <div style="color: red"> */
/* ✅ Классы или CSS переменные */

/* ❌ !important для решения специфичности */
.btn { color: blue !important; }
/* ✅ Правильно организовать слои и специфичность */
@layer components { .btn { color: blue; } }
```

### 33.5 Антипаттерны доступности

```css
/* ❌ Удалять outline без замены */
* { outline: none; }
/* ✅ Оставить для :focus-visible */
:focus { outline: none; }
:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }

/* ❌ Слишком маленькие цели нажатия */
.icon-btn { width: 16px; height: 16px; }
/* ✅ Минимум 44x44 */
.icon-btn {
  width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center;
}

/* ❌ Цвет как единственный индикатор */
.required { color: red; } /* что если человек не видит цвет? */
/* ✅ Дополнительный индикатор */
.required::after { content: ' *'; color: red; aria-hidden: true; }

/* ❌ content только визуальный */
.icon::before { content: '→'; }
/* ✅ Спрятать от screen reader */
.icon::before { content: '→'; aria-hidden: 'true'; }
/* или: */
.icon { speak: none; }

/* ❌ Убирать видимость без aria */
.modal { visibility: hidden; }
/* ✅ */
.modal { visibility: hidden; }  /* + aria-hidden="true" в HTML */
```

---

## 34. ОТЛАДКА CSS

### 34.1 Техники отладки

```css
/* ─── Outline для всех элементов (временно) ─── */
* { outline: 1px solid red; }
* * { outline: 1px solid green; }
* * * { outline: 1px solid blue; }

/* ─── Цветной background для понимания размеров ─── */
.debug { background: rgb(255 0 0 / 0.1); }
.debug * { background: rgb(0 255 0 / 0.1); }

/* ─── Проверить overflow ─── */
* {
  outline: 1px solid rgba(255 0 0 / 0.3);
  overflow: visible;
}

/* ─── Медленные анимации ─── */
*, *::before, *::after {
  animation-duration: 10s !important;
  transition-duration: 5s !important;
}

/* ─── Визуализация grid и flex ─── */
/* Используй DevTools браузера (F12 → Inspector → Grid/Flex badge) */
```

### 34.2 Работа с DevTools

```css
/* Chrome DevTools — полезные функции: */
/*
- Elements > Styles: просмотр всех стилей, в т.ч. унаследованных
- Elements > Computed: вычисленные значения
- Elements > Layout: Grid/Flex визуализация
- :hov кнопка: имитация :hover, :focus, :active, :visited
- CSS Overview (More tools): анализ цветов, шрифтов, media queries
- Coverage: неиспользуемый CSS
*/

/* ─── Полезные data-атрибуты для отладки ─── */
[data-debug] {
  outline: 2px solid red !important;
}
[data-debug="flex"]  { background: rgba(0 255 0 / 0.1) !important; }
[data-debug="grid"]  { background: rgba(0 0 255 / 0.1) !important; }
```

---

## 35. БИБЛИОТЕКА СНИППЕТОВ

### 35.1 Центрирование

```css
/* Методы центрирования — выбери нужный */

/* 1. Flexbox (универсальный) */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 2. Grid */
.grid-center {
  display: grid;
  place-items: center;
}

/* 3. Absolute + transform */
.abs-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* 4. Absolute + inset + margin */
.abs-center-margin {
  position: absolute;
  inset: 0;
  width: fit-content;
  height: fit-content;
  margin: auto;
}

/* 5. Grid с margin auto */
.grid-margin-center {
  display: grid;
}
.grid-margin-center > * {
  margin: auto;
}
```

### 35.2 Визуальные эффекты

```css
/* ─── Frosted glass ─── */
.glass {
  background: rgb(255 255 255 / 0.1);
  backdrop-filter: blur(10px) saturate(180%);
  -webkit-backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgb(255 255 255 / 0.15);
  border-radius: var(--radius-xl);
}
.glass-dark {
  background: rgb(0 0 0 / 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgb(255 255 255 / 0.1);
}

/* ─── Gradient text ─── */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* ─── Neon glow ─── */
.neon {
  color: #0ff;
  text-shadow:
    0 0 5px #0ff,
    0 0 10px #0ff,
    0 0 20px #0ff,
    0 0 40px #00f;
}
.neon-box {
  box-shadow:
    0 0 5px var(--color-accent),
    0 0 20px var(--color-accent),
    0 0 40px var(--color-accent);
}

/* ─── Neumorphism ─── */
.neumorphic {
  background: #e0e5ec;
  border-radius: var(--radius-xl);
  box-shadow:
    6px 6px 12px #b8bec7,
    -6px -6px 12px #ffffff;
}
.neumorphic-pressed {
  box-shadow:
    inset 6px 6px 12px #b8bec7,
    inset -6px -6px 12px #ffffff;
}

/* ─── Grain / Noise texture ─── */
.grainy {
  position: relative;
}
.grainy::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.1'/%3E%3C/svg%3E");
  border-radius: inherit;
  pointer-events: none;
  opacity: 0.4;
}

/* ─── Underline animation ─── */
.animated-underline {
  text-decoration: none;
  background-image: linear-gradient(var(--color-accent), var(--color-accent));
  background-repeat: no-repeat;
  background-position: 0% 100%;
  background-size: 0% 2px;
  transition: background-size 0.3s var(--ease-out);
}
.animated-underline:hover {
  background-size: 100% 2px;
}

/* ─── Aspect ratio box (старый метод) ─── */
/* Используй новый aspect-ratio: */
.ratio-box { aspect-ratio: 16 / 9; }
/* Фолбэк: */
.ratio-box-fallback {
  position: relative;
  padding-block-end: 56.25%; /* 9/16 * 100 */
}
.ratio-box-fallback > * {
  position: absolute;
  inset: 0;
}

/* ─── Smooth corners (superellipse) ─── */
.smooth-corners {
  border-radius: 30%;
  /* iOS-like через SVG clip-path для точного суперэллипса */
}

/* ─── Stacked cards ─── */
.stack-cards {
  position: relative;
}
.stack-cards::before,
.stack-cards::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: inherit;
  z-index: -1;
}
.stack-cards::before {
  transform: rotate(-2deg) translateY(-4px);
}
.stack-cards::after {
  transform: rotate(2deg) translateY(-8px);
  background: var(--color-bg-subtle);
}

/* ─── Dotted / Dashed border ─── */
.dotted-border {
  border: 2px dashed var(--color-border-strong);
  border-radius: var(--radius-xl);
}

/* ─── Радужная рамка ─── */
.rainbow-border {
  position: relative;
  border-radius: var(--radius-xl);
  background: var(--color-surface);
}
.rainbow-border::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: calc(var(--radius-xl) + 2px);
  background: conic-gradient(
    hsl(0 100% 50%),
    hsl(60 100% 50%),
    hsl(120 100% 50%),
    hsl(180 100% 50%),
    hsl(240 100% 50%),
    hsl(300 100% 50%),
    hsl(360 100% 50%)
  );
  z-index: -1;
}
```

### 35.3 Layout рецепты

```css
/* ─── Sidebar layout (Holy Grail) ─── */
.with-sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-8);
}
.with-sidebar > :first-child {
  flex-basis: 250px;
  flex-grow: 1;
}
.with-sidebar > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-inline-size: 50%;
}

/* ─── Stack layout ─── */
.stack { display: flex; flex-direction: column; }
.stack > * { margin-block: 0; }
.stack > * + * { margin-block-start: var(--stack-space, var(--space-4)); }

/* ─── Cluster layout ─── */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-gap, var(--space-4));
  justify-content: var(--cluster-justify, flex-start);
  align-items: var(--cluster-align, center);
}

/* ─── Cover layout (центр + верх + низ) ─── */
.cover {
  display: flex;
  flex-direction: column;
  min-block-size: 100dvh;
  padding: var(--space-8);
}
.cover > * { margin-block: auto; }
.cover > :first-child { margin-block-start: 0; }
.cover > :last-child  { margin-block-end: 0; }

/* ─── Reel (горизонтальная прокрутка) ─── */
.reel {
  display: flex;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  gap: var(--space-4);
  padding-block: var(--space-4);
  scrollbar-width: thin;
}
.reel > * {
  flex: 0 0 auto;
  scroll-snap-align: start;
}

/* ─── Imposter (absolute поверх) ─── */
.imposter-container { position: relative; }
.imposter {
  position: absolute;
  inset-block-start: 50%;
  inset-inline-start: 50%;
  transform: translate(-50%, -50%);
}

/* ─── Frame (соотношение сторон с обрезкой) ─── */
.frame {
  aspect-ratio: var(--ratio, 16 / 9);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.frame > img,
.frame > video {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
}

/* ─── Switcher (переключение на одноколоночный) ─── */
.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}
.switcher > * {
  flex-grow: 1;
  flex-basis: calc((var(--threshold, 768px) - 100%) * 999);
}
```

### 35.4 Анимационные эффекты

```css
/* ─── Появление с задержкой (stagger) ─── */
.stagger-parent > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fade-up 0.5s var(--ease-out) forwards;
}
.stagger-parent > :nth-child(1) { animation-delay: 0.0s; }
.stagger-parent > :nth-child(2) { animation-delay: 0.1s; }
.stagger-parent > :nth-child(3) { animation-delay: 0.2s; }
.stagger-parent > :nth-child(4) { animation-delay: 0.3s; }
.stagger-parent > :nth-child(5) { animation-delay: 0.4s; }

@keyframes fade-up {
  to { opacity: 1; transform: translateY(0); }
}

/* ─── Hover 3D card ─── */
.card-3d-wrapper {
  perspective: 1000px;
}
.card-3d-inner {
  transition: transform 0.3s var(--ease-out);
  transform-style: preserve-3d;
}
/* JS устанавливает --rx и --ry через mousemove */
.card-3d-inner {
  transform: rotateX(calc(var(--rx, 0) * 1deg)) rotateY(calc(var(--ry, 0) * 1deg));
}

/* ─── Морфинг кнопки в спиннер ─── */
.btn-morphing {
  --btn-width: 120px;
  width: var(--btn-width);
  transition:
    width var(--duration-slow) var(--ease-out),
    border-radius var(--duration-slow) var(--ease-out);
  overflow: hidden;
}
.btn-morphing.loading {
  width: 44px;
  border-radius: 50%;
  pointer-events: none;
}

/* ─── Текстовые эффекты ─── */
/* Reveal при hover */
.text-reveal {
  position: relative;
  overflow: hidden;
  display: inline-block;
}
.text-reveal::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-accent);
  transform: translateX(-101%);
  transition: transform 0.4s var(--ease-out);
}
.text-reveal:hover::after {
  transform: translateX(101%);
}
```

### 35.5 Современные CSS Selectors рецепты

```css
/* ─── Стилизовать форму при наличии ошибок ─── */
form:has(input:user-invalid) .submit-btn {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ─── Адаптация при наличии sidebar ─── */
.layout:has(.sidebar) .main {
  max-width: calc(100% - 280px);
}

/* ─── Чётные/нечётные карточки ─── */
.card:nth-child(even) {
  transform: translateY(20px);
}

/* ─── Последний элемент без border ─── */
.list-item:not(:last-child) {
  border-bottom: 1px solid var(--color-border);
}

/* ─── Выбрать элементы по количеству ─── */
/* Если элементов больше 3 — показать в сетке */
.grid:has(> :nth-child(4)) {
  grid-template-columns: repeat(2, 1fr);
}

/* ─── Стиль при пустом контейнере ─── */
.container:empty::after {
  content: 'Нет элементов';
  color: var(--color-text-muted);
  font-style: italic;
}
/* Или: */
.container:has(> *:nth-child(1))::after { display: none; }

/* ─── Последние N элементов ─── */
.item:nth-last-child(-n+3) {
  /* последние 3 элемента */
  background: var(--color-brand-100);
}

/* ─── Каждые N-ые группы ─── */
.item:nth-child(4n+1) { border-left: 3px solid var(--color-accent); }

/* ─── Hover на соседние элементы ─── */
.item { opacity: 1; transition: opacity 0.2s; }
.list:has(.item:hover) .item:not(:hover) { opacity: 0.5; }
```

---

## 36. СПРАВОЧНИК СВОЙСТВ ПО КАТЕГОРИЯМ

### 36.1 Быстрая таблица важнейших свойств

```
╔══════════════════════════════════════════════════════════════╗
║  КАТЕГОРИЯ           СВОЙСТВА                                ║
╠══════════════════════════════════════════════════════════════╣
║  Box Model           box-sizing, display, width, height,     ║
║                      margin, padding, overflow               ║
╠══════════════════════════════════════════════════════════════╣
║  Flexbox (на контейнере):                                    ║
║                      flex-direction, flex-wrap, flex-flow,   ║
║                      justify-content, align-items,           ║
║                      align-content, gap                      ║
║  Flexbox (на item):  flex, flex-grow, flex-shrink,           ║
║                      flex-basis, align-self, order           ║
╠══════════════════════════════════════════════════════════════╣
║  Grid (контейнер):   grid-template-columns/rows/areas,       ║
║                      grid-auto-flow/rows/columns,            ║
║                      justify/align-items/content, gap        ║
║  Grid (item):        grid-column/row, grid-area,             ║
║                      justify/align-self                      ║
╠══════════════════════════════════════════════════════════════╣
║  Position            position, top/right/bottom/left,        ║
║                      inset, z-index                          ║
╠══════════════════════════════════════════════════════════════╣
║  Typography          font-family/size/weight/style,          ║
║                      line-height, letter-spacing,            ║
║                      text-align/decoration/transform,        ║
║                      white-space, overflow-wrap, hyphens     ║
╠══════════════════════════════════════════════════════════════╣
║  Color               color, background, opacity              ║
║                      color-scheme, color-mix()               ║
╠══════════════════════════════════════════════════════════════╣
║  Background          background-color/image/size/position/   ║
║                      repeat/attachment/clip                  ║
╠══════════════════════════════════════════════════════════════╣
║  Border              border, border-radius, outline          ║
╠══════════════════════════════════════════════════════════════╣
║  Effects             box-shadow, filter, backdrop-filter,    ║
║                      mix-blend-mode, clip-path               ║
╠══════════════════════════════════════════════════════════════╣
║  Transform           transform, transform-origin,            ║
║                      translate, rotate, scale                ║
╠══════════════════════════════════════════════════════════════╣
║  Animation           transition, animation, @keyframes       ║
║                      animation-timeline                      ║
╠══════════════════════════════════════════════════════════════╣
║  Media               @media, @container, @supports, @layer   ║
╠══════════════════════════════════════════════════════════════╣
║  Variables           --custom-property, var(), @property     ║
╠══════════════════════════════════════════════════════════════╣
║  Functions           calc(), clamp(), min(), max(),          ║
║                      color-mix(), oklch(), env()             ║
╚══════════════════════════════════════════════════════════════╝
```

### 36.2 Значения по умолчанию — важнейшие

```css
/* Знать эти дефолты = понимать CSS */
display:     inline          (большинство элементов)
             block           (div, p, h1-h6, article, section...)
             table           (table)
             list-item       (li)

position:    static
z-index:     auto
overflow:    visible
opacity:     1
visibility:  visible

flex-direction:  row
flex-wrap:       nowrap
flex-grow:       0
flex-shrink:     1
flex-basis:      auto
align-items:     stretch      (!) — не center
justify-content: flex-start

grid-auto-flow:  row
align-items:     stretch      (!) — не center

font-weight:     400
font-style:      normal
line-height:     normal (≈1.2)
text-align:      start (≈left для LTR)
text-decoration: none (для большинства) / underline (для a)
white-space:     normal
word-break:      normal
text-transform:  none
vertical-align:  baseline     (для inline)

border-style:    none         (!) — нужно явно задать
background:      transparent
box-shadow:      none
transform:       none
transition:      none
animation:       none

cursor:          auto
pointer-events:  auto
user-select:     auto
```

### 36.3 Единицы измерения

```css
/* ─── Абсолютные ─── */
px   /* пиксели (технически не физические в 2024) */
pt   /* пункты (1pt = 1/72in) — только для print */
in, cm, mm, pc  /* для print */

/* ─── Относительные к шрифту ─── */
em   /* относительно font-size текущего элемента */
rem  /* относительно font-size корневого элемента (:root) */
ex   /* высота буквы 'x' */
ch   /* ширина цифры '0' */
cap  /* высота заглавной буквы */
lh   /* line-height текущего элемента */
rlh  /* line-height корневого элемента */

/* ─── Viewport ─── */
vw   /* % ширины viewport */
vh   /* % высоты viewport (проблема: мобильный Safari) */
vmin /* меньшее из vw и vh */
vmax /* большее из vw и vh */
vb   /* % block-size viewport */
vi   /* % inline-size viewport */

/* Dynamic viewport (рекомендуется для мобильных) */
dvw, dvh, dvmin, dvmax  /* dynamic — учитывает UI браузера */
svw, svh                /* small — с полным UI браузера */
lvw, lvh                /* large — без UI браузера */

/* ─── Container query units ─── */
cqw   /* % от inline-size ближайшего контейнера */
cqh   /* % от block-size */
cqi   /* = cqw для LTR */
cqb   /* = cqh для LTR */
cqmin /* меньшее из cqi и cqb */
cqmax /* большее из cqi и cqb */

/* ─── Угловые ─── */
deg   /* градусы: 0-360 */
rad   /* радианы: 0-6.28 */
grad  /* градианы: 0-400 */
turn  /* обороты: 0-1 */

/* ─── Временные ─── */
s     /* секунды */
ms    /* миллисекунды */

/* ─── Разрешение ─── */
dpi   /* dots per inch */
dpcm  /* dots per cm */
dppx  /* dots per px (= device-pixel-ratio) */

/* ─── Частота ─── */
Hz, kHz  /* для speech (редко) */

/* ─── Специальные значения ─── */
auto         /* браузер вычисляет */
none         /* отсутствие значения */
inherit      /* наследовать от родителя */
initial      /* начальное значение свойства */
unset        /* inherit для наследуемых, initial для остальных */
revert       /* до стиля браузера */
revert-layer /* до предыдущего @layer */
currentColor /* текущий цвет текста */
```

---

## ДОПОЛНЕНИЕ: ЧЕКЛИСТ СОВРЕМЕННОГО CSS

```
✅ АРХИТЕКТУРА
□ CSS переменные для всех токенов дизайна (цвета, отступы, шрифты)
□ @layer для управления специфичностью
□ Mobile-first подход
□ Логические свойства (margin-inline, padding-block)
□ box-sizing: border-box на *

✅ ТИПОГРАФИКА
□ font-size: 100% на :root (не px)
□ Fluid типографика через clamp()
□ text-wrap: balance для заголовков
□ max-width: 65ch для параграфов
□ Система типографической шкалы

✅ РАСКЛАДКА
□ Grid для двухмерных раскладок
□ Flexbox для одномерных
□ min(100%, Xpx) для адаптивных минимумов
□ Нет float для раскладки

✅ ПРОИЗВОДИТЕЛЬНОСТЬ
□ Анимация только transform и opacity
□ will-change только где нужно
□ font-display: swap для webfonts
□ content-visibility для длинных страниц

✅ ДОСТУПНОСТЬ
□ :focus-visible для всех интерактивных элементов
□ prefers-reduced-motion уважается
□ Минимальные размеры целей нажатия 44x44px
□ Достаточный контраст цветов (4.5:1 минимум)
□ Не только цвет как индикатор состояния

✅ ТЁМНАЯ ТЕМА
□ color-scheme: light dark на :root
□ Все цвета через переменные
□ prefers-color-scheme применён

✅ СОВРЕМЕННЫЕ ФИЧИ
□ container-type для Container Queries
□ clamp() для fluid значений
□ oklch() для цветов
□ CSS Nesting для вложенных стилей
□ :has() вместо JS где возможно
```

---

*Руководство охватывает CSS Living Standard актуальный на 2025 год.*  
*Все примеры — рабочий, современный код без устаревших паттернов.*
