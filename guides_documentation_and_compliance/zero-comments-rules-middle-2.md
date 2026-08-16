# Zero-Level Documentation Standards — Middle Grade
### One comment per logical unit. Every single one of them closed.

> **Research & incident basis:** Envato/ThemeForest author requirements, idiomatic-css
> (necolas), CSS Guidelines (cssguidelin.es), Google JavaScript Style Guide, JSDoc 3
> standard, WordPress Coding Standards (CSS + JS), and the internal full/lite guides —
> plus a full character-by-character audit of `customer-account-sandbox-build-2d.html`
> (12,012 lines) that checked every comment in the file rather than sampling one.

| Scope | Comments found | Broken |
|---|---|---|
| CSS `/* */` (lines 61–2344) | 198 opening `/*` / 196 closing `*/` | **2** |
| JS `/* */` and `//` (lines 5018–12006) | 159 block + 700 line | 0 |
| HTML `<!-- -->` in markup | 291 | 0 |
| HTML `<!-- -->` inside JS template literals | 5 | 0 |

Both breaks were in CSS — isolated typos in otherwise-correct sections: Wallet card
typography and the Promotions `.ls-wide` utility. JS and HTML were both 100% clean
across every category checked, including the easy-to-miss case of HTML comments
written inside JS template strings that only become real markup once rendered into
the DOM. That clean record is exactly why this guide treats termination discipline
as a habit for every language covered here, not a patch for the one language that
slipped once.

---

## Core Principle

**Comment density = one block per logical unit.**

A "logical unit" is any named section, component, class, public method, or non-obvious
pattern. Everything inside that unit that is self-explanatory gets no comment.
Everything that isn't obvious gets one inline note — one line, one sentence.

```
                   ┌─────────────────────────────────────────────┐
  zero-comments    │  Comments only on tricky inline lines        │  ← too sparse
  -lite.md         │  Large sections uncommented                  │
                   └─────────────────────────────────────────────┘

                   ┌─────────────────────────────────────────────┐
  THIS GUIDE  →    │  Header block per section / component        │  ← target
                   │  JSDoc per public method                     │
                   │  One-line "why" on non-obvious properties    │
                   └─────────────────────────────────────────────┘

                   ┌─────────────────────────────────────────────┐
  zero-comments    │  Multi-line block per individual property    │  ← too dense
  -rules.md        │  Paragraph explanations everywhere           │
                   └─────────────────────────────────────────────┘
```

But writing the right amount is only half the job. **A comment is not "done" when
the wording is right. It's done when it's closed.** An unclosed comment is not a
style problem — it is a deletion. It doesn't warn you, doesn't fail a build, and
usually doesn't throw in the browser (not always — see *The Double Comment* family
later in this guide for the exceptions). The rule it swallowed simply stops
existing, and the file still looks complete, until someone notices a font size, a
letter-spacing, or an entire breakpoint is missing, with no clue in sight as to why.

Every rule in this guide about *how much* to write assumes the comment actually
closes. The two absolute rules below are what make that assumption safe.

---

## ⚠ Absolute Ban: No Numbering in Comments

**Numbering in comments is forbidden in every form, without exception.**

This means: no arabic numerals, no roman numerals, no letters used as indices,
no "Step X", no "Part X", no paragraph markers, no ordered-list prefixes,
no "first / second / third" used as structural labels.

Comments are written for human readers, not for outlining tools.
A human writer navigating a large stylesheet uses names and visual weight —
not a numeric index. The moment you number a comment, you are writing
documentation structure, not a human remark.

```css
/* ✗ FORBIDDEN — every variant of this pattern */

/* — 1. Container layout ───────────────────── */
/* — 2. Child elements ─────────────────────── */

/* Step 1: reset */
/* Part A: tokens */
/* 0. Tokens */
/* 3.1 Public API */
```

```css
/* ✓ CORRECT — name the concept, not the sequence */

/* ─── CONTAINER LAYOUT ──────────────────────── */
/* container layout */

/* reset */
/* tokens */
```

If you feel the urge to number something, it means you have not found
the right name for it yet. Find the name. Drop the number.

---

## ⚠ Absolute Rule: No Comment Ships Unclosed

**Every `/*` gets its own `*/` before the next real line of code. Every time. No
exception for "I'll close it after the last sentence," and none for short, one-off
remarks.**

This is what actually happened in the Wallet section of this exact codebase — real
code, real line numbers, from the audit above:

```
        /* ─── COMPONENT: CARD TYPOGRAPHY ────────────────────────────
           font-size uses container-query units (cqw) — Bootstrap fs-*
           utilities do not cover cqw, so these classes are intentionally
           kept as scoped CSS rather than replaced with Bootstrap utilities.
           These are CSS classes, not inline style= attributes.

        .wallet-container .wallet-card-label {     ← looks like code. Is comment text.
            font-size: 2.5cqw;                       ← looks like code. Is comment text.
        }

        .wallet-container .wallet-card-value {     ← looks like code. Is comment text.
            font-size: 3.2cqw;                       ← looks like code. Is comment text.
        }

        /* ─── COMPONENT: ICON SIZES ──────────────────────────────────
           18px = inline icon inside dropdown buttons.
           48px = large icon in the Add Card placeholder.
           Bootstrap fs-* utilities do not map to these exact sizes. */
           ↑ this closing */ ends the FIRST comment (opened 17 lines up), not
             this one — the two rules above, and this header's own text, were
             never real CSS.
```

The forgotten `*/` belonged at the end of the description — right after
"attributes." — three lines before the first swallowed selector. Nothing after
it is code until the parser finds a `*/` somewhere, and it always will, because
another comment is always coming soon. That's why this bug hides so well: the
file still *reads* like a complete, well-commented stylesheet, top to bottom.

Seventy lines earlier in the same file, the same author wrote the identical
pattern and closed it correctly:

```css
        /* ─── THEME TOKENS ───────────────────────────────────────────
           Card gradient presets — assign a --wallet-gradient-* variable
           to any .wallet-card via a .wallet-bg-* utility class.
           To add a new theme, define a --wallet-gradient-[name] token
           here and a corresponding .wallet-bg-[name] rule in the
           Theme Gradients section below. */
```

This is not a knowledge gap. It's a single dropped keystroke, in an otherwise
identically-formatted comment, by an author who got the same pattern right 194
other times in the same file. That's the actual danger: discipline this
repetitive needs a mechanical backstop, not just care — which is exactly what
the rest of this section provides.

---

## Why This Failure Is Silent — and Not Always the Same Failure

A missing semicolon breaks the next rule and something visibly collapses. A
misspelled class name matches nothing, and dev tools flag it instantly. An
unclosed comment usually does neither — though, as *The Undying Method* and
*The Double Comment* show later in this guide, "usually" is doing some work in
that sentence.

