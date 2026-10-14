# RT-DocLayout: Real-Time End-to-End Document Layout Analysis with Reading Order in the Wild

> **arXiv**: [2606.23344v1](https://arxiv.org/abs/2606.23344v1) ｜ **发布日期**: 2026-06-22 ｜ **分类**: cs.CV ｜ **页数**: 16

## 摘要

Accurate document layout analysis remains a critical bottleneck for document parsing systems, due to the intricate coupling among heterogeneous document layout elements, geometric distortions (\eg, paper warping and bending, perspective variations), and reading order within diverse layout structures. Existing approaches typically rely on fragmented multi-stage pipelines or computationally heavy generative Transformer architectures, leading to error propagation and limited efficiency. In this paper, we present RT-DocLayout, a highly efficient end-to-end framework for document layout analysis, designed as a front-end for document parsing tasks. The proposed model unifies classification, detection, pixel-level segmentation, and reading order prediction for layout elements within a single 33M-parameter architecture. Built upon the RT-DETR, our key contribution is a unified multi-task formulation within a single query-based decoder that simultaneously classifies, regresses bounding box, generates masks, and constructs relationship to reason reading order. By jointly learning geometric and structural representations, RT-DocLayout introduces multi-task optimization that substantially improves robustness under real-world document distortions. Extensive experiments on public benchmarks demonstrate state-of-the-art performance in document layout analysis while maintaining real-time inference speed(132.1 FPS). When coupled with downstream OCR engines, RT-DocLayout significantly improves full-document reconstruction quality, providing a scalable and practical foundation for real-world document intelligence systems.

---

## 正文

RT-DocLayout: Real-Time End-to-End Document Layout
Analysis with Reading Order in the Wild
Cheng Cui, Tingquan Gao, Xueqing Wang, Changda Zhou,
Hongen Liu, Ting Sun, Yubo Zhang, Zelun Zhang, Jiaxuan Liu,
Manhui Lin, Yue Zhang, Suyin Liang, Yiqing Xiang, Yi Liu
PaddlePaddle Team, Baidu Inc.
paddleocr@baidu.com
Abstract
Accurate document layout analysis remains a critical bottleneck for
document parsing systems, due to the intricate coupling among het-
erogeneous document layout elements, geometric distortions (e.g., pa-
per warping and bending, perspective variations), and reading order
within diverse layout structures. Existing approaches typically rely on
fragmented multi-stage pipelines or computationally heavy generative
Transformer architectures, leading to error propagation and limited
efficiency.
In this paper, we present RT-DocLayout, a highly efficient end-to-end
framework for document layout analysis, designed as a front-end for
document parsing tasks. The proposed model unifies classification,
detection, pixel-level segmentation, and reading order prediction for
layout elements within a single 33M-parameter architecture. Built upon
the RT-DETR, our key contribution is a unified multi-task formulation
within a single query-based decoder that simultaneously classifies, re-
gresses bounding box, generates masks, and constructs relationship to
reason reading order.
By jointly learning geometric and structural representations, RT-
DocLayout introduces multi-task optimization that substantially im-
proves robustness under real-world document distortions. Extensive
experiments on public benchmarks demonstratestate-of-the-art per-
formance in document layout analysis while maintaining real-time
inference speed(132.1 FPS). When coupled with downstream OCR en-
gines, RT-DocLayout significantly improves full-document reconstruc-
tion quality, providing a scalable and practical foundation for real-world
document intelligence systems.
RT-DocLayout is released in PaddleOCR under the name PP-DocLayoutV3. RT-DocLayout is the name used in this
academic publication, while PP-DocLayoutV3 is the name adopted in the PaddleOCR open-source project. The
model weights are publicly available athttps://huggingface.co/PaddlePaddle/PP-DocLayoutV3
arXiv:2606.23344v1 [cs.CV] 22 Jun 2026

Overall
FPS (images/second)
68
70
75
80
85
90
94
1 10 100
20M
3090M
1160M
53M
33M
DocLayout-YOLO
(Overall: 76.27, FPS: 107.4)
Dolphin-v2
(Overall: 71.44, FPS: 0.9)
MinerU2.5
(Overall: 86.61, FPS: 2.4)
PP-DocLayoutV2
(Overall: 87.12, FPS: 110.9)
RT-DocLayout
(Overall: 92.46, FPS: 132.1)
(a)
Raw
Scanning
Warping
Screen-Photography
Illumination
Skew
DocLayout-YOLO
MinerU2.5
Dolphin-v2
PP-DocLayoutV2
RT-DocLayout (Ours)
89
90
92
93
95
87
89
90
92
94
60
68
76
84
92
80
83
86
89
92
71
77
82
88
93
57
66
74
83
92 (b)
Figure 1|Performance and Robustness of RT-DocLayout.Our proposed method achieves a
new state-of-the-art in document layout analysis, demonstrating superior accuracy, real-time
speed, and robustness.(a)Comparison of performance (Overall Accuracy), inference speed
(FPS), and model parameter count (indicated by bubble size). Our RT-DocLayout (red bubble)
sets a new benchmark by achieving 92.46% accuracy and 132.1 FPS with a compact
33M-parameter model, significantly surpassing previous leading methods like PP-DocLayoutV2
and MinerU2.5 in all three metrics. The overall accuracy is the average score across the six
dimensions shown in (b). All experiments were performed using PaddleOCR-VL-1.5-0.9B as the
downstream recognizer. Inference speed was tested on an NVIDIA A100 GPU with a batch size
of 32.(b)Head-to-head comparison on six challenging dimensions from the OmniDocBench
v1.5 and Real5-OmniDocBench. RT-DocLayout consistently achieves the highest scores across
all dimensions (Raw, Scanning, Warping, Screen-Photography, Illumination, and Skew), proving
its exceptional robustness and generalizability under diverse real-world conditions.

### 1. Introduction
Document Layout Analysis (DLA) is a fundamental prerequisite for automated Document
Intelligence. Despite the success of deep learning in detecting layout elements, in complex
scenarios involving mobile photography or digitization of bound archives, where geometric
deformations are prevalent, document parsing is still hindered by two primary challenges:
fragmented structural modeling and coarse geometric representation.
Current methodologies typically follow two suboptimal paths. First, cascaded pipelines
attempt to reconstruct reading order by stacking a layout detector with secondary relationship
models (e.g., GNNs [1] or heuristic sorting [2]). Such systems are inherently fragile, as detection
errors propagate through the stages, and the lack of end-to-end integration prevents the model
from capturing the synergistic dependencies between layout and topology. Second, large-scale
pre-trained Transformers and VLMs (e.g., LayoutLMv3 [3], DiT [4], MinerU [5], Dolphin [6])
have achieved impressive results but remain computationally expensive. Moreover, these
models primarily rely on coarse-grained bounding boxes, which fail to provide the pixel-level
masks necessary to isolate layout elements in warped, curved, or tilted documents. This lack
of geometric precision often leads to content interference from background noise or adjacent
elements, limiting the fidelity of downstream parsing.
To bridge this gap, we propose RT-DocLayout, a 33M-parameter unified framework based
on the RT-DETR [7] architecture. RT-DocLayout breaks the conventional boundary by unifying
2

classification, detection, segmentation, and reading order prediction within a single query-
based Transformer decoder. In a single forward pass, each object query concurrently classifies,
regresses bounding boxes, generates high-fidelity masks for geometrically complex regions, and
predicts reading order.
The core strength of RT-DocLayout lies in its ability to provide a multi-dimensional structural
representation. By generating precise pixel-level masks instead of simple rectangles, the model
provides a purified input for downstream OCR engines, effectively mitigating the interference
caused by document deformations. This unified multi-task learning paradigm ensures that
geometric shape and logical sequence are modeled within a shared feature space, leading
to superior structural consistency. Notably, RT-DocLayout achieves state-of-the-art (SOTA)
performance across multiple benchmarks with a compact 33M-parameter footprint, offering a
highly efficient and scalable solution for real-time industrial document parsing, as shown on
Fig. 3.
Our contributions are summarized as follows:
• We propose RT-DocLayout, a unified 33M-parameter Transformer framework for docu-
ment layout analysis that achieves end-to-end classification, detection, pixel-level mask
generation, and reading order prediction.
• We demonstrate that providing pixel-level masks for non-rigidly deformed regions signifi-
cantly enhances the robustness of document parsing compared to traditional bounding-
box-based methods.
• Extensive experiments demonstrate that RT-DocLayout achieves SOTA accuracy while
maintaining real-time inference efficiency, validating its effectiveness as a practical front-
end for document parsing systems.

### 2. Related Work

### 2.1. Document Layout Element Detection
Early approaches adapted Faster R-CNN [8] and Mask R-CNN [9] to document images [10, 11].
DiT [4] introduced self-supervised pre-training for document Transformers, and the LayoutLM
series [12, 13, 3] pioneered joint text–layout–visual pre-training. DocLayout-YOLO [ 14] im-
proved inference speed for practical deployment. Despite these advances, all methods remain
confined to axis-aligned bounding boxes that degrade OCR fidelity under geometric distortion,
and none jointly models reading order.

### 2.2. Reading Order Prediction
Rule-based XYCut [2] is brittle on complex layouts. Data-driven methods cast the problem
as sequence generation or relation prediction: LayoutReader [15] pre-trains an autoregressive
Transformer on the ReadingBank benchmark, and XYLayoutLM [16] integrates spatial reading
order into layout-aware pre-training. All these methods operate as post-hoc modules after a
separate detector, forming cascaded pipelines prone to error propagation.

### 2.3. Unified Document Parsing Frameworks
Donut [17] and Nougat [18] generate structured markup via OCR-free encoder–decoder models;
UDOP [19] further unifies vision, text, and layout in a generative framework. Large VLMs,
3

including Dolphin [6], MinerU2.5 [5], MinerU2 [20], and dots.ocr [21], extend this to multi-task
document parsing at high computational cost. Closer to our setting, DLAFormer [ 22] jointly
predicts layout regions and reading order via a unified label space in an end-to-end DETR-
based framework, and PP-DocLayoutV2 [23] appends a decoupled reading order module to
RT-DETR [7] for compact real-time parsing. Both remain restricted to axis-aligned bounding
boxes and do not address geometric distortions from warping, perspective, or skew.
Our approach.RT-DocLayout addresses all of the above limitations with a compact, purely
visual architecture. Building on the insight that detection and segmentation can be jointly
optimized via unified queries [24], we extend RT-DETR [7] to support end-to-end segmentation.
Our unified multi-task formulation concurrently predicts bounding boxes, high-fidelity pixel-
level masks, and reading order in a single forward pass, replacing both autoregressive generation
and cascaded pipelines with deterministic, non-autoregressive decoding.

### 3. Proposed Approach

### 3.1. Framework Overview
Built upon the high-efficiency RT-DETR detector, RT-DocLayout reformulates document layout
analysis as a unified, mask-centric prediction task. Instead of relying on conventional bounding-
box representations, the framework produces pixel-accurate layout elements position while
jointly modeling reading order relationships within a single Transformer architecture. This
design enables reliable isolation of document layout elements under challenging conditions
such as skewed or geometrically distorted pages, where bounding-box-based methods often
introduce ambiguity and background interference. By integrating detection and reading order
prediction into one framework, RT-DocLayout eliminates redundant post-processing stages
and promotes structurally consistent and robust document layout analysis under geometric
variations.

### 3.2. Architecture Design
Building upon the high-efficiency RT-DETR object detector [ 7], RT-DocLayout extends the
detection paradigm toward unified structural prediction for document layout analysis, as shown
on Fig. 2. Instead of relying solely on bounding-box representations, the model adds a mask-
based detection head that produces pixel-accurate segments, enabling precise isolation of layout
elements under challenging conditions such as skewed, curved, or geometrically distorted pages
where axis-aligned boxes often introduce ambiguity and background contamination.
Unlike the decoupled pointer-network design used in prior systems [ 23], RT-DocLayout
integrates reading order prediction directly into the Transformer decoder, allowing geometric
perception and relationship representation of reading order to be optimized jointly. Following
the query-based paradigm, the decoder iteratively refines𝑁 object queries𝑄={𝑞 𝑖}𝑁𝑖=1∈R 𝑁×𝑑 ,
where each query encodes both spatial and structural semantics. Relative reading order logits
matrix is calculated from the refined query embeddings, enabling absolute reading order for all
elements by voting-based ranking strategy.
Specifically, refined queries are projected into a shared relational space to compute the
pairwise precedence score:
𝑆𝑖,𝑗 =
𝑞⊤𝑖 𝑊⊤𝑞 𝑊𝑘𝑞𝑗−𝑞⊤𝑗𝑊⊤𝑞 𝑊𝑘𝑞𝑖
√
𝑑ℎ
, (1)
4

Figure 2|The unified architecture of RT-DocLayout, featuring parallel heads for segmentation
and reading order prediction.
where𝑊𝑞,𝑊𝑘∈R 𝑑ℎ×𝑑 are learnable projection matrices that map queries to a relational em-
bedding space, and𝑑ℎ denotes the head dimension. The resulting relation matrix𝑆∈R 𝑁×𝑁 is
inherently anti-symmetric (𝑆𝑖,𝑗 =−𝑆 𝑗,𝑖), where𝑆𝑖,𝑗 > 0 indicates that element𝑖 precedes element 𝑗.
During inference, a voting-based ranking strategy converts pairwise relations into a globally
consistent sequence. After applying the sigmoid function, the precedence vote for element 𝑗 is
computed by summing over all incoming edges:
𝑉𝑗 =
𝑁∑︁
𝑖=1
𝜎(𝑆𝑖,𝑗), where𝑆 𝑖,𝑖 =0, (2)
where𝑉𝑗 represents the expected number of elements preceding element 𝑗. The final reading
order is obtained by sorting elements in ascending order of𝑉𝑗—elements with fewer predecessors
appear earlier in the sequence.
Through this joint optimization of classification, detection, segmentation, and pairwise order
relationship within a single vision-centric architecture, RT-DocLayout produces the complete
document structure in one forward pass, simultaneously outputting category labels, bounding
boxes, pixel-level masks, and reading orders. This unified formulation promotes structurally
consistent and geometrically robust document layout analysis while eliminating redundant
post-processing and separated feature extraction stages.

### 3.3. Loss Function Design
The training objective of RT-DocLayout is formulated as a multi-task optimization problem
that jointly supervises classification, bounding-box, segmentation mask, and pairwise order
relationship. We employ the Hungarian algorithm to establish optimal bipartite matching
between predictions and ground-truth annotations before loss computation.
Overall Objective.The total loss is a weighted combination of six components:
Ltotal =
∑︁
𝑘∈K
𝜆𝑘·L 𝑘, (3)
whereK={cls , bbox, giou, mask, dice, order} and the weights are set as 𝜆cls = 4, 𝜆bbox = 5,
𝜆giou = 2, 𝜆mask = 5, 𝜆dice = 5, and 𝜆order = 50. The reading order loss receives a substantially
higher weight for two reasons. First, it addresses the gradient dilution problem: the order loss
5

operates on𝑂(𝑁 2) pairs, meaning each pairwise prediction receives gradients diluted by a factor
of approximately𝑁/2. In contrast, other object-level losses scale at 𝑂(𝑁) , maintaining a more
direct gradient impact. Second, while others losses benefit from deep supervision across all
decoder layers (providing𝐿 times more gradient updates for a model with𝐿 layers), the order
loss is computed only at the final layer and thus receives significantly fewer optimization signals
throughout training.
Classification and Detection Losses.For category prediction, we adopt focal loss with
𝛼=0.25 and𝛾=2.0 to address class imbalance:
Lcls =− 1𝑁 ∑︁𝑖 𝛼𝑦𝑖(1−𝑝 𝑖)𝛾 log(𝑝𝑖), (4)
where𝑝𝑖 denotes the predicted probability for the ground-truth class𝑦𝑖. Bounding box regression
combinesℓ 1 loss and GIoU loss:
Lbbox =∥𝑏 𝑖− ˆ𝑏𝑖∥1,L giou =1−GIoU(𝑏 𝑖, ˆ𝑏𝑖), (5)
where𝑏 𝑖 and ˆ𝑏𝑖 represent predicted and ground-truth boxes respectively.
Mask Segmentation Loss.Pixel-level mask supervision comprises binary cross-entropy and
Dice loss:
Lmask =BCE(𝑚 𝑖, ˆ𝑚𝑖),L dice =1− 2|𝑚𝑖∩ˆ𝑚𝑖|+1|𝑚𝑖|+|ˆ𝑚 𝑖|+1 . (6)
Following MaskDINO, we employ point-based sampling with importance weighting to compute
mask loss efficiently, sampling 𝐾= 12544 points per mask with 75% allocated to uncertain
regions.
Relative Reading Order Loss.The key contribution of our loss design is the pairwise reading
order supervision. Given 𝑁 matched layout elements with ground-truth reading order indices
{𝑜1,𝑜 2,...,𝑜 𝑁}, we construct a binary target matrix𝑇∈{0, 1} 𝑁×𝑁 where:
𝑇𝑖,𝑗 =
(
1 if𝑜 𝑖 < 𝑜𝑗 (element𝑖precedes𝑗)
0 otherwise . (7)
The antisymmetric pairwise scorer predicts pairwise logits𝑆∈R 𝑁×𝑁 with the constraint:
𝑆𝑖,𝑗 =
𝑓(𝑞 𝑖,𝑞 𝑗)−𝑓(𝑞 𝑗,𝑞𝑖)√
𝑑ℎ
,𝑓(𝑞 𝑖,𝑞 𝑗)=(𝑊 𝑞𝑞𝑖)⊤(𝑊𝑘𝑞𝑗), (8)
ensuring𝑆 𝑖,𝑗 =−𝑆 𝑗,𝑖 for consistent ordering relationships.
To emphasize local ordering correctness, we introduce locality-aware weighting. For element
pairs within a dynamic neighbor window𝑘=max( 5, 0.3𝑁), we apply a higher weight𝑤local = 2.0:
𝑤𝑖,𝑗 =
(
𝑤local if 0<|𝑜 𝑖−𝑜 𝑗|⩽𝑘
1.0 otherwise . (9)
To handle potential annotation noise, we employ Generalized Cross Entropy (GCE) loss with
label smoothing (𝜀=0.01):
Lorder = 1|𝑃| ∑︁(𝑖,𝑗)∈𝑃 𝑤𝑖,𝑗·GCE(𝑆 𝑖,𝑗 ,𝑇𝑖,𝑗), (10)
6

where𝑃 denotes the set of valid upper-triangular pairs (excluding diagonal), and GCE(𝑧 ,𝑡)=
(1−𝑝 𝑞𝑡)/𝑞with𝑝 𝑡 =𝜎(𝑧)if𝑡=1 else 1−𝜎(𝑧), and𝑞=0.7 for robustness.
Deep Supervision.Auxiliary losses from intermediate decoder layers provide deep supervi-
sion for classification, detection, and segmentation, improving gradient flow and convergence.
The reading order loss, however, is computed only at the final decoder layer. This design
choice is motivated by the observation that accurate reading order prediction fundamentally
depends on precise object localization and classification—intermediate layer representations
lack sufficient spatial and semantic refinement to provide meaningful order supervision.

### 3.4. Physical Spatial Aware Data Augmentation
In real-world scenarios, document images captured by mobile devices exhibit complex geo-
metric distortions that can be categorized into two distinct physical processes: intrinsic surface
deformation and extrinsic projective transformation. However, standard document datasets
typically provide only axis-aligned bounding boxes or flat polygon annotations, which fail to
capture the pixel-level nuances of warped pages.
Intrinsic Surface Extrinsic Projective
𝑥!=𝑥+𝐴⋅𝑓"𝜔#⋅𝑦⋅𝑑"
𝐴:Amplitude 𝜔:SpatialFrequency 𝑓:Wavefunction
𝑦!=𝑦+𝐴⋅𝑓#𝜔"⋅𝑥⋅𝑑# Rotation Shear
 Perspective
Deformation Transformation
Figure 3|The Physical Spatial Aware Data Augmentation Pipeline.
To bridge this domain gap, we propose an online physical spatial aware data augmentation
pipeline, as shown on Fig. 3, that decouples the augmentation into a cascaded process: first
simulating the non-rigid physical warping of the paper surface, and subsequently modeling
the stochastic camera viewpoints. This pipeline dynamically synthesizes realistic distortions
from standard flat annotations, providing a robust foundation for training deformation-aware
segmentation models.
Stage 1: Intrinsic Surface Deformation (ISD).To characterize the non-rigid geometric priors
of physical documents, such as page curling in bound volumes. We propose a mesh-based
warping operator. Unlike standard linear transformations, ISD employs smooth, periodic dis-
placement fields to simulate paper deformation. For each pixel(𝑥 ,𝑦), the deformed coordinates
(𝑥′,𝑦′)are computed as:
𝑥′ =𝑥+𝐴·𝑓 𝑥 𝜔𝑦·𝑦 ·𝑑 𝑥,𝑦 ′ =𝑦+𝐴·𝑓 𝑦(𝜔𝑥·𝑥)·𝑑 𝑦 (11)
7

where 𝑓𝑥, 𝑓𝑦 ∈ {sin, cos} are randomly sampled wave functions, 𝐴=𝛼min(𝐻 ,𝑊) is the
displacement amplitude proportional to the image resolution with𝛼 drawn from a configurable
range,𝜔𝑥 =𝛽𝜋/𝑊 and𝜔𝑦 =𝛽𝜋/𝐻 control the spatial frequency with𝛽 sampled uniformly, and
𝑑𝑥,𝑑𝑦∈{− 1, 1} randomize the displacement direction. The operator supports two stochastic
modes: a single-axis mode that applies displacement along only one axis to simulate unidirec-
tional page curl, and an intense mode that applies displacement along both axes simultane-
ously to simulate compound deformations. Image and masks are remapped with bilinear and
nearest-neighbor interpolation, respectively. Border padding is dynamically computed from the
maximum displacement amplitudes to preserve all content.
Stage 2: Extrinsic Projective Transformation (EPT).Document images frequently undergo
geometric distortions due to variations in camera perspective. To account for this, EPT simulates
the variability of camera viewpoints in uncontrolled environments. We formulate this process
as a composite homography 𝑀, which maps the previously warped surface into a 3D-aware
perspective space. The transformation matrix𝑀∈R 3×3 is decomposed as follows:
𝑀=𝑆·𝑅·𝑃(12)
where 𝑃 introduces perspective foreshortening via its projective parameters 𝑝20 and 𝑝21,
mimicking oblique viewing angles; 𝑅 and𝑆 account for in-plane rotation and angular shear,
respectively, to simulate natural hand-held capture. Finally, the instance-level ground truth
is updated by re-extracting axis-aligned bounding boxes from the transformed pixel-accurate
masks.

### 4. Experiments

### 4.1. Experimental Setup

### 4.1.1. Datasets
To ensure robust model performance across diverse real-world document scenarios, we curate
an in-house dataset for layout analysis. The data sources encompass 38k document images
across diverse domains, including Academic papers, Textbooks, Market Analysis, Financial
reports, Slides, Newspapers, Supplementary Teaching Materials, Examination Papers, and
various Invoices and Receipts. The dataset features meticulous manual annotations across 25
distinct layout element categories: Paragraph Title, Image, Text, Number, Abstract, Content,
Figure Title, Display Formula, Table, Reference, Doc Title, Footnote, Header, Algorithm, Footer,
Seal, Chart, Formula Number, Aside Text, Reference Content, Header Image, Footer Image,
Inline Formula, Vertical Text, and Vision Footnote. All documents are manually annotated with
element-level boundaries and their corresponding reading order, enabling effective training and
evaluation for both layout element detection and reading order prediction. This high-quality
ground truth ensures that the model can accurately reconstruct both the spatial structure and the
logical flow of complex documents. All experiments in this paper are trained on this dataset. For
evaluation, we adopt OmniDocBench v1.5 [25]and its real-world document–oriented derivative
dataset, Real5-OmniDocBench [26].

### 4.1.2. Evaluation Metrics
Due to the lack of standardized evaluation metrics that comprehensively measure layout analysis
capability—covering both layout detection and reading order prediction—we evaluate RT-
8

Table 1|Comparison of different layout analysis modules combined with various recognition
systems on OmniDocBench v1.5. As DocLayout-YOLO does not output reading order, we
employ the XYCut algorithm as a post-processing.
Layout Analysis Params FPS Recognition Method Overall↑ TextEdit↓ FormulaCDM↑Table TEDS↑ Reading OrderEdit↓
DocLayout-YOLO [14] 20M 107.4
MonkeyOCR [27] 85.10 0.130 85.99 82.31 0.169
MinerU2.5 [5] 85.73 0.138 87.26 83.73 0.177
Dolphin-v2 [28] 84.14 0.150 83.92 83.47 0.178
PaddleOCR-VL-1.5-0.9B [29] 87.29 0.127 88.74 85.83 0.169
MinerU2.5 [5] 1.2B 2.4
MonkeyOCR [27] 89.69 0.047 87.06 86.71 0.050
MinerU2.5 [5] 90.17 0.052 87.81 87.95 0.053
Dolphin-v2 [28] 88.25 0.068 83.55 88.02 0.062
PaddleOCR-VL-1.5-0.9B [29] 91.31 0.046 87.57 90.92 0.051
Dolphin-v2 [28] 3B 0.9
MonkeyOCR [27] 89.14 0.051 87.28 85.24 0.061
MinerU2.5 [5] 89.58 0.055 87.71 86.57 0.067
Dolphin-v2 [28] 87.49 0.073 83.04 86.69 0.067
PaddleOCR-VL-1.5-0.9B [29] 90.36 0.049 87.60 88.36 0.060
PP-DocLayoutV2 [23] 53M 110.9
MonkeyOCR [27] 91.32 0.038 89.41 88.41 0.045
MinerU2.5 [5] 92.00 0.042 90.51 89.66 0.051
Dolphin-v2 [28] 87.49 0.073 83.04 86.69 0.067
PaddleOCR-VL-1.5-0.9B [29] 93.56 0.03492.09 92.03 0.042
RT-DocLayout 33M 132.1
MonkeyOCR [27] 92.51 0.039 92.37 89.07 0.044
MinerU2.5 [5] 92.68 0.043 92.19 90.12 0.049
Dolphin-v2 [28] 90.72 0.060 89.17 89.00 0.058
PaddleOCR-VL-1.5-0.9B [29] 94.50 0.03594.21 92.76 0.042
DocLayout using downstream document parsing benchmarks. Rather than relying solely
on geometric detection accuracy, this protocol assesses whether predicted layouts effectively
support structured document parsing in realistic scenarios.
Specifically, we conduct evaluation on OmniDocBench v1.5 and its real-world extension,
Real5-OmniDocBench, measuring performance on formulas, tables, textual content, and reading
order. These metrics jointly reflect spatial localization accuracy as well as the structural and
semantic coherence captured by the layout model.

### 4.1.3. Implementation Details
The model is initialized with the pre-trained weights of PP-DocLayout_plus-L, we scaled our
training corpus to over 38k high-quality document samples. Each sample underwent rigorous
manual annotation to provide ground truth, including coordinates, categorical labels, and
absolute reading order for every layout elements. To achieve the environmental robustness,
we designed a specialized Distortion-Aware Data Augmentation pipeline. Unlike standard
augmentations, this pipeline specifically simulates complex physical deformations found in
real-world mobile photography. We utilize the AdamW optimizer with a weight decay of 0.0001.
The learning rate is set to a constant 2 × 10−4 to ensure stable convergence of the integrated
antisymmetric pairwise scorer and Mask heads. The model is trained for 150 epochs with a total
batch size of 32.
9

Table 2|Comparison of layout analysis and recognition system combinations on
Real5-OmniDocBench. As DocLayout-YOLO does not output reading order, we employ the
XYCut algorithm as a post-processing. Overall is the average across five scenarios—Scanning,
Warping, Screen-Photography, Illumination, and Skew (abbreviated as Scan, Warp, Screen,
Illum, Skew).
Layout Analysis Params FPS Recognition Method Overall↑ Scan↑Warp↑Screen↑Illum↑Skew↑
DocLayout-YOLO [14] 20M 107.4
MonkeyOCR [27] 73.57 84.09 74.81 76.89 81.99 50.06
MinerU2.5 [5] 72.92 85.00 72.92 77.38 82.68 46.62
Dolphin-v2 [28] 72.72 83.40 73.59 75.90 81.00 49.71
PaddleOCR-VL-1.5-0.9B [29] 74.07 85.57 74.70 77.67 83.65 48.74
MinerU2.5 [5] 1.2B 2.4
MonkeyOCR [27] 85.23 88.70 84.10 87.16 87.63 78.56
MinerU2.5 [5] 84.55 88.37 82.85 88.29 88.02 75.20
Dolphin-v2 [28] 82.48 87.20 82.72 85.89 86.17 70.45
PaddleOCR-VL-1.5-0.9B [29] 85.67 89.74 83.92 89.24 89.29 76.16
Dolphin-v2 [28] 3B 0.9
MonkeyOCR [27] 69.74 87.86 58.41 81.01 68.31 53.12
MinerU2.5 [5] 60.88 87.70 45.38 76.75 58.54 36.01
Dolphin-v2 [28] 67.40 85.72 58.08 73.30 64.03 55.84
PaddleOCR-VL-1.5-0.9B [29] 67.66 88.66 52.58 81.06 66.15 49.84
PP-DocLayoutV2 [23] 53M 110.9
MonkeyOCR [27] 85.10 90.47 85.90 81.60 88.86 78.65
MinerU2.5 [5] 83.87 90.98 83.88 81.98 89.06 73.44
Dolphin-v2 [28] 84.16 89.46 84.54 81.11 87.97 77.71
PaddleOCR-VL-1.5-0.9B [29] 85.83 92.04 86.00 83.28 90.80 77.03
RT-DocLayout 33M 132.1
MonkeyOCR [27] 89.79 91.73 89.38 89.67 89.72 88.44
MinerU2.5 [5] 89.89 91.74 88.96 90.38 90.31 88.06
Dolphin-v2 [28] 88.97 90.36 88.47 88.61 89.39 88.04
PaddleOCR-VL-1.5-0.9B [29] 92.05 93.43 91.25 91.76 92.16 91.66

### 4.2. Main Results
4.2.1. OmniDocBench v1.5
Table 1 presents the performance of different layout analysis modules combined with various
recognition methods on OmniDocBench v1.5.
Across all evaluated recognition methods, RT-DocLayout achieves the best Overall perfor-
mance. When paired with PaddleOCR-VL-1.5-0.9B, RT-DocLayout reaches an Overall score
of 94.50, which is the highest among all evaluated combinations. Consistent improvements
can also be observed when RT-DocLayout is combined with MonkeyOCR, MinerU2.5, and
Dolphin-v2, demonstrating its compatibility with heterogeneous recognition architectures.
In addition to the Overall metric, RT-DocLayout brings consistent gains across multiple
evaluation dimensions, including text accuracy (Edit distance), formula recognition (CDM),
table structure similarity (TEDS), and reading order prediction (Edit distance). These results
indicate that improving layout analysis quality can positively influence recognition performance
in a holistic manner.
Moreover, RT-DocLayout contains only 33 M parameters and infer at 132.1 FPS, achieving
both the highest inference speed and the best overall accuracy among all evaluated layout
analysis modules.
10

Table 3|Ablation study of our model components on OmniDocBench v1.5 and its real-world
degradation subset, Real5-OmniDocBench. We analyze the impact of the localization method
(Loc: bbox vs. mask), the reading order module (Order), and our proposed data augmentation
(DA). Metrics are Overall accuracy (O,↑) and Reading Order distance (RO,↓). Our full model
(last row) achieves the best performance, demonstrating the effectiveness of each component.
Components OmniDocBench v1.5 Real5-OmniDocBench
Scan Warp Screen Illum Skew
Loc Order DA O↑RO↓ O↑RO↓O↑RO↓O↑RO↓O↑RO↓O↑RO↓
bbox XYCut [2]× 93.81 0.082 90.30 0.749 84.44 0.720 88.35 0.744 88.90 0.747 77.18 0.662
bbox+mask XYCut [2]× 94.33 0.074 90.22 0.742 84.40 0.721 88.55 0.744 89.14 0.747 75.63 0.673
bbox+mask Decoupled× 93.87 0.189 92.85 0.192 85.91 0.238 91.22 0.195 91.55 0.188 76.24 0.325
bbox+mask Coupled× 94.390.041 93.29 0.045 86.68 0.092 91.550.05092.12 0.054 77.55 0.146
bbox+mask Coupled✓ 94.500.042 93.43 0.045 91.25 0.063 91.760.05992.16 0.051 91.66 0.061

### 4.2.2. Real5-OmniDocBench
To further evaluate robustness under real-world physical distortions, we conduct experiments
on Real5-OmniDocBench, which includes five challenging scenarios: Scanning, Warping, Screen-
Photography, Illumination, and Skew.
As shown in Table 2, RT-DocLayout consistently achieves superior performance across
different recognition systems. When combined with PaddleOCR-VL-1.5-0.9B, it obtains an
Overall score of 92.05%, which is the highest among all configurations.
The improvements are particularly evident in geometrically challenging scenarios such as
Warping and Skew. For example, when paired with PaddleOCR-VL-1.5-0.9B, RT-DocLayout
achieves 91.25% on Warp and 91.66% on Skew. In contrast, box-based layout analysis methods
exhibit more noticeable performance degradation in these settings. This observation suggests
that more precise geometric modeling can improve robustness under various distortions.
Furthermore, the performance gains brought by RT-DocLayout remain consistent across
different recognition methods, indicating that the improvements are not specific to a particular
downstream model but stem from enhanced layout analysis.

### 4.3. Ablation Study and Analysis
We conduct a structured ablation study on OmniDocBench v1.5 and Real5-OmniDocBench, to
analyze how each component of RT-DocLayout contributes to unified document layout analysis.
All experiments use PaddleOCR-VL-1.5-0.9B as the downstream recognizer. The results are
summarized in Table 3.
Effectiveness of Mask-based Localization.As shown in the first two rows of Table 3,
replacing pure bounding-box supervision with joint mask prediction (𝑏𝑏𝑜𝑥+𝑚𝑎𝑠𝑘 ) improves
the Overall accuracy (𝑂) from 93.81% to 94.33% on OmniDocBench v1.5. The introduction
of pixel-level masks provides finer structural cues, allowing the model to better distinguish
overlapping or closely-packed elements, which is reflected in the consistent𝑂 gains across most
scenarios on Real5-OmniDocBench.
Coupled Reading Order Learning.A key contribution of RT-DocLayout is the end-to-
end prediction of reading order. Compared to the heuristic XYCut [2], our Coupled learning
11

approach (penultimate row) significantly reduces the Reading Order distance (𝑅𝑂) from 0.074 to
0.041 on OmniDocBench v1.5. More importantly, in complex scenarios like the "Warp" subset,
the𝑅𝑂 distance drops drastically from 0.721 (XYCut) to 0.092. It is worth noting that the Reading
Order distance (𝑅𝑂) of decoupled learning strategy (reading order as a separate trained model
without joint optimization) is 0.189, performing significantly worse than 0.074 (XYCut) on
OmniDocBench v1.5. However, this performance deficit is effectively reversed through joint
optimization. This further validates that integrating reading order directly into the layout
perception phase allows the model to capture global structural dependencies more effectively.
Robustness through realistic augmentation.The most significant performance leap on
Real5-OmniDocBench comes from our proposed data augmentation (DA). When DA is enabled
(last row), the model’s performance on the "Warp" and "Skew" subsets of Real5-OmniDocBench
increases by 4.57 (86.68%→ 91.25%) and 14.11 percentage points (77.55%→ 91.66%) respectively.
Crucially, this robustness extends beyond localization to reading order: on the "Skew" subset, the
Reading Order (RO) distance drops significantly from 0.146 to 0.061, while on the "Warp" subset,
it improves from 0.092 to 0.063. Since our model generates mask-level outputs, the DA can
simulate realistic geometric distortions (like page curling or camera tilting) while maintaining
pixel-level ground truth. These results demonstrate that by training on mask-guided synthetic
distortions, RT-DocLayout learns to preserve spatial-logical consistency even under non-linear
transformations. Consequently, our model achieves state-of-the-art robustness against real-
world physical deformations without sacrificing accuracy on OmniDocBench v1.5.
Origin PP-DocLayoutV2Ours
(a)
Origin PP-DocLayoutV2Ours
(b)
Origin PP-DocLayoutV2Ours
(c)
Origin PP-DocLayoutV2Ours
(d)
Figure 4| Qualitative comparison on four real-world scenarios. Each group shows, left to right:
Origin, PP-DocLayoutV2,Ours.(a)Skew.(b)Page warping.(c)Non-uniform illumination.
(d)Screen photography.
12


### 4.4. Qualitative Analysis and Case Insights
Fig. 4 compares RT-DocLayout with PP-DocLayoutV2, a previous state-of-the-art real-time
document layout analysis method, across four real-world scenarios: skew (a), page warping (b),
non-uniform illumination (c), and screen photography (d). In (a) and (b), axis-aligned boxes
span background and neighboring elements when the document geometry deviates from a
fronto-parallel plane; RT-DocLayout masks follow the actual boundaries under each distortion.
In (c), PP-DocLayoutV2 misses content in the darker region due to low contrast; RT-DocLayout
produces consistent predictions across the full layout. In (d), PP-DocLayoutV2 conflates tables,
text blocks, and titles into coarse regions; RT-DocLayout recovers fine-grained element bound-
aries under the screen-captured condition.These cases demonstrate that RT-DocLayout produces
accurate and geometrically consistent layout predictions across diverse real-world degradations.

### 5. Conclusion
In this paper, we presented RT-DocLayout, a unified and efficient Transformer-based framework
for real-time document layout analysis. Moving beyond the conventional box-centric paradigm,
RT-DocLayout unifies layout detection, pixel-level segmentation, and reading order prediction
within a single non-autoregressive forward pass. This unified formulation improves structural
consistency and geometric robustness, particularly for documents with complex distortions.
Extensive experiments show that RT-DocLayout, with only 33 M parameters, achieves a
superior balance between accuracy and efficiency, outperforming substantially larger models
in both geometric fidelity and real-time deployment capability. RT-DocLayout establishes a
scalable and structurally aware foundation for next-generation document intelligence systems.
References
[1] Chen-Yu Lee, Chun-Liang Li, Chu Wang, Renshen Wang, Yasuhisa Fujii, Siyang Qin, Ashok
Popat, and Tomas Pfister. Rope: Reading order equivariant positional encoding for graph-
based document information extraction, 2021. URL https://arxiv.org/abs/2106.1
0786.
[2] Jaekyu Ha, Robert M Haralick, and Ihsin T Phillips. Recursive xy cut using bounding boxes
of connected components. InProceedings of 3rd International Conference on Document Analysis
and Recognition, volume 2, pages 952–955. IEEE, 1995.
[3] Yupan Huang, Tengchao Lv, Lei Cui, Yutong Lu, and Furu Wei. Layoutlmv3: Pre-training
for document ai with unified text and image masking, 2022. URL https://arxiv.org/
abs/2204.08387.
[4] Junlong Li, Yiheng Xu, Tengchao Lv, Lei Cui, Cha Zhang, and Furu Wei. Dit: Self-supervised
pre-training for document image transformer, 2022. URL https://arxiv.org/abs/22
03.02378.
[5] Junbo Niu, Zheng Liu, Zhuangcheng Gu, Bin Wang, Linke Ouyang, Zhiyuan Zhao, Tao Chu,
Tianyao He, Fan Wu, Qintong Zhang, Zhenjiang Jin, Guang Liang, Rui Zhang, Wenzheng
Zhang, Yuan Qu, Zhifei Ren, Yuefeng Sun, Yuanhong Zheng, Dongsheng Ma, Zirui Tang,
Boyu Niu, Ziyang Miao, Hejun Dong, Siyi Qian, Junyuan Zhang, Jingzhou Chen, Fangdong
Wang, Xiaomeng Zhao, Liqun Wei, Wei Li, Shasha Wang, Ruiliang Xu, Yuanyuan Cao,
Lu Chen, Qianqian Wu, Huaiyu Gu, Lindong Lu, Keming Wang, Dechen Lin, Guanlin
13

Shen, Xuanhe Zhou, Linfeng Zhang, Yuhang Zang, Xiaoyi Dong, Jiaqi Wang, Bo Zhang,
Lei Bai, Pei Chu, Weijia Li, Jiang Wu, Lijun Wu, Zhenxiang Li, Guangyu Wang, Zhongying
Tu, Chao Xu, Kai Chen, Yu Qiao, Bowen Zhou, Dahua Lin, Wentao Zhang, and Conghui
He. Mineru2.5: A decoupled vision-language model for efficient high-resolution document
parsing, 2025. URLhttps://arxiv.org/abs/2509.22186.
[6] Hao Feng, Shu Wei, Xiang Fei, Wei Shi, Yingdong Han, Lei Liao, Jinghui Lu, Binghong Wu,
Qi Liu, Chunhui Lin, Jingqun Tang, Hao Liu, and Can Huang. Dolphin: Document image
parsing via heterogeneous anchor prompting, 2025. URL https://arxiv.org/abs/25
05.14059.
[7] Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang,
Yi Liu, and Jie Chen. Detrs beat yolos on real-time object detection, 2024. URL https:
//arxiv.org/abs/2304.08069.
[8] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. Faster r-cnn: Towards real-time
object detection with region proposal networks, 2016. URL https://arxiv.org/abs/
1506.01497.
[9] Kaiming He, Georgia Gkioxari, Piotr Dollár, and Ross Girshick. Mask r-cnn, 2018. URL
https://arxiv.org/abs/1703.06870.
[10] Xu Zhong, Jianbin Tang, and Antonio Jimeno Yepes. Publaynet: largest dataset ever for
document layout analysis, 2019. URLhttps://arxiv.org/abs/1908.07836.
[11] Zejiang Shen, Ruochen Zhang, Melissa Dell, Benjamin Charles Germain Lee, Jacob Carlson,
and Weining Li. Layoutparser: A unified toolkit for deep learning based document image
analysis, 2021. URLhttps://arxiv.org/abs/2103.15348.
[12] Yiheng Xu, Minghao Li, Lei Cui, Shaohan Huang, Furu Wei, and Ming Zhou. Layoutlm:
Pre-training of text and layout for document image understanding. InProceedings of the
26th ACM SIGKDD International Conference on Knowledge Discovery &amp; Data Mining,
KDD ’20, page 1192–1200. ACM, August 2020. doi: 10.1145/3394486.3403172. URL
http://dx.doi.org/10.1145/3394486.3403172.
[13] Yang Xu, Yiheng Xu, Tengchao Lv, Lei Cui, Furu Wei, Guoxin Wang, Yijuan Lu, Dinei
Florencio, Cha Zhang, Wanxiang Che, Min Zhang, and Lidong Zhou. Layoutlmv2: Multi-
modal pre-training for visually-rich document understanding, 2022. URL https://arxi
v.org/abs/2012.14740.
[14] Zhiyuan Zhao, Hengrui Kang, Bin Wang, and Conghui He. Doclayout-yolo: Enhancing
document layout analysis through diverse synthetic data and global-to-local adaptive
perception, 2024. URLhttps://arxiv.org/abs/2410.12628.
[15] Zilong Wang, Yiheng Xu, Lei Cui, Jingbo Shang, and Furu Wei. Layoutreader: Pre-training
of text and layout for reading order detection, 2021. URL https://arxiv.org/abs/21
08.11591.
[16] Zhangxuan Gu, Changhua Meng, Ke Wang, Jun Lan, Weiqiang Wang, Ming Gu, and
Liqing Zhang. Xylayoutlm: Towards layout-aware multimodal networks for visually-rich
document understanding, 2022. URLhttps://arxiv.org/abs/2203.06947.
14

[17] Geewook Kim, Teakgyu Hong, Moonbin Yim, Jeongyeon Nam, Jinyoung Park, Jinyeong
Yim, Wonseok Hwang, Sangdoo Yun, Dongyoon Han, and Seunghyun Park. Ocr-free
document understanding transformer, 2022. URL https://arxiv.org/abs/2111.156
64.
[18] Lukas Blecher, Guillem Cucurull, Thomas Scialom, and Robert Stojnic. Nougat: Neural
optical understanding for academic documents, 2023. URL https://arxiv.org/abs/
2308.13418.
[19] Zineng Tang, Ziyi Yang, Guoxin Wang, Yuwei Fang, Yang Liu, Chenguang Zhu, Michael
Zeng, Cha Zhang, and Mohit Bansal. Unifying vision, text, and layout for universal
document processing, 2023. URLhttps://arxiv.org/abs/2212.02623.
[20] opendatalab. Mineru2.0-2505-0.9b. https://huggingface.co/opendatalab/Miner
U2.0-2505-0.9B, 2025.
[21] Yumeng Li, Guang Yang, Hao Liu, Bowen Wang, and Colin Zhang. dots.ocr: Multilingual
document layout parsing in a single vision-language model, 2025. URLhttps://arxiv.
org/abs/2512.02498.
[22] Jiawei Wang, Kai Hu, and Qiang Huo. Dlaformer: An end-to-end transformer for document
layout analysis, 2024. URLhttps://arxiv.org/abs/2405.11757.
[23] Cheng Cui, Ting Sun, Suyin Liang, Tingquan Gao, Zelun Zhang, Jiaxuan Liu, Xueqing
Wang, Changda Zhou, Hongen Liu, Manhui Lin, Yue Zhang, Yubo Zhang, Handong
Zheng, Jing Zhang, Jun Zhang, Yi Liu, Dianhai Yu, and Yanjun Ma. Paddleocr-vl: Boosting
multilingual document parsing via a 0.9b ultra-compact vision-language model, 2025. URL
https://arxiv.org/abs/2510.14528.
[24] Feng Li, Hao Zhang, Huaizhe xu, Shilong Liu, Lei Zhang, Lionel M. Ni, and Heung-Yeung
Shum. Mask dino: Towards a unified transformer-based framework for object detection
and segmentation, 2022. URLhttps://arxiv.org/abs/2206.02777.
[25] Linke Ouyang, Yuan Qu, Hongbin Zhou, Jiawei Zhu, Rui Zhang, Qunshu Lin, Bin Wang,
Zhiyuan Zhao, Man Jiang, Xiaomeng Zhao, Jin Shi, Fan Wu, Pei Chu, Minghao Liu, Zhenxi-
ang Li, Chao Xu, Bo Zhang, Botian Shi, Zhongying Tu, and Conghui He. Omnidocbench:
Benchmarking diverse pdf document parsing with comprehensive annotations, 2025. URL
https://arxiv.org/abs/2412.07626.
[26] Changda Zhou, Ziyue Gao, Xueqing Wang, Tingquan Gao, Cheng Cui, Jing Tang, and
Yi Liu. Real5-omnidocbench: A full-scale physical reconstruction benchmark for robust
document parsing in the wild, 2026. URLhttps://arxiv.org/abs/2603.04205.
[27] Zhang Li, Yuliang Liu, Qiang Liu, Zhiyin Ma, Ziyang Zhang, Shuo Zhang, Biao Yang,
Zidun Guo, Jiarui Zhang, Xinyu Wang, and Xiang Bai. Monkeyocr: Document parsing
with a structure-recognition-relation triplet paradigm, 2026. URL https://arxiv.org/
abs/2506.05218.
[28] Hao Feng, Wei Shi, Ke Zhang, Xiang Fei, Lei Liao, Dingkang Yang, Yongkun Du, Xuecheng
Wu, Jingqun Tang, Yang Liu, Hong Chen, and Can Huang. Dolphin-v2: Universal document
parsing via scalable anchor prompting, 2026. URL https://arxiv.org/abs/2602.053
84.
15

[29] Cheng Cui, Ting Sun, Suyin Liang, Tingquan Gao, Zelun Zhang, Jiaxuan Liu, Xueqing
Wang, Changda Zhou, Hongen Liu, Manhui Lin, Yue Zhang, Yubo Zhang, Yi Liu, Dianhai
Yu, and Yanjun Ma. Paddleocr-vl-1.5: Towards a multi-task 0.9b vlm for robust in-the-wild
document parsing, 2026. URLhttps://arxiv.org/abs/2601.21957.
16