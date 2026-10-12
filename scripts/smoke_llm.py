"""最小 LLM 调用脚本 —— 第 3 步的验收工具。

用法：
    uv run python scripts/smoke_llm.py
    uv run python scripts/smoke_llm.py --stream   # 看流式输出

只要这个脚本能打印出模型回答，就说明
「API Key + Base URL + 模型名 + 网络」这四件事全都对了。
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings  # noqa: E402
from app.llm import llm_client  # noqa: E402


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream", action="store_true", help="用流式模式输出")
    parser.add_argument("--q", default="用一句话解释什么是 RAG。", help="要问的问题")
    args = parser.parse_args()

    print("=" * 60)
    print(f"base_url  : {settings.openai_base_url}")
    print(f"model     : {settings.llm_model}")
    print(f"api_key   : {'已配置' if llm_client.enabled else '未配置（将走离线降级）'}")
    print("=" * 60)

    messages = [{"role": "user", "content": args.q}]

    if args.stream:
        print("流式输出：", end="", flush=True)
        async for piece in llm_client.chat_stream(messages):
            print(piece, end="", flush=True)
        print()
    else:
        resp = await llm_client.chat(messages)
        print(resp["content"])
        if resp.get("usage"):
            print("\n--- token 用量 ---")
            print(resp["usage"])

    await llm_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
