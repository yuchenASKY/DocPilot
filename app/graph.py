"""Agent 编排层：一张「图」决定每次问话怎么走。
这里提供了两份实现：
- `run_pipeline()`：纯 Python 版，零依赖、逻辑清晰，方便你理解每一步；
- `build_langgraph()`：LangGraph 版（装了 langgraph 才可用），
  把同样的流程表达成 StateGraph，好处是状态可视化、可持久化、可中断续跑。
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