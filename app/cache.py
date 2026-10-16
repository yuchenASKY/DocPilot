"""Redis 封装：缓存 + 限流 + 会话持久化（第 13 步 ①）。

三个用途：

| 用途 | 函数 | 缓存什么 | TTL |
|---|---|---|---|
| embedding 缓存 | `embed_cached()` | 文本 → 向量 | 7 天 |
| 检索结果缓存 | `get_json()` / `set_json()`（`retriever` 调用） | query → 结果列表 | 1 小时 |
| 滑动窗口限流 | `rate_limit()` | 时间戳有序集合 | 窗口秒数 |

★ 贯穿全文件的一条设计：**失败要开放（fail-open）**。
  缓存是「加速手段」，不是「功能依赖」—— Redis 连不上时应该退化成「没有缓存」，
  而不是让用户连问题都问不了。所以每个 Redis 操作都自己 catch 住异常并降级，
  绝不把 Redis 的故障变成 500。
  （反例：`rate_limit()` 里直接 `await r.zcard()`，Redis 一挂就是
   `ConnectionError` → 整个 `/chat` 500 —— 这是「加了缓存反而更脆」的典型。）

★ 第二条纪律：**TTL 要加随机抖动**，见 `_ttl_with_jitter()`。
"""

from __future__ import annotations

import hashlib
import json
import logging
import random
import time
import uuid
from typing import Any

import redis.asyncio as aioredis

from .config import settings
from .embedding import embedder

logger = logging.getLogger(__name__)

# 各类 key 的 TTL（秒）。取值依据见第 13 步知识点 2。
EMBED_TTL = 7 * 86400      # embedding：同一段文本的向量几乎不变
RETRIEVAL_TTL = 3600       # 检索结果：文档更新后要能及时反映，别超过 1 小时
SESSION_TTL = 3600         # 会话状态：用户离开后没必要长期占内存

_client: aioredis.Redis | None = None

# --- 熔断（fail-open 的第二层）---
# 光「catch 住异常」还不够：Redis 挂掉时**每次**操作都要白等 2 秒超时，
# 而一次 /chat 会碰 3 次 Redis（限流 + 读会话 + 写会话）⇒ 凭空多 6 秒，
# 而且它对每一轮请求都重试，永远不会自己判断「该歇一会儿了」。
# 所以：一旦失败，就把它标记为「冷却期内不再访问」，请求直接走降级路径。
# 本机实测：加熔断前每次操作 ~2013 ms（恒定），加之后第 2 次起 ~0 ms。
_COOLDOWN = 10.0
_down_until = 0.0


def _breaker_open() -> bool:
    return _now() < _down_until


def _trip(reason: object) -> None:
    """标记 Redis 不可用，冷却 `_COOLDOWN` 秒。"""
    global _down_until
    _down_until = _now() + _COOLDOWN
    logger.warning(
        "Redis 不可用，熔断 %.0f 秒（期间缓存/限流全部直接降级，不再等待超时）：%s",
        _COOLDOWN,
        reason,
    )


def reset_breaker() -> None:
    """恢复访问（测试用，也可以在运维脚本里手动调）。"""
    global _down_until
    _down_until = 0.0


async def get_redis() -> aioredis.Redis | None:
    """取 Redis 客户端；没启用、熔断中、连不上都返回 None（调用方按「没有缓存」处理）。"""
    global _client
    if not settings.use_redis or _breaker_open():
        return None
    if _client is None:
        _client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
            # 连不上/超时就快点失败，别把请求挂死 —— fail-open 的前提是「失败要快」
            socket_connect_timeout=1,
            socket_timeout=1,
            health_check_interval=30,
        )
    return _client


async def close_redis() -> None:
    """服务停止时调用，避免留下连不上的连接。"""
    global _client
    if _client is not None:
        try:
            await _client.aclose()
        except Exception:  # noqa: BLE001
            pass
        _client = None


async def ping() -> bool:
    """Redis 到底通没通 —— 给 `/stats` 用。

    为什么不直接看 `settings.use_redis`：配置里写着 true、Redis 却没起来，
    是第 13 步最容易踩的状态（缓存和限流会「静默地完全不生效」）。
    """
    r = await get_redis()
    if r is None:
        return False
    try:
        await r.ping()
        return True
    except Exception as exc:  # noqa: BLE001
        _trip(exc)
        return False


# ---------------- key 设计 ----------------


def _key(prefix: str, text: str) -> str:
    """`前缀:内容摘要`。

    用 md5 当 key 而不是原文：① key 短、好比对；② 查询内容不会明文落在 Redis 里。
    （md5 在这里只当「摘要」用，不是当安全哈希 —— 这场景不需要抗碰撞。）
    """
    return f"{prefix}:{hashlib.md5(text.encode('utf-8')).hexdigest()}"


def _now() -> float:
    """当前时间戳。

    单独抽成一个函数是为了**可测**：单元测试要模拟「同一毫秒内来 25 个请求」，
    直接 monkeypatch 这个函数就行。如果测试去改全局 `time.time`，
    会把 logging 等所有依赖时间的库一起改坏（本机实测：整个 pytest 会崩）。
    """
    return time.time()


def _ttl_with_jitter(ttl: int, ratio: float = 0.1) -> int:
    """TTL 加 ±ratio 的随机抖动。

    为什么必须加：一批 key 如果是同一秒写入、又用同一个 TTL，
    就会**在同一秒集体过期**，那一刻的请求全部同时回源 —— 这就是「缓存雪崩」。
    抖动让过期时间散开，把回源压力摊平（第 13 步知识点 3）。
    """
    delta = int(ttl * ratio)
    if delta <= 0:
        return ttl
    return ttl + random.randint(-delta, delta)


