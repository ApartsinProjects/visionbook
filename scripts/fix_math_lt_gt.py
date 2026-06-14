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
SENT = "\x00DISPLAYMATH\x00"
# inline $...$ on a single line; guarded below to TeX-looking content only
INLINE = re.compile(r"\$([^$\n]+?)\$")
TEX_HINT = re.compile(r"[\\_^{}]")

def _escape(inner):
    fixed = inner.replace("&lt;", "<").replace("&gt;", ">")  # normalize (idempotent)
    return fixed.replace("<", "&lt;").replace(">", "&gt;")

def fix_span(m):
    # a $$...$$ math span contains no real HTML tags
    return "$$" + _escape(m.group(1)) + "$$"

def fix_inline(m):
    inner = m.group(1)
    # only treat as math (and only act) when it looks like TeX and has < or >;
    # this skips currency like "$5" / "$10" which have no TeX hint.
    if ("<" in inner or ">" in inner) and TEX_HINT.search(inner):
        return "$" + _escape(inner) + "$"
    return m.group(0)

n_files = n_spans = 0
for f in ROOT.rglob("*.html"):
    if any(s in f.relative_to(ROOT).parts for s in SKIP):
        continue
    html = f.read_text(encoding="utf-8", errors="replace")
    # display $$...$$ first, then mask them so inline $...$ does not cross $$
    new = DISPLAY.sub(fix_span, html)
    masked = DISPLAY.sub(lambda m: SENT, new)
    masked = INLINE.sub(fix_inline, masked)
    # restore display spans in order
    disp = DISPLAY.findall(new)
    it = iter(disp)
    new = re.sub(re.escape(SENT), lambda m: "$$" + next(it) + "$$", masked)
    if new != html:
        f.write_text(new, encoding="utf-8")
        n_files += 1
        print(f"fixed {f.relative_to(ROOT)}")
print(f"\nfixed {n_files} files")
