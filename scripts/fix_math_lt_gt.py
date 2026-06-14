"""Escape bare < and > inside $$...$$ display-math spans so the HTML parser does
not mistake e.g. \\sum_{j<i} for an <i> tag (which breaks KaTeX delimiter pairing
and leaves raw $$ in the page). Operates only on $$...$$ spans (unambiguous math),
leaves inline $...$ and all other HTML untouched. Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "templates", "node_modules", ".git", "pagefind", "scripts"}

DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.S)

def fix_span(m):
    inner = m.group(1)
    # normalize first (idempotent), then escape every bare < and >;
    # a $$...$$ math span contains no real HTML tags.
    fixed = inner.replace("&lt;", "<").replace("&gt;", ">")
    fixed = fixed.replace("<", "&lt;").replace(">", "&gt;")
    return "$$" + fixed + "$$"

n_files = n_spans = 0
for f in ROOT.rglob("*.html"):
    if any(s in f.relative_to(ROOT).parts for s in SKIP):
        continue
    html = f.read_text(encoding="utf-8", errors="replace")
    spans = DISPLAY.findall(html)
    if not spans:
        continue
    new = DISPLAY.sub(fix_span, html)
    if new != html:
        before = sum(("<" in s or ">" in s) for s in spans)
        f.write_text(new, encoding="utf-8")
        n_files += 1
        n_spans += before
        print(f"fixed {f.relative_to(ROOT)} ({before} math spans had </> )")
print(f"\nfixed {n_files} files")
