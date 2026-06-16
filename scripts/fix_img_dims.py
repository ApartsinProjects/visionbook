"""Add width/height attributes to <img> tags that lack them (a11y / layout-shift).

For each book HTML page, find <img> tags missing width or height, resolve the
local src to a file, read its real pixel dimensions with Pillow, and inject the
attributes. Skips data: URIs, remote URLs, and tags that already have both.
"""
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = ("KDP", "vendor", "pagefind", "node_modules", "_diagnostics", ".git", "templates", "scripts")
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
dim_cache = {}

def dims(img_path):
    if img_path not in dim_cache:
        try:
            with Image.open(img_path) as im:
                dim_cache[img_path] = im.size
        except Exception:
            dim_cache[img_path] = None
    return dim_cache[img_path]

changed_files = added = 0
for f in ROOT.rglob("*.html"):
    if f.relative_to(ROOT).parts[0] in SKIP_DIRS:
        continue
    text = f.read_text(encoding="utf-8", errors="replace")
    n_local = [0]

    def repl(m):
        tag = m.group(0)
        if re.search(r'\bwidth\s*=', tag) and re.search(r'\bheight\s*=', tag):
            return tag
        src = re.search(r'\bsrc\s*=\s*"([^"]+)"', tag)
        if not src:
            return tag
        url = src.group(1)
        if url.startswith(("http", "data:", "//")):
            return tag
        img_path = (f.parent / url).resolve()
        wh = dims(img_path)
        if not wh:
            return tag
        w, h = wh
        add = ""
        if not re.search(r'\bwidth\s*=', tag):
            add += f' width="{w}"'
        if not re.search(r'\bheight\s*=', tag):
            add += f' height="{h}"'
        n_local[0] += 1
        return tag[:4] + add + tag[4:]  # insert right after "<img"

    new = IMG_RE.sub(repl, text)
    if n_local[0]:
        f.write_text(new, encoding="utf-8")
        changed_files += 1
        added += n_local[0]

print(f"added width/height to {added} <img> tags across {changed_files} files")
