# Руководство по контейнеризации
## Стандарт виджетов: HTML · CSS · JavaScript

---

## Основной стандарт (лучшие практики)

| # | Правило | Обоснование |
|---|---|---|
| 1 | CSS-селектор как точка входа | Несколько экземпляров на одной странице без конфликтов |
| 2 | Тихий `return` при отсутствии контейнера | Безопасно включать глобально на любой странице |
| 3 | Все CSS-правила ограничены контейнером | Стили не могут вытекать за пределы виджета |
| 4 | Префикс `_` у всех свойств класса | Чёткое визуальное разделение публичного и приватного API |
| 5 | DOM-хелперы `$` / `$$` в конструкторе | Нет повторений `this._root.querySelector` по всему коду |
| 6 | `DOMContentLoaded` для инициализации | Работает независимо от расположения скрипта |
| 7 | Атрибуты `data-*` как JS-хуки | HTML-структура и JS-логика полностью разделены |
| 8 | DOM-ссылки кешируются один раз | Нет повторных вызовов querySelector во время выполнения |
| 9 | Состояние как единственный источник истины | UI всегда производится из состояния, а не из DOM |
| 10 | `AbortController` для обработчиков событий | Один `abort()` удаляет все обработчики при `destroy()` |
| 11 | Конфиг и начальные данные как `static` свойства класса | INIT остаётся одной строкой; всё самодостаточно |
| 12 | Сигнатура конструктора `(selector, opts = {})` | Минимальный вызов; переопределения только при необходимости |

---

## 1. Структура файла

Каждый виджет — это самодостаточный HTML-файл (или отдельные HTML + CSS + JS при извлечении для продакшна). Порядок разделов фиксирован:

```
<style>
  /* 0. Токены (CSS custom properties)  */
  /* 1. Layout контейнера               */
  /* 2. Дочерние элементы (секции)      */
  /* 3. Состояния                       */
  /* 4. Анимации (@keyframes)           */
  /* 5. Адаптивность (@media)           */
</style>

<section class="widget-container">
  <!-- разметка виджета -->
</section>

<script>
  /* 1. КЛАСС
   *   ├── static свойства конфига
   *   ├── static начальные данные
   *   ├── constructor
   *   ├── методы рендеринга
   *   ├── методы действий
   *   ├── привязка событий
   *   ├── хелперы
   *   ├── destroy()
   *   └── static _validate()
   */

  /* 2. INIT — DOMContentLoaded  */
</script>
```

**Ключевое отличие от старых версий:** отдельного блока `CONFIG` над классом нет. Все константы и начальные данные живут как `static` свойства внутри класса. Блок `INIT` всегда состоит из одной строки.

---

## 2. HTML

### 2.1 Контейнер

Контейнер — корневой элемент виджета. Используйте семантический тег, соответствующий содержимому (`<section>`, `<article>`, `<nav>`, `<div>`). Только класс — без `id`:

```html
<!-- ✅ правильно -->
<section class="messages-container" aria-label="Переписка с продавцом">

<!-- ⚠️  неправильно — id создаёт лишнюю связь с JS -->
<section id="messages-module" class="messages-container">
```

Если `id` нужен для Bootstrap-компонента или ARIA-ссылки (`aria-labelledby`, `aria-activedescendant`), это допустимое исключение — но инициализация JS всё равно идёт через селектор класса.

### 2.2 JS-хуки через `data-*`

Классы — для стилей. Атрибуты `data-*` — для JS. Никогда не используйте `querySelector('.btn-primary')` для логики:

```html
<!-- ✅ правильно — JS-хук отделён от стилей -->
<button class="btn btn-primary" data-action="send">Отправить</button>
<div class="messages-list" data-ref="messages"></div>

<!-- ⚠️  неправильно — класс несёт двойную ответственность -->
<button class="btn btn-primary js-send-btn">Отправить</button>
```