# ---------------- 通用 JSON 缓存 ----------------


async def get_json(key: str) -> Any | None:
    """读缓存；任何异常都当成「没命中」。"""
    r = await get_redis()
    if r is None:
        return None
    try:
        raw = await r.get(key)
    except Exception as exc:  # noqa: BLE001
        _trip(exc)
        return None
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        await delete(key)          # 脏数据（比如上一版格式变了）直接清掉
        return None


async def set_json(key: str, value: Any, ttl: int) -> None:
    """写缓存；写失败只打日志，不影响业务流程。

    用 `SET key val EX seconds` 而不是 `SETEX` —— 后者在 Redis 8 里**已被标记弃用**
    （本机实测：fakeredis 2.40 会对每次调用打一行 DeprecationWarning）。
    """
    r = await get_redis()
    if r is None:
        return
    try:
        await r.set(key, json.dumps(value, ensure_ascii=False), ex=_ttl_with_jitter(ttl))
    except Exception as exc:  # noqa: BLE001
        _trip(exc)


async def delete(*keys: str) -> int:
    r = await get_redis()
    if r is None or not keys:
        return 0
    try:
        return await r.delete(*keys)
    except Exception as exc:  # noqa: BLE001
        _trip(exc)
        return 0


async def clear_prefix(prefix: str, batch: int = 500) -> int:
    """按前缀清空（用 SCAN 而不是 KEYS —— KEYS 会阻塞整个 Redis）。

    用途：**索引重建 / 上传新文档后，必须清掉检索结果缓存**，
    否则用户会拿到基于旧文档的答案，而且这个 bug 极其隐蔽（第 13 步知识点 2 的纪律）。
    """
    r = await get_redis()
    if r is None:
        return 0
    removed = 0
    try:
        async for k in r.scan_iter(match=f"{prefix}*", count=batch):
            removed += await r.delete(k)
    except Exception as exc:  # noqa: BLE001
        _trip(exc)
    if removed:
        logger.info("已清理缓存前缀 %s*：%d 个 key", prefix, removed)
    return removed


async def clear_retrieval_cache() -> int:
    """给「索引变了」的场合调用（`build_index --rebuild`、`/upload`）。"""
    return await clear_prefix("retr:")


# ---------------- embedding 缓存 ----------------


async def embed_cached(text: str) -> list[float]:
    """同一个文本 7 天内只向量化一次。

    为什么值得缓：embedding 走的是**按量计费**的接口（第 6 步），
    而索引重建、评测反复跑、用户重复提问都会重复向量化同一段文本。
    """
    key = _key("emb", text)
    cached = await get_json(key)
    if cached is not None:
        return cached
    vec = await embedder.embed_one(text)
    await set_json(key, vec, EMBED_TTL)
    return vec


# ---------------- 滑动窗口限流 ----------------


async def rate_limit(key: str, limit: int = 20, window: int = 60) -> bool:
    """滑动窗口限流，返回 True 表示允许通过。

    实现（ZSET 当滑动窗口）：拿**时间戳当分数**把每次请求记进有序集合，
    先删掉窗口外的，再数窗口内的 —— 比「固定窗口」精确：
    固定窗口会有「窗口边界处放行 2 倍流量」的问题（59 秒来 20 次、61 秒再来 20 次）。

    ⚠️ **member 必须唯一**，所以用 `时间戳:随机数`。
       如果写成 `zadd(k, {str(now): now})`（很多教程的写法），
       同一毫秒内的多次请求会**覆盖同一个 member**，计数变少 ⇒ 限流被悄悄放宽。
       本机实测：连发 25 次请求时 time.time() 会出现重复值，第 21 次拦不住。
    """
    r = await get_redis()
    if r is None:
        return True                     # 没启 Redis 就不限流（本地开发）
    now = _now()
    k = f"rl:{key}"
    try:
        pipe = r.pipeline()
        pipe.zremrangebyscore(k, 0, now - window)          # 清掉窗口外的
        pipe.zcard(k)                                      # 数窗口内的（不含本次）
        pipe.zadd(k, {f"{now}:{uuid.uuid4().hex[:8]}": now})
        pipe.expire(k, window)
        _, count, *_ = await pipe.execute()
    except Exception as exc:  # noqa: BLE001
        _trip(exc)
        return True                                        # 宁可漏拦，不可全拦
    return count < limit


async def rate_limit_count(key: str, window: int = 60) -> int:
    """窗口内已发生的请求数 —— 只用于观测/调试。"""
    r = await get_redis()
    if r is None:
        return 0
    try:
        return int(await r.zcount(f"rl:{key}", _now() - window, "+inf"))
    except Exception:  # noqa: BLE001
        return 0


# ---------------- 会话持久化 ----------------
# 注意：这里刻意**只存 dict、不 import memory.Session** ——
# memory.py 要 import cache，cache 反过来 import memory 就成环了。
# 序列化/反序列化放在 memory.py 里做（那是它自己的数据结构）。


async def save_session(session_id: str, payload: dict) -> None:
    """会话状态落 Redis（带 TTL）。重启服务、多进程部署都不会丢。"""
    await set_json(f"session:{session_id}", payload, SESSION_TTL)


async def load_session(session_id: str) -> dict | None:
    return await get_json(f"session:{session_id}")


async def delete_session(session_id: str) -> int:
    return await delete(f"session:{session_id}") + await delete(f"rl:chat:{session_id}")
