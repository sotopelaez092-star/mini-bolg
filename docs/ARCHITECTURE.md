# FastAPI Mini Blog - 项目骨架设计文档

## 1. 技术栈选型

### 1.1 核心框架
- **FastAPI 0.104+**: 现代、高性能的 Web 框架
- **Python 3.11+**: 最新 LTS 版本，性能提升显著
- **Uvicorn**: ASGI 服务器，支持异步

### 1.2 数据层
- **SQLAlchemy 2.0**: ORM 框架（支持异步）
- **Alembic**: 数据库迁移工具
- **PostgreSQL 14+**: 主数据库（生产环境）
- **Redis 7+**: 缓存层（后续扩展）
- **asyncpg**: PostgreSQL 异步驱动

### 1.3 数据验证与序列化
- **Pydantic 2.x**: 数据验证
- **pydantic-settings**: 配置管理

### 1.4 安全认证
- **python-jose[cryptography]**: JWT 实现
- **passlib[bcrypt]**: 密码加密
- **python-multipart**: 文件上传支持

### 1.5 日志与监控
- **structlog**: 结构化日志
- **prometheus-client**: Prometheus 指标
- **opentelemetry**: 分布式追踪（可选）

### 1.6 开发工具
- **pytest**: 单元测试
- **pytest-asyncio**: 异步测试支持
- **pytest-cov**: 测试覆盖率
- **black**: 代码格式化
- **ruff**: 快速 Linter
- **mypy**: 类型检查
- **pre-commit**: Git hooks

### 1.7 API 文档
- **Swagger UI**: 自动生成（FastAPI 内置）
- **ReDoc**: 备选文档界面

---

## 2. 项目文件结构

```
fastapi-mini-blog/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI/CD 配置
│       └── test.yml            # 测试流程
│
├── alembic/                    # 数据库迁移
│   ├── versions/               # 迁移版本
│   ├── env.py                  # Alembic 环境配置
│   └── script.py.mako          # 迁移脚本模板
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                 # 应用入口
│   │
│   ├── api/                    # API 层
│   │   ├── __init__.py
│   │   ├── deps.py             # 通用依赖项
│   │   ├── errors.py           # 错误处理
│   │   └── v1/                 # API v1 版本
│   │       ├── __init__.py
│   │       ├── endpoints/      # 端点模块
│   │       │   ├── __init__.py
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── posts.py
│   │       │   ├── comments.py
│   │       │   ├── categories.py
│   │       │   └── tags.py
│   │       └── router.py       # 路由聚合
│   │
│   ├── core/                   # 核心功能
│   │   ├── __init__.py
│   │   ├── config.py           # 配置管理
│   │   ├── security.py         # 安全工具（JWT、密码）
│   │   ├── logging.py          # 日志配置
│   │   ├── metrics.py          # 监控指标
│   │   └── exceptions.py       # 自定义异常
│   │
│   ├── db/                     # 数据库层
│   │   ├── __init__.py
│   │   ├── base.py             # 基类导入
│   │   ├── session.py          # 会话管理
│   │   └── init_db.py          # 数据库初始化
│   │
│   ├── models/                 # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── base.py             # 基础模型类
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── category.py
│   │   └── tag.py
│   │
│   ├── schemas/                # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── common.py           # 通用 Schema
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── category.py
│   │   └── tag.py
│   │
│   ├── crud/                   # CRUD 操作层
│   │   ├── __init__.py
│   │   ├── base.py             # 基础 CRUD 类
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── category.py
│   │   └── tag.py
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth.py             # 认证服务
│   │   ├── post.py             # 文章服务
│   │   └── search.py           # 搜索服务
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── datetime.py
│       ├── validators.py
│       └── helpers.py
│
├── tests/                      # 测试目录
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   ├── api/                    # API 测试
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── test_auth.py
│   │       ├── test_posts.py
│   │       └── test_users.py
│   ├── crud/                   # CRUD 测试
│   └── services/               # 服务测试
│
├── scripts/                    # 脚本工具
│   ├── init_db.py              # 初始化数据库
│   ├── create_superuser.py     # 创建管理员
│   └── lint.sh                 # 代码检查脚本
│
├── docs/                       # 文档目录
│   ├── api/                    # API 文档
│   ├── development.md          # 开发指南
│   └── deployment.md           # 部署指南
│
├── .env.example                # 环境变量示例
├── .env.development            # 开发环境配置
├── .env.test                   # 测试环境配置
├── .env.production             # 生产环境配置（不提交）
├── .gitignore
├── .pre-commit-config.yaml     # pre-commit 配置
├── pyproject.toml              # 项目配置（black、ruff、mypy）
├── requirements.txt            # 生产依赖
├── requirements-dev.txt        # 开发依赖
├── alembic.ini                 # Alembic 配置
├── docker-compose.yml          # Docker 编排
├── Dockerfile                  # Docker 镜像
├── Makefile                    # 常用命令快捷方式
└── README.md
```

