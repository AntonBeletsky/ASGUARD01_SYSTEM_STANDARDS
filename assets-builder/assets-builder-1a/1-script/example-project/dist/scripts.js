/* ============================================================
   TABLE OF CONTENTS
   ============================================================
   - assets/js/vendor/tiny-lib.min.js  [vendor] | used on: about.html, index.html, shop.html
   - assets/js/main.js  [shared] | used on: about.html, index.html, shop.html
   - assets/js/pages/shop.js  [page-specific] | used on: shop.html
   ============================================================ */
/* ============================================================
   FILE: assets/js/vendor/tiny-lib.min.js
   SCOPE: vendor
   USED ON: about.html, index.html, shop.html
   SIZE: 25 bytes | 2 lines
   ⚠ UNUSED (по данным анализа): tl
   ============================================================ */
function tl(a){return a}

/* ============================================================
   FILE: assets/js/main.js
   SCOPE: shared
   USED ON: about.html, index.html, shop.html
   SIZE: 187 bytes | 11 lines
   CONFLICTS: initApp (severity: high)
   ⚠ UNUSED (по данным анализа): legacyHelper
   ============================================================ */
function initApp() {
  console.log('app init');
}
function showToast(msg) {
  console.log('toast:', msg);
}
function legacyHelper() {
  console.log('never called anywhere');
}
initApp();

/* ============================================================
   FILE: assets/js/pages/shop.js
   SCOPE: page-specific
   USED ON: shop.html
   SIZE: 141 bytes | 8 lines
   CONFLICTS: initApp (severity: high)
   ============================================================ */
function initApp() {
  console.log('shop app init - different body');
}
function addToCart(id) {
  showToast('added ' + id);
}
addToCart(1);
