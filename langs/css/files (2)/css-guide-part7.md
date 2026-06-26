# PART VII — CSS: SPECIALTY COMPONENTS & COMPLETE REFERENCE

---

## 117. TREE VIEW / FILE SYSTEM

```css
/* ─── File tree component ─── */
.tree {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  line-height: 1.6;
  user-select: none;
}

.tree-node {
  position: relative;
}

/* Connecting lines */
.tree-node::before {
  content: '';
  position: absolute;
  inset-inline-start: -1.25rem;
  inset-block-start: 0;
  bottom: 50%;
  width: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.tree-node:last-child::after {
  content: '';
  position: absolute;
  inset-inline-start: -1.25rem;
  top: 50%;
  bottom: 0;
  border-left: 1px solid var(--color-bg-subtle); /* hide vertical line */
  background: var(--color-surface);
  width: 2px;
}

.tree-children {
  padding-inline-start: 1.5rem;
  border-inline-start: 1px solid var(--color-border);
  margin-inline-start: 0.5rem;
}

/* Node row */
.tree-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--duration-fast);
  min-height: 1.75rem;
}

.tree-row:hover { background: var(--color-bg-subtle); }
.tree-row.selected {
  background: color-mix(in srgb, var(--color-accent) 12%, transparent);
  color: var(--color-accent);
}
.tree-row.focused {
  outline: 2px solid var(--color-accent);
  outline-offset: -2px;
}

/* Toggle arrow */
.tree-toggle {
  width: 1rem;
  height: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  flex-shrink: 0;
  transition: rotate var(--duration-fast) var(--ease-out);
  font-size: 0.6rem;
}
.tree-toggle::before { content: '▶'; }
.tree-node.open > .tree-row .tree-toggle { rotate: 90deg; }
.tree-node--leaf > .tree-row .tree-toggle { visibility: hidden; }

/* File type icon */
.tree-icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
  font-size: 0.875rem;
}

/* File-type colors */
.tree-icon--folder   { color: var(--color-warning-500); }
.tree-icon--js       { color: #f7df1e; }
.tree-icon--ts       { color: #3178c6; }
.tree-icon--css      { color: #1572b6; }
.tree-icon--html     { color: #e34f26; }
.tree-icon--json     { color: var(--color-success-500); }
.tree-icon--md       { color: var(--color-neutral-500); }
.tree-icon--image    { color: var(--color-brand-400); }
.tree-icon--svg      { color: oklch(0.7 0.2 30); }
.tree-icon--git      { color: oklch(0.5 0.15 30); }

.tree-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* File name rename input */
.tree-label--editing {
  background: var(--color-surface);
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-sm);
  padding: 0 0.25rem;
  outline: none;
  font: inherit;
  width: 100%;
}

/* Context menu indicator */
.tree-row:hover::after {
  content: '···';
  margin-inline-start: auto;
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
}

/* Drag/drop */
.tree-row.drag-over {
  background: color-mix(in srgb, var(--color-accent) 15%, transparent);
  outline: 1px dashed var(--color-accent);
}

/* Search highlight */
.tree-label mark {
  background: var(--color-warning-200);
  color: var(--color-warning-900);
  border-radius: 2px;
}

/* Hidden files */
.tree-node--hidden > .tree-row .tree-label { opacity: 0.5; font-style: italic; }

/* Modified indicator */
.tree-node--modified > .tree-row .tree-label::after {
  content: '●';
  color: var(--color-warning-500);
  font-size: 0.5em;
  vertical-align: super;
  margin-inline-start: 0.25em;
}
```

---

## 118. AI / CHATBOT UI

```css
/* ─── AI Assistant interface ─── */
.ai-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--color-bg-subtle);
}

/* Message threads */
.ai-thread {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  max-width: 800px;
  margin-inline: auto;
  width: 100%;
  scroll-behavior: smooth;
}

/* User message */
.ai-msg--user {
  align-self: flex-end;
  display: flex;
  align-items: flex-end;
  gap: var(--space-3);
  max-width: 75%;
  animation: msg-in-right 0.2s var(--ease-out);
}

@keyframes msg-in-right {
  from { opacity: 0; translate: 16px 0; }
}

.ai-msg--user .ai-bubble {
  background: var(--color-accent);
  color: white;
  border-radius: var(--radius-2xl) var(--radius-2xl) var(--radius-sm) var(--radius-2xl);
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-sm);
  line-height: 1.6;
  word-break: break-word;
}

/* AI message */
.ai-msg--assistant {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  animation: msg-in-left 0.2s var(--ease-out);
}

@keyframes msg-in-left {
  from { opacity: 0; translate: -16px 0; }
}

.ai-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, oklch(0.6 0.25 280), oklch(0.6 0.25 200));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
  margin-block-start: 0.25rem;
}

.ai-msg--assistant .ai-bubble {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm) var(--radius-2xl) var(--radius-2xl) var(--radius-2xl);
  padding: var(--space-4) var(--space-5);
  font-size: var(--font-size-sm);
  line-height: 1.7;
  max-width: calc(100% - 2.75rem);
  box-shadow: var(--shadow-sm);
}

/* Streaming text cursor */
.ai-bubble--streaming::after {
  content: '▋';
  animation: cursor-blink 0.7s step-end infinite;
  color: var(--color-accent);
  margin-inline-start: 0.1em;
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* AI thinking / processing */
.ai-thinking {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  animation: msg-in-left 0.2s var(--ease-out);
}

.ai-thinking-bubble {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm) var(--radius-2xl) var(--radius-2xl) var(--radius-2xl);
  padding: var(--space-3) var(--space-4);
  display: flex;
  gap: 4px;
  align-items: center;
}

.ai-thinking-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--color-text-muted);
  animation: thinking 1.4s ease-in-out infinite;
}
.ai-thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.ai-thinking-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes thinking {
  0%, 60%, 100% { scale: 0.6; opacity: 0.4; }
  30%           { scale: 1;   opacity: 1; }
}

/* Code blocks in AI responses */
.ai-bubble pre {
  background: var(--color-neutral-900);
  color: var(--color-neutral-100);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  overflow-x: auto;
  margin-block: var(--space-3);
  font-size: 0.8125rem;
  line-height: 1.7;
  position: relative;
}

.ai-bubble pre .copy-btn {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  padding: 0.25rem 0.625rem;
  background: rgba(255 255 255 / 0.1);
  border: 1px solid rgba(255 255 255 / 0.15);
  border-radius: var(--radius-md);
  color: rgba(255 255 255 / 0.7);
  font-size: 0.6875rem;
  cursor: pointer;
  transition: background var(--duration-fast);
}
.ai-bubble pre .copy-btn:hover { background: rgba(255 255 255 / 0.2); }

/* Action buttons below AI message */
.ai-actions {
  display: flex;
  gap: var(--space-2);
  margin-block-start: var(--space-2);
  padding-inline-start: 2.75rem;
}

.ai-action-btn {
  padding: 0.25rem 0.625rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.ai-action-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

/* AI Input area */
.ai-input-area {
  padding: var(--space-4);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
}

.ai-input-wrapper {
  max-width: 800px;
  margin-inline: auto;
  position: relative;
}

.ai-input {
  width: 100%;
  padding: 0.875rem 3.5rem 0.875rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  background: var(--color-surface);
  font: inherit;
  font-size: var(--font-size-sm);
  resize: none;
  outline: none;
  max-height: 200px;
  overflow-y: auto;
  line-height: 1.5;
  box-shadow: var(--shadow-sm);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}

.ai-input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

.ai-send-btn {
  position: absolute;
  bottom: 0.625rem;
  right: 0.625rem;
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-lg);
  background: var(--color-accent);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
}
.ai-send-btn:hover { background: var(--color-accent-hover); scale: 1.05; }
.ai-send-btn:disabled { opacity: 0.4; cursor: not-allowed; scale: 1; }

/* Suggestion chips */
.ai-suggestions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  max-width: 800px;
  margin-inline: auto;
  margin-block-end: var(--space-3);
}

.ai-suggestion {
  padding: 0.4rem 0.875rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface);
  font-size: var(--font-size-xs);
  cursor: pointer;
  color: var(--color-text-muted);
  transition: background var(--duration-fast), border-color var(--duration-fast), color var(--duration-fast);
  white-space: nowrap;
}
.ai-suggestion:hover {
  background: var(--color-bg-subtle);
  border-color: var(--color-accent);
  color: var(--color-accent);
}
```

