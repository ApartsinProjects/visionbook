# Conformance Checklist

Structural and formatting requirements for every VisionBook HTML page. Maintained by
the Meta Agent (#36/41) and enforced by the Controller (#37/42). Wave-2 (CONFORM) and
wave-4 (VALIDATE) agents fix every item directly; an audit-only report is not acceptable.

## A. Header links
Every page has the standard `chapter-header` with `header-nav` (book-title-link to root
`index.html`, toc-link to root `toc.html`), `part-label` linking the part index,
`chapter-label` linking the chapter index, and an `h1` with the section title.
Relative depths: section/chapter-index files use `../../`, part index uses `../`.

## B. Epigraph format
Every section file and chapter index opens (after the header) with
`<blockquote class="epigraph"><p>"..."</p><cite>A [Adjective] [Vision Role]</cite></blockquote>`.
1-3 sentences, witty, relevant to the section's theme, never mean-spirited.

## C. Prerequisites prose
The chapter index states in prose which chapters the reader should have read first,
with links. Section openers orient the reader ("In the previous section ... now ...").

## D. Callout classes
Only classes defined in `styles/book.css` are used. Required per SECTION:
at least one `big-picture` (immediately after the epigraph), one `key-insight`,
one `practical-example` or worked code walk-through, one `research-frontier`.
Up to two `fun-note` per section. `library-shortcut` wherever a from-scratch
implementation has a production library equivalent. Every callout has a
`<div class="callout-title">`.

## E. Code blocks and captions
Code blocks use `<pre><code class="language-python">` (or the correct language).
Every code block is followed (BELOW, after `</pre>`) by a specific, unique
`<div class="code-caption">`. Code is runnable, uses current library APIs, and
non-obvious lines carry short comments. Expected output shown where it teaches.

## F. Research frontier
At least one `research-frontier` callout per section connecting the material to
current research (2024-2026), with concrete names of methods or papers.

## G. What's Next
Every chapter index ends with a "What's Next" section (before the bibliography)
linking the next chapter and previewing how the story continues.

## H. Bibliography
Chapter index carries a `<section class="bibliography">` with 8-15 annotated,
hyperlinked entries (arXiv, official docs, GitHub), card layout, grouped by category
(Foundational Papers, Books, Tools & Libraries, Tutorials, Datasets & Benchmarks).
Real URLs only; no invented references.

## I. Navigation footer
Every section has a `chapter-nav` (prev section, chapter index, next section) and the
standard footer (edition line, copyright line with Contents link, last-updated script).
First section's prev points to the chapter index; last section's next points to the
next chapter (or next part index at part boundaries).

## J. CSS and asset completeness
Every page links `../../styles/book.css`, `../../styles/pygments.css`, KaTeX vendor
css+js (with auto-render onload), Prism theme+bundle, and `../../scripts/book.js`
(depths adjusted per location). No full inline style blocks; minimal page-specific
overrides only.

## K. Math
Math uses KaTeX delimiters `$...$` / `$$...$$`. No raw Unicode math where a formula
belongs; no LaTeX environments KaTeX cannot render. Inline math inside code comments
stays plain text.

## L. Cross-references
At least 3 inline cross-chapter hyperlinks per section, following
CROSS_REFERENCE_MAP.md arcs. Paths follow the relative path rules in BOOK_CONFIG.md
and must point at files that exist.

## M. Content structure
Main content sits in `<main class="content">`. Subsections use numbered `h2`
("1. Topic", "2. Topic") with `level-badge` spans where depth varies
(beginner/intermediate/advanced). No stretch of more than 3 paragraphs without a
visual break (callout, code, figure, table, or list).

## N. Style rules
Zero em dashes (U+2014), zero ` -- `, zero en dashes (U+2013) in prose.
Justified text comes from the stylesheet; do not override. Exercises (2-3 per
section: conceptual, coding, analysis) appear before the navigation footer.
Every section file is complete, valid HTML ending with `</html>`.
