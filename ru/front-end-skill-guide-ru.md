# FRONT-END SKILL GUIDE
## Bootstrap 5.3 · UI/UX Patterns · Universal Design System
### Version 1.0 | Production-Grade Methodology

---

## НАЗНАЧЕНИЕ СКИЛЛА

Используй этот скилл при создании любого веб-интерфейса на Bootstrap 5.3:
лендингов, дашбордов, SaaS-интерфейсов, корпоративных сайтов, порталов,
компонентных библиотек, форм, витрин продуктов.

**Обязательно читай этот файл ПЕРЕД написанием любого кода.**

---

## ЧАСТЬ I — ФИЛОСОФИЯ ДИЗАЙНА

### 1.1 Принцип «Намеренного Дизайна»

Каждое решение должно быть обосновано контекстом. Задай себе 4 вопроса до начала:

```
1. КОНТЕКСТ:  Кто использует интерфейс? В какой ситуации?
2. ЭМОЦИЯ:    Что должен чувствовать пользователь? (доверие / азарт / спокойствие)
3. ДЕЙСТВИЕ:  Какое главное действие нужно совершить?
4. ПАМЯТЬ:    Что запомнится? Какой один элемент будет отличительным?
```

### 1.2 Эстетические Направления (выбери одно, не смешивай)

| Направление        | Характеристики                                    | Bootstrap-реализация              |
|--------------------|---------------------------------------------------|-----------------------------------|
| **Refined Minimal** | Воздух, точность, монохром + один акцент          | `gap-*`, `py-6+`, тонкие borders |
| **Editorial**       | Крупная типографика, сетка-ломка, асимметрия      | `display-1..6`, offset columns    |
| **Corporate Trust** | Синие тона, чёткая иерархия, без сюрпризов        | `primary`, строгая сетка          |
| **Tech/Dark**       | Тёмный фон, свечение, mono-шрифты, глитч-детали   | `data-bs-theme="dark"` + CSS vars |
| **Organic/Warm**    | Земляные тона, скруглённые формы, serif-типографика | кастомные `--bs-*` переменные   |
| **Brutalist**       | Сырые borders, жирный шрифт, нарочитые нарушения  | отключение теней, raw HTML        |
| **Luxury**          | Золото/кремовый, засечные шрифты, щедрый padding  | расширенные spacing-токены        |
| **Playful/Product** | Яркие градиенты, rounded-full, иллюстрации        | `rounded-pill`, custom gradients  |

---

## ЧАСТЬ II — СИСТЕМА ТОКЕНОВ (Bootstrap CSS Variables)

### 2.1 Архитектура Переменных

Всегда переопределяй Bootstrap через CSS Custom Properties — **никогда** не хардкоди цвета в компонентах.

```css
:root {
  /* ── BRAND PALETTE ─────────────────────────── */
  --brand-50:  #f0f9ff;
  --brand-100: #e0f2fe;
  --brand-500: #0ea5e9;
  --brand-600: #0284c7;
  --brand-900: #0c4a6e;

  --accent-400: #f59e0b;
  --accent-500: #d97706;

  --neutral-0:   #ffffff;
  --neutral-50:  #f8fafc;
  --neutral-100: #f1f5f9;
  --neutral-200: #e2e8f0;
  --neutral-400: #94a3b8;
  --neutral-600: #475569;
  --neutral-800: #1e293b;
  --neutral-900: #0f172a;
  --neutral-950: #020617;

  /* ── BOOTSTRAP REMAPPING ────────────────────── */
  --bs-primary:        var(--brand-500);
  --bs-primary-rgb:    14, 165, 233;
  --bs-body-bg:        var(--neutral-50);
  --bs-body-color:     var(--neutral-800);
  --bs-border-color:   var(--neutral-200);
  --bs-border-radius:  0.5rem;
  --bs-border-radius-lg: 0.875rem;
  --bs-border-radius-xl: 1.25rem;
  --bs-box-shadow:     0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --bs-box-shadow-lg:  0 10px 40px rgba(0,0,0,.10);

  /* ── TYPOGRAPHY SCALE ───────────────────────── */
  --font-display: 'YourDisplayFont', serif;
  --font-body:    'YourBodyFont', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  /* ── SPACING EXTENSIONS ─────────────────────── */
  --space-18: 4.5rem;
  --space-24: 6rem;
  --space-32: 8rem;

  /* ── ANIMATION ──────────────────────────────── */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-back:  cubic-bezier(0.36, 0, 0.66, -0.56);
  --duration-fast: 150ms;
  --duration-base: 250ms;
  --duration-slow: 400ms;
}

/* Dark theme override */
[data-bs-theme="dark"] {
  --bs-body-bg:      var(--neutral-950);
  --bs-body-color:   var(--neutral-100);
  --bs-border-color: var(--neutral-800);
  --bs-box-shadow:   0 1px 3px rgba(0,0,0,.4);
}
```

