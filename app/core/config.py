# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
from urllib.parse import quote_plus
from pydantic_settings import SettingsConfigDict
import secrets

class Settings(BaseSettings):
    # ---------------------------
    # Pydantic 配置
    # ---------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ---------------------------
    # 应用基础配置
    # ---------------------------
    PROJECT_NAME: str = Field(default="FastAPI Mini Blog")
    VERSION: str = Field(default="1.0.0")
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    # ---------------------------
    # 数据库配置
    # ---------------------------
    DATABASE_URL: Optional[str] = None
    DATABASE_URL_ASYNC: Optional[str] = None
    DATABASE_POOLER_HOST: Optional[str] = None
    DATABASE_POOLER_PORT: str = "6543"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_NAME: str = "postgres"
    DATABASE_SSL_VERIFY: bool = False

    def model_post_init(self, __context) -> None:
        """
        根据连接池变量动态拼接 DATABASE_URL（优先使用 .env 中的完整 DATABASE_URL）
        """
        if not self.DATABASE_URL and self.DATABASE_POOLER_HOST and self.DATABASE_PASSWORD:
            self.DATABASE_URL = (
                f"postgresql+psycopg2://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}"
                f"@{self.DATABASE_POOLER_HOST}:{self.DATABASE_POOLER_PORT}/{self.DATABASE_NAME}"
                f"?sslmode=require"
            )
        if not self.DATABASE_URL_ASYNC and self.DATABASE_POOLER_HOST and self.DATABASE_PASSWORD:
            self.DATABASE_URL_ASYNC = (
                f"postgresql+asyncpg://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}"
                f"@{self.DATABASE_POOLER_HOST}:{self.DATABASE_POOLER_PORT}/{self.DATABASE_NAME}"
            )

    # ---------------------------
    # 安全配置
    # ---------------------------
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ---------------------------
    # 跨域配置（使用 default_factory 避免深拷贝问题）
    # ---------------------------
    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])


# 实例化配置
settings = Settings()

if __name__ == "__main__":
    print("DATABASE_URL =", settings.DATABASE_URL)
    print("DATABASE_URL_ASYNC =", settings.DATABASE_URL_ASYNC)