# Scout report - Building Vision AI - application readiness - 2026-06-18

Scope: audit whether the book can serve as a main reference for leading researchers and developers in ten application areas. This is a read-only report and improvement plan. No book content was changed.

## Executive Verdict

The book is strong as a general graduate-to-practitioner reference for image processing, classical vision, deep learning vision, 3D, generative vision, evaluation, and deployment. It is not yet sufficient as the main reference for leading researchers in all ten application areas without targeted domain supplements.

The largest issue is not missing core vision theory. The issue is application-specific body of knowledge: domain data formats, benchmarks, regulatory constraints, sensor physics, production workflows, recent foundation models, and failure modes that define research practice in each application.

Priority summary:

| Rank | Application | Readiness as main reference | Main gap |
|---:|---|---|---|
| 1 | Industrial inspection and quality control | High after one focused anomaly chapter | Dedicated industrial anomaly detection and line integration |
| 2 | AR, 3D reconstruction, and spatial computing | High after one frontier refresh | Feed-forward 3D reconstruction and spatial-computing workflow |
| 3 | Creative AI and generative media | High | Current image and video model landscape, product evaluation |
| 4 | Robotics and embodied AI | Medium-high | VLA policies, robot data, sim-to-real, RGB-D manipulation |
| 5 | Autonomous vehicles and ADAS | Medium | BEV, occupancy, sensor fusion, planning, safety cases |
| 6 | Medical imaging AI | Medium | Modalities, clinical workflow, DICOM/NIfTI, medical FMs, regulation |
| 7 | Scientific imaging and computational microscopy | Medium | Bioimage-specific models, microscopy restoration, lab QC |
| 8 | Document, retail, and visual search systems | Medium | Document VLMs, OCR-free and OCR-augmented pipelines, retrieval serving |
| 9 | Security, biometrics, and surveillance analytics | Low-medium | Biometrics, FRTE-style evaluation, privacy law, liveness, ReID protocols |
| 10 | Remote sensing and Earth observation | Low | Geospatial sensors, CRS, multispectral/SAR, EO foundation models |

## Cross-cutting Strengths Already Present

The book already has the right foundation spine:

| Need | Existing coverage |
|---|---|
| Raw pixels, sensors, color, compression | Ch. 0 to 1, 3 to 7 |
| Segmentation, detection, tracking | Ch. 11, 23, 24, 15, 26 |
| Geometry, calibration, SLAM, depth | Ch. 12 to 14, Ch. 27 |
| Foundation models and self-supervision | Ch. 22, 25, 34, 36 |
| Generative vision and synthetic data | Ch. 30 to 38, especially 33 to 37 |
| Deployment and tooling | Ch. 8, 17, 28, 29, 38, Appendix E |
| Evaluation and safety | Ch. 37, Appendix B |
| Capstone integration | Capstone defect-inspection project |

Evidence from local keyword probes: defect 171 hits, robot 291, SLAM 254, NeRF 192, Gaussian splatting 50, FLUX 82, OCR 38, microscopy 27, medical 66. Thin areas: remote sensing 0, geospatial 0, biometric 1, visual search 2, scientific imaging 1, MedSAM 1.

## Recent Frontier Signals Used for Scouting

The scout used recent literature and project signals, including:

