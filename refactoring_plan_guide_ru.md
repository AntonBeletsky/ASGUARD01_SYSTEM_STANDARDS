# Refactoring Plan Guide
> Corporate standard for structured, auditable, machine-readable refactoring instructions.
> Version 1.0.0

---

## 1. Назначение документа

Этот стандарт описывает формат, структуру и процесс создания планов рефакторинга для любого масштаба задач — от правки одного CSS-класса до переработки архитектуры модуля.

Цель стандарта:
- Сделать план проверяемым до выполнения
- Исключить двусмысленность в формулировках "было / стало"
- Обеспечить трассируемость каждого изменения
- Дать возможность частичного применения и отката
- Стандартизировать аудит плана как отдельный обязательный этап

---

## 2. Когда использовать этот формат

| Ситуация | Использовать план |
|---|---|
| Правка 1–2 строк в одном файле | ❌ Не нужен |
| Изменения в 2+ файлах | ✅ Обязателен |
| Изменения затрагивают HTML + CSS + JS одновременно | ✅ Обязателен |
| Изменения в shared/системных стилях | ✅ Обязателен |
| Работа затрагивает публичный API класса или data-атрибуты | ✅ Обязателен |
| Задача делается несколькими людьми | ✅ Обязателен |

---

## 3. Жизненный цикл плана

```
DRAFT → AUDIT → APPROVED → IN PROGRESS → DONE / ROLLED BACK
```

| Статус | Описание |
|---|---|
| `draft` | План написан, не проверен |
| `audit` | Проводится проверка на конфликты и зависимости |
| `approved` | Прошёл аудит, готов к выполнению |
| `in_progress` | Выполняется, часть пунктов закрыта |
| `done` | Все пункты выполнены и проверены |
| `rolled_back` | Откат — причина фиксируется в `rollback_reason` |

---

## 4. Структура JSON плана

### 4.1 Корневой объект

```json
{
  "plan": {
    "meta": { ... },
    "scope": { ... },
    "audit": { ... },
    "blocks": [ ... ],
    "verification": { ... }
  }
}
```

### 4.2 Объект `meta` — обязательный

```json
"meta": {
  "id": "rfc-2025-001",
  "title": "Краткое название задачи",
  "status": "draft | audit | approved | in_progress | done | rolled_back",
  "version": "1.0.0",
  "created": "2025-10-14",
  "updated": "2025-10-14",
  "author": "имя или команда",
  "reviewer": "имя или команда | null",
  "rollback_reason": null
}
```

**Правила:**
- `id` — уникальный, формат `rfc-YYYY-NNN`
- `version` — семантическое версионирование самого плана
- `rollback_reason` — заполняется только при статусе `rolled_back`
- `reviewer` — обязателен если статус `approved` или выше

### 4.3 Объект `scope` — обязательный

```json
"scope": {
  "files": [
    "path/to/file.html",
    "path/to/file.css",
    "path/to/file.js"
  ],
  "components": ["MessagesController", ".messages-container"],
  "excluded": ["customer-account-orders.js"],
  "breaking_change": false
}
```

**Правила:**
- `files` — точные пути, не паттерны
- `excluded` — явно перечислить что НЕ трогается, особенно если это неочевидно
- `breaking_change` — `true` если меняется публичный API, data-атрибуты используемые извне, или CSS классы используемые в других компонентах

### 4.4 Объект `audit` — обязательный, заполняется после проверки

```json
"audit": {
  "status": "passed | failed | partial",
  "conducted_by": "имя | null",
  "conducted_at": "2025-10-14 | null",
  "findings": [
    {
      "item_id": "html-2",
      "severity": "critical | warning | info",
      "description": "Описание находки",
      "resolution": "Как исправлено в плане"
    }
  ]
}
```

**Правила:**
- `findings` может быть пустым массивом — это означает что замечаний нет
- severity `critical` блокирует статус `approved` до устранения
- severity `warning` документируется, но не блокирует
- severity `info` — наблюдение без действия

### 4.5 Массив `blocks` — основное тело плана

```json
"blocks": [
  {
    "block": "HTML | CSS | JS | CONFIG | OTHER",
    "file": "path/to/file",
    "changes": [ ... ]
  }
]
```

**Правила:**
- Один `block` — один файл
- Если один тип файла но несколько файлов — создавать отдельные блоки
- Порядок блоков = порядок применения

### 4.6 Объект `change` — единица изменения

