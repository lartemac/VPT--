#!/usr/bin/env python3
"""
DuckDuckGo 搜索测试（新版 ddgs 库）
"""

from ddgs import DDGS
import sys

def test_duckduckgo():
    """测试 DuckDuckGo 搜索功能"""

    print("=" * 80)
    print("DuckDuckGo 搜索测试（新版 ddgs）")
    print("=" * 80)
    print()

    # 初始化
    ddgs = DDGS()

    # 测试1：中文搜索
    print("[测试1/3] 中文搜索：中信银行留学信用卡年费")
    print("-" * 80)

    try:
        results = list(ddgs.text("中信银行留学信用卡年费", max_results=3))

        if results:
            print(f"✅ 找到 {len(results)} 条结果\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. 【标题】{r.get('title', 'N/A')}")
                print(f"   【链接】{r.get('href', 'N/A')}")
                print(f"   【摘要】{r.get('body', 'N/A')[:80]}...")
                print()
        else:
            print("❌ 未找到结果\n")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}\n")

    print("-" * 80)
    print()

    # 测试2：英文搜索
    print("[测试2/3] 英文搜索：Python 3.14 new features")
    print("-" * 80)

    try:
        results = list(ddgs.text("Python 3.14 new features", max_results=3))

        if results:
            print(f"✅ 找到 {len(results)} 条结果\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. 【标题】{r.get('title', 'N/A')}")
                print(f"   【链接】{r.get('href', 'N/A')}")
                print()
        else:
            print("❌ 未找到结果\n")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}\n")

    print("-" * 80)
    print()

    # 测试3：新闻搜索
    print("[测试3/3] 新闻搜索：人工智能新闻 2026")
    print("-" * 80)

    try:
        results = list(ddgs.news("人工智能 2026", max_results=3))

        if results:
            print(f"✅ 找到 {len(results)} 条新闻\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. 【标题】{r.get('title', 'N/A')}")
                print(f"   【来源】{r.get('source', 'N/A')}")
                print(f"   【日期】{r.get('date', 'N/A')}")
                print(f"   【链接】{r.get('url', 'N/A')}")
                print()
        else:
            print("❌ 未找到新闻结果\n")

    except Exception as e:
        print(f"❌ 搜索失败：{str(e)}\n")

    print("=" * 80)
    print("✅ 测试完成")
    print("=" * 80)

    return True

def main():
    try:
        test_duckduckgo()

        print()
        print("🎉 DuckDuckGo 搜索可用！")
        print()
        print("优点：")
        print("  ✅ 完全免费")
        print("  ✅ 无需 API key")
        print("  ✅ 无使用限制")
        print("  ✅ 保护隐私（不追踪用户）")
        print("  ✅ 中英文搜索都支持")
        print()
        print("可以作为 Claude WebSearch 的补充方案！")

    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
