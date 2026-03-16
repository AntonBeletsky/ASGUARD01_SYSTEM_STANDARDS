/*
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                          BEM ARCHITECTURE GUIDE                             ║
║                      Block Element Modifier Methodology                      ║
║                                                                              ║
║           Complete Guide: HTML, CSS, and JavaScript Implementation           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

VERSION: 2.0
UPDATED: March 16, 2024
AUDIENCE: Frontend developers, CSS architects, component builders
SCOPE: HTML, CSS, JavaScript integration with BEM

*/

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

/*
1.  INTRODUCTION & PHILOSOPHY
2.  CORE CONCEPTS (Block, Element, Modifier)
3.  NAMING CONVENTIONS
4.  HTML IMPLEMENTATION
5.  CSS IMPLEMENTATION
6.  JAVASCRIPT INTEGRATION
7.  ADVANCED PATTERNS
8.  REAL-WORLD EXAMPLES (Button, Input, Modal, Form)
9.  COMMON MISTAKES & SOLUTIONS
10. BEM WITH CSS MODULES
11. BEM WITH SASS/SCSS
12. BEM VS OTHER METHODOLOGIES
13. PERFORMANCE CONSIDERATIONS
14. ACCESSIBILITY IN BEM
15. SCALING BEM (Design Systems)
16. MIGRATION GUIDE
17. TOOLS & AUTOMATION
18. FAQ & TROUBLESHOOTING
*/


// ============================================================================
// 1. INTRODUCTION & PHILOSOPHY
// ============================================================================

/*
WHAT IS BEM?
────────────
BEM = Block Element Modifier

A naming convention for CSS classes that makes your code:
  • More predictable
  • Easier to read
  • Easier to scale
  • Easier to maintain
  • Less prone to naming conflicts


WHY BEM?
────────

Without BEM:
  .button { }
  .button .icon { }      ← Depends on HTML structure
  .button.active { }     ← Unclear what "active" means
  .button-large { }      ← Inconsistent naming
  Result: Chaos, specificity wars, maintenance nightmare


With BEM:
  .button { }            ← Clear: this is the block
  .button__icon { }      ← Clear: icon element of button
  .button--primary { }   ← Clear: primary variant of button
  .button--disabled { }  ← Clear: disabled state of button
  Result: Predictable, scalable, maintainable


THE BEM PHILOSOPHY
──────────────────

"Look at the class name and know exactly what it does"

Every class should answer:
  Q1: What is this? (Block name)
  Q2: Is it a part of something? (Element)
  Q3: Is it a variant or state? (Modifier)


CORE PRINCIPLES
───────────────

1. BLOCK-LEVEL THINKING
   Components are independent blocks
   No dependencies between blocks
   Each block can be used anywhere

2. ELEMENT OWNERSHIP
   Elements belong to one block only
   Never nest elements: .block__element__subelement ✗
   Elements are not standalone

3. MODIFIER INDEPENDENCE
   Modifiers change appearance/behavior but don't replace
   Can use multiple modifiers: class="button button--primary button--large"
   Should work with and without modifiers

4. SINGLE RESPONSIBILITY
   Each class does one thing
   Easy to understand purpose
   Easy to override if needed

5. NO CASCADE
   Direct styles, no deep nesting
   Avoid: .button > div > span
   Result: Predictable specificity
*/


// ============================================================================
// 2. CORE CONCEPTS
// ============================================================================

/*
BLOCK
─────

Definition:
  A functionally independent page component that can be reused
  The highest level of an abstraction
  The "namespace" for elements and modifiers


Characteristics:
  ✓ Standalone - can exist on any page
  ✓ Reusable - used multiple times
  ✓ Portable - moved between projects
  ✓ Independent - no external dependencies
  ✓ Named with 1-2 words: .button, .form, .navigation


Examples of Blocks:
  .button      - A button component
  .input       - An input field
  .card        - A card container
  .header      - Page header
  .sidebar     - Page sidebar
  .modal       - Modal dialog
  .dropdown    - Dropdown menu
  .tabs        - Tab component
  .pagination  - Pagination
  .badge       - Badge component


Key Rule: Block names are unique
  If you have multiple buttons, they're all .button
  If you have different button styles, use modifiers


ELEMENT
───────

Definition:
  A constituent part of a block that has no standalone meaning
  Depends on its parent block
  Only makes sense in the context of its block


Characteristics:
  ✓ Part of a block - cannot exist standalone
  ✓ Named relative to block: .block__element
  ✓ Double underscore __ separates block from element
  ✓ Multiple elements in one block: .button__icon, .button__text


Naming Rules:
  .block__element
  ↑     ↑  ↑
  |     |  └─ Element name
  |     └──── Separator: double underscore
  └────────── Block name


Examples:

Button block:
  .button          ← Block
  .button__icon    ← Icon element inside button
  .button__text    ← Text element inside button

Input block:
  .input           ← Block
  .input__label    ← Label element
  .input__field    ← Input field element
  .input__error    ← Error message element

Card block:
  .card            ← Block
  .card__image     ← Image element
  .card__title     ← Title element
  .card__content   ← Content element
  .card__footer    ← Footer element


Key Rule: Don't nest elements
  ✗ Wrong:  .button__wrapper__inner
  ✓ Right:  .button__inner (if needed)

  ✗ Wrong:  .form__group__label
  ✓ Right:  .form__label (separate block: .form-group)


MODIFIER
────────

Definition:
  A flag on a block or element that changes appearance/behavior
  Represents a variant, state, or temporary property
  Optional - can be absent


Characteristics:
  ✓ Changes how block/element looks or acts
  ✓ Named relative to block/element: .block--modifier
  ✓ Double hyphen -- separates block from modifier
  ✓ Can be boolean (present/absent) or key-value
  ✓ Can combine multiple modifiers


Naming Rules:

  For blocks:
    .block--modifier
    .button--primary
    .button--large
    .button--disabled

  For elements:
    .block__element--modifier
    .button__icon--small
    .button__text--bold


Examples of Modifiers:

Variants (visual styles):
  .button--primary      ← Blue/main button
  .button--secondary    ← Gray/secondary button
  .button--danger       ← Red/destructive button
  .button--ghost        ← Outlined button

States (temporary changes):
  .button--disabled     ← Disabled state
  .button--loading      ← Loading state
  .button--active       ← Active/selected state
  .input--error         ← Has validation error
  .input--filled        ← Has content

Sizes:
  .button--small        ← Small button
  .button--large        ← Large button
  .button--fullwidth    ← Full width button

Responsive:
  .button--mobile       ← Mobile version
  .button--desktop      ← Desktop version

Boolean modifiers (just present or not):
  .button--disabled     ← Boolean: button is disabled or not
  .input--required      ← Boolean: field is required or not


Key Rules:

1. Modifiers are optional
   .button               ← Valid without modifiers
   .button--primary      ← Valid with modifier

2. Can combine modifiers
   .button.button--primary.button--large   ← Valid
   ✓ Multiple classes on one element

3. Modifiers aren't standalone
   ✗ <div class="--primary">              ← Invalid
   ✓ <button class="button--primary">     ← Valid

4. Modifier means "in addition to"
   .button--primary doesn't replace .button
   Always apply both: class="button button--primary"
*/


// ============================================================================
// 3. NAMING CONVENTIONS
// ============================================================================

/*
BASIC RULES
───────────

1. CLASS NAME STRUCTURE
   .block__element--modifier
   
   Examples:
   .button              ← Block only
   .button__icon        ← Block + Element
   .button--primary     ← Block + Modifier
   .button__icon--small ← Block + Element + Modifier


2. ALLOWED CHARACTERS
   ✓ Letters (a-z, A-Z)
   ✓ Numbers (0-9)
   ✓ Hyphens (-)
   ✓ Underscores (_)
   
   ✗ Spaces
   ✗ Special characters: @, #, $, %, etc.


3. FORMATTING
   Separators:
   • Block from Element: __ (double underscore)
   • Element/Block from Modifier: -- (double hyphen)
   • Word separation: - (single hyphen)
   
   Convention (lowercase):
   .button--primary-bg  ← All lowercase
   ✗ .Button--Primary   ← No camelCase
   ✗ .button--PRIMARY   ← No UPPERCASE


4. NAMING WORDS
   Use meaningful, descriptive words
   
   ✓ .button__icon      ← Clear what it is
   ✓ .form__label       ← Clear what it is
   ✓ .card__image       ← Clear what it is
   
   ✗ .btn__ic           ← Too abbreviated
   ✗ .f__l              ← Meaningless
   ✗ .c__img            ← Unclear


PRACTICAL NAMING EXAMPLES
──────────────────────────

Example 1: Button Component
  Block:     .button
  Elements:  .button__icon, .button__text
  Modifiers: .button--primary, .button--secondary, .button--disabled, .button--loading
  Full:      .button.button--primary
  Full:      .button__icon.button__icon--small


Example 2: Form Component
  Block:     .form
  Elements:  .form__group, .form__label, .form__input, .form__error
  Modifiers: .form--login, .form--register, .form--compact
  Full:      .form.form--login
  Full:      .form__input.form__input--error


Example 3: Card Component
  Block:     .card
  Elements:  .card__image, .card__title, .card__text, .card__footer, .card__link
  Modifiers: .card--featured, .card--horizontal, .card--small
  Full:      .card.card--featured
  Full:      .card__image.card__image--loading


Example 4: Navbar Component
  Block:     .navbar
  Elements:  .navbar__logo, .navbar__menu, .navbar__link, .navbar__user
  Modifiers: .navbar--sticky, .navbar--dark, .navbar--compact
  Full:      .navbar.navbar--sticky
  Full:      .navbar__link.navbar__link--active


ABBREVIATION POLICY
────────────────────

When to abbreviate:
  ✓ Use common abbreviations: btn (button), img (image), msg (message)
  ✓ Be consistent: always use btn or always use button, not both
  ✓ Common abbreviations team agrees on

When not to abbreviate:
  ✗ Obscure abbreviations nobody understands
  ✗ Mix of abbreviated and full words
  ✗ Saves so little typing, costs readability


Recommended abbreviations:
  btn       → button
  img       → image
  msg       → message
  nav       → navigation
  prev      → previous
  bg        → background
  txt       → text
  attr      → attribute
  calc      → calculate
  config    → configuration
  temp      → temporary


MULTIPLE BLOCKS? USE NEW CLASSES
─────────────────────────────────

If you have multiple different components, don't force one block.

✗ Wrong (forcing one block):
  .form--button
  .form__button
  These are actually DIFFERENT components

✓ Right (separate blocks):
  .form         ← Form block
  .button       ← Button block (independent)
  Use both: <button class="button button--primary">


NAMING CONVENTIONS SUMMARY
──────────────────────────

Component Name     Block Name       Elements              Modifiers
────────────────   ──────────────   ──────────────────   ──────────────────
Button             .button          .button__icon        .button--primary
                                    .button__text        .button--disabled
                                                         .button--loading

Input              .input           .input__label        .input--error
                                    .input__field        .input--disabled
                                    .input__error        .input--required

Card               .card            .card__image         .card--featured
                                    .card__title         .card--horizontal
                                    .card__content       .card--small

Modal              .modal           .modal__overlay      .modal--open
                                    .modal__content      .modal--fullscreen
                                    .modal__close

Form               .form            .form__group         .form--compact
                                    .form__label         .form--inline
                                    .form__input
*/