### 2.2 Типографическая Система

```css
/* Подключение шрифтов — примеры сочетаний */

/* Вариант A: Editorial */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap');

/* Вариант B: Tech/Modern */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap');

/* Вариант C: Luxury */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300&family=Jost:wght@300;400;500&display=swap');

/* Вариант D: Brutalist/Bold */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Barlow+Condensed:wght@600;800&display=swap');

/* ЗАПРЕЩЕНЫ: Inter, Roboto, Arial, system-ui как основные */

/* Типографическая шкала поверх Bootstrap */
.display-hero {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw, 7rem);
  line-height: 1.0;
  letter-spacing: -0.03em;
  font-weight: 900;
}

h1, .h1 { font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.1; }
h2, .h2 { font-size: clamp(1.5rem, 3vw, 2.5rem); line-height: 1.2; }
h3, .h3 { font-size: clamp(1.25rem, 2vw, 1.75rem); line-height: 1.3; }

.text-label {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.text-balance { text-wrap: balance; }
```

---

## ЧАСТЬ III — СЕТОЧНАЯ СИСТЕМА И ЛЭЙАУТ

### 3.1 Bootstrap Grid — Продвинутые Паттерны

```html
<!-- ПАТТЕРН: Hero с асимметрией 7/5 -->
<section class="container py-section">
  <div class="row align-items-center g-5">
    <div class="col-lg-7 order-lg-1">
      <!-- Контент -->
    </div>
    <div class="col-lg-5 order-lg-2">
      <!-- Визуал / иллюстрация -->
    </div>
  </div>
</section>

<!-- ПАТТЕРН: Masonry-like Card Grid -->
<div class="row g-4">
  <div class="col-12 col-md-8"><!-- Featured card --></div>
  <div class="col-12 col-md-4"><!-- Secondary --></div>
  <div class="col-12 col-md-4"><!-- Card --></div>
  <div class="col-12 col-md-4"><!-- Card --></div>
  <div class="col-12 col-md-4"><!-- Card --></div>
</div>

<!-- ПАТТЕРН: Bento Box Grid (CSS Grid поверх Bootstrap) -->
<div class="bento-grid">
  <div class="bento-item bento-span-2"><!-- Wide --></div>
  <div class="bento-item"><!-- Normal --></div>
  <div class="bento-item bento-tall"><!-- Tall --></div>
  <div class="bento-item"><!-- Normal --></div>
  <div class="bento-item bento-span-2"><!-- Wide --></div>
</div>
```

```css
/* Bento Grid System */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 280px;
  gap: 1rem;
}
.bento-span-2 { grid-column: span 2; }
.bento-tall   { grid-row: span 2; }

@media (max-width: 768px) {
  .bento-grid { grid-template-columns: 1fr; grid-auto-rows: auto; }
  .bento-span-2, .bento-tall { grid-column: auto; grid-row: auto; }
}

/* Section Spacing Utility */
.py-section { padding-block: clamp(4rem, 10vw, 8rem); }
.py-section-sm { padding-block: clamp(2rem, 5vw, 4rem); }
```

### 3.2 Breakpoint-Стратегия