---

## 119. SETTINGS / PREFERENCES PAGE

```css
/* ─── Settings layout ─── */
.settings-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 0;
  min-height: calc(100dvh - var(--header-height, 60px));
}

@media (max-width: 768px) {
  .settings-layout { grid-template-columns: 1fr; }
  .settings-nav { display: none; }
}

/* Settings sidebar nav */
.settings-nav {
  border-right: 1px solid var(--color-border);
  padding: var(--space-4);
  position: sticky;
  top: var(--header-height, 60px);
  height: calc(100dvh - var(--header-height, 60px));
  overflow-y: auto;
}

.settings-nav__section {
  margin-block-end: var(--space-4);
}

.settings-nav__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  padding: 0.25rem var(--space-3);
  margin-block-end: var(--space-1);
}

.settings-nav__link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.5rem var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  text-decoration: none;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.settings-nav__link:hover { background: var(--color-bg-subtle); color: var(--color-text); }
.settings-nav__link.active {
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  color: var(--color-accent);
  font-weight: var(--font-weight-medium);
}

/* Settings main content */
.settings-content {
  padding: var(--space-8);
  max-width: 660px;
}

/* Settings section */
.settings-section {
  margin-block-end: var(--space-10);
  padding-block-end: var(--space-10);
  border-bottom: 1px solid var(--color-border);
}
.settings-section:last-child { border: none; }

.settings-section__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-semibold);
  margin-block-end: var(--space-1);
}

.settings-section__desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-block-end: var(--space-6);
}

/* Setting row */
.setting-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-6);
  padding-block: var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
.setting-row:last-child { border: none; }

.setting-row__info { flex: 1; min-width: 0; }

.setting-row__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  margin-block-end: var(--space-1);
}

.setting-row__desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  line-height: 1.5;
}

.setting-row__control { flex-shrink: 0; }

/* Danger zone */
.settings-danger {
  border: 1px solid var(--color-danger-200);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  background: var(--color-danger-100);
}

.settings-danger__title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-danger-700);
  margin-block-end: var(--space-1);
}

/* Settings search */
.settings-search {
  position: relative;
  margin-block-end: var(--space-6);
}

.settings-search__input {
  width: 100%;
  padding: 0.5rem 0.75rem 0.5rem 2.25rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font: inherit;
  font-size: var(--font-size-sm);
  background: var(--color-surface);
  outline: none;
  transition: border-color var(--duration-fast);
}
.settings-search__input:focus { border-color: var(--color-accent); }

.settings-search__icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  translate: 0 -50%;
  color: var(--color-text-muted);
  pointer-events: none;
}
```

---

## 120. PROFILE PAGE

```css
/* ─── Profile hero ─── */
.profile-hero {
  position: relative;
}

.profile-cover {
  height: 200px;
  background: linear-gradient(
    135deg,
    var(--color-brand-600),
    var(--color-brand-400)
  );
  border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
  overflow: hidden;
}

.profile-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Cover edit button */
.profile-cover__edit {
  position: absolute;
  bottom: var(--space-3);
  right: var(--space-3);
  padding: 0.375rem 0.75rem;
  background: rgba(0 0 0 / 0.5);
  color: white;
  border: 1px solid rgba(255 255 255 / 0.3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-xs);
  cursor: pointer;
  backdrop-filter: blur(4px);
  opacity: 0;
  transition: opacity var(--duration-fast);
}
.profile-cover:hover .profile-cover__edit { opacity: 1; }

/* Avatar row */
.profile-avatar-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 0 var(--space-6) var(--space-4);
  margin-block-start: -3rem;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.profile-avatar {
  width: 6rem;
  height: 6rem;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--color-surface);
  box-shadow: var(--shadow-md);
  background: var(--color-bg-muted);
  flex-shrink: 0;
  position: relative;
}

.profile-avatar__edit {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  border: 2px solid var(--color-surface);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.profile-actions {
  display: flex;
  gap: var(--space-2);
  align-items: center;
  padding-block-end: 0.25rem;
}

/* Profile info */
.profile-info {
  padding: var(--space-4) var(--space-6) var(--space-6);
}

.profile-name {
  font-size: var(--step-2);
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Verified badge */
.verified-badge {
  color: var(--color-brand-500);
  font-size: 1.25rem;
  flex-shrink: 0;
}

.profile-handle {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  margin-block-end: var(--space-3);
}

.profile-bio {
  font-size: var(--font-size-sm);
  line-height: 1.6;
  max-width: 55ch;
  margin-block-end: var(--space-4);
}

/* Profile meta row */
.profile-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-block-end: var(--space-4);
}

.profile-meta__item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.profile-meta__item a {
  color: var(--color-accent);
  text-decoration: none;
}
.profile-meta__item a:hover { text-decoration: underline; }

/* Follow stats */
.profile-stats {
  display: flex;
  gap: var(--space-6);
  font-size: var(--font-size-sm);
}

.profile-stat {
  display: flex;
  align-items: baseline;
  gap: 0.375rem;
  cursor: pointer;
}

.profile-stat__count {
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}

.profile-stat__label { color: var(--color-text-muted); }

/* Profile tabs */
.profile-tabs {
  border-bottom: 1px solid var(--color-border);
  display: flex;
  overflow-x: auto;
  scrollbar-width: none;
  position: sticky;
  top: var(--header-height, 0);
  background: var(--color-surface);
  z-index: var(--z-sticky);
}
.profile-tabs::-webkit-scrollbar { display: none; }

.profile-tab {
  padding: 0.875rem 1.25rem;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  text-decoration: none;
  white-space: nowrap;
  border-bottom: 2px solid transparent;
  transition: color var(--duration-fast), border-color var(--duration-fast);
}
.profile-tab:hover { color: var(--color-text); }
.profile-tab.active {
  color: var(--color-text);
  border-bottom-color: var(--color-text);
}
```

