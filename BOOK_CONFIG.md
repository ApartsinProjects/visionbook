# Book Configuration

This file contains all book-specific details for the textbook production pipeline
(the `book-skills` 42-agent team). The pipeline skill and its agent definitions are
generic; this file is the only place where content specific to THIS book lives.

## Book Identity

- **Title**: Building Vision AI: From Pixels to Generative Models
- **Subtitle**: A Practitioner's Guide to Image Processing, Classical Computer Vision, Deep Learning, and Generative Vision Models
- **Target Audience**: Software engineers and students with basic Python and linear algebra (vectors, matrices, dot products). No prior computer vision experience required.
- **Output Format**: HTML chapter files linking to the shared stylesheet `styles/book.css`
- **Author/Footer line**: `© 2026 Alexander Apartsin · <a href="../../toc.html">Contents</a>` (adjust relative depth per file location)
- **Edition line for footers**: `Building Vision AI: From Pixels to Generative Models, First Edition`

## The Four-Part Arc

1. **Part I: Image Processing** (Ch 0-8): pixels, color, histograms, filtering, frequency, geometry, morphology, restoration.
2. **Part II: Classical Computer Vision** (Ch 9-17): features, matching, multi-view geometry, motion, classical recognition.
3. **Part III: Deep Learning for Computer Vision** (Ch 18-29): CNNs, transformers, detection, segmentation, self-supervision, video, 3D, deployment.
4. **Part IV: Generative Vision Models** (Ch 30-38): VAEs, GANs, diffusion, text-to-image, controllable editing, video/3D generation, evaluation and governance.

A recurring narrative thread: concepts introduced classically return learned. Convolution (Ch 3) becomes the CNN layer (Ch 19); denoising (Ch 7) becomes diffusion (Ch 33); inpainting (Ch 7) becomes generative editing (Ch 35); geometry (Ch 12-14) returns in NeRF (Ch 27). Agents should exploit these arcs for cross-references (see CROSS_REFERENCE_MAP.md).

## Visual Style

- **Stylesheet**: every HTML file links `styles/book.css` (full callout system, 22 types). Code highlighting uses Prism (vendor) plus `styles/pygments.css`. Math uses KaTeX (vendor).
- **Illustrations**: inline SVG diagrams with `<figure class="diagram">` and numbered `<figcaption>`. Generated PNG illustrations are a later wave (gemini-imagegen); do not block on them.
- **Application Examples**: `.callout.practical-example` boxes, realistic industry mini-stories.
- **Bibliographies**: card layout on the chapter index page, 8 to 15 hyperlinked annotated entries.
- **Epigraphs**: humorous quotes attributed to a fictional AI vision persona, format "A [Adjective] [Vision Role]".

### Example epigraph personas (vision-flavored)

- "A Slightly Overexposed Image Sensor"
- "A Convolution Kernel With Boundary Issues"
- "An Edge Detector Who Sees Things in Black and White"
- "A Mildly Overfit Vision Transformer"
- "A Diffusion Model, Halfway Through Denoising"
- "A GAN Discriminator Who Trusts No One"
- "A Feature Point That Refused to Match"
- "A Camera That Lost Its Calibration"
- "An Anchor Box With Attachment Problems"
- "A Latent Vector Looking for Meaning"

## HTML Head Boilerplate

Section files (`part-*/module-*/section-N.M.html`) use this head (no analytics, no pagefind yet):

```html
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Section N.M: Title. One-sentence description." name="description"/>
<title>Section N.M: Title | Building Vision AI</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../styles/pygments.css" rel="stylesheet"/>
<link href="../../vendor/katex/katex.min.css" rel="stylesheet"/>
<script defer="" src="../../vendor/katex/katex.min.js"></script>
<script defer="" onload="renderMathInElement(document.body, {
  delimiters: [
  {left: '$$', right: '$$', display: true},
  {left: '$', right: '$', display: false}
  ],
  throwOnError: false
  });" src="../../vendor/katex/contrib/auto-render.min.js"></script>
<link href="../../vendor/prism/prism-theme.css" rel="stylesheet"/>
<script defer="" src="../../vendor/prism/prism-bundle.min.js"></script>
<script defer="" src="../../scripts/book.js"></script>
```

Chapter index files (`part-*/module-*/index.html`) use the same with the same `../../` depth.
Part index files (`part-*/index.html`) use `../` depth. Root files use no prefix.

Every page carries the standard header:

```html
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Vision AI: From Pixels to Generative Models</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="part-label"><a href="../index.html">Part [ROMAN]: [PART TITLE]</a></div>
<div class="chapter-label"><a href="index.html">Chapter [N]: [CHAPTER TITLE]</a></div>
<h1>[SECTION TITLE]</h1>
</header>
```

## Chapter Map (Current Structure)

Module directory numbers equal global chapter numbers (0 to 38). The canonical
section-level breakdown lives in `toc.html` (the detailed ToC); this map is the
chapter-level source of truth.

