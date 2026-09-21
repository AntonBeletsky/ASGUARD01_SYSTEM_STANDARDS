# Формат заголовков-комментариев в `style.css` / `scripts.js`

Ниже — реальный вывод скрипта (не придуманный образец), чтобы при написании summary пользователю модель ссылалась на настоящий формат.

## Оглавление (верх файла)

```css
/* ============================================================
   TABLE OF CONTENTS
   ============================================================
   - assets/css/vendor/tiny-lib.min.css  [vendor] | used on: about.html, index.html, shop.html
   - assets/css/base.css  [shared] | used on: about.html, index.html, shop.html
   - assets/css/pages/shop.css  [page-specific] | used on: shop.html
   - assets/css/unused.css  [orphan]
   ============================================================ */
```
(`--comment-lang ru` даёт тот же блок с заголовком `ОГЛАВЛЕНИЕ`.)

## Заголовок секции (перед каждым исходным файлом)

Обычный файл без проблем:
```css
/* ============================================================
   FILE: assets/css/base.css
   SCOPE: shared
   USED ON: about.html, index.html, shop.html
   SIZE: 92 bytes | 8 lines
   ============================================================ */
```

С зависимостью (`@import`) и конфликтом:
```css
/* ============================================================
   FILE: assets/css/shared.css
   SCOPE: shared
   USED ON: about.html, index.html, shop.html
   SIZE: 240 bytes | 19 lines
   DEPENDS ON: assets/css/base.css, assets/css/print.css
   CONFLICTS: .btn (severity: medium); .card (severity: high); .container (severity: low)
   ============================================================ */
```

Orphan-файл (не подключён нигде, но не удаляется — только помечается):
```css
/* ============================================================
   FILE: assets/css/unused.css
   SCOPE: orphan
   ⚠ ORPHAN — not linked from any scanned HTML page
   SIZE: 32 bytes | 4 lines
   ============================================================ */
```

С пометкой extended-режима (класс/функция не найдены в использовании):
```
⚠ UNUSED (по данным анализа): .unused-badge (unused)
```
или для случая "возможно используется динамически" (никогда не удаляется даже с `--strip-unused`):
```
⚠ UNUSED (по данным анализа): .js-active-state (dynamic-suspect)
```

## `@import` с медиа-условием

Если файл был импортирован как `@import url("print.css") print;`, его секция в выводе оборачивается в `@media`, чтобы не потерять исходную семантику:
```css
/* ============================================================
   FILE: assets/css/print.css
   SCOPE: shared
   ...
   ============================================================ */
@media print {
.container { display: none; }
}
```

## Order-conflict баннер (только `scripts.js`, только если реально обнаружен)

Ставится сразу после TOC, до первой секции:
```css
/* ############################################################
   ВНИМАНИЕ: обнаружен противоречивый порядок подключения JS
   между страницами — авто-сортировка не может угодить обеим.
   - a.js vs b.js:
       page1.html: a.js -> b.js
       page2.html: b.js -> a.js
   Итоговый порядок ниже — best-effort (topological + first-seen).
   ############################################################ */
```
Если видишь этот баннер в собранном файле — значит `WF-3` уже должен был остановить процесс до `build` и спросить пользователя; баннер также появляется в `warn`-режиме, если пользователь осознанно согласился продолжить.

## После `--strip-unused`

Удалённое правило заменяется однострочным маркером, а не пропадает бесследно:
```css
/* removed by --strip-unused: .definitely-unused */
```
