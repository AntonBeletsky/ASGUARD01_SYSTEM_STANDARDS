# Kill Fucked Customization — Make Clean Bootstrap

> **Одно правило**: кастомный CSS пишется только тогда, когда Bootstrap физически не может этого сделать.
> Всё остальное — utility-классы в HTML. Вопрос перед каждым правилом: *«Что именно тут уникального?»* Если ответ — «ничего» — правило умирает.

---

## Содержание

1. [Дерево решений](#1-дерево-решений)
2. [Фаза 0 — Заморозить токены](#2-фаза-0--заморозить-токены)
3. [Фаза 1 — Убить font-size-only классы](#3-фаза-1--убить-font-size-only-классы)
4. [Фаза 2 — Слить дубли компонентов](#4-фаза-2--слить-дубли-компонентов)
5. [Фаза 3 — Заменить кастомные табы на nav-underline](#5-фаза-3--заменить-кастомные-табы-на-nav-underline)
6. [Фаза 4 — Убить структурный CSS страницы](#6-фаза-4--убить-структурный-css-страницы)
7. [Фаза 5 — Почистить JS-шаблоны](#7-фаза-5--почистить-js-шаблоны)
8. [Фаза 6 — Проверка состояний и dark mode](#8-фаза-6--проверка-состояний-и-dark-mode)
9. [Таблица замен: токены](#9-таблица-замен-токены)
10. [Таблица замен: CSS-классы → BS utilities](#10-таблица-замен-css-классы--bs-utilities)
11. [Таблица замен: компоненты](#11-таблица-замен-компоненты)
12. [Что остаётся кастомным — и почему](#12-что-остаётся-кастомным--и-почему)
13. [Финальный чеклист](#13-финальный-чеклист)

---

## 1. Дерево решений

Прогонять **каждое** CSS-правило через этот фильтр до начала любых правок.

```
Есть кастомное CSS-правило
         │
         ▼
Bootstrap utility делает то же самое?
    ДА  ──►  УБИТЬ правило, поставить utility в HTML
         │
        НЕТ
         ▼
Класс нужен как JS-хук, но Bootstrap utility покрывает стиль?
    ДА  ──►  ЗАМЕНИТЬ: убрать CSS, добавить BS-класс в HTML/JS-шаблон
         │
        НЕТ
         ▼
Это дублирует другой кастомный класс?
    ДА  ──►  СЛИТЬ в один класс, удалить остальные
         │
        НЕТ
         ▼
Правило содержит свойства, которые BS уже даёт?
    ДА  ──►  УРЕЗАТЬ: оставить только уникальные свойства,
             остальные убрать и поставить utility
         │
        НЕТ
         ▼
    ОСТАВИТЬ без изменений
    (уникальная логика — нет BS-эквивалента)
```

**Пять исходов:** УБИТЬ / ЗАМЕНИТЬ / СЛИТЬ / УРЕЗАТЬ / ОСТАВИТЬ.
Нет шестого. Нет «оставить пока» и «может пригодится».

---

## 2. Фаза 0 — Заморозить токены

**Делать первым.** Если начать с правил, а не с токенов — при удалении классов останутся мёртвые `var(--custom-*)` ссылки, которые ничего не делают, но засоряют CSS.

### Алгоритм

1. Выписать все кастомные `--prefix-*` токены из `:root` / контейнера.
2. Для каждого найти Bootstrap-аналог по таблице ниже.
3. Если аналог есть — токен **удаляется**, все `var(--prefix-*)` в правилах меняются на `var(--bs-*)`.
4. Если аналога нет — токен **остаётся**, но переносится на контейнер виджета, а не на `:root`.

### Почему токены нельзя оставлять на `:root`

Кастомный токен на `:root` — это глобальная переменная. Если на странице два разных виджета используют один и тот же токен-имя с разными значениями, они конфликтуют. Bootstrap сам держит свои токены на `:root`, мы не конкурируем с его пространством имён. Всё кастомное — только на `.widget-container`:

```css
/* ❌ Неправильно — глобальный scope */
:root {
  --rv-brand: #1a56db;
  --rv-radius: 14px;
}

/* ✅ Правильно — scope на контейнер */
.rv-page {
  --rv-star: #f59e0b; /* остаётся: нет BS-аналога */
}
```

### Чего не трогаем

`--rv-bar-pct` и подобные **динамические** токены, которые JS ставит через `element.style.setProperty()` — это не design-токены, это механизм передачи данных из JS в CSS. Их не трогаем.

---

## 3. Фаза 1 — Убить font-size-only классы

Самая большая категория мусора. Паттерн выглядит так:

```css
/* ❌ Это и есть «font-size-only» класс — убить */
.rv-card-meta  { font-size: 13px; }
.rv-card-title { font-size: 15px; }
.rv-form-label { font-size: 14px; }
```

### Правило

Если **единственное** свойство класса — `font-size`, и это значение совпадает с Bootstrap-утилитой или с базовым размером шрифта — класс не нужен.

### Таблица соответствий font-size → BS utility

| Значение | Bootstrap utility | Примечание |
|---|---|---|
| `≈ 11–12px` | `small` | `0.875em` от родителя |
| `13px` | `small` | близко, принять |
| `14px` | *(ничего)* | базовый размер BS по умолчанию — класс не нужен |
| `15px` | *(ничего)* | убрать класс, оставить как есть |
| `1rem / 16px` | *(ничего)* | базовый размер — класс не нужен |
| `1.25rem / 20px` | `fs-5` | |
| `1.5rem / 24px` | `fs-4` | |
| `2rem / 32px` | `fs-3` | |
| `2rem+` | `fs-2`, `fs-1` | |
| `< 12px` | `small` + кастом | только если дизайн требует |

### Как заменять

Класс удаляется из CSS. В HTML или в JS-шаблоне (innerHTML-строках) класс заменяется на BS utility:

```html
<!-- ❌ До -->
<span class="rv-card-meta">Jan 15, 2025</span>
<h2 class="rv-card-title">Product Name</h2>

<!-- ✅ После -->
<span class="small text-secondary">Jan 15, 2025</span>
<h2 class="fw-semibold">Product Name</h2>
```

### Особый случай: `font-size` + ещё что-то

Если класс делает `font-size` И что-то ещё — класс не убивается полностью. Проходим через дерево решений: если оставшиеся свойства тоже покрывает BS — убиваем. Если нет — урезаем: удаляем `font-size`, оставляем уникальное:

```css
/* ❌ До — font-size + ещё одно свойство */
.rv-bar-label { font-size: 13px; width: 44px; }
.rv-bar-count { font-size: 13px; width: 24px; text-align: right; }

/* ✅ После — убрали font-size (→ small в HTML), оставили уникальное */
.rv-page .rv-bar-label { width: 44px; }
.rv-page .rv-bar-count { width: 24px; text-align: right; }
```

---

## 4. Фаза 2 — Слить дубли компонентов

Bootstrap-проекты часто растут органически: сначала `.product-card`, потом `.comment-card`, потом `.stat-card` — и у всех одинаковые `border`, `border-radius`, `box-shadow`. Это копипаст, замаскированный под разные классы.

### Как найти дубли

```bash
# Быстрый поиск одинаковых наборов свойств
grep -A5 "box-shadow:" style.css | sort | uniq -d
```

Или просто визуально: если два класса отличаются только именем и имеют одинаковые `border`, `radius`, `shadow` — это дубли.

### Стратегия слияния

1. Выбрать **один** базовый класс (обычно самый первый или самый общий).
2. В HTML/JS заменить все остальные классы на базовый.
3. Уникальные свойства каждого варианта — вынести в модификаторы:

```css
/* ❌ До — три копии одного блока */
.rv-card {
  border-radius: 14px;
  border: 1px solid var(--bs-border-color-translucent);
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.05);
  transition: box-shadow .18s ease;
  overflow: hidden;
}
.rv-comment-card {
  border-radius: 14px;
  border: 1px solid var(--bs-border-color-translucent);
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.05);
  transition: box-shadow .18s ease;
}
.rv-stat-card {
  border-radius: 14px;
  border: 1px solid var(--bs-border-color-translucent);
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.05);
  padding: 1rem 1.2rem;
  background: var(--bs-body-bg);
}

/* ✅ После — один базовый класс + Bootstrap утилиты */
/* padding и bg идут через p-3, bg-body прямо в HTML */
.rv-page .rv-card {
  box-shadow: var(--bs-box-shadow-sm);
  transition: box-shadow .18s ease;
  overflow: hidden; /* только это нельзя сделать utility */
}
.rv-page .rv-card:hover {
  box-shadow: var(--bs-box-shadow);
}
```

```html
<!-- rv-stat-card получает p-3 bg-body прямо в HTML -->
<div class="rv-card card rounded-3 p-3 bg-body">...</div>
```

### После слияния — урезать до уникального

После того как дубли слиты в один класс, этот один класс снова прогоняется через дерево решений. Часто оказывается, что теперь в нём уже нет ничего, что BS не умеет, кроме одного-двух свойств.

---

## 5. Фаза 3 — Заменить кастомные табы на nav-underline

Bootstrap 5.3 добавил `.nav-underline` — подчёркивающие табы с transition. Если в проекте есть кастомный стиль табов через `.nav-link`, который рисует `border-bottom: 2px solid` при активном состоянии — это `.nav-underline`, написанный руками.

### Как опознать

```css
/* Признак: border-bottom на nav-link + смена цвета на .active */
.my-tabs .nav-link {
  border-bottom: 2px solid transparent;
  transition: color .18s ease, border-color .18s ease;
}
.my-tabs .nav-link.active {
  border-bottom-color: var(--bs-primary);
}
```

Это `.nav-underline`. Весь блок — в мусор.

### Замена

```html
<!-- ❌ До -->
<ul class="nav my-tabs">
  <li class="nav-item">
    <button class="nav-link active" ...>Tab 1</button>
  </li>
</ul>

<!-- ✅ После -->
<ul class="nav nav-underline">
  <li class="nav-item">
    <button class="nav-link active" ...>Tab 1</button>
  </li>
</ul>
```

Весь кастомный CSS блока табов удаляется. Bootstrap берёт на себя цвет, `border-bottom`, transition, состояния `:hover` и `.active`.

### Если цвет активного таба отличается от `--bs-primary`

Оставляем **одну строку** переопределения:

```css
/* Единственное, что остаётся от всего блока кастомных табов */
.rv-page .nav-underline .nav-link.active {
  color: var(--rv-brand); /* если бренд-цвет отличается от BS primary */
  border-bottom-color: var(--rv-brand);
}
```

---

## 6. Фаза 4 — Убить структурный CSS страницы

### Глобальный `body` override — всегда ошибка

```css
/* ❌ Это нельзя делать — ломает все остальные компоненты страницы */
body {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
}
```

Компонент не владеет `body`. Если шрифт нужен — он подключается через BS-переопределение `--bs-font-sans-serif` на контейнере виджета:

```css
/* ✅ Правильно — только внутри компонента */
.rv-page {
  --bs-font-sans-serif: 'DM Sans', sans-serif;
  font-size: 0.9375rem; /* 15px через em */
}
```

Но в большинстве случаев и это не нужно — если дизайн-система проекта уже задаёт нужный шрифт глобально.

### Кастомный контейнер-центровщик — заменить на BS container

```css
/* ❌ До — кастомная центровка */
.rv-page { max-width: 860px; margin-inline: auto; }
```

Bootstrap имеет готовые контейнеры. Выбрать ближайший:

| BS класс | Max-width | Когда использовать |
|---|---|---|
| `container-sm` | 540px | узкие формы |
| `container-md` | 720px | средние виджеты |
| `container-lg` | 960px | стандартные страницы |
| `container-xl` | 1140px | широкие дашборды |
| `container` | адаптивный | универсально |

860px ≈ `container-lg` (960px). Разница 100px — принять. Кастомный `max-width` убирается, в HTML ставится `container-lg`:

```html
<!-- ❌ До -->
<div class="rv-page">

<!-- ✅ После -->
<div class="rv-page container-lg">
```

Если `860px` критично и `container-lg` не подходит — переопределить через BS-переменную, не писать отдельный класс:

```css
/* Переопределение BS-переменной контейнера — не кастомный класс */
.rv-page { --bs-container-lg-max-width: 860px; }
```

---

## 7. Фаза 5 — Почистить JS-шаблоны

Когда компонент генерирует HTML через `innerHTML` в JS — классы живут в строках вида:

```js
return `<span class="rv-card-meta">${this._esc(p.date)}</span>`;
```

После удаления CSS-правил нужно обновить эти строки. Алгоритм тот же: убитый класс → BS utility в строку шаблона.

### Правила безопасности

- В JS-шаблонах применяются только **статические** Bootstrap-классы (строки-литералы). Динамические значения всегда через `_esc()` или `textContent` — не как часть класса.
- Никогда: `` `class="${userInput}"` `` — это XSS.
- Допустимо: `` `class="badge rounded-pill ${this._esc(badgeClass)}"` `` — если `badgeClass` берётся из доверенного конфига (`STATUS_MAP`), не от пользователя.

### Типичные замены в шаблонах

```js
// ❌ До — кастомные классы
`<span class="rv-card-meta">${date}</span>`
`<p class="rv-card-text">${text}</p>`
`<h2 class="rv-card-title">${name}</h2>`
`<span class="rv-badge-status text-bg-success">Published</span>`
`<div class="rv-section-hdr">Label</div>`

// ✅ После — Bootstrap utilities
`<span class="small text-secondary">${date}</span>`
`<p class="mb-2">${text}</p>`
`<h2 class="fw-semibold">${name}</h2>`
`<span class="badge rounded-pill text-bg-success">Published</span>`
`<div class="small text-secondary text-uppercase fw-semibold">Label</div>`
```

### Outgoing-комментарии: bg-tint через data-атрибут

Если компонент добавляет фоновый тинт через CSS-селектор `[data-comment-type="outgoing"]` с кастомным токеном — убираем CSS, добавляем BS-класс прямо в JS-шаблон:

```js
// ❌ До — CSS делает bg через data-атрибут с кастомным цветом
// CSS: .rv-comment-card[data-comment-type="outgoing"] { background: var(--rv-brand-soft); }
const cardClass = `rv-comment-card`;

// ✅ После — BS utility прямо в шаблоне, нет кастомного CSS
const tintClass = c.type === 'outgoing' ? 'bg-primary-subtle' : '';
const cardClass = `rv-card card rounded-3 ${tintClass}`;
```

---

## 8. Фаза 6 — Проверка состояний и dark mode

### Dark mode

Bootstrap 5.3 переключает тему через `data-bs-theme="dark"` на `<html>`. Все `--bs-*` переменные при этом автоматически меняют значения. Кастомные `var(--rv-*)` токены — нет.

**Тест:** добавить `data-bs-theme="dark"` на `<html>`, пройтись по компоненту. Если что-то сломалось — там остался хардкодный цвет или кастомный токен без dark-mode варианта.

**Фикс:** каждый оставшийся кастомный токен должен иметь dark-mode переопределение:

```css
.rv-page {
  --rv-star: #f59e0b; /* светлая тема — янтарный */
}

[data-bs-theme="dark"] .rv-page {
  --rv-star: #fbbf24; /* тёмная тема — чуть светлее */
}
```

Для фонов и текстов — использовать только `--bs-*` семантические переменные, они уже адаптированы:

```css
/* ✅ Автоматически адаптируется к dark mode */
background: var(--bs-body-bg);
color: var(--bs-body-color);
border-color: var(--bs-border-color);

/* ❌ Не адаптируется */
background: #ffffff;
color: #212529;
```

### Проверка состояний через data-атрибуты

После рефакторинга убедиться, что JS по-прежнему правильно ставит `data-state` / `data-*` атрибуты, на которые завязан оставшийся кастомный CSS:

```js
// Эти механизмы должны работать после чистки:
el.dataset.state = 'liked';         // → .rv-helpful-btn[data-state="liked"]
article.dataset.new = 'true';       // → .rv-card[data-new="true"] { animation }
picker.classList.add('is-invalid'); // → .rv-star-picker.is-invalid { animation }
```

### Проверка responsive

Единственный кастомный `@media`, который обычно остаётся — фиксированные размеры изображений/аватаров на mobile. Bootstrap не умеет менять конкретные пиксельные размеры через утилиты:

```css
/* Остаётся — нет BS-аналога для точных размеров thumb */
@media (max-width: 575.98px) {
  .rv-page .rv-product-thumb,
  .rv-page .rv-product-thumb-placeholder {
    width: 68px;
    height: 68px;
  }
}
```

---

## 9. Таблица замен: токены

| Кастомный токен | Значение | Bootstrap-замена |
|---|---|---|
| `--rv-brand` / `--custom-primary` | hex синий | `var(--bs-primary)` |
| `--rv-brand-soft` | светло-синий tint | `var(--bs-primary-subtle)` |
| `--rv-radius` | `8–14px` | `var(--bs-border-radius-lg)` (0.5rem) или `--bs-border-radius-xl` |
| `--rv-shadow` | лёгкая тень | `var(--bs-box-shadow-sm)` |
| `--rv-shadow-hover` | тень на hover | `var(--bs-box-shadow)` |
| `--rv-transition` | `.18s ease` | убить, писать inline где нужно |
| `--rv-font` | название шрифта | `--bs-font-sans-serif` на контейнере |
| любой `--*-success` | зелёный | `var(--bs-success)` / `var(--bs-success-subtle)` |
| любой `--*-danger` | красный | `var(--bs-danger)` / `var(--bs-danger-subtle)` |
| любой `--*-warning` | жёлтый | `var(--bs-warning)` / `var(--bs-warning-subtle)` |
| любой `--*-info` | голубой | `var(--bs-info)` / `var(--bs-info-subtle)` |
| `--*-secondary-text` | серый текст | `var(--bs-secondary-color)` |
| `--*-border` | цвет границы | `var(--bs-border-color)` |
| `--*-bg` / `--*-surface` | фон | `var(--bs-body-bg)` / `var(--bs-tertiary-bg)` |

---

## 10. Таблица замен: CSS-классы → BS utilities

### Типографика

| Кастомный класс | Что делает | BS utility |
|---|---|---|
| `.meta-label` / `.card-meta` | `font-size: 12–13px` | `small` |
| `.title` / `.heading` | `font-size: 20–22px` | `h5` / `fs-5` |
| `.subtitle` | `font-size: 13px` | `small text-secondary` |
| `.label-uppercase` | `text-transform: uppercase; letter-spacing` | `text-uppercase` + `fw-semibold` |
| `.bold-text` | `font-weight: 700` | `fw-bold` |
| `.semibold-text` | `font-weight: 600` | `fw-semibold` |
| `.muted-text` | `color: gray` | `text-secondary` |
| `.hint-text` | `color: lighter gray` | `text-body-tertiary` |
| `.monospace` | `font-family: monospace` | `font-monospace` |
| `.truncate` | `overflow: hidden; text-overflow: ellipsis` | `text-truncate` (+ `mw-0` на flex) |
| `.break-word` | `word-break: break-word` | `text-break` |

### Spacing

| Кастомный стиль | BS utility |
|---|---|
| `padding: 16px` | `p-3` |
| `padding: 24px` | `p-4` |
| `padding: 48px 16px` | `py-5 px-3` |
| `margin-bottom: 8px` | `mb-2` |
| `margin-bottom: 16px` | `mb-3` |
| `margin-top: auto` | `mt-auto` |
| `gap: 8px` | `gap-2` |
| `gap: 16px` | `gap-3` |

### Отображение и выравнивание

| Кастомный стиль | BS utility |
|---|---|
| `display: none` | `d-none` |
| `display: flex; align-items: center` | `d-flex align-items-center` |
| `display: flex; justify-content: space-between` | `d-flex justify-content-between` |
| `flex-shrink: 0` | `flex-shrink-0` |
| `flex-grow: 1` | `flex-grow-1` |
| `min-width: 0` | `mw-0` (кастомная утилита) |
| `text-align: center` | `text-center` |
| `opacity: 0.5` | `opacity-50` |
| `visibility: hidden` | `invisible` |
| `overflow: hidden` | `overflow-hidden` |
| `cursor: pointer` | используй `<button>` |

### Цвета и фоны

| Кастомный класс | BS utility |
|---|---|
| `.bg-light-gray` / `.surface` | `bg-body-tertiary` |
| `.bg-white` | `bg-body` |
| `.bg-primary-tint` | `bg-primary-subtle` |
| `.bg-success-tint` | `bg-success-subtle` |
| `.text-gray` | `text-secondary` |
| `.text-blue` | `text-primary` |
| `.text-green` | `text-success` |
| `.text-red` | `text-danger` |

### Borders и тени

| Кастомный стиль | BS utility |
|---|---|
| `border: 1px solid var(--bs-border-color)` | `border` |
| `border-top: 1px solid ...` | `border-top` |
| `border-radius: 8px` | `rounded-3` |
| `border-radius: 14px` | `rounded-4` |
| `border-radius: 50%` | `rounded-circle` |
| `border-radius: 999px` | `rounded-pill` |
| `box-shadow: small` | `shadow-sm` |
| `box-shadow: medium` | `shadow` |
| `box-shadow: large` | `shadow-lg` |
| `box-shadow: none` | `shadow-none` |

### Inline styles → BS utilities

| `style="..."` | BS utility |
|---|---|
| `style="font-size:.875rem"` | `small` или `fs-6` |
| `style="font-weight:600"` | `fw-semibold` |
| `style="font-weight:700"` | `fw-bold` |
| `style="color:#6c757d"` | `text-secondary` |
| `style="display:none"` | `d-none` |
| `style="text-align:center"` | `text-center` |
| `style="white-space:nowrap"` | `text-nowrap` |
| `style="word-break:break-word"` | `text-break` |
| `style="font-family:monospace"` | `font-monospace` |
| `style="opacity:.5"` | `opacity-50` |
| `style="cursor:pointer"` | использовать `<button>` |

---

## 11. Таблица замен: компоненты

### Кнопки

```html
<!-- ❌ Кастомная кнопка -->
<button class="custom-btn custom-btn-blue">Click</button>
<style>
.custom-btn { padding: 8px 16px; border-radius: 4px; border: none; cursor: pointer; }
.custom-btn-blue { background: #3498db; color: white; }
</style>

<!-- ✅ Bootstrap -->
<button class="btn btn-primary">Click</button>
```

### Бейджи / статусы

```html
<!-- ❌ Кастомный badge -->
<span class="status-badge status-published">Published</span>
<style>
.status-badge { padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; }
.status-published { background: #4bbf73; color: #fff; }
</style>

<!-- ✅ Bootstrap -->
<span class="badge rounded-pill text-bg-success">Published</span>
```

### Формы

```html
<!-- ❌ Кастомное поле -->
<input class="custom-input" type="text">
<style>
.custom-input { border: 1px solid #ddd; border-radius: 4px; padding: 8px 12px; font-size: 14px; width: 100%; }
.custom-input:focus { border-color: #3498db; outline: none; }
</style>

<!-- ✅ Bootstrap -->
<input class="form-control" type="text">
```

### Табы с `border-bottom`

```html
<!-- ❌ Кастомные underline-табы -->
<ul class="nav my-tabs">
  <li><button class="nav-link active">Tab</button></li>
</ul>

<!-- ✅ Bootstrap nav-underline (BS 5.3+) -->
<ul class="nav nav-underline">
  <li class="nav-item"><button class="nav-link active" ...>Tab</button></li>
</ul>
```

### Empty state

```html
<!-- ❌ Кастомный empty state -->
<div class="empty-state">
  <i class="bi bi-inbox"></i>
  <p class="empty-title">Nothing here</p>
  <p class="empty-sub">Items will appear here.</p>
</div>
<style>
.empty-state { text-align: center; padding: 3rem 1rem; }
.empty-state i { font-size: 44px; color: #aaa; display: block; margin-bottom: 1rem; }
.empty-title { font-weight: 600; margin-bottom: 4px; }
</style>

<!-- ✅ Bootstrap utilities — нет кастомного CSS -->
<div class="text-center py-5 px-3">
  <i class="bi bi-inbox fs-1 text-secondary opacity-25 d-block mb-3"></i>
  <p class="fw-semibold mb-1">Nothing here</p>
  <p class="text-secondary small mb-0">Items will appear here.</p>
</div>
```

### Аккордеон с кастомной стрелкой

```html
<!-- ❌ Кастомный toggle с ручной стрелкой -->
<button class="my-toggle" aria-expanded="false">
  Title
  <span class="my-chevron">▾</span>
</button>
<style>
.my-chevron { transition: transform .2s; }
.my-toggle[aria-expanded="true"] .my-chevron { transform: rotate(180deg); }
</style>

<!-- ✅ Bootstrap accordion — стрелка, transition, aria-expanded автоматически -->
<button class="accordion-button collapsed" type="button"
        data-bs-toggle="collapse" data-bs-target="#section-1">
  Title
</button>
```

### Input group с поиском

```html
<!-- ❌ Кастомный search bar с невидимым швом -->
<div class="search-wrap">
  <span class="search-icon">🔍</span>
  <input class="search-input" type="text" placeholder="Search…">
</div>
<style>
.search-wrap { display: flex; border: 1px solid #ddd; border-radius: 20px; }
.search-icon { padding: 8px 12px; }
.search-input { border: none; outline: none; flex: 1; border-radius: 0 20px 20px 0; }
</style>

<!-- ✅ Bootstrap input-group -->
<div class="input-group">
  <span class="input-group-text bg-body-tertiary border-end-0 rounded-start-pill">
    <i class="bi bi-search text-secondary"></i>
  </span>
  <input type="search" class="form-control bg-body-tertiary border-start-0 rounded-end-pill"
         placeholder="Search…">
</div>
```

---

## 12. Что остаётся кастомным — и почему

Не всё можно убить. Этот список — то, что **должно** оставаться кастомным, и объяснение почему.

### Фиксированные размеры изображений и аватаров

```css
/* ОСТАВИТЬ — Bootstrap не умеет задавать конкретные px-размеры через utility */
.rv-page .rv-product-thumb {
  width: 92px;
  height: 92px;
  object-fit: contain;
  flex-shrink: 0;
  padding: 6px;
}
.rv-page .rv-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  flex-shrink: 0;
}
```

`w-25`, `w-50` и т.д. — это проценты, не пиксели. Для точных размеров — кастомный CSS обязателен.

### Рейтинговые прогресс-бары с CSS-переменной шириной

```css
/* ОСТАВИТЬ — ширина управляется через JS: el.style.setProperty('--rv-bar-pct', pct) */
.rv-page .rv-bar-track {
  height: 8px;
  border-radius: var(--bs-border-radius-pill);
  overflow: hidden;
}
.rv-page .rv-bar-fill {
  height: 100%;
  background: var(--rv-star);
  width: var(--rv-bar-pct, 0%);
  transition: width .5s ease;
}
```

Bootstrap `progress` компонент не поддерживает управление шириной через CSS-переменные из JS.

### Звёздный пикер (интерактивный, ARIA)

```css
/* ОСТАВИТЬ — BS не имеет star-rating компонента */
.rv-star-picker span {
  font-size: 28px;
  cursor: pointer;
  color: var(--bs-border-color);
  transition: color .18s ease;
}
.rv-star-picker span.active { color: var(--rv-star); }
.rv-star-picker span:focus-visible {
  outline: 2px solid var(--bs-primary);
  border-radius: 2px;
}
.rv-star-picker.is-invalid { animation: rv-shake 0.35s ease; }
```

### Hover-тень на карточках

```css
/* ОСТАВИТЬ — BS не предоставляет hover-shadow utility */
.rv-page .rv-card:hover {
  box-shadow: var(--bs-box-shadow);
}
```

(Базовая тень — `shadow-sm` утилита в HTML. Hover-тень — кастомная строка CSS.)

### State-атрибутные хуки

```css
/* ОСТАВИТЬ — BS не умеет менять внешний вид через data-атрибуты */
.rv-page .rv-card[data-new="true"] {
  animation: rv-card-in 200ms ease both;
}
.rv-page .rv-helpful-btn[data-state="liked"] {
  opacity: 0.6;
  pointer-events: none;
}
```

### Анимации

```css
/* ОСТАВИТЬ — BS не имеет общей системы keyframe-анимаций */
@keyframes rv-card-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes rv-shake {
  0%, 100% { transform: translateX(0); }
  20%      { transform: translateX(-6px); }
  60%      { transform: translateX(6px); }
}
```

Правила: анимировать только `transform` и `opacity` (compositor thread, нет reflow). Префикс `rv-` на имени `@keyframes` обязателен — keyframe-имена глобальные.

---

## 13. Финальный чеклист

Прогнать перед коммитом.

### Токены

- [ ] Нет `--custom-*` токенов на `:root` — все кастомные токены на `.widget-container`
- [ ] Нет токенов-дублей Bootstrap (`--custom-primary` вместо `var(--bs-primary)`)
- [ ] Динамические токены (JS через `setProperty`) не тронуты
- [ ] Оставшиеся кастомные токены имеют `[data-bs-theme="dark"]` переопределение

### CSS-классы

- [ ] Нет классов, чьё единственное свойство — `font-size` — заменены на `small` / `fs-*`
- [ ] Нет дублей — нескольких классов с одинаковыми наборами свойств
- [ ] Нет классов, которые делают только то, что BS utility уже делает
- [ ] Глобальный `body { font-family; font-size }` override убран
- [ ] Кастомный контейнер-центровщик заменён на `container-*` класс
- [ ] Все `border-radius` через `var(--bs-border-radius-*)` или `rounded-*` utility
- [ ] Все `box-shadow` через `var(--bs-box-shadow*)` или `shadow-*` utility

### HTML и JS-шаблоны

- [ ] Нет `style="..."` атрибутов (кроме динамических значений из JS-данных)
- [ ] Badge/статус классы заменены на `badge rounded-pill text-bg-*`
- [ ] Font-size классы в innerHTML-шаблонах заменены на `small`, `fs-*`
- [ ] `.section-header` классы заменены на `small text-secondary text-uppercase fw-semibold`
- [ ] Empty state использует только BS utilities (`py-5 text-center fs-1 opacity-25`)
- [ ] `form-control-sm` используется для маленьких textarea вместо кастомного `font-size`
- [ ] Кастомные `nav-link` стили с `border-bottom` заменены на `nav-underline`

### Состояния и behaviour

- [ ] `data-state` / `data-*` атрибуты, на которые завязан оставшийся CSS, работают
- [ ] Анимации `data-new` и `is-invalid` запускаются корректно
- [ ] Hover-тени работают (кастомный `rv-card:hover` не удалён)
- [ ] Лайк-кнопка в состоянии `liked` стилится через `[data-state="liked"]`

### Dark mode

- [ ] Добавить `data-bs-theme="dark"` на `<html>`, пройтись по компоненту визуально
- [ ] Нет хардкодных hex-цветов в оставшемся CSS
- [ ] Нет хардкодных `rgba(0,0,0,...)` — заменены на `rgba(var(--bs-dark-rgb), ...)`
- [ ] Оставшиеся кастомные токены (`--rv-star`) имеют dark-mode значение

### Responsive

- [ ] `@media` breakpoints используют BS-значения: `575.98px`, `767.98px`, `991.98px`
- [ ] Thumbnail/avatar `@media` с конкретными px-размерами оставлены
- [ ] `prefers-reduced-motion` для анимаций оставлен

### Счёт

После чистки примерный ориентир: **−60–70% деклараций**. Если меньше — что-то не убили. Если CSS вырос — добавили лишнего.

---

## Антипаттерны — никогда

```css
/* ❌ !important для борьбы с Bootstrap */
.my-card { padding: 20px !important; }
/* Решение: использовать p-4 utility в HTML */

/* ❌ Дублировать BS utility в кастомном классе */
.centered { text-align: center; }
.flex-center { display: flex; align-items: center; }
/* Решение: text-center, d-flex align-items-center */

/* ❌ Hardcode hex вместо BS переменной */
.label { color: #6c757d; }
/* Решение: color: var(--bs-secondary-color); или text-secondary utility */

/* ❌ Глобальный override Bootstrap компонента */
.card { border-radius: 12px; }
/* Решение: добавить rounded-4 в HTML на нужных карточках */

/* ❌ Кастомный breakpoint, не совпадающий с BS */
@media (max-width: 800px) { ... }
/* Решение: @media (max-width: 767.98px) — BS md breakpoint */
```

---

*Гайд написан на основе аудита my-reviews-5e.html и применим к любому Bootstrap 5.3+ компоненту.*
*Версия: 1.0 — Bootstrap 5.3+*
