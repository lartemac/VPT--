#!/usr/bin/env python3
"""
DuckDuckGo 搜索工具
完全免费、无需API key、实时网络搜索
用途：Claude WebSearch 的补充方案
"""

from ddgs import DDGS
import sys
import json

def ddg_search(query, max_results=5, search_type="text"):
    """
    DuckDuckGo 搜索函数

    参数：
        query: 搜索问题
        max_results: 最多返回几条结果（1-20）
        search_type: 搜索类型（text/news）

    返回：
        搜索结果（格式化字符串）
    """

    try:
        ddgs = DDGS()

        if search_type == "news":
            # 新闻搜索
            results = list(ddgs.news(query, max_results=max_results))

            if not results:
                return "❌ 未找到相关新闻"

            output = f"📰 新闻搜索结果（{query}）\n"
            output += "=" * 80 + "\n\n"

            for i, r in enumerate(results, 1):
                output += f"{i}. 【标题】{r.get('title', 'N/A')}\n"
                output += f"   【来源】{r.get('source', 'N/A')}\n"
                output += f"   【日期】{r.get('date', 'N/A')}\n"
                output += f"   【链接】{r.get('url', 'N/A')}\n"

                # 如果有正文摘要，添加
                if r.get('body'):
                    output += f"   【摘要】{r.get('body', '')[:150]}...\n"

                output += "\n"

            return output

        else:
            # 普通文本搜索
            results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return "❌ 未找到相关结果"

            output = f"🔍 搜索结果（{query}）\n"
            output += "=" * 80 + "\n\n"

            for i, r in enumerate(results, 1):
                output += f"{i}. 【标题】{r.get('title', 'N/A')}\n"
                output += f"   【链接】{r.get('href', 'N/A')}\n"
                output += f"   【摘要】{r.get('body', 'N/A')[:200]}...\n"
                output += "\n"

            return output

    except Exception as e:
        return f"❌ 搜索失败：{str(e)}"

def ddg_search_json(query, max_results=5, search_type="text"):
    """
    返回 JSON 格式的搜索结果（便于程序处理）
    """

    try:
        ddgs = DDGS()

        if search_type == "news":
            results = list(ddgs.news(query, max_results=max_results))
        else:
            results = list(ddgs.text(query, max_results=max_results))

        return json.dumps(results, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def main():
    """命令行接口"""

    if len(sys.argv) < 2:
        print("DuckDuckGo 搜索工具")
        print()
        print("用法：")
        print("  python3 ddg_search.py \"搜索问题\" [结果数量] [搜索类型]")
        print()
        print("参数：")
        print("  搜索问题   - 要搜索的内容（必需）")
        print("  结果数量   - 返回几条结果（1-20，默认5）")
        print("  搜索类型   - text（普通）/ news（新闻），默认text")
        print()
        print("示例：")
        print("  python3 ddg_search.py \"中信银行信用卡年费\"")
        print("  python3 ddg_search.py \"Python 3.14\" 3")
        print("  python3 ddg_search.py \"AI新闻\" 5 news")
        print()
        print("特点：")
        print("  ✅ 完全免费")
        print("  ✅ 无需 API key")
        print("  ✅ 无使用限制")
        print("  ✅ 保护隐私")
        print("  ✅ 实时网络搜索")
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    search_type = sys.argv[3] if len(sys.argv) > 3 else "text"

    # 限制范围
    if max_results < 1:
        max_results = 1
    elif max_results > 20:
        max_results = 20

    if search_type not in ["text", "news"]:
        search_type = "text"

    # 执行搜索
    result = ddg_search(query, max_results, search_type)
    print(result)

if __name__ == "__main__":
    main()
