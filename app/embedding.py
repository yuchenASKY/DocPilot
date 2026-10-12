"""Embedding：把文本变成向量。

两种模式：
1. 真实模式：调用 OpenAI 兼容的 /embeddings 接口；
2. 离线模式：用「字符 n-gram 哈希」造一个确定性伪向量。

离线模式不是为了效果，而是为了让你在没有 Key、没有网络的时候
也能把「切块 → 向量化 → 检索 → 生成」整条链路跑通。
"""

from __future__ import annotations

import hashlib

import httpx
import numpy as np

from .config import settings


def _hash_embed(text: str, dim: int) -> list[float]:
    """确定性伪向量：同样的文本永远得到同样的向量。

    做法：把文本切成 3-gram，各自哈希到一个维度上累加，最后做 L2 归一化。
    好处是「字面越接近的文本，向量越接近」，足够演示检索效果。
    """
    vec = np.zeros(dim, dtype=np.float32)
    text = text.strip().lower()
    if not text:
        return vec.tolist()

    grams = [text[i : i + 3] for i in range(max(1, len(text) - 2))]
    for g in grams:
        h = int(hashlib.md5(g.encode()).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if (h >> 8) % 2 == 0 else -1.0
        vec[idx] += sign

    norm = float(np.linalg.norm(vec))
    if norm > 0:
        vec /= norm
    return vec.tolist()


class Embedder:
    def __init__(self) -> None:
        self.dim = settings.embed_dim
        self.mode = "api" if settings.embed_enabled else "offline-hash"
        self._client: httpx.AsyncClient | None = None
        if settings.embed_enabled:
            # 用 embedding 专用的地址 / Key（没配就自动回落到 LLM 的那套）
            base = settings.effective_embed_base_url
            # 防呆：DeepSeek 只有 chat、没有 /embeddings，不拦的话你会收到一个
            # 很难懂的 404。这里直接给出人话提示。
            if "deepseek" in base.lower():
                raise RuntimeError(
                    "EMBED_BASE_URL 指向了 DeepSeek，但 DeepSeek 没有 /embeddings 接口。\n"
                    "请换一家支持 embedding 的服务商（硅基流动 / 智谱 / 阿里百炼），"
                    "参考 .env.example 里 Embedding 那一段的说明。"
                )
            self._client = httpx.AsyncClient(
                base_url=base.rstrip("/"),
                timeout=httpx.Timeout(60.0, connect=15.0),
                headers={
                    "Authorization": f"Bearer {settings.effective_embed_api_key}",
                    "Content-Type": "application/json",
                },
            )

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """批量向量化。批量调用比逐条调用省一大半时间和钱。"""
        if not texts:
            return []
        if self._client is None:
            return [_hash_embed(t, self.dim) for t in texts]

        resp = await self._client.post(
            "/embeddings",
            json={"model": settings.embed_model, "input": texts},
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        data.sort(key=lambda d: d.get("index", 0))
        return [d["embedding"] for d in data]

    async def embed_one(self, text: str) -> list[float]:
        return (await self.embed([text]))[0]

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()


embedder = Embedder()