// ============================================================================
// 4. HTML IMPLEMENTATION
// ============================================================================

/*
BLOCK IN HTML
─────────────

The block is the root element of a component.
Can be any HTML element (div, section, nav, etc).

Examples:

  <div class="button">Click me</div>
  
  <button class="button">Click me</button>
  
  <section class="card">
    ...
  </section>


ELEMENTS IN HTML
────────────────

Elements are nested inside the block.
Represent structural parts of the block.

Structure:
  <div class="block">
    <div class="block__element">Content</div>
    <div class="block__element">Content</div>
  </div>

Example - Button:
  <button class="button">
    <svg class="button__icon">...</svg>
    <span class="button__text">Click me</span>
  </button>

Example - Card:
  <article class="card">
    <img src="..." class="card__image" />
    <h2 class="card__title">Title</h2>
    <p class="card__text">Content</p>
    <a href="#" class="card__link">Learn more</a>
  </article>

Example - Form Group:
  <div class="form__group">
    <label class="form__label" for="email">Email</label>
    <input type="email" class="form__input" id="email" />
    <span class="form__error">Invalid email</span>
  </div>


MODIFIERS IN HTML
──────────────────

Modifiers are applied as additional classes.
Never replace the base class, always add to it.

Structure:
  <div class="block block--modifier">Content</div>
  
Multiple modifiers:
  <div class="block block--modifier1 block--modifier2">Content</div>

Example - Button with modifiers:
  <button class="button button--primary">
    Primary Button
  </button>

  <button class="button button--primary button--large">
    Large Primary Button
  </button>

  <button class="button button--secondary button--disabled">
    Disabled Secondary Button
  </button>

Example - Elements with modifiers:
  <div class="card card--featured">
    <img src="..." class="card__image card__image--large" />
    <h2 class="card__title card__title--bold">Featured Card</h2>
    <p class="card__text">Content</p>
  </div>

Example - Form with modifiers:
  <form class="form form--login">
    <div class="form__group">
      <label class="form__label">Email</label>
      <input type="email" class="form__input form__input--error" />
      <span class="form__error">Invalid email</span>
    </div>
  </form>


COMPLETE HTML EXAMPLE - BUTTON COMPONENT
──────────────────────────────────────────

Basic button:
  <button class="button">
    Click me
  </button>

Button with icon:
  <button class="button button--primary">
    <svg class="button__icon" viewBox="0 0 24 24">
      <path d="..."/>
    </svg>
    <span class="button__text">Click me</span>
  </button>

Disabled button:
  <button class="button button--secondary button--disabled" disabled>
    Disabled
  </button>

Loading button:
  <button class="button button--primary button--loading">
    <span class="button__spinner"></span>
    <span class="button__text">Loading...</span>
  </button>

Full-width button:
  <button class="button button--primary button--block">
    Full Width Button
  </button>


COMPLETE HTML EXAMPLE - MODAL COMPONENT
─────────────────────────────────────────

<div class="modal modal--open">
  <!-- Overlay for closing -->
  <div class="modal__overlay"></div>
  
  <!-- Content container -->
  <div class="modal__content">
    <!-- Close button -->
    <button class="modal__close" aria-label="Close dialog">
      ×
    </button>
    
    <!-- Header -->
    <div class="modal__header">
      <h2 class="modal__title">Modal Title</h2>
    </div>
    
    <!-- Body -->
    <div class="modal__body">
      <p>Modal content goes here</p>
    </div>
    
    <!-- Footer -->
    <div class="modal__footer">
      <button class="button button--secondary">Cancel</button>
      <button class="button button--primary">Confirm</button>
    </div>
  </div>
</div>


SEMANTIC HTML WITH BEM
───────────────────────

BEM works with semantic HTML.
Use proper HTML elements as blocks.

Examples:

  <nav class="navigation">
    <ul class="navigation__list">
      <li class="navigation__item">
        <a class="navigation__link" href="/">Home</a>
      </li>
    </ul>
  </nav>

  <article class="post">
    <h1 class="post__title">Article Title</h1>
    <time class="post__date">2024-03-16</time>
    <div class="post__content">...</div>
    <footer class="post__footer">...</footer>
  </article>

  <header class="header">
    <div class="header__logo">...</div>
    <nav class="header__nav">...</nav>
    <button class="header__menu">Menu</button>
  </header>


KEY RULES FOR HTML
───────────────────

1. ✓ Block is the root
   <div class="button">...</div>

2. ✓ Elements are inside block
   <div class="button">
     <svg class="button__icon">...</svg>
   </div>

3. ✗ Elements NOT nested in each other
   ✗ <div class="button__inner">
        <span class="button__icon__small">...</span>
      </div>

4. ✓ Multiple modifiers on same element
   <button class="button button--primary button--large">

5. ✓ Use semantic HTML with BEM
   <nav class="navigation">

6. ✗ Don't force hierarchy
   ✗ <div class="button form__button">  ← Confusing
   ✓ <button class="button">            ← Clear

7. ✓ Keep structure shallow
   Avoid deep nesting - BEM works best with flat structure

8. ✓ Data attributes separate from styling
   <button class="button" data-action="save">
*/


// ============================================================================
// 5. CSS IMPLEMENTATION
// ============================================================================

/*
BASIC BLOCK CSS
────────────────

.block {
  /* Block styles */
  display: block;
  padding: 10px;
  border: 1px solid;
  background: white;
}

Example:
  .button {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
  }


ELEMENT CSS
────────────

.block__element {
  /* Element styles */
}

Example:
  .button__icon {
    width: 20px;
    height: 20px;
    margin-right: 8px;
    display: inline-block;
    vertical-align: middle;
  }

  .button__text {
    display: inline-block;
    vertical-align: middle;
  }


MODIFIER CSS
─────────────

Apply additional styles on top of block/element.

.block--modifier {
  /* Override or add styles */
}

Example:
  .button--primary {
    background-color: #007bff;
    color: white;
  }

  .button--secondary {
    background-color: #6c757d;
    color: white;
  }

  .button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }

Element modifier:
  .button__icon--small {
    width: 16px;
    height: 16px;
  }

  .button__icon--large {
    width: 24px;
    height: 24px;
  }


STATE MODIFIERS (Special)
──────────────────────────

Some modifiers represent state (temporary).
Can be controlled by CSS classes OR pseudo-classes.

CSS Class Approach:
  .button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  /* Apply when button has disabled attribute */
  .button:disabled,
  .button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

Interactive States (pseudo-classes):
  .button:hover {
    background-color: darken(#007bff, 10%);
  }

  .button:active {
    box-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.2);
  }

  .button:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
  }

Combined approach:
  .button {
    background-color: #007bff;
    transition: background-color 0.3s ease;
  }

  .button:hover {
    background-color: #0056b3;
  }

  .button--disabled {
    opacity: 0.6;
  }


NO NESTING IN BEM
──────────────────

One of the most important rules: flat CSS structure.

✗ Wrong (nesting):
  .button {
    padding: 10px;
  }
  
  .button .icon {
    width: 20px;
  }

Problems with nesting:
  • Depends on HTML structure
  • Higher specificity
  • .button .icon applies to ANY .icon inside .button
  • Can't reuse .icon elsewhere without side effects
  • Harder to maintain

✓ Right (flat):
  .button {
    padding: 10px;
  }
  
  .button__icon {
    width: 20px;
  }

Advantages:
  • Independent of HTML structure
  • Same specificity everywhere
  • Explicit what element is affected
  • Reusable everywhere
  • Easy to maintain


SPECIFICITY IS FLAT
────────────────────

All selectors in BEM have the same specificity:
  .button       = 0,0,1,0  (one class)
  .button--primary = 0,0,1,0  (one class)
  .button__icon = 0,0,1,0  (one class)

Benefits:
  ✓ No specificity wars
  ✓ Easy to override if needed
  ✓ Last rule wins (predictable)
  ✓ No !important needed


CASCADING IS INTENTIONAL
──────────────────────────

Parent/Child relationship is EXPLICIT through naming,
not through CSS structure.

✗ Wrong (implicit):
  .card {
    padding: 10px;
  }
  
  .card h2 {
    font-size: 20px;
  }

✓ Right (explicit):
  .card {
    padding: 10px;
  }
  
  .card__title {
    font-size: 20px;
  }

Benefit: When reading CSS, you know exactly what's styled,
without reading HTML structure.


MODIFIER STYLE STRUCTURE
──────────────────────────

How to organize modifier styles:

Option 1: Separate rule for each modifier
  .button {
    padding: 10px;
    background: #007bff;
  }

  .button--primary {
    background: #007bff;
  }

  .button--secondary {
    background: #6c757d;
  }

  .button--disabled {
    opacity: 0.6;
  }