```json
{
  "id": "html-1",
  "title": "Короткое название изменения",
  "status": "pending | done | skipped",
  "risk": "low | medium | high",
  "dependencies": [],
  "was": "точный фрагмент кода который будет заменён",
  "now": "точный фрагмент кода который придёт на замену",
  "why": "обоснование — что было не так и почему это решение правильное",
  "notes": "опциональные замечания, edge cases, что проверить после"
}
```

**Правила для `id`:**
- Формат `{block_type}-{N}` — например `html-1`, `css-3`, `js-2`
- Уникален в пределах всего плана, не только блока

**Правила для `was` / `now`:**
- Это точный код, не описание
- Если изменение — удаление, `now` = `"/* deleted */"`
- Если изменение — добавление нового (не замена), `was` = `"/* new addition */"`
- Код должен быть скопирован из реального файла, не написан по памяти
- Контекстные строки (соседний код для ориентира) оборачиваются в комментарий `// [context]`

**Правила для `risk`:**
- `low` — изолированное изменение, нет внешних зависимостей
- `medium` — затрагивает shared стили, data-атрибуты или классы используемые в JS
- `high` — меняет публичный API, breaking change, или затрагивает несколько компонентов

**Правила для `dependencies`:**
- Массив id других изменений которые должны быть применены раньше
- Пример: `"dependencies": ["html-1"]` — этот пункт применять только после html-1
- Пустой массив = нет зависимостей, можно применять в любом порядке

**Правила для `status`:**
- `pending` — не выполнено
- `done` — выполнено и проверено
- `skipped` — сознательно пропущено, причина в `notes`

### 4.7 Объект `verification` — чеклист после выполнения

```json
"verification": {
  "manual": [
    "Открыть вкладку Messages, выбрать тред — счётчик отображается",
    "Отправить сообщение — typing indicator появляется и исчезает",
    "Проверить тёмную тему — фоны корректны",
    "Проверить мобильный вид — переключатель колонок работает"
  ],
  "automated": [
    "npm run lint:css",
    "npm run test:unit -- messages"
  ]
}
```

**Правила:**
- `manual` — конкретные действия, не общие слова типа "протестировать"
- `automated` — реальные команды которые можно запустить
- Если автотестов нет — `"automated": []`, не удалять ключ

---

## 5. Полный пример плана