---

## 121. ORG CHART

```css
/* ─── Organizational chart ─── */
.org-chart {
  overflow: auto;
  padding: var(--space-8);
}

.org-tree {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

/* Level */
.org-level {
  display: flex;
  justify-content: center;
  gap: 0;
  position: relative;
}

/* Horizontal connector */
.org-level::before {
  content: '';
  position: absolute;
  top: 0;
  height: 1px;
  background: var(--color-border);
  left: calc(50% / var(--items, 1));
  right: calc(50% / var(--items, 1));
}

/* Vertical connector to parent */
.org-level::after {
  content: '';
  position: absolute;
  top: -2rem;
  left: 50%;
  height: 2rem;
  width: 1px;
  background: var(--color-border);
}

.org-level:first-child::after { display: none; }

/* Node */
.org-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 var(--space-4);
  position: relative;
}

/* Vertical line down to children */
.org-node::after {
  content: '';
  position: absolute;
  bottom: -2rem;
  left: 50%;
  height: 2rem;
  width: 1px;
  background: var(--color-border);
}

.org-node:only-child::after { display: none; }
.org-level:last-child .org-node::after { display: none; }

/* Card */
.org-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-3) var(--space-4);
  min-width: 160px;
  text-align: center;
  margin-block-end: 2rem;
  cursor: pointer;
  transition:
    box-shadow var(--duration-fast),
    border-color var(--duration-fast),
    scale var(--duration-fast) var(--ease-bounce);
  box-shadow: var(--shadow-sm);
}

.org-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-accent);
  scale: 1.02;
}

.org-card.highlighted {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 5%, var(--color-surface));
}

.org-card__avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  object-fit: cover;
  margin-inline: auto;
  margin-block-end: var(--space-2);
  border: 2px solid var(--color-border);
}

.org-card__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  line-height: 1.3;
}

.org-card__title {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-block-start: var(--space-1);
}

.org-card__dept {
  display: inline-flex;
  margin-block-start: var(--space-2);
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-size: 0.625rem;
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--dept-color, var(--color-bg-muted));
  color: white;
}

/* Department colors */
.org-card[data-dept="engineering"] { --dept-color: var(--color-brand-600); }
.org-card[data-dept="design"]      { --dept-color: oklch(0.55 0.22 310); }
.org-card[data-dept="product"]     { --dept-color: var(--color-success-600); }
.org-card[data-dept="hr"]          { --dept-color: var(--color-warning-600); }
.org-card[data-dept="finance"]     { --dept-color: oklch(0.45 0.1 250); }
```

---

## 122. FEATURE COMPARISON MATRIX

```css
/* ─── Feature / Pricing comparison matrix ─── */
.comparison-matrix {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border);
}

.matrix-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

/* Sticky header column */
.matrix-table th:first-child,
.matrix-table td:first-child {
  position: sticky;
  left: 0;
  background: var(--color-surface);
  z-index: 2;
  box-shadow: 1px 0 0 var(--color-border);
}

/* Plan headers */
.matrix-table thead tr:first-child th {
  padding: var(--space-6) var(--space-4);
  text-align: center;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  position: sticky;
  top: 0;
  z-index: 3;
}

/* Featured plan column */
.matrix-col--featured {
  background: color-mix(in srgb, var(--color-accent) 4%, var(--color-surface));
}

.plan-header__badge {
  display: inline-flex;
  padding: 0.2em 0.6em;
  background: var(--color-accent);
  color: white;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  border-radius: var(--radius-full);
  margin-block-end: var(--space-2);
}

.plan-header__name {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
}

.plan-header__price {
  font-size: var(--step-2);
  font-weight: var(--font-weight-black);
  color: var(--color-text);
  margin-block: var(--space-2);
}

.plan-header__period {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-normal);
  color: var(--color-text-muted);
}

/* Category rows */
.matrix-category {
  background: var(--color-bg-subtle);
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

/* Feature rows */
.matrix-table tbody tr:not(.matrix-category-row) td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
  text-align: center;
  vertical-align: middle;
}

.matrix-table tbody tr:not(.matrix-category-row) td:first-child {
  text-align: start;
  color: var(--color-text);
}

.matrix-table tbody tr:hover td {
  background: var(--color-bg-subtle);
}
.matrix-table tbody tr:hover .matrix-col--featured {
  background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface));
}

/* Check / X icons */
.check { color: var(--color-success-500); font-size: 1.1em; }
.cross  { color: var(--color-neutral-400); font-size: 1.1em; }
.partial {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25em;
  height: 1.25em;
  border-radius: 50%;
  background: var(--color-warning-100);
  color: var(--color-warning-700);
  font-size: 0.75em;
  font-weight: bold;
}
```

---

## 123. CLIP-PATH ANIMATIONS

```css
/* ─── Reveal effects via clip-path ─── */

/* 1. Curtain reveal (left to right) */
.clip-curtain {
  clip-path: inset(0 100% 0 0);
  animation: curtain-open 0.6s var(--ease-out) forwards;
}
@keyframes curtain-open {
  to { clip-path: inset(0 0% 0 0); }
}

/* 2. Circle expand */
.clip-circle-in {
  clip-path: circle(0% at 50% 50%);
  animation: circle-in 0.5s var(--ease-out) forwards;
}
@keyframes circle-in {
  to { clip-path: circle(150% at 50% 50%); }
}

/* 3. Circle from corner */
.clip-circle-corner {
  clip-path: circle(0% at 0% 0%);
  animation: circle-corner 0.6s var(--ease-out) forwards;
}
@keyframes circle-corner {
  to { clip-path: circle(200% at 0% 0%); }
}

/* 4. Wipe from bottom */
.clip-wipe-up {
  clip-path: inset(100% 0 0 0);
  animation: wipe-up 0.5s var(--ease-out) forwards;
}
@keyframes wipe-up {
  to { clip-path: inset(0% 0 0 0); }
}

/* 5. Diamond reveal */
.clip-diamond {
  clip-path: polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%);
  animation: diamond-reveal 0.6s var(--ease-out) forwards;
}
@keyframes diamond-reveal {
  to { clip-path: polygon(50% -50%, 150% 50%, 50% 150%, -50% 50%); }
}

/* 6. Diagonal swipe */
.clip-diagonal {
  clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);
  animation: diagonal-swipe 0.5s var(--ease-out) forwards;
}
@keyframes diagonal-swipe {
  to { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
}

/* 7. Iris (center expand like camera) */
.clip-iris {
  clip-path: polygon(
    50% 50%, 50% 50%, 50% 50%, 50% 50%,
    50% 50%, 50% 50%, 50% 50%, 50% 50%
  );
  animation: iris-open 0.5s var(--ease-out) forwards;
}
@keyframes iris-open {
  to {
    clip-path: polygon(
      0% 0%, 100% 0%, 100% 100%, 0% 100%
    );
  }
}

/* 8. Morphing blob on hover */
.clip-blob {
  clip-path: polygon(25% 5%, 75% 5%, 95% 25%, 95% 75%, 75% 95%, 25% 95%, 5% 75%, 5% 25%);
  transition: clip-path 0.4s var(--ease-out);
}
.clip-blob:hover {
  clip-path: polygon(50% 0%, 90% 20%, 100% 60%, 75% 100%, 25% 100%, 0% 60%, 10% 20%, 50% 0%);
}

/* 9. Text reveal via parent clip */
.text-reveal-wrapper {
  overflow: hidden;
}
.text-reveal-line {
  translate: 0 100%;
  animation: line-slide-up 0.5s var(--ease-out) forwards;
  animation-delay: calc(var(--line, 0) * 80ms);
}
@keyframes line-slide-up {
  to { translate: 0 0; }
}

/* 10. Scroll-driven clip-path */
.scroll-clip {
  clip-path: inset(20% 10%);
  animation: expand-clip linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 60%;
}
@keyframes expand-clip {
  to { clip-path: inset(0% 0%); }
}
```

