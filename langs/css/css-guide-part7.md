\# PART VII — CSS: SPECIALTY COMPONENTS \& COMPLETE REFERENCE



\---



\## 117. TREE VIEW / FILE SYSTEM



```css

/\* ─── File tree component ─── \*/

.tree {

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.6;

&#x20; user-select: none;

}



.tree-node {

&#x20; position: relative;

}



/\* Connecting lines \*/

.tree-node::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-inline-start: -1.25rem;

&#x20; inset-block-start: 0;

&#x20; bottom: 50%;

&#x20; width: 1rem;

&#x20; border-bottom: 1px solid var(--color-border);

}



.tree-node:last-child::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-inline-start: -1.25rem;

&#x20; top: 50%;

&#x20; bottom: 0;

&#x20; border-left: 1px solid var(--color-bg-subtle); /\* hide vertical line \*/

&#x20; background: var(--color-surface);

&#x20; width: 2px;

}



.tree-children {

&#x20; padding-inline-start: 1.5rem;

&#x20; border-inline-start: 1px solid var(--color-border);

&#x20; margin-inline-start: 0.5rem;

}



/\* Node row \*/

.tree-row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.2rem 0.5rem;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

&#x20; min-height: 1.75rem;

}



.tree-row:hover { background: var(--color-bg-subtle); }

.tree-row.selected {

&#x20; background: color-mix(in srgb, var(--color-accent) 12%, transparent);

&#x20; color: var(--color-accent);

}

.tree-row.focused {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: -2px;

}



/\* Toggle arrow \*/

.tree-toggle {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; flex-shrink: 0;

&#x20; transition: rotate var(--duration-fast) var(--ease-out);

&#x20; font-size: 0.6rem;

}

.tree-toggle::before { content: '▶'; }

.tree-node.open > .tree-row .tree-toggle { rotate: 90deg; }

.tree-node--leaf > .tree-row .tree-toggle { visibility: hidden; }



/\* File type icon \*/

.tree-icon {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; flex-shrink: 0;

&#x20; font-size: 0.875rem;

}



/\* File-type colors \*/

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

&#x20; flex: 1;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



/\* File name rename input \*/

.tree-label--editing {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-accent);

&#x20; border-radius: var(--radius-sm);

&#x20; padding: 0 0.25rem;

&#x20; outline: none;

&#x20; font: inherit;

&#x20; width: 100%;

}



/\* Context menu indicator \*/

.tree-row:hover::after {

&#x20; content: '···';

&#x20; margin-inline-start: auto;

&#x20; color: var(--color-text-muted);

&#x20; letter-spacing: 0.05em;

}



/\* Drag/drop \*/

.tree-row.drag-over {

&#x20; background: color-mix(in srgb, var(--color-accent) 15%, transparent);

&#x20; outline: 1px dashed var(--color-accent);

}



/\* Search highlight \*/

.tree-label mark {

&#x20; background: var(--color-warning-200);

&#x20; color: var(--color-warning-900);

&#x20; border-radius: 2px;

}



/\* Hidden files \*/

.tree-node--hidden > .tree-row .tree-label { opacity: 0.5; font-style: italic; }



/\* Modified indicator \*/

.tree-node--modified > .tree-row .tree-label::after {

&#x20; content: '●';

&#x20; color: var(--color-warning-500);

&#x20; font-size: 0.5em;

&#x20; vertical-align: super;

&#x20; margin-inline-start: 0.25em;

}

```



\---



\## 118. AI / CHATBOT UI



```css

/\* ─── AI Assistant interface ─── \*/

.ai-chat {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; height: 100%;

&#x20; background: var(--color-bg-subtle);

}



/\* Message threads \*/

.ai-thread {

&#x20; flex: 1;

&#x20; overflow-y: auto;

&#x20; padding: var(--space-6) var(--space-4);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-6);

&#x20; max-width: 800px;

&#x20; margin-inline: auto;

&#x20; width: 100%;

&#x20; scroll-behavior: smooth;

}



/\* User message \*/

.ai-msg--user {

&#x20; align-self: flex-end;

&#x20; display: flex;

&#x20; align-items: flex-end;

&#x20; gap: var(--space-3);

&#x20; max-width: 75%;

&#x20; animation: msg-in-right 0.2s var(--ease-out);

}



@keyframes msg-in-right {

&#x20; from { opacity: 0; translate: 16px 0; }

}



.ai-msg--user .ai-bubble {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border-radius: var(--radius-2xl) var(--radius-2xl) var(--radius-sm) var(--radius-2xl);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.6;

&#x20; word-break: break-word;

}



/\* AI message \*/

.ai-msg--assistant {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; gap: var(--space-3);

&#x20; animation: msg-in-left 0.2s var(--ease-out);

}



@keyframes msg-in-left {

&#x20; from { opacity: 0; translate: -16px 0; }

}



.ai-avatar {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-lg);

&#x20; background: linear-gradient(135deg, oklch(0.6 0.25 280), oklch(0.6 0.25 200));

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; flex-shrink: 0;

&#x20; margin-block-start: 0.25rem;

}



.ai-msg--assistant .ai-bubble {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-sm) var(--radius-2xl) var(--radius-2xl) var(--radius-2xl);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.7;

&#x20; max-width: calc(100% - 2.75rem);

&#x20; box-shadow: var(--shadow-sm);

}



/\* Streaming text cursor \*/

.ai-bubble--streaming::after {

&#x20; content: '▋';

&#x20; animation: cursor-blink 0.7s step-end infinite;

&#x20; color: var(--color-accent);

&#x20; margin-inline-start: 0.1em;

}



@keyframes cursor-blink {

&#x20; 0%, 100% { opacity: 1; }

&#x20; 50%       { opacity: 0; }

}



/\* AI thinking / processing \*/

.ai-thinking {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3);

&#x20; animation: msg-in-left 0.2s var(--ease-out);

}



.ai-thinking-bubble {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-sm) var(--radius-2xl) var(--radius-2xl) var(--radius-2xl);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; display: flex;

&#x20; gap: 4px;

&#x20; align-items: center;

}



.ai-thinking-dot {

&#x20; width: 7px;

&#x20; height: 7px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-text-muted);

&#x20; animation: thinking 1.4s ease-in-out infinite;

}

.ai-thinking-dot:nth-child(2) { animation-delay: 0.2s; }

.ai-thinking-dot:nth-child(3) { animation-delay: 0.4s; }



@keyframes thinking {

&#x20; 0%, 60%, 100% { scale: 0.6; opacity: 0.4; }

&#x20; 30%           { scale: 1;   opacity: 1; }

}



/\* Code blocks in AI responses \*/

.ai-bubble pre {

&#x20; background: var(--color-neutral-900);

&#x20; color: var(--color-neutral-100);

&#x20; padding: var(--space-4);

&#x20; border-radius: var(--radius-lg);

&#x20; overflow-x: auto;

&#x20; margin-block: var(--space-3);

&#x20; font-size: 0.8125rem;

&#x20; line-height: 1.7;

&#x20; position: relative;

}



.ai-bubble pre .copy-btn {

&#x20; position: absolute;

&#x20; top: var(--space-2);

&#x20; right: var(--space-2);

&#x20; padding: 0.25rem 0.625rem;

&#x20; background: rgba(255 255 255 / 0.1);

&#x20; border: 1px solid rgba(255 255 255 / 0.15);

&#x20; border-radius: var(--radius-md);

&#x20; color: rgba(255 255 255 / 0.7);

&#x20; font-size: 0.6875rem;

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

}

.ai-bubble pre .copy-btn:hover { background: rgba(255 255 255 / 0.2); }



/\* Action buttons below AI message \*/

.ai-actions {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; margin-block-start: var(--space-2);

&#x20; padding-inline-start: 2.75rem;

}



.ai-action-btn {

&#x20; padding: 0.25rem 0.625rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25rem;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.ai-action-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }



/\* AI Input area \*/

.ai-input-area {

&#x20; padding: var(--space-4);

&#x20; background: var(--color-surface);

&#x20; border-top: 1px solid var(--color-border);

}



.ai-input-wrapper {

&#x20; max-width: 800px;

&#x20; margin-inline: auto;

&#x20; position: relative;

}



.ai-input {

&#x20; width: 100%;

&#x20; padding: 0.875rem 3.5rem 0.875rem 1rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; background: var(--color-surface);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; resize: none;

&#x20; outline: none;

&#x20; max-height: 200px;

&#x20; overflow-y: auto;

&#x20; line-height: 1.5;

&#x20; box-shadow: var(--shadow-sm);

&#x20; transition: border-color var(--duration-fast), box-shadow var(--duration-fast);

}



.ai-input:focus {

&#x20; border-color: var(--color-accent);

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);

}



.ai-send-btn {

&#x20; position: absolute;

&#x20; bottom: 0.625rem;

&#x20; right: 0.625rem;

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-lg);

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

}

.ai-send-btn:hover { background: var(--color-accent-hover); scale: 1.05; }

.ai-send-btn:disabled { opacity: 0.4; cursor: not-allowed; scale: 1; }



/\* Suggestion chips \*/

.ai-suggestions {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; flex-wrap: wrap;

&#x20; max-width: 800px;

&#x20; margin-inline: auto;

&#x20; margin-block-end: var(--space-3);

}



.ai-suggestion {

&#x20; padding: 0.4rem 0.875rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; background: var(--color-surface);

&#x20; font-size: var(--font-size-xs);

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; transition: background var(--duration-fast), border-color var(--duration-fast), color var(--duration-fast);

&#x20; white-space: nowrap;

}

.ai-suggestion:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; border-color: var(--color-accent);

&#x20; color: var(--color-accent);

}

```



