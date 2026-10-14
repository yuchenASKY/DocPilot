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

    # --- 检索（第 5 / 8 步用）---
    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 80
    hybrid_alpha: float = 0.5      # 混合检索权重（0~1，越大越偏向向量）
    rrf_k: int = 60                # RRF 融合常数，论文推荐 60

    # --- 存储 ---
    vector_dir: Path = ROOT_DIR / ".data" / "vectorstore"
    upload_dir: Path = ROOT_DIR / ".data" / "uploads"
    docs_dir: Path = ROOT_DIR / "data" / "docs"

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


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    # 首次启动时把数据目录建出来，省得后面写文件时报「目录不存在」
    s.vector_dir.mkdir(parents=True, exist_ok=True)
    s.upload_dir.mkdir(parents=True, exist_ok=True)
    return s


settings = get_settings()