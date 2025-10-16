from fastapi import FastAPI, Depends
from app.db.session import get_db
from app.core.config import settings
from app.api.v1 import auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/db/test")
async def db_test(db=Depends(get_db)):
    try:
        # ✅ 改成 asyncpg 的 fetchval()
        result = await db.fetchval("SELECT 1")
        return {"message": "✅ Database connected successfully!", "result": result}
    except Exception as e:
        return {"message": "❌ Database test failed", "error": str(e)}
