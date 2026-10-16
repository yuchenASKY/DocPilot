from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（app/ 的上一级）
ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- LLM ---
    openai_api_key: str = ""
    openai_base_url: str = "https://api.deepseek.com/v1"
    llm_model: str = "deepseek-chat"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1024

    # --- Embedding（第 6 步用）---
    # 注意：DeepSeek 只有 chat、没有 /embeddings 接口，
    # 所以 EMBED_BASE_URL / EMBED_API_KEY 通常要填另一家服务商。
    embed_model: str = ""          # 留空 -> 使用内置离线伪向量
    embed_dim: int = 512           # 必须与所选模型匹配（bge-m3=1024、智谱 embedding-3=2048…）
    embed_api_key: str = ""        # 留空 -> 复用 OPENAI_API_KEY
    embed_base_url: str = ""       # 留空 -> 复用 OPENAI_BASE_URL
    embed_batch_size: int = 10     # 单次请求最多发几条文本：阿里百炼上限 20，多数服务商 10

    # --- Rerank（第 8 步 ④用）---
    # 真实的 cross-encoder 重排服务。
    # ⚠️ 注意：阿里百炼的 rerank **不支持 OpenAI 兼容端点**（实测 /compatible-mode/v1/rerank 是 404），
    #    必须走 DashScope 原生路径 —— 代码里会自动拼 /api/v1/services/rerank/text-rerank/text-rerank。
    #    所以 RERANK_BASE_URL 填**主机地址**（不要带 /compatible-mode/v1）。
    rerank_model: str = ""         # 例：gte-rerank-v2；留空 -> 不调 API，退化成覆盖率基线
    rerank_api_key: str = ""       # 留空 -> 复用 EMBED_API_KEY（通常同一家服务商）
    rerank_base_url: str = ""      # 留空 -> https://dashscope.aliyuncs.com
    use_rerank: bool = False       # 默认关：开了会更准，但每次检索多一次 API 调用（更慢也更贵）

    # --- 检索（第 5 / 8 / 12 步用）---
    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 80
    hybrid_alpha: float = 0.5      # 混合检索权重（0~1，越大越偏向向量）
    rrf_k: int = 60                # RRF 融合常数，论文推荐 60

    # 相关性阈值（第 12 步 ⑤）：向量相似度低于它的候选一律丢弃。
    # ★ 这是「拒答」能不能真正生效的关键 —— 没有它，任何问题都会返回 top_k 条，
    #   graph.py 里那句 `if not hits: 拒答` 永远不触发，库外问题照样拿到 5 条
    #   无关文档、还把它们当「引用来源」返回给前端。
    # 0.49 是用本项目 40 题 golden set **实测标定**出来的：
    #   应拒答题的最高分 = 0.4875，应命中题的最低 top-1 = 0.5018（两者不重叠）。
    # ⚠️ 换语料或换 embedding 模型后**必须重标** —— 这个值依赖于
    #   「语料的相似度分布」，不是一个通用常数。标法：跑
    #   `uv run python eval/run_eval.py`，对比「该拒答」与「该命中」两类的分数区间。
    # 设为 0 或负数 = 关闭过滤（退回旧行为）。
    min_score: float = 0.49

    # --- 存储 ---
    vector_dir: Path = ROOT_DIR / ".data" / "vectorstore"
    upload_dir: Path = ROOT_DIR / ".data" / "uploads"
    docs_dir: Path = ROOT_DIR / "data" / "docs"

    # --- 可选：Langfuse 追踪（第 12 步 ⑥）---
    # 三个都填了才会启用；任一为空 → app/tracing.py 里全部是空操作。
    # 免费注册：https://cloud.langfuse.com（自建也一样，改 HOST 即可）
    langfuse_public_key: str = ""    # LANGFUSE_PUBLIC_KEY，形如 pk-lf-...
    langfuse_secret_key: str = ""    # LANGFUSE_SECRET_KEY，形如 sk-lf-...
    langfuse_host: str = "https://cloud.langfuse.com"

    # --- 可选 Redis（第 13 步用）---
    redis_url: str = "redis://127.0.0.1:6379/0"
    use_redis: bool = False

    @property
    def llm_enabled(self) -> bool:
        """有没有配真实 LLM Key。没配就走离线降级，保证链路能跑通。"""
        return bool(self.openai_api_key.strip())

    @property
    def effective_embed_api_key(self) -> str:
        """embedding 实际用哪个 Key：优先 EMBED_API_KEY，否则复用 LLM 的。"""
        return (self.embed_api_key or self.openai_api_key).strip()

    @property
    def effective_embed_base_url(self) -> str:
        """embedding 实际请求哪个地址：优先 EMBED_BASE_URL，否则复用 LLM 的。"""
        return (self.embed_base_url or self.openai_base_url).strip()

    @property
    def embed_enabled(self) -> bool:
        """有没有配真实 embedding 服务（第 6 步用）。

        判的是 embedding 自己那套凭据（可以是另一家服务商），
        不再要求「LLM 也必须配」—— 两件事本来就是独立的。
        """
        return (
            bool(self.embed_model.strip())
            and bool(self.effective_embed_base_url)
            and bool(self.effective_embed_api_key)
        )

    @property
    def effective_rerank_api_key(self) -> str:
        """rerank 用哪个 Key：优先 RERANK_API_KEY，否则复用 embedding 的（通常是同一家）。"""
        return (self.rerank_api_key or self.embed_api_key or self.openai_api_key).strip()

    @property
    def effective_rerank_base_url(self) -> str:
        """rerank 的主机地址：优先 RERANK_BASE_URL，否则默认阿里百炼。

        注意这里给的是**主机**（不含 /compatible-mode/v1）——
        百炼的 rerank 走 DashScope 原生路径，和 embedding 的端点不是同一个。
        """
        return (self.rerank_base_url or "https://dashscope.aliyuncs.com").strip()

    @property
    def rerank_enabled(self) -> bool:
        """有没有配真实 rerank 服务。

        没配（或调用失败）时，`_rerank()` 会退化成「查询词覆盖率」基线 ——
        效果差但链路完整，而且能用来量出「上真模型之后提升多少」。
        """
        return bool(self.rerank_model.strip()) and bool(self.effective_rerank_api_key)

    @property
    def langfuse_enabled(self) -> bool:
        """有没有配 Langfuse（第 12 步 ⑥）。

        刻意做成「两个 Key 都填才算开」：只填一半时 langfuse 自己会打
        一句 "Authentication error ... Client will be disabled" 然后全程静默，
        很难看出是漏填了 —— 不如在配置层就拦住。
        """
        return bool(self.langfuse_public_key.strip()) and bool(
            self.langfuse_secret_key.strip()
        )


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    # 首次启动时把数据目录建出来，省得后面写文件时报「目录不存在」
    s.vector_dir.mkdir(parents=True, exist_ok=True)
    s.upload_dir.mkdir(parents=True, exist_ok=True)
    return s


settings = get_settings()