```
Mobile-first ВСЕГДА. Порядок медиа-запросов: xs → sm → md → lg → xl → xxl

Ключевые точки Bootstrap 5.3:
  xs:  0px     → одна колонка, вертикальный стек
  sm:  576px   → начало адаптации, 2 колонки в сетке
  md:  768px   → переход от мобильного к десктоп-паттернам
  lg:  992px   → основной десктопный лэйаут
  xl:  1200px  → расширенный контент, боковые панели
  xxl: 1400px  → максимальная ширина, editorial layouts

Правила:
- Контейнер: всегда container (не container-fluid для контента)
- Max-width контента: 1200-1320px (не шире)
- Читаемые колонки: col-md-8, col-lg-6 для длинного текста
- Никогда не ставь фиксированные px-размеры в HTML-классах
```

---

## ЧАСТЬ IV — UI/UX ПАТТЕРНЫ

### 4.1 Навигация

```html
<!-- ПАТТЕРН: Sticky Navbar с backdrop-blur -->
<nav class="navbar navbar-expand-lg navbar-glass sticky-top">
  <div class="container">
    <a class="navbar-brand fw-bold" href="#">Brand</a>
    <button class="navbar-toggler border-0" type="button"
            data-bs-toggle="collapse" data-bs-target="#nav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="nav">
      <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-1">
        <li class="nav-item"><a class="nav-link" href="#">Features</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Pricing</a></li>
        <li class="nav-item ms-lg-3">
          <a class="btn btn-primary btn-sm px-4" href="#">Get Started</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

```css
.navbar-glass {
  background: rgba(var(--bs-body-bg-rgb), 0.85);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border-bottom: 1px solid var(--bs-border-color);
  transition: background var(--duration-base) ease,
              box-shadow var(--duration-base) ease;
}
.navbar-glass.scrolled {
  background: rgba(var(--bs-body-bg-rgb), 0.97);
  box-shadow: var(--bs-box-shadow);
}
```

```javascript
// Navbar scroll behavior
const navbar = document.querySelector('.navbar-glass');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 20);
}, { passive: true });
```

### 4.2 Hero Секция

```html
<!-- ПАТТЕРН: Hero с градиентным фоном и текстовым акцентом -->
<section class="hero-section position-relative overflow-hidden">
  <div class="hero-bg-effect" aria-hidden="true"></div>
  <div class="container position-relative">
    <div class="row justify-content-center text-center py-section">
      <div class="col-lg-8 col-xl-7">
        <div class="badge-label mb-4">
          <span class="text-label">New Release · v2.0</span>
        </div>
        <h1 class="display-hero text-balance mb-4">
          Build interfaces that <em class="text-gradient">people love</em>
        </h1>
        <p class="lead text-secondary mb-5 mx-auto" style="max-width:520px">
          Subtitle no longer than 2 строки. Конкретный benefit, без buzzwords.
        </p>
        <div class="d-flex flex-wrap gap-3 justify-content-center">
          <a href="#" class="btn btn-primary btn-lg px-5">Primary CTA</a>
          <a href="#" class="btn btn-ghost btn-lg">
            Secondary CTA <i class="bi bi-arrow-right ms-1"></i>
          </a>
        </div>
        <!-- Social proof -->
        <div class="mt-5 d-flex align-items-center justify-content-center gap-3">
          <div class="avatar-stack"><!-- аватары --></div>
          <span class="text-secondary small">
            Trusted by <strong>10,000+</strong> developers
          </span>
        </div>
      </div>
    </div>
  </div>
</section>
```

```css
.hero-section {
  background: var(--neutral-950);
  color: white;
  min-height: 90vh;
  display: flex;
  align-items: center;
}

.hero-bg-effect {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% -10%, var(--brand-600) 0%, transparent 70%),
    radial-gradient(ellipse 40% 40% at 80% 60%, var(--accent-500) 0%, transparent 60%);
  opacity: 0.4;
  pointer-events: none;
}