- SAM 2 extends promptable segmentation to images and video with streaming memory and reports stronger video segmentation with fewer interactions than prior approaches: https://arxiv.org/abs/2408.00714
- Medical SAM 2 adapts SAM 2 to 2D and 3D medical segmentation framed as tracking: https://arxiv.org/abs/2408.00874
- MedSAM2 reports promptable 3D medical image and video segmentation using more than 455,000 3D image-mask pairs and 76,000 frames: https://arxiv.org/html/2504.03600v1
- DINOv3 is positioned by Meta as a scaled self-supervised universal vision backbone, including satellite imagery: https://ai.meta.com/blog/dinov3-self-supervised-vision-model/ and https://arxiv.org/abs/2508.10104
- VGGT directly predicts camera parameters, depth, point maps, and tracks from one to many views in under a second: https://arxiv.org/abs/2503.11651
- Prithvi-EO 2.0 is an open geospatial foundation model trained on global HLS satellite imagery: https://research.ibm.com/publications/prithvi-eo-an-open-access-geospatial-foundation-model-advancing-earth-science-through-global-collaboration
- TerraMind is presented as an any-to-any multimodal Earth-observation foundation model: https://geoawesome.com/foundation-models-for-eo-how-to-start/
- Autonomous-driving world-model surveys now organize the field around future physical-world generation, behavior planning, and prediction-planning interaction: https://arxiv.org/html/2501.11260v2
- Industrial anomaly detection has moved toward training-free, few-shot, VLM-based, diffusion-based, and 3D point-cloud anomaly methods: https://github.com/m-3lab/awesome-industrial-anomaly-detection and https://link.springer.com/article/10.1007/s10462-025-11287-7
- DocVLM integrates OCR-derived layout and text signals into VLMs for document understanding: https://openaccess.thecvf.com/content/CVPR2025/html/Nacson_DocVLM_Make_Your_VLM_an_Efficient_Reader_CVPR_2025_paper.html
- Segment Anything for Microscopy adapts SAM to multidimensional microscopy segmentation and tracking: https://www.nature.com/articles/s41592-024-02580-4
- FluoResFM is a 2026 fluorescence microscopy restoration foundation model: https://www.nature.com/articles/s41467-026-70307-4
- FLUX.1 Kontext unifies image generation and editing via flow matching with text and image context: https://arxiv.org/abs/2506.15742

## Application Audits and Improvement Plan

### 1. Medical Imaging AI

Specific applications: MRI tumor segmentation, CT organ segmentation, chest X-ray triage, retinal vessel analysis, computational pathology, synthetic medical data.

Current coverage:

- Strong generic segmentation, restoration, denoising, super-resolution, synthetic data, evaluation, and responsible deployment.
- Some medical examples exist, but they are scattered.
- Search evidence: medical 66, radiology 2, pathology 15, MedSAM 1, biomed 5.

Readiness: Medium. The book can teach the vision methods, but not yet serve as a main reference for medical-imaging researchers.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | DICOM, NIfTI, Hounsfield units, voxel spacing, windowing, slice thickness | Medical images are not ordinary RGB files | Add Section 1.6 or Appendix B medical-data subsection |
| P1 | 2D versus 2.5D versus 3D segmentation | Central design choice in radiology and pathology | Ch. 24 after semantic and instance segmentation |
| P1 | Medical segmentation FMs: MedSAM, Medical SAM 2, MedSAM2, nnU-Net as baseline | This is now the practical starting point | Ch. 24 or Ch. 25 application case |
| P1 | Clinical validation: patient-level splits, site shift, calibration, uncertainty, reader studies | Leading medical AI work is judged by clinical validity, not just Dice | Ch. 37 plus Appendix B |
| P2 | MONAI, TorchIO, SimpleITK, whole-slide pathology tooling | Developer workflow is domain-specific | Ch. 29 tools addendum |
| P2 | Regulatory and privacy workflow: PHI, de-identification, audit logs, FDA SaMD, EU MDR | Deployment depends on governance | Ch. 37.6 domain box |

Concrete plan:

1. Add a new chapter-level case study: "Medical Imaging AI: From Voxels to Clinical Validation".
2. Add a table mapping modalities to tensor conventions: X-ray, CT, MRI, ultrasound, WSI pathology, OCT.
3. Add a hands-on lab using MONAI or SimpleITK: load a 3D volume, resample spacing, window intensities, run a 3D segmentation baseline, evaluate Dice and Hausdorff distance.
4. Add a benchmark map: BraTS, MSD, KiTS, CheXpert, MIMIC-CXR, NIH ChestXray14, CAMELYON, TCGA pathology.
5. Add bibliography entries for Medical SAM 2, MedSAM2, medical foundation-model reviews, MONAI, nnU-Net, and clinical validation papers.

### 2. Autonomous Vehicles and ADAS

Specific applications: lane and curb detection, pedestrian and vehicle detection, multi-camera BEV perception, occupancy prediction, visual localization, scenario generation, driver monitoring.

