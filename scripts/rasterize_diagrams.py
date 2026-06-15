"""Rasterize all inline <svg> diagrams in an EPUB to JPEG images (KFX-safe).

Same rationale/infra as rasterize_math.py: KFX's SVG support is fragile (text
fonts -> E06424, case/dimension/CSS quirks -> E00115, etc.). Rendering each
diagram to an image in headless Chromium (exact fonts/CSS) and swapping in an
<img> makes the Kindle EPUB pure text+images. The web book keeps crisp SVG.

Run on building-vision-ai-mathimg.epub (math already rasterized; remaining <svg>
are diagrams with their authored inline <style>, rendered correctly by Chromium).

Usage: python scripts/rasterize_diagrams.py KDP/output/building-vision-ai-mathimg.epub
       [--limit-chapter ch_0041]
Writes <input>-diagrams.epub  (or, with --limit-chapter, just the work dir)
"""
import sys, re, zipfile, shutil, hashlib, threading, functools, http.server, socketserver
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

SRC = Path(sys.argv[1])
LIMIT = sys.argv[sys.argv.index("--limit-chapter") + 1] if "--limit-chapter" in sys.argv else None
WORK = Path("E:/Projects/VisionBook/KDP/_diagrast")
SCALE = 2.0

if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
with zipfile.ZipFile(SRC) as z:
    z.extractall(WORK)

img_dir = WORK / "EPUB" / "diagrams"
img_dir.mkdir(exist_ok=True)
chapters = sorted((WORK / "EPUB" / "chapters").glob("*.xhtml"))
if LIMIT:
    chapters = [c for c in chapters if LIMIT in c.name]

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(WORK))
httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
PORT = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}"

TAG_JS = r"""
() => {
  // outermost inline svgs only (diagrams); not nested
  const svgs = Array.from(document.querySelectorAll('svg')).filter(e => !e.parentElement.closest('svg'));
  const out = [];
  let i = 0;
  for (const el of svgs) {
    const id = '__d' + (i++);
    el.setAttribute('data-did', id);
    const r = el.getBoundingClientRect();
    out.push({id, w: Math.max(1, Math.round(r.width)), h: Math.max(1, Math.round(r.height))});
  }
  return out;
}
"""

manifest_imgs = []
total = 0
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=SCALE, viewport={"width": 1000, "height": 1400})
    for ci, chap in enumerate(chapters):
        page.goto(f"{BASE}/EPUB/chapters/{chap.name}", wait_until="load")
        page.add_style_tag(content="html,body{background:#ffffff;}")
        try:
            page.evaluate("async () => { await Promise.all([...document.fonts].map(f => f.load().catch(()=>{}))); await document.fonts.ready; }")
        except Exception:
            pass
        page.wait_for_timeout(200)
        meta = page.evaluate(TAG_JS)
        if not meta:
            continue
        repl = {}
        for m in meta:
            loc = page.locator(f'[data-did="{m["id"]}"]')
            png = img_dir / "_tmp.png"
            try:
                loc.screenshot(path=str(png))
            except Exception:
                continue
            h = hashlib.sha1(png.read_bytes()).hexdigest()[:16]
            out = img_dir / f"d_{h}.jpg"
            if not out.exists():
                im = Image.open(png).convert("RGBA")
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[3])
                bg.save(out, "JPEG", quality=88, optimize=True)
                manifest_imgs.append((out.name, f"diagimg_{h}"))
            png.unlink(missing_ok=True)
            repl[m["id"]] = (f'<img src="../diagrams/{out.name}" alt="diagram" '
                             f'style="display:block;margin:1em auto;max-width:100%;height:auto;" '
                             f'width="{m["w"]}" height="{m["h"]}"/>')
            total += 1
        page.evaluate(
            """(repl) => { for (const [id, html] of Object.entries(repl)) {
                 const el = document.querySelector('[data-did="'+id+'"]');
                 if (el) { const t=document.createElement('template'); t.innerHTML=html.trim();
                           el.replaceWith(t.content.firstChild); } } }""", repl)
        chap.write_text(page.content(), encoding="utf-8")
        print(f"[{ci+1}/{len(chapters)}] {chap.name[:46]}: {len(meta)} svg")
    browser.close()
httpd.shutdown()
print(f"\nrasterized {total} diagrams, {len(manifest_imgs)} unique images")

if LIMIT:
    print("limit mode: work dir", WORK); sys.exit(0)

# also rasterize standalone .svg icon files referenced by CSS background -> leave as-is
# (they are tiny; KFX renders them once. If they error we drop them later.)

# register diagram images, repackage
opf_path = next((WORK / "EPUB").glob("*.opf"), None) or next(WORK.rglob("*.opf"))
opf = opf_path.read_text(encoding="utf-8")
items = "".join(f'<item href="diagrams/{h}" id="{i}" media-type="image/jpeg"/>' for h, i in manifest_imgs)
opf = opf.replace("</manifest>", items + "</manifest>")
opf_path.write_text(opf, encoding="utf-8")

out_epub = SRC.with_name(SRC.stem + "-diagrams.epub")
with zipfile.ZipFile(out_epub, "w") as z:
    zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
    z.writestr(zi, b"application/epub+zip")
    for p in WORK.rglob("*"):
        if p.is_file():
            rel = p.relative_to(WORK).as_posix()
            if rel != "mimetype":
                z.write(p, rel, compress_type=zipfile.ZIP_DEFLATED)
print("wrote", out_epub)