- **CSS and HTML never validate comment contents.** Anything between `/*` and
  the next `*/` — or between `<!--` and the next `-->` — including perfectly
  valid selectors, declarations, and markup, is just text to the parser. No
  syntax error is possible, because nothing inside a comment is ever parsed
  as code.
- **The browser never complains.** No console warning, no failed rule, no red
  underline. The rule simply isn't there — the same as if it had never been
  written at all.
- **The file still reads correctly to a human.** A swallowed section header
  keeps its dash-bar formatting. A skim-review sees
  `/* ─── COMPONENT: ICON SIZES ─── */` and moves on, never suspecting it's
  sitting inside someone else's comment.
- **JS is the interesting middle case.** A JSDoc block left open is silent
  exactly as often as CSS — right up until the moment there's no *later* `*/`
  anywhere in the file to accidentally close it, at which point it becomes a
  hard `SyntaxError`. In a file with 159 block comments, there is almost
  always a later one to swallow into. That's why the JS trailing-description
  case in this guide (*The Vanishing Method*) is silent, and why nesting a
  comment inside a JSDoc'd method (*The Undying Method*) is not.
- **The only reliable signal is a count.** Total `/*` must equal total `*/` in
  any file that doesn't intentionally nest markers (and comments must never
  nest — see *The Double Comment* family below). That's the entire mechanism
  behind the audit that caught this bug: 198 opens, 196 closes in CSS, delta
  2, three rules gone — against 159 JS block comments and 291 HTML comments
  that all closed exactly where they should have.

Treat every comment block the way you'd treat an opening bracket or quote:
closing it is not optional, and "I'll get it at the end" is exactly how this
bug ships.

---

## The Delimiter-First Technique

The fix is a writing habit, not a proofreading step.

**Never write the opening delimiter and plan to add the closer later.** Write
both delimiters first, in the same motion, then fill in the text between them.

```
✗ HOW THIS BUG HAPPENS                    ✓ HOW TO PREVENT IT

Type /*                                   Type /**/
Type the description                      Move the cursor between the
Type more description                       two `*/` markers
Move to the next line to add              Type the description inside —
  the code                                  the closer is already there
Forget the closer ever needed to          Add line breaks inside as needed
  be added
```

This applies to every block comment in every language this guide covers: CSS
`/* */`, JS `/** */`, and HTML `<!-- -->`. If the closer exists before you
start typing content, it cannot be forgotten — only moved on purpose.

---

## Mandatory Delimiter Balance Check

Add this to the Pre-Release Checklist at the end of this guide. Run it on any
file where a comment was added, edited, or moved — not just once at the very
end.

**Manual scan:** read top to bottom. Every `/*` must be immediately followed,
within that same block, by its own `*/`. If you reach a selector or property
line while still "inside" a comment you opened earlier, stop — that comment is
unterminated.

**Automated check**, whenever shell access is available:

```bash
opens=$(grep -o '/\*' style.css | wc -l)
closes=$(grep -o '\*/' style.css | wc -l)
echo "opens=$opens closes=$closes"
# These must be exactly equal. Any other result means at least one
# comment in the file is unterminated (or, rarer, an orphaned closer
# exists with no matching opener — see "The Double Comment").
```

If the CSS lives inside an inline `<style>` block in an HTML file, isolate that
block's line range before counting — this is literally how the audit above
scoped its own check:

```bash
sed -n '61,2344p' customer-account-sandbox-build-2d.html > /tmp/inline.css
opens=$(grep -o '/\*' /tmp/inline.css | wc -l)
closes=$(grep -o '\*/' /tmp/inline.css | wc -l)
echo "opens=$opens closes=$closes"   # → opens=198 closes=196
```

The same scoping applies to inline `<script>` blocks:

```bash
sed -n '5018,12006p' customer-account-sandbox-build-2d.html > /tmp/inline.js
```

**Known limitations.** A naive grep count has two blind spots that a real
character-by-character parser accounts for and a quick count will not:

- **Comment-like text inside quoted strings.** `content: "/* not a comment */";`
  in CSS, or a JS string containing the literal characters `/*`, inflates both
  counts and can mask a real imbalance if it happens to inflate both sides
  equally.
- **Division vs. line comment, and regex literals, in JS.** `a / b` is not the
  start of a comment; `/pattern/g` is a regex literal, not two stray slashes.
  Counting raw `/` characters in JS is meaningless — count `/*` and `*/`
  specifically, and even then treat the result as a strong signal, not proof.

A count that comes back balanced is a good sign, not a guarantee — see *The
Double Comment* below for a case where the count is balanced and the file is
still broken. A count that comes back unbalanced is unambiguous: something in
that file is broken, full stop.

This is the exact check — at this level of rigor — that found the Wallet and
Promotions bugs and confirmed everything else in the file was clean: 159 JS
block comments, 291 HTML comments in markup, and 5 HTML comments embedded in
JS template literals, all correctly paired.

---

## Failure Pattern Index

Eight known mechanisms account for nearly every case of this bug across CSS,
JS, and HTML. Two are the exact incidents from the Customer Account Page
audit. The rest are the same mechanisms, extrapolated to the other places —
and the other languages — where they're most likely to recur. Each is worked
in full, wrong and correct side by side, where it naturally comes up in the
JavaScript, CSS, and HTML sections below.

| Mechanism | CSS | JS | HTML |
|---|---|---|---|
| Trailing Description | **Wallet card typography** — real incident | The Vanishing Method | The Vanishing Region |
| Aside That Never Ends | **Promotions `.ls-wide`** — real incident | The Short-Lived Field | The Silent Accommodation |
| Padding Slip | The Padding Slip | not applicable — see note | not applicable — see note |
| Double Comment | The Double Comment | The Undying Method | The Reappearing Element |
| Merged Header (edit-time) | The Merged Header | same mechanism — see note | same mechanism — see note |
| Media Query Swallow (blast radius) | The Media Query Swallow | The Long Stretch | folded into The Vanishing Region |
| Templated Comment (HTML rendered from JS) | not applicable | The Templated Comment | The Templated Comment |

*Padding Slip doesn't transfer to JS because its section headers are `//` line
comments, which close themselves on every line by construction — see the note
under JS Section Headers below. It doesn't get a separate HTML case either,
for the opposite reason: HTML has no line-comment syntax at all, so every HTML
comment, however short, already carries the exact risk Padding Slip
describes — there's no "short, safe version" to contrast it with.*

*Merged Header is an editing-workflow risk, not a syntax risk — the mechanism
is identical in JS and HTML, just wearing different delimiters. One detailed
example makes the point; it's repeated briefly, not in full, where it comes up
for the other two languages.*

