# FastAPI Mini Blog

一个使用 FastAPI 构建的轻量级博客系统，适合学习和实战练习。

## ✨ 功能特性

- 🔐 用户认证系统（JWT）
- 📝 文章 CRUD 操作
- 🏷️ 文章分类和标签
- 💬 评论系统
- 📄 分页和搜索
- 📚 自动生成的 API 文档

## 🛠️ 技术栈

- **FastAPI** - 现代、高性能的 Web 框架
- **SQLAlchemy** - ORM 数据库工具
- **PostgreSQL** - 数据库
- **Pydantic** - 数据验证
- **Alembic** - 数据库迁移
- **JWT** - 身份认证

## 📋 环境要求

- Python 3.8+
- PostgreSQL 12+ (或 SQLite 用于开发)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/fastapi-mini-blog.git
cd fastapi-mini-blog
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows 用户: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

### 5. 初始化数据库

```bash
alembic upgrade head
```

### 6. 运行项目

```bash
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档

## 📁 项目结构

```
fastapi-mini-blog/
├── app/
│   ├── api/          # API 路由
│   ├── core/         # 核心功能（安全、配置等）
│   ├── models/       # 数据库模型
│   ├── schemas/      # Pydantic 模型
│   ├── database.py   # 数据库连接
│   └── main.py       # 应用入口
├── alembic/          # 数据库迁移文件
├── tests/            # 测试文件
└── requirements.txt  # 项目依赖
```

## 🔑 API 端点

### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录

### 文章
- `GET /api/v1/posts` - 获取文章列表
- `GET /api/v1/posts/{id}` - 获取文章详情
- `POST /api/v1/posts` - 创建文章
- `PUT /api/v1/posts/{id}` - 更新文章
- `DELETE /api/v1/posts/{id}` - 删除文章

### 用户
- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me` - 更新用户信息

## 🧪 运行测试

```bash
pytest
```

## 📝 开发计划

- [x] 项目初始化
- [ ] 用户认证系统
- [ ] 文章 CRUD
- [ ] 评论系统
- [ ] 文章搜索
- [ ] 图片上传
- [ ] 前端界面（可选）

## 📄 许可证

MIT License

## 👤 作者

SHIZAI

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！