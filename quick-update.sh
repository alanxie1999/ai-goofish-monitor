#!/bin/bash
set -e

echo "============================================================"
echo "🚀 Docker 快速更新指南 - 自动下单功能"
echo "============================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}⚠️  请在您的部署服务器上依次执行以下命令：${NC}"
echo ""
echo "============================================================"
echo "步骤 1: 拉取最新代码"
echo "============================================================"
echo "cd /your/project/path"
echo "git pull origin master"
echo ""
echo "============================================================"
echo "步骤 2: 停止服务并清理"
echo "============================================================"
echo "docker compose down"
echo "docker rmi \$(docker images | grep ai-goofish-monitor | awk '{print \$3}') || true"
echo "docker builder prune -f"
echo ""
echo "============================================================"
echo "步骤 3: 重新构建并启动（重要：--no-cache）"
echo "============================================================"
echo "docker compose build --no-cache"
echo "docker compose up -d"
echo ""
echo "============================================================"
echo "步骤 4: 查看日志确认启动成功"
echo "============================================================"
echo "docker compose logs -f app"
echo ""
echo "============================================================"
echo "步骤 5: 强制刷新浏览器"
echo "============================================================"
echo -e "${YELLOW}访问 http://your-server:8000${NC}"
echo "按 ${GREEN}Ctrl+Shift+R${NC} 强制刷新浏览器"
echo ""
echo "============================================================"
echo "验证功能"
echo "============================================================"
echo "1. 创建新任务"
echo "2. 滚动到「价格范围」下方"
echo "3. 应该看到「🎯 自动下单」选项"
echo ""
echo "============================================================"
echo -e "${YELLOW}📋 完整的一条命令版本：${NC}"
echo "============================================================"
cat << 'COMMAND'
cd /your/project/path && \
git pull origin master && \
docker compose down && \
docker rmi $(docker images | grep ai-goofish-monitor | awk '{print $3}') || true && \
docker builder prune -f && \
docker compose build --no-cache && \
docker compose up -d && \
docker compose logs --tail=30 app
COMMAND
echo ""
echo "============================================================"
echo "💡 提示：创建自动更新脚本"
echo "============================================================"
cat > /tmp/update-auto-order.sh << 'SCRIPT'
#!/bin/bash
set -e
echo "🚀 开始更新..."
cd /your/project/path
git pull origin master
docker compose down
docker rmi $(docker images | grep ai-goofish-monitor | awk '{print $3}') || true
docker builder prune -f
docker compose build --no-cache
docker compose up -d
sleep 10
docker compose ps
docker compose logs --tail=20 app
echo "🎉 更新完成！请使用 Ctrl+Shift+R 刷新浏览器"
SCRIPT

echo "将上面的内容保存为 /your/project/path/update.sh"
echo "然后执行：chmod +x update.sh && ./update.sh"
echo "============================================================"
echo ""
echo -e "${GREEN}✅ 祝您使用愉快！${NC}"