```json
{
  "plan": {
    "meta": {
      "id": "rfc-2025-001",
      "title": "Messages tab — привести к общей системе account page",
      "status": "approved",
      "version": "1.0.0",
      "created": "2025-10-14",
      "updated": "2025-10-14",
      "author": "frontend-team",
      "reviewer": "lead-dev",
      "rollback_reason": null
    },

    "scope": {
      "files": [
        "source/shop/customer-account/customer-account.html",
        "source/shop/customer-account/customer-account.css",
        "source/shop/customer-account/customer-account-messages.js"
      ],
      "components": ["MessagesController", ".messages-container", "#tab-correspondence"],
      "excluded": [
        "customer-account-orders.js",
        "customer-account-wishlist.js",
        "shared account layout (sidebar, .account-content-area)"
      ],
      "breaking_change": false
    },

    "audit": {
      "status": "passed",
      "conducted_by": "lead-dev",
      "conducted_at": "2025-10-14",
      "findings": [
        {
          "item_id": "html-2",
          "severity": "critical",
          "description": "План предлагал создать новый tab-header внутри section, но он уже существует выше в #tab-correspondence. Привело бы к дублированию заголовка.",
          "resolution": "Изменение переформулировано: card-header удаляется, [data-ref=thread-count] переезжает в уже существующий tab-header."
        }
      ]
    },

    "blocks": [
      {
        "block": "HTML",
        "file": "source/shop/customer-account/customer-account.html",
        "changes": [
          {
            "id": "html-1",
            "title": "Убрать карточные классы с section.messages-container",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<section class=\"messages-container card shadow-none shadow-md-sm d-flex flex-column overflow-hidden rounded-0 rounded-md-3\" aria-label=\"Seller Correspondence\">",
            "now": "<section class=\"messages-container d-flex flex-column overflow-hidden\" aria-label=\"Seller Correspondence\">",
            "why": "card, shadow-none, shadow-md-sm, rounded-0, rounded-md-3 создают вложенную карточку внутри .account-content-area которая сама уже карточка. Ни одна другая вкладка не создаёт собственной карточной обёртки.",
            "notes": null
          },
          {
            "id": "html-2",
            "title": "Удалить card-header, перенести [data-ref=thread-count] в существующий tab-header",
            "status": "pending",
            "risk": "medium",
            "dependencies": [],
            "was": "// [context] существующий tab-header:\n<span class=\"text-muted small fw-bold\">Support &amp; Sellers</span>\n\n// удаляемый card-header:\n<div class=\"card-header d-flex align-items-center gap-2 py-2\">\n  <span class=\"fw-semibold\">Correspondence</span>\n  <span class=\"badge text-bg-secondary ms-auto\" data-ref=\"thread-count\" aria-live=\"polite\" aria-label=\"Total threads\">0 threads</span>\n</div>",
            "now": "// tab-header с перенесённым счётчиком:\n<span class=\"text-muted small fw-bold\" data-ref=\"thread-count\" aria-live=\"polite\" aria-label=\"Total threads\">Support &amp; Sellers</span>\n\n// card-header удалён полностью",
            "why": "Заголовок уже существует в tab-header выше section. card-header дублирует его и создаёт чужеродный Bootstrap card-паттерн внутри не-карточного контекста. JS ищет [data-ref=thread-count] по атрибуту через querySelector — позиция в DOM не важна. _syncThreadCount() перезапишет текст при инициализации.",
            "notes": "Текст 'Support & Sellers' сохраняется как начальное содержимое — JS перезапишет его на '10 threads' при DOMContentLoaded."
          },
          {
            "id": "html-3",
            "title": "Убрать bg-body-tertiary с nav.msg-sidebar",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<nav class=\"msg-sidebar col-12 col-md-4 d-flex flex-column border-end bg-body-tertiary h-100\" aria-label=\"Seller threads\">",
            "now": "<nav class=\"msg-sidebar col-12 col-md-4 d-flex flex-column border-end h-100\" aria-label=\"Seller threads\">",
            "why": "bg-body-tertiary создаёт третий фоновый слой внутри контентной зоны. Разделение колонок уже обеспечивает border-end.",
            "notes": null
          },
          {
            "id": "html-4",
            "title": "Убрать bg-body-secondary и исправить py-2 на py-3 в шапке чата",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<div class=\"border-bottom px-3 py-2 bg-body-secondary d-flex align-items-center gap-2\">",
            "now": "<div class=\"border-bottom px-3 py-3 d-flex align-items-center gap-2\">",
            "why": "bg-body-secondary создаёт лишний фоновый слой. py-2 не соответствует вертикальному ритму проекта.",
            "notes": null
          },
          {
            "id": "html-5",
            "title": "Убрать bg-body-secondary с input bar",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<div class=\"border-top p-2 d-flex gap-2 align-items-end bg-body-secondary\">",
            "now": "<div class=\"border-top p-2 d-flex gap-2 align-items-end\">",
            "why": "Та же проблема что html-4 — лишний фоновый слой в нижней панели ввода.",
            "notes": null
          }
        ]
      },

      {
        "block": "CSS",
        "file": "source/shop/customer-account/customer-account.css",
        "changes": [
          {
            "id": "css-1",
            "title": "Удалить медиа-блок с border-radius !important",
            "status": "pending",
            "risk": "low",
            "dependencies": ["html-1"],
            "was": "@media (min-width: 768px) {\n  .messages-container {\n    border-radius: var(--bs-card-border-radius) !important;\n  }\n}",
            "now": "/* deleted */",
            "why": "Блок компенсировал rounded-0 на карточке. После html-1 карточки нет — компенсировать нечего. !important не используется нигде в shared стилях проекта.",
            "notes": null
          },
          {
            "id": "css-2",
            "title": "Убрать !important с мобильных display:none переключателей",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "@media (max-width: 767.98px) {\n  .messages-container.msg-mob-chat .msg-sidebar {\n    display: none !important;\n  }\n}\n@media (max-width: 767.98px) {\n  .messages-container:not(.msg-mob-chat) .msg-panel {\n    display: none !important;\n  }\n}",
            "now": "@media (max-width: 767.98px) {\n  .messages-container.msg-mob-chat .msg-sidebar {\n    display: none;\n  }\n}\n@media (max-width: 767.98px) {\n  .messages-container:not(.msg-mob-chat) .msg-panel {\n    display: none;\n  }\n}",
            "why": "Специфичность селектора (0,3,0) перебивает Bootstrap утилиты (0,1,0) без !important. Использование !important без необходимости затрудняет дальнейшее переопределение стилей.",
            "notes": null
          },
          {
            "id": "css-3",
            "title": "Исправить неверный Bootstrap токен в --msg-bubble-recv-bg",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "--msg-bubble-recv-bg: var(--bs-body-secondary);",
            "now": "--msg-bubble-recv-bg: var(--bs-secondary-bg);",
            "why": "var(--bs-body-secondary) — color токен (цвет текста), не background. var(--bs-secondary-bg) — правильный фоновый токен. В тёмной теме пузырь получал неверный цвет.",
            "notes": "В светлой теме визуальная разница минимальна. Проверять в тёмной теме."
          }
        ]
      },

      {
        "block": "JS",
        "file": "source/shop/customer-account/customer-account-messages.js",
        "changes": [
          {
            "id": "js-1",
            "title": "Изменений не требуется",
            "status": "skipped",
            "risk": "low",
            "dependencies": [],
            "was": "/* no changes */",
            "now": "/* no changes */",
            "why": "Все JS привязки идут через data-ref атрибуты которые сохранены во всех пунктах плана. _syncThreadCount() перезапишет содержимое [data-ref=thread-count] при инициализации независимо от позиции элемента в DOM.",
            "notes": "Блок включён для явного подтверждения что JS аудирован и не требует правок."
          }
        ]
      }
    ],

    "verification": {
      "manual": [
        "Открыть вкладку Messages — заголовок 'MESSAGES' и счётчик тредов отображаются в одной строке",
        "Счётчик показывает корректное число тредов (10 threads)",
        "Выбрать тред — имя продавца, order ID и статус-бейдж появляются в шапке чата",
        "Отправить сообщение — typing indicator появляется, исчезает, приходит bot-ответ",
        "Проверить светлую тему — фоны внутри Messages совпадают с фоном .account-content-area",
        "Проверить тёмную тему — входящие пузыри имеют корректный фон (не текстовый цвет)",
        "Сузить окно до 767px — отображается только сайдбар",
        "Выбрать тред на мобиле — переключается на панель чата, появляется кнопка Back",
        "Нажать Back — возврат к сайдбару"
      ],
      "automated": []
    }
  }
}
```

