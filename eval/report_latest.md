# DocPilot 评测报告

- 题目数量：40
- 检索命中率：**95.0%**
- 平均耗时：4022.7 ms

> 命中判定规则：`expected_source` 落在返回的 `sources` 里算命中；
> `expected_source` 为空（应拒答）时，以「**没有返回任何来源**」算命中。

## 生成层指标（RAGAS）

本轮未启用（`--no-ragas` 或没有可用样本）。

## 逐题明细

| # | 问题 | 期望来源 | 实际来源 | 命中 | 耗时(ms) |
| --- | --- | --- | --- | --- | --- |
| 1 | 文本切块有哪些策略？ | chunking-csCL_QChunker-Learning-Question-Aware-Text-Chunking-for-D_2603.11650v1.pdf | chunking-csCL_QChunker-Learning-Question-Aware-Text-Chunking-for-D_2603.11650v1.pdf, rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md | Y | 13088 |
| 2 | 文本块的大小会怎么影响 RAG 的效果？ | rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md | rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md | Y | 4622 |
| 3 | 用大模型做查询改写一般怎么做？ | query-rw-csDB_ReSequel-Robust-LLM-assisted-Query-Rewriting-and-Opt_2606.20853v2.pdf | conv-csIR_Conversational-Search-From-Fundamentals-to-Frontiers_2506.10635v1.txt, query-rw-csDB_ReSequel-Robust-LLM-assisted-Query-Rewriting-and-Opt_2606.20853v2.pdf | Y | 3647 |
| 4 | 语义缓存是怎么判断命中的？ | sem-cache-csAI_LaCache-Robust-Semantic-Caching-for-LLM-Serving_2608.01718v1.md | sem-cache-csAI_LaCache-Robust-Semantic-Caching-for-LLM-Serving_2608.01718v1.md | Y | 4056 |
| 5 | 怎么检测大语言模型的幻觉？ | faithful-csAI_Automatic-Layer-Selection-for-Hallucination-Detectio_2605.26366v3.txt | faithful-csAI_Automatic-Layer-Selection-for-Hallucination-Detectio_2605.26366v3.txt | Y | 3253 |
| 6 | RAG 系统应该用什么指标来评测？ | rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf | rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf | Y | 5058 |
| 7 | 重排阶段是怎么给候选句子打分的？ | rerank-csIR_Local-to-Global-Sentence-Level-Graph-Reranking-for-S_2608.30525v2.txt | rerank-csIR_Local-to-Global-Sentence-Level-Graph-Reranking-for-S_2608.30525v2.txt | Y | 4339 |
| 8 | 近似最近邻检索在高维空间会遇到什么困难？ | ann-csDS_Approximate-Nearest-Neighbor-in-Ultra-High-Dimension_2609.09427v1.pdf | ann-csDS_Approximate-Nearest-Neighbor-in-Ultra-High-Dimension_2609.09427v1.pdf | Y | 3454 |
| 9 | 稠密检索为什么要引入路由策略？ | dense-retr-csIR_Towards-Dynamic-Dense-Retrieval-with-Routing-Strateg_2602.22547v1.pdf | dense-retr-csIR_Towards-Dynamic-Dense-Retrieval-with-Routing-Strateg_2602.22547v1.pdf | Y | 3068 |
| 10 | 提示压缩会不会损失效果？ | ctx-comp-csCL_Prompt-Compression-in-Diffusion-Large-Language-Model_2605.17932v2.pdf | ctx-comp-csCL_Prompt-Compression-in-Diffusion-Large-Language-Model_2605.17932v2.pdf | Y | 4095 |
| 11 | QChunker 是怎么做文本切块的？ | chunking-csCL_QChunker-Learning-Question-Aware-Text-Chunking-for-D_2603.11650v1.pdf | chunking-csCL_QChunker-Learning-Question-Aware-Text-Chunking-for-D_2603.11650v1.pdf | Y | 3186 |
| 12 | ReSequel 是怎么做查询改写的？ | query-rw-csDB_ReSequel-Robust-LLM-assisted-Query-Rewriting-and-Opt_2606.20853v2.pdf | query-rw-csDB_ReSequel-Robust-LLM-assisted-Query-Rewriting-and-Opt_2606.20853v2.pdf | Y | 4205 |
| 13 | LaCache 是怎么实现语义缓存的？ | sem-cache-csAI_LaCache-Robust-Semantic-Caching-for-LLM-Serving_2608.01718v1.md | sem-cache-csAI_LaCache-Robust-Semantic-Caching-for-LLM-Serving_2608.01718v1.md | Y | 3949 |
| 14 | Q-CARE 用什么指标来评测 RAG？ | rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf | rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf | Y | 3506 |
| 15 | RT-DocLayout 的实时性是怎么量化的？ | doc-parse-csCV_RT-DocLayout-Real-Time-End-to-End-Document-Layout-An_2606.23344v1.md | doc-parse-csCV_RT-DocLayout-Real-Time-End-to-End-Document-Layout-An_2606.23344v1.md | Y | 2947 |
| 16 | SimpleTool 是怎么加速函数调用的？ | tool-call-csCL_SimpleTool-Parallel-Decoding-for-Real-Time-LLM-Funct_2603.00030v1.pdf | tool-call-csCL_SimpleTool-Parallel-Decoding-for-Real-Time-LLM-Funct_2603.00030v1.pdf | Y | 5295 |
| 17 | STAR 检索器是怎么利用知识图谱的？ | graphrag-csIR_STAR-Semantic-Tuned-and-Tail-Adaptive-Retriever-for_2605.18765v1.pdf | graphrag-csIR_STAR-Semantic-Tuned-and-Tail-Adaptive-Retriever-for_2605.18765v1.pdf | Y | 3495 |
| 18 | 自对比引导是怎么改善文本表示的？ | embedding-csCL_Focusing-Condition-Inference-Time-Self-Contrastive-S_2609.32684v1.pdf | embedding-csCL_Focusing-Condition-Inference-Time-Self-Contrastive-S_2609.32684v1.pdf | Y | 3417 |
| 19 | LLM 推理服务常用的框架有哪些？ | llm-serve-csSE_LLM-Serving-in-the-Wild-An-Empirical-Study-of-Framew_2608.03036v1.pdf | llm-serve-csSE_LLM-Serving-in-the-Wild-An-Empirical-Study-of-Framew_2608.03036v1.pdf | Y | 3551 |
| 20 | 不确定性感知的双学生知识蒸馏是怎么做的？ | distill-csCV_Uncertainty-Aware-Dual-Student-Knowledge-Distillatio_2511.18826v1.pdf | distill-csCV_Uncertainty-Aware-Dual-Student-Knowledge-Distillatio_2511.18826v1.pdf | Y | 4006 |
| 21 | LLMLingua-2 是什么？ | ctx-comp-csCL_Prompt-Compression-in-Diffusion-Large-Language-Model_2605.17932v2.pdf | ctx-comp-csCL_Prompt-Compression-in-Diffusion-Large-Language-Model_2605.17932v2.pdf | Y | 3795 |
| 22 | cross-encoder 和双塔模型有什么区别？ | rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf | dense-retr-csIR_Towards-Dynamic-Dense-Retrieval-with-Routing-Strateg_2602.22547v1.pdf, graphrag-csIR_STAR-Semantic-Tuned-and-Tail-Adaptive-Retriever-for_2605.18765v1.pdf, hybrid-csIR_Semantic-Candidate-Job-Matching-A-Comparative-Evalua_2609.23307v1.pdf | N | 4808 |
| 23 | BM25 在重排流程里扮演什么角色？ | rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf | rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf, rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf | Y | 4597 |
| 24 | 什么是 ℓ∞ 范数下的近似最近邻？ | ann-csDS_Approximate-Nearest-Neighbor-in-Ultra-High-Dimension_2609.09427v1.pdf | ann-csDS_Approximate-Nearest-Neighbor-in-Ultra-High-Dimension_2609.09427v1.pdf | Y | 4755 |
| 25 | FRAMES 这个基准测的是什么？ | long-ctx-csCL_Incentivizing-In-depth-Reasoning-over-Long-Contexts_2601.12465v1.pdf | hybrid-csIR_Semantic-Candidate-Job-Matching-A-Comparative-Evalua_2609.23307v1.pdf, long-ctx-csCL_Incentivizing-In-depth-Reasoning-over-Long-Contexts_2601.12465v1.pdf, tool-call-csCL_SimpleTool-Parallel-Decoding-for-Real-Time-LLM-Funct_2603.00030v1.pdf | Y | 2988 |
| 26 | SimpleTool 的 parallel decodi | tool-call-csCL_SimpleTool-Parallel-Decoding-for-Real-Time-LLM-Funct_2603.00030v1.pdf | tool-call-csCL_SimpleTool-Parallel-Decoding-for-Real-Time-LLM-Funct_2603.00030v1.pdf | Y | 4357 |
| 27 | 文档版面分析要识别哪些元素？ | doc-parse-csCV_RT-DocLayout-Real-Time-End-to-End-Document-Layout-An_2606.23344v1.md | doc-parse-csCV_RT-DocLayout-Real-Time-End-to-End-Document-Layout-An_2606.23344v1.md | Y | 2843 |
| 28 | 对话式检索和传统检索有什么区别？ | conv-csIR_Conversational-Search-From-Fundamentals-to-Frontiers_2506.10635v1.txt | conv-csIR_Conversational-Search-From-Fundamentals-to-Frontiers_2506.10635v1.txt | Y | 3377 |
| 29 | 混合检索和 Rerank 有什么区别？ | rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf | hybrid-csIR_Semantic-Candidate-Job-Matching-A-Comparative-Evalua_2609.23307v1.pdf, rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf, rerank-csIR_Local-to-Global-Sentence-Level-Graph-Reranking-for-S_2608.30525v2.txt, rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf | Y | 4989 |
| 30 | 块大小和检索质量之间是什么关系？ | rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md | rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md | Y | 4840 |
| 31 | 查询改写和重排分别发生在 RAG 流程的哪个阶段？ | query-rw-csDB_ReSequel-Robust-LLM-assisted-Query-Rewriting-and-Opt_2606.20853v2.pdf | conv-csIR_Conversational-Search-From-Fundamentals-to-Frontiers_2506.10635v1.txt, rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md, rerank-csIR_Local-to-Global-Sentence-Level-Graph-Reranking-for-S_2608.30525v2.txt | N | 3919 |
| 32 | 幻觉检测和忠实度指标有什么关系？ | faithful-csAI_Automatic-Layer-Selection-for-Hallucination-Detectio_2605.26366v3.txt | faithful-csAI_Automatic-Layer-Selection-for-Hallucination-Detectio_2605.26366v3.txt, rag-eval-csAI_Towards-Query-Agnostic-RAG-Evaluation-via-Query-Cove_2608.11238v3.pdf | Y | 5389 |
| 33 | 长上下文模型能替代 RAG 吗？ | long-ctx-csCL_Incentivizing-In-depth-Reasoning-over-Long-Contexts_2601.12465v1.pdf | long-ctx-csCL_Incentivizing-In-depth-Reasoning-over-Long-Contexts_2601.12465v1.pdf, rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md, rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf | Y | 4054 |
| 34 | 提示压缩和上下文工程是什么关系？ | ctx-comp-csCL_Prompt-Compression-in-Diffusion-Large-Language-Model_2605.17932v2.pdf | ctx-comp-csCL_Prompt-Compression-in-Diffusion-Large-Language-Model_2605.17932v2.pdf, embedding-csCL_Focusing-Condition-Inference-Time-Self-Contrastive-S_2609.32684v1.pdf | Y | 4203 |
| 35 | 知识蒸馏和模型压缩的共同目标是什么？ | distill-csCV_Uncertainty-Aware-Dual-Student-Knowledge-Distillatio_2511.18826v1.pdf | distill-csCV_Uncertainty-Aware-Dual-Student-Knowledge-Distillatio_2511.18826v1.pdf | Y | 3867 |
| 36 | 语义缓存和向量检索有什么联系？ | sem-cache-csAI_LaCache-Robust-Semantic-Caching-for-LLM-Serving_2608.01718v1.md | sem-cache-csAI_LaCache-Robust-Semantic-Caching-for-LLM-Serving_2608.01718v1.md | Y | 4770 |
| 37 | 量子纠缠的最新实验进展是什么？ |  | - | Y | 4437 |
| 38 | 2026 年世界杯的冠军是哪支球队？ |  | - | Y | 941 |
| 39 | 红烧肉怎么做才好吃？ |  | - | Y | 849 |
| 40 | 苏州有哪些值得去的古典园林？ |  | - | Y | 894 |

