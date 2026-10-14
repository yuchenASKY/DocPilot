"""Embedding：把文本变成向量。

两种模式：
1. 真实模式：调用 OpenAI 兼容的 /embeddings 接口；
2. 离线模式：用「字符 n-gram 哈希」造一个确定性伪向量。

离线模式不是为了效果，而是为了让你在没有 Key、没有网络的时候
也能把「切块 → 向量化 → 检索 → 生成」整条链路跑通。
"""

from __future__ import annotations

import asyncio
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
        # ★ 客户端**不在这里创建**，见 _get_client() 的说明。
        #   一句话：httpx.AsyncClient 的连接池会绑定到「创建它时正在运行的那个
        #   事件循环」上；模块导入时根本没有循环，在这里建好就会被第一个用到它的
        #   `asyncio.run()` 绑死，等那次 run 结束（循环关闭）后，第二次 run 复用
        #   到旧连接就会 `RuntimeError: Event loop is closed`。
        self._client: httpx.AsyncClient | None = None
        self._client_loop: asyncio.AbstractEventLoop | None = None
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

    def _get_client(self) -> httpx.AsyncClient | None:
        """取「当前事件循环」下的 HTTP 客户端；循环换了就重建。

        为什么要按循环记账，而不是只建一次：
          httpx.AsyncClient 底层的连接池、TLS 流、锁都绑在**创建它的那个循环**上。
          而 `asyncio.run()` 每次都新建一个循环、跑完立刻关掉。于是：

            for q in questions:
                asyncio.run(retrieve(q))      # 脚本里最自然的写法

          第一轮：在循环 A 上建连接池，请求成功，循环 A 关闭；
          第二轮：复用池里那条属于循环 A 的陈旧连接，关闭它时要把回调投递回
                  循环 A —— 循环 A 已经关了 → `RuntimeError: Event loop is closed`。
          现象就是「第一条查询正常，第二条才炸」，很容易误以为是 API 或代码错。

          pytest 默认每个用例一个循环、FastAPI TestClient 每次请求一个循环，
          都是同一个坑。所以这里记住「客户端属于哪个循环」，换循环就丢弃重建。
        """
        if not settings.embed_enabled:
            return None
        loop = asyncio.get_running_loop()
        if self._client is None or self._client_loop is not loop:
            self._client = httpx.AsyncClient(
                base_url=settings.effective_embed_base_url.rstrip("/"),
                timeout=httpx.Timeout(60.0, connect=15.0),
                headers={
                    "Authorization": f"Bearer {settings.effective_embed_api_key}",
                    "Content-Type": "application/json",
                },
            )
            self._client_loop = loop
        return self._client

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """批量向量化。

        分两件事：
        1. **必须分批** —— 不少服务商对「单次请求的文本条数」有硬上限
           （阿里百炼 20 条、多数服务商 10 条），一次把几百个片段全发过去
           会直接被拒：`batch size is invalid, it should not be larger than 20`。
           批量大小用 .env 的 EMBED_BATCH_SIZE 控制，默认 10。
        2. **批量本身就省时省钱** —— 同样 100 条文本，分 10 批发比发 100 次快得多。
        """
        if not texts:
            return []
        client = self._get_client()
        if client is None:
            return [_hash_embed(t, self.dim) for t in texts]

        step = max(1, settings.embed_batch_size)
        out: list[list[float]] = []
        for i in range(0, len(texts), step):
            batch = texts[i : i + step]
            resp = await client.post(
                "/embeddings",
                json={"model": settings.embed_model, "input": batch},
            )
            # 不用 raise_for_status()：它只抛一句 "400 Bad Request"，
            # 而真正的原因（批次超限 / 模型名错 / 余额不足）写在响应体里。
            if resp.status_code != 200:
                raise RuntimeError(
                    "embedding 请求失败 HTTP %d（第 %d~%d 条，共 %d 条）：\n%s"
                    % (resp.status_code, i + 1, i + len(batch), len(texts),
                       resp.text[:500])
                )
            data = resp.json()["data"]
            data.sort(key=lambda d: d.get("index", 0))
            out.extend(d["embedding"] for d in data)
        return out

    async def embed_one(self, text: str) -> list[float]:
        return (await self.embed([text]))[0]

    async def aclose(self) -> None:
        """只关「当前循环」下的连接池。

        换过循环的旧客户端挂在已经关闭的循环上，对它调 aclose() 自己就会抛
        RuntimeError（正是它要修的毛病），所以只能放下引用让 GC 回收。
        """
        client, loop = self._client, self._client_loop
        self._client = None
        self._client_loop = None
        if client is not None and loop is asyncio.get_running_loop():
            await client.aclose()


embedder = Embedder()