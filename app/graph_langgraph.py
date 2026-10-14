from typing import TypedDict

from langgraph.graph import END, START, StateGraph

# 注意这个文件是「直接跑」的（uv run python app/graph_langgraph.py），
# 所以只能用**绝对导入** —— 直接执行包内文件时 __package__ 是空的，
# 写 `from . import retriever` 会报
# "ImportError: attempted relative import with no known parent package"。
from app import retriever
from app.graph import SYSTEM_PROMPT, _build_context, _route
# _route() 放在 graph.py 里（纯 Python 版的 run_pipeline 也要用它），
# 这里导入复用，避免两份实现各自漂移。
from app.llm import llm_client
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict, total=False):
    question: str
    route: str
    context: str
    sources: list
    answer: str
    retry_count: int


async def node_route(state):
    state["route"] = await _route(state["question"], True)
    return state


async def node_retrieve(state):
    hits = await retriever.retrieve(state["question"], use_hybrid=True)
    context, sources = _build_context(hits)
    state["context"] = context
    state["sources"] = sources
    return state


async def node_generate(state):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"参考资料：\n{state.get('context', '')}\n\n问题：{state['question']}"}]
    resp = await llm_client.chat(messages)
    state["answer"] = resp.get("content", "")
    return state


graph = StateGraph(State)
graph.add_node("route", node_route)
graph.add_node("retrieve", node_retrieve)
graph.add_node("generate", node_generate)

graph.add_edge(START, "route")
graph.add_conditional_edges(
    "route",
    lambda s: "retrieve" if s["route"] == "retrieve" else "generate",
    {"retrieve": "retrieve", "generate": "generate"},
)
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile(checkpointer=MemorySaver())

print(app.get_graph().draw_mermaid())