"""
Supabase 客户端配置
"""
from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 创建 Supabase 客户端
supabase: Client = None

def get_supabase_client() -> Client:
    """获取 Supabase 客户端实例"""
    global supabase
    
    if supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise Exception("Supabase URL 和 Key 未配置")
        
        try:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logger.info("Supabase 客户端创建成功")
        except Exception as e:
            logger.error(f"创建 Supabase 客户端失败: {e}")
            raise
    
    return supabase

def init_supabase():
    """初始化 Supabase 客户端"""
    try:
        get_supabase_client()
        logger.info("Supabase 初始化成功")
    except Exception as e:
        logger.error(f"Supabase 初始化失败: {e}")
        raise


