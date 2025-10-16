import ssl
import logging
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.dialects.postgresql import base as pg_base
from app.core.config import settings
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_cursor

# Monkey patch: disable prepared statements in asyncpg cursor
async def do_execute_no_prepare(self, cursor, statement, parameters, context=None):
    await cursor._connection.execute(statement, *parameters)

AsyncAdapt_asyncpg_cursor.do_execute = do_execute_no_prepare

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logger = logging.getLogger("db.session")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# -----------------------------------------------------------------------------
# DSN Configuration
# -----------------------------------------------------------------------------
ASYNC_DSN = settings.DATABASE_URL
if not ASYNC_DSN:
    raise RuntimeError("❌ DATABASE_URL 未配置。请在环境变量或 .env 中提供。")

RAW_DSN = ASYNC_DSN.replace("+asyncpg", "")
IS_POOLER = ".pooler." in RAW_DSN
logger.info(f"🌐 Using {'PgBouncer Pooler' if IS_POOLER else 'Direct'} connection.")

# -----------------------------------------------------------------------------
# SSL Context
# -----------------------------------------------------------------------------
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# -----------------------------------------------------------------------------
# asyncpg Connector
# -----------------------------------------------------------------------------
async def async_creator():
    """自定义连接函数，兼容 PgBouncer"""
    conn = await asyncpg.connect(
        RAW_DSN,
        ssl=ssl_context,
        statement_cache_size=0,  # ✅ 禁用 asyncpg 缓存
    )
    return conn

# -----------------------------------------------------------------------------
# SQLAlchemy Engine
# -----------------------------------------------------------------------------
engine = create_async_engine(
    "postgresql+asyncpg://",
    echo=(settings.ENVIRONMENT == "development"),
    future=True,
    async_creator=async_creator,
    connect_args={"statement_cache_size": 0},  # ✅ 禁用 SQLAlchemy 自带缓存
    pool_pre_ping=True,
)

# 彻底禁用 SQLAlchemy 层 statement cache
engine.dialect.supports_statement_cache = False

# Monkey patch: Skip server version check for PgBouncer
def _skip_init(self, connection):
    self.server_version_info = (14, 0)
    return

if IS_POOLER:
    pg_base.PGDialect.initialize = _skip_init
    logger.warning("⚙️ Applied PGDialect.initialize() monkey patch to skip version check.")

# -----------------------------------------------------------------------------
# Async Session
# -----------------------------------------------------------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


import asyncpg

async def get_db():
    conn = await asyncpg.connect(RAW_DSN, ssl=ssl_context, statement_cache_size=0)
    try:
        yield conn
    finally:
        await conn.close()
