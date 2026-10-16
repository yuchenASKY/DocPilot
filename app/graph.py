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

import logging
import time
from typing import Any

from . import retriever, tools, tracing

# rewrite_query() 定义在 retriever.py 末尾（第 8 步 ③），这里必须显式导入 ——
# 因为它不是 retriever 的「属性式」用法（那样要写 retriever.rewrite_query），
# 漏了这行 run_pipeline 一跑就 NameError: name 'rewrite_query' is not defined。
from .retriever import rewrite_query
from .config import settings
from .llm import llm_client

# 本模块自己的 logger（第 11 步 ⑥ 要打印 token 消耗）。
# ★ 写日志前必须先有它 —— 每个模块一个，tools.py 里那个不能跨文件用。
logger = logging.getLogger(__name__)

# ① root 保持 WARNING —— 第三方库的 INFO 自动被挡在门外
logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
# ② 只把自己这个包放开到 INFO
logging.getLogger("app").setLevel(logging.INFO)

# 注意：memory 是**第 11 步才有的模块**，所以不要写在文件顶部 ——
# 否则第 7~10 步 `import app.graph` 会直接 ModuleNotFoundError，
# 连带 app.main / pytest / GET /health 全部起不来。
# 改成在真正用到它的两个函数里延迟导入（见 run_pipeline / run_stream 开头）。

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


_TOOL_HINTS = ("计算", "算一下", "多少钱", "多少秒", "时间", "今天", "现在", "最新", "搜索", "联网")


_DIRECT_HINTS = ("你好", "你是谁", "谢谢", "hi", "hello")


async def _route(question: str, use_tools: bool) -> str:
    """判断这次该走哪条分支

    这是整张图的「条件路由」节点，也是 LangGraph 最核心的能力。
    它存在的意义是省钱省延迟：不是所有问题都值得走一遍
    「embedding → 检索 → 融合 → 重排」，「你好」这种直接答就行。

    返回值必须是下面三个字符串之一（graph 的 add_conditional_edges 认这三个）：
      "direct"    → 简单问候/闲聊，直接生成，不检索
      "tool"      → 需要算数、查时间、联网等，走工具调用分支
      "retrieve"  → 需要查本地文档，走检索分支（默认兜底，最常用）

    规格：
      1. 返回值必须落在上面三个值里（返回别的会让图找不到边）；
      2. `use_tools=False` 时不能返回 "tool"（否则会走进没有工具的分支）；
      3. 拿不准的时候返回 "retrieve" —— 宁可多检索一次，也不要漏答。

    提示：
      - 最简实现：关键词命中。`_DIRECT_HINTS` / `_TOOL_HINTS` 就在上面，
        注意「你好」要配合长度判断，否则「你好，帮我查下切块策略」会被误判成 direct；
      - `q = question.lower()` 能让英文大小写不敏感；
      - 升级路线（面试可以讲）：用一个小模型做意图分类，
        或直接用第 9 步的 Function Calling 让模型自己选。
        但要注意那会多一次 LLM 调用 —— 这就是「路由规则该多聪明」的取舍。
    """
    q = question.lower()

    # 注意顺序：先判工具、再判闲聊。
    # 反过来的话「你好，帮我算一下 1+1」会被误判成 direct。
    if use_tools and any(h in q for h in _TOOL_HINTS):
        return "tool"
    if len(question) < 12 and any(h in q for h in _DIRECT_HINTS):
        return "direct"
    return "retrieve"          # 兜底：宁可多检索一次，也不要漏答


# @observe 让这次问答成为追踪面板上的**一条 trace**（根 span）。
# 没配 Langfuse 时它是「原样返回原函数」，零开销（见 app/tracing.py）。
@tracing.observe(name="chat")
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
    # memory 是第 11 步的模块，延迟到用它的地方再导入（原因见文件顶部注释）
    from .memory import get_session

    t0 = time.perf_counter()
    session = get_session(session_id)

    # ★ Session 里存历史用的字段是 turns，而且元素是 Turn 对象（dataclass）；
    #   而 rewrite_query(question, history) 要的是 [{"role":..., "content":...}] 这种
    #   dict（它内部用 m.get(...) 取值）。所以必须先转一次：
    #   - 写 session.messages → AttributeError（根本没这个字段）
    #   - 直接传 session.turns → AttributeError: 'Turn' object has no attribute 'get'
    history = [{"role": t.role, "content": t.content} for t in session.turns]
    q = await rewrite_query(question, history)

    # 1) 路由：这一步决定「要不要查资料 / 要不要调工具」
    route = await _route(question, use_tools)

    # 2) 检索 / 工具
    sources: list[dict] = []
    used_tools: list[str] = []
    context = "（本次未检索）"

    if route == "retrieve":
        hits = await retriever.retrieve(q, top_k=top_k, use_hybrid=True)
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

    usage = resp.get("usage", {})
    logger.info("prompt_tokens=%s", usage.get("prompt_tokens"))

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


@tracing.observe(name="chat_stream")
async def run_stream(question: str, session_id: str = "default"):
    """流式版：先检索，再把生成结果逐段 yield 给 SSE。

    和 run_pipeline 的区别只有最后一步 —— 不是等答案攒齐再返回，
    而是拿到一段就 yield 一段，前端才能做出「打字机」效果。
    """
    # memory 是第 11 步的模块，延迟到用它的地方再导入（原因见文件顶部注释）
    from .memory import get_session

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