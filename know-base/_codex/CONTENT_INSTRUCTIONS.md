# Content Instructions for Section Fragments

Use these instructions whenever writing or reviewing a Markdown fragment.

## Base Prompt

```text
Write high-quality English technical guide content for the given software engineering section.

Use the provided volume title, chapter title, section ID, and section title exactly.
The audience is experienced software engineers, senior engineers, tech leads, and architects.

The content must be practical, precise, and self-contained.
Explain what the concept means, why it matters, how to apply it, what trade-offs exist, and how to review real work against it.

Use Markdown only.
Do not change the section ID or title.
Do not add references to sections that are not present in the JSON.
Do not include filler, motivational text, vague best practices, or repeated boilerplate.
```

## Required Structure

Each section fragment must use this content structure:

```markdown
#### <section-id> <section-title>

##### Purpose

##### Core Ideas

##### Practical Guidance

##### Trade-offs

##### Examples

##### Common Mistakes

##### Review Checklist
```

## Writing Standard

Good content should:

- define the topic in concrete engineering terms;
- explain the operational impact of the topic;
- include realistic code, architecture, process, or design examples when useful;
- name trade-offs instead of pretending there is one universal answer;
- connect guidance to maintainability, correctness, security, performance, reliability, or team scale;
- use concise paragraphs and focused bullet lists;
- avoid repeating the same sentences across sections.

## Section Depth

Default target:

```text
500-900 words per section
```

Shorter sections are acceptable only when the topic is narrow and still complete. Complex sections may be longer, but they should remain focused.

## Example Quality Bar

Weak:

```text
Good names are important because they make code easier to read.
```

Strong:

```text
A variable name should encode the role the value plays in the current scope, not its implementation type. `retryDeadline` is more useful than `date`, because it tells the reader how the value constrains behavior and where changing it may affect control flow.
```

## Review Checklist

Before marking a fragment as `reviewed`, confirm:

- the section title and ID match the JSON exactly;
- the section is useful without needing another document;
- advice is specific enough to apply in code review or design review;
- examples support the guidance instead of decorating it;
- trade-offs are explicit;
- there are no placeholders;
- there is no obvious hallucinated standard, tool, or citation;
- the tone is professional, direct, and technical.

## Anti-Patterns

Do not write:

- empty definitions;
- generic listicles;
- long introductions;
- duplicated wording from neighboring sections;
- unsupported numeric claims;
- fake citations;
- broad philosophical essays;
- content that ignores the chapter context.