Option 2: Group related properties
  .button {
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  /* Color variants */
  .button--primary {
    background: #007bff;
    color: white;
  }

  .button--primary:hover {
    background: #0056b3;
  }

  .button--secondary {
    background: #6c757d;
    color: white;
  }

  /* States */
  .button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Sizes */
  .button--small {
    padding: 5px 10px;
    font-size: 12px;
  }

  .button--large {
    padding: 15px 30px;
    font-size: 18px;
  }


COMPLETE BUTTON COMPONENT CSS
───────────────────────────────

/* Base button */
.button {
  display: inline-block;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  text-align: center;
  user-select: none;
  -webkit-user-select: none;
}

/* Focus state */
.button:focus-visible {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

/* Disabled */
.button:disabled,
.button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

/* Elements */
.button__icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  display: inline-block;
  vertical-align: middle;
}

.button__text {
  display: inline-block;
  vertical-align: middle;
}

/* Color Variants */
.button--primary {
  background-color: #007bff;
  color: white;
}

.button--primary:hover:not(:disabled) {
  background-color: #0056b3;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.button--primary:active:not(:disabled) {
  background-color: #004085;
}

.button--secondary {
  background-color: #6c757d;
  color: white;
}

.button--secondary:hover:not(:disabled) {
  background-color: #5a6268;
}

.button--danger {
  background-color: #dc3545;
  color: white;
}

.button--danger:hover:not(:disabled) {
  background-color: #c82333;
}

/* Size Variants */
.button--small {
  padding: 8px 16px;
  font-size: 14px;
}

.button--large {
  padding: 16px 32px;
  font-size: 18px;
}

/* Full Width */
.button--block {
  display: block;
  width: 100%;
}

/* Loading State */
.button--loading {
  position: relative;
  pointer-events: none;
}

.button--loading::after {
  content: '';
  display: inline-block;
  width: 14px;
  height: 14px;
  margin-left: 8px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}


CSS VARIABLES WITH BEM
───────────────────────

Use CSS custom properties for configuration.

/* Define variables on block */
.button {
  --button-padding: 12px 24px;
  --button-bg: #007bff;
  --button-color: white;
  --button-radius: 4px;
  
  display: inline-block;
  padding: var(--button-padding);
  background: var(--button-bg);
  color: var(--button-color);
  border-radius: var(--button-radius);
}

/* Override in modifier */
.button--primary {
  --button-bg: #007bff;
}

.button--secondary {
  --button-bg: #6c757d;
}

.button--small {
  --button-padding: 8px 16px;
}

/* Use on elements */
.button__icon {
  width: var(--button-icon-size, 20px);
  height: var(--button-icon-size, 20px);
}


KEY RULES FOR CSS
──────────────────

1. ✓ Flat structure
   .block { }
   .block__element { }
   .block--modifier { }

2. ✗ No nesting
   ✗ .block { .element { } }
   ✓ .block { }
     .block__element { }

3. ✓ Same specificity
   .button = 0,0,1,0
   .button--primary = 0,0,1,0

4. ✗ No element nesting in selectors
   ✗ .button .icon { }
   ✓ .button__icon { }

5. ✓ Use pseudo-classes for states
   .button:hover { }
   .button:focus { }
   .button:disabled { }

6. ✓ Modifiers add to base
   <button class="button button--primary">

7. ✗ Don't replace base with modifier
   ✗ class="button--primary"
   ✓ class="button button--primary"

8. ✓ Use CSS variables
   --component-property: value;
*/


// ============================================================================
// 6. JAVASCRIPT INTEGRATION
// ============================================================================

/*
QUERYING ELEMENTS
──────────────────

Selecting elements using BEM classes:

Selecting the block:
  const button = document.querySelector('.button');

Selecting elements within block:
  const icon = button.querySelector('.button__icon');
  const text = button.querySelector('.button__text');

Better: Use data attributes for JS hooks
  <button class="button" data-js-button>
    <svg class="button__icon" data-js-button-icon></svg>
    <span class="button__text" data-js-button-text">Click me</span>
  </button>

Then query with data attributes:
  const button = document.querySelector('[data-js-button]');
  const icon = button.querySelector('[data-js-button-icon]');
  const text = button.querySelector('[data-js-button-text]');

Advantages of data-* attributes:
  ✓ Separate JS hooks from CSS classes
  ✓ Can change CSS without breaking JS
  ✓ Explicit what's used for JavaScript


MANAGING STATE WITH CLASSES
─────────────────────────────

Using classList to toggle modifiers:

Adding a modifier:
  button.classList.add('button--disabled');
  // Button now has class: "button button--disabled"

Removing a modifier:
  button.classList.remove('button--disabled');
  // Button now has class: "button"

Toggling a modifier:
  button.classList.toggle('button--loading');
  // Adds if absent, removes if present

Checking for modifier:
  if (button.classList.contains('button--loading')) {
    console.log('Button is loading');
  }

Multiple modifiers:
  button.classList.add('button--primary');
  button.classList.add('button--large');
  // Button now: "button button--primary button--large"


EXAMPLE: BUTTON COMPONENT WITH JS
────────────────────────────────────

HTML:
  <button class="button button--primary" data-js-button>
    <svg class="button__icon" aria-hidden="true">...</svg>
    <span class="button__text">Click me</span>
  </button>

JavaScript Class:
  class Button {
    constructor(element) {
      this.element = element;
      this.isLoading = false;
      this.init();
    }

    init() {
      // Add click listener
      this.element.addEventListener('click', () => this.handleClick());
    }

    handleClick() {
      // Dispatch custom event for listeners
      const event = new CustomEvent('button:clicked', {
        detail: { buttonId: this.element.id }
      });
      this.element.dispatchEvent(event);
    }

    setLoading(isLoading) {
      this.isLoading = isLoading;
      
      if (isLoading) {
        this.element.classList.add('button--loading');
        this.element.disabled = true;
        this.element.setAttribute('aria-busy', 'true');
      } else {
        this.element.classList.remove('button--loading');
        this.element.disabled = false;
        this.element.setAttribute('aria-busy', 'false');
      }
    }

    disable() {
      this.element.classList.add('button--disabled');
      this.element.disabled = true;
      this.element.setAttribute('aria-disabled', 'true');
    }

    enable() {
      this.element.classList.remove('button--disabled');
      this.element.disabled = false;
      this.element.setAttribute('aria-disabled', 'false');
    }
  }

Usage:
  const button = new Button(document.querySelector('[data-js-button]'));
  
  button.element.addEventListener('button:clicked', (e) => {
    button.setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      button.setLoading(false);
    }, 2000);
  });


SYNCING CSS CLASSES AND ATTRIBUTES
────────────────────────────────────

Keep CSS classes and attributes in sync:

Disabled state:
  // Both class and attribute
  button.classList.add('button--disabled');
  button.setAttribute('aria-disabled', 'true');
  
  OR use HTML attribute:
  button.disabled = true;

Loading state:
  button.classList.add('button--loading');
  button.setAttribute('aria-busy', 'true');

Active state:
  button.classList.add('button--active');
  button.setAttribute('aria-pressed', 'true');  // For toggleable buttons


EXAMPLE: FORM INPUT WITH VALIDATION
──────────────────────────────────────

HTML:
  <div class="input" data-js-input-group>
    <label class="input__label" for="email">Email</label>
    <input 
      type="email" 
      class="input__field" 
      id="email"
      data-js-input-field
    />
    <span class="input__error" data-js-input-error></span>
  </div>

JavaScript:
  class Input {
    constructor(groupElement) {
      this.group = groupElement;
      this.field = this.group.querySelector('[data-js-input-field]');
      this.errorElement = this.group.querySelector('[data-js-input-error]');
      this.validators = [];
      this.init();
    }

    init() {
      this.field.addEventListener('blur', () => this.validate());
      this.field.addEventListener('input', () => this.clearError());
    }

    addValidator(validatorFn) {
      this.validators.push(validatorFn);
    }

    validate() {
      for (const validator of this.validators) {
        const result = validator(this.field.value);
        
        if (result !== true) {
          this.setError(result);
          return false;
        }
      }
      
      this.clearError();
      return true;
    }

    setError(message) {
      this.group.classList.add('input--error');
      this.field.classList.add('input__field--error');
      this.field.setAttribute('aria-invalid', 'true');
      this.errorElement.textContent = message;
    }

    clearError() {
      this.group.classList.remove('input--error');
      this.field.classList.remove('input__field--error');
      this.field.setAttribute('aria-invalid', 'false');
      this.errorElement.textContent = '';
    }

    getValue() {
      return this.field.value;
    }
  }

Usage:
  const emailInput = new Input(document.querySelector('[data-js-input-group]'));
  
  emailInput.addValidator((value) => {
    if (!value) return 'Email is required';
    if (!value.includes('@')) return 'Invalid email format';
    return true;
  });


DELEGATING TO PARENT
──────────────────────

Use event delegation for many elements:

HTML:
  <div class="button-group" data-js-button-group>
    <button class="button button--primary" data-action="save">Save</button>
    <button class="button button--secondary" data-action="cancel">Cancel</button>
    <button class="button button--danger" data-action="delete">Delete</button>
  </div>

JavaScript:
  class ButtonGroup {
    constructor(element) {
      this.element = element;
      this.init();
    }

    init() {
      this.element.addEventListener('click', (e) => {
        const button = e.target.closest('.button');
        if (!button) return;
        
        const action = button.dataset.action;
        this.handleAction(action);
      });
    }

    handleAction(action) {
      switch(action) {
        case 'save':
          console.log('Saving...');
          break;
        case 'cancel':
          console.log('Cancelled');
          break;
        case 'delete':
          console.log('Deleted');
          break;
      }
    }
  }


KEY RULES FOR JS
─────────────────

1. ✓ Use data-* attributes for JS hooks
   <button class="button" data-js-button>

2. ✓ Query by data attributes
   querySelector('[data-js-button]')

3. ✓ Use classList to manage modifiers
   element.classList.add('button--loading')

4. ✓ Sync classes with ARIA attributes
   classList.add + setAttribute in same method

5. ✗ Don't query by CSS classes if avoidable
   ✗ querySelector('.button__text')  (too specific)
   ✓ querySelector('[data-js-button-text]')  (explicit)

6. ✓ Dispatch custom events for communication
   element.dispatchEvent(new CustomEvent('button:clicked'))

7. ✓ Keep JS and CSS synchronized
   If CSS expects .button--disabled, JS should add it
*/


// ============================================================================
// 7. ADVANCED PATTERNS
// ============================================================================

/*
MIXIN CLASSES
──────────────

Reusing styles across different blocks:

Problem:
  .button { padding: 10px; }
  .link { padding: 10px; }
  
  Both have same padding, but in BEM we need separate classes.

Solution 1: Extend at HTML level
  <button class="button padding-utility">
  <a class="link padding-utility">

Solution 2: Common styles in shared rule
  .button,
  .link {
    padding: 10px;
    border: none;
  }

Solution 3: CSS Variables (best)
  :root {
    --spacing-default: 10px;
  }
  
  .button {
    padding: var(--spacing-default);
  }
  
  .link {
    padding: var(--spacing-default);
  }


PSEUDO-ELEMENTS WITH MODIFIERS
────────────────────────────────

Use pseudo-elements for decorative content:

✓ Correct:
  .button::before {
    content: '';
    display: block;
    /* ... */
  }

✓ With modifier:
  .button--loading::after {
    content: '';
    animation: spin 1s linear infinite;
  }

The ::before and ::after don't need BEM names.
They're part of the element they decorate.


