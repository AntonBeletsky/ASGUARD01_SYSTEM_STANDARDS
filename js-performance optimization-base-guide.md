# 🚀 Полное руководство по написанию производительного JavaScript

> **Цель:** Писать JS-код, который не тормозит браузер, не жрёт память и не вызывает `[Violation]` в консоли.  
> **Уровень:** Middle → Senior  
> **Версия:** ES2024+

---

## Содержание

1. [Как браузер рендерит страницу](#1-как-браузер-рендерит-страницу)
2. [Layout Thrashing — враг №1](#2-layout-thrashing--враг-1)
3. [Оптимизация работы с DOM](#3-оптимизация-работы-с-dom)
4. [События: scroll, resize, mousemove](#4-события-scroll-resize-mousemove)
5. [Утечки памяти](#5-утечки-памяти)
6. [Тяжёлые вычисления и Web Workers](#6-тяжёлые-вычисления-и-web-workers)
7. [Таймеры и асинхронность](#7-таймеры-и-асинхронность)
8. [Анимации: правильно и неправильно](#8-анимации-правильно-и-неправильно)
9. [Работа с данными и структурами](#9-работа-с-данными-и-структурами)
10. [Загрузка скриптов и бандлы](#10-загрузка-скриптов-и-бандлы)
11. [Профилирование в Chrome DevTools](#11-профилирование-в-chrome-devtools)
12. [Виртуальный скролл и большие списки](#12-виртуальный-скролл-и-большие-списки)
13. [Closures, GC и управление памятью](#13-closures-gc-и-управление-памятью)
14. [Быстрые паттерны vs медленные антипаттерны](#14-быстрые-паттерны-vs-медленные-антипаттерны)
15. [Чеклист перед деплоем](#15-чеклист-перед-деплоем)

---

## 1. Как браузер рендерит страницу

Прежде чем фиксить баги — нужно понять, как браузер вообще работает. Это фундамент всего руководства.

### Пиксельный конвейер (Pixel Pipeline)

```
JavaScript → Style → Layout → Paint → Composite
```

| Этап | Что происходит |
|------|---------------|
| **JavaScript** | Выполняется твой код |
| **Style** | Браузер считает, какие CSS-правила применяются к элементам |
| **Layout** | Считается позиция и размер каждого элемента (reflow) |
| **Paint** | Заполнение пикселями — цвета, тени, тексты (repaint) |
| **Composite** | Слои накладываются друг на друга и выводятся на экран |

### Правило 16 мс

Браузер стремится к **60 FPS**. Это означает, что на каждый кадр есть **~16.6 мс** для ВСЕГО: JS, стили, layout, paint.

Если твой JS-код занимает 50 мс — ты пропустил **3 кадра**. Пользователь видит подёргивание.

### Что триггерит Layout (reflow)

Любое изменение, влияющее на геометрию страницы:

- Изменение `width`, `height`, `margin`, `padding`, `border`
- Добавление/удаление DOM-элементов
- Изменение текста или шрифта
- Изменение `display`, `position`
- Изменение `className`

### Что триггерит только Paint (repaint, дешевле)

- `color`, `background-color`
- `box-shadow`, `border-radius`
- `outline`, `visibility`

### Что работает только на Composite (самое дешёвое)

- `transform`
- `opacity`
- `filter`

> 💡 **Золотое правило анимаций:** Анимируй только `transform` и `opacity` — это не вызывает ни reflow, ни repaint.

---

## 2. Layout Thrashing — враг №1

**Layout Thrashing** (дерготня макета) — это когда JS поочерёдно пишет и читает геометрические свойства DOM, заставляя браузер делать полный пересчёт на каждой итерации.

### ❌ Плохо: чтение после записи в цикле

```javascript
const boxes = document.querySelectorAll('.box');

// ПЛОХО: каждая итерация — это forced reflow
for (let i = 0; i < boxes.length; i++) {
  boxes[i].style.width = '100px';         // ЗАПИСЬ → Layout invalidated
  const height = boxes[i].offsetHeight;   // ЧТЕНИЕ  → Forced reflow!
  boxes[i].style.height = height * 2 + 'px'; // ЗАПИСЬ
}
```

Браузер не может отложить пересчёт, потому что ты тут же требуешь актуальное значение.

### ✅ Хорошо: сначала читаем ВСЁ, потом пишем ВСЁ

```javascript
const boxes = document.querySelectorAll('.box');

// ШАГ 1: Читаем все нужные значения разом
const heights = Array.from(boxes).map(box => box.offsetHeight);

// ШАГ 2: Пишем все изменения разом
boxes.forEach((box, i) => {
  box.style.width = '100px';
  box.style.height = heights[i] * 2 + 'px';
});
```

Теперь браузер делает ровно один reflow — в конце.

### Свойства, вызывающие Forced Reflow при чтении

```javascript
// Все эти чтения форсируют reflow если DOM "грязный":
element.offsetTop / offsetLeft / offsetWidth / offsetHeight
element.scrollTop / scrollLeft / scrollWidth / scrollHeight
element.clientTop / clientLeft / clientWidth / clientHeight
element.getBoundingClientRect()
element.getClientRects()
window.getComputedStyle(element)
window.innerWidth / innerHeight
document.documentElement.scrollTop
```

### Инструмент для автоматического обнаружения: `FastDOM`

```javascript
import fastdom from 'fastdom';

// Все операции чтения группируются вместе
fastdom.measure(() => {
  const height = element.offsetHeight;
  
  // Все операции записи группируются вместе
  fastdom.mutate(() => {
    element.style.height = height * 2 + 'px';
  });
});
```

---

## 3. Оптимизация работы с DOM

DOM — это не JavaScript. Обращение к DOM похоже на пересечение границы с таможней. Каждый лишний переход — потеря времени.

### ❌ Плохо: вставка в цикле напрямую

```javascript
const list = document.getElementById('list');

// ПЛОХО: 1000 reflow и repaint
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Элемент ${i}`;
  list.appendChild(li); // Каждый append → reflow
}
```

### ✅ Хорошо: `DocumentFragment`

```javascript
const list = document.getElementById('list');
const fragment = document.createDocumentFragment();

// Строим дерево в памяти — никакого reflow
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Элемент ${i}`;
  fragment.appendChild(li);
}

// Один единственный reflow
list.appendChild(fragment);
```

### ✅ Ещё лучше: `innerHTML` одной строкой

```javascript
const items = Array.from({ length: 1000 }, (_, i) => `<li>Элемент ${i}</li>`);
list.innerHTML = items.join('');
// Один reflow, минимальный оверхед
```

### Кэшируй DOM-запросы

```javascript
// ❌ ПЛОХО: каждый раз обходит DOM
function update() {
  document.getElementById('counter').textContent = count; // поиск каждый раз!
}

// ✅ ХОРОШО: один раз нашли — сохранили
const counter = document.getElementById('counter');
function update() {
  counter.textContent = count;
}
```

### Минимизируй глубину DOM

Чем глубже дерево — тем дольше reflow. Избегай ненужных оберток:

```html
<!-- ❌ ПЛОХО: лишние div'ы -->
<div class="wrapper">
  <div class="inner">
    <div class="content">
      <span>Текст</span>
    </div>
  </div>
</div>

<!-- ✅ ХОРОШО -->
<p class="content">Текст</p>
```

### `classList` вместо прямого изменения стилей

```javascript
// ❌ ПЛОХО: 3 отдельных изменения стилей = потенциально 3 reflow
element.style.width = '100px';
element.style.height = '100px';
element.style.backgroundColor = 'red';

// ✅ ХОРОШО: 1 изменение className = 1 reflow
element.classList.add('active');
// В CSS: .active { width: 100px; height: 100px; background: red; }

// Или через cssText — тоже один reflow
element.style.cssText = 'width: 100px; height: 100px; background: red;';
```

---

## 4. События: scroll, resize, mousemove

Эти события могут стрелять **сотни раз в секунду**. Навесить на них тяжёлый обработчик — верный способ убить производительность.

### Throttle — ограничение частоты вызовов

Идеально для: `scroll`, `mousemove`, `touchmove`

```javascript
// Реализация throttle
function throttle(fn, limit) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      return fn.apply(this, args);
    }
  };
}

// Обработчик вызывается не чаще, чем раз в 16 мс (~60 FPS)
window.addEventListener('scroll', throttle(() => {
  updateScrollPosition();
}, 16));
```

### Debounce — выполнение после паузы

Идеально для: `resize`, `input`, `keyup`, поисковые запросы

```javascript
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Функция вызовется только через 300 мс ПОСЛЕ последнего resize
window.addEventListener('resize', debounce(() => {
  recalculateLayout();
}, 300));
```

### `passive: true` для событий скролла

Говоришь браузеру: «Я не буду вызывать `preventDefault()`, делай скролл сразу, не жди моего обработчика».

```javascript
// ❌ ПЛОХО: браузер ждёт завершения обработчика перед скроллом
window.addEventListener('scroll', handler);

// ✅ ХОРОШО: скролл не блокируется
window.addEventListener('scroll', handler, { passive: true });
window.addEventListener('touchstart', handler, { passive: true });
window.addEventListener('touchmove', handler, { passive: true });
```

### `IntersectionObserver` вместо scroll

Не нужно слушать `scroll` для определения видимости элементов:

```javascript
// ❌ ПЛОХО: в каждом кадре scroll считаем getBoundingClientRect()
window.addEventListener('scroll', () => {
  const rect = element.getBoundingClientRect();
  if (rect.top < window.innerHeight) {
    element.classList.add('visible');
  }
});

// ✅ ХОРОШО: браузер сам уведомит, когда элемент появится
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // Отписываемся после срабатывания
    }
  });
}, { threshold: 0.1 });

observer.observe(element);
```

### `ResizeObserver` вместо resize на window

```javascript
// ✅ Следим только за конкретным элементом, не за всем окном
const resizeObserver = new ResizeObserver(entries => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    adjustComponent(width, height);
  }
});

resizeObserver.observe(myElement);
// Не забудь отписаться когда элемент удаляется:
// resizeObserver.unobserve(myElement);
```

### Event Delegation — делегирование событий

```javascript
// ❌ ПЛОХО: 1000 слушателей для 1000 элементов
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ ХОРОШО: один слушатель на родителе
document.getElementById('list').addEventListener('click', (e) => {
  const item = e.target.closest('.item');
  if (item) handleClick(item);
});
```

---

## 5. Утечки памяти

Утечка памяти — это когда объект больше не нужен, но сборщик мусора не может его удалить, потому что на него где-то есть ссылка.

### Типичные причины

#### 1. Незачищенные таймеры

```javascript
// ❌ ПЛОХО: setInterval живёт вечно, держит ссылку на объект
class Component {
  constructor() {
    this.data = new Array(1000000).fill('данные');
    this.interval = setInterval(() => {
      console.log(this.data.length); // this захвачен в closure!
    }, 1000);
  }
}

const comp = new Component();
// comp = null; — но interval всё равно работает и держит comp в памяти!

// ✅ ХОРОШО: явная очистка
class Component {
  constructor() {
    this.data = new Array(1000000).fill('данные');
    this.interval = setInterval(() => {
      console.log(this.data.length);
    }, 1000);
  }
  
  destroy() {
    clearInterval(this.interval); // Обязательно!
    this.data = null;
  }
}
```

#### 2. Забытые слушатели событий

```javascript
// ❌ ПЛОХО
function init() {
  const heavyObject = { data: new Array(1000000) };
  
  window.addEventListener('resize', () => {
    console.log(heavyObject.data.length); // Closure держит heavyObject
  });
  // После init() heavyObject не освобождается!
}

// ✅ ХОРОШО: именованная функция, которую можно удалить
function init() {
  const heavyObject = { data: new Array(1000000) };
  
  function handleResize() {
    console.log(heavyObject.data.length);
  }
  
  window.addEventListener('resize', handleResize);
  
  // Возвращаем функцию очистки
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}

const cleanup = init();
// При уничтожении компонента:
cleanup();
```

#### 3. Отсоединённые DOM-узлы (Detached DOM)

```javascript
// ❌ ПЛОХО: элемент удалён из DOM, но JS держит ссылку
let detachedElement;

function createAndRemove() {
  const div = document.createElement('div');
  document.body.appendChild(div);
  detachedElement = div; // Глобальная ссылка!
  document.body.removeChild(div);
  // div удалён из DOM, но detachedElement всё ещё ссылается на него
}

// ✅ ХОРОШО
function createAndRemove() {
  const div = document.createElement('div');
  document.body.appendChild(div);
  document.body.removeChild(div);
  // div выходит из области видимости и будет собран GC
}
```

#### 4. `WeakMap` и `WeakRef` для слабых ссылок

Когда нужно хранить данные, связанные с объектами, но не мешать GC:

```javascript
// ❌ ПЛОХО: Map держит сильную ссылку на элементы
const cache = new Map();
cache.set(domElement, { someData: 'value' });
// Если domElement удалён — Map всё равно держит его!

// ✅ ХОРОШО: WeakMap не мешает сборке мусора
const cache = new WeakMap();
cache.set(domElement, { someData: 'value' });
// Когда domElement будет собран GC — запись в WeakMap исчезнет автоматически
```

#### 5. Случайные глобальные переменные

```javascript
// ❌ ПЛОХО: забыл var/let/const → переменная стала глобальной
function processData() {
  result = []; // Это window.result — утечка!
  for (let i = 0; i < 1000000; i++) {
    result.push(i);
  }
}

// ✅ ХОРОШО: всегда объявляй переменные явно
function processData() {
  const result = [];
  for (let i = 0; i < 1000000; i++) {
    result.push(i);
  }
  return result;
}
```

> 💡 Используй `'use strict'` или ES-модули — случайные глобальные переменные станут ошибкой.

---

## 6. Тяжёлые вычисления и Web Workers

Всё что занимает более **50 мс** в основном потоке — проблема. Кнопки не кликаются, анимации зависают.

### Что такое Web Worker

Web Worker — это отдельный поток выполнения. Он не имеет доступа к DOM, но может выполнять любые вычисления, не блокируя интерфейс.

```javascript
// worker.js — отдельный файл
self.addEventListener('message', (e) => {
  const { data } = e;
  
  // Тяжёлая работа в отдельном потоке
  const result = heavyComputation(data);
  
  self.postMessage(result);
});

function heavyComputation(data) {
  return data.reduce((acc, val) => acc + val * val, 0);
}
```

```javascript
// main.js — основной поток
const worker = new Worker('./worker.js');

worker.postMessage(hugeArray); // Отправляем данные

worker.addEventListener('message', (e) => {
  displayResult(e.data); // Получаем результат
});

worker.addEventListener('error', (e) => {
  console.error('Worker error:', e);
});

// Когда worker больше не нужен:
worker.terminate();
```

### Transferable Objects — передача без копирования

По умолчанию данные между потоками **копируются**. Для больших массивов используй `Transferable`:

```javascript
const buffer = new ArrayBuffer(1024 * 1024 * 100); // 100 МБ

// ❌ Копирует 100 МБ
worker.postMessage(buffer);

// ✅ Передаёт право владения — нулевое время копирования
worker.postMessage(buffer, [buffer]);
// После этого buffer в основном потоке недоступен
```

### SharedArrayBuffer — разделяемая память

```javascript
// Оба потока работают с одной и той же памятью
const sharedBuffer = new SharedArrayBuffer(1024);
const sharedArray = new Int32Array(sharedBuffer);

worker.postMessage({ sharedBuffer });

// В worker.js:
self.addEventListener('message', ({ data }) => {
  const sharedArray = new Int32Array(data.sharedBuffer);
  Atomics.add(sharedArray, 0, 1); // Атомарная операция — безопасно
});
```

### Разбивка на чанки с `scheduler.postTask` / `setTimeout`

Если не хочешь выносить в Worker, можно разбить работу на мелкие куски:

```javascript
// ❌ ПЛОХО: блокирует поток на секунды
function processMillionItems(items) {
  return items.map(item => heavyProcess(item));
}

// ✅ ХОРОШО: обрабатываем по 100 элементов за кадр
function processInChunks(items, chunkSize = 100) {
  return new Promise((resolve) => {
    const results = [];
    let index = 0;
    
    function processChunk() {
      const end = Math.min(index + chunkSize, items.length);
      
      while (index < end) {
        results.push(heavyProcess(items[index]));
        index++;
      }
      
      if (index < items.length) {
        // Отдаём управление браузеру между чанками
        setTimeout(processChunk, 0);
        // Или лучше: requestIdleCallback(processChunk);
      } else {
        resolve(results);
      }
    }
    
    processChunk();
  });
}
```

### `requestIdleCallback` — работа в паузах

```javascript
// Выполняется когда браузер не занят
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && tasksQueue.length > 0) {
    const task = tasksQueue.shift();
    task();
  }
  
  if (tasksQueue.length > 0) {
    // Если не успели — планируем следующий слот
    requestIdleCallback(processTasks);
  }
}, { timeout: 2000 }); // Максимум ждём 2 секунды
```

---

## 7. Таймеры и асинхронность

### `setTimeout(fn, 0)` — не равно «сразу»

```javascript
// setTimeout(fn, 0) гарантирует выполнение не раньше следующей итерации event loop
// Реальная задержка может быть 4+ мс из-за минимального порога браузера

// Для запуска в следующем микротаске используй Promise:
Promise.resolve().then(() => {
  // Выполнится быстрее, чем setTimeout(fn, 0)
});

// Или queueMicrotask:
queueMicrotask(() => {
  // Выполнится в конце текущего синхронного кода
});
```

### Накопление таймеров

```javascript
// ❌ ПЛОХО: каждый клик создаёт новый интервал
button.addEventListener('click', () => {
  setInterval(updateCounter, 1000); // Утечка!
});

// ✅ ХОРОШО: один интервал
let intervalId = null;

button.addEventListener('click', () => {
  if (intervalId) clearInterval(intervalId);
  intervalId = setInterval(updateCounter, 1000);
});
```

### `async/await` не делает код параллельным сам по себе

```javascript
// ❌ ПЛОХО: запросы выполняются последовательно (3 секунды)
async function loadData() {
  const users = await fetchUsers();     // 1 сек
  const posts = await fetchPosts();     // 1 сек
  const comments = await fetchComments(); // 1 сек
  return { users, posts, comments };
}

// ✅ ХОРОШО: все запросы параллельно (1 секунда)
async function loadData() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ]);
  return { users, posts, comments };
}
```

### Избегай блокирующего кода в `async`

```javascript
// ❌ ПЛОХО: async не помогает против синхронных вычислений
async function badExample() {
  await fetchData();
  
  // Этот цикл всё равно блокирует основной поток!
  for (let i = 0; i < 100_000_000; i++) {
    doSomething();
  }
}
```

---

## 8. Анимации: правильно и неправильно

### `requestAnimationFrame` — единственно верный способ

```javascript
// ❌ ПЛОХО: setTimeout с фиксированным интервалом
function animate() {
  updatePosition();
  setTimeout(animate, 16); // Не синхронизировано с частотой экрана!
}

// ✅ ХОРОШО: синхронизировано с рендером браузера
function animate(timestamp) {
  const deltaTime = timestamp - lastTimestamp;
  lastTimestamp = timestamp;
  
  updatePosition(deltaTime);
  
  requestAnimationFrame(animate);
}

let lastTimestamp = 0;
requestAnimationFrame(animate);

// Остановка анимации
const rafId = requestAnimationFrame(animate);
cancelAnimationFrame(rafId);
```

### CSS-анимации vs JS-анимации

Когда возможно — используй CSS. Браузер может перенести CSS-анимации на GPU:

```css
/* ✅ ХОРОШО: только transform и opacity — GPU композитинг */
.element {
  transition: transform 0.3s ease, opacity 0.3s ease;
  will-change: transform, opacity; /* Подсказка браузеру */
}

.element.active {
  transform: translateX(100px);
  opacity: 0.5;
}

/* ❌ ПЛОХО: вызывает reflow */
.element {
  transition: width 0.3s, left 0.3s, top 0.3s;
}
```

### `will-change` — используй осторожно

```css
/* ✅ Хорошо: только для элементов, которые реально анимируются */
.animated-element {
  will-change: transform;
}

/* ❌ Плохо: не вешай на всё подряд!
   Это создаёт новый слой композитора = жрёт видеопамять */
* {
  will-change: transform; /* Убьёт производительность! */
}
```

```javascript
// ✅ Лучше: добавляй/удаляй will-change динамически
element.style.willChange = 'transform'; // Перед анимацией
// ... анимация ...
element.style.willChange = 'auto'; // После анимации — освобождаем ресурсы
```

### Web Animations API

```javascript
// Современная JS-анимация без requestAnimationFrame
const animation = element.animate([
  { transform: 'translateX(0)', opacity: 1 },
  { transform: 'translateX(200px)', opacity: 0 }
], {
  duration: 500,
  easing: 'ease-out',
  fill: 'forwards'
});

animation.onfinish = () => {
  element.remove();
};

// Можно паузить, перематывать
animation.pause();
animation.play();
animation.cancel();
```

---

## 9. Работа с данными и структурами

### Выбор правильной структуры данных

```javascript
// ❌ ПЛОХО: поиск в массиве — O(n)
const users = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }];
function getUser(id) {
  return users.find(u => u.id === id); // Перебирает всех!
}

// ✅ ХОРОШО: поиск в Map — O(1)
const usersMap = new Map([
  [1, { id: 1, name: 'Alice' }],
  [2, { id: 2, name: 'Bob' }]
]);
function getUser(id) {
  return usersMap.get(id); // Мгновенно!
}
```

### Set для уникальных значений

```javascript
// ❌ ПЛОХО: indexOf — O(n)
const seen = [];
const unique = items.filter(item => {
  if (seen.indexOf(item) !== -1) return false;
  seen.push(item);
  return true;
});

// ✅ ХОРОШО: Set — O(1) для проверки наличия
const unique = [...new Set(items)];
```

### Избегай мутаций больших объектов в циклах

```javascript
// ❌ ПЛОХО: создаём новый объект через spread на каждой итерации
let state = {};
for (const item of hugeArray) {
  state = { ...state, [item.id]: item }; // Копирует ВСЕ ключи каждый раз!
}

// ✅ ХОРОШО: прямое присваивание
const state = {};
for (const item of hugeArray) {
  state[item.id] = item;
}
// Или через Object.fromEntries:
const state = Object.fromEntries(hugeArray.map(item => [item.id, item]));
```

### Парсинг больших JSON

```javascript
// ❌ ПЛОХО: парсинг 50 МБ блокирует поток
const data = JSON.parse(hugJsonString);

// ✅ ХОРОШО: стриминговый парсинг через Response
async function parseHugeJson(jsonString) {
  const response = new Response(jsonString);
  return response.json(); // Не блокирует главный поток
}

// ✅ Ещё лучше: для очень больших данных — Web Worker
// worker.js:
self.addEventListener('message', ({ data }) => {
  const parsed = JSON.parse(data);
  self.postMessage(parsed);
});
```

### Мемоизация тяжёлых вычислений

```javascript
// Простая мемоизация
function memoize(fn) {
  const cache = new Map();
  
  return function (...args) {
    const key = JSON.stringify(args);
    
    if (cache.has(key)) {
      return cache.get(key);
    }
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const expensiveCalc = memoize((n) => {
  // Тяжёлые вычисления
  return fibonacci(n);
});

expensiveCalc(40); // Считает
expensiveCalc(40); // Берёт из кэша мгновенно
```

---

## 10. Загрузка скриптов и бандлы

### Атрибуты `async` и `defer`

```html
<!-- ❌ ПЛОХО: блокирует парсинг HTML -->
<script src="app.js"></script>

<!-- ✅ async: загружается параллельно, выполняется сразу после загрузки -->
<!-- Порядок выполнения не гарантирован -->
<script src="analytics.js" async></script>

<!-- ✅ defer: загружается параллельно, выполняется после парсинга HTML -->
<!-- Порядок выполнения гарантирован, идеально для основного кода -->
<script src="app.js" defer></script>
```

### Code Splitting — загрузка по требованию

```javascript
// ❌ ПЛОХО: весь код загружается при старте
import { heavyFeature } from './heavyFeature.js';

// ✅ ХОРОШО: загружаем только когда нужно
async function loadFeature() {
  const { heavyFeature } = await import('./heavyFeature.js');
  heavyFeature();
}

button.addEventListener('click', loadFeature);
```

### Preload и Prefetch

```html
<!-- Preload: загружаем критичный ресурс как можно скорее -->
<link rel="preload" href="critical.js" as="script">

<!-- Prefetch: загружаем то, что понадобится на следующей странице -->
<link rel="prefetch" href="next-page.js" as="script">

<!-- Preconnect: устанавливаем соединение заранее -->
<link rel="preconnect" href="https://api.example.com">
```

### Tree Shaking — убираем мёртвый код

```javascript
// ❌ ПЛОХО: импортируем всю библиотеку (100+ КБ)
import _ from 'lodash';
const result = _.cloneDeep(obj);

// ✅ ХОРОШО: импортируем только нужное (несколько КБ)
import cloneDeep from 'lodash/cloneDeep';
const result = cloneDeep(obj);

// Или используй нативный аналог:
const result = structuredClone(obj); // ES2022, встроено в браузер
```

---

## 11. Профилирование в Chrome DevTools

### Performance Panel — поиск тормозов

1. `F12` → вкладка **Performance**
2. Нажми **Record** (⏺)
3. Воспроизведи проблемное действие
4. Стоп → анализируй

**Что искать:**
- Длинные **жёлтые блоки** = долгий JS
- Красные треугольники = dropped frames
- Фиолетовые блоки = Layout/Reflow
- Зелёные блоки = Paint

### Memory Panel — поиск утечек

```javascript
// Алгоритм поиска утечки:
// 1. Memory → Take Heap Snapshot (S1)
// 2. Выполни подозрительное действие N раз
// 3. Take Heap Snapshot (S2)
// 4. Comparison S2 vs S1 → ищи растущие объекты
```

### Performance.mark() — кастомные метрики

```javascript
// Разметка кода для измерения
performance.mark('dataProcessing:start');

processHugeArray(data);

performance.mark('dataProcessing:end');
performance.measure('dataProcessing', 'dataProcessing:start', 'dataProcessing:end');

// Получаем результат
const [measure] = performance.getEntriesByName('dataProcessing');
console.log(`Обработка заняла: ${measure.duration.toFixed(2)} мс`);
```

### Логирование медленных операций

```javascript
function measurePerformance(name, fn) {
  const start = performance.now();
  const result = fn();
  const end = performance.now();
  
  const duration = end - start;
  if (duration > 16) {
    console.warn(`⚠️ Slow operation "${name}": ${duration.toFixed(2)}ms`);
  }
  
  return result;
}

measurePerformance('renderList', () => renderItems(data));
```

---

## 12. Виртуальный скролл и большие списки

Рендер 10 000 DOM-элементов убьёт любой браузер. Решение — рендерить только видимые.

### Принцип виртуального скролла

```javascript
class VirtualScroll {
  constructor(container, items, itemHeight) {
    this.container = container;
    this.items = items;
    this.itemHeight = itemHeight;
    this.containerHeight = container.clientHeight;
    this.visibleCount = Math.ceil(this.containerHeight / itemHeight) + 2; // +2 буфер
    
    // Заглушка для правильной высоты скролла
    this.phantom = document.createElement('div');
    this.phantom.style.height = `${items.length * itemHeight}px`;
    container.appendChild(this.phantom);
    
    this.viewport = document.createElement('div');
    this.viewport.style.position = 'absolute';
    this.viewport.style.top = '0';
    this.viewport.style.width = '100%';
    container.appendChild(this.viewport);
    
    container.style.position = 'relative';
    container.style.overflow = 'auto';
    
    container.addEventListener('scroll', throttle(() => this.render(), 16), { passive: true });
    this.render();
  }
  
  render() {
    const scrollTop = this.container.scrollTop;
    const startIndex = Math.floor(scrollTop / this.itemHeight);
    const endIndex = Math.min(startIndex + this.visibleCount, this.items.length);
    
    this.viewport.style.transform = `translateY(${startIndex * this.itemHeight}px)`;
    this.viewport.innerHTML = this.items
      .slice(startIndex, endIndex)
      .map(item => `<div style="height:${this.itemHeight}px">${item.name}</div>`)
      .join('');
  }
}

// Использование: рендерим только ~20 элементов из 100 000
new VirtualScroll(
  document.getElementById('list'),
  generateItems(100_000),
  50 // высота элемента
);
```

---

## 13. Closures, GC и управление памятью

### Как работает Garbage Collector

GC собирает объекты, до которых нельзя «добраться» из корня (window, стек вызовов).

```javascript
// Этот объект будет собран GC
function createTemp() {
  const obj = { data: new Array(1000000) };
  return obj.data.length; // Возвращаем только число
  // obj больше недоступен → будет собран
}

// Этот НЕ будет собран (глобальная ссылка)
const global = { data: new Array(1000000) };
```

### Closure — мощь и ответственность

```javascript
// ❌ ПЛОХО: closure захватывает гигантский массив на всё время жизни функции
function createHandler(hugeData) {
  return function handleClick() {
    console.log(hugeData.length); // hugeData живёт пока живёт handleClick
  };
}

// ✅ ХОРОШО: захватываем только то, что нужно
function createHandler(hugeData) {
  const length = hugeData.length; // Копируем только нужное значение
  // hugeData теперь не захвачен!
  return function handleClick() {
    console.log(length);
  };
}
```

### Явное обнуление ссылок

```javascript
class DataProcessor {
  constructor() {
    this.cache = new Map();
    this.buffer = new ArrayBuffer(1024 * 1024 * 50); // 50 МБ
  }
  
  process(data) {
    // ... работа ...
  }
  
  dispose() {
    this.cache.clear();
    this.cache = null;
    this.buffer = null;
    // Теперь GC может освободить память
  }
}
```

---

## 14. Быстрые паттерны vs медленные антипаттерны

### Сводная таблица

| Ситуация | ❌ Медленно | ✅ Быстро |
|----------|-----------|---------|
| Уникальные значения | `arr.indexOf(x) !== -1` | `set.has(x)` |
| Поиск по ключу | `arr.find(i => i.id === x)` | `map.get(x)` |
| Клонирование объекта | Ручной перебор | `structuredClone(obj)` |
| Плоский массив из массивов | `[].concat(...arrays)` | `arrays.flat()` |
| Строки в цикле | `str += 'chunk'` | `chunks.push(); chunks.join('')` |
| Вставка множества элементов | `appendChild` в цикле | `DocumentFragment` |
| Анимация | `setInterval` | `requestAnimationFrame` |
| Видимость элемента | `scroll` + `getBoundingClientRect` | `IntersectionObserver` |
| Тяжёлые вычисления | Синхронно в потоке | `Web Worker` |
| Пустой `setTimeout` | `setTimeout(fn, 0)` | `queueMicrotask(fn)` |

### Строки: конкатенация vs join

```javascript
// ❌ ПЛОХО: создаёт новую строку на каждой итерации
let html = '';
for (const item of items) {
  html += `<li>${item.name}</li>`; // 10000 строк = 10000 аллокаций
}

// ✅ ХОРОШО
const html = items.map(item => `<li>${item.name}</li>`).join('');
// Или template literals с join
```

### Проверка существования ключа

```javascript
// ❌ Медленно
if (obj.hasOwnProperty('key')) { ... }

// ✅ Быстро (ES2022)
if (Object.hasOwn(obj, 'key')) { ... }

// ✅ Или просто (если нет прототипных ловушек)
if ('key' in obj) { ... }
```

---

## 15. Чеклист перед деплоем

### DOM и Layout

- [ ] Нет чтения после записи в циклах (Layout Thrashing)
- [ ] DOM-изменения батчятся через `DocumentFragment`
- [ ] DOM-элементы кэшируются в переменные
- [ ] Стили меняются через `classList`, не через `.style.*` по одному

### События

- [ ] `scroll`, `mousemove`, `resize` используют `throttle`/`debounce`
- [ ] События `scroll`/`touch` используют `{ passive: true }`
- [ ] Применяется делегирование событий где возможно
- [ ] Все слушатели удаляются при уничтожении компонента

### Память

- [ ] Все `setInterval`/`setTimeout` очищаются
- [ ] Нет случайных глобальных переменных
- [ ] Нет detached DOM-узлов с живыми JS-ссылками
- [ ] Используются `WeakMap`/`WeakRef` для кэшей, привязанных к объектам

### Производительность

- [ ] Тяжёлые вычисления (>50 мс) вынесены в Web Worker
- [ ] Анимации используют только `transform` и `opacity`
- [ ] Анимации управляются через `requestAnimationFrame`
- [ ] `will-change` используется точечно и временно
- [ ] Большие списки используют виртуальный скролл

### Загрузка

- [ ] Скрипты имеют атрибут `defer` или `async`
- [ ] Используется code splitting для больших модулей
- [ ] Нет импортов целых библиотек (используется tree shaking)

### Инструменты

- [ ] Проверен Performance в DevTools (нет длинных желтых блоков)
- [ ] Проверен Memory в DevTools (нет растущих утечек)
- [ ] Нет `[Violation]` в консоли
- [ ] Lighthouse Performance Score > 90

---

## Словарь терминов

| Термин | Значение |
|--------|----------|
| **Reflow** | Пересчёт геометрии страницы (дорого) |
| **Repaint** | Перерисовка пикселей без изменения геометрии (дешевле) |
| **Composite** | Склейка GPU-слоёв (очень дёшево) |
| **Layout Thrashing** | Чередование чтения/записи геометрии DOM в цикле |
| **Memory Leak** | Память выделена, но не освобождается |
| **Throttle** | Ограничение частоты вызовов функции |
| **Debounce** | Вызов функции только после окончания паузы |
| **Web Worker** | Фоновый поток для тяжёлых вычислений |
| **GC** | Garbage Collector — сборщик мусора |
| **RAF** | requestAnimationFrame — хук перед каждым кадром |
| **FPS** | Frames Per Second, цель — 60 |
| **Main Thread** | Основной поток браузера, где живёт JS и DOM |

---

*Последнее обновление: 2024. Стандарты: ES2024, Chrome 120+.*
