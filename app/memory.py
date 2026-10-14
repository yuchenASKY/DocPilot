"""记忆机制。

三层结构（也是面试标准答案的结构）：
1. 短期记忆：最近 N 轮对话原文，直接塞进 Prompt —— 便宜、快，但会撑爆上下文；
2. 长期记忆：把历史对话「摘要」后向量化存起来，需要时按相似度召回；
3. 压缩策略：超过窗口就滚动摘要（把旧对话压成一段要点），保住关键信息。

骨架里用内存字典实现，重启即失效；
生产环境把 _sessions 换成 Redis，重启后会话还在（第 14 步做）。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import settings


@dataclass
class Turn:
    role: str
    content: str


@dataclass
class Session:
    session_id: str
    turns: list[Turn] = field(default_factory=list)
    summary: str = ""            # 滚动摘要（长期记忆的载体）
    max_turns: int = 20          # 超过就把最早的 turns 压进 summary

    def add(self, role: str, content: str) -> None:
        self.turns.append(Turn(role=role, content=content))
        if len(self.turns) > self.max_turns:
            self._compress()

    def _compress(self) -> None:
        """上下文压缩

        触发时机：`add()` 里发现轮数超过 `max_turns` 就会调用它。
        要解决的问题：上下文不能无限涨 —— ① 窗口有上限；② **每一轮都要为全部历史
        重新付费**，聊到第 20 轮输入 token 可能是第 1 轮的 20 倍；③ 太长会稀释注意力。

        规格（做到这三条就算过）：
          1. 调用后 `len(self.turns)` 必须 <= `max_turns`（否则 add() 会反复触发，死循环风险）；
          2. 被丢弃的早期对话要压进 `self.summary`（不能直接扔），
             且 `self.summary` 非空；
          3. 不能把 `self.turns` 整个清空 —— 最近几轮的原文要保留
             （指代、约束、偏好这些细节靠摘要会丢）。

        两条实现路线：
          A. 朴素版（先跑通再优化）：把最早的一半对话截断成短句拼接进 summary。
             好处是零成本、无依赖；代价是丢信息。
          B. 生产版（第 11 步真正要做的）：调一次 LLM 生成摘要，prompt 里明确要求
             「保留实体、用户偏好、已确认的结论，压成 200 字要点」；
             再把摘要向量化存进长期记忆库，需要时按当前问题相似度召回。
             ⚠️ 注意：这里调 LLM 会让 add() 变成异步 —— 你需要决定是
             改成 `async def`（并调整调用方），还是用 `asyncio.to_thread` 包一层。
        """
        # 朴素版（路线 A）：把较早的对话压进 summary，保留最近几轮原文。
        # 生产版应改成调一次 LLM 生成摘要（见第 11 步知识点）。
        if len(self.turns) <= self.max_turns:
            return
        keep = max(1, self.max_turns // 2)      # 保留最近 keep 轮原文
        cut = len(self.turns) - keep
        dropped, self.turns = self.turns[:cut], self.turns[cut:]
        brief = "；".join(f"{t.role}:{t.content[:40]}" for t in dropped)
        self.summary = (self.summary + " " + brief).strip()[:1000]

    def to_messages(self, system_prompt: str) -> list[dict]:
        msgs: list[dict] = [{"role": "system", "content": system_prompt}]
        if self.summary:
            msgs.append(
                {
                    "role": "system",
                    "content": f"以下是更早对话的摘要，供你参考：{self.summary}",
                }
            )
        msgs.extend({"role": t.role, "content": t.content} for t in self.turns)
        return msgs


_sessions: dict[str, Session] = {}


def get_session(session_id: str) -> Session:
    if session_id not in _sessions:
        _sessions[session_id] = Session(session_id=session_id)
    return _sessions[session_id]


def clear_session(session_id: str) -> bool:
    return _sessions.pop(session_id, None) is not None


def stats() -> dict:
    return {
        "active_sessions": len(_sessions),
        "max_turns_per_session": 20,
        "redis_enabled": settings.use_redis,
    }