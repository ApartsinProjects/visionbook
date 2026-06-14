"""Downscale generated illustrations to web size and convert PNG->JPEG, then
rewrite each chapter's _specs.json filename .png -> .jpg so the embed step
references the optimized files. Keeps the repo lean (~20 MB vs ~85 MB).
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MAXSIDE = 1100
Q = 85
tot_before = tot_after = n = 0

for spec_file in sorted(ROOT.glob("part-*/module-*/images/_specs.json")):
    data = json.loads(spec_file.read_text(encoding="utf-8"))
    img_dir = spec_file.parent
    for s in data["specs"]:
        png = img_dir / s["filename"]
        if not png.exists() or not png.suffix == ".png":
            continue
        jpg = png.with_suffix(".jpg")
        tot_before += png.stat().st_size
        im = Image.open(png).convert("RGB")
        im.thumbnail((MAXSIDE, MAXSIDE), Image.LANCZOS)
        im.save(jpg, "JPEG", quality=Q, optimize=True)
        tot_after += jpg.stat().st_size
        png.unlink()
        s["filename"] = jpg.name  # rewrite spec to optimized file
        n += 1
    spec_file.write_text(json.dumps(data, indent=1), encoding="utf-8")

print(f"Optimized {n} images: {tot_before/1e6:.1f} MB -> {tot_after/1e6:.1f} MB")
