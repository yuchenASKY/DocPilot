"""向量库：本地 numpy 实现，可平滑替换成 Chroma / Milvus / pgvector。

为什么骨架先用 numpy 而不是直接上 Milvus：
面试时会问「为什么选这个向量库」。合理的进阶路径是
  入门用 Chroma（最轻） → 简历项目用 Milvus / pgvector（有工程感）。
本文件把「增 / 查 / 存 / 载」四个动作抽象成固定接口，
换库时只要实现同样四个方法，上层 retrieve.py 一行都不用改。
（这就是「面向接口编程」，也是 IoC/DI 想解决的问题——面试可以类比着讲。）
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .config import settings
from .ingest import Chunk


class VectorStore:
    """极简向量库：向量存 .npy，元数据存 .jsonl。"""

    def __init__(self, path: str | Path | None = None) -> None:
        self.dir = Path(path or settings.vector_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self._vec_path = self.dir / "vectors.npy"
        self._meta_path = self.dir / "meta.jsonl"
        self.vectors: np.ndarray = np.zeros((0, settings.embed_dim), dtype=np.float32)
        self.metas: list[dict] = []
        self.load()

    # ---------- 增 ----------
    def add(self, chunks: list[Chunk], vectors: list[list[float]]) -> int:
        if not chunks:
            return 0
        new_vecs = np.asarray(vectors, dtype=np.float32)

        # 按 chunk_id 去重，重复入库时覆盖旧版本
        existing = {m["chunk_id"]: i for i, m in enumerate(self.metas)}
        keep_idx: list[int] = []
        for i, meta in enumerate(self.metas):
            if meta["chunk_id"] not in {c.chunk_id for c in chunks}:
                keep_idx.append(i)

        old_vecs = self.vectors[keep_idx] if len(keep_idx) else np.zeros(
            (0, self.vectors.shape[1]), dtype=np.float32
        )
        old_metas = [self.metas[i] for i in keep_idx]

        self.vectors = np.vstack([old_vecs, new_vecs]).astype(np.float32)
        self.metas = old_metas + [
            {
                "chunk_id": c.chunk_id,
                "text": c.text,
                "source": c.source,
                "page": c.page,
                **c.meta,
            }
            for c in chunks
        ]
        _ = existing  # 保留变量便于调试
        return len(chunks)

    # ---------- 查 ----------
    def search(
        self, query_vec: list[float], top_k: int = 5
    ) -> list[tuple[dict, float]]:
        """余弦相似度检索

        规格：
          1. 库为空 → 返回 []；
          2. 返回 list[(元数据 dict, 相似度 float)]，按相似度降序；
          3. 返回条数 <= top_k。

        提示（用 numpy，别写 Python 双层循环）：
          - 余弦相似度 = 点积 / 模长之积。本项目的向量入库前都做过 L2 归一化，
            所以 余弦相似度就等于点积 —— 可以直接用一次矩阵乘法
            `self.vectors @ q` 把所有相似度一次算完（O(n·d)，走的是 C 层，比你写循环快几十倍）；
          - 顺手把 q 也归一化一次，换 embedding 模型后不至于结果全错；
          - Top-K 不必全排序：`np.argpartition(-sims, k-1)[:k]` 是 O(n)，
            比 `np.argsort` 的 O(n log n) 快；拿到这 k 个之后再对它们排序。
          - 下面那段维度校验是现成的，保留它 —— 这类「静默错误」最难排查。
        """
        if len(self.metas) == 0:
            return []

        q = np.asarray(query_vec, dtype=np.float32)
        qn = float(np.linalg.norm(q))
        if qn > 0:
            q = q / qn

        # 维度不一致（换过 embedding 模型）时给明确提示，别静默出错
        if q.shape[0] != self.vectors.shape[1]:
            raise ValueError(
                f"向量维度不匹配：查询 {q.shape[0]} vs 库 {self.vectors.shape[1]}。"
                "换过 embedding 模型后需要重建索引：uv run python scripts/build_index.py --rebuild"
            )

        # ------------------------------------------------------------------
        # TODO(第 6 步)：在这里算出 sims，取出 Top-K，按降序返回
        #   sims = ...                                  # 一次矩阵乘法
        #   idx  = ...                                  # O(n) 取 Top-K
        #   return [(self.metas[i], float(sims[i])) for i in idx]
        # ------------------------------------------------------------------
        # 向量入库前都做过 L2 归一化，所以余弦相似度就等于点积 ——
        # 一次矩阵乘法把所有相似度算完（走 numpy 的 C 层，比 Python 循环快几十倍）
        sims = self.vectors @ q

        # Top-K 不必全排序：argpartition 是 O(n)，拿到这 k 个之后再对它们排序
        k = min(top_k, len(sims))
        idx = np.argpartition(-sims, k - 1)[:k]
        idx = idx[np.argsort(-sims[idx])]

        return [(self.metas[i], float(sims[i])) for i in idx]

    # ---------- 存 / 载 ----------
    def save(self) -> None:
        np.save(self._vec_path, self.vectors)
        with self._meta_path.open("w", encoding="utf-8") as f:
            for m in self.metas:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def load(self) -> None:
        if self._vec_path.exists() and self._meta_path.exists():
            self.vectors = np.load(self._vec_path).astype(np.float32)
            with self._meta_path.open("r", encoding="utf-8") as f:
                self.metas = [json.loads(line) for line in f if line.strip()]

    def __len__(self) -> int:
        return len(self.metas)


store = VectorStore()