.text-gradient {
  background: linear-gradient(135deg, var(--brand-400), var(--accent-400));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.badge-label {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 1rem;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 100px;
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(8px);
}
```

### 4.3 Feature Cards (Bento Pattern)

```html
<!-- ПАТТЕРН: Feature Bento Grid -->
<section class="py-section bg-body-tertiary">
  <div class="container">
    <div class="text-center mb-5">
      <span class="text-label text-primary d-block mb-2">Features</span>
      <h2 class="h1 text-balance">Everything you need</h2>
    </div>
    <div class="bento-grid">
      <!-- Featured: large card -->
      <div class="bento-item bento-span-2 card-feature card-feature--primary">
        <div class="card-feature__icon">⚡</div>
        <h3>Lightning Fast</h3>
        <p>Description up to 2 строк. Конкретная деталь.</p>
        <div class="card-feature__visual"><!-- иллюстрация/скриншот --></div>
      </div>
      <!-- Normal cards -->
      <div class="bento-item card-feature">
        <div class="card-feature__icon">🔒</div>
        <h3>Secure</h3>
        <p>One line value proposition.</p>
      </div>
      <!-- ... -->
    </div>
  </div>
</section>
```

```css
.card-feature {
  background: var(--bs-body-bg);
  border: 1px solid var(--bs-border-color);
  border-radius: var(--bs-border-radius-xl);
  padding: 2rem;
  transition: transform var(--duration-base) var(--ease-out-expo),
              box-shadow var(--duration-base) ease,
              border-color var(--duration-base) ease;
  overflow: hidden;
}
.card-feature:hover {
  transform: translateY(-4px);
  box-shadow: var(--bs-box-shadow-lg);
  border-color: var(--bs-primary);
}
.card-feature--primary {
  background: linear-gradient(135deg, var(--brand-900), var(--brand-800));
  border-color: var(--brand-700);
  color: white;
}
.card-feature__icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}
```

### 4.4 Pricing

```html
<!-- ПАТТЕРН: Pricing с переключателем month/year -->
<section class="py-section">
  <div class="container">
    <!-- Toggle -->
    <div class="d-flex align-items-center justify-content-center gap-3 mb-5">
      <span>Monthly</span>
      <div class="form-check form-switch mb-0">
        <input class="form-check-input" type="checkbox" id="billingToggle" role="switch">
      </div>
      <span>Annual <span class="badge bg-success-subtle text-success ms-1">Save 20%</span></span>
    </div>
    <!-- Cards -->
    <div class="row justify-content-center g-4">
      <div class="col-md-6 col-lg-4">
        <div class="pricing-card">
          <div class="pricing-card__tier text-label mb-3">Starter</div>
          <div class="pricing-card__price">
            <span class="pricing-amount">$0</span>
            <span class="text-secondary">/mo</span>
          </div>
          <ul class="pricing-features mt-4 mb-4">
            <li><i class="bi bi-check2 text-success me-2"></i>Feature one</li>
            <li><i class="bi bi-check2 text-success me-2"></i>Feature two</li>
            <li class="text-muted"><i class="bi bi-x me-2"></i>Pro feature</li>
          </ul>
          <a href="#" class="btn btn-outline-primary w-100">Get started free</a>
        </div>
      </div>
      <div class="col-md-6 col-lg-4">
        <div class="pricing-card pricing-card--featured">
          <div class="pricing-card__badge">Most Popular</div>
          <!-- ... -->
        </div>
      </div>
    </div>
  </div>
</section>
```

```css
.pricing-card {
  background: var(--bs-body-bg);
  border: 1px solid var(--bs-border-color);
  border-radius: var(--bs-border-radius-xl);
  padding: 2.5rem 2rem;
  position: relative;
  height: 100%;
  transition: transform var(--duration-base) var(--ease-out-expo);
}
.pricing-card--featured {
  background: var(--neutral-900);
  border-color: var(--brand-500);
  color: white;
  transform: scale(1.03);
  box-shadow: 0 0 0 4px rgba(var(--bs-primary-rgb), 0.15),
              var(--bs-box-shadow-lg);
}
.pricing-card__badge {
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--brand-500);
  color: white;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.25rem 1rem;
  border-radius: 0 0 0.75rem 0.75rem;
}
.pricing-amount { font-size: 3rem; font-weight: 800; line-height: 1; }
.pricing-features { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.75rem; }
```

### 4.5 Формы

```html
<!-- ПАТТЕРН: Floating Label Form (Bootstrap 5.3 native) -->
<div class="card shadow-sm border-0" style="max-width: 480px; margin: auto;">
  <div class="card-body p-4 p-md-5">
    <h2 class="mb-1">Create account</h2>
    <p class="text-secondary mb-4">Join 10,000+ developers</p>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" id="name" placeholder="Name">
      <label for="name">Full name</label>
    </div>
    <div class="form-floating mb-3">
      <input type="email" class="form-control" id="email" placeholder="Email">
      <label for="email">Email address</label>
    </div>
    <div class="form-floating mb-4 position-relative">
      <input type="password" class="form-control" id="pwd" placeholder="Password">
      <label for="pwd">Password</label>
      <button class="btn-password-toggle" type="button" aria-label="Show password">
        <i class="bi bi-eye"></i>
      </button>
    </div>

    <button type="submit" class="btn btn-primary w-100 btn-lg mb-3">
      Create account
    </button>
    <p class="text-center text-secondary small">
      Already have an account? <a href="#" class="text-primary">Sign in</a>
    </p>
  </div>
