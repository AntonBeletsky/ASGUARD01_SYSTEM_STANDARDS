# Clean Code: HTML, CSS & JavaScript
> Практическое руководство. Без воды, без академизма — только правила, антипаттерны и рабочие примеры.

---

## Table of Contents

1. [Почему «чистый код» — это не эстетика, а выживание](#1-почему-чистый-код--это-не-эстетика-а-выживание)
2. [HTML — структура и смысл](#2-html--структура-и-смысл)
3. [CSS — порядок и инкапсуляция](#3-css--порядок-и-инкапсуляция)
4. [JavaScript — логика без хаоса](#4-javascript--логика-без-хаоса)
5. [Правила взаимодействия HTML + CSS + JS](#5-правила-взаимодействия-html--css--js)
6. [Универсальные правила чистого кода](#6-универсальные-правила-чистого-кода)
7. [Red Flags — это надо рефакторить прямо сейчас](#7-red-flags--это-надо-рефакторить-прямо-сейчас)
8. [Чеклист перед коммитом](#8-чеклист-перед-коммитом)

---

## 1. Почему «чистый код» — это не эстетика, а выживание

Грязный код не просто некрасив. Он создаёт конкретные проблемы:

| Проблема | Симптом |
|---|---|
| Глобальные селекторы | Два виджета на странице → оба сломаны |
| Стили и логика в одних классах | Переименовал класс в CSS → упал JS |
| Состояние в DOM | Дублируешь элемент → дублируешь баги |
| Вешаешь листенер на каждый элемент | Добавил элемент динамически → нет реакции |
| Функции по 200 строк | Меняешь одно → ломается другое |
| Магические числа и строки | `if (status === 3)` — что такое 3? |

Цель чистого кода — **чтобы любой разработчик (включая тебя через 6 месяцев) понял, что происходит, не запуская отладчик**.

---

## 2. HTML — структура и смысл

### Правило 1: HTML — это контент и структура, не стили и не логика

HTML описывает **что** это, не **как** выглядит и не **что делает**.

```html
<!-- 🍝 Плохо: стиль захардкожен, смысла нет -->
<div style="color: red; font-weight: bold; cursor: pointer;" onclick="doSomething()">
  Click me
</div>

<!-- ✅ Хорошо: структура + семантика, всё остальное снаружи -->
<button type="button" class="alert-btn" data-js="dismiss-alert">
  Dismiss
</button>
```

### Правило 2: Используй семантические теги

Каждый тег несёт смысл. Скринридеры, SEO и твои коллеги скажут спасибо.

```html
<!-- 🍝 Плохо: div на всё -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>
<div class="main-content">
  <div class="article">
    <div class="article-title">Hello</div>
    <div class="article-body">...</div>
  </div>
</div>

<!-- ✅ Хорошо: теги говорят сами за себя -->
<header>
  <nav>
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Hello</h1>
    <p>...</p>
  </article>
</main>
```

**Шпаргалка семантики:**

| Тег | Когда использовать |
|---|---|
| `<header>` | Шапка страницы или секции |
| `<nav>` | Навигационные ссылки |
| `<main>` | Основной контент страницы (один на странице) |
| `<section>` | Тематически обособленный блок с заголовком |
| `<article>` | Самодостаточный контент (пост, карточка товара) |
| `<aside>` | Боковой контент, связанный с основным |
| `<footer>` | Подвал страницы или секции |
| `<button>` | Действие — всегда `<button>`, не `<div>` |
| `<a>` | Навигация — всегда `<a>`, не `<button>` |
| `<figure>` + `<figcaption>` | Картинка с подписью |

### Правило 3: Атрибуты — по делу

```html
<!-- 🍝 Плохо -->
<img src="photo.jpg">
<input type="text">
<button>Submit</button>

<!-- ✅ Хорошо -->
<img src="photo.jpg" alt="Portrait of user John Doe" width="300" height="300">
<input type="email" id="user-email" name="email" autocomplete="email" required
       aria-label="Email address" placeholder="you@example.com">
<button type="submit" aria-label="Submit registration form">Submit</button>
```

Обязательные атрибуты:
- `alt` на каждом `<img>` (пустой `alt=""` если декоративное)
- `type` на каждом `<button>` (`button`, `submit`, `reset`)
- `for` на каждом `<label>` → привязан к `id` input
- `lang` на `<html>` тег

### Правило 4: Не злоупотребляй ID

ID — глобальный идентификатор. На странице он должен быть **один**. Это делает компоненты неповторяемыми.

```html
<!-- 🍝 Плохо: ID как крючок для JS и CSS одновременно -->
<div id="wishlist-items" class="wishlist">...</div>

<!-- ✅ Хорошо: ID только если реально нужен один глобальный элемент
     (якорная ссылка, ARIA-атрибут). Для JS — data-js. -->
<div class="wishlist" data-js="wishlist" aria-label="Your wishlist">...</div>
```

### Правило 5: Разделяй крючки для CSS и JS

```html
<!-- 🍝 Плохо: один атрибут делает всё -->
<button class="btn btn-primary delete-btn">Delete</button>
<!-- Если переименуешь .delete-btn в CSS — сломается JS -->

<!-- ✅ Хорошо: явное разделение ответственности -->
<button class="btn btn-primary" data-js="delete-btn">Delete</button>
<!-- class → CSS, data-js → JS. Независимо. -->
```

---

## 3. CSS — порядок и инкапсуляция

### Правило 1: Один класс — одна ответственность

```css
/* 🍝 Плохо: класс делает всё */
.card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  color: red;          /* это состояние ошибки */
  font-size: 11px;     /* это типографика */
  opacity: 0.5;        /* это disabled-состояние */
}

/* ✅ Хорошо: базовый класс + модификаторы */
.card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.card--error   { color: red; }
.card--small   { font-size: 11px; }
.card--disabled { opacity: 0.5; pointer-events: none; }
```

### Правило 2: Используй CSS-переменные для всего, что повторяется

```css
/* 🍝 Плохо: магические числа везде */
.btn       { background: #2563eb; border-radius: 6px; }
.badge     { background: #2563eb; }
.link      { color: #2563eb; }
.input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.2); }

/* ✅ Хорошо: одно место — все цвета и размеры */
:root {
  --color-primary:        #2563eb;
  --color-primary-light:  rgba(37, 99, 235, 0.15);
  --color-error:          #dc2626;
  --color-text:           #111827;
  --color-text-muted:     #6b7280;
  --color-bg:             #ffffff;
  --color-border:         #e5e7eb;

  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   16px;

  --space-xs:    4px;
  --space-sm:    8px;
  --space-md:    16px;
  --space-lg:    24px;
  --space-xl:    40px;

  --font-size-sm:   13px;
  --font-size-base: 16px;
  --font-size-lg:   20px;
  --font-size-xl:   28px;

  --transition-base: 150ms ease;
}

.btn       { background: var(--color-primary); border-radius: var(--radius-md); }
.badge     { background: var(--color-primary); }
.link      { color: var(--color-primary); }
.input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
```

### Правило 3: Порядок свойств в блоке

Не рандомный. Читается сверху вниз: **откуда это? → что это? → как выглядит внутри → декорации**

```css
.component {
  /* 1. Позиционирование (влияет на других) */
  position: relative;
  top: 0;
  z-index: 10;

  /* 2. Блочная модель (собственный размер) */
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 400px;
  padding: var(--space-md);
  margin: 0 auto;

  /* 3. Типографика */
  font-size: var(--font-size-base);
  font-weight: 500;
  line-height: 1.5;
  color: var(--color-text);

  /* 4. Визуал */
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  /* 5. Поведение */
  cursor: pointer;
  transition: box-shadow var(--transition-base);
  overflow: hidden;
}
```

### Правило 4: Состояния — явно и предсказуемо

```css
/* Все состояния одного компонента — рядом */
.btn { ... }                         /* base */
.btn:hover { ... }                   /* hover */
.btn:focus-visible { ... }           /* keyboard focus — не :focus */
.btn:active { ... }                  /* press */
.btn:disabled,
.btn[aria-disabled="true"] { ... }   /* disabled */
.btn--loading { ... }                /* async state */
.btn--error { ... }                  /* error state */
```

### Правило 5: Не хакай специфичность

```css
/* 🍝 Плохо: войны специфичности */
div.container > ul > li.item .title { color: red; }
#main .sidebar .widget h2.title { color: blue !important; }

/* ✅ Хорошо: плоская специфичность, максимум один уровень вложенности */
.card-title          { color: var(--color-text); }
.card-title--error   { color: var(--color-error); }

/* !important — только для utility классов, и только там */
.visually-hidden {
  position: absolute !important;
  width: 1px !important;
  clip: rect(0 0 0 0) !important;
  overflow: hidden !important;
}
```

### Правило 6: Mobile-first медиазапросы

```css
/* 🍝 Плохо: desktop-first, переопределяешь всё */
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; gap: 12px; }
}

/* ✅ Хорошо: mobile-first, добавляешь только то, что нужно */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-sm);
}
@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(4, 1fr); gap: var(--space-lg); }
}
```

---

## 4. JavaScript — логика без хаоса

### Правило 1: Функции делают одно дело

Название функции должно полностью описывать, что она делает. Если нужен союз «и» — это уже две функции.

```js
// 🍝 Плохо: одна функция делает всё
function handleSubmit() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  if (!name || !email) {
    document.getElementById('error').textContent = 'Fill all fields';
    document.getElementById('error').style.display = 'block';
    return;
  }
  fetch('/api/submit', { method: 'POST', body: JSON.stringify({ name, email }) })
    .then(r => r.json())
    .then(data => {
      document.getElementById('form').style.display = 'none';
      document.getElementById('success').style.display = 'block';
      document.getElementById('success').textContent = `Welcome, ${data.name}!`;
    });
}

// ✅ Хорошо: каждая функция — одна задача
function getFormData(els) {
  return {
    name:  els.nameInput.value.trim(),
    email: els.emailInput.value.trim(),
  };
}

function validateFormData({ name, email }) {
  if (!name)  return 'Name is required';
  if (!email) return 'Email is required';
  if (!email.includes('@')) return 'Email is invalid';
  return null; // null = valid
}

function showError(els, message) {
  els.errorMsg.textContent = message;
  els.errorMsg.hidden = false;
}

function showSuccess(els, userName) {
  els.form.hidden = true;
  els.successMsg.textContent = `Welcome, ${userName}!`;
  els.successMsg.hidden = false;
}

async function submitFormData(data) {
  const response = await fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function handleSubmit(els) {
  const data = getFormData(els);
  const error = validateFormData(data);
  if (error) { showError(els, error); return; }

  try {
    const result = await submitFormData(data);
    showSuccess(els, result.name);
  } catch (err) {
    showError(els, 'Something went wrong. Please try again.');
    console.error('Form submit failed:', err);
  }
}
```

### Правило 2: Именование — это документация

```js
// 🍝 Плохо: загадочные имена
const d  = new Date();
const u  = getUser();
const arr = users.filter(x => x.a === true);
function proc(i) { ... }
let flag = false;

// ✅ Хорошо: имя = намерение
const createdAt    = new Date();
const currentUser  = getUser();
const activeUsers  = users.filter(user => user.isActive);
function processPayment(invoice) { ... }
let isMenuOpen = false;

// Булевы переменные — всегда is/has/can/should
let isLoading    = false;
let hasErrors    = false;
let canSubmit    = true;
let shouldRetry  = false;

// Массивы — во множественном числе
const users   = [];
const prices  = [];
const options = [];

// Функции — глагол + существительное
function fetchUserProfile(userId) { ... }
function updateCartTotal(items) { ... }
function validateEmailFormat(email) { ... }
function renderProductCard(product) { ... }
```

### Правило 3: Никаких магических значений

```js
// 🍝 Плохо: что такое 3? что такое 'active'?
if (user.role === 3) { ... }
if (order.status === 'A') { ... }
setTimeout(cleanup, 5000);

// ✅ Хорошо: константы с именами
const USER_ROLES = {
  GUEST:  1,
  USER:   2,
  ADMIN:  3,
};

const ORDER_STATUS = {
  PENDING:   'P',
  ACTIVE:    'A',
  COMPLETED: 'C',
  CANCELLED: 'X',
};

const CLEANUP_DELAY_MS = 5_000;

if (user.role === USER_ROLES.ADMIN) { ... }
if (order.status === ORDER_STATUS.ACTIVE) { ... }
setTimeout(cleanup, CLEANUP_DELAY_MS);
```

### Правило 4: Ранний возврат вместо вложенных if

```js
// 🍝 Плохо: пирамида смерти
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.user) {
        if (order.user.isVerified) {
          // настоящая логика — на 4 уровне вложенности
          submitOrder(order);
        } else {
          showError('User not verified');
        }
      } else {
        showError('No user attached');
      }
    } else {
      showError('Cart is empty');
    }
  } else {
    showError('No order');
  }
}

// ✅ Хорошо: guard clauses — выходим рано при ошибках
function processOrder(order) {
  if (!order)                   return showError('No order');
  if (order.items.length === 0) return showError('Cart is empty');
  if (!order.user)              return showError('No user attached');
  if (!order.user.isVerified)   return showError('User not verified');

  // настоящая логика — не утопает во вложенности
  submitOrder(order);
}
```

### Правило 5: Обработка ошибок — везде, где что-то может упасть

```js
// 🍝 Плохо: fetch без обработки ошибок
async function loadProducts() {
  const data = await fetch('/api/products').then(r => r.json());
  renderProducts(data);
}

// ✅ Хорошо
async function loadProducts(els) {
  els.loadingSpinner.hidden = false;
  els.errorMsg.hidden = true;

  try {
    const response = await fetch('/api/products');

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const products = await response.json();

    if (!Array.isArray(products)) {
      throw new TypeError('Expected an array of products');
    }

    renderProducts(els, products);

  } catch (err) {
    // Показываем пользователю — понятное сообщение
    els.errorMsg.textContent = 'Failed to load products. Please refresh.';
    els.errorMsg.hidden = false;

    // Логируем для разработчика — полный контекст
    console.error('[loadProducts] Failed:', err);
  } finally {
    els.loadingSpinner.hidden = true;
  }
}
```

### Правило 6: Иммутабельность данных

```js
// 🍝 Плохо: мутируем данные напрямую
function addToCart(cart, product) {
  cart.items.push(product);              // мутация массива
  cart.total += product.price;           // мутация объекта
  return cart;                           // возвращаем тот же объект
}

function removeFromCart(cart, productId) {
  const index = cart.items.findIndex(i => i.id === productId);
  cart.items.splice(index, 1);           // мутация
}

// ✅ Хорошо: всегда новый объект
function addToCart(cart, product) {
  return {
    ...cart,
    items: [...cart.items, product],
    total: cart.total + product.price,
  };
}

function removeFromCart(cart, productId) {
  const newItems = cart.items.filter(item => item.id !== productId);
  return {
    ...cart,
    items: newItems,
    total: newItems.reduce((sum, item) => sum + item.price, 0),
  };
}

// Использование
let cart = { items: [], total: 0 };
cart = addToCart(cart, { id: '1', name: 'Shoes', price: 99 });
cart = removeFromCart(cart, '1');
```

---

## 5. Правила взаимодействия HTML + CSS + JS

Это самая важная секция. Большинство «спагетти» рождается именно здесь.

### Три слоя, три ответственности

```
HTML  →  Структура и семантика. Что это и из чего состоит.
CSS   →  Внешний вид. Как это выглядит в каждом состоянии.
JS    →  Поведение. Что происходит при действиях пользователя.
```

Каждый слой меняет DOM своим способом:

```
HTML          — задаёт начальную структуру
CSS классы    — управляют состоянием визуала (is-open, has-error, is-loading)
data-атрибуты — хуки для JS (data-js, data-action, data-id)
JS            — добавляет/убирает CSS-классы состояний и читает data-атрибуты
```

### Паттерн: CSS управляет видимостью, JS управляет классами

```css
/* CSS: определяем все состояния */
.dropdown__menu             { display: none; }
.dropdown__menu.is-open     { display: block; }

.form__error                { display: none; }
.form__error.is-visible     { display: block; color: var(--color-error); }

.btn.is-loading             { pointer-events: none; opacity: 0.7; }
.btn.is-loading::after      { content: '...'; }
```

```js
// JS: только переключает классы — не трогает style напрямую
function toggleDropdown(els) {
  const isOpen = els.menu.classList.toggle('is-open');
  els.toggle.setAttribute('aria-expanded', isOpen);
}

function showFieldError(fieldEl, message) {
  const errorEl = fieldEl.closest('.form__field')
                          .querySelector('[data-js="field-error"]');
  errorEl.textContent = message;
  errorEl.classList.add('is-visible');
  fieldEl.setAttribute('aria-invalid', 'true');
}

function setButtonLoading(btnEl, isLoading) {
  btnEl.classList.toggle('is-loading', isLoading);
  btnEl.disabled = isLoading;
}
```

**Правило:** JS никогда не пишет `element.style.display = 'none'`. Только добавляет/убирает классы.

### Паттерн: состояние — в JS, рендер — в одном месте

```js
// ✅ Единственная функция, которая пишет в DOM
function render(state, els) {
  // Список товаров
  els.list.innerHTML = state.items.map(item => `
    <li class="wishlist__item" data-js="wishlist-item" data-item-id="${item.id}">
      <span class="wishlist__item-name">${escapeHtml(item.name)}</span>
      <button class="btn btn--icon" data-js="remove-btn" aria-label="Remove ${escapeHtml(item.name)}">
        ×
      </button>
    </li>
  `).join('');

  // Пустое состояние
  els.emptyMsg.hidden = state.items.length > 0;

  // Счётчик
  els.counter.textContent = state.items.length;
  els.counter.hidden = state.items.length === 0;
}

// Любое изменение: обновляем state → вызываем render
function removeItem(state, id) {
  return { ...state, items: state.items.filter(item => item.id !== id) };
}
```

### Паттерн: полная инкапсуляция компонента

```js
function createWishlist(rootEl) {
  // 1. Все DOM-запросы — один раз, в одном месте
  const els = {
    list:      rootEl.querySelector('[data-js="wishlist-list"]'),
    emptyMsg:  rootEl.querySelector('[data-js="empty-msg"]'),
    counter:   rootEl.querySelector('[data-js="counter"]'),
    selectAll: rootEl.querySelector('[data-js="select-all-btn"]'),
  };

  // 2. Состояние — в JS, не в DOM
  let state = {
    items:    [],
    selected: new Set(),
  };

  // 3. Рендер — единственная точка записи в DOM
  function render() {
    els.list.innerHTML = state.items.map(item => `
      <li data-js="wishlist-item" data-item-id="${item.id}"
          aria-selected="${state.selected.has(item.id)}">
        <span>${escapeHtml(item.name)}</span>
        <button data-js="remove-btn">Remove</button>
      </li>
    `).join('');

    els.emptyMsg.hidden    = state.items.length > 0;
    els.counter.textContent = state.items.length;
  }

  // 4. Делегированные события — один листенер на всё
  els.list.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('[data-js="remove-btn"]');
    if (removeBtn) {
      const itemEl = removeBtn.closest('[data-js="wishlist-item"]');
      setState({ items: state.items.filter(i => i.id !== itemEl.dataset.itemId) });
    }

    const itemEl = e.target.closest('[data-js="wishlist-item"]');
    if (itemEl && !e.target.closest('button')) {
      toggleSelected(itemEl.dataset.itemId);
    }
  });

  els.selectAll?.addEventListener('click', () => {
    setState({ selected: new Set(state.items.map(i => i.id)) });
  });

  // 5. Обновление состояния — через одну функцию
  function setState(patch) {
    state = { ...state, ...patch };
    render();
  }

  function toggleSelected(id) {
    const next = new Set(state.selected);
    next.has(id) ? next.delete(id) : next.add(id);
    setState({ selected: next });
  }

  // 6. Публичное API
  return {
    setItems:         (items) => setState({ items }),
    getSelectedIds:   () => [...state.selected],
    clearSelection:   () => setState({ selected: new Set() }),
  };
}

// Bootstrap
document.querySelectorAll('[data-js="wishlist"]').forEach(el => {
  const wishlist = createWishlist(el);
  el._wishlist = wishlist; // сохраняем instance если нужен снаружи
});
```

---

## 6. Универсальные правила чистого кода

### DRY — Don't Repeat Yourself

```js
// 🍝 Плохо: одна логика, три копии
document.querySelector('#save-btn').addEventListener('click', async () => {
  document.querySelector('#save-btn').disabled = true;
  document.querySelector('#save-btn').textContent = 'Saving...';
  await saveData();
  document.querySelector('#save-btn').disabled = false;
  document.querySelector('#save-btn').textContent = 'Save';
});

document.querySelector('#publish-btn').addEventListener('click', async () => {
  document.querySelector('#publish-btn').disabled = true;
  document.querySelector('#publish-btn').textContent = 'Publishing...';
  await publishData();
  document.querySelector('#publish-btn').disabled = false;
  document.querySelector('#publish-btn').textContent = 'Publish';
});

// ✅ Хорошо: общий паттерн — в функцию
async function withLoadingState(btnEl, loadingText, action) {
  const originalText = btnEl.textContent;
  btnEl.disabled = true;
  btnEl.textContent = loadingText;

  try {
    await action();
  } finally {
    btnEl.disabled = false;
    btnEl.textContent = originalText;
  }
}

saveBtn.addEventListener('click', () =>
  withLoadingState(saveBtn, 'Saving...', saveData)
);

publishBtn.addEventListener('click', () =>
  withLoadingState(publishBtn, 'Publishing...', publishData)
);
```

### YAGNI — You Aren't Gonna Need It

Не пиши код «на будущее». Пиши код для текущей задачи.

```js
// 🍝 Плохо: абстракция, которая никому не нужна
class UniversalDataFetcherWithRetryAndCachingAndTransformationPipeline {
  constructor(options = {}) { ... }
  setTransformer(fn) { ... }
  setCache(ttl) { ... }
  // 200 строк кода, используется в одном месте
}

// ✅ Хорошо: решаешь задачу, которая есть сейчас
async function fetchProducts() {
  const response = await fetch('/api/products');
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
// Усложнишь, когда появится реальная потребность
```

### KISS — Keep It Simple, Stupid

```js
// 🍝 Плохо: overengineered
const getDiscount = (price, userType, promoCode, isHoliday, memberYears) => {
  return (
    (promoCode ? PROMO_DISCOUNTS[promoCode] ?? 0 : 0) +
    (userType === 'premium' ? (memberYears > 2 ? 0.15 : 0.10) : 0) +
    (isHoliday ? 0.05 : 0)
  ) * price;
};

// ✅ Хорошо: явно, читаемо, отлаживаемо
function getDiscount(price, { userType, promoCode, isHoliday, memberYears }) {
  let discount = 0;

  if (promoCode && PROMO_DISCOUNTS[promoCode]) {
    discount += PROMO_DISCOUNTS[promoCode];
  }

  if (userType === 'premium') {
    discount += memberYears > 2 ? 0.15 : 0.10;
  }

  if (isHoliday) {
    discount += 0.05;
  }

  return price * discount;
}
```

### Комментарии — объясняй «почему», не «что»

```js
// 🍝 Плохо: комментарий дублирует код
// Увеличиваем счётчик на 1
counter++;

// Проверяем, равна ли цена нулю
if (price === 0) { ... }

// ✅ Хорошо: комментарий объясняет неочевидное решение
// Safari не поддерживает :focus-visible без полифила до версии 15.4.
// Добавляем класс вручную через JS для единообразия.
input.addEventListener('focus', () => input.classList.add('js-focus-visible'));

// Добавляем задержку 100ms: без неё popover закрывается раньше,
// чем успевает сработать click на trigger (порядок событий blur → click).
setTimeout(() => closePopover(), 100);
```

---

## 7. Red Flags — это надо рефакторить прямо сейчас

Ищи в коде эти паттерны с помощью grep или поиска в редакторе:

```bash
# Глобальные ID-запросы
grep -r "getElementById" src/

# Глобальные querySelector
grep -r "document\.querySelector" src/

# Прямая запись стилей
grep -r "\.style\." src/

# Инлайн-обработчики в HTML
grep -r "onclick=" templates/
grep -r "onchange=" templates/

# InnerHTML без escaping (XSS риск)
grep -r "innerHTML" src/

# console.log оставленные в продакшне
grep -r "console\.log" src/

# TODO и FIXME без задачи в трекере
grep -r "TODO\|FIXME\|HACK\|XXX" src/
```

| Что нашёл | Что делать |
|---|---|
| `document.getElementById` | Обернуть в `init(rootEl)`, заменить на `rootEl.querySelector('[data-js=...]')` |
| `element.style.display = 'none'` | Заменить на `element.hidden = true` или CSS-класс |
| `onclick="..."` в HTML | Убрать в JS, добавить `addEventListener` |
| `innerHTML = userInput` | Санитизировать через `escapeHtml()` или `textContent` |
| Функция > 50 строк | Разбить на меньшие функции |
| Переменная `data`, `item`, `obj`, `temp` | Переименовать в осмысленное имя |
| Три и более уровня вложенности `if` | Рефакторить на guard clauses |

---

## 8. Чеклист перед коммитом

### HTML
- [ ] Семантические теги использованы по назначению
- [ ] У каждого `<img>` есть `alt`
- [ ] У каждого `<button>` есть `type`
- [ ] У каждого `<input>` есть `label` (явный или `aria-label`)
- [ ] ID уникальны на странице
- [ ] CSS-классы и `data-js` атрибуты разделены
- [ ] Нет `onclick`, `onchange`, `onfocus` в HTML

### CSS
- [ ] Повторяющиеся значения вынесены в CSS-переменные
- [ ] Нет магических числа без переменной
- [ ] `!important` отсутствует (кроме utility-классов)
- [ ] Все состояния компонента описаны: hover, focus, active, disabled, error
- [ ] Специфичность максимум 1–2 уровня
- [ ] Используется `focus-visible` вместо `focus`

### JavaScript
- [ ] Нет `document.getElementById` / `document.querySelector` вне `init`-функций
- [ ] Все DOM-запросы сделаны один раз, в `els = {...}`
- [ ] Нет `element.style.X` — только переключение классов
- [ ] Нет читения состояния из DOM (`textContent`, атрибутов)
- [ ] Состояние хранится в JS-переменных
- [ ] `render()` — единственная функция, пишущая в DOM
- [ ] Листенеры вешаются через делегирование, не на каждый элемент
- [ ] У каждого `async`/`fetch` есть `try/catch`
- [ ] Нет магических строк и чисел — только именованные константы
- [ ] Функции <= 30–40 строк, делают одно дело
- [ ] Нет `console.log` в продакшн-коде

### Общее
- [ ] Код читается без комментариев (имена говорят сами)
- [ ] Комментарии объясняют «почему», а не «что»
- [ ] Нет закомментированного мёртвого кода
- [ ] Нет TODO без ссылки на задачу в трекере

---

*Чистый код — не про красоту. Про то, чтобы следующий человек (или ты сам) не провёл час, пытаясь понять, что тут вообще происходит.*
