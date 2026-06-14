"""Inject Pagefind search UI into every book page.

For each HTML page (excluding vendor/templates/pagefind): add the pagefind-ui
css+js to <head> at the correct relative depth, and a <div id="search"> search
box into the chapter-header nav so book.js's PagefindUI initializer picks it up.
Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"vendor", "templates", "node_modules", ".git", "pagefind", "scripts", ".claude"}

def depth_prefix(rel):
    # number of directory levels below root
    n = len(rel.parts) - 1
    return "../" * n

def main():
    head_n = box_n = 0
    for f in ROOT.rglob("*.html"):
        rel = f.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP):
            continue
        html = f.read_text(encoding="utf-8", errors="replace")
        orig = html
        pre = depth_prefix(rel)

        # 1. head assets (idempotent)
        if "pagefind-ui.css" not in html:
            assets = (f'<link href="{pre}pagefind/pagefind-ui.css" rel="stylesheet"/>\n'
                      f'<script defer="" src="{pre}pagefind/pagefind-ui.js"></script>\n')
            if "</head>" in html:
                html = html.replace("</head>", assets + "</head>", 1)
                head_n += 1

        # 2. search box after the header-nav (idempotent); skip pages without that nav (e.g. cover)
        if 'id="search"' not in html and 'class="header-nav"' in html:
            m = re.search(r'(<nav class="header-nav">.*?</nav>)', html, re.S)
            if m:
                box = m.group(1) + '\n<div class="header-search"><div id="search"></div></div>'
                html = html[:m.start()] + box + html[m.end():]
                box_n += 1

        if html != orig:
            f.write_text(html, encoding="utf-8")
    print(f"head assets added to {head_n} pages; search box added to {box_n} pages")

if __name__ == "__main__":
    main()