NESTING BLOCKS WITHIN BLOCKS
──────────────────────────────

You can nest blocks, but keep them independent:

Example - Card with Button inside:
  <article class="card">
    <h2 class="card__title">Title</h2>
    <p class="card__text">Content</p>
    
    <!-- Button is a separate block -->
    <button class="button button--primary">
      Learn more
    </button>
  </article>

CSS:
  .card {
    padding: 20px;
    border: 1px solid #ccc;
  }

  .card__title {
    font-size: 20px;
  }

  .card__text {
    margin-bottom: 10px;
  }

  .button {
    /* Button styles - independent */
  }

Key: Button is not .card__button. It's a standalone .button.


CONTEXT MODIFIERS
───────────────────

Sometimes a block needs slight adjustments based on context:

Option 1: Container class
  <div class="sidebar">
    <button class="button button--primary">Action</button>
  </div>

  CSS:
    .sidebar .button {
      /* Adjustments in sidebar */
      width: 100%;
    }

Option 2: Block modifier for context
  <div class="sidebar">
    <button class="button button--primary button--in-sidebar">
      Action
    </button>
  </div>

  CSS:
    .button--in-sidebar {
      width: 100%;
    }

Option 3: CSS variables (best)
  <div class="sidebar" style="--button-width: 100%">
    <button class="button button--primary">Action</button>
  </div>

  CSS:
    .button {
      width: var(--button-width, auto);
    }


MULTIPLE VARIANTS
───────────────────

Managing many combinations:

Don't:
  .button--primary-small
  .button--primary-large
  .button--secondary-small
  .button--secondary-large

Do:
  .button--primary
  .button--secondary
  .button--small
  .button--large

  <!-- Combine in HTML -->
  <button class="button button--primary button--small">

Advantages:
  ✓ Less CSS
  ✓ More flexible
  ✓ Modifiers are independent
  ✓ Easy to combine


UTILITY-LIKE MODIFIERS
───────────────────────

Some modifiers are like utilities:

  .button--margin-right {
    margin-right: 10px;
  }

  .button--full-width {
    width: 100%;
  }

But usually better to use CSS classes separately:

  <button class="button button--primary margin-right-md full-width">

Or use spacing utilities:

  <button class="button button--primary mr-md w-full">


OPTIONAL ELEMENTS
───────────────────

Elements that might not always be present:

CSS should still style all elements:
  .button { }
  .button__icon { }  <!-- May not be present -->
  .button__text { }  <!-- May not be present -->

HTML options:
  <button class="button">Just text</button>

  <button class="button">
    <svg class="button__icon"></svg>
    Just icon
  </button>

  <button class="button">
    <svg class="button__icon"></svg>
    <span class="button__text">Text</span>
  </button>

All valid - CSS handles missing elements gracefully.
*/


// ============================================================================
// 8. REAL-WORLD EXAMPLES
// ============================================================================

/*
EXAMPLE 1: BUTTON COMPONENT (COMPLETE)
──────────────────────────────────────────

HTML:
────

  <button class="button button--primary" data-js-button>
    <svg class="button__icon" aria-hidden="true">
      <use href="#icon-arrow"></use>
    </svg>
    <span class="button__text">Click me</span>
  </button>

  <button class="button button--secondary button--disabled">
    Disabled Button
  </button>

  <button class="button button--large button--block">
    Full Width Large Button
  </button>

CSS:
────

  /* Base button */
  .button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    
    font-size: 16px;
    font-weight: 600;
    font-family: inherit;
    
    cursor: pointer;
    transition: all 0.3s ease;
    
    user-select: none;
    -webkit-user-select: none;
  }

  /* Focus */
  .button:focus-visible {
    outline: 2px solid;
    outline-offset: 2px;
  }

  /* Disabled */
  .button:disabled,
  .button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }

  /* Elements */
  .button__icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
  }

  .button__text {
    /* Default - flex handles it */
  }

  /* Variants */
  .button--primary {
    background-color: #007bff;
    color: white;
  }

  .button--primary:hover:not(:disabled) {
    background-color: #0056b3;
  }

  .button--secondary {
    background-color: #6c757d;
    color: white;
  }

  .button--secondary:hover:not(:disabled) {
    background-color: #5a6268;
  }

  /* Sizes */
  .button--small {
    padding: 8px 16px;
    font-size: 14px;
  }

  .button--large {
    padding: 16px 32px;
    font-size: 18px;
  }

  /* Full Width */
  .button--block {
    display: flex;
    width: 100%;
  }

  /* Loading */
  .button--loading {
    position: relative;
  }

  .button--loading::after {
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

JavaScript:
────────────

  class Button {
    constructor(element) {
      this.element = element;
      this.isLoading = false;
      this.init();
    }

    init() {
      this.element.addEventListener('click', () => this.handleClick());
    }

    handleClick() {
      const event = new CustomEvent('button:click');
      this.element.dispatchEvent(event);
    }

    setLoading(isLoading) {
      this.isLoading = isLoading;
      this.element.classList.toggle('button--loading', isLoading);
      this.element.disabled = isLoading;
    }
  }

  document.querySelectorAll('[data-js-button]').forEach(el => {
    new Button(el);
  });


EXAMPLE 2: FORM INPUT COMPONENT
─────────────────────────────────

HTML:
────

  <div class="input" data-js-input-group>
    <label class="input__label" for="email">Email</label>
    <input
      type="email"
      class="input__field"
      id="email"
      data-js-input-field
      required
    />
    <span class="input__hint">We won't spam you</span>
    <span class="input__error" data-js-input-error></span>
  </div>

CSS:
────

  .input {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .input__label {
    font-size: 14px;
    font-weight: 600;
    color: #333;
  }

  .input__field {
    padding: 12px;
    font-size: 16px;
    border: 2px solid #e0e0e0;
    border-radius: 4px;
    transition: all 0.3s ease;
    font-family: inherit;
  }

  .input__field:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
  }

  .input__hint {
    font-size: 13px;
    color: #666;
    font-style: italic;
  }

  .input__error {
    display: none;
    font-size: 13px;
    color: #dc3545;
    font-weight: 500;
  }

  /* Error state */
  .input--error {
    /* Container state */
  }

  .input--error .input__field {
    border-color: #dc3545;
    background-color: #fff5f5;
  }

  .input--error .input__error {
    display: block;
  }

JavaScript:
────────────

  class Input {
    constructor(groupEl) {
      this.group = groupEl;
      this.field = this.group.querySelector('[data-js-input-field]');
      this.errorEl = this.group.querySelector('[data-js-input-error]');
      this.validators = [];
      this.init();
    }

    init() {
      this.field.addEventListener('blur', () => this.validate());
      this.field.addEventListener('input', () => this.clearError());
    }

    addValidator(fn) {
      this.validators.push(fn);
    }

    validate() {
      for (const validator of this.validators) {
        const result = validator(this.field.value);
        if (result !== true) {
          this.setError(result);
          return false;
        }
      }
      this.clearError();
      return true;
    }

    setError(message) {
      this.group.classList.add('input--error');
      this.field.setAttribute('aria-invalid', 'true');
      this.errorEl.textContent = message;
    }

    clearError() {
      this.group.classList.remove('input--error');
      this.field.setAttribute('aria-invalid', 'false');
      this.errorEl.textContent = '';
    }
  }


EXAMPLE 3: MODAL DIALOG COMPONENT
───────────────────────────────────

HTML:
────

  <div class="modal" role="dialog" aria-modal="true" data-js-modal>
    <div class="modal__overlay" data-js-modal-close></div>
    
    <div class="modal__content">
      <button class="modal__close" data-js-modal-close" aria-label="Close">
        ×
      </button>
      
      <div class="modal__header">
        <h2 class="modal__title">Dialog Title</h2>
      </div>
      
      <div class="modal__body">
        <p>Content goes here</p>
      </div>
      
      <div class="modal__footer">
        <button class="button button--secondary" data-js-modal-close>
          Cancel
        </button>
        <button class="button button--primary">
          Confirm
        </button>
      </div>
    </div>
  </div>

CSS:
────

  .modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
  }

  .modal--open {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal__overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    cursor: pointer;
  }

  .modal__content {
    position: relative;
    background: white;
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow: auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    
    display: flex;
    flex-direction: column;
  }

  .modal__close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: transparent;
    border: none;
    font-size: 24px;
    cursor: pointer;
    padding: 8px;
  }

  .modal__header {
    padding: 32px 32px 16px;
    border-bottom: 1px solid #e0e0e0;
  }

  .modal__title {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
  }

  .modal__body {
    padding: 24px 32px;
    flex: 1;
    overflow: auto;
  }

  .modal__footer {
    padding: 16px 32px;
    border-top: 1px solid #e0e0e0;
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }

JavaScript:
────────────

  class Modal {
    constructor(element) {
      this.element = element;
      this.isOpen = false;
      this.init();
    }

    init() {
      // Close buttons
      const closeButtons = this.element.querySelectorAll('[data-js-modal-close]');
      closeButtons.forEach(btn => {
        btn.addEventListener('click', () => this.close());
      });

      // Escape key
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen) {
          this.close();
        }
      });
    }

    open() {
      this.isOpen = true;
      this.element.classList.add('modal--open');
      this.element.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    close() {
      this.isOpen = false;
      this.element.classList.remove('modal--open');
      this.element.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = 'auto';
    }
  }

*/


// ============================================================================
// 9. COMMON MISTAKES & SOLUTIONS
// ============================================================================