---

## 124. COOKIE CONSENT & LEGAL UI

```css
/* ─── Cookie consent banner ─── */
.cookie-banner {
  position: fixed;
  inset-block-end: var(--space-4);
  inset-inline: var(--space-4);
  max-width: 420px;
  background: var(--color-neutral-900);
  color: var(--color-neutral-100);
  border-radius: var(--radius-2xl);
  padding: var(--space-5);
  z-index: var(--z-toast);
  box-shadow: var(--shadow-2xl);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);

  animation: banner-slide-in 0.4s var(--ease-bounce);
}

@keyframes banner-slide-in {
  from { translate: 0 120%; opacity: 0; }
}

.cookie-banner.dismissing {
  animation: banner-slide-out 0.3s var(--ease-in) forwards;
}

@keyframes banner-slide-out {
  to { translate: 0 120%; opacity: 0; }
}

.cookie-banner__icon {
  font-size: 2rem;
}

.cookie-banner__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-base);
}

.cookie-banner__text {
  font-size: var(--font-size-sm);
  color: var(--color-neutral-400);
  line-height: 1.6;
}

.cookie-banner__text a {
  color: var(--color-neutral-300);
  text-decoration: underline;
}

.cookie-banner__actions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.cookie-btn {
  flex: 1;
  padding: 0.625rem 1rem;
  border-radius: var(--radius-lg);
  font: inherit;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  border: 1px solid transparent;
  white-space: nowrap;
}

.cookie-btn--accept {
  background: var(--color-accent);
  color: white;
  border-color: var(--color-accent);
}
.cookie-btn--accept:hover { background: var(--color-accent-hover); }

.cookie-btn--decline {
  background: transparent;
  color: var(--color-neutral-400);
  border-color: var(--color-neutral-600);
}
.cookie-btn--decline:hover { background: var(--color-neutral-800); color: var(--color-neutral-200); }

.cookie-btn--customize {
  width: 100%;
  background: transparent;
  color: var(--color-neutral-400);
  font-size: var(--font-size-xs);
  text-decoration: underline;
  flex: none;
}

/* ─── Cookie preferences modal ─── */
.cookie-preferences {
  padding: var(--space-6);
  max-width: 560px;
}

.cookie-category {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  padding-block: var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
.cookie-category:last-child { border: none; }

.cookie-category__info { flex: 1; }
.cookie-category__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  margin-block-end: var(--space-1);
}
.cookie-category__desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  line-height: 1.5;
}

.cookie-required-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-style: italic;
  align-self: center;
}

/* ─── Terms / Privacy page ─── */
.legal-page {
  max-width: 720px;
  margin-inline: auto;
  padding: var(--space-8);
}

.legal-page h1 {
  font-size: var(--step-3);
  font-weight: var(--font-weight-black);
  margin-block-end: var(--space-2);
}

.legal-meta {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-block-end: var(--space-8);
  padding-block-end: var(--space-8);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  gap: var(--space-6);
}
```

---

## 125. GAMIFICATION COMPONENTS

```css
/* ─── Leaderboard ─── */
.leaderboard {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.leaderboard-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  transition:
    box-shadow var(--duration-fast),
    translate  var(--duration-fast);
  animation: rank-in 0.4s var(--ease-out) backwards;
  animation-delay: calc(var(--rank, 0) * 60ms);
}

@keyframes rank-in {
  from { opacity: 0; translate: -20px 0; }
}

.leaderboard-item:hover {
  box-shadow: var(--shadow-md);
  translate: 2px 0;
}

/* Top 3 special styling */
.leaderboard-item:nth-child(1) { border-color: #FFD700; background: linear-gradient(to right, #fffde7, var(--color-surface)); }
.leaderboard-item:nth-child(2) { border-color: #C0C0C0; background: linear-gradient(to right, #f5f5f5, var(--color-surface)); }
.leaderboard-item:nth-child(3) { border-color: #CD7F32; background: linear-gradient(to right, #fff8f0, var(--color-surface)); }

/* Rank badge */
.rank-badge {
  min-width: 2rem;
  height: 2rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-black);
  font-size: var(--font-size-sm);
  flex-shrink: 0;
  font-variant-numeric: tabular-nums;
}

.rank-badge--1 { background: #FFD700; color: #7a5c00; }
.rank-badge--2 { background: #C0C0C0; color: #555; }
.rank-badge--3 { background: #CD7F32; color: #fff; }
.rank-badge--n { background: var(--color-bg-muted); color: var(--color-text-muted); }

.leaderboard-item__info { flex: 1; min-width: 0; }
.leaderboard-item__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.leaderboard-item__sub { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.leaderboard-item__score {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
  color: var(--color-text);
  flex-shrink: 0;
}

.leaderboard-item__change {
  font-size: var(--font-size-xs);
  flex-shrink: 0;
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  gap: 0.2em;
}
.leaderboard-item__change--up   { color: var(--color-success-500); }
.leaderboard-item__change--down { color: var(--color-danger-500); }
.leaderboard-item__change--same { color: var(--color-text-muted); }

/* ─── Achievement badge ─── */
.achievement {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  text-align: center;
  transition: scale var(--duration-fast) var(--ease-bounce);
  position: relative;
  overflow: hidden;
}

.achievement:hover { scale: 1.03; }

.achievement.locked {
  opacity: 0.4;
  filter: grayscale(100%);
}

.achievement.newly-unlocked {
  animation: achievement-unlock 0.6s var(--ease-bounce);
  border-color: var(--color-warning-400);
}

@keyframes achievement-unlock {
  0%   { scale: 0.5; rotate: -10deg; opacity: 0; }
  60%  { scale: 1.15; rotate: 5deg; }
  100% { scale: 1; rotate: 0deg; opacity: 1; }
}

.achievement__icon {
  font-size: 2.5rem;
  line-height: 1;
}

.achievement__name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  line-height: 1.3;
}

.achievement__desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

/* Shine on unlock */
.achievement.newly-unlocked::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    transparent 30%,
    rgba(255 255 255 / 0.5) 50%,
    transparent 70%
  );
  animation: achievement-shine 0.8s ease-out;
}

@keyframes achievement-shine {
  from { translate: -100% -100%; }
  to   { translate: 100% 100%; }
}

/* ─── XP / Level progress ─── */
.xp-bar {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.xp-bar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.xp-level {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.xp-level__badge {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-warning-400), var(--color-warning-600));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-black);
  font-size: var(--font-size-sm);
  box-shadow: 0 0 0 3px var(--color-warning-200);
}

.xp-level__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
}

.xp-bar__track {
  height: 8px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.xp-bar__fill {
  height: 100%;
  background: linear-gradient(to right, var(--color-warning-400), var(--color-warning-600));
  border-radius: inherit;
  width: var(--xp-pct, 0%);
  transition: width 1s var(--ease-out);
  position: relative;
  overflow: hidden;
}

/* Animated sheen on XP bar */
.xp-bar__fill::after {
  content: '';
  position: absolute;
  inset-block: 0;
  width: 50%;
  background: linear-gradient(to right, transparent, rgba(255 255 255 / 0.4), transparent);
  animation: xp-sheen 2s ease-in-out infinite;
}

@keyframes xp-sheen {
  from { translate: -200% 0; }
  to   { translate: 400% 0; }
}

.xp-bar__numbers {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}
```

