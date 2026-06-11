# Cross-Reference Map

Progressive-depth concepts that appear in multiple chapters at different levels.
Cross-Reference (#13), Narrative Continuity (#14), and ENRICH-wave agents use these
arcs to place inline links. Each arc reads "introduced -> deepened -> transformed".

## The book's signature arcs (classical concept returns learned)

| Concept | Introduced | Deepened | Transformed |
|---|---|---|---|
| Convolution | Ch 3 (kernels, filtering) | Ch 19 (learnable conv layers) | Ch 33 (U-Net denoiser inside diffusion) |
| Denoising | Ch 7 (Gaussian, NLM) | Ch 31 (denoising autoencoders) | Ch 33 (diffusion = learned iterative denoising) |
| Inpainting | Ch 7 (classical PDE/exemplar) | Ch 24 (masks from segmentation) | Ch 35 (generative inpainting/outpainting) |
| Super-resolution | Ch 7 (classical) | Ch 28 (efficient SR at the edge) | Ch 33/34 (diffusion upscalers) |
| Image pyramids / multi-scale | Ch 4 (Gaussian/Laplacian) | Ch 20, Ch 24 (feature hierarchies, FPN-style fusion) | Ch 33 (latent multi-resolution) |
| Edges & gradients | Ch 3 (Sobel), Ch 9 (Canny) | Ch 19 (learned first-layer filters resemble edge detectors) | Ch 35 (edge maps as ControlNet conditions) |
| Features & descriptors | Ch 10 (SIFT/ORB) | Ch 25 (learned representations replace hand-crafted) | Ch 34 (CLIP embeddings as universal descriptors) |
| Segmentation | Ch 11 (watershed, graph cuts) | Ch 24 (FCN to SAM) | Ch 35 (masks drive editing) |
| Geometry & cameras | Ch 5 (homographies), Ch 12-14 (calibration, stereo, SfM) | Ch 27 (NeRF/splats need poses; COLMAP feeds NeRF) | Ch 36 (3D generation, world models) |
| Optical flow & motion | Ch 15 (LK, Horn-Schunck) | Ch 26 (RAFT, deep tracking) | Ch 36 (temporal consistency in video generation) |
| Histograms & statistics | Ch 2 | Ch 21 (normalization statistics, augmentation) | Ch 37 (distribution metrics: FID compares feature statistics) |
| Latent spaces | Ch 30 (concept) | Ch 31 (VAE), Ch 32 (GAN latents) | Ch 33 (latent diffusion), Ch 35 (inversion for editing) |
| Attention | Ch 22 (ViT self-attention) | Ch 24 (mask transformers), Ch 26 (video transformers) | Ch 33/34 (cross-attention conditioning on text) |
| Evaluation metrics | Ch 1 (PSNR/SSIM) | Ch 23/24 (IoU, mAP, mIoU) | Ch 37 (FID, KID, CLIPScore, human eval) |
| Data augmentation | Ch 5 (geometric transforms) | Ch 21 (augmentation policies) | Ch 37 (generative models as data engines) |
| Noise models | Ch 7 | Ch 21 (label noise) | Ch 33 (noise schedules) |
| Camera/sensor pipeline | Ch 1 (ISP) | Ch 28 (edge cameras) | Appendix E (hardware guide) |
| Thresholding & binarization | Ch 2 | Ch 6 (morphology consumes binary maps) | Ch 24 (per-pixel logits thresholded at inference) |
| Transfer learning | Ch 21 | Ch 25 (foundation backbones) | Ch 34/35 (fine-tuning generators, LoRA) |
| Tracking | Ch 15 (Kalman, mean-shift) | Ch 26 (learned MOT) | Ch 36 (object permanence in world models) |
| World models & simulation | Ch 15 (motion models, Kalman state estimation) | Ch 26 (video understanding), Ch 31 (latent dynamics need VAE latents) | Ch 36.5-36.8 (RSSM/Dreamer, generative simulators, JEPA) |
| Self-supervision to prediction | Ch 25 (DINO, MAE, contrastive) | Ch 25.6 (foundation models) | Ch 36.7 (JEPA: predict in representation space, decoder-free) |
| Scores & energies | Ch 30.4 (EBMs, score matching, Langevin) | Ch 33.3 (score SDEs) | Ch 33.5 (flow matching as the modern descendant) |

## Linking rules

- When a chapter first touches an arc, link FORWARD ("we will meet this again when ...")
  sparingly (max 1-2 per section) and link BACKWARD generously ("as built in Section X.Y").
- Use the relative path rules in BOOK_CONFIG.md; link to the chapter index or a specific
  section file, never to a heading anchor that does not exist.
- Tools-of-the-Trade chapters (8, 17, 29, 38) link back to every chapter in their part.
