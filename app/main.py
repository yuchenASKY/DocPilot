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

from . import graph, ingest, memory, tools, tracing
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

    return UploadResponse(
        filename=file.filename, saved_to=str(dest), chunks=len(chunks), indexed=True
    )


@app.post("/session/{session_id}/clear", tags=["对话"])
async def clear_session(session_id: str) -> dict:
    ok = memory.clear_session(session_id)
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
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
