import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine, text
from app.core.config import settings

print("🔌 连接数据库中...")

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()")).fetchone()
        print("✅ 数据库连接成功！当前时间：", result[0])
except Exception as e:
    print("❌ 数据库连接失败:", e)