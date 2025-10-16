import asyncio
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User

@pytest.fixture(scope="function")
def client():
    # 使用文件型 SQLite，避免内存库的连接隔离问题
    engine = create_async_engine(
        "sqlite+aiosqlite:///./test_auth.db",
        echo=False,
        future=True,
    )

    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())

    TestSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    # 覆盖依赖，确保路由使用测试数据库
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # 还原依赖、关闭引擎、清理测试文件
    app.dependency_overrides.clear()
    async def teardown():
        await engine.dispose()
    asyncio.run(teardown())
    try:
        os.remove("./test_auth.db")
    except OSError:
        pass

def test_register_success_and_duplicate(client):
    payload = {"email": "tester@example.com", "password": "secret123", "full_name": "Tester"}

    # 第一次注册成功
    r1 = client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["email"] == payload["email"]
    assert data1.get("full_name") == payload["full_name"]
    assert "id" in data1
    # 响应模型不应包含敏感字段
    assert "hashed_password" not in data1

    # 第二次用相同邮箱，返回 400
    r2 = client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already registered"

def test_register_invalid_email_returns_422(client):
    bad_payload = {"email": "not-an-email", "password": "secret123", "full_name": None}
    r = client.post("/api/v1/auth/register", json=bad_payload)
    assert r.status_code == 422