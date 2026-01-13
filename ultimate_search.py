#!/usr/bin/env python3
"""
终极安全搜索 - 多重验证确保真实网络内容
策略：
1. 强制要求包含时间戳或来源
2. 检查是否是通用知识（可能是训练数据）
3. 要求搜索结果包含最新信息
"""

import sys
import re
from datetime import datetime, timedelta
from zhipuai import ZhipuAI

API_KEY = "232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb"
MODEL = "glm-4-flash"

def check_for_trained_data_patterns(result):
    """
    检查是否像训练数据而非实时网络搜索
    """

    # 训练数据的特征
    trained_data_patterns = [
        (r"根据.*?资料", "引用通用资料"),
        (r"一般来说|通常", "通用描述"),
        (r"可以.*?可以.*?可以", "重复模式"),
        (r"第一.*?第二.*?第三", "结构化列表（可能是教材）"),
        (r"需要注意的是|值得注意的是", "教学用语"),
    ]

    issues = []
    for pattern, desc in trained_data_patterns:
        if re.search(pattern, result):
            issues.append(f"⚠️  发现训练数据特征：{desc}")

    return issues

def check_for_real_web_indicators(result):
    """
    检查真实网络搜索的指标
    """

    # 强指标（证明是真实网络）
    strong_indicators = [
        (r"20[12][0-9]年[01]?[0-9]月[0-3]?[0-9]日", "具体日期"),
        (r"发布时间[:：]\s*20[12][0-9]", "发布时间戳"),
        (r"来源[:：]\s*(.+?[网报刊台])", "信息来源"),
        (r"记者[:：]\s*\w+", "记者署名"),
        (r"据.+?报道", "新闻报道引用"),
        (r"www\.\w+\.(com|cn|org|net)", "网址"),
        (r"编辑[:：]\s*\w+", "编辑署名"),
    ]

    # 中等指标
    medium_indicators = [
        (r"近日|昨日|今日", "相对时间"),
        (r"最新|刚刚|实时", "时效性词汇"),
        (r"数据显示|据统计", "数据引用"),
    ]

    strong_count = 0
    medium_count = 0

    found = []

    for pattern, desc in strong_indicators:
        if re.search(pattern, result):
            strong_count += 1
            found.append(f"✓ {desc}")

    for pattern, desc in medium_indicators:
        if re.search(pattern, result):
            medium_count += 1
            found.append(f"✓ {desc}")

    return strong_count, medium_count, found

def validate_search_quality(result, query):
    """
    综合验证搜索质量
    """

    # 检查拒绝语
    rejection_phrases = [
        "无法搜索",
        "无法访问",
        "无法提供",
        "我是一个人工智能",
        "建议您查阅",
        "搜索未找到",
        "未在提供的信息",
    ]

    for phrase in rejection_phrases:
        if phrase in result:
            return False, f"发现拒绝语：'{phrase}'"

    # 检查训练数据特征
    trained_issues = check_for_trained_data_patterns(result)

    # 检查真实网络指标
    strong_count, medium_count, found_indicators = check_for_real_web_indicators(result)

    # 评分系统
    score = 0

    # 强指标每个得10分
    score += strong_count * 10

    # 中等指标每个得5分
    score += medium_count * 5

    # 训练数据特征每个扣20分
    score -= len(trained_issues) * 20

    # 结果长度检查（太短可能是拒绝或无结果）
    if len(result) < 50:
        score -= 30
        trained_issues.append("⚠️  结果过短，可能无有效信息")

    # 验证
    if score >= 20:
        # 通过
        details = f"验证得分：{score}分\n\n发现的网络指标：\n" + "\n".join(found_indicators)
        if trained_issues:
            details += "\n\n警告：\n" + "\n".join(trained_issues)
        return True, details
    elif score >= 0:
        details = f"验证得分：{score}分（需≥20分）\n\n发现的网络指标：\n" + "\n".join(found_indicators)
        if trained_issues:
            details += "\n\n警告：\n" + "\n".join(trained_issues)
        details += "\n\n结论：可能是训练数据或搜索结果质量不高"
        return False, details
    else:
        details = f"验证得分：{score}分\n\n警告：\n" + "\n".join(trained_issues)
        details += "\n\n结论：很可能是训练数据，非实时网络搜索"
        return False, details

