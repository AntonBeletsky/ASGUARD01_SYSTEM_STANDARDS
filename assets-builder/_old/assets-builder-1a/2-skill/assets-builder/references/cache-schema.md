# Формат `build-report.json` и `.assets-builder-cache.json`

Оба файла — реальный вывод скрипта (см. пример полного отчёта в `references/sample-build-report.md`). Здесь — что означает каждое поле.

## `build-report.json` (читать в WF-2/WF-3/WF-6 — основной источник решений)

```json
{
  "meta": { "generatedAt": "...", "mode": "extended", "totalFiles": 12, "htmlPages": 3, "cssFiles": 6, "jsFiles": 3 },
  "classification": { "shared": [...], "page-specific": [...], "orphan": [...], "vendor": [...] },
  "conflicts": {
    "css": [ { "conflict_type": "css-selector", "name": ".card", "files": [...], "severity": "high", "detail": "..." } ],
    "js":  [ { "conflict_type": "js-symbol", "name": "initApp", "files": [...], "severity": "high", "detail": "..." } ],
    "jsOrder": [ { "files": [...], "page_a": "...", "order_a": [...], "page_b": "...", "order_b": [...] } ]
  },
  "externalAssets": [ { "page": "index.html", "kind": "js-src", "href": "https://...", "line": 6 } ],
  "dominoTop": [ { "file": "assets/css/base.css", "affectedPages": 3 } ],
  "cache": { "reused": 0, "rescanned": 12 },
  "usage": {
    "unusedCss": [".never-linked", "..."],
    "dynamicSuspectCss": [],
    "unusedJs": ["legacyHelper", "..."]
  },
  "output": { "css": "/abs/path/style.css", "js": "/abs/path/scripts.js", "cssSizeBytes": 3297, "jsSizeBytes": 1757, "originalCssBytes": 564, "originalJsBytes": 353 }
}
```

**Что читать для WF-3 (гейт)**: `conflicts.css[].severity`, `conflicts.js[].severity`, `conflicts.jsOrder` (пустой массив = нет проблем; непустой = блокирующая ситуация независимо от `severity`, т.к. `jsOrder` по своей природе всегда требует решения человека).

**`usage` присутствует только при `--mode extended`** — в `basic` этого ключа нет, а не пустой объект. Проверяй через `"usage" in report`, а не `report.get("usage", {})`, если важно различить "extended, но пусто" от "basic".

**`output` присутствует только у `build`**, не у `scan`.

## `.assets-builder-cache.json` (обычно не нужно читать напрямую — статистика уже в `report["cache"]`)

```json
{
  "cacheVersion": 1,
  "generatedAt": "...",
  "projectRoot": "/abs/path",
  "files": { "assets/css/base.css": { "hash": "...", "size": 92, "mtime": "...", "type": "css" } },
  "parsedCss": { "assets/css/base.css": [ { "selector": ".container", "declarations": {"max-width": "1100px"}, "line": 4 } ] },
  "parsedJs":  { "assets/js/main.js":   [ { "name": "initApp", "line": 1, "body_hash": "a2460a4e" } ] },
  "cssSelectors": { "...": "то же, что usage.cssSelectors в отчёте, если extended" },
  "jsSymbols":    { "...": "аналогично для JS" },
  "conflicts": [ "плоский список css+js конфликтов, как в conflicts.css + conflicts.js отчёта" ]
}
```

`parsedCss`/`parsedJs` — то, что реально ускоряет повторные запуски: при неизменившемся хеше файла эти записи переиспользуются вместо повторного парсинга. Если файл удалить из кеша вручную — ничего не сломается, просто следующий `build` пересчитает его как изменённый.

Не путай `cssSelectors`/`jsSymbols` в кеше (плоская карта по имени селектора/функции, агрегированная по всему проекту) с `parsedCss`/`parsedJs` (по каждому файлу отдельно, до агрегации).