---

## 3. 配置管理

### 3.1 配置分层策略
- **默认配置**: `config.py` 中的默认值
- **环境变量**: `.env` 文件覆盖
- **环境区分**: development、test、production

### 3.2 配置项分类
```python
# app/core/config.py

class Settings:
    # 应用基础配置
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    
    # 环境配置
    ENVIRONMENT: Literal["development", "test", "production"]
    DEBUG: bool
    
    # 数据库配置
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # Redis 配置（可选）
    REDIS_URL: Optional[str] = None
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # 限流配置
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".png", ".gif"]
```

### 3.3 多环境配置示例
```bash
# .env.development
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/miniblog_dev
LOG_LEVEL=DEBUG

# .env.production
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db/miniblog
LOG_LEVEL=INFO
```

---

## 4. 日志系统

### 4.1 日志策略
- **结构化日志**: 使用 structlog，便于日志分析
- **日志级别**: DEBUG、INFO、WARNING、ERROR、CRITICAL
- **日志格式**: JSON 格式（生产）/ 彩色文本（开发）
- **日志输出**: stdout（容器化环境）/ 文件（传统部署）

### 4.2 日志内容规范
```python
# 必须包含的字段
{
    "timestamp": "2025-10-14T10:30:00Z",
    "level": "INFO",
    "logger": "app.api.v1.posts",
    "message": "Post created successfully",
    "request_id": "uuid-xxx",
    "user_id": "uuid-yyy",
    "event": "post.created",
    "duration_ms": 150
}
```

### 4.3 日志记录点
- API 请求/响应（包含耗时）
- 数据库查询（慢查询告警）
- 业务关键操作（创建、更新、删除）
- 异常和错误
- 安全事件（登录失败、权限拒绝）

---

## 5. 数据库连接池

### 5.1 连接池配置
```python
# 推荐配置
POOL_SIZE = 5                    # 核心连接数
MAX_OVERFLOW = 10                # 最大溢出连接数
POOL_TIMEOUT = 30                # 获取连接超时（秒）
POOL_RECYCLE = 3600              # 连接回收时间（秒）
POOL_PRE_PING = True             # 连接前测试
ECHO = False                     # 生产环境关闭 SQL 日志
```

### 5.2 连接池监控指标
- 当前活跃连接数
- 连接池大小
- 连接获取等待时间
- 连接超时次数
- 慢查询数量

### 5.3 异步数据库最佳实践
```python
# 使用 AsyncSession
# 支持连接池
# 正确处理事务
# 避免连接泄漏
```

---

## 6. 监控指标

### 6.1 核心指标（RED 方法）
**Request Rate（请求速率）**
- `http_requests_total`: 总请求数（按端点、方法、状态码）
- `http_requests_per_second`: 每秒请求数

**Error Rate（错误率）**
- `http_requests_errors_total`: 错误请求数
- `http_error_rate`: 错误率百分比

**Duration（响应时间）**
- `http_request_duration_seconds`: 请求耗时直方图
- `http_request_duration_seconds_summary`: P50、P95、P99

### 6.2 资源指标
- `db_connections_active`: 活跃数据库连接数
- `db_connections_idle`: 空闲连接数
- `db_query_duration_seconds`: 数据库查询耗时
- `cache_hits_total`: 缓存命中数（如使用 Redis）
- `cache_misses_total`: 缓存未命中数

### 6.3 业务指标
- `user_registrations_total`: 用户注册数
- `posts_created_total`: 文章创建数
- `comments_created_total`: 评论创建数
- `active_users_gauge`: 活跃用户数

### 6.4 指标暴露端点
```
GET /metrics  # Prometheus 格式
```

---

## 7. 开发规范

### 7.1 命名规范

**文件和目录**
- 全小写，使用下划线分隔: `user_service.py`
- 包名简短且有意义: `api`, `models`, `schemas`

**Python 代码**
```python
# 类名：PascalCase
class UserService:
    pass

# 函数名：snake_case
def get_user_by_id():
    pass

# 常量：UPPER_SNAKE_CASE
MAX_UPLOAD_SIZE = 5242880

# 私有成员：前缀下划线
def _internal_helper():
    pass

# 类型注解
def create_user(user_data: UserCreate) -> User:
    pass
```

**数据库命名**
```sql
-- 表名：复数形式，snake_case
users, posts, comments

-- 列名：snake_case
user_id, created_at, is_active

-- 索引：idx_表名_列名
idx_posts_author_id
idx_posts_created_at

-- 外键：fk_表名_引用表名
fk_posts_users
```

### 7.2 模块划分原则

**分层架构**
```
Endpoint (API层) 
    ↓ 调用
Service (业务逻辑层)
    ↓ 调用
CRUD (数据访问层)
    ↓ 操作
Models (数据模型层)
```