Current coverage:

- Strong: camera geometry, calibration, stereo, optical flow, SLAM, detection, segmentation, video, deployment, world models.
- Existing content mentions driving and BEV, but it is not organized as an autonomous-driving reference.
- Search evidence: autonomous 29, driving 96, BEV 25, occupancy 7.

Readiness: Medium. Excellent foundations, but missing the modern autonomous-driving stack as a coherent system.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | BEV perception taxonomy: Lift-Splat-Shoot, BEVFormer lineage, multi-view temporal fusion | Core modern AV perception representation | Ch. 23 or new Ch. 26 addendum |
| P1 | Occupancy networks and 4D occupancy forecasting | Replacing pure box perception in planning-facing stacks | Ch. 24 or Ch. 36 |
| P1 | Sensor fusion: camera, LiDAR, radar, IMU, HD maps | Real AV systems are not camera-only | Ch. 12 to 14 and Appendix E |
| P1 | Planning-facing evaluation: nuScenes, Waymo, Argoverse, closed-loop simulation, safety metrics | AV research is judged by downstream planning and safety | Appendix B and Ch. 37 |
| P2 | World models for driving: GAIA-1, DriveDreamer-style simulation, future BEV or occupancy generation | Current frontier for synthetic scenarios and planning | Ch. 36.6 and 36.8 |
| P2 | Driver monitoring and cabin vision | A practical ADAS area not covered as a case | Ch. 26 application box |

Concrete plan:

1. Add a full section: "BEV and Occupancy Perception for Autonomous Driving".
2. Add a diagram: camera views to features, depth distribution, BEV grid, temporal fusion, occupancy head, planner interface.
3. Add a lab: train or run a small BEV-style perception model on a tiny nuScenes sample or synthetic multi-camera toy dataset.
4. Add an evaluation table: 2D AP, 3D AP, NDS, mIoU occupancy, planning L2, collision rate, closed-loop score.
5. Add an AV world-model case study in Ch. 36 connecting generated futures to planning risk.

### 3. Robotics and Embodied AI

Specific applications: warehouse robots, visual navigation, grasping, mobile manipulation, drones, humanoid perception, robot inspection.

Current coverage:

- Strong for geometry, SLAM, depth, detection, segmentation, tracking, deployment, world models.
- The book has robot examples, but the foundation-policy frontier is only partially present.
- Search evidence: robot 291, grasp 10, drone 69.

Readiness: Medium-high. It can serve perception researchers well, but not yet leading embodied-AI researchers.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Vision-language-action models: RT-2, OpenVLA, pi0-style policies, GR00T-style robot FMs | Central 2024 to 2026 robotics frontier | Ch. 36 or new embodied-AI section |
| P1 | Robot data: Open X-Embodiment, teleoperation, action spaces, proprioception | VLA research is data and action-interface driven | Appendix B and Ch. 36 |
| P1 | Hand-eye calibration, RGB-D, depth-camera artifacts, tactile fusion | Practical manipulation depends on robot-specific sensing | Ch. 12 and Appendix E |
| P2 | Sim-to-real, domain randomization, synthetic data for robotics | Links generative vision to embodied deployment | Ch. 37.3 and Ch. 36 |
| P2 | ROS2, Isaac Sim, LeRobot, robot evaluation protocols | Developer workflow is outside generic CV tooling | Tools chapter addendum |

Concrete plan:

1. Add Section 36.9: "Vision-Language-Action Models for Robots".
2. Add a diagram: observation tokens, language instruction, action chunking, proprioception, policy head, closed-loop execution.
3. Add a lab or notebook: visual servoing or pick-place with a simulated RGB-D camera, plus a tiny imitation-learning baseline.
4. Add a case study contrasting classical perception stack versus VLA policy stack for warehouse picking.
5. Add bibliography for RT-2, OpenVLA, pi0, GR00T, LeRobot, Open X-Embodiment, Dreamer robotics uses.

### 4. Industrial Inspection and Quality Control

Specific applications: PCB inspection, weld inspection, surface defects, fastener inspection, pharmaceutical packaging, textile defects, metrology.