Most of these patterns share one symptom: a rule or block silently stops
applying, with no error anywhere. The Double Comment family is the exception —
in CSS it produces a broken, often-visible rule; in JS (*The Undying Method*)
it produces a `SyntaxError`, and, stranger still, the code it was meant to
disable stays fully active. Worth knowing precisely because it's tempting to
assume every comment bug is silent when only some are.

---

## Comment Decision Tree

Before writing any comment, run this check:

```
Is this a top-level section boundary (layout zone, major feature area)?
  └─ YES → Write a top-level section header (see §CSS Two-Tier Hierarchy)

Is this a sub-section or component group within a section?
  └─ YES → Write a sub-section marker (see §CSS Two-Tier Hierarchy)

Is this a JS class or public method?
  └─ YES → Write a JSDoc block (see §JavaScript)

Is the code self-evident from its name and structure?
  └─ YES → Write nothing

Does this line use a non-obvious pattern, browser workaround,
performance tradeoff, or security measure?
  └─ YES → Write one inline comment explaining WHY (not WHAT)

Everything else → no comment needed
```

---

## JavaScript

### Class Header (JSDoc)

Every class gets a single JSDoc block. Max 3 lines of description.
Include `@param` only for constructor arguments that are not obvious from the name.

```js
/**
 * Controls tab navigation and URL-hash-based deep linking for the account page.
 * Replaces default Bootstrap tab behavior to support direct URL access and
 * browser back/forward navigation.
 *
 * @param {string} selector - CSS selector for the root container element.
 */
class AccountPageController {
```

---

### Public Methods (JSDoc)

Public methods that form the component's API get a JSDoc block.
One-sentence description + `@param` / `@returns` only when the types or purpose
are not obvious from the name.

```js
/**
 * Activates the tab matching the given id and updates the URL hash.
 *
 * @param {string} tabId - Must match the `id` of a `.tab-pane` element.
 */
navigate(tabId) {

/**
 * Removes all event listeners and resets component state.
 * Call this before removing the component from the DOM.
 */
destroy() {
```

Private and internal helper methods get **no JSDoc** — use a single `//` line
only if the logic is non-obvious.

```js
// Normalize the hash value: strip leading "#" and decode URI encoding.
_parseHash(raw) {
```

---

### The Vanishing Method

JS faces the same risk as CSS, but only for block comments. The
`// ─── SECTION ───` headers shown further down close themselves on every
line, so they're never at risk. JSDoc blocks are.

```js
/* ✗ WRONG — closer missing after "URL hash." */

/**
 * Activates the tab matching the given id and updates the URL hash.
 *
 * @param {string} tabId - Must match the `id` of a `.tab-pane` element.
navigate(tabId) {
  this._activeTab = tabId;
  location.hash = tabId;
}

/**
 * Removes all event listeners and resets component state.
 * Call this before removing the component from the DOM.
 */
destroy() {
  this._ac.abort();
}
```

Because `destroy`'s own JSDoc block happens to supply the next `*/`, the
parser finds a legal place to stop — just far later than intended. `navigate`
never throws a syntax error. It simply stops being a method: both its JSDoc
and its body are now comment text. Calling `controller.navigate('overview')`
later fails at runtime with "not a function," nowhere near the actual mistake.

```js
/* ✓ CORRECT */

/**
 * Activates the tab matching the given id and updates the URL hash.
 *
 * @param {string} tabId - Must match the `id` of a `.tab-pane` element.
 */
navigate(tabId) {
  this._activeTab = tabId;
  location.hash = tabId;
}
```

**Rule:** don't assume JS "just throws" when a comment is left open. It only
throws if no later `*/` exists anywhere in the file. In any class with more
than one JSDoc'd method — which is most of them — a later block supplies an
accidental closer, and the failure is exactly as silent as CSS.

---

### The Undying Method

The mirror image of *The Vanishing Method* — and the reason "comment it out
to disable it" is dangerous in JS, not just CSS. JS comments don't nest
either. Wrapping a JSDoc'd method in `/* */` puts a `/**` (itself starting
with `/*`) inside the wrapper, which does nothing special, and puts the
JSDoc's own `*/` right where the wrapper's closer should be.

```js
/* ✗ WRONG — nested comment closes early, and throws */

/*
/**
 * Removes all event listeners and resets component state.
 */
destroy() {
  this._ac.abort();
}
*/
```

The outer `/*` closes at the *first* `*/` the parser meets — the one ending
the JSDoc block, right before `destroy() {`. That means `destroy() { ... }`
is no longer inside any comment. It's live, callable code — the opposite of
"disabled." Parsing then reaches the final `*/` on its own line: a bare `*`
where a new statement is expected, which JS cannot parse. Result: a
`SyntaxError` that stops the whole file from loading, on a line that looks
completely disabled to anyone reading it.

```js
/* ✓ CORRECT — delete the method, don't comment it out */

// Method removed: destroy() logic moved to the shared unmount() lifecycle hook.
```

**Rule:** never wrap a block in a comment if it might already contain one —
and don't leave disabled code in a shipped file at all (see *Remove* in the
Pre-Release Checklist). If a method needs to go, delete it. If the reason
matters, say so in one line; don't preserve the dead code to explain itself.

---

### JS Section Headers — Two Tiers

Inside a class, use the dash-bar format for every logical group.
All caps, no numbers, no letters used as ordinals.

```js
class AccountPageController {

  // ─── STATIC CONFIGURATION ────────────────────────────────────────────
  // ─── CONSTRUCTOR ─────────────────────────────────────────────────────
  // ─── PRIVATE STATE ───────────────────────────────────────────────────
  // ─── EVENT BINDING ───────────────────────────────────────────────────
  // ─── ROUTING ─────────────────────────────────────────────────────────
  // ─── RENDERING ───────────────────────────────────────────────────────
  // ─── PUBLIC API ──────────────────────────────────────────────────────
  // ─── TEARDOWN ────────────────────────────────────────────────────────
}
```

Every one of these is a `//` line comment, not a `/* */` block. A line comment
closes itself the instant the line ends — there's no delimiter to forget, and
no fill-dash editing that could trim one away. This is why *The Padding Slip*
(the CSS case of a hand-adjusted header losing its closer, later in this
guide) has no JS equivalent: the format that would be at risk simply isn't
used here.

---

### Inline "Why" Comments

One line only. Explains the architectural decision, not the syntax.

