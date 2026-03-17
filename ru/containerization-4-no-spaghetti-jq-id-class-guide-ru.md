# Containerization Guide — v4
## Widget Standard: HTML · CSS · JavaScript
### No Spaghetti · No jQuery · No ID/Class JS Hooks · Secure · Fast

---

## Приоритеты (читать перед всем остальным)

Правила этого гайда выстроены в жёсткой иерархии. Если два правила вступают в противоречие — побеждает то, что стоит выше.

```
1. DATA-АТРИБУТЫ — абсолютный фундамент          ← нерушимо, не переписывается ничем
2. ЧИСТОТА КОДА  — структура, изоляция, читаемость ← действует везде где не нарушает п.3
3. БЕЗОПАСНОСТЬ  — XSS, pollution, escaping        ← отменяет любые "удобства" п.2
4. БЫСТРОДЕЙСТВИЕ — no Violation, no thrashing     ← финальный аудит, не меняет архитектуру
```

Контейнеризация стоит **над** этой цепочкой — она задаёт форму виджета. Всё остальное работает внутри этой формы.

---

## Нулевой закон: JS работает только через data-атрибуты

Это единственное правило без исключений. Нарушение этого правила делает невалидным весь виджет.

```html
<!-- ✅ ПРАВИЛЬНО — JS-хук через data-атрибут -->
<button class="btn btn-primary" data-action="send">Send</button>
<div class="msg-list"          data-ref="messages"></div>
<li  class="ord-item"          data-id="order-42" data-state="active"></li>

<!-- ❌ ЗАПРЕЩЕНО — класс как JS-хук -->
<button class="btn btn-primary js-send-btn">Send</button>

<!-- ❌ ЗАПРЕЩЕНО — id как JS-хук -->
<button id="send-btn" class="btn btn-primary">Send</button>

<!-- ❌ ЗАПРЕЩЕНО — jQuery -->
$('#send-btn').on('click', handler);
$('.js-send-btn').show();
```

### Таблица data-атрибутов

| Атрибут | Назначение | Пример |
|---|---|---|
| `data-ref` | DOM-ссылка, кэшируется в конструкторе один раз | `data-ref="send-btn"` |
| `data-action` | Триггер делегированного обработчика | `data-action="send"` |
| `data-id` | Идентификатор записи | `data-id="order-42"` |
| `data-state` | JS-управляемое состояние, читается CSS | `data-state="active"` |

### Единственные легальные исключения для `id`

`id` допустим **только** в двух случаях — оба исключительно для HTML/ARIA, не для JS-запросов:

```html
<!-- ✅ ARIA-связь — id здесь семантически обязателен -->
<div role="dialog" aria-labelledby="modal-title-id" hidden>
  <h2 id="modal-title-id">Confirm deletion</h2>
</div>

<!-- ✅ Якорная ссылка -->
<h2 id="section-payments">Payments</h2>
<a href="#section-payments">Go to payments</a>
```

JS никогда не ищет эти элементы через `getElementById` — он находит их через `data-ref` или через `aria-labelledby` атрибут.

### Запрещённые методы выборки

```js
// ❌ ВСЁ ЭТО ЗАПРЕЩЕНО
document.getElementById('anything')
document.querySelector('.some-class')
document.querySelector('#some-id')
document.getElementsByClassName('something')
$('#anything')
$('.anything')

// ✅ РАЗРЕШЕНО ТОЛЬКО ТАК
this._root.querySelector('[data-ref="name"]')   // через data-ref
this._root.querySelector('[data-action="name"]') // через data-action
e.target.closest('[data-action]')               // при делегировании
document.querySelectorAll('.widget-container')  // bootstrap всех виджетов — по CSS-классу контейнера
document.getElementById(id)                     // только для ARIA/якоря, не для логики
```

---

## 1. Структура файла

Каждый виджет — самодостаточный HTML-файл. Порядок секций фиксирован:

