# 🚀 Supabase 数据库配置指南

## 📋 概述

本项目已配置为使用 Supabase 作为后端数据库服务。Supabase 提供了 PostgreSQL 数据库、实时订阅、用户认证和文件存储等功能。

## 🔧 配置步骤

### 1. 创建 Supabase 项目

1. 访问 [Supabase](https://supabase.com)
2. 注册/登录账户
3. 点击 "New Project" 创建新项目
4. 填写项目信息：
   - **Name**: `mini-blog` (或你喜欢的名称)
   - **Database Password**: 设置一个强密码（记住这个密码）
   - **Region**: 选择离你最近的区域

### 2. 获取配置信息

创建项目后，在项目仪表板中：

1. 进入 **Settings** → **API**
2. 复制以下信息：
   - **Project URL** (SUPABASE_URL)
   - **anon public** key (SUPABASE_KEY)

3. 进入 **Settings** → **Database**
4. 复制 **Connection string** 中的信息：
   - **Host**: `db.[your-project-ref].supabase.co`
   - **Database name**: `postgres`
   - **Port**: `5432`
   - **User**: `postgres`
   - **Password**: 你设置的数据库密码

### 3. 配置环境变量

编辑项目根目录下的 `.env` 文件：

```bash
# 替换为你的实际值
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
```

### 4. 安装依赖

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 5. 测试连接

启动应用测试连接：

```bash
uvicorn app.main:app --reload
```

如果配置正确，你应该看到：
```
INFO: 数据库引擎创建成功
INFO: Supabase 客户端创建成功
INFO: Supabase 初始化成功
INFO: 应用启动成功，Supabase 已初始化
```

## 🗄️ 数据库迁移

### 使用 Alembic 进行数据库迁移

1. **初始化 Alembic**（如果还没有）：
```bash
alembic init alembic
```

2. **创建迁移文件**：
```bash
alembic revision --autogenerate -m "Initial migration"
```

3. **执行迁移**：
```bash
alembic upgrade head
```

## 🔐 安全注意事项

1. **不要提交 `.env` 文件到版本控制**
2. **在生产环境中使用强密码**
3. **定期轮换 API 密钥**
4. **启用 Row Level Security (RLS)**

## 📚 常用 Supabase 功能

### 1. 用户认证
```python
from app.core.supabase import get_supabase_client

supabase = get_supabase_client()

# 用户注册
user = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "password123"
})

# 用户登录
user = supabase.auth.sign_in_with_password({
    "email": "user@example.com", 
    "password": "password123"
})
```

### 2. 数据库操作
```python
# 插入数据
result = supabase.table('posts').insert({
    "title": "My Post",
    "content": "Post content"
}).execute()

# 查询数据
posts = supabase.table('posts').select("*").execute()

# 更新数据
result = supabase.table('posts').update({
    "title": "Updated Title"
}).eq('id', 1).execute()
```

### 3. 实时订阅
```python
# 订阅表变化
def handle_changes(payload):
    print(f"Table changed: {payload}")

supabase.table('posts').on('INSERT', handle_changes).subscribe()
```

## 🆘 故障排除

### 常见问题

1. **连接失败**
   - 检查 `.env` 文件中的配置是否正确
   - 确认 Supabase 项目是否正常运行
   - 检查网络连接

2. **认证失败**
   - 确认 SUPABASE_KEY 是否正确
   - 检查项目是否已激活

3. **数据库连接失败**
   - 确认 DATABASE_URL 格式正确
   - 检查数据库密码是否正确
   - 确认数据库是否已创建

### 获取帮助

- [Supabase 官方文档](https://supabase.com/docs)
- [Supabase Python 客户端文档](https://github.com/supabase/supabase-py)
- [FastAPI 文档](https://fastapi.tiangolo.com/)

## 🎉 完成！

配置完成后，你就可以开始使用 Supabase 的所有功能了！记得在开发过程中定期备份数据库。
