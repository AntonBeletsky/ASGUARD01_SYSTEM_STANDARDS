# CSS Animation Detection & Classification Guide

> Полное руководство по обнаружению, классификации и аудиту CSS-анимаций в проекте.  
> Основано на исследовании файлов `cont-claude-refac-customer-account-*.html`.

---

## Содержание

1. [Что искать — сигнальные слова](#1-что-искать--сигнальные-слова)
2. [Трёхуровневая таксономия](#2-трёхуровневая-таксономия)
3. [Паттерны по назначению](#3-паттерны-по-назначению)
4. [Easing-функции — полная карта](#4-easing-функции--полная-карта)
5. [Перформанс: compositor vs paint vs layout](#5-перформанс-compositor-vs-paint-vs-layout)
6. [Что обнаружено в проекте — итог аудита](#6-что-обнаружено-в-проекте--итог-аудита)
7. [Неисследованная территория](#7-неисследованная-территория)
8. [Большой закомментированный блок — вся библиотека](#8-большой-закомментированный-блок--вся-библиотека)

---

## 1. Что искать — сигнальные слова

При аудите CSS-файла или HTML-компонента нужно grep-нуть следующие ключевые слова. Каждое из них — маркер одного из слоёв анимационного стека.

### Grep-команды для аудита

```bash
# Все @keyframes в проекте
grep -rn "@keyframes" ./src --include="*.css" --include="*.html"

# Все animation-декларации
grep -rn "animation:" ./src --include="*.css" --include="*.html"

# Все transition-декларации
grep -rn "transition:" ./src --include="*.css" --include="*.html"

# Transform-функции
grep -rn "transform:" ./src --include="*.css" --include="*.html"

# Перформанс-хинты
grep -rn "will-change:\|backface-visibility:\|perspective:" ./src

# Кастомные кривые
grep -rn "cubic-bezier" ./src --include="*.css" --include="*.html"

# Всё сразу — полный аудит
grep -rhE "(@keyframes|animation:|transition:|transform:|will-change:|cubic-bezier)" \
  ./src --include="*.css" --include="*.html" | sort -u
```

### Сигнальные слова по группам

| Группа | Ключевые слова |
|--------|---------------|
| **Keyframe-анимации** | `@keyframes`, `animation:`, `animation-name:`, `animation-duration:`, `animation-delay:`, `animation-fill-mode:`, `animation-iteration-count:`, `animation-play-state:` |
| **Переходы** | `transition:`, `transition-property:`, `transition-duration:`, `transition-timing-function:`, `transition-delay:` |
| **Трансформации** | `transform:`, `transform-origin:`, `transform-style:`, `transform-box:` |
| **3D-контекст** | `perspective:`, `perspective-origin:`, `backface-visibility:` |
| **Перформанс** | `will-change:`, `contain:`, `isolation:` |
| **Современные** | `animation-timeline:`, `animation-range:`, `view-transition-name:`, `offset-path:`, `@property` |
| **Easing** | `cubic-bezier(`, `steps(`, `linear(`, `ease`, `ease-in`, `ease-out`, `ease-in-out` |

---

## 2. Трёхуровневая таксономия

CSS-анимации делятся на три уровня по механизму работы:

```
┌─────────────────────────────────────────────────────┐
│                  CSS MOTION STACK                   │
├─────────────────────────────────────────────────────┤
│  УРОВЕНЬ 1: @keyframes + animation                  │
│  Автономная анимация. Не требует триггера состояния │
│  Примеры: shimmer, bounce, fadeInUp, shake          │
├─────────────────────────────────────────────────────┤
│  УРОВЕНЬ 2: transition                              │
│  Реакция на смену состояния (:hover, :checked,      │
│  JS-класс). Интерполирует ДВА состояния.            │
│  Примеры: hover lift, color change, scale on hover  │
├─────────────────────────────────────────────────────┤
│  УРОВЕНЬ 3: transform (статический)                 │
│  Моментальное преобразование без анимации.          │
│  Используется как конечное состояние transition     │
│  или внутри @keyframes.                             │
└─────────────────────────────────────────────────────┘
```

### Ключевое разделение `transition` vs `animation`

| Свойство | `transition` | `animation + @keyframes` |
|----------|-------------|--------------------------|
| Триггер | Смена CSS-состояния | Автономно / JS-класс |
| Состояний | 2 (from → to) | Неограничено (0% → 100%) |
| Цикличность | Нет | `infinite` |
| Управление | JS через classList | `animation-play-state` |
| Задержка | `transition-delay` | `animation-delay` |
| Применение | Интерактив, hover | Loader, attention, enter/exit |

---

## 3. Паттерны по назначению

### 3.1 Enter-анимации (появление)

Элемент появляется на странице или в DOM.

| Паттерн | Свойства | Длительность |
|---------|---------|-------------|
| **fadeInUp** | `opacity: 0→1` + `translateY(12px→0)` | 0.2–0.35s |
| **fadeInDown** | `opacity: 0→1` + `translateY(-12px→0)` | 0.2–0.35s |
| **fadeInLeft** | `opacity: 0→1` + `translateX(-12px→0)` | 0.2–0.35s |
| **fadeInRight** | `opacity: 0→1` + `translateX(12px→0)` | 0.2–0.35s |
| **popIn (zoomIn)** | `opacity: 0→1` + `scale(0.85→1)` | 0.3–0.4s |
| **flipIn** | `rotateY(90deg→0)` + `perspective` | 0.4–0.5s |
| **slideDown** | `max-height: 0→N` или `grid-template-rows: 0fr→1fr` | 0.3s |

### 3.2 Exit-анимации (исчезновение)

Элемент убирается из видимой области перед удалением из DOM.

| Паттерн | Свойства | Длительность |
|---------|---------|-------------|
| **fadeOutLeft** | `opacity: 1→0` + `translateX(0→-16px)` | 0.2–0.35s |
| **fadeOutRight** | `opacity: 1→0` + `translateX(0→16px)` | 0.2–0.35s |
| **fadeOutDown** | `opacity: 1→0` + `translateY(0→12px)` | 0.2–0.35s |
| **zoomOut** | `opacity: 1→0` + `scale(1→0.85)` | 0.2–0.3s |
| **flyOut** | `opacity: 1→0` + `translateY(0→-40px)` | 0.3s |

### 3.3 Attention-анимации (привлечение внимания)

Однократные или бесконечные анимации для привлечения взгляда.

| Паттерн | Механизм | Применение |
|---------|---------|-----------|
| **shake** | `translateX` осцилляция | Ошибка валидации |
| **pulseGlow** | `box-shadow` ripple (0→12px→0) | Активный шаг, статус |
| **bounce** | `translateY` вверх-вниз | Typing indicator |
| **heartbeat** | `scale(1→1.2→1)` двойной пульс | Like/favorite |
| **wiggle** | `rotate(-5deg→5deg)` | Уведомление о новом |
| **jello** | `skew` + `scale` волна | Игровой UI |

### 3.4 Infinite loop (бесконечные фоновые)

Запускаются сразу и работают до снятия класса.

| Паттерн | Механизм | Применение |
|---------|---------|-----------|
| **shimmer** | `translateX(-100%→100%)` на `::after` с gradient | Skeleton loading |
| **spin** | `rotate(0→360deg)` | Spinner загрузки |
| **breathe** | `scale(1→1.04→1)` медленно | Живой элемент |
| **float** | `translateY(0→-8px→0)` | Floating badge |
| **blink** | `opacity: 1→0→1` резко, через `steps()` | Cursor в typewriter |
| **wave** | `rotate` с delay по дочерним | Dots typing indicator |

### 3.5 State-анимации (прогресс и состояние)

Анимируют переход между логическими состояниями.

| Паттерн | Механизм | Применение |
|---------|---------|-----------|
| **progress bar** | `width: 0→N%` с `cubic-bezier` | Шаги, загрузка |
| **stroke draw** | `stroke-dashoffset` SVG | Checkmark, иконки |
| **typewriter** | `width: 0→auto` + `steps(N)` | Hero-текст |
| **count-up** | JS + `animation-duration` | Статистика, баланс |

---

## 4. Easing-функции — полная карта

### Стандартные ключевые слова

| Ключевое слово | Эквивалент cubic-bezier | Характер |
|---------------|------------------------|---------|
| `linear` | `cubic-bezier(0, 0, 1, 1)` | Механический, без ускорения |
| `ease` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Плавный старт и конец |
| `ease-in` | `cubic-bezier(0.42, 0, 1, 1)` | Медленный старт, быстрый конец |
| `ease-out` | `cubic-bezier(0, 0, 0.58, 1)` | Быстрый старт, медленный конец |
| `ease-in-out` | `cubic-bezier(0.42, 0, 0.58, 1)` | Симметрично замедленный |
| `step-start` | `steps(1, start)` | Мгновенно в начале |
| `step-end` | `steps(1, end)` | Мгновенно в конце |

### Кастомные cubic-bezier (найдены в проекте)

```css
/* Bounce / Spring — y2 > 1.0 создаёт overshoot */
cubic-bezier(0.18, 0.89, 0.32, 1.28)   /* popIn, bubble-in */
cubic-bezier(0.175, 0.885, 0.32, 1.275) /* easeOutBack, 3D flip */

/* Material Design */
cubic-bezier(0.25, 0.8, 0.25, 1)        /* standard hover */
cubic-bezier(0.4, 0, 0.2, 1)            /* standard — progress bar */
cubic-bezier(0.4, 0, 1, 1)              /* accelerate */
cubic-bezier(0, 0, 0.2, 1)             /* decelerate */
```

### Популярные именованные кривые (не найдены в проекте)

```css
/* Robert Penner easings — классика */
cubic-bezier(0.55, 0.085, 0.68, 0.53)  /* easeInQuad */
cubic-bezier(0.25, 0.46, 0.45, 0.94)   /* easeOutQuad */
cubic-bezier(0.215, 0.61, 0.355, 1)    /* easeOutCubic */
cubic-bezier(0.23, 1, 0.32, 1)         /* easeOutExpo */
cubic-bezier(0.68, -0.55, 0.265, 1.55) /* easeInOutBack */

/* Новый CSS linear() — CSS-пружина (2023+) */
linear(0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%, 1.077, 1.121, 1.077 24.3%, 0.996 28%, 1)
```

### Правило y > 1.0 (overshoot)

Если любое из четырёх значений `cubic-bezier(x1, y1, x2, y2)` выходит за диапазон `[0, 1]` — это создаёт **пружинный эффект** (overshoot). `x1`, `x2` обязаны быть в `[0, 1]`, но `y1`, `y2` — нет.

```
y2 = 1.28  →  небольшой overshoot (bounce)
y2 = 1.55  →  сильный overshoot (упругий)
y1 = -0.55 →  начинается "назад" перед движением вперёд
```

---

## 5. Перформанс: compositor vs paint vs layout

### Иерархия стоимости

```
ДЁШЕВО ────────────────────────────────────── ДОРОГО

  transform       opacity      filter     background    width/height
  [GPU только]  [GPU только]  [paint]     [paint]       [layout+paint]
      ✅             ✅           ⚠️          ⚠️              🚫
```

### Свойства по слоям рендеринга

**Compositor-only (GPU, 60fps без проблем):**
- `transform` — translateX/Y/Z, scale, rotate, skew, matrix
- `opacity`

**Paint (перерисовка пикселей, без layout):**
- `background-color`, `background-image`
- `color`, `border-color`, `outline-color`
- `box-shadow`, `text-shadow`
- `filter`, `backdrop-filter`
- `visibility`

**Layout + Paint (самые дорогие — reflow всего дерева):**
- `width`, `height`, `min-/max-`
- `margin`, `padding`
- `top`, `right`, `bottom`, `left`
- `font-size`, `line-height`
- `display`, `float`, `position`

### Ключевые свойства оптимизации

```css
/* Хинт браузеру заранее создать compositor layer */
will-change: transform;
will-change: transform, opacity;

/* Снять после завершения анимации (JS) */
element.addEventListener('animationend', () => {
  element.style.willChange = 'auto';
});

/* CSS containment — ограничить reflow до контейнера */
contain: layout style;

/* Предотвратить мерцание при 3D-трансформациях */
backface-visibility: hidden;

/* Явно задать пространство трансформаций */
transform-style: preserve-3d;
```

### Доступность — prefers-reduced-motion

```css
/* ОБЯЗАТЕЛЬНО добавлять в каждый проект с анимациями */
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
```

---

## 6. Что обнаружено в проекте — итог аудита

### Найденные @keyframes (7 уникальных)

| Имя в коде | Абстрактное имя | Файл | Назначение |
|-----------|----------------|------|-----------|
| `wishlist-appear` | fadeInUp | wishlist | Появление карточки |
| `viewed-card-in` | fadeInUp | viewed-items | Появление в сетке/списке |
| `mysizes-fade-in` | fadeInUp | mysizes | Контент аккордеона |
| `payments-fade-in` | fadeInUp | my-payments | Появление списка карт |
| `myreviews-card-in` | fadeInUp | my-reviews | Появление отзыва |
| `messages-bubble-in` | popIn | messages | Появление пузыря чата |
| `walletDialogZoomIn` | popIn | mywallet | Открытие модального окна |
| `wishlist-remove` | fadeOutLeft | wishlist | Удаление из списка |
| `myreviews-shake` | shakeHorizontal | my-reviews | Ошибка валидации |
| `stepPulse` | pulseGlow | orders | Активный шаг доставки |
| `shimmer` | shimmer | viewed-items | Skeleton loading |
| `messages-dot-bounce` | bounceY | messages | Typing indicator |

### Найденные transition-паттерны

| Паттерн | CSS | Файлы |
|---------|-----|-------|
| Hover lift | `transform: translateY(-2px)` + shadow | wallet, payments, wishlist |
| Scale on hover | `transform: scale(1.04–1.35)` | promo, viewed-items |
| Color change | `background`, `color`, `border-color` 0.15–0.3s | все файлы |
| Progress bar | `width: N%` + `cubic-bezier(.4,0,.2,1)` | orders |
| 3D flip | `rotateY` + `perspective: 1000px` | mywallet |

### Используемые easing-функции

```
ease           — основной (большинство анимаций)
ease-out       — stepPulse
ease-in        — wishlist-remove (быстро "улетает")
ease-in-out    — shimmer (плавный loop)
cubic-bezier(0.18, 0.89, 0.32, 1.28)    — popIn (bounce)
cubic-bezier(0.175, 0.885, 0.32, 1.275) — 3D flip (easeOutBack)
cubic-bezier(0.25, 0.8, 0.25, 1)        — hover transform
cubic-bezier(.4, 0, .2, 1)              — progress bar
```

### Найденные перформанс-практики

- ✅ `will-change: transform` и `will-change: transform, opacity` — присутствуют
- ✅ `animation-fill-mode: both` и `forwards` — везде корректно
- ✅ Явный сброс `animation: none !important` при необходимости
- ✅ Комментарий о GPU cleanup после завершения анимации
- ❌ `prefers-reduced-motion` — отсутствует, рекомендуется добавить
- ❌ `backface-visibility: hidden` — отсутствует для 3D flip
- ❌ `contain:` — не используется

---

## 7. Неисследованная территория

Паттерны, которых нет в проекте, но которые представляют интерес для развития:

### Современные CSS API (2023+)

```
scroll-driven animations  — animation-timeline: scroll() / view()
View Transition API       — view-transition-name + startViewTransition()
CSS @property             — анимируемые custom properties (Houdini)
linear() easing           — CSS-пружины без JS
offset-path / motion-path — движение по SVG-пути
```

### Паттерны, которые стоит добавить

| Паттерн | Механизм | Где применить |
|---------|---------|--------------|
| SVG stroke draw | `stroke-dashoffset` | Success checkmark |
| Stagger | `--i` + `calc(var(--i) * .1s)` | Сетки карточек |
| Accordion (CSS) | `grid-template-rows: 0fr → 1fr` | Размеры, FAQ |
| Typewriter | `width` + `steps(N)` | Onboarding |
| clip-path morph | `polygon()` → `polygon()` | Баннеры |
| Gradient animation | `background-position` | Aurora-карты |

---

## 8. Большой закомментированный блок — вся библиотека

Ниже — полная библиотека всех анимационных паттернов, изученных в ходе исследования. Весь код намеренно закомментирован и предназначен для справки, копирования отдельных блоков и документирования дизайн-системы.

```css
/* ============================================================
   CSS ANIMATION LIBRARY — FULL REFERENCE
   ============================================================
   Версия: 1.0
   Источник: аудит cont-claude-refac-customer-account-*.html
   
   СОДЕРЖАНИЕ:
   
   A. CSS CUSTOM PROPERTIES (переменные)
   B. @KEYFRAMES — ENTER (появление)
   C. @KEYFRAMES — EXIT (исчезновение)
   D. @KEYFRAMES — ATTENTION (привлечение внимания)
   E. @KEYFRAMES — INFINITE LOOP (бесконечные)
   F. @KEYFRAMES — STATE (состояние и прогресс)
   G. @KEYFRAMES — ADVANCED (продвинутые / не в проекте)
   H. UTILITY CLASSES — animation helpers
   I. TRANSITIONS — hover и интерактив
   J. TRANSFORM — статические трансформации
   K. PERFORMANCE — оптимизация
   L. EASING — cubic-bezier коллекция
   M. ACCESSIBILITY — prefers-reduced-motion
   N. MODERN CSS — новые API (2023+)
   ============================================================ */


/* ============================================================
   A. CSS CUSTOM PROPERTIES
   Централизованные переменные для единообразия.
   Задаются на :root или на .anim-vars-контейнере.
   ============================================================ */

/*
:root {
  --anim-duration-fast:   0.18s;   // мгновенные реакции (ripple, fade)
  --anim-duration-base:   0.3s;    // стандарт для большинства
  --anim-duration-slow:   0.5s;    // сложные enter-анимации
  --anim-duration-xslow:  0.85s;   // progress bar, loading

  --anim-ease-default:    ease;
  --anim-ease-out:        ease-out;
  --anim-ease-in:         ease-in;
  --anim-ease-inout:      ease-in-out;

  // Bounce — overshoot (y2 > 1.0)
  --anim-ease-bounce:     cubic-bezier(0.18, 0.89, 0.32, 1.28);
  --anim-ease-back:       cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --anim-ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);

  // Material Design
  --anim-ease-material:       cubic-bezier(0.25, 0.8, 0.25, 1);
  --anim-ease-material-std:   cubic-bezier(0.4, 0, 0.2, 1);
  --anim-ease-material-accel: cubic-bezier(0.4, 0, 1, 1);
  --anim-ease-material-decel: cubic-bezier(0, 0, 0.2, 1);
}
*/


/* ============================================================
   B. @KEYFRAMES — ENTER (появление)
   
   Все enter-анимации строятся на двух compositor-only
   свойствах: opacity + transform. Никакого layout.
   fill-mode: both или forwards.
   ============================================================ */

/*
// --- fadeInUp (самый частый паттерн в проекте) ---
// Источники: wishlist-appear, viewed-card-in, mysizes-fade-in,
//            payments-fade-in, myreviews-card-in
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);  // 8px–16px в зависимости от контекста
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
// .anim-fade-in-up { animation: fadeInUp 0.3s ease both; }


// --- fadeInDown ---
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-12px); }
  to   { opacity: 1; transform: translateY(0); }
}
// .anim-fade-in-down { animation: fadeInDown 0.3s ease both; }


// --- fadeInLeft ---
@keyframes fadeInLeft {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}
// .anim-fade-in-left { animation: fadeInLeft 0.3s ease both; }


// --- fadeInRight ---
@keyframes fadeInRight {
  from { opacity: 0; transform: translateX(16px); }
  to   { opacity: 1; transform: translateX(0); }
}
// .anim-fade-in-right { animation: fadeInRight 0.3s ease both; }


// --- popIn / zoomIn (bounce easing) ---
// Источники: messages-bubble-in, walletDialogZoomIn
// Ключевой момент: cubic-bezier с y2=1.28 даёт overshoot (пружину)
@keyframes popIn {
  0%   { opacity: 0; transform: scale(0.85) translateY(5px); }
  100% { opacity: 1; transform: scale(1)    translateY(0); }
}
// .anim-pop-in { animation: popIn 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28) both; }


// --- flipInY (3D переворот) ---
// Требует perspective на родителе: perspective: 1000px
// Источник: mywallet карточки
@keyframes flipInY {
  0%   { opacity: 0; transform: perspective(400px) rotateY(90deg); }
  100% { opacity: 1; transform: perspective(400px) rotateY(0deg); }
}
// .anim-flip-in-y { animation: flipInY 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) both; }


// --- slideDown (через grid-template-rows — современный CSS) ---
// Не требует фиксированной высоты. Работает в Chrome 107+, FF 109+, Safari 16+
@keyframes slideDown {
  from { grid-template-rows: 0fr; opacity: 0; }
  to   { grid-template-rows: 1fr; opacity: 1; }
}
// .anim-slide-down > * { overflow: hidden; min-height: 0; }
// .anim-slide-down { display: grid; animation: slideDown 0.3s ease both; }


// --- bounceIn ---
@keyframes bounceIn {
  0%   { opacity: 0; transform: scale(0.3); }
  50%  { opacity: 1; transform: scale(1.08); }
  70%  { transform: scale(0.95); }
  100% { transform: scale(1); }
}
// .anim-bounce-in { animation: bounceIn 0.5s both; }
*/


/* ============================================================
   C. @KEYFRAMES — EXIT (исчезновение)
   
   Exit-анимации ВСЕГДА должны использоваться с JS:
   после окончания анимации элемент нужно убрать из DOM
   или скрыть через display:none / visibility:hidden.
   Слушай событие: element.addEventListener('animationend', cb)
   ============================================================ */

/*
// --- fadeOutLeft ---
// Источник: wishlist-remove
// Используется при "смахивании" элемента из списка
@keyframes fadeOutLeft {
  from { opacity: 1; transform: translateX(0); }
  to   { opacity: 0; transform: translateX(-16px); }
}
// .anim-fade-out-left { animation: fadeOutLeft 0.2s ease-in forwards; }


// --- fadeOutRight ---
@keyframes fadeOutRight {
  from { opacity: 1; transform: translateX(0); }
  to   { opacity: 0; transform: translateX(16px); }
}
// .anim-fade-out-right { animation: fadeOutRight 0.2s ease-in forwards; }


// --- fadeOutDown ---
@keyframes fadeOutDown {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(12px); }
}
// .anim-fade-out-down { animation: fadeOutDown 0.2s ease-in forwards; }


// --- zoomOut ---
@keyframes zoomOut {
  from { opacity: 1; transform: scale(1); }
  to   { opacity: 0; transform: scale(0.85); }
}
// .anim-zoom-out { animation: zoomOut 0.2s ease-in forwards; }


// --- flyOut (резкий вылет вверх) ---
@keyframes flyOut {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-32px); }
}
// .anim-fly-out { animation: flyOut 0.3s ease-in forwards; }
*/


/* ============================================================
   D. @KEYFRAMES — ATTENTION (привлечение внимания)
   
   Однократные (forwards) или короткие animate-and-stop.
   Всегда должны заканчиваться в исходном состоянии
   или через fill-mode: forwards.
   ============================================================ */

/*
// --- shakeHorizontal ---
// Источник: myreviews-shake
// Классический индикатор ошибки. 4 осцилляции за 0.4s
@keyframes shakeHorizontal {
  0%, 100% { transform: translateX(0); }
  20%, 60%  { transform: translateX(-6px); }
  40%, 80%  { transform: translateX(6px); }
}
// .anim-shake { animation: shakeHorizontal 0.4s ease forwards; }


// --- shakeVertical ---
@keyframes shakeVertical {
  0%, 100% { transform: translateY(0); }
  20%, 60%  { transform: translateY(-4px); }
  40%, 80%  { transform: translateY(4px); }
}
// .anim-shake-v { animation: shakeVertical 0.4s ease forwards; }


// --- heartbeat (double pulse) ---
// Для кнопок "лайк", "избранное"
@keyframes heartbeat {
  0%   { transform: scale(1); }
  14%  { transform: scale(1.3); }
  28%  { transform: scale(1); }
  42%  { transform: scale(1.2); }
  70%  { transform: scale(1); }
}
// .anim-heartbeat { animation: heartbeat 0.6s ease both; }


// --- wiggle ---
// Уведомление о новом элементе, badge
@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  15%       { transform: rotate(-8deg); }
  30%       { transform: rotate(8deg); }
  45%       { transform: rotate(-5deg); }
  60%       { transform: rotate(5deg); }
  75%       { transform: rotate(-2deg); }
}
// .anim-wiggle { animation: wiggle 0.6s ease both; }


// --- tada ---
// Комбинированный scale + rotate, более театральный
@keyframes tada {
  0%   { transform: scale(1) rotate(0deg); }
  10%, 20% { transform: scale(0.9) rotate(-3deg); }
  30%, 50%, 70%, 90% { transform: scale(1.1) rotate(3deg); }
  40%, 60%, 80%      { transform: scale(1.1) rotate(-3deg); }
  100% { transform: scale(1) rotate(0deg); }
}
// .anim-tada { animation: tada 0.8s ease both; }
*/


/* ============================================================
   E. @KEYFRAMES — INFINITE LOOP (бесконечные)
   
   Используют animation-iteration-count: infinite.
   ВАЖНО: снимать класс (или animation: none) когда
   элемент уходит из viewport для экономии GPU.
   ============================================================ */

/*
// --- shimmer (skeleton loading) ---
// Источник: viewed-items shimmer
// Применяется через ::after с overflow: hidden на родителе
@keyframes shimmerSweep {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(200%); }
}
// .anim-shimmer {
//   position: relative;
//   overflow: hidden;
//   background-color: var(--skeleton-base, #e2e8f0);
// }
// .anim-shimmer::after {
//   content: "";
//   position: absolute;
//   inset: 0;
//   background: linear-gradient(
//     90deg,
//     transparent 0%,
//     rgba(255, 255, 255, 0.7) 50%,
//     transparent 100%
//   );
//   animation: shimmerSweep 1.5s ease-in-out infinite;
// }


// --- pulseGlow (ripple box-shadow) ---
// Источник: stepPulse (orders)
// box-shadow анимируется через paint layer, но приемлемо для slow pulse
@keyframes pulseGlow {
  0%   { box-shadow: 0 0 0 0   rgba(14, 165, 233, 0.45); }
  70%  { box-shadow: 0 0 0 12px rgba(14, 165, 233, 0); }
  100% { box-shadow: 0 0 0 0   rgba(14, 165, 233, 0); }
}
// .anim-pulse { animation: pulseGlow 2s ease-out infinite; }


// --- bounceY (typing indicator) ---
// Источник: messages-dot-bounce
// Применяется к 3 точкам с animation-delay для волнового эффекта:
// .dot:nth-child(1) { animation-delay: 0s; }
// .dot:nth-child(2) { animation-delay: 0.2s; }
// .dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounceY {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}
// .anim-bounce { animation: bounceY 1.2s ease-in-out infinite; }


// --- spin (spinner) ---
@keyframes spinCW {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
// .anim-spin { animation: spinCW 1s linear infinite; }


// --- breathe (медленный живой пульс) ---
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%       { transform: scale(1.04); opacity: 0.85; }
}
// .anim-breathe { animation: breathe 3s ease-in-out infinite; }


// --- float (floating badge / element) ---
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}
// .anim-float { animation: float 3s ease-in-out infinite; }
*/


/* ============================================================
   F. @KEYFRAMES — STATE (состояние и прогресс)
   
   Анимируют видимый переход между двумя логическими
   состояниями UI. Часто однократные.
   ============================================================ */

/*
// --- progress bar fill ---
// Источник: orders progress (transition, не @keyframes)
// Вариант через @keyframes для более сложных сценариев
@keyframes progressFill {
  from { width: 0%; }
  to   { width: var(--progress-target, 100%); }
}
// .anim-progress { animation: progressFill 0.85s cubic-bezier(.4, 0, .2, 1) both; }
// Использование: <div class="anim-progress" style="--progress-target: 65%">


// --- SVG stroke draw (рисующийся checkmark/иконка) ---
// Для работы нужно знать длину пути: path.getTotalLength()
// Пример: длина 120px → stroke-dasharray: 120; stroke-dashoffset: 120 → 0
@keyframes strokeDraw {
  from { stroke-dashoffset: var(--stroke-length, 100); }
  to   { stroke-dashoffset: 0; }
}
// svg path.anim-draw {
//   stroke-dasharray: var(--stroke-length, 100);
//   stroke-dashoffset: var(--stroke-length, 100);
//   animation: strokeDraw 0.5s ease-out forwards;
// }


// --- typewriter эффект ---
// Шрифт ДОЛЖЕН быть monospace для корректной пошаговой анимации
// steps(N) — N = количество символов в тексте
@keyframes typing {
  from { width: 0; }
  to   { width: 100%; }
}
@keyframes cursorBlink {
  from, to { border-color: transparent; }
  50%       { border-color: currentColor; }
}
// .anim-typewriter {
//   overflow: hidden;
//   white-space: nowrap;
//   width: 0;
//   font-family: monospace;
//   border-right: 2px solid;
//   animation:
//     typing 2s steps(30, end) forwards,
//     cursorBlink 0.75s step-end infinite;
// }
*/


/* ============================================================
   G. @KEYFRAMES — ADVANCED (продвинутые / не в проекте)
   
   Паттерны из неисследованной территории.
   Требуют внимания к браузерной поддержке.
   ============================================================ */

/*
// --- clip-path morph ---
// Оба polygon() должны иметь одинаковое количество точек
@keyframes morphShape {
  from { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }  // прямоугольник
  to   { clip-path: polygon(50% 0, 100% 100%, 0 100%, 50% 0); } // треугольник
}
// .anim-morph { animation: morphShape 0.5s ease both; }


// --- gradient sweep (aurora effect) ---
// Анимирует background-position, не сам градиент (нельзя напрямую)
@keyframes gradientSweep {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
// .anim-aurora {
//   background: linear-gradient(270deg, #0ea5e9, #8b5cf6, #ec4899);
//   background-size: 300% 300%;
//   animation: gradientSweep 4s ease infinite;
// }


// --- stagger через CSS custom property ---
// JS устанавливает --i для каждого элемента:
// el.style.setProperty('--i', index);
// Или через :nth-child в CSS:
// li:nth-child(1) { --i: 0; }
// li:nth-child(2) { --i: 1; }
// ...
// .stagger-item {
//   animation: fadeInUp 0.3s ease both;
//   animation-delay: calc(var(--i, 0) * 0.08s);
// }


// --- motion path (движение по SVG-пути) ---
// Браузерная поддержка: Chrome 84+, Firefox 97+, Safari 15.4+
@keyframes moveAlongPath {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}
// .anim-motion-path {
//   offset-path: path('M 10,80 Q 95,10 180,80 T 340,80');
//   offset-rotate: auto;           // ориентирует элемент вдоль пути
//   animation: moveAlongPath 2s ease-in-out infinite;
// }
*/


/* ============================================================
   H. UTILITY CLASSES — animation helpers
   
   Готовые классы для подключения анимаций.
   Добавляются/убираются JS-ом через classList.
   ============================================================ */

/*
// Базовые входящие
// .is-entering  { animation: fadeInUp var(--anim-duration-base, 0.3s) ease both; }
// .is-exiting   { animation: fadeOutLeft var(--anim-duration-fast, 0.18s) ease-in forwards; }
// .is-error     { animation: shakeHorizontal 0.4s ease forwards; }
// .is-loading   { animation: shimmerSweep 1.5s ease-in-out infinite; }
// .is-attention { animation: pulseGlow 2s ease-out infinite; }

// Управление воспроизведением
// .anim-paused  { animation-play-state: paused; }
// .anim-running { animation-play-state: running; }
// .no-anim      { animation: none !important; transition: none !important; }

// Задержки для stagger (можно расширять)
// .delay-1 { animation-delay: 0.05s; }
// .delay-2 { animation-delay: 0.10s; }
// .delay-3 { animation-delay: 0.15s; }
// .delay-4 { animation-delay: 0.20s; }
// .delay-5 { animation-delay: 0.25s; }
*/


/* ============================================================
   I. TRANSITIONS — hover и интерактив
   
   Все паттерны, найденные в проекте.
   Применяются к базовому состоянию элемента,
   срабатывают при :hover, :focus, .is-active и т.д.
   ============================================================ */

/*
// --- hover lift (карточки, платёжные методы) ---
// Найдено в: wallet, payments, wishlist
// .card {
//   transition: transform 0.2s ease, box-shadow 0.2s ease;
// }
// .card:hover {
//   transform: translateY(-2px);
//   box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.12);
// }


// --- scale on hover (изображения, промо) ---
// Найдено в: promo-zero, viewed-items
// Контейнер: overflow: hidden, чтобы картинка не вылезала
// .card-img-wrapper { overflow: hidden; }
// .card-img-wrapper img {
//   transition: transform 0.4s ease;
// }
// .card-img-wrapper:hover img {
//   transform: scale(1.08);
// }


// --- color transition (кнопки, табы, чипсы) ---
// Найдено во всех файлах
// .btn {
//   transition: background-color 0.18s ease, color 0.18s ease, border-color 0.18s ease;
// }


// --- комбинированный (border + transform + color) ---
// Найдено в: wallet payment method cards
// .payment-card {
//   transition: border-color 0.3s ease, transform 0.3s ease, color 0.3s ease, background 0.3s ease;
// }
// .payment-card.is-selected,
// .payment-card:hover {
//   border-color: var(--accent-color);
//   transform: translateY(-2px) scale(1.01);
// }


// --- progress bar width ---
// Найдено в: orders (transition, не @keyframes)
// .progress-fill {
//   transition: width 0.85s cubic-bezier(.4, 0, .2, 1);
// }


// --- 3D flip card ---
// Найдено в: mywallet
// .card-3d-scene {
//   perspective: 1000px;
// }
// .card-3d {
//   transform-style: preserve-3d;
//   transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
//   backface-visibility: hidden;
// }
// .card-3d.is-flipped {
//   transform: rotateY(180deg);
// }
// .card-3d-front, .card-3d-back {
//   backface-visibility: hidden;
// }
// .card-3d-back {
//   transform: rotateY(180deg);
// }


// --- opacity + visibility (правильный паттерн для доступности) ---
// Никогда не анимировать только opacity без visibility,
// иначе элемент остаётся кликабельным когда opacity: 0
// .tooltip {
//   opacity: 0;
//   visibility: hidden;
//   transition: opacity 0.2s ease, visibility 0.2s ease;
//   pointer-events: none;
// }
// .tooltip.is-visible {
//   opacity: 1;
//   visibility: visible;
//   pointer-events: auto;
// }
*/


/* ============================================================
   J. TRANSFORM — статические трансформации
   
   Найденные значения transform в проекте (без анимации).
   Используются как конечные состояния в :hover или @keyframes.
   ============================================================ */

/*
// Translate (найденные значения)
// transform: translateY(-2px);   // hover lift малый
// transform: translateY(-4px);   // hover lift средний
// transform: translateY(-10px);  // hover lift большой
// transform: translateY(12px);   // начало fadeInUp
// transform: translateX(-6px);   // фаза shake влево
// transform: translateX(6px);    // фаза shake вправо

// Scale (найденные значения)
// transform: scale(0.85);        // начало popIn
// transform: scale(0.9);         // альтернативный popIn start
// transform: scale(1);           // нормальное состояние
// transform: scale(1.01);        // selected payment card
// transform: scale(1.04);        // hover button
// transform: scale(1.05);        // hover promo card
// transform: scale(1.1);         // hover icon
// transform: scale(1.15);        // акцентированный hover
// transform: scale(1.35);        // zoom image on hover

// Rotate
// transform: rotate(-45deg);     // иконка (крестик закрытия)

// Комбинированные
// transform: translateY(-2px) scale(1.01);  // selected card lift
*/


/* ============================================================
   K. PERFORMANCE — оптимизация
   
   Все перформанс-свойства, найденные и рекомендованные.
   ============================================================ */

/*
// --- will-change — GPU hint ---
// Найдено в проекте:
// will-change: transform;
// will-change: transform, opacity;
//
// Правила использования:
// 1. Добавлять ПЕРЕД началом анимации (через JS или постоянно)
// 2. Снимать ПОСЛЕ завершения анимации
// 3. Не применять к слишком многим элементам — каждый создаёт compositor layer
//
// Паттерн с JS:
// element.addEventListener('mouseenter', () => element.style.willChange = 'transform');
// element.addEventListener('animationend', () => element.style.willChange = 'auto');
// element.addEventListener('mouseleave', () => element.style.willChange = 'auto');


// --- contain — ограничение reflow ---
// Изолирует элемент от влияния на внешний layout
// contain: layout;           // дочерние не влияют на внешний layout
// contain: style;            // счётчики и подобное изолированы
// contain: paint;            // не рисуется вне границ (как overflow:hidden)
// contain: layout style;     // комбинация (найдено как рекомендация)
// contain: strict;           // всё сразу (layout + style + paint + size)


// --- animation cleanup паттерн (найден как комментарий в проекте) ---
// После завершения однократной анимации снимаем GPU-слой:
//
// element.addEventListener('animationend', () => {
//   element.style.willChange = 'auto';
//   element.style.animation = '';  // или конкретный класс убрать
// }, { once: true });


// --- IntersectionObserver для infinite-loop анимаций ---
// Ставит анимацию на паузу когда элемент вне viewport:
//
// const observer = new IntersectionObserver((entries) => {
//   entries.forEach(el => {
//     el.target.style.animationPlayState =
//       el.isIntersecting ? 'running' : 'paused';
//   });
// });
// document.querySelectorAll('.anim-shimmer, .anim-pulse').forEach(el => observer.observe(el));
*/


/* ============================================================
   L. EASING — cubic-bezier коллекция
   
   Все кривые, найденные в проекте + полная справка.
   Для визуализации: https://cubic-bezier.com
   ============================================================ */

/*
// === НАЙДЕНЫ В ПРОЕКТЕ ===

// Bounce / PopIn — overshoot, y2 > 1.0
// cubic-bezier(0.18, 0.89, 0.32, 1.28)    — messages-bubble-in, walletDialogZoomIn
// cubic-bezier(0.175, 0.885, 0.32, 1.275) — 3D flip карты (easeOutBack)
// cubic-bezier(0.34, 1.56, 0.64, 1)       — сильный spring (рекомендован для добавления)

// Material Design
// cubic-bezier(0.25, 0.8, 0.25, 1)        — hover transform (standard)
// cubic-bezier(0.4, 0, 0.2, 1)            — progress bar (standard)
// cubic-bezier(0.4, 0, 1, 1)              — accelerate (ease-in вариант)
// cubic-bezier(0, 0, 0.2, 1)             — decelerate (ease-out вариант)


// === ПОЛНАЯ КОЛЛЕКЦИЯ (Robert Penner easings) ===

// Quad
// ease-in-quad:      cubic-bezier(0.55, 0.085, 0.68, 0.53)
// ease-out-quad:     cubic-bezier(0.25, 0.46, 0.45, 0.94)
// ease-in-out-quad:  cubic-bezier(0.455, 0.03, 0.515, 0.955)

// Cubic
// ease-in-cubic:     cubic-bezier(0.55, 0.055, 0.675, 0.19)
// ease-out-cubic:    cubic-bezier(0.215, 0.61, 0.355, 1)
// ease-in-out-cubic: cubic-bezier(0.645, 0.045, 0.355, 1)

// Quart
// ease-in-quart:     cubic-bezier(0.895, 0.03, 0.685, 0.22)
// ease-out-quart:    cubic-bezier(0.165, 0.84, 0.44, 1)
// ease-in-out-quart: cubic-bezier(0.77, 0, 0.175, 1)

// Expo
// ease-in-expo:      cubic-bezier(0.95, 0.05, 0.795, 0.035)
// ease-out-expo:     cubic-bezier(0.19, 1, 0.22, 1)
// ease-in-out-expo:  cubic-bezier(1, 0, 0, 1)

// Back (overshoot)
// ease-in-back:      cubic-bezier(0.6, -0.28, 0.735, 0.045)
// ease-out-back:     cubic-bezier(0.175, 0.885, 0.32, 1.275)
// ease-in-out-back:  cubic-bezier(0.68, -0.55, 0.265, 1.55)

// Новый CSS linear() синтаксис (2023+) — пружина без JS
// animation-timing-function: linear(
//   0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%,
//   0.938 16.7%, 1.077, 1.121, 1.077 24.3%, 0.996 28%, 1
// );
*/


/* ============================================================
   M. ACCESSIBILITY — доступность
   
   ОБЯЗАТЕЛЬНЫЙ БЛОК. Отсутствовал в проекте.
   Добавить в глобальный CSS (base.css / reset.css).
   ============================================================ */

/*
// --- prefers-reduced-motion ---
// Пользователи с вестибулярными расстройствами могут
// включить "уменьшить движение" в настройках ОС.
// CSS реагирует через этот медиа-запрос.

@media (prefers-reduced-motion: reduce) {
  // Вариант 1: полное отключение всех анимаций
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    transition-delay: 0ms !important;
    scroll-behavior: auto !important;
  }
}

@media (prefers-reduced-motion: no-preference) {
  // Вариант 2 (предпочтительнее): анимации только для тех,
  // кто НЕ просил уменьшить движение
  // .card { transition: transform 0.3s ease; }
  // .anim-fade-in-up { animation: fadeInUp 0.3s ease both; }
}


// --- focus-visible для клавиатурной навигации ---
// Анимация фокуса только для клавиатуры, не для мыши:
// *:focus { outline: none; }
// *:focus-visible {
//   outline: 2px solid var(--accent-color);
//   outline-offset: 2px;
//   transition: outline-offset 0.1s ease;
// }
*/


/* ============================================================
   N. MODERN CSS — новые API (2023+)
   
   Браузерная поддержка: проверять на caniuse.com
   Не используются в проекте — исследовательский раздел.
   ============================================================ */

/*
// --- Scroll-driven animations (Chrome 115+) ---
// Анимация привязана к прокрутке страницы или контейнера.
// Замена JS IntersectionObserver для простых случаев.

// @keyframes fadeInScroll {
//   from { opacity: 0; transform: translateY(20px); }
//   to   { opacity: 1; transform: translateY(0); }
// }
// .scroll-reveal {
//   animation: fadeInScroll linear both;
//   animation-timeline: view();           // привязка к viewport
//   animation-range: entry 0% entry 30%; // когда элемент входит в view
// }

// Прогресс-бар страницы (читалка):
// .reading-progress {
//   animation: progressFill linear;
//   animation-timeline: scroll(root);    // привязка к корневому скроллу
// }


// --- View Transition API (Chrome 111+, Safari 18+) ---
// Кинематографические переходы между состояниями без GSAP.
// CSS:
// .hero-image { view-transition-name: hero; }
// ::view-transition-old(hero) { animation: slideOut 0.4s ease; }
// ::view-transition-new(hero) { animation: slideIn 0.4s ease; }
//
// JS запуск:
// document.startViewTransition(() => {
//   updateDOM();  // любое изменение DOM
// });


// --- CSS @property (Houdini, Chrome 85+) ---
// Делает custom properties анимируемыми.
// Без @property браузер не знает тип и не интерполирует.

// @property --gradient-angle {
//   syntax: '<angle>';
//   initial-value: 0deg;
//   inherits: false;
// }
// @keyframes rotateGradient {
//   to { --gradient-angle: 360deg; }
// }
// .rotating-border {
//   background: conic-gradient(from var(--gradient-angle), #0ea5e9, #8b5cf6, #0ea5e9);
//   animation: rotateGradient 3s linear infinite;
// }


// --- CSS @layer + анимации ---
// Организация анимаций по слоям (specificity control)
// @layer base, components, animations;
// @layer animations {
//   .anim-fade-in-up { animation: fadeInUp 0.3s ease both; }
// }


// --- anchor positioning (2024) ---
// Позиционирование относительно другого элемента.
// Актуально для tooltip-анимаций с правильной привязкой.
// .tooltip {
//   position-anchor: --target;
//   top: anchor(bottom);
//   transition: opacity 0.2s ease;
// }
*/


/* ============================================================
   END OF CSS ANIMATION LIBRARY REFERENCE
   
   Быстрый старт:
   1. Скопировать нужный @keyframes (раскомментировать)
   2. Добавить utility-класс или встроить в компонент
   3. Убедиться что анимирует только transform/opacity (перформанс)
   4. Добавить prefers-reduced-motion в глобальный CSS
   5. Тестировать с DevTools: Rendering → Emulate CSS media → prefers-reduced-motion

   Полезные ссылки:
   - https://cubic-bezier.com       — визуализация кривых
   - https://easings.net            — коллекция именованных easing
   - https://csstriggers.com        — какие свойства вызывают layout/paint
   - https://animista.net           — генератор @keyframes
   - https://caniuse.com            — поддержка браузерами
   ============================================================ */
```

---

*Руководство основано на аудите 11 компонентов customer account section. Версия 1.0.*