| Атрибут | Назначение | Пример |
|---|---|---|
| `data-ref` | Статическая DOM-ссылка, кешируется в конструкторе | `data-ref="send-btn"` |
| `data-action` | Триггер делегированного обработчика событий | `data-action="send"` |
| `data-id` | Идентификатор записи | `data-id="order-42"` |
| `data-state` | Отражает состояние, управляемое JS; используется также в CSS | `data-state="active"` |

**`data-ref` не конфликтует между виджетами.** Все поиски идут через `$('[data-ref="..."]')`, где `$` ограничен `this._root`. Два виджета на одной странице с одинаковыми `data-ref` никогда не помешают друг другу — каждый контроллер видит только свой контейнер.

### 2.3 ARIA

Минимально необходимое для доступности:

```html
<!-- Интерактивные списки — паттерн listbox -->
<ul role="listbox" aria-label="Список заказов" aria-activedescendant="">
  <li role="option" aria-selected="false" tabindex="0" id="item-1">...</li>
</ul>

<!-- Live-регионы — обновления зачитываются скринридерами -->
<div role="log" aria-live="polite" aria-atomic="false">
  <!-- сообщения чата, добавляемые динамически -->
</div>

<!-- Статусные бейджи -->
<span aria-live="polite" aria-label="Статус заказа">Доставлен</span>
```

Клавиатурная навигация для listbox: `↑↓` перемещают фокус, `Home`/`End` переходят к краям, `Enter`/`Space` активируют.

---

## 3. CSS

### 3.1 Скопирование — главное правило

**Каждый CSS-селектор в виджете обязан начинаться с имени класса контейнера. Без исключений:**

```css
/* ✅ правильно — все стили изолированы */
.orders-container .order-card { }
.orders-container .order-card:hover { }
.orders-container .stepper { }

/* ⚠️  неправильно — стили утекают на всю страницу */
.order-card { }
.stepper { }
```

Это гарантирует:
- Два экземпляра одного виджета на странице никогда не конфликтуют
- Стили можно переопределять снаружи без `!important`
- Удаление виджета удаляет все его стили вместе с ним

### 3.2 Именование классов — префикс

Все дочерние классы получают уникальный короткий префикс — сокращение имени контейнера:

```css
/* контейнер: .messages-container */
/* префикс:   msg-                */

.messages-container .msg-bubble  { }
.messages-container .msg-input   { }
.messages-container .msg-sidebar { }
```

Формат: `[prefix]-[element]` или `[prefix]-[element]--[modifier]` (в стиле BEM).

### 3.3 Состояния через `data-state`

Для состояний, переключаемых JS, — предпочитайте `data-state` вместо modifier-классов. Состояние тогда видно прямо в HTML без инспекции вычисленных классов:

```css
/* ✅ предпочтительно — состояние читается в DOM */
.orders-container .order-card[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* также допустимо — BEM-модификатор */
.orders-container .order-card--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

В JS всегда устанавливайте и Bootstrap-класс (для встроенных стилей) **и** `data-state` (для CSS-хуков):

```js
el.classList.toggle('active', isActive);      // Bootstrap visual
el.dataset.state = isActive ? 'active' : '';  // CSS-хук
```

### 3.4 CSS custom properties (токены)

Токены виджета — это скопированные CSS-переменные, объявленные на контейнере — раздел `0` таблицы стилей. Это единственное место, где живут дизайн-значения. Дочерние правила потребляют токены, а не сырые значения:

```css
/* --- 0. Токены --- */
.messages-container {
  --msg-bubble-radius:      0.75rem;
  --msg-bubble-sent-bg:     var(--bs-primary);
  --msg-bubble-sent-color:  #fff;
  --msg-bubble-recv-bg:     var(--bs-body-secondary);
  --msg-bubble-recv-color:  var(--bs-body-color);
  --msg-active-accent:      var(--bs-primary);
  --msg-input-max-height:   96px;
  --msg-anim-duration:      120ms;
}
```

Токены можно переопределить снаружи без `!important`:

```css
/* Кастомизация одного экземпляра на странице */
.messages-container {
  --msg-bubble-sent-bg: #6f42c1;
}
```

#### Правило сосуществования токенов и Bootstrap

Если дизайн-система (Bootstrap) уже предоставляет класс для базовой стилизации — используйте его. Добавляйте BEM-модификаторы рядом для переопределений через токены, но **никогда не убирайте Bootstrap-класс**:

```js
// ✅ правильно — Bootstrap обеспечивает базовый цвет и адаптацию темы;
//                BEM-модификатор открывает хук токена для внешнего переопределения
isSent
  ? 'bg-primary text-white msg-msg--sent'
  : 'bg-body-secondary text-body msg-msg--recv'

