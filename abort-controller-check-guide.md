# AbortController — Руководство по проверке и внедрению
## Для виджетов стандарта containerization-6

---

## Зачем это нужно

Каждый `addEventListener` создаёт ссылку на callback-функцию. Пока эта ссылка существует — callback и всё замкнутое в нём (DOM-элементы, state, данные) не может быть собрано garbage collector'ом.

Виджеты containerization-6 встраиваются в страницы с табами. При переключении таба виджет может монтироваться и демонтироваться. Без снятия listeners каждое такое переключение добавляет новый слой висящих ссылок.

```
Открыл таб → создан виджет → 10 addEventListener
Закрыл таб → DOM очищен, но 10 callbacks всё ещё в памяти
Открыл таб → ещё 10 addEventListener → 20 callbacks
Закрыл таб → 20 callbacks в памяти
...
```

`AbortController` решает это одним вызовом:

```js
this._ac = new AbortController();

// Все listeners регистрируются с одним signal
element.addEventListener('click', handler, { signal: this._ac.signal });
element.addEventListener('input', handler, { signal: this._ac.signal });
// ... сколько угодно listeners

// При демонтаже — один вызов убирает все
destroy() {
  this._ac.abort(); // все listeners сняты, память освобождена
}
```

---

## Структура по гайду

Согласно containerization-6, в каждом виджете обязательны три элемента:

```js
class WidgetController {

  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // ... DOM refs, state ...

    this._ac = new AbortController(); // ← ОБЯЗАТЕЛЬНО в конструкторе
    this._render();
    this._bind();
  }

  _bind() {
    const sig = { signal: this._ac.signal }; // ← объявить один раз

    this._root.addEventListener('click', e => { ... }, sig);
    this._root.addEventListener('keydown', e => { ... }, sig);
    document.addEventListener('keydown', e => { ... }, sig);
    // каждый listener получает sig
  }

  destroy() {
    this._ac.abort(); // ← ОБЯЗАТЕЛЬНО, снимает все listeners разом
  }
}
```

---

## Фаза 1 — Аудит файла

### 1.1 Быстрая проверка: три вопроса

```
1. Есть ли this._ac = new AbortController() в конструкторе?
2. Есть ли destroy() { this._ac.abort() }?
3. Каждый ли addEventListener передаёт { signal: this._ac.signal }?
```

Если хотя бы один ответ «нет» — файл требует исправления.

### 1.2 grep-проверка

```bash
# Найти все addEventListener в файле (исключая комментарии и DOMContentLoaded)
grep -n 'addEventListener' file.html | grep -v '^\s*//' | grep -v 'DOMContentLoaded'

# Найти AbortController
grep -n 'AbortController\|_ac\|\.abort()' file.html

# Найти destroy
grep -n 'destroy()' file.html | grep -v '^\s*//'
```

### 1.3 Классификация listeners

Пройди по каждому найденному `addEventListener` и определи категорию:

| Категория | Описание | Действие |
|---|---|---|
| **NEEDS_SIG** | Обычный listener без `signal` | Добавить `sig` |
| **ONCE_OK** | `{ once: true }` | Не трогать — легально |
| **PASSIVE_OK** | `{ passive: true }` без `signal` | Добавить `signal` к объекту опций |
| **INIT_SKIP** | `DOMContentLoaded` на `document` | Не трогать — инициализация |

---

## Фаза 2 — Категории нарушений

### AC_MISSING — нет AbortController вообще

Файл не содержит ни `AbortController`, ни `destroy()`. Все listeners висят вечно.

**Что делать:** добавить всё с нуля — `this._ac`, `destroy()`, `sig` ко всем listeners.

### AC_PARTIAL — AC есть, но не все listeners используют signal

`AbortController` объявлен, `sig` объявлен, но часть listeners вызвана без третьего аргумента.

**Что делать:** найти все listeners без `sig` и добавить его.

### PRIVATE_FIELD — класс использует private fields (`#`)

Виджет использует `#ac` вместо `this._ac`. Подход идентичен, только синтаксис другой.

```js
// В классе с private fields:
#ac = new AbortController();  // ← объявить в списке полей класса

#setupEventListeners() {
  const sig = { signal: this.#ac.signal };
  element.addEventListener('click', handler, sig);
}

destroy() {
  this.#ac.abort();
}
```