\---



\## 119. SETTINGS / PREFERENCES PAGE



```css

/\* ─── Settings layout ─── \*/

.settings-layout {

&#x20; display: grid;

&#x20; grid-template-columns: 220px 1fr;

&#x20; gap: 0;

&#x20; min-height: calc(100dvh - var(--header-height, 60px));

}



@media (max-width: 768px) {

&#x20; .settings-layout { grid-template-columns: 1fr; }

&#x20; .settings-nav { display: none; }

}



/\* Settings sidebar nav \*/

.settings-nav {

&#x20; border-right: 1px solid var(--color-border);

&#x20; padding: var(--space-4);

&#x20; position: sticky;

&#x20; top: var(--header-height, 60px);

&#x20; height: calc(100dvh - var(--header-height, 60px));

&#x20; overflow-y: auto;

}



.settings-nav\_\_section {

&#x20; margin-block-end: var(--space-4);

}



.settings-nav\_\_label {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; padding: 0.25rem var(--space-3);

&#x20; margin-block-end: var(--space-1);

}



.settings-nav\_\_link {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.5rem var(--space-3);

&#x20; border-radius: var(--radius-md);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.settings-nav\_\_link:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.settings-nav\_\_link.active {

&#x20; background: color-mix(in srgb, var(--color-accent) 10%, transparent);

&#x20; color: var(--color-accent);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Settings main content \*/

.settings-content {

&#x20; padding: var(--space-8);

&#x20; max-width: 660px;

}



/\* Settings section \*/

.settings-section {

&#x20; margin-block-end: var(--space-10);

&#x20; padding-block-end: var(--space-10);

&#x20; border-bottom: 1px solid var(--color-border);

}

.settings-section:last-child { border: none; }



.settings-section\_\_title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; margin-block-end: var(--space-1);

}



.settings-section\_\_desc {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-6);

}



/\* Setting row \*/

.setting-row {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; justify-content: space-between;

&#x20; gap: var(--space-6);

&#x20; padding-block: var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

}

.setting-row:last-child { border: none; }



.setting-row\_\_info { flex: 1; min-width: 0; }



.setting-row\_\_label {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; margin-block-end: var(--space-1);

}



.setting-row\_\_desc {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.5;

}



.setting-row\_\_control { flex-shrink: 0; }



/\* Danger zone \*/

.settings-danger {

&#x20; border: 1px solid var(--color-danger-200);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-6);

&#x20; background: var(--color-danger-100);

}



.settings-danger\_\_title {

&#x20; font-size: var(--font-size-base);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-danger-700);

&#x20; margin-block-end: var(--space-1);

}



/\* Settings search \*/

.settings-search {

&#x20; position: relative;

&#x20; margin-block-end: var(--space-6);

}



.settings-search\_\_input {

&#x20; width: 100%;

&#x20; padding: 0.5rem 0.75rem 0.5rem 2.25rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; background: var(--color-surface);

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast);

}

.settings-search\_\_input:focus { border-color: var(--color-accent); }



.settings-search\_\_icon {

&#x20; position: absolute;

&#x20; left: 0.75rem;

&#x20; top: 50%;

&#x20; translate: 0 -50%;

&#x20; color: var(--color-text-muted);

&#x20; pointer-events: none;

}

```



\---



\## 120. PROFILE PAGE



```css

/\* ─── Profile hero ─── \*/

.profile-hero {

&#x20; position: relative;

}



.profile-cover {

&#x20; height: 200px;

&#x20; background: linear-gradient(

&#x20;   135deg,

&#x20;   var(--color-brand-600),

&#x20;   var(--color-brand-400)

&#x20; );

&#x20; border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;

&#x20; overflow: hidden;

}



.profile-cover img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

}



/\* Cover edit button \*/

.profile-cover\_\_edit {

&#x20; position: absolute;

&#x20; bottom: var(--space-3);

&#x20; right: var(--space-3);

&#x20; padding: 0.375rem 0.75rem;

&#x20; background: rgba(0 0 0 / 0.5);

&#x20; color: white;

&#x20; border: 1px solid rgba(255 255 255 / 0.3);

&#x20; border-radius: var(--radius-md);

&#x20; font-size: var(--font-size-xs);

&#x20; cursor: pointer;

&#x20; backdrop-filter: blur(4px);

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

}

.profile-cover:hover .profile-cover\_\_edit { opacity: 1; }



/\* Avatar row \*/

.profile-avatar-row {

&#x20; display: flex;

&#x20; align-items: flex-end;

&#x20; justify-content: space-between;

&#x20; padding: 0 var(--space-6) var(--space-4);

&#x20; margin-block-start: -3rem;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-4);

}



.profile-avatar {

&#x20; width: 6rem;

&#x20; height: 6rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; border: 4px solid var(--color-surface);

&#x20; box-shadow: var(--shadow-md);

&#x20; background: var(--color-bg-muted);

&#x20; flex-shrink: 0;

&#x20; position: relative;

}



.profile-avatar\_\_edit {

&#x20; position: absolute;

&#x20; bottom: 0;

&#x20; right: 0;

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border: 2px solid var(--color-surface);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 0.75rem;

}



.profile-actions {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; align-items: center;

&#x20; padding-block-end: 0.25rem;

}



/\* Profile info \*/

.profile-info {

&#x20; padding: var(--space-4) var(--space-6) var(--space-6);

}



.profile-name {

&#x20; font-size: var(--step-2);

&#x20; font-weight: var(--font-weight-bold);

&#x20; line-height: 1.2;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



/\* Verified badge \*/

.verified-badge {

&#x20; color: var(--color-brand-500);

&#x20; font-size: 1.25rem;

&#x20; flex-shrink: 0;

}



.profile-handle {

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-end: var(--space-3);

}



.profile-bio {

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.6;

&#x20; max-width: 55ch;

&#x20; margin-block-end: var(--space-4);

}



/\* Profile meta row \*/

.profile-meta {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-4);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-4);

}



.profile-meta\_\_item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

}



.profile-meta\_\_item a {

&#x20; color: var(--color-accent);

&#x20; text-decoration: none;

}

.profile-meta\_\_item a:hover { text-decoration: underline; }



/\* Follow stats \*/

.profile-stats {

&#x20; display: flex;

&#x20; gap: var(--space-6);

&#x20; font-size: var(--font-size-sm);

}



.profile-stat {

&#x20; display: flex;

&#x20; align-items: baseline;

&#x20; gap: 0.375rem;

&#x20; cursor: pointer;

}



.profile-stat\_\_count {

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-text);

&#x20; font-variant-numeric: tabular-nums;

}



.profile-stat\_\_label { color: var(--color-text-muted); }



/\* Profile tabs \*/

.profile-tabs {

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; overflow-x: auto;

&#x20; scrollbar-width: none;

&#x20; position: sticky;

&#x20; top: var(--header-height, 0);

&#x20; background: var(--color-surface);

&#x20; z-index: var(--z-sticky);

}

.profile-tabs::-webkit-scrollbar { display: none; }



.profile-tab {

&#x20; padding: 0.875rem 1.25rem;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; white-space: nowrap;

&#x20; border-bottom: 2px solid transparent;

&#x20; transition: color var(--duration-fast), border-color var(--duration-fast);

}

.profile-tab:hover { color: var(--color-text); }

.profile-tab.active {

&#x20; color: var(--color-text);

&#x20; border-bottom-color: var(--color-text);

}

```



