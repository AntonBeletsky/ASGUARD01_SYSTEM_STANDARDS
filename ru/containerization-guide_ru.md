# Containerization Guide
## Единый стандарт виджетов: HTML · CSS · JavaScript

---

## Единый стандарт (best practices)

| # | Правило | Обоснование |
|---|---|---|
| 1 | CSS-селектор как точка входа | Несколько экземпляров на странице без конфликтов |
| 2 | Тихий `return` при отсутствии контейнера | Безопасно подключать глобально на весь сайт |
| 3 | Все CSS-правила скоуплены под контейнер | Стили не утекают наружу |
| 4 | `_` префикс на всех свойствах класса | Визуальное разделение публичного и приватного API |
| 5 | DOM-хелпер `$` / `$$` в конструкторе | Нет повторения `this._root.querySelector` по всему коду |
| 6 | `DOMContentLoaded` для инициализации | Работает независимо от места подключения скрипта |
| 7 | `data-*` атрибуты как JS-хуки | HTML-структура и JS-логика развязаны |
| 8 | DOM-ссылки кешируются один раз | Нет повторных querySelector в рантайме |
| 9 | State как единый источник правды | UI всегда производное от state, не от DOM |
| 10 | `AbortController` для событий | Единый `abort()` снимает все листенеры при `destroy()` |

---

## 1. Структура файла

Каждый виджет — один self-contained HTML-файл (или отдельные HTML + CSS + JS при вынесении в production). Порядок секций фиксированный:

```
<style>
  /* 1. Переменные и токены */
  /* 2. Контейнер */
  /* 3. Дочерние элементы (по секциям) */
  /* 4. Состояния */
  /* 5. Анимации (@keyframes) */
  /* 6. Адаптив (@media) */
</style>

<div class="widget-container">
  <!-- разметка виджета -->
</div>

<script>
  /* 1. CONFIG — константы */
  /* 2. CLASS — ES6 класс */
  /* 3. SEED DATA / MOCK — тестовые данные */
  /* 4. INIT — DOMContentLoaded */
</script>
```

---

## 2. HTML

### 2.1 Контейнер

Контейнер — корневой элемент виджета. Семантический тег по смыслу (`<section>`, `<article>`, `<nav>`, `<div>`). Только класс, никакого `id`:

```html
<!-- ✅ правильно -->
<section class="messages-container" aria-label="Переписка с продавцами">

<!-- ⚠️  неправильно — id создаёт лишнюю связь с JS -->
<section id="messages-module" class="messages-container">
```

Если `id` нужен для Bootstrap-компонента или ARIA — это исключение, но JS-инициализация всё равно идёт через класс-селектор.

### 2.2 JS-хуки через `data-*`

Классы — для стилей. `data-*` атрибуты — для JS. Никогда не делать `querySelector('.btn-primary')` для логики:

```html
<!-- ✅ правильно — JS-хук отдельно от стилей -->
<button class="btn btn-primary" data-action="send">Отправить</button>
<div class="messages-list" data-ref="messages"></div>

<!-- ⚠️  неправильно — класс несёт двойную нагрузку -->
<button class="btn btn-primary js-send-btn">Отправить</button>
```

Префикс `data-ref` — для статических DOM-ссылок которые кешируются в конструкторе.
Префикс `data-action` — для делегированных обработчиков событий.
Префикс `data-state` — для отражения состояния элемента (используется и в CSS).

```html
<div class="order-card" data-state="shipped">
<div class="order-card" data-state="cancelled">
```

### 2.3 ARIA

Минимально необходимое для доступности:

```html
<!-- Интерактивные списки — listbox pattern -->
<ul role="listbox" aria-label="Список заказов" aria-activedescendant="">
  <li role="option" aria-selected="false" tabindex="0" id="item-1">...</li>
</ul>

<!-- Живые регионы — обновления зачитываются screen reader -->
<div role="log" aria-live="polite" aria-atomic="false">
  <!-- сообщения чата -->
</div>

<!-- Статусы -->
<span aria-live="polite" aria-label="Статус заказа">Доставлен</span>
```

---

## 3. CSS

### 3.1 Скоупинг — главное правило

**Каждый CSS-селектор виджета должен начинаться с имени контейнера.** Без исключений:

```css
/* ✅ правильно — все стили изолированы */
.orders-container .order-card { }
.orders-container .order-card:hover { }
.orders-container .stepper { }

/* ⚠️  неправильно — стили утекают на всю страницу */
.order-card { }
.stepper { }
```

Это позволяет:
- Ставить два виджета на одной странице без конфликтов
- Переопределять стили снаружи контейнера (`body .orders-container .order-card`) без `!important`
- Удалить весь виджет — все стили удаляются вместе с ним

### 3.2 Именование классов — префикс

Все дочерние классы виджета получают уникальный короткий префикс. Он совпадает (или сокращает) имя контейнера:

```css
/* контейнер: .messages-container */
/* префикс:    msg- */

.messages-container .msg-bubble { }
.messages-container .msg-input { }
.messages-container .msg-sidebar { }
```