```js
// ─── STATIC CONFIGURATION ────────────────────────────────────────────

// Guards against Prototype Pollution when merging external data objects.
static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);


// ─── CONSTRUCTOR ─────────────────────────────────────────────────────

// AbortController lets all listeners be removed in one call during teardown.
this._ac = new AbortController();

const sig = { signal: this._ac.signal };

// ─── EVENT BINDING ───────────────────────────────────────────────────

// Event Delegation: one listener on the parent handles all current and future items.
this._list.addEventListener('click', this._onItemClick.bind(this));

// Scoped to this._root so identical components on the same page don't interfere.
this._q = (sel) => this._root.querySelector(sel);

// ─── ROUTING ─────────────────────────────────────────────────────────

// Reacts to browser back/forward navigation via the URL hash.
window.addEventListener('hashchange', () => this._handleHash(), sig);

// ─── TEARDOWN ────────────────────────────────────────────────────────

// Calling abort() removes every listener registered with this._ac.signal.
this._ac.abort();
```

---

### The Short-Lived Field

The same failure as *The Aside That Never Ends* in CSS: a short note, written
as if it were a one-liner, split across a blank line before it closes.

```js
/* ✗ WRONG */

class AccountPageController {

  // ─── CONSTRUCTOR ─────────────────────────────────────────────────────

  /* 280ms matches the CSS transition duration for .tab-pane, so the active

  this._transitionMs = 280;
  this._activeTab = null;
  // ...rest of the class continues here, including a later /* */ block
  // that accidentally supplies the closer for the comment opened above
```

`this._transitionMs = 280;` is now comment text, not a field assignment. The
class body still parses — `_activeTab` and everything after it are fine,
because a later comment further down in the class supplies the accidental
`*/` — but `this._transitionMs` is `undefined` everywhere it's read. Any code that
does `setTimeout(fn, this._transitionMs)` now fires with `NaN`, and nothing
about that error points back to a comment.

```js
/* ✓ CORRECT */

class AccountPageController {

  // ─── CONSTRUCTOR ─────────────────────────────────────────────────────

  /* 280ms matches the CSS transition duration for .tab-pane, so the active
     indicator never visibly lags behind the panel it's tracking. */
  this._transitionMs = 280;
  this._activeTab = null;
}
```

**Rule:** if a note fits on one line, write it, close it, and only then move
to a new line. There's no such thing as a quick aside that gets its closer
added afterward — "afterward" is exactly when it gets forgotten.

---

### The Long Stretch

The same failure as *The Vanishing Method*, but with nothing nearby to limit
the damage. `//` line comments are always safe to write next to a broken
block — but they don't help close one either. If the methods right after the
break happen to use `//` instead of JSDoc, the swallow keeps going until it
reaches the next `/** */` block, however far away that is.

The JSDoc below is the real `validateInstallments` block from the audit
(lines 6918–6932) — 14 lines, verified correctly closed in the actual file,
and singled out in the report specifically because its length didn't cause
any problem. Here's the shape of what dropping its closer would have done:

```js
/* ✗ WRONG — three methods vanish, not one */

/**
 * Validates all data fields used in HTML templates and guards against common attacks.
 *
 * Prototype Pollution prevention: rejects items with __proto__, constructor, or
 * prototype as keys — these could allow attackers to inject properties onto the
 * global Object prototype if the data is merged into a plain object.
 *
 * Type checking ensures all fields match expected types. Invalid items are
 * silently dropped; only valid items pass through.
 * Uses Object.hasOwn (not 'in') to avoid prototype chain false positives.
 *
 * @param {any} items - Raw data to validate
 * @returns {Array} Filtered array of valid installment objects
 * @static

validateInstallments(items) {
  return items.filter(item => Object.hasOwn(item, 'amount'));
}

// Formats a currency amount using the user's locale settings.
formatCurrency(value) {
  return new Intl.NumberFormat(this._locale).format(value);
}

// Debounces rapid calls so _handleScroll runs at most once per interval.
_handleScrollDebounced(fn, ms) {
  let last = 0;
  return (...args) => {
    const now = Date.now();
    if (now - last >= ms) { last = now; fn(...args); }
  };
}

/**
 * Removes all event listeners and resets component state.
 */
destroy() {
  this._ac.abort();
}
```

`validateInstallments`, `formatCurrency`, and `_handleScrollDebounced` are all
comment text. None of the three `//` lines in between could close anything —
line comments only ever close themselves — so the swallow runs uninterrupted
until `destroy`'s own JSDoc finally supplies a `*/`. The blast radius here
isn't "one method." It's "every method until the next block comment,"
whichever one that turns out to be — in this real class, that's two extra
methods lost for the price of one missing `*/`.

```js
/* ✓ CORRECT — the actual, verified state of the file */

/**
 * Validates all data fields used in HTML templates and guards against common attacks.
 *
 * Prototype Pollution prevention: rejects items with __proto__, constructor, or
 * prototype as keys — these could allow attackers to inject properties onto the
 * global Object prototype if the data is merged into a plain object.
 *
 * Type checking ensures all fields match expected types. Invalid items are
 * silently dropped; only valid items pass through.
 * Uses Object.hasOwn (not 'in') to avoid prototype chain false positives.
 *
 * @param {any} items - Raw data to validate
 * @returns {Array} Filtered array of valid installment objects
 * @static
 */
validateInstallments(items) {
  return items.filter(item => Object.hasOwn(item, 'amount'));
}
```

**Rule:** treat a JSDoc block above a method that's followed by several
`//`-only methods with extra care — there's no accidental safety net nearby.
Length isn't the risk factor here — this is the longest block comment in the
whole file, and it's also one of the 159 that closed correctly. The balance
check in this guide catches a break like this regardless of how far it
travels; that's exactly why the check matters more than trying to eyeball
the gap.

---

### Component Entry Point

```js
// Initialize once the DOM is ready.
document.addEventListener('DOMContentLoaded', () => {
  new AccountPageController('.account-page-container');
});
```

---

### The Templated Comment

A comment can be perfectly valid JavaScript and still be a broken HTML
comment — if it's written inside a template literal that gets inserted into
the DOM. The JS parser only ever sees a big string; it doesn't know, or care,
that part of that string is meant to become a real HTML comment once
rendered. The audit above checked exactly this category, across three
template locations in the file, and found five comment pairs, all correctly
closed — including the real one below, at lines 5177–5178. This is what
breaking it would have looked like:

```js
/* ✗ WRONG — valid JS, broken HTML once rendered */

function renderBonusCard(card) {
  return `
      <!-- data-action="show-info" triggers _handleShowInfo() via event delegation.
           data-bonus-card identifies which card's description to announce.

    <div class="bonus-card" data-action="show-info" data-bonus-card="${card.id}">
      <p>${card.description}</p>
    </div>
  `;
}
```

This function has no JS syntax error. `renderBonusCard()` runs, returns a
string, and nothing in the console complains. The problem only appears once
that string is written into the DOM — typically via `innerHTML` — at which
point the browser's HTML parser opens the `<!--` and never finds a `-->` to
close it anywhere in the string. The entire card, `<div>` and all, is parsed
as comment content and never renders. Nothing appears where the card should
be, and nothing in DevTools points at a comment as the cause.

