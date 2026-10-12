"""接口冒烟测试（第 4 步的验收）。

只验「服务没挂、字段没写错」，不验模型效果 —— 模型效果归第 12 步的评测脚本管。

跑法：
    .venv/Scripts/python.exe -m pytest -q tests
    # 或者在 PyCharm 里右击 tests 目录 → Run 'pytest in tests'

★ 关于「跳过的测试」（PyCharm 里显示为灰色的 s）：
  /chat、/stats、/upload 要等第 7~12 步把模块补齐后才存在，
  所以下面这几个测试用 skipif 自动判断 —— 接口还没写就跳过（显示 s），
  等你把接口补上，同一个测试会自动开始跑，不需要回来改测试代码。
  所以本步跑出「1 passed, 3 skipped」是正常的；
  等第 12 步做完，它会自动变成「4 passed」。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 让 pytest 能找到项目根下的 app 包（否则报 No module named 'app'）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def _has_route(path: str) -> bool:
    """这个接口写好了吗？写好了就不跳过对应测试。"""
    return any(getattr(route, "path", None) == path for route in app.routes)


def test_health_ok() -> None:
    """/health 必须 200，且关键字段都在。"""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "llm_enabled" in body
    assert isinstance(body["indexed_chunks"], int)


@pytest.mark.skipif(
    not _has_route("/chat"),
    reason="/chat 还没实现（第 7 步）—— 补上接口后这个测试会自动开始跑",
)
def test_chat_returns_full_schema() -> None:
    """/chat 的响应字段一个都不能少 —— 少一个前端就对不上。"""
    r = client.post("/chat", json={"question": "你好", "session_id": "smoke"})
    assert r.status_code == 200
    body = r.json()
    for key in ("session_id", "answer", "sources", "used_tools", "route", "latency_ms"):
        assert key in body, f"响应里少了字段：{key}"


@pytest.mark.skipif(
    not _has_route("/chat"),
    reason="/chat 还没实现（第 7 步）—— 补上接口后这个测试会自动开始跑",
)
def test_chat_rejects_empty_question() -> None:
    """空问题应该被 pydantic 挡下来，返回 422（不是你手写的 if）。"""
    r = client.post("/chat", json={"question": ""})
    assert r.status_code == 422


@pytest.mark.skipif(
    not _has_route("/stats"),
    reason="/stats 还没实现（第 12 步）—— 补上接口后这个测试会自动开始跑",
)
def test_stats_ok() -> None:
    """/stats 是排查问题时的第一站。"""
    r = client.get("/stats")
    assert r.status_code == 200
    body = r.json()
    assert "indexed_chunks" in body
    assert "tools" in body