---

## 126. SURVEY / QUESTIONNAIRE UI

```css
/* ─── Survey container ─── */
.survey {
  max-width: 640px;
  margin-inline: auto;
  padding: var(--space-8) var(--space-4);
}

.survey__progress {
  margin-block-end: var(--space-8);
}

.survey__progress-label {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-block-end: var(--space-2);
}

/* Question card */
.survey-question {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  animation: question-slide 0.3s var(--ease-out);
}

@keyframes question-slide {
  from { opacity: 0; translate: 0 20px; }
}

.survey-question__number {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-accent);
  margin-block-end: var(--space-2);
}

.survey-question__text {
  font-size: var(--step-1);
  font-weight: var(--font-weight-semibold);
  line-height: 1.4;
  margin-block-end: var(--space-6);
  text-wrap: balance;
}

.survey-question__sub {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-block-start: -var(--space-4);
  margin-block-end: var(--space-6);
}

/* Answer options */
.survey-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.survey-option {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast),
    scale        var(--duration-fast) var(--ease-bounce);
  user-select: none;
}

.survey-option:hover {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 4%, transparent);
}

.survey-option input { display: none; }

.survey-option__indicator {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  flex-shrink: 0;
  transition: border-color var(--duration-fast), background var(--duration-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.survey-option:has(input:checked) {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
  scale: 1.01;
}

.survey-option:has(input:checked) .survey-option__indicator {
  border-color: var(--color-accent);
  background: var(--color-accent);
}

.survey-option:has(input:checked) .survey-option__indicator::after {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
}

.survey-option__emoji { font-size: 1.5rem; flex-shrink: 0; }
.survey-option__text  { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.survey-option__desc  { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* NPS scale */
.nps-scale {
  display: flex;
  gap: var(--space-1);
  justify-content: center;
  flex-wrap: wrap;
}

.nps-btn {
  width: 3rem;
  height: 3rem;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  cursor: pointer;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  font-variant-numeric: tabular-nums;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast),
    scale        var(--duration-fast) var(--ease-bounce);
}

.nps-btn:hover { border-color: var(--color-accent); scale: 1.05; }
.nps-btn.selected { background: var(--color-accent); border-color: var(--color-accent); color: white; scale: 1.1; }

/* NPS color coding */
.nps-btn:nth-child(-n+6)  { --hover-tint: var(--color-danger-100); }
.nps-btn:nth-child(n+7):nth-child(-n+8) { --hover-tint: var(--color-warning-100); }
.nps-btn:nth-child(n+9)   { --hover-tint: var(--color-success-100); }

.nps-labels {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-block-start: var(--space-2);
}
```

---

## 127. CSS SHORTHAND PROPERTIES — COMPLETE GUIDE

```css
/* ─── Every important CSS shorthand ─── */

/* BORDER */
border: 2px solid red;
/* Expands to: border-width border-style border-color */
/* Sides: border-top, border-right, border-bottom, border-left */
/* Logical: border-block-start, border-inline-start */

/* BORDER-RADIUS */
border-radius: 8px;                    /* all corners */
border-radius: 8px 4px;               /* TL+BR | TR+BL */
border-radius: 8px 4px 6px;           /* TL | TR+BL | BR */
border-radius: 8px 4px 6px 2px;       /* TL TR BR BL */
border-radius: 8px / 4px;             /* horiz-radius / vert-radius */
border-radius: 8px 4px / 2px 6px;    /* TL+BR horiz | TR+BL horiz / TL+BR vert | TR+BL vert */

/* MARGIN and PADDING */
margin: 1rem;                          /* all sides */
margin: 1rem 2rem;                     /* block | inline */
margin: 1rem 2rem 3rem;               /* top | inline | bottom */
margin: 1rem 2rem 3rem 4rem;          /* top right bottom left */
/* Logical: margin-block, margin-inline, margin-block-start etc */

/* BACKGROUND */
background: url('img.jpg') center/cover no-repeat fixed;
/* Order: image position/size repeat attachment origin clip color */
background: linear-gradient(red, blue), url('img.jpg') center/cover no-repeat #fff;
/* Multiple: comma-separated layers, color only on last */

/* FONT */
font: italic bold 1.25rem/1.5 'Arial', sans-serif;
/* MUST include: size and family. Optional: style weight variant/stretch size/line-height */
font: var(--font-weight-bold) var(--font-size-base)/1.5 var(--font-sans);

/* TRANSITION */
transition: color 0.2s ease, background 0.2s ease 0.1s;
/* property duration timing-function delay */
/* Multiple: comma-separated */

/* ANIMATION */
animation: fadeIn 0.3s ease-out 0s 1 normal both running;
/* name duration timing delay count direction fill-mode play-state */

/* OUTLINE */
outline: 2px solid var(--color-accent);
/* width style color — no individual sides, no border-radius */

/* LIST-STYLE */
list-style: disc inside url('bullet.svg');
/* type position image */

/* GRID */
grid: auto / 1fr 2fr;                              /* rows / columns */
grid: "header" auto "main" 1fr "footer" auto / 1fr; /* template */

/* FLEX */
flex: 1 1 auto;   /* grow shrink basis */
flex: 1;          /* 1 1 0 */
flex: auto;       /* 1 1 auto */
flex: none;       /* 0 0 auto */

/* FLEX-FLOW */
flex-flow: row wrap;  /* direction wrap */

/* GAP */
gap: 1rem 2rem;  /* row-gap column-gap */

/* PLACE-ITEMS */
place-items: center;        /* align-items justify-items */
place-content: center;      /* align-content justify-content */
place-self: center;         /* align-self justify-self */

/* SCROLL-MARGIN / SCROLL-PADDING */
scroll-margin: 1rem;        /* all sides */
scroll-padding: 0 1rem;     /* block | inline */

/* INSET */
inset: 0;                   /* top right bottom left */
inset: 1rem 2rem;           /* block inline */
inset-block: 0;             /* top bottom */
inset-inline: 0;            /* left right */

/* OVERFLOW */
overflow: hidden auto;      /* x y — in CSS4 */

/* TEXT-DECORATION */
text-decoration: underline dotted var(--color-accent) 2px;
/* line style color thickness */

/* MASK */
mask: url('mask.png') center/cover no-repeat;
/* image position/size repeat */

/* COLUMNS (Multi-column) */
columns: 3 200px;           /* count width */

/* CONTAIN-INTRINSIC-SIZE */
contain-intrinsic-size: 0 300px;   /* inline-size block-size */

/* ANIMATION-RANGE */
animation-range: entry 0% entry 50%;  /* start end */

/* SCROLL-TIMELINE */
scroll-timeline: --name block;  /* name axis */

/* VIEW-TIMELINE */
view-timeline: --name block;

/* CONTAINER */
container: name / inline-size;   /* name type */

/* WILL-CHANGE */
/* Not a shorthand but often misused: */
will-change: transform, opacity;  /* comma-separated properties */
```