```js
/* ✓ CORRECT — the actual, verified state of the file */

function renderBonusCard(card) {
  return `
      <!-- data-action="show-info" triggers _handleShowInfo() via event delegation.
           data-bonus-card identifies which card's description to announce. -->
    <div class="bonus-card" data-action="show-info" data-bonus-card="${card.id}">
      <p>${card.description}</p>
    </div>
  `;
}
```

**Rule:** an HTML comment inside a JS template literal has to pass two
checks, not one — valid as JS (which it almost always is, since JS treats
the whole thing as a string) and valid as the HTML it becomes after
rendering. The JS parser will never catch a broken one; only checking the
rendered output, or scanning the template's own `<!--`/`-->` balance, will.

---

### What Gets No Comment

```js
this._activeTab = null;                         // ← obvious from name
this._root = document.querySelector(selector);  // ← obvious
el.classList.add('is-active');                  // ← self-evident
return this._activeTab;                         // ← trivial getter body
```

---

## CSS

### File Header

Every CSS file starts with a one-block header: what this file covers and any
dependency notes.

```css
/**
 * Account Page — Layout and component styles.
 * Depends on: bootstrap.min.css (grid, utilities), tokens.css (CSS variables).
 * Custom properties defined in :root below override Bootstrap defaults.
 */
```

---

### CSS Two-Tier Section Hierarchy

CSS files have two distinct levels of section marker.
They must **look visually different** so you can read the file's structure
at a glance while scrolling — without counting or indexing anything.

---

#### Tier A — Top-Level Section

Use the full dash-bar with ALL CAPS. Marks a major zone of the stylesheet:
a whole feature area, a layout region, or a cross-cutting concern.
These are the landmarks of the file.

```css
/* ════════════════════════════════════════════════════════════════════
   THEME TOKENS
   ════════════════════════════════════════════════════════════════════ */

/* ─── RESET & BASE ───────────────────────────────────────────────────── */

/* ─── LAYOUT ─────────────────────────────────────────────────────────── */

/* ─── COMPONENT: SIDEBAR ─────────────────────────────────────────────── */

/* ─── COMPONENT: TAB NAVIGATION ──────────────────────────────────────── */

/* ─── RESPONSIVE: TABLET (max 1199px) ────────────────────────────────── */

/* ─── RESPONSIVE: MOBILE (max 767px) ─────────────────────────────────── */

/* ─── ACCESSIBILITY ──────────────────────────────────────────────────── */

/* ─── PRINT ──────────────────────────────────────────────────────────── */
```

Use the double-line `═` box only for the single most important section
in a file (typically THEME TOKENS or a file-level architectural note).
Everywhere else, the single dash-bar is correct.

---

#### The Padding Slip

Tier A headers are hand-filled with `─` to hit column ~72 (see the Section
Header Format Reference below). That fill often gets adjusted after the
fact — lengthened, shortened, restyled — and the trailing ` */` gets treated
as more filler and trimmed along with the extra dashes.

```css
/* ✗ WRONG — closer trimmed along with the dash fill */

/* ─── RESPONSIVE: TABLET (max 1199px) ----------------------------------

@media (max-width: 1199.98px) {
  .sidebar { width: 240px; }
}
```

```css
/* ✓ CORRECT */

/* ─── RESPONSIVE: TABLET (max 1199px) ──────────────────────────────── */

@media (max-width: 1199.98px) {
  .sidebar { width: 240px; }
}
```

**Rule:** when adjusting a header's fill length, touch the dash run only.
Treat ` */` as a fixed suffix — never part of the fill, never something to
eyeball back into place.

---

#### Tier B — Sub-Section Marker

Marks a named group **within** a top-level section: a layout sub-zone,
a modifier group, a state cluster, a set of related selectors.

Sub-section markers are lowercase, no fill characters, no border —
just a brief human phrase that names what follows.

```css
/* container layout */

/* child elements */

/* hover and focus states */

/* open / collapsed variants */

/* reduced-motion override */
```

The visual contrast between Tier A (heavy, uppercase, bordered) and
Tier B (quiet, lowercase, no border) lets a reader instantly understand
depth without any numbering.

---

#### Why Two Tiers Work

```css
/* ─── COMPONENT: SIDEBAR ─────────────────────────────────────────────── */
/* Vertical navigation panel. Collapses to horizontal scroll on mobile. */

/* container layout */

.sidebar {
  position: sticky;
  top: 72px;             /* Offset clears the fixed top navigation bar. */
  overflow-y: auto;
}

/* child elements */

.sidebar__nav { ... }
.sidebar__item { ... }

/* hover and focus states */

.sidebar__item:hover { ... }
.sidebar__item:focus-visible { ... }
```

The top-level header names the component. The sub-section markers name the
groups inside it. No index, no counter, no sequence — just names.

---

### Component Block Description

Each top-level component section starts with a one- or two-line prose note
right below the header. State what it is and one key behavioral fact.
Skip the note if there is nothing non-obvious to say.

```css
/* ─── COMPONENT: SIDEBAR ─────────────────────────────────────────────── */
/* Vertical navigation panel. Switches to a horizontal scroll layout
   on mobile — see the Responsive section below. */

.sidebar { ... }
```

```css
/* ─── THEME TOKENS ───────────────────────────────────────────────────── */
/* Override these variables in your own stylesheet to retheme the component.
   All color values in this file reference these tokens. */

:root {
  --primary:   #4F46E5;
  --surface:   #FFFFFF;
  --text:      #1C1C1E;
  --radius-md: 8px;
}
```

---

### The Trailing Description

The real incident behind this pattern — the Wallet section's `CARD TYPOGRAPHY`
comment — is traced in full, line by line, in *Absolute Rule: No Comment Ships
Unclosed* near the start of this guide. The shape of it: a Tier A header's own
dash-bar line closes correctly; it's the prose description underneath, the
*Component Block Description* just above this one, that doesn't.

```css
/* ✓ CORRECT — closer sits on the last line of the description */

        /* ─── COMPONENT: CARD TYPOGRAPHY ────────────────────────────
           font-size uses container-query units (cqw) — Bootstrap fs-*
           utilities do not cover cqw, so these classes are intentionally
           kept as scoped CSS rather than replaced with Bootstrap utilities.
           These are CSS classes, not inline style= attributes. */

        .wallet-container .wallet-card-label {
            font-size: 2.5cqw;
        }
```

**Rule:** the closing `*/` always sits on the same line as the last word of
the description — never alone on its own line, where a later edit can drop it
without disturbing anything else visibly.

---

### Inline Property Notes

Use inline comments only for non-obvious values or intentional overrides.
Keep to the end of the line or the line above — never a paragraph.

```css
.sidebar {
  position: sticky;
  top: 72px;                 /* Offset clears the fixed top navigation bar. */
  overflow-y: auto;
  scrollbar-width: thin;     /* Firefox only; Chrome uses ::-webkit-scrollbar below. */
}

/* ─── Z-INDEX STACK ──────────────────────────────────────────────────── */
/* Layering order (low → high): backdrop → modal → tooltip.
   Matches Bootstrap defaults so third-party overlays stay in context. */

.modal-backdrop { z-index: 1040; }
.modal          { z-index: 1050; }
.tooltip        { z-index: 1070; }
```

---

### The Aside That Never Ends

The second real incident from the audit, and the shorter, easier-to-miss
sibling of *The Trailing Description*. A short, inline-style note that spans
two lines instead of one — and the second line simply never gets a closer
before the selector that follows it.

```css
/* ✗ WRONG — this is the actual Promotions section bug, verbatim */

        /* letter-spacing has no Bootstrap utility class.
           Scoped to container — every selector starts with the container class.
        .promo-offers-container .ls-wide {
            letter-spacing: 0.1em;
        }

        /* ── Promo card ──────────────────────────────────────────── */
```

The comment opens on line one and is never closed — the description ends
mid-thought with "container class." and no `*/`, and the very next line is
the selector, not a blank line giving anyone a chance to notice. `.ls-wide`
and its one declaration become comment text. The next `/*`, belonging to the
"Promo card" header, isn't a new comment either — it's still just characters
inside the first one — until its own `*/` finally closes the whole run.

```css
/* ✓ CORRECT */

        /* letter-spacing has no Bootstrap utility class.
           Scoped to container — every selector starts with the container class. */
        .promo-offers-container .ls-wide {
            letter-spacing: 0.1em;
        }

        /* ── Promo card ──────────────────────────────────────────── */
```

One line below the fix, in the same file, the same author wrote the identical
shape of comment and closed it correctly on the first attempt:

```css
        /* hover lift (translateY + box-shadow) has no Bootstrap utility equivalent. */
```

**Rule:** if a note fits on one line, write it, close it, and only then move
to a new line. There's no such thing as a quick aside that gets its closer
added afterward — "afterward" is exactly when it gets forgotten. The very
next line in this file, written by the same person in the same sitting,
proves the habit usually holds — which is exactly why a mechanical check
matters more than trying harder.

---

### The Double Comment

CSS comments do not nest. Wrapping a block that already contains an inline
`/* why */` note creates a second `/*` that does nothing special, and a
*first* `*/` that closes the outer comment early — leaving the rest of the
block as broken, orphaned CSS.

```css
/* ✗ WRONG — nested comment closes early */

/*
.sidebar {
  position: sticky;
  top: 72px;             /* Offset clears the fixed top navigation bar. */
  overflow-y: auto;
}
*/
```

The outer comment actually closes right after `navigation bar.` — at the
first `*/` the parser meets. The selector and its first two declarations
became comment text and never applied. Everything after that point —
`overflow-y: auto;` onward, including the final stray `*/` — is left outside
any rule, which is invalid CSS.

```css
/* ✓ CORRECT — delete the rule, don't comment it out */

/* Rule removed: sidebar offset now handled by --header-height token. */
```

**Rule:** never wrap a block in a comment if it might already contain one —
and don't leave disabled code in a shipped file at all. If a rule needs to
go, delete it. If the reason matters, say so in one line; don't preserve the
dead code to explain itself.

---

### Responsive Blocks

State *what changes* and *at what breakpoint* in the section header.
No need to repeat it on every rule inside.

```css
/* ─── RESPONSIVE: MOBILE (max 767px) ─────────────────────────────────── */
/* Sidebar collapses into a swipeable horizontal scroll nav. */

@media (max-width: 767.98px) {
  .sidebar {
    position: static;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
  }
}
```

---

### The Media Query Swallow

The same failure as *The Trailing Description*, but on a Responsive or
Accessibility block — which means the blast radius is an entire breakpoint
or accommodation, not one typography rule.

```css
/* ✗ WRONG */

/* ─── RESPONSIVE: MOBILE (max 767px) ─────────────────────────────────── */
/* Sidebar collapses into a swipeable horizontal scroll nav.

@media (max-width: 767.98px) {
  .sidebar {
    position: static;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
  }
}

/* ─── ACCESSIBILITY ──────────────────────────────────────────────────── */
```

```css
/* ✓ CORRECT */

/* ─── RESPONSIVE: MOBILE (max 767px) ─────────────────────────────────── */
/* Sidebar collapses into a swipeable horizontal scroll nav. */

@media (max-width: 767.98px) {
  .sidebar {
    position: static;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
  }
}

/* ─── ACCESSIBILITY ──────────────────────────────────────────────────── */
```

**Rule:** give Responsive and Accessibility descriptions the same care as
any other. Losing one of these doesn't misplace a font size — it silently
removes a whole device layout or a WCAG accommodation, with nothing on the
page to suggest it's missing.

---

### Accessibility Block

```css
/* ─── ACCESSIBILITY ──────────────────────────────────────────────────── */
/* Disables animations for users with the OS reduced-motion preference.
   Follows WCAG 2.1 guideline 2.3.3. */

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

### What Gets No Comment

```css
.btn { display: inline-flex; }      /* ← obvious */
.is-hidden { display: none; }       /* ← obvious */
h1, h2, h3 { line-height: 1.2; }   /* ← obvious */
```

---

## HTML

HTML comments carry more baseline risk than CSS or JS, for a simple reason:
there is no line-comment option. Every HTML comment, however short, is a
`<!-- -->` block — the exact form that needs a deliberate closer. There's no
`//`-equivalent to fall back on for a quick one-word note, which means the
discipline in this section has to hold for every comment, not just the long
ones.

### Root Container

One comment per component root. Covers: what it is, how JS finds it,
and any routing or behavioral note that affects the whole component.

```html
<!--
  Customer Account Page — root element.
  Hooked by AccountPageController via the .account-page-container class.
  Uses a custom JS router (not Bootstrap tabs) so tabs are reachable via URL hash.
-->
<div class="account-page-container">
```

---

### The Vanishing Region

HTML comments have the largest blast radius of the three languages: there is
no equivalent of "the next section's header will probably close it soon." If
no later `-->` exists further down the file, everything to the end of the
document — tags, scripts, all of it — is swallowed.

```html
<!-- ✗ WRONG — closer missing after the routing note -->

<!--
  Customer Account Page — root element.
  Hooked by AccountPageController via the .account-page-container class.
  Uses a custom JS router (not Bootstrap tabs) so tabs are reachable via URL hash.

<div class="account-page-container">
  <aside class="sidebar">...</aside>
  <main class="content-area">...</main>
</div>
```

