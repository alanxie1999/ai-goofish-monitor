# 闲鱼智能监控系统 - 安装部署指南

本文档提供详细的安装、部署和更新说明，支持 Docker 和手动部署两种方式。

## 📋 目录

- [系统要求](#系统要求)
- [快速开始（Docker 推荐）](#快速开始 docker 推荐)
- [手动部署](#手动部署)
- [功能配置](#功能配置)
- [更新说明](#更新说明)
- [故障排查](#故障排查)
- [常见问题](#常见问题)

---

## 系统要求

### 硬件要求
- **CPU**: 2 核心及以上
- **内存**: 4GB RAM 及以上（推荐 8GB）
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接

### 软件要求

#### Docker 部署（推荐）
- Docker 20.10+
- Docker Compose 2.0+
- Git

#### 手动部署
- Python 3.10+
- Node.js 18+
- Git
- Chromium/Chrome 浏览器（用于 Playwright）

---

## 快速开始（Docker 推荐）

### 1. 克隆项目

```bash
git clone https://github.com/alanxie1999/ai-goofish-monitor.git
cd ai-goofish-monitor
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入必要配置
nano .env
```

**必填配置项**：
```bash
# AI 模型配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# Web 访问配置
WEB_USERNAME=admin
WEB_PASSWORD=your_secure_password
SERVER_PORT=8000
```

### 3. 启动 Docker 服务

```bash
# 构建并启动（首次启动需要较长时间）
docker compose up --build -d

# 查看启动日志
docker compose logs -f app

# 检查服务状态
docker compose ps
```

### 4. 访问系统

打开浏览器访问：
```
http://localhost:8000
```

使用 `.env` 中配置的用户名密码登录。

### 5. 初始化配置

首次使用需要：

1. **配置通知推送**（可选）
   - 进入「系统设置」→「通知推送」
   - 配置 Ntfy、Telegram、企业微信等

2. **添加账号**（可选）
   - 进入「账号管理」
   - 使用 Chrome 扩展提取闲鱼登录状态

3. **创建监控任务**
   - 进入「任务管理」
   - 点击「+ 创建新任务」
   - 填写任务名称、搜索关键词、详细需求等

---

## 手动部署

### 1. 系统依赖安装

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip nodejs npm git curl
```

#### CentOS/RHEL
```bash
sudo yum install -y python3.10 python3-devel nodejs npm git curl
```

#### macOS
```bash
brew install python@3.10 nodejs git
```

### 2. 克隆项目

```bash
git clone https://github.com/alanxie1999/ai-goofish-monitor.git
cd ai-goofish-monitor
```

### 3. 安装后端依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 4. 安装前端依赖

```bash
cd web-ui
npm install
npm run build
cd ..
```

### 5. 配置环境变量

```bash
cp .env.example .env
nano .env
```

编辑必要配置（参考 Docker 部署部分）。

### 6. 创建必要目录

```bash
mkdir -p logs state images jsonl prompts static
```

### 7. 启动服务

#### 方式 1：直接启动
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动后端
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

#### 方式 2：使用启动脚本
```bash
chmod +x start.sh
./start.sh
```

### 8. 访问系统

打开浏览器访问：
```
http://localhost:8000
```

---

## 功能配置

### 通知推送配置

系统支持多种通知方式：

#### Ntfy（推荐）
```bash
NTFY_TOPIC_URL=https://ntfy.sh/your_topic_name
```

#### Telegram
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

#### 企业微信
```bash
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key
```

#### Bark（iOS）
```bash
BARK_URL=https://api.day.app/your_device_key/
```

### 自动下单功能配置

**创建任务时启用**：

1. 创建新任务
2. 展开「自动下单」区域
3. 开启「启用自动下单」
4. 设置目标价格（如：5000）
5. 选择操作类型：
   - **仅通知**：价格匹配时只发送通知
   - **生成下单链接**：生成可直接跳转的订单链接
   - **自动购买**：实验性功能

**API 方式**：
```json
{
  "task_name": "iPhone 监控",
  "keyword": "iPhone 15",
  "auto_order_enabled": true,
  "auto_order_target_price": "5000",
  "auto_order_action": "generate_link"
}
```

### 卖家活跃时间筛选

**创建任务时设置**：

1. 展开「卖家活跃时间」区域
2. 选择活跃时间范围：
   - 不限（默认）
   - 1 小时内活跃
   - 24 小时内活跃
   - 3 天内活跃
   - 7 天内活跃

### 任务定时配置

支持 Cron 表达式和预设值：

**预设值**：
- 每 5 分钟：`*/5 * * * *`
- 每 15 分钟：`*/15 * * * *`
- 每小时：`0 * * * *`
- 每天 8 点：`0 8 * * *`

**自定义**：
```bash
# 每小时第 30 分钟
30 * * * *

# 每周一 9 点
0 9 * * 1

# 每天 8 点、12 点、18 点
0 8,12,18 * * *
```

---

## 更新说明

### Docker 部署更新

```bash
# 1. 进入项目目录
cd /path/to/project

# 2. 拉取最新代码
git pull origin master

# 3. 停止服务
docker compose down

# 4. 清理旧镜像（重要！）
docker rmi $(docker images | grep ai-goofish-monitor | awk '{print $3}') || true
docker builder prune -f

# 5. 重新构建（使用 --no-cache）
docker compose build --no-cache
docker compose up -d

# 6. 查看日志
docker compose logs -f app

# 7. 强制刷新浏览器
# 访问 http://localhost:8000 按 Ctrl+Shift+R
```

### 手动部署更新

```bash
# 1. 拉取代码
cd /path/to/project
git pull origin master

# 2. 更新后端依赖
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 3. 更新前端
cd web-ui
npm install
npm run build
cd ..

# 4. 重启服务
# 停止当前运行的服务（Ctrl+C）
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### 新功能：自动下单和卖家活跃时间

最新版本（`master` 分支）包含：

- ✅ **自动下单功能**：价格匹配时生成下单链接
- ✅ **卖家活跃时间检测**：筛选最近活跃的卖家
- ✅ **智能格式化**：刚刚/X 分钟/X 小时前
- ✅ **活跃等级评估**：非常活跃/活跃/一般/不活跃

更新后请强制刷新浏览器（Ctrl+Shift+R）。

---

## 故障排查

### 后端启动失败

**症状**：`docker compose logs`显示错误

**解决**：
```bash
# 查看详细错误
docker compose logs app --tail=100

# 检查环境变量
docker compose exec app env | grep OPENAI

# 测试 AI 连接
docker compose exec app python3 -c "from src.config import client; print('OK')"
```

### 前端无法访问

**症状**：浏览器显示空白页或 404

**解决**：
```bash
# 检查静态文件
ls -la /app/static/  # Docker 内
ls -la web-ui/dist/  # 本地

# 重新构建前端
cd web-ui && npm install && npm run build
cd .. && docker compose restart app
```

### 自动下单功能不显示

**症状**：创建任务时看不到「自动下单」选项

**解决**：
1. **清除浏览器缓存**：`Ctrl+Shift+R`
2. **重新构建镜像**：`docker compose build --no-cache`
3. **检查代码版本**：
   ```bash
   docker compose exec app ls -la src/services/auto_order_service.py
   ```

### 卖家活跃时间为"未知"

**症状**：卖家信息中活跃时间显示"未知"

**说明**：
- 不是所有卖家都有活跃时间数据
- 取决于闲鱼 API 返回
- 部分卖家隐藏了活跃状态

**解决**：这是正常现象，不影响其他功能。

### 登录状态失效

**症状**：任务运行失败，提示需要登录

**解决**：
```bash
# 1. 重新提取 Cookie
# 使用 Chrome 扩展重新提取

# 2. 更新账号
# 进入「账号管理」→ 更新对应账号

# 3. 查看失败日志
docker compose logs app | grep "登录"
```

### 内存占用过高

**症状**：系统内存占用超过 80%

**解决**：
```bash
# 1. 限制并发数
# 在 .env 中添加：
IMAGE_DOWNLOAD_CONCURRENCY=2
AI_ANALYSIS_CONCURRENCY=2

# 2. 定期清理图片
docker compose exec app bash
rm -rf images/task_images_*
exit

# 3. 重启服务
docker compose restart
```

---

## 常见问题

### Q1: 支持哪些 AI 模型？
**A**: 支持所有 OpenAI 兼容的模型：
- GPT-4 / GPT-3.5
- Claude（通过代理）
- 文心一言、通义千问等国产模型

配置示例：
```bash
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat
```

### Q2: 一个账号可以运行几个任务？
**A**: 建议一个账号同时运行不超过 3 个任务。多账号可启用账号轮换：
```bash
# .env 配置
ACCOUNT_ROTATION_ENABLED=true
ACCOUNT_ROTATION_MODE=per_task
```

### Q3: 自动下单是全自动吗？
**A**: 当前是**半自动**模式：
- ✅ 自动生成下单链接
- ✅ 自动推送通知
- ❌ 需要手动点击链接确认支付（安全考虑）

### Q4: 支持 Windows 部署吗？
**A**: 支持！Docker 部署在所有平台都一样：
```powershell
# PowerShell
git clone <repo>
cd ai-goofish-monitor
docker compose up --build -d
```

### Q5: 如何备份数据？
**A**: 备份以下目录：
```bash
# 需要备份的目录
- logs/        # 运行日志
- state/       # 登录状态
- images/      # 商品图片
- jsonl/       # 结果数据
- .env         # 配置文件（敏感！）

# 备份命令
tar -czf backup_$(date +%Y%m%d).tar.gz logs state images jsonl .env
```

### Q6: 迁移服务器怎么做？
**A**: 
```bash
# 1. 备份
tar -czf backup.tar.gz logs state images jsonl .env

# 2. 新服务器安装 Docker
curl -fsSL https://get.docker.com | sh

# 3. 克隆项目
git clone <repo>
cd ai-goofish-monitor

# 4. 恢复数据
tar -xzf backup.tar.gz

# 5. 启动
docker compose up --build -d
```

### Q7: 如何查看运行日志？
**A**:
```bash
# Docker 部署
docker compose logs -f app

# 手动部署
tail -f logs/app.log

# 查看特定任务日志
docker compose exec app bash
cat logs/task_*.log
```

### Q8: 支持多用户吗？
**A**: 当前版本只支持单用户（admin）。多用户功能在开发中。

### Q9: 任务运行很慢怎么办？
**A**:
```bash
# 1. 减少搜索页数
# 创建任务时设置 max_pages=1

# 2. 关闭图片分析
# 创建任务时关闭"分析商品图片"

# 3. 使用更快的 AI 模型
OPENAI_MODEL_NAME=gpt-3.5-turbo

# 4. 添加更多账号轮换
# 在「账号管理」中添加多个账号
```

### Q10: 如何反馈问题或建议？
**A**: 
- 📧 GitHub Issues: https://github.com/alanxie1999/ai-goofish-monitor/issues
- 💬 Discussions: https://github.com/alanxie1999/ai-goofish-monitor/discussions

---

## 技术支持

### 文档资源
- 📖 [自动下单功能文档](./AUTO_ORDER_FEATURE.md)
- 📖 [卖家活跃时间文档](./SELLER_ACTIVE_FEATURE.md)
- 📖 [Pull Request 详情](./PR_DESCRIPTION.md)

### 社区支持
- GitHub Issues: 报告 Bug 和请求功能
- GitHub Discussions: 交流使用经验

### 开发进度
- 最新功能在 `master` 分支
- 开发中功能在 `dev` 分支
- 定期发布 Release 版本

---

## 更新日志

### v1.2.0（最新版）
- ✨ 新增自动下单功能
- ✨ 新增卖家活跃时间检测
- ✨ 支持活跃等级评估
- ✨ 前台筛选功能增强
- 🐛 修复已知问题

### v1.1.0
- ✨ 新增账号轮换功能
- ✨ 新增 IP 代理支持
- ✨ 优化 AI 分析性能

### v1.0.0
- 🎉 首次发布
- ✨ 基础监控功能
- ✨ AI 智能分析
- ✨ 多渠道通知推送

---

**祝您使用愉快！** 🎉

如有问题，请查阅本文档或提交 Issue。
