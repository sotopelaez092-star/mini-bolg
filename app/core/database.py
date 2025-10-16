from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 创建数据库引擎
if settings.DATABASE_URL:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # 连接前检查连接是否有效
        pool_recycle=300,    # 5分钟后回收连接
        echo=settings.ENVIRONMENT == "development"  # 开发环境显示SQL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("数据库引擎创建成功")
else:
    logger.error("DATABASE_URL 未配置")
    engine = None
    SessionLocal = None

def get_db():
    """获取数据库会话"""
    if not SessionLocal:
        raise Exception("数据库未正确配置")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