Every element inside — the entire component, and anything below it in the
file — is now comment content, unless some later, unrelated `-->` happens to
exist further down.

```html
<!-- ✓ CORRECT -->

<!--
  Customer Account Page — root element.
  Hooked by AccountPageController via the .account-page-container class.
  Uses a custom JS router (not Bootstrap tabs) so tabs are reachable via URL hash.
-->
<div class="account-page-container">
  <aside class="sidebar">...</aside>
  <main class="content-area">...</main>
</div>
```

**Rule:** write the closing `-->` for a root-element or region comment on its
own line, directly above the tag it describes, in the same pass as the
opening `<!--` — never appended after the markup is already in place.

---

### The Reappearing Element

The HTML shape of *The Double Comment*. HTML comments don't nest either — the
first `-->` the parser meets closes the *outer* wrapper, no matter how many
`<!--` appear inside it. Anything after that point becomes live markup
again — the opposite of "hidden."

```html
<!-- ✗ WRONG — nested comment closes early -->

<!--
<div class="wallet-container">
  <!-- data-wallet-id identifies which stored card this panel renders. -->
  <span class="wallet-card-label">Visa •••• 4242</span>
</div>
-->
```

The outer `<!--` closes at the first `-->` it meets — the one ending the
inner `data-wallet-id` note. `<div class="wallet-container">` and the inner
comment's own opening are swallowed and never render. But
`<span class="wallet-card-label">Visa •••• 4242</span>` is now *outside* any
comment: it renders, visible, on the page — the opposite of what "commenting
it out" was supposed to do. `</div>` becomes a stray closing tag with no
matching open, and the literal characters `-->` can surface as visible text
wherever the browser's error recovery lands.

```html
<!-- ✓ CORRECT — delete the markup, don't comment it out -->

<!-- Removed: wallet-card-label duplicate, now rendered by the card template. -->
```

**Rule:** never wrap markup in a comment if it might already contain one. The
failure here isn't quiet like the others — a card number appearing where it
shouldn't is the kind of thing a screenshot catches immediately, but by then
it's already shipped.

---

### Major Layout Regions

Comment only the outermost wrapper of each region — not every div inside.

```html
<!-- Sidebar navigation — becomes a horizontal scroll strip on mobile. -->
<aside class="sidebar">

<!-- Main content area — tab panels are rendered here by AccountPageController. -->
<main class="content-area">

<!-- Sticky action bar — always visible at the bottom on mobile viewports. -->
<div class="action-bar">
```

---

### data-* Attributes as Public API

When a component reads `data-*` attributes as configuration, document them
on the element that owns them — one line per attribute.

```html
<!--
  Navigation trigger.
  data-target: id of the .tab-pane this button activates (must match exactly).
  data-track:  optional analytics event label sent on click.
-->
<button class="nav-btn" data-target="overview" data-track="tab_overview">
  Overview
</button>
```

---

### ARIA Attributes Toggled by JS

If JS toggles an ARIA attribute, say so — otherwise the static value looks like a bug.

```html
<!--
  aria-expanded is toggled to "true"/"false" by SidebarController on open/close.
  aria-controls links this button to the panel it reveals for screen readers.
-->
<button class="sidebar-toggle"
        aria-expanded="false"
        aria-controls="sidebar-panel">
  Menu
</button>
```

---

### The Silent Accommodation

The HTML shape of *The Aside That Never Ends* — and, fittingly, it's an
accessibility note that goes missing.

```html
<!-- ✗ WRONG -->

<!-- role="status" is required so screen readers announce balance updates.

<span class="wallet-balance" role="status">$0.00</span>
```

The comment never closes, so the `<span>` — balance value, `role="status"`,
and all — is swallowed entirely. The element doesn't just lose its
accessibility semantics; it doesn't render at all. Sighted users see a
missing balance. Screen reader users were the ones the comment was trying to
help, and they lose the most: nothing is announced, because nothing is there.

```html
<!-- ✓ CORRECT -->

<!-- role="status" is required so screen readers announce balance updates. -->

<span class="wallet-balance" role="status">$0.00</span>
```

**Rule:** treat accessibility notes with the same one-line-closes-on-one-line
discipline as everything else in this guide — the impact of losing one falls
hardest on the users who could least afford it.

---

### Third-Party Embed Wrappers

```html
<!-- Stripe payment form mount point — content is injected by Stripe.js. -->
<div id="stripe-card-element"></div>
```

---

### What Gets No Comment

```html
<header class="site-header">       <!-- ← obvious -->
<footer class="site-footer">       <!-- ← obvious -->
<ul class="nav-list">              <!-- ← obvious -->
<p class="hero__subtitle">         <!-- ← obvious -->
```

---

## Editing Existing Files Safely

Most of these bugs are introduced during an edit to a file that was already
correct — not while writing from a blank page. Here's what that looks like in
practice, and the habits that catch it before it ships.

### The Merged Header

This one isn't introduced while writing — it's introduced while *editing*.
A find-and-replace or diff-based edit that removes a rule block between two
sections can take a neighboring comment's closer or opener with it, even
though neither was part of the intended change.

Before the edit, both sections close correctly:

```css
/* ─── COMPONENT: SIDEBAR ─────────────────────────────────────────────── */
/* Vertical navigation panel. */

.sidebar { position: sticky; top: 72px; }

/* legacy sidebar variant — remove after Q3 migration */
.sidebar--legacy { position: fixed; }

/* ─── COMPONENT: TAB NAVIGATION ──────────────────────────────────────── */
/* Custom JS router, not Bootstrap tabs. */

.tab-nav { display: flex; }
```

The edit is meant to delete only `.sidebar--legacy` and its comment line.
If the deleted range's boundary lands one line early — inside the previous
line's closer instead of after it — the result is:

```css
/* ✗ WRONG — after the edit */

/* ─── COMPONENT: SIDEBAR ─────────────────────────────────────────────── */
/* Vertical navigation panel.

.sidebar { position: sticky; top: 72px; }

/* ─── COMPONENT: TAB NAVIGATION ──────────────────────────────────────── */
/* Custom JS router, not Bootstrap tabs. */

.tab-nav { display: flex; }
```

The Sidebar description's own `*/` was removed along with the legacy block.
Now the entire `.sidebar` rule and the Tab Navigation header's dash-bar line
are swallowed into one comment; only the Tab Navigation description and
`.tab-nav` itself still work, because that description line supplies a fresh
closer of its own.

The mechanism here doesn't care which language it's wearing. The same
collateral-damage edit can take out a JS JSDoc block sitting next to a
deleted private method, or an HTML region comment sitting next to a deleted
layout wrapper — different delimiters, identical cause: an edit's boundary
landed one line short, or one line long, of where it should have.

