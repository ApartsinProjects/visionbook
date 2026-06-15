"""Bisection helper to find the one KFX-unrenderable SVG (E00115).

Copies the kindle EPUB to a test EPUB, replacing every inline <svg>...</svg> with a
trivial placeholder in the chapters whose (sorted) index falls in [LO, HI). Convert
the test EPUB: if it now succeeds, the bad SVG is in the neutralized range; narrow.

Usage: python scripts/bisect_svg_epub.py <LO> <HI>   (indices into svg-chapter list)
       python scripts/bisect_svg_epub.py --list       (show svg-containing chapters)
Writes KDP/output/building-vision-ai-bisect.epub
"""
import re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "KDP/output/building-vision-ai-kindle.epub"
DST = ROOT / "KDP/output/building-vision-ai-bisect.epub"
PLACEHOLDER = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="#dddddd"/></svg>'
SVG = re.compile(r"<svg.*?</svg>", re.S)

zin = zipfile.ZipFile(SRC)
chap = sorted(n for n in zin.namelist() if n.startswith("EPUB/chapters/") and n.endswith(".xhtml"))
svg_chaps = [n for n in chap if "<svg" in zin.read(n).decode("utf-8", "replace")]

if "--list" in sys.argv:
    for i, n in enumerate(svg_chaps):
        print(i, Path(n).name[:70])
    print("total svg-containing chapters:", len(svg_chaps))
    sys.exit(0)

lo, hi = int(sys.argv[1]), int(sys.argv[2])
targets = set(svg_chaps[lo:hi])
n_neut = 0
with zipfile.ZipFile(DST, "w") as zout:
    zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
    zout.writestr(zi, b"application/epub+zip")
    for name in zin.namelist():
        if name == "mimetype":
            continue
        data = zin.read(name)
        if name in targets:
            txt = data.decode("utf-8", "replace")
            txt, c = SVG.subn(PLACEHOLDER, txt)
            n_neut += c
            data = txt.encode("utf-8")
        zout.writestr(name, data, zipfile.ZIP_DEFLATED)
zin.close()
print(f"neutralized {n_neut} svgs across chapters [{lo}:{hi}] ({len(targets)} files) -> {DST.name}")
