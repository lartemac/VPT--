#!/usr/bin/env python3
"""
DuckDuckGo 搜索测试
测试完全免费、无需 API key 的搜索引擎
"""

from duckduckgo_search import DDGS
import sys

def test_basic_search():
    """基础搜索测试"""

    print("=" * 80)
    print("DuckDuckGo 搜索测试")
    print("=" * 80)
    print()

    # 测试1：中文搜索
    print("[测试1] 中文搜索：中信银行留学信用卡年费")
    print("-" * 80)

    try:
        ddgs = DDGS()
        results = ddgs.text("中信银行留学信用卡年费", max_results=5)

        if results:
            print(f"✓ 找到 {len(results)} 条结果：\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. 标题：{result.get('title', 'N/A')}")
                print(f"   链接：{result.get('href', 'N/A')}")
                print(f"   摘要：{result.get('body', 'N/A')[:100]}...")
                print()
        else:
            print("✗ 未找到结果")

    except Exception as e:
        print(f"✗ 搜索失败：{str(e)}")
        return False

    print()
    print("-" * 80)
    print()

    # 测试2：英文搜索
    print("[测试2] 英文搜索：Python 3.14 release date")
    print("-" * 80)

    try:
        ddgs = DDGS()
        results = ddgs.text("Python 3.14 release date", max_results=3)

        if results:
            print(f"✓ 找到 {len(results)} 条结果：\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. 标题：{result.get('title', 'N/A')}")
                print(f"   链接：{result.get('href', 'N/A')}")
                print()
        else:
            print("✗ 未找到结果")

    except Exception as e:
        print(f"✗ 搜索失败：{str(e)}")

    print()
    print("-" * 80)
    print()

    # 测试3：新闻搜索
    print("[测试3] 新闻搜索：2026年科技新闻")
    print("-" * 80)

    try:
        ddgs = DDGS()
        results = ddgs.news("2026年科技新闻", max_results=3)

        if results:
            print(f"✓ 找到 {len(results)} 条新闻：\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. 标题：{result.get('title', 'N/A')}")
                print(f"   来源：{result.get('source', 'N/A')}")
                print(f"   日期：{result.get('date', 'N/A')}")
                print(f"   链接：{result.get('url', 'N/A')}")
                print()
        else:
            print("✗ 未找到新闻结果")

    except Exception as e:
        print(f"✗ 搜索失败：{str(e)}")

    print()
    print("=" * 80)
    print("测试完成")
    print("=" * 80)

    return True

def main():
    if not test_basic_search():
        sys.exit(1)

    print()
    print("✅ DuckDuckGo 搜索可用！")
    print()
    print("优点：")
    print("  ✓ 完全免费")
    print("  ✓ 无需 API key")
    print("  ✓ 无使用限制")
    print("  ✓ 保护隐私")
    print("  ✓ 中文支持良好")
    print()
    print("建议：")
    print("  可以作为 Claude WebSearch 的补充方案")

if __name__ == "__main__":
    main()
