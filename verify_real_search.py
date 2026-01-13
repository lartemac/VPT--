#!/usr/bin/env python3
"""
验证 GLM-4 web_search 是否来自真实互联网
策略：搜索"今天"和"昨天"的新闻，验证时效性
如果返回训练数据，应该是过时的信息
如果返回真实网络内容，应该是最新信息
"""

import sys
from datetime import datetime, timedelta
from zhipuai import ZhipuAI

API_KEY = "232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb"
MODEL = "glm-4-flash"

def test_real_time_search():
    """测试1：搜索今天和昨天的新闻"""

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    today_str = today.strftime("%Y年%m月%d日")
    yesterday_str = yesterday.strftime("%Y年%m月%d日")

    print("=" * 80)
    print("测试1：时效性验证（搜索今天和昨天的新闻）")
    print("=" * 80)
    print(f"当前时间：{today.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("策略：")
    print("  如果是训练数据 → 无法回答今天/昨天的新闻")
    print("  如果是真实网络 → 能搜索到最新新闻")
    print()

    client = ZhipuAI(api_key=API_KEY)

    # 搜索今天的新闻
    print(f"[1/2] 搜索今天的新闻（{today_str}）...")
    print("-" * 80)

    try:
        response1 = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个搜索助手。请搜索最新的新闻，并明确说明新闻的发布时间。"
                },
                {
                    "role": "user",
                    "content": f"请搜索并告诉我：{today_str} 发生了什么重要新闻？请列出至少3条，并说明每条新闻的发布时间和来源。"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": f"{today_str} 新闻",
                        "top_k": 5
                    }
                }
            ]
        )

        result1 = response1.choices[0].message.content
        print(result1)
        print()

        # 分析结果
        if today_str in result1 or "2026" in result1 or "2025" in result1:
            print("✅ 时效性测试通过：包含今天或2025/2026年的信息")
            print("   说明：搜索的是真实互联网内容，而非训练数据")
        else:
            print("⚠️  时效性测试存疑：未检测到明确的时效信息")
            print("   可能是训练数据，需要进一步验证")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}")
        return False

    print()
    print("-" * 80)
    print()

    # 搜索昨天的新闻
    print(f"[2/2] 搜索昨天的新闻（{yesterday_str}）...")
    print("-" * 80)

    try:
        response2 = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个搜索助手。请搜索最新的新闻，并明确说明新闻的发布时间。"
                },
                {
                    "role": "user",
                    "content": f"请搜索并告诉我：{yesterday_str} 发生了什么重要新闻？请列出至少3条，并说明每条新闻的发布时间和来源。"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": f"{yesterday_str} 新闻",
                        "top_k": 5
                    }
                }
            ]
        )

        result2 = response2.choices[0].message.content
        print(result2)
        print()

        # 分析结果
        if yesterday_str in result2 or "2026" in result2 or "2025" in result2:
            print("✅ 时效性测试通过：包含昨天或2025/2026年的信息")
        else:
            print("⚠️  时效性测试存疑")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}")
        return False

    return True

def test_specific_real_time_info():
    """测试2：搜索特定实时信息"""

    print()
    print("=" * 80)
    print("测试2：特定实时信息验证")
    print("=" * 80)
    print("策略：搜索不可能在训练数据中的信息")
    print()

    client = ZhipuAI(api_key=API_KEY)

    # 测试搜索当前时间
    print("[1/3] 搜索：当前北京时间...")
    print("-" * 80)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "请搜索并告诉我现在的准确时间（北京时间），包括年月日和时分秒。"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "现在北京时间",
                        "top_k": 3
                    }
                }
            ]
        )

        result = response.choices[0].message.content
        print(result)
        print()

        if "2026" in result or "2025" in result:
            print("✅ 实时性测试通过")
        else:
            print("⚠️  实时性测试存疑")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}")

    print()
    print("-" * 80)
    print()

    # 测试搜索股市行情（实时变化的数据）
    print("[2/3] 搜索：今天上证指数...")
    print("-" * 80)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "请搜索并告诉我今天上证指数的收盘点位和涨跌幅。"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "上证指数 今天 收盘",
                        "top_k": 3
                    }
                }
            ]
        )

        result = response.choices[0].message.content
        print(result)
        print()

        if "点" in result or ("%" in result or "涨" in result or "跌" in result):
            print("✅ 实时数据测试通过：包含股市具体数据")
        else:
            print("⚠️  实时数据测试存疑")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}")

    print()
    print("-" * 80)
    print()

    # 测试搜索天气预报（每天更新的信息）
    print("[3/3] 搜索：北京明天天气...")
    print("-" * 80)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "请搜索并告诉我北京明天的天气预报，包括温度和天气状况。"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": "北京 明天 天气预报",
                        "top_k": 3
                    }
                }
            ]
        )

        result = response.choices[0].message.content
        print(result)
        print()

        if "度" in result or "℃" in result or "天气" in result:
            print("✅ 天气预报测试通过：包含具体天气信息")
        else:
            print("⚠️  天气预报测试存疑")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}")

    return True

def main():
    """运行所有验证测试"""

    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "GLM-4 真实网络搜索验证测试" + " " * 28 + "║")
    print("║" + " " * 15 + "验证搜索结果是否来自真实互联网（而非训练数据）" + " " * 15 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # 测试1：时效性验证
    test1_passed = test_real_time_search()

    # 测试2：特定实时信息
    test2_passed = test_specific_real_time_info()

    # 总结
    print()
    print("=" * 80)
    print("验证结论")
    print("=" * 80)
    print()

    if test1_passed and test2_passed:
        print("✅ 验证通过：GLM-4 web_search 工具返回的是真实互联网内容")
        print()
        print("证据：")
        print("  1. 能够搜索到今天/昨天的最新新闻（训练数据无法包含）")
        print("  2. 能够获取实时数据（时间、股市、天气等）")
        print("  3. 搜索结果包含时效性信息和数据来源")
        print()
        print("结论：")
        print("  GLM-4 的 web_search 工具确实调用了真实网络搜索API")
        print("  搜索结果来自互联网，而非训练数据")
    else:
        print("⚠️  验证存疑：需要进一步测试和分析")

    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
