// university_erd.js
// ER-диаграмма университетской модели курсов.
//
// Данные (ENTITIES/RELATIONS) — единственный источник истины: из них строится и текст
// диаграммы для Mermaid, и доступная HTML-таблица (erd-006). Это исключает расхождение
// между «тем, что видно на картинке» и «тем, что доступно текстом» — они физически не
// могут разойтись, потому что рендерятся из одного и того же массива.
//
// Состав таблиц и связей намеренно оставлен без изменений относительно исходного файла —
// в т.ч. кратность связи DEPARTMENT-TEACHER("headed by"), где ранее (в анализе
// university_course_map.json) было найдено расхождение с моделью данных. Это отдельная
// задача про корректность модели, не про UI/UX, поэтому здесь не трогаю.

const ENTITIES = [
  { name: 'DEPARTMENT', fields: [
    ['id', 'id', 'PK'], ['code', 'string', 'UK'], ['name', 'string', ''], ['head_teacher_id', 'id', 'FK'],
  ]},
  { name: 'SEMESTER', fields: [
    ['id', 'id', 'PK'], ['label', 'string', 'UK'], ['start_date', 'date', ''], ['end_date', 'date', ''], ['is_active', 'bool', ''],
  ]},
  { name: 'ROOM', fields: [
    ['id', 'id', 'PK'], ['number', 'string', 'UK'], ['capacity', 'int32', ''], ['has_computers', 'bool', ''],
  ]},
  { name: 'TEACHER', fields: [
    ['id', 'uuid', 'PK'], ['department_id', 'id', 'FK'], ['last_name', 'string', ''], ['email', 'string', 'UK'], ['academic_title', 'string', ''], ['is_active', 'bool', ''],
  ]},
  { name: 'STUDENT', fields: [
    ['id', 'uuid', 'PK'], ['student_number', 'string', 'UK'], ['last_name', 'string', ''], ['email', 'string', 'UK'], ['year_of_study', 'int8', ''], ['gpa', 'decimal', ''], ['is_active', 'bool', ''],
  ]},
  { name: 'COURSE', fields: [
    ['id', 'id', 'PK'], ['department_id', 'id', 'FK'], ['code', 'string', 'UK'], ['title', 'string', ''], ['credits', 'int8', ''], ['max_students', 'int32', ''], ['is_elective', 'bool', ''],
  ]},
  { name: 'COURSE_TEACHER', fields: [
    ['id', 'id', 'PK'], ['course_id', 'id', 'FK'], ['teacher_id', 'uuid', 'FK'], ['semester_id', 'id', 'FK'], ['role', 'string', ''],
  ]},
  { name: 'LESSON', fields: [
    ['id', 'id', 'PK'], ['course_id', 'id', 'FK'], ['semester_id', 'id', 'FK'], ['teacher_id', 'uuid', 'FK'], ['room_id', 'id', 'FK'], ['lesson_type', 'enum', ''], ['scheduled_date', 'date', ''], ['start_time', 'time', ''], ['is_cancelled', 'bool', ''],
  ]},
  { name: 'ENROLLMENT', fields: [
    ['id', 'id', 'PK'], ['student_id', 'uuid', 'FK'], ['course_id', 'id', 'FK'], ['semester_id', 'id', 'FK'], ['enrolled_at', 'timestamp', ''], ['is_active', 'bool', ''],
  ]},
  { name: 'ATTENDANCE', fields: [
    ['id', 'id', 'PK'], ['student_id', 'uuid', 'FK'], ['lesson_id', 'id', 'FK'], ['status', 'enum', ''], ['recorded_at', 'timestamp', ''],
  ]},
  { name: 'ASSIGNMENT', fields: [
    ['id', 'id', 'PK'], ['course_id', 'id', 'FK'], ['title', 'string', ''], ['max_score', 'int32', ''], ['weight', 'decimal', ''], ['due_date', 'datetime', ''],
  ]},
  { name: 'SUBMISSION', fields: [
    ['id', 'id', 'PK'], ['assignment_id', 'id', 'FK'], ['student_id', 'uuid', 'FK'], ['status', 'enum', ''], ['score', 'decimal', ''], ['graded_by', 'uuid', 'FK'],
  ]},
  { name: 'COURSE_GRADE', fields: [
    ['id', 'id', 'PK'], ['enrollment_id', 'id', 'FK'], ['numeric_score', 'decimal', ''], ['letter_grade', 'enum', ''], ['passed', 'bool', ''], ['issued_by', 'uuid', 'FK'],
  ]},
];