</div>
```

```css
/* Улучшенные формы */
.form-control, .form-select {
  border-color: var(--bs-border-color);
  transition: border-color var(--duration-fast) ease,
              box-shadow var(--duration-fast) ease;
}
.form-control:focus, .form-select:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 3px rgba(var(--bs-primary-rgb), 0.15);
}
.form-floating > .form-control:focus ~ label,
.form-floating > .form-control:not(:placeholder-shown) ~ label {
  color: var(--bs-primary);
}
.btn-password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--neutral-400);
  cursor: pointer;
  padding: 0.25rem;
  z-index: 5;
}
```

### 4.6 Данные и Таблицы (Dashboard Pattern)

```html
<!-- ПАТТЕРН: Stats Row -->
<div class="row g-3 mb-4">
  <div class="col-6 col-xl-3">
    <div class="stat-card">
      <div class="stat-card__label">Total Revenue</div>
      <div class="stat-card__value">$48,295</div>
      <div class="stat-card__delta positive">
        <i class="bi bi-arrow-up-right"></i> +12.5%
      </div>
    </div>
  </div>
  <!-- × 3 -->
</div>

<!-- ПАТТЕРН: Responsive Table -->
<div class="card border-0 shadow-sm">
  <div class="card-header d-flex align-items-center justify-content-between border-0 pt-4 pb-0">
    <h5 class="mb-0">Recent Orders</h5>
    <div class="d-flex gap-2">
      <input class="form-control form-control-sm" placeholder="Search...">
      <button class="btn btn-sm btn-outline-secondary">Export</button>
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead class="table-light">
        <tr>
          <th class="ps-4">Order</th>
          <th>Customer</th>
          <th>Status</th>
          <th class="text-end pe-4">Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="ps-4"><code>#ORD-001</code></td>
          <td>
            <div class="d-flex align-items-center gap-2">
              <div class="avatar-sm bg-primary rounded-circle"></div>
              <div>
                <div class="fw-medium">John Doe</div>
                <div class="text-secondary small">john@example.com</div>
              </div>
            </div>
          </td>
          <td><span class="badge bg-success-subtle text-success">Completed</span></td>
          <td class="text-end pe-4 fw-semibold">$299.00</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

```css
.stat-card {
  background: var(--bs-body-bg);
  border: 1px solid var(--bs-border-color);
  border-radius: var(--bs-border-radius-lg);
  padding: 1.5rem;
}
.stat-card__label { font-size: 0.8125rem; color: var(--neutral-400); font-weight: 500; margin-bottom: 0.5rem; }
.stat-card__value { font-size: 2rem; font-weight: 800; line-height: 1.1; }
.stat-card__delta { font-size: 0.8125rem; font-weight: 600; margin-top: 0.5rem; }
.stat-card__delta.positive { color: #16a34a; }
.stat-card__delta.negative { color: #dc2626; }
```

### 4.7 Toast / Alert / Notification

```css
/* Custom Toasts */
.toast-custom {
  --toast-accent: var(--bs-primary);
  background: var(--bs-body-bg);
  border: 1px solid var(--bs-border-color);
  border-left: 4px solid var(--toast-accent);
  border-radius: var(--bs-border-radius-lg);
  box-shadow: var(--bs-box-shadow-lg);
}
.toast-custom.toast--success { --toast-accent: #16a34a; }
.toast-custom.toast--error   { --toast-accent: #dc2626; }
.toast-custom.toast--warning { --toast-accent: #d97706; }
```

---