/*
MISTAKE 1: Wrong Separator
──────────────────────────

✗ Wrong:
  .button-icon    ← Single hyphen (block-like)
  .button__-icon  ← Double hyphen after underscore
  .button---icon  ← Three hyphens

✓ Right:
  .button__icon   ← Double underscore for element
  .button--primary ← Double hyphen for modifier


MISTAKE 2: Nesting Elements
───────────────────────────

✗ Wrong:
  .button__wrapper__inner
  .form__group__input
  .card__content__text

✓ Right:
  .button__wrapper (if needed as separate element)
  .button__inner
  .form__input (no group nesting)
  .card__text (no content nesting)

Why: Elements belong directly to block, not to other elements.


MISTAKE 3: Nesting in CSS
──────────────────────────

✗ Wrong:
  .button {
    padding: 10px;
    
    .icon {        ← Nesting (even in SCSS)
      width: 20px;
    }
  }

✓ Right:
  .button {
    padding: 10px;
  }

  .button__icon {
    width: 20px;
  }

Reason: Even with SCSS, flat structure is clearer.


MISTAKE 4: Forgetting Base Class
─────────────────────────────────

✗ Wrong:
  <button class="button--primary">
  
  Should always have base:
  <button class="button button--primary">

✓ Right:
  <button class="button button--primary">
  
  Modifier adds to base, doesn't replace it.


MISTAKE 5: Confusing Multiple Blocks
──────────────────────────────────────

✗ Wrong:
  class="form form__button"     ← Button is not element of form
  class="card form__input"      ← Mixing unrelated blocks

✓ Right:
  class="form"
  <button class="button">       ← Separate block
  
  class="card"
  <input class="input">         ← Separate block


MISTAKE 6: One Block Multiple Classes
───────────────────────────────────────

✗ Wrong:
  class="button--primary--large"  ← Wrong, only one modifier per hyphen set
  
✓ Right:
  class="button button--primary button--large"  ← Multiple modifier classes


MISTAKE 7: Styling by Position
────────────────────────────────

✗ Wrong:
  .button:first-child {
    margin-left: 0;
  }

  This styles differently based on position, not semantic meaning.

✓ Right:
  .button--first {
    margin-left: 0;
  }
  
  Or use flexbox/grid, not position-based styling.


MISTAKE 8: Cascade Dependencies
───────────────────────────────

✗ Wrong:
  .form .button {
    width: 100%;
  }

  Now buttons inside forms are different. Bad.

✓ Right:
  .button--block {
    width: 100%;
  }
  
  <button class="button button--block">


MISTAKE 9: Too Many Elements
──────────────────────────────

If a component has many sub-parts, reconsider structure:

✗ Possibly wrong:
  .panel__header
  .panel__nav
  .panel__nav-item
  .panel__nav-link
  .panel__content
  .panel__content-section
  .panel__footer

Consider: Are some of these independent blocks?

✓ Better:
  .panel (main component)
  .panel__header
  .panel__content
  .panel__footer

  And inside:
  .navigation (separate block)
  .section (separate block)


MISTAKE 10: Inconsistent Naming
────────────────────────────────

✗ Wrong:
  .button__icon    (one component)
  .card-image      (another component, different style)
  .form_input      (third component, underscore separator)

✓ Right:
  .button__icon
  .card__image
  .form__input

All consistent naming throughout project.


FIXES SUMMARY
──────────────

| Mistake | Wrong | Right |
|---------|-------|-------|
| Separators | .button-icon | .button__icon |
| Nested elements | .button__inner__wrapper | .button__inner |
| Nested CSS | .button { .icon {} } | .button { } .button__icon { } |
| Missing base | .button--primary | .button.button--primary |
| Element-like | .form__button | .button (separate) |
| Position-based | .button:first-child { } | .button--first { } |
| Multiple modifiers | .button--primary-large | .button--primary.button--large |
| Cascade | .form .button { } | .button--block { } |
| Inconsistent | .btn, .btn-, btn_ | .button__ (consistent) |
*/


// ============================================================================
// 10. BEM WITH CSS MODULES
// ============================================================================

/*
CSS MODULES OVERVIEW
─────────────────────

CSS Modules automatically scope class names:

Without CSS Modules (BEM):
  /* button.css */
  .button { }
  .button__icon { }

  /* Global scope - could conflict */

With CSS Modules:
  /* button.module.css */
  .button { }
  .button__icon { }

  /* Becomes: button_button__2a3b, button_button__icon__4c5d */
  /* Scoped - no conflicts */


COMBINING BEM WITH CSS MODULES
────────────────────────────────

CSS Modules add a hash to prevent conflicts.
BEM is still useful for semantics and naming.

File: Button.module.css
────────────────────────

  .button {
    display: inline-block;
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .button:hover {
    background-color: #0056b3;
  }

  /* Elements */
  .icon {
    width: 20px;
    height: 20px;
    margin-right: 8px;
  }

  /* Modifiers */
  .primary {
    background-color: #007bff;
  }

  .secondary {
    background-color: #6c757d;
  }

  .disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

Note: In CSS Modules, you usually drop the full BEM names
and just use local names since they're scoped anyway.

HTML/JSX:
──────────

  import styles from './Button.module.css';

  function Button({ variant = 'primary', disabled, children }) {
    return (
      <button
        className={`
          ${styles.button}
          ${styles[variant]}
          ${disabled ? styles.disabled : ''}
        `}
        disabled={disabled}
      >
        {children}
      </button>
    );
  }

Or with classnames library:

  import styles from './Button.module.css';
  import classNames from 'classnames';

  function Button({ variant = 'primary', disabled, children }) {
    return (
      <button
        className={classNames(
          styles.button,
          styles[variant],
          { [styles.disabled]: disabled }
        )}
        disabled={disabled}
      >
        {children}
      </button>
    );
  }


FULL EXAMPLE WITH CSS MODULES
───────────────────────────────

Directory structure:
  components/
  └── Button/
      ├── Button.jsx
      ├── Button.module.css
      └── Button.test.jsx

Button.module.css:
─────────────────

  .button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    
    font-size: 16px;
    font-weight: 600;
    font-family: inherit;
    
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .button:focus-visible {
    outline: 2px solid;
    outline-offset: 2px;
  }

  .button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Elements */
  .icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
  }

  .text {
    flex: 1;
  }

  /* Variants */
  .primary {
    background-color: #007bff;
    color: white;
  }

  .primary:hover:not(:disabled) {
    background-color: #0056b3;
  }

  .secondary {
    background-color: #6c757d;
    color: white;
  }

  .secondary:hover:not(:disabled) {
    background-color: #5a6268;
  }

  /* Sizes */
  .small {
    padding: 8px 16px;
    font-size: 14px;
  }

  .large {
    padding: 16px 32px;
    font-size: 18px;
  }

  /* Full width */
  .block {
    display: flex;
    width: 100%;
  }

Button.jsx:
────────────

  import styles from './Button.module.css';
  import classNames from 'classnames';

  export function Button({
    variant = 'primary',
    size = 'medium',
    fullWidth = false,
    disabled = false,
    icon,
    children,
    ...props
  }) {
    const buttonClasses = classNames(
      styles.button,
      styles[variant],
      {
        [styles.small]: size === 'small',
        [styles.large]: size === 'large',
        [styles.block]: fullWidth
      }
    );

    return (
      <button
        className={buttonClasses}
        disabled={disabled}
        {...props}
      >
        {icon && <span className={styles.icon}>{icon}</span>}
        {children && <span className={styles.text}>{children}</span>}
      </button>
    );
  }

Usage:
───────

  <Button variant="primary">
    Click me
  </Button>

  <Button
    variant="secondary"
    size="large"
    fullWidth
    disabled
  >
    Disabled
  </Button>

  <Button
    variant="primary"
    icon={<CheckIcon />}
  >
    Save
  </Button>


CSS MODULES VS BEM
────────────────────

| Aspect | BEM | CSS Modules + BEM |
|--------|-----|-------------------|
| Naming | Full BEM names | Short local names |
| Scope | Global (need careful naming) | Scoped (no conflicts) |
| Complexity | Manual naming discipline | Automatic scoping |
| Flexibility | Modular but verbose | Clean and simple |
| Team size | Better for large teams | Good for any size |
| Migration | Easy from nothing | Needs build tools |

Best: Use CSS Modules with BEM for class organization.
*/


// ============================================================================
// 11. BEM WITH SASS/SCSS
// ============================================================================

/*
SCSS NESTING FOR BEM
─────────────────────

SCSS allows nesting, but we maintain flat output:

❌ DON'T DO THIS (bad practice):
  .button {
    padding: 10px;

    .icon {        // This becomes .button .icon (nesting)
      width: 20px;
    }

    &--primary {   // This is OK - generates .button--primary
      background: blue;
    }
  }

✓ DO THIS (using &):
  .button {
    padding: 10px;

    &__icon {      // Generates .button__icon (correct)
      width: 20px;
    }

    &--primary {   // Generates .button--primary (correct)
      background: blue;
    }

    &:hover {      // Generates .button:hover (correct)
      opacity: 0.9;
    }
  }


FULL SCSS BUTTON EXAMPLE
─────────────────────────

File: button.scss

  // Variables
  $button-padding: 12px 24px;
  $button-bg-primary: #007bff;
  $button-bg-hover: #0056b3;
  $button-radius: 4px;
  $button-font-size: 16px;
  $button-font-weight: 600;

  // Button base
  .button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    padding: $button-padding;
    border: none;
    border-radius: $button-radius;

    font-size: $button-font-size;
    font-weight: $button-font-weight;
    font-family: inherit;

    cursor: pointer;
    transition: all 0.3s ease;
    user-select: none;
    -webkit-user-select: none;

    // Focus
    &:focus-visible {
      outline: 2px solid currentColor;
      outline-offset: 2px;
    }

    // Disabled
    &:disabled,
    &--disabled {
      opacity: 0.6;
      cursor: not-allowed;
      pointer-events: none;
    }

    // Elements
    &__icon {
      width: 20px;
      height: 20px;
      flex-shrink: 0;
    }

    &__text {
      flex: 1;
    }

    // Modifiers - Color
    &--primary {
      background-color: $button-bg-primary;
      color: white;

      &:hover:not(:disabled) {
        background-color: $button-bg-hover;
        box-shadow: 0 4px 12px rgba($button-bg-primary, 0.3);
      }

      &:active:not(:disabled) {
        background-color: darken($button-bg-hover, 10%);
      }
    }

    &--secondary {
      background-color: #6c757d;
      color: white;

      &:hover:not(:disabled) {
        background-color: #5a6268;
      }
    }

    &--danger {
      background-color: #dc3545;
      color: white;

      &:hover:not(:disabled) {
        background-color: #c82333;
      }
    }

    // Modifiers - Size
    &--small {
      padding: 8px 16px;
      font-size: 14px;
    }

    &--large {
      padding: 16px 32px;
      font-size: 18px;
    }

    // Modifiers - State
    &--loading {
      position: relative;

      &::after {
        content: '';
        display: inline-block;
        width: 14px;
        height: 14px;
        margin-left: 8px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 0.8s linear infinite;
      }
    }

    // Modifiers - Full width
    &--block {
      display: flex;
      width: 100%;
    }
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }


USING MIXINS
──────────────

For truly shared styles:

  @mixin button-reset {
    border: none;
    padding: 0;
    font-family: inherit;
    cursor: pointer;
  }

  @mixin focus-outline {
    &:focus-visible {
      outline: 2px solid currentColor;
      outline-offset: 2px;
    }
  }

  .button {
    @include button-reset;
    @include focus-outline;
    
    // ... rest of styles
  }


SCSS VARIABLES FOR THEME
──────────────────────────

Organize variables by component:

  // _colors.scss
  $color-primary: #007bff;
  $color-secondary: #6c757d;
  $color-danger: #dc3545;

  // _spacing.scss
  $spacing-xs: 4px;
  $spacing-sm: 8px;
  $spacing-md: 12px;
  $spacing-lg: 24px;

  // _typography.scss
  $font-size-sm: 14px;
  $font-size-base: 16px;
  $font-size-lg: 18px;

  // button.scss
  @import 'colors';
  @import 'spacing';
  @import 'typography';

  .button {
    padding: $spacing-md $spacing-lg;
    font-size: $font-size-base;
    background-color: $color-primary;
  }


MAINTAINING BEM IN SCSS
────────────────────────

Tips:

1. Use & for nesting elements and modifiers
   &__element { }
   &--modifier { }

2. DON'T nest child elements
   ✗ &__element { &__sub { } }
   ✓ &__element { }
     &__sub { }

3. Keep output flat
   Compiled CSS should be flat BEM, not nested

4. Use variables for colors, sizing, spacing
   Keeps design system consistent

5. Use mixins for genuinely shared styles
   Most styles should be on specific components

Compiled output should always be:
  .button { }
  .button__icon { }
  .button--primary { }

Not:
  .button { }
  .button .icon { }  ← This is wrong
*/


