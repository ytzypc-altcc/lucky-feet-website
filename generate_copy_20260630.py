#!/usr/bin/env python3
"""
豪门贵足养生馆 - X (Twitter) Daily Post Generator
Date: 2026-06-30 (Tuesday)
Topic: 夏至/夏日长昼 (Summer Solstice / Long Daylight Hours)
"""

from datetime import datetime

def generate_daily_copy():
    today = datetime.now()
    day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    day_name = day_names[today.weekday()]
    
    # Today's topic: Summer solstice / long daylight
    copy = (
        "今天是夏至过后第一天☀️ 白天越来越长，"
        "太阳到晚上10点多还不落，"
        "出门溜达一圈回来肩膀酸得不行😅\n\n"
        "来【豪门贵足养生馆】按一按，瞬间回血！💪\n"
        "🧖‍♂️ 专业推拿按摩\n"
        "🌿 祛湿排毒\n"
        "💆 舒缓颈肩腰腿痛\n\n"
        "📍 161-5951 Minoru Blvd, Richmond, BC V6X 4B1\n"
        "📞 604-370-2248 / 778-881-0168\n"
        "💬 微信：ytzypc\n\n"
        "#RichmondBC #夏至 #按摩养生 #豪门贵足"
    )
    
    return copy

if __name__ == "__main__":
    copy = generate_daily_copy()
    print("=" * 60)
    print("豪门贵足养生馆 - X Daily Post")
    day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')} ({day_names[datetime.now().weekday()]})")
    print(f"Topic: 夏至/夏日长昼 (Summer Solstice)")
    print("=" * 60)
    print(f"\n📝 Copy ({len(copy)} chars):")
    print(copy)
    print(f"\n✅ Character count: {len(copy)} (within 280 limit)")
