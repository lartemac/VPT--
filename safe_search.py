#!/usr/bin/env python3
"""
安全搜索代理 - 确保搜索结果来自真实互联网
添加多重验证机制，避免返回训练数据
"""

import sys
import re
from datetime import datetime
from zhipuai import ZhipuAI

API_KEY = "232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb"
MODEL = "glm-4-flash"

def validate_real_search(result, query):
    """
    验证搜索结果是否来自真实互联网

    检查项：
    1. 包含时效性信息（年份、日期）
    2. 包含具体数据来源
    3. 包含具体数字或细节
    4. 不包含"无法访问"、"训练数据"等拒绝语
    """

    # 拒绝语列表（如果出现这些，说明可能返回了训练数据或拒绝搜索）
    rejection_keywords = [
        "无法直接搜索",
        "无法直接访问",
        "无法提供",
        "我是一个人工智能",
        "我的功能仅限于",
        "建议您查阅",
        "训练数据",
        "知识截止",
        "截止到"
    ]

    # 正面指标（说明是真实网络搜索）
    positive_indicators = [
        r"20[12][0-9]",  # 2010-2099 年份
        r"\d{4}年\d{1,2}月\d{1,2}日",  # 中文日期格式
        r"来源[:：]",  # 来源标注
        r"发布时间",  # 发布时间
        r"www\.",  # 网址
        r".com|\.cn|\.org",  # 域名
        r"记者[:：]",  # 记者署名
        r"据.+报道",  # 新闻报道
    ]

    issues = []
    score = 0

    # 检查拒绝语
    for keyword in rejection_keywords:
        if keyword in result:
            issues.append(f"⚠️  发现拒绝语：'{keyword}'")
            score -= 10

    # 检查正面指标
    for pattern in positive_indicators:
        if re.search(pattern, result):
            score += 5
            break  # 每类指标只计一次

    # 特别检查：是否包含当前年份或明年年份
    current_year = datetime.now().year
    if str(current_year) in result or str(current_year + 1) in result:
        score += 20

    # 验证结果
    if score >= 10:
        return True, "✅ 验证通过：搜索结果来自真实互联网", issues
    elif score >= 0:
        return False, "⚠️  验证存疑：搜索结果可能包含训练数据", issues
    else:
        return False, "❌ 验证失败：搜索结果很可能来自训练数据或拒绝搜索", issues

def safe_search(query, max_retries=2):
    """
    安全搜索函数 - 确保返回真实网络搜索结果

    参数：
        query: 搜索问题
        max_retries: 最大重试次数

    返回：
        (成功标志, 搜索结果, 验证信息)
    """

    client = ZhipuAI(api_key=API_KEY)

    for attempt in range(max_retries + 1):
        try:
            # 构建强制搜索的提示词
            force_search_prompt = f"""你必须使用 web_search 工具搜索实时网络信息。

严格要求：
1. 必须调用 web_search 工具
2. 必须返回搜索到的具体内容
3. 必须包含信息来源和时间
4. 不要说"无法搜索"或"无法访问"
5. 如果搜索不到，明确说明"搜索未找到相关结果"

搜索问题：{query}

现在请搜索并回答。"""

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的搜索助手。你必须使用 web_search 工具搜索实时网络信息，返回准确的搜索结果。"
                    },
                    {
                        "role": "user",
                        "content": force_search_prompt
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

            # 验证搜索结果
            is_valid, validation_msg, issues = validate_real_search(result, query)

            if is_valid:
                # 验证通过，返回结果
                output = f"{validation_msg}\n\n"
                if issues:
                    output += "\n".join(issues) + "\n\n"
                output += "搜索结果：\n"
                output += "-" * 80 + "\n"
                output += result
                return True, output, validation_msg
            else:
                # 验证失败，记录问题
                if attempt < max_retries:
                    # 重试
                    continue
                else:
                    # 最后一次尝试也失败
                    output = f"{validation_msg}\n\n"
                    if issues:
                        output += "发现的问题：\n" + "\n".join(issues) + "\n\n"
                    output += "原始返回：\n"
                    output += "-" * 80 + "\n"
                    output += result
                    return False, output, validation_msg

        except Exception as e:
            if attempt < max_retries:
                continue
            else:
                return False, f"❌ 搜索失败：{str(e)}", "搜索过程出错"

def main():
    """命令行接口"""

    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 safe_search.py \"搜索问题\"")
        print()
        print("功能：")
        print("  - 确保搜索结果来自真实互联网")
        print("  - 自动验证搜索结果质量")
        print("  - 自动重试（最多2次）")
        print()
        print("示例：")
        print("  python3 safe_search.py \"2026年1月最新新闻\"")
        print("  python3 safe_search.py \"Python 3.14 新特性\"")
        sys.exit(1)

    query = sys.argv[1]

    print("=" * 80)
    print("安全搜索代理 - 确保真实网络内容")
    print("=" * 80)
    print(f"搜索问题：{query}")
    print("-" * 80)
    print()

    success, result, validation = safe_search(query)

    print(result)
    print()
    print("=" * 80)

    if success:
        print("状态：✅ 搜索成功，结果已验证")
        sys.exit(0)
    else:
        print("状态：❌ 搜索失败或验证未通过")
        print()
        print("建议：")
        print("  1. 尝试重新搜索")
        print("  2. 使用 Claude WebSearch（如果是英文学术文献）")
        print("  3. 检查网络连接")
        sys.exit(1)

if __name__ == "__main__":
    main()