## ЧАСТЬ V — АНИМАЦИЯ И МИКРОИНТЕРАКЦИИ

### 5.1 Page Load Animation

```css
/* Staggered reveal — применяй к секциям */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

[data-animate] {
  opacity: 0;
  animation: fadeUp var(--duration-slow) var(--ease-out-expo) forwards;
}
[data-animate="1"] { animation-delay: 0ms; }
[data-animate="2"] { animation-delay: 100ms; }
[data-animate="3"] { animation-delay: 200ms; }
[data-animate="4"] { animation-delay: 300ms; }
[data-animate="5"] { animation-delay: 400ms; }
```

```javascript
// Intersection Observer для lazy анимаций
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('[data-animate]').forEach(el => {
  el.style.animationPlayState = 'paused';
  observer.observe(el);
});
```

### 5.2 Button Micro-interactions

```css
/* Primary Button */
.btn-primary {
  position: relative;
  overflow: hidden;
  transition: transform var(--duration-fast) var(--ease-out-expo),
              box-shadow var(--duration-fast) ease;
}
.btn-primary::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.1);
  transform: translateX(-100%);
  transition: transform 300ms var(--ease-out-expo);
}
.btn-primary:hover::after { transform: translateX(0); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(var(--bs-primary-rgb), 0.4); }
.btn-primary:active { transform: translateY(0); }

/* Ghost Button */
.btn-ghost {
  background: transparent;
  border: 1px solid var(--bs-border-color);
  color: var(--bs-body-color);
  transition: all var(--duration-fast) ease;
}
.btn-ghost:hover {
  background: var(--neutral-100);
  border-color: var(--neutral-300);
}
```

### 5.3 Card Hover Effect

```css
.card-hover {
  transition: transform var(--duration-base) var(--ease-out-expo),
              box-shadow var(--duration-base) ease;
  will-change: transform;
}
.card-hover:hover {
  transform: translateY(-6px) scale(1.01);
  box-shadow: var(--bs-box-shadow-lg);
}

/* Glow on hover для dark-темы */
[data-bs-theme="dark"] .card-hover:hover {
  box-shadow:
    0 0 0 1px rgba(var(--bs-primary-rgb), 0.3),
    0 20px 60px rgba(0,0,0,.5),
    0 0 80px rgba(var(--bs-primary-rgb), 0.07);
}
```

### 5.4 Loading States

```css
/* Skeleton Loader */
.skeleton {
  background: linear-gradient(90deg,
    var(--neutral-200) 0%,
    var(--neutral-100) 50%,
    var(--neutral-200) 100%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--bs-border-radius);
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

/* Button Loading State */
.btn.is-loading {
  pointer-events: none;
  position: relative;
  color: transparent !important;
}
.btn.is-loading::after {
  content: '';
  position: absolute;
  width: 1rem; height: 1rem;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
@keyframes spin { to { transform: translate(-50%, -50%) rotate(360deg); } }
```

---

## ЧАСТЬ VI — ПАТТЕРНЫ КОМПОНЕНТОВ

### 6.1 Avatar Stack

```html
<div class="avatar-stack">
  <img src="..." class="avatar-stack__item" alt="User 1">
  <img src="..." class="avatar-stack__item" alt="User 2">
  <img src="..." class="avatar-stack__item" alt="User 3">
  <div class="avatar-stack__item avatar-stack__more">+5</div>
</div>
```

