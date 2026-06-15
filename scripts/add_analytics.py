"""Inject the Google Analytics (gtag.js) tag into the <head> of every book HTML page.

Idempotent: skips any file that already contains the measurement ID. Placed as
high in <head> as possible per Google's guidance. Web-only: the EPUB/KPF build
drops <script> chrome, so this does not reach the ebook.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GA_ID = "G-FQJHVSGYWS"
SNIPPET = (
    '<!-- Google tag (gtag.js) -->\n'
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
    '<script>\n'
    '  window.dataLayer = window.dataLayer || [];\n'
    '  function gtag(){dataLayer.push(arguments);}\n'
    "  gtag('js', new Date());\n"
    f"  gtag('config', '{GA_ID}');\n"
    '</script>\n'
)
SKIP_DIRS = ("KDP", "vendor", "pagefind", "node_modules", "_diagnostics", ".git", ".html2epub_cache")
HEAD_RE = re.compile(r"<head\b[^>]*>", re.IGNORECASE)

changed = skipped = 0
targets = list(ROOT.rglob("*.html"))
for f in targets:
    rel = f.relative_to(ROOT)
    if rel.parts and rel.parts[0] in SKIP_DIRS:
        continue
    text = f.read_text(encoding="utf-8", errors="replace")
    if GA_ID in text:
        skipped += 1
        continue
    m = HEAD_RE.search(text)
    if not m:
        print("  no <head>:", rel)
        continue
    new = text[: m.end()] + "\n" + SNIPPET + text[m.end():]
    f.write_text(new, encoding="utf-8")
    changed += 1

print(f"injected GA tag into {changed} files, skipped {skipped} (already had it)")
