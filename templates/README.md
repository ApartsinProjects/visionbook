# Page Templates

Standard templates for creating new pages in the textbook. All styling comes from `../styles/book.css` (single source of truth). No inline styles should be used.

## Templates

### `part-index.html`
For part landing pages (e.g., `part-9-safety-strategy/index.html`).
- Stylesheet path: `../styles/book.css`
- Nav links: `../index.html` and `../toc.html`
- Contains: part-overview, big-picture callout, chapter-cards, whats-next, footer

### `chapter-index.html`
For chapter landing pages (e.g., `part-9-safety-strategy/module-32-safety-ethics-regulation/index.html`).
- Stylesheet path: `../../styles/book.css`
- Nav links: `../../index.html` and `../../toc.html`
- Contains: epigraph, illustration, overview, big-picture, practical-examples, fun-notes, objectives, prereqs, sections-list, whats-next, chapter-nav, bibliography, footer

### `section.html`
For section content pages (e.g., `section-32.1.html`).
- Stylesheet path: `../../styles/book.css`
- Nav links: `../../index.html` and `../../toc.html`
- Contains: epigraph, big-picture, content headings, callouts (all 10 types), code blocks, figures, exercises, section-nav, footer

## Mandatory Elements (all pages)

1. `<header class="chapter-header">` (never bare `<header>`)
2. `<nav class="header-nav">` with `class="book-title-link"` and `class="toc-link"`
3. `<main class="content">` wrapper (never `<div class="container">`)
4. `<footer><p>Fifth Edition, 2026 &middot; <a href="RELATIVE/toc.html">Contents</a></p></footer>`

## Callout Types (10 total)

All callouts use: `<div class="callout TYPE" title="TOOLTIP"><div class="callout-title">TITLE</div>CONTENT</div>`

| Type | CSS Class | Title Text | Tooltip |
|------|-----------|------------|---------|
| Big Picture | `big-picture` | Big Picture | Big Picture: Core concept overview |
| Key Insight | `key-insight` | Key Insight | Key Insight: Important takeaway |
| Note | `note` | Note | Note: Additional context |
| Warning | `warning` | Warning | Warning: Common pitfall |
| Practical Example | `practical-example` | Practical Example: TITLE | Practical Example: Hands-on demonstration |
| Fun Fact | `fun-note` | Fun Fact | Fun Fact: Interesting trivia |
| Research Frontier | `research-frontier` | Research Frontier | Research Frontier: Cutting-edge development |
| Algorithm | `algorithm` | Algorithm: NAME | Algorithm: Step-by-step procedure |
| Tip | `tip` | Tip: TITLE | Tip: Helpful suggestion |
| Library Shortcut | `library-shortcut` | Library Shortcut: TOOL in Practice | Library Shortcut: Production tool recommendation |
| Exercise | `exercise` | Exercise N.M.K: Title BADGE | Exercise: Practice problem |

## Exercise Badges

`<span class="exercise-type TYPE">Label</span>` where TYPE is: `conceptual`, `coding`, `analysis`, or `discussion`.

## Bibliography Format

Use `<div class="bib-entry-card">` (never `<ol class="bib-list">`):
```html
<div class="bib-entry-card">
    <div class="bib-ref">Author. "Title." (Year). <a href="URL" target="_blank">link</a></div>
    <div class="bib-annotation">Annotation text.</div>
</div>
```

## Cross-References

Links to other chapters/sections use: `<a class="cross-ref" href="RELATIVE_PATH">visible text</a>`

## Rules

- No inline styles on any element (links, headings, divs, figures, images)
- No em dashes or double dashes in text; use commas, semicolons, colons, or parentheses
- All paths are relative (never absolute)
- Book title: "Building Conversational AI with LLMs and Agents"
- Footer: "Fifth Edition, 2026"