```css
.avatar-stack { display: flex; }
.avatar-stack__item {
  width: 2rem; height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--bs-body-bg);
  margin-left: -0.5rem;
  object-fit: cover;
}
.avatar-stack__item:first-child { margin-left: 0; }
.avatar-stack__more {
  background: var(--neutral-200);
  color: var(--neutral-600);
  font-size: 0.6875rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### 6.2 Tag / Badge System

```css
.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.2rem 0.65rem;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid currentColor;
}
.tag-primary { color: var(--brand-600); background: var(--brand-50); border-color: var(--brand-200); }
.tag-success { color: #15803d; background: #f0fdf4; border-color: #bbf7d0; }
.tag-warning { color: #92400e; background: #fffbeb; border-color: #fde68a; }
.tag-danger  { color: #991b1b; background: #fef2f2; border-color: #fecaca; }
.tag-neutral { color: var(--neutral-600); background: var(--neutral-100); border-color: var(--neutral-200); }
```

### 6.3 Sidebar (Dashboard Layout)

```html
<div class="dashboard-layout">
  <aside class="sidebar">
    <div class="sidebar__logo">Brand</div>
    <nav class="sidebar__nav">
      <div class="sidebar__section-title">Main</div>
      <a href="#" class="sidebar__item active">
        <i class="bi bi-grid-fill"></i> Dashboard
      </a>
      <a href="#" class="sidebar__item">
        <i class="bi bi-people"></i> Users
      </a>
    </nav>
    <div class="sidebar__footer">
      <!-- User avatar + logout -->
    </div>
  </aside>
  <main class="dashboard-main">
    <!-- Content -->
  </main>
</div>
```

```css
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 260px;
  flex-shrink: 0;
  background: var(--neutral-950);
  color: var(--neutral-300);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.sidebar__logo { color: white; font-size: 1.25rem; font-weight: 800; padding: 0 0.75rem 1.5rem; }
.sidebar__section-title {
  font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--neutral-500);
  padding: 1rem 0.75rem 0.4rem;
}
.sidebar__item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border-radius: 0.5rem;
  color: var(--neutral-400);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all var(--duration-fast) ease;
}
.sidebar__item:hover { background: rgba(255,255,255,.06); color: white; }
.sidebar__item.active { background: rgba(var(--bs-primary-rgb), 0.15); color: var(--brand-400); }
.dashboard-main { flex: 1; min-width: 0; padding: 2rem; background: var(--neutral-50); }

@media (max-width: 991px) {
  .sidebar { display: none; } /* Заменяется offcanvas */
}
```

### 6.4 Empty State

```html
<div class="empty-state">
  <div class="empty-state__icon">📭</div>
  <h3 class="empty-state__title">No results found</h3>
  <p class="empty-state__desc">Try adjusting your search or filters</p>
  <a href="#" class="btn btn-primary btn-sm mt-3">Clear filters</a>
</div>
```

```css
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--neutral-400);
}
.empty-state__icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.6; }
.empty-state__title { font-size: 1.125rem; font-weight: 600; color: var(--neutral-600); margin-bottom: 0.5rem; }
.empty-state__desc { font-size: 0.9rem; }
```

---

## ЧАСТЬ VII — АРХИТЕКТУРНЫЕ ПРИНЦИПЫ

### 7.1 Структура CSS файла

```css
/* ============================================================
   PROJECT NAME — Main Stylesheet
   Architecture: Token-first → Base → Layout → Components → Utilities
   ============================================================ */

/* 1. TOKENS ─────────────────────────────────────── */
/* CSS Custom Properties (см. Часть II) */

/* 2. BASE RESET ──────────────────────────────────── */
/* Минимальные глобальные стили */

/* 3. TYPOGRAPHY ─────────────────────────────────── */
/* Шрифтовые классы, heading overrides */

/* 4. LAYOUT ─────────────────────────────────────── */
/* Grid systems, section spacing */

/* 5. COMPONENTS ─────────────────────────────────── */
/* Каждый компонент — отдельный блок с комментарием */
/* [component: navbar] */
/* [component: hero] */
/* [component: cards] */

/* 6. PAGE-SPECIFIC ──────────────────────────────── */
/* Стили конкретных страниц */

/* 7. UTILITIES ───────────────────────────────────── */
/* Кастомные utility-классы */

/* 8. ANIMATIONS ─────────────────────────────────── */
/* @keyframes и transition helpers */

/* 9. DARK THEME ─────────────────────────────────── */
/* [data-bs-theme="dark"] overrides */

/* 10. MEDIA QUERIES ─────────────────────────────── */
/* Только то, что нельзя решить Bootstrap-классами */
```

### 7.2 Именование и Организация

```
Принципы:
✓ BEM для кастомных компонентов: .card-feature__icon
✓ Bootstrap utilities в HTML, кастомные — в CSS
✓ Данные в data-атрибутах: data-bs-theme, data-animate
✗ Не писать !important (кроме reset-случаев)
✗ Не дублировать Bootstrap переменные
✗ Не использовать ID для стилизации
✗ Не вкладывать селекторы глубже 3 уровней
```

### 7.3 HTML Архитектура

```html
<!DOCTYPE html>
<html lang="ru" data-bs-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="...">

  <!-- Preconnect шрифты -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <!-- Bootstrap Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <!-- Custom CSS (ПОСЛЕ Bootstrap) -->
  <link rel="stylesheet" href="style.css">

  <title>Page Title</title>
