# 闲鱼智能监控系统 - 手动部署指南

适用于无法使用 Docker 的环境，或需要自定义配置的高级用户。

## 📋 目录

- [系统要求](#系统要求)
- [环境准备](#环境准备)
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [启动运行](#启动运行)
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
- Python 3.10+
- Node.js 18+
- Git
- Chromium/Chrome 浏览器

---

## 环境准备

### Ubuntu/Debian 系统

```bash
# 更新软件源
sudo apt update

# 安装 Python 3.10
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 安装其他依赖
sudo apt install -y git curl wget

# 验证安装
python3 --version  # 应为 3.10+
node --version      # 应为 v18+
npm --version
```

### CentOS/RHEL 系统

```bash
# 安装 EPEL 源
sudo yum install -y epel-release

# 安装 Python 3.10
sudo yum install -y python3.10 python3-devel

# 安装 Node.js 18
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# 安装其他依赖
sudo yum install -y git curl wget

# 验证安装
python3 --version
node --version
```

### macOS

```bash
# 使用 Homebrew 安装
brew install python@3.10 nodejs git

# 验证安装
python3 --version
node --version
```

### Windows（WSL）

```bash
# 在 WSL2 中安装 Ubuntu，然后参考 Ubuntu 部分
# 或使用 Python 和 Node.js 的 Windows 安装包
```

---

## 安装步骤

### 步骤 1：克隆项目

```bash
git clone https://github.com/alanxie1999/ai-goofish-monitor.git
cd ai-goofish-monitor
```

### 步骤 2：配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑配置文件
nano .env
```

**必填配置**：
```bash
OPENAI_API_KEY=sk-your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4
WEB_USERNAME=admin
WEB_PASSWORD=your_secure_password
```

### 步骤 3：创建必要的目录

```bash
mkdir -p logs state images jsonl prompts static
```

### 步骤 4：安装后端依赖

```bash
# 创建 Python 虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 升级 pip
pip install --upgrade pip

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 安装 Playwright 系统依赖（需要 sudo）
playwright install-deps chromium
```

### 步骤 5：安装前端依赖

```bash
cd web-ui

# 安装 Node.js 依赖
npm install

# 构建前端
npm run build

# 返回根目录
cd ..
```

### 步骤 6：复制静态文件

```bash
# 前端构建产物复制到静态目录
cp -r web-ui/dist/* static/
```

---

## 配置说明

### 环境配置

编辑 `.env` 文件：

```bash
# ========== AI 模型配置 ==========
OPENAI_API_KEY=sk-your_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# ========== Web 配置 ==========
WEB_USERNAME=admin
WEB_PASSWORD=your_password
SERVER_PORT=8000

# ========== 爬虫配置 ==========
RUN_HEADLESS=true
LOGIN_IS_EDGE=false

# ========== 通知配置（可选）==========
NTFY_TOPIC_URL=https://ntfy.sh/your_topic
TELEGRAM_BOT_TOKEN=your_token
```

### 虚拟环境管理

```bash
# 激活虚拟环境
source venv/bin/activate

# 退出虚拟环境
deactivate

# 查看所有安装的包
pip list

# 更新依赖
pip install -r requirements.txt --upgrade
```

### 前端开发模式

```bash
cd web-ui

# 启动开发服务器（热重载）
npm run dev

# 构建生产版本
npm run build
```

---

## 启动运行

### 方式 1：使用启动脚本（推荐）

```bash
# 赋予执行权限
chmod +x start.sh

# 启动服务
./start.sh
```

### 方式 2：手动启动后端

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 FastAPI 应用
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### 方式 3：使用 nohup 后台运行

```bash
# 激活虚拟环境并后台运行
nohup bash -c 'source venv/bin/activate && python -m uvicorn src.app:app --host 0.0.0.0 --port 8000' > app.log 2>&1 &

# 查看进程
ps aux | grep uvicorn

# 查看日志
tail -f app.log

# 停止服务
pkill -f "uvicorn src.app"
```

### 方式 4：使用 systemd 服务（推荐生产环境）

创建服务文件：
```bash
sudo nano /etc/systemd/system/goofish-monitor.service
```

内容：
```ini
[Unit]
Description=Goofish Monitor Service
After=network.target

[Service]
User=your_user
Group=your_user
WorkingDirectory=/path/to/ai-goofish-monitor
Environment="PATH=/path/to/ai-goofish-monitor/venv/bin"
ExecStart=/path/to/ai-goofish-monitor/venv/bin/python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable goofish-monitor
sudo systemctl start goofish-monitor

# 查看状态
sudo systemctl status goofish-monitor
```

### 访问系统

打开浏览器访问：
```
http://localhost:8000
```

---

## 功能启用

### 自动下单功能

创建任务时配置：

1. 进入「任务管理」
2. 点击「+ 创建新任务」
3. 填写基本信息
4. 展开「自动下单」区域
5. 开启「启用自动下单」
6. 设置目标价格和操作类型

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

创建任务时展开「卖家活跃时间」区域，选择活跃时间范围。

### 通知推送配置

进入「系统设置」→「通知推送」配置各种通知渠道。

---

## 更新升级

### 标准更新流程

```bash
# 1. 进入项目目录
cd /path/to/ai-goofish-monitor

# 2. 停止当前服务
# 如果是前台运行：按 Ctrl+C
# 如果是后台：pkill -f "uvicorn src.app"
# 如果是 systemd：sudo systemctl stop goofish-monitor

# 3. 拉取最新代码
git pull origin master

# 4. 更新依赖
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. 更新前端
cd web-ui
npm install
npm run build
cp -r dist/* ../static/
cd ..

# 6. 清理缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 7. 重新启动
./start.sh
# 或：sudo systemctl start goofish-monitor
```

### 一键更新脚本

创建 `update.sh`：
```bash
#!/bin/bash
set -e

echo "🚀 开始更新..."
git pull origin master
source venv/bin/activate
pip install -r requirements.txt --upgrade
cd web-ui && npm install && npm run build && cp -r dist/* ../static/ && cd ..
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "🎉 更新完成！请重启服务"
echo "   ./start.sh"
```

使用方法：
```bash
chmod +x update.sh
./update.sh
```

### 验证更新

```bash
# 1. 查看版本
git log --oneline -1

# 2. 测试后端
source venv/bin/activate
python3 -c "from src.services.auto_order_service import AutoOrderService; print('✅ 后端正常')"

# 3. 测试前端
ls -la static/index.html
```

---

## 故障排查

### Python 依赖安装失败

**症状**：`pip install -r requirements.txt` 报错

**解决**：
```bash
# 升级 pip
pip install --upgrade pip setuptools wheel

# 清除缓存
pip cache purge

# 重新安装
pip install -r requirements.txt --no-cache-dir
```

### Playwright 安装失败

**症状**：`playwright install chromium` 失败

**解决**：
```bash
# 安装系统依赖
sudo apt install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# 手动下载 Chromium
playwright install chromium
```

### Node.js 依赖安装失败

**症状**：`npm install` 报错

**解决**：
```bash
# 清除缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf web-ui/node_modules
cd web-ui && npm install
```

### 前端构建失败

**症状**：`npm run build` 报错

**解决**：
```bash
cd web-ui

# 清理
rm -rf node_modules dist .vite

# 重新安装
npm install

# 重新构建
npm run build
```

### 后端启动失败

**症状**：`uvicorn src.app:app` 启动报错

**解决**：
```bash
# 检查 Python 版本（需要 3.10+）
python3 --version

# 检查虚拟环境
source venv/bin/activate
which python

# 检查依赖
pip list | grep -E "pydantic|fastapi|uvicorn"

# 查看详细错误
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 2>&1 | tail -50
```

### 端口已被占用

**症状**：`Address already in use`

**解决**：
```bash
# 查看占用端口的进程
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>

# 或修改端口（.env）
SERVER_PORT=8001
```

### 内存不足

**症状**：系统卡顿，OOM Killer 杀死进程

**解决**：
1. 减少并发数：
   ```bash
   # .env 配置
   IMAGE_DOWNLOAD_CONCURRENCY=2
   AI_ANALYSIS_CONCURRENCY=2
   ```

2. 增加 Swap 空间：
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### 查看日志

```bash
# 应用日志
tail -f logs/app.log

# 系统日志
journalctl -u goofish-monitor -f

# Nginx 日志（如有）
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 性能问题

**症状**：响应慢，任务运行时间长

**优化**：
```bash
# 1. 减少搜索页数
# 创建任务时设置 max_pages=1

# 2. 关闭图片分析
# 创建任务时关闭"分析商品图片"

# 3. 使用更快的 AI 模型
OPENAI_MODEL_NAME=gpt-3.5-turbo

# 4. 增加系统资源
# CPU、内存、网络带宽
```

---

## 备份恢复

### 备份数据

```bash
# 创建备份目录
mkdir -p ~/backups/goofish-monitor

# 备份所有数据
tar -czf ~/backups/goofish-monitor/backup_$(date +%Y%m%d).tar.gz \
  logs state images jsonl .env venv

# 只备份关键数据
tar -czf ~/backups/goofish-monitor/backup_minimal.tar.gz \
  state .env
```

### 恢复数据

```bash
# 停止服务
pkill -f "uvicorn src.app"

# 解压备份
cd /path/to/ai-goofish-monitor
tar -xzf ~/backups/goofish-monitor/backup_YYYYMMDD.tar.gz

# 重启服务
./start.sh
```

---

## 安全加固

### 防火墙配置

```bash
# UFW（Ubuntu）
sudo ufw allow 8000/tcp
sudo ufw enable

# Firewalld（CentOS）
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 修改默认密码

```bash
# .env 中设置
WEB_PASSWORD=YourStrongPassword123!
```

### 使用 Nginx 反向代理

安装 Nginx：
```bash
sudo apt install -y nginx
```

配置 Nginx：
```bash
sudo nano /etc/nginx/sites-available/goofish-monitor
```

内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/goofish-monitor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### HTTPS 配置

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 常见问题

**Q: 虚拟环境无法激活？**
A: 检查路径是否正确：`source venv/bin/activate`

**Q: pip 安装权限错误？**
A: 使用 `--break-system-packages` 或重新创建虚拟环境

**Q: 前端页面空白？**
A: 检查 `static/` 目录是否有构建产物

**Q: Playwright 浏览器下载慢？**
A: 使用国内镜像或手动下载

**Q: 如何开机自启？**
A: 使用 systemd 服务（见上方配置）

**Q: 数据太多磁盘满了？**
A: 定期清理 `images/task_images_*` 目录

**Q: 支持 Windows 直接部署吗？**
A: 不推荐，建议使用 WSL2 或 Docker Desktop

---

**需要帮助？**

- 📖 [Docker 部署指南](./DOCKER_INSTALL.md)
- 🐛 [提交 Issue](https://github.com/alanxie1999/ai-goofish-monitor/issues)
- 💬 [讨论区](https://github.com/alanxie1999/ai-goofish-monitor/discussions)