Current coverage:

- This is the strongest application fit. The book has morphology, measurement, restoration, classification, defect examples, and a full defect-inspection capstone.
- Search evidence: industrial 52, defect 171, anomaly 14, MVTec 3.

Readiness: High after one focused anomaly-detection expansion.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Industrial anomaly detection taxonomy: reconstruction, feature memory, one-class, few-shot, VLM-guided | Core of modern inspection research | Ch. 24 or new Ch. 29 section |
| P1 | Benchmarks: MVTec AD, MVTec AD 2, VisA, BTAD, DAGM, KolektorSDD | Researchers need shared evaluation references | Appendix B and capstone |
| P1 | PatchCore, PaDiM, FastFlow, WinCLIP, training-free VLM anomaly detection | Practical baselines missing | Ch. 25 and Ch. 29 |
| P2 | Lighting, optics, telecentric lenses, line-scan cameras, strobing | Industrial success often begins before the model | Appendix E |
| P2 | Production quality systems: false reject rate, escape rate, SPC, traceability | Metrics differ from academic AP | Ch. 37 and capstone |

Concrete plan:

1. Add a new section: "Industrial Visual Anomaly Detection".
2. Extend the capstone with a branch: supervised defect classifier versus unsupervised anomaly detector versus synthetic defect augmentation.
3. Add a benchmark table and metric mapping: AUROC, pixel AUROC, PRO, FPR at target recall, escape rate.
4. Add a practical optics box: when to spend money on lighting instead of a larger model.
5. Add a production-pattern callout on per-SKU calibration and drift monitoring.

### 5. Remote Sensing and Earth Observation

Specific applications: crop monitoring, wildfire detection, flood mapping, building footprint extraction, land-cover classification, change detection, disaster response.

Current coverage:

- Core segmentation, classification, registration, restoration, and foundation-model ideas transfer.
- Domain-specific coverage is almost absent.
- Search evidence: remote sensing 0, geospatial 0, satellite 20.

Readiness: Low. This needs a real domain supplement.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Multispectral and hyperspectral imagery, SAR, LiDAR, DEMs | EO data is not RGB photography | New appendix or application chapter |
| P1 | Geospatial coordinate systems, tiling, reprojection, cloud masks, temporal stacks | Developer workflow is geospatial first | Tools chapter addendum |
| P1 | EO foundation models: Prithvi-EO, TerraMind, Satlas, Clay, DOFA, DINOv3 satellite variant | Current frontier and practical baseline set | Ch. 25 and Appendix B |
| P1 | Benchmarks: BigEarthNet, SpaceNet, xView, SEN12MS, GEO-Bench, DynamicEarthNet | Main reference must direct evaluation | Appendix B |
| P2 | Change detection, weak labels, label noise, domain shift across geography and season | Central research problems | Ch. 24 and Ch. 37 |

Concrete plan:

1. Add a new application chapter or appendix: "Earth Observation and Geospatial Vision".
2. Add a data-model table: RGB aerial, Sentinel-2 multispectral, Landsat HLS, SAR, hyperspectral, DEM.
3. Add a lab: load Sentinel-2 tiles with rasterio or stackstac, mask clouds, tile into patches, run land-cover segmentation.
4. Add a foundation-model section covering Prithvi-EO 2.0 and TerraMind, with what changes relative to natural-image FMs.
5. Add a figure: pixel grid versus map grid, CRS, geotransform, tiling pyramid, temporal cube.

### 6. Security, Biometrics, and Surveillance Analytics

Specific applications: face recognition, liveness detection, person re-identification, multi-camera tracking, license plate recognition, deepfake detection, provenance.

Current coverage:

- Strong for detection, tracking, recognition foundations, deepfakes, watermarking, provenance, and evaluation principles.
- Weak for biometrics-specific research and governance.
- Search evidence: biometric 1, face recognition 1, re-identification 12, surveillance 3.