// ⚠️  неправильно — Bootstrap-класс убран, адаптация тёмной темы потеряна,
//                   захардкоженный цвет (#fff) ломает темизацию
isSent ? 'msg-msg--sent' : 'msg-msg--recv'
```

Соответствующий CSS-модификатор переопределяет только то, что нужно — он **не дублирует** свойства, которые уже обрабатывает Bootstrap:

```css
/* ✅ правильно — только хук токена, без дублирования border-radius / padding */
.messages-container .msg-msg--sent {
  background: var(--msg-bubble-sent-bg);
  color:      var(--msg-bubble-sent-color);
}

/* ⚠️  неправильно — дублирует rounded-3, и !important ломает возможность переопределения */
.messages-container .msg-msg--sent {
  background:    var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius) !important;
}
```

### 3.5 Анимации

Имена `@keyframes` должны содержать префикс виджета — имена keyframe глобальны:

```css
/* ✅ правильно */
@keyframes msg-bubble-in {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ⚠️  неправильно — может конфликтовать с другим виджетом на странице */
@keyframes bubble-in { }
```

Все блоки `@keyframes` собираются в отдельный раздел (`4. Анимации`) — никогда не встраиваются внутрь разделов дочерних элементов.

Анимируйте только `transform` и `opacity` — они выполняются в потоке компоновщика и не вызывают reflow.

### 3.6 Адаптивность

Блоки `@media` внутри `<style>` виджета охватывают только его стили. Брейкпоинты берутся из дизайн-системы (Bootstrap: 576 / 768 / 992 / 1200):

```css
@media (max-width: 767.98px) {
  .messages-container .msg-sidebar { display: none !important; }
  .messages-container.msg-mob-chat .msg-sidebar { display: flex !important; }
}
```

---

## 4. JavaScript

### 4.1 Структура класса

Весь конфиг, начальные данные и логика живут внутри класса. Ничего не утекает в область видимости модуля.

```js
class WidgetController {

  // ─── 0. STATIC CONFIG ──────────────────────────────────────
  static DELAY_MS        = 1000;
  static MAX_PREVIEW     = 38;
  static FORBIDDEN_KEYS  = Object.freeze(['__proto__', 'constructor', 'prototype']);

  // ─── 0b. STATIC SEED DATA ──────────────────────────────────
  // Присваивается после тела класса — см. §4.10
  // static SEED_DATA = [...];

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────
  /**
   * @param {string} selector - Селектор корневого элемента, например '.widget-container'
   * @param {Object} [opts]
   * @param {Array}  [opts.data]  - Переопределение данных; по умолчанию WidgetController.SEED_DATA
   * @param {number} [opts.delay] - Переопределение задержки; по умолчанию WidgetController.DELAY_MS
   */
  constructor(selector, opts = {}) {

    // 1a. Найти контейнер — тихий выход если не найден
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Хелперы области видимости (создаются один раз, используются везде)
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Кешировать DOM-ссылки через data-ref
    this._list    = $('[data-ref="list"]');
    this._input   = $('[data-ref="input"]');
    this._sendBtn = $('[data-ref="send-btn"]');

    // 1d. Опции со статическими значениями по умолчанию
    this._delay = opts.delay ?? WidgetController.DELAY_MS;

    // 1e. Данные — opts перекрывает → static seed → валидация
    const raw  = opts.data ?? WidgetController.SEED_DATA;
    const data = raw.filter(d => WidgetController._validate(d));

    // 1f. Состояние — единственный источник истины
    this._state = {
      items:    data,
      activeId: null,
      loading:  false,
    };

    // 1g. AbortController для обработчиков событий
    this._ac = new AbortController();

    // 1h. Запуск
    this._render();
    this._bind();
  }

  // ─── 2. RENDER ─────────────────────────────────────────────
  /** @private */
  _render() { }

  /** @private */
  _renderItem(item) { }

  // ─── 3. ACTIONS ────────────────────────────────────────────
  /** @private */
  _select(id) {
    this._state.activeId = id;
    this._render(); // всегда производить UI из состояния
  }

  /** @private */
  _submit() { }

  // ─── 4. EVENTS ─────────────────────────────────────────────
  /** @private */
  _bind() {
    const sig = { signal: this._ac.signal };

    // Один делегированный обработчик на root покрывает ВСЕ [data-action] дочерние элементы,
    // включая динамически добавленные после инициализации.
    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      switch (btn.dataset.action) {
        case 'send':   this._submit(); break;
        case 'remove': this._remove(btn.dataset.id); break;
        case 'back':   this._handleBack(); break;
      }
    }, sig);

    this._input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._submit(); }
    }, sig);
  }

  // ─── 5. HELPERS ────────────────────────────────────────────

  /** @private */
  _scrollBottom() {
    this._messages.scrollTop = this._messages.scrollHeight;
  }

  /**
   * @param {string} s
   * @param {number} maxLen
   * @returns {string}
   * @private
   */
  _cut(s, maxLen) {
    return s.length > maxLen ? s.slice(0, maxLen) + '…' : s;
  }

  /**
   * Экранирует все 7 HTML-символов, рекомендованных OWASP.
   * Используйте для метаданных в innerHTML. Пользовательский текст всегда через textContent.
   * @param {string} s
   * @returns {string}
   * @private
   */
  _esc(s) {
    return String(s ?? '')
      .replace(/&/g,  '&amp;')
      .replace(/</g,  '&lt;')
      .replace(/>/g,  '&gt;')
      .replace(/"/g,  '&quot;')
      .replace(/'/g,  '&#x27;')
      .replace(/\//g, '&#x2F;')
      .replace(/`/g,  '&#x60;');
  }

  // ─── 6. LIFECYCLE ──────────────────────────────────────────

  /**
   * Удаляет все обработчики событий. Вызывайте при размонтировании виджета.
   */
  destroy() {
    this._ac.abort();
  }

  // ─── 7. STATIC ─────────────────────────────────────────────

  /**
   * Защита от prototype pollution.
   * Валидирует объект и все вложенные массивы.
   * @param {Object} obj
   * @returns {boolean}
   */
  static _validate(obj) {
    const forbidden = WidgetController.FORBIDDEN_KEYS;
    if (!obj || typeof obj !== 'object') return false;
    return !Object.keys(obj).some(k => forbidden.includes(k));
  }
}

// Начальные данные присваиваются после объявления класса — сохраняет читаемость тела класса
WidgetController.SEED_DATA = [
  // { id, ...fields }
];
```

### 4.2 Тихий return — обязательно

Виджет может быть подключён на страницах, где его контейнера нет. Никогда не бросайте ошибку:

```js
// ✅ правильно — нет лишних сообщений в консоли на посторонних страницах
this._root = document.querySelector(selector);
if (!this._root) return;

// ⚠️  неправильно — выбрасывает ошибку на каждой странице без виджета
if (!this._root) throw new Error('WidgetController: container not found');
```

### 4.3 Конвенция приватных свойств

Все внутренние свойства используют `_`. Методы публичного API префикса не имеют:

```js
// ✅ внутренние — _ сразу указывает на приватность
this._root    = ...
this._state   = ...
this._sendBtn = ...

// ✅ публичный API — без префикса, вызывается внешним кодом
controller.destroy()
controller.setItems(items)

// ⚠️  неправильно — неотличимо от публичного API
this.root  = ...
this.state = ...
```

### 4.4 DOM-хелперы `$` / `$$`

Объявляются в конструкторе, ограничены `this._root`. Не могут достать ничего за пределами виджета:

```js
// ✅ объявить один раз, использовать везде внутри класса
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

this._form  = $('[data-ref="form"]');
this._items = $$('[data-ref="item"]');

// ⚠️  неправильно — утекает из области видимости, повторяется
this._form = document.querySelector('[data-ref="form"]');
```

`$$` также готовит к работе с динамическим контентом — запрос выполняется в момент вызова, а не в момент кеширования.

### 4.5 Static конфиг и начальные данные

Константы конфига и мок/начальные данные принадлежат классу как `static` свойства — не как отдельные `const`-объявления над классом. Это сохраняет область видимости модуля чистой, а блок `INIT` минимальным:

```js
class OrdersController {
  static DELAY_MS       = 1000;
  static MAX_PREVIEW    = 38;
  static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
}

// Большие массивы данных присваиваются после тела класса для читаемости
OrdersController.SEED_DATA = [ /* ... */ ];
```

Внутренние ссылки используют `WidgetController.PROP_NAME`, а не голый идентификатор:

```js
// ✅ правильно
this._delay = opts.delay ?? MessagesController.DELAY_MS;
const preview = this._cut(text, MessagesController.MAX_PREVIEW);

// ⚠️  неправильно — голое имя работает только если const живёт во внешней области
this._delay = opts.delay ?? DELAY_MS;
```

### 4.6 Сигнатура конструктора

Всегда `(selector, opts = {})`. Селектор обязателен; всё остальное опционально со статическим значением по умолчанию:

```js
// ✅ минимальный вызов — применяются все значения по умолчанию
new MessagesController('.messages-container');

// ✅ переопределить только то, что нужно
new MessagesController('.messages-container', { delay: 500 });
new MessagesController('.messages-container', { data: apiData });

// ⚠️  неправильно — заставляет вызывающий код знать внутренние значения по умолчанию
new MessagesController({ selector: '.messages-container', delay: 1000, data: SEED });

// ⚠️  неправильно — передавать значение по умолчанию обратно в конструктор — шум
new MessagesController('.messages-container', { delay: MessagesController.DELAY_MS });
```

Валидация данных (защита от prototype pollution) выполняется внутри конструктора, не в блоке `INIT`:

```js
constructor(selector, opts = {}) {
  // ...
  const raw  = opts.data ?? WidgetController.SEED_DATA;
  const data = raw.filter(d => WidgetController._validate(d)); // ← внутри, не снаружи
  // ...
}
```

### 4.7 Состояние как единственный источник истины

UI — всегда проекция состояния. Никогда не читайте состояние обратно из DOM:

```js
// ✅ правильно — сначала обновить состояние, затем рендерить
_select(id) {
  this._state.activeId = id;
  this._render();
}

// ⚠️  неправильно — чтение состояния из DOM
_select(id) {
  const current = this._root.querySelector('.active')?.dataset.id;
  // ...логика, управляемая DOM вместо состояния
}
```

### 4.8 AbortController для событий

Каждый вызов `addEventListener` получает `{ signal: this._ac.signal }`. `destroy()` удаляет их все:

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   this._onClick,  sig);
  this._root.addEventListener('keydown', this._onKey,    sig);
  window.addEventListener('resize',      this._onResize, sig);
  // ^ window-обработчики тоже удаляются при abort()
}

destroy() {
  this._ac.abort(); // удаляет все обработчики, зарегистрированные с этим сигналом
}
```

### 4.9 Делегирование событий

Один обработчик на root покрывает все `[data-action]`-цели, включая динамически добавленные элементы:

```js
// ✅ правильно — один обработчик, работает и для будущих элементов
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  switch (btn.dataset.action) {
    case 'send':   this._submit(); break;
    case 'remove': this._remove(btn.dataset.id); break;
    case 'back':   this._handleBack(); break;
  }
}, { signal: this._ac.signal });

// ⚠️  неправильно — по одному обработчику на элемент, ломается на динамическом контенте,
//                   signal не передан = обработчик утекает при destroy()
this._sendBtn.addEventListener('click', () => this._submit());
this._backBtn.addEventListener('click', () => this._handleBack());
```

Встроенные `click`-обработчики на отдельных кнопках допустимы только для событий `keydown` / `input`, где делегирование непрактично.

#### Выносите встроенные обработчики в именованные методы

Если делегированное действие содержит больше 2–3 строк логики, выносите его в именованный приватный метод. Это сохраняет `_bind()` читаемым, а логику — тестируемой в изоляции:

```js
// ✅ правильно — логика в именованном методе
case 'back': this._handleBack(); break;

_handleBack() {
  this._root.classList.remove('msg-mob-chat');
  this._state.activeId = null;
  this._renderMessages();
  // ...
}

// ⚠️  неправильно — сложная логика захоронена внутри _bind()
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (btn?.dataset.action === 'back') {
    this._root.classList.remove('msg-mob-chat');
    this._state.activeId = null;
    // ... ещё 10 строк
  }
});
```

### 4.10 Защита от XSS

Пользовательский текст — только `textContent`. Метаданные сервера/API в `innerHTML` — всегда через `_esc()`:

```js
// ✅ правильно
bubble.textContent = userMessage;                           // XSS невозможен
li.innerHTML = `<span>${this._esc(apiData.name)}</span>`;  // метаданные экранированы