**职责划分**
- **Endpoint**: 接收请求、参数验证、返回响应
- **Service**: 业务逻辑、事务管理、调用多个 CRUD
- **CRUD**: 数据库操作，单表或简单关联
- **Models**: 数据库表定义
- **Schemas**: 请求/响应数据验证

### 7.3 代码风格规范

**使用工具强制**
```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true
```

**导入顺序**
```python
# 1. 标准库
import json
from typing import List

# 2. 第三方库
from fastapi import FastAPI
from sqlalchemy import select

# 3. 本地导入
from app.core.config import settings
from app.models.user import User
```

### 7.4 注释和文档

**函数文档字符串**
```python
def create_post(
    db: AsyncSession,
    post_data: PostCreate,
    author_id: str
) -> Post:
    """
    创建新文章
    
    Args:
        db: 数据库会话
        post_data: 文章创建数据
        author_id: 作者 ID
        
    Returns:
        创建的文章对象
        
    Raises:
        ValueError: 如果数据验证失败
        DatabaseError: 如果数据库操作失败
    """
    pass
```

**API 端点文档**
```python
@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user)
) -> PostResponse:
    """
    创建新文章
    
    - **title**: 文章标题（必填）
    - **content**: 文章内容（必填）
    - **category_id**: 分类 ID（可选）
    """
    pass
```

### 7.5 错误处理规范

**自定义异常**
```python
# app/core/exceptions.py
class AppException(Exception):
    """应用基础异常"""
    pass

class NotFoundError(AppException):
    """资源不存在"""
    pass

class UnauthorizedError(AppException):
    """未授权"""
    pass

class ForbiddenError(AppException):
    """无权限"""
    pass
```

**统一错误响应**
```json
{
    "detail": "错误描述",
    "error_code": "USER_NOT_FOUND",
    "timestamp": "2025-10-14T10:30:00Z"
}
```

### 7.6 测试规范

**测试命名**
```python
# 格式: test_<功能>_<场景>_<预期结果>
def test_create_post_with_valid_data_returns_201():
    pass

def test_create_post_without_auth_returns_401():
    pass
```

**测试覆盖要求**
- 核心业务逻辑：100%
- CRUD 操作：100%
- API 端点：90%+
- 工具函数：80%+

### 7.7 Git 提交规范

**提交信息格式**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建、工具等

**示例**
```
feat(auth): add JWT refresh token support

- Implement refresh token endpoint
- Add refresh token to login response
- Update token expiration logic

Closes #123
```

### 7.8 代码审查清单

**功能**
- [ ] 功能是否符合需求
- [ ] 边界条件处理
- [ ] 错误处理完整

**性能**
- [ ] 无 N+1 查询问题
- [ ] 使用适当的索引
- [ ] 避免不必要的计算

**安全**
- [ ] 输入验证
- [ ] SQL 注入防护
- [ ] 权限检查

**可维护性**
- [ ] 代码清晰易读
- [ ] 适当的注释
- [ ] 遵循项目规范

---

## 8. 持续集成/部署

### 8.1 CI/CD 流程
```
代码提交 → Lint 检查 → 单元测试 → 集成测试 → 构建镜像 → 部署
```

### 8.2 自动化检查
- 代码格式检查（black、ruff）
- 类型检查（mypy）
- 测试覆盖率
- 安全扫描（bandit）

### 8.3 部署策略
- 蓝绿部署
- 金丝雀发布
- 健康检查端点

---

## 9. 开发工作流

### 9.1 本地开发
```bash
# 1. 安装依赖
make install

# 2. 启动数据库
make db-up

# 3. 运行迁移
make migrate

# 4. 启动开发服务器
make dev

# 5. 运行测试
make test
```

### 9.2 功能开发流程
1. 创建功能分支: `git checkout -b feat/xxx`
2. 编写代码和测试
3. 运行 `make lint` 和 `make test`
4. 提交代码: 遵循提交规范
5. 创建 Pull Request
6. 代码审查
7. 合并到主分支

---

## 10. 性能优化建议

### 10.1 数据库优化
- 添加必要的索引
- 使用查询优化（select_related、批量操作）
- 避免 N+1 查询
- 使用数据库连接池

### 10.2 API 优化
- 响应分页
- 字段过滤（只返回需要的字段）
- 缓存常用数据
- 异步处理耗时任务

### 10.3 代码优化
- 使用生成器处理大数据集
- 异步 I/O 操作
- 避免重复计算
- 合理使用缓存

---

## 附录：快速命令参考

```bash
# 安装依赖
pip install -r requirements.txt -r requirements-dev.txt

# 代码格式化
black app/ tests/
ruff check app/ tests/ --fix

# 类型检查
mypy app/

# 运行测试
pytest tests/ -v --cov=app --cov-report=html

# 数据库迁移
alembic revision --autogenerate -m "描述"
alembic upgrade head

# 创建管理员
python scripts/create_superuser.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```