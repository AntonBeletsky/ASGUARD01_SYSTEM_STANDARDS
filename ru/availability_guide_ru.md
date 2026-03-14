# Полный гайд по веб-доступности для фронтенд-разработчиков

> **WCAG 2.2** · **ARIA 1.2** · **HTML · CSS · JavaScript**

---

## Содержание

1. [Что такое доступность и зачем она нужна](#1-что-такое-доступность-и-зачем-она-нужна)
2. [Стандарты и уровни WCAG](#2-стандарты-и-уровни-wcag)
3. [Семантический HTML — основа всего](#3-семантический-html--основа-всего)
4. [ARIA — полное руководство](#4-aria--полное-руководство)
5. [Клавиатурная навигация](#5-клавиатурная-навигация)
6. [Управление фокусом через JavaScript](#6-управление-фокусом-через-javascript)
7. [Доступные формы](#7-доступные-формы)
8. [Изображения и медиаконтент](#8-изображения-и-медиаконтент)
9. [Цвет, контраст и визуальное оформление (CSS)](#9-цвет-контраст-и-визуальное-оформление-css)
10. [Движение и анимации](#10-движение-и-анимации)
11. [Доступные компоненты UI](#11-доступные-компоненты-ui)
12. [Живые регионы и уведомления](#12-живые-регионы-и-уведомления)
13. [Мобильная доступность](#13-мобильная-доступность)
14. [Тестирование доступности](#14-тестирование-доступности)
15. [Чеклист разработчика](#15-чеклист-разработчика)
16. [Инструменты и ресурсы](#16-инструменты-и-ресурсы)

---

## 1. Что такое доступность и зачем она нужна

**Веб-доступность (a11y)** — это практика разработки сайтов и приложений так, чтобы ими могли пользоваться все люди, включая тех, кто имеет физические, зрительные, слуховые, когнитивные или двигательные ограничения.

### Кто использует вспомогательные технологии

| Категория | Инструменты |
|---|---|
| Незрячие и слабовидящие | Скрінрідери (NVDA, JAWS, VoiceOver, TalkBack) |
| Двигательные ограничения | Клавиатура, switch-устройства, eye-tracking |
| Слабослышащие | Субтитры, транскрипты |
| Когнитивные особенности | Упрощённый язык, предсказуемый интерфейс |
| Пожилые пользователи | Увеличение текста, высокий контраст |
| Временные ограничения | Сломанная рука, яркий свет на экране |

### Почему это важно

- **~15% населения Земли** имеют те или иные ограничения (ВОЗ)
- Многие страны требуют соответствия WCAG по закону (ADA, EAA, Закон о связи Украины)
- Доступный код = чистый, семантический, SEO-friendly код
- Улучшает опыт для всех пользователей (elevator pitch: субтитры придумали для глухих, но ими пользуются все)

---

## 2. Стандарты и уровни WCAG

**WCAG (Web Content Accessibility Guidelines)** — международный стандарт от W3C.

### 4 основных принципа (POUR)

| Принцип | Суть |
|---|---|
| **P**erceivable — Воспринимаемость | Контент должен быть воспринят любым способом |
| **O**perable — Управляемость | Интерфейс должен быть доступен с любого устройства ввода |
| **U**nderstandable — Понятность | Контент и интерфейс должны быть понятны |
| **R**obust — Надёжность | Контент должен работать с разными вспомогательными технологиями |

### Уровни соответствия

- **A** — минимальный, обязательный
- **AA** — стандарт для большинства сайтов (требуется по закону в большинстве стран)
- **AAA** — расширенный, для специализированных ресурсов

> 🎯 **Цель большинства проектов: WCAG 2.2 AA**

---

## 3. Семантический HTML — основа всего

### Золотое правило

```html
<!-- ❌ Плохо — потеряна семантика, нужно дублировать всё через ARIA -->
<div class="button" onclick="submit()">Отправить</div>

<!-- ✅ Хорошо — нативное поведение, клавиатура, роль — бесплатно -->
<button type="submit">Отправить</button>
```

### Структура документа

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Уникальный и описательный заголовок страницы</title>
</head>
<body>

  <!-- Ссылка-пропуск для клавиатурных пользователей -->
  <a href="#main-content" class="skip-link">Перейти к основному содержимому</a>

  <header>
    <nav aria-label="Основная навигация">
      <ul>
        <li><a href="/">Главная</a></li>
        <li><a href="/about">О нас</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <h1>Заголовок страницы</h1>
    <!-- Основной контент -->
  </main>

  <aside aria-label="Дополнительные материалы">
    <!-- Боковая панель -->
  </aside>

  <footer>
    <!-- Подвал -->
  </footer>

</body>
</html>
```

### Иерархия заголовков

```html
<!-- ❌ Плохо — пропуск уровней, заголовки ради стиля -->
<h1>Сайт компании</h1>
<h3>Услуги</h3>  <!-- пропущен h2! -->
<h5>Разработка</h5>

<!-- ✅ Хорошо — последовательная иерархия -->
<h1>Сайт компании</h1>
  <h2>Услуги</h2>
    <h3>Разработка</h3>
    <h3>Дизайн</h3>
  <h2>Контакты</h2>
```

### Семантические теги и их смысл

```html
<!-- Текстовые -->
<p>Абзац</p>
<strong>Важное (семантически)</strong>     <!-- не просто жирный -->
<em>Акцент (семантически)</em>             <!-- не просто курсив -->
<b>Визуально жирный</b>                    <!-- без смысла -->
<i>Визуально курсив</i>                    <!-- без смысла -->
<mark>Выделено/найдено</mark>
<abbr title="Hypertext Markup Language">HTML</abbr>
<time datetime="2024-01-15">15 января</time>
<code>console.log()</code>
<kbd>Ctrl+C</kbd>                          <!-- клавиша клавиатуры -->
<blockquote cite="https://source.com">Цитата</blockquote>
<cite>Источник цитаты</cite>

<!-- Структурные -->
<article>   <!-- самостоятельный контент (статья, карточка) -->
<section>   <!-- тематический раздел -->
<aside>     <!-- боковой/дополнительный контент -->
<figure>    <!-- иллюстрация, схема, код -->
  <figcaption>Подпись к иллюстрации</figcaption>
</figure>

<!-- Списки -->
<ul>  <!-- ненумерованный -->
<ol>  <!-- нумерованный -->
<dl>  <!-- список определений -->
  <dt>Термин</dt>
  <dd>Определение</dd>
</dl>
```

### Ссылки vs кнопки

```html
<!-- Ссылка — для навигации, меняет URL -->
<a href="/page">Перейти на страницу</a>
<a href="https://external.com" target="_blank" rel="noopener noreferrer">
  Внешний сайт
  <span class="visually-hidden">(открывается в новой вкладке)</span>
</a>

<!-- Кнопка — для действий, не меняет URL -->
<button type="button" onclick="openModal()">Открыть модалку</button>
<button type="submit">Отправить форму</button>
<button type="reset">Сбросить форму</button>
```

---

## 4. ARIA — полное руководство

> **Первое правило ARIA**: Не используй ARIA, если есть нативный HTML-элемент.

### Роли (role)

#### Структурные роли
```html
<div role="banner">       <!-- = <header> верхнего уровня -->
<div role="navigation">   <!-- = <nav> -->
<div role="main">         <!-- = <main> -->
<div role="complementary"><!-- = <aside> -->
<div role="contentinfo">  <!-- = <footer> верхнего уровня -->
<div role="search">       <!-- форма поиска -->
<div role="region" aria-labelledby="section-title"> <!-- = <section> с именем -->
```

#### Виджет-роли
```html
<div role="button">       <!-- интерактивная кнопка -->
<div role="link">         <!-- ссылка -->
<div role="checkbox">     <!-- чекбокс -->
<div role="radio">        <!-- радиокнопка -->
<div role="textbox">      <!-- текстовое поле -->
<div role="combobox">     <!-- выпадающий список с вводом -->
<div role="listbox">      <!-- список для выбора -->
<div role="option">       <!-- элемент listbox/combobox -->
<div role="slider">       <!-- ползунок -->
<div role="spinbutton">   <!-- числовой ввод со стрелками -->
<div role="switch">       <!-- тумблер вкл/выкл -->
<div role="tab">          <!-- вкладка -->
<div role="tablist">      <!-- контейнер вкладок -->
<div role="tabpanel">     <!-- панель содержимого вкладки -->
<div role="menu">         <!-- контекстное меню -->
<div role="menuitem">     <!-- пункт меню -->
<div role="menuitemcheckbox"> <!-- пункт меню с чекбоксом -->
<div role="menuitemradio">    <!-- пункт меню с радио -->
<div role="tree">         <!-- дерево элементов -->
<div role="treeitem">     <!-- элемент дерева -->
<div role="grid">         <!-- интерактивная сетка -->
<div role="gridcell">     <!-- ячейка сетки -->
<div role="tooltip">      <!-- всплывающая подсказка -->
<div role="dialog">       <!-- диалоговое окно -->
<div role="alertdialog">  <!-- диалог с предупреждением -->
```

#### Роли для живого контента
```html
<div role="alert">        <!-- срочное сообщение (auto aria-live="assertive") -->
<div role="status">       <!-- статусное сообщение (auto aria-live="polite") -->
<div role="log">          <!-- лог сообщений -->
<div role="marquee">      <!-- прокручиваемый контент -->
<div role="timer">        <!-- таймер -->
<div role="progressbar">  <!-- прогресс-бар -->
```

---

### Свойства (Properties)

#### Именование элементов
```html
<!-- aria-label — прямой ярлык -->
<button aria-label="Закрыть диалог">✕</button>
<input type="search" aria-label="Поиск по сайту">
<nav aria-label="Хлебные крошки">...</nav>

<!-- aria-labelledby — ссылка на id элемента с именем -->
<h2 id="products-title">Наши продукты</h2>
<section aria-labelledby="products-title">...</section>

<!-- Именование по нескольким элементам -->
<span id="first">Имя</span>
<span id="last">Фамилия</span>
<input aria-labelledby="first last">

<!-- aria-describedby — дополнительное описание -->
<label for="password">Пароль</label>
<input id="password" type="password" aria-describedby="password-hint password-strength">
<p id="password-hint">Минимум 8 символов, буквы и цифры</p>
<p id="password-strength">Надёжность: средняя</p>

<!-- aria-details — ссылка на подробное описание -->
<img src="chart.png" alt="График продаж" aria-details="chart-description">
<div id="chart-description">
  <h3>Данные графика продаж</h3>
  <table>...</table>
</div>
```

#### Отношения между элементами
```html
<!-- aria-controls — элемент управляет другим -->
<button aria-controls="sidebar" aria-expanded="false">Открыть боковую панель</button>
<aside id="sidebar">...</aside>

<!-- aria-owns — элемент "владеет" другим (для нестандартных DOM-структур) -->
<ul role="tree" aria-owns="subtree">...</ul>

<!-- aria-flowto — следующий элемент в потоке чтения -->
<div id="step1" aria-flowto="step2">Шаг 1</div>
<div id="step2">Шаг 2</div>

<!-- aria-activedescendant — активный дочерний элемент -->
<ul role="listbox" aria-activedescendant="opt2" tabindex="0">
  <li role="option" id="opt1">Опция 1</li>
  <li role="option" id="opt2" aria-selected="true">Опция 2</li>
</ul>
```

#### Дополнительная информация
```html
<!-- aria-haspopup — есть всплывающий элемент -->
<button aria-haspopup="menu">Меню</button>
<button aria-haspopup="dialog">Открыть настройки</button>
<button aria-haspopup="listbox">Выбрать город</button>
<!-- значения: menu | listbox | tree | grid | dialog | true -->

<!-- aria-keyshortcuts — горячие клавиши -->
<button aria-keyshortcuts="Alt+S">Сохранить</button>

<!-- aria-roledescription — переопределить описание роли -->
<div role="region" aria-roledescription="слайд" aria-label="Слайд 1 из 5">...</div>

<!-- aria-placeholder — подсказка в поле ввода -->
<div role="textbox" aria-placeholder="Введите сообщение">...</div>

<!-- aria-valuemin, aria-valuemax, aria-valuenow, aria-valuetext -->
<div role="slider" 
  aria-valuemin="0" 
  aria-valuemax="100" 
  aria-valuenow="42"
  aria-valuetext="42 процента">
</div>

<!-- aria-posinset, aria-setsize — позиция в наборе -->
<li role="option" aria-setsize="10" aria-posinset="3">Элемент 3 из 10</li>

<!-- aria-level — уровень заголовка или дерева -->
<div role="heading" aria-level="2">Заголовок второго уровня</div>

<!-- aria-colcount, aria-rowcount, aria-colindex, aria-rowindex — таблицы -->
<table aria-rowcount="100">
  <tr aria-rowindex="1">
    <td aria-colindex="1">Ячейка</td>
  </tr>
</table>

<!-- aria-colspan, aria-rowspan — для ARIA-таблиц -->
<div role="gridcell" aria-colspan="2">Объединённая ячейка</div>
```

---

### Состояния (States)

```html
<!-- Видимость и состояние -->
<div aria-hidden="true">          <!-- скрыто от AT -->
<button aria-disabled="true">     <!-- отключено -->
<details>
  <summary aria-expanded="false"> <!-- свёрнуто/развёрнуто -->

<!-- Выбор и отметка -->
<option aria-selected="true">     <!-- выбрано в списке -->
<input type="checkbox" aria-checked="true">  <!-- отмечено -->
<input type="checkbox" aria-checked="mixed"> <!-- частично (indeterminate) -->
<div role="radio" aria-checked="false">      <!-- радио не выбрано -->
<button role="switch" aria-checked="true">   <!-- тумблер включён -->

<!-- Редактирование -->
<input aria-readonly="true">      <!-- только чтение -->
<input aria-required="true">      <!-- обязательное поле -->
<input aria-invalid="true">       <!-- невалидное значение -->
<input aria-invalid="grammar">    <!-- ошибка грамматики -->
<input aria-invalid="spelling">   <!-- ошибка орфографии -->

<!-- Состояния для сортируемых таблиц -->
<th aria-sort="ascending">        <!-- сортировка по возрастанию -->
<th aria-sort="descending">       <!-- сортировка по убыванию -->
<th aria-sort="none">             <!-- не отсортировано -->

<!-- Текущий элемент -->
<a aria-current="page">Текущая страница</a>
<li aria-current="step">Текущий шаг</li>
<tr aria-current="row">Текущая строка</tr>
<!-- значения: page | step | location | date | time | true -->

<!-- Нажатое состояние (для toggle-кнопок) -->
<button aria-pressed="true">Жирный</button>
<button aria-pressed="false">Курсив</button>

<!-- Захват (drag & drop) -->
<div aria-grabbed="true">         <!-- захвачен -->
<div aria-dropeffect="move">      <!-- принимает перетаскивание -->

<!-- Занятость -->
<div aria-busy="true">Загрузка...</div>
```

---

### aria-live — Живые регионы

```html
<!-- polite — скрінрідер зачитает после текущей фразы -->
<div aria-live="polite">
  Найдено 42 результата
</div>

<!-- assertive — прерывает скрінрідер немедленно (только для критических сообщений) -->
<div aria-live="assertive" role="alert">
  Критическая ошибка! Сессия истекла.
</div>

<!-- off — изменения не зачитываются -->
<div aria-live="off">...</div>

<!-- aria-atomic — зачитывать всё или только изменения -->
<div aria-live="polite" aria-atomic="true">
  Корзина: 3 товара на сумму 1500 грн
</div>

<!-- aria-relevant — какие изменения зачитывать -->
<!-- additions | removals | text | all -->
<div aria-live="polite" aria-relevant="additions text">
  <!-- зачитывать только добавления и изменения текста -->
</div>
```

---

## 5. Клавиатурная навигация

### Основные клавиши

| Клавиша | Действие |
|---|---|
| `Tab` | Следующий фокусируемый элемент |
| `Shift+Tab` | Предыдущий фокусируемый элемент |
| `Enter` | Активировать ссылку или кнопку |
| `Space` | Активировать кнопку, чекбокс |
| `Стрелки` | Навигация внутри компонента (tabs, menu, listbox) |
| `Esc` | Закрыть диалог/меню, отменить действие |
| `Home/End` | Первый/последний элемент в группе |

### tabindex

```html
<!-- tabindex="0" — добавить в порядок таба (только для нативно-нефокусируемых) -->
<div role="button" tabindex="0">Кастомная кнопка</div>

<!-- tabindex="-1" — убрать из таба, но сохранить возможность focus() через JS -->
<div id="modal-content" tabindex="-1">Содержимое модалки</div>

<!-- tabindex="1+" — НЕ ИСПОЛЬЗОВАТЬ! Ломает натуральный порядок -->
<!-- ❌ -->
<button tabindex="2">Кнопка 2</button>
<button tabindex="1">Кнопка 1</button>
```

### Skip Links (ссылки-пропуски)

```html
<!-- HTML -->
<a href="#main-content" class="skip-link">Перейти к основному содержимому</a>
<a href="#nav" class="skip-link">Перейти к навигации</a>
```

```css
/* CSS */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 9999;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 0;
}
```

### Порядок фокуса

```html
<!-- Порядок таба должен совпадать с визуальным порядком -->
<!-- Не меняй порядок только через CSS (flex-direction: row-reverse и т.п.) -->

<!-- ❌ Плохо — визуальный и DOM порядок разные -->
<style>
  .container { display: flex; flex-direction: row-reverse; }
</style>
<div class="container">
  <button>Кнопка 3</button>  <!-- визуально справа, в DOM первая -->
  <button>Кнопка 2</button>
  <button>Кнопка 1</button>  <!-- визуально слева, в DOM последняя -->
</div>

<!-- ✅ Хорошо — DOM порядок совпадает с визуальным -->
<div class="container">
  <button>Кнопка 1</button>
  <button>Кнопка 2</button>
  <button>Кнопка 3</button>
</div>
```

---

## 6. Управление фокусом через JavaScript

### Базовые операции

```javascript
// Установить фокус на элемент
element.focus();

// Убрать фокус
element.blur();

// Получить текущий элемент в фокусе
const focused = document.activeElement;

// Проверить, можно ли сфокусировать элемент
function isFocusable(el) {
  return el.tabIndex >= 0 && !el.disabled && el.offsetWidth > 0;
}
```

### Focus Trap — ловушка фокуса для модальных окон

```javascript
function createFocusTrap(container) {
  const focusableSelectors = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
    'details > summary',
  ].join(', ');

  function getFocusableElements() {
    return [...container.querySelectorAll(focusableSelectors)];
  }

  function handleKeydown(e) {
    if (e.key !== 'Tab') return;

    const focusable = getFocusableElements();
    const firstEl = focusable[0];
    const lastEl = focusable[focusable.length - 1];

    if (e.shiftKey) {
      // Shift+Tab — идём назад
      if (document.activeElement === firstEl) {
        e.preventDefault();
        lastEl.focus();
      }
    } else {
      // Tab — идём вперёд
      if (document.activeElement === lastEl) {
        e.preventDefault();
        firstEl.focus();
      }
    }
  }

  container.addEventListener('keydown', handleKeydown);

  return {
    activate() {
      const focusable = getFocusableElements();
      if (focusable.length) focusable[0].focus();
    },
    deactivate() {
      container.removeEventListener('keydown', handleKeydown);
    }
  };
}

// Использование
const modal = document.getElementById('modal');
const trap = createFocusTrap(modal);

function openModal() {
  modal.removeAttribute('hidden');
  modal.setAttribute('aria-hidden', 'false');
  trap.activate();
  // Сохранить элемент, который был в фокусе до открытия
  previousFocus = document.activeElement;
}

function closeModal() {
  modal.setAttribute('hidden', '');
  modal.setAttribute('aria-hidden', 'true');
  trap.deactivate();
  // Вернуть фокус
  previousFocus?.focus();
}
```

### Управление фокусом при роутинге (SPA)

```javascript
// При смене страницы в SPA — переместить фокус на заголовок или main
function handleRouteChange() {
  const main = document.getElementById('main-content');
  const heading = document.querySelector('h1');
  
  // Убедиться, что элемент фокусируем
  const target = heading || main;
  if (target) {
    if (!target.hasAttribute('tabindex')) {
      target.setAttribute('tabindex', '-1');
    }
    target.focus();
    // Прокрутить наверх
    window.scrollTo(0, 0);
  }
}
```

### Клавиатурные события

```javascript
// Полная поддержка клавиатуры для кастомного компонента
element.addEventListener('keydown', (e) => {
  switch (e.key) {
    case 'Enter':
    case ' ':         // пробел для кнопок
      e.preventDefault();
      element.click();
      break;
    case 'Escape':
      closeMenu();
      break;
    case 'ArrowDown':
      e.preventDefault();
      focusNextItem();
      break;
    case 'ArrowUp':
      e.preventDefault();
      focusPrevItem();
      break;
    case 'Home':
      e.preventDefault();
      focusFirstItem();
      break;
    case 'End':
      e.preventDefault();
      focusLastItem();
      break;
  }
});
```

### Roving tabindex — для навигации внутри компонента

```javascript
// Паттерн: только один элемент в группе имеет tabindex="0", остальные "-1"
// Стрелками перемещаемся внутри, Tab выходит из компонента

class RovingTabindex {
  constructor(container, itemSelector) {
    this.container = container;
    this.itemSelector = itemSelector;
    this.items = [...container.querySelectorAll(itemSelector)];
    this.currentIndex = 0;

    this.init();
  }

  init() {
    this.items.forEach((item, i) => {
      item.setAttribute('tabindex', i === 0 ? '0' : '-1');
    });

    this.container.addEventListener('keydown', this.handleKeydown.bind(this));
  }

  setFocus(index) {
    this.items[this.currentIndex].setAttribute('tabindex', '-1');
    this.currentIndex = (index + this.items.length) % this.items.length;
    this.items[this.currentIndex].setAttribute('tabindex', '0');
    this.items[this.currentIndex].focus();
  }

  handleKeydown(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      this.setFocus(this.currentIndex + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      this.setFocus(this.currentIndex - 1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      this.setFocus(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      this.setFocus(this.items.length - 1);
    }
  }
}

// Использование
const tablist = document.querySelector('[role="tablist"]');
new RovingTabindex(tablist, '[role="tab"]');
```

---

## 7. Доступные формы

### Правильная разметка

```html
<form novalidate>  <!-- отключаем нативные браузерные подсказки, делаем свои -->

  <!-- Каждое поле должно иметь label -->
  <div class="field">
    <label for="name">
      Имя
      <span aria-hidden="true">*</span>  <!-- звёздочка декоративная -->
    </label>
    <input 
      id="name" 
      type="text" 
      name="name"
      autocomplete="given-name"
      aria-required="true"
      aria-describedby="name-error"
    >
    <span id="name-error" role="alert" aria-live="polite" class="error" hidden>
      Введите ваше имя
    </span>
  </div>

  <!-- Группы полей — fieldset + legend -->
  <fieldset>
    <legend>Способ оплаты</legend>
    
    <label>
      <input type="radio" name="payment" value="card">
      Банковская карта
    </label>
    <label>
      <input type="radio" name="payment" value="cash">
      Наличные
    </label>
  </fieldset>

  <!-- Чекбоксы -->
  <fieldset>
    <legend>Уведомления</legend>
    <label>
      <input type="checkbox" name="email-notify">
      По электронной почте
    </label>
    <label>
      <input type="checkbox" name="sms-notify">
      По SMS
    </label>
  </fieldset>

  <!-- Select -->
  <div class="field">
    <label for="country">Страна</label>
    <select id="country" name="country" autocomplete="country">
      <option value="">-- Выберите страну --</option>
      <option value="ua">Украина</option>
      <option value="pl">Польша</option>
    </select>
  </div>

  <!-- Textarea -->
  <div class="field">
    <label for="message">
      Сообщение
      <span class="hint">(необязательно)</span>
    </label>
    <textarea 
      id="message" 
      name="message"
      rows="5"
      aria-describedby="message-hint"
    ></textarea>
    <p id="message-hint" class="hint">Максимум 500 символов</p>
  </div>

  <!-- Кнопка с ясным действием -->
  <button type="submit">Отправить заявку</button>
  
</form>
```

### Валидация и ошибки

```javascript
function validateField(input) {
  const errorEl = document.getElementById(input.getAttribute('aria-describedby').split(' ')[0]);
  
  if (!input.value.trim() && input.required) {
    // Показать ошибку
    input.setAttribute('aria-invalid', 'true');
    errorEl.textContent = 'Это поле обязательно для заполнения';
    errorEl.removeAttribute('hidden');
    return false;
  }
  
  // Убрать ошибку
  input.setAttribute('aria-invalid', 'false');
  errorEl.setAttribute('hidden', '');
  return true;
}

// Сводная ошибка при сабмите
function showSummaryError(errors) {
  const summary = document.getElementById('error-summary');
  const list = summary.querySelector('ul');
  
  list.innerHTML = errors.map(err => 
    `<li><a href="#${err.fieldId}">${err.message}</a></li>`
  ).join('');
  
  summary.removeAttribute('hidden');
  summary.focus();  // переместить фокус на сводку
}
```

```html
<!-- Сводка ошибок — размещается в начале формы -->
<div 
  id="error-summary" 
  role="alert" 
  tabindex="-1"
  hidden
>
  <h2>Пожалуйста, исправьте следующие ошибки:</h2>
  <ul>
    <!-- Ошибки с ссылками на поля -->
  </ul>
</div>
```

### autocomplete — помощь при заполнении

```html
<input autocomplete="name">          <!-- полное имя -->
<input autocomplete="given-name">    <!-- имя -->
<input autocomplete="family-name">   <!-- фамилия -->
<input autocomplete="email">         <!-- email -->
<input autocomplete="tel">           <!-- телефон -->
<input autocomplete="username">      <!-- имя пользователя -->
<input autocomplete="current-password"> <!-- текущий пароль -->
<input autocomplete="new-password">  <!-- новый пароль -->
<input autocomplete="street-address"><!-- адрес -->
<input autocomplete="postal-code">   <!-- почтовый индекс -->
<input autocomplete="country">       <!-- страна -->
<input autocomplete="cc-number">     <!-- номер карты -->
<input autocomplete="cc-exp">        <!-- срок карты -->
```

### Скрытые визуально, но доступные лейблы

```css
/* Visually hidden — скрыто визуально, но читается скрінрідером */
.visually-hidden,
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focusable версия — для skip links */
.visually-hidden:focus,
.sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

---

## 8. Изображения и медиаконтент

### alt-тексты

```html
<!-- Информативное изображение — описывай контент -->
<img src="team.jpg" alt="Команда из 5 человек позирует у офиса компании Acme">

<!-- Функциональное изображение — описывай действие/назначение -->
<button>
  <img src="search-icon.svg" alt="">  <!-- alt="" если есть текст рядом -->
  Поиск
</button>

<a href="/">
  <img src="logo.svg" alt="Acme — на главную">
</a>

<!-- Декоративное изображение — пустой alt -->
<img src="decorative-wave.svg" alt="" role="presentation">

<!-- Сложное изображение — графики, диаграммы -->
<figure>
  <img 
    src="sales-chart.png" 
    alt="График продаж за 2024 год" 
    aria-describedby="chart-data"
  >
  <figcaption id="chart-data">
    Продажи Q1: 120 тыс. Q2: 145 тыс. Q3: 98 тыс. Q4: 210 тыс.
    Годовой рост — 15% по сравнению с 2023 годом.
  </figcaption>
</figure>

<!-- SVG — используй title и desc -->
<svg role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Логотип компании</title>
  <desc id="svg-desc">Синий круг с белой буквой A в центре</desc>
  <!-- ... -->
</svg>

<!-- Фоновое CSS-изображение с текстовым содержимым -->
<div class="hero-banner" role="img" aria-label="Горная вершина на рассвете">
</div>
```

### Видео и аудио

```html
<!-- Видео с субтитрами и расшифровкой -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  
  <!-- Субтитры -->
  <track kind="subtitles" src="subs-ru.vtt" srclang="ru" label="Русский" default>
  <track kind="subtitles" src="subs-en.vtt" srclang="en" label="English">
  
  <!-- Тифлокомментарий для слабовидящих -->
  <track kind="descriptions" src="desc-ru.vtt" srclang="ru" label="Описание">
  
  <!-- Для браузеров без поддержки video -->
  <p>Ваш браузер не поддерживает видео. 
     <a href="video.mp4">Скачать видео</a>
  </p>
</video>

<!-- Ссылка на транскрипт -->
<p>
  <a href="transcript.html">Читать транскрипт видео</a>
</p>

<!-- Аудио -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<a href="transcript.html">Транскрипт подкаста</a>
```

---

## 9. Цвет, контраст и визуальное оформление (CSS)

### Контраст текста (WCAG AA)

| Тип текста | Минимальный контраст (AA) | Усиленный (AAA) |
|---|---|---|
| Обычный текст | 4.5:1 | 7:1 |
| Крупный текст (18pt/14pt bold) | 3:1 | 4.5:1 |
| UI-компоненты, графики | 3:1 | — |
| Декоративные элементы | Нет требований | — |

```css
/* Проверяй контраст инструментами! */

/* ❌ Плохо — серый текст на белом фоне, контраст ~2:1 */
.hint { color: #aaa; }

/* ✅ Хорошо — тёмно-серый на белом, контраст ~7:1 */
.hint { color: #595959; }
```

### Не используй цвет как единственный индикатор

```html
<!-- ❌ Плохо — только цвет отличает ошибку от успеха -->
<input class="error">  <!-- красная рамка -->
<input class="success">  <!-- зелёная рамка -->

<!-- ✅ Хорошо — цвет + иконка + текст -->
<div class="field-error">
  <span aria-hidden="true">⚠</span>
  <input aria-invalid="true" aria-describedby="err">
  <span id="err">Неверный формат email</span>
</div>
```

```css
/* Ссылки должны отличаться от текста не только цветом */

/* ❌ Плохо — только цвет */
a { color: blue; }

/* ✅ Хорошо — цвет + подчёркивание */
a {
  color: #0066cc;
  text-decoration: underline;
}

/* Или при достаточном контрасте — убрать underline, но добавить другой визуальный признак */
a {
  color: #0066cc;
  text-decoration: none;
  border-bottom: 2px solid currentColor;
}
a:hover, a:focus {
  text-decoration: underline;
}
```

### Видимый фокус

```css
/* ❌ НИКОГДА не убирай outline без замены! */
*:focus { outline: none; }  /* это ЗАПРЕЩЕНО */

/* ✅ Убирай только если есть замена */
:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Красивый стиль только для клавиатурных пользователей */
:focus:not(:focus-visible) {
  outline: none;  /* убираем при клике мышью */
}

:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
  border-radius: 2px;
}
```

### Размер текста и адаптивность

```css
/* Используй относительные единицы */
html { font-size: 100%; }   /* не px! */
body { font-size: 1rem; }

/* Текст должен масштабироваться до 200% без потери контента */
@media (max-width: 600px) {
  body { font-size: clamp(1rem, 2.5vw, 1.25rem); }
}

/* Межстрочный интервал — минимум 1.5 для основного текста */
p {
  line-height: 1.5;
  /* Пространство после абзаца */
  margin-bottom: 1.5em;
  /* Максимальная ширина для читаемости */
  max-width: 75ch;
}

/* Межбуквенный интервал */
p { letter-spacing: 0.12em; }   /* не больше */
/* Межсловный */
p { word-spacing: 0.16em; }     /* не больше */
```

### Режим высокого контраста (Windows)

```css
/* Поддержка Windows High Contrast Mode */
@media (forced-colors: active) {
  /* Принудительные цвета, игнорировать свои */
  .custom-button {
    border: 2px solid ButtonText;  /* системный цвет */
    color: ButtonText;
    background: ButtonFace;
  }

  /* Не скрывать outline */
  *:focus {
    outline: 2px solid Highlight !important;
  }
}

/* Старый синтаксис для IE */
@media (-ms-high-contrast: active) {
  .icon { border: 1px solid windowText; }
}
```

### Пользовательские цветовые предпочтения

```css
/* Тёмная тема системы */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #121212;
    --text: #e0e0e0;
    --accent: #90caf9;
  }
}

/* Светлая тема */
@media (prefers-color-scheme: light) {
  :root {
    --bg: #ffffff;
    --text: #212121;
    --accent: #1565c0;
  }
}
```

---

## 10. Движение и анимации

### prefers-reduced-motion

```css
/* Базовые анимации */
.button {
  transition: transform 0.2s ease, background-color 0.2s ease;
}

/* Отключить/упростить при системной настройке */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Более тонкий подход — убрать только декоративные анимации */
@media (prefers-reduced-motion: reduce) {
  .hero-animation { animation: none; }
  .parallax { transform: none !important; }
  .scroll-fade { opacity: 1 !important; }
  
  /* Оставить функциональные (фокус, состояния) */
  :focus-visible { outline: 3px solid #005fcc; }
}
```

```javascript
// Проверка в JavaScript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // Запустить анимацию
  animateElement(el);
} else {
  // Показать сразу
  el.style.opacity = '1';
}
```

### Опасные анимации (эпилепсия)

```
❌ ЗАПРЕЩЕНО:
- Мигание чаще 3 раз в секунду
- Большие мигающие области (>25% экрана)
- Красные вспышки
```

---

## 11. Доступные компоненты UI

### Модальное диалоговое окно

```html
<button id="open-modal">Открыть диалог</button>

<div
  id="modal"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
  hidden
>
  <h2 id="modal-title">Подтверждение удаления</h2>
  <p id="modal-desc">Это действие нельзя отменить. Вы уверены?</p>
  
  <div class="modal-actions">
    <button id="confirm-delete" autofocus>Удалить</button>
    <button id="close-modal">Отмена</button>
  </div>
</div>

<div id="modal-backdrop" hidden></div>
```

```javascript
const modal = document.getElementById('modal');
const openBtn = document.getElementById('open-modal');
const closeBtn = document.getElementById('close-modal');
let lastFocused;

function openModal() {
  lastFocused = document.activeElement;
  modal.removeAttribute('hidden');
  document.getElementById('modal-backdrop').removeAttribute('hidden');
  document.body.setAttribute('aria-hidden', 'true');  // скрыть основной контент
  modal.removeAttribute('aria-hidden');
  
  // Фокус на первый интерактивный элемент или autofocus
  modal.querySelector('[autofocus]')?.focus() || 
  modal.querySelector('button, input, [tabindex="0"]')?.focus();
}

function closeModal() {
  modal.setAttribute('hidden', '');
  document.getElementById('modal-backdrop').setAttribute('hidden', '');
  document.body.removeAttribute('aria-hidden');
  lastFocused?.focus();  // вернуть фокус
}

// Закрыть по Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modal.hidden) closeModal();
});

// Закрыть по клику на фон
document.getElementById('modal-backdrop').addEventListener('click', closeModal);
```

### Вкладки (Tabs)

```html
<div class="tabs">
  <div role="tablist" aria-label="Информация о продукте">
    <button 
      role="tab" 
      id="tab-desc"
      aria-controls="panel-desc"
      aria-selected="true"
      tabindex="0"
    >Описание</button>
    
    <button 
      role="tab" 
      id="tab-specs"
      aria-controls="panel-specs"
      aria-selected="false"
      tabindex="-1"
    >Характеристики</button>
    
    <button 
      role="tab" 
      id="tab-reviews"
      aria-controls="panel-reviews"
      aria-selected="false"
      tabindex="-1"
    >Отзывы</button>
  </div>

  <div role="tabpanel" id="panel-desc" aria-labelledby="tab-desc">
    <h3>Описание товара</h3>
    <p>...</p>
  </div>
  
  <div role="tabpanel" id="panel-specs" aria-labelledby="tab-specs" hidden>
    <h3>Технические характеристики</h3>
    <p>...</p>
  </div>
  
  <div role="tabpanel" id="panel-reviews" aria-labelledby="tab-reviews" hidden>
    <h3>Отзывы покупателей</h3>
    <p>...</p>
  </div>
</div>
```

```javascript
const tablist = document.querySelector('[role="tablist"]');
const tabs = [...tablist.querySelectorAll('[role="tab"]')];

tablist.addEventListener('keydown', (e) => {
  const currentIndex = tabs.indexOf(document.activeElement);
  let newIndex;
  
  if (e.key === 'ArrowRight') {
    newIndex = (currentIndex + 1) % tabs.length;
  } else if (e.key === 'ArrowLeft') {
    newIndex = (currentIndex - 1 + tabs.length) % tabs.length;
  } else if (e.key === 'Home') {
    newIndex = 0;
  } else if (e.key === 'End') {
    newIndex = tabs.length - 1;
  } else return;
  
  e.preventDefault();
  activateTab(tabs[newIndex]);
});

function activateTab(tab) {
  // Сбросить все
  tabs.forEach(t => {
    t.setAttribute('aria-selected', 'false');
    t.setAttribute('tabindex', '-1');
    document.getElementById(t.getAttribute('aria-controls')).hidden = true;
  });
  
  // Активировать нужную
  tab.setAttribute('aria-selected', 'true');
  tab.setAttribute('tabindex', '0');
  tab.focus();
  document.getElementById(tab.getAttribute('aria-controls')).hidden = false;
}
```

### Аккордеон

```html
<div class="accordion">
  <h3>
    <button
      type="button"
      aria-expanded="false"
      aria-controls="section1-content"
      id="section1-header"
    >
      Как оформить заказ?
      <span aria-hidden="true" class="icon">▼</span>
    </button>
  </h3>
  <div
    id="section1-content"
    role="region"
    aria-labelledby="section1-header"
    hidden
  >
    <p>Для оформления заказа...</p>
  </div>

  <h3>
    <button
      type="button"
      aria-expanded="false"
      aria-controls="section2-content"
      id="section2-header"
    >
      Способы оплаты
    </button>
  </h3>
  <div
    id="section2-content"
    role="region"
    aria-labelledby="section2-header"
    hidden
  >
    <p>Мы принимаем...</p>
  </div>
</div>
```

### Выпадающее меню (Disclosure)

```html
<div class="dropdown">
  <button 
    type="button"
    aria-haspopup="menu"
    aria-expanded="false"
    aria-controls="user-menu"
    id="user-menu-btn"
  >
    Профиль
  </button>
  
  <ul 
    role="menu"
    id="user-menu"
    aria-labelledby="user-menu-btn"
    hidden
  >
    <li role="none">
      <a role="menuitem" href="/settings">Настройки</a>
    </li>
    <li role="none">
      <a role="menuitem" href="/orders">Заказы</a>
    </li>
    <li role="none">
      <button role="menuitem" type="button">Выйти</button>
    </li>
  </ul>
</div>
```

### Тост-уведомления

```html
<!-- Контейнер для тостов -->
<div 
  id="toast-container"
  aria-live="polite"
  aria-atomic="false"
  class="toast-container"
>
</div>
```

```javascript
function showToast(message, type = 'info', duration = 5000) {
  const container = document.getElementById('toast-container');
  
  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.setAttribute('role', type === 'error' ? 'alert' : 'status');
  toast.innerHTML = `
    <span class="toast__message">${message}</span>
    <button class="toast__close" aria-label="Закрыть уведомление">✕</button>
  `;
  
  toast.querySelector('.toast__close').addEventListener('click', () => {
    removeToast(toast);
  });
  
  container.appendChild(toast);
  
  if (duration > 0) {
    setTimeout(() => removeToast(toast), duration);
  }
  
  return toast;
}

function removeToast(toast) {
  toast.setAttribute('aria-hidden', 'true');
  toast.addEventListener('transitionend', () => toast.remove());
}
```

### Карусель/Слайдер

```html
<section aria-roledescription="карусель" aria-label="Популярные товары">
  
  <!-- Управление -->
  <div class="carousel-controls">
    <button 
      type="button" 
      aria-label="Предыдущий слайд"
      id="prev-btn"
    >‹</button>
    
    <!-- Индикатор -->
    <div role="group" aria-label="Слайды">
      <button aria-label="Слайд 1" aria-current="true" aria-pressed="true">•</button>
      <button aria-label="Слайд 2" aria-pressed="false">•</button>
      <button aria-label="Слайд 3" aria-pressed="false">•</button>
    </div>
    
    <button 
      type="button" 
      aria-label="Следующий слайд"
      id="next-btn"
    >›</button>
    
    <!-- Пауза автопрокрутки -->
    <button 
      type="button" 
      id="autoplay-btn"
      aria-label="Остановить автопрокрутку"
      aria-pressed="true"
    >⏸</button>
  </div>
  
  <!-- Слайды -->
  <div class="carousel-slides">
    <div 
      role="group"
      aria-roledescription="слайд"
      aria-label="1 из 3: Смартфон Samsung"
      aria-hidden="false"
    >
      <img src="phone.jpg" alt="Смартфон Samsung Galaxy S24">
      <h3>Samsung Galaxy S24</h3>
      <p>от 29 999 грн</p>
    </div>
    
    <div 
      role="group"
      aria-roledescription="слайд"
      aria-label="2 из 3: Ноутбук Apple"
      aria-hidden="true"
    >
      <!-- ... -->
    </div>
  </div>
  
</section>
```

### Таблицы данных

```html
<!-- Простая таблица -->
<table>
  <caption>Отчёт о продажах за Q4 2024</caption>
  <thead>
    <tr>
      <th scope="col">Товар</th>
      <th scope="col">Количество</th>
      <th scope="col">Сумма, грн</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Смартфон</td>
      <td>150</td>
      <td>2 250 000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td>Итого</td>
      <td>450</td>
      <td>5 750 000</td>
    </tr>
  </tfoot>
</table>

<!-- Сложная таблица с группировкой -->
<table>
  <caption>Расписание занятий</caption>
  <thead>
    <tr>
      <th scope="col" id="time-col">Время</th>
      <th scope="col" id="mon-col">Пн</th>
      <th scope="col" id="tue-col">Вт</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row" id="row-9">9:00</th>
      <td headers="mon-col row-9">Математика</td>
      <td headers="tue-col row-9">Физика</td>
    </tr>
  </tbody>
</table>

<!-- Сортируемая таблица -->
<table>
  <thead>
    <tr>
      <th scope="col">
        <button aria-sort="none" type="button">
          Имя <span aria-hidden="true">↕</span>
        </button>
      </th>
      <th scope="col">
        <button aria-sort="ascending" type="button">
          Дата <span aria-hidden="true">↑</span>
        </button>
      </th>
    </tr>
  </thead>
</table>
```

---

## 12. Живые регионы и уведомления

### Паттерны использования

```javascript
// Универсальная функция для сообщений скрінрідеру
function announce(message, priority = 'polite') {
  const announcer = document.getElementById(`aria-announcer-${priority}`);
  
  // Очистить и переустановить — гарантирует зачитывание
  announcer.textContent = '';
  
  requestAnimationFrame(() => {
    announcer.textContent = message;
  });
}

// Разместить в HTML (невидимые)
// <div id="aria-announcer-polite" aria-live="polite" class="visually-hidden"></div>
// <div id="aria-announcer-assertive" aria-live="assertive" class="visually-hidden"></div>

// Использование
announce('Товар добавлен в корзину');
announce('Критическая ошибка: не удалось сохранить', 'assertive');
announce(`Найдено ${count} результатов`);
announce('Загрузка завершена, показано 20 из 100 товаров');
```

### Прогресс загрузки

```html
<!-- Индикатор загрузки страницы -->
<div 
  id="loading" 
  role="status" 
  aria-live="polite"
  aria-label="Загрузка"
  hidden
>
  <span aria-hidden="true" class="spinner"></span>
  <span class="visually-hidden">Загрузка, пожалуйста подождите</span>
</div>

<!-- Прогресс-бар -->
<div role="progressbar" 
  aria-valuenow="45" 
  aria-valuemin="0" 
  aria-valuemax="100"
  aria-label="Загрузка файла"
  aria-valuetext="45 процентов завершено"
>
  <div class="progress-bar__fill" style="width: 45%"></div>
</div>

<!-- Неопределённый прогресс -->
<div role="progressbar" 
  aria-label="Обработка запроса"
  aria-valuetext="Выполняется"
>
  <!-- Анимированный индикатор -->
</div>
```

---

## 13. Мобильная доступность

### Touch-цели

```css
/* Минимальный размер touch-цели: 44×44px (Apple HIG) / 48×48px (Material) */
button,
a,
input[type="checkbox"],
input[type="radio"] {
  min-height: 44px;
  min-width: 44px;
}

/* Увеличить область клика без изменения визуального размера */
.small-button {
  position: relative;
  padding: 4px;
}

.small-button::after {
  content: '';
  position: absolute;
  inset: -10px;  /* расширяем область клика */
}
```

### Масштабирование

```html
<!-- НЕ запрещай масштабирование! -->
<!-- ❌ Плохо -->
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, maximum-scale=1">

<!-- ✅ Хорошо -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Жесты

```javascript
// Для сложных жестов предоставляй альтернативу
// Например, swipe можно заменить кнопками

// Pointer events поддерживают все устройства ввода
element.addEventListener('pointerdown', handleStart);
element.addEventListener('pointermove', handleMove);
element.addEventListener('pointerup', handleEnd);

// Или используй touch-action CSS
.swipeable {
  touch-action: pan-y;  /* разрешить вертикальный скролл, не мешать горизонтальному свайпу */
}
```

---

## 14. Тестирование доступности

### Автоматическое тестирование

```bash
# axe-core — самый популярный
npm install axe-core

# Playwright + axe
npm install @axe-core/playwright

# Jest + axe
npm install jest-axe
```

```javascript
// axe-core в браузере
import axe from 'axe-core';

axe.run(document, {
  runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
}).then(results => {
  if (results.violations.length) {
    console.error('Нарушения доступности:', results.violations);
    results.violations.forEach(v => {
      console.error(`[${v.impact}] ${v.description}`);
      v.nodes.forEach(n => console.error('  Элемент:', n.html));
    });
  }
});

// Playwright тест
import { checkA11y, injectAxe } from 'axe-playwright';

test('главная страница доступна', async ({ page }) => {
  await page.goto('/');
  await injectAxe(page);
  await checkA11y(page, null, {
    axeOptions: {
      runOnly: ['wcag2a', 'wcag2aa']
    }
  });
});

// Jest тест
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('кнопка доступна', async () => {
  const { container } = render(<MyButton label="Сохранить" />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Ручное тестирование

#### Тест с клавиатурой (без мыши!)
```
1. Открыть страницу
2. Нажать Tab — виден ли фокус?
3. Пройти по всем интерактивным элементам
4. Можно ли активировать каждый элемент Enter/Space?
5. Работают ли модальные окна (Escape закрывает)?
6. Вернулся ли фокус после закрытия?
7. Работает ли skip link?
```

#### Тест со скрінрідером

| ОС | Скрінрідер | Браузер |
|---|---|---|
| Windows | NVDA (бесплатно) | Firefox, Chrome |
| Windows | JAWS | IE, Chrome |
| macOS | VoiceOver (встроен, Cmd+F5) | Safari |
| iOS | VoiceOver (встроен) | Safari |
| Android | TalkBack (встроен) | Chrome |
| Linux | Orca | Firefox |

```
Базовый тест VoiceOver (macOS):
1. Cmd+F5 — включить
2. Tab — переход между элементами
3. VO+Стрелки — навигация по содержимому
4. VO+U — ротор (быстрая навигация)
5. Cmd+F5 — выключить
```

### DevTools

```javascript
// Chrome DevTools → Accessibility tree (Cmd+Shift+P → "Accessibility")
// Firefox → Developer Tools → Accessibility tab
// Lighthouse → Accessibility audit

// Проверить порядок фокуса
document.addEventListener('focusin', (e) => {
  console.log('Focused:', e.target.tagName, e.target.id, e.target.className);
});

// Список всех интерактивных элементов
const interactive = document.querySelectorAll(
  'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
);
console.table([...interactive].map(el => ({
  tag: el.tagName,
  text: el.textContent?.trim() || el.value || el.alt,
  tabindex: el.tabIndex,
})));
```

---

## 15. Чеклист разработчика

### HTML
- [ ] Указан `lang` на `<html>`
- [ ] Уникальный и описательный `<title>` на каждой странице
- [ ] Правильная иерархия заголовков (h1 → h2 → h3)
- [ ] Используются семантические теги (nav, main, header, footer, article)
- [ ] Все изображения имеют `alt` (пустой для декоративных)
- [ ] Каждое поле формы связано с `<label>`
- [ ] Группы полей обёрнуты в `<fieldset>` с `<legend>`
- [ ] Ссылки используются для навигации, кнопки — для действий
- [ ] Внешние ссылки имеют предупреждение об открытии в новой вкладке
- [ ] Таблицы данных имеют `<caption>` и `scope` у заголовков

### ARIA
- [ ] ARIA используется только там, где нет нативного HTML
- [ ] Все интерактивные кастомные элементы имеют роль
- [ ] Все элементы без видимого текста имеют `aria-label` или `aria-labelledby`
- [ ] Динамический контент использует `aria-live`
- [ ] Модальные окна используют `role="dialog"` и `aria-modal`
- [ ] `aria-expanded` актуален у кнопок-триггеров
- [ ] `aria-invalid` и `aria-required` на полях формы

### Клавиатура
- [ ] Весь функционал доступен с клавиатуры
- [ ] Видимый фокус на всех интерактивных элементах
- [ ] Порядок фокуса логичен (совпадает с визуальным)
- [ ] Нет ловушек фокуса (кроме модальных окон)
- [ ] Модальные окна имеют focus trap и закрываются по Escape
- [ ] Есть skip link в начале страницы
- [ ] `tabindex` только 0 или -1, никогда больше

### CSS
- [ ] Контраст текста минимум 4.5:1 (AA)
- [ ] Контраст UI-элементов минимум 3:1
- [ ] Цвет не единственный индикатор информации
- [ ] `outline` виден при фокусе (не `outline: none`)
- [ ] Анимации отключаются при `prefers-reduced-motion`
- [ ] Нет `user-scalable=no` в viewport
- [ ] Текст масштабируется до 200% без потери контента
- [ ] Touch-цели минимум 44×44px

### JavaScript
- [ ] Динамические изменения анонсируются скрінрідеру
- [ ] Фокус возвращается после закрытия диалогов
- [ ] При роутинге (SPA) фокус перемещается на новый контент
- [ ] Обработчики событий на и click, и keydown/keypress

### Тестирование
- [ ] Пройден тест с axe-core (0 критических нарушений)
- [ ] Протестировано с клавиатурой (без мыши)
- [ ] Протестировано с VoiceOver или NVDA
- [ ] Lighthouse Accessibility score ≥ 90

---

## 16. Инструменты и ресурсы

### Браузерные расширения
- **axe DevTools** — автоматическая проверка доступности
- **WAVE** — визуальная проверка
- **Accessibility Insights** — полный аудит (Microsoft)
- **Colour Contrast Analyser** — проверка контраста

### Инструменты разработчика
- **Storybook + @storybook/addon-a11y** — проверка компонентов
- **eslint-plugin-jsx-a11y** — статический анализ JSX
- **axe-core, jest-axe, @axe-core/playwright** — автотесты
- **Lighthouse** (встроен в Chrome DevTools)
- **Pa11y** — CLI-инструмент для автоматизации

### Онлайн-инструменты
- **WebAIM Contrast Checker** — contrast.webaim.org
- **Colour Contrast Checker** — colourcontrast.cc
- **Accessible Color Palette Builder** — venngage.com/tools/accessible-color-palette-generator
- **WAVE** — wave.webaim.org
- **AChecker** — achecker.achecks.ca

### Стандарты и документация
- **WCAG 2.2** — w3.org/TR/WCAG22
- **ARIA 1.2** — w3.org/TR/wai-aria-1.2
- **ARIA Authoring Practices** — w3.org/WAI/ARIA/apg
- **WebAIM** — webaim.org
- **MDN Accessibility** — developer.mozilla.org/en-US/docs/Web/Accessibility
- **The A11y Project** — a11yproject.com

### Паттерны и компоненты
- **ARIA APG Patterns** — w3.org/WAI/ARIA/apg/patterns (каноническое руководство)
- **Inclusive Components** — inclusive-components.design
- **Headless UI** — headlessui.com
- **Radix UI** — radix-ui.com
- **React Aria** — react-spectrum.adobe.com/react-aria

---

## Быстрый справочник: самые частые ошибки

| Ошибка | Решение |
|---|---|
| `<div onclick>` вместо `<button>` | Используй `<button>` |
| Изображение без `alt` | Добавь `alt` или `alt=""` |
| `outline: none` без замены | Стилизуй `:focus-visible` |
| Поле формы без `<label>` | Добавь `<label for>` или `aria-label` |
| Контраст < 4.5:1 | Измени цвет текста или фона |
| Фокус не возвращается после закрытия диалога | Сохрани `lastFocused` и верни |
| `tabindex="3"` и выше | Только `0` или `-1` |
| Анимация без `prefers-reduced-motion` | Добавь media query |
| Только цвет как индикатор | Добавь иконку, текст, форму |
| `user-scalable=no` в viewport | Удали это ограничение |
| Пустая ссылка `<a href="#">` | Используй `<button>` или добавь `aria-label` |
| Нет skip link | Добавь в начало страницы |
| `aria-label` дублирует видимый текст | Убери лишний `aria-label` |

---

*Этот гайд основан на WCAG 2.2, WAI-ARIA 1.2 и ARIA Authoring Practices Guide.*  
*Последнее обновление: 2024*