```
<style>
  /* 0. Tokens (CSS custom properties)  */
  /* 1. Container layout                */
  /* 2. Child elements                  */
  /* 3. Modal(s)                        */
  /* 4. States                          */
  /* 5. Animations (@keyframes)         */
  /* 6. Responsive (@media)             */
</style>

<section class="widget-container">
  <!-- разметка виджета -->

  <!-- Модалки — всегда внутри контейнера, перед закрывающим тегом -->
  <div class="wgt-modal-overlay" data-ref="modal-confirm"
       role="dialog" aria-modal="true" aria-labelledby="wgt-modal-title" hidden>
    <div class="wgt-modal">
      <h2 id="wgt-modal-title" class="wgt-modal__title"></h2>
      <p  class="wgt-modal__body"></p>
      <div class="wgt-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>
</section>

<script>
  /* 1. CLASS
   *   ├── static FORBIDDEN_KEYS
   *   ├── static config props
   *   ├── static seed data
   *   ├── constructor
   *   │     ├── find root (silent return)
   *   │     ├── $ / $$ helpers
   *   │     ├── cache DOM refs via data-ref
   *   │     ├── validate & init state
   *   │     ├── AbortController
   *   │     └── _render() + _bind()
   *   ├── _render() methods
   *   ├── _handle() action methods
   *   ├── _bind() — один listener + switch
   *   ├── _esc() — XSS escaping
   *   ├── destroy()
   *   └── static _validate()
   */

  /* 2. INIT — DOMContentLoaded, одна строка */
</script>
```

---

## 2. HTML

### 2.1 Контейнер

Семантический тег, только класс — никаких `id` на корневом элементе:

```html
<!-- ✅ правильно -->
<section class="orders-container" aria-label="Order list">

<!-- ❌ неправильно — id создаёт глобальную связь с JS -->
<section id="orders-module" class="orders-container">
```

### 2.2 JS-хуки — только data-атрибуты

Класс — это CSS. `data-ref` / `data-action` — это JS. Они никогда не смешиваются:

```html
<!-- ✅ правильно — хуки отделены от стилей -->
<button class="btn btn-primary" data-action="send">Send</button>
<div class="ord-list"           data-ref="list"></div>
<li  class="ord-item"           data-id="order-42" data-state="new"></li>

<!-- ❌ неправильно — класс несёт двойную ответственность -->
<button class="btn btn-primary js-send-btn">Send</button>

<!-- ❌ неправильно — id как JS-хук -->
<button id="send-btn" class="btn btn-primary">Send</button>
```

### 2.3 Модалки — только внутри контейнера

Модалки живут **внутри** контейнера, перед закрывающим тегом. Размещение снаружи — нарушение:

```html
<section class="orders-container">

  <!-- ... основная разметка ... -->

  <!-- ✅ правильно — модалка внутри, токены наследуются -->
  <div class="ord-modal-overlay" data-ref="modal-delete"
       role="dialog" aria-modal="true" aria-labelledby="ord-modal-title" hidden>
    <div class="ord-modal">
      <h2 id="ord-modal-title" class="ord-modal__title">Delete order?</h2>
      <p  class="ord-modal__body">This action cannot be undone.</p>
      <div class="ord-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>

</section>

<!-- ❌ неправильно — снаружи контейнера: токены не работают, стили утекают -->
<div class="ord-modal-overlay">...</div>
```

Почему внутри: CSS custom properties наследуются вниз по дереву. Модалка снаружи контейнера не видит `--ord-*` токены. Кроме того, правило скопинга CSS (§3.1) требует, чтобы каждый селектор начинался с класса контейнера — снаружи это невозможно выполнить.

`position: fixed` работает одинаково независимо от места в DOM — модалка всё равно перекроет весь экран.

### 2.4 ARIA

Минимально необходимое:

