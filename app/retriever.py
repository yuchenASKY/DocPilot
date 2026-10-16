"""检索层：向量检索 + BM25 关键词检索 → RRF 融合 → 可选 Rerank。

这一段是整个 RAG 里最能拉开差距的地方，面试几乎所有追问都落在这里：
- 为什么不能只用向量检索？（专有名词、代码标识符、型号数字会漏）
- 怎么融合两路结果？（RRF，按排名而非分数，避免量纲不同）
- Rerank 和向量检索什么区别？（双塔 vs 交叉编码器，精度高但慢）
"""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from . import tracing
from . import vectorstore as vs_mod
from .config import settings
from .embedding import embedder
from .llm import llm_client


@dataclass
class Retrieved:
    text: str
    source: str
    page: int | None
    score: float
    vec_score: float = 0.0
    kw_score: float = 0.0
    rerank_score: float = 0.0


def _tokenize(text: str) -> list[str]:
    """中文分词

    BM25 是基于词的算法，中文没有空格，所以必须先分词，否则整句被当成一个词，
    BM25 会完全失效。

    规格：
      - 返回 list[str]，非空文本的返回值不能为空；
      - 同一个输入必须得到同一个输出（确定性，否则检索结果会飘）。

    提示：
      - 最省事的做法：转小写 → 去掉空白 → 用「单字 + 相邻二字组（bigram）」拼接。
        单字保证召回，二字组提供一点搭配信息，零依赖且对中文够用；
      - 想更进一步：`uv pip install jieba` 后用 `jieba.lcut(text)`，
        切出来的词更准，BM25 效果会明显更好 —— 这可以写进你的优化记录。
    """
    text = text.lower()
    chars = [c for c in text if not c.isspace()]
    # 单字保证召回，相邻二字组提供一点搭配信息 —— 零依赖且对中文够用
    bigrams = [chars[i] + chars[i + 1] for i in range(len(chars) - 1)]
    return chars + bigrams


def _keyword_scores(query: str, metas: list[dict]) -> dict[str, float]:
    """返回 {chunk_id: 关键词分数}。优先用 rank_bm25，缺依赖时退化为重叠度。"""
    if not metas:
        return {}
    corpus = [m["text"] for m in metas]
    q_tokens = _tokenize(query)

    try:
        from rank_bm25 import BM25Okapi

        bm25 = BM25Okapi([_tokenize(d) for d in corpus])
        scores = bm25.get_scores(q_tokens)
        return {
            m["chunk_id"]: float(s) for m, s in zip(metas, scores)
        }
    except ImportError:
        # 降级：按查询词在片段中的覆盖比例打分
        qset = set(q_tokens) or {query}
        out: dict[str, float] = {}
        for m in metas:
            doc = set(_tokenize(m["text"]))
            out[m["chunk_id"]] = len(qset & doc) / max(1, len(qset))
        return out