// ⚠️  опасно
bubble.innerHTML = userMessage;
li.innerHTML = `<span>${apiData.name}</span>`;
```

### 4.11 Защита от prototype pollution

`_validate()` — это `static` метод. Он проверяет как ключи верхнего уровня, так и вложенные массивы. Вызывается внутри конструктора, не в `INIT`:

```js
static _validate(obj) {
  const forbidden = WidgetController.FORBIDDEN_KEYS;
  if (!obj || typeof obj !== 'object') return false;
  if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
  // Валидация вложенных массивов сообщений/элементов тоже
  for (const key of Object.keys(obj)) {
    if (Array.isArray(obj[key])) {
      for (const child of obj[key]) {
        if (!WidgetController._validate(child)) return false;
      }
    }
  }
  return true;
}
```

---

## 5. Инициализация

### 5.1 Стандартный паттерн — всегда одна строка

```js
document.addEventListener('DOMContentLoaded', () => {
  new MessagesController('.messages-container');
});
```

`DOMContentLoaded` срабатывает, когда DOM полностью разобран, независимо от расположения `<script>`. Валидация данных и значения по умолчанию обрабатываются конструктором — в `INIT` нет бизнес-логики.

### 5.2 С переопределениями

```js
document.addEventListener('DOMContentLoaded', () => {
  new MessagesController('.messages-container', { data: apiData, delay: 500 });
});
```

### 5.3 Несколько экземпляров на одной странице

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.messages-container').forEach(el => {
    new MessagesController(`#${el.id}`);
  });
});
```

Поскольку все DOM-запросы ограничены `this._root`, несколько экземпляров одного виджета никогда не мешают друг другу — даже с одинаковыми значениями `data-ref` внутри каждого.

---

## 6. Соглашения об именовании

### 6.1 Классы и файлы

| Что | Конвенция | Пример |
|---|---|---|
| ES6-класс | PascalCase + суффикс `Controller` | `MessagesController` |
| CSS-контейнер | kebab-case + суффикс `-container` | `.messages-container` |
| CSS дочерний префикс | короткий kebab | `msg-` |
| BEM-модификатор | `[prefix]-[element]--[modifier]` | `.msg-msg--sent` |
| HTML-файл | `feature-hash.html` | `correspondence-4e.html` |
| Переменная экземпляра | camelCase | `const messagesController` |

### 6.2 Атрибуты `data-*`

| Назначение | Атрибут | Пример |
|---|---|---|
| DOM-ссылка (кешируется в конструкторе) | `data-ref` | `data-ref="send-btn"` |
| Триггер действия (делегированный обработчик) | `data-action` | `data-action="send"` |
| Идентификатор записи | `data-id` | `data-id="order-42"` |
| Состояние элемента, управляемое JS (также задаёт CSS) | `data-state` | `data-state="active"` |

### 6.3 Static свойства

| Что | Конвенция | Пример |
|---|---|---|
| Константа конфига | SCREAMING_SNAKE | `static DELAY_MS = 1000` |
| Замороженный список | SCREAMING_SNAKE | `static FORBIDDEN_KEYS = Object.freeze([...])` |
| Массив начальных данных | SCREAMING_SNAKE | `static SEED_DATA = [...]` (или присваивается после тела класса) |

---

## 7. Чеклист нового виджета

```
HTML
  [ ] Контейнер использует семантический тег, только класс (без id)
  [ ] DOM-ссылки используют data-ref, действия — data-action
  [ ] JS-управляемые состояния используют data-state
  [ ] data-id на всех элементах списка
  [ ] ARIA: role, aria-label, aria-live там, где применимо
  [ ] Клавиатурная навигация реализована для интерактивных списков

