"""Add scope="col" to <th> header cells inside <thead> that lack a scope attr (a11y)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = ("KDP", "vendor", "pagefind", "node_modules", "_diagnostics", ".git", "templates", "scripts")
THEAD = re.compile(r"<thead\b.*?</thead>", re.IGNORECASE | re.DOTALL)
TH = re.compile(r"<th\b([^>]*)>", re.IGNORECASE)

files = changed = added = 0
for f in ROOT.rglob("*.html"):
    if f.relative_to(ROOT).parts[0] in SKIP:
        continue
    text = f.read_text(encoding="utf-8", errors="replace")
    if "<thead" not in text:
        continue
    n = [0]

    def fix_thead(m):
        block = m.group(0)
        def fix_th(t):
            attrs = t.group(1)
            if re.search(r'\bscope\s*=', attrs, re.I):
                return t.group(0)
            n[0] += 1
            return f"<th scope=\"col\"{attrs}>"
        return TH.sub(fix_th, block)

    new = THEAD.sub(fix_thead, text)
    if n[0]:
        f.write_text(new, encoding="utf-8")
        changed += 1
        added += n[0]

print(f"added scope=col to {added} thead <th> across {changed} files")
