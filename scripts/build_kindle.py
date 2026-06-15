"""Build the KFX-ready Kindle EPUB from the math-rasterized EPUB.

Chain (math already rasterized to images in building-vision-ai-mathimg.epub):
  1. sanitize_epub_kindle.py   rem/px->em, font-size 0/inherit/0em fix, system-ui->sans-serif, inline-block->inline
  2. fix_kfx_svg_text_attrs    SVG <text> px->em, proprietary font-family (incl. Verdana)->generic
  3. fix_svg_style_kdp         inline SVG <style> rules -> presentation attrs
  4. fix_svg_kfx_normalize     SVG element/attr case, width/height, font shorthand, svg CSS rules
  5. strip KaTeX               remove now-unused katex.min.css + KaTeX fonts + links + manifest items

Output: KDP/output/building-vision-ai-kindle.epub
"""
import subprocess, sys, re, zipfile
from pathlib import Path

ROOT = Path("E:/Projects/VisionBook")
SK = Path("C:/Users/apart/.claude/skills/epub2kpf/scripts")
PY = "C:/Python314/python.exe"
MATHIMG = ROOT / "KDP/output/building-vision-ai-mathimg-diagrams.epub"
KINDLE_TMP = ROOT / "KDP/output/building-vision-ai-mathimg-diagrams-kindle.epub"
OUT = ROOT / "KDP/output/building-vision-ai-kindle.epub"


def run(*args):
    r = subprocess.run([PY, *map(str, args)], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(ok)")
    if r.returncode:
        print(r.stderr[-800:]); sys.exit(1)


run(ROOT / "scripts/sanitize_epub_kindle.py", MATHIMG)
run(SK / "direct_jar/fix_kfx_svg_text_attrs.py", KINDLE_TMP)
run(SK / "kdp_post_build/fix_svg_style_kdp.py", KINDLE_TMP)
run(ROOT / "scripts/fix_svg_kfx_normalize.py", KINDLE_TMP)
run(SK / "kdp_post_build/fix_strip_web_chrome.py", KINDLE_TMP)

# Append KFX-safe font-size for UA-keyword-sized elements. <sub>/<sup>/<small>
# inherit the UA `font-size:smaller` (a keyword, not em/rem) -> KFX E02208.
import io
_z = zipfile.ZipFile(KINDLE_TMP, "a")
# can't append-edit a member in place; instead rebuild the css via a second pass
_z.close()
_buf = {}
_zin = zipfile.ZipFile(KINDLE_TMP)
for _n in _zin.namelist():
    _buf[_n] = _zin.read(_n)
_zin.close()
for _n in list(_buf):
    if _n.endswith("epub_overrides.css"):
        _buf[_n] += b"\nsub,sup{font-size:0.83em}\nsmall{font-size:0.85em}\nbig{font-size:1.15em}\n"
with zipfile.ZipFile(KINDLE_TMP, "w") as _zo:
    _zi = zipfile.ZipInfo("mimetype"); _zi.compress_type = zipfile.ZIP_STORED
    _zo.writestr(_zi, b"application/epub+zip")
    for _n, _d in _buf.items():
        if _n == "mimetype":
            continue
        _zo.writestr(_n, _d, zipfile.ZIP_DEFLATED)
print("appended sub/sup/small font-size to epub_overrides.css")

# 5. strip KaTeX (dead weight now that math is images)
zin = zipfile.ZipFile(KINDLE_TMP)
drop = {n for n in zin.namelist() if "katex.min.css" in n or re.search(r"fonts/KaTeX_", n)}
with zipfile.ZipFile(OUT, "w") as zout:
    zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
    zout.writestr(zi, b"application/epub+zip")
    for name in zin.namelist():
        if name == "mimetype" or name in drop:
            continue
        data = zin.read(name); low = name.lower()
        if low.endswith((".xhtml", ".html")):
            data = re.sub(rb'<link[^>]*katex\.min\.css[^>]*>', b'', data)
        elif low.endswith(".opf"):
            data = re.sub(rb'<item[^>]*katex\.min\.css[^>]*/>', b'', data)
            data = re.sub(rb'<item[^>]*fonts/KaTeX_[^>]*/>', b'', data)
        zout.writestr(name, data, zipfile.ZIP_DEFLATED)
zin.close()
print(f"stripped {len(drop)} katex files -> {OUT.name}")

# 6. Post-process OUT: rasterize the 4 callout SVG icons to PNG (KFX reads
#    svg-as-css-background dims as "null 200" -> E06405) and embed a real TTF
#    body font (else KFX W10800 "can't find max FONT_STYLE/WEIGHT" -> stage-2 exit 1).
import io
from fontTools.ttLib import TTFont
from PIL import Image
from playwright.sync_api import sync_playwright

# 6a. build VBBody TTF set from KaTeX_Main woff2 (in MATHIMG base) if missing
ttf_dir = ROOT / "KDP/_fonts_ttf"; ttf_dir.mkdir(exist_ok=True)
KMAIN = ["KaTeX_Main-Regular", "KaTeX_Main-Bold", "KaTeX_Main-Italic", "KaTeX_Main-BoldItalic"]
if not all((ttf_dir / f"{b}.ttf").exists() for b in KMAIN):
    _src = zipfile.ZipFile(MATHIMG)
    for b in KMAIN:
        f = TTFont(io.BytesIO(_src.read(f"EPUB/fonts/{b}.woff2"))); f.flavor = None
        f.save(str(ttf_dir / f"{b}.ttf"))
    _src.close()

buf = {}
zin = zipfile.ZipFile(OUT)
for n in zin.namelist():
    buf[n] = zin.read(n)
zin.close()

# 6b. rasterize callout-*.svg icons -> png
svgicons = [n for n in buf if n.lower().endswith(".svg")]
if svgicons:
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(device_scale_factor=3, viewport={"width": 220, "height": 220})
        for n in svgicons:
            svg = buf[n].decode("utf-8", "replace")
            if "width=" not in svg[:svg.find(">")]:
                svg = re.sub(r"<svg\b", '<svg width="200" height="200"', svg, count=1)
            pg.set_content(f'<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:#fff}}</style><div style="width:200px;height:200px">{svg}</div>')
            pg.wait_for_timeout(120)
            shot = pg.locator("svg").screenshot()
            im = Image.open(io.BytesIO(shot)).convert("RGBA"); bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3])
            o = io.BytesIO(); bg.save(o, "PNG", optimize=True)
            buf[n[:-4] + ".png"] = o.getvalue()
        br.close()
    for n in svgicons:
        del buf[n]