---

## Фаза 3 — Внедрение

### 3.1 Шаг 1 — Добавить `this._ac` в конструктор

Место: **после** кэширования DOM-ссылок, **перед** вызовами `_render()` и `_bind()`.

```js
// ✅ правильное место
constructor(selector) {
  this._root = document.querySelector(selector);
  if (!this._root) return;

  // DOM refs
  this._itemsList = this._root.querySelector('[data-ref="items-list"]');

  // State
  this._state = { ... };

  this._ac = new AbortController(); // ← здесь

  this._render();
  this._bind();
}
```

### 3.2 Шаг 2 — Добавить `destroy()`

Место: последний метод класса перед закрывающей скобкой `}`.

```js
// ✅ последний метод в классе
destroy() {
  this._ac.abort();
}
```

### 3.3 Шаг 3 — Добавить `sig` в `_bind()`

Объявить `const sig` **первой строкой** метода, передать во все listeners.

```js
_bind() {
  const sig = { signal: this._ac.signal }; // ← первая строка

  this._root.addEventListener('click', e => { ... }, sig);
  this._root.addEventListener('keydown', e => { ... }, sig);
  document.addEventListener('keydown', e => { ... }, sig);
}
```

### 3.4 Listeners вне `_bind()`

Если listeners объявляются в других методах (`_initPersonal()`, `_setupInputMasks()`, `#setupEventListeners()`), `sig` нужно добавлять там же:

```js
_initPersonal() {
  const sig = { signal: this._ac.signal }; // ← sig в каждом методе с listeners

  this._editBtn.addEventListener('click', () => this._enterEditMode(), sig);
  this._saveBtn.addEventListener('click', () => this._handleSave(), sig);
}
```

Не создавай новый `AbortController` в каждом методе — только один `this._ac` на весь виджет.

### 3.5 Listeners с `{ passive: true }`

`passive` и `signal` объединяются в один объект опций:

```js
// ✅ правильно
this._root.addEventListener('scroll', this._onScroll.bind(this), {
  signal: this._ac.signal,
  passive: true,
});

// ❌ неправильно — sig перезаписывает passive
this._root.addEventListener('scroll', handler, sig);        // теряет passive
this._root.addEventListener('scroll', handler, { passive: true }); // теряет signal
```

### 3.6 `{ once: true }` — легальное исключение

Listeners с `{ once: true }` автоматически снимаются после первого срабатывания. `signal` добавлять не обязательно, но можно.

```js
// ✅ легально без signal — снимается сам
picker.addEventListener('animationend', () => {
  picker.classList.remove('is-invalid');
}, { once: true });

// ✅ тоже легально — signal + once (дополнительная страховка)
picker.addEventListener('animationend', () => {
  picker.classList.remove('is-invalid');
}, { once: true, signal: this._ac.signal });
```

Правило: если `{ once: true }` — не трогай. Если без `once` — нужен `signal`.

### 3.7 Динамически создаваемые listeners (в forEach, per-item)

```js
// ❌ проблема — listeners на каждой карточке, нет способа снять
items.forEach(item => {
  const card = this._buildCard(item);
  card.addEventListener('click', () => this._handleClick(item.id));
});

// ✅ решение — делегация на root вместо listeners на элементах
_bind() {
  const sig = { signal: this._ac.signal };
  this._root.addEventListener('click', e => {
    const card = e.target.closest('[data-id]');
    if (!card) return;
    this._handleClick(card.dataset.id);
  }, sig);
}
```

Делегация — стандартный паттерн containerization-6. Один listener на root вместо N listeners на дочерних элементах.

---

## Фаза 4 — Валидация

### 4.1 После каждого файла — автоматическая проверка

