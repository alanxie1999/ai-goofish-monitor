# Pull Request: 自动下单和卖家活跃时间检测功能

## 📋 变更概述

本次 PR 包含两个主要功能的实现：

1. **自动下单功能** - 当商品价格匹配设定条件时自动生成下单链接并推送通知
2. **卖家活跃时间检测** - 检测卖家上线时间并提供前台筛选功能

---

## ✨ 功能 1: 自动下单功能

### 功能描述
当搜索到符合指定价格的商品后，系统可以自动生成下单链接并推送通知，实现半自动化的商品监控和购买流程。

### 主要特性
- ✅ 价格匹配检测（支持目标价格和价格区间）
- ✅ 自动生成 PC 端和移动端下单链接
- ✅ 下单链接直接跳转到闲鱼订单确认页
- ✅ 下单信息附加到通知推送中
- ✅ 支持所有已配置的通知渠道
- ✅ 三种操作模式：仅通知/生成链接/自动购买（实验性）

### 技术实现
**新增文件:**
- `src/services/order_link_service.py` - 订单链接生成服务
- `src/services/auto_order_service.py` - 自动下单核心逻辑
- `tests/test_auto_order.py` - 单元测试

**修改文件:**
- `src/domain/models/task.py` - 扩展任务模型（+3 个字段）
- `src/services/item_analysis_dispatcher.py` - 集成自动下单检查
- `src/scraper.py` - 初始化自动下单服务
- `web-ui/src/components/tasks/TaskForm.vue` - 添加配置 UI
- `web-ui/src/i18n/messages/zh-CN-extra.ts` - 翻译支持

**任务模型新增字段:**
```python
auto_order_enabled: bool = False
auto_order_target_price: Optional[str] = None
auto_order_action: Literal["notify_only", "generate_link", "auto_buy"] = "notify_only"
```

### 使用示例
```json
{
  "task_name": "iPhone 监控",
  "keyword": "iPhone 15",
  "auto_order_enabled": true,
  "auto_order_target_price": "5000",
  "auto_order_action": "generate_link"
}
```

### 通知示例
```
商品标题：iPhone 15 Pro Max 256G 蓝色钛金属
当前售价：8999
下单链接 (PC): https://www.goofish.com/order/confirm?itemId=xxx&price=8999
下单链接 (手机): https://m.goofish.com/order/confirm?itemId=xxx&price=8999

[自动下单] 价格匹配，已生成下单链接，请点击链接购买。
```

---

## ✨ 功能 2: 卖家活跃时间检测

### 功能描述
在搜索商品时自动检测卖家的上线时间（最后活跃时间），并在前台提供筛选选项，帮助用户快速定位活跃卖家，提高沟通效率和购买成功率。

### 主要特性
- ✅ 从个人主页 API 采集最后活跃时间
- ✅ 从商品详情页 API 获取卖家在线状态
- ✅ 智能格式化活跃时间显示
- ✅ 评估卖家活跃等级（5 个等级）
- ✅ 前台筛选功能（5 个时间段选项）

### 活跃等级说明
| 等级 | 条件 | 说明 |
|------|------|------|
| 🔥 非常活跃 | 1 小时内 | 卖家正在线或刚刚离开 |
| ✅ 活跃 | 24 小时内 | 卖家今天活跃过 |
| ⏳ 一般 | 72 小时内 | 卖家最近 3 天活跃 |
| 💤 不活跃 | 超过 72 小时 | 卖家较长时间未活跃 |
| ❓ 未知 | 无法获取 | API 未返回活跃时间 |

### 智能格式化显示
- <1 分钟：刚刚在线
- 1-60 分钟：X 分钟前
- 1-24 小时：X 小时前
- 1-7 天：X 天前
- 7-30 天：X 周前
- >30 天：具体日期（YYYY-MM-DD）

### 技术实现
**新增文件:**
- `src/services/seller_active_service.py` - 活跃时间服务
- `SELLER_ACTIVE_FEATURE.md` - 功能文档
- `demo_seller_active.py` - 演示脚本

