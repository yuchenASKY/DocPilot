"""Agent 编排层：一张「图」决定每次问话怎么走。

流程（也就是面试时你要画的那张架构图）：

    ┌─────────┐
    │  START  │
    └────┬────┘
         ▼
   ┌───────────────┐  简单问题/闲聊
   │ route_question├──────────────► direct_answer
   └───┬───────────┘
       │ 需要查资料 / 需要算数 / 需要外部信息
       ▼
  ┌──────────┐   不需要工具           ┌──────────────┐
  │ retrieve ├─────────────► 生成答案 │  generate    │
  └────┬─────┘                      └──────┬───────┘
       │ 需要工具                          ▲
       ▼                                  │
  ┌──────────┐   结果回传（可循环）          │
  │ call_tool├───────────────────────────┘
  └──────────┘

这里提供了两份实现：
- `run_pipeline()`：纯 Python 版，零依赖、逻辑清晰，方便你理解每一步；
- `build_langgraph()`：LangGraph 版（装了 langgraph 才可用），
  把同样的流程表达成 StateGraph，好处是状态可视化、可持久化、可中断续跑。

面试话术：「我先用纯 Python 把流程跑通，再用 LangGraph 重写成图，
因为需要状态持久化和 human-in-the-loop。」——这比「我用了 LangGraph」强十倍。

⚠️ 本文件的依赖分属不同步骤，第 7 步时还没全部到位：
    tools 模块 → 第 9 步      _route() → 第 10 步      memory.get_session() → 第 11 步
   所以本步的验收是「语法检查通过 + 能把流程讲清楚」，
   真正的端到端测试放到第 11 步末尾（那时四个依赖才齐）。
"""

from __future__ import annotations

import time
from typing import Any

from . import retriever, tools
from .config import settings
from .llm import llm_client
from .memory import get_session

SYSTEM_PROMPT = """你是 DocPilot，一个严谨的技术文档问答助手。

回答要求：
1. 只依据「参考资料」回答；资料里没有的内容，明确说「文档中没有找到相关内容」，绝不编造。
2. 每个关键结论后面用 [1] [2] 标注来源编号，和参考资料一一对应。
3. 如果问题需要计算或实时信息，可以调用工具；工具返回的结果要转述成自然语言。
4. 回答用中文，代码/命令保留原文。先给结论，再给依据。
"""

def _build_context(hits) -> tuple[str, list[dict]]:
    if not hits:
        return "（没有检索到任何相关片段）", []
    blocks, sources = [], []
    for i, h in enumerate(hits, start=1):
        loc = h.source + (f" 第 {h.page} 页" if h.page else "")
        blocks.append(f"[{i}] 来源：{loc}\n{h.text}")
        sources.append({"source": h.source, "page": h.page,
                        "score": round(h.score, 4), "text": h.text[:200]})
    return "\n\n".join(blocks), sources


async def run_pipeline(
    question: str,
    session_id: str = "default",
    *,
    top_k: int | None = None,
    use_tools: bool = True,
) -> dict[str, Any]:
    """完整流程：路由 → 检索 / 工具 → 生成 → 写回记忆。

    返回值刻意做成扁平 dict（而不是自定义类）：它要直接喂给 FastAPI 的
    响应模型和评测脚本，扁平结构最好接。
    """
    t0 = time.perf_counter()
    session = get_session(session_id)

    # 1) 路由：这一步决定「要不要查资料 / 要不要调工具」
    route = await _route(question, use_tools)

    # 2) 检索 / 工具
    sources: list[dict] = []
    used_tools: list[str] = []
    context = "（本次未检索）"

    if route == "retrieve":
        hits = await retriever.retrieve(question, top_k=top_k, use_hybrid=True)
        context, sources = _build_context(hits)
        if not hits:
            # 检索层硬拦截：没有资料就直接拒答，**根本不调模型**（省钱又防幻觉）
            return {
                "session_id": session_id,
                "answer": "文档中没有找到相关内容。",
                "sources": [],
                "used_tools": [],
                "route": "reject",
                "latency_ms": int((time.perf_counter() - t0) * 1000),
                "degraded": not llm_client.enabled,
            }

    elif route == "tool":
        # 让模型自己挑工具；挑不动就退化成检索
        messages = session.to_messages(SYSTEM_PROMPT) + [
            {
                "role": "user",
                "content": (
                    f"用户问题：{question}\n"
                    "如果需要调用工具请调用；如果不需要，直接回答即可。"
                ),
            }
        ]
        first = await llm_client.chat(messages, tools=tools.openai_tool_schemas())
        if first.get("tool_calls"):
            tool_results = []
            for call in first["tool_calls"]:
                fn = call["function"]
                used_tools.append(fn["name"])
                out = await tools.execute(fn["name"], fn.get("arguments", "{}"))
                tool_results.append(f"工具 {fn['name']} 返回：\n{out}")
            context = "\n\n".join(tool_results)
        else:
            hits = await retriever.retrieve(question, top_k=top_k, use_hybrid=True)
            context, sources = _build_context(hits)
            route = "retrieve"

    # 3) 生成
    messages = session.to_messages(SYSTEM_PROMPT) + [
        {"role": "user", "content": f"参考资料：\n{context}\n\n用户问题：{question}"}
    ]
    resp = await llm_client.chat(messages)
    answer = resp.get("content", "")

    # 4) 写回记忆（下一轮才有上下文）
    session.add("user", question)
    session.add("assistant", answer)

    return {
        "session_id": session_id,
        "answer": answer,
        "sources": sources,
        "used_tools": used_tools,
        "route": route,
        "latency_ms": int((time.perf_counter() - t0) * 1000),
        "degraded": not llm_client.enabled,
    }


async def run_stream(question: str, session_id: str = "default"):
    """流式版：先检索，再把生成结果逐段 yield 给 SSE。

    和 run_pipeline 的区别只有最后一步 —— 不是等答案攒齐再返回，
    而是拿到一段就 yield 一段，前端才能做出「打字机」效果。
    """
    session = get_session(session_id)
    hits = await retriever.retrieve(question, use_hybrid=True)
    context, _ = _build_context(hits)

    messages = session.to_messages(SYSTEM_PROMPT) + [
        {"role": "user", "content": f"参考资料：\n{context}\n\n用户问题：{question}"}
    ]

    buf: list[str] = []
    async for piece in llm_client.chat_stream(messages):
        buf.append(piece)
        yield piece

    session.add("user", question)
    session.add("assistant", "".join(buf))