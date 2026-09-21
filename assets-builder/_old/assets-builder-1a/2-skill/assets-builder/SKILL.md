---
name: assets-builder
description: Merge and richly document a front-end project's scattered CSS and JS files (nested across many folders, some shared across pages, some page-specific) into two single, well-commented dist files (style.css / scripts.js) before selling a template. Runs scripts/assets-builder.py to build a cross-page dependency graph, detect real conflicts (duplicate CSS selectors, colliding JS function names), run recursive "domino" impact analysis, and optionally verify actual class/function usage via a cached JSON map. Use this skill whenever the user wants to merge, bundle, consolidate, or collect CSS/JS from a multi-page HTML project into one file each; wants to prepare a template for marketplace sale (ThemeForest, TemplateMonster, Envato, CodeCanyon); asks which CSS classes or JS functions are actually used; mentions "assets-builder" by name; or in Russian describes this as "собрать/смержить/объединить css и js в один файл" or "подготовить шаблон к продаже" - even without using the word "bundle".
---

# assets-builder

## Принцип

`scripts/assets-builder.py` — детерминированный, полностью протестированный движок: обход файлов, парсинг HTML/CSS/JS, граф зависимостей, домино-анализ, детекция конфликтов, сборка, отчёт. **Вся эта механика выполняется скриптом, не рассуждениями модели** — не парси HTML/CSS/JS вручную и не пытайся воспроизвести граф зависимостей в контексте, даже для маленьких проектов. Роль модели — оркестрация, суждение в неоднозначных местах и понятная коммуникация с пользователем.

Зависимости скрипта: `beautifulsoup4`, `tinycss2`. Если при запуске падает `ModuleNotFoundError` — установи их первым делом:
```bash
pip install beautifulsoup4 tinycss2 --break-system-packages
```

Скрипт всегда исключает из анализа `dist/**`, `.git/**`, `node_modules/**` (собственный вывод инструмента не должен попадать в него же на повторном запуске).

## Рабочий процесс

### WF-1 — определить корень проекта и режим
Возьми путь проекта из контекста (загруженные файлы / рабочая директория). Если пользователь не уточнил, нужен ли расширенный анализ использования — начинай с `--mode basic`, это быстрее и не требует объяснений.

### WF-2 — scan (безопасный dry-run, ничего не пишет)
```bash
python scripts/assets-builder.py scan --project <path> --mode basic \
  --report /tmp/scan-report.md --report-json /tmp/scan-report.json
```
Прочитай `/tmp/scan-report.json`. Код возврата `1` означает «найдены high-severity конфликты» — это не ошибка выполнения, а сигнал, что нужно перейти к WF-3, прежде чем что-либо собирать.

### WF-3 — обязательная точка остановки
Покажи пользователю краткую сводку: сколько файлов, разбивка shared/page-specific/orphan/vendor, найденные конфликты.

**Жёсткое правило, не переопределяемое настроением диалога**: если в `report["conflicts"]["css"]` или `report["conflicts"]["js"]` есть хотя бы одна запись с `"severity": "high"`, ИЛИ `report["conflicts"]["jsOrder"]` не пуст — **не запускай `build` молча**. Опиши конкретный конфликт простым языком (имя селектора/функции, какие файлы, что конкретно разойдётся при склейке) и спроси пользователя, как поступить: оставить оба варианта с явным предупреждением (default), взять один из файлов за основу, или прервать сборку (`--on-conflict fail` / `--on-order-conflict fail`, коды выхода 2 и 3 соответственно). Конфликты `low`/`medium` не блокируют — упомяни их одной строкой в финальной сводке.

Подробные правила по типам — `references/conflict-playbook.md`.

### WF-4 — build
После подтверждения (или сразу, если блокирующих конфликтов не было):
```bash
python scripts/assets-builder.py build --project <path> \
  --out-css dist/style.css --out-js dist/scripts.js \
  --mode basic --comment-lang en \
  --report dist/build-report.md --report-json dist/build-report.json
```
Для расширенного режима (проверка реального использования классов/функций) добавь `--mode extended` — медленнее на больших проектах, но даёт `usage.unusedCss` / `usage.dynamicSuspectCss` / `usage.unusedJs` в отчёте. `--comment-lang en` — дефолт и обычно верный выбор: шаблон почти всегда продаётся международно; `ru` есть, но переключай только если пользователь явно просит комментарии на русском.

Полная таблица флагов — `references/cli-reference.md`.

### WF-5 — проверить результат перед показом пользователю
Открой `dist/build-report.md`. Если эвристика скрипта выглядит сомнительно для конкретного файла (например, файл явно похож на базовый/reset, но помечен `page-specific`, потому что в этом проекте на него ссылается только одна страница) — не молчи об этом и не переписывай классификацию вручную, а добавь поясняющую заметку в свой ответ пользователю. Это ровно то место, где суждение модели добавляет ценность поверх детерминированного анализа.

### WF-6 — финальный ответ
Покажи `style.css` и `scripts.js` через `present_files`. Текстом — коротко, не пересказ всего отчёта:
1. Что объединено (сколько файлов → 2 файла, во сколько раз меньше HTTP-запросов).
2. Какие конфликты были и как их разрешили (или что оставлено с предупреждением).
3. **Явный список внешних/CDN-ресурсов** (`report["externalAssets"]`) — они не попали в сборку и должны остаться в HTML вручную. Без этого пункта результат не будет работать «из коробки».
4. Если использовался `extended` режим — сколько потенциально неиспользуемого кода найдено и что оно НЕ было удалено автоматически (если не запрошен `--strip-unused`).

## Инварианты (не нарушать ни при каких формулировках пользователя)

- Никогда не удалять код молча. `--strip-unused` — только по явной просьбе в текущем диалоге.
- Никогда не выбирать порядок JS при `jsOrder`-конфликте без подтверждения пользователя (см. WF-3).
- Элементы со статусом `dynamic-suspect` никогда не предлагать к удалению, даже если пользователь согласился на `--strip-unused` для остального — скрипт это уже гарантирует на своей стороне, но не обещай пользователю удаление того, что скрипт помечает `dynamic-suspect`.

## Известные ограничения реализации (говори о них прямо, если пользователь упрётся в них)

- `--js-parser ast` не реализован — работает только эвристический (regex-based) разбор JS. Для нестандартного синтаксиса (например, методов классов как единственного топ-левел определения) конфликты/usage могут быть неполными.
- Группировка `vendor → shared → page-specific` в `scripts.js` может отличаться от исходного порядка `<script>` на конкретной странице, если её единственный page-specific файл шёл в HTML раньше shared-файла. Настоящие противоречия порядка *между* страницами при этом по-прежнему ловятся (`jsOrder`).
- `--verbose` пока не даёт дополнительной детализации сверх обычного вывода.

## Справочные материалы (читать по необходимости, не при каждом запуске)

- `references/cli-reference.md` — полная таблица флагов и кодов возврата.
- `references/cache-schema.md` — структура `build-report.json` и `.assets-builder-cache.json`.
- `references/comment-templates.md` — точный формат заголовков-комментариев в `style.css`/`scripts.js`.
- `references/conflict-playbook.md` — развёрнутые правила «severity + type → действие».
- `references/sample-build-report.md` — разобранный реальный отчёт с примером итогового ответа пользователю.