def _rrf_fuse(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    """RRF 融合

    为什么需要它：向量相似度是 0—1 的余弦值，BM25 分数却是没有上界的实数，
    两者量纲不同，不能直接加权相加（要先归一化，而归一化本身会引入偏差）。
    RRF 只用「名次」，天然规避了整个问题。

    公式：
        score(d) = Σ_i  1 / (k + rank_i(d))

        其中 rank_i(d) 是文档 d 在第 i 路检索结果里的名次（从 1 开始），k 常取 60。

    规格：
      - 入参 rankings 是「多路检索结果」，每一路是一个按相关性降序排好的 doc_id 列表；
      - 返回 {doc_id: 融合分数}；
      - 没被任何一路召回的文档不会出现在结果里。

    举例（用来核对你写对没有，k=60）：
        _rrf_fuse([["a", "b"]], 60)
        → {"a": 1/61 ≈ 0.016393, "b": 1/62 ≈ 0.016129}

        # a 在向量路第 1、在 BM25 路第 2
        _rrf_fuse([["a", "b"], ["b", "a"]], 60)
        → {"a": 1/61 + 1/62, "b": 1/62 + 1/61}   # 两条路都靠前的会赢
    """
    fused: dict[str, float] = {}
    for ranking in rankings:
        # rank 从 1 开始数 —— 名次越靠前，1/(k+rank) 越大
        for rank, doc_id in enumerate(ranking, start=1):
            fused[doc_id] = fused.get(doc_id, 0.0) + 1.0 / (k + rank)
    return fused


@tracing.observe(name="retrieve", as_type="retriever")
async def retrieve(
        query: str,
        top_k: int | None = None,
        *,
        use_hybrid: bool = True,
        use_rerank: bool | None = None,
) -> list[Retrieved]:
    # use_rerank 传 None 时取配置里的开关（USE_RERANK）。
    # 之所以给个「全局开关」而不是默认 True：开它会多一次 API 调用（更慢也更贵），
    # 应该是「你想用才开」，而不是悄悄替你花钱。显式传参仍然优先。
    if use_rerank is None:
        use_rerank = settings.use_rerank
    k = top_k or settings.top_k
    store = vs_mod.store
    if len(store) == 0:
        return []

    # 1) 向量检索
    q_vec = await embedder.embed_one(query)
    vec_hits = store.search(q_vec, top_k=k * 3)
    vec_map = {m["chunk_id"]: (m, s) for m, s in vec_hits}
    vec_ranking = [m["chunk_id"] for m, _ in vec_hits]

    # 2) 关键词检索
    kw_map: dict[str, float] = {}
    kw_ranking: list[str] = []
    if use_hybrid:
        kw_map = _keyword_scores(query, store.metas)
        kw_ranking = sorted(kw_map, key=lambda cid: -kw_map[cid])[: k * 3]

    # 3) RRF 融合
    rankings = [vec_ranking] + ([kw_ranking] if kw_ranking else [])
    fused = _rrf_fuse(rankings, settings.rrf_k)

    # 4) 组装结果
    meta_by_id = {m["chunk_id"]: m for m in store.metas}
    ordered = sorted(fused, key=lambda cid: -fused[cid])[: k * 2]

    results: list[Retrieved] = []
    for cid in ordered:
        m = meta_by_id.get(cid)
        if m is None:
            continue
        results.append(
            Retrieved(
                text=m["text"],
                source=m["source"],
                page=m.get("page"),
                score=fused[cid],
                vec_score=vec_map.get(cid, (None, 0.0))[1],
                kw_score=kw_map.get(cid, 0.0),
            )
        )

    # 5) 相关性阈值过滤（第 12 步 ⑤）
    #    必须在 Rerank **之前** —— 免得把 rerank 的钱花在注定要丢的候选上。
    #    判据用**向量相似度**而不是 RRF 融合分：前者是 0~1 的余弦值、有绝对含义；
    #    后者只在 0.016~0.033 那条窄带里（见 _rrf_fuse 的注释），当不了绝对门槛。
    #    ⚠️ 副作用：只被 BM25 召回、没被向量召回的结果 vec_score 是 0.0，会被一并滤掉。
    #    在本项目语料下无损失（中文问 + 英文料时 BM25 单独 Top-1 就是 0/5）；
    #    但如果以后加了中文语料、BM25 真的开始有用，要重新评估这一步。
    if settings.min_score > 0:
        best = max((r.vec_score for r in results), default=0.0)
        results = [r for r in results if r.vec_score >= settings.min_score]
        if not results:
            # 「一条都没过阈值」是**预期行为**，不是异常：
            # 说明这个问题在知识库里确实没有依据，交给上层（graph.py）去拒答。
            print(f"[retrieve] 无候选过阈值 min_score={settings.min_score}"
                  f"（最高 {best:.4f}）→ 交由上层拒答")

    # 6) 可选 Rerank（交叉编码器精度更高，但更慢更贵，所以只对粗排结果重排）
    if use_rerank:
        results = await _rerank(query, results, k)

    return results[:k]


# 出现这些词，才说明「这句话里有个指代，单看它没法检索」
_PRONOUNS = ("它", "这个", "那个", "这些", "那些", "上面", "前面", "刚才", "该", "此")


def _format_history(history: list[dict], limit: int = 6) -> str:
    """只带最近 limit 条 —— 历史越长越贵，而且更早的内容对改写没有帮助。"""
    rows = []
    for m in history[-limit:]:
        who = "用户" if m.get("role") == "user" else "助手"
        rows.append("%s：%s" % (who, str(m.get("content", ""))[:400]))
    return "\n".join(rows) or "（无）"


def needs_rewrite(question: str, history: list[dict] | None) -> bool:
    """要不要花这次 LLM 调用？两个条件缺一不可：

    1. 有对话历史 —— 单轮提问里不存在「它」指代什么；
    2. 问题里出现指代词 —— 「RRF 怎么融合」这种本身完整的问句，改了也不会更好。

    这是本步最容易忽略、也最能体现工程意识的一点：
    改写要花钱、要加延迟，不该无脑对每个问题都做。
    """
    if not history:
        return False
    return any(p in question for p in _PRONOUNS)


async def rewrite_query(question: str, history: list[dict] | None = None) -> str:
    """把多轮里的「残缺问句」补成可以独立检索的完整问句。

    ★ 失败要能退化：改写没拿到内容（空串）时一律退回原问题 ——
      检索链路绝不能因为「改写这一步出问题」而整个挂掉。
    """

    if not needs_rewrite(question, history):
        return question
    REWRITE_PROMPT = """把用户的最新问题改写成一个不依赖上下文、语义完整、
        可以独立用于检索的问题。只输出改写后的问题，不要解释。

        对话历史：
        {history}

        最新问题：{question}
        改写后："""
    messages = [
        {
            "role": "user",
            "content": REWRITE_PROMPT.format(
                history=_format_history(history or []), question=question
            ),
        }
    ]
    resp = await llm_client.chat(messages, temperature=0.0)
    rewritten = (resp.get("content") or "").strip()
    return rewritten or question


async def _rerank_scores(query: str, texts: list[str]) -> list[float] | None:
    """调真实 cross-encoder rerank 服务，返回与 texts **等长**的相关性分数。

    为什么每次新建 client、而不是像 embedding.py 那样维护连接池：
      rerank 一次请求约 600 ms，建 client 那十几毫秒可以忽略；
      而 httpx 的连接池绑在「创建它的那个事件循环」上，跨循环复用会踩
      `RuntimeError: Event loop is closed`（本项目踩过，见第 11 步）。一次一建天然避开。

    任何失败（网络、限流、响应格式变动）都返回 None ——
    由 `_rerank()` 降级到基线打分。**重排这一环不能把整条检索链路带崩。**
    """
    if not texts:
        return []

    url = (
        settings.effective_rerank_base_url.rstrip("/")
        + "/api/v1/services/rerank/text-rerank/text-rerank"
    )
    payload = {
        "model": settings.rerank_model,
        "input": {"query": query, "documents": texts},
        # return_documents=False：只要分数，不回传原文（省带宽）
        "parameters": {"return_documents": False, "top_n": len(texts)},
    }
    headers = {
        "Authorization": f"Bearer {settings.effective_rerank_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0)
        ) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        results = data["output"]["results"]
    except Exception as exc:  # noqa: BLE001
        print(f"[rerank] 调用失败，降级为覆盖率基线：{type(exc).__name__}: {exc}")
        return None

    # 服务返回的是「按分数降序、带原始下标 index」的列表 ——
    # 必须按 index 还原成与 texts 对齐的顺序，否则分数会错配到别的片段上。
    scores = [0.0] * len(texts)
    for row in results:
        idx = row.get("index")
        if isinstance(idx, int) and 0 <= idx < len(texts):
            scores[idx] = float(row.get("relevance_score", 0.0))
    return scores


async def _rerank(query: str, items: list[Retrieved], top_k: int) -> list[Retrieved]:
    """Rerank 重排序 —— 用**真实 cross-encoder 模型**（配了就走 API）。

    和向量检索的区别（面试必答）：向量检索是双塔，query 和 doc 分别编码再算相似度，
    快但精度有损；Rerank 是交叉编码器，把 query 和 doc 拼在一起过一遍模型，
    token 之间有完整注意力交互，准但慢一到两个数量级。所以只对粗排结果做。

    两条路线：
      A. **真实模型（当前实现）**：调阿里百炼的 `gte-rerank-v2`
         —— 同一个 `EMBED_API_KEY` 就能用，不用另开账号。
         端点走 DashScope 原生路径（百炼**不支持** OpenAI 兼容的 `/rerank`，实测 404）。
         换 provider（Jina / Cohere / BGE）只需改 `.env` 的
         `RERANK_MODEL` + `RERANK_BASE_URL`，代码不用动。
      B. **降级基线**：没配、或调用失败时，用「查询词在片段里的覆盖度」打分。
         效果差（中文问 + 英文料时覆盖率大量为 0），但保证链路完整。

    规格（做到这三条就算过）：
      1. 给每个 item 填上 `it.rerank_score`（float）；
      2. 按 rerank_score 降序返回；
      3. 返回条数 <= top_k。
    """
    if not items:
        return []

    scores = None
    if settings.rerank_enabled:
        scores = await _rerank_scores(query, [it.text for it in items])

    if scores is not None:
        # 真实 cross-encoder 分数：同一个模型出的，量纲一致，可直接排序
        for it, s in zip(items, scores):
            it.rerank_score = s
    else:
        # 降级基线：覆盖率为主、原始 RRF 分为辅。
        # ⚠️ 这两项量纲差一个数量级（实测约 24 倍），实际排序基本由 coverage 决定 ——
        # 这正是第 8 步 ④ 记录过的「量纲失衡」，留在这里当反例。
        terms = set(_tokenize(query))
        for it in items:
            if not terms:
                it.rerank_score = it.score
                continue
            coverage = sum(1 for t in terms if t in it.text) / len(terms)
            it.rerank_score = 0.7 * coverage + 0.3 * it.score

    return sorted(items, key=lambda x: -x.rerank_score)[:top_k]