```html
<!-- Интерактивные списки -->
<ul role="listbox" aria-label="Order list" aria-activedescendant="">
  <li role="option" aria-selected="false" tabindex="0" id="item-1">...</li>
</ul>

<!-- Живые регионы — обновления для скринридеров -->
<div role="log" aria-live="polite" aria-atomic="false">
  <!-- динамически добавляемые сообщения -->
</div>

<!-- Модальный диалог -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title-id" hidden>
  <h2 id="modal-title-id">Confirm deletion</h2>
</div>
```

Клавиатура для listbox: `↑↓` — фокус, `Home`/`End` — края, `Enter`/`Space` — активация.
Клавиатура для модалки: `Escape` закрывает, фокус возвращается на триггер.

---

## 3. CSS

### 3.1 Скопинг — кардинальное правило

**Каждый CSS-селектор виджета начинается с класса контейнера. Без исключений:**

```css
/* ✅ правильно — стили изолированы */
.orders-container .ord-card        { }
.orders-container .ord-card:hover  { }
.orders-container .ord-modal       { }

/* ❌ неправильно — стили утекают на всю страницу */
.ord-card  { }
.ord-modal { }
```

Модалки — не исключение. `position: fixed` не освобождает от правила скопинга:

```css
/* ✅ правильно — скопировано, хотя визуально на весь экран */
.orders-container .ord-modal-overlay { position: fixed; inset: 0; }

/* ❌ неправильно */
.ord-modal-overlay { position: fixed; inset: 0; }
```

### 3.2 Нейминг классов

Все дочерние классы получают короткий префикс, сокращённый от имени контейнера:

```css
/* контейнер: .messages-container → префикс: msg- */
.messages-container .msg-bubble  { }
.messages-container .msg-input   { }

/* BEM-модификатор: [prefix]-[element]--[modifier] */
.messages-container .msg-bubble--sent { }
.messages-container .msg-bubble--recv { }

/* контейнер: .orders-container → префикс: ord- */
.orders-container .ord-modal-overlay { }
.orders-container .ord-modal         { }
.orders-container .ord-modal__title  { }
```

### 3.3 Состояния через `data-state`

JS-управляемые состояния — через `data-state`, а не через modifier-классы:

```css
/* ✅ предпочтительно — состояние видно прямо в HTML */
.orders-container .ord-item[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* допустимо — BEM-модификатор */
.orders-container .ord-item--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

В JS устанавливай оба — Bootstrap-класс для визуала и `data-state` для CSS-хуков:

```js
el.classList.toggle('active', isActive);
el.dataset.state = isActive ? 'active' : '';
```

### 3.4 CSS custom properties (токены)

Токены объявляются на контейнере — секция `0` стилей. Дочерние правила потребляют токены, не сырые значения:

```css
/* --- 0. Tokens --- */
.orders-container {
  --ord-accent:       var(--bs-primary);
  --ord-card-radius:  .5rem;
  --ord-anim-dur:     150ms;
}

/* Дочерние правила — только токены */
.orders-container .ord-card {
  border-radius: var(--ord-card-radius);
  border-color:  var(--ord-accent);
}

/* Модалка наследует токены автоматически — она внутри контейнера */
.orders-container .ord-modal {
  border-radius: var(--ord-card-radius);
}
```

Bootstrap-классы не выбрасываются — BEM-модификатор только добавляет то, чего Bootstrap не покрывает:

```css
/* ✅ правильно — не дублируем то, что делает Bootstrap */
.messages-container .msg-bubble--sent {
  background: var(--msg-bubble-sent-bg);
  color:      var(--msg-bubble-sent-color);
}

/* ❌ неправильно — дублируем Bootstrap + !important */
.messages-container .msg-bubble--sent {
  background:    var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius) !important;
  padding:       .5rem 1rem !important;
}
```

### 3.5 Стили модалок — секция 3

```css
/* --- 3. Modals --- */

.orders-container .ord-modal-overlay {
  position:        fixed;
  inset:           0;
  z-index:         1050;
  display:         flex;
  align-items:     center;
  justify-content: center;
  background:      rgba(0, 0, 0, .45);
}

.orders-container .ord-modal-overlay[hidden] {
  display: none;
}