---

## 128. CSS POLYFILLS & PROGRESSIVE ENHANCEMENT

```css
/* ─── Progressive enhancement patterns ─── */

/* ── :has() fallback ── */
/* Without :has() — use JS to add class */
/* With :has() */
@supports selector(:has(*)) {
  .form:has(input:invalid) { border-color: red; }
}
/* Fallback */
.form.has-invalid { border-color: red; }

/* ── Container queries fallback ── */
@supports (container-type: inline-size) {
  .wrapper { container-type: inline-size; }
  @container (min-width: 400px) {
    .card { flex-direction: row; }
  }
}
/* Fallback: media query */
@media (min-width: 600px) {
  .card { flex-direction: row; }
}

/* ── CSS Nesting fallback ── */
/* Modern */
.parent {
  & .child { color: red; }
}
/* Compiled (PostCSS output) */
.parent .child { color: red; }

/* ── oklch() fallback ── */
.element {
  color: #3b82f6;                           /* legacy fallback */
  color: oklch(0.6 0.2 250);               /* modern */
}
/* Or via @supports */
@supports (color: oklch(0 0 0)) {
  :root { --accent: oklch(0.6 0.2 250); }
}

/* ── color-mix() fallback ── */
.el {
  background: rgba(59, 130, 246, 0.15);    /* fallback */
  background: color-mix(in srgb, var(--color-accent) 15%, transparent);
}

/* ── Scroll-Driven animations fallback ── */
@supports (animation-timeline: scroll()) {
  .progress { animation: fill linear; animation-timeline: scroll(root); }
}
/* Fallback: JS scroll handler */

/* ── View Transitions fallback ── */
/* JS: if (!document.startViewTransition) { updateDOM(); return; } */

/* ── anchor-name fallback ── */
@supports (anchor-name: --a) {
  .tooltip { position: fixed; top: anchor(bottom); }
}
/* Fallback: JS positioning */

/* ── dvh fallback ── */
.hero {
  min-height: 100vh;    /* fallback */
  min-height: 100dvh;   /* override if supported */
}

/* ── clamp() fallback ── */
.fluid-text {
  font-size: 1.5rem;                        /* fallback */
  font-size: clamp(1rem, 2vw + 0.5rem, 2rem);
}

/* ── gap in flexbox fallback ── */
.flex-gap > * + * { margin-inline-start: 1rem; } /* fallback */
@supports (gap: 1rem) {
  .flex-gap > * + * { margin-inline-start: 0; }
  .flex-gap { gap: 1rem; }
}

/* ── Logical properties fallback ── */
/* Auto-resolved by PostCSS logical plugin: */
.el {
  margin-left: 1rem;              /* fallback */
  margin-inline-start: 1rem;      /* override */
}

/* ── @layer fallback ── */
/* Browsers that don't support @layer treat everything as unlayered */
/* (normal specificity rules apply) */
/* So you can write @layer safely with no fallback needed for functionality */
/* Just don't rely on layer ordering for critical styles */

/* ── interpolate-size fallback ── */
.accordion {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s;   /* fallback */
}
.accordion.open { max-height: 2000px; }

@supports (interpolate-size: allow-keywords) {
  :root { interpolate-size: allow-keywords; }
  .accordion { max-height: none; height: 0; transition: height 0.3s; }
  .accordion.open { height: auto; }
}

/* ── text-wrap: balance fallback ── */
h1 {
  /* No fallback needed — just ignored in older browsers */
  text-wrap: balance;
}
```

---

## 129. COMPLETE UTILITY CLASS SYSTEM