\---



\## 121. ORG CHART



```css

/\* ─── Organizational chart ─── \*/

.org-chart {

&#x20; overflow: auto;

&#x20; padding: var(--space-8);

}



.org-tree {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: 0;

}



/\* Level \*/

.org-level {

&#x20; display: flex;

&#x20; justify-content: center;

&#x20; gap: 0;

&#x20; position: relative;

}



/\* Horizontal connector \*/

.org-level::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 0;

&#x20; height: 1px;

&#x20; background: var(--color-border);

&#x20; left: calc(50% / var(--items, 1));

&#x20; right: calc(50% / var(--items, 1));

}



/\* Vertical connector to parent \*/

.org-level::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: -2rem;

&#x20; left: 50%;

&#x20; height: 2rem;

&#x20; width: 1px;

&#x20; background: var(--color-border);

}



.org-level:first-child::after { display: none; }



/\* Node \*/

.org-node {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; padding: 0 var(--space-4);

&#x20; position: relative;

}



/\* Vertical line down to children \*/

.org-node::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; bottom: -2rem;

&#x20; left: 50%;

&#x20; height: 2rem;

&#x20; width: 1px;

&#x20; background: var(--color-border);

}



.org-node:only-child::after { display: none; }

.org-level:last-child .org-node::after { display: none; }



/\* Card \*/

.org-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; min-width: 160px;

&#x20; text-align: center;

&#x20; margin-block-end: 2rem;

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   box-shadow var(--duration-fast),

&#x20;   border-color var(--duration-fast),

&#x20;   scale var(--duration-fast) var(--ease-bounce);

&#x20; box-shadow: var(--shadow-sm);

}



.org-card:hover {

&#x20; box-shadow: var(--shadow-md);

&#x20; border-color: var(--color-accent);

&#x20; scale: 1.02;

}



.org-card.highlighted {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 5%, var(--color-surface));

}



.org-card\_\_avatar {

&#x20; width: 3rem;

&#x20; height: 3rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; margin-inline: auto;

&#x20; margin-block-end: var(--space-2);

&#x20; border: 2px solid var(--color-border);

}



.org-card\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.3;

}



.org-card\_\_title {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-start: var(--space-1);

}



.org-card\_\_dept {

&#x20; display: inline-flex;

&#x20; margin-block-start: var(--space-2);

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: 0.625rem;

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.05em;

&#x20; background: var(--dept-color, var(--color-bg-muted));

&#x20; color: white;

}



/\* Department colors \*/

.org-card\[data-dept="engineering"] { --dept-color: var(--color-brand-600); }

.org-card\[data-dept="design"]      { --dept-color: oklch(0.55 0.22 310); }

.org-card\[data-dept="product"]     { --dept-color: var(--color-success-600); }

.org-card\[data-dept="hr"]          { --dept-color: var(--color-warning-600); }

.org-card\[data-dept="finance"]     { --dept-color: oklch(0.45 0.1 250); }

```



\---



\## 122. FEATURE COMPARISON MATRIX



```css

/\* ─── Feature / Pricing comparison matrix ─── \*/

.comparison-matrix {

&#x20; overflow-x: auto;

&#x20; -webkit-overflow-scrolling: touch;

&#x20; border-radius: var(--radius-xl);

&#x20; border: 1px solid var(--color-border);

}



.matrix-table {

&#x20; width: 100%;

&#x20; border-collapse: collapse;

&#x20; min-width: 600px;

}



/\* Sticky header column \*/

.matrix-table th:first-child,

.matrix-table td:first-child {

&#x20; position: sticky;

&#x20; left: 0;

&#x20; background: var(--color-surface);

&#x20; z-index: 2;

&#x20; box-shadow: 1px 0 0 var(--color-border);

}



/\* Plan headers \*/

.matrix-table thead tr:first-child th {

&#x20; padding: var(--space-6) var(--space-4);

&#x20; text-align: center;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; z-index: 3;

}



/\* Featured plan column \*/

.matrix-col--featured {

&#x20; background: color-mix(in srgb, var(--color-accent) 4%, var(--color-surface));

}



.plan-header\_\_badge {

&#x20; display: inline-flex;

&#x20; padding: 0.2em 0.6em;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; border-radius: var(--radius-full);

&#x20; margin-block-end: var(--space-2);

}



.plan-header\_\_name {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

}



.plan-header\_\_price {

&#x20; font-size: var(--step-2);

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-text);

&#x20; margin-block: var(--space-2);

}



.plan-header\_\_period {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-normal);

&#x20; color: var(--color-text-muted);

}



/\* Category rows \*/

.matrix-category {

&#x20; background: var(--color-bg-subtle);

&#x20; padding: var(--space-2) var(--space-4);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; border-bottom: 1px solid var(--color-border);

}



/\* Feature rows \*/

.matrix-table tbody tr:not(.matrix-category-row) td {

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; font-size: var(--font-size-sm);

&#x20; text-align: center;

&#x20; vertical-align: middle;

}



.matrix-table tbody tr:not(.matrix-category-row) td:first-child {

&#x20; text-align: start;

&#x20; color: var(--color-text);

}



.matrix-table tbody tr:hover td {

&#x20; background: var(--color-bg-subtle);

}

.matrix-table tbody tr:hover .matrix-col--featured {

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface));

}



/\* Check / X icons \*/

.check { color: var(--color-success-500); font-size: 1.1em; }

.cross  { color: var(--color-neutral-400); font-size: 1.1em; }

.partial {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; width: 1.25em;

&#x20; height: 1.25em;

&#x20; border-radius: 50%;

&#x20; background: var(--color-warning-100);

&#x20; color: var(--color-warning-700);

&#x20; font-size: 0.75em;

&#x20; font-weight: bold;

}

```



\---



\## 123. CLIP-PATH ANIMATIONS