Readiness: Low-medium. The book covers adjacent CV, not the biometrics body of knowledge.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Face recognition pipeline: detection, alignment, embeddings, verification versus identification | Foundation of biometric systems | Ch. 16 or Ch. 25 application section |
| P1 | Evaluation: ROC, DET, FAR, FRR, FNIR, FPIR, thresholding by operating point, NIST FRTE | Biometrics has specialized metrics | Ch. 37 |
| P1 | Presentation attack detection and liveness | Critical deployment requirement | Ch. 16 or Ch. 37 |
| P1 | ReID protocols: Market-1501, MSMT17, multi-camera tracking, privacy-preserving ReID | Needed for surveillance analytics | Ch. 15 and Ch. 26 |
| P1 | Governance: consent, bias, demographic differentials, law enforcement constraints | A main reference cannot omit this | Ch. 37.6 |

Concrete plan:

1. Add a section: "Biometrics and Re-Identification: Recognition Under Governance".
2. Add a metric box translating classification metrics into biometric operating points.
3. Add a case study: deploying face verification versus deploying person ReID in a privacy-constrained facility.
4. Add bibliography entries for NIST FRTE, National Academies facial recognition governance, recent biometrics foundation-model surveys, and ReID surveys.
5. Add a clear warning that generic face-recognition demos are not deployment-grade biometric systems.

### 7. AR, 3D Reconstruction, and Spatial Computing

Specific applications: AR object anchoring, room scanning, photogrammetry, neural scene capture, 3D Gaussian splatting, spatial maps, digital twins.

Current coverage:

- Strong: camera calibration, PnP, SfM, SLAM, stereo, depth, NeRF, 3D Gaussian splatting, DUSt3R, MASt3R, VGGT mentions.
- Search evidence: Gaussian splatting 50, NeRF 192, DUSt3R 18, MASt3R 21.

Readiness: High after a frontier refresh and workflow consolidation.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Feed-forward 3D reconstruction workflow: DUSt3R, MASt3R, VGGT, pose-free splatting | Current frontier is moving beyond COLMAP-first pipelines | Ch. 27 |
| P1 | Spatial computing product workflow: capture, reconstruct, compress, stream, interact | Researchers and developers need end-to-end systems | Ch. 27 or Appendix E |
| P2 | Mobile constraints: ARCore/ARKit, depth APIs, anchors, relocalization, lighting estimation | Practical AR differs from offline 3D reconstruction | Ch. 14 and Appendix E |
| P2 | 3D asset formats and compression: splat formats, mesh extraction, Gaussian compression | Deployment detail for spatial apps | Ch. 28 or Ch. 38 |

Concrete plan:

1. Add Section 27.7: "Feed-Forward 3D Reconstruction and Spatial Capture".
2. Add a comparison table: COLMAP+MVS, NeRF, 3DGS, DUSt3R, MASt3R, VGGT, pose-free splatting.
3. Add a lab: reconstruct a small scene with COLMAP and compare against a feed-forward model output, focusing on failure modes.
4. Add a figure: capture path from phone video to camera poses, point maps, splats, relocalization, AR overlay.
5. Add bibliography entries for VGGT, FreeSplatter, DUSt3R, MASt3R, 3DGS compression, ARCore/ARKit docs.

### 8. Creative AI and Generative Media Tools

Specific applications: text-to-image systems, image editing, inpainting, style workflows, video generation, branded asset generation, synthetic-data studios.

Current coverage:

- Very strong: VAEs, GANs, diffusion, flow matching, guidance, latent diffusion, text-to-image, controllable generation, editing, video, 3D, tools, hosted APIs, evaluation, provenance.
- Search evidence: text-to-image 249, FLUX 82, video generation 24.

Readiness: High. This is one of the book's best-supported application areas.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Current model landscape refresh: SD3.5, FLUX variants, FLUX.1 Kontext, OpenAI/Google video APIs, open video models | Model names and capabilities move quickly | Ch. 34 to 38 |
| P1 | Product evaluation: prompt suites, brand consistency, editing preservation, latency, cost, safety filters | Developer teams need product-level metrics | Ch. 37 and Ch. 38 |
| P2 | Rights management and provenance workflow in creative pipelines | Production teams need compliance | Ch. 37.5 and 37.6 |
| P2 | Multi-step workflow testing for ComfyUI and API pipelines | Needed for maintainable production pipelines | Ch. 38.2 |