// ============================================================================
// 12. BEM VS OTHER METHODOLOGIES
// ============================================================================

/*
BEM vs OOCSS (Object Oriented CSS)
───────────────────────────────────

OOCSS:
  Separates structure from skin
  .button { border: 1px; }
  .blue-button { background: blue; }

  <button class="button blue-button">

BEM:
  Structure and skin together
  .button { }
  .button--primary { background: blue; }

  <button class="button button--primary">

BEM advantage: Clearer naming and intent


BEM vs SMACSS (Scalable Modular Architecture)
───────────────────────────────────────────────

SMACSS:
  Categories: Base, Layout, Module, State, Theme
  Classes by purpose

BEM:
  Block, Element, Modifier
  Classes by structure

Both good. BEM is more specific about naming.


BEM vs Utility-First (Tailwind)
─────────────────────────────────

Utility-first (Tailwind):
  <button class="bg-blue-500 px-4 py-2 rounded text-white">

BEM:
  <button class="button button--primary">

Trade-offs:
  Utility-first: More flexible, more verbose HTML
  BEM: More readable HTML, more CSS to write

Many prefer mixing: semantic classes + utilities
  <button class="button button--primary p-4">


BEM vs CSS-in-JS
──────────────────

CSS-in-JS:
  Styles scoped to component automatically
  No naming conflicts

  const buttonStyle = css`
    background-color: #007bff;
    padding: 12px 24px;
  `;

BEM:
  Manual naming to avoid conflicts
  Global CSS (loaded once)

  .button { background-color: #007bff; }

Both work. BEM is simpler for many projects.


RECOMMENDATION
────────────────

Use BEM when:
  ✓ Traditional CSS workflow
  ✓ Need predictable, scalable naming
  ✓ Team of any size
  ✓ Plain HTML/CSS/JS
  ✓ Don't want build complexity

Use CSS-in-JS when:
  ✓ Using React/Vue/etc
  ✓ Want automatic scoping
  ✓ Dynamic styles from props
  ✓ Heavy component dependency

Use Utility-first when:
  ✓ Want rapid prototyping
  ✓ Design tokens are clear
  ✓ Team comfortable with HTM L

Best: Hybrid approach
  Use BEM component naming
  Add utility classes for spacing/layout
  Use CSS Modules for scoping
*/


// ============================================================================
// 13. PERFORMANCE CONSIDERATIONS
// ============================================================================

/*
CSS SIZE
─────────

BEM is efficient:
  • Flat selectors (all classes, no nesting)
  • Same specificity (no escalation)
  • Reusable patterns

Typical BEM stylesheet size:
  Small component (Button): 1-2 KB
  Medium component (Form): 3-5 KB
  Large component (Table): 5-10 KB
  System of 50 components: 200-400 KB


SELECTORS PERFORMANCE
──────────────────────

BEM uses class selectors only:
  .button { }          ← Very fast
  .button__icon { }    ← Very fast
  .button--primary { } ← Very fast

Slower selectors to avoid:
  .button .icon { }    ← Descendant (slower)
  .button > div { }    ← Child (slow)
  [data-button] { }    ← Attribute (slow)

BEM is optimized for selector speed.


CLASS RENDERING
────────────────

When element gets classes:
  <button class="button button--primary button--loading">

Browser applies in order:
  1. .button styles
  2. .button--primary styles (override if conflict)
  3. .button--loading styles (override if conflict)

All classes are equally specific, so order matters:
  Put specifics after base in CSS file.


REFLOW/REPAINT
────────────────

Adding/removing BEM classes:
  element.classList.add('button--loading');
  
Causes repaint (fast) not reflow (slow) because:
  • Just changing appearance
  • Not changing layout
  • Structure stays same

Good for performance.


CSS FILE SIZE OPTIMIZATION
────────────────────────────

Keep BEM files small:

✓ Good:
  Each component has own CSS file
  Import only what you need
  Total: 50 components × 5KB = 250KB

✗ Bad:
  One massive global CSS file
  All styles loaded always
  Total: 500KB always

Use CSS bundlers:
  • Minification: 250KB → 180KB
  • Gzip: 180KB → 45KB
  • Tree-shaking: Remove unused styles


MEDIA QUERY OPTIMIZATION
──────────────────────────

BEM with responsive:

  .button { padding: 12px 24px; }

  .button--mobile {
    padding: 8px 12px;
  }

  @media (max-width: 768px) {
    .button {
      padding: 8px 12px;
    }
  }

Or use CSS variables for cleaner approach:

  :root {
    --button-padding: 12px 24px;
  }

  @media (max-width: 768px) {
    :root {
      --button-padding: 8px 12px;
    }
  }

  .button {
    padding: var(--button-padding);
  }


JAVASCRIPT PERFORMANCE
───────────────────────

classList is efficient:
  element.classList.add('button--loading');     ← Fast
  element.classList.remove('button--loading');  ← Fast
  element.classList.toggle('button--loading');  ← Fast

Better than:
  element.className += ' button--loading';      ← Slower
  element.style.opacity = '0.6';                ← Slower


CRITICAL RENDERING PATH
─────────────────────────

BEM doesn't block rendering:
  • Flat selectors parse quickly
  • No deep cascade to calculate
  • Simple specificity

Result: Faster rendering than complex selectors.
*/


// ============================================================================
// 14. ACCESSIBILITY IN BEM
// ============================================================================

/*
ARIA ATTRIBUTES WITH BEM
──────────────────────────

Use BEM classes for styling.
Use ARIA attributes for accessibility.
Keep them in sync.

Example - Button disabled state:

HTML:
  <button class="button button--disabled" aria-disabled="true">
    Disabled Button
  </button>

CSS:
  .button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }

JavaScript:
  button.classList.add('button--disabled');
  button.setAttribute('aria-disabled', 'true');

Why: Screen reader must know button is disabled


EXAMPLE - ERROR STATE
──────────────────────

HTML:
  <div class="input input--error">
    <input class="input__field" aria-invalid="true" />
    <span class="input__error" role="alert">
      Email is invalid
    </span>
  </div>

CSS:
  .input--error .input__field {
    border-color: #dc3545;
    background: #fff5f5;
  }

JavaScript:
  input.classList.add('input--error');
  input.setAttribute('aria-invalid', 'true');


SEMANTIC HTML WITH BEM
────────────────────────

Use semantic elements as blocks:

✓ Right:
  <nav class="navigation">
    <ul class="navigation__list">
      <li class="navigation__item">
        <a class="navigation__link">Home</a>
      </li>
    </ul>
  </nav>

  <button class="button button--primary">
    Click
  </button>

  <article class="post">
    <h1 class="post__title">Title</h1>
  </article>

✗ Wrong:
  <div class="navigation">
    <div class="navigation__list">
      <div class="navigation__item">
        <div class="navigation__link">Home</div>
      </div>
    </div>
  </div>

  <div class="button">
    Click
  </div>


FOCUS STATES WITH BEM
──────────────────────

Every interactive element needs focus styles:

  .button:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
  }

  .button--disabled:focus-visible {
    outline: none;
  }

Good focus styles:
  ✓ 2px outline minimum
  ✓ High contrast color
  ✓ Clear visible indicator
  ✓ Not hidden behind other elements


SKIP LINKS WITH BEM
─────────────────────

Help keyboard users skip navigation:

  <a class="skip-link" href="#main-content">
    Skip to main content
  </a>

  <nav class="navigation">...</nav>

  <main id="main-content" class="main">
    ...
  </main>

CSS:
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
  }

  .skip-link:focus {
    top: 0;
  }


LABELING WITH BEM
───────────────────

Always connect labels to inputs:

  <div class="form__group">
    <label class="form__label" for="email">
      Email
    </label>
    <input
      type="email"
      class="form__input"
      id="email"
    />
  </div>

Never:
  <label class="form__label">
    Email
    <input type="email" class="form__input" />
  </label>

Better: Explicit connection with for/id


COLOR CONTRAST WITH BEM
─────────────────────────

Ensure minimum contrast ratios:

  .button--primary {
    background-color: #007bff;    ← 65% luminance
    color: white;                 ← 100% luminance
    /* Contrast ratio: 8.59:1 ✓ */
  }

  .text--secondary {
    color: #666666;  ← Low contrast on white
    /* Contrast ratio: 4.48:1 - OK but borderline */
  }

Accessibility standards:
  Normal text: 4.5:1 minimum
  Large text (18px+): 3:1 minimum
  UI components: 3:1 minimum


REDUCED MOTION WITH BEM
─────────────────────────

Respect user's motion preferences:

CSS:
  @media (prefers-reduced-motion: reduce) {
    .button {
      transition: none;
      animation: none;
    }

    .button--loading::after {
      animation: none;
    }
  }

JavaScript:
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Remove animations
  }


EMPTY STATE MESSAGES
──────────────────────

Make empty states accessible:

  <div class="empty-state">
    <svg class="empty-state__icon" aria-hidden="true">
      ...
    </svg>
    <h2 class="empty-state__title">
      No results found
    </h2>
    <p class="empty-state__description">
      Try a different search term
    </p>
  </div>

Note aria-hidden="true" on decorative icon.
*/


// ============================================================================
// 15. SCALING BEM (DESIGN SYSTEMS)
// ============================================================================