Формат: `[prefix]-[element]` или `[prefix]-[element]--[modifier]` (BEM-like).

### 3.3 Состояния через data-атрибуты

Для состояний которые переключает JS — `data-state` вместо добавления классов:

```css
/* ✅ читаемо, состояние видно прямо в HTML */
.orders-container .order-card[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* альтернатива — класс-модификатор тоже приемлем */
.orders-container .order-card--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

### 3.4 Переменные

Токены виджета — скоупленные CSS-переменные, не глобальные:

```css
.messages-container {
  --msg-bubble-radius: 1rem;
  --msg-bubble-sent-bg: var(--bs-primary);
  --msg-bubble-recv-bg: var(--bs-body-secondary);
  --msg-sidebar-width: 280px;
}

.messages-container .msg-bubble--sent {
  background: var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius);
}
```

### 3.5 Анимации

Имена `@keyframes` тоже должны иметь префикс — они глобальны:

```css
/* ✅ правильно */
@keyframes msg-bubble-in {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ⚠️  неправильно — может конфликтовать с другим виджетом */
@keyframes bubble-in { }
```

Анимации только через `transform` + `opacity` — compositor thread, нет reflow.

### 3.6 Адаптив

`@media` внутри `<style>` виджета — только стили самого виджета. Брейкпоинты берутся из дизайн-системы (Bootstrap: 576 / 768 / 992 / 1200):

```css
@media (max-width: 767.98px) {
  .messages-container .msg-sidebar { display: none !important; }
  .messages-container.msg-mob-chat .msg-sidebar { display: flex !important; }
}
```

---

## 4. JavaScript

### 4.1 Структура класса

```js
class WidgetController {

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────────
  constructor(selector, opts = {}) {
    // 1a. Найти контейнер — тихий выход если не найден
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Скоуп-хелперы (создаются один раз, используются везде)
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Кеш DOM-ссылок
    this._list    = $('[data-ref="list"]');
    this._input   = $('[data-ref="input"]');
    this._sendBtn = $('[data-ref="send-btn"]');

    // 1d. Опции с defaults
    this._delay = opts.delay ?? 1000;

    // 1e. State — единый источник правды
    this._state = {
      items:    [],
      activeId: null,
      loading:  false,
    };

    // 1f. AbortController для событий
    this._ac = new AbortController();

    // 1g. Запуск
    this._render();
    this._bind();
  }

  // ─── 2. RENDER ─────────────────────────────────────────────────
  _render() { }
  _renderItem(item) { }

  // ─── 3. ACTIONS ────────────────────────────────────────────────
  _select(id) { }
  _submit() { }

  // ─── 4. EVENTS ─────────────────────────────────────────────────
  _bind() {
    const sig = { signal: this._ac.signal };

    // делегирование — один листенер на контейнер
    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      this[`_on_${btn.dataset.action}`]?.(btn, e);
    }, sig);
  }

  // ─── 5. HELPERS ────────────────────────────────────────────────
  _esc(s) {
    return String(s ?? '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;').replace(/`/g, '&#x60;');
  }

  _cut(s, n) {
    return s.length > n ? s.slice(0, n) + '…' : s;
  }

  // ─── 6. LIFECYCLE ──────────────────────────────────────────────
  destroy() {
    this._ac.abort(); // снимает ВСЕ листенеры одним вызовом
  }
}
```

### 4.2 Тихий return — обязательно

Виджет может быть подключён глобально. Если контейнер не найден — молча ничего не делать:

```js
// ✅ правильно
this._root = document.querySelector(selector);
if (!this._root) return;

// ⚠️  неправильно — летит в консоль на всех страницах без виджета
if (!this._root) throw new Error('...');
```

### 4.3 Конвенция приватных свойств

Все внутренние свойства класса — с `_` префиксом. Это конвенция, не языковое ограничение (для настоящей приватности — `#prop`, ES2022):

```js
// ✅ правильно — сразу видно что трогать снаружи нельзя
this._root     = ...
this._state    = ...
this._sendBtn  = ...

// ⚠️  неправильно — не отличить приватное от публичного
this.root      = ...
this.state     = ...
this.sendBtn   = ...
```

Публичный API (если нужен) — без `_`:

```js
// методы которые может вызывать внешний код
controller.setItems(items)
controller.destroy()
```

### 4.4 DOM-хелперы `$` / `$$`

Объявляются в конструкторе, скоуплены на контейнер. Устраняют повторение длинных querySelector:

```js
// ✅ один раз объявил — везде используешь
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

this._form    = $('[data-ref="form"]');
this._items   = $$('[data-ref="item"]');

// ⚠️  неправильно — дублирование по всему классу
this._form    = this._root.querySelector('[data-ref="form"]');
this._items   = this._root.querySelectorAll('[data-ref="item"]');
// ... и потом снова в _render(), снова в _bind()...
```

### 4.5 State как единый источник правды

UI — это всегда отражение state. Никогда не читать состояние из DOM:

```js
// ✅ правильно — state обновился, потом render
_select(id) {
  this._state.activeId = id;
  this._render();          // UI перестраивается из state
}

// ⚠️  неправильно — читаем состояние из DOM
_select(id) {
  const current = this._root.querySelector('.active')?.dataset.id;
  // ...логика на основе DOM вместо state
}
```

### 4.6 AbortController для событий

Позволяет снять все обработчики одним вызовом. Обязателен если виджет может быть уничтожен:

```js
constructor(selector) {
  // ...
  this._ac = new AbortController();
  this._bind();
}

_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   this._onClick, sig);
  this._root.addEventListener('keydown', this._onKey,   sig);
  window.addEventListener('resize',      this._onResize, sig);
  // ^ снимется тоже, хотя вешается на window
}

destroy() {
  this._ac.abort(); // снимает абсолютно все листенеры
}
```

### 4.7 Делегирование событий

Один листенер на контейнер вместо листенера на каждый элемент. Работает для динамически добавляемых элементов:

```js
// ✅ правильно — один листенер, работает для новых элементов
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  const actions = {
    'send':   () => this._send(),
    'remove': () => this._remove(btn.dataset.id),
    'toggle': () => this._toggle(btn.dataset.id),
  };

  actions[btn.dataset.action]?.();
});

// ⚠️  неправильно — листенер на каждый элемент
this._root.querySelectorAll('[data-action="send"]').forEach(btn => {
  btn.addEventListener('click', () => this._send());
});
```

### 4.8 XSS-защита

Пользовательский текст — только `textContent`. HTML-метаданные — только через `_esc()`:

```js
// ✅ правильно
bubble.textContent = userMessage;    // никакой XSS
li.innerHTML = `<span>${this._esc(serverData.name)}</span>`;

// ⚠️  опасно
bubble.innerHTML = userMessage;      // XSS-уязвимость
li.innerHTML = `<span>${serverData.name}</span>`;
```

### 4.9 Защита от Prototype Pollution

При обработке внешних данных (API, localStorage) — проверять ключи:

```js
const FORBIDDEN = Object.freeze(['__proto__', 'constructor', 'prototype']);

static _validate(obj) {
  if (Object.keys(obj).some(k => FORBIDDEN.includes(k))) return false;
  return true;
}

// В init:
const safeItems = rawData.filter(item => WidgetController._validate(item));
```

---

## 5. Инициализация

### 5.1 Стандартный паттерн

```js
document.addEventListener('DOMContentLoaded', () => {
  new WidgetController('.widget-container');
});
```

`DOMContentLoaded` — работает независимо от места подключения скрипта: в `<head>`, в `<body>`, как внешний файл.

### 5.2 С опциями

```js
document.addEventListener('DOMContentLoaded', () => {
  const safeData = SEED_DATA.filter(d => WidgetController._validate(d));

  new WidgetController({
    selector: '.widget-container',
    data:     safeData,
    delay:    1000,
  });
});
```

### 5.3 Несколько экземпляров

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.messages-container').forEach(el => {
    new MessagesController({ selector: `#${el.id}`, ... });
  });
});
```

---

## 6. Именование

### 6.1 Классы и файлы

| Что | Конвенция | Пример |
|---|---|---|
| ES6 класс | PascalCase + суффикс `Controller` | `MessagesController` |
| CSS-контейнер | kebab-case + суффикс `-container` | `.messages-container` |
| CSS-префикс дочерних | короткий kebab | `msg-` |
| HTML-файл | `feature-hash.html` | `correspondence-3f.html` |
| Экземпляр | camelCase | `const messagesController` |

### 6.2 Данные в `data-*`

| Назначение | Атрибут | Пример |
|---|---|---|
| Ссылка для кеширования | `data-ref` | `data-ref="send-btn"` |
| Триггер действия | `data-action` | `data-action="remove"` |
| Идентификатор записи | `data-id` | `data-id="order-42"` |
| Отображение состояния | `data-state` | `data-state="shipped"` |

---

## 7. Чеклист при создании нового виджета

```
HTML
  [ ] Контейнер — семантический тег, только class, без id
  [ ] JS-хуки через data-ref / data-action, не через классы
  [ ] ARIA: role, aria-label, aria-live где нужно

CSS
  [ ] Все селекторы начинаются с .widget-container
  [ ] @keyframes с префиксом
  [ ] Токены как CSS-переменные внутри контейнера

JS
  [ ] Тихий return если контейнер не найден
  [ ] $ / $$ хелперы в конструкторе
  [ ] DOM-ссылки кешированы в конструкторе, нигде больше
  [ ] Все свойства с _ префиксом
  [ ] state как единый источник правды
  [ ] AbortController для событий
  [ ] Делегирование вместо листенера на каждый элемент
  [ ] textContent для пользовательского текста
  [ ] _esc() для серверных данных в innerHTML
  [ ] _validate() для внешних объектов
  [ ] DOMContentLoaded в init
```