CSS
  [ ] Раздел 0 — токены объявлены на контейнере
  [ ] Каждый дочерний селектор начинается с .widget-container
  [ ] BEM-модификаторы используются вместе с Bootstrap-классами, а не вместо них
  [ ] CSS BEM-модификатора не дублирует то, что уже предоставляет Bootstrap
  [ ] Нет !important внутри правил модификаторов
  [ ] Имена @keyframes содержат префикс виджета
  [ ] Все @keyframes собраны в отдельном разделе Анимации
  [ ] @media брейкпоинты соответствуют дизайн-системе

JS
  [ ] Нет свободных констант над классом — всё является static
  [ ] Начальные данные присвоены как WidgetController.SEED_DATA после тела класса
  [ ] Сигнатура конструктора — (selector, opts = {})
  [ ] Тихий return если контейнер не найден
  [ ] Хелперы $ / $$ объявлены в конструкторе, ограничены this._root
  [ ] DOM-ссылки кешированы через data-ref в конструкторе и нигде более
  [ ] opts разрешены со static значениями по умолчанию (opts.delay ?? ClassName.DELAY_MS)
  [ ] Данные валидированы внутри конструктора, не в INIT
  [ ] Все внутренние свойства используют префикс _
  [ ] Состояние — единственный источник истины — никогда не читать состояние из DOM
  [ ] AbortController: this._ac в конструкторе, signal передан в каждый addEventListener
  [ ] destroy() вызывает this._ac.abort()
  [ ] Все делегированные действия идут через один root click listener + switch
  [ ] Сложные обработчики действий вынесены в именованные методы _handleXxx()
  [ ] Пользовательский текст через textContent, никогда через innerHTML
  [ ] Метаданные экранированы через _esc() перед innerHTML
  [ ] Внешние данные валидированы через static _validate()

INIT
  [ ] DOMContentLoaded оборачивает init
  [ ] Init — одна строка: new WidgetController('.widget-container')
  [ ] Нет фильтрации данных, нет сборки опций в INIT — всё внутри конструктора
```