.orders-container .ord-modal {
  background:    var(--bs-body-bg);
  border-radius: var(--ord-card-radius, .5rem);
  box-shadow:    0 8px 32px rgba(0, 0, 0, .18);
  padding:       1.5rem;
  width:         min(480px, 90vw);
  max-height:    90vh;
  overflow-y:    auto;
  animation:     ord-modal-in var(--ord-anim-dur, 150ms) ease-out both;
}

.orders-container .ord-modal__title   { font-size: 1.125rem; font-weight: 600; margin-bottom: .5rem; }
.orders-container .ord-modal__body    { color: var(--bs-secondary-color); margin-bottom: 1.5rem; }
.orders-container .ord-modal__actions { display: flex; gap: .5rem; justify-content: flex-end; }
```

### 3.6 Анимации

`@keyframes` имена несут префикс виджета — имена кейфреймов глобальны:

```css
/* --- 5. Animations --- */

/* ✅ правильно — префикс защищает от конфликтов */
@keyframes ord-modal-in {
  from { opacity: 0; transform: scale(.95); }
  to   { opacity: 1; transform: scale(1);   }
}

/* ❌ неправильно — может конфликтовать с другим виджетом */
@keyframes modal-in { }
```

Анимируй только `transform` и `opacity` — они работают на compositor thread без reflow и repaint.

---

## 4. JavaScript

### 4.1 Структура класса

```js
class WidgetController {

  // ─── 0. STATIC CONFIG ──────────────────────────────────────
  static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
  static DELAY_MS       = 1000;
  static MAX_PREVIEW    = 38;

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────
  constructor(selector, opts = {}) {

    // 1a. Найти корень — тихий выход если не найден
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Хелперы — скопированы на this._root, не достают наружу
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Кэшируем DOM-ссылки через data-ref — один раз, здесь
    this._list    = $('[data-ref="list"]');
    this._input   = $('[data-ref="input"]');
    this._sendBtn = $('[data-ref="send-btn"]');

    // 1d. Модалки — тот же $ хелпер, они внутри контейнера
    this._modalDelete = $('[data-ref="modal-delete"]');

    // 1e. Опции с дефолтами из static свойств
    this._delay = opts.delay ?? WidgetController.DELAY_MS;

    // 1f. Данные — валидируем перед использованием
    const raw  = opts.data ?? WidgetController.SEED_DATA;
    const data = raw.filter(d => WidgetController._validate(d));

    // 1g. State — единственный источник истины
    this._state = {
      items:    data,
      activeId: null,
      loading:  false,
      modal:    null,  // { type: 'delete', targetId: '...' } | null
    };

    // 1h. AbortController — один abort() убивает все listeners
    this._ac = new AbortController();

    // 1i. Запуск
    this._render();
    this._bind();
  }

  // ─── 2. RENDER ─────────────────────────────────────────────

  _render() {
    // Весь рендер — производное от this._state
    // Никогда не читаем состояние из DOM
    this._renderList();
    this._renderModal();
  }

  _renderList() {
    // ✅ пользовательский текст — textContent, данные API — _esc()
    this._list.innerHTML = this._state.items.map(item => `
      <li class="ord-item"
          data-id="${this._esc(item.id)}"
          data-state="${this._esc(item.status)}">
        <span class="ord-item__name">${this._esc(item.name)}</span>
        <button class="btn btn-sm btn-danger" data-action="remove" data-id="${this._esc(item.id)}">
          Remove
        </button>
      </li>
    `).join('');
  }

  _renderModal() {
    // Видимость модалки — из state, не из DOM
    const { modal } = this._state;
    this._modalDelete.hidden = modal?.type !== 'delete';
    if (modal?.type === 'delete') {
      this._modalDelete.querySelector('[data-ref="modal-body"]')
        .textContent = `Delete order #${modal.targetId}?`;
      // textContent — потому что targetId это пользовательские данные
    }
  }

  // ─── 3. ACTIONS ────────────────────────────────────────────

