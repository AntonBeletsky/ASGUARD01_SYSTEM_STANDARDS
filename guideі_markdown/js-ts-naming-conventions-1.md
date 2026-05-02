# JavaScript & TypeScript Naming Conventions — The Complete Guide

> Covers ECMAScript / TypeScript best practices, based on Airbnb Style Guide, Google JS Guide, TypeScript Handbook, and community standards.
> **Aligned with the Containerization Standard v11: Law Zero (data attributes only for JS), flat kebab-case HTML/CSS, no BEM.**

---

## Table of Contents

1. [General Principles](#1-general-principles)
2. [Variables](#2-variables)
3. [Constants](#3-constants)
4. [Functions](#4-functions)
5. [Classes](#5-classes)
6. [Interfaces & Types (TypeScript)](#6-interfaces--types-typescript)
7. [Enums (TypeScript)](#7-enums-typescript)
8. [Generics (TypeScript)](#8-generics-typescript)
9. [Methods](#9-methods)
10. [Properties & Fields](#10-properties--fields)
11. [Private Members & Widget Controller Conventions](#11-private-members--widget-controller-conventions)
12. [Parameters](#12-parameters)
13. [Namespaces & Modules](#13-namespaces--modules)
14. [Files & Directories](#14-files--directories)
15. [React & JSX / TSX Conventions](#15-react--jsx--tsx-conventions)
16. [Event Handlers](#16-event-handlers)
17. [Boolean Variables](#17-boolean-variables)
18. [Async / Promise Naming](#18-async--promise-naming)
19. [Type Assertions & Type Guards](#19-type-assertions--type-guards)
20. [Decorators](#20-decorators)
21. [Test Files & Test Identifiers](#21-test-files--test-identifiers)
22. [Abbreviations & Acronyms](#22-abbreviations--acronyms)
23. [DOM Interaction Conventions](#23-dom-interaction-conventions)
24. [Naming Anti-patterns](#24-naming-anti-patterns)
25. [Quick Reference Cheatsheet](#25-quick-reference-cheatsheet)
26. [References & Further Reading](#26-references--further-reading)

---

## 1. General Principles

- **Be descriptive, not terse.** `userAccountList` beats `ul` or `data`.
- **Be consistent.** Pick one convention per construct and never mix.
- **Avoid abbreviations** unless they are universally known (`url`, `id`, `http`, `api`). Inside widget code, never abbreviate class names, `data-ref` values, `data-action` values, or token names — `orders-item` not `ord-item`, `this._itemsList` not `this._il`.
- **Pronounceable names.** If you can't say it out loud, reconsider.
- **Don't encode the type in the name** (Hungarian notation is dead): `strName` → `name`, `arrItems` → `items`.
- **Avoid noise words**: `data`, `info`, `object`, `manager` add no meaning. `userData` → `user`, `configManager` → `config`.
- **Use positive naming for booleans**: `isLoading`, not `isNotLoading`.
- **Avoid single-letter names** except for well-understood loop counters (`i`, `j`, `k`) or math variables (`x`, `y`).
- **JS never touches classes for logic.** In widget code, JS reads and writes `data-ref`, `data-action`, `data-id`, `data-state` — never class names. Classes are for CSS exclusively.
- **State lives in JS, not in the DOM.** `this._state` is the single source of truth. The DOM is written to from state; it is never read back as a data source.

---

## 2. Variables

Use **camelCase**.

```ts
// ✅ Good
let userName = "Alice";
let itemCount = 42;
let fetchedUsers: User[] = [];

// ❌ Bad
let UserName = "Alice";     // PascalCase is for classes
let user_name = "Alice";    // snake_case is not JS/TS convention
let usrnm = "Alice";        // cryptic abbreviation
```

### Naming patterns by data type

| Data | Example |
|------|---------|
| String | `firstName`, `pageTitle` |
| Number | `itemCount`, `maxRetries`, `pageIndex` |
| Array | `users`, `orderItems`, `selectedIds` (use **plural nouns**) |
| Object | `userProfile`, `requestConfig` |
| Map/Set | `userMap`, `activeIds` |
| Tuple | `coordinates`, `range` |

---

## 3. Constants

### Module-level / compile-time constants

Use **SCREAMING_SNAKE_CASE** for true constants that never change:

```ts
// ✅ Good
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";
const DEFAULT_TIMEOUT_MS = 5000;

// ❌ Bad
const maxRetryCount = 3;   // looks like a variable
const Max_Retry = 3;       // mixed case
```

### Static class constants (widget controllers)

Widget controller classes declare all constants as `static` properties — no loose constants above the class:

```js
class OrdersController {
    // ✅ Correct — everything static, SCREAMING_SNAKE for true constants
    static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
    static DEFAULTS = {
        delay:   1000,
        loop:    false,
        showNav: true,
    };
    static MAX_PREVIEW = 38;
    static SEED_DATA = [];

    // ❌ Wrong — loose constant above the class
    // const MAX_PREVIEW = 38;
}
```

### Object / config constants

Use **camelCase** (or PascalCase for exported config objects):

```ts
// ✅ Good
const defaultConfig = {
  retries: 3,
  timeout: 5000,
};

export const HttpStatus = {
  OK: 200,
  NOT_FOUND: 404,
} as const;
```

### `const` vs "constant"

`const` just means the binding is immutable, not that the value is a true constant. Use SCREAMING_SNAKE_CASE only for values that are semantically constant across the entire application.

---

## 4. Functions

Use **camelCase**. Name functions with a **verb** or **verb phrase**.

```ts
// ✅ Good
function getUserById(id: string): User { return ...; }
function calculateTotalPrice(items: CartItem[]): number { return ...; }
function formatDate(date: Date): string { return ...; }
function isEmailValid(email: string): boolean { return ...; }

// ❌ Bad
function user(id: string) { ... }      // noun only, unclear purpose
function GetUser(id: string) { ... }   // PascalCase reserved for constructors
function g(id: string) { ... }         // meaningless
```

### Common verb prefixes

| Prefix | Use case | Example |
|--------|----------|---------|
| `get` | Returns a value synchronously | `getUser()`, `getTotal()` |
| `fetch` | Async retrieval (API call) | `fetchUsers()`, `fetchOrderById()` |
| `set` | Sets/updates a value | `setUserName()` |
| `update` | Partial update | `updateProfile()` |
| `create` | Factory / instantiation | `createOrder()` |
| `build` | Builder pattern | `buildQuery()` |
| `make` | Same as build/create | `makeRequest()` |
| `handle` | Event or action handler | `handleSubmit()` |
| `on` | Event callback | `onSuccess()`, `onError()` |
| `is` / `has` / `can` / `should` | Boolean predicate | `isAdmin()`, `hasPermission()` |
| `check` | Validation that may throw | `checkAuth()` |
| `validate` | Returns true/false or error | `validateEmail()` |
| `parse` | Transforms raw data | `parseResponse()` |
| `format` | Transforms for display | `formatCurrency()` |
| `calculate` / `compute` | Math / derived values | `calculateDiscount()` |
| `render` | Returns UI | `renderButton()` |
| `init` / `initialize` | Setup | `initDatabase()` |
| `reset` | Restore to defaults | `resetForm()` |
| `load` | Load data | `loadConfig()` |
| `save` / `store` | Persist data | `saveSettings()` |
| `delete` / `remove` | Deletion | `deleteUser()`, `removeItem()` |
| `clear` | Empty a collection | `clearCache()` |
| `find` | Search, may return undefined | `findUserByEmail()` |
| `search` | Query-based search | `searchProducts()` |
| `filter` | Narrow a collection | `filterActiveUsers()` |
| `sort` | Reorder | `sortByDate()` |
| `map` / `transform` | Shape transformation | `mapToDto()` |
| `convert` | Type conversion | `convertToCsv()` |
| `send` | Communication | `sendEmail()` |
| `emit` | Events | `emitChange()` |
| `dispatch` | State management | `dispatchAction()` |
| `subscribe` / `unsubscribe` | Pub/sub | `subscribeToChanges()` |

---

## 5. Classes

Use **PascalCase**. Name with a **noun** that describes what the class represents.

```ts
// ✅ Good
class UserRepository { ... }
class ShoppingCart { ... }
class AuthenticationService { ... }
class HttpClient { ... }
class EventEmitter { ... }

// ❌ Bad
class userRepository { ... }   // camelCase
class manage_users { ... }     // snake_case
class DoUserStuff { ... }      // verb phrase
```

### Widget controller classes

Widget controllers follow the same PascalCase rule. The class name is the **widget name in PascalCase + `Controller`**:

```js
// ✅ Correct
class OrdersController { ... }
class NewslettersController { ... }
class MySizesController { ... }
class WishlistController { ... }

// ❌ Wrong
class ordersController { ... }  // camelCase
class Orders { ... }            // missing Controller suffix
class OrdCtrl { ... }           // abbreviation — cryptic
```

### Abstract classes

Prefix with `Abstract` or use a descriptive noun:

```ts
// Option 1 — explicit prefix
abstract class AbstractRepository<T> { ... }

// Option 2 — describe the role (preferred by many)
abstract class BaseRepository<T> { ... }
abstract class BaseController { ... }
```

### Singleton / service classes

Still PascalCase; the naming suffix hints at the pattern:

```ts
class LoggerService { ... }
class CacheService { ... }
class ConfigStore { ... }
```

---

## 6. Interfaces & Types (TypeScript)

### Interfaces

Use **PascalCase**. **Do NOT prefix with `I`** (the `I` prefix is an outdated Microsoft/COM convention).

```ts
// ✅ Good
interface User {
  id: string;
  name: string;
  email: string;
}

interface Repository<T> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
}

// ❌ Bad
interface IUser { ... }           // redundant 'I' prefix
interface user { ... }            // camelCase
interface UserInterface { ... }   // redundant suffix
```

### Type Aliases

Use **PascalCase** — same as interfaces:

```ts
// ✅ Good
type UserId = string;
type Callback<T> = (value: T) => void;
type UserRole = "admin" | "editor" | "viewer";
type Nullable<T> = T | null;
type ApiResponse<T> = {
  data: T;
  status: number;
  message: string;
};

// ❌ Bad
type userRole = "admin" | "editor";  // camelCase
type USER_ROLE = "admin" | "editor"; // SCREAMING_SNAKE_CASE
```

### Interface vs Type — naming consistency

Treat them identically in naming. Prefer `interface` for object shapes (extendable), `type` for unions, intersections, and primitives.

---

## 7. Enums (TypeScript)

### Enum name — PascalCase

```ts
// ✅ Good
enum Direction {
  Up,
  Down,
  Left,
  Right,
}

enum HttpStatus {
  OK = 200,
  BadRequest = 400,
  Unauthorized = 401,
  NotFound = 404,
  InternalServerError = 500,
}

// ❌ Bad
enum direction { ... }   // camelCase
enum DIRECTION { ... }   // SCREAMING_SNAKE_CASE
```

### Enum members

Use **PascalCase** for members (Google & TypeScript Handbook recommendation):

```ts
// ✅ Preferred
enum Color {
  Red,
  Green,
  Blue,
}

// ⚠️ Also used (older codebases)
enum Color {
  RED,
  GREEN,
  BLUE,
}
```

### Const Enums (prefer `as const` objects)

Many teams now prefer `as const` objects over enums for better tree-shaking:

```ts
// Modern alternative to enum
const Direction = {
  Up: "UP",
  Down: "DOWN",
  Left: "LEFT",
  Right: "RIGHT",
} as const;

type Direction = typeof Direction[keyof typeof Direction];
```

---

## 8. Generics (TypeScript)

Use **single uppercase letters** for simple, well-understood generics. Use **descriptive PascalCase names** for domain-specific generics.

```ts
// ✅ Simple / universal generics
function identity<T>(value: T): T { return value; }
function first<T>(arr: T[]): T | undefined { return arr[0]; }
function map<T, U>(arr: T[], fn: (item: T) => U): U[] { return arr.map(fn); }

// ✅ Descriptive generics (when context matters)
interface Repository<TEntity, TId = string> {
  findById(id: TId): Promise<TEntity | null>;
}

type ApiResponse<TData> = {
  data: TData;
  error: string | null;
};

// ❌ Bad
function map<type1, type2>(...) { ... }   // lowercase
```

### Common generic letter conventions

| Letter | Convention |
|--------|-----------|
| `T` | Primary type |
| `U`, `V` | Additional types |
| `K` | Key type (especially in `Record<K, V>`) |
| `V` | Value type |
| `E` | Element type |
| `R` | Return type |
| `P` | Props (React) |
| `S` | State (React) |

---

## 9. Methods

Use **camelCase**, same verb conventions as functions.

```ts
class UserService {
  // ✅ Good
  async getUserById(id: string): Promise<User> { ... }
  async createUser(dto: CreateUserDto): Promise<User> { ... }
  async updateUserEmail(id: string, email: string): Promise<void> { ... }
  async deleteUser(id: string): Promise<void> { ... }
  isAdmin(user: User): boolean { ... }
  hasPermission(user: User, action: string): boolean { ... }

  // ❌ Bad
  async User(id: string) { ... }     // noun only
  async GET_USER(id: string) { ... } // screaming
  async u(id: string) { ... }        // meaningless
}
```

### Widget controller private methods

Widget controller private methods use `_` prefix (underscored camelCase) and follow strict naming conventions:

| Method | Pattern | Example |
|--------|---------|---------|
| Data attribute reader | `_readDataAttrs()` | always this name |
| Render orchestrator | `_render()` | always this name |
| Partial renderer | `_render` + noun | `_renderList()`, `_renderModal()` |
| Action handler | `_handle` + PascalCase noun | `_handleRemove()`, `_handleSend()` |
| Event binder | `_bind()` | always this name |
| XSS escaper | `_esc()` | always this name |
| Closer | `_close` + noun | `_closeModal()` |
| Opener | `_open` + noun | `_openModal()` |
| Destroyer | `destroy()` | always this name, always last |

```js
class OrdersController {
    // ✅ Correct method names
    _readDataAttrs() { ... }
    _render()        { ... }
    _renderList()    { ... }
    _renderModal()   { ... }
    _handleRemove()  { ... }
    _handleSend()    { ... }
    _bind()          { ... }
    _esc(str)        { ... }
    _closeModal()    { ... }
    destroy()        { ... }   // always last

    // ❌ Wrong
    _hr()            { ... }   // cryptic abbreviation
    _rm()            { ... }   // cryptic abbreviation
    handleRemove()   { ... }   // missing _ prefix for private method
    Render()         { ... }   // PascalCase
}
```

### Accessor methods (getters/setters)

Prefer native getter/setter syntax when the property is simple:

```ts
class Circle {
  private _radius: number;

  get radius(): number {
    return this._radius;
  }

  set radius(value: number) {
    if (value < 0) throw new Error("Radius cannot be negative");
    this._radius = value;
  }

  get area(): number {
    return Math.PI * this._radius ** 2;
  }
}
```

---

## 10. Properties & Fields

Use **camelCase** for instance properties:

```ts
class Order {
  // ✅ Good
  orderId: string;
  createdAt: Date;
  totalAmount: number;
  lineItems: LineItem[];

  // ❌ Bad
  OrderId: string;     // PascalCase
  created_at: Date;    // snake_case
  total: number;       // too vague
}
```

### Static properties

```ts
class HttpClient {
  static readonly DEFAULT_TIMEOUT = 5000;   // SCREAMING for true constants
  static instanceCount = 0;                  // camelCase for mutable statics
}
```

### Widget controller state and config properties

```js
class OrdersController {
    constructor(selector, opts = {}) {
        // ✅ _root — always this name for the container reference
        this._root = document.querySelector(selector);
        if (!this._root) return;

        // ✅ _cfg — always this name for merged configuration
        this._cfg = {
            ...OrdersController.DEFAULTS,
            ...opts,
            ...this._readDataAttrs(),
        };

        // ✅ _state — always this name, single source of truth
        this._state = {
            items:    [],
            activeId: null,
            loading:  false,
            modal:    null,
        };

        // ✅ _ac — always this name for the AbortController
        this._ac = new AbortController();
    }
}
```

---

## 11. Private Members & Widget Controller Conventions

### TypeScript `private` keyword

Use camelCase — no prefix needed because `private` already signals access:

```ts
class UserService {
  // ✅ TypeScript private (compile-time only)
  private readonly repository: UserRepository;
  private cache: Map<string, User> = new Map();

  protected logger: Logger;
}
```

### JavaScript `#` private fields

ES2022 native private fields — use **`#` prefix** directly:

```ts
class BankAccount {
  #balance: number = 0;
  #transactionHistory: Transaction[] = [];

  deposit(amount: number): void {
    this.#balance += amount;
  }
}
```

### Underscore prefix `_` — widget controller standard

In vanilla JS widget controllers (non-TypeScript), `_` prefix marks private instance properties and methods. This is the required pattern inside the containerization standard:

```js
class OrdersController {

    constructor(selector, opts = {}) {
        this._root        // DOM root reference — private
        this._cfg         // merged config object — private
        this._state       // application state — private
        this._ac          // AbortController — private

        // ✅ Cached DOM refs — camelCase, describes the element
        this._itemsList   = $('[data-ref="items-list"]');
        this._sendBtn     = $('[data-ref="send-btn"]');
        this._deleteModal = $('[data-ref="modal-delete"]');

        // ❌ Wrong — cryptic, abbreviated
        this._il  = $('[data-ref="items-list"]');   // what is "il"?
        this._sb  = $('[data-ref="send-btn"]');
        this._dm  = $('[data-ref="modal-delete"]');
    }
}
```

### DOM reference naming table (widget controllers)

| What | Convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| Cached DOM ref | `_` + camelCase noun phrase | `this._itemsList` | `this._il` |
| Cached DOM ref | `_` + camelCase noun phrase | `this._sendBtn` | `this._sb` |
| Cached DOM ref | `_` + camelCase noun phrase | `this._deleteModal` | `this._dm` |
| State object key | camelCase noun | `this._state.activeId` | `this._state.aid` |
| Config object key | camelCase noun, matches DEFAULTS | `this._cfg.showNav` | `this._cfg.sn` |
| Private method | `_` + verb + noun | `_handleRemove()` | `_hr()` |
| Helper variable | noun or verb+noun | `const items`, `const filtered` | `const d`, `const tmp` |

---

## 12. Parameters

Use **camelCase**. Be descriptive — avoid single letters except in callbacks:

```ts
// ✅ Good
function createUser(firstName: string, lastName: string, role: UserRole): User { ... }
function fetchOrdersByDateRange(startDate: Date, endDate: Date): Promise<Order[]> { ... }

// Callbacks — short names acceptable here
const doubled = numbers.map((n) => n * 2);
const found = users.find((user) => user.isActive);

// ❌ Bad
function createUser(fn: string, ln: string, r: UserRole): User { ... }  // cryptic
function fetch(s: Date, e: Date): Promise<Order[]> { ... }              // meaningless
```

### Destructured parameters

```ts
// ✅ Good
function renderUser({ id, name, role }: User): string {
  return `${name} (${role})`;
}

function createOrder({
  userId,
  items,
  shippingAddress,
}: CreateOrderDto): Order { ... }
```

### Rest parameters

Use a clear **plural noun**:

```ts
// ✅ Good
function logMessages(...messages: string[]): void { ... }
function mergeObjects<T>(...objects: Partial<T>[]): T { ... }

// ❌ Bad
function log(...args: string[]): void { ... }  // args is vague
```

---

## 13. Namespaces & Modules

### TypeScript Namespaces

Use **PascalCase** (same as classes):

```ts
namespace Validation {
  export interface StringValidator {
    isAcceptable(s: string): boolean;
  }

  export class LettersOnlyValidator implements StringValidator {
    isAcceptable(s: string): boolean {
      return /^[A-Za-z]+$/.test(s);
    }
  }
}
```

> **Note:** Prefer ES modules (`import`/`export`) over namespaces in modern code. Namespaces are mainly used in declaration files (`.d.ts`).

### Module (file) exports

Named exports use their own conventions (camelCase for functions/vars, PascalCase for classes/types). The module name (file name) should match what it exports.

---

## 14. Files & Directories

### JavaScript / TypeScript files

Use **kebab-case** (all lowercase, hyphens):

```
// ✅ Good
user-service.ts
shopping-cart.ts
auth-middleware.ts
format-date.ts
use-auth.ts         (custom React hook)
app-config.ts

// ❌ Bad
UserService.ts      // PascalCase (common in some ecosystems — avoid unless framework requires)
userService.ts      // camelCase
user_service.ts     // snake_case
```

> **Exception:** React component files use **PascalCase** to match the component name: `UserCard.tsx`, `LoginForm.tsx`.

### Index files

```
components/
  Button/
    index.ts          ← re-exports Button
    Button.tsx
    Button.test.tsx
    Button.styles.ts
```

### Test files

```
user-service.test.ts
user-service.spec.ts      ← alternative suffix
__tests__/user-service.ts ← Jest convention
```

### Type declaration files

```
user.types.ts
api.d.ts
global.d.ts
```

### Directory naming

Use **kebab-case** for directories:

```
src/
  components/
  hooks/
  utils/
  api-client/
  data-access/
```

---

## 15. React & JSX / TSX Conventions

### Components

Use **PascalCase** — required by React (lowercase = HTML element):

```tsx
// ✅ Good
function UserCard({ user }: UserCardProps): JSX.Element { ... }
const LoginForm: React.FC<LoginFormProps> = ({ onSubmit }) => { ... }
export default function HomePage(): JSX.Element { ... }

// ❌ Bad — React treats this as a DOM element
function userCard() { ... }
```

### Props interfaces

Use **PascalCase + `Props` suffix**:

```tsx
// ✅ Good
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
}

// ❌ Bad
interface IButtonProps { ... }    // I prefix
interface buttonProps { ... }     // camelCase
type ButtonPropsType { ... }      // redundant Type suffix
```

### Custom Hooks

**Must start with `use`** (React rule):

```ts
// ✅ Good
function useAuth(): AuthContext { ... }
function usePaginatedUsers(pageSize: number) { ... }
function useDebounce<T>(value: T, delay: number): T { ... }
function useLocalStorage<T>(key: string, initialValue: T) { ... }

// ❌ Bad — React won't recognize these as hooks
function authHook() { ... }
function getUser() { ... }  // looks like a regular function
```

### Context

```tsx
// Context object
const AuthContext = React.createContext<AuthContextValue | null>(null);

// Provider component
function AuthProvider({ children }: { children: React.ReactNode }) { ... }

// Consumer hook
function useAuthContext(): AuthContextValue { ... }
```

### Higher-Order Components (HOC)

Prefix with `with`:

```tsx
// ✅ Good
function withAuth<P extends object>(Component: React.ComponentType<P>) { ... }
function withErrorBoundary<P>(Component: React.ComponentType<P>) { ... }

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

---

## 16. Event Handlers

Use **`handle` prefix** for definitions, **`on` prefix** for props/callbacks:

```tsx
// ✅ Good — method/function definitions
function handleClick(event: React.MouseEvent): void { ... }
function handleSubmit(event: React.FormEvent): void { ... }
function handleInputChange(event: React.ChangeEvent<HTMLInputElement>): void { ... }
function handleUserDelete(userId: string): void { ... }

// ✅ Good — props that receive handlers
interface FormProps {
  onSubmit: (data: FormData) => void;
  onCancel: () => void;
  onChange?: (value: string) => void;
}

// In JSX
<Button onClick={handleClick} />
<Form onSubmit={handleSubmit} onCancel={handleCancel} />

// ❌ Bad
function clickHandler() { ... }   // reversed naming
function submitForm() { ... }     // no handler intent
const handler = () => { ... }     // vague
```

### Widget controller action handlers

In widget controllers, all action dispatch goes through a single root `click` listener with a `switch` on `data-action`. Complex branches are extracted to named `_handleXxx()` methods:

```js
_bind() {
    const sig = { signal: this._ac.signal };

    // ✅ One root listener + switch for all data-action
    this._root.addEventListener('click', e => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        switch (btn.dataset.action) {
            case 'send':          this._handleSend(); break;
            case 'remove':        this._handleRemove(btn.dataset.id); break;
            case 'modal-open':    this._handleModalOpen(btn.dataset.id); break;
            case 'modal-cancel':  this._closeModal(); break;
            case 'modal-confirm': this._handleConfirm(); break;
        }
    }, sig);
}

// ✅ Extracted handler — _handle + PascalCase noun
_handleRemove(id) { ... }
_handleSend()     { ... }
_handleModalOpen(id) { ... }
_handleConfirm()  { ... }

// ❌ Wrong
_onRemove()   { ... }   // should be _handle, not _on
_remove()     { ... }   // missing handle prefix — ambiguous
_hr()         { ... }   // cryptic
```

---

## 17. Boolean Variables

Use **`is`, `has`, `can`, `should`, `was`, `did`** prefixes:

```ts
// ✅ Good
let isLoading = false;
let isAuthenticated = false;
let isVisible = true;
let hasErrors = false;
let hasPermission = true;
let canEdit = false;
let canDelete = false;
let shouldRefetch = true;
let wasModified = false;
let didSubmit = false;

// In interfaces
interface User {
  isActive: boolean;
  isVerified: boolean;
  hasSubscription: boolean;
}

// ❌ Bad
let loading = false;         // ambiguous — could be a loading state object
let authenticated = false;   // adjective without prefix
let errors = false;          // sounds like array of errors
let editPermission = false;  // noun phrase, unclear it's boolean
```

### Widget controller state booleans

```js
this._state = {
    // ✅ Boolean state fields use the same is/has/can convention
    loading:  false,     // ✅ acceptable in state objects (type is clear from context)
    isOpen:   false,     // ✅ explicit prefix also fine
    hasItems: false,     // ✅ explicit prefix

    // ❌ Wrong
    l:    false,         // cryptic
    open: false,         // ambiguous in a state bag context
};
```

---

## 18. Async / Promise Naming

### Async functions

No special prefix needed — the return type `Promise<T>` or `async` keyword conveys it. Use `fetch` instead of `get` to signal an async operation:

```ts
// ✅ Good
async function fetchUser(id: string): Promise<User> { ... }
async function loadDashboardData(): Promise<DashboardData> { ... }
async function saveOrder(order: Order): Promise<void> { ... }

// ⚠️ Potentially misleading — "get" implies sync
async function getUser(id: string): Promise<User> { ... }
```

### Promise variables

Suffix with the result type, not the word "Promise":

```ts
// ✅ Good
const user = await fetchUser(id);
const userPromise = fetchUser(id);  // when storing the promise (uncommon)

// ❌ Bad
const userPromise = await fetchUser(id);  // await resolves it — no longer a Promise
const promisedUser = fetchUser(id);
```

### Callbacks and async patterns

```ts
// ✅ Good
const handleAsyncAction = async (): Promise<void> => { ... };

// ✅ Naming promise chains
fetchUsers()
  .then((users) => filterActive(users))
  .then((activeUsers) => renderUserList(activeUsers))
  .catch((error) => handleFetchError(error));
```

---

## 19. Type Assertions & Type Guards

No naming convention for assertions, but prefer type guards over assertions:

```ts
// ✅ Prefer type guards (named with is-prefix)
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null && "id" in value;
}

function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}

// Type predicates follow the isXxx pattern
function isNonNullable<T>(value: T): value is NonNullable<T> {
  return value !== null && value !== undefined;
}
```

---

## 20. Decorators

Use **PascalCase** for class decorators (they act like classes). Use **camelCase** for method/property decorators:

```ts
// ✅ Class decorators — PascalCase
@Injectable()
@Controller("/users")
@Singleton
class UserService { ... }

// ✅ Method / property decorators — camelCase
class UserController {
  @get("/users")
  @authorize("admin")
  @validate(CreateUserSchema)
  async createUser(@body() dto: CreateUserDto) { ... }
}
```

---

## 21. Test Files & Test Identifiers

### Test file naming

```
user-service.test.ts     ← unit test
user-service.spec.ts     ← spec / behavior test
user-service.e2e.ts      ← end-to-end test
user-service.int.ts      ← integration test
```

### `describe` blocks — use the class/function name

```ts
describe("UserService", () => {
  describe("getUserById", () => {
    it("should return the user when found", async () => { ... });
    it("should throw NotFoundException when user does not exist", async () => { ... });
    it("should return null when id is empty", async () => { ... });
  });
});
```

### `it` / `test` descriptions — plain English, behavior-driven

```ts
// ✅ Good — describes expected behavior
it("should return 401 when user is not authenticated", ...);
it("should update the cart total when item is added", ...);
it("returns an empty array when no users match the filter", ...);

// ❌ Bad — vague
it("works", ...);
it("test user", ...);
it("getUserById", ...);  // just repeats the function name
```

### Test variables

```ts
// ✅ Use 'mock', 'stub', 'spy', 'fake' prefixes
const mockUserRepository = createMockRepository<User>();
const stubEmailService = { send: jest.fn() };
const spyLogger = jest.spyOn(logger, "error");

// ✅ Use 'expected' / 'actual' for assertions
const expectedUser: User = { id: "1", name: "Alice" };
const actualUser = await service.getUserById("1");
expect(actualUser).toEqual(expectedUser);
```

---

## 22. Abbreviations & Acronyms

### Well-known abbreviations — keep lowercase in camelCase

```ts
// ✅ Good
const apiUrl = "https://api.example.com";
const htmlContent = "<p>Hello</p>";
const userId = "abc123";
const httpClient = new HttpClient();

// ❌ Bad — inconsistent casing
const APIUrl = "...";
const HTMLContent = "...";
const userID = "...";  // ambiguous — looks like a constant
```

### Acronyms in PascalCase — capitalize only the first letter

```ts
// ✅ Good
class HttpClient { ... }       // not HTTPClient
class XmlParser { ... }        // not XMLParser
interface JsonResponse { ... } // not JSONResponse
function parseUrl(url: string) { ... }   // not parseURL

// Exception: 2-letter acronyms are usually all caps
class IOStream { ... }
type ID = string;
```

### Widget code — no abbreviations ever

In widget controllers, data attribute values, `data-ref` names, `data-action` values, CSS class names, and token names must use full, readable words:

```js
// ✅ Full words everywhere in widget code
this._itemsList       = $('[data-ref="items-list"]');
this._sendBtn         = $('[data-ref="send-btn"]');
this._state.activeId  = null;

// data-ref values
data-ref="items-list"        // ✅ full words
data-ref="send-btn"          // ✅ full words

// data-action values
data-action="remove-item"    // ✅ verb-noun
data-action="modal-confirm"  // ✅ modal- prefix for modal actions

// ❌ Wrong
this._il       = $('[data-ref="il"]');   // cryptic ref name
data-ref="il"                            // cryptic
data-action="ri"                         // cryptic
```

---

## 23. DOM Interaction Conventions

This section is unique to this guide and is derived from the Containerization Standard v11. It governs how JS interacts with the DOM inside widgets.

### Law Zero: JS operates exclusively through data attributes

Classes are for CSS. IDs are for ARIA and anchors. Data attributes are for JS. These roles never mix:

```js
// ✅ CORRECT — locate elements via data-ref
this._sendBtn   = this._root.querySelector('[data-ref="send-btn"]');
this._itemsList = this._root.querySelector('[data-ref="items-list"]');

// ✅ CORRECT — delegate actions via data-action
this._root.addEventListener('click', e => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    // dispatch on btn.dataset.action
});

// ✅ CORRECT — track records via data-id
const id = btn.dataset.id;

// ✅ CORRECT — read/write state via data-state
li.dataset.state = 'active';
// CSS: .orders-item[data-state="active"] { ... }

// ❌ FORBIDDEN — querySelector by class for logic
this._root.querySelector('.orders-item');
this._root.querySelector('.send-btn');

// ❌ FORBIDDEN — getElementById for logic
document.getElementById('send-btn');

// ❌ FORBIDDEN — jQuery
$('.send-btn').on('click', handler);
$('#modal').show();

// ❌ FORBIDDEN — class manipulation for state
btn.classList.add('btn-loading');
li.classList.add('orders-item--active');
// Instead: li.dataset.state = 'active';
```

### Allowed query methods (widget context)

```js
// ✅ These are the ONLY legal query methods inside a widget class

// Bootstrap — finds the container itself (one-time, outside class body)
document.querySelector('.orders-container')

// Inside the class — everything scoped through this._root
this._root.querySelector('[data-ref="name"]')       // cached DOM ref
this._root.querySelector('[data-action="name"]')    // action target
this._root.querySelectorAll('[data-id]')            // iterate records
e.target.closest('[data-action]')                   // delegation
e.target.closest('[data-id]')                       // record resolution

// ARIA + anchor ID lookups (only for ARIA wiring, never for logic)
document.getElementById(id)
```

### State management naming

State is always `this._state`, an object with camelCase keys. DOM is always derived from state — never the reverse:

```js
// ✅ State drives DOM
this._state = {
    items:    [],
    activeId: null,
    loading:  false,
    modal:    null,   // { type: 'delete', targetId: '...' } | null
};

// ✅ Render is derived from state
_render() {
    this._renderList();
    this._renderModal();
}

// ❌ WRONG — reading state back from DOM
_handleSomething() {
    const isActive = this._someEl.classList.contains('is-active');  // forbidden
    const id = this._someEl.querySelector('.orders-item').dataset.id; // class query forbidden
}
```

### AbortController — always `this._ac`

```js
// ✅ Declared in constructor, used in _bind(), terminated in destroy()
this._ac = new AbortController();

_bind() {
    const sig = { signal: this._ac.signal };
    this._root.addEventListener('click', handler, sig);
    this._root.addEventListener('keydown', handler, sig);
    // passive listeners:
    this._root.addEventListener('scroll', handler, { signal: this._ac.signal, passive: true });
}

destroy() {
    this._ac.abort(); // removes ALL listeners in one call
}

// ❌ Wrong — local AbortController inside a helper method
_someHelper() {
    const ac = new AbortController();  // forbidden — use the shared this._ac
}
```

### Security: `_esc()` and `textContent`

All user-supplied or external data inserted into the DOM must be escaped or use `textContent`:

```js
// ✅ User text — textContent, no escaping needed
el.textContent = user.name;

// ✅ External/server data in innerHTML — always through _esc()
this._itemsList.innerHTML = items.map(item => `
    <li class="orders-item"
        data-id="${this._esc(item.id)}"
        data-state="${this._esc(item.status)}">
        <span class="name">${this._esc(item.name)}</span>
    </li>
`).join('');

// ❌ FORBIDDEN — unescaped data in innerHTML
this._itemsList.innerHTML = `<li>${item.name}</li>`;  // XSS risk

// ❌ FORBIDDEN — inline style in templates
return `<div style="font-size:.6rem">${label}</div>`;

// ✅ Correct — CSS class in template
return `<div class="orders-stepper-label">${this._esc(label)}</div>`;
```

### CSS custom property updates from JS

The only legal use of `.style` in JS is setting CSS custom property values after render, when the value is numeric and cannot be known at build time:

```js
// ✅ Only legal use of .style in widget JS
el.style.setProperty('--orders-fill-percent', pct + '%');
// CSS: .orders-track-fill { width: var(--orders-fill-percent, 0%); }

// ❌ FORBIDDEN — style property assignment
icon.style.fontSize = '18px';
icon.style.color = 'red';
```

---

## 24. Naming Anti-patterns

### ❌ Generic / meaningless names

```ts
// Bad
const data = fetchUsers();
const result = processOrder(order);
const temp = calculateTotal();
const value = getConfig();
const obj = new UserService();
const info = getUserInfo();

// Good
const users = fetchUsers();
const processedOrder = processOrder(order);
const orderTotal = calculateTotal();
const appConfig = getConfig();
const userService = new UserService();
const userProfile = getUserInfo();
```

### ❌ Misleading names

```ts
// Implies list/array but it's a count
const users = 42;       // should be userCount
// Implies boolean but returns user
const isUser = getUser(); // should be user

// Names that lie about return type
function getUsers(): User { ... }    // returns one user, not many
function findUser(): User[] { ... }  // returns many, not one
```

### ❌ Unnecessary context repetition

```ts
// In class UserService — "user" is redundant in method names
class UserService {
  getUserById() { ... }      // ❌ "user" is obvious from class name
  getById() { ... }          // ✅ better
  getUserProfile() { ... }   // ❌
  getProfile() { ... }       // ✅
}

// In a user object — "user" is redundant
const user = {
  userName: "Alice",   // ❌
  name: "Alice",       // ✅
  userAge: 30,         // ❌
  age: 30,             // ✅
};
```

### ❌ Numeric suffixes

```ts
// Bad — what's the difference?
const user1 = getUser(id1);
const user2 = getUser(id2);

// Good — be specific
const currentUser = getUser(currentUserId);
const targetUser = getUser(targetUserId);
```

### ❌ Negated booleans

```ts
// Bad — double negatives are confusing
const isNotActive = !user.isActive;
if (!isNotActive) { ... }   // confusing!

// Good
const isActive = user.isActive;
if (isActive) { ... }
```

### ❌ Class selectors in widget JS

```js
// ❌ FORBIDDEN — querying by class inside a widget
this._root.querySelector('.orders-item')
this._root.querySelectorAll('.nav-link')
btn.classList.contains('is-active')
btn.classList.add('btn--loading')

// ✅ Correct
this._root.querySelector('[data-ref="items-list"]')
this._root.querySelectorAll('[data-id]')
btn.dataset.state === 'active'
btn.dataset.state = 'loading'
```

### ❌ Abbreviated widget identifiers

```js
// ❌ Wrong in widget code — abbreviations forbidden
data-ref="il"            // → data-ref="items-list"
data-action="ri"         // → data-action="remove-item"
this._il                 // → this._itemsList
this._cfg.sn             // → this._cfg.showNav
--ord-accent             // → --orders-accent
class="ord-item"         // → class="orders-item"
@keyframes ord-mi {}     // → @keyframes orders-modal-in {}
id="omt"                 // → id="orders-modal-title"
```

---

## 25. Quick Reference Cheatsheet

| Construct | Convention | Example |
|-----------|-----------|---------|
| Variable | camelCase | `userCount`, `isLoading` |
| Constant (primitive) | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_URL` |
| Constant (object) | camelCase or PascalCase | `defaultConfig`, `HttpStatus` |
| Function | camelCase + verb | `getUserById()`, `fetchOrders()` |
| Class | PascalCase + noun | `UserService`, `ShoppingCart` |
| Widget controller class | PascalCase + `Controller` | `OrdersController`, `WishlistController` |
| Abstract class | PascalCase + `Base`/`Abstract` | `BaseRepository`, `AbstractHandler` |
| Interface | PascalCase (no `I`) | `User`, `Repository<T>` |
| Type alias | PascalCase | `UserId`, `Callback<T>` |
| Enum | PascalCase | `Direction`, `HttpStatus` |
| Enum member | PascalCase | `Direction.Up`, `HttpStatus.NotFound` |
| Generic | T, U, K / PascalCase | `T`, `TEntity`, `TId` |
| Method | camelCase + verb | `calculateTotal()`, `isAdmin()` |
| Widget private method | `_` + camelCase verb | `_handleRemove()`, `_renderList()` |
| Property | camelCase | `firstName`, `createdAt` |
| Private field (`#`) | camelCase | `#balance`, `#cache` |
| Widget private field | `_` + camelCase | `this._root`, `this._state` |
| Parameter | camelCase | `userId`, `startDate` |
| Rest parameter | camelCase plural | `...messages`, `...items` |
| Namespace | PascalCase | `Validation`, `Utils` |
| File (TS/JS) | kebab-case | `user-service.ts` |
| File (React) | PascalCase | `UserCard.tsx`, `LoginForm.tsx` |
| Directory | kebab-case | `api-client/`, `data-access/` |
| React component | PascalCase | `UserCard`, `LoginButton` |
| React props type | PascalCase + `Props` | `UserCardProps`, `ButtonProps` |
| Custom hook | `use` + PascalCase | `useAuth`, `usePagination` |
| HOC | `with` + PascalCase | `withAuth`, `withLogging` |
| Context | PascalCase + `Context` | `AuthContext`, `ThemeContext` |
| Event handler prop | `on` + PascalCase | `onClick`, `onSubmit`, `onChange` |
| Event handler fn | `handle` + PascalCase | `handleClick`, `handleSubmit` |
| Boolean variable | `is/has/can/should` + adj | `isActive`, `hasErrors`, `canEdit` |
| Type guard | `is` + PascalCase | `isUser()`, `isApiError()` |
| Decorator (class) | PascalCase | `@Injectable`, `@Controller` |
| Decorator (method) | camelCase | `@get`, `@authorize` |
| Test describe | Class/function name | `describe("UserService", ...)` |
| Test it/test | Plain English behavior | `it("should return 404 when...")` |
| Mock/stub/spy | prefix + name | `mockRepo`, `stubMailer`, `spyLog` |
| Widget static const | SCREAMING_SNAKE | `static DEFAULTS`, `static MAX_PREVIEW` |
| Widget DOM ref | `_` + camelCase noun | `this._itemsList`, `this._sendBtn` |
| Widget state key | camelCase noun | `this._state.activeId` |
| Widget config key | camelCase, matches DEFAULTS | `this._cfg.showNav` |
| Widget data-ref value | kebab-case full words | `"items-list"`, `"send-btn"` |
| Widget data-action value | `verb-noun` full words | `"remove-item"`, `"modal-confirm"` |
| Widget data-state value | full adjective/noun | `"active"`, `"cancelled"`, `"loading"` |
| **Class as JS hook** | **❌ FORBIDDEN** | ~~`.js-send-btn`~~, ~~`classList.add`~~ for state |
| **ID as JS hook** | **❌ FORBIDDEN** | ~~`getElementById('send-btn')`~~ |
| **jQuery** | **❌ FORBIDDEN** | ~~`$('.anything')`~~ |

---

## 26. References & Further Reading

| Resource | URL |
|----------|-----|
| **Airbnb JavaScript Style Guide** | https://github.com/airbnb/javascript |
| **Google JavaScript Style Guide** | https://google.github.io/styleguide/jsguide.html |
| **Google TypeScript Style Guide** | https://google.github.io/styleguide/tsguide.html |
| **TypeScript Handbook** | https://www.typescriptlang.org/docs/handbook/ |
| **TypeScript Do's and Don'ts** | https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html |
| **Microsoft TypeScript Coding Guidelines** | https://github.com/microsoft/TypeScript/wiki/Coding-guidelines |
| **ESLint** | https://eslint.org |
| **@typescript-eslint** | https://typescript-eslint.io |
| **Prettier** | https://prettier.io |
| **Clean Code (Robert C. Martin)** | ISBN 978-0132350884 |
| **React Naming Conventions** | https://react.dev/learn/thinking-in-react |
| **MDN — data-* attributes** | https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes |
| **MDN — AbortController** | https://developer.mozilla.org/en-US/docs/Web/API/AbortController |

### Recommended ESLint rules for naming

```json
{
  "@typescript-eslint/naming-convention": [
    "error",
    { "selector": "variable", "format": ["camelCase", "UPPER_CASE"] },
    { "selector": "function", "format": ["camelCase"] },
    { "selector": "class", "format": ["PascalCase"] },
    {
      "selector": "interface",
      "format": ["PascalCase"],
      "custom": { "regex": "^I[A-Z]", "match": false }
    },
    { "selector": "typeAlias", "format": ["PascalCase"] },
    { "selector": "enum", "format": ["PascalCase"] },
    { "selector": "enumMember", "format": ["PascalCase"] }
  ],
  "no-restricted-globals": [
    "error",
    { "name": "jQuery", "message": "jQuery is forbidden. Use data attributes and native DOM APIs." },
    { "name": "$", "message": "$ (jQuery) is forbidden. Use data-ref and data-action attributes." }
  ]
}
```

### Stylelint rule for enforcing no-BEM class pattern

```json
{
  "selector-class-pattern": "^[a-z][a-z0-9]*(-[a-z0-9]+)*$"
}
```

> This regex allows single-hyphen kebab-case (`.orders-item`, `.btn-primary`) and explicitly rejects double-underscore `__` and double-hyphen `--` BEM separators. Add it to `.stylelintrc.json`. Do not install `stylelint-selector-bem-pattern`.

---

*Last updated: 2026 — Based on TypeScript 5.x, ES2024, React 18+, Containerization Standard v11. BEM interaction patterns removed; Law Zero and data-state conventions added in §23.*