**Rule:** after any edit that adds, removes, or reorders lines near a
comment, re-view the surrounding lines and re-run the balance check before
moving on. Don't trust that an edit "only touched the lines it targeted" —
verify what's left on both sides of the change.

### General Practice

- Before editing, check whether the target text sits inside or next to a
  comment block. If it does, treat both the opener and the closer as part
  of what you're touching, even if your change only concerns the code
  between them.
- After any find-and-replace or range-based edit near a comment, re-view a
  window of at least ten lines on both sides of the change — not only the
  lines you intended to modify.
- Re-run the delimiter balance check on the file after the edit, not just
  before shipping. A file that was balanced before your edit and is
  unbalanced after it tells you exactly which edit caused the break.
- Never assume a diff "only touched what it shows." A replaced string that
  starts or ends mid-comment can leave an opener or closer stranded outside
  the visible diff.

---

## Section Header Format Reference

### JavaScript
```js
// ─── SECTION NAME ────────────────────────────────────────────────────
```

### CSS — Tier A (top-level section)
```css
/* ─── SECTION NAME ──────────────────────────────────────────────────── */
```
For the single dominant section in a file:
```css
/* ════════════════════════════════════════════════════════════════════
   SECTION NAME
   ════════════════════════════════════════════════════════════════════ */
```

### CSS — Tier B (sub-section within a top-level section)
```css
/* sub-section name in lowercase */
```

### HTML
```html
<!-- ═══ SECTION NAME ════════════════════════════════════════════════ -->
```
*(Use `═` only for top-level page regions in large HTML files — not inside components)*

**Minimum line length for Tier A:** fill to column ~72 so headers stand out on scroll.
**Casing:** ALL CAPS for Tier A section names, lowercase for Tier B sub-section names.

---

## Comment Density Summary

| Location | Comment type | Required? |
|---|---|---|
| JS class | JSDoc block (1–3 lines + `@param`) | Always |
| JS public method | JSDoc block (1 line + `@param`/`@returns` if non-obvious) | Always |
| JS private method | `//` one line — only if logic is non-obvious | When non-obvious |
| JS section boundary | `// ─── NAME ───` header | Always |
| JS non-obvious line | `//` inline "why" | When non-obvious |
| CSS file | File header block | Always |
| CSS top-level section (Tier A) | `/* ─── NAME ─── */` dash-bar header | Always |
| CSS sub-section (Tier B) | `/* lowercase name */` quiet marker | When grouping is useful |
| CSS component block | 1–2 line prose description | Always |
| CSS non-obvious property | Inline `/* why */` | When non-obvious |
| HTML component root | 1–3 line description block | Always |
| HTML major layout region | 1-line description | Always |
| HTML data-* config | One line per attribute | When non-obvious |
| HTML ARIA toggled by JS | 1–2 line note | Always |

---

## Pre-Release Checklist

### Remove
- [ ] Any number in a comment used as an index or sequence marker
- [ ] Any letter used as an index (`A.`, `B.`, `a)`)
- [ ] Words like "first", "second", "third" used as structural labels
- [ ] `§` symbols and internal rule references
- [ ] Changelog language: `updated`, `fixed`, `v2.1`, `TEMP`, `refactored`
- [ ] Internal TODOs: `// TODO: refactor this`, `// FIXME: workaround`
- [ ] Comments that paraphrase the code (`// loop through items`)
- [ ] Names like `Law Zero`, `containerization-N`, `hook-protocol`
- [ ] Commented-out blocks of any kind, in any language — delete the code,
      don't disable it with a comment wrapper (see *The Double Comment* family)

### Verify
- [ ] Every class has a JSDoc block
- [ ] Every public method has a JSDoc block
- [ ] Every top-level CSS section has a Tier A dash-bar header
- [ ] Sub-sections inside components use quiet lowercase Tier B markers
- [ ] Every component root in HTML has a description block
- [ ] Inline "why" comments use industry terms (Memory Safety, Event Delegation, etc.)
- [ ] No comment contains any form of numeric or alphabetic sequencing
- [ ] All `data-*` attributes that JS reads are documented on their element
- [ ] All ARIA attributes toggled by JS have a note explaining the JS behavior
- [ ] No comment block exceeds 3 lines (except class-level JSDoc)
- [ ] Count of `/*` equals count of `*/` in every CSS block touched this session
- [ ] Every multi-line CSS description closes on the same line as its last word
- [ ] No `*/` sits alone on its own line with nothing else
- [ ] No comment contains a `/*` or `<!--` anywhere inside its own text
- [ ] Every JSDoc block opened with `/**` has its own `*/` before the next `{`
- [ ] Every HTML region comment closes with `-->` before the first tag it describes
- [ ] Any HTML comment inside a JS template literal closes with `-->` before
      the markup it precedes (see *The Templated Comment*)
- [ ] Any comment touched by a find-and-replace edit was re-viewed after the
      edit, not just before it

### The Test

> You are a junior developer. You bought the template.
> You open an unfamiliar file and read only the comments — not the code.
>
> **Can you answer these?**
> — What does this component/section do?
> — Why was this pattern used?
> — Where do I change X?
>
> If the answer to any question is *no* — add or rewrite the comment.
> If the comment answers none of them — delete it.

### The Count

> Before you consider any comment-touching edit finished, count.
> `/*` equals `*/`? If not, you introduced — or inherited — an unterminated
> comment somewhere in the lines you touched.
>
> Find it before you ship it. Not after someone asks why the wallet cards, or
> the mobile breakpoint, don't look right — when the answer turns out to be
> two missing characters, three sections back.

---

## Quick Reference

Two summaries: what to comment, and how to make sure it survives.

```
ALWAYS COMMENT                          NEVER COMMENT
──────────────────────────────────      ──────────────────────────────────
Class and public method headers         Self-evident variable names
Top-level section boundaries (Tier A)   Trivial getters and setters
Sub-section groups (Tier B)             Obvious loop bodies
Component root elements in HTML         Standard HTML structure elements
Non-obvious patterns (why, not what)    Code that reads like plain English
data-* attributes read by JS            Sequence or order of sections
ARIA attributes toggled by JS           Internal rules or version history
                                        Numbers of any kind
```

```
ALWAYS                                   NEVER
──────────────────────────────────      ──────────────────────────────────
Write /**/ first, content second        Write /* and add */ "at the end"
Close on the same line as the last      Leave */ alone on its own line
  word of the comment
Re-check balance after every edit       Trust a diff "only touched what
  near a comment                          it shows"
Delete dead code                        Comment out a block that may
                                           already contain a comment
Treat CSS silence as a bug signal       Assume "no error" means "no bug"
```

---

*"One comment per logical unit. Written for the buyer, not the author. Explains why,
not what. Never counts, never left open — the file won't warn you, but the count
will."*
