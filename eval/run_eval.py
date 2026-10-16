"""评测脚本 —— 第 12 步的核心产出（面试杀手锏）。

它会做四件事：
1. 逐题跑一遍 /chat 链路，记录耗时；
2. 算「检索命中率」（期望来源文档是否出现在返回的 sources 里）；
3. 用 RAGAS 算三个生成层指标：faithfulness / answer_relevancy / context_recall；
4. 输出一份 Markdown 评测报告，含逐题明细与失败案例。

用法：
    uv run python eval/run_eval.py --limit 5      # 先跑 5 题试水（强烈建议）
    uv run python eval/run_eval.py                # 全量 40 题（RAGAS 很慢，见下）
    uv run python eval/run_eval.py --no-ragas     # 只算检索命中率，跳过 RAGAS

为什么「检索命中率」不叫「准确率」：
检索阶段没有标准答案可比，只能看「该命中的文档有没有被召回」。
这就是命中率（Hit Rate），也是 RAGAS 里 context_recall 的简化版。

⚠️ 关于 RAGAS 的速度：每题要**多次** LLM 调用（faithfulness 要逐句归因），
实测 2 条数据就要 68 秒 ⇒ 40 题大约半小时。所以：
先 `--limit 5` 确认流程通了，再决定要不要全量跑。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import graph, tracing  # noqa: E402
from app.config import settings  # noqa: E402
from app.retriever import retrieve  # noqa: E402

# 注意：ragas 相关的 import 全部写在函数内部（见 run_ragas）——
# 它这一套的版本坑比较多（下面 _install_vertexai_stub 有详细说明），
# 放函数里能保证「即使 RAGAS 挂了，检索命中率这部分照样能跑出来」。

EVAL_FILE = Path(__file__).resolve().parent / "golden_set.jsonl"

RAGAS_METRIC_NAMES = ("faithfulness", "answer_relevancy", "context_recall")
RAGAS_TOP_K = 5
RAGAS_MAX_TOKENS = 4096  # ★ 见 build_ragas_llm 的注释


def load_golden() -> list[dict]:
    items = []
    with EVAL_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


# ---------------------------------------------------------------- RAGAS 部分


def _install_vertexai_stub() -> None:
    """★ 坑 1：`import ragas` 会直接 ModuleNotFoundError，必须先补这个 stub。

    根因：ragas 0.4.3 的 `ragas/llms/base.py` 里写了
        from langchain_community.chat_models.vertexai import ChatVertexAI
    而 langchain-community 0.4.2 **已经把这个模块删掉了**（上游没同步）——
    两个都是各自的最新版，但互相不兼容。

    `ChatVertexAI` 只出现在 ragas 的
        MULTIPLE_COMPLETION_SUPPORTED = [OpenAI, ChatOpenAI, ..., ChatVertexAI, VertexAI]
    这个列表里，用途是 `isinstance` 式判断「该 LLM 是否支持 n-completion」，
    **永远不会被实例化** ⇒ 所以一个空类就够。
    """
    import langchain_community.chat_models as _cm

    if hasattr(_cm, "ChatVertexAI"):
        return
    _stub = types.ModuleType("langchain_community.chat_models.vertexai")

    class ChatVertexAI: ...

    _stub.ChatVertexAI = ChatVertexAI
    sys.modules["langchain_community.chat_models.vertexai"] = _stub


def build_ragas_llm():
    """给 RAGAS 单独造一个 LLM 实例。

    ★ 坑 2：**不能用项目默认的配置**。faithfulness / context_recall 要让模型输出
    「逐句归因」的结构化 JSON，内容很长；而项目里 `llm_max_tokens = 1024`，
    不够用 ⇒ RAGAS 抛 IncompleteOutputException ⇒ 指标全是 NaN。
    所以这里单独给 4096，不动项目的全局配置。
    """
    from openai import OpenAI
    from ragas.llms import llm_factory

    return llm_factory(
        settings.llm_model,
        client=OpenAI(api_key=settings.openai_api_key,
                      base_url=settings.openai_base_url),
        max_tokens=RAGAS_MAX_TOKENS,
    )


def build_ragas_embeddings():
    """embedding 走项目自己那套（本项目是阿里百炼，不是 OpenAI）。

    ★ 坑 3：ragas 0.4.3 的 `OpenAIEmbeddings` 只实现了 `embed_text` / `embed_texts`，
    但 `AnswerRelevancy` 内部调的还是旧接口 `embed_query`
    ⇒ AttributeError ⇒ answer_relevancy 是 NaN。补两个别名即可。
    """
    from openai import OpenAI
    from ragas.embeddings import OpenAIEmbeddings

    emb = OpenAIEmbeddings(
        client=OpenAI(api_key=settings.effective_embed_api_key,
                      base_url=settings.effective_embed_base_url),
        model=settings.embed_model,
    )
    if not hasattr(emb, "embed_query"):
        emb.embed_query = emb.embed_text
    if not hasattr(emb, "embed_documents"):
        emb.embed_documents = emb.embed_texts
    return emb


def _scores_from_result(result) -> dict:
    """从 ragas 的 EvaluationResult 里取出三个指标的均值。

    ⚠️ 不要写 `dict(result)` —— 实测会抛 `KeyError: 0`。走 `to_pandas()` 是公开且稳的。
    """
    names = RAGAS_METRIC_NAMES
    try:
        df = result.to_pandas()
    except Exception as exc:  # noqa: BLE001
        print(f"      [!] 解析 RAGAS 结果失败：{exc}")
        return {}
    return {n: round(float(df[n].mean()), 4) for n in names if n in df.columns}


async def run_ragas(records: list[dict]) -> dict:
    """把「完整答案 + 片段全文 + ground_truth」送进 RAGAS，返回三个生成层指标。

    为什么需要 records 而不是直接用 run() 里的 details：
    details 里有 `answer_preview`（**截到 120 字符**）和 `got_sources`（**只有文件名**），
    这两样都喂不了 RAGAS —— 它要完整答案和片段**全文**。
    """
    if not records:
        print("[!] 没有可用于 RAGAS 的样本（需要有 ground_truth），跳过。")
        return {}
    if not settings.embed_enabled:
        print("[!] 没有配真实 embedding 服务，RAGAS 的 answer_relevancy 算不了，跳过。")
        return {}

    _install_vertexai_stub()
    from datasets import Dataset
    from ragas import evaluate

    # 这里刻意用 ragas.metrics 的「旧」路径：它会提醒
    # "Importing ... from 'ragas.metrics' is deprecated, use 'ragas.metrics.collections'"，
    # 但实测 `ragas.metrics.collections.faithfulness` 拿到的是**子模块**（module），
    # 不是能直接喂给 evaluate 的指标对象 —— 新路径的用法还没稳定。
    # 所以先留着旧路径：那两条 DeprecationWarning 不影响结果，等 ragas v1.0 再迁移。
    from ragas.metrics import answer_relevancy, context_recall, faithfulness

    data = Dataset.from_dict({
        "question":     [d["question"] for d in records],
        "answer":       [d["answer"] for d in records],
        "contexts":     [d["contexts"] for d in records],
        "ground_truth": [d["ground_truth"] for d in records],
    })
    print(f"[*] RAGAS 开始评测 {len(records)} 条（每条要多次 LLM 调用，耐心等）…")
    result = evaluate(
        data,
        metrics=[faithfulness, answer_relevancy, context_recall],
        llm=build_ragas_llm(),
        embeddings=build_ragas_embeddings(),
    )
    scores = _scores_from_result(result)
    print(f"[*] RAGAS 结果：{scores}")
    return scores


async def _full_contexts(question: str) -> list[str]:
    """取检索片段的**全文**给 RAGAS 用。

    `graph` 返回的 `sources[].text` 被截到 200 字符 —— 信息量不够会让 RAGAS 失真
    （faithfulness 会误判成「不忠实」）。所以这里再检索一次拿全文，多花约 300 ms/题。
    """
    try:
        hits = await retrieve(question, top_k=RAGAS_TOP_K, use_hybrid=True)
        return [h.text for h in hits]
    except Exception as exc:  # noqa: BLE001
        print(f"      [!] 取 context 失败：{exc}")
        return []


# ---------------------------------------------------------------- 检索评测


async def run(limit: int | None = None) -> tuple[dict, list[dict]]:
    """跑一遍检索评测。

    返回 `(report, records)`：
      - `report` 会被写进 `report_latest.md` / `.json`（结构固定，见下）；
      - `records` 是给 RAGAS 用的完整样本（**不写进 json**，因为有完整上下文，体积大）。

    `report` 的结构是固定的 —— 因为下面的 `write_markdown()` 直接读它，
    改字段名会导致报告生成失败。必须包含：

        {
          "total":          int,      # 题目总数
          "hit_rate":       float,    # 命中率，0~1
          "avg_latency_ms": float,    # 平均耗时（毫秒）
          "embed_mode":     ...,      # 说明性字段，报告里会打印
          "details": [                # 逐题明细，每项必须有这 5 个键：
            {
              "question":        str,
              "expected_source": str,
              "got_sources":     list[str],   # 实际命中的来源文件名
              "hit":             bool,
              "latency_ms":      int,
              # "answer_preview" / "error" 可选，但强烈建议加上
            },
            ...
          ]
        }

    两个必须处理的细节：
      - 单题失败不能让整个评测崩掉 —— try/except 包住每题，继续跑下一题；
      - `expected_source` 为空的题目（「应该拒答」那类），命中规则是
        「**没有返回任何来源**」才算命中，这条要写进报告（面试官会问「你怎么定义命中」）。
    """
    items = load_golden()
    if limit:
        items = items[:limit]

    details: list[dict] = []
    records: list[dict] = []
    hits = 0
    total_ms = 0

    print(f"[*] 共 {len(items)} 题，开始评测…\n")
    for i, item in enumerate(items, start=1):
        t0 = time.perf_counter()
        try:
            result = await graph.run_pipeline(item["question"], session_id=f"eval-{i}")
            error = ""
        except Exception as exc:  # noqa: BLE001
            # 单题失败不能让整个评测崩掉，记下错误继续跑下一题
            result, error = {"sources": [], "answer": ""}, str(exc)

        cost_ms = int((time.perf_counter() - t0) * 1000)
        total_ms += cost_ms

        got_sources = {s["source"] for s in result.get("sources", [])}
        expect = item.get("expected_source", "")
        # expected_source 为空的题（典型是「应该拒答」那一类）：
        # 这类题的正确行为是「检索不到东西」，所以用「没有来源」当作命中。
        # 这个判定规则要写进评测报告 —— 面试官会问「你怎么定义命中」。
        hit = (expect in got_sources) if expect else (not got_sources)
        hits += int(hit)

        flag = "命中" if hit else "未命中"
        print(f"  {i:>2}. [{flag}] {item['question'][:36]}  ({cost_ms} ms)")
        if error:
            print(f"      错误：{error}")

        details.append(
            {
                "question": item["question"],
                "expected_source": expect,
                "got_sources": sorted(got_sources),
                "hit": hit,
                "latency_ms": cost_ms,
                "answer_preview": (result.get("answer") or "")[:120],
                "error": error,
            }
        )

        # ★ 给 RAGAS 攒样本：只要「有 ground_truth」的题（拒答题没有标准答案可比）。
        if item.get("ground_truth"):
            records.append(
                {
                    "question": item["question"],
                    "answer": result.get("answer") or "",   # 完整答案
                    "contexts": await _full_contexts(item["question"]),
                    "ground_truth": item["ground_truth"],
                }
            )

    return {
        "total": len(items),
        "hit_rate": round(hits / len(items), 4) if items else 0.0,
        "avg_latency_ms": round(total_ms / len(items), 1) if items else 0.0,
        "embed_mode": settings.embed_dim,
        "details": details,
    }, records


def write_markdown(report: dict, out: Path) -> None:
    lines = [
        "# DocPilot 评测报告",
        "",
        f"- 题目数量：{report['total']}",
        f"- 检索命中率：**{report['hit_rate'] * 100:.1f}%**",
        f"- 平均耗时：{report['avg_latency_ms']} ms",
        "",
        "> 命中判定规则：`expected_source` 落在返回的 `sources` 里算命中；",
        "> `expected_source` 为空（应拒答）时，以「**没有返回任何来源**」算命中。",
        "",
    ]

    rg = report.get("ragas") or {}
    if rg:
        lines += [
            "## 生成层指标（RAGAS）",
            "",
            f"- faithfulness（忠实度）：**{rg.get('faithfulness', '-')}**",
            f"- answer_relevancy（答案相关度）：**{rg.get('answer_relevancy', '-')}**",
            f"- context_recall（上下文召回）：**{rg.get('context_recall', '-')}**",
            "",
            "> 注意 context_recall 天然偏低：语料是英文论文，而 `ground_truth` 是中文概括，",
            "> 语言与粒度都不匹配会让「逐句归因」的判定变严 —— 这是真实信号，不是 bug。",
            "",
        ]
    else:
        lines += ["## 生成层指标（RAGAS）", "", "本轮未启用（`--no-ragas` 或没有可用样本）。", ""]

    lines += [
        "## 逐题明细",
        "",
        "| # | 问题 | 期望来源 | 实际来源 | 命中 | 耗时(ms) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, d in enumerate(report["details"], start=1):
        lines.append(
            f"| {i} | {d['question'][:28]} | {d['expected_source']} | "
            f"{', '.join(d['got_sources']) or '-'} | {'Y' if d['hit'] else 'N'} | "
            f"{d['latency_ms']} |"
        )

    missed = [d for d in report["details"] if not d["hit"]]
    lines += ["", "## 失败案例分析", ""]
    if not missed:
        lines.append("本轮无未命中题目。")
    else:
        # 两类失败的成因**完全不同**，排查方向必须分开写 ——
        # 「检索没找到」和「该拒答却答了」不是一回事，前者调召回，后者调阈值。
        miss_have = [d for d in missed if d["expected_source"]]
        miss_refuse = [d for d in missed if not d["expected_source"]]

        if miss_have:
            lines += [f"### 一、该命中却没命中（{len(miss_have)} 条）", ""]
            for d in miss_have:
                lines.append(
                    f"- **{d['question']}**：期望 `{d['expected_source']}`，"
                    f"实际 `{', '.join(d['got_sources']) or '空'}`。"
                )
                lines.append(
                    "  排查方向：① 该文档是否真的入库（`--rebuild` 后确认片段数）；"
                    "② 切块是否过碎、切断了关键段落；"
                    "③ `top_k` 是否太小；"
                    "④ **问法太泛**（没有专有名词时向量分不开，"
                    "多篇文档得分接近）—— 这一类要靠术语词典或 Rerank 精排。"
                )

        if miss_refuse:
            lines += ["", f"### 二、该拒答却答了（{len(miss_refuse)} 条）", ""]
            for d in miss_refuse:
                got = ", ".join(s.split("_")[0] for s in d["got_sources"][:3])
                lines.append(
                    f"- **{d['question']}**：期望拒答，却返回了 "
                    f"{len(d['got_sources'])} 条来源（`{got}`…）。"
                )
            lines += [
                "",
                "  **共同根因：`retrieve()` 没有相关性阈值** —— "
                "只要索引非空就一定返回 `top_k` 条，"
                "于是 `graph.py` 里那句 `if not hits: 拒答` **永远不触发**，"
                "无关文档照样被当成「引用来源」返回给前端。",
                "",
                "  **修法**：在 `retrieve()` 出口加分数门槛（向量相似度 + 融合分双阈值），"
                "低于门槛的直接丢弃 —— 拒答题才可能命中，`sources` 也不会再误导用户。",
                "",
            ]

        lines += [
            "> ⚠️ 注意「应拒答」那类如果**偶尔**命中，可能是巧合：",
            "> 问题里含「最新」「今天」这类词会走 `route == \"tool\"` 分支，",
            "> 那条路不检索，`sources` 恰好为空 ⇒ 被判定成「成功拒答」。",
            "> 这不是真的拒答能力，别写进简历。",
            "",
        ]

    lines += [
        "",
        "## 检索方案对比（已实测 · 40 题 golden set）",
        "",
        "> ⚠️ 下面这几行是**历史实测数据**（2026-10-15 跑的），**不是本次运行的结果** ——",
        "> 本次的命中率看上面「总览」。这张表的意义是「横向比出哪个方案更好」，",
        "> 面试官问「你怎么知道加了 X 有效」时，答案就是它。",
        "",
        "| 配置 | 检索命中率（语料内） | 平均延迟/题 | 结论 |",
        "| --- | --- | --- | --- |",
        "| 纯向量 | 94.4%（34/36） | 358 ms | 基线 |",
        "| + BM25 混合检索（RRF 融合） | 94.4%（34/36） | 815 ms | 没提升 —— 中文问 + 英文料时 BM25 是负资产 |",
        "| **+ 真 Rerank（走纯向量路线）** | **97.2%（35/36）** | 4631 ms | 有效，但 **13 倍延迟** ⇒ 默认关闭 |",
        "| + 混合检索 + 真 Rerank | 94.4%（34/36） | 5144 ms | 被 BM25 拖着，重排也救不回来 |",
        "",
        "> Rerank 用的是阿里百炼 `gte-rerank-v2`；单次调用稳定 4.3 秒（测 6 次）。",
        "> 复现方式：把 `.env` 的 `USE_RERANK` 改成 `true` 再跑一遍本脚本。",
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[OK] 报告已写入 {out}")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-ragas", action="store_true",
                        help="跳过 RAGAS（只算检索命中率，快）")
    args = parser.parse_args()

    report, records = await run(args.limit)
    print(f"\n检索命中率：{report['hit_rate'] * 100:.1f}%")
    print(f"平均耗时：{report['avg_latency_ms']} ms")

    # 先跑 RAGAS 再写报告，这样报告里能带上分数
    if args.no_ragas:
        report["ragas"] = {}
    else:
        print()
        report["ragas"] = await run_ragas(records)

    out = Path(__file__).resolve().parent / "report_latest.md"
    write_markdown(report, out)

    json_out = Path(__file__).resolve().parent / "report_latest.json"
    json_out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ★ 第 12 步 ⑥：追踪的 span 是批量上报的，**脚本退出前必须 flush**，
    #   否则缓冲区里没发出去的全部丢掉（跑一次评测白跑）。
    if tracing.enabled():
        print("\n[追踪] 正在上报调用链到 Langfuse ...")
    tracing.flush()


if __name__ == "__main__":
    asyncio.run(main())
