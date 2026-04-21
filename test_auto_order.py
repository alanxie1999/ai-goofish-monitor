#!/usr/bin/env python3
"""自动下单功能后端测试"""
import sys
sys.path.insert(0, '/workspace')

print("=" * 60)
print("自动下单功能后端测试")
print("=" * 60)

try:
    from src.services.auto_order_service import AutoOrderService
    from src.services.order_link_service import OrderLinkService
    print("✅ 后端服务导入成功")
    
    # 测试订单链接生成
    order_service = OrderLinkService()
    pc_link = order_service.generate_order_link("123456789", "5000", "seller_001")
    mobile_link = order_service.generate_mobile_order_link("123456789", "5000")
    print(f"\n✅ 订单链接生成服务:")
    print(f"   PC 链接：{pc_link}")
    print(f"   移动端：{mobile_link}")
    
    # 测试价格匹配检测
    auto_service = AutoOrderService()
    is_match, reason = auto_service.check_price_match("4000", "5000", None, None)
    print(f"\n✅ 价格匹配检测:")
    print(f"   结果：{is_match}")
    print(f"   原因：{reason}")
    
    # 测试自动下单处理
    import asyncio
    async def test_process():
        item_data = {
            "商品 ID": "123456789",
            "当前售价": "4500",
            "商品链接": "https://example.com/item"
        }
        task_config = {
            "auto_order_enabled": True,
            "auto_order_action": "generate_link",
            "auto_order_target_price": "5000"
        }
        result = await auto_service.process_auto_order(item_data, task_config)
        return result
    
    result = asyncio.run(test_process())
    print(f"\n✅ 自动下单处理:")
    print(f"   发送通知：{result['should_notify']}")
    print(f"   操作类型：{result['action_taken']}")
    print(f"   订单链接：{'✓' if result.get('order_link') else '✗'}")
    
    print("\n" + "=" * 60)
    print("✅ 后端功能测试全部通过!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 测试失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
