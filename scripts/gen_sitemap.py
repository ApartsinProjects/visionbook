"""Generate sitemap.xml for the published book (GitHub Pages / custom domain).

Enumerates every content HTML page, maps it to its canonical URL, and writes
sitemap.xml at the repo root. index.html files become directory URLs with a
trailing slash; other pages keep their .html path. Re-run after adding pages.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://visionbook.apartsin.com/"
LASTMOD = "2026-06-15"
SKIP_DIRS = ("KDP", "vendor", "pagefind", "node_modules", "_diagnostics",
             ".git", ".html2epub_cache", "templates", "scripts")

urls = []
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT)
    if rel.parts[0] in SKIP_DIRS:
        continue
    posix = rel.as_posix()
    if posix == "index.html":
        loc = BASE
    elif posix.endswith("/index.html"):
        loc = BASE + posix[: -len("index.html")]   # keep trailing slash
    else:
        loc = BASE + posix
    urls.append(loc)

# index/landing pages first (priority), then the rest, stable
def prio(u):
    if u == BASE:
        return "1.0"
    return "0.8" if u.endswith("/") else "0.6"

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{escape(u)}</loc>")
    lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
    lines.append(f"    <priority>{prio(u)}</priority>")
    lines.append("  </url>")
lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote sitemap.xml with {len(urls)} URLs")
