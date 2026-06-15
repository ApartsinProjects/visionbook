"""Flexible SVG bisection: neutralize inline <svg> in svg-chapter index range [LO:HI).
Usage: python scripts/bisect2.py <input.epub> <LO> <HI> <out.epub>
       python scripts/bisect2.py <input.epub> --list
"""
import re, sys, zipfile
from pathlib import Path

PH='<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10"><rect width="10" height="10" fill="#dddddd"/></svg>'
SVG = re.compile(r"<svg.*?</svg>", re.S)

src = Path(sys.argv[1])
zin = zipfile.ZipFile(src)
chap = sorted(n for n in zin.namelist() if n.startswith("EPUB/chapters/") and n.endswith(".xhtml"))
svg_chaps = [n for n in chap if "<svg" in zin.read(n).decode("utf-8", "replace")]

if "--list" in sys.argv:
    for i, n in enumerate(svg_chaps):
        print(i, Path(n).name[:70])
    print("total:", len(svg_chaps))
    sys.exit(0)

lo, hi = int(sys.argv[2]), int(sys.argv[3])
dst = Path(sys.argv[4])
targets = set(svg_chaps[lo:hi])
n = 0
with zipfile.ZipFile(dst, "w") as zout:
    zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
    zout.writestr(zi, b"application/epub+zip")
    for name in zin.namelist():
        if name == "mimetype":
            continue
        data = zin.read(name)
        if name in targets:
            txt = data.decode("utf-8", "replace")
            txt, c = SVG.subn(PH, txt); n += c
            data = txt.encode("utf-8")
        zout.writestr(name, data, zipfile.ZIP_DEFLATED)
zin.close()
print(f"neutralized {n} svgs in [{lo}:{hi}] -> {dst.name}")
