# Отчёт сборки assets-builder (2026-08-19T19:10:36.342109+00:00)

Режим: **extended** · Файлов: 12 (HTML: 3, CSS: 6, JS: 3)

## Классификация
- **shared** (4): assets/css/base.css, assets/css/print.css, assets/css/shared.css, assets/js/main.js
- **page-specific** (2): assets/css/pages/shop.css, assets/js/pages/shop.js
- **orphan** (1): assets/css/unused.css
- **vendor** (2): assets/css/vendor/tiny-lib.min.css, assets/js/vendor/tiny-lib.min.js

## Конфликты CSS
- `.btn` [medium] в assets/css/pages/shop.css, assets/css/shared.css — разные свойства — каскад скомбинирует без потерь
- `.card` [high] в assets/css/pages/shop.css, assets/css/shared.css — совпадающие свойства с разными значениями: ['padding']
- `.container` [low] в assets/css/base.css, assets/css/print.css, assets/css/shared.css — пересекающиеся свойства, но значения совпадают

## Конфликты JS
- `initApp` [high] в assets/js/main.js, assets/js/pages/shop.js — разное тело у одинакового имени — при конкатенации последнее определение молча победит

## Внешние ресурсы (не включены в сборку — оставить в HTML вручную)
- index.html: `https://cdn.example.com/analytics.js` (js-src)

## Домино: наиболее влиятельные общие файлы
- `assets/css/base.css` — затрагивает 3 стр.
- `assets/css/print.css` — затрагивает 3 стр.
- `assets/css/shared.css` — затрагивает 3 стр.
- `assets/js/main.js` — затрагивает 3 стр.

## Расширенный режим: использование
- Неиспользуемые CSS-классы/ID (4): .never-linked, .tl-col, .tl-row, .unused-badge
- Возможно динамические CSS (0): —
- Неиспользуемые JS-функции/переменные (2): legacyHelper, tl

## Кеш
- Переиспользовано из кеша: 0, пересканировано: 12