Concrete plan:

1. Add a 2026 model-landscape table in Ch. 34.3 and Ch. 38.3.
2. Add a creative-tool evaluation rubric: instruction adherence, identity preservation, edit locality, temporal consistency, cost per accepted asset.
3. Add a practical lab: build a controlled editing workflow and score it with a small prompt suite.
4. Add a production-pattern callout: when to use closed APIs, open inference providers, or self-hosted FLUX-class models.

### 9. Document, Retail, and Visual Search Systems

Specific applications: OCR cleanup, invoice extraction, document VQA, product recognition, multimodal product search, fashion recommendation, barcode and label inspection.

Current coverage:

- Strong for document cleanup, OCR preprocessing, embeddings, CLIP, classification, retrieval-adjacent concepts, and deployment.
- Weak for modern document VLMs and production retrieval serving.
- Search evidence: OCR 38, document 1057, retail 27, visual search 2.

Readiness: Medium.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Document AI model families: LayoutLM lineage, Donut, DocVLM, OCR-free versus OCR-augmented VLMs | Current document systems are multimodal, not just OCR | Ch. 25 or new application section |
| P1 | Retrieval systems: CLIP/SigLIP embeddings, vector indexes, hybrid search, hard negatives, catalog metadata | Main topic for retail visual search | Ch. 25 and Ch. 29 |
| P1 | Evaluation: field-level F1, table extraction, retrieval recall@k, nDCG, online A/B metrics | Application metrics differ from CV benchmarks | Ch. 37 and Appendix B |
| P2 | Production: deduplication, moderation, cold start, color/style attributes, variant handling | Retail systems live or die on data ops | Ch. 28 or Ch. 29 |

Concrete plan:

1. Add a section: "Document and Product Vision Systems".
2. Add a diagram: pixels to OCR or VLM, layout tokens, extracted fields, embeddings, vector search, re-ranking.
3. Add a lab: build product visual search with CLIP or SigLIP embeddings and FAISS, evaluate recall@k and nDCG.
4. Add a document AI case: invoice extraction with OCR-preprocess baseline, OCR-free model, and OCR-augmented VLM.
5. Add bibliography entries for Donut, LayoutLMv3, DocVLM, SigLIP, ecommerce embedding models.

### 10. Scientific Imaging and Computational Microscopy

Specific applications: cell segmentation, organoid segmentation, particle tracking, fluorescence denoising, microscopy super-resolution, material microstructure analysis.

Current coverage:

- Strong for restoration, denoising, deconvolution, segmentation, morphology, tracking, synthetic data, and metrics.
- Weak for bioimage-specific data, tools, and foundation models.
- Search evidence: microscopy 27, cell 545, scientific imaging 1.

Readiness: Medium.

Missing topics:

| Priority | Gap | Why it matters | Suggested placement |
|---|---|---|---|
| P1 | Bioimage model families: Cellpose, StarDist, ilastik, u-SAM, Cellpose-SAM, VISTA-2D | These are practical baselines for researchers | Ch. 24 and Ch. 29 |
| P1 | Microscopy restoration FMs: FluoResFM-style multi-task restoration | Restoration is a core microscopy bottleneck | Ch. 7 and Ch. 25 |
| P1 | Microscopy-specific failure modes: uneven illumination, PSF, photobleaching, z-stacks, anisotropy, batch effects | Generic natural-image assumptions fail | Ch. 1, Ch. 7, Ch. 24 |
| P2 | Scientific metrics and reproducibility: object-level F1, tracking lineage, biological endpoint validation | Pixel metrics alone are insufficient | Ch. 37 |
| P2 | Tooling: napari, bioimage.io, image.sc ecosystem | Developer workflow is domain-specific | Ch. 29 tools addendum |

Concrete plan:

1. Add a focused section: "Bioimage Analysis and Computational Microscopy".
2. Add a lab: segment nuclei with Cellpose or u-SAM, measure region properties, compare pixel Dice with object-level biological counts.
3. Extend Ch. 7 with a microscopy restoration box: denoising, deconvolution, super-resolution, PSF, and validation traps.
4. Add a figure: microscope acquisition pipeline, sample, optics, sensor, PSF, restoration, segmentation, measurement, biological claim.
5. Add bibliography entries for Cellpose, StarDist, Segment Anything for Microscopy, FluoResFM, bioimage.io, napari.

