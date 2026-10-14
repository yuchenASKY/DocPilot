# `data/docs` 语料来源清单

本目录共 **20 篇** arXiv 预印本（开放获取），**全部是 AI / 检索 / RAG 技术方向**，共 25.9 MB。抓取时间：2026-10-13。

> 为什么全用 arXiv：它是**开放获取**，PDF 可合法下载再分发到本地知识库；
> 而 Elsevier / Springer / IEEE 等出版社的 PDF 有付费墙，不适合直接入库。

---

## 为什么是「垂直」而不是「多领域」

项目定位是 **技术文档问答（DocPilot）**，语料越垂直，做得越深、面试越好讲。

另外还有两个实际好处：

1. **golden set 写得出来** —— 20 篇同领域论文你才有可能人工标注 40 条问答对；
   跨度 20 个学科时，你连「标准答案是什么」都判断不了。
2. **评测结论可信** —— 第 12 步要对比「混合检索 vs 纯向量」，
   同领域语料里专有名词密度高，差异才看得出来。

> 曾经还有一批 20 篇跨学科论文（天文 / 量子 / 生物 / 金融），已移到 `data/_archive_batch1/` —— **不在 `docs/` 下，所以不会被入库**。
> 想拿回来测「跨领域检索」就把它移回 `docs/`，然后重建索引。

---

## 格式分布

| 格式 | 篇数 | 作用 |
|---|---|---|
| `.pdf` | 14 | 真实语料形态，考验第 5 步的 PDF 解析（pypdf） |
| `.txt` | 3 | 纯文本，由 PDF 提取正文，考验最简解析分支 |
| `.md` | 3 | Markdown，由 PDF 正文重排（带标题层级），考验 MD 解析 |

> 同一篇论文**只保留一种格式** —— 否则同一内容会入库两份，检索时重复命中。

---

## 清单

主题是按**说明文档里的知识点**挑的，每一篇都对应你后面某一步要学的东西：

