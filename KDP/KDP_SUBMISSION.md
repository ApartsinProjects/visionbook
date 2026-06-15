# KDP Submission Package — Building Vision AI

Everything needed to publish on Amazon Kindle Direct Publishing (kdp.amazon.com).
Structured metadata: `KDP/metadata/metadata.yaml`. Validated deliverables below.

## Deliverables (validated)

| File | What | Status |
|---|---|---|
| `KDP/output/building-vision-ai.epub` | Reflowable EPUB 3 manuscript (26.4 MB, 277 chapters, 244 illustrations, server-rendered KaTeX math) | **epubcheck 5.3.0: 0 fatals / 0 errors / 0 warnings** |
| `KDP/output/building-vision-ai.kpf` | Kindle-native KPF (83 MB; math + diagrams rasterized to images, embedded text font) | **Kindle Previewer 3: Enhanced Typesetting Supported, 0 errors, 0 quality issues** |
| `KDP/cover/cover_kdp.jpg` | Ebook cover, 1600x2560 baseline JPEG | OK (see cover note) |

Either file can be uploaded to KDP. The EPUB is the lighter, source-faithful manuscript (crisp vector math/diagrams); the KPF is the Kindle-native package validated end-to-end by Kindle Previewer with Enhanced Typesetting on.

Rebuild the EPUB any time: `HTML2EPUB_KATEX_OUTPUT=html python -m html2epub build .`
Re-validate: run epubcheck 5.3.0 (Java) on the .epub.

Rebuild the KPF: `python scripts/rasterize_math.py KDP/output/building-vision-ai.epub` then
`python scripts/rasterize_diagrams.py KDP/output/building-vision-ai-mathimg.epub` then
`python scripts/build_kindle.py`, then convert with
`python <epub2kpf>/scripts/kpv_convert.py --epub KDP/output/building-vision-ai-kindle.epub --output KDP/output/kpf_out`.

## KDP "Kindle eBook Details" page — paste these

- **Language:** English
- **Book Title:** Building Vision AI
- **Subtitle:** From Pixels to Generative Models
- **Series:** (none)
- **Edition number:** 1
- **Author:** Alexander Apartsin
- **Contributor:** Yehudit Aperstein (role: Author)
- **Description:** use the `description` field in `metadata.yaml` (under 4000 chars; KDP allows light HTML such as `<b>`, `<br>`, lists if you want emphasis).
- **Publishing rights:** "I own the copyright and I hold the necessary publishing rights."
- **Primary audience / explicit content:** No.
- **Keywords (7):**
  1. computer vision OpenCV scikit-image image processing
  2. deep learning CNN vision transformer PyTorch tutorial
  3. object detection segmentation YOLO SAM DETR
  4. diffusion models Stable Diffusion text-to-image generation
  5. NeRF 3D Gaussian splatting structure from motion
  6. self-supervised foundation models CLIP DINO MAE
  7. generative AI synthetic data evaluation FID
- **Categories (up to 3 BISAC):**
  1. COMPUTERS / Computer Vision & Pattern Recognition (COM016000)
  2. COMPUTERS / Artificial Intelligence / General (COM004000)
  3. COMPUTERS / Machine Theory (COM018000)

## KDP "Kindle eBook Content" page

- **Manuscript:** upload `KDP/output/building-vision-ai.epub` (reflowable; KDP accepts EPUB directly).
- **Cover:** upload `KDP/cover/cover_kdp.jpg` (or use the KDP Cover Creator).
- **DRM:** recommendation — disable (DRM is irreversible and adds nothing for a technical book). Author's choice.
- **Page-read / preview:** after upload, open the KDP Previewer and spot-check a math-heavy chapter (e.g. 33 Diffusion), a code chapter (e.g. 19 CNNs), and an illustrated chapter; confirm math, code, and figures render.

## KDP "Pricing" page (author decisions)

- **Royalty plan:** 70% (list price USD 2.99-9.99) or 35% (outside that band). A ~600-page technical book typically lists 9.99-19.99; 70% applies only up to 9.99.
- **Territories:** All territories (worldwide rights).
- **Price:** set per your strategy; KDP auto-converts to other marketplaces.

## Cover note

`cover_kdp.jpg` is **1600 x 2560 px (1.6:1), baseline RGB JPEG, 300 dpi** — exactly
KDP's ideal ebook cover spec (longest side 2560 >= the recommended 2500, well within
the 1000-10000 px range, under 50 MB). No further cover work needed.

## Optional: KPF via epub2kpf (only if KDP's EPUB converter complains)

KDP accepts the validated EPUB directly. If you prefer a Kindle-native KPF (KPV
qualitychecks 0 errors, the Kindle post-build patches for named entities / cover
classifier), run the `epub2kpf` skill on `KDP/output/building-vision-ai.epub`. That is
the only remaining step beyond this package, and it is needed only if the direct EPUB
upload is rejected.

## What is NOT auto-decided here

Pricing, royalty band, DRM, and territories are deliberate author choices left blank
in `metadata.yaml`. ISBN is optional (KDP assigns a free ASIN); supply your own ISBN
only if you want one that carries across stores.
