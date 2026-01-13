#!/usr/bin/env python3
"""
GLM-4 网络搜索工具
用途：当 Claude WebSearch 达到使用上限时，使用 GLM 进行搜索
创建时间：2026-01-13
"""

import sys
import json
from zhipuai import ZhipuAI

# API 配置
API_KEY = "232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb"
MODEL = "glm-4-flash"  # 使用快速、经济的模型

def search_with_glm(query, top_k=5, detail_level="简洁"):
    """
    使用 GLM-4 进行网络搜索

    参数：
        query: 搜索问题
        top_k: 返回前N个搜索结果（1-10）
        detail_level: 详细程度（简洁/中等/详细）
    """

    # 根据详细程度调整提示词
    if detail_level == "简洁":
        system_prompt = "你是一个搜索助手。请简洁回答用户问题，重点突出关键信息。"
    elif detail_level == "详细":
        system_prompt = "你是一个搜索助手。请详细回答用户问题，包括背景信息和细节。"
    else:
        system_prompt = "你是一个搜索助手。请清晰、准确地回答用户问题。"

    try:
        client = ZhipuAI(api_key=API_KEY)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"请搜索并回答：{query}"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "search_query": query,
                        "top_k": top_k
                    }
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ 搜索失败：{str(e)}"

def main():
    """命令行接口"""

    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 glm_search.py \"搜索问题\"")
        print()
        print("示例：")
        print("  python3 glm_search.py \"中信银行留学卡年费\"")
        print("  python3 glm_search.py \"Python 最新版本\" 详细")
        print()
        print("参数：")
        print("  第1个参数：搜索问题（必需）")
        print("  第2个参数：详细程度（可选：简洁/中等/详细，默认：中等）")
        sys.exit(1)

    # 解析参数
    query = sys.argv[1]
    detail_level = sys.argv[2] if len(sys.argv) > 2 else "中等"

    # 验证详细程度参数
    if detail_level not in ["简洁", "中等", "详细"]:
        detail_level = "中等"

    # 显示搜索信息
    print("=" * 80)
    print(f"GLM-4 网络搜索")
    print("=" * 80)
    print(f"搜索问题：{query}")
    print(f"详细程度：{detail_level}")
    print("-" * 80)
    print()

    # 执行搜索
    result = search_with_glm(query, top_k=5, detail_level=detail_level)

    # 显示结果
    print(result)
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