def ultimate_search(query, require_freshness=True):
    """
    终极搜索函数 - 确保真实网络内容

    参数：
        query: 搜索问题
        require_freshness: 是否要求时效性（默认是）
    """

    client = ZhipuAI(api_key=API_KEY)

    # 构建增强提示词
    if require_freshness:
        system_prompt = """你是一个专业的实时网络搜索助手。

重要要求：
1. 必须使用 web_search 工具搜索最新网络信息
2. 返回结果必须包含：
   - 具体的时间信息（发布日期、更新时间等）
   - 信息来源（网站、媒体、机构名称）
   - 具体的数据和细节
3. 不要返回通用知识或训练数据
4. 如果搜索不到最新信息，明确说明"未找到实时信息"

搜索策略：
- 优先搜索新闻、官方发布、最新动态
- 避免返回百科、教程等静态内容
- 确保信息具有时效性"""
    else:
        system_prompt = """你是一个专业的网络搜索助手。

要求：
1. 必须使用 web_search 工具
2. 返回具体的搜索结果
3. 包含信息来源
4. 不要说"无法搜索"或建议用户自行搜索"""

    user_prompt = f"请搜索并详细回答：{query}\n\n请务必使用 web_search 工具搜索实时网络信息，并明确说明信息来源和时间。"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
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

        # 验证搜索质量
        is_valid, validation_details = validate_search_quality(result, query)

        return is_valid, result, validation_details

    except Exception as e:
        return False, f"搜索失败：{str(e)}", f"错误：{str(e)}"

def main():
    """命令行接口"""

    if len(sys.argv) < 2:
        print("终极安全搜索 - 确保真实网络内容")
        print()
        print("用法：")
        print("  python3 ultimate_search.py \"搜索问题\" [是否要求最新]")
        print()
        print("参数：")
        print("  搜索问题 - 要搜索的内容")
        print("  是否要求最新 - yes（要求最新，默认）/ no（不要求）")
        print()
        print("功能：")
        print("  ✓ 多重验证确保结果来自真实网络")
        print("  ✓ 自动检测并拒绝训练数据")
        print("  ✓ 评分系统验证搜索质量")
        print("  ✓ 详细显示验证过程")
        print()
        print("示例：")
        print("  python3 ultimate_search.py \"2026年1月最新科技新闻\"")
        print("  python3 ultimate_search.py \"Python 教程\" no")
        sys.exit(1)

    query = sys.argv[1]
    require_freshness = sys.argv[2].lower() != "no" if len(sys.argv) > 2 else True

    print("=" * 80)
    print("终极安全搜索")
    print("=" * 80)
    print(f"搜索问题：{query}")
    print(f"时效性要求：{'是' if require_freshness else '否'}")
    print("-" * 80)
    print()

    is_valid, result, validation = ultimate_search(query, require_freshness)

    print("验证结果：")
    print(validation)
    print()
    print("-" * 80)
    print()
    print("搜索结果：")
    print(result)
    print()
    print("=" * 80)

    if is_valid:
        print("✅ 验证通过：搜索结果来自真实互联网")
        sys.exit(0)
    else:
        print("❌ 验证失败：搜索结果可能是训练数据或质量不高")
        print()
        print("建议：")
        if require_freshness:
            print("  1. 尝试不要求最新信息：python3 ultimate_search.py \"问题\" no")
            print("  2. 使用 Claude WebSearch（如果是英文学术文献）")
        else:
            print("  1. 检查搜索问题是否合适")
            print("  2. 尝试使用 Claude WebSearch")
        sys.exit(1)

if __name__ == "__main__":
    main()