  _handleRemove(id) {
    this._lastFocused = document.activeElement;
    this._state.modal = { type: 'delete', targetId: id };
    this._renderModal();
    this._modalDelete.querySelector('button').focus();
  }

  _handleModalConfirm() {
    const { modal } = this._state;
    if (modal?.type === 'delete') this._deleteItem(modal.targetId);
    this._closeModal();
  }

  _closeModal() {
    this._state.modal = null;
    this._renderModal();
    this._lastFocused?.focus();
  }

  _deleteItem(id) {
    this._state.items = this._state.items.filter(i => i.id !== id);
    this._renderList();
  }

  // ─── 4. EVENTS ─────────────────────────────────────────────

  _bind() {
    const sig = { signal: this._ac.signal };

    // Один listener на корне — покрывает виджет и модалки
    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;

      switch (btn.dataset.action) {
        case 'send':          this._submit(); break;
        case 'remove':        this._handleRemove(btn.dataset.id); break;
        case 'modal-cancel':  this._closeModal(); break;
        case 'modal-confirm': this._handleModalConfirm(); break;
      }
    }, sig);

    // passive: true — не блокируем scroll
    this._root.addEventListener('scroll', this._onScroll.bind(this),
      { signal: this._ac.signal, passive: true });

    this._input?.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._submit(); }
    }, sig);

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && this._state.modal) this._closeModal();
    }, sig);
  }

  // ─── 5. HELPERS ────────────────────────────────────────────

  /**
   * Экранирует 7 OWASP-символов.
   * Обязателен для всех данных в innerHTML — пользовательских И серверных.
   * Пользовательский текст → textContent (никогда innerHTML).
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

  _cut(s, maxLen) {
    return s.length > maxLen ? s.slice(0, maxLen) + '…' : s;
  }

  // ─── 6. LIFECYCLE ──────────────────────────────────────────

  destroy() {
    this._ac.abort(); // убивает все listeners одним вызовом
  }

  // ─── 7. STATIC ─────────────────────────────────────────────

  /**
   * Защита от prototype pollution.
   * Вызывается в конструкторе, не в INIT.
   * Проверяет объект и вложенные массивы рекурсивно.
   */
  static _validate(obj) {
    const forbidden = WidgetController.FORBIDDEN_KEYS;
    if (!obj || typeof obj !== 'object') return false;
    if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
    for (const key of Object.keys(obj)) {
      if (Array.isArray(obj[key])) {
        for (const child of obj[key]) {
          if (!WidgetController._validate(child)) return false;
        }
      }
    }
    return true;
  }
}

// Seed-данные после тела класса — для читаемости
WidgetController.SEED_DATA = [];
```

### 4.2 Тихий выход — обязателен

```js
// ✅ правильно — виджет безопасно включать на любой странице
this._root = document.querySelector(selector);
if (!this._root) return;

// ❌ неправильно — бросает ошибку на каждой странице без виджета
if (!this._root) throw new Error('container not found');
```

### 4.3 Хелперы `$` / `$$`

Объявляются в конструкторе, скопированы на `this._root`. Физически не могут достать наружу:

```js
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

// ✅ Все запросы только через хелперы
this._list  = $('[data-ref="list"]');
this._modal = $('[data-ref="modal-delete"]');

// ❌ Запрещено — достаёт за пределы контейнера
this._list  = document.querySelector('[data-ref="list"]');
this._modal = document.getElementById('modal-delete');
```

### 4.4 State — единственный источник истины

UI — это проекция state. Никогда не читаем состояние из DOM:

```js
// ✅ правильно — обновляем state, потом рендерим
_select(id) {
  this._state.activeId = id;
  this._render();
}

// ❌ неправильно — читаем состояние из DOM
_select(id) {
  const current = this._root.querySelector('[data-state="active"]')?.dataset.id;
}
```

### 4.5 XSS — правило без исключений

Это место где безопасность отменяет удобство:

```js
// ✅ пользовательский текст — ТОЛЬКО textContent
bubble.textContent = userMessage;

