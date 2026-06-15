# KDP Publish Folder — final upload artifacts only

This folder holds ONLY the files you upload to Amazon KDP. Everything else under
`KDP/` (the `output/`, `_mathrast/`, `_diagrast/`, `*.log` directories) is build
scratch and intermediate artifacts; do not upload from there.

## What to upload

| File | KDP slot | Notes |
|---|---|---|
| `building-vision-ai.kpf` | Manuscript (eBook content) | **Preferred.** Pre-converted Kindle package; validated by Kindle Previewer 3 (Enhanced Typesetting Supported, 0 errors, 0 quality issues). Bypasses KDP's server-side EPUB→KFX converter. |
| `building-vision-ai.epub` | Manuscript (alternative) | epubcheck 0/0/0 reflowable EPUB. KDP converts it server-side; that path produced web-CSS notices and (once) a transient KDP-internal error. Prefer the KPF. |
| `cover.jpg` | Cover | 1600x2560 baseline JPEG, meets KDP spec. |
| `KDP_LISTING.md` | (reference) | Exact title/subtitle/author/keywords/categories/description fields to paste into the web form. |
| `description.html` | Description box | Light-HTML book description (KDP accepts this markup). |

## Why KPF over EPUB

KDP accepts both, but a `.kpf` is already converted to Kindle Format X, so KDP
does not re-run its EPUB→KFX server conversion on it. The EPUB upload of this
title triggered thousands of non-blocking CSS notices (the book's `var(--…)`
custom properties evaluate to `nullem`/`nanem` on KDP's converter) and, once, a
transient KDP-side internal error. Uploading the KPF sidesteps all of that.

## Edition / freshness

These artifacts must match the current Second Edition (2026). The `.kpf` and
`.epub` here are build outputs and are git-ignored; regenerate them whenever the
book content changes:

```
# from repo root
HTML2EPUB_KATEX_OUTPUT=html python -m html2epub build .            # -> KDP/output/building-vision-ai.epub
python scripts/rasterize_math.py KDP/output/building-vision-ai.epub
python scripts/rasterize_diagrams.py KDP/output/building-vision-ai-mathimg.epub
python scripts/build_kindle.py                                      # -> KDP/output/building-vision-ai-kindle.epub
python <epub2kpf>/scripts/kpv_convert.py --epub KDP/output/building-vision-ai-kindle.epub --output KDP/output/kpf_out
# then copy the validated finals into this folder:
cp KDP/output/kpf_out/KPF/building-vision-ai-kindle.kpf KDP/publish/building-vision-ai.kpf
cp KDP/output/building-vision-ai.epub                    KDP/publish/building-vision-ai.epub
```

Confirm Kindle Previewer reports 0 errors before uploading.