## Proposed Book-Level Improvements

### A. Add an Application Reference Layer

Create a new appendix: "Appendix G: Application Reference Maps".

For each application, include:

- canonical tasks
- input data types and formats
- minimum methods from the book
- domain-specific methods not covered elsewhere
- datasets and benchmarks
- metrics
- failure modes
- recommended reading path through the book
- current frontier models and tools

This is the fastest way to make the book usable as a main reference without bloating every core chapter.

### B. Add Five Domain Deep-Dive Sections

Highest-value additions:

1. Earth Observation and Geospatial Vision
2. Medical Imaging AI
3. Industrial Visual Anomaly Detection
4. Vision-Language-Action Models for Robotics
5. Document and Product Visual Search

These five close the largest gaps across the ten application areas.

### C. Add Benchmark Tables to Appendix B

Appendix B should gain domain tables:

- Medical: BraTS, MSD, KiTS, CheXpert, MIMIC-CXR, CAMELYON, TCGA
- Autonomous driving: KITTI, Cityscapes, BDD100K, nuScenes, Waymo, Argoverse, OpenLane, Occ3D-style occupancy sets
- Robotics: Open X-Embodiment, RLBench, RoboMimic, ManiSkill, Meta-World, LIBERO
- Industrial: MVTec AD, MVTec AD 2, VisA, BTAD, DAGM, KolektorSDD
- EO: BigEarthNet, SpaceNet, xView, SEN12MS, DynamicEarthNet, GEO-Bench
- Biometrics and surveillance: LFW, IJB-C, MegaFace, NIST FRTE, Market-1501, MSMT17, MOTChallenge
- Document and retail: RVL-CDIP, FUNSD, DocVQA, PubTables-1M, DeepFashion, Product1M
- Microscopy: BBBC, Cell Tracking Challenge, TissueNet, LIVECell, MoNuSeg, Cellpose datasets

### D. Add Domain Metrics Callouts

Add a recurring callout type: "Metric Shift".

Examples:

- Medical: Dice is not enough; report Hausdorff distance, calibration, site shift, patient-level validation.
- AV: AP is not enough; report planning impact and closed-loop safety.
- Industrial: AUROC is not enough; report escape rate at a fixed false reject rate.
- Biometrics: accuracy is not enough; report FAR/FRR at operating thresholds and demographic differentials.
- Retrieval: top-1 accuracy is not enough; report recall@k, nDCG, latency, and catalog drift.

### E. Add Domain Tooling Boxes

Add compact tooling boxes:

- Medical: MONAI, SimpleITK, TorchIO, pydicom, nnU-Net
- EO: rasterio, xarray, stackstac, geemap, TorchGeo, GeoPandas
- Robotics: ROS2, Isaac Sim, LeRobot, OpenVLA stack, Open X-Embodiment loaders
- Industrial: anomalib, MVTec loaders, OpenCV metrology, line-scan camera SDK notes
- Document and retail: PaddleOCR, Docling, LayoutParser, FAISS, Milvus, Elasticsearch vector search
- Microscopy: napari, Cellpose, StarDist, ilastik, bioimage.io

## Implementation Order

| Phase | Scope | Outcome |
|---:|---|---|
| 1 | Appendix G application maps | Immediate positioning boost for all ten areas |
| 2 | Earth observation, medical, industrial anomaly sections | Closes the three most visible reference gaps |
| 3 | Robotics VLA and document visual search sections | Adds current frontier relevance for developers |
| 4 | Benchmark tables and metric-shift callouts | Raises research-grade usefulness |
| 5 | Bibliography and code/tool refresh | Makes the plan defensible and practical |
| 6 | Optional capstone variants | Turns the core capstone into a family of domain projects |

## No-Edit Status

This report is an audit and improvement plan only. No application chapters, sections, bibliography entries, code, or HTML content were modified.