**修改文件:**
- `src/parsers.py` - 扩展 `parse_user_head_data` 提取活跃时间
- `src/scraper.py` - 从 sellerDO 提取活跃信息
- `src/services/item_analysis_dispatcher.py` - 集成活跃时间处理
- `web-ui/src/types/result.d.ts` - 类型定义扩展
- `web-ui/src/components/tasks/TaskForm.vue` - 添加筛选 UI
- `web-ui/src/i18n/messages/zh-CN-extra.ts` - 翻译支持

**卖家信息新增字段:**
```typescript
interface SellerInfo {
  "卖家最后活跃时间"?: string;
  "卖家活跃时间格式化"?: string;
  "卖家活跃等级"?: string;
  "卖家在线状态"?: string;
  // ...
}
```

### 使用示例
任务创建时选择"24 小时内活跃"，系统将只推送最近活跃的卖家的商品。

---

## 🧪 测试

### 自动下单功能测试
```bash
python3 << 'PYEOF'
from src.services.auto_order_service import AutoOrderService

service = AutoOrderService()
is_match, reason = service.check_price_match(
    item_price="4500",
    target_price="5000",
    min_price=None,
    max_price=None
)
print(f"价格匹配测试：{is_match}, {reason}")
PYEOF
```

### 卖家活跃时间测试
```bash
python3 << 'PYEOF'
from src.services.seller_active_service import format_active_time, get_active_level
from datetime import datetime

now = datetime.now().isoformat()
print(f"格式化：{format_active_time(now)}")
print(f"活跃等级：{get_active_level(now)}")
PYEOF
```

### 运行演示脚本
```bash
# 自动下单功能演示
python3 demo_auto_order.py

# 卖家活跃时间演示
python3 demo_seller_active.py
```

---

## 📊 统计数据

```
2 个功能分支合并
11 个文件新增
19 个文件修改
+1,524 行代码添加
-92 行代码删除
2 个文档文件
2 个演示脚本
```

---

## 📸 截图

### 自动下单配置
任务表单中的自动下单配置区域（UI 已更新）

### 卖家活跃时间筛选
任务表单中的卖家活跃时间筛选选项（UI 已更新）

---

## 🔗 相关文档

- [自动下单功能文档](./AUTO_ORDER_FEATURE.md)
- [卖家活跃时间功能文档](./SELLER_ACTIVE_FEATURE.md)

---

## 📝 提交历史

```bash
f68c968 feat: 添加卖家活跃时间检测及筛选功能
9873fe9 feat: 实现自动下单功能
```

---

## ✅ Checklist

- [x] 代码通过测试
- [x] 类型定义更新
- [x] 前端 UI 更新
- [x] i18n 翻译完整
- [x] 功能文档编写
- [x] 演示脚本可用
- [x] 向后兼容
- [ ] 需要更新 README 文档
- [ ] 需要测试数据库迁移（无）
- [ ] 需要更新配置文件（否）

---

## 🚀 部署说明

1. **无需数据库迁移**: 所有新字段存储在现有 JSON 结构中
2. **无需配置变更**: 新功能默认关闭，通过 UI 开启
3. **向后兼容**: 已有任务不受影响

---

## 🔮 未来计划

### 自动下单功能
- [ ] 全自动购买（需要闲鱼 API 支持）
- [ ] 自动填写收货地址
- [ ] 订单状态追踪
- [ ] 历史价格趋势分析

### 卖家活跃时间功能
- [ ] 结果页面筛选支持
- [ ] 活跃等级徽章展示
- [ ] 排除不活跃卖家选项
- [ ] 响应时间统计
- [ ] 活跃趋势图表

---

## ⚠️ 注意事项

1. **自动下单**: 当前为半自动模式，需要用户手动点击链接确认支付
2. **活跃时间**: 不是所有卖家都有活跃时间数据，取决于闲鱼 API 返回
3. **隐私保护**: 部分卖家可能隐藏了活跃状态
4. **实时性**: 活跃时间不是实时更新的，有一定延迟

---

**Reviewers**: 请重点关注自动下单逻辑和活跃时间解析的准确性
**Testers**: 请在真实环境下测试价格匹配和卖家筛选功能