## 失败案例分析

### 一、该命中却没命中（2 条）

- **cross-encoder 和双塔模型有什么区别？**：期望 `rrf-csCL_Evaluating-Biomedical-Reranking-for-LLM-Based-Questi_2610.01324v1.pdf`，实际 `dense-retr-csIR_Towards-Dynamic-Dense-Retrieval-with-Routing-Strateg_2602.22547v1.pdf, graphrag-csIR_STAR-Semantic-Tuned-and-Tail-Adaptive-Retriever-for_2605.18765v1.pdf, hybrid-csIR_Semantic-Candidate-Job-Matching-A-Comparative-Evalua_2609.23307v1.pdf`。
  排查方向：① 该文档是否真的入库（`--rebuild` 后确认片段数）；② 切块是否过碎、切断了关键段落；③ `top_k` 是否太小；④ **问法太泛**（没有专有名词时向量分不开，多篇文档得分接近）—— 这一类要靠术语词典或 Rerank 精排。
- **查询改写和重排分别发生在 RAG 流程的哪个阶段？**：期望 `query-rw-csDB_ReSequel-Robust-LLM-assisted-Query-Rewriting-and-Opt_2606.20853v2.pdf`，实际 `conv-csIR_Conversational-Search-From-Fundamentals-to-Frontiers_2506.10635v1.txt, rag-csIR_The-Effect-of-Text-Chunk-Size-on-Retrieval-Augmented_2607.24767v1.md, rerank-csIR_Local-to-Global-Sentence-Level-Graph-Reranking-for-S_2608.30525v2.txt`。
  排查方向：① 该文档是否真的入库（`--rebuild` 后确认片段数）；② 切块是否过碎、切断了关键段落；③ `top_k` 是否太小；④ **问法太泛**（没有专有名词时向量分不开，多篇文档得分接近）—— 这一类要靠术语词典或 Rerank 精排。