```python
# Python-скрипт для проверки файла
with open('widget.html') as f:
    lines = f.readlines()

# Функция точного поиска закрывающей скобки addEventListener
def has_signal(lines, listener_line_idx):
    combined = ''.join(lines[listener_line_idx:listener_line_idx+60])
    # { once: true } — легально
    if '{ once' in lines[listener_line_idx]:
        return True
    # Найти закрывающую скобку addEventListener(...)
    start = combined.find('addEventListener(')
    if start == -1: return False
    start = combined.find('(', start + len('addEventListener'))
    depth = 0
    for i in range(start, len(combined)):
        if combined[i] == '(': depth += 1
        elif combined[i] == ')':
            depth -= 1
            if depth == 0:
                segment = combined[max(0, i-25):i+2]
                return 'signal' in segment or 'sig' in segment
    return False

# Проверка
problems = []
for i, line in enumerate(lines):
    if 'addEventListener' in line and 'DOMContentLoaded' not in line:
        if not line.strip().startswith(('//', '*')):
            if not has_signal(lines, i):
                problems.append((i+1, line.strip()))

print(f"AC: {'✅' if any('AbortController' in l for l in lines) else '❌'}")
print(f"destroy: {'✅' if any('destroy()' in l for l in lines) else '❌'}")
print(f"Listeners без signal: {len(problems)}")
for n, l in problems:
    print(f"  L{n}: {l[:80]}")
```

### 4.2 Чеклист перед коммитом

```
□ this._ac = new AbortController() в конструкторе
□ destroy() { this._ac.abort() } как последний метод класса
□ const sig = { signal: this._ac.signal } — первая строка _bind()
□ Каждый addEventListener (кроме DOMContentLoaded) передаёт sig
□ { passive: true } listeners объединены с signal в один объект
□ { once: true } listeners — оставлены как есть (легально)
□ Listeners в forEach заменены на делегацию (или имеют sig)
□ Listeners в других методах (_initXxx, #setupXxx) — тоже имеют sig
□ document.addEventListener(...) — тоже имеет sig (особенно важно!)
```

---

## Типичные ошибки

### ❌ AC объявлен, destroy нет

```js
constructor() {
  this._ac = new AbortController(); // есть
  this._bind();
}
// destroy() отсутствует — abort() никогда не вызывается, AC бесполезен
```

### ❌ destroy есть, sig не передаётся

```js
destroy() { this._ac.abort(); } // есть

_bind() {
  this._root.addEventListener('click', handler); // нет sig — abort() не снимет
}
```

### ❌ Новый AbortController в каждом методе

```js
_initPersonal() {
  const ac = new AbortController(); // ← локальный AC
  btnEdit.addEventListener('click', handler, { signal: ac.signal });
  // ac нигде не сохраняется → abort() вызвать невозможно
}
```

### ❌ sig объявлен, но не передан в многострочный listener

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click', e => {
    // ... много кода ...
  }); // ← закрывающая скобка без sig!
}
```

### ✅ Правильно — sig на закрывающей скобке

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click', e => {
    // ... много кода ...
  }, sig); // ← sig здесь
}
```

---

## Справочник: форматы передачи signal

```js
const sig = { signal: this._ac.signal };

// Однострочный listener
el.addEventListener('click', handler, sig);

// Многострочный listener
el.addEventListener('click', e => {
  // ...
}, sig);

// С passive
el.addEventListener('scroll', handler, {
  signal: this._ac.signal,
  passive: true,
});

// Inline объект (избегать — хуже читаемость)
el.addEventListener('click', handler, { signal: this._ac.signal });

// forEach — sig объявлен снаружи, передаётся в каждый
spans.forEach(span => {
  span.addEventListener('click', () => { ... }, sig);
  span.addEventListener('keydown', e => { ... }, sig);
});

// Bootstrap events — тоже через sig
modal.addEventListener('hidden.bs.modal', () => { ... }, sig);
modal.addEventListener('hide.bs.modal', () => { ... }, sig);
modal.addEventListener('shown.bs.modal', () => { ... }, sig);
```

---

## Итоговая таблица: что делать в каждой ситуации

| Ситуация | Действие |
|---|---|
| Нет AC, нет destroy, нет sig | Добавить все три: AC в конструктор, destroy в конец класса, sig во все listeners |
| AC есть, destroy есть, часть listeners без sig | Найти listeners без sig, добавить |
| `{ once: true }` без sig | Не трогать |
| `{ passive: true }` без sig | Объединить: `{ signal: ..., passive: true }` |
| `document.addEventListener` без sig | Обязательно добавить sig — это глобальный listener |
| Listeners в методах кроме `_bind()` | Добавить sig там же, использовать `this._ac.signal` |
| Listeners в forEach на DOM-элементах | Рассмотреть делегацию; если нет — добавить sig |
| Private fields (`#ac`) | Синтаксис другой, логика идентична |
