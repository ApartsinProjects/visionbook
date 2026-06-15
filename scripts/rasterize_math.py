"""Rasterize all KaTeX math in the Kindle EPUB to JPEG images (KFX-safe).

KFX / Enhanced Typesetting rejects KaTeX's HTML math (display:table-cell ->
E02015, inline-block -> E00204, px -> E02208). Rendering each math element to an
image removes ALL KaTeX CSS from KFX's view. The web book keeps crisp inline math;
this only rewrites the Kindle EPUB copy.

Approach: extract the EPUB, load each chapter in headless Chromium (Playwright) so
KaTeX + its fonts render exactly, screenshot every .katex / .katex-display element,
replace it with an <img> (inline math keeps baseline via vertical-align), then
repackage the EPUB and register the new images in the OPF manifest.

Usage: python scripts/rasterize_math.py KDP/output/building-vision-ai-kindle.epub [--limit-chapter ch_0033]
"""
import sys, re, zipfile, shutil, hashlib, threading, functools, http.server, socketserver
from pathlib import Path
from playwright.sync_api import sync_playwright

SRC = Path(sys.argv[1])
LIMIT = None
if "--limit-chapter" in sys.argv:
    LIMIT = sys.argv[sys.argv.index("--limit-chapter") + 1]

ROOT = Path("E:/Projects/VisionBook")
WORK = ROOT / "KDP" / "_mathrast"
SCALE = 2.5
BASE_PX = 16.0

# --- 1. extract ---
if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
with zipfile.ZipFile(SRC) as z:
    z.extractall(WORK)

# serve WORK over HTTP (Chromium blocks file:// font loads as cross-origin)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(WORK))
httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
PORT = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASEURL = f"http://127.0.0.1:{PORT}"

chap_dir = WORK / "EPUB" / "chapters"
math_dir = WORK / "EPUB" / "math"
math_dir.mkdir(exist_ok=True)
chapters = sorted(chap_dir.glob("*.xhtml"))
if LIMIT:
    chapters = [c for c in chapters if LIMIT in c.name]

# JS: tag each outermost math element, return metadata
TAG_JS = r"""
() => {
  const out = [];
  const displays = Array.from(document.querySelectorAll('.katex-display'));
  const inlines = Array.from(document.querySelectorAll('.katex')).filter(e => !e.closest('.katex-display'));
  let i = 0;
  for (const el of displays) {
    const id = '__m' + (i++);
    el.setAttribute('data-mid', id);
    el.style.padding = '0.5em 0.3em';         // avoid clipping tall fractions/operators
    el.style.overflow = 'visible';
    const r = el.getBoundingClientRect();
    out.push({id, type:'display', w:r.width, h:r.height, depthEm:0});
  }
  for (const el of inlines) {
    const id = '__m' + (i++);
    el.setAttribute('data-mid', id);
    el.style.overflow = 'visible';
    const r0 = el.getBoundingClientRect();
    const big = r0.height > 34;               // tall (fraction/sum) -> treat as block
    el.style.display = 'inline-block';        // so vertical padding actually grows the box
    el.style.padding = big ? '0.5em 0.3em' : '0.15em 0.08em';
    const r = el.getBoundingClientRect();
    let depth = 0;
    const strut = el.querySelector('.strut');
    if (strut) {
      const va = getComputedStyle(strut).verticalAlign;
      const px = parseFloat(va);
      if (!isNaN(px)) depth = -px;            // strut VA is negative = depth below baseline
    }
    out.push({id, type: big ? 'display' : 'inline', w:r.width, h:r.height, depthEm: depth/16.0});
  }
  return out;
}
"""

manifest_imgs = []  # (href, id)
total = 0

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=SCALE, viewport={"width": 900, "height": 1400})
    for ci, chap in enumerate(chapters):
        page.goto(f"{BASEURL}/EPUB/chapters/{chap.name}", wait_until="load")
        page.add_style_tag(content="html,body{background:#ffffff;}")
        try:
            page.evaluate("""async () => {
                await Promise.all([...document.fonts].map(f => f.load().catch(() => {})));
                await document.fonts.ready;
            }""")
        except Exception:
            pass
        page.wait_for_timeout(200)
        meta = page.evaluate(TAG_JS)
        if not meta:
            continue
        repl = {}  # id -> img html
        for m in meta:
            loc = page.locator(f'[data-mid="{m["id"]}"]')
            png = math_dir / f"_tmp.png"
            try:
                loc.screenshot(path=str(png))
            except Exception:
                continue
            data = png.read_bytes()
            h = hashlib.sha1(data).hexdigest()[:16]
            out = math_dir / f"m_{h}.jpg"
            if not out.exists():
                # convert png->jpg white bg via PIL
                from PIL import Image
                im = Image.open(png).convert("RGBA")
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[3])
                bg.save(out, "JPEG", quality=90, optimize=True)
                manifest_imgs.append((f"math/{out.name}", f"mathimg_{h}"))
            png.unlink(missing_ok=True)
            hEm = m["h"] / BASE_PX / SCALE * SCALE  # rect already CSS px
            hEm = m["h"] / BASE_PX
            if m["type"] == "display":
                wpx = m["w"]; hpx = m["h"]
                repl[m["id"]] = (f'<img src="../math/{out.name}" alt="math" '
                                 f'style="display:block;margin:0.8em auto;max-width:100%;height:auto;" '
                                 f'width="{int(wpx)}" height="{int(hpx)}"/>')
            else:
                va = -m["depthEm"]
                repl[m["id"]] = (f'<img src="../math/{out.name}" alt="math" '
                                 f'style="height:{hEm:.3f}em;vertical-align:{va:.3f}em;" '
                                 f'class="mathi"/>')
            total += 1
        # apply replacements in DOM, then serialize
        page.evaluate(
            """(repl) => {
                for (const [id, html] of Object.entries(repl)) {
                  const el = document.querySelector('[data-mid="'+id+'"]');
                  if (el) { const t=document.createElement('template'); t.innerHTML=html.trim();
                            el.replaceWith(t.content.firstChild); }
                }
            }""", repl)
        html = page.content()
        # ensure xhtml-ish: write back
        chap.write_text(html, encoding="utf-8")
        print(f"[{ci+1}/{len(chapters)}] {chap.name[:50]}: {len(meta)} math")
    browser.close()

httpd.shutdown()
print(f"\nrasterized {total} math elements, {len(manifest_imgs)} unique images")

if LIMIT:
    print("limit mode: not repackaging. work dir:", WORK)
    sys.exit(0)

# --- register math images in the OPF manifest ---
opf_path = next((WORK / "EPUB").glob("*.opf"), None) or next(WORK.rglob("*.opf"))
opf = opf_path.read_text(encoding="utf-8")
items = "".join(
    f'<item href="math/{Path(h).name}" id="{i}" media-type="image/jpeg"/>'
    for h, i in manifest_imgs
)
opf = opf.replace("</manifest>", items + "</manifest>")
opf_path.write_text(opf, encoding="utf-8")

# --- repackage as EPUB (mimetype stored first) ---
out_epub = SRC.with_name(SRC.stem + "-mathimg.epub")
files = [p for p in WORK.rglob("*") if p.is_file() and p.name not in ("_mathimgs.json",)]
with zipfile.ZipFile(out_epub, "w") as z:
    zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
    z.writestr(zi, b"application/epub+zip")
    for p in files:
        rel = p.relative_to(WORK).as_posix()
        if rel == "mimetype":
            continue
        z.write(p, rel, compress_type=zipfile.ZIP_DEFLATED)
print("wrote", out_epub)
