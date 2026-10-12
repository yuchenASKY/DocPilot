"""文档接入：解析（PDF / MD / TXT） → 递归切块 → 带元数据的片段。

RAG 的第一公里。切块质量直接决定后面检索效果，
所以「切块策略」是 AI 岗面试的必问题。
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

# 分隔符优先级：先按「结构边界」切，不够长再往细粒度降级
_SEPARATORS = ["\n\n", "\n", "。", "！", "？", ". ", "；", ";", "，", ",", " ", ""]


@dataclass
class Chunk:
    text: str
    source: str
    page: int | None = None
    chunk_id: str = ""
    meta: dict = field(default_factory=dict)


def _read_pdf(path: Path) -> list[tuple[int, str]]:
    """返回 [(页码, 该页文本), ...]。没装 pypdf 时给出友好提示。"""
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "解析 PDF 需要 pypdf，请执行：uv pip install pypdf"
        ) from exc

    reader = PdfReader(str(path))
    pages: list[tuple[int, str]] = []
    for i, page in enumerate(reader.pages, start=1):
        pages.append((i, page.extract_text() or ""))
    return pages


def _read_text(path: Path) -> list[tuple[int | None, str]]:
    return [(None, path.read_text(encoding="utf-8", errors="ignore"))]


def load_file(path: str | Path) -> list[Chunk]:
    """把单个文件解析成「未切块」的原始段落列表。"""
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        pages = _read_pdf(path)
    elif suffix in {".md", ".markdown", ".txt", ".rst", ".py", ".java"}:
        pages = _read_text(path)
    else:
        raise ValueError(f"暂不支持的文件类型：{suffix}")

    out: list[Chunk] = []
    for page_no, text in pages:
        text = _normalize(text)
        if not text.strip():
            continue
        out.append(Chunk(text=text, source=path.name, page=page_no))
    return out


def _normalize(text: str) -> str:
    """清洗：统一换行、压缩多余空行、去掉页眉页脚噪声。

    PDF 抽出来的文本混着页眉页脚和多余空行，不清洗会污染切块结果
    （同一个句子被空行拆开、页码混进正文），所以这一步不能省。
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 常见页脚噪声：形如 "12 / 300" 或 "第 12 页"
    text = re.sub(r"\n\s*\d+\s*/\s*\d+\s*\n", "\n", text)
    text = re.sub(r"\n\s*第\s*\d+\s*页\s*\n", "\n", text)
    return text.strip()


def split_text(
        text: str,
        chunk_size: int,
        overlap: int,
        separators: list[str] | None = None,
) -> list[str]:
    """递归字符切块

    规格（做到这四条就算过）：
      1. 输入的每个片段，长度都 <= chunk_size（特殊情况见第 4 条）；
      2. 优先在「语义边界」切开，顺序是 空行 > 换行 > 句号 > 逗号 …（见模块级 _SEPARATORS）；
         宁可片段短一点，也不要切断一个完整句子；
      3. 相邻片段之间保留 overlap 个字符的重叠（答案正好落在切缝上时，
         没有重叠会导致两半都不完整、检索不到）；
      4. 只有实在找不到分隔符时才硬切字符（此时 step = chunk_size - overlap）；
      5. 重叠和上限冲突时，以「不超长」为准 —— 如果 tail + piece 超过 chunk_size，
         就放弃这次重叠（这条最容易漏：500 的字块接上 80 的重叠 = 580，切块就不均匀了）。

    建议做法（思路，不是代码）：
      - 先把文本按 separators[0] 切开；
      - 逐块往一个缓冲区里攒，攒到再加就超过 chunk_size 就先把缓冲区收成一个片段；
      - 如果某一块本身就超长，用 separators[1:] 递归调用自己；
      - 新片段开头带上上一段的末尾 overlap 个字符。

          说明文档第 5 步「必须掌握的知识点」+ LangChain 的
      RecursiveCharacterTextSplitter 文档。
    """
    separators = separators or _SEPARATORS

    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    sep = separators[0]
    rest = separators[1:]

    if sep == "":
        # 兜底：已经细到没有分隔符可用，只能按固定长度硬切
        step = max(1, chunk_size - overlap)
        return [text[i: i + chunk_size] for i in range(0, len(text), step)]

    pieces = text.split(sep)
    chunks: list[str] = []
    buf = ""

    for piece in pieces:
        candidate = buf + sep + piece if buf else piece
        if len(candidate) <= chunk_size:
            buf = candidate  # 还没满，继续往里攒
            continue

        if buf:
            chunks.append(buf)  # 满了，先把缓冲收成一个片段

        if len(piece) > chunk_size:
            # 单个 piece 本身就超长 → 用更细的分隔符递归处理它
            chunks.extend(split_text(piece, chunk_size, overlap, rest))
            buf = ""
        else:
            # 新片段开头带上上一段的末尾 overlap 个字符，避免答案正好落在切缝上。
            # 注意 tail + piece 有可能超过 chunk_size（tail 最多 overlap 个字符），
            # 这时宁可放弃这次重叠，也要守住「片段不超长」这条硬规格 ——
            # 否则片段会长到 500+80=580，切块就不均匀了。
            tail = chunks[-1][-overlap:] if chunks and overlap else ""
            buf = tail + piece
            if len(buf) > chunk_size:
                buf = piece

    if buf.strip():
        chunks.append(buf)

    return [c.strip() for c in chunks if c.strip()]


def build_chunks(
    path: str | Path,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """解析 + 切块，产出可直接入库的 Chunk 列表。"""
    from .config import settings

    cs = chunk_size or settings.chunk_size
    ov = overlap if overlap is not None else settings.chunk_overlap

    chunks: list[Chunk] = []
    for seg in load_file(path):
        for i, piece in enumerate(split_text(seg.text, cs, ov)):
            cid = hashlib.md5(
                f"{seg.source}:{seg.page}:{i}:{piece}".encode()
            ).hexdigest()[:16]
            chunks.append(
                Chunk(
                    text=piece,
                    source=seg.source,
                    page=seg.page,
                    chunk_id=cid,
                    meta={"chunk_index": i},
                )
            )
    return chunks