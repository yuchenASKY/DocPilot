"""FastAPI 入口：把能力暴露成 HTTP 接口。

四个核心接口（第 4 步的验收标准就是这四个都能通）：
  GET  /health         健康检查——部署后用来判断服务活没活
  POST /chat           一问一答
  POST /chat/stream    SSE 流式输出（打字机效果）
  POST /upload         上传文档 → 自动解析切块入库

另外附赠：
  POST /session/{id}/clear  清空某个会话的记忆
  GET  /stats               看当前索引了多少片段、活跃会话数
"""

from __future__ import annotations

import json
import shutil
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from . import cache, graph, ingest, memory, tools, tracing
from .cache import rate_limit
from .config import settings
from .embedding import embedder
from .llm import llm_client
from .schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    SourceChunk,
    UploadResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时什么都不用做（向量库在导入时自动载入），
    关闭时统一释放 HTTP 连接池。"""
    yield
    await llm_client.aclose()
    await embedder.aclose()
    await cache.close_redis()          # 第 13 步 ①：断开 Redis 连接
    # ★ 追踪的 span 是「批量上报」的，进程退出前必须 flush，否则缓冲区里的会丢
    tracing.flush()
    tracing.shutdown()


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
    # 第 13 步 ②：按 session 限流，60 秒内最多 20 次。
    # ★ 位置必须在这里 —— 在 run_pipeline() **之前**。
    #   限流的意义是拦住超额请求；如果先做完了检索和生成再检查，
    #   钱已经花掉了（embeddings + LLM 都算过了）。
    if not await rate_limit(f"chat:{req.session_id}", limit=20, window=60):
        raise HTTPException(
            status_code=429,
            detail="请求过于频繁，请稍后再试",
            headers={"Retry-After": "60"},
        )

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
        # 流式这条也限流：不拦的话「打字机效果」正好绕过了限流（一样要钱）
        if not await rate_limit(f"chat:{req.session_id}", limit=20, window=60):
            err = json.dumps({"error": "请求过于频繁，请稍后再试"}, ensure_ascii=False)
            yield f"event: error\ndata: {err}\n\n"
            yield "event: done\ndata: [DONE]\n\n"
            return
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


@app.post("/upload", response_model=UploadResponse, tags=["文档"])
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名为空")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".md", ".markdown", ".txt"}:
        raise HTTPException(status_code=400, detail=f"不支持的类型：{suffix}")

    dest = settings.upload_dir / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        chunks = ingest.build_chunks(dest)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"解析失败：{exc}") from exc

    if not chunks:
        return UploadResponse(
            filename=file.filename, saved_to=str(dest), chunks=0, indexed=False
        )

    vectors = await embedder.embed([c.text for c in chunks])

    from . import vectorstore

    vectorstore.store.add(chunks, vectors)
    vectorstore.store.save()
    # ★ 第 13 步纪律：索引一变，检索结果缓存立刻作废。
    #   不清的话，用户会拿到「新文档入索引之前」的答案，而且完全不报错 —— 最难查的那类 bug。
    await cache.clear_retrieval_cache()

    return UploadResponse(
        filename=file.filename, saved_to=str(dest), chunks=len(chunks), indexed=True
    )


@app.post("/session/{session_id}/clear", tags=["对话"])
async def clear_session(session_id: str) -> dict:
    # 第 13 步 ③：内存和 Redis 都要清，否则下次会被 Redis 捞回来
    ok = await memory.aclear_session(session_id)
    return {"cleared": ok, "session_id": session_id}


@app.get("/stats", tags=["系统"])
async def stats() -> dict:
    from . import vectorstore

    return {
        "indexed_chunks": len(vectorstore.store),
        "tools": list(tools.TOOLS),
        "memory": memory.stats(),
        "llm_enabled": llm_client.enabled,
        "embed_mode": embedder.mode,
        "tracing": tracing.enabled(),
        # 第 13 步 ①：use_redis 是「配置里写着开」，connected 才是「真的通」
        # —— 两者不一致就是「缓存和限流静默失效」的状态，必须能一眼看出来
        "cache": {
            "use_redis": settings.use_redis,
            "connected": await cache.ping(),
        },
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
