# assets-builder build report (2026-08-23T19:41:18.319438+00:00)

Mode: **extended** · Files: 12 (HTML: 3, CSS: 6, JS: 3)

## Classification
- **shared** (4): assets/css/base.css, assets/css/print.css, assets/css/shared.css, assets/js/main.js
- **page-specific** (2): assets/css/pages/shop.css, assets/js/pages/shop.js
- **orphan** (1): assets/css/unused.css
- **vendor** (2): assets/css/vendor/tiny-lib.min.css, assets/js/vendor/tiny-lib.min.js

## CSS conflicts
- `.btn` [medium] in assets/css/pages/shop.css, assets/css/shared.css — different properties — the cascade will combine them without loss
- `.card` [high] in assets/css/pages/shop.css, assets/css/shared.css — overlapping properties with different values: ['padding']
- `.container` [low] in assets/css/base.css, assets/css/print.css, assets/css/shared.css — overlapping properties, but the values match

## JS conflicts
- `initApp` [high] in assets/js/main.js, assets/js/pages/shop.js — same name, different body — the last definition silently wins when concatenated

## External resources (not merged — keep in HTML manually)
- index.html: `https://cdn.example.com/analytics.js` (js-src)

## Domino: most influential shared files
- `assets/css/base.css` — affects 3 page(s).
- `assets/css/print.css` — affects 3 page(s).
- `assets/css/shared.css` — affects 3 page(s).
- `assets/js/main.js` — affects 3 page(s).

## Extended mode: usage
- Unused CSS classes/IDs (4): .never-linked, .tl-col, .tl-row, .unused-badge
- Possibly dynamic CSS (0): —
- Unused JS functions/variables (2): legacyHelper, tl

## Cache
- Reused from cache: 0, rescanned: 12