| # | 主题 | 标题 | 发布 | 格式 | 对应步骤 | arXiv |
| 1 | chunking | QChunker: Learning Question-Aware Text Chunking for Domain RAG via Multi-Agent Debate | 2026-03-12 | PDF | 第5步 递归切块 | [2603.11650v1](https://arxiv.org/abs/2603.11650v1) |
| 2 | hybrid | Semantic Candidate-Job Matching: A Comparative Evaluation of Dense Embedding Models in Hybrid Re | 2026-09-20 | PDF | 第8步 混合检索 | [2609.23307v1](https://arxiv.org/abs/2609.23307v1) |
| 3 | rrf | Evaluating Biomedical Reranking for LLM-Based Question Answering over Longitudinal Clinical Note | 2026-10-01 | PDF | 第8步 RRF | [2610.01324v1](https://arxiv.org/abs/2610.01324v1) |
| 4 | rerank | Local-to-Global Sentence-Level Graph Reranking for Scientific Synthesis | 2026-08-31 | TXT | 第8步 Rerank | [2608.30525v2](https://arxiv.org/abs/2608.30525v2) |
| 5 | ann | Approximate Nearest Neighbor in Ultra-High Dimensional $\ell_\infty$ | 2026-09-08 | PDF | 第6/8步 向量检索 | [2609.09427v1](https://arxiv.org/abs/2609.09427v1) |
| 6 | dense-retr | Towards Dynamic Dense Retrieval with Routing Strategy | 2026-02-26 | PDF | 第6步 向量化 | [2602.22547v1](https://arxiv.org/abs/2602.22547v1) |
| 7 | rag | The Effect of Text Chunk Size on Retrieval-Augmented Generation Performance | 2026-06-08 | MD | 全项目 综述 | [2607.24767v1](https://arxiv.org/abs/2607.24767v1) |
| 8 | query-rw | ReSequel: Robust LLM-assisted Query Rewriting and Optimization using Templatization and Sampling | 2026-06-18 | PDF | 第11步 Query Rewrite | [2606.20853v2](https://arxiv.org/abs/2606.20853v2) |
| 9 | tool-call | SimpleTool: Parallel Decoding for Real-Time LLM Function Calling | 2026-02-04 | PDF | 第9步 工具调用 | [2603.00030v1](https://arxiv.org/abs/2603.00030v1) |
| 10 | faithful | Automatic Layer Selection for Hallucination Detection | 2026-05-25 | TXT | 第12步 忠实度 | [2605.26366v3](https://arxiv.org/abs/2605.26366v3) |
| 11 | rag-eval | Towards Query-Agnostic RAG Evaluation via Query Coverage and Claim Verifiability | 2026-07-31 | PDF | 第12步 评测体系 | [2608.11238v3](https://arxiv.org/abs/2608.11238v3) |
| 12 | conv | Conversational Search: From Fundamentals to Frontiers in the LLM Era | 2025-06-12 | TXT | 第11步 多轮记忆 | [2506.10635v1](https://arxiv.org/abs/2506.10635v1) |
| 13 | sem-cache | LaCache: Robust Semantic Caching for LLM Serving | 2026-08-03 | MD | 第13步 Redis 缓存 | [2608.01718v1](https://arxiv.org/abs/2608.01718v1) |
| 14 | ctx-comp | Prompt Compression in Diffusion Large Language Models: Evaluating LLMLingua-2 on LLaDA | 2026-05-18 | PDF | 第11步 上下文工程 | [2605.17932v2](https://arxiv.org/abs/2605.17932v2) |
| 15 | long-ctx | Incentivizing In-depth Reasoning over Long Contexts with Process Advantage Shaping | 2026-01-18 | PDF | 第11步 长上下文 | [2601.12465v1](https://arxiv.org/abs/2601.12465v1) |
| 16 | graphrag | STAR: Semantic-Tuned and Tail-Adaptive Retriever for Graph-Augmented Generation | 2026-04-11 | PDF | 进阶 GraphRAG | [2605.18765v1](https://arxiv.org/abs/2605.18765v1) |
| 17 | embedding | Focusing Condition: Inference-Time Self-Contrastive Steering Elicits Better Conditional Text Emb | 2026-09-26 | PDF | 第6步 embedding 模型 | [2609.32684v1](https://arxiv.org/abs/2609.32684v1) |
| 18 | doc-parse | RT-DocLayout: Real-Time End-to-End Document Layout Analysis with Reading Order in the Wild | 2026-06-22 | MD | 第5步 文档解析 | [2606.23344v1](https://arxiv.org/abs/2606.23344v1) |
| 19 | llm-serve | LLM Serving in the Wild: An Empirical Study of Frameworks, Methods, and System Designs | 2026-08-04 | PDF | 第13步 部署性能 | [2608.03036v1](https://arxiv.org/abs/2608.03036v1) |
| 20 | distill | Uncertainty-Aware Dual-Student Knowledge Distillation for Efficient Image Classification | 2025-11-24 | PDF | 进阶 蒸馏优化 | [2511.18826v1](https://arxiv.org/abs/2511.18826v1) |

---

## 注意

**1）这批是预印本，未经同行评审。** 用作 RAG 语料没问题（你要的是「有内容可检索」），
但**不要**在报告里把它们当已确立的结论引用。

**2）语料变了，索引必须重建。**

```bash
.venv/Scripts/python.exe scripts/build_index.py --rebuild
```

**3）中文问题 + 英文语料 + 离线伪向量 = 检索不到。** 这点很重要：

- 论文正文是英文，而离线伪向量是「字符 3-gram 哈希」，**只认字面重叠、不懂语义**；
- 你问「切块策略有哪些做法」，它没法命中英文的 `chunking strategies`。

两个办法，任选：

- **换用真实 embedding 模型**（`BAAI/bge-m3` 之类的多语言模型，中英跨语言），第 8 步之前必须做；
- **测试时直接用英文提问**（如 `What are common text chunking strategies?`），伪向量下就能命中。

**4）关于「怎么防止缓存被击穿」这类问题。** 学术论文里**没有**这种工程细节 ——
`LaCache` 讲的是语义缓存的设计与鲁棒性，能覆盖抽象的「缓存」概念，
但「缓存击穿 / 雪崩」是工程实践词。想测这类问题，要么换个学术化的问法
（如「语义缓存的命中率怎么保证」），要么另外把技术博客 / 官方文档放进 `docs/`。
