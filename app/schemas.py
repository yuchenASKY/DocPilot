"""请求 / 响应数据模型（pydantic v2）。

为什么要有这一层：
1. 自动校验客户端传来的参数，类型不对直接 422，不用手写 if 判断；
2. FastAPI 靠它自动生成 /docs 里的接口文档；
3. 响应模型固定字段后，前端对接不会因为字段名改动而炸。
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(default="user", description="user / assistant / system")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="用户问题")
    session_id: str = Field(default="default", description="会话 ID，用于区分多轮上下文")
    top_k: int = Field(default=5, ge=1, le=20, description="检索返回的片段数")
    use_tools: bool = Field(default=True, description="是否允许 Agent 调用工具")


class SourceChunk(BaseModel):
    source: str = Field(..., description="来源文件名")
    page: int | None = Field(default=None, description="页码，Markdown 无页码时为 null")
    score: float = Field(default=0.0, description="相关性分数")
    text: str = Field(default="", description="命中片段原文（截断展示）")


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[SourceChunk] = Field(default_factory=list)
    used_tools: list[str] = Field(default_factory=list)
    route: str = Field(default="retrieve", description="本次走的分支：direct / retrieve / tool")
    latency_ms: int = 0
    degraded: bool = Field(default=False, description="是否处于离线降级模式")


class UploadResponse(BaseModel):
    filename: str
    saved_to: str
    chunks: int
    indexed: bool


class HealthResponse(BaseModel):
    status: str
    llm_enabled: bool
    embed_mode: str
    indexed_chunks: int
    version: str = "0.1.0"


class EvalItem(BaseModel):
    question: str
    ground_truth: str = ""
    expected_source: str = ""


class EvalReport(BaseModel):
    total: int
    hit_rate: float
    avg_latency_ms: float
    details: list[dict[str, Any]] = Field(default_factory=list)