// ✅ данные API/сервера в innerHTML — ТОЛЬКО через _esc()
li.innerHTML = `
  <span class="name">${this._esc(apiData.name)}</span>
  <span class="date">${this._esc(apiData.date)}</span>
`;

// ❌ ЗАПРЕЩЕНО — прямой innerHTML с любыми внешними данными
bubble.innerHTML = userMessage;
li.innerHTML = `<span>${apiData.name}</span>`;

// ❌ ЗАПРЕЩЕНО — даже если кажется безопасным
container.innerHTML = serverRenderedHtml;
```

Правило: если данные пришли не из твоего кода — они идут через `_esc()` или `textContent`.

### 4.6 Prototype pollution — защита в конструкторе

`_validate()` вызывается в конструкторе до того как данные попадают в state. В `INIT` блоке никакой логики нет:

```js
// ✅ правильно — валидация внутри конструктора
constructor(selector, opts = {}) {
  const raw  = opts.data ?? WidgetController.SEED_DATA;
  const data = raw.filter(d => WidgetController._validate(d));
  this._state = { items: data, ... };
}

// ❌ неправильно — логика в INIT
document.addEventListener('DOMContentLoaded', () => {
  const safeData = rawData.filter(d => validate(d)); // логика не здесь
  new OrdersController('.orders-container', { data: safeData });
});
```

### 4.7 AbortController — очистка одним вызовом

Каждый `addEventListener` регистрируется с `{ signal: this._ac.signal }`. `destroy()` — одна строка:

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   handler, sig);
  this._root.addEventListener('keydown', handler, sig);
  window.addEventListener('resize',      handler, sig);
  document.addEventListener('keydown',   handler, sig);
  // scroll и touch — добавляем passive: true
  this._root.addEventListener('scroll',  handler, { ...sig, passive: true });
}

destroy() {
  this._ac.abort(); // все listeners выше убиты одновременно
}
```

### 4.8 Делегирование событий

Один listener на корне через `e.target.closest('[data-action]')` — покрывает весь виджет включая модалки и динамически добавленные элементы:

```js
// ✅ правильно — один listener, всё через switch
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  switch (btn.dataset.action) {
    case 'send':          this._submit(); break;
    case 'remove':        this._handleRemove(btn.dataset.id); break;
    case 'modal-cancel':  this._closeModal(); break;
    case 'modal-confirm': this._handleModalConfirm(); break;
  }
}, { signal: this._ac.signal });

// ❌ неправильно — отдельные listeners на каждом элементе
this._sendBtn.addEventListener('click', () => this._submit());
this._modalConfirmBtn.addEventListener('click', () => this._handleModalConfirm());
```

Сложная логика — выносится в именованный метод, не остаётся в switch:

```js
// ✅ правильно
case 'remove': this._handleRemove(btn.dataset.id); break;

_handleRemove(id) {
  this._lastFocused = document.activeElement;
  this._state.modal = { type: 'delete', targetId: id };
  this._renderModal();
}

// ❌ неправильно — логика внутри switch/listener
case 'remove': {
  const focused = document.activeElement;
  this._state.modal = { type: 'delete', targetId: btn.dataset.id };
  this._renderModal();
  // ... ещё 10 строк
  break;
}
```

---

## 5. Производительность — финальный аудит

Раздел не меняет архитектуру. Это чек-лист после того как код написан по правилам выше.

### 5.1 Layout Thrashing

Никогда не читай геометрию сразу после записи стилей в цикле:

```js
// ❌ ПЛОХО — forced reflow на каждой итерации
items.forEach(el => {
  el.style.width = '100px';
  const h = el.offsetHeight; // читаем после записи → принудительный reflow
  el.style.height = h * 2 + 'px';
});

// ✅ ХОРОШО — сначала все чтения, потом все записи
const heights = items.map(el => el.offsetHeight); // все чтения разом
items.forEach((el, i) => {
  el.style.width  = '100px';
  el.style.height = heights[i] * 2 + 'px';        // все записи разом
});
```

