"""LLM 客户端：用 httpx 直接打 OpenAI 兼容协议。

为什么不用官方 openai SDK：
DeepSeek、通义千问、智谱、Kimi 都提供「OpenAI 兼容接口」，
一个 httpx 客户端就能全接上，换服务商只改 .env 的 BASE_URL，代码一行不动。
（面试被问「你怎么做多模型兼容」时，这就是答案。）

同时提供两个方法：
- chat()        一次性返回完整回答
- chat_stream() 逐段 yield，用于 SSE 流式输出（IM 那种「打字机效果」）
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from .config import settings

# 离线降级回答：没有 API Key 时用它，保证工程链路能跑通
_OFFLINE_REPLY = (
    "【离线模式】当前没有配置真实的 LLM API Key，这里返回的是占位回答。\n"
    "检索到的片段已在 sources 字段中返回，说明 RAG 链路本身是通的。\n"
    "在 .env 里填好 OPENAI_API_KEY 后重启服务，就会换成真实模型的回答。"
)


class LLMClient:
    def __init__(self) -> None:
        self.enabled = settings.llm_enabled
        # 注意：HTTP 头只能是 ASCII。没配 Key 时不要把它塞进头里，
        # 否则占位符里一旦有中文就会在构造客户端时抛 UnicodeEncodeError。
        key = settings.openai_api_key.strip() if self.enabled else "not-configured"
        self._client = httpx.AsyncClient(
            base_url=settings.openai_base_url.rstrip("/"),
            timeout=httpx.Timeout(60.0, connect=15.0),
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )

    # ---------- 非流式 ----------
    async def chat(
        self,
        messages: list[dict],
        *,
        temperature: float | None = None,
        tools: list[dict] | None = None,
    ) -> dict:
        """返回完整响应体（含可能的 tool_calls）。"""
        if not self.enabled:
            return {"content": _OFFLINE_REPLY, "tool_calls": []}

        payload: dict = {
            "model": settings.llm_model,
            "messages": messages,
            "temperature": (
                settings.llm_temperature if temperature is None else temperature
            ),
            "max_tokens": settings.llm_max_tokens,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        msg = data["choices"][0]["message"]
        return {
            "content": msg.get("content") or "",
            "tool_calls": msg.get("tool_calls") or [],
            "usage": data.get("usage", {}),
        }

    # ---------- 流式 ----------
    async def chat_stream(self, messages: list[dict]) -> AsyncIterator[str]:
        """逐段产出增量文本，配合 FastAPI 的 StreamingResponse 做 SSE。"""
        if not self.enabled:
            for piece in _OFFLINE_REPLY:
                yield piece
            return

        payload = {
            "model": settings.llm_model,
            "messages": messages,
            "temperature": settings.llm_temperature,
            "max_tokens": settings.llm_max_tokens,
            "stream": True,
        }
        async with self._client.stream(
            "POST", "/chat/completions", json=payload
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line or not line.startswith("data:"):
                    continue
                chunk = line[5:].strip()
                if chunk == "[DONE]":
                    break
                try:
                    delta = json.loads(chunk)["choices"][0]["delta"]
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
                piece = delta.get("content")
                if piece:
                    yield piece

    async def aclose(self) -> None:
        await self._client.aclose()


# 模块级单例：全项目共用一个 LLMClient（也就共用一个连接池）。
# 其它模块一律 `from .llm import llm_client` 后直接用，不要自己 new。
llm_client = LLMClient()