```css

/\* ─── Reveal effects via clip-path ─── \*/



/\* 1. Curtain reveal (left to right) \*/

.clip-curtain {

&#x20; clip-path: inset(0 100% 0 0);

&#x20; animation: curtain-open 0.6s var(--ease-out) forwards;

}

@keyframes curtain-open {

&#x20; to { clip-path: inset(0 0% 0 0); }

}



/\* 2. Circle expand \*/

.clip-circle-in {

&#x20; clip-path: circle(0% at 50% 50%);

&#x20; animation: circle-in 0.5s var(--ease-out) forwards;

}

@keyframes circle-in {

&#x20; to { clip-path: circle(150% at 50% 50%); }

}



/\* 3. Circle from corner \*/

.clip-circle-corner {

&#x20; clip-path: circle(0% at 0% 0%);

&#x20; animation: circle-corner 0.6s var(--ease-out) forwards;

}

@keyframes circle-corner {

&#x20; to { clip-path: circle(200% at 0% 0%); }

}



/\* 4. Wipe from bottom \*/

.clip-wipe-up {

&#x20; clip-path: inset(100% 0 0 0);

&#x20; animation: wipe-up 0.5s var(--ease-out) forwards;

}

@keyframes wipe-up {

&#x20; to { clip-path: inset(0% 0 0 0); }

}



/\* 5. Diamond reveal \*/

.clip-diamond {

&#x20; clip-path: polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%);

&#x20; animation: diamond-reveal 0.6s var(--ease-out) forwards;

}

@keyframes diamond-reveal {

&#x20; to { clip-path: polygon(50% -50%, 150% 50%, 50% 150%, -50% 50%); }

}



/\* 6. Diagonal swipe \*/

.clip-diagonal {

&#x20; clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);

&#x20; animation: diagonal-swipe 0.5s var(--ease-out) forwards;

}

@keyframes diagonal-swipe {

&#x20; to { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }

}



/\* 7. Iris (center expand like camera) \*/

.clip-iris {

&#x20; clip-path: polygon(

&#x20;   50% 50%, 50% 50%, 50% 50%, 50% 50%,

&#x20;   50% 50%, 50% 50%, 50% 50%, 50% 50%

&#x20; );

&#x20; animation: iris-open 0.5s var(--ease-out) forwards;

}

@keyframes iris-open {

&#x20; to {

&#x20;   clip-path: polygon(

&#x20;     0% 0%, 100% 0%, 100% 100%, 0% 100%

&#x20;   );

&#x20; }

}



/\* 8. Morphing blob on hover \*/

.clip-blob {

&#x20; clip-path: polygon(25% 5%, 75% 5%, 95% 25%, 95% 75%, 75% 95%, 25% 95%, 5% 75%, 5% 25%);

&#x20; transition: clip-path 0.4s var(--ease-out);

}

.clip-blob:hover {

&#x20; clip-path: polygon(50% 0%, 90% 20%, 100% 60%, 75% 100%, 25% 100%, 0% 60%, 10% 20%, 50% 0%);

}



/\* 9. Text reveal via parent clip \*/

.text-reveal-wrapper {

&#x20; overflow: hidden;

}

.text-reveal-line {

&#x20; translate: 0 100%;

&#x20; animation: line-slide-up 0.5s var(--ease-out) forwards;

&#x20; animation-delay: calc(var(--line, 0) \* 80ms);

}

@keyframes line-slide-up {

&#x20; to { translate: 0 0; }

}



/\* 10. Scroll-driven clip-path \*/

.scroll-clip {

&#x20; clip-path: inset(20% 10%);

&#x20; animation: expand-clip linear both;

&#x20; animation-timeline: view();

&#x20; animation-range: entry 0% entry 60%;

}

@keyframes expand-clip {

&#x20; to { clip-path: inset(0% 0%); }

}

```



\---



\## 124. COOKIE CONSENT \& LEGAL UI



```css

/\* ─── Cookie consent banner ─── \*/

.cookie-banner {

&#x20; position: fixed;

&#x20; inset-block-end: var(--space-4);

&#x20; inset-inline: var(--space-4);

&#x20; max-width: 420px;

&#x20; background: var(--color-neutral-900);

&#x20; color: var(--color-neutral-100);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-5);

&#x20; z-index: var(--z-toast);

&#x20; box-shadow: var(--shadow-2xl);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-4);



&#x20; animation: banner-slide-in 0.4s var(--ease-bounce);

}



@keyframes banner-slide-in {

&#x20; from { translate: 0 120%; opacity: 0; }

}



.cookie-banner.dismissing {

&#x20; animation: banner-slide-out 0.3s var(--ease-in) forwards;

}



@keyframes banner-slide-out {

&#x20; to { translate: 0 120%; opacity: 0; }

}



.cookie-banner\_\_icon {

&#x20; font-size: 2rem;

}



.cookie-banner\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-base);

}



.cookie-banner\_\_text {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-neutral-400);

&#x20; line-height: 1.6;

}



.cookie-banner\_\_text a {

&#x20; color: var(--color-neutral-300);

&#x20; text-decoration: underline;

}



.cookie-banner\_\_actions {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; flex-wrap: wrap;

}



.cookie-btn {

&#x20; flex: 1;

&#x20; padding: 0.625rem 1rem;

&#x20; border-radius: var(--radius-lg);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; border: 1px solid transparent;

&#x20; white-space: nowrap;

}



.cookie-btn--accept {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border-color: var(--color-accent);

}

.cookie-btn--accept:hover { background: var(--color-accent-hover); }



.cookie-btn--decline {

&#x20; background: transparent;

&#x20; color: var(--color-neutral-400);

&#x20; border-color: var(--color-neutral-600);

}

.cookie-btn--decline:hover { background: var(--color-neutral-800); color: var(--color-neutral-200); }



.cookie-btn--customize {

&#x20; width: 100%;

&#x20; background: transparent;

&#x20; color: var(--color-neutral-400);

&#x20; font-size: var(--font-size-xs);

&#x20; text-decoration: underline;

&#x20; flex: none;

}



/\* ─── Cookie preferences modal ─── \*/

.cookie-preferences {

&#x20; padding: var(--space-6);

&#x20; max-width: 560px;

}



.cookie-category {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; justify-content: space-between;

&#x20; gap: var(--space-4);

&#x20; padding-block: var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

}

.cookie-category:last-child { border: none; }



.cookie-category\_\_info { flex: 1; }

.cookie-category\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-end: var(--space-1);

}

.cookie-category\_\_desc {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.5;

}



.cookie-required-label {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-style: italic;

&#x20; align-self: center;

}



/\* ─── Terms / Privacy page ─── \*/

.legal-page {

&#x20; max-width: 720px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-8);

}



.legal-page h1 {

&#x20; font-size: var(--step-3);

&#x20; font-weight: var(--font-weight-black);

&#x20; margin-block-end: var(--space-2);

}



.legal-meta {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-8);

&#x20; padding-block-end: var(--space-8);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; gap: var(--space-6);

}

```



\---



\## 125. GAMIFICATION COMPONENTS



```css

/\* ─── Leaderboard ─── \*/

.leaderboard {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.leaderboard-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; transition:

&#x20;   box-shadow var(--duration-fast),

&#x20;   translate  var(--duration-fast);

&#x20; animation: rank-in 0.4s var(--ease-out) backwards;

&#x20; animation-delay: calc(var(--rank, 0) \* 60ms);

}



@keyframes rank-in {

&#x20; from { opacity: 0; translate: -20px 0; }

}



.leaderboard-item:hover {

&#x20; box-shadow: var(--shadow-md);

&#x20; translate: 2px 0;

}



/\* Top 3 special styling \*/

.leaderboard-item:nth-child(1) { border-color: #FFD700; background: linear-gradient(to right, #fffde7, var(--color-surface)); }

.leaderboard-item:nth-child(2) { border-color: #C0C0C0; background: linear-gradient(to right, #f5f5f5, var(--color-surface)); }

.leaderboard-item:nth-child(3) { border-color: #CD7F32; background: linear-gradient(to right, #fff8f0, var(--color-surface)); }



/\* Rank badge \*/

.rank-badge {

&#x20; min-width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-md);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-black);

&#x20; font-size: var(--font-size-sm);

&#x20; flex-shrink: 0;

&#x20; font-variant-numeric: tabular-nums;

}



.rank-badge--1 { background: #FFD700; color: #7a5c00; }

.rank-badge--2 { background: #C0C0C0; color: #555; }

.rank-badge--3 { background: #CD7F32; color: #fff; }

.rank-badge--n { background: var(--color-bg-muted); color: var(--color-text-muted); }



.leaderboard-item\_\_info { flex: 1; min-width: 0; }

.leaderboard-item\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}

.leaderboard-item\_\_sub { font-size: var(--font-size-xs); color: var(--color-text-muted); }



.leaderboard-item\_\_score {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

&#x20; color: var(--color-text);

&#x20; flex-shrink: 0;

}



.leaderboard-item\_\_change {

&#x20; font-size: var(--font-size-xs);

&#x20; flex-shrink: 0;

&#x20; font-weight: var(--font-weight-medium);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.2em;

}

.leaderboard-item\_\_change--up   { color: var(--color-success-500); }

.leaderboard-item\_\_change--down { color: var(--color-danger-500); }

.leaderboard-item\_\_change--same { color: var(--color-text-muted); }



/\* ─── Achievement badge ─── \*/

.achievement {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-4);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; text-align: center;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

&#x20; position: relative;

&#x20; overflow: hidden;

}



.achievement:hover { scale: 1.03; }



.achievement.locked {

&#x20; opacity: 0.4;

&#x20; filter: grayscale(100%);

}



.achievement.newly-unlocked {

&#x20; animation: achievement-unlock 0.6s var(--ease-bounce);

&#x20; border-color: var(--color-warning-400);

}



@keyframes achievement-unlock {

&#x20; 0%   { scale: 0.5; rotate: -10deg; opacity: 0; }

&#x20; 60%  { scale: 1.15; rotate: 5deg; }

&#x20; 100% { scale: 1; rotate: 0deg; opacity: 1; }

}



.achievement\_\_icon {

&#x20; font-size: 2.5rem;

&#x20; line-height: 1;

}



.achievement\_\_name {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; line-height: 1.3;

}



.achievement\_\_desc {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



/\* Shine on unlock \*/

.achievement.newly-unlocked::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: linear-gradient(

&#x20;   135deg,

&#x20;   transparent 30%,

&#x20;   rgba(255 255 255 / 0.5) 50%,

&#x20;   transparent 70%

&#x20; );

&#x20; animation: achievement-shine 0.8s ease-out;

}



@keyframes achievement-shine {

&#x20; from { translate: -100% -100%; }

&#x20; to   { translate: 100% 100%; }

}



/\* ─── XP / Level progress ─── \*/

.xp-bar {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-4);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.xp-bar\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

}



.xp-level {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



.xp-level\_\_badge {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

&#x20; background: linear-gradient(135deg, var(--color-warning-400), var(--color-warning-600));

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-black);

&#x20; font-size: var(--font-size-sm);

&#x20; box-shadow: 0 0 0 3px var(--color-warning-200);

}



.xp-level\_\_label {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-semibold);

}



.xp-bar\_\_track {

&#x20; height: 8px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.xp-bar\_\_fill {

&#x20; height: 100%;

&#x20; background: linear-gradient(to right, var(--color-warning-400), var(--color-warning-600));

&#x20; border-radius: inherit;

&#x20; width: var(--xp-pct, 0%);

&#x20; transition: width 1s var(--ease-out);

&#x20; position: relative;

&#x20; overflow: hidden;

}



/\* Animated sheen on XP bar \*/

.xp-bar\_\_fill::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; width: 50%;

&#x20; background: linear-gradient(to right, transparent, rgba(255 255 255 / 0.4), transparent);

&#x20; animation: xp-sheen 2s ease-in-out infinite;

}



@keyframes xp-sheen {

&#x20; from { translate: -200% 0; }

&#x20; to   { translate: 400% 0; }

}



.xp-bar\_\_numbers {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-variant-numeric: tabular-nums;

}

```



