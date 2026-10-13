async def run_pipeline(
    question: str,
    session_id: str = "default",
    *,
    top_k: int | None = None,
    use_tools: bool = True,
) -> dict[str, any]:
    """纯 Python 版编排：路由 → 检索/工具 → 生成。"""
    t0 = time.perf_counter()
    session = get_session(session_id)
    route = await _route(question, use_tools)

    sources: list[dict] = []
    used_tools: list[str] = []
    context = "（本次未检索）"

    if route == "retrieve":
        hits = await retriever.retrieve(question, top_k=top_k, use_hybrid=True)
        context, sources = _build_context(hits)

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
        first = await llm_client.chat(
            messages, tools=tools.openai_tool_schemas()
        )
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

    messages = session.to_messages(SYSTEM_PROMPT) + [
        {
            "role": "user",
            "content": f"参考资料：\n{context}\n\n用户问题：{question}",
        }
    ]
    resp = await llm_client.chat(messages)
    answer = resp.get("content", "")

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
    """流式版：先检索，再把生成结果逐段 yield 给 SSE。"""
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