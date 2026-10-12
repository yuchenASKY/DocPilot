"""FastAPI 入口（第 4 步的最小可运行版：只做 /health）。

后面几步会陆续往这个文件里补接口：
  第 7 步 → /chat 与 /chat/stream
  第 11 步 → /session/{id}/clear
  第 12 步 → /stats、/upload
本步 ② 末尾那份 170 行的是**最终形态**，等接口都齐了再整体替换成它。
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .llm import llm_client
from .schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时不用做事；关闭时释放 HTTP 连接池。"""
    yield
    await llm_client.aclose()


app = FastAPI(
    title="DocPilot API",
    description="基于 RAG 的技术文档智能问答 Agent",
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
    return HealthResponse(
        status="ok",
        llm_enabled=llm_client.enabled,
        embed_mode="not-ready",   # 第 6 步接上 embedding 后改成 embedder.mode
        indexed_chunks=0,         # 第 6 步建好索引后改成真实数量
        version="0.1.0",
    )