# 6c. embed VBBody + rewrite css/opf
faces = "".join(f'@font-face{{font-family:"VBBody";font-weight:{w};font-style:{s};src:url(../fonts/{b}.ttf) format("truetype");}}'
                 for b, w, s in zip(KMAIN, ["normal", "bold", "normal", "bold"], ["normal", "normal", "italic", "italic"]))
for b in KMAIN:
    buf[f"EPUB/fonts/{b}.ttf"] = (ttf_dir / f"{b}.ttf").read_bytes()
for n in list(buf):
    if n.endswith("epub_overrides.css"):
        buf[n] += ("\n" + faces + '\nbody{font-family:"VBBody",serif}\n').encode()
    elif n.lower().endswith(".css"):
        buf[n] = re.sub(rb"(icons/callout-[\w-]+)\.svg", rb"\1.png", buf[n])
    elif n.lower().endswith(".opf"):
        items = "".join(f'<item href="fonts/{b}.ttf" id="vbf{i}" media-type="font/ttf"/>' for i, b in enumerate(KMAIN))
        buf[n] = re.sub(rb"</manifest>", items.encode() + b"</manifest>", buf[n])
        buf[n] = re.sub(rb'(<item[^>]*icons/callout-[\w-]+)\.svg("[^>]*media-type=")image/svg\+xml', rb"\1.png\2image/png", buf[n])

with zipfile.ZipFile(OUT, "w") as zout:
    zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
    zout.writestr(zi, b"application/epub+zip")
    for n, d in buf.items():
        if n != "mimetype":
            zout.writestr(n, d, zipfile.ZIP_DEFLATED)
print(f"post-processed {OUT.name}: callout icons->png, VBBody font embedded")
