"""Langfuse 追踪接入（可选，第 12 步 ⑥）。

★ 先说一个**必须纠正的常见误解**：
   网上都说「配好环境变量，Langfuse 就会自动上报」—— 这话对一半。
   Langfuse 能自动跟踪 **OpenAI SDK / LangChain / LlamaIndex**，是因为它在
   那些库里挂了回调（patch 的是 SDK 的客户端对象）。而本项目第 3 步就做了一个
   设计选择：**用裸 httpx 直接打 OpenAI 兼容协议**（换来「换服务商只改 .env」）。
   框架无从插手 ⇒ **光配环境变量一个 span 都不会有，必须自己打点**。

这里做三件事：
  1. 没配 LANGFUSE_* 时，`@observe()` **原样返回原函数**（连包装层都不加，零开销）；
  2. 配了时，把 run_pipeline → retrieve / chat / execute 串成一棵调用链；
  3. 顺手把每次 LLM 的 token 用量挂到 generation 上（面板上能直接看花了多少）。

依赖形态：**可选**。没装 langfuse 只是打一行 warning，项目照常跑。
"""

from __future__ import annotations

import logging
import os
from typing import Any, Callable

from .config import settings

logger = logging.getLogger(__name__)

# langfuse 的入口函数；没配 Key 或没装包时保持 None —— 全模块靠它判断「要不要干活」
_OBSERVE: Callable | None = None
_CLIENT_FACTORY: Callable | None = None


def _push_env() -> None:
    """把 `.env` 里读到的 Langfuse 配置**写回进程环境变量**。

    ★ 这一步必须做，而且极容易漏 —— 漏了就是「配了等于没配」：
      `pydantic-settings` 只是把 `.env` **读进 Settings 对象**，
      它**不会**把值导出到 `os.environ`。而 langfuse 的 SDK 是从
      **进程环境变量**取凭据的（`LANGFUSE_PUBLIC_KEY` 等）。
      于是现象是：`settings.langfuse_enabled` 是 `True`（配置确实读到了）、
      每个 `@observe` 装饰器也包上了，但 SDK 客户端因为「没有 public_key」
      被**静默禁用** —— 面板上一条 trace 都没有，只在初始化时打一行 warning。

      本机实测（2026-10-16）：修之前 `get_client().auth_check()` → `False`
      + 「Authentication error: ... Client will be disabled」；修之后 → `True`。

    用 `setdefault` 而不是直接赋值：真实环境变量（CI / docker -e）优先级更高，
    应该盖过 `.env`。
    """
    os.environ.setdefault("LANGFUSE_PUBLIC_KEY", settings.langfuse_public_key)
    os.environ.setdefault("LANGFUSE_SECRET_KEY", settings.langfuse_secret_key)
    # 两个名字都写：不同版本的 SDK / 不同机房拿到的是不同的那个
    os.environ.setdefault("LANGFUSE_HOST", settings.langfuse_host)
    os.environ.setdefault("LANGFUSE_BASE_URL", settings.langfuse_host)


def _load() -> None:
    """真的要用的时候才 import langfuse（它自己会拉一堆 OTel 依赖，不便宜）。"""
    global _OBSERVE, _CLIENT_FACTORY
    try:
        from langfuse import get_client, observe
    except ImportError as exc:
        logger.warning(
            "已配置 LANGFUSE_*，但没装 langfuse 包，追踪已跳过（%s）。"
            "装它：uv pip install langfuse",
            exc,
        )
        return
    _OBSERVE, _CLIENT_FACTORY = observe, get_client


if settings.langfuse_enabled:
    _push_env()
    _load()


def enabled() -> bool:
    """当前是否真的在追踪（供 /stats 之类的接口展示）。"""
    return _OBSERVE is not None


def observe(name: str | None = None, **kwargs: Any) -> Callable:
    """`langfuse.observe()` 的降级版。

    没接追踪时**原样返回原函数**（而不是套一层空壳跑一遍）—— 这样关闭追踪时
    性能完全等于没有这个功能，而且 `functools.wraps` 之类的元信息也不会丢。
    """

    def decorator(fn: Callable) -> Callable:
        if _OBSERVE is None:
            return fn
        try:
            return _OBSERVE(name=name or fn.__name__, **kwargs)(fn)
        except Exception as exc:  # noqa: BLE001 —— 追踪绝不能让业务挂掉
            logger.warning("追踪包装失败，已跳过 %s：%s", name, exc)
            return fn

    return decorator


def update_generation(**fields: Any) -> None:
    """给「当前」generation 补信息（token 用量、模型名…）。

    只能在被 `@observe(as_type="generation")` 包住的函数体里调用；
    没接追踪 / 不在 generation 里，都是安静的 no-op。
    """
    if _CLIENT_FACTORY is None:
        return
    try:
        _CLIENT_FACTORY().update_current_generation(**fields)
    except Exception:  # noqa: BLE001
        pass


def flush() -> None:
    """把缓冲区里的 span 全发出去。

    ★ 这一行不能省：Langfuse 走 OpenTelemetry **批量上报**，进程退出时
    缓冲区里没发出去的 span **会直接丢**。跑评测脚本（几秒就跑完）尤其需要；
    常驻的 uvicorn 服务倒是可以不管（它会定期自动 flush）。
    """
    if _CLIENT_FACTORY is None:
        return
    try:
        _CLIENT_FACTORY().flush()
    except Exception:  # noqa: BLE001
        pass


def shutdown() -> None:
    """彻底关掉追踪客户端（服务停止时调用，避免残留后台线程）。"""
    if _CLIENT_FACTORY is None:
        return
    try:
        _CLIENT_FACTORY().shutdown()
    except Exception:  # noqa: BLE001
        pass
