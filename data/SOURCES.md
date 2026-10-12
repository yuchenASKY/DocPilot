# `data/docs` 语料来源清单

本目录的 20 篇论文全部来自 **arXiv 预印本（开放获取）**，抓取时间：2026-10-12。

> 为什么全用 arXiv：它是**开放获取**，PDF 可合法下载再分发到本地知识库；
> 而 Elsevier / Springer / IEEE 等出版社的 PDF 有付费墙，不适合直接入库。


## 格式说明（故意做成三种格式）

| 格式 | 篇数 | 作用 |
|---|---|---|
| `.pdf` | 12 | 真实语料形态，考验第 5 步的 PDF 解析（pypdf） |
| `.txt` | 4 | 纯文本，由 PDF 提取正文，考验最简解析分支 |
| `.md` | 4 | Markdown，由 PDF 正文重排（带标题层级），考验 MD 解析 |

> 同一篇论文**只保留一种格式** —— 否则同一内容会入库两份，检索时重复命中。


## 清单

| # | 领域 | 标题 | 发布 | 格式 | arXiv |
|---|---|---|---|---|---|
| 1 | `cs.AI` | LLM-IDEA: Identifiability-Driven Experimental Agent for Autonomous Discovery of Mechanistic World Models | 2026-10-08 | PDF | [2610.11253v1](https://arxiv.org/abs/2610.11253v1) |
| 2 | `cs.CL` | From Retrieval to Reconstruction: Constructing Evolvable Cognitive Memory for Long-Term Dialogue | 2026-10-08 | PDF | [2610.11314v1](https://arxiv.org/abs/2610.11314v1) |
| 3 | `cs.CV` | Exploring Attention Sinks in Text-to-Image Transformers from Diffusion and Autoregressive Models | 2026-10-09 | PDF | [2610.13337v1](https://arxiv.org/abs/2610.13337v1) |
| 4 | `cs.LG` | Toward Joint Optimization of Circuit Depth and Training Data Size in Adaptively Grown Quantum Classifiers | 2026-10-08 | PDF | [2610.12428v1](https://arxiv.org/abs/2610.12428v1) |
| 5 | `cs.DC` | Adaptive Multi-Discriminator WGAN Framework for Resource-Constrained Internet of Vehicles Using Reinforcement Learning and Game Theory | 2026-10-07 | PDF | [2610.10926v1](https://arxiv.org/abs/2610.10926v1) |
| 6 | `cs.DB` | Query Performance Tuning with Optimal Exploration of Optimizer Cost Model Parameter Space | 2026-10-02 | PDF | [2610.02607v1](https://arxiv.org/abs/2610.02607v1) |
| 7 | `cs.CR` | Black-Box Adversarial Patch Attacks on VLAs via Ancestor VLM Exploitation | 2026-10-07 | PDF | [2610.09708v1](https://arxiv.org/abs/2610.09708v1) |
| 8 | `cs.SE` | (When) Should a Software Factory be Lights-off? Benchmarking Code Review Agents on Bug Detection | 2026-10-09 | PDF | [2610.13668v1](https://arxiv.org/abs/2610.13668v1) |
| 9 | `cs.RO` | AutoBio+: Benchmarking Dexterous Manipulation with Dynamic Experimental Phenomena in Realistic Laboratories | 2026-10-09 | PDF | [2610.13643v1](https://arxiv.org/abs/2610.13643v1) |
| 10 | `cs.HC` | SPHERE: Adaptive VR Indoor Scene Generation via LLM-Enhanced Spatial Preference Learning and Human-in-the-Loop RL | 2026-10-01 | PDF | [2610.02023v1](https://arxiv.org/abs/2610.02023v1) |
| 11 | `stat.ML` | Conformal Prediction for Spatially Dependent Data via Sequential Whitening | 2026-10-07 | PDF | [2610.10168v1](https://arxiv.org/abs/2610.10168v1) |
| 12 | `math.OC` | Decentralized SGD under Heavy-Tailed Noise: Optimal Convergence Rates and the Role of Gradient Clipping | 2026-10-07 | PDF | [2610.10527v1](https://arxiv.org/abs/2610.10527v1) |
| 13 | `math.PR` | An infinite-dimensional Skorokhod problem with a diagonalization approach | 2026-10-02 | TXT | [2610.03541v1](https://arxiv.org/abs/2610.03541v1) |
| 14 | `quant-ph` | Error-Corrected Memory and Logic on a Heavy-Hex Superconducting-Qubit Processor | 2026-10-08 | TXT | [2610.11658v1](https://arxiv.org/abs/2610.11658v1) |
| 15 | `cond-mat.mtrl-sci` | Specialized machine learning force fields for materials dynamics | 2026-10-08 | TXT | [2610.12151v2](https://arxiv.org/abs/2610.12151v2) |
| 16 | `astro-ph.EP` | Correcting stellar contamination in transmission spectroscopy with contemporaneous monitoring: Application to GJ 1214 b | 2026-09-28 | TXT | [2609.35721v1](https://arxiv.org/abs/2609.35721v1) |
| 17 | `q-bio.BM` | Fold'EM: Direct atomic structure inference from Cryo-EM particles | 2026-10-01 | MD | [2610.01358v2](https://arxiv.org/abs/2610.01358v2) |
| 18 | `q-fin.PM` | Eliciting ESG Preferences for Reinforcement Learning-Based Portfolio Optimization | 2026-09-02 | MD | [2609.02677v1](https://arxiv.org/abs/2609.02677v1) |
| 19 | `eess.AS` | Lossless Inference Acceleration for ASR via EAGLE-Style Speculative Decoding | 2026-10-09 | MD | [2610.13506v1](https://arxiv.org/abs/2610.13506v1) |
| 20 | `econ.EM` | Conditional Tensor Diffusion: Distributional Counterfactual Learning and Inference | 2026-09-22 | MD | [2609.25924v1](https://arxiv.org/abs/2609.25924v1) |

## 注意

- 这些是**预印本**，未经过同行评审。用作 RAG 语料没问题（你要的是「有内容可检索」），
  但**不要**在报告里把它们当作已确立的结论引用。
- 想换成自己的语料：把这 20 个文件删掉，换成你的文档，然后重建索引。
- 主题跨度刻意做得很大（20 个领域），好处是能**测出混合检索 vs 纯向量检索的差异**：
  跨领域语料里专有名词多（如 `Skorokhod`、`conformal prediction`），
  纯向量检索容易漏，BM25 关键词检索能补上 —— 这正好是第 8 步要验证的事。
