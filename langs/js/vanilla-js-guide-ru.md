# Монументальное руководство по современному Vanilla JS для ИИ-агентов

> **Версия:** 2025 | **Охват:** ES2015 → ES2025 | **Среда:** Браузер, нет Node.js  
> **Назначение:** Полный, самодостаточный справочник по написанию правильного современного чистого JavaScript без фреймворков

---

## 📋 Содержание

1. [Философия современного JS](#1-философия-современного-js)
2. [Переменные и область видимости](#2-переменные-и-область-видимости)
3. [Типы данных и структуры](#3-типы-данных-и-структуры)
4. [Современный синтаксис ES6+](#4-современный-синтаксис-es6)
5. [Функции](#5-функции)
6. [Классы и прототипы](#6-классы-и-прототипы)
7. [Асинхронное программирование](#7-асинхронное-программирование)
8. [Модульная система ES Modules](#8-модульная-система-es-modules)
9. [DOM API — современный подход](#9-dom-api--современный-подход)
10. [События и делегирование](#10-события-и-делегирование)
11. [Fetch API и работа с сетью](#11-fetch-api-и-работа-с-сетью)
12. [Хранилища данных в браузере](#12-хранилища-данных-в-браузере)
13. [Управление состоянием](#13-управление-состоянием)
14. [Паттерны проектирования](#14-паттерны-проектирования)
15. [Современные Observer API](#15-современные-observer-api)
16. [Web Components](#16-web-components)
17. [Производительность](#17-производительность)
18. [Безопасность](#18-безопасность)
19. [Обработка ошибок](#19-обработка-ошибок)
20. [Современные Web API](#20-современные-web-api)
21. [Анимации и визуальные эффекты](#21-анимации-и-визуальные-эффекты)
22. [Тестирование ванильного JS](#22-тестирование-ванильного-js)
23. [Антипаттерны и ловушки](#23-антипаттерны-и-ловушки)
24. [Чеклист качества](#24-чеклист-качества)

---

## 1. Философия современного JS

### 1.1 Ключевые принципы

```
Принцип 1: Предпочитай декларативность императивности
Принцип 2: Иммутабельность по умолчанию, мутация — исключение
Принцип 3: Функции — чистые, предсказуемые, без побочных эффектов
Принцип 4: Явное лучше неявного (explicit over implicit)
Принцип 5: Обработка ошибок — не опционально, а обязательно
Принцип 6: Доступность (a11y) и производительность — с первого дня
Принцип 7: Используй платформу (Platform API), не сражайся с ней
```

### 1.2 Что считается «современным» JS в 2025

| Эра | Стандарт | Ключевые возможности |
|-----|----------|----------------------|
| Старый JS | ES5 (2009) | `var`, `prototype`, `arguments`, callbacks |
| Переходный | ES6/ES2015 | `let/const`, классы, стрелки, промисы |
| Зрелый | ES2017–2020 | `async/await`, `?.`, `??`, `globalThis` |
| Современный | ES2021–2025 | `at()`, `structuredClone`, `groupBy`, top-level await |

### 1.3 Правило совместимости

```js
// ❌ Плохо — полагаться на устаревшее
var x = 1;
document.all;
arguments.callee;

// ✅ Хорошо — проверять поддержку при необходимости
if ('IntersectionObserver' in window) {
  // современный путь
} else {
  // fallback
}
```

---

## 2. Переменные и область видимости

### 2.1 Правило: никогда `var`

```js
// ❌ ЗАПРЕЩЕНО — var поднимается (hoisting), нет блочной области
function bad() {
  if (true) {
    var x = 10; // видна во всей функции!
  }
  console.log(x); // 10 — неожиданно
}

// ✅ const по умолчанию
const PI = 3.14159;

// ✅ let только если значение переназначается
let count = 0;
count++;

// ❌ const не означает глубокую иммутабельность объектов!
const obj = { a: 1 };
obj.a = 2; // разрешено — модификация свойства
obj = {}; // SyntaxError — переназначение запрещено
```

### 2.2 Область видимости — правило наименьших привилегий

```js
// ❌ Плохо — переменная живёт дольше, чем нужна
let result;
if (condition) {
  result = computeHeavy();
}
doSomething(result);

// ✅ Хорошо — переменная в минимальной области
const result = condition ? computeHeavy() : null;
doSomething(result);
```

### 2.3 Временная мёртвая зона (TDZ)

```js
// let и const НЕ hoisting'ятся инициализацией
console.log(x); // ReferenceError: Cannot access 'x' before initialization
let x = 5;

// var — hoisting с инициализацией undefined
console.log(y); // undefined — тихая ошибка!
var y = 5;
```

### 2.4 Деструктуризация с дефолтными значениями

```js
// Массивы
const [first, second = 'default', , fourth] = [1, undefined, 3, 4];

// Объекты с переименованием и дефолтами
const { name: userName = 'Аноним', age = 0 } = user ?? {};

// Вложенная деструктуризация
const { address: { city, country = 'UA' } = {} } = person;

// В параметрах функции
function render({ title = '', className = '', children = [] } = {}) {
  // Всегда передавай {} как дефолтный параметр — иначе Error при вызове без аргументов
}
```

### 2.5 Замыкания (Closures) — правильное использование

```js
// ✅ Замыкание для инкапсуляции состояния
function createCounter(initial = 0) {
  let count = initial; // приватное состояние

  return {
    increment: () => ++count,
    decrement: () => --count,
    reset: () => { count = initial; },
    get value() { return count; },
  };
}

const counter = createCounter(10);
counter.increment(); // 11
counter.value;       // 11

// ✅ Замыкание для мемоизации
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
```

---

## 3. Типы данных и структуры

### 3.1 Примитивы и ссылочные типы

```js
// Примитивы (immutable, сравниваются по значению)
typeof 42          // 'number'
typeof 42n         // 'bigint'
typeof 'str'       // 'string'
typeof true        // 'boolean'
typeof undefined   // 'undefined'
typeof null        // 'object' ← историческая ошибка!
typeof Symbol()    // 'symbol'

// Надёжная проверка null
const isNull = (val) => val === null;

// Ссылочные типы (сравниваются по ссылке)
const a = { x: 1 };
const b = { x: 1 };
a === b; // false — разные ссылки!

// ✅ Глубокое сравнение — structuredClone + JSON (для простых случаев)
const deepEqual = (a, b) => JSON.stringify(a) === JSON.stringify(b);
// Важно: не работает с Date, Function, Map, Set, circular refs
```

### 3.2 Числа — ловушки

```js
// ❌ Опасные сравнения с float
0.1 + 0.2 === 0.3; // false!

// ✅ Используй Number.EPSILON
const almostEqual = (a, b) => Math.abs(a - b) < Number.EPSILON;

// Проверки числа
Number.isFinite(Infinity);   // false
Number.isFinite(42);         // true
Number.isNaN(NaN);           // true
Number.isNaN('NaN');         // false — в отличие от глобального isNaN()
Number.isInteger(4.0);       // true
Number.isSafeInteger(2**53); // false

// BigInt для больших целых
const big = 9007199254740991n + 1n; // точно
```

### 3.3 Строки — современные методы

```js
// Template literals
const html = `
  <div class="${className}">
    <h1>${title.trim()}</h1>
    ${items.map(item => `<li>${item}</li>`).join('')}
  </div>
`;

// Tagged templates
function safeHtml(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i - 1];
    const escaped = String(value ?? '').replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return result + escaped + str;
  });
}
const safe = safeHtml`<p>${userInput}</p>`; // XSS-защита

// Современные методы строк
'hello'.padStart(8, '0');          // '000hello'
'  trim me  '.trimStart();          // 'trim me  '
'abc'.repeat(3);                    // 'abcabcabc'
'ab cd'.replaceAll(' ', '_');       // 'ab_cd'
'hello world'.at(-1);              // 'd'
'hello'.includes('ell');           // true
'hello world'.startsWith('hello'); // true
```

### 3.4 Массивы — иммутабельные операции

```js
const arr = [1, 2, 3, 4, 5];

// ❌ Мутирующие методы (избегать когда нужна иммутабельность)
arr.push(6);     // мутация
arr.splice(1,1); // мутация
arr.sort();      // мутация на месте!

// ✅ Иммутабельные альтернативы
const withNew    = [...arr, 6];                  // append
const without2   = arr.filter((_, i) => i !== 1); // remove by index
const sorted     = [...arr].sort((a, b) => a - b); // sort copy

// ✅ Современные иммутабельные методы (ES2023)
arr.toSorted((a, b) => a - b);       // новый sorted массив
arr.toReversed();                     // новый reversed массив
arr.toSpliced(1, 1, 99);             // новый spliced массив
arr.with(2, 99);                      // новый с заменой элемента по индексу

// Полезные трансформации
const flat = [[1,2],[3,[4,5]]].flat(2);          // [1,2,3,4,5]
const flatMapped = [1,2,3].flatMap(x => [x, x*2]); // [1,2,2,4,3,6]

// Поиск
arr.find(x => x > 3);          // 4 — элемент
arr.findIndex(x => x > 3);     // 3 — индекс
arr.findLast(x => x < 4);      // 3 — с конца
arr.findLastIndex(x => x < 4); // 2

// Проверки
arr.every(x => x > 0);  // true
arr.some(x => x > 4);   // true
arr.includes(3);         // true
Array.isArray(arr);      // true

// Accumulate
arr.reduce((acc, val, idx, src) => acc + val, 0); // 15

// Индексирование с конца
arr.at(-1); // 5 — последний элемент
arr.at(-2); // 4 — предпоследний
```

### 3.5 Объекты — современные методы

```js
const obj = { a: 1, b: 2, c: 3 };

// Итерация
Object.keys(obj);         // ['a', 'b', 'c']
Object.values(obj);       // [1, 2, 3]
Object.entries(obj);      // [['a',1], ['b',2], ['c',3]]
Object.fromEntries([...]);// обратное преобразование

// Трансформация объекта через entries (мощный паттерн!)
const doubled = Object.fromEntries(
  Object.entries(obj).map(([key, value]) => [key, value * 2])
);
// { a: 2, b: 4, c: 6 }

// Merge (spread — поверхностное слияние)
const merged = { ...defaults, ...overrides };

// Object.assign — поверхностное слияние с мутацией target
const result = Object.assign({}, base, extra); // иммутабельно если target {}

// ✅ Глубокое клонирование (ES2022)
const deep = structuredClone(original);
// Поддерживает: Date, Map, Set, ArrayBuffer, RegExp, circular refs
// НЕ поддерживает: Function, Symbol, DOM nodes

// Проверка свойств
'a' in obj;                    // true — включая прототип!
Object.hasOwn(obj, 'a');       // true — только собственные (ES2022)
obj.hasOwnProperty('a');       // устаревший эквивалент

// Дескрипторы и заморозка
const frozen = Object.freeze({ x: 1, y: { z: 2 } });
frozen.x = 99; // тихий fail (TypeError в strict mode)
frozen.y.z = 99; // работает! заморозка поверхностная

// Глубокая заморозка
function deepFreeze(obj) {
  Object.freeze(obj);
  Object.values(obj)
    .filter(v => v && typeof v === 'object' && !Object.isFrozen(v))
    .forEach(deepFreeze);
  return obj;
}
```

### 3.6 Map и Set — когда использовать вместо Object/Array

```js
// Map vs Object
// ✅ Map: ключи любого типа, сохраняет порядок, iterable, нет prototype pollution
const map = new Map();
map.set('key', 'value');
map.set(42, 'number key');
map.set(objRef, 'object key'); // объект как ключ!
map.get('key');    // 'value'
map.has(42);       // true
map.size;          // 3
map.delete('key');
map.clear();

// Инициализация из массива пар
const fromArr = new Map([['a', 1], ['b', 2]]);

// Итерация
for (const [key, value] of map) { /*...*/ }
[...map.entries()]; // → массив пар
[...map.keys()];
[...map.values()];

// ✅ WeakMap — для приватных данных, не мешает GC
const _private = new WeakMap();
class Foo {
  constructor() {
    _private.set(this, { secret: 42 });
  }
  getSecret() { return _private.get(this).secret; }
}

// Set — уникальные значения
const set = new Set([1, 2, 3, 2, 1]); // Set {1, 2, 3}
set.add(4);
set.has(2);   // true
set.size;     // 4

// Уникализация массива
const unique = [...new Set(array)];

// Операции над множествами (ES2024)
const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);
a.union(b);        // {1,2,3,4,5,6}
a.intersection(b); // {3,4}
a.difference(b);   // {1,2}
a.isSubsetOf(b);   // false
```

### 3.7 Symbol

```js
// Symbol — уникальный примитив, часто для "приватных" ключей
const id = Symbol('id'); // описание только для дебага
const id2 = Symbol('id');
id === id2; // false — всегда уникальны

// Использование как скрытый ключ объекта
const _cache = Symbol('cache');
class Service {
  constructor() {
    this[_cache] = new Map(); // не видно в for...in, Object.keys()
  }
}

// Глобальный реестр символов
const globalId = Symbol.for('app.id'); // создать/получить по ключу
Symbol.keyFor(globalId); // 'app.id'

// Встроенные символы (well-known symbols)
class Range {
  constructor(start, end) { this.start = start; this.end = end; }
  
  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;
    return {
      next() {
        return current <= end
          ? { value: current++, done: false }
          : { done: true };
      }
    };
  }
}
[...new Range(1, 5)]; // [1, 2, 3, 4, 5]
```

---

## 4. Современный синтаксис ES6+

### 4.1 Optional Chaining `?.`

```js
// ❌ Старый защитный код
const city = user && user.address && user.address.city;

// ✅ Optional chaining
const city = user?.address?.city;

// Методы
const result = obj?.method?.();

// Массивы
const first = arr?.[0];

// Динамический ключ
const val = obj?.[dynamicKey];

// ⚠️ Не злоупотребляй — если null там ожидается, это баг
// Используй ?. только когда null/undefined — нормальное состояние
```

### 4.2 Nullish Coalescing `??`

```js
// ?? vs ||
// || — срабатывает на любое falsy: 0, '', false, null, undefined
// ?? — только на null/undefined

const count = response.count ?? 0;  // 0 из response — сохраняется
const count2 = response.count || 0; // 0 из response → заменится на 0 (без изменений, но семантически опасно)

// Практический пример
function init({ timeout = 5000, debug = false, title = '' } = {}) {}
// Если передать { timeout: 0 } — default destructuring сохранит 0 ✅
// Но если написать: const timeout = opts.timeout ?? 5000 — тоже правильно

// Логические операторы присваивания (ES2021)
a ??= 'default'; // a = a ?? 'default'  — только если a null/undefined
a ||= 'default'; // a = a || 'default'  — если a falsy
a &&= transform(a); // a = a && transform(a) — только если a truthy
```

### 4.3 Spread и Rest

```js
// REST — собирает оставшиеся аргументы/элементы
function sum(...numbers) {         // rest в параметрах
  return numbers.reduce((a, b) => a + b, 0);
}

const [head, ...tail] = [1, 2, 3, 4]; // rest в деструктуризации
const { a, ...rest } = { a: 1, b: 2, c: 3 }; // rest объекта

// SPREAD — разворачивает итерируемые
const combined = [...arr1, ...arr2];          // объединение массивов
const merged = { ...obj1, ...obj2 };          // слияние объектов
Math.max(...numbers);                          // передача как аргументы
const copy = [...original];                    // поверхностная копия массива
const objCopy = { ...original };              // поверхностная копия объекта

// ⚠️ Spread копирует только поверхностно!
const matrix = [[1,2],[3,4]];
const copy = [...matrix]; // копия массива, НО вложенные массивы — те же ссылки
```

### 4.4 Тернарный оператор — правила использования

```js
// ✅ Простые условия
const label = isActive ? 'Активен' : 'Неактивен';
const className = `btn ${isPrimary ? 'btn-primary' : 'btn-secondary'}`;

// ❌ Вложенные тернарные — читаемость хуже нуля
const result = a ? b ? 'x' : 'y' : c ? 'z' : 'w'; // никогда!

// ✅ Используй if/else или switch для сложной логики
function getStatus(code) {
  if (code === 200) return 'OK';
  if (code === 404) return 'Not Found';
  if (code === 500) return 'Server Error';
  return 'Unknown';
}
```

### 4.5 Short-circuit evaluation

```js
// && как guard (если левое falsy — не выполняем правое)
isLoggedIn && renderUserMenu();
user && user.name && showGreeting(user.name);

// || как дефолт
const name = inputName || 'Guest';

// В JSX-стиле шаблонах (условный рендеринг)
const html = `
  ${isLoading ? '<div class="spinner"></div>' : ''}
  ${items.length > 0 ? renderList(items) : '<p>Пусто</p>'}
`;
```

### 4.6 Destructuring — продвинутые паттерны

```js
// Swap переменных без temp
let a = 1, b = 2;
[a, b] = [b, a]; // a=2, b=1

// Деструктуризация результата функции
const { data, error, loading } = useQuery(query);
const [state, setState] = createState(initial);

// Итерация entries с деструктуризацией
for (const [index, value] of array.entries()) { /*...*/ }
for (const [key, value] of map) { /*...*/ }
for (const [key, value] of Object.entries(obj)) { /*...*/ }

// Вычисляемые ключи в деструктуризации
const key = 'name';
const { [key]: value } = obj; // извлекает obj.name в переменную value

// Переименование с дефолтом
const { 
  user_name: username = 'Anonymous',
  user_age: age = 0,
  settings: { theme = 'dark' } = {}
} = apiResponse;
```

---

## 5. Функции

### 5.1 Стрелочные vs обычные функции

```js
// Обычная функция: собственный this, arguments, может быть конструктором
function regular(x) {
  console.log(this);     // зависит от контекста вызова
  console.log(arguments); // доступен
  return x * 2;
}

// Стрелочная: this из замыкания, нет arguments, нельзя конструктор
const arrow = (x) => x * 2;

// ✅ Когда НУЖНА обычная функция:
// 1. Метод объекта, где нужен this
const obj = {
  value: 42,
  getValue() { return this.value; }, // ✅ обычная
  // getValue: () => this.value,     // ❌ this = window/undefined!
};

// 2. Конструктор (но лучше class)
// 3. Методы прототипа
// 4. Обработчики событий, где нужен this = element

// ✅ Когда ЛУЧШЕ стрелочная:
// 1. Колбэки в map/filter/reduce
[1,2,3].map(x => x * 2);

// 2. Промисы
fetch(url).then(res => res.json()).then(data => setData(data));

// 3. Когда нужно захватить внешний this
class Timer {
  start() {
    setInterval(() => {
      this.tick(); // this = Timer (стрелка захватывает из start)
    }, 1000);
  }
}
```

### 5.2 Параметры функций

```js
// Дефолтные параметры (вычисляются при каждом вызове!)
function createUser(name, role = 'user', date = new Date()) { }

// ❌ Мутабельные значения как дефолт — классическая ошибка
function addItem(list = []) { // Каждый вызов без аргумента — ОДИН и тот же []
  list.push('item');
  return list;
}
// В данном случае это безопасно потому что [] создаётся при каждом вызове!
// Это отличие JS от Python, где дефолт вычисляется один раз.

// Rest + обычные параметры
function log(level, ...messages) {
  console[level](...messages);
}

// Объект настроек — лучшая практика для >3 параметров
function initApp({ 
  container, 
  theme = 'light', 
  lang = 'ru',
  debug = false,
  onReady = null,
} = {}) {
  // Легко расширять без нарушения API
}
```

### 5.3 Чистые функции

```js
// ❌ Нечистая функция — зависит от внешнего состояния и изменяет его
let total = 0;
function addToTotal(value) {
  total += value; // побочный эффект!
  return total;   // результат зависит от внешнего состояния
}

// ✅ Чистая функция — только аргументы → результат
function add(a, b) { return a + b; }
function formatUser(user) { return { ...user, fullName: `${user.first} ${user.last}` }; }

// Правило: если функция делает DOM-операцию, запрос, запись в storage,
// логирование — она нечистая. Это нормально. Изолируй нечистое на краях.
```

### 5.4 Функции высшего порядка

```js
// Compose — правая к левой
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

// Pipe — левая к правой (читаемее)
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

const process = pipe(
  trim,
  toLowerCase,
  removeSpecialChars,
  truncate(100),
);
process(userInput);

// Partial application
const partial = (fn, ...preArgs) => (...laterArgs) => fn(...preArgs, ...laterArgs);
const add10 = partial(add, 10);
add10(5); // 15

// Curry
const curry = fn => {
  const arity = fn.length;
  return function curried(...args) {
    return args.length >= arity
      ? fn(...args)
      : (...more) => curried(...args, ...more);
  };
};

const curriedAdd = curry((a, b, c) => a + b + c);
curriedAdd(1)(2)(3); // 6
curriedAdd(1, 2)(3); // 6
```

### 5.5 Генераторы

```js
// Generator function — функция, которую можно ставить на паузу
function* range(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}

[...range(0, 10, 2)]; // [0, 2, 4, 6, 8]
for (const n of range(1, 5)) { console.log(n); }

// Бесконечный генератор
function* infinite(start = 0) {
  let i = start;
  while (true) yield i++;
}

const gen = infinite();
gen.next().value; // 0
gen.next().value; // 1

// Async генератор — для потоков данных
async function* paginate(fetchPage) {
  let page = 1;
  while (true) {
    const data = await fetchPage(page);
    if (!data.length) return;
    yield data;
    page++;
  }
}

for await (const items of paginate(fetchItems)) {
  renderItems(items);
}
```

---

## 6. Классы и прототипы

### 6.1 Современный синтаксис классов

```js
class EventEmitter {
  // Приватные поля (ES2022) — настоящая приватность!
  #listeners = new Map();
  #maxListeners = 10;
  
  // Статическое приватное поле
  static #instances = 0;
  
  // Статическое публичное поле
  static version = '1.0.0';

  constructor() {
    EventEmitter.#instances++;
  }

  // Статический метод
  static getInstanceCount() {
    return EventEmitter.#instances;
  }

  // Геттер
  get listenerCount() {
    return [...this.#listeners.values()]
      .reduce((sum, arr) => sum + arr.length, 0);
  }
  
  // Сеттер с валидацией
  set maxListeners(n) {
    if (typeof n !== 'number' || n < 0) throw new TypeError('Expected non-negative number');
    this.#maxListeners = n;
  }

  on(event, listener) {
    if (!this.#listeners.has(event)) {
      this.#listeners.set(event, []);
    }
    this.#listeners.get(event).push(listener);
    return this; // для chaining
  }

  off(event, listener) {
    if (!this.#listeners.has(event)) return this;
    const listeners = this.#listeners.get(event).filter(l => l !== listener);
    this.#listeners.set(event, listeners);
    return this;
  }

  emit(event, ...args) {
    this.#listeners.get(event)?.forEach(fn => fn(...args));
    return this;
  }
  
  once(event, listener) {
    const wrapper = (...args) => {
      listener(...args);
      this.off(event, wrapper);
    };
    return this.on(event, wrapper);
  }
}
```

### 6.2 Наследование

```js
class Component extends EventEmitter {
  #root;
  
  constructor(selector) {
    super(); // обязательно до обращения к this!
    this.#root = document.querySelector(selector);
    if (!this.#root) throw new Error(`Element not found: ${selector}`);
  }

  // Переопределение родительского метода
  on(event, listener) {
    // Добавляем логику до/после
    console.log(`Listening to: ${event}`);
    return super.on(event, listener);
  }

  render() {
    throw new Error('Subclasses must implement render()'); // abstract-like
  }

  mount() {
    this.#root.innerHTML = this.render();
    this.bindEvents();
    this.emit('mounted');
    return this;
  }
  
  bindEvents() {} // Можно переопределить
  
  destroy() {
    this.#root.innerHTML = '';
    this.emit('destroyed');
  }
}

class Button extends Component {
  #label;
  #onClick;

  constructor(selector, { label, onClick }) {
    super(selector);
    this.#label = label;
    this.#onClick = onClick;
  }

  render() {
    return `<button class="btn">${this.#label}</button>`;
  }

  bindEvents() {
    this.#root.querySelector('.btn')
      .addEventListener('click', this.#onClick);
  }
}
```

### 6.3 Mixins паттерн

```js
// Миксины для множественного «наследования» поведения
const Serializable = (Base) => class extends Base {
  toJSON() {
    return JSON.stringify(Object.fromEntries(
      Object.entries(this).filter(([, v]) => typeof v !== 'function')
    ));
  }
  
  static fromJSON(json) {
    return Object.assign(new this(), JSON.parse(json));
  }
};

const Validatable = (Base) => class extends Base {
  validate() {
    return Object.entries(this.constructor.schema ?? {}).every(
      ([field, rule]) => rule(this[field])
    );
  }
};

class Model {}
class User extends Serializable(Validatable(Model)) {
  static schema = {
    name: v => typeof v === 'string' && v.length > 0,
    age: v => Number.isInteger(v) && v >= 0,
  };
}
```

---

## 7. Асинхронное программирование

### 7.1 Промисы — глубокое понимание

```js
// Создание промиса
const promise = new Promise((resolve, reject) => {
  // Асинхронная работа
  setTimeout(() => {
    const success = Math.random() > 0.5;
    success ? resolve('data') : reject(new Error('Failed'));
  }, 1000);
});

// Состояния промиса: pending → fulfilled | rejected
// Промис нельзя отменить! (для отмены — AbortController или библиотека)

// Цепочка промисов
fetch('/api/user')
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json(); // возвращаем новый промис
  })
  .then(user => fetchUserPosts(user.id)) // можно возвращать промис
  .then(posts => renderPosts(posts))
  .catch(error => handleError(error))  // перехватывает все ошибки выше
  .finally(() => hideLoader());         // всегда выполняется
```

### 7.2 async/await — правильный стиль

```js
// ✅ Базовый паттерн
async function loadUser(id) {
  const response = await fetch(`/api/users/${id}`);
  
  if (!response.ok) {
    throw new Error(`Failed to load user: ${response.status}`);
  }
  
  return response.json();
}

// ✅ Обработка ошибок с try/catch
async function initDashboard(userId) {
  try {
    const [user, posts, settings] = await Promise.all([
      loadUser(userId),
      loadUserPosts(userId),
      loadSettings(),
    ]);
    renderDashboard({ user, posts, settings });
  } catch (error) {
    if (error.name === 'AbortError') return; // отмена — не ошибка
    console.error('Dashboard init failed:', error);
    showErrorMessage('Не удалось загрузить данные. Попробуйте позже.');
  } finally {
    hideLoader();
  }
}

// ✅ Параллельные запросы — Promise.all
// Запускает все одновременно, ждёт всех, падает при первой ошибке
const [users, products] = await Promise.all([
  fetchUsers(),
  fetchProducts(),
]);

// ✅ Promise.allSettled — ждёт всех, не падает на ошибке
const results = await Promise.allSettled([fetch('/api/1'), fetch('/api/2')]);
results.forEach(result => {
  if (result.status === 'fulfilled') process(result.value);
  else console.warn('Failed:', result.reason);
});

// ✅ Promise.race — берёт первый завершившийся
const timeout = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Timeout')), 5000)
);
const data = await Promise.race([fetchData(), timeout]);

// ✅ Promise.any — первый успешный (ES2021)
const fastest = await Promise.any([
  fetchFromServer1(),
  fetchFromServer2(),
  fetchFromServer3(),
]); // только если ВСЕ упали → AggregateError

// ❌ Типичная ошибка — последовательные await вместо параллельных
// МЕДЛЕННО — выполняются по очереди:
const user = await fetchUser(id);    // 200ms
const posts = await fetchPosts(id);  // 200ms → итого 400ms
// БЫСТРО — параллельно:
const [user, posts] = await Promise.all([fetchUser(id), fetchPosts(id)]); // 200ms
```

### 7.3 Отмена запросов — AbortController

```js
// ✅ Отмена fetch-запроса
class DataService {
  #controllers = new Map();

  async fetch(key, url, options = {}) {
    // Отменяем предыдущий запрос с тем же ключом
    this.abort(key);
    
    const controller = new AbortController();
    this.#controllers.set(key, controller);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') return null; // отменили — не ошибка
      throw error;
    } finally {
      this.#controllers.delete(key);
    }
  }

  abort(key) {
    this.#controllers.get(key)?.abort();
  }

  abortAll() {
    this.#controllers.forEach(c => c.abort());
    this.#controllers.clear();
  }
}

// Использование с поиском (debounce + отмена)
const service = new DataService();
let searchTimeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(async () => {
    const results = await service.fetch('search', `/api/search?q=${e.target.value}`);
    if (results) renderResults(results);
  }, 300);
});
```

### 7.4 Async итераторы и потоки

```js
// Чтение потока данных
async function readStream(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let result = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      result += decoder.decode(value, { stream: true });
      // Можно обновлять UI по мере получения данных
      updateProgress(result);
    }
  } finally {
    reader.releaseLock();
  }
  return result;
}

// Streaming LLM-ответ
async function streamText(prompt, onChunk) {
  const response = await fetch('/api/generate', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
    headers: { 'Content-Type': 'application/json' },
  });

  for await (const chunk of response.body) {
    const text = new TextDecoder().decode(chunk);
    onChunk(text);
  }
}
```

---

## 8. Модульная система ES Modules

### 8.1 Экспорт и импорт

```js
// ===== math.js =====
// Именованный экспорт
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export class Vector { /*...*/ }

// Дефолтный экспорт — один на модуль
export default class Calculator { /*...*/ }

// Реэкспорт
export { PI as MathPI } from './constants.js';
export * from './utils.js';
export * as utils from './utils.js'; // namespace re-export

// ===== main.js =====
// Именованные импорты
import { PI, add } from './math.js';

// Дефолтный + именованные
import Calculator, { PI, add } from './math.js';

// Namespace import
import * as Math from './math.js';
Math.PI; Math.add(1, 2);

// Переименование
import { add as sum } from './math.js';

// Только побочные эффекты
import './polyfills.js';
```

### 8.2 Динамические импорты

```js
// Загрузка модуля по требованию (code splitting)
async function loadChart() {
  const { default: Chart } = await import('./chart.js');
  return new Chart();
}

// Условная загрузка
const module = await import(
  isDev ? './logger-dev.js' : './logger-prod.js'
);

// Ленивая загрузка большого модуля
button.addEventListener('click', async () => {
  const { openEditor } = await import('./editor.js');
  openEditor(content);
});

// Параллельная загрузка нескольких модулей
const [{ default: Chart }, { default: Table }] = await Promise.all([
  import('./chart.js'),
  import('./table.js'),
]);
```

### 8.3 Паттерны организации модулей

```js
// ===== index.js (barrel file) =====
// Экспортируй публичный API, скрывай внутренние детали
export { UserService } from './UserService.js';
export { PostService } from './PostService.js';
export type { User, Post } from './types.js';

// ===== Структура проекта =====
// src/
//   components/     — UI компоненты
//     Button/
//       Button.js
//       Button.css
//       index.js    — реэкспорт
//   services/       — бизнес-логика, API
//   utils/          — утилиты без состояния
//   store/          — состояние приложения
//   main.js         — точка входа

// В HTML для ES modules
// <script type="module" src="./main.js"></script>
// type="module" автоматически: defer, strict mode, свой scope
```

### 8.4 Import Maps (нет npm без сборщика)

```html
<!-- В HTML — маппинг имён на URL -->
<script type="importmap">
{
  "imports": {
    "lodash": "https://cdn.jsdelivr.net/npm/lodash-es@4.17.21/lodash.js",
    "lodash/": "https://cdn.jsdelivr.net/npm/lodash-es@4.17.21/",
    "utils": "./src/utils/index.js"
  }
}
</script>

<script type="module">
  import debounce from 'lodash/debounce.js'; // работает!
  import { formatDate } from 'utils';
</script>
```

---

## 9. DOM API — современный подход

### 9.1 Выборка элементов

```js
// ✅ Современные селекторы
const el       = document.querySelector('.card');        // первый
const all      = document.querySelectorAll('.item');     // NodeList
const byId     = document.getElementById('app');        // быстрее
const byClass  = document.getElementsByClassName('btn'); // HTMLCollection (живая!)
const byTag    = document.getElementsByTagName('div');   // HTMLCollection (живая!)

// NodeList vs HTMLCollection
// NodeList: статический (querySelectorAll), итерируется for...of, forEach
// HTMLCollection: живой (меняется при изменении DOM), только for...of

// Конвертация в массив для array-методов
const items = Array.from(document.querySelectorAll('.item'));
// или
const items2 = [...document.querySelectorAll('.item')];

// Поиск внутри элемента (область поиска)
const form = document.querySelector('form');
const inputs = form.querySelectorAll('input'); // только внутри формы

// Closest — поиск вверх по DOM
const listItem = button.closest('li'); // ближайший предок <li>
const modal = btn.closest('[role="dialog"]');

// Matches — проверка соответствия селектору
element.matches('.active');      // boolean
element.matches(':hover');       // true если курсор над элементом
```

### 9.2 Создание и вставка элементов

```js
// ✅ Создание элементов
const card = document.createElement('div');
card.className = 'card';
card.id = 'card-1';
card.dataset.id = '42';         // data-атрибут
card.textContent = 'Safe text'; // безопасно, без XSS

// Атрибуты
card.setAttribute('aria-label', 'Card');
card.getAttribute('aria-label'); // 'Card'
card.removeAttribute('aria-label');
card.hasAttribute('hidden'); // boolean

// ✅ Безопасная HTML-вставка
function createElement(tag, { className, text, html, attrs = {}, children = [] } = {}) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text) el.textContent = text;      // безопасно!
  if (html) el.innerHTML = html;        // ⚠️ только доверенный HTML!
  Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
  children.forEach(child => el.append(child));
  return el;
}

// ✅ Вставка — современные методы
parent.append(child);              // в конец (принимает Node и строку)
parent.prepend(child);             // в начало
sibling.before(newEl);             // перед
sibling.after(newEl);              // после
target.replaceWith(newEl);         // замена

// insertAdjacentHTML — самый производительный для HTML-строк
element.insertAdjacentHTML('beforebegin', html); // перед элементом
element.insertAdjacentHTML('afterbegin', html);  // начало содержимого
element.insertAdjacentHTML('beforeend', html);   // конец содержимого
element.insertAdjacentHTML('afterend', html);    // после элемента

// ✅ Батчинг для производительности
const fragment = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  fragment.append(li);
});
list.append(fragment); // одна операция DOM вместо N
```

### 9.3 Классы и стили

```js
// classList API — предпочтительный метод
el.classList.add('active', 'visible');    // добавить
el.classList.remove('hidden', 'loading'); // удалить
el.classList.toggle('open');              // переключить
el.classList.toggle('active', condition); // по условию
el.classList.replace('old', 'new');       // заменить
el.classList.contains('active');          // проверить
[...el.classList];                        // в массив

// CSS Custom Properties (переменные) из JS
el.style.setProperty('--color', '#ff0000');
getComputedStyle(el).getPropertyValue('--color');

// ✅ Предпочитай классы прямым стилям
// ❌ el.style.display = 'flex'; el.style.color = 'red';
// ✅ el.classList.add('visible');

// Когда нужны прямые стили — динамические значения
el.style.transform = `translateX(${offsetX}px)`;
el.style.setProperty('--progress', `${percent}%`);

// Получение computed styles
const styles = getComputedStyle(el);
styles.getPropertyValue('font-size'); // '16px'
styles.color; // 'rgb(0, 0, 0)'
```

### 9.4 Размеры и позиции

```js
// getBoundingClientRect — позиция относительно viewport
const rect = el.getBoundingClientRect();
rect.top;    // от верха viewport
rect.left;   // от левого края viewport
rect.width;  // ширина
rect.height; // высота
rect.x;      // алиас left
rect.y;      // алиас top

// Позиция относительно документа
const scrollTop = window.scrollY || document.documentElement.scrollTop;
const absoluteTop = rect.top + scrollTop;

// offsetWidth/offsetHeight — layout size (включая padding, border)
el.offsetWidth;  // без scrollbar
el.clientWidth;  // без border, без scrollbar
el.scrollWidth;  // включая скрытую часть

// ✅ Определение переполнения
const isOverflowing = el.scrollWidth > el.clientWidth;

// Scroll
window.scrollTo({ top: 0, behavior: 'smooth' });
el.scrollIntoView({ behavior: 'smooth', block: 'start' });
el.scrollBy({ top: 100, behavior: 'smooth' });
```

### 9.5 Работа с формами

```js
// FormData — современный способ
const form = document.querySelector('form');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  
  const data = new FormData(form);
  
  // Чтение значений
  data.get('email');        // строка
  data.getAll('tags[]');    // массив (для multiple)
  [...data.entries()];      // все пары
  
  // Преобразование в объект
  const obj = Object.fromEntries(data);
  
  // Отправка как multipart (файлы) или JSON
  fetch('/api/submit', {
    method: 'POST',
    body: data, // Content-Type автоматически multipart/form-data
  });
});

// Валидация полей
const input = form.querySelector('input[name="email"]');
input.validity.valid;         // boolean
input.validity.valueMissing;  // true если required и пусто
input.validity.typeMismatch;  // true если неверный тип
input.validationMessage;      // браузерное сообщение
input.setCustomValidity('Уже занято'); // кастомная ошибка
input.setCustomValidity(''); // сброс

// Программная валидация
form.checkValidity(); // false если есть invalid поля
form.reportValidity(); // то же + показывает сообщения
```

---

## 10. События и делегирование

### 10.1 Современная работа с событиями

```js
// addEventListener — полный синтаксис
element.addEventListener(type, handler, options);

// options объект (предпочтительно)
el.addEventListener('click', handler, {
  once: true,       // автоматически удалить после первого срабатывания
  passive: true,    // обещаем не вызывать preventDefault (для scroll-оптимизации)
  capture: false,   // фаза захвата (true) или всплытие (false, default)
  signal: controller.signal, // AbortSignal для удаления
});

// ✅ Удаление через AbortController (лучший современный способ)
const controller = new AbortController();
const { signal } = controller;

el.addEventListener('click', handler, { signal });
el.addEventListener('mouseover', otherHandler, { signal });
window.addEventListener('resize', resizeHandler, { signal });

// Удалить все разом
controller.abort(); // все три listener удалятся

// Удаление через removeEventListener (требует ту же функцию!)
el.removeEventListener('click', handler); // handler должна быть та же ссылка
```

### 10.2 Делегирование событий

```js
// ❌ Плохо — listener на каждый элемент
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', handleClick);
});
// Проблемы: много listener-ов, не работает для динамически добавленных

// ✅ Делегирование — один listener на родителя
document.querySelector('.list').addEventListener('click', (e) => {
  const item = e.target.closest('.list-item');
  if (!item) return; // клик был вне элементов списка
  
  const action = e.target.closest('[data-action]')?.dataset.action;
  
  switch (action) {
    case 'delete': deleteItem(item.dataset.id); break;
    case 'edit':   editItem(item.dataset.id);   break;
    default:       selectItem(item.dataset.id);
  }
});

// Универсальный делегатор
function delegate(parent, selector, eventType, handler) {
  parent.addEventListener(eventType, (e) => {
    const target = e.target.closest(selector);
    if (target && parent.contains(target)) {
      handler.call(target, e, target);
    }
  });
}

delegate(document.body, '[data-action="delete"]', 'click', (e, btn) => {
  const id = btn.closest('[data-id]').dataset.id;
  deleteItem(id);
});
```

### 10.3 Custom Events

```js
// Создание и диспатч кастомных событий
function dispatch(element, eventName, detail = {}) {
  element.dispatchEvent(new CustomEvent(eventName, {
    detail,
    bubbles: true,    // всплывает вверх по DOM
    cancelable: true, // можно preventDefault()
    composed: true,   // проходит через Shadow DOM
  }));
}

// Dispatch
dispatch(formEl, 'form:submit', { data: formData });

// Listen — работает как обычное событие
formEl.addEventListener('form:submit', (e) => {
  console.log(e.detail.data);
});

// Паттерн — шина событий через document
const bus = {
  on: (event, handler) => document.addEventListener(event, handler),
  off: (event, handler) => document.removeEventListener(event, handler),
  emit: (event, detail) => document.dispatchEvent(
    new CustomEvent(event, { detail, bubbles: false })
  ),
};

bus.on('user:login', (e) => showWelcome(e.detail.user));
bus.emit('user:login', { user: { name: 'Иван' } });
```

### 10.4 Производительность событий

```js
// Debounce — задержка после последнего вызова
function debounce(fn, delay, { leading = false } = {}) {
  let timer;
  return function(...args) {
    const callNow = leading && !timer;
    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if (!leading) fn.apply(this, args);
    }, delay);
    if (callNow) fn.apply(this, args);
  };
}

// Throttle — не чаще чем раз в N мс
function throttle(fn, limit) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => { inThrottle = false; }, limit);
    }
  };
}

// Использование
input.addEventListener('input', debounce(search, 300));
window.addEventListener('scroll', throttle(updateHeader, 100));
window.addEventListener('resize', debounce(recalculate, 200));

// ✅ passive для scroll/touch — критично для производительности
window.addEventListener('scroll', handler, { passive: true });
document.addEventListener('touchmove', handler, { passive: true });
```

---

## 11. Fetch API и работа с сетью

### 11.1 Полный API клиент

```js
class HttpClient {
  #baseUrl;
  #defaultHeaders;
  #interceptors;

  constructor(baseUrl, options = {}) {
    this.#baseUrl = baseUrl.replace(/\/$/, '');
    this.#defaultHeaders = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    this.#interceptors = {
      request: options.requestInterceptor ?? (c => c),
      response: options.responseInterceptor ?? (r => r),
      error: options.errorInterceptor ?? null,
    };
  }

  async #request(method, path, { body, params, headers = {}, signal } = {}) {
    const url = new URL(this.#baseUrl + path);
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.set(key, value);
        }
      });
    }

    const config = this.#interceptors.request({
      method,
      headers: { ...this.#defaultHeaders, ...headers },
      body: body ? JSON.stringify(body) : undefined,
      signal,
    });

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = new HttpError(response.status, response.statusText, response);
        if (this.#interceptors.error) {
          return this.#interceptors.error(error);
        }
        throw error;
      }
      
      const contentType = response.headers.get('Content-Type') ?? '';
      const data = contentType.includes('application/json')
        ? await response.json()
        : await response.text();
        
      return this.#interceptors.response(data);
    } catch (error) {
      if (error instanceof HttpError) throw error;
      throw new NetworkError(error.message, error);
    }
  }

  get(path, options) { return this.#request('GET', path, options); }
  post(path, options) { return this.#request('POST', path, options); }
  put(path, options) { return this.#request('PUT', path, options); }
  patch(path, options) { return this.#request('PATCH', path, options); }
  delete(path, options) { return this.#request('DELETE', path, options); }
}

class HttpError extends Error {
  constructor(status, statusText, response) {
    super(`HTTP ${status}: ${statusText}`);
    this.name = 'HttpError';
    this.status = status;
    this.response = response;
  }
}

class NetworkError extends Error {
  constructor(message, cause) {
    super(message);
    this.name = 'NetworkError';
    this.cause = cause;
  }
}

// Использование
const api = new HttpClient('https://api.example.com', {
  headers: { Authorization: `Bearer ${token}` },
});

const users = await api.get('/users', { params: { page: 1, limit: 20 } });
const user = await api.post('/users', { body: { name, email } });
```

### 11.2 Retry и Timeout

```js
// Retry с экспоненциальным откатом
async function fetchWithRetry(url, options = {}, { retries = 3, delay = 500 } = {}) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      
      // Не ретраить 4xx (кроме 429 Too Many Requests)
      if (response.status < 500 && response.status !== 429) {
        throw new HttpError(response.status, response.statusText);
      }
      
      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      if (attempt === retries) throw error;
      if (error.name === 'AbortError') throw error; // не ретраить отменённые
      
      const waitTime = delay * 2 ** attempt + Math.random() * 100; // jitter
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
  }
}

// Timeout через AbortSignal (современный способ)
const response = await fetch(url, {
  signal: AbortSignal.timeout(5000), // ES2022
});

// Или вручную
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);
try {
  const response = await fetch(url, { signal: controller.signal });
} finally {
  clearTimeout(timeoutId);
}
```

### 11.3 Кэширование

```js
class CacheService {
  #cache = new Map();
  
  async get(key, fetcher, ttl = 60_000) {
    const cached = this.#cache.get(key);
    
    if (cached && Date.now() - cached.timestamp < ttl) {
      return cached.data;
    }
    
    const data = await fetcher();
    this.#cache.set(key, { data, timestamp: Date.now() });
    return data;
  }
  
  invalidate(key) { this.#cache.delete(key); }
  invalidateAll() { this.#cache.clear(); }
  
  // Запрос с дедупликацией — повторные запросы ждут первый
  #pending = new Map();
  
  async dedupe(key, fetcher) {
    if (this.#pending.has(key)) {
      return this.#pending.get(key);
    }
    
    const promise = fetcher().finally(() => this.#pending.delete(key));
    this.#pending.set(key, promise);
    return promise;
  }
}

const cache = new CacheService();
const user = await cache.get(`user:${id}`, () => api.get(`/users/${id}`), 5 * 60_000);
```

---

## 12. Хранилища данных в браузере

### 12.1 localStorage и sessionStorage

```js
// Обёртка с сериализацией и обработкой ошибок
class Storage {
  #storage;
  #prefix;

  constructor(type = 'local', prefix = 'app:') {
    this.#storage = type === 'local' ? localStorage : sessionStorage;
    this.#prefix = prefix;
  }

  #key(key) { return this.#prefix + key; }

  set(key, value, ttl = null) {
    try {
      const item = ttl
        ? { value, expires: Date.now() + ttl }
        : { value };
      this.#storage.setItem(this.#key(key), JSON.stringify(item));
      return true;
    } catch (e) {
      // QuotaExceededError — storage полон
      console.warn('Storage write failed:', e);
      return false;
    }
  }

  get(key, defaultValue = null) {
    try {
      const raw = this.#storage.getItem(this.#key(key));
      if (!raw) return defaultValue;

      const item = JSON.parse(raw);
      if (item.expires && Date.now() > item.expires) {
        this.remove(key);
        return defaultValue;
      }
      return item.value;
    } catch {
      return defaultValue;
    }
  }

  remove(key) { this.#storage.removeItem(this.#key(key)); }
  
  clear(prefix = '') {
    const fullPrefix = this.#prefix + prefix;
    [...Array(this.#storage.length).keys()]
      .map(i => this.#storage.key(i))
      .filter(key => key?.startsWith(fullPrefix))
      .forEach(key => this.#storage.removeItem(key));
  }
  
  // Listen to changes from other tabs
  static onExternalChange(callback) {
    window.addEventListener('storage', (e) => {
      callback({
        key: e.key,
        oldValue: JSON.parse(e.oldValue ?? 'null')?.value,
        newValue: JSON.parse(e.newValue ?? 'null')?.value,
        url: e.url,
      });
    });
  }
}

const store = new Storage('local', 'myapp:');
store.set('user', { name: 'Иван' }, 24 * 60 * 60 * 1000); // 24 часа TTL
store.get('user'); // { name: 'Иван' }
```

### 12.2 IndexedDB — асинхронное хранилище

```js
// Современная обёртка над IndexedDB
class IDB {
  #db = null;
  #name;
  #version;
  #stores;

  constructor(name, version, stores) {
    this.#name = name;
    this.#version = version;
    this.#stores = stores;
  }

  async open() {
    if (this.#db) return this;
    
    this.#db = await new Promise((resolve, reject) => {
      const request = indexedDB.open(this.#name, this.#version);
      
      request.onupgradeneeded = (e) => {
        const db = e.target.result;
        this.#stores.forEach(({ name, keyPath, indexes = [] }) => {
          if (!db.objectStoreNames.contains(name)) {
            const store = db.createObjectStore(name, { keyPath });
            indexes.forEach(({ name: iName, keyPath: iKeyPath, options }) => {
              store.createIndex(iName, iKeyPath, options);
            });
          }
        });
      };
      
      request.onsuccess = e => resolve(e.target.result);
      request.onerror = e => reject(e.target.error);
    });
    
    return this;
  }

  #transaction(storeName, mode = 'readonly') {
    return this.#db.transaction(storeName, mode).objectStore(storeName);
  }

  async get(store, key) {
    return this.#promisify(this.#transaction(store).get(key));
  }

  async put(store, value) {
    return this.#promisify(this.#transaction(store, 'readwrite').put(value));
  }

  async delete(store, key) {
    return this.#promisify(this.#transaction(store, 'readwrite').delete(key));
  }

  async getAll(store, query = null, count = undefined) {
    return this.#promisify(this.#transaction(store).getAll(query, count));
  }

  async clear(store) {
    return this.#promisify(this.#transaction(store, 'readwrite').clear());
  }

  #promisify(request) {
    return new Promise((resolve, reject) => {
      request.onsuccess = e => resolve(e.target.result);
      request.onerror = e => reject(e.target.error);
    });
  }
}

// Использование
const db = new IDB('myApp', 1, [
  { name: 'users', keyPath: 'id', indexes: [{ name: 'email', keyPath: 'email', options: { unique: true } }] },
  { name: 'posts', keyPath: 'id' },
]);

await db.open();
await db.put('users', { id: 1, email: 'a@b.com', name: 'Иван' });
const user = await db.get('users', 1);
```

---

## 13. Управление состоянием

### 13.1 Реактивное состояние на Proxy

```js
// Реактивность через Proxy — основа Vue, MobX
function reactive(target, onChange) {
  const handler = {
    get(obj, key) {
      const value = obj[key];
      if (value && typeof value === 'object') {
        return reactive(value, onChange); // вложенная реактивность
      }
      return value;
    },
    set(obj, key, value) {
      const oldValue = obj[key];
      obj[key] = value;
      if (oldValue !== value) onChange(key, value, oldValue);
      return true;
    },
    deleteProperty(obj, key) {
      const hadKey = key in obj;
      delete obj[key];
      if (hadKey) onChange(key, undefined, obj[key]);
      return true;
    },
  };
  return new Proxy(target, handler);
}

// Хранилище состояния
class Store {
  #state;
  #listeners = new Map();
  #history = [];
  #maxHistory = 50;

  constructor(initialState) {
    this.#state = reactive({ ...initialState }, (key) => {
      this.#notify(key);
    });
  }

  get state() {
    return this.#state;
  }

  // Подписка на конкретный ключ или '*' для всех
  subscribe(key, listener) {
    if (!this.#listeners.has(key)) this.#listeners.set(key, new Set());
    this.#listeners.get(key).add(listener);
    
    // Возвращаем функцию отписки
    return () => this.#listeners.get(key).delete(listener);
  }

  update(updater) {
    this.#history.push(structuredClone(this.#state));
    if (this.#history.length > this.#maxHistory) this.#history.shift();
    
    if (typeof updater === 'function') {
      updater(this.#state);
    } else {
      Object.assign(this.#state, updater);
    }
  }

  undo() {
    const prev = this.#history.pop();
    if (prev) Object.assign(this.#state, prev);
  }

  #notify(key) {
    this.#listeners.get(key)?.forEach(fn => fn(this.#state[key], this.#state));
    this.#listeners.get('*')?.forEach(fn => fn(this.#state[key], this.#state));
  }
}

// Использование
const store = new Store({ count: 0, user: null, loading: false });

const unsub = store.subscribe('count', (newCount) => {
  counterEl.textContent = newCount;
});

store.update({ count: 1 });
store.update(s => s.count++);
store.undo();

unsub(); // отписаться
```

### 13.2 Простое управление состоянием компонента

```js
// Сигналы — современный паттерн (как в Solid.js, Preact Signals)
function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  const get = () => value;
  
  const set = (newValue) => {
    const next = typeof newValue === 'function' ? newValue(value) : newValue;
    if (next !== value) {
      value = next;
      subscribers.forEach(fn => fn(value));
    }
  };

  const subscribe = (fn) => {
    subscribers.add(fn);
    return () => subscribers.delete(fn);
  };

  return { get, set, subscribe };
}

function createEffect(fn, deps) {
  const run = () => fn();
  deps.forEach(dep => dep.subscribe(run));
  run(); // немедленный запуск
}

// Использование
const count = createSignal(0);
const doubled = { get: () => count.get() * 2 }; // производное состояние

createEffect(() => {
  document.querySelector('#counter').textContent = count.get();
}, [count]);

count.set(x => x + 1); // реактивное обновление
```

---

## 14. Паттерны проектирования

### 14.1 Singleton

```js
// ES Module — сам по себе singleton (выполняется один раз)
// services/database.js
let instance = null;

export function getDatabase() {
  if (!instance) {
    instance = new Database();
  }
  return instance;
}

// Или через static
class AppConfig {
  static #instance = null;
  
  static getInstance() {
    return (AppConfig.#instance ??= new AppConfig());
  }
  
  // Приватный конструктор — условно, JS не запрещает new
  constructor() {
    if (AppConfig.#instance) throw new Error('Use AppConfig.getInstance()');
    this.theme = 'dark';
    this.lang = 'ru';
  }
}
```

### 14.2 Observer (pub/sub)

```js
class EventBus {
  #events = new Map();
  
  on(event, callback, { once = false, signal } = {}) {
    if (!this.#events.has(event)) this.#events.set(event, new Set());
    
    const wrapper = once ? (...args) => {
      callback(...args);
      this.off(event, wrapper);
    } : callback;
    
    this.#events.get(event).add(wrapper);
    
    // AbortSignal поддержка
    signal?.addEventListener('abort', () => this.off(event, wrapper), { once: true });
    
    return () => this.off(event, wrapper);
  }

  off(event, callback) {
    this.#events.get(event)?.delete(callback);
  }

  emit(event, ...args) {
    this.#events.get(event)?.forEach(fn => {
      try { fn(...args); } catch (e) { console.error(e); }
    });
  }
  
  once(event, callback) { return this.on(event, callback, { once: true }); }
  
  clear(event) {
    event ? this.#events.delete(event) : this.#events.clear();
  }
}

export const bus = new EventBus();
```

### 14.3 Factory

```js
// Фабрика компонентов
const ComponentFactory = {
  #registry = new Map(),
  
  register(name, ComponentClass) {
    this.#registry.set(name, ComponentClass);
    return this; // chaining
  },
  
  create(name, ...args) {
    const ComponentClass = this.#registry.get(name);
    if (!ComponentClass) throw new Error(`Unknown component: ${name}`);
    return new ComponentClass(...args);
  },
};

ComponentFactory
  .register('button', ButtonComponent)
  .register('modal', ModalComponent)
  .register('table', TableComponent);

const modal = ComponentFactory.create('modal', { title: 'Hello' });
```

### 14.4 Command (Undo/Redo)

```js
class CommandHistory {
  #undoStack = [];
  #redoStack = [];

  execute(command) {
    command.execute();
    this.#undoStack.push(command);
    this.#redoStack = []; // новая команда инвалидирует redo
  }

  undo() {
    const command = this.#undoStack.pop();
    if (!command) return;
    command.undo();
    this.#redoStack.push(command);
  }

  redo() {
    const command = this.#redoStack.pop();
    if (!command) return;
    command.execute();
    this.#undoStack.push(command);
  }

  get canUndo() { return this.#undoStack.length > 0; }
  get canRedo() { return this.#redoStack.length > 0; }
}

// Команда
class SetStyleCommand {
  constructor(element, property, newValue) {
    this.element = element;
    this.property = property;
    this.newValue = newValue;
    this.oldValue = element.style[property];
  }
  execute() { this.element.style[this.property] = this.newValue; }
  undo()    { this.element.style[this.property] = this.oldValue; }
}

const history = new CommandHistory();
history.execute(new SetStyleCommand(el, 'color', 'red'));
history.undo();
```

### 14.5 Strategy

```js
// Стратегия — взаимозаменяемые алгоритмы
const SortStrategies = {
  bubble: (arr) => { /*...*/ },
  quick: (arr) => { /*...*/ },
  merge: (arr) => { /*...*/ },
};

class DataList {
  #data;
  #strategy;
  
  constructor(data, strategy = 'quick') {
    this.#data = data;
    this.#strategy = SortStrategies[strategy];
  }
  
  setStrategy(name) {
    if (!SortStrategies[name]) throw new Error(`Unknown strategy: ${name}`);
    this.#strategy = SortStrategies[name];
  }
  
  sort() { return this.#strategy([...this.#data]); }
}
```

### 14.6 Proxy паттерн

```js
// Proxy для логирования, валидации, кэширования
function createValidatedModel(target, schema) {
  return new Proxy(target, {
    set(obj, key, value) {
      if (schema[key]) {
        const { type, min, max, required } = schema[key];
        if (required && !value) throw new Error(`${key} is required`);
        if (type && typeof value !== type) throw new TypeError(`${key} must be ${type}`);
        if (min !== undefined && value < min) throw new RangeError(`${key} min is ${min}`);
        if (max !== undefined && value > max) throw new RangeError(`${key} max is ${max}`);
      }
      obj[key] = value;
      return true;
    },
  });
}

const user = createValidatedModel({}, {
  name: { type: 'string', required: true },
  age: { type: 'number', min: 0, max: 150 },
});

user.name = 'Иван'; // OK
user.age = -5; // RangeError
```

---

## 15. Современные Observer API

### 15.1 IntersectionObserver — ленивая загрузка

```js
// Ленивая загрузка изображений
function lazyLoadImages(selector = 'img[data-src]') {
  const images = document.querySelectorAll(selector);
  
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        
        const img = entry.target;
        img.src = img.dataset.src;
        img.srcset = img.dataset.srcset ?? '';
        img.removeAttribute('data-src');
        obs.unobserve(img);
      });
    }, {
      rootMargin: '200px 0px', // начать загрузку за 200px до появления
      threshold: 0,
    });
    
    images.forEach(img => observer.observe(img));
    return () => observer.disconnect();
  } else {
    // Fallback
    images.forEach(img => {
      img.src = img.dataset.src;
    });
  }
}

// Анимация при появлении в viewport
function animateOnScroll(selector, className = 'visible') {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add(className);
        observer.unobserve(entry.target); // только раз
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll(selector).forEach(el => observer.observe(el));
  return () => observer.disconnect();
}

// Infinite scroll
function setupInfiniteScroll(sentinel, loadMore) {
  const observer = new IntersectionObserver(async ([entry]) => {
    if (!entry.isIntersecting) return;
    observer.unobserve(sentinel);
    await loadMore();
    observer.observe(sentinel);
  }, { rootMargin: '100px' });

  observer.observe(sentinel);
  return () => observer.disconnect();
}
```

### 15.2 MutationObserver — наблюдение за DOM

```js
// Отслеживание изменений DOM
function watchDOM(target, callback, options = {}) {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      switch (mutation.type) {
        case 'childList':
          callback('children', {
            added: [...mutation.addedNodes],
            removed: [...mutation.removedNodes],
          });
          break;
        case 'attributes':
          callback('attribute', {
            name: mutation.attributeName,
            oldValue: mutation.oldValue,
            newValue: mutation.target.getAttribute(mutation.attributeName),
          });
          break;
        case 'characterData':
          callback('text', {
            oldValue: mutation.oldValue,
            newValue: mutation.target.textContent,
          });
          break;
      }
    });
  });

  observer.observe(target, {
    childList: true,           // изменения дочерних узлов
    subtree: true,             // рекурсивно
    attributes: true,          // изменения атрибутов
    attributeOldValue: true,   // сохранять старые значения атрибутов
    characterData: true,       // изменения текстовых узлов
    characterDataOldValue: true,
    ...options,
  });

  return () => observer.disconnect();
}

// Паттерн — авто-инициализация компонентов
const initComponents = () => {
  document.querySelectorAll('[data-component]:not([data-init])')
    .forEach(el => {
      const name = el.dataset.component;
      ComponentFactory.create(name, el);
      el.dataset.init = 'true';
    });
};

const unwatch = watchDOM(document.body, (type, data) => {
  if (type === 'children' && data.added.length) {
    initComponents();
  }
}, { childList: true, subtree: true, attributes: false });
```

### 15.3 ResizeObserver — реакция на изменение размеров

```js
// Адаптивная логика без window resize
function watchSize(element, callback) {
  let rafId;
  
  const observer = new ResizeObserver((entries) => {
    // Используем rAF чтобы избежать лишних вычислений
    cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(() => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        callback({ width, height, element: entry.target });
      }
    });
  });

  observer.observe(element);
  return () => { observer.unobserve(element); cancelAnimationFrame(rafId); };
}

// Использование
const stopWatching = watchSize(chart, ({ width }) => {
  chart.rerender({ columns: width > 600 ? 12 : 4 });
});
```

### 15.4 PerformanceObserver

```js
// Мониторинг производительности
const perfObserver = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    if (entry.entryType === 'largest-contentful-paint') {
      console.log('LCP:', entry.startTime);
    }
    if (entry.entryType === 'layout-shift') {
      console.log('CLS delta:', entry.value);
    }
    if (entry.entryType === 'first-input') {
      console.log('FID:', entry.processingStart - entry.startTime);
    }
  });
});

perfObserver.observe({ entryTypes: ['largest-contentful-paint', 'layout-shift', 'first-input'] });
```

---

## 16. Web Components

### 16.1 Custom Elements

```js
class ToastNotification extends HTMLElement {
  // Отслеживаемые атрибуты
  static observedAttributes = ['type', 'message', 'duration'];
  
  // Shadow DOM для инкапсуляции стилей
  #shadow;
  #timer;

  constructor() {
    super();
    this.#shadow = this.attachShadow({ mode: 'open' });
  }

  // Lifecycle callbacks
  connectedCallback() {
    this.#render();
    this.#setup();
  }

  disconnectedCallback() {
    clearTimeout(this.#timer);
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) this.#render();
  }

