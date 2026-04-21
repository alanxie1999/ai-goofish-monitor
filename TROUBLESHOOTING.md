# 自动下单功能故障排查指南

## 问题原因

自动下单功能代码已提交，但前端没有显示，通常是以下原因：

1. **前端代码未重新编译**
2. **浏览器缓存了旧版本**
3. **生产环境构建未更新**

## 📋 解决步骤

### 方案 1：清除浏览器缓存（推荐首选）

1. 在浏览器中按 `Ctrl+Shift+R` (Windows/Linux) 或 `Cmd+Shift+R` (Mac) 强制刷新
2. 或者：
   - 打开开发者工具 (F12)
   - 右键点击刷新按钮
   - 选择"清空缓存并硬性重新加载"

### 方案 2：重新安装前端依赖并编译

```bash
cd /workspace/web-ui

# 清除依赖和构建缓存
rm -rf node_modules
rm -rf dist
rm -rf .vite

# 重新安装依赖
npm install

# 清理后端静态文件目录
rm -rf /workspace/static/*

# 重新构建
npm run build

# 如果使用 Docker
docker compose up --build -d
```

### 方案 3：检查构建目录

确认前端是否成功构建：

```bash
ls -la /workspace/web-ui/dist/
```

应该包含 `assets/` 目录和各种 JS/CSS 文件。

### 方案 4：检查后端是否正确提供静态文件

查看后端是否从正确目录提供静态文件：

```bash
# 查看静态文件配置
grep -r "static" /workspace/src/app.py | head -5

# 检查静态文件目录
ls -la /workspace/static/
```

## ✅ 验证方式

### 1. 前端验证

打开浏览器开发者工具 (F12)，在 Console 中：

```javascript
// 检查是否包含自动下单的翻译键
console.log(window.__VUE_I18N_GLOBAL__);
```

### 2. API 验证

通过 API 创建任务测试：

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "测试自动下单",
    "keyword": "iPhone",
    "auto_order_enabled": true,
    "auto_order_target_price": "5000",
    "auto_order_action": "generate_link"
  }'
```

查看响应中是否包含自动下单字段。

### 3. 查看任务列表

```bash
curl http://localhost:8000/api/tasks
```

检查任务是否包含 `auto_order_enabled` 等字段。

## 🔍 前端自动下单选项位置

创建任务时，自动下单选项位于：

1. **任务名称**
2. **搜索关键词**
3. **判断模式**
4. **详细需求**
5. **价格范围**
6. **--- 分割线 ---**
7. **🎯 自动下单** ← 在这里！

## 🐛 常见错误

### 错误 1：翻译键缺失
```
Cannot read properties of undefined (reading 'autoOrder')
```
**解决**: 清除浏览器缓存，或检查 `zh-CN-extra.ts` 文件

### 错误 2：组件未定义
```
Unknown custom element: Switch
```
**解决**: 前端依赖未正确安装，运行 `rm -rf node_modules && npm install`

### 错误 3：API 400 错误
```
400 Bad Request: auto_order_enabled
```
**解决**: 后端代码未更新，重启后端服务

## 📝 完整重新部署命令

```bash
# 停止现有服务
docker compose down

# 清理缓存
docker compose rm -f

# 重新构建
cd /workspace
rm -rf web-ui/node_modules web-ui/dist
cd web-ui
npm install
npm run build
cd ..

# 重新拉取代码（如果从 git 拉取）
git pull origin master

# 重新启动
docker compose up --build -d

# 查看日志
docker compose logs -f app
```

## 🧪 快速测试脚本

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/workspace')

# 导入测试
try:
    from src.services.auto_order_service import AutoOrderService
    from src.services.order_link_service import OrderLinkService
    print("✅ 后端服务导入成功")
    
    # 测试服务
    order_service = OrderLinkService()
    link = order_service.generate_order_link("123456", "5000")
    print(f"✅ 订单链接生成：{link}")
    
    auto_service = AutoOrderService()
    is_match, reason = auto_service.check_price_match("4000", "5000", None, None)
    print(f"✅ 价格匹配检测：{is_match}, {reason}")
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
```

运行测试：
```bash
python3 /workspace/test_auto_order.py
```

## 📞 需要帮助？

如果以上方法都不行，请检查：

1. **日志文件**: `/workspace/logs/` 目录
2. **浏览器 Console**: F12 查看前端错误
3. **网络请求**: F12 Network 标签查看 API 响应