// [from, to, mermaid-cardinality, label (как в исходнике), русское описание для таблицы]
const RELATIONS = [
  ['DEPARTMENT', 'TEACHER', '||--o{', 'employs', 'Одна кафедра — много преподавателей'],
  ['DEPARTMENT', 'COURSE', '||--o{', 'offers', 'Одна кафедра — много курсов'],
  ['DEPARTMENT', 'TEACHER', '}o--||', 'headed by', 'Глава кафедры (см. примечание в шапке файла)'],
  ['TEACHER', 'COURSE_TEACHER', '||--o{', 'assigned to', 'Назначения преподавателя на курсы'],
  ['COURSE', 'COURSE_TEACHER', '||--o{', 'taught by', 'Кто ведёт курс'],
  ['SEMESTER', 'COURSE_TEACHER', '||--o{', 'in', 'В каком семестре ведётся'],
  ['COURSE', 'LESSON', '||--o{', 'has sessions', 'Занятия курса'],
  ['SEMESTER', 'LESSON', '||--o{', 'during', 'В каком семестре проходит'],
  ['TEACHER', 'LESSON', '||--o{', 'conducts', 'Кто проводит занятие'],
  ['ROOM', 'LESSON', '||--o{', 'hosts', 'Где проходит занятие'],
  ['STUDENT', 'ENROLLMENT', '||--o{', 'registers in', 'Записи студента на курсы'],
  ['COURSE', 'ENROLLMENT', '||--o{', 'receives', 'Записи на курс'],
  ['SEMESTER', 'ENROLLMENT', '||--o{', 'for', 'В каком семестре'],
  ['STUDENT', 'ATTENDANCE', '||--o{', 'recorded at', 'Посещаемость студента'],
  ['LESSON', 'ATTENDANCE', '||--o{', 'tracks', 'Посещаемость по занятию'],
  ['COURSE', 'ASSIGNMENT', '||--o{', 'assigns', 'Задания курса'],
  ['ASSIGNMENT', 'SUBMISSION', '||--o{', 'answered by', 'Сдачи по заданию'],
  ['STUDENT', 'SUBMISSION', '||--o{', 'submits', 'Сдачи студента'],
  ['TEACHER', 'SUBMISSION', '||--o{', 'grades', 'Кто проверяет сдачу'],
  ['ENROLLMENT', 'COURSE_GRADE', '||--||', 'results in', 'Одна запись — одна итоговая оценка'],
  ['TEACHER', 'COURSE_GRADE', '||--o{', 'issues', 'Кто выставил оценку'],
];

// ---------- Построение текста диаграммы из данных (erd-005: accTitle/accDescr) ----------
function buildDiagramSource() {
  const lines = ['erDiagram'];
  lines.push('  accTitle: ER-диаграмма университетской модели курсов');
  lines.push('  accDescr: 13 таблиц и 21 связь — кафедры, преподаватели, студенты, курсы, занятия, посещаемость, задания и оценки.');
  for (const e of ENTITIES) {
    lines.push(`  ${e.name} {`);
    for (const [n, t, k] of e.fields) {
      lines.push(`    ${t} ${n}${k ? ' ' + k : ''}`);
    }
    lines.push('  }');
  }
  lines.push('');
  for (const [from, to, card, label] of RELATIONS) {
    lines.push(`  ${from} ${card} ${to} : "${label}"`);
  }
  return lines.join('\n');
}

// ---------- Тема (erd-009: живой listener + ручной переключатель) ----------
function isDarkNow() {
  return document.documentElement.getAttribute('data-bs-theme') === 'dark';
}

function applyThemeAttr(isDark) {
  document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
  const btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.textContent = isDark ? 'Светлая тема' : 'Тёмная тема';
    btn.setAttribute('aria-pressed', String(isDark));
  }
}

function initTheme() {
  // Начальное значение уже выставлено инлайн-скриптом в <head> (чтобы не мигало неверной темой).
  applyThemeAttr(isDarkNow());

  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    applyThemeAttr(e.matches);
    renderDiagram(); // цвета зашиты в SVG на момент рендера — при смене темы нужен перерендер
  });

  document.getElementById('theme-toggle')?.addEventListener('click', () => {
    applyThemeAttr(!isDarkNow());
    renderDiagram();
  });
}

// ---------- Состояния UI (erd-003/erd-004: загрузка / готово / ошибка) ----------
function showLoading() {
  document.getElementById('erd-status')?.classList.remove('d-none');
  document.getElementById('erd-error')?.classList.add('d-none');
  document.getElementById('erd')?.classList.add('d-none');
}
function showDiagram() {
  document.getElementById('erd-status')?.classList.add('d-none');
  document.getElementById('erd-error')?.classList.add('d-none');
  document.getElementById('erd')?.classList.remove('d-none');
}
function showError(err) {
  document.getElementById('erd-status')?.classList.add('d-none');
  document.getElementById('erd')?.classList.add('d-none');
  document.getElementById('erd-error')?.classList.remove('d-none');
  const msg = document.getElementById('erd-error-message');
  if (msg) {
    msg.textContent = 'Техническая причина: ' + (err && err.message ? err.message : String(err));
  }
}