\---



\## 126. SURVEY / QUESTIONNAIRE UI



```css

/\* ─── Survey container ─── \*/

.survey {

&#x20; max-width: 640px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-8) var(--space-4);

}



.survey\_\_progress {

&#x20; margin-block-end: var(--space-8);

}



.survey\_\_progress-label {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-2);

}



/\* Question card \*/

.survey-question {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-8);

&#x20; animation: question-slide 0.3s var(--ease-out);

}



@keyframes question-slide {

&#x20; from { opacity: 0; translate: 0 20px; }

}



.survey-question\_\_number {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-accent);

&#x20; margin-block-end: var(--space-2);

}



.survey-question\_\_text {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; line-height: 1.4;

&#x20; margin-block-end: var(--space-6);

&#x20; text-wrap: balance;

}



.survey-question\_\_sub {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-start: -var(--space-4);

&#x20; margin-block-end: var(--space-6);

}



/\* Answer options \*/

.survey-options {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.survey-option {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-4);

&#x20; border: 2px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast),

&#x20;   scale        var(--duration-fast) var(--ease-bounce);

&#x20; user-select: none;

}



.survey-option:hover {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 4%, transparent);

}



.survey-option input { display: none; }



.survey-option\_\_indicator {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border: 2px solid var(--color-border);

&#x20; border-radius: 50%;

&#x20; flex-shrink: 0;

&#x20; transition: border-color var(--duration-fast), background var(--duration-fast);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

}



.survey-option:has(input:checked) {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

&#x20; scale: 1.01;

}



.survey-option:has(input:checked) .survey-option\_\_indicator {

&#x20; border-color: var(--color-accent);

&#x20; background: var(--color-accent);

}



.survey-option:has(input:checked) .survey-option\_\_indicator::after {

&#x20; content: '';

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; background: white;

}



.survey-option\_\_emoji { font-size: 1.5rem; flex-shrink: 0; }

.survey-option\_\_text  { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }

.survey-option\_\_desc  { font-size: var(--font-size-xs); color: var(--color-text-muted); }



/\* NPS scale \*/

.nps-scale {

&#x20; display: flex;

&#x20; gap: var(--space-1);

&#x20; justify-content: center;

&#x20; flex-wrap: wrap;

}



.nps-btn {

&#x20; width: 3rem;

&#x20; height: 3rem;

&#x20; border: 2px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; background: var(--color-surface);

&#x20; cursor: pointer;

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; font-variant-numeric: tabular-nums;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast),

&#x20;   scale        var(--duration-fast) var(--ease-bounce);

}



.nps-btn:hover { border-color: var(--color-accent); scale: 1.05; }

.nps-btn.selected { background: var(--color-accent); border-color: var(--color-accent); color: white; scale: 1.1; }



/\* NPS color coding \*/

.nps-btn:nth-child(-n+6)  { --hover-tint: var(--color-danger-100); }

.nps-btn:nth-child(n+7):nth-child(-n+8) { --hover-tint: var(--color-warning-100); }

.nps-btn:nth-child(n+9)   { --hover-tint: var(--color-success-100); }



.nps-labels {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-start: var(--space-2);

}

```



\---



\## 127. CSS SHORTHAND PROPERTIES — COMPLETE GUIDE