```
Part 1: Image Processing (part-1-image-processing/)
  Ch 0: Foundations: The Python Imaging Stack       module-00-python-imaging-stack
  Ch 1: Digital Image Fundamentals                  module-01-digital-image-fundamentals
  Ch 2: Point Operations, Histograms & Thresholding module-02-point-operations-histograms
  Ch 3: Spatial Filtering & Convolution             module-03-spatial-filtering-convolution
  Ch 4: The Frequency Domain & Multi-Scale Analysis module-04-frequency-domain-multiscale
  Ch 5: Geometric Transformations & Image Warping   module-05-geometric-transformations
  Ch 6: Morphology, Binary Images & Shape           module-06-morphology-binary-shape
  Ch 7: Image Restoration & Enhancement             module-07-restoration-enhancement
  Ch 8: Tools of the Trade: Image Processing Stack  module-08-tools-of-the-trade

Part 2: Classical Computer Vision (part-2-classical-computer-vision/)
  Ch 9:  Edges, Lines & Curves                      module-09-edges-lines-curves
  Ch 10: Keypoints, Descriptors & Matching          module-10-keypoints-descriptors-matching
  Ch 11: Classical Segmentation & Grouping          module-11-classical-segmentation
  Ch 12: Camera Models & Calibration                module-12-camera-models-calibration
  Ch 13: Two-View Geometry, Stereo & Depth          module-13-two-view-stereo-depth
  Ch 14: Structure from Motion & Visual SLAM        module-14-sfm-visual-slam
  Ch 15: Motion, Optical Flow & Tracking            module-15-motion-flow-tracking
  Ch 16: Classical Recognition Pipelines            module-16-classical-recognition
  Ch 17: Tools of the Trade: Classical CV Stack     module-17-tools-of-the-trade

Part 3: Deep Learning for Computer Vision (part-3-deep-learning-for-vision/)
  Ch 18: Neural Networks & PyTorch for Vision       module-18-neural-networks-pytorch
  Ch 19: Convolutional Neural Networks              module-19-convolutional-neural-networks
  Ch 20: CNN Architectures: LeNet to ConvNeXt       module-20-cnn-architectures
  Ch 21: Training Recipes: Data, Augmentation & Transfer  module-21-training-recipes
  Ch 22: Vision Transformers                        module-22-vision-transformers
  Ch 23: Object Detection                           module-23-object-detection
  Ch 24: Segmentation: Semantic, Instance & Promptable    module-24-segmentation
  Ch 25: Self-Supervised Learning & Foundation Models     module-25-self-supervised-foundation-models
  Ch 26: Video Understanding                        module-26-video-understanding
  Ch 27: Depth, 3D Vision & Neural Scene Representations  module-27-depth-3d-neural-scenes
  Ch 28: Efficient Vision & Edge Deployment         module-28-efficient-vision-deployment
  Ch 29: Tools of the Trade: Deep Vision Stack      module-29-tools-of-the-trade

Part 4: Generative Vision Models (part-4-generative-vision-models/)
  Ch 30: Foundations of Generative Modeling         module-30-generative-foundations
  Ch 31: Autoencoders & Variational Autoencoders    module-31-autoencoders-vaes
  Ch 32: Generative Adversarial Networks            module-32-gans
  Ch 33: Diffusion Models                           module-33-diffusion-models
  Ch 34: Text-to-Image Systems                      module-34-text-to-image
  Ch 35: Controllable Generation & Image Editing    module-35-controllable-generation-editing
  Ch 36: Video, 3D & World Generation               module-36-video-3d-world-generation
  Ch 37: Evaluation, Safety & Generative Data Engines     module-37-evaluation-safety-data-engines
  Ch 38: Tools of the Trade: Generative Vision Stack      module-38-tools-of-the-trade
```

Front matter lives in `front-matter/` (F1-F7), appendices in `appendices/` (A-E),
capstone in `capstone/`. See `toc.html` for the full plan.

## Relative Path Rules

- Same part: `../module-XX-name/index.html`
- Different part: `../../part-N-name/module-XX-name/index.html`
- To book root from a section file: `../../`

## Batch Partitioning (for parallel agent runs)

- Batch A: Part 1 (Ch 0-8, 9 modules)
- Batch B: Part 2 (Ch 9-17, 9 modules)
- Batch C: Part 3 (Ch 18-29, 12 modules)
- Batch D: Part 4 (Ch 30-38, 9 modules)

Two agents must never edit the same file at overlapping times. One chapter equals
one file set; different chapters may proceed in parallel; agent waves within a
chapter run strictly in sequence.

## The "Right Tool" Principle

Every section that teaches a concept from scratch must also include a
`.callout.library-shortcut` showing the same task solved in a few lines with a modern
library (OpenCV, scikit-image, PyTorch, torchvision, timm, ultralytics, Hugging Face
diffusers, etc.). State the line-count reduction explicitly and name what the library
handles internally.

## Style Rules (non-negotiable)

1. NEVER use em dashes or double dashes anywhere. Use commas, semicolons, colons, parentheses, or separate sentences.
2. Book hierarchy terminology: Part > Chapter > Section. Never "course", "lecture", "module" in reader-facing prose (directory names keep `module-NN` for tooling compatibility).
3. Every figure, table, code block, and callout must be referenced in surrounding prose.
4. Code captions (`<div class="code-caption">`) go BELOW the code block, are specific, and are unique within a file.
5. Every chapter index ends with a "What's Next" section linking the next chapter, placed before the bibliography.
6. Use `.part-label` (not `.subtitle`) for the Part label in headers.
7. No placeholder text of any kind. Every section ships complete or is not created.
