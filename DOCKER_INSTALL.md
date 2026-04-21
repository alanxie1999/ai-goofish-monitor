# 闲鱼智能监控系统 - Docker 部署指南

**推荐使用 Docker 部署** - 最简单、最可靠的部署方式，无需配置复杂的环境依赖。

## 📋 目录

- [系统要求](#系统要求)
- [快速安装](#快速安装)
- [配置说明](#配置说明)
- [功能启用](#功能启用)
- [更新升级](#更新升级)
- [故障排查](#故障排查)

---

## 系统要求

### 硬件要求
- **CPU**: 2 核心及以上
- **内存**: 4GB RAM 及以上（推荐 8GB）
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- Docker 20.10+
- Docker Compose 2.0+
- Git

---

## 快速安装

### 步骤 1：克隆项目

```bash
git clone https://github.com/alanxie1999/ai-goofish-monitor.git
cd ai-goofish-monitor
```

### 步骤 2：配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑配置文件（推荐使用 nano 或 vim）
nano .env
```

**必填配置**：
```bash
# ========== AI 模型配置（必填）==========
OPENAI_API_KEY=sk-your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# ========== Web 访问配置（可选）==========
WEB_USERNAME=admin
WEB_PASSWORD=your_secure_password
SERVER_PORT=8000
```

**可选配置**（通知推送）：
```bash
# Ntfy 通知（推荐，最简单）
NTFY_TOPIC_URL=https://ntfy.sh/your_topic_name

# Telegram 通知
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 企业微信通知
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key
```

### 步骤 3：一键启动

```bash
# 构建并启动（首次需要 5-10 分钟）
docker compose up --build -d

# 查看启动日志
docker compose logs -f app

# 检查服务状态
docker compose ps
```

**预期输出**：
```
NAME                STATUS              PORTS
ai-goofish-monitor-app   Up (healthy)   0.0.0.0:8000->8000/tcp
```

### 步骤 4：访问系统

打开浏览器访问：
```
http://localhost:8000
```

使用 `.env` 中配置的用户名密码登录（默认：admin / 您设置的密码）。

---

## 配置说明

### 环境配置文件

所有配置都在 `.env` 文件中，常用配置项：

#### AI 模型配置
```bash
# OpenAI GPT-4
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# 或使用其他兼容模型
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat
```

#### 账号轮换配置
```bash
# 启用账号轮换
ACCOUNT_ROTATION_ENABLED=true
ACCOUNT_ROTATION_MODE=per_task
ACCOUNT_STATE_DIR=state
```

#### 性能优化配置
```bash
# 降低并发（内存不足时）
IMAGE_DOWNLOAD_CONCURRENCY=2
AI_ANALYSIS_CONCURRENCY=2

# 调试模式
AI_DEBUG_MODE=false
RUN_HEADLESS=true
```

#### 数据存储路径
```bash
# 默认路径（挂载到 Docker 容器）
./logs:/app/logs         # 日志文件
./state:/app/state       # 登录状态
./images:/app/images     # 商品图片
./jsonl:/app/jsonl       # 结果数据
```

### Docker Compose 配置

默认的 `docker-compose.yml`：

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./logs:/app/logs
      - ./state:/app/state
      - ./images:/app/images
      - ./jsonl:/app/jsonl
    ports:
      - "8000:8000"
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
```

---

## 功能启用

### 自动下单功能

创建任务时配置：

1. 进入「任务管理」
2. 点击「+ 创建新任务」
3. 填写基本信息（任务名称、关键词等）
4. 展开「自动下单」区域
5. 开启「启用自动下单」
6. 设置目标价格（如：5000）
7. 选择操作类型：
   - **仅通知**：价格匹配时只发送通知
   - **生成下单链接**：生成可直接跳转的订单链接（推荐）
   - **自动购买**：实验性功能（暂未完全实现）

**API 方式**：
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "iPhone 监控",
    "keyword": "iPhone 15",
    "auto_order_enabled": true,
    "auto_order_target_price": "5000",
    "auto_order_action": "generate_link"
  }'
```

### 卖家活跃时间筛选

用途：筛选最近活跃的卖家，提高沟通效率。

1. 创建任务时展开「卖家活跃时间」区域
2. 选择活跃时间范围：
   - 不限（默认）
   - 1 小时内活跃 🔥
   - 24 小时内活跃 ✅
   - 3 天内活跃 ⏳
   - 7 天内活跃 💤

### 通知推送配置

进入「系统设置」→「通知推送」：

#### Ntfy（推荐）
最简单，无需 API Key：
```bash
NTFY_TOPIC_URL=https://ntfy.sh/your_topic_name
```

#### Telegram
需要 Bot Token 和 Chat ID：
```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=987654321
```

#### 企业微信
需要 Webhook URL：
```bash
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
```

---

## 更新升级

### 标准更新流程

```bash
# 1. 进入项目目录
cd /path/to/ai-goofish-monitor

# 2. 拉取最新代码
git pull origin master

# 3. 停止当前服务
docker compose down

# 4. 删除旧镜像（重要！）
docker rmi $(docker images | grep ai-goofish-monitor | awk '{print $3}') || true

# 5. 清理构建缓存
docker builder prune -f

# 6. 重新构建镜像（必须使用 --no-cache）
docker compose build --no-cache

# 7. 启动服务
docker compose up -d

# 8. 查看启动日志
docker compose logs -f app
```

### 一键更新脚本

创建 `update.sh`：
```bash
#!/bin/bash
set -e

echo "🚀 开始更新..."
git pull origin master
docker compose down
docker rmi $(docker images | grep ai-goofish-monitor | awk '{print $3}') || true
docker builder prune -f
docker compose build --no-cache
docker compose up -d
sleep 10
docker compose logs --tail=30 app
echo "🎉 更新完成！请使用 Ctrl+Shift+R 刷新浏览器"
```

使用方法：
```bash
chmod +x update.sh
./update.sh
```

### 验证更新

1. **查看版本**：
   ```bash
   docker compose exec app git log --oneline -1
   ```

2. **检查新功能**：
   - 访问 http://localhost:8000
   - 按 **Ctrl+Shift+R** 强制刷新
   - 创建任务时查看是否有新功能选项

3. **API 测试**：
   ```bash
   curl http://localhost:8000/api/tasks | jq .
   ```

---

## 故障排查

### 容器无法启动

**症状**：`docker compose ps` 显示容器退出

**解决**：
```bash
# 查看详细错误
docker compose logs app --tail=100

# 检查配置文件
docker compose exec app cat .env

# 测试 AI 连接
docker compose exec app python3 -c "from src.config import client; print('OK')"
```

### 前端无法访问

**症状**：浏览器显示空白页或 404

**解决**：
```bash
# 检查静态文件
docker compose exec app ls -la /app/static/

# 重新构建前端
docker compose down
docker compose build --no-cache
docker compose up -d
```

### 自动下单功能不显示

**症状**：创建任务时看不到「自动下单」选项

**解决**：
1. **清除浏览器缓存**：按 `Ctrl+Shift+R`
2. **检查镜像版本**：
   ```bash
   docker compose exec app ls -la src/services/auto_order_service.py
   ```
3. **重新构建**：
   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

### 内存占用过高

**症状**：服务器内存占用超过 80%

**解决**：
```bash
# 1. 限制并发数（.env 配置）
IMAGE_DOWNLOAD_CONCURRENCY=2
AI_ANALYSIS_CONCURRENCY=2

# 2. 清理图片缓存
docker compose exec app bash -c "rm -rf images/task_images_*"

# 3. 重启服务
docker compose restart
```

### 登录状态失效

**症状**：任务运行失败，提示需要登录

**解决**：
```bash
# 1. 重新提取 Cookie（使用 Chrome 扩展）

# 2. 更新账号
# 进入「账号管理」→ 更新对应账号

# 3. 查看失败日志
docker compose logs app | grep "登录"
```

### 查看日志

```bash
# 实时日志
docker compose logs -f app

# 最近 100 行
docker compose logs app --tail=100

# 特定时间段
docker compose logs app --since="2024-01-20 10:00:00" --until="2024-01-20 12:00:00"

# 进入容器查看
docker compose exec app bash
cat logs/app.log
```

### 进入容器调试

```bash
# 进入容器
docker compose exec app bash

# 检查 Python 环境
python3 --version
pip list | grep -i requirement

# 检查服务
ls -la src/services/

# 测试功能
python3 -c "
from src.services.auto_order_service import AutoOrderService
print('✅ 自动下单服务正常')
"

# 退出容器
exit
```

### 备份和恢复

**备份**：
```bash
# 备份所有数据
tar -czf backup_$(date +%Y%m%d).tar.gz logs state images jsonl .env

# 只备份重要数据
tar -czf backup_minimal.tar.gz state .env
```

**恢复**：
```bash
# 停止服务
docker compose down

# 解压备份
tar -xzf backup_YYYYMMDD.tar.gz

# 启动服务
docker compose up -d
```

---

## 性能优化

### 降低内存占用

编辑 `.env`：
```bash
# 减少并发
IMAGE_DOWNLOAD_CONCURRENCY=2
AI_ANALYSIS_CONCURRENCY=2

# 限制页面数
DEFAULT_MAX_PAGES=1
```

### 提高运行速度

```bash
# 增加并发（内存充足时）
IMAGE_DOWNLOAD_CONCURRENCY=5
AI_ANALYSIS_CONCURRENCY=3

# 使用更快的模型
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

### 多账号轮换

```bash
# .env 配置
ACCOUNT_ROTATION_ENABLED=true
ACCOUNT_ROTATION_MODE=per_task
ACCOUNT_STATE_DIR=state

# 在「账号管理」中添加多个账号
```

---

## 安全建议

### 修改默认密码

```bash
# .env 中设置强密码
WEB_PASSWORD=YourSecurePassword123!
```

### 限制访问 IP

```yaml
# docker-compose.yml 中添加
services:
  app:
    ports:
      - "127.0.0.1:8000:8000"  # 只允许本地访问
```

配合 Nginx 反向代理：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        allow 192.168.1.0/24;  # 只允许内网
        deny all;
    }
}
```

### HTTPS 配置

使用 Nginx + Let's Encrypt：
```bash
sudo certbot --nginx -d your-domain.com
```

---

## 常见问题

**Q: Docker 镜像很大，有办法减小吗？**
A: 可以使用精简版 Dockerfile，或定期清理未使用的镜像：
```bash
docker system prune -a
```

**Q: 可以在 Windows 上部署吗？**
A: 可以！Docker Desktop for Windows 完全支持，步骤相同。

**Q: 多用户支持？**
A: 当前版本只支持单用户，多用户功能在开发中。

**Q: 数据存在哪里？**
A: 数据挂载在宿主机目录：`./logs`, `./state`, `./images`, `./jsonl`

**Q: 如何完全卸载？**
A:
```bash
docker compose down -v
docker rmi $(docker images | grep ai-goofish-monitor)
rm -rf logs state images jsonl
```

---

**需要帮助？**

- 📖 [完整文档](./INSTALLATION.md)
- 🐛 [提交 Issue](https://github.com/alanxie1999/ai-goofish-monitor/issues)
- 💬 [讨论区](https://github.com/alanxie1999/ai-goofish-monitor/discussions)
