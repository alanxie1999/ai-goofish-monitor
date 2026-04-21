# Docker 部署更新自动下单功能指南

## 🚨 问题原因

Docker 部署后没有自动下单功能，是因为：
1. **前端构建缓存**: Docker 镜像中的前端代码是旧的
2. **未重新构建镜像**: 代码更新后需要重新构建 Docker 镜像

## ✅ 解决方案（在您的服务器上执行）

### 方法 1: 完整重新构建（推荐）

在您的服务器上执行以下命令：

```bash
# 1. 进入项目目录
cd /path/to/your/project

# 2. 拉取最新代码
git pull origin master

# 3. 停止现有服务
docker compose down

# 4. 删除旧的 Docker 镜像（重要！）
docker rmi $(docker images | grep ai-goofish | awk '{print $3}')

# 5. 清理构建缓存
docker builder prune -f

# 6. 重新构建并启动（--no-cache 确保不使用缓存）
docker compose build --no-cache
docker compose up -d

# 7. 查看日志确认启动成功
docker compose logs -f app
```

### 方法 2: 仅重新构建前端（快速）

如果不想完全重建，可以只重建前端部分：

```bash
# 1. 拉取最新代码
git pull origin master

# 2. 停止服务
docker compose down

# 3. 删除前端构建缓存
docker volume rm $(docker volume ls -q | grep node_modules)

# 4. 重新构建
docker compose build app
docker compose up -d

# 5. 查看日志
docker compose logs -f app
```

### 方法 3: 挂载本地构建（开发环境）

如果您在开发环境，可以挂载本地构建：

```yaml
# docker-compose.yml 中添加或修改
services:
  app:
    volumes:
      - ./web-ui/dist:/app/static:ro
```

然后本地重建前端：

```bash
cd web-ui
npm install
npm run build
cd ..
docker compose restart app
```

## 📝 Docker Compose 配置检查

确保您的 `docker-compose.yml` 包含正确配置：

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      # 添加构建参数
      args:
        - BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    volumes:
      - ./logs:/app/logs
      - ./state:/app/state
      - ./images:/app/images
      - ./jsonl:/app/jsonl
    ports:
      - "8000:8000"
    restart: unless-stopped
```

## 🧪 验证更新

### 1. 检查容器内代码版本

```bash
# 进入容器
docker compose exec app bash

# 检查自动下单服务是否存在
ls -la /app/src/services/auto_order_service.py
ls -la /app/src/services/order_link_service.py

# 检查前端文件
ls -la /app/static/index.html

# 查看文件修改时间
stat /app/src/services/auto_order_service.py
```

### 2. API 测试

```bash
# 在宿主机测试
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "测试",
    "keyword": "test",
    "auto_order_enabled": true,
    "auto_order_target_price": "1000"
  }'
```

### 3. 前端验证

打开浏览器访问 `http://your-server:8000`，按 `Ctrl+Shift+R` 强制刷新，然后：

1. 创建新任务
2. 滚动到"价格范围"下方
3. 应该看到"🎯 自动下单"选项

## 🐛 常见问题

### Q1: 前端页面还是旧的
**A**: 清除浏览器缓存（Ctrl+Shift+R），或者检查 Docker 镜像是否正确更新：

```bash
docker images | grep ai-goofish
docker compose ps
```

### Q2: 容器启动失败
**A**: 查看详细错误日志：

```bash
docker compose logs app --tail=100
```

### Q3: 自动下单服务导入失败
**A**: 检查容器内的文件：

```bash
docker compose exec app ls -la /app/src/services/
```

应该包含：
- `auto_order_service.py`
- `order_link_service.py`
- `seller_active_service.py`

### Q4: 数据库错误
**A**: 自动下单功能的字段是存储在 JSON 中的，不需要数据库迁移。如果遇到数据库错误，检查：

```bash
docker compose exec app python3 -c "from src.domain.models.task import Task; print('OK')"
```

## 📊 完整更新脚本

创建一个更新脚本 `/workspace/update.sh`：

```bash
#!/bin/bash
set -e

echo "🚀 开始更新..."

# 1. 拉取最新代码
echo "📦 拉取代码..."
git pull origin master

# 2. 停止服务
echo "⏹️  停止服务..."
docker compose down

# 3. 清理旧镜像
echo "🧹 清理旧镜像..."
docker rmi $(docker images | grep ai-goofish-monitor) || true
docker builder prune -f

# 4. 重新构建
echo "🔨 重新构建镜像..."
docker compose build --no-cache

# 5. 启动服务
echo "🚀 启动服务..."
docker compose up -d

# 6. 等待启动
echo "⏳ 等待服务启动..."
sleep 10

# 7. 检查状态
echo "✅ 检查服务状态..."
docker compose ps
docker compose logs --tail=20 app

echo "🎉 更新完成！"
echo "请使用 Ctrl+Shift+R 强制刷新浏览器"
```

使用方法：

```bash
chmod +x /workspace/update.sh
./update.sh
```

## 🔍 调试技巧

### 查看容器内文件

```bash
# 查看任务模型
docker compose exec app head -50 /app/src/domain/models/task.py | grep -A 5 auto_order

# 查看前端文件
docker compose exec app grep -r "autoOrder" /app/static/ || echo "未找到（可能前端未构建）"

# 查看实际运行的代码
docker compose exec app python3 -c "
import sys
sys.path.insert(0, '/app')
from src.services.auto_order_service import AutoOrderService
print('✅ 自动下单服务加载成功')
"
```

### 热重载开发模式

如果需要在开发环境测试，可以启用热重载：

```yaml
# docker-compose.dev.yml
services:
  app:
    command: uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
```

然后运行：

```bash
docker compose -f docker-compose.dev.yml up
```

## 📞 需要帮助？

如果更新后还是不行，请提供以下信息：

1. `docker compose ps` 的输出
2. `docker compose logs app --tail=50` 的日志
3. 浏览器 Console 的错误截图
4. `docker images | grep ai-goofish` 的输出