```css
/* ─── Production-ready utility layer ─── */
@layer utilities {

  /* ── DISPLAY ── */
  :where(.d-block)        { display: block }
  :where(.d-inline)       { display: inline }
  :where(.d-inline-block) { display: inline-block }
  :where(.d-flex)         { display: flex }
  :where(.d-inline-flex)  { display: inline-flex }
  :where(.d-grid)         { display: grid }
  :where(.d-inline-grid)  { display: inline-grid }
  :where(.d-none)         { display: none }
  :where(.d-contents)     { display: contents }
  :where(.d-flow-root)    { display: flow-root }

  /* Responsive display */
  @media (max-width: 639px)  { :where(.hide-mobile)  { display: none } }
  @media (min-width: 640px)  { :where(.show-mobile-only) { display: none } }
  @media (max-width: 1023px) { :where(.hide-tablet)  { display: none } }
  @media (min-width: 1024px) { :where(.hide-desktop) { display: none } }

  /* ── FLEXBOX ── */
  :where(.flex-row)    { flex-direction: row }
  :where(.flex-col)    { flex-direction: column }
  :where(.flex-wrap)   { flex-wrap: wrap }
  :where(.flex-nowrap) { flex-wrap: nowrap }
  :where(.flex-1)      { flex: 1 1 0% }
  :where(.flex-auto)   { flex: 1 1 auto }
  :where(.flex-none)   { flex: none }
  :where(.shrink-0)    { flex-shrink: 0 }
  :where(.grow)        { flex-grow: 1 }
  :where(.grow-0)      { flex-grow: 0 }

  :where(.items-start)    { align-items: flex-start }
  :where(.items-end)      { align-items: flex-end }
  :where(.items-center)   { align-items: center }
  :where(.items-baseline) { align-items: baseline }
  :where(.items-stretch)  { align-items: stretch }

  :where(.justify-start)   { justify-content: flex-start }
  :where(.justify-end)     { justify-content: flex-end }
  :where(.justify-center)  { justify-content: center }
  :where(.justify-between) { justify-content: space-between }
  :where(.justify-around)  { justify-content: space-around }
  :where(.justify-evenly)  { justify-content: space-evenly }

  :where(.self-start)  { align-self: flex-start }
  :where(.self-end)    { align-self: flex-end }
  :where(.self-center) { align-self: center }
  :where(.self-stretch){ align-self: stretch }
  :where(.self-auto)   { align-self: auto }

  :where(.place-center) { place-items: center }

  /* ── GAP ── */
  :where(.gap-0)   { gap: 0 }
  :where(.gap-1)   { gap: var(--space-1) }
  :where(.gap-2)   { gap: var(--space-2) }
  :where(.gap-3)   { gap: var(--space-3) }
  :where(.gap-4)   { gap: var(--space-4) }
  :where(.gap-5)   { gap: var(--space-5) }
  :where(.gap-6)   { gap: var(--space-6) }
  :where(.gap-8)   { gap: var(--space-8) }
  :where(.gap-10)  { gap: var(--space-10) }

  :where(.row-gap-4) { row-gap: var(--space-4) }
  :where(.col-gap-4) { column-gap: var(--space-4) }

  /* ── SIZE ── */
  :where(.w-auto)   { width: auto }
  :where(.w-full)   { width: 100% }
  :where(.w-screen) { width: 100vw }
  :where(.w-fit)    { width: fit-content }
  :where(.w-min)    { width: min-content }
  :where(.w-max)    { width: max-content }
  :where(.h-auto)   { height: auto }
  :where(.h-full)   { height: 100% }
  :where(.h-screen) { height: 100dvh }
  :where(.h-fit)    { height: fit-content }
  :where(.min-w-0)  { min-width: 0 }
  :where(.min-h-0)  { min-height: 0 }
  :where(.min-h-screen) { min-height: 100dvh }

  /* ── MARGIN ── */
  :where(.m-auto)  { margin: auto }
  :where(.mx-auto) { margin-inline: auto }
  :where(.my-auto) { margin-block: auto }
  :where(.m-0)     { margin: 0 }

  /* Generate m-1 through m-16 */
  :where(.mt-0)  { margin-block-start: 0 }
  :where(.mb-0)  { margin-block-end: 0 }
  :where(.mt-4)  { margin-block-start: var(--space-4) }
  :where(.mb-4)  { margin-block-end: var(--space-4) }
  :where(.mt-8)  { margin-block-start: var(--space-8) }
  :where(.mb-8)  { margin-block-end: var(--space-8) }
  :where(.ms-auto) { margin-inline-start: auto }
  :where(.me-auto) { margin-inline-end: auto }

  /* ── PADDING ── */
  :where(.p-0)  { padding: 0 }
  :where(.p-2)  { padding: var(--space-2) }
  :where(.p-4)  { padding: var(--space-4) }
  :where(.p-6)  { padding: var(--space-6) }
  :where(.p-8)  { padding: var(--space-8) }
  :where(.px-4) { padding-inline: var(--space-4) }
  :where(.py-4) { padding-block: var(--space-4) }
  :where(.px-6) { padding-inline: var(--space-6) }
  :where(.py-6) { padding-block: var(--space-6) }
  :where(.px-8) { padding-inline: var(--space-8) }
  :where(.py-8) { padding-block: var(--space-8) }

  /* ── POSITION ── */
  :where(.static)   { position: static }
  :where(.relative) { position: relative }
  :where(.absolute) { position: absolute }
  :where(.fixed)    { position: fixed }
  :where(.sticky)   { position: sticky }
  :where(.inset-0)  { inset: 0 }
  :where(.inset-auto) { inset: auto }
  :where(.top-0)    { top: 0 }
  :where(.bottom-0) { bottom: 0 }
  :where(.left-0)   { left: 0 }
  :where(.right-0)  { right: 0 }

  /* ── Z-INDEX ── */
  :where(.z-0)        { z-index: 0 }
  :where(.z-10)       { z-index: 10 }
  :where(.z-20)       { z-index: 20 }
  :where(.z-50)       { z-index: 50 }
  :where(.z-auto)     { z-index: auto }

  /* ── OVERFLOW ── */
  :where(.overflow-auto)    { overflow: auto }
  :where(.overflow-hidden)  { overflow: hidden }
  :where(.overflow-clip)    { overflow: clip }
  :where(.overflow-scroll)  { overflow: scroll }
  :where(.overflow-visible) { overflow: visible }
  :where(.overflow-x-auto)  { overflow-x: auto; overflow-y: hidden }
  :where(.overflow-y-auto)  { overflow-y: auto; overflow-x: hidden }
  :where(.overflow-x-hidden){ overflow-x: hidden }
  :where(.overflow-y-hidden){ overflow-y: hidden }

  /* ── BORDER RADIUS ── */
  :where(.rounded-none) { border-radius: 0 }
  :where(.rounded-sm)   { border-radius: var(--radius-sm) }
  :where(.rounded)      { border-radius: var(--radius-md) }
  :where(.rounded-lg)   { border-radius: var(--radius-lg) }
  :where(.rounded-xl)   { border-radius: var(--radius-xl) }
  :where(.rounded-2xl)  { border-radius: var(--radius-2xl) }
  :where(.rounded-full) { border-radius: var(--radius-full) }

  /* ── SHADOW ── */
  :where(.shadow-none) { box-shadow: none }
  :where(.shadow-sm)   { box-shadow: var(--shadow-sm) }
  :where(.shadow)      { box-shadow: var(--shadow-md) }
  :where(.shadow-lg)   { box-shadow: var(--shadow-lg) }
  :where(.shadow-xl)   { box-shadow: var(--shadow-xl) }

  /* ── TYPOGRAPHY ── */
  :where(.text-xs)   { font-size: var(--font-size-xs) }
  :where(.text-sm)   { font-size: var(--font-size-sm) }
  :where(.text-base) { font-size: var(--font-size-base) }
  :where(.text-lg)   { font-size: var(--font-size-lg) }
  :where(.text-xl)   { font-size: var(--font-size-xl) }
  :where(.text-2xl)  { font-size: var(--font-size-2xl) }
  :where(.text-3xl)  { font-size: var(--font-size-3xl) }

  :where(.font-thin)     { font-weight: 100 }
  :where(.font-light)    { font-weight: 300 }
  :where(.font-normal)   { font-weight: 400 }
  :where(.font-medium)   { font-weight: 500 }
  :where(.font-semibold) { font-weight: 600 }
  :where(.font-bold)     { font-weight: 700 }
  :where(.font-black)    { font-weight: 900 }

  :where(.italic)  { font-style: italic }
  :where(.not-italic) { font-style: normal }

  :where(.text-left)    { text-align: left }
  :where(.text-center)  { text-align: center }
  :where(.text-right)   { text-align: right }
  :where(.text-start)   { text-align: start }
  :where(.text-end)     { text-align: end }
  :where(.text-justify) { text-align: justify }

  :where(.uppercase)    { text-transform: uppercase }
  :where(.lowercase)    { text-transform: lowercase }
  :where(.capitalize)   { text-transform: capitalize }
  :where(.normal-case)  { text-transform: none }

  :where(.underline)    { text-decoration-line: underline }
  :where(.no-underline) { text-decoration: none }
  :where(.line-through) { text-decoration-line: line-through }

  :where(.leading-none)    { line-height: 1 }
  :where(.leading-tight)   { line-height: var(--line-height-tight) }
  :where(.leading-snug)    { line-height: var(--line-height-snug) }
  :where(.leading-normal)  { line-height: var(--line-height-normal) }
  :where(.leading-relaxed) { line-height: var(--line-height-relaxed) }

  :where(.tracking-tight)   { letter-spacing: var(--letter-spacing-tight) }
  :where(.tracking-normal)  { letter-spacing: 0 }
  :where(.tracking-wide)    { letter-spacing: var(--letter-spacing-wide) }
  :where(.tracking-wider)   { letter-spacing: var(--letter-spacing-wider) }
  :where(.tracking-widest)  { letter-spacing: var(--letter-spacing-widest) }

  :where(.truncate)    { white-space: nowrap; overflow: hidden; text-overflow: ellipsis }
  :where(.text-nowrap) { white-space: nowrap }
  :where(.text-wrap)   { white-space: normal }
  :where(.text-break)  { overflow-wrap: break-word; word-break: break-word }
  :where(.text-balance){ text-wrap: balance }
  :where(.text-pretty) { text-wrap: pretty }

  :where(.clamp-1) { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden }
  :where(.clamp-2) { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden }
  :where(.clamp-3) { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden }

  /* ── COLOR ── */
  :where(.text-inherit)  { color: inherit }
  :where(.text-current)  { color: currentColor }
  :where(.text-muted)    { color: var(--color-text-muted) }
  :where(.text-subtle)   { color: var(--color-text-subtle) }
  :where(.text-accent)   { color: var(--color-accent) }
  :where(.text-danger)   { color: var(--color-danger-500) }
  :where(.text-success)  { color: var(--color-success-500) }
  :where(.text-warning)  { color: var(--color-warning-500) }

  /* ── BACKGROUND ── */
  :where(.bg-transparent) { background: transparent }
  :where(.bg-surface)     { background: var(--color-surface) }
  :where(.bg-subtle)      { background: var(--color-bg-subtle) }
  :where(.bg-muted)       { background: var(--color-bg-muted) }
  :where(.bg-accent)      { background: var(--color-accent) }

  /* ── OPACITY ── */
  :where(.opacity-0)   { opacity: 0 }
  :where(.opacity-25)  { opacity: 0.25 }
  :where(.opacity-50)  { opacity: 0.5 }
  :where(.opacity-75)  { opacity: 0.75 }
  :where(.opacity-100) { opacity: 1 }

  /* ── CURSOR ── */
  :where(.cursor-auto)    { cursor: auto }
  :where(.cursor-default) { cursor: default }
  :where(.cursor-pointer) { cursor: pointer }
  :where(.cursor-wait)    { cursor: wait }
  :where(.cursor-text)    { cursor: text }
  :where(.cursor-move)    { cursor: move }
  :where(.cursor-grab)    { cursor: grab }
  :where(.cursor-not-allowed) { cursor: not-allowed }

  /* ── POINTER EVENTS ── */
  :where(.pointer-none) { pointer-events: none }
  :where(.pointer-auto) { pointer-events: auto }

  /* ── USER SELECT ── */
  :where(.select-none) { user-select: none }
  :where(.select-text) { user-select: text }
  :where(.select-all)  { user-select: all }

  /* ── VISIBILITY ── */
  :where(.visible)   { visibility: visible }
  :where(.invisible) { visibility: hidden }

  :where(.sr-only) {
    position: absolute !important;
    width: 1px !important; height: 1px !important;
    padding: 0 !important; margin: -1px !important;
    overflow: hidden !important; clip: rect(0,0,0,0) !important;
    white-space: nowrap !important; border: 0 !important;
  }

  /* ── TRANSITIONS ── */
  :where(.transition-none)       { transition: none }
  :where(.transition)            { transition: all var(--duration-fast) var(--ease-default) }
  :where(.transition-colors)     { transition: color var(--duration-fast), background-color var(--duration-fast), border-color var(--duration-fast) }
  :where(.transition-opacity)    { transition: opacity var(--duration-fast) }
  :where(.transition-transform)  { transition: transform var(--duration-normal) var(--ease-out) }
  :where(.transition-shadow)     { transition: box-shadow var(--duration-fast) }
  :where(.duration-fast)         { transition-duration: var(--duration-fast) }
  :where(.duration-normal)       { transition-duration: var(--duration-normal) }
  :where(.duration-slow)         { transition-duration: var(--duration-slow) }
  :where(.ease-in)               { transition-timing-function: var(--ease-in) }
  :where(.ease-out)              { transition-timing-function: var(--ease-out) }
  :where(.ease-bounce)           { transition-timing-function: var(--ease-bounce) }

  /* ── MISC ── */
  :where(.isolate)        { isolation: isolate }
  :where(.will-transform) { will-change: transform }
  :where(.gpu)            { transform: translateZ(0); will-change: transform }
  :where(.aspect-square)  { aspect-ratio: 1 }
  :where(.aspect-video)   { aspect-ratio: 16/9 }
  :where(.object-cover)   { object-fit: cover }
  :where(.object-contain) { object-fit: contain }
  :where(.object-center)  { object-position: center }
  :where(.resize-none)    { resize: none }
  :where(.appearance-none){ appearance: none; -webkit-appearance: none }
}
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                 CSS MASTER GUIDE — PARTS I–VII                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  129 chapters · 700+ code examples · ~25,000+ lines                 ║
║                                                                      ║
║  NEW IN PART VII:                                                    ║
║  ✅ Tree view / file explorer (full interaction states)              ║
║  ✅ AI Chatbot UI (streaming, thinking, suggestions)                 ║
║  ✅ Settings page (nav, rows, danger zone, search)                   ║
║  ✅ Profile page (cover, avatar, stats, tabs)                        ║
║  ✅ Org chart (multi-level, department colors)                       ║
║  ✅ Feature comparison matrix (sticky columns, check marks)          ║
║  ✅ Clip-path animations (10 patterns: curtain, iris, wipe, blob)   ║
║  ✅ Cookie consent banner + preferences modal                        ║
║  ✅ Gamification (leaderboard, achievements, XP bar)                 ║
║  ✅ Survey / NPS (options, scale, animations)                        ║
║  ✅ CSS Shorthand complete reference                                  ║
║  ✅ Polyfills & progressive enhancement patterns                     ║
║  ✅ Complete utility class system (200+ classes with :where())       ║
╚══════════════════════════════════════════════════════════════════════╝
```
