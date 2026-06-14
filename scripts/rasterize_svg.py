"""Rasterize the inline <svg> containing a marker substring in a source HTML file
to a PNG (via Edge headless) and replace it with an <img>. KFX cannot render some
SVG features (patterns, mixed tspan/text); rasterizing is the faithful KFX-safe fix.
Improves both web and EPUB (PNG looks identical). Idempotent-ish (re-run regenerates).

Usage: python scripts/rasterize_svg.py <html_file> <marker_substring> <out_basename>
"""
import re, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

src = Path(sys.argv[1]); marker = sys.argv[2]; base = sys.argv[3]
t = src.read_text(encoding="utf-8")
svg = None
for m in re.finditer(r"<svg.*?</svg>", t, re.S):
    if marker in m.group(0):
        svg, span = m.group(0), m.span(); break
if not svg:
    print("marker not found in any svg"); sys.exit(1)

vb = re.search(r'view[bB]ox="0 0 ([\d.]+) ([\d.]+)"', svg)
W, H = (int(float(vb.group(1))), int(float(vb.group(2)))) if vb else (860, 400)
sized = re.sub(r"<svg", f'<svg width="{W}" height="{H}"', svg, count=1)
tmp_html = ROOT / "KDP" / "_rast.html"
tmp_png = ROOT / "KDP" / "_rast.png"
tmp_html.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}</style>' + sized, encoding="utf-8")
subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                "--force-device-scale-factor=2", f"--window-size={W},{H}",
                f"--screenshot={tmp_png}", tmp_html.resolve().as_uri()],
               check=True, timeout=120, capture_output=True)

img_dir = src.parent / "images"; img_dir.mkdir(exist_ok=True)
im = Image.open(tmp_png).convert("RGB"); im.thumbnail((1200, 1200), Image.LANCZOS)
outp = img_dir / (base + ".jpg")
im.save(outp, "JPEG", quality=88, optimize=True)

al = re.search(r'aria-label="([^"]*)"', svg)
alt = al.group(1) if al else base.replace("-", " ")
img = f'<img src="images/{outp.name}" alt="{alt}" style="max-width:100%;height:auto;display:block;margin:1em auto;" loading="lazy"/>'
src.write_text(t[:span[0]] + img + t[span[1]:], encoding="utf-8")
tmp_html.unlink(missing_ok=True); tmp_png.unlink(missing_ok=True)
print(f"rasterized -> {outp.name} ({im.size}); replaced svg in {src.name}")
