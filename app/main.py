"""FastAPI 入口：把能力暴露成 HTTP 接口。

第 7 步完成后的样子 —— 项目第一次能端到端问答：
  GET  /health         健康检查（从这一步起返回真实数据，不再是写死的值）
  POST /chat           一问一答
  POST /chat/stream    SSE 流式输出（打字机效果）

后面还会继续补：
  第 11 步 → /session/{id}/clear
  第 12 步 → /stats、/upload
"""

from __future__ import annotations

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from . import graph
from .embedding import embedder
from .llm import llm_client
from .schemas import ChatRequest, ChatResponse, HealthResponse, SourceChunk


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时什么都不用做（向量库在导入时自动载入），
    关闭时统一释放 HTTP 连接池。"""
    yield
    await llm_client.aclose()
    await embedder.aclose()


app = FastAPI(
    title="DocPilot API",
    description="基于 RAG + LangGraph 的技术文档智能问答 Agent",
    version="0.1.0",
    lifespan=lifespan,
)

# 开发阶段放开跨域，方便本地前端联调；上线时收窄成具体域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["系统"])
async def health() -> HealthResponse:
    """健康检查：部署后用来判断服务活没活。"""
    from . import vectorstore

    return HealthResponse(
        status="ok",
        llm_enabled=llm_client.enabled,
        embed_mode=embedder.mode,
        indexed_chunks=len(vectorstore.store),
        version="0.1.0",
    )


@app.post("/chat", response_model=ChatResponse, tags=["对话"])
async def chat(req: ChatRequest) -> ChatResponse:
    result = await graph.run_pipeline(
        req.question,
        session_id=req.session_id,
        top_k=req.top_k,
        use_tools=req.use_tools,
    )
    return ChatResponse(
        session_id=result["session_id"],
        answer=result["answer"],
        sources=[SourceChunk(**s) for s in result["sources"]],
        used_tools=result["used_tools"],
        route=result["route"],
        latency_ms=result["latency_ms"],
        degraded=result["degraded"],
    )


@app.post("/chat/stream", tags=["对话"])
async def chat_stream(req: ChatRequest):
    """SSE 流式：前端用 EventSource 接，能做出逐字输出的效果。"""

    async def event_gen():
        yield f"event: meta\ndata: {json.dumps({'session_id': req.session_id}, ensure_ascii=False)}\n\n"
        try:
            async for piece in graph.run_stream(req.question, req.session_id):
                payload = json.dumps({"delta": piece}, ensure_ascii=False)
                yield f"event: delta\ndata: {payload}\n\n"
        except Exception as exc:  # noqa: BLE001
            err = json.dumps({"error": str(exc)}, ensure_ascii=False)
            yield f"event: error\ndata: {err}\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )