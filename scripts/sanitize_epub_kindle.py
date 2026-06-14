"""Post-build Kindle CSS sanitizer for the EPUB (does NOT touch web source).

KFX / Enhanced Typesetting rejects `rem` units ("Unsupported/Unknown unit : rem",
codes E05204/E02211) and non-em/rem font-size units (E02208). The web book uses
rem correctly; this rewrites a COPY of the EPUB so the Kindle build uses em.

Rewrites inside .css and .xhtml/.html ZIP entries:
  - <number>rem            -> <number>em   (1rem ~= 1em at default root size)
  - font-size:<n>px        -> font-size:<n/16>em
  - display:inline-block in table contexts is left for a later pass if needed.

Rebuilds a valid EPUB (mimetype stored first). Usage:
  python scripts/sanitize_epub_kindle.py KDP/output/building-vision-ai.epub
Writes <name>-kindle.epub next to it.
"""
import re
import sys
import zipfile
from pathlib import Path

src = Path(sys.argv[1])
dst = src.with_name(src.stem + "-kindle.epub")

REM = re.compile(r"(?<![\w.])(\d*\.?\d+)rem\b")
PXFONT = re.compile(r"(font-size\s*:\s*)(\d*\.?\d+)px", re.I)

def px_to_em(m):
    return f"{m.group(1)}{float(m.group(2))/16:.3f}em"

IB = re.compile(r"display\s*:\s*inline-block", re.I)

def sanitize(text):
    n_rem = len(REM.findall(text))
    text = REM.sub(lambda m: m.group(1) + "em", text)
    text, n_px = PXFONT.subn(px_to_em, text)
    # KFX E00204: inline-block unsupported inside tables. Kindle reflows, so
    # plain inline is a safe global substitute (badges/chips stay inline).
    text = IB.sub("display:inline", text)
    return text, n_rem, n_px

zin = zipfile.ZipFile(src, "r")
names = zin.namelist()
tot_rem = tot_px = 0
entries = []  # (name, bytes, compress)
for name in names:
    data = zin.read(name)
    if name.endswith((".css", ".xhtml", ".html", ".htm")):
        txt = data.decode("utf-8", errors="replace")
        txt, nr, npx = sanitize(txt)
        tot_rem += nr; tot_px += npx
        data = txt.encode("utf-8")
    entries.append((name, data))
zin.close()

# mimetype MUST be first and STORED (uncompressed), no extra fields
with zipfile.ZipFile(dst, "w") as zout:
    if "mimetype" in dict(entries):
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        zout.writestr(zi, b"application/epub+zip")
    for name, data in entries:
        if name == "mimetype":
            continue
        zout.writestr(name, data, zipfile.ZIP_DEFLATED)

print(f"wrote {dst.name}: rewrote {tot_rem} rem -> em, {tot_px} px font-sizes -> em")