/*
ORGANIZING LARGE SYSTEMS
──────────────────────────

For 50+ components:

components/
├── Button/
│   ├── Button.css
│   └── Button.md
├── Input/
├── Card/
├── Modal/
├── Navigation/
└── ...

shared/
├── _variables.css    (colors, spacing, sizing)
├── _reset.css        (normalize styles)
├── _typography.css   (fonts, sizes)
└── _utilities.css    (common patterns)

index.css             (import all)


NAMING CONVENTIONS FOR SCALE
──────────────────────────────

When team is large, standardize:

✓ Use single-word block names where possible
  .button not .btn-component
  .card not .card-item
  .navigation not .nav-bar

✓ Consistent element naming
  All blocks have: __label, __content, __footer (if they need them)
  Don't use: __info, __body, __wrapper (confusing across components)

✓ Standard modifiers
  Variants: --primary, --secondary, --danger
  Sizes: --small, --medium, --large (not --sm, --md, --lg)
  States: --active, --disabled, --loading (standard states)


SHARED PATTERNS ACROSS COMPONENTS
────────────────────────────────────

Common modifiers across system:

All interactive components:
  .{component}--disabled
  .{component}--loading
  .{component}--active

All sizing:
  --small, --medium, --large (consistent across all)

All color variants:
  --primary, --secondary, --danger, --success (same everywhere)

Example - Consistency:

  .button--primary     ← Blue, for main actions
  .input--primary      ← Blue, for main inputs
  .card--primary       ← Blue variant

  .button--disabled    ← Dimmed, can't click
  .input--disabled     ← Dimmed, can't type
  .form--disabled      ← Dimmed, can't submit


COMPONENT DOCUMENTATION
────────────────────────

Each component needs docs:

components/Button/README.md:
────────────────────────────

# Button Component

## Description
Primary call-to-action component.

## Markup
```html
<button class="button button--primary">
  Click me
</button>
```

## CSS Classes
- `.button` - Base button
- `.button__icon` - Icon inside button
- `.button__text` - Text inside button
- `.button--primary` - Blue, for main actions
- `.button--secondary` - Gray, for secondary actions
- `.button--disabled` - Disabled state
- `.button--loading` - Loading state
- `.button--small` - Small size
- `.button--large` - Large size
- `.button--block` - Full width

## Modifiers
Can combine: `class="button button--primary button--large"`

## States
- Hover: Darker background
- Active: Even darker
- Focus: Outline
- Disabled: Dimmed, no interaction

## Usage in Code
```javascript
const button = new Button(document.querySelector('.button'));
button.setLoading(true);
button.disable();
```

## Browser Support
Chrome, Firefox, Safari, Edge (latest versions)

## Accessibility
- Proper focus states
- ARIA labels
- Keyboard accessible
- Works with screen readers

## Related Components
- Input: Form field
- Form: Form container


VERSIONING COMPONENTS
───────────────────────

Track changes:

components/Button/CHANGELOG.md:
────────────────────────────────

## v2.1.0 (2024-03-16)
- Added loading state animation
- Improved focus styles for accessibility
- New CSS variable system

## v2.0.0 (2024-02-01) - BREAKING
- Renamed .button-icon to .button__icon
- Renamed .btn-primary to .button--primary
- Removed deprecated .button-disabled modifier

## v1.0.0 (2024-01-01)
- Initial release


THEMING WITH BEM
──────────────────

Organize colors as theme:

shared/_colors.css:
────────────────────

  :root {
    --color-primary: #007bff;
    --color-secondary: #6c757d;
    --color-danger: #dc3545;
    --color-success: #28a745;
    ...
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --color-primary: #0d6efd;
      --color-secondary: #6c757d;
      ...
    }
  }

button.css:
────────────

  .button--primary {
    background-color: var(--color-primary);
  }

  .button--secondary {
    background-color: var(--color-secondary);
  }

  .button--danger {
    background-color: var(--color-danger);
  }

Now changing theme only requires updating variables!


COMPONENT DEPENDENCIES
───────────────────────

Map which components use which others:

Button depends on: nothing
Input depends on: nothing
Form depends on: Button, Input
Modal depends on: Button
Navigation depends on: nothing

This helps with versioning and updates.
*/


// ============================================================================
// 16. MIGRATION GUIDE
// ============================================================================

/*
MIGRATING FROM NO NAMING CONVENTION
──────────────────────────────────────

Before (chaos):
  .header { }
  .header .button { }
  .button { }
  .button:hover { }
  .button.active { }
  .btn-primary { }
  .form-group > .input { }

After (BEM):
  .header { }
  .header__nav { }
  .header__button { } OR .button (separate)
  
  .button { }
  .button:hover { }
  .button--active { }
  .button--primary { }

  .form { }
  .form__group { }
  .form__input { }

Steps:

1. Identify independent components
   (Button, Card, Form, Modal, Navigation)

2. For each component, create BEM structure
   Block: component name
   Elements: major parts
   Modifiers: variants and states

3. Rename CSS classes to BEM
   Do it systematically, component by component

4. Update HTML to use new class names

5. Update JavaScript selectors

6. Test everything

7. Update team documentation


MIGRATING FROM BOOTSTRAP
─────────────────────────

Bootstrap (utility-class heavy):
  <button class="btn btn-primary btn-lg">

BEM (semantic classes):
  <button class="button button--primary button--large">

Differences:
  Bootstrap abbreviates: btn, btn-lg, btn-primary
  BEM is explicit: button, button--large, button--primary

Migration:
  1. Remove Bootstrap CSS
  2. Create BEM CSS (similar structure, better naming)
  3. Update HTML classes
  4. Adjust JavaScript selectors

Bootstrap CSS:
  .btn { padding: 10px; }
  .btn-primary { background: blue; }
  .btn-lg { padding: 15px; }

BEM CSS (equivalent):
  .button { padding: 10px; }
  .button--primary { background: blue; }
  .button--large { padding: 15px; }

Example button migration:
  <button class="btn btn-primary btn-lg">
  
  to:
  
  <button class="button button--primary button--large">


MIGRATING FROM SMACSS
───────────────────────

SMACSS (by purpose):
  l-container (layout)
  m-card (module/component)
  is-active (state)

BEM (by structure):
  .card (block)
  .card__content (element)
  .card--active (modifier)

Mapping:
  SMACSS modules → BEM blocks
  SMACSS states → BEM modifiers
  SMACSS layout → Separate layout blocks

Usually straightforward migration.


GRADUAL MIGRATION
────────────────────

Don't convert everything at once:

Phase 1 (Week 1):
  Establish BEM guidelines
  Create style guide documentation

Phase 2 (Week 2-3):
  Migrate critical components (Button, Input, Form)
  Update their JavaScript

Phase 3 (Week 4-5):
  Migrate secondary components
  Run tests

Phase 4 (Week 6):
  Migrate remaining components
  Remove old CSS

Phase 5 (Week 7):
  Cleanup and optimization
  Team training


TESTING DURING MIGRATION
──────────────────────────

Key tests:

1. Visual regression testing
   Old classes → New classes should look same

2. Selector testing
   JavaScript should still find elements

3. Browser compatibility
   Ensure no new issues

Tools:
  - Percy for visual regression
  - Jest for JavaScript tests
  - Lighthouse for performance


DOCUMENTATION DURING MIGRATION
────────────────────────────────

Keep records:
  - Original CSS class name
  - New BEM class name
  - Migration date
  - Status (done/in-progress)

Example migration tracker:
  Component | Old Class | New Class | Status
  Button | .btn | .button | ✓ Done
  Input | .input-field | .input__field | ✓ Done
  Form | .form-group | .form__group | In Progress
  Card | .card | .card | Not Started


ROLLBACK PLAN
─────────────

Have plan to rollback if needed:
  1. Keep old CSS files temporarily
  2. Be able to revert HTML changes
  3. Have rollback tested
  4. Communicate plan to team

Once confident, delete old CSS files.
*/


// ============================================================================
// 17. TOOLS & AUTOMATION
// ============================================================================

/*
LINTERS FOR BEM
────────────────

Tools that check BEM compliance:

Stylelint (CSS linter):
  Install: npm install stylelint

Config (.stylelintrc.json):
  {
    "rules": {
      "selector-no-qualifying-type": true,
      "selector-max-id": 0,
      "selector-max-type": 1,
      "selector-max-universal": 0,
      "selector-max-attribute": 0,
      "selector-max-pseudo-class": 2,
      "selector-max-specificity": "0,1,0",
      "declaration-no-important": true
    }
  }

This enforces:
  - No ID selectors
  - Only class selectors (mostly)
  - No nesting
  - No !important


CLASS NAME VALIDATORS
───────────────────────

Check naming conventions:

stylelint-bem-naming
  Plugin that validates BEM naming

Config:
  "stylelint-bem-naming/bem-notation": {
    "elementSeparator": "__",
    "modifierSeparator": "--"
  }

This ensures:
  - Blocks use single word: .button (not .button-group)
  - Elements use __: .button__icon
  - Modifiers use --: .button--primary


IDE SUPPORT
────────────

VS Code extensions:

1. BEM Helper
   Extension provides snippets and validation

2. CSS Peek
   Jump from class to CSS file

3. Stylelint
   Real-time linting in editor


DOCUMENTATION GENERATORS
──────────────────────────

Generate component docs automatically:

KSS (Knapsack Style Sheets):
  Extracts CSS comments and generates docs

Example CSS:
  /**
   * Button component
   *
   * .button           - Base button
   * .button--primary  - Primary variant
   * .button--large    - Large size
   */
  .button { }

Generates HTML documentation automatically.


VISUAL TESTING
────────────────

Tools for visual regression:

Percy (visual testing):
  Captures screenshots after CSS changes
  Compares with baseline
  Flags visual regressions

Usage:
  1. Create baseline
  2. Make CSS changes
  3. Percy compares
  4. Review changes
  5. Approve or reject


COMPONENT REGISTRIES
──────────────────────

Store all components in one place:

Storybook (most popular):
  Framework-agnostic component showcase

Example story (Button.stories.jsx):
  export default {
    title: 'Components/Button',
    component: Button,
  };

  export const Primary = () => (
    <Button variant="primary">Click me</Button>
  );

  export const Secondary = () => (
    <Button variant="secondary">Click me</Button>
  );

  export const Disabled = () => (
    <Button disabled>Disabled</Button>
  );

Visit: http://localhost:6006
Browse all components
See live changes


NAMING CONVENTIONS TOOLS
───────────────────────────

ESLint rules for JS:

When using className in React/Vue:

  {
    "rules": {
      "no-class-name-conflicts": "warn"
    }
  }