  // Геттеры для атрибутов
  get type() { return this.getAttribute('type') ?? 'info'; }
  get message() { return this.getAttribute('message') ?? ''; }
  get duration() { return Number(this.getAttribute('duration') ?? 3000); }

  #render() {
    this.#shadow.innerHTML = `
      <style>
        :host {
          display: block;
          position: fixed;
          bottom: 1rem;
          right: 1rem;
          z-index: 9999;
        }
        .toast {
          padding: 0.75rem 1.25rem;
          border-radius: 0.5rem;
          color: white;
          font-family: system-ui;
          animation: slideIn 0.3s ease;
        }
        .toast--info    { background: #3b82f6; }
        .toast--success { background: #10b981; }
        .toast--error   { background: #ef4444; }
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to   { transform: translateX(0);   opacity: 1; }
        }
      </style>
      <div class="toast toast--${this.type}" role="alert">
        ${this.message}
      </div>
    `;
  }

  #setup() {
    if (this.duration > 0) {
      this.#timer = setTimeout(() => this.remove(), this.duration);
    }
  }
  
  // Статический метод-утилита
  static show(message, type = 'info', duration = 3000) {
    const toast = document.createElement('app-toast');
    toast.setAttribute('message', message);
    toast.setAttribute('type', type);
    toast.setAttribute('duration', String(duration));
    document.body.append(toast);
    return toast;
  }
}

customElements.define('app-toast', ToastNotification);

// Использование
ToastNotification.show('Сохранено!', 'success');
// или в HTML: <app-toast message="Привет" type="info"></app-toast>
```

### 16.2 HTML Templates и Slots

```js
// template элемент — клонируемый инертный HTML
const template = document.createElement('template');
template.innerHTML = `
  <style>
    .card { border: 1px solid #e2e8f0; border-radius: 8px; }
    ::slotted(h2) { margin: 0; }
  </style>
  <div class="card">
    <header class="card__header">
      <slot name="title"><span>Без заголовка</span></slot>
    </header>
    <div class="card__body">
      <slot></slot>  <!-- дефолтный слот -->
    </div>
    <footer class="card__footer">
      <slot name="actions"></slot>
    </footer>
  </div>
`;

class CardComponent extends HTMLElement {
  connectedCallback() {
    const shadow = this.attachShadow({ mode: 'open' });
    shadow.append(template.content.cloneNode(true));
  }
}

customElements.define('ui-card', CardComponent);

// В HTML:
// <ui-card>
//   <h2 slot="title">Заголовок</h2>
//   <p>Контент</p>
//   <button slot="actions">OK</button>
// </ui-card>
```

---

## 17. Производительность

### 17.1 requestAnimationFrame — анимации

```js
// ✅ Анимация через rAF — синхронизация с частотой экрана
class Animator {
  #rafId = null;
  #startTime = null;

  animate(duration, onFrame, onComplete) {
    this.stop();
    
    const tick = (timestamp) => {
      if (!this.#startTime) this.#startTime = timestamp;
      const elapsed = timestamp - this.#startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      onFrame(easeInOutQuad(progress)); // прогресс 0→1
      
      if (progress < 1) {
        this.#rafId = requestAnimationFrame(tick);
      } else {
        this.#startTime = null;
        onComplete?.();
      }
    };
    
    this.#rafId = requestAnimationFrame(tick);
    return this;
  }

  stop() {
    if (this.#rafId) {
      cancelAnimationFrame(this.#rafId);
      this.#rafId = null;
      this.#startTime = null;
    }
    return this;
  }
}

// Функции смягчения
const easeInOutQuad = t => t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
const easeOutCubic  = t => 1 - Math.pow(1-t, 3);

// Smooth scroll
function smoothScrollTo(target, duration = 500) {
  const start = window.scrollY;
  const end = target instanceof Element
    ? target.getBoundingClientRect().top + start
    : target;
  const distance = end - start;
  
  new Animator().animate(duration, (progress) => {
    window.scrollTo(0, start + distance * easeInOutQuad(progress));
  });
}
```

### 17.2 Virtual Scrolling — рендер тысяч элементов

```js
class VirtualList {
  #container;
  #itemHeight;
  #items;
  #renderItem;
  #visibleItems = new Map();
  #rafId;

  constructor({ container, itemHeight, items, renderItem }) {
    this.#container = container;
    this.#itemHeight = itemHeight;
    this.#items = items;
    this.#renderItem = renderItem;
    this.#init();
  }

  #init() {
    // Внутренний контейнер полной высоты
    this.#inner = document.createElement('div');
    this.#inner.style.height = `${this.#items.length * this.#itemHeight}px`;
    this.#inner.style.position = 'relative';
    this.#container.append(this.#inner);
    
    this.#container.style.overflow = 'auto';
    this.#container.style.position = 'relative';
    
    this.#container.addEventListener('scroll', () => {
      cancelAnimationFrame(this.#rafId);
      this.#rafId = requestAnimationFrame(() => this.#render());
    }, { passive: true });
    
    this.#render();
  }

  #render() {
    const { scrollTop, clientHeight } = this.#container;
    const startIndex = Math.max(0, Math.floor(scrollTop / this.#itemHeight) - 2);
    const endIndex = Math.min(
      this.#items.length - 1,
      Math.ceil((scrollTop + clientHeight) / this.#itemHeight) + 2
    );

    // Удалить элементы вне видимой области
    for (const [i, el] of this.#visibleItems) {
      if (i < startIndex || i > endIndex) {
        el.remove();
        this.#visibleItems.delete(i);
      }
    }

    // Добавить новые видимые элементы
    for (let i = startIndex; i <= endIndex; i++) {
      if (this.#visibleItems.has(i)) continue;
      const el = this.#renderItem(this.#items[i], i);
      el.style.position = 'absolute';
      el.style.top = `${i * this.#itemHeight}px`;
      el.style.width = '100%';
      this.#inner.append(el);
      this.#visibleItems.set(i, el);
    }
  }
}
```

### 17.3 Web Workers — тяжёлые вычисления

```js
// ✅ Перенос тяжёлой работы в Worker
// worker.js (отдельный файл)
self.addEventListener('message', (e) => {
  const { type, payload, id } = e.data;
  
  try {
    let result;
    if (type === 'sort') result = heavySort(payload);
    if (type === 'process') result = processData(payload);
    self.postMessage({ id, result });
  } catch (error) {
    self.postMessage({ id, error: error.message });
  }
});

// main.js — обёртка над Worker
class WorkerPool {
  #worker;
  #pending = new Map();
  #idCounter = 0;

  constructor(workerUrl) {
    this.#worker = new Worker(workerUrl, { type: 'module' });
    this.#worker.addEventListener('message', ({ data }) => {
      const { id, result, error } = data;
      const { resolve, reject } = this.#pending.get(id) ?? {};
      this.#pending.delete(id);
      error ? reject(new Error(error)) : resolve(result);
    });
  }

  run(type, payload) {
    return new Promise((resolve, reject) => {
      const id = ++this.#idCounter;
      this.#pending.set(id, { resolve, reject });
      this.#worker.postMessage({ type, payload, id });
    });
  }

  terminate() { this.#worker.terminate(); }
}

const pool = new WorkerPool('./worker.js');
const sorted = await pool.run('sort', hugeArray);
```

### 17.4 Оптимизация работы с DOM

```js
// ❌ Forced Layout/Reflow — чтение и запись вперемешку
boxes.forEach(box => {
  const height = box.offsetHeight;  // read — reflow
  box.style.height = height + 10 + 'px'; // write
  const width = box.offsetWidth;   // read — снова reflow!
  box.style.width = width + 10 + 'px'; // write
});

// ✅ Batch reads, then batch writes
const sizes = boxes.map(box => ({
  h: box.offsetHeight,
  w: box.offsetWidth,
}));
boxes.forEach((box, i) => {
  box.style.height = sizes[i].h + 10 + 'px';
  box.style.width = sizes[i].w + 10 + 'px';
});

// ✅ CSS contain для изоляции layout
// .component { contain: content; }  — в CSS
// Тогда изменения внутри не вызывают reflow снаружи

// ✅ will-change — подсказка браузеру
el.style.willChange = 'transform'; // только для элементов которые анимируются!
// После анимации убери: el.style.willChange = 'auto';

// ✅ CSS transform вместо top/left
// ❌ el.style.top = y + 'px';
// ✅ el.style.transform = `translateY(${y}px)`;
```

### 17.5 Мемоизация и кэширование

```js
// Мемоизация с WeakMap (для объектных аргументов — GC-friendly)
function memoizeWeak(fn) {
  const cache = new WeakMap();
  return function(arg) {
    if (cache.has(arg)) return cache.get(arg);
    const result = fn.call(this, arg);
    cache.set(arg, result);
    return result;
  };
}

// LRU Cache
class LRUCache {
  #capacity;
  #cache = new Map();

  constructor(capacity) { this.#capacity = capacity; }

  get(key) {
    if (!this.#cache.has(key)) return undefined;
    // Переставить в конец (LRU порядок)
    const value = this.#cache.get(key);
    this.#cache.delete(key);
    this.#cache.set(key, value);
    return value;
  }

  set(key, value) {
    if (this.#cache.has(key)) this.#cache.delete(key);
    else if (this.#cache.size >= this.#capacity) {
      // Удалить наименее используемый (первый в Map)
      this.#cache.delete(this.#cache.keys().next().value);
    }
    this.#cache.set(key, value);
  }
}
```

---

## 18. Безопасность

### 18.1 XSS предотвращение

```js
// ❌ НИКОГДА не делай так с пользовательскими данными
el.innerHTML = userInput;
document.write(userInput);
eval(userInput);
new Function(userInput)();
el.setAttribute('href', userInput); // javascript: URL!

// ✅ Эскейпинг HTML
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
  // Альтернатива — ручной replace
}

// Или через Map
const htmlEntities = new Map([
  ['&', '&amp;'],
  ['<', '&lt;'],
  ['>', '&gt;'],
  ['"', '&quot;'],
  ["'", '&#x27;'],
]);
const escapeHtml2 = str => str.replace(/[&<>"']/g, ch => htmlEntities.get(ch));

// ✅ Используй textContent вместо innerHTML для пользовательских данных
el.textContent = userInput; // безопасно всегда

// ✅ DOMPurify для санитизации доверенного HTML
// Используй библиотеку DOMPurify если нужно рендерить HTML от пользователя
import DOMPurify from 'dompurify';
el.innerHTML = DOMPurify.sanitize(userHtml);

// ✅ Валидация URL
function isSafeUrl(url) {
  try {
    const parsed = new URL(url);
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}

// ✅ Безопасные атрибуты
function setSafeHref(link, url) {
  if (isSafeUrl(url)) {
    link.href = url;
  } else {
    console.warn('Unsafe URL blocked:', url);
  }
}
```

### 18.2 Content Security Policy

```js
// В HTTP заголовке или meta тег:
// Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com; img-src * data:;

// Динамические скрипты — использовать nonce
// В HTML: <script nonce="abc123">...</script>
// В CSP: script-src 'nonce-abc123'

// Использование Trusted Types (современный стандарт)
if (window.trustedTypes?.createPolicy) {
  const policy = trustedTypes.createPolicy('app', {
    createHTML: (input) => DOMPurify.sanitize(input),
    createScriptURL: (url) => isSafeUrl(url) ? url : '',
  });
  
  el.innerHTML = policy.createHTML(userHtml); // безопасно!
}
```

### 18.3 Защита от CSRF и других атак

```js
// CSRF токен
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content
    ?? document.cookie.match(/csrf-token=([^;]+)/)?.[1];
}

// Добавлять CSRF токен к мутирующим запросам
const api = new HttpClient('/api', {
  requestInterceptor: (config) => {
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(config.method)) {
      config.headers['X-CSRF-Token'] = getCsrfToken();
    }
    return config;
  },
});

// Clickjacking защита (проверка в iframe)
if (window.top !== window.self) {
  document.body.innerHTML = 'Страница не может быть загружена в iframe';
  window.top.location = window.self.location;
}

// Sanitize localStorage перед парсингом
function safeGet(key) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    return JSON.parse(raw); // может упасть на плохих данных
  } catch {
    localStorage.removeItem(key); // удалить битые данные
    return null;
  }
}
```

---

## 19. Обработка ошибок

### 19.1 Иерархия кастомных ошибок

```js
// Базовый класс
class AppError extends Error {
  constructor(message, code, context = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.context = context;
    this.timestamp = new Date().toISOString();
    
    // Корректный stack trace в V8
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }
  
  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      context: this.context,
    };
  }
}

class ValidationError extends AppError {
  constructor(field, message, value) {
    super(message, 'VALIDATION_ERROR', { field, value });
    this.field = field;
  }
}

class NetworkError extends AppError {
  constructor(message, status, url) {
    super(message, 'NETWORK_ERROR', { status, url });
    this.status = status;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} with id ${id} not found`, 'NOT_FOUND', { resource, id });
  }
}

// Использование
try {
  throw new ValidationError('email', 'Invalid email format', 'not-an-email');
} catch (error) {
  if (error instanceof ValidationError) {
    showFieldError(error.field, error.message);
  } else if (error instanceof NetworkError) {
    showNetworkError();
  } else {
    throw error; // передать выше
  }
}
```

### 19.2 Глобальная обработка ошибок

```js
// Перехват синхронных ошибок
window.addEventListener('error', (event) => {
  const { error, filename, lineno, colno } = event;
  reportError({
    type: 'uncaught',
    message: error?.message,
    stack: error?.stack,
    source: `${filename}:${lineno}:${colno}`,
  });
  // event.preventDefault(); — подавить дефолтный вывод в консоль
});

// Перехват необработанных отклонений промисов
window.addEventListener('unhandledrejection', (event) => {
  const { reason, promise } = event;
  reportError({
    type: 'unhandledRejection',
    message: reason?.message ?? String(reason),
    stack: reason?.stack,
  });
  event.preventDefault(); // предотвратить вывод в консоль
});

// Сервис отчётов об ошибках
async function reportError(errorInfo) {
  try {
    await fetch('/api/errors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...errorInfo,
        url: location.href,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString(),
      }),
      keepalive: true, // отправить даже при выгрузке страницы
    });
  } catch {
    // Молча игнорировать — не хотим рекурсии ошибок
  }
}
```

### 19.3 Result тип (Railway-oriented programming)

```js
// Функциональный паттерн — явная обработка ошибок без try/catch
class Result {
  #value;
  #error;
  #isOk;

  constructor(value, error, isOk) {
    this.#value = value;
    this.#error = error;
    this.#isOk = isOk;
  }

  static ok(value) { return new Result(value, null, true); }
  static err(error) { return new Result(null, error, false); }

  get isOk() { return this.#isOk; }
  get isErr() { return !this.#isOk; }
  get value() {
    if (!this.#isOk) throw new Error('Cannot get value of Err');
    return this.#value;
  }
  get error() {
    if (this.#isOk) throw new Error('Cannot get error of Ok');
    return this.#error;
  }

  map(fn) { return this.#isOk ? Result.ok(fn(this.#value)) : this; }
  flatMap(fn) { return this.#isOk ? fn(this.#value) : this; }
  mapErr(fn) { return !this.#isOk ? Result.err(fn(this.#error)) : this; }
  
  match({ ok, err }) {
    return this.#isOk ? ok(this.#value) : err(this.#error);
  }
  
  unwrapOr(defaultValue) {
    return this.#isOk ? this.#value : defaultValue;
  }
}

// Обёртка для async функций
async function tryAsync(fn) {
  try {
    return Result.ok(await fn());
  } catch (error) {
    return Result.err(error);
  }
}

// Использование
const result = await tryAsync(() => api.get('/users'));

result.match({
  ok: users => renderUsers(users),
  err: error => showError(error.message),
});

// Цепочка
const processed = result
  .map(users => users.filter(u => u.active))
  .map(users => users.sort((a, b) => a.name.localeCompare(b.name)))
  .unwrapOr([]);
```

---

## 20. Современные Web API

### 20.1 URL и URLSearchParams

```js
// Работа с URL
const url = new URL('https://example.com/search?q=test&page=2');
url.hostname;  // 'example.com'
url.pathname;  // '/search'
url.hash;      // ''
url.searchParams.get('q');   // 'test'
url.searchParams.get('page'); // '2'

// Изменение
url.searchParams.set('page', 3);
url.searchParams.append('filter', 'active');
url.searchParams.delete('q');
url.toString(); // полная строка URL

// Создание query строки
const params = new URLSearchParams({
  q: 'поиск',
  sort: 'date',
  order: 'desc',
});
params.toString(); // 'q=%D0%BF%D0%BE%D0%B8%D1%81%D0%BA&sort=date&order=desc'

// Итерация
for (const [key, value] of params) { /*...*/ }
Object.fromEntries(params); // в объект
```

### 20.2 Clipboard API

```js
// Запись в буфер обмена
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback для старых браузеров
    const el = document.createElement('textarea');
    el.value = text;
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.append(el);
    el.select();
    const success = document.execCommand('copy');
    el.remove();
    return success;
  }
}

// Чтение из буфера (требует разрешения)
async function readFromClipboard() {
  try {
    return await navigator.clipboard.readText();
  } catch {
    return null;
  }
}
```

### 20.3 Notifications API

```js
// Push-уведомления
async function requestNotifications() {
  if (!('Notification' in window)) return false;
  if (Notification.permission === 'granted') return true;
  if (Notification.permission === 'denied') return false;
  
  const permission = await Notification.requestPermission();
  return permission === 'granted';
}

async function notify(title, options = {}) {
  if (!(await requestNotifications())) return;
  
  const notification = new Notification(title, {
    body: options.body ?? '',
    icon: options.icon ?? '/icon.png',
    badge: options.badge,
    tag: options.tag ?? 'default',
    renotify: true,
    silent: false,
    ...options,
  });
  
  notification.addEventListener('click', () => {
    window.focus();
    notification.close();
    options.onClick?.();
  });
  
  return notification;
}
```

### 20.4 Page Visibility API

```js
// Определение видимости вкладки
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    // Вкладка скрыта — пауза, экономия ресурсов
    pauseAnimations();
    stopPolling();
  } else {
    // Вкладка снова активна
    resumeAnimations();
    startPolling();
    syncDataIfStale();
  }
});

// Polling с учётом видимости
function startSmartPolling(fn, interval) {
  let timer;
  
  const poll = async () => {
    if (!document.hidden) await fn();
    timer = setTimeout(poll, interval);
  };
  
  poll();
  return () => clearTimeout(timer);
}
```

### 20.5 History API

```js
// Управление историей браузера (SPA routing)
class Router {
  #routes = new Map();
  #notFound = null;

  route(path, handler) {
    this.#routes.set(path, handler);
    return this;
  }

  notFound(handler) {
    this.#notFound = handler;
    return this;
  }

  navigate(path, state = {}, { replace = false } = {}) {
    if (replace) {
      history.replaceState(state, '', path);
    } else {
      history.pushState(state, '', path);
    }
    this.#dispatch(path, state);
  }

  start() {
    window.addEventListener('popstate', (e) => {
      this.#dispatch(location.pathname, e.state);
    });
    this.#dispatch(location.pathname, history.state);
    return this;
  }

  #dispatch(path, state) {
    const handler = this.#routes.get(path)
      ?? this.#findDynamic(path)
      ?? this.#notFound;
    handler?.(path, state);
  }

  #findDynamic(path) {
    for (const [pattern, handler] of this.#routes) {
      const regex = new RegExp('^' + pattern.replace(/:(\w+)/g, '(?<$1>[^/]+)') + '$');
      const match = path.match(regex);
      if (match) return (p, s) => handler(p, { ...s, params: match.groups });
    }
    return null;
  }
}

const router = new Router()
  .route('/', () => renderHome())
  .route('/users', () => renderUsers())
  .route('/users/:id', (path, { params }) => renderUser(params.id))
  .notFound(() => render404())
  .start();

router.navigate('/users/42');
```

### 20.6 structuredClone и transferable objects

```js
// structuredClone — нативное глубокое клонирование (ES2022)
const original = {
  date: new Date(),
  map: new Map([['a', 1]]),
  set: new Set([1, 2, 3]),
  arr: [1, [2, 3]],
  buffer: new ArrayBuffer(8),
};
const clone = structuredClone(original);
// Поддерживает: Date, Map, Set, ArrayBuffer, RegExp, Error, bigint
// НЕ поддерживает: Function, DOM nodes, WeakMap/WeakSet, Symbol

// Transfer — передача без копирования (в Worker)
const buffer = new ArrayBuffer(1024 * 1024); // 1MB
worker.postMessage({ buffer }, [buffer]); // buffer передаётся, не копируется!
// После transfer buffer в main thread становится пустым
```

---

## 21. Анимации и визуальные эффекты

### 21.1 Web Animations API

```js
// Нативные CSS-анимации из JS
const animation = element.animate([
  { opacity: 0, transform: 'translateY(-20px)' },
  { opacity: 1, transform: 'translateY(0)' },
], {
  duration: 300,
  easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  fill: 'forwards',
  delay: 0,
  iterations: 1,
});

// Управление
animation.pause();
animation.play();
animation.reverse();
animation.cancel();
animation.finish();

// Promise по завершении
await animation.finished;
element.classList.add('visible');

// Keyframe эффект
const effect = new KeyframeEffect(element, [
  { transform: 'scale(1)' },
  { transform: 'scale(1.1)' },
  { transform: 'scale(1)' },
], { duration: 200, easing: 'ease-in-out' });

const anim = new Animation(effect, document.timeline);
anim.play();
```

### 21.2 CSS Custom Properties и JS

```js
// Управление CSS переменными из JS — мощный паттерн
const root = document.documentElement;

// Читать
const primaryColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();

// Устанавливать
root.style.setProperty('--primary-color', '#3b82f6');
root.style.setProperty('--spacing-unit', '8px');

// Анимация через CSS переменные
function animateValue(property, from, to, duration, easing = easeInOutQuad) {
  const start = performance.now();
  
  const tick = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const value = from + (to - from) * easing(progress);
    
    root.style.setProperty(property, value);
    
    if (progress < 1) requestAnimationFrame(tick);
  };
  
  requestAnimationFrame(tick);
}

animateValue('--scroll-progress', 0, 1, 500);
```

### 21.3 Canvas

```js
// Правильная инициализация Canvas
function setupCanvas(canvas) {
  const dpr = window.devicePixelRatio ?? 1;
  const rect = canvas.getBoundingClientRect();
  
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;
  
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  return { ctx, width: rect.width, height: rect.height };
}

// Анимация Canvas
class CanvasRenderer {
  #canvas;
  #ctx;
  #rafId;
  #state;

  constructor(canvas, initialState) {
    this.#canvas = canvas;
    const { ctx, width, height } = setupCanvas(canvas);
    this.#ctx = ctx;
    this.#state = { ...initialState, width, height };
    
    // Перерисовка при изменении размеров
    new ResizeObserver(() => {
      const { ctx, width, height } = setupCanvas(canvas);
      this.#ctx = ctx;
      this.#state = { ...this.#state, width, height };
    }).observe(canvas);
  }

  start() {
    const tick = () => {
      this.#update();
      this.#draw();
      this.#rafId = requestAnimationFrame(tick);
    };
    this.#rafId = requestAnimationFrame(tick);
  }

  stop() { cancelAnimationFrame(this.#rafId); }

  #update() {
    // Обновить состояние (переопределить в подклассе)
  }

  #draw() {
    const { ctx, width, height } = this.#state;
    ctx.clearRect(0, 0, width, height);
    // Рисовать (переопределить в подклассе)
  }
}
```

---

## 22. Тестирование ванильного JS

### 22.1 Тестируемый код — архитектура

```js
// ✅ Разделяй бизнес-логику и DOM — бизнес-логика тестируется легко

// НЕТЕСТИРУЕМО — всё смешано
function handleCartAdd(productId) {
  const product = document.querySelector(`[data-id="${productId}"]`);
  const priceEl = product.querySelector('.price');
  const price = parseFloat(priceEl.textContent);
  const cartTotal = document.querySelector('#cart-total');
  cartTotal.textContent = parseFloat(cartTotal.textContent) + price;
  localStorage.setItem('cart', JSON.stringify({ total: ... }));
}

// ТЕСТИРУЕМО — чистая логика отдельно от DOM
export function calculateCartTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function addItemToCart(cart, item) {
  const existing = cart.find(i => i.id === item.id);
  if (existing) {
    return cart.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
  }
  return [...cart, { ...item, quantity: 1 }];
}

// DOM-логика использует чистые функции
function handleCartAdd(productId) {
  const product = getProductById(productId);
  state.update(s => { s.cart = addItemToCart(s.cart, product); });
  renderCart(store.state.cart);
}
```

### 22.2 Минимальный тест-раннер

```js
// Простейший assert без фреймворков
const test = (() => {
  const results = [];
  
  async function run(description, fn) {
    try {
      await fn();
      results.push({ pass: true, description });
      console.log(`✅ ${description}`);
    } catch (error) {
      results.push({ pass: false, description, error: error.message });
      console.error(`❌ ${description}: ${error.message}`);
    }
  }
  
  const assert = {
    equal: (a, b) => {
      if (a !== b) throw new Error(`Expected ${JSON.stringify(a)} to equal ${JSON.stringify(b)}`);
    },
    deepEqual: (a, b) => {
      if (JSON.stringify(a) !== JSON.stringify(b)) {
        throw new Error(`Expected ${JSON.stringify(a)} to deep equal ${JSON.stringify(b)}`);
      }
    },
    throws: (fn, expectedMsg) => {
      try { fn(); throw new Error('Expected to throw'); }
      catch (e) {
        if (expectedMsg && !e.message.includes(expectedMsg)) {
          throw new Error(`Expected message "${expectedMsg}", got "${e.message}"`);
        }
      }
    },
    truthy: (val) => { if (!val) throw new Error(`Expected truthy, got ${val}`); },
    falsy: (val) => { if (val) throw new Error(`Expected falsy, got ${val}`); },
  };
  
  const summary = () => {
    const pass = results.filter(r => r.pass).length;
    console.log(`\n${pass}/${results.length} tests passed`);
  };
  
  return { run, assert, summary };
})();

// Тесты
await test.run('addItemToCart adds new item', () => {
  const cart = [];
  const result = addItemToCart(cart, { id: 1, price: 100, name: 'Book' });
  test.assert.equal(result.length, 1);
  test.assert.equal(result[0].quantity, 1);
});

await test.run('addItemToCart increments existing item', () => {
  const cart = [{ id: 1, price: 100, name: 'Book', quantity: 1 }];
  const result = addItemToCart(cart, { id: 1, price: 100, name: 'Book' });
  test.assert.equal(result.length, 1);
  test.assert.equal(result[0].quantity, 2);
});

await test.run('calculateCartTotal sums correctly', () => {
  const cart = [
    { price: 100, quantity: 2 },
    { price: 50, quantity: 1 },
  ];
  test.assert.equal(calculateCartTotal(cart), 250);
});

test.summary();
```

---

## 23. Антипаттерны и ловушки

### 23.1 Управление памятью

```js
// ❌ Утечки памяти — классические случаи

// 1. Забытые event listeners
function setup(el) {
  el.addEventListener('click', heavyHandler);
  // el удалён из DOM, но listener держит ссылку → утечка!
}

// ✅ Убирать listeners при удалении
function setup(el) {
  const controller = new AbortController();
  el.addEventListener('click', heavyHandler, { signal: controller.signal });
  el.addEventListener('destroy', () => controller.abort(), { once: true });
}

// 2. Замыкания, удерживающие большие объекты
function createHandler(bigData) {
  // bigData не GC-ится пока handler жив
  return function() { console.log(bigData.length); };
}

// ✅ Взять только нужное
function createHandler(bigData) {
  const length = bigData.length; // только число
  bigData = null; // освободить ссылку (если не нужна)
  return function() { console.log(length); };
}

// 3. setTimeout/setInterval — никогда не чистятся
class Component {
  #intervalId;
  
  start() {
    this.#intervalId = setInterval(() => this.update(), 1000);
  }
  
  destroy() {
    clearInterval(this.#intervalId); // ОБЯЗАТЕЛЬНО!
  }
}

// 4. Observer-ы без disconnect
const observer = new IntersectionObserver(callback);
observer.observe(el);
// el удалён, observer продолжает работать
// ✅: observer.disconnect() в cleanup
```

### 23.2 Типичные JavaScript ошибки

```js
// ❌ this в колбэках
class Timer {
  count = 0;
  start() {
    setInterval(function() {
      this.count++; // this = undefined (strict) или window!
    }, 1000);
  }
}
// ✅ Arrow function или bind:
setInterval(() => this.count++, 1000);
setInterval(function() { this.count++; }.bind(this), 1000);

// ❌ Мутация аргументов функции
function sortUsers(users) {
  return users.sort((a, b) => a.name.localeCompare(b.name)); // мутирует оригинал!
}
// ✅
function sortUsers(users) {
  return [...users].sort((a, b) => a.name.localeCompare(b.name));
}

// ❌ for...in для массивов
const arr = [1, 2, 3];
for (const key in arr) { console.log(key); } // '0', '1', '2' — строки, не числа!
// И может включить ключи из прототипа!
// ✅ for...of
for (const value of arr) { console.log(value); } // 1, 2, 3

// ❌ Сравнение с NaN
NaN === NaN; // false!
// ✅
Number.isNaN(value);
Object.is(value, NaN);

// ❌ typeof null
typeof null === 'object'; // true — историческая ошибка
// ✅
value === null;

// ❌ Неправильный parseInt
parseInt('08'); // 0 в старых движках (octal)
// ✅ Всегда передавай radix
parseInt('08', 10); // 8
// Лучше:
Number('08'); // 8
+'08'; // 8

// ❌ delete из массива
const arr2 = [1, 2, 3];
delete arr2[1]; // [1, empty, 3] — разреженный массив!
// ✅
arr2.splice(1, 1); // [1, 3]

// ❌ Проверка пустого объекта
obj === {}; // false — разные ссылки!
// ✅
Object.keys(obj).length === 0;
JSON.stringify(obj) === '{}'; // не работает с Symbol ключами

// ❌ Array.prototype.sort без компаратора
[10, 9, 2, 1, 11].sort(); // [1, 10, 11, 2, 9] — лексикографически!
// ✅
[10, 9, 2, 1, 11].sort((a, b) => a - b); // [1, 2, 9, 10, 11]

// ❌ Потерянный await
async function bad() {
  const data = fetch('/api'); // забыл await!
  data.json(); // TypeError: data.json is not a function
}

// ❌ Race condition при параллельных запросах
let latestResult;
input.addEventListener('input', async (e) => {
  const result = await search(e.target.value);
  latestResult = result; // более ранний запрос может прийти позже!
  render(result);
});
// ✅ Отмена предыдущих запросов (AbortController паттерн)
```

### 23.3 Производительные антипаттерны

```js
// ❌ DOM-операции в цикле
for (let i = 0; i < 1000; i++) {
  document.body.innerHTML += '<div>' + i + '</div>'; // 1000 reflow!
}
// ✅ Fragment
const frag = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = i;
  frag.append(div);
}
document.body.append(frag);

// ❌ Чтение layout свойств в анимационном цикле
function animate() {
  element.style.left = element.offsetLeft + 1 + 'px'; // read → reflow → write → reflow
  requestAnimationFrame(animate);
}
// ✅ Отслеживать позицию в переменной
let x = element.offsetLeft;
function animate() {
  x += 1;
  element.style.transform = `translateX(${x}px)`;
  requestAnimationFrame(animate);
}

// ❌ Создание объектов в горячем пути
function update() {
  const pos = { x: mouse.x, y: mouse.y }; // объект каждый кадр → GC давление
  render(pos);
  requestAnimationFrame(update);
}
// ✅ Переиспользовать объект
const pos = { x: 0, y: 0 };
function update() {
  pos.x = mouse.x;
  pos.y = mouse.y;
  render(pos);
  requestAnimationFrame(update);
}

// ❌ Добавление inline-стилей когда лучше класс
el.style.display = 'flex';
el.style.alignItems = 'center';
el.style.justifyContent = 'center';
// ✅
el.classList.add('flex-center');
// CSS: .flex-center { display: flex; align-items: center; justify-content: center; }
```

### 23.4 Промис-антипаттерны

```js
// ❌ Promise hell — вернулись к callback hell
fetch(url).then(res => {
  res.json().then(data => {
    processData(data).then(result => {
      saveResult(result).then(() => {
        showSuccess();
      });
    });
  });
});
// ✅ Правильная цепочка или async/await
const result = await processData(await (await fetch(url)).json());
await saveResult(result);
showSuccess();

// ❌ Создание ненужного Promise-обёртки
// (Promise constructor anti-pattern)
function fetchUser(id) {
  return new Promise((resolve, reject) => {
    fetch(`/users/${id}`)
      .then(res => resolve(res.json()))
      .catch(reject);
  });
}
// ✅ Просто верни промис
function fetchUser(id) {
  return fetch(`/users/${id}`).then(res => res.json());
}

// ❌ Смешивание .then() и try/catch без понимания
async function bad() {
  try {
    const data = await fetch(url)
      .then(r => r.json())
      .catch(e => null); // подавляет ошибку!
    // data может быть null — не узнаем почему
  } catch (e) { }
}
```

---

## 24. Чеклист качества

### 24.1 Синтаксис и стиль

```
✅ Используется const по умолчанию, let при необходимости переназначения
✅ var не используется нигде
✅ Стрелочные функции в колбэках, обычные функции для методов
✅ Деструктуризация там, где повышает читаемость
✅ Optional chaining ?. для потенциально null/undefined значений
✅ Nullish coalescing ?? вместо || для нулевых значений
✅ Template literals вместо конкатенации строк
✅ Spread для слияния, rest для сбора аргументов
✅ async/await вместо .then() цепочек (обычно)
✅ Именованные параметры через объект для функций с 3+ параметрами
```

### 24.2 Безопасность

```
✅ textContent вместо innerHTML для пользовательских данных
✅ Все URL валидируются перед использованием в href/src
✅ Нет eval(), new Function(), setTimeout(string)
✅ Данные из localStorage/URL params санитизируются перед использованием
✅ CSRF токены в мутирующих запросах
✅ Нет секретов в клиентском коде (API keys, паролей)
```

### 24.3 Производительность

```
✅ Batch DOM-операции через DocumentFragment
✅ Анимации через requestAnimationFrame или CSS
✅ Тяжёлые вычисления в Web Worker
✅ Изображения с lazy loading (IntersectionObserver или loading="lazy")
✅ Event listeners с passive: true для scroll/touch
✅ Debounce/throttle для высокочастотных событий
✅ Нет принудительного reflow в анимационных циклах
✅ Виртуализация для длинных списков (>100 элементов)
```

### 24.4 Обработка ошибок

```
✅ Все async функции имеют try/catch или обрабатывают .catch()
✅ AbortController для отмены fetch-запросов
✅ Глобальный обработчик unhandledrejection
✅ Информативные сообщения об ошибках для пользователя
✅ Нет пустых catch блоков (catch(e) {})
✅ Кастомные Error классы для разных типов ошибок
```

### 24.5 Управление памятью

```
✅ Event listeners удаляются при уничтожении компонента
✅ setInterval/setTimeout очищаются в cleanup
✅ Observer-ы (Intersection, Mutation, Resize) disconnectятся
✅ AbortController используется для группового удаления listeners
✅ WeakMap/WeakRef для данных привязанных к объектам (не мешают GC)
```

### 24.6 Доступность (a11y)

```
✅ Интерактивные элементы — семантические теги (button, a, input)
✅ ARIA-атрибуты для динамических изменений (aria-live, aria-expanded)
✅ Управление фокусом в модалках и выпадающих меню
✅ Keyboard navigation для всех интерактивных элементов
✅ Динамические изменения контента объявляются через aria-live regions
```

### 24.7 Модульность и тестируемость

```
✅ Бизнес-логика отделена от DOM-манипуляций
✅ Функции чистые там, где возможно
✅ Зависимости инжектируются, не создаются внутри
✅ Модули экспортируют минимальный публичный API
✅ Большие функции разбиты на маленькие с одной ответственностью
```

---

## Быстрый справочник — современный синтаксис

```js
// ══════════════ ПЕРЕМЕННЫЕ ══════════════
const x = 1;          // иммутабельная ссылка (по умолчанию)
let y = 1;             // мутабельная ссылка
// var — никогда

// ══════════════ ДЕСТРУКТУРИЗАЦИЯ ══════════════
const { a, b: renamed, c = 'default' } = obj;
const [first, , third] = arr;
const { x: { y: deepY } = {} } = nested;

// ══════════════ СПРЕД/РЕСТ ══════════════
const merged  = { ...obj1, ...obj2 };
const arr2    = [...arr1, ...arr2];
const [h, ...tail] = arr;
const { a: _, ...rest } = obj;
function fn(x, ...args) {}

// ══════════════ OPTIONAL/NULLISH ══════════════
obj?.prop?.nested;     // безопасный доступ
obj?.[key];            // динамический ключ
fn?.();                // безопасный вызов
x ?? 'default';        // только null/undefined
x ??= 'value';         // присвоить если null/undefined
x ||= 'value';         // присвоить если falsy
x &&= transform(x);   // присвоить если truthy

// ══════════════ ФУНКЦИИ ══════════════
const fn = (x) => x * 2;                    // arrow
const fn2 = (x) => ({ wrapped: x });        // объект (скобки!)
async function load() { return await f(); }  // async
function* gen() { yield 1; yield 2; }       // generator

// ══════════════ КЛАССЫ ══════════════
class Foo extends Bar {
  #private = 0;
  static count = 0;
  get value() { return this.#private; }
  set value(v) { this.#private = v; }
  method() { super.method(); }
  static create() { return new Foo(); }
}

// ══════════════ ПРОМИСЫ ══════════════
await Promise.all([p1, p2]);         // все или ошибка
await Promise.allSettled([p1, p2]);  // все (с результатами)
await Promise.race([p1, p2]);        // первый
await Promise.any([p1, p2]);         // первый успешный

// ══════════════ МОДУЛИ ══════════════
export const x = 1;
export default class {};
import { x } from './mod.js';
import def, { x } from './mod.js';
const { default: mod } = await import('./mod.js');

// ══════════════ ИТЕРАЦИЯ ══════════════
for (const val of iterable) {}       // значения
for (const [i, v] of arr.entries()) {} // индекс + значение
for (const [k, v] of map) {}         // Map
for (const [k, v] of Object.entries(obj)) {} // объект

// ══════════════ СОВРЕМЕННЫЕ МЕТОДЫ ══════════════
arr.at(-1);             // последний элемент
arr.findLast(fn);       // поиск с конца
arr.toSorted(fn);       // sorted copy
arr.toReversed();       // reversed copy
arr.flatMap(fn);        // map + flat(1)
Object.hasOwn(obj, k);  // проверка собственного свойства
structuredClone(obj);   // глубокое клонирование
Object.groupBy(arr, fn); // группировка (ES2024)
```

---

---

## 25. Регулярные выражения — современный подход

### 25.1 Флаги и литералы

```js
// Флаги регулярных выражений
// g — глобальный поиск (все совпадения)
// i — без учёта регистра
// m — многострочный (^ и $ для каждой строки)
// s — dotAll (. совпадает с \n)
// u — Unicode режим (правильная работа с emoji)
// y — sticky (поиск только с lastIndex)
// d — индексы совпадений (ES2022)
// v — unicode sets (ES2024)

// Всегда используй флаг u для Unicode
const hasEmoji = /\p{Emoji}/u.test(str);

// Именованные группы захвата (ES2018)
const dateRe = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const match = '2025-01-15'.match(dateRe);
match?.groups?.year;  // '2025'
match?.groups?.month; // '01'
match?.groups?.day;   // '15'

// Обратная ссылка на именованную группу
const dupWord = /\b(?<word>\w+)\s+\k<word>\b/i;
dupWord.test('the the test'); // true
```

### 25.2 Современные методы

```js
// String.prototype.matchAll — все совпадения с группами (флаг g обязателен)
const text = 'color: red; background: blue; border: green';
const propRe = /(?<prop>[\w-]+):\s*(?<value>\w+)/g;

for (const match of text.matchAll(propRe)) {
  console.log(match.groups); // { prop: 'color', value: 'red' }, ...
}

// В массив
const props = [...text.matchAll(propRe)]
  .map(m => [m.groups.prop, m.groups.value]);

// replace с именованными группами
const swapped = '2025-01-15'.replace(
  /(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/,
  '$<d>.$<m>.$<y>' // 15.01.2025
);
```

### 25.3 Lookahead и Lookbehind

```js
// Lookahead — совпадение если за ним следует...
/\d+(?= рублей)/.exec('100 рублей'); // '100'
/\d+(?! рублей)/.exec('100 долларов'); // '100' (отрицательный)

// Lookbehind (ES2018) — совпадение если перед ним...
/(?<=\$)\d+/.exec('$100'); // '100'
/(?<!\$)\d+/.exec('€100'); // '100' (отрицательный)

// Практически — замена паролей в логах
const safeLog = (str) =>
  str.replace(/(?<="password"\s*:\s*")[^"]+(?=")/g, '***');

safeLog('{"password": "secret123"}'); // '{"password": "***"}'
```

### 25.4 Утилиты

```js
// Экранирование спецсимволов (для динамических паттернов)
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Динамический поиск с подсветкой
function highlight(text, searchTerm) {
  const re = new RegExp(`(${escapeRegex(searchTerm)})`, 'gi');
  return text.replace(re, '<mark>$1</mark>');
}

// Готовые валидаторы
const validators = {
  email:    /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/,
  hexColor: /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/,
  slug:     /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  uuid:     /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
  ipv4:     /^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$/,
};

const validate = (type, value) => validators[type]?.test(value) ?? false;
```

---

## 26. Intl API — интернационализация

### 26.1 Числа и валюта

```js
// Валюта по локали
new Intl.NumberFormat('ru-RU', {
  style: 'currency', currency: 'RUB', minimumFractionDigits: 0,
}).format(1234567.89); // '1 234 568 ₽'

// Компактный формат
new Intl.NumberFormat('ru-RU', {
  notation: 'compact', compactDisplay: 'short',
}).format(1_500_000); // '1,5 млн'

// Единицы измерения
new Intl.NumberFormat('ru-RU', {
  style: 'unit', unit: 'kilometer-per-hour',
}).format(120); // '120 км/ч'

// Диапазон
new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' })
  .formatRange(100, 200); // '100 – 200 ₽'
```

### 26.2 Даты и относительное время

```js
// Форматирование даты
new Intl.DateTimeFormat('ru-RU', {
  year: 'numeric', month: 'long', day: 'numeric',
  hour: '2-digit', minute: '2-digit',
  timeZone: 'Europe/Kiev',
}).format(new Date()); // '15 января 2025 г., 14:30'

// Относительное время (ES2020)
const rtf = new Intl.RelativeTimeFormat('ru-RU', { numeric: 'auto' });
rtf.format(-1, 'day');   // 'вчера'
rtf.format(-3, 'hour');  // '3 часа назад'
rtf.format(2, 'week');   // 'через 2 недели'

// Авто-выбор единицы
function timeAgo(date) {
  const diffSec = Math.round((Date.now() - new Date(date)) / 1000);
  const rtf = new Intl.RelativeTimeFormat('ru-RU', { numeric: 'auto' });

  const thresholds = [
    [60,          -diffSec,                              'second'],
    [3600,        -Math.round(diffSec / 60),             'minute'],
    [86400,       -Math.round(diffSec / 3600),           'hour'],
    [86400 * 30,  -Math.round(diffSec / 86400),          'day'],
    [86400 * 365, -Math.round(diffSec / (86400 * 30)),   'month'],
    [Infinity,    -Math.round(diffSec / (86400 * 365)),  'year'],
  ];

  for (const [threshold, value, unit] of thresholds) {
    if (Math.abs(diffSec) < threshold) return rtf.format(value, unit);
  }
}

// Список
new Intl.ListFormat('ru-RU', { type: 'conjunction' })
  .format(['яблоки', 'груши', 'вишни']); // 'яблоки, груши и вишни'

// Сортировка по локали
const coll = new Intl.Collator('ru-RU', { sensitivity: 'base' });
['яблоко', 'Апельсин', 'абрикос'].sort(coll.compare);
```

---

## 27. Service Workers и PWA

### 27.1 Регистрация

```js
async function registerSW() {
  if (!('serviceWorker' in navigator)) return;

  const registration = await navigator.serviceWorker.register('/sw.js', {
    scope: '/',
    updateViaCache: 'none',
  });

  registration.addEventListener('updatefound', () => {
    const newWorker = registration.installing;
    newWorker.addEventListener('statechange', () => {
      if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
        showUpdateBanner(() => newWorker.postMessage({ type: 'SKIP_WAITING' }));
      }
    });
  });

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    window.location.reload();
  });
}
```

### 27.2 Стратегии кэширования (sw.js)

```js
const STATIC = 'static-v1';
const DYNAMIC = 'dynamic-v1';
const PRECACHE = ['/', '/index.html', '/app.js', '/styles.css', '/offline.html'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(STATIC).then(c => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== STATIC && k !== DYNAMIC).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Cache First — статика (JS, CSS, шрифты)
async function cacheFirst(req) {
  const cached = await caches.match(req);
  if (cached) return cached;
  const res = await fetch(req);
  if (res.ok) (await caches.open(STATIC)).put(req, res.clone());
  return res;
}

// Network First — API, HTML
async function networkFirst(req) {
  try {
    const res = await fetch(req);
    if (res.ok) (await caches.open(DYNAMIC)).put(req, res.clone());
    return res;
  } catch {
    return (await caches.match(req)) ?? caches.match('/offline.html');
  }
}

// Stale While Revalidate — баланс скорость/свежесть
async function staleWhileRevalidate(req) {
  const cache = await caches.open(DYNAMIC);
  const cached = await cache.match(req);
  const fetchPromise = fetch(req).then(res => { if (res.ok) cache.put(req, res.clone()); return res; });
  return cached ?? fetchPromise;
}

self.addEventListener('fetch', (e) => {
  const { request } = e;
  const url = new URL(request.url);

  if (url.pathname.startsWith('/api/'))      return e.respondWith(networkFirst(request));
  if (/\.(js|css|woff2?|png|svg)$/.test(url.pathname)) return e.respondWith(cacheFirst(request));
  if (request.mode === 'navigate')           return e.respondWith(staleWhileRevalidate(request));
});
```

---

## 28. WebSocket — надёжный клиент

```js
class ReconnectingWS extends EventTarget {
  #url; #ws = null;
  #delay = 1000; #maxDelay = 30_000;
  #attempts = 0; #manual = false;
  #pending = []; #ping = null;

  constructor(url) { super(); this.#url = url; }

  connect() { this.#manual = false; this.#open(); return this; }

  #open() {
    this.#ws = new WebSocket(this.#url);
    this.#ws.onopen = () => {
      this.#attempts = 0; this.#delay = 1000;
      this.dispatchEvent(new Event('connected'));
      this.#pending.forEach(m => this.#ws.send(m));
      this.#pending = [];
      this.#ping = setInterval(() => {
        if (this.#ws?.readyState === WebSocket.OPEN) this.send({ type: 'ping' });
      }, 25_000);
    };
    this.#ws.onmessage = ({ data }) => {
      try {
        const parsed = JSON.parse(data);
        if (parsed.type !== 'pong') this.dispatchEvent(new CustomEvent('message', { detail: parsed }));
      } catch {
        this.dispatchEvent(new CustomEvent('message', { detail: data }));
      }
    };
    this.#ws.onclose = (e) => {
      clearInterval(this.#ping);
      this.dispatchEvent(new CustomEvent('disconnected', { detail: { code: e.code } }));
      if (!this.#manual && e.code !== 1000) this.#reconnect();
    };
  }

  #reconnect() {
    const delay = Math.min(this.#delay * 2 ** this.#attempts++, this.#maxDelay) + Math.random() * 500;
    setTimeout(() => this.#open(), delay);
  }

  send(data) {
    const msg = typeof data === 'string' ? data : JSON.stringify(data);
    this.#ws?.readyState === WebSocket.OPEN ? this.#ws.send(msg) : this.#pending.push(msg);
    return this;
  }

  close() { this.#manual = true; clearInterval(this.#ping); this.#ws?.close(1000); }
}

// Использование
const ws = new ReconnectingWS('wss://api.example.com/ws');
ws.addEventListener('connected', () => ws.send({ type: 'subscribe', channel: 'live' }));
ws.addEventListener('message', ({ detail }) => handleMessage(detail));
ws.connect();
```

---

## 29. File API

### 29.1 Чтение файлов

```js
// Современное открытие файла
async function openFile(accept = []) {
  if ('showOpenFilePicker' in window) {
    try {
      const [handle] = await showOpenFilePicker({ types: accept, multiple: false });
      return handle.getFile();
    } catch (e) { if (e.name !== 'AbortError') throw e; return null; }
  }
  // Fallback через <input>
  return new Promise(resolve => {
    const input = Object.assign(document.createElement('input'), { type: 'file' });
    input.addEventListener('change', () => resolve(input.files[0] ?? null), { once: true });
    input.click();
  });
}

// Чтение содержимого (современные Blob методы)
async function readFileContent(file) {
  return {
    text: await file.text(),                           // UTF-8 строка
    buffer: await file.arrayBuffer(),                  // бинарные данные
    url: URL.createObjectURL(file),                    // временный URL (нужно revokeObjectURL!)
    hash: await sha256(await file.arrayBuffer()),      // SHA-256 хэш
  };
}

// Drag & Drop
function setupDropZone(el, onFiles) {
  el.addEventListener('dragover', e => { e.preventDefault(); el.classList.add('over'); });
  el.addEventListener('dragleave', e => { if (!el.contains(e.relatedTarget)) el.classList.remove('over'); });
  el.addEventListener('drop', e => {
    e.preventDefault();
    el.classList.remove('over');
    const files = [...(e.dataTransfer.files ?? [])];
    if (files.length) onFiles(files);
  });
}
```

### 29.2 Сохранение файлов

```js
async function saveFile(content, filename, mimeType = 'text/plain') {
  if ('showSaveFilePicker' in window) {
    try {
      const handle = await showSaveFilePicker({ suggestedName: filename });
      const writable = await handle.createWritable();
      await writable.write(content);
      await writable.close();
      return;
    } catch (e) { if (e.name === 'AbortError') return; }
  }
  // Fallback
  const blob = content instanceof Blob ? content : new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  Object.assign(document.createElement('a'), { href: url, download: filename }).click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// Примеры
await saveFile(JSON.stringify(data, null, 2), 'export.json', 'application/json');
await saveFile(csvText, 'report.csv', 'text/csv');
```

---

## 30. Продвинутая валидация форм

```js
class FormValidator {
  #form; #rules; #errors = new Map();

  constructor(form, rules) { this.#form = form; this.#rules = rules; }

  static R = {
    required:  v => (v !== '' && v != null) || 'Поле обязательно',
    minLength: n => v => v.length >= n || `Минимум ${n} символов`,
    maxLength: n => v => v.length <= n || `Максимум ${n} символов`,
    min:       n => v => Number(v) >= n || `Не менее ${n}`,
    max:       n => v => Number(v) <= n || `Не более ${n}`,
    pattern:   (re, msg) => v => re.test(v) || msg,
    email:     v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Неверный email',
    match:     field => (v, data) => v === data[field] || 'Поля не совпадают',
  };

  #check(name, value, all) {
    for (const rule of this.#rules[name] ?? []) {
      const r = typeof rule === 'function' ? rule(value, all) : rule;
      if (r !== true && r) return r;
    }
    return null;
  }

  validate() {
    const data = Object.fromEntries(new FormData(this.#form));
    this.#errors.clear();
    for (const name of Object.keys(this.#rules)) {
      const err = this.#check(name, data[name] ?? '', data);
      if (err) this.#errors.set(name, err);
    }
    this.#render();
    return { valid: this.#errors.size === 0, data, errors: Object.fromEntries(this.#errors) };
  }

  watch() {
    const data = () => Object.fromEntries(new FormData(this.#form));
    this.#form.querySelectorAll('[name]').forEach(field => {
      field.addEventListener('blur', () => {
        const err = this.#check(field.name, field.value, data());
        err ? this.#errors.set(field.name, err) : this.#errors.delete(field.name);
        this.#renderField(field, err);
      });
      field.addEventListener('input', () => {
        if (this.#errors.has(field.name)) {
          this.#errors.delete(field.name);
          this.#renderField(field, null);
        }
      });
    });
    return this;
  }

  #render() {
    this.#form.querySelectorAll('[name]').forEach(f =>
      this.#renderField(f, this.#errors.get(f.name) ?? null)
    );
  }

  #renderField(field, error) {
    field.classList.toggle('invalid', !!error);
    field.setAttribute('aria-invalid', String(!!error));
    let el = this.#form.querySelector(`[data-error="${field.name}"]`);
    if (!el) {
      el = Object.assign(document.createElement('span'), {
        className: 'field-error', role: 'alert',
      });
      el.dataset.error = field.name;
      field.after(el);
    }
    el.textContent = error ?? '';
    el.hidden = !error;
  }
}

// Использование
const { R } = FormValidator;
const v = new FormValidator(form, {
  name:     [R.required, R.minLength(2)],
  email:    [R.required, R.email],
  password: [R.required, R.minLength(8), R.pattern(/[A-Z]/, 'Нужна заглавная')],
  confirm:  [R.required, R.match('password')],
}).watch();

form.addEventListener('submit', e => {
  e.preventDefault();
  const { valid, data } = v.validate();
  if (valid) submit(data);
});
```

---

## 31. JSDoc — типизация без TypeScript

```js
// @ts-check — включить проверку типов в файле

/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} name
 * @property {string} email
 * @property {'admin'|'user'|'guest'} role
 * @property {Date} [createdAt]
 */

/**
 * @template T
 * @typedef {Object} ApiResponse
 * @property {T} data
 * @property {number} status
 * @property {string} [error]
 */

/**
 * Загрузить пользователя
 * @param {number} id
 * @param {{ timeout?: number, signal?: AbortSignal }} [options]
 * @returns {Promise<ApiResponse<User>>}
 * @throws {HttpError}
 */
async function loadUser(id, options = {}) { /* ... */ }

/**
 * @template T
 * @param {T[]} arr
 * @param {(item: T) => boolean} predicate
 * @returns {T[]}
 */
const filter = (arr, predicate) => arr.filter(predicate);

// Утверждение типа
const input = /** @type {HTMLInputElement} */ (document.querySelector('input[name="email"]'));
input.value; // VS Code знает тип!

// Enum
/** @enum {string} */
const Status = Object.freeze({ PENDING: 'pending', ACTIVE: 'active', DONE: 'done' });

// Generic createElement с типами
/**
 * @template {keyof HTMLElementTagNameMap} K
 * @param {K} tag
 * @param {Partial<HTMLElementTagNameMap[K]>} [props]
 * @returns {HTMLElementTagNameMap[K]}
 */
function el(tag, props = {}) {
  return Object.assign(document.createElement(tag), props);
}

const btn = el('button', { textContent: 'OK', disabled: false }); // → HTMLButtonElement
```

---

## 32. Конечный автомат (FSM)

```js
class StateMachine {
  #state; #transitions; #actions; #listeners = new Set();

  constructor({ initial, transitions, actions = {} }) {
    this.#state = initial;
    this.#transitions = transitions;
    this.#actions = actions;
  }

  get state() { return this.#state; }
  get can()   { return (event) => !!(this.#transitions[this.#state]?.[event]); }

  send(event, payload) {
    const next = this.#transitions[this.#state]?.[event];
    if (!next) { console.warn(`Invalid: ${this.#state} + ${event}`); return false; }

    const prev = this.#state;
    this.#state = typeof next === 'function' ? next(this.#state, payload) : next;

    this.#actions[`${prev}:exit`]?.(payload);
    this.#actions[`${this.#state}:enter`]?.(payload);
    this.#actions[event]?.(payload);
    this.#listeners.forEach(fn => fn({ from: prev, to: this.#state, event, payload }));
    return true;
  }

  subscribe(fn) { this.#listeners.add(fn); return () => this.#listeners.delete(fn); }
}

// Машина для загрузки данных
const loader = new StateMachine({
  initial: 'idle',
  transitions: {
    idle:    { FETCH: 'loading' },
    loading: { SUCCESS: 'success', ERROR: 'error', CANCEL: 'idle' },
    success: { FETCH: 'loading', RESET: 'idle' },
    error:   { RETRY: 'loading', RESET: 'idle' },
  },
  actions: {
    'loading:enter': () => showSpinner(),
    'loading:exit':  () => hideSpinner(),
    SUCCESS: ({ data }) => render(data),
    'error:enter': ({ error }) => showError(error),
  },
});

async function load(url) {
  loader.send('FETCH');
  try {
    loader.send('SUCCESS', { data: await api.get(url) });
  } catch (e) {
    loader.send('ERROR', { error: e.message });
  }
}
```

---

## 33. Оптимистичные обновления

```js
// UI меняется до ответа сервера, откат при ошибке
class OptimisticStore {
  #state; #listeners = new Set(); #pending = new Map();

  constructor(state) { this.#state = state; }

  async optimistic(opId, applyFn, serverFn) {
    const snapshot = structuredClone(this.#state);
    applyFn(this.#state);
    this.#emit();

    this.#pending.set(opId, snapshot);
    try {
      const result = await serverFn();
      this.#pending.delete(opId);
      return result;
    } catch (err) {
      // Откат состояния
      Object.assign(this.#state, this.#pending.get(opId));
      this.#pending.delete(opId);
      this.#emit();
      throw err;
    }
  }

  subscribe(fn) { this.#listeners.add(fn); return () => this.#listeners.delete(fn); }
  #emit() { this.#listeners.forEach(fn => fn(this.#state)); }
  get state() { return this.#state; }
}

// Использование — лайк поста
const store = new OptimisticStore({ posts: [] });

async function likePost(id) {
  await store.optimistic(
    `like-${id}`,
    state => {
      const post = state.posts.find(p => p.id === id);
      if (post) { post.liked = !post.liked; post.likes += post.liked ? 1 : -1; }
    },
    () => api.post(`/posts/${id}/like`)
  );
}
```

---

## 34. Crypto API

```js
// Криптографически безопасный UUID
const uuid = crypto.randomUUID(); // ES2021

// SHA-256 хэш строки
async function sha256(message) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(message));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

// AES-GCM шифрование/дешифрование
const Crypto = {
  async generateKey() {
    return crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);
  },

  async encrypt(data, key) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const enc = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key,
      new TextEncoder().encode(JSON.stringify(data)));
    const result = new Uint8Array(12 + enc.byteLength);
    result.set(iv);
    result.set(new Uint8Array(enc), 12);
    return btoa(String.fromCharCode(...result));
  },

  async decrypt(ciphertext, key) {
    const data = Uint8Array.from(atob(ciphertext), c => c.charCodeAt(0));
    const dec = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: data.slice(0, 12) }, key, data.slice(12));
    return JSON.parse(new TextDecoder().decode(dec));
  },

  // Ключ из пароля (PBKDF2)
  async deriveKey(password, salt = crypto.getRandomValues(new Uint8Array(16))) {
    const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt, iterations: 100_000, hash: 'SHA-256' },
      base, { name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']
    );
    return { key, salt };
  },
};
```

---

## 35. Доступность (a11y) из JS

### 35.1 Управление фокусом

```js
const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),' +
  'select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

class FocusTrap {
  #el; #prev; #ctrl;

  constructor(el) { this.#el = el; }

  activate() {
    this.#prev = document.activeElement;
    this.#ctrl = new AbortController();
    document.addEventListener('keydown', this.#trap.bind(this), { signal: this.#ctrl.signal });
    (this.#focusable()[0] ?? this.#el).focus();
    return this;
  }

  deactivate() { this.#ctrl?.abort(); this.#prev?.focus(); return this; }

  #focusable() {
    return [...this.#el.querySelectorAll(FOCUSABLE)].filter(el => !el.closest('[hidden],[inert]'));
  }

  #trap(e) {
    if (e.key !== 'Tab') return;
    const els = this.#focusable();
    if (!els.length) { e.preventDefault(); return; }
    const first = els[0], last = els.at(-1), active = document.activeElement;

    if (e.shiftKey && (active === first || !this.#el.contains(active))) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && (active === last || !this.#el.contains(active))) {
      e.preventDefault(); first.focus();
    }
  }
}

// Объявления для screen reader
class Announcer {
  #polite; #assertive;
  constructor() {
    this.#polite    = this.#mk('polite');
    this.#assertive = this.#mk('assertive');
    document.body.append(this.#polite, this.#assertive);
  }
  #mk(mode) {
    const el = document.createElement('div');
    el.setAttribute('aria-live', mode);
    el.setAttribute('aria-atomic', 'true');
    el.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
    return el;
  }
  polite(msg)    { this.#polite.textContent = ''; requestAnimationFrame(() => this.#polite.textContent = msg); }
  assertive(msg) { this.#assertive.textContent = ''; requestAnimationFrame(() => this.#assertive.textContent = msg); }
}

export const announcer = new Announcer();
```

---

## 36. Геолокация и Device APIs

```js
// Геолокация
const GeoService = {
  async getPosition(opts = {}) {
    if (!navigator.geolocation) throw new Error('Геолокация не поддерживается');
    return new Promise((res, rej) => navigator.geolocation.getCurrentPosition(
      p => res({ lat: p.coords.latitude, lng: p.coords.longitude, accuracy: p.coords.accuracy }),
      e => rej(new Error(['', 'Запрещено', 'Недоступно', 'Таймаут'][e.code])),
      { enableHighAccuracy: false, timeout: 10_000, maximumAge: 60_000, ...opts }
    ));
  },

  // Расстояние в метрах (гаверсинус)
  distance({ lat: a, lng: b }, { lat: c, lng: d }) {
    const R = 6371e3, toRad = x => x * Math.PI / 180;
    const dLat = toRad(c - a), dLon = toRad(d - b);
    const h = Math.sin(dLat/2)**2 + Math.cos(toRad(a)) * Math.cos(toRad(c)) * Math.sin(dLon/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1-h));
  },
};

// Network info
const conn = navigator.connection ?? navigator.mozConnection ?? navigator.webkitConnection;
conn?.addEventListener('change', () => console.log(conn.effectiveType, conn.downlink + 'Mbps'));

// Online/Offline
window.addEventListener('online',  () => syncData());
window.addEventListener('offline', () => showOfflineBanner());

// Page Visibility
document.addEventListener('visibilitychange', () => {
  document.hidden ? pausePolling() : resumePolling();
});
```

---

## 37. Профилирование производительности

```js
// Core Web Vitals
class WebVitals {
  static measure() {
    const v = {};

    new PerformanceObserver(l => { v.lcp = l.getEntries().at(-1).startTime; })
      .observe({ type: 'largest-contentful-paint', buffered: true });

    let cls = 0;
    new PerformanceObserver(l => { l.getEntries().forEach(e => { if (!e.hadRecentInput) cls += e.value; }); v.cls = cls; })
      .observe({ type: 'layout-shift', buffered: true });

    new PerformanceObserver(l => { l.getEntries().forEach(e => { v.inp = Math.max(v.inp ?? 0, e.duration); }); })
      .observe({ type: 'event', durationThreshold: 40, buffered: true });

    const nav = performance.getEntriesByType('navigation')[0];
    v.ttfb = nav?.responseStart ?? 0;
    return v;
  }

  static rate(metric, value) {
    const good = { lcp: 2500, cls: 0.1, inp: 200, ttfb: 800 };
    const poor = { lcp: 4000, cls: 0.25, inp: 500, ttfb: 1800 };
    return value <= (good[metric] ?? 0) ? 'good' : value <= (poor[metric] ?? 0) ? 'needs-improvement' : 'poor';
  }
}

// Разбивка долгих задач (Task splitting)
async function processChunked(items, fn, chunkSize = 100) {
  for (let i = 0; i < items.length; i += chunkSize) {
    items.slice(i, i + chunkSize).forEach(fn);
    await new Promise(r => setTimeout(r, 0)); // yield to browser
  }
}

// scheduler.yield (новый API)
async function yieldToMain() {
  if ('scheduler' in window && scheduler.yield) return scheduler.yield();
  return new Promise(r => setTimeout(r, 0));
}

// Long Task monitoring
new PerformanceObserver(l => {
  l.getEntries().forEach(e => {
    if (e.duration > 50) console.warn(`Long task ${e.duration.toFixed(0)}ms`);
  });
}).observe({ type: 'longtask' });
```

---

## 38. Streams API

```js
// Кастомный ReadableStream
const countdownStream = (from) => new ReadableStream({
  start(ctrl) {
    let n = from;
    const id = setInterval(() => n > 0 ? ctrl.enqueue(n--) : (ctrl.close(), clearInterval(id)), 1000);
  },
});

// Чтение с for-await
for await (const val of countdownStream(5)) console.log(val);

// Fetch + TextDecoder + TransformStream (NDJSON)
async function* streamJSON(url) {
  const response = await fetch(url);
  const reader = response.body
    .pipeThrough(new TextDecoderStream())
    .getReader();

  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += value;
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines.filter(Boolean)) {
      try { yield JSON.parse(line); } catch { /* skip */ }
    }
  }
}

// Загрузка с прогрессом
async function fetchWithProgress(url, onProgress) {
  const res = await fetch(url);
  const total = Number(res.headers.get('Content-Length') ?? 0);
  let loaded = 0;

  const body = res.body.pipeThrough(new TransformStream({
    transform(chunk, ctrl) {
      loaded += chunk.length;
      onProgress({ loaded, total, percent: total ? loaded / total : 0 });
      ctrl.enqueue(chunk);
    },
  }));
  return new Response(body, res);
}
```

---

## 39. Полная SPA архитектура

### 39.1 Структура

```
src/
├── main.js               ← bootstrap
├── router.js             ← клиентский роутинг
├── store/index.js        ← глобальное состояние
├── services/
│   ├── api.js            ← HTTP клиент
│   └── auth.service.js
├── components/
│   ├── ui/               ← переиспользуемые
│   └── pages/            ← страницы (lazy-loaded)
└── utils/
    ├── dom.js
    └── format.js
```

### 39.2 Bootstrap

```js
// main.js
import { router } from './router.js';
import { store } from './store/index.js';
import { AuthService } from './services/auth.service.js';

async function bootstrap() {
  try {
    await AuthService.init(); // Восстановить сессию

    router
      .route('/',        () => import('./components/pages/HomePage.js').then(m => m.default))
      .route('/users',   () => import('./components/pages/UsersPage.js').then(m => m.default))
      .route('/users/:id', () => import('./components/pages/UserPage.js').then(m => m.default))
      .notFound(         () => import('./components/pages/NotFoundPage.js').then(m => m.default))
      .guard(path => {
        if (!store.state.user && path !== '/login') {
          router.navigate('/login', {}, { replace: true });
          return false;
        }
        return true;
      })
      .start();

    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(console.warn);
    }
  } catch (e) {
    document.getElementById('app').innerHTML =
      `<div class="fatal-error"><h1>Ошибка запуска</h1><p>${escapeHtml(e.message)}</p>
       <button onclick="location.reload()">Перезагрузить</button></div>`;
  }
}

bootstrap();
```

### 39.3 Lazy page loader с skeleton

```js
class PageLoader {
  #container; #current = null; #ctrl = null;

  constructor(container) { this.#container = container; }

  async load(pageFactory) {
    this.#ctrl?.abort();
    this.#ctrl = new AbortController();
    const { signal } = this.#ctrl;

    this.#skeleton();

    try {
      const PageClass = await pageFactory();
      if (signal.aborted) return;

      this.#current?.destroy?.();
      await new Promise(r => setTimeout(r, 100)); // минимальное время скелетона
      if (signal.aborted) return;

      this.#container.innerHTML = '';
      this.#current = new PageClass();
      this.#current.mount(this.#container);
    } catch (e) {
      if (e.name === 'AbortError') return;
      this.#container.innerHTML =
        `<div class="page-error" role="alert">
           <h2>Ошибка загрузки</h2>
           <p>${escapeHtml(e.message)}</p>
           <button onclick="history.back()">Назад</button>
         </div>`;
    }
  }

  #skeleton() {
    this.#container.innerHTML =
      `<div class="skeleton-page" aria-busy="true">
         <div class="skeleton skeleton--title"></div>
         <div class="skeleton skeleton--text"></div>
         <div class="skeleton skeleton--block"></div>
       </div>`;
  }
}
```

---

## Алфавитный справочник методов

| Метод | Категория | Описание |
|-------|-----------|----------|
| `arr.at(-1)` | Array | Элемент с конца |
| `arr.findLast(fn)` | Array | Поиск с конца |
| `arr.flat(n)` | Array | Уплощение вложенности |
| `arr.flatMap(fn)` | Array | map + flat(1) |
| `arr.toSorted(fn)` | Array ES2023 | Sorted копия |
| `arr.toReversed()` | Array ES2023 | Reversed копия |
| `arr.toSpliced(i,n)` | Array ES2023 | Spliced копия |
| `arr.with(i, v)` | Array ES2023 | Замена по индексу, копия |
| `Array.from(it, fn)` | Array | Из итерируемого |
| `Object.hasOwn(o, k)` | Object ES2022 | Собственное свойство |
| `Object.fromEntries(it)` | Object | Из пар |
| `Object.groupBy(arr, fn)` | Object ES2024 | Группировка |
| `structuredClone(v)` | Global ES2022 | Глубокое клонирование |
| `str.at(-1)` | String | Символ с конца |
| `str.replaceAll(s, r)` | String | Замена всех |
| `str.matchAll(re)` | String | Все совпадения+группы |
| `str.trimStart/End()` | String | Обрезка с одной стороны |
| `Promise.allSettled()` | Promise | Все, не падает |
| `Promise.any()` | Promise ES2021 | Первый успешный |
| `AbortSignal.timeout(ms)` | AbortSignal ES2022 | Таймаут |
| `AbortSignal.any([...])` | AbortSignal ES2024 | От любого |
| `crypto.randomUUID()` | Crypto ES2021 | UUID v4 |
| `el.closest(sel)` | DOM | Ближайший предок |
| `el.matches(sel)` | DOM | Соответствие селектору |
| `el.replaceWith(new)` | DOM | Замена |
| `el.before/after(...)` | DOM | Вставка рядом |
| `el.append(...)` | DOM | Добавить в конец |
| `el.prepend(...)` | DOM | Добавить в начало |

---

## Версии стандартов

| Стандарт | Год | Ключевые возможности |
|----------|-----|----------------------|
| ES2015 (ES6) | 2015 | `let/const`, классы, промисы, модули, деструктуризация, Symbol, Map/Set, генераторы, `for...of`, стрелочные функции |
| ES2016 | 2016 | `Array.includes`, `**` (степень) |
| ES2017 | 2017 | `async/await`, `Object.entries/values`, `padStart/End`, SharedArrayBuffer |
| ES2018 | 2018 | `Promise.finally`, rest/spread объекты, именованные regex-группы, `for await...of`, Async iteration |
| ES2019 | 2019 | `Array.flat/flatMap`, `Object.fromEntries`, `trimStart/End`, необязательный `catch(e)` |
| ES2020 | 2020 | `BigInt`, `?.`, `??`, `Promise.allSettled`, `globalThis`, динамический `import()`, `String.matchAll` |
| ES2021 | 2021 | `Promise.any`, `String.replaceAll`, `&&= \|\|= ??=`, `WeakRef`, `crypto.randomUUID` |
| ES2022 | 2022 | Приватные поля `#`, `Object.hasOwn`, `.at()`, `structuredClone`, `Error.cause`, top-level await |
| ES2023 | 2023 | `findLast/findLastIndex`, `toSorted/toReversed/toSpliced/with`, Hashbang grammar |
| ES2024 | 2024 | `Object.groupBy`, `Promise.withResolvers`, Set-операции `union/intersection/difference`, `ArrayBuffer.resize` |
| ES2025 | 2025 | Iterator helpers, `import attributes`, RegExp `/v` flag, `Float16Array` |

---

*Руководство охватывает ES2015–ES2025. Проверяй поддержку на* [caniuse.com](https://caniuse.com) *и* [MDN Web Docs](https://developer.mozilla.org).  
*39 основных разделов | ~7500+ строк кода и примеров | 2025*