> ⚠️ 注意「应拒答」那类如果**偶尔**命中，可能是巧合：
> 问题里含「最新」「今天」这类词会走 `route == "tool"` 分支，
> 那条路不检索，`sources` 恰好为空 ⇒ 被判定成「成功拒答」。
> 这不是真的拒答能力，别写进简历。


## 检索方案对比（已实测 · 40 题 golden set）

> ⚠️ 下面这几行是**历史实测数据**（2026-10-15 跑的），**不是本次运行的结果** ——
> 本次的命中率看上面「总览」。这张表的意义是「横向比出哪个方案更好」，
> 面试官问「你怎么知道加了 X 有效」时，答案就是它。

| 配置 | 检索命中率（语料内） | 平均延迟/题 | 结论 |
| --- | --- | --- | --- |
| 纯向量 | 94.4%（34/36） | 358 ms | 基线 |
| + BM25 混合检索（RRF 融合） | 94.4%（34/36） | 815 ms | 没提升 —— 中文问 + 英文料时 BM25 是负资产 |
| **+ 真 Rerank（走纯向量路线）** | **97.2%（35/36）** | 4631 ms | 有效，但 **13 倍延迟** ⇒ 默认关闭 |
| + 混合检索 + 真 Rerank | 94.4%（34/36） | 5144 ms | 被 BM25 拖着，重排也救不回来 |

> Rerank 用的是阿里百炼 `gte-rerank-v2`；单次调用稳定 4.3 秒（测 6 次）。
> 复现方式：把 `.env` 的 `USE_RERANK` 改成 `true` 再跑一遍本脚本。