</head>
<body>

  <!-- SKIP LINK (accessibility) -->
  <a class="visually-hidden-focusable" href="#main-content">Skip to content</a>

  <!-- NAVBAR -->
  <nav ...></nav>

  <!-- MAIN -->
  <main id="main-content">
    <section ...></section>
    <!-- ... -->
  </main>

  <!-- FOOTER -->
  <footer ...></footer>

  <!-- Scripts в конце body -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="main.js" defer></script>
</body>
</html>
```

---

## ЧАСТЬ VIII — ACCESSIBILITY (a11y)

```
Обязательный минимум:
✓ Контрастность текста: min 4.5:1 (normal), 3:1 (large/bold)
✓ Все интерактивные элементы — keyboard navigable
✓ Focus-visible стили (не убирать outline!)
✓ aria-label для иконочных кнопок
✓ role="img" + aria-label для декоративных SVG
✓ alt для всех img (пустой alt="" для декоративных)
✓ Семантический HTML: nav, main, footer, section, article, aside
✓ Заголовки в правильной иерархии h1→h2→h3
✓ form labels связаны с inputs (for/id или aria-labelledby)
✓ prefers-reduced-motion для анимаций
```

```css
/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Видимый focus */
:focus-visible {
  outline: 2px solid var(--bs-primary);
  outline-offset: 3px;
}
```

---

## ЧАСТЬ IX — PERFORMANCE

```
Приоритеты загрузки:
✓ Critical CSS inline в <head> (или минимальный first paint)
✓ Шрифты с display=swap
✓ Изображения с loading="lazy" (кроме hero LCP)
✓ Bootstrap через CDN с integrity hash
✓ will-change только для анимируемых элементов (снять после анимации)
✓ transform/opacity для анимаций (не margin/padding/top/left)
✓ Один requestAnimationFrame для scroll listeners
✓ IntersectionObserver вместо scroll events
```

---

## ЧАСТЬ X — ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ

```
ДИЗАЙН
□ Выбрано одно эстетическое направление
□ Шрифты — не Inter/Roboto/Arial
□ Цветовые токены определены через CSS vars
□ Есть один запоминающийся визуальный элемент

АДАПТИВНОСТЬ
□ Проверено на xs (375px), md (768px), lg (1024px), xl (1440px)
□ Touch targets min 44×44px
□ Нет горизонтального скролла
□ Изображения не выходят за контейнер

КОМПОНЕНТЫ
□ Состояния кнопок: default / hover / active / disabled / loading
□ Формы: empty / filled / error / success states
□ Карточки: default / hover
□ Пустые состояния для списков

АРХИТЕКТУРА
□ CSS организован по секциям
□ Нет хардкоженных цветов в компонентах
□ Bootstrap не переопределён через !important
□ JS не блокирует рендер

ACCESSIBILITY
□ Контрастность проверена
□ Клавиатурная навигация работает
□ Screen reader тест пройден (VoiceOver/NVDA)
□ prefers-reduced-motion учтён

PERFORMANCE
□ Нет неиспользуемого CSS Bootstrap (или кастомная сборка)
□ Изображения оптимизированы (WebP)
□ Анимации через transform/opacity
□ Шрифты preconnect + display=swap
```

---

## БЫСТРЫЙ СТАРТ — ШАБЛОН

При каждом новом проекте:
1. Скопируй блок токенов из **Части II**
2. Выбери эстетическое направление из **Части I**
3. Подключи шрифтовую пару из **Части II.2**
4. Собери лэйаут из паттернов **Части III**
5. Добавь нужные компоненты из **Части IV—VI**
6. Прогони чеклист из **Части X**

---

*FRONT-END SKILL GUIDE v1.0 | Bootstrap 5.3 | UI/UX Patterns | Universal Design System*