---

## 6. Правила именования id

```
rfc-YYYY-NNN        — id плана
html-N              — HTML изменение
css-N               — CSS изменение  
js-N                — JS изменение
config-N            — конфиг файлы (.env, package.json и т.д.)
other-N             — всё остальное
```

N — порядковый номер начиная с 1, сквозной по всему плану.

---

## 7. Правила качества `was` / `now`

| Требование | Правило |
|---|---|
| Источник | Код скопирован из реального файла, не написан по памяти |
| Контекст | Соседние строки для ориентира оборачиваются в `// [context]` |
| Удаление | `now` = `"/* deleted */"` |
| Добавление | `was` = `"/* new addition */"` |
| Нет изменений | `was` и `now` = `"/* no changes */"`, `status` = `"skipped"` |
| Форматирование | Переносы строк через `\n`, отступы сохраняются |

---

## 8. Правила аудита

Аудит — обязательный этап между `draft` и `approved`. Аудит проводит человек отличный от автора плана, или автор после паузы не менее 1 часа.

Аудит проверяет:

1. **DOM зависимости** — все `data-ref`, `id`, `class` используемые в JS существуют в `now` версии HTML
2. **CSS зависимости** — все классы из `was` CSS не используются в других компонентах за пределами scope
3. **Порядок применения** — `dependencies` заполнены корректно, нет циклических зависимостей
4. **Breaking changes** — если меняется публичный API или cross-component классы, `breaking_change: true`
5. **Дублирование** — `now` не создаёт элементы которые уже существуют в DOM

Каждая находка фиксируется в `audit.findings`. Критические находки исправляются в плане до смены статуса на `approved`.

---

## 9. Частичное применение и откат

**Частичное применение:**
Каждый `change` независим если `dependencies: []`. Можно применить только часть пунктов, выставив остальным `status: "skipped"` с причиной в `notes`.

**Откат:**
Поле `was` в каждом пункте — это инструкция отката. Применить в обратном порядке, учитывая `dependencies`. После отката выставить `meta.status: "rolled_back"` и заполнить `meta.rollback_reason`.

---

## 10. Версионирование плана

При изменении плана после создания — увеличивать `meta.version`:
- Патч (`1.0.0` → `1.0.1`) — исправление опечаток, уточнение `notes`
- Минор (`1.0.0` → `1.1.0`) — добавление новых `change` пунктов
- Мажор (`1.0.0` → `2.0.0`) — пересмотр scope, изменение уже выполненных пунктов, смена подхода

Обновлять `meta.updated` при каждом изменении.
