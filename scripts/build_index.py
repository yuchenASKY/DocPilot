"""把 data/docs 下的文档解析、切块、向量化、写入向量库。

用法：
    uv run python scripts/build_index.py            # 增量（按 chunk_id 去重）
    uv run python scripts/build_index.py --rebuild   # 清空重建（换 embedding 模型后必须重建）
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import ingest, vectorstore  # noqa: E402
from app.config import settings  # noqa: E402
from app.embedding import embedder  # noqa: E402

SUPPORTED = {".pdf", ".md", ".markdown", ".txt"}


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="清空索引后重建")
    parser.add_argument("--dir", default=str(settings.docs_dir), help="文档目录")
    args = parser.parse_args()

    docs_dir = Path(args.dir)
    files = [p for p in docs_dir.rglob("*") if p.suffix.lower() in SUPPORTED]

    if not files:
        print(f"[!] {docs_dir} 里没有找到可解析的文档（支持 {SUPPORTED}）")
        print("    把 PDF / Markdown 丢进这个目录再跑一次。")
        return

    print(f"[*] embedding 模式：{embedder.mode}")
    if args.rebuild:
        vectorstore.store.vectors = vectorstore.store.vectors[:0]
        vectorstore.store.metas = []
        print("[*] 已清空旧索引")

    total = 0
    for path in files:
        try:
            chunks = ingest.build_chunks(path)
        except Exception as exc:  # noqa: BLE001
            print(f"[x] {path.name} 解析失败：{exc}")
            continue

        if not chunks:
            print(f"[-] {path.name} 没有切出内容，跳过")
            continue

        vectors = await embedder.embed([c.text for c in chunks])
        vectorstore.store.add(chunks, vectors)
        total += len(chunks)
        print(f"[+] {path.name:<40} {len(chunks):>4} 个片段")

    vectorstore.store.save()
    print(f"\n[OK] 本次入库 {total} 个片段，库中共 {len(vectorstore.store)} 个")
    print(f"     索引位置：{settings.vector_dir}")
    await embedder.aclose()


if __name__ == "__main__":
    asyncio.run(main())