# Разобранный пример: реальный прогон на тестовой фикстуре

Ниже — фактический `build-report.json`, полученный при валидации `assets-builder.py` (см. `fixture-example.tar.gz` из поставки скрипта), не придуманный пример. 3 страницы (`index.html`, `about.html`, `shop.html`), 6 CSS и 3 JS файла, `--mode extended`.

## Ключевые поля отчёта

```json
{
  "meta": { "mode": "extended", "totalFiles": 12, "htmlPages": 3, "cssFiles": 6, "jsFiles": 3 },
  "classification": {
    "shared": ["assets/css/base.css", "assets/css/print.css", "assets/css/shared.css", "assets/js/main.js"],
    "page-specific": ["assets/css/pages/shop.css", "assets/js/pages/shop.js"],
    "orphan": ["assets/css/unused.css"],
    "vendor": ["assets/css/vendor/tiny-lib.min.css", "assets/js/vendor/tiny-lib.min.js"]
  },
  "conflicts": {
    "css": [
      {"name": ".btn", "files": ["...shop.css", "...shared.css"], "severity": "medium"},
      {"name": ".card", "files": ["...shop.css", "...shared.css"], "severity": "high",
       "detail": "совпадающие свойства с разными значениями: ['padding']"},
      {"name": ".container", "files": ["base.css","print.css","shared.css"], "severity": "low"}
    ],
    "js": [{"name": "initApp", "files": ["main.js", "shop.js"], "severity": "high"}],
    "jsOrder": []
  },
  "externalAssets": [{"page": "index.html", "href": "https://cdn.example.com/analytics.js", "kind": "js-src"}],
  "usage": {
    "unusedCss": [".never-linked", ".tl-col", ".tl-row", ".unused-badge"],
    "dynamicSuspectCss": [],
    "unusedJs": ["legacyHelper", "tl"]
  },
  "output": {"cssSizeBytes": 3297, "jsSizeBytes": 1757, "originalCssBytes": 564, "originalJsBytes": 353}
}
```

**Замечание про размер**: `output` показывает, что итоговый файл (3297 байт) БОЛЬШЕ суммы исходников (564 байта) — это ожидаемо на маленьком тестовом проекте: заголовки-комментарии имеют фиксированный размер на файл, а сами файлы тут крошечные. На реальном проекте с файлами по несколько КБ доля комментариев в итоговом размере будет незначительной. Если пользователь удивится росту размера — объясни это, а не скрывай.

## Разбор по WF-3 (гейт)

`.card` и `initApp` — `severity: "high"` → это ровно тот случай, когда WF-3 требует остановиться и спросить пользователя, а не переходить к `build` молча. `.btn` (medium) и `.container` (low) — не блокируют. `jsOrder` пуст — противоречий порядка между страницами нет.

## Пример финального ответа пользователю (WF-6)

После того как пользователь подтвердил (или не было блокирующих конфликтов) и `build` выполнен:

> Собрал 9 внутренних CSS/JS файлов (+ 2 vendor) с 3 страниц в `style.css` и `scripts.js`.
>
> Конфликты:
> - `.card` — в `shared.css` и `shop.css` разный `padding` (10px / 20px). Оставил оба с пометкой в комментариях; по порядку каскада побеждает вариант из `shop.css` (20px), так как он идёт позже.
> - `initApp` — одноимённая функция с разным телом в `main.js` и `shop.js`. Аналогично оставил обе с явным предупреждением — стоит решить в исходниках, какая версия нужна, скрипт сам их не сливает.
> - `.btn` и `.container` определены в нескольких файлах, но без реального конфликта — упоминаю для полноты, ничего делать не нужно.
>
> Расширенный анализ нашёл 4 потенциально неиспользуемых CSS-класса и 2 JS-функции (включая `legacyHelper`) — оставил в файле с пометкой, ничего не удалил.
>
> Не забудьте: `analytics.js` (внешний, с CDN) не вошёл в сборку — его нужно оставить в `index.html` вручную, иначе аналитика перестанет подключаться.

Это калибровочный пример тона и объёма — не шаблон для копирования дословно на каждый ответ.