Свойства, вызывающие forced reflow при чтении:
`offsetTop`, `offsetHeight`, `scrollTop`, `clientWidth`, `getBoundingClientRect()`, `getComputedStyle()`.

### 5.2 Пассивные listeners для scroll/touch

```js
// ❌ ПЛОХО — браузер ждёт завершения обработчика перед скроллом → [Violation]
this._root.addEventListener('scroll', handler);
window.addEventListener('touchstart', handler);

// ✅ ХОРОШО — браузер скроллит немедленно, не ждёт
this._root.addEventListener('scroll',     handler, { signal: this._ac.signal, passive: true });
window.addEventListener('touchstart',     handler, { signal: this._ac.signal, passive: true });
window.addEventListener('touchmove',      handler, { signal: this._ac.signal, passive: true });
```

### 5.3 Throttle для частых событий

```js
// scroll, mousemove, resize — могут стрелять сотни раз в секунду
_bind() {
  const sig = { signal: this._ac.signal, passive: true };
  this._root.addEventListener('scroll',
    this._throttle(this._onScroll.bind(this), 16), sig); // ~60fps
}

_throttle(fn, limit) {
  let last = 0;
  return (...args) => {
    const now = Date.now();
    if (now - last >= limit) { last = now; fn(...args); }
  };
}
```

### 5.4 Стили через classList

```js
// ❌ ПЛОХО — потенциально 3 отдельных reflow
el.style.width  = '100px';
el.style.height = '100px';
el.style.color  = 'red';

// ✅ ХОРОШО — один reflow
el.classList.add('is-active');
// CSS: .widget-container .el.is-active { width: 100px; height: 100px; color: red; }

// или одной строкой
el.style.cssText = 'width:100px; height:100px; color:red';
```

### 5.5 DocumentFragment для массовой вставки

```js
// ❌ ПЛОХО — reflow на каждый appendChild
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  this._list.appendChild(li);
});

// ✅ ХОРОШО — один reflow
// Вариант 1: innerHTML (рекомендуется — проще и не медленнее)
this._list.innerHTML = items.map(item =>
  `<li data-id="${this._esc(item.id)}">${this._esc(item.name)}</li>`
).join('');

// Вариант 2: DocumentFragment (если нужно сохранить существующие listeners)
const frag = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name; // textContent безопасен без _esc()
  frag.appendChild(li);
});
this._list.appendChild(frag);
```

---

## 6. Инициализация

### 6.1 Стандартный паттерн — всегда одна строка

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
});
```

`DOMContentLoaded` работает независимо от места `<script>` в документе. Вся логика — в конструкторе. В INIT нет ничего кроме `new`.

### 6.2 С переопределением

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container', { data: apiData, delay: 500 });
});
```