Custom rule to warn about:
  className="button-icon"  ← Wrong separator
  className="button--icon" ← Missing underscore


BUILD TOOL OPTIMIZATION
─────────────────────────

Webpack/Vite configuration:

1. CSS extraction
  Extract CSS to separate file

2. Minification
  csso-loader minifies CSS

3. Autoprefixer
  Add vendor prefixes

4. PurgeCSS
  Remove unused CSS

Example webpack config:
  {
    test: /\.css$/,
    use: [
      'style-loader',
      'css-loader',
      'autoprefixer-loader',
      'csso-loader'
    ]
  }


TAILWIND + BEM COMBINATION
────────────────────────────

Some teams use both:

Component CSS (BEM):
  .button { }
  .button--primary { }

Spacing/Layout (Tailwind):
  <button class="button button--primary px-4 py-2">

Config (tailwind.config.js):
  module.exports = {
    corePlugins: [
      'padding', // Only spacing utilities
      'margin',
      'gap'
    ]
  }

This gives:
  ✓ Readable component classes (BEM)
  ✓ Flexible spacing (Tailwind utilities)
*/


// ============================================================================
// 18. FAQ & TROUBLESHOOTING
// ============================================================================

/*
Q1: When to use BEM vs CSS Modules vs Tailwind?
────────────────────────────────────────────────

A: All have merits:

Use BEM when:
  - Traditional CSS workflow
  - Team prefers semantic class names
  - Need predictable, maintainable CSS
  - Don't want build complexity

Use CSS Modules when:
  - Using React/Vue/Svelte
  - Want automatic scoping
  - Need isolation between components

Use Tailwind when:
  - Rapid prototyping needed
  - Design tokens are clear
  - Team comfortable with HTML classes

Best: Hybrid
  BEM for component structure
  CSS Modules for scoping
  Some utilities for spacing/layout


Q2: How deep can nesting go?
──────────────────────────────

A: Only one level deep in BEM naming.

✓ Correct:
  .block
  .block__element
  .block__element--modifier

✗ Wrong:
  .block__element__subelement
  .block__element__subelement--modifier

If you need deeper structure, reconsider:
  Are some parts independent components?
  Can they be separate blocks?


Q3: Block or Element? How to decide?
──────────────────────────────────────

A: Ask: "Can this exist independently?"

Block candidates:
  - Button (appears everywhere)
  - Card (standalone component)
  - Form (can be used alone)
  - Modal (independent dialog)

Element candidates:
  - Button icon (only makes sense in button)
  - Form label (only makes sense in form)
  - Modal close (only makes sense in modal)

If in doubt: Make it an element of the parent.
You can always extract to block later.


Q4: Can blocks modify elements of other blocks?
─────────────────────────────────────────────

A: Generally no. Each block is independent.

✗ Avoid:
  .form .button__icon {
    /* Form shouldn't style Button's elements */
  }

✓ Instead:
  If button needs adjustments in form, use modifier:
  <button class="button button--in-form">

Or use CSS variables:
  <form style="--button-icon-size: 16px">
    <button class="button">
      <svg class="button__icon">
    </button>
  </form>

This keeps components independent.


Q5: How many modifiers can one element have?
──────────────────────────────────────────────

A: As many as needed.

  <button class="button button--primary button--large button--loading">

Is perfectly valid BEM.

But if combinations are common, might be worth:
  - Using CSS variables
  - Creating a preset modifier
  - Reconsidering your variant strategy


Q6: What about responsive modifications?
──────────────────────────────────────────

A: Use media queries or separate modifiers.

Option 1: Media query
  .button { padding: 12px; }
  @media (max-width: 768px) {
    .button { padding: 8px; }
  }

Option 2: Modifier for each breakpoint
  .button--mobile { padding: 8px; }
  .button--desktop { padding: 12px; }
  
  HTML with JavaScript:
  <button class="button button--mobile">

Option 3: CSS variables (best)
  .button { padding: var(--button-padding, 12px); }
  @media (max-width: 768px) {
    :root { --button-padding: 8px; }
  }


Q7: How to handle complex nested components?
──────────────────────────────────────────────

A: Flatten into multiple blocks.

Wrong approach:
  .panel__header__nav
  .panel__header__nav__item
  .panel__header__nav__link

Right approach:
  .panel (main component)
  .panel__header
  .panel__content
  .panel__footer

  .navigation (separate block)
  .navigation__item
  .navigation__link

  HTML:
  <div class="panel">
    <header class="panel__header">
      <nav class="navigation">
        <a class="navigation__link">Home</a>
      </nav>
    </header>
  </div>


Q8: What about global styles?
──────────────────────────────

A: Keep them minimal.

Use base styles for:
  * Reset/Normalize
  * Typography defaults
  * Root layout
  * Theme variables

✓ Good:
  body { font-family: ...; }
  h1 { font-size: 32px; }
  :root { --color-primary: #007bff; }

✗ Avoid:
  .container { ... }
  .row { ... }
  .col { ... }

Global styles keep component CSS cleaner.


Q9: How to handle conditional styling?
────────────────────────────────────────

A: Use JavaScript to toggle modifiers.

JavaScript:
  if (isDisabled) {
    button.classList.add('button--disabled');
  } else {
    button.classList.remove('button--disabled');
  }

Or if using framework:
  <button class={`button ${isDisabled ? 'button--disabled' : ''}`}>

Or with classnames library:
  <button className={classNames('button', {
    'button--disabled': isDisabled
  })}>


Q10: BEM seems verbose, why not abbreviate?
──────────────────────────────────────────

A: Verbosity has advantages:

.button__icon  ← Clear what it is
.btn__ico      ← Abbreviated, unclear

Benefits of verbose:
  ✓ Self-documenting code
  ✓ Searchable (fewer false positives)
  ✓ No abbreviation confusion
  ✓ Easier for new team members

You can abbreviate your abbreviations later if needed,
but clarity-first approach prevents problems.


Q11: Does BEM work with Pre-processors?
─────────────────────────────────────────

A: Yes, with caveats.

Good with SCSS/LESS:
  .button {
    padding: 10px;
    
    &__icon { }      ✓ Good - uses nesting correctly
    &--primary { }   ✓ Good - generates .button--primary
  }

Avoid in SCSS:
  .button {
    padding: 10px;
    
    .icon { }        ✗ Bad - nests, generates .button .icon
  }

Rule: Nested output should be flat BEM.
Use & for element/modifier chaining only.


Q12: How does BEM scale to enterprise?
──────────────────────────────────────

A: Very well, with guidelines.

Key for scale:
  1. Standardized naming
     All variants use --primary, --secondary
     All sizes use --small, --medium, --large

  2. Component registry
     Storybook or similar
     Single source of truth

  3. Documentation
     Every component documented
     API, CSS classes, usage examples

  4. Tooling
     Linting rules enforced
     CI/CD checks for naming

  5. Design system
     Color palette defined
     Spacing, typography rules
     Modifier guidelines

Enterprise example: IBM Carbon Design System
  Uses BEM
  500+ companies use it
  Highly standardized and documented


Q13: Any gotchas with BEM and CSS specificity?
─────────────────────────────────────────────

A: BEM makes specificity predictable.

Golden rule: All BEM classes have same specificity
  .button       = 0,0,1,0
  .button--primary = 0,0,1,0
  .button__icon = 0,0,1,0

Advantages:
  ✓ No specificity wars
  ✓ Later rules override earlier
  ✓ Easy to override when needed
  ✓ Predictable cascade


Q14: How to handle animations with BEM?
──────────────────────────────────────────

A: Use modifiers for animation states.

CSS:
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .button {
    transition: opacity 0.3s ease;
  }

  .button--entering {
    animation: fadeIn 0.3s ease;
  }

JavaScript:
  button.classList.add('button--entering');
  setTimeout(() => {
    button.classList.remove('button--entering');
  }, 300);

Or use :hover, :active directly in CSS
for simple state changes.


Q15: Security considerations with BEM?
──────────────────────────────────────

A: BEM is CSS-only, no security implications.

But remember:
  - Don't expose sensitive info in class names
  - ✗ class="button button--user-id-12345"
  - ✓ Use data attributes instead: data-user-id

CSS classes are visible in HTML source, so:
  Anything in class name is public
  Use data-* for sensitive information
*/

// ============================================================================
// END OF BEM GUIDE
// ============================================================================

/*
SUMMARY
════════

BEM (Block Element Modifier) is a naming methodology for CSS
that makes code more predictable, scalable, and maintainable.

KEY POINTS:
───────────

1. NAMING:
   .block           ← Independent component
   .block__element  ← Part of block
   .block--modifier ← Variant or state

2. PRINCIPLES:
   • Flat CSS structure (no nesting)
   • Same specificity everywhere
   • Independent components
   • Single responsibility

3. HTML:
   <button class="button button--primary">
     <svg class="button__icon"></svg>
     <span class="button__text">Click me</span>
   </button>

4. CSS:
   .button { }
   .button__icon { }
   .button--primary { }
   .button:hover { }

5. JAVASCRIPT:
   button.classList.add('button--loading');
   button.classList.remove('button--loading');

BENEFITS:
──────────
✓ Predictable code structure
✓ Easy to maintain at scale
✓ Reduces naming conflicts
✓ Modular and reusable
✓ Works with all tools (SCSS, CSS Modules, Tailwind)
✓ Good for team collaboration
✓ Future-proof


WHEN TO USE BEM:
─────────────────
✓ Traditional CSS workflows
✓ Large projects with many developers
✓ Component-based architecture
✓ Long-term maintainability important
✓ Team values predictability


NOT NEEDED FOR:
────────────────
✗ Tiny one-off projects
✗ Static sites with few components
✗ Teams already using CSS-in-JS or Tailwind effectively
✗ When rapid prototyping is priority


NEXT STEPS:
─────────────
1. Read INTRODUCTION & PHILOSOPHY
2. Learn CORE CONCEPTS thoroughly
3. Study REAL-WORLD EXAMPLES
4. Try naming your first component
5. Practice writing CSS and HTML
6. Integrate into your workflow


RESOURCES:
───────────
Official BEM Site: bem.info
BEM Methodology: getbem.com
CSS Tricks Guide: css-tricks.com/bem-101/
Real-world examples: github.com (search "bem")


FINAL THOUGHTS:
────────────────
BEM is not a rule set you must follow religiously.
It's a set of best practices you can adapt to your needs.

Take what works for your team.
Drop what doesn't.
The goal is: scalable, maintainable CSS.

BEM provides a proven path to that goal.

*/

