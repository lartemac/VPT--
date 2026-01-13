#!/usr/bin/env python3
"""
GLM 自动搜索代理
用途：让 Claude Code 在需要搜索时自动调用 GLM API
设计：无感知集成，Claude 只需调用此脚本即可获得搜索结果
"""

import sys
import json
from zhipuai import ZhipuAI

# API 配置
API_KEY = "232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb"
MODEL = "glm-4-flash"

def auto_search(query, return_format="text"):
    """
    自动搜索函数（供 Claude 调用）

    参数：
        query: 搜索问题
        return_format: 返回格式（text/json/summary）

    返回：
        搜索结果（根据 return_format 格式化）
    """

    try:
        client = ZhipuAI(api_key=API_KEY)

        # 根据返回格式调整系统提示
        if return_format == "json":
            system_prompt = """你是一个搜索助手。请以 JSON 格式返回搜索结果，包含以下字段：
{
  "summary": "简要总结（1-2句话）",
  "key_points": ["要点1", "要点2", ...],
  "sources": ["来源1", "来源2"],
  "details": "详细信息"
}"""
        elif return_format == "summary":
            system_prompt = "你是一个搜索助手。请用3-5句话总结搜索结果，突出关键信息。"
        else:
            system_prompt = "你是一个搜索助手。请清晰、准确地回答用户问题。"

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
                        "top_k": 5
                    }
                }
            ]
        )

        result = response.choices[0].message.content

        # 如果要求 JSON 格式，尝试解析
        if return_format == "json":
            try:
                # 尝试提取 JSON（去除可能的 markdown 代码块标记）
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    result = result.split("```")[1].split("```")[0].strip()

                parsed = json.loads(result)
                return json.dumps(parsed, ensure_ascii=False, indent=2)
            except:
                # 如果解析失败，返回原始文本
                return result

        return result

    except Exception as e:
        error_msg = f"❌ 搜索失败：{str(e)}"
        if return_format == "json":
            return json.dumps({"error": error_msg}, ensure_ascii=False)
        return error_msg

def main():
    """命令行接口"""

    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 auto_search.py \"搜索问题\" [格式]")
        print()
        print("格式选项：")
        print("  text    - 普通文本（默认）")
        print("  summary - 简要总结（3-5句话）")
        print("  json    - JSON 格式")
        print()
        print("示例：")
        print("  python3 auto_search.py \"中信银行信用卡年费\"")
        print("  python3 auto_search.py \"Python 最新版本\" summary")
        print("  python3 auto_search.py \"MacBook Pro 2026\" json")
        sys.exit(1)

    query = sys.argv[1]
    return_format = sys.argv[2] if len(sys.argv) > 2 else "text"

    if return_format not in ["text", "summary", "json"]:
        return_format = "text"

    result = auto_search(query, return_format)
    print(result)

if __name__ == "__main__":
    main()