### 6.3 Несколько экземпляров

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.orders-container').forEach(el => {
    new OrdersController(el);
  });
});
```

Все DOM-запросы скопированы на `this._root` — несколько экземпляров на странице никогда не конфликтуют, даже с одинаковыми `data-ref` внутри.

---

## 7. Нейминг

### 7.1 Классы и файлы

| Что | Конвенция | Пример |
|---|---|---|
| ES6 класс | PascalCase + `Controller` | `OrdersController` |
| CSS контейнер | kebab + `-container` | `.orders-container` |
| CSS префикс дочерних | короткий kebab | `ord-` |
| BEM модификатор | `[prefix]-[el]--[mod]` | `.ord-item--cancelled` |
| Модальный оверлей | `[prefix]-modal-overlay` | `.ord-modal-overlay` |
| HTML файл | `feature-hash.html` | `orders-4f.html` |

### 7.2 data-атрибуты

| Назначение | Атрибут | Пример |
|---|---|---|
| DOM-ссылка (кэш в конструкторе) | `data-ref` | `data-ref="send-btn"` |
| Триггер действия | `data-action` | `data-action="send"` |
| Открытие модалки | `data-action` | `data-action="modal-open-delete"` |
| Отмена модалки | `data-action` | `data-action="modal-cancel"` |
| Подтверждение модалки | `data-action` | `data-action="modal-confirm"` |
| Идентификатор записи | `data-id` | `data-id="order-42"` |
| JS-состояние (также CSS-хук) | `data-state` | `data-state="active"` |

### 7.3 Static свойства

| Что | Конвенция | Пример |
|---|---|---|
| Конфиг-константа | SCREAMING_SNAKE | `static DELAY_MS = 1000` |
| Заморозка | SCREAMING_SNAKE | `static FORBIDDEN_KEYS = Object.freeze([...])` |
| Seed-данные | SCREAMING_SNAKE | `static SEED_DATA = [...]` |

---

## 8. Чеклист перед коммитом

### Нулевой закон (data-атрибуты)
- [ ] Нет `getElementById` ни в одном JS-файле (кроме ARIA/якорей)
- [ ] Нет `querySelector('.class')` для логики
- [ ] Нет `querySelector('#id')` для логики
- [ ] Нет `getElementsByClassName`
- [ ] Нет jQuery (`$`, `jQuery`)
- [ ] Нет `js-*` классов в HTML
- [ ] Все JS-хуки — только `data-ref`, `data-action`, `data-id`, `data-state`
- [ ] `document.querySelector` используется только для bootstrap инициализации по классу контейнера

### HTML
- [ ] Контейнер — семантический тег, только класс (нет `id`)
- [ ] Модалки внутри контейнера, перед закрывающим тегом
- [ ] Каждая модалка имеет `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, `hidden`
- [ ] ARIA: `role`, `aria-label`, `aria-live` где применимо
- [ ] Клавиатурная навигация реализована для интерактивных списков

### CSS
- [ ] Каждый селектор начинается с класса контейнера
- [ ] Секция 0 — токены объявлены на контейнере
- [ ] Стили модалок в секции 3
- [ ] `@keyframes` имена с префиксом виджета
- [ ] Все `@keyframes` в секции 5
- [ ] Нет `!important` в modifier-правилах
- [ ] Анимации только через `transform` и `opacity`

### JS — архитектура
- [ ] Нет loose констант над классом — всё `static`
- [ ] Конструктор `(selector, opts = {})`
- [ ] Тихий выход если контейнер не найден
- [ ] `$` / `$$` хелперы в конструкторе, скопированы на `this._root`
- [ ] DOM-ссылки кэшированы через `data-ref` в конструкторе, нигде больше
- [ ] State — единственный источник истины, DOM не читается как источник данных
- [ ] Видимость модалки из `this._state.modal`, не из DOM
- [ ] Один root click listener + switch для всех `[data-action]`
- [ ] Сложные обработчики вынесены в именованные `_handleXxx()` методы
- [ ] `AbortController` в конструкторе, signal везде
- [ ] `destroy()` вызывает `this._ac.abort()`
- [ ] `_closeModal()` возвращает фокус на `this._lastFocused`

### JS — безопасность
- [ ] Пользовательский текст — только `textContent`, никогда `innerHTML`
- [ ] Все данные в `innerHTML` — только через `_esc()`
- [ ] Внешние данные валидируются через `static _validate()` в конструкторе
- [ ] `FORBIDDEN_KEYS` включает `__proto__`, `constructor`, `prototype`

### JS — производительность
- [ ] Нет чтения геометрии после записи стилей в одном цикле (Layout Thrashing)
- [ ] `scroll`, `touchstart`, `touchmove` используют `passive: true`
- [ ] `scroll`, `mousemove`, `resize` используют throttle/debounce
- [ ] Стили меняются через `classList` или `cssText`, не через `.style.*` по одному
- [ ] Нет `[Violation]` в консоли браузера

### INIT
- [ ] `DOMContentLoaded` оборачивает инициализацию
- [ ] Инициализация — одна строка `new WidgetController('.widget-container')`
- [ ] Нет никакой логики в INIT — всё в конструкторе