```css

/\* ─── Every important CSS shorthand ─── \*/



/\* BORDER \*/

border: 2px solid red;

/\* Expands to: border-width border-style border-color \*/

/\* Sides: border-top, border-right, border-bottom, border-left \*/

/\* Logical: border-block-start, border-inline-start \*/



/\* BORDER-RADIUS \*/

border-radius: 8px;                    /\* all corners \*/

border-radius: 8px 4px;               /\* TL+BR | TR+BL \*/

border-radius: 8px 4px 6px;           /\* TL | TR+BL | BR \*/

border-radius: 8px 4px 6px 2px;       /\* TL TR BR BL \*/

border-radius: 8px / 4px;             /\* horiz-radius / vert-radius \*/

border-radius: 8px 4px / 2px 6px;    /\* TL+BR horiz | TR+BL horiz / TL+BR vert | TR+BL vert \*/



/\* MARGIN and PADDING \*/

margin: 1rem;                          /\* all sides \*/

margin: 1rem 2rem;                     /\* block | inline \*/

margin: 1rem 2rem 3rem;               /\* top | inline | bottom \*/

margin: 1rem 2rem 3rem 4rem;          /\* top right bottom left \*/

/\* Logical: margin-block, margin-inline, margin-block-start etc \*/



/\* BACKGROUND \*/

background: url('img.jpg') center/cover no-repeat fixed;

/\* Order: image position/size repeat attachment origin clip color \*/

background: linear-gradient(red, blue), url('img.jpg') center/cover no-repeat #fff;

/\* Multiple: comma-separated layers, color only on last \*/



/\* FONT \*/

font: italic bold 1.25rem/1.5 'Arial', sans-serif;

/\* MUST include: size and family. Optional: style weight variant/stretch size/line-height \*/

font: var(--font-weight-bold) var(--font-size-base)/1.5 var(--font-sans);



/\* TRANSITION \*/

transition: color 0.2s ease, background 0.2s ease 0.1s;

/\* property duration timing-function delay \*/

/\* Multiple: comma-separated \*/



/\* ANIMATION \*/

animation: fadeIn 0.3s ease-out 0s 1 normal both running;

/\* name duration timing delay count direction fill-mode play-state \*/



/\* OUTLINE \*/

outline: 2px solid var(--color-accent);

/\* width style color — no individual sides, no border-radius \*/



/\* LIST-STYLE \*/

list-style: disc inside url('bullet.svg');

/\* type position image \*/



/\* GRID \*/

grid: auto / 1fr 2fr;                              /\* rows / columns \*/

grid: "header" auto "main" 1fr "footer" auto / 1fr; /\* template \*/



/\* FLEX \*/

flex: 1 1 auto;   /\* grow shrink basis \*/

flex: 1;          /\* 1 1 0 \*/

flex: auto;       /\* 1 1 auto \*/

flex: none;       /\* 0 0 auto \*/



/\* FLEX-FLOW \*/

flex-flow: row wrap;  /\* direction wrap \*/



/\* GAP \*/

gap: 1rem 2rem;  /\* row-gap column-gap \*/



/\* PLACE-ITEMS \*/

place-items: center;        /\* align-items justify-items \*/

place-content: center;      /\* align-content justify-content \*/

place-self: center;         /\* align-self justify-self \*/



/\* SCROLL-MARGIN / SCROLL-PADDING \*/

scroll-margin: 1rem;        /\* all sides \*/

scroll-padding: 0 1rem;     /\* block | inline \*/



/\* INSET \*/

inset: 0;                   /\* top right bottom left \*/

inset: 1rem 2rem;           /\* block inline \*/

inset-block: 0;             /\* top bottom \*/

inset-inline: 0;            /\* left right \*/



/\* OVERFLOW \*/

overflow: hidden auto;      /\* x y — in CSS4 \*/



/\* TEXT-DECORATION \*/

text-decoration: underline dotted var(--color-accent) 2px;

/\* line style color thickness \*/



/\* MASK \*/

mask: url('mask.png') center/cover no-repeat;

/\* image position/size repeat \*/



/\* COLUMNS (Multi-column) \*/

columns: 3 200px;           /\* count width \*/



/\* CONTAIN-INTRINSIC-SIZE \*/

contain-intrinsic-size: 0 300px;   /\* inline-size block-size \*/



/\* ANIMATION-RANGE \*/

animation-range: entry 0% entry 50%;  /\* start end \*/



/\* SCROLL-TIMELINE \*/

scroll-timeline: --name block;  /\* name axis \*/



/\* VIEW-TIMELINE \*/

view-timeline: --name block;



/\* CONTAINER \*/

container: name / inline-size;   /\* name type \*/



/\* WILL-CHANGE \*/

/\* Not a shorthand but often misused: \*/

will-change: transform, opacity;  /\* comma-separated properties \*/

```



\---



\## 128. CSS POLYFILLS \& PROGRESSIVE ENHANCEMENT



```css

/\* ─── Progressive enhancement patterns ─── \*/



/\* ── :has() fallback ── \*/

/\* Without :has() — use JS to add class \*/

/\* With :has() \*/

@supports selector(:has(\*)) {

&#x20; .form:has(input:invalid) { border-color: red; }

}

/\* Fallback \*/

.form.has-invalid { border-color: red; }



/\* ── Container queries fallback ── \*/

@supports (container-type: inline-size) {

&#x20; .wrapper { container-type: inline-size; }

&#x20; @container (min-width: 400px) {

&#x20;   .card { flex-direction: row; }

&#x20; }

}

/\* Fallback: media query \*/

@media (min-width: 600px) {

&#x20; .card { flex-direction: row; }

}



/\* ── CSS Nesting fallback ── \*/

/\* Modern \*/

.parent {

&#x20; \& .child { color: red; }

}

/\* Compiled (PostCSS output) \*/

.parent .child { color: red; }



/\* ── oklch() fallback ── \*/

.element {

&#x20; color: #3b82f6;                           /\* legacy fallback \*/

&#x20; color: oklch(0.6 0.2 250);               /\* modern \*/

}

/\* Or via @supports \*/

@supports (color: oklch(0 0 0)) {

&#x20; :root { --accent: oklch(0.6 0.2 250); }

}



/\* ── color-mix() fallback ── \*/

.el {

&#x20; background: rgba(59, 130, 246, 0.15);    /\* fallback \*/

&#x20; background: color-mix(in srgb, var(--color-accent) 15%, transparent);

}



/\* ── Scroll-Driven animations fallback ── \*/

@supports (animation-timeline: scroll()) {

&#x20; .progress { animation: fill linear; animation-timeline: scroll(root); }

}

/\* Fallback: JS scroll handler \*/



/\* ── View Transitions fallback ── \*/

/\* JS: if (!document.startViewTransition) { updateDOM(); return; } \*/



/\* ── anchor-name fallback ── \*/

@supports (anchor-name: --a) {

&#x20; .tooltip { position: fixed; top: anchor(bottom); }

}

/\* Fallback: JS positioning \*/



/\* ── dvh fallback ── \*/

.hero {

&#x20; min-height: 100vh;    /\* fallback \*/

&#x20; min-height: 100dvh;   /\* override if supported \*/

}



/\* ── clamp() fallback ── \*/

.fluid-text {

&#x20; font-size: 1.5rem;                        /\* fallback \*/

&#x20; font-size: clamp(1rem, 2vw + 0.5rem, 2rem);

}



/\* ── gap in flexbox fallback ── \*/

.flex-gap > \* + \* { margin-inline-start: 1rem; } /\* fallback \*/

@supports (gap: 1rem) {

&#x20; .flex-gap > \* + \* { margin-inline-start: 0; }

&#x20; .flex-gap { gap: 1rem; }

}



/\* ── Logical properties fallback ── \*/

/\* Auto-resolved by PostCSS logical plugin: \*/

.el {

&#x20; margin-left: 1rem;              /\* fallback \*/

&#x20; margin-inline-start: 1rem;      /\* override \*/

}



/\* ── @layer fallback ── \*/

/\* Browsers that don't support @layer treat everything as unlayered \*/

/\* (normal specificity rules apply) \*/

/\* So you can write @layer safely with no fallback needed for functionality \*/

/\* Just don't rely on layer ordering for critical styles \*/



/\* ── interpolate-size fallback ── \*/

.accordion {

&#x20; max-height: 0;

&#x20; overflow: hidden;

&#x20; transition: max-height 0.4s;   /\* fallback \*/

}

.accordion.open { max-height: 2000px; }



@supports (interpolate-size: allow-keywords) {

&#x20; :root { interpolate-size: allow-keywords; }

&#x20; .accordion { max-height: none; height: 0; transition: height 0.3s; }

&#x20; .accordion.open { height: auto; }

}



/\* ── text-wrap: balance fallback ── \*/

h1 {

&#x20; /\* No fallback needed — just ignored in older browsers \*/

&#x20; text-wrap: balance;

}

```



\---



\## 129. COMPLETE UTILITY CLASS SYSTEM