// ---------- Пост-обработка SVG (без изменений от исходного файла) ----------
function postProcessSvg(container) {
  container.querySelectorAll('.node').forEach((node) => {
    const firstPath = node.querySelector('path[d]');
    if (!firstPath) return;
    const d = firstPath.getAttribute('d');
    const nums = d.match(/-?[\d.]+/g)?.map(Number);
    if (!nums || nums.length < 8) return;
    const xs = [nums[0], nums[2], nums[4], nums[6]];
    const ys = [nums[1], nums[3], nums[5], nums[7]];
    const x = Math.min(...xs), y = Math.min(...ys);
    const w = Math.max(...xs) - x, h = Math.max(...ys) - y;
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x); rect.setAttribute('y', y);
    rect.setAttribute('width', w); rect.setAttribute('height', h);
    rect.setAttribute('rx', '8');
    for (const a of ['fill', 'stroke', 'stroke-width', 'class', 'style']) {
      if (firstPath.hasAttribute(a)) rect.setAttribute(a, firstPath.getAttribute(a));
    }
    firstPath.replaceWith(rect);
  });
  container.querySelectorAll('.row-rect-odd path, .row-rect-even path').forEach((p) => {
    p.setAttribute('stroke', 'none');
  });
}

// ---------- Рендер (erd-003: динамический import вместо статического — ловится try/catch) ----------
let renderToken = 0;

async function renderDiagram() {
  const myToken = ++renderToken;
  showLoading();
  try {
    await document.fonts.ready;
    const { default: mermaid } = await import('https://esm.sh/mermaid@11/dist/mermaid.esm.min.mjs');
    if (myToken !== renderToken) return; // тему/повтор успели нажать ещё раз — эта попытка устарела

    const dark = isDarkNow();
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      fontFamily: '"Anthropic Sans", sans-serif',
      themeVariables: {
        darkMode: dark,
        fontSize: '12px',
        fontFamily: '"Anthropic Sans", sans-serif',
        lineColor: dark ? '#9c9a92' : '#73726c',
        textColor: dark ? '#c2c0b6' : '#3d3d3a',
        primaryColor: dark ? '#3C3489' : '#EEEDFE',
        primaryBorderColor: dark ? '#AFA9EC' : '#7F77DD',
        primaryTextColor: dark ? '#EEEDFE' : '#26215C',
        secondaryColor: dark ? '#085041' : '#E1F5EE',
        secondaryBorderColor: dark ? '#5DCAA5' : '#0F6E56',
        secondaryTextColor: dark ? '#E1F5EE' : '#04342C',
        tertiaryColor: dark ? '#3B6D11' : '#EAF3DE',
        tertiaryBorderColor: dark ? '#97C459' : '#3B6D11',
        tertiaryTextColor: dark ? '#EAF3DE' : '#173404',
      },
    });

    const { svg } = await mermaid.render('erd-svg', buildDiagramSource());
    if (myToken !== renderToken) return;

    const erd = document.getElementById('erd');
    erd.innerHTML = svg;
    postProcessSvg(erd);
    showDiagram();
  } catch (err) {
    if (myToken !== renderToken) return;
    console.error('ERD render failed:', err);
    showError(err);
  }
}

// ---------- Доступная таблица (erd-006) — не зависит от успеха рендера диаграммы ----------
function keyBadge(k) {
  if (!k) return '';
  const cls = k === 'PK' ? 'text-bg-primary' : k === 'FK' ? 'text-bg-secondary' : 'text-bg-info';
  return `<span class="badge ${cls}">${k}</span>`;
}

function renderAccessibleTable() {
  const entBody = document.getElementById('erd-entities-body');
  if (entBody) {
    entBody.innerHTML = ENTITIES.flatMap((e) =>
      e.fields.map(([n, t, k]) => `<tr><td>${e.name}</td><td>${n}</td><td>${t}</td><td>${keyBadge(k)}</td></tr>`)
    ).join('');
  }
  const relBody = document.getElementById('erd-relations-body');
  if (relBody) {
    relBody.innerHTML = RELATIONS.map(([from, to, , label, ru]) =>
      `<tr><td>${from}</td><td>${to}</td><td>${label}</td><td>${ru}</td></tr>`
    ).join('');
  }
}

// ---------- Инициализация ----------
document.getElementById('erd-retry')?.addEventListener('click', renderDiagram);

initTheme();
renderAccessibleTable();
renderDiagram();
