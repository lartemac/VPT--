#!/usr/bin/env python3
"""
GLM-4.7 通用助手工具
支持多种任务：文本生成、代码编写、数据分析、医学问答等
"""

import sys
from zhipuai import ZhipuAI

# API 配置
API_KEY = "REDACTED_GLM_API_KEY"

# 模型配置
MODELS = {
    "plus": "glm-4-plus",      # 最新最强（GLM-4.7）
    "flash": "glm-4-flash",    # 快速经济
    "air": "glm-4-air",        # 轻量级
    "standard": "glm-4"        # 标准版
}

def chat_with_glm(prompt, model="plus", temperature=0.7, max_tokens=2000, system_prompt=None):
    """
    使用 GLM-4.7 进行对话

    参数：
        prompt: 用户提示词
        model: 模型选择（plus/flash/air/standard）
        temperature: 温度（0-1，越高越创意）
        max_tokens: 最大输出长度
        system_prompt: 系统提示词（可选）
    """

    model_name = MODELS.get(model, "glm-4-plus")

    # 构建消息
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    try:
        client = ZhipuAI(api_key=API_KEY)

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return {
            "success": True,
            "model": response.model,
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """命令行接口"""

    if len(sys.argv) < 2:
        print("=" * 80)
        print("GLM-4.7 通用助手")
        print("=" * 80)
        print()
        print("用法：")
        print("  python3 glm47_helper.py \"你的问题或任务\" [模型]")
        print()
        print("模型选项：")
        print("  plus     - GLM-4.7 Plus（最新最强，默认）")
        print("  flash    - GLM-4 Flash（快速经济）")
        print("  air      - GLM-4 Air（轻量级）")
        print("  standard - GLM-4（标准版）")
        print()
        print("示例：")
        print("  python3 glm47_helper.py \"帮我写一个Python排序算法\"")
        print("  python3 glm47_helper.py \"牙髓炎的诊断标准\" flash")
        print("  python3 glm47_helper.py \"分析这组数据的统计特征\" plus")
        print()
        print("=" * 80)
        sys.exit(1)

    # 解析参数
    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "plus"

    # 显示任务信息
    print("=" * 80)
    print(f"GLM-4.7 助手（模型：{model.upper()}）")
    print("=" * 80)
    print(f"任务：{prompt}")
    print("-" * 80)
    print()

    # 执行任务
    result = chat_with_glm(prompt, model=model)

    # 显示结果
    if result["success"]:
        print(result["content"])
        print()
        print("-" * 80)
        print(f"📊 Token 使用：{result['usage']['total_tokens']} "
              f"（输入：{result['usage']['prompt_tokens']}, "
              f"输出：{result['usage']['completion_tokens']}）")
        print(f"✅ 模型：{result['model']}")
    else:
        print(f"❌ 错误：{result['error']}")

    print("=" * 80)

if __name__ == "__main__":
    main()
