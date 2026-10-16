"""缓存 / 限流 / 会话外置的单元测试（第 13 步 ①②③）。

为什么用 fakeredis 而不是真 Redis：
    单元测试不该依赖外部服务 —— 别人 clone 下来就要能跑。
    `fakeredis.aioredis.FakeRedis` 实现的是**真的 Redis 协议语义**
    （ZSET 的 `zadd/zcard/zremrangebyscore`、`setex` 的 TTL、`scan_iter`…），
    所以测的是我们的逻辑，不是「有没有连上 Redis」。

怎么把它接进来：只替换 `app.cache` 里那个 `aioredis.from_url`。
    这样 `get_redis()` 及其下游代码**一行都不改**，走的是生产同一条路径。
"""

from __future__ import annotations

import asyncio

import fakeredis
import fakeredis.aioredis
import pytest

from app import cache


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    """每个用例一个干净的假 Redis，并让 app.cache 用它。"""
    server = fakeredis.FakeServer()

    def _from_url(url, **kwargs):
        return fakeredis.aioredis.FakeRedis(server=server, decode_responses=True)

    monkeypatch.setattr(cache.aioredis, "from_url", _from_url)
    monkeypatch.setattr(cache.settings, "use_redis", True)
    monkeypatch.setattr(cache, "_client", None)      # 清掉上一个用例的客户端
    cache.reset_breaker()                            # 清掉上一个用例留下的熔断状态
    yield server
    asyncio.run(cache.close_redis())


def test_rate_limit_allows_20_then_blocks():
    """滑动窗口：60 秒内前 20 次放行，第 21 次开始拒绝。"""

    async def run():
        results = [await cache.rate_limit("t1", limit=20, window=60) for _ in range(25)]
        return results

    results = asyncio.run(run())
    assert all(results[:20]), "前 20 次都应该放行"
    assert not any(results[20:]), "第 21 次起都应该被拦"


def test_rate_limit_counts_same_timestamp_requests(monkeypatch):
    """同一时间戳的多次请求必须各算一次。

    这是文档原版片段 `zadd(k, {str(now): now})` 的 bug：
    同一毫秒内 member 相同 ⇒ `zadd` 覆盖 ⇒ 计数偏少 ⇒ 限流被悄悄放宽。
    这里把 `_now` 压成固定值，等价于「一毫秒内来了 25 个请求」。

    ⚠️ 注意 patch 的是 `cache._now` 而不是全局 `time.time` ——
       改全局 time 会把 logging 一起改坏（logging 构造 LogRecord 时要 time.time()），
       本机实测会让整个 pytest 崩在无关的地方。
    """
    monkeypatch.setattr(cache, "_now", lambda: 1_700_000_000.0)

    async def run():
        return [await cache.rate_limit("t2", limit=20, window=60) for _ in range(25)]

    results = asyncio.run(run())
    assert all(results[:20])
    assert not any(results[20:]), "member 去重导致计数偏少 ⇒ 第 21 次会被误放行"


def test_embed_cache_hits_second_time():
    """第二次问同一句话，不应该再调 embedding 接口。"""
    calls = {"n": 0}

    async def fake_embed_one(text):
        calls["n"] += 1
        return [0.1, 0.2, 0.3]

    cache.embedder.embed_one = fake_embed_one

    async def run():
        v1 = await cache.embed_cached("文本切块有哪些策略？")
        v2 = await cache.embed_cached("文本切块有哪些策略？")
        v3 = await cache.embed_cached("完全不一样的问题")
        return v1, v2, v3

    v1, v2, v3 = asyncio.run(run())
    assert v1 == v2 == [0.1, 0.2, 0.3]
    assert calls["n"] == 2, "同一文本只应真正向量化一次（另一次是新文本）"
    assert v3 == [0.1, 0.2, 0.3]


def test_session_roundtrip_survives_memory_loss():
    """会话写进 Redis 后，即使本地内存清空也能恢复（模拟「重启服务」）。"""
    from app import memory

    async def run():
        s = await memory.aget_session("abc")
        s.add("user", "RRF 怎么融合？")
        s.add("assistant", "按名次倒数相加。")
        await memory.asave_session(s)

        memory._sessions.clear()                 # ← 模拟进程重启：内存全没了
        again = await memory.aget_session("abc")
        return again

    again = asyncio.run(run())
    assert len(again.turns) == 2
    assert again.turns[0].content == "RRF 怎么融合？"


def test_clear_session_removes_from_redis():
    from app import memory

    async def run():
        s = await memory.aget_session("toclear")
        s.add("user", "hi")
        await memory.asave_session(s)
        assert await cache.load_session("toclear") is not None
        ok = await memory.aclear_session("toclear")
        return ok, await cache.load_session("toclear")

    ok, after = asyncio.run(run())
    assert ok is True
    assert after is None, "只清内存不清 Redis，下次会被捞回来"


def test_fail_open_when_redis_unavailable(monkeypatch):
    """Redis 连不上时必须「当没有缓存」，不能抛异常。

    这是最容易被忽略的一条：如果限流里直接 `await r.zcard()`，
    Redis 一挂整个 `/chat` 就是 500 —— 加了缓存反而更脆。
    """
    class Boom:
        def pipeline(self, *a, **kw):
            raise ConnectionError("redis is down")

        async def ping(self):
            raise ConnectionError("redis is down")

    monkeypatch.setattr(cache, "_client", Boom())

    async def run():
        allowed = await cache.rate_limit("t3", limit=1, window=60)
        got = await cache.get_json("any:key")
        await cache.set_json("any:key", {"a": 1}, 60)
        return allowed, got

    allowed, got = asyncio.run(run())
    assert allowed is True, "Redis 挂了要放行（fail-open），而不是抛异常"
    assert got is None
    assert asyncio.run(cache.ping()) is False


def test_breaker_skips_redis_after_first_failure(monkeypatch):
    """熔断：第一次失败后，冷却期内**不再访问 Redis**（不再等超时）。

    为什么需要它：只 catch 异常的话，Redis 挂掉时每次操作都要白等一个超时，
    而一次 /chat 要碰 3 次 Redis。本机实测（连不上的 Redis）：
    加熔断前每次操作恒定 ~2013 ms，加之后第 2 次起 ~0 ms。
    """
    hits = {"n": 0}

    class Boom:
        def pipeline(self, *a, **kw):
            hits["n"] += 1
            raise ConnectionError("redis is down")

    monkeypatch.setattr(cache, "_client", Boom())
    cache.reset_breaker()

    async def run():
        r1 = await cache.rate_limit("b1", limit=1, window=60)
        after_first = hits["n"]
        r2 = await cache.rate_limit("b2", limit=1, window=60)
        r3 = await cache.get_json("any")
        return r1, r2, r3, after_first, hits["n"]

    r1, r2, r3, after_first, after_third = asyncio.run(run())
    assert (r1, r2) == (True, True)
    assert r3 is None
    assert after_first == 1
    assert after_third == 1, "熔断期内不该再碰 Redis（否则每次都要白等超时）"
