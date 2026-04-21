#!/usr/bin/env python3
"""
卖家活跃时间检测功能演示
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.seller_active_service import (
    format_active_time,
    get_active_level,
    is_seller_recently_active,
)

def demo():
    print("\n")
    print("★" * 30)
    print(" 卖家活跃时间检测功能演示")
    print("★" * 30)
    print()
    
    # 模拟不同卖家的活跃时间
    sellers = [
        {
            "昵称": "数码达人小张",
            "lastActiveTime": datetime.now().isoformat(),
        },
        {
            "昵称": "二手商贩小李",
            "lastActiveTime": (datetime.now() - timedelta(minutes=30)).isoformat(),
        },
        {
            "昵称": "个人卖家王女士",
            "lastActiveTime": (datetime.now() - timedelta(hours=3)).isoformat(),
        },
        {
            "昵称": "电子产品专营",
            "lastActiveTime": (datetime.now() - timedelta(days=2)).isoformat(),
        },
        {
            "昵称": "很久不来的卖家",
            "lastActiveTime": (datetime.now() - timedelta(days=15)).isoformat(),
        },
        {
            "昵称": "神秘卖家",
            "lastActiveTime": None,
        },
    ]
    
    print("=" * 70)
    print(f"{'卖家昵称':<20} {'活跃时间':<15} {'活跃等级':<10}")
    print("=" * 70)
    
    for seller in sellers:
        formatted = format_active_time(seller["lastActiveTime"])
        level = get_active_level(seller["lastActiveTime"])
        
        # 添加徽章
        badge = ""
        if level == "非常活跃":
            badge = "🔥"
        elif level == "活跃":
            badge = "✅"
        elif level == "一般":
            badge = "⏳"
        elif level == "不活跃":
            badge = "💤"
        else:
            badge = "❓"
        
        print(f"{seller['昵称']:<22} {formatted:<15} {badge} {level}")
    
    print("=" * 70)
    print()
    
    # 演示筛选功能
    print("【筛选示例】只看 24 小时内活跃的卖家：")
    print("-" * 70)
    for seller in sellers:
        if is_seller_recently_active(seller["lastActiveTime"], within_hours=24):
            formatted = format_active_time(seller["lastActiveTime"])
            level = get_active_level(seller["lastActiveTime"])
            print(f"  ✓ {seller['昵称']}: {formatted} ({level})")
    
    print()
    print("-" * 70)
    print(f"共找到 {sum(1 for s in sellers if is_seller_recently_active(s['lastActiveTime'], within_hours=24))} 个活跃卖家")
    print()
    
    print("★" * 30)
    print(" 演示完成!")
    print("★" * 30)
    print()

if __name__ == "__main__":
    demo()