```css

/\* ─── Production-ready utility layer ─── \*/

@layer utilities {



&#x20; /\* ── DISPLAY ── \*/

&#x20; :where(.d-block)        { display: block }

&#x20; :where(.d-inline)       { display: inline }

&#x20; :where(.d-inline-block) { display: inline-block }

&#x20; :where(.d-flex)         { display: flex }

&#x20; :where(.d-inline-flex)  { display: inline-flex }

&#x20; :where(.d-grid)         { display: grid }

&#x20; :where(.d-inline-grid)  { display: inline-grid }

&#x20; :where(.d-none)         { display: none }

&#x20; :where(.d-contents)     { display: contents }

&#x20; :where(.d-flow-root)    { display: flow-root }



&#x20; /\* Responsive display \*/

&#x20; @media (max-width: 639px)  { :where(.hide-mobile)  { display: none } }

&#x20; @media (min-width: 640px)  { :where(.show-mobile-only) { display: none } }

&#x20; @media (max-width: 1023px) { :where(.hide-tablet)  { display: none } }

&#x20; @media (min-width: 1024px) { :where(.hide-desktop) { display: none } }



&#x20; /\* ── FLEXBOX ── \*/

&#x20; :where(.flex-row)    { flex-direction: row }

&#x20; :where(.flex-col)    { flex-direction: column }

&#x20; :where(.flex-wrap)   { flex-wrap: wrap }

&#x20; :where(.flex-nowrap) { flex-wrap: nowrap }

&#x20; :where(.flex-1)      { flex: 1 1 0% }

&#x20; :where(.flex-auto)   { flex: 1 1 auto }

&#x20; :where(.flex-none)   { flex: none }

&#x20; :where(.shrink-0)    { flex-shrink: 0 }

&#x20; :where(.grow)        { flex-grow: 1 }

&#x20; :where(.grow-0)      { flex-grow: 0 }



&#x20; :where(.items-start)    { align-items: flex-start }

&#x20; :where(.items-end)      { align-items: flex-end }

&#x20; :where(.items-center)   { align-items: center }

&#x20; :where(.items-baseline) { align-items: baseline }

&#x20; :where(.items-stretch)  { align-items: stretch }



&#x20; :where(.justify-start)   { justify-content: flex-start }

&#x20; :where(.justify-end)     { justify-content: flex-end }

&#x20; :where(.justify-center)  { justify-content: center }

&#x20; :where(.justify-between) { justify-content: space-between }

&#x20; :where(.justify-around)  { justify-content: space-around }

&#x20; :where(.justify-evenly)  { justify-content: space-evenly }



&#x20; :where(.self-start)  { align-self: flex-start }

&#x20; :where(.self-end)    { align-self: flex-end }

&#x20; :where(.self-center) { align-self: center }

&#x20; :where(.self-stretch){ align-self: stretch }

&#x20; :where(.self-auto)   { align-self: auto }



&#x20; :where(.place-center) { place-items: center }



&#x20; /\* ── GAP ── \*/

&#x20; :where(.gap-0)   { gap: 0 }

&#x20; :where(.gap-1)   { gap: var(--space-1) }

&#x20; :where(.gap-2)   { gap: var(--space-2) }

&#x20; :where(.gap-3)   { gap: var(--space-3) }

&#x20; :where(.gap-4)   { gap: var(--space-4) }

&#x20; :where(.gap-5)   { gap: var(--space-5) }

&#x20; :where(.gap-6)   { gap: var(--space-6) }

&#x20; :where(.gap-8)   { gap: var(--space-8) }

&#x20; :where(.gap-10)  { gap: var(--space-10) }



&#x20; :where(.row-gap-4) { row-gap: var(--space-4) }

&#x20; :where(.col-gap-4) { column-gap: var(--space-4) }



&#x20; /\* ── SIZE ── \*/

&#x20; :where(.w-auto)   { width: auto }

&#x20; :where(.w-full)   { width: 100% }

&#x20; :where(.w-screen) { width: 100vw }

&#x20; :where(.w-fit)    { width: fit-content }

&#x20; :where(.w-min)    { width: min-content }

&#x20; :where(.w-max)    { width: max-content }

&#x20; :where(.h-auto)   { height: auto }

&#x20; :where(.h-full)   { height: 100% }

&#x20; :where(.h-screen) { height: 100dvh }

&#x20; :where(.h-fit)    { height: fit-content }

&#x20; :where(.min-w-0)  { min-width: 0 }

&#x20; :where(.min-h-0)  { min-height: 0 }

&#x20; :where(.min-h-screen) { min-height: 100dvh }



&#x20; /\* ── MARGIN ── \*/

&#x20; :where(.m-auto)  { margin: auto }

&#x20; :where(.mx-auto) { margin-inline: auto }

&#x20; :where(.my-auto) { margin-block: auto }

&#x20; :where(.m-0)     { margin: 0 }



&#x20; /\* Generate m-1 through m-16 \*/

&#x20; :where(.mt-0)  { margin-block-start: 0 }

&#x20; :where(.mb-0)  { margin-block-end: 0 }

&#x20; :where(.mt-4)  { margin-block-start: var(--space-4) }

&#x20; :where(.mb-4)  { margin-block-end: var(--space-4) }

&#x20; :where(.mt-8)  { margin-block-start: var(--space-8) }

&#x20; :where(.mb-8)  { margin-block-end: var(--space-8) }

&#x20; :where(.ms-auto) { margin-inline-start: auto }

&#x20; :where(.me-auto) { margin-inline-end: auto }



&#x20; /\* ── PADDING ── \*/

&#x20; :where(.p-0)  { padding: 0 }

&#x20; :where(.p-2)  { padding: var(--space-2) }

&#x20; :where(.p-4)  { padding: var(--space-4) }

&#x20; :where(.p-6)  { padding: var(--space-6) }

&#x20; :where(.p-8)  { padding: var(--space-8) }

&#x20; :where(.px-4) { padding-inline: var(--space-4) }

&#x20; :where(.py-4) { padding-block: var(--space-4) }

&#x20; :where(.px-6) { padding-inline: var(--space-6) }

&#x20; :where(.py-6) { padding-block: var(--space-6) }

&#x20; :where(.px-8) { padding-inline: var(--space-8) }

&#x20; :where(.py-8) { padding-block: var(--space-8) }



&#x20; /\* ── POSITION ── \*/

&#x20; :where(.static)   { position: static }

&#x20; :where(.relative) { position: relative }

&#x20; :where(.absolute) { position: absolute }

&#x20; :where(.fixed)    { position: fixed }

&#x20; :where(.sticky)   { position: sticky }

&#x20; :where(.inset-0)  { inset: 0 }

&#x20; :where(.inset-auto) { inset: auto }

&#x20; :where(.top-0)    { top: 0 }

&#x20; :where(.bottom-0) { bottom: 0 }

&#x20; :where(.left-0)   { left: 0 }

&#x20; :where(.right-0)  { right: 0 }



&#x20; /\* ── Z-INDEX ── \*/

&#x20; :where(.z-0)        { z-index: 0 }

&#x20; :where(.z-10)       { z-index: 10 }

&#x20; :where(.z-20)       { z-index: 20 }

&#x20; :where(.z-50)       { z-index: 50 }

&#x20; :where(.z-auto)     { z-index: auto }



&#x20; /\* ── OVERFLOW ── \*/

&#x20; :where(.overflow-auto)    { overflow: auto }

&#x20; :where(.overflow-hidden)  { overflow: hidden }

&#x20; :where(.overflow-clip)    { overflow: clip }

&#x20; :where(.overflow-scroll)  { overflow: scroll }

&#x20; :where(.overflow-visible) { overflow: visible }

&#x20; :where(.overflow-x-auto)  { overflow-x: auto; overflow-y: hidden }

&#x20; :where(.overflow-y-auto)  { overflow-y: auto; overflow-x: hidden }

&#x20; :where(.overflow-x-hidden){ overflow-x: hidden }

&#x20; :where(.overflow-y-hidden){ overflow-y: hidden }



&#x20; /\* ── BORDER RADIUS ── \*/

&#x20; :where(.rounded-none) { border-radius: 0 }

&#x20; :where(.rounded-sm)   { border-radius: var(--radius-sm) }

&#x20; :where(.rounded)      { border-radius: var(--radius-md) }

&#x20; :where(.rounded-lg)   { border-radius: var(--radius-lg) }

&#x20; :where(.rounded-xl)   { border-radius: var(--radius-xl) }

&#x20; :where(.rounded-2xl)  { border-radius: var(--radius-2xl) }

&#x20; :where(.rounded-full) { border-radius: var(--radius-full) }



&#x20; /\* ── SHADOW ── \*/

&#x20; :where(.shadow-none) { box-shadow: none }

&#x20; :where(.shadow-sm)   { box-shadow: var(--shadow-sm) }

&#x20; :where(.shadow)      { box-shadow: var(--shadow-md) }

&#x20; :where(.shadow-lg)   { box-shadow: var(--shadow-lg) }

&#x20; :where(.shadow-xl)   { box-shadow: var(--shadow-xl) }



&#x20; /\* ── TYPOGRAPHY ── \*/

&#x20; :where(.text-xs)   { font-size: var(--font-size-xs) }

&#x20; :where(.text-sm)   { font-size: var(--font-size-sm) }

&#x20; :where(.text-base) { font-size: var(--font-size-base) }

&#x20; :where(.text-lg)   { font-size: var(--font-size-lg) }

&#x20; :where(.text-xl)   { font-size: var(--font-size-xl) }

&#x20; :where(.text-2xl)  { font-size: var(--font-size-2xl) }

&#x20; :where(.text-3xl)  { font-size: var(--font-size-3xl) }



&#x20; :where(.font-thin)     { font-weight: 100 }

&#x20; :where(.font-light)    { font-weight: 300 }

&#x20; :where(.font-normal)   { font-weight: 400 }

&#x20; :where(.font-medium)   { font-weight: 500 }

&#x20; :where(.font-semibold) { font-weight: 600 }

&#x20; :where(.font-bold)     { font-weight: 700 }

&#x20; :where(.font-black)    { font-weight: 900 }



&#x20; :where(.italic)  { font-style: italic }

&#x20; :where(.not-italic) { font-style: normal }



&#x20; :where(.text-left)    { text-align: left }

&#x20; :where(.text-center)  { text-align: center }

&#x20; :where(.text-right)   { text-align: right }

&#x20; :where(.text-start)   { text-align: start }

&#x20; :where(.text-end)     { text-align: end }

&#x20; :where(.text-justify) { text-align: justify }



&#x20; :where(.uppercase)    { text-transform: uppercase }

&#x20; :where(.lowercase)    { text-transform: lowercase }

&#x20; :where(.capitalize)   { text-transform: capitalize }

&#x20; :where(.normal-case)  { text-transform: none }



&#x20; :where(.underline)    { text-decoration-line: underline }

&#x20; :where(.no-underline) { text-decoration: none }

&#x20; :where(.line-through) { text-decoration-line: line-through }



&#x20; :where(.leading-none)    { line-height: 1 }

&#x20; :where(.leading-tight)   { line-height: var(--line-height-tight) }

&#x20; :where(.leading-snug)    { line-height: var(--line-height-snug) }

&#x20; :where(.leading-normal)  { line-height: var(--line-height-normal) }

&#x20; :where(.leading-relaxed) { line-height: var(--line-height-relaxed) }



&#x20; :where(.tracking-tight)   { letter-spacing: var(--letter-spacing-tight) }

&#x20; :where(.tracking-normal)  { letter-spacing: 0 }

&#x20; :where(.tracking-wide)    { letter-spacing: var(--letter-spacing-wide) }

&#x20; :where(.tracking-wider)   { letter-spacing: var(--letter-spacing-wider) }

&#x20; :where(.tracking-widest)  { letter-spacing: var(--letter-spacing-widest) }



&#x20; :where(.truncate)    { white-space: nowrap; overflow: hidden; text-overflow: ellipsis }

&#x20; :where(.text-nowrap) { white-space: nowrap }

&#x20; :where(.text-wrap)   { white-space: normal }

&#x20; :where(.text-break)  { overflow-wrap: break-word; word-break: break-word }

&#x20; :where(.text-balance){ text-wrap: balance }

&#x20; :where(.text-pretty) { text-wrap: pretty }



&#x20; :where(.clamp-1) { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden }

&#x20; :where(.clamp-2) { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden }

&#x20; :where(.clamp-3) { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden }



&#x20; /\* ── COLOR ── \*/

&#x20; :where(.text-inherit)  { color: inherit }

&#x20; :where(.text-current)  { color: currentColor }

&#x20; :where(.text-muted)    { color: var(--color-text-muted) }

&#x20; :where(.text-subtle)   { color: var(--color-text-subtle) }

&#x20; :where(.text-accent)   { color: var(--color-accent) }

&#x20; :where(.text-danger)   { color: var(--color-danger-500) }

&#x20; :where(.text-success)  { color: var(--color-success-500) }

&#x20; :where(.text-warning)  { color: var(--color-warning-500) }



&#x20; /\* ── BACKGROUND ── \*/

&#x20; :where(.bg-transparent) { background: transparent }

&#x20; :where(.bg-surface)     { background: var(--color-surface) }

&#x20; :where(.bg-subtle)      { background: var(--color-bg-subtle) }

&#x20; :where(.bg-muted)       { background: var(--color-bg-muted) }

&#x20; :where(.bg-accent)      { background: var(--color-accent) }



&#x20; /\* ── OPACITY ── \*/

&#x20; :where(.opacity-0)   { opacity: 0 }

&#x20; :where(.opacity-25)  { opacity: 0.25 }

&#x20; :where(.opacity-50)  { opacity: 0.5 }

&#x20; :where(.opacity-75)  { opacity: 0.75 }

&#x20; :where(.opacity-100) { opacity: 1 }



&#x20; /\* ── CURSOR ── \*/

&#x20; :where(.cursor-auto)    { cursor: auto }

&#x20; :where(.cursor-default) { cursor: default }

&#x20; :where(.cursor-pointer) { cursor: pointer }

&#x20; :where(.cursor-wait)    { cursor: wait }

&#x20; :where(.cursor-text)    { cursor: text }

&#x20; :where(.cursor-move)    { cursor: move }

&#x20; :where(.cursor-grab)    { cursor: grab }

&#x20; :where(.cursor-not-allowed) { cursor: not-allowed }



&#x20; /\* ── POINTER EVENTS ── \*/

&#x20; :where(.pointer-none) { pointer-events: none }

&#x20; :where(.pointer-auto) { pointer-events: auto }



&#x20; /\* ── USER SELECT ── \*/

&#x20; :where(.select-none) { user-select: none }

&#x20; :where(.select-text) { user-select: text }

&#x20; :where(.select-all)  { user-select: all }



&#x20; /\* ── VISIBILITY ── \*/

&#x20; :where(.visible)   { visibility: visible }

&#x20; :where(.invisible) { visibility: hidden }



&#x20; :where(.sr-only) {

&#x20;   position: absolute !important;

&#x20;   width: 1px !important; height: 1px !important;

&#x20;   padding: 0 !important; margin: -1px !important;

&#x20;   overflow: hidden !important; clip: rect(0,0,0,0) !important;

&#x20;   white-space: nowrap !important; border: 0 !important;

&#x20; }



&#x20; /\* ── TRANSITIONS ── \*/

&#x20; :where(.transition-none)       { transition: none }

&#x20; :where(.transition)            { transition: all var(--duration-fast) var(--ease-default) }

&#x20; :where(.transition-colors)     { transition: color var(--duration-fast), background-color var(--duration-fast), border-color var(--duration-fast) }

&#x20; :where(.transition-opacity)    { transition: opacity var(--duration-fast) }

&#x20; :where(.transition-transform)  { transition: transform var(--duration-normal) var(--ease-out) }

&#x20; :where(.transition-shadow)     { transition: box-shadow var(--duration-fast) }

&#x20; :where(.duration-fast)         { transition-duration: var(--duration-fast) }

&#x20; :where(.duration-normal)       { transition-duration: var(--duration-normal) }

&#x20; :where(.duration-slow)         { transition-duration: var(--duration-slow) }

&#x20; :where(.ease-in)               { transition-timing-function: var(--ease-in) }

&#x20; :where(.ease-out)              { transition-timing-function: var(--ease-out) }

&#x20; :where(.ease-bounce)           { transition-timing-function: var(--ease-bounce) }



&#x20; /\* ── MISC ── \*/

&#x20; :where(.isolate)        { isolation: isolate }

&#x20; :where(.will-transform) { will-change: transform }

&#x20; :where(.gpu)            { transform: translateZ(0); will-change: transform }

&#x20; :where(.aspect-square)  { aspect-ratio: 1 }

&#x20; :where(.aspect-video)   { aspect-ratio: 16/9 }

&#x20; :where(.object-cover)   { object-fit: cover }

&#x20; :where(.object-contain) { object-fit: contain }

&#x20; :where(.object-center)  { object-position: center }

&#x20; :where(.resize-none)    { resize: none }

&#x20; :where(.appearance-none){ appearance: none; -webkit-appearance: none }

}

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║                 CSS MASTER GUIDE — PARTS I–VII                       ║

╠══════════════════════════════════════════════════════════════════════╣

║  129 chapters · 700+ code examples · \~25,000+ lines                 ║

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

║  ✅ Polyfills \& progressive enhancement patterns                     ║

║  ✅ Complete utility class system (200+ classes with :where())       ║

╚══════════════════════════════════════════════════════════════════════╝

```

