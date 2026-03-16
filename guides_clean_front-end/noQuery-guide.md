# noQuery Guide — DOM Selectors Without the Chaos
> Полный справочник по написанию селекторов в vanilla JS: от базовых правил до продвинутых паттернов. Дополняет clean-code-html-css-js.md, no-selector-spaghetti-in-js-guide.md и ai-despaghettization-refactoring-guide.md.

---

## Table of Contents

1. [Философия: почему важен способ выбора элементов](#1-философия-почему-важен-способ-выбора-элементов)
2. [Иерархия методов выборки — что и когда использовать](#2-иерархия-методов-выборки--что-и-когда-использовать)
3. [data-js атрибуты — полная спецификация](#3-data-js-атрибуты--полная-спецификация)
4. [Паттерн els-объекта — всё о сборке DOM-ссылок](#4-паттерн-els-объекта--всё-о-сборке-dom-ссылок)
5. [Скоупинг: rootEl и локальные запросы](#5-скоупинг-roоtel-и-локальные-запросы)
6. [Динамический DOM — селекторы для контента, которого ещё нет](#6-динамический-dom--селекторы-для-контента-которого-ещё-нет)
7. [querySelector vs getElementById vs getElementsBy* — полная таблица](#7-queryselector-vs-getelementbyid-vs-getelementsby--полная-таблица)
8. [Комплексные и составные селекторы](#8-комплексные-и-составные-селекторы)
9. [Атрибутные селекторы — расширенный справочник](#9-атрибутные-селекторы--расширенный-справочник)
10. [Делегирование событий — глубокий разбор](#10-делегирование-событий--глубокий-разбор)
11. [Типичные ошибки и как их избежать](#11-типичные-ошибки-и-как-их-избежать)
12. [Отладка селекторов](#12-отладка-селекторов)
13. [Справочник: быстрые паттерны](#13-справочник-быстрые-паттерны)

---

## 1. Философия: почему важен способ выбора элементов

DOM-запрос — это точка связи между JS и HTML. Каждый такой запрос создаёт зависимость: если HTML изменится, JS может сломаться. Задача этого гайда — сделать эти зависимости **явными, минимальными и безопасными**.

### Три вопроса перед любым DOM-запросом

```
1. Где этот запрос живёт?      → Должен быть в init, в блоке els = { ... }
2. Откуда он стартует?         → Из rootEl, не из document
3. По какому атрибуту?         → По data-js, не по классу и не по ID
```

Если ответ на любой из них неправильный — это и есть источник будущей боли.

### Стоимость глобального запроса

```js
// Эта строка ничего не стоит сейчас...
const btn = document.getElementById('submit-btn');

// ...но стоит дорого когда:
// - появится второй экземпляр виджета на странице
// - ID изменят при рефакторинге HTML
// - кто-то другой добавит элемент с таким же ID
// - нужно будет написать тест без реального браузера
```

---

## 2. Иерархия методов выборки — что и когда использовать

### Полная таблица решений

| Ситуация | Правильный метод | Запрещённый метод |
|---|---|---|
| Один элемент по JS-хуку | `rootEl.querySelector('[data-js="name"]')` | `document.getElementById('name')` |
| Несколько элементов по JS-хуку | `rootEl.querySelectorAll('[data-js="name"]')` | `document.getElementsByClassName('name')` |
| Ближайший предок при делегировании | `e.target.closest('[data-js="name"]')` | `e.target.parentNode.parentNode` |
| Все экземпляры виджета для bootstrap | `document.querySelectorAll('[data-js="widget"]')` | `document.getElementsByClassName('widget')` |
| Проверка наличия элемента | `rootEl.querySelector('[data-js="x"]') !== null` | `document.getElementById('x')` |
| ARIA-связь (labelledby, describedby) | `document.getElementById(id)` | — |
| Якорные ссылки (#anchor) | `document.getElementById(id)` | — |

> **Правило**: `document.getElementById` допустим только для ARIA-связей и якорей — там ID семантически необходим. Для всего остального — `data-js` через `rootEl`.

### Почему `querySelectorAll` лучше `getElementsByClassName`

```js
// getElementsByClassName возвращает HTMLCollection — живую коллекцию.
// Она меняется при изменении DOM, что вызывает неочевидные баги в циклах.
const items = document.getElementsByClassName('item');
items.length; // 3
// Где-то в коде один элемент удалён из DOM
items.length; // 2 — коллекция обновилась сама!

// querySelectorAll возвращает NodeList — статичный снимок на момент запроса.
const items = rootEl.querySelectorAll('[data-js="item"]');
items.length; // 3
// DOM изменился — items.length всё ещё 3. Предсказуемо.
```

---

## 3. data-js атрибуты — полная спецификация

### Синтаксис и соглашения об именовании

```html
<!-- Формат: data-js="[компонент]-[роль]" -->

<!-- ✅ Правильно: kebab-case, описывает роль элемента -->
<button data-js="submit-btn">Send</button>
<input  data-js="search-input">
<ul     data-js="items-list">
<span   data-js="counter-badge">0</span>
<div    data-js="error-msg" hidden></div>

<!-- ❌ Неправильно: camelCase, дублирует класс, слишком общее -->
<button data-js="submitBtn">Send</button>
<button data-js="btn-primary">Send</button>
<div    data-js="container">...</div>
```

### Корневой элемент виджета

```html
<!-- Корневой элемент получает имя виджета без суффикса -->
<section data-js="checkout">
  <input  data-js="email-input">
  <input  data-js="name-input">
  <button data-js="submit-btn">Checkout</button>
  <p      data-js="error-msg" hidden></p>
</section>

<!-- Для списков с динамическими элементами: контейнер + шаблон элемента -->
<ul data-js="cart-list">
  <li data-js="cart-item" data-item-id="42">
    <span data-js="item-name">Product</span>
    <button data-js="remove-btn">×</button>
  </li>
</ul>
```

### data-js vs data-* для данных

```html
<!-- data-js — ТОЛЬКО для JS-хуков (querySelector) -->
<li data-js="cart-item"
    data-item-id="42"
    data-price="1990"
    data-category="shoes">
  ...
</li>

<!-- JS читает данные через dataset, не через querySelector -->
```

```js
function handleRemove(itemEl) {
  const id       = itemEl.dataset.itemId;    // "42"
  const price    = Number(itemEl.dataset.price);   // 1990
  const category = itemEl.dataset.category;  // "shoes"
}
```

> **Правило**: `data-js` — адрес для querySelector. `data-*` (остальные) — хранилище данных для dataset. Не путать.

### Документирование data-js контрактов

Каждый `data-js` атрибут — это контракт между HTML и JS. Его нужно документировать.

```js
// wishlist.js

/**
 * Wishlist widget
 *
 * Required data-js attributes on rootEl:
 *   [data-js="wishlist-list"]       — контейнер для элементов списка
 *   [data-js="select-all-btn"]      — кнопка "выбрать все"
 *   [data-js="delete-selected-btn"] — кнопка "удалить выбранные"
 *   [data-js="selected-count"]      — счётчик выбранных
 *
 * data-* on list items (data-js="wishlist-item"):
 *   data-item-id  — уникальный ID товара
 */
function createWishlist(rootEl) { ... }
```

---

## 4. Паттерн els-объекта — всё о сборке DOM-ссылок

### Базовая структура

```js
function createCheckout(rootEl) {
  // Все DOM-запросы — один раз, в одном месте, в начале функции
  const els = {
    emailInput: rootEl.querySelector('[data-js="email-input"]'),
    nameInput:  rootEl.querySelector('[data-js="name-input"]'),
    submitBtn:  rootEl.querySelector('[data-js="submit-btn"]'),
    errorMsg:   rootEl.querySelector('[data-js="error-msg"]'),
    successMsg: rootEl.querySelector('[data-js="success-msg"]'),
  };

  // Дальше в коде — только els.emailInput, els.submitBtn, etc.
  // Никаких повторных querySelector внутри обработчиков
}
```

### Обязательная валидация els в разработке

Тихие `null` ломают код непредсказуемо. Лучше упасть громко сразу.

```js
function createCheckout(rootEl) {
  const els = {
    emailInput: rootEl.querySelector('[data-js="email-input"]'),
    submitBtn:  rootEl.querySelector('[data-js="submit-btn"]'),
    errorMsg:   rootEl.querySelector('[data-js="error-msg"]'),
  };

  // Валидация в dev-режиме
  if (process.env.NODE_ENV !== 'production') {
    Object.entries(els).forEach(([key, el]) => {
      if (!el) {
        console.error(
          `[createCheckout] Missing required element: els.${key}\n` +
          `Expected: rootEl.querySelector('[data-js="..."]')\n` +
          `RootEl:`, rootEl
        );
      }
    });
  }

  // ...
}
```

### Опциональные элементы

Не все элементы обязаны существовать — некоторые условны (показываются только в определённых состояниях).

```js
const els = {
  // Обязательные — виджет не работает без них
  list:      rootEl.querySelector('[data-js="items-list"]'),
  submitBtn: rootEl.querySelector('[data-js="submit-btn"]'),

  // Опциональные — могут отсутствовать в некоторых контекстах
  emptyMsg:    rootEl.querySelector('[data-js="empty-msg"]')    ?? null,
  loadingSpinner: rootEl.querySelector('[data-js="spinner"]')  ?? null,
  stickyHeader:   rootEl.querySelector('[data-js="sticky-h"]') ?? null,
};

// При использовании опциональных — всегда проверка
function render() {
  els.emptyMsg?.hidden = state.items.length > 0;
  els.loadingSpinner?.classList.toggle('is-visible', state.loading);
}
```

### els для коллекций (querySelectorAll)

```js
const els = {
  // Одиночные элементы
  form:       rootEl.querySelector('[data-js="filter-form"]'),
  clearBtn:   rootEl.querySelector('[data-js="clear-btn"]'),

  // Коллекции — именуются во множественном числе
  filterBtns: rootEl.querySelectorAll('[data-js="filter-btn"]'),
  checkboxes: rootEl.querySelectorAll('[data-js="option-checkbox"]'),
};

// Итерация
els.filterBtns.forEach(btn => {
  btn.setAttribute('aria-pressed', btn.dataset.category === state.category);
});
```

> **Важно**: `querySelectorAll` возвращает статичный NodeList. Если элементы добавляются динамически после инита — нельзя хранить коллекцию в `els`. Нужно делегирование (см. раздел 10).

---

## 5. Скоупинг: rootEl и локальные запросы

### Почему rootEl, а не document

```js
// ❌ Глобальный запрос — ломается при дублировании виджета
function initWishlist() {
  const list = document.querySelector('.wishlist-list');
  // Если на странице два списка желаний — оба запроса вернут первый
}

// ✅ Локальный запрос — работает для любого количества экземпляров
function createWishlist(rootEl) {
  const list = rootEl.querySelector('[data-js="wishlist-list"]');
  // Каждый экземпляр работает только со своим DOM
}

// Bootstrap: инициализация всех экземпляров
document.querySelectorAll('[data-js="wishlist"]').forEach(createWishlist);
```

### Передача rootEl явно vs через замыкание

```js
// Вариант 1: rootEl как параметр (предпочтительно для фабричных функций)
function createDropdown(rootEl) {
  const toggle = rootEl.querySelector('[data-js="toggle"]');
  const menu   = rootEl.querySelector('[data-js="menu"]');
  // rootEl доступен через параметр
}

// Вариант 2: rootEl через замыкание (для вложенных модулей)
function createForm(rootEl) {
  const els = { /* ... */ };

  // Вложенный модуль получает свой контейнер как rootEl
  const suggestionList = createSuggestionList(
    rootEl.querySelector('[data-js="suggestions"]')
  );
}
```

### Глубина вложенности запросов

```js
function createProductCard(rootEl) {
  const els = {
    // ✅ Запрос от rootEl — один уровень вложенности в querySelector
    title:     rootEl.querySelector('[data-js="product-title"]'),
    price:     rootEl.querySelector('[data-js="product-price"]'),
    addToCart: rootEl.querySelector('[data-js="add-to-cart-btn"]'),
  };

  // ✅ Допустимо: поиск внутри найденного контейнера
  const gallery = rootEl.querySelector('[data-js="product-gallery"]');
  const mainImg = gallery?.querySelector('[data-js="gallery-main-img"]');
  const thumbs  = gallery?.querySelectorAll('[data-js="gallery-thumb"]');
}
```

```js
// ❌ Плохо: цепочки из parentNode/children — хрупко, ломается при изменении HTML
const btn = e.target.parentNode.parentNode.children[2];

// ✅ Хорошо: closest() для подъёма, querySelector для спуска
const card = e.target.closest('[data-js="product-card"]');
const title = card.querySelector('[data-js="product-title"]');
```

---

## 6. Динамический DOM — селекторы для контента, которого ещё нет

### Проблема: статичный els не видит новые элементы

```js
function createList(rootEl) {
  // ❌ Этот NodeList заморожен на момент инита
  const items = rootEl.querySelectorAll('[data-js="list-item"]');

  // Добавим новый item в DOM...
  rootEl.insertAdjacentHTML('beforeend', '<li data-js="list-item">New</li>');

  // items всё ещё содержит только старые элементы
  items.length; // 3, а не 4
}
```

### Решение 1: Делегирование (предпочтительно)

```js
function createList(rootEl) {
  const els = {
    list: rootEl.querySelector('[data-js="items-list"]'),
  };

  // Слушаем стабильный контейнер, не сами items
  els.list.addEventListener('click', (e) => {
    const item = e.target.closest('[data-js="list-item"]');
    if (!item) return;
    handleItemClick(item);
  });
}
```

### Решение 2: Повторный запрос в render()

```js
function createList(rootEl) {
  const els = {
    list: rootEl.querySelector('[data-js="items-list"]'),
  };

  let state = { items: [] };

  function render() {
    // Рендерим HTML
    els.list.innerHTML = state.items.map(item => `
      <li data-js="list-item" data-item-id="${item.id}">
        <span data-js="item-name">${escapeHtml(item.name)}</span>
        <button data-js="remove-btn">×</button>
      </li>
    `).join('');

    // После рендера можно сделать querySelectorAll — это уже новые элементы
    // Но лучше делегирование, чем повторный запрос
  }
}
```

### Решение 3: MutationObserver для сторонних изменений DOM

Когда DOM меняет не твой код (сторонняя библиотека, legacy-скрипт):

```js
function createWidget(rootEl) {
  function initNewItem(itemEl) {
    // Настройка нового элемента
    itemEl.dataset.initialized = 'true';
  }

  // Инициализируем уже существующие
  rootEl.querySelectorAll('[data-js="item"]:not([data-initialized])').forEach(initNewItem);

  // Следим за появлением новых
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(({ addedNodes }) => {
      addedNodes.forEach(node => {
        if (node.nodeType !== Node.ELEMENT_NODE) return;

        // Проверяем сам добавленный элемент
        if (node.matches('[data-js="item"]:not([data-initialized])')) {
          initNewItem(node);
        }

        // И его потомков
        node.querySelectorAll('[data-js="item"]:not([data-initialized])')
            .forEach(initNewItem);
      });
    });
  });

  observer.observe(rootEl, { childList: true, subtree: true });

  return {
    destroy: () => observer.disconnect()
  };
}
```

---

## 7. querySelector vs getElementById vs getElementsBy* — полная таблица

| Метод | Возвращает | Живая? | Стартует от | Использовать? |
|---|---|---|---|---|
| `getElementById` | Element \| null | — | document только | Только для ARIA/якорей |
| `querySelector` | Element \| null | Нет | Любой элемент | ✅ Да |
| `querySelectorAll` | NodeList (static) | Нет | Любой элемент | ✅ Да |
| `getElementsByClassName` | HTMLCollection | ✅ Живая | document/Element | ❌ Нет |
| `getElementsByTagName` | HTMLCollection | ✅ Живая | document/Element | ❌ Нет |
| `getElementsByName` | NodeList (live) | ✅ Живая | document только | ❌ Нет |
| `closest` | Element \| null | — | Элемент (вверх) | ✅ Да |
| `matches` | boolean | — | Элемент | ✅ Да (в делегировании) |

### Живые коллекции — источник скрытых багов

```js
// ❌ Опасный паттерн с живой коллекцией
const items = document.getElementsByClassName('item'); // живая!

for (let i = 0; i < items.length; i++) {
  items[i].classList.remove('item'); // Удаляем класс...
  // ...и items[i] пропадает из коллекции! i растёт, length падает.
  // Каждый второй элемент пропускается. Классический баг.
}

// ✅ Безопасно с querySelectorAll
const items = rootEl.querySelectorAll('[data-js="item"]'); // статичный snapshot
items.forEach(item => item.classList.remove('item')); // все обработаны
```

---

## 8. Комплексные и составные селекторы

### Когда нужен составной селектор

```js
// Один data-js атрибут может появляться в разных состояниях
// — используй комбинацию с другими атрибутами

// Найти только активный таб
const activeTab = rootEl.querySelector('[data-js="tab"][aria-selected="true"]');

// Найти только незаблокированный input
const enabledInput = rootEl.querySelector('[data-js="quantity-input"]:not([disabled])');

// Найти первый видимый элемент
const firstVisible = rootEl.querySelector('[data-js="item"]:not([hidden])');
```

### Псевдоклассы в querySelector

```js
// :not() — исключить по атрибуту или классу
const uninitializedItems = rootEl.querySelectorAll('[data-js="item"]:not([data-ready])');

// :has() — выбрать контейнер, содержащий определённый потомок (современные браузеры)
const cardsWithBadge = rootEl.querySelectorAll('[data-js="card"]:has([data-js="badge"])');

// :nth-child() — для позиционных запросов (редко нужен в правильном коде)
const everyOtherRow = rootEl.querySelectorAll('[data-js="table-row"]:nth-child(even)');

// :is() — группировка селекторов
const anyInteractive = rootEl.querySelectorAll(':is([data-js="btn"], [data-js="link"])');
```

### Комбинаторы (потомок vs прямой ребёнок)

```js
// " " (пробел) — любой потомок
const allBtns = rootEl.querySelectorAll('[data-js="toolbar"] [data-js="btn"]');

// ">" — только прямые дети (осторожно: хрупко)
const directChildren = rootEl.querySelectorAll('[data-js="nav"] > [data-js="nav-item"]');

// "~" и "+" — siblings (очень редко нужны)
```

> **Правило**: Не злоупотребляй комбинаторами и псевдоклассами. Чем сложнее селектор, тем сложнее его поддерживать. Если нужен сложный селектор — возможно, стоит добавить ещё один `data-js` атрибут.

---

## 9. Атрибутные селекторы — расширенный справочник

### Синтаксис атрибутных селекторов

```js
// Точное совпадение (основной паттерн)
rootEl.querySelector('[data-js="submit-btn"]')

// Содержит слово (разделённое пробелами) — редко нужен
rootEl.querySelector('[class~="active"]')

// Начинается с (полезен для пространства имён)
rootEl.querySelectorAll('[data-js^="modal-"]')
// Найдёт: data-js="modal-overlay", data-js="modal-header", data-js="modal-close"

// Заканчивается на (полезен для группировки типов)
rootEl.querySelectorAll('[data-js$="-btn"]')
// Найдёт: data-js="submit-btn", data-js="cancel-btn", data-js="delete-btn"

// Содержит подстроку (широкий поиск)
rootEl.querySelectorAll('[data-js*="item"]')
// Найдёт: data-js="cart-item", data-js="wishlist-item", data-js="item-name"

// Атрибут существует (любое значение)
rootEl.querySelectorAll('[data-item-id]')
// Найдёт все элементы с атрибутом data-item-id независимо от значения

// Регистронезависимое сравнение (редко, но есть)
rootEl.querySelector('[data-status="active" i]')
// Найдёт: data-status="Active", data-status="ACTIVE", data-status="active"
```

### Практические паттерны

```js
// Найти все элементы модуля по namespace-префиксу
const allModalEls = rootEl.querySelectorAll('[data-js^="modal-"]');

// Найти все кнопки виджета
const allBtns = rootEl.querySelectorAll('[data-js$="-btn"]');

// Проверить, является ли элемент нашим JS-хуком
if (el.hasAttribute('data-js')) { ... }

// Прочитать значение data-js для логики (с осторожностью)
const role = el.getAttribute('data-js'); // "submit-btn"
```

---

## 10. Делегирование событий — глубокий разбор

### Как работает делегирование

Событие возникает на элементе и всплывает вверх по DOM. Слушатель на родителе перехватывает его, а `e.target` указывает на исходный элемент.

```
[document]
    └── [rootEl] ← слушатель здесь
            └── [list]
                    ├── [item] ← клик здесь
                    │       └── [icon] ← или здесь
                    └── [item]
```

### closest() — правильный способ обработки делегирования

```js
// ❌ Наивный подход — ломается при клике на дочерний элемент
els.list.addEventListener('click', (e) => {
  if (e.target.dataset.js === 'delete-btn') {
    // Если внутри кнопки есть <svg> или <span> — e.target будет ими, не кнопкой
    handleDelete(e.target);
  }
});

// ✅ Правильно — closest() поднимается вверх до нужного элемента
els.list.addEventListener('click', (e) => {
  const deleteBtn = e.target.closest('[data-js="delete-btn"]');
  if (deleteBtn) handleDelete(deleteBtn);
});
```

### Несколько действий в одном делегированном слушателе

```js
function createCart(rootEl) {
  const els = {
    list: rootEl.querySelector('[data-js="cart-list"]'),
  };

  els.list.addEventListener('click', (e) => {
    // Паттерн: каждое действие — отдельная переменная + ранний выход
    const removeBtn = e.target.closest('[data-js="remove-btn"]');
    if (removeBtn) {
      handleRemove(removeBtn.closest('[data-js="cart-item"]').dataset.itemId);
      return;
    }

    const increaseBtn = e.target.closest('[data-js="increase-qty"]');
    if (increaseBtn) {
      handleQuantityChange(
        increaseBtn.closest('[data-js="cart-item"]').dataset.itemId,
        +1
      );
      return;
    }

    const decreaseBtn = e.target.closest('[data-js="decrease-qty"]');
    if (decreaseBtn) {
      handleQuantityChange(
        decreaseBtn.closest('[data-js="cart-item"]').dataset.itemId,
        -1
      );
      return;
    }
  });
}
```

### Делегирование с data-action — альтернативный паттерн

```html
<!-- Вместо разных data-js для каждой кнопки — data-action -->
<li data-js="cart-item" data-item-id="42">
  <span data-js="item-name">Product</span>
  <button data-action="increase">+</button>
  <button data-action="decrease">−</button>
  <button data-action="remove">×</button>
</li>
```

```js
const ACTIONS = {
  increase: (item) => handleQuantityChange(item.dataset.itemId, +1),
  decrease: (item) => handleQuantityChange(item.dataset.itemId, -1),
  remove:   (item) => handleRemove(item.dataset.itemId),
};

els.list.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  const action = ACTIONS[btn.dataset.action];
  if (!action) return;

  const item = btn.closest('[data-js="cart-item"]');
  action(item);
});
```

> Этот паттерн удобен при большом количестве однотипных действий. `data-js` остаётся для querySelector в `els`, `data-action` — для диспетчеризации событий.

### События, которые не всплывают

Не все события можно делегировать через обычный слушатель:

| Событие | Всплывает? | Решение |
|---|---|---|
| `click` | ✅ Да | Делегировать напрямую |
| `input` | ✅ Да | Делегировать напрямую |
| `change` | ✅ Да | Делегировать напрямую |
| `submit` | ✅ Да | Делегировать напрямую |
| `keydown` / `keyup` | ✅ Да | Делегировать напрямую |
| `focus` | ❌ Нет | Использовать `focusin` или `{ capture: true }` |
| `blur` | ❌ Нет | Использовать `focusout` или `{ capture: true }` |
| `scroll` | ❌ Нет | Слушатель на конкретном элементе |
| `mouseenter` | ❌ Нет | Использовать `mouseover` + `closest()` |
| `mouseleave` | ❌ Нет | Использовать `mouseout` + `closest()` |

```js
// ✅ Делегирование focus/blur через focusin/focusout (всплывают)
rootEl.addEventListener('focusin', (e) => {
  const input = e.target.closest('[data-js="form-input"]');
  if (input) input.classList.add('is-focused');
});

rootEl.addEventListener('focusout', (e) => {
  const input = e.target.closest('[data-js="form-input"]');
  if (input) input.classList.remove('is-focused');
});
```

### Ограничение делегирования с closest()

`closest()` ищет вверх по DOM от `e.target` до корня документа. Чтобы ограничить поиск своим виджетом — проверяй, что найденный элемент находится внутри `rootEl`:

```js
els.list.addEventListener('click', (e) => {
  const item = e.target.closest('[data-js="list-item"]');

  // Без проверки: closest() может найти элемент за пределами rootEl
  if (item && rootEl.contains(item)) {
    handleItemClick(item);
  }
});
```

---

## 11. Типичные ошибки и как их избежать

### Ошибка 1: querySelector внутри обработчика события

```js
// ❌ DOM запрашивается при каждом клике
btn.addEventListener('click', () => {
  const menu = document.querySelector('[data-js="dropdown-menu"]');
  menu.classList.toggle('is-open');
});

// ✅ Запрос один раз в els
function createDropdown(rootEl) {
  const els = {
    btn:  rootEl.querySelector('[data-js="dropdown-btn"]'),
    menu: rootEl.querySelector('[data-js="dropdown-menu"]'),
  };

  els.btn.addEventListener('click', () => {
    els.menu.classList.toggle('is-open');
  });
}
```

### Ошибка 2: Слушатель на каждом элементе списка

```js
// ❌ При добавлении новых элементов — нет слушателя
rootEl.querySelectorAll('[data-js="item"]').forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ Один делегированный слушатель на контейнере
const list = rootEl.querySelector('[data-js="items-list"]');
list.addEventListener('click', (e) => {
  const item = e.target.closest('[data-js="item"]');
  if (item) handleClick(item);
});
```

### Ошибка 3: Чтение состояния из DOM

```js
// ❌ DOM используется как источник истины
function getTotal() {
  let total = 0;
  document.querySelectorAll('[data-js="item-price"]').forEach(el => {
    total += parseFloat(el.textContent);
  });
  return total;
}

// ✅ Состояние в JS, DOM только отображает его
let state = { items: [] };

function getTotal() {
  return state.items.reduce((sum, item) => sum + item.price, 0);
}

function render() {
  els.totalDisplay.textContent = getTotal().toFixed(2);
}
```

### Ошибка 4: Запрос до DOMContentLoaded

```js
// ❌ Скрипт выполняется до загрузки DOM
const btn = document.querySelector('[data-js="submit-btn"]'); // null!
btn.addEventListener('click', ...); // TypeError

// ✅ Запрос внутри функции, вызываемой после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-js="checkout"]').forEach(createCheckout);
});

// Или: скрипт с defer атрибутом
// <script src="app.js" defer></script>
// С defer не нужен DOMContentLoaded wrapper
```

### Ошибка 5: Утечка ссылок через хранение NodeList

```js
// ❌ Сохраняем NodeList — удалённые элементы всё ещё в памяти
const allItems = [];

function addItem(itemEl) {
  allItems.push(itemEl); // если элемент удалится из DOM — ссылка останется
}

// ✅ Храним данные, не DOM-ссылки
const itemIds = new Set();

function addItem(id) {
  itemIds.add(id);
}

// Нужен элемент? Находи его каждый раз через querySelector
function getItemEl(id) {
  return rootEl.querySelector(`[data-js="item"][data-item-id="${id}"]`);
}
```

---

## 12. Отладка селекторов

### Быстрая проверка селектора в консоли

```js
// Работает ли селектор?
document.querySelector('[data-js="submit-btn"]')
// → <button data-js="submit-btn">...</button> или null

// Сколько элементов найдёт?
document.querySelectorAll('[data-js="cart-item"]').length
// → 3

// Правильный ли rootEl?
document.querySelector('[data-js="checkout"]')
// → <section data-js="checkout">...</section>

// closest() от конкретного элемента (с помощью $0 — последнего выбранного в DevTools)
$0.closest('[data-js="cart-item"]')
```

### Отладка "null" в els

```js
function createWidget(rootEl) {
  const els = {
    btn: rootEl.querySelector('[data-js="action-btn"]'),
  };

  // Если els.btn === null:
  // 1. Проверь rootEl — он правильный?
  console.log('rootEl:', rootEl);
  console.log('rootEl innerHTML:', rootEl.innerHTML);

  // 2. Проверь наличие атрибута вручную
  console.log('found:', rootEl.querySelector('[data-js="action-btn"]'));

  // 3. Проверь опечатки в data-js
  // "action-btn" в JS vs "actionBtn" в HTML?
}
```

### grep-команды для поиска проблемных мест

```bash
# Все места с глобальными запросами (кандидаты на рефакторинг)
grep -rn "document\.getElementById\|document\.querySelector\|document\.querySelectorAll" src/

# Все data-js значения в HTML (для сверки с JS)
grep -roh 'data-js="[^"]*"' templates/ | sort | uniq

# Все data-js значения в JS (для сверки с HTML)
grep -roh 'data-js="[^"]*"' src/ | sort | uniq

# Разница между HTML и JS (что объявлено но не используется или наоборот)
# Запусти оба grep выше и сравни результаты
```

---

## 13. Справочник: быстрые паттерны

### Полный шаблон виджета

```js
/**
 * MyWidget — [описание виджета]
 *
 * Required data-js on rootEl:
 *   [data-js="my-widget"]        — корневой элемент
 *   [data-js="my-widget-list"]   — контейнер списка
 *   [data-js="my-widget-counter"] — счётчик
 *   [data-js="add-btn"]          — кнопка добавления
 *
 * Optional:
 *   [data-js="empty-msg"]        — сообщение при пустом списке
 *
 * Usage:
 *   document.querySelectorAll('[data-js="my-widget"]').forEach(createMyWidget);
 */
function createMyWidget(rootEl) {
  // 1. Все DOM-запросы — один раз, в els
  const els = {
    list:    rootEl.querySelector('[data-js="my-widget-list"]'),
    counter: rootEl.querySelector('[data-js="my-widget-counter"]'),
    addBtn:  rootEl.querySelector('[data-js="add-btn"]'),
    emptyMsg: rootEl.querySelector('[data-js="empty-msg"]') ?? null,
  };

  // 2. Состояние в JS
  let state = {
    items: [],
  };

  // 3. Единственная функция записи в DOM
  function render() {
    els.list.innerHTML = state.items.map(item => `
      <li data-js="my-widget-item" data-item-id="${item.id}">
        <span>${escapeHtml(item.name)}</span>
        <button data-action="remove">×</button>
      </li>
    `).join('');

    els.counter.textContent = state.items.length;
    if (els.emptyMsg) els.emptyMsg.hidden = state.items.length > 0;
  }

  // 4. Обновление состояния всегда через setState
  function setState(patch) {
    state = { ...state, ...patch };
    render();
  }

  // 5. Делегированные события на стабильном контейнере
  els.list.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    if (btn.dataset.action === 'remove') {
      const item = btn.closest('[data-js="my-widget-item"]');
      setState({ items: state.items.filter(i => i.id !== item.dataset.itemId) });
    }
  });

  els.addBtn.addEventListener('click', () => {
    const newItem = { id: crypto.randomUUID(), name: 'New item' };
    setState({ items: [...state.items, newItem] });
  });

  // 6. Инициализация
  render();

  // 7. Публичный API
  return {
    getItems: () => [...state.items],
    setItems: (items) => setState({ items }),
    destroy:  () => { /* AbortController.abort() если нужен */ },
  };
}

// Bootstrap
document.querySelectorAll('[data-js="my-widget"]').forEach(el => {
  el._myWidget = createMyWidget(el);
});
```

### Шпаргалка: что куда

```
ВЫБОРКА:
  Один элемент              → rootEl.querySelector('[data-js="name"]')
  Несколько элементов       → rootEl.querySelectorAll('[data-js="name"]')
  Предок при делегировании  → e.target.closest('[data-js="name"]')
  Bootstrap (все виджеты)   → document.querySelectorAll('[data-js="widget"]')
  ARIA/якорь                → document.getElementById('id') — единственный случай для getElementById

ИМЕНОВАНИЕ data-js:
  Корень виджета            → data-js="widget-name"
  Элемент внутри виджета    → data-js="role-type" (submit-btn, email-input, error-msg)
  Данные элемента           → data-item-id, data-price, data-category (не data-js!)
  Действие для диспетчера   → data-action="remove" (не data-js!)

ELS-ОБЪЕКТ:
  Обязательные              → прямое присваивание
  Опциональные              → с ?? null
  Динамические коллекции    → НЕ хранить в els, использовать делегирование

ДЕЛЕГИРОВАНИЕ:
  Обычные события           → addEventListener на стабильном контейнере
  focus/blur                → focusin/focusout (они всплывают)
  mouseenter/mouseleave     → mouseover/mouseout + closest()
  Несколько действий        → closest('[data-action]') + объект диспетчера
```

---

*Один rootEl. Один els. Один render. Делегирование вместо per-element слушателей. Данные в JS, DOM — только отображение.*
