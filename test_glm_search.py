#!/usr/bin/env python3
"""
测试智谱 GLM-4.7 API 是否支持网络搜索功能
测试时间：2026-01-13
"""

import sys
import json

def test_glm_search():
    """测试 GLM-4 搜索功能"""

    print("=" * 80)
    print("智谱 GLM-4.7 API 搜索功能测试")
    print("=" * 80)
    print()

    # API Key（从 PPTGen 项目配置中获取）
    API_KEY = "232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb"

    print(f"[1/5] 使用 API Key: {API_KEY[:20]}...")
    print()

    try:
        # 导入 zhipuai 库
        print("[2/5] 导入 zhipuai 库...")
        from zhipuai import ZhipuAI
        print("✓ zhipuai 库导入成功")
        print()

        # 初始化客户端
        print("[3/5] 初始化 GLM 客户端...")
        client = ZhipuAI(api_key=API_KEY)
        print("✓ 客户端初始化成功")
        print()

        # 测试1：尝试使用 web_search 工具
        print("[4/5] 测试1：尝试调用 web_search 工具...")
        print("-" * 80)

        try:
            response = client.chat.completions.create(
                model="glm-4-flash",  # 使用快速模型
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个搜索助手。"
                    },
                    {
                        "role": "user",
                        "content": "请搜索：中信银行留学信用卡年费 2026"
                    }
                ],
                tools=[
                    {
                        "type": "web_search",
                        "web_search": {
                            "search_query": "中信银行留学信用卡年费 2026",
                            "top_k": 3
                        }
                    }
                ]
            )

            print("✓ API 调用成功！")
            print()
            print("响应内容：")
            print("-" * 80)
            print(response.choices[0].message.content)
            print("-" * 80)
            print()
            print("✓✓✓ web_search 工具调用成功！")
            web_search_supported = True

        except Exception as e:
            print(f"✗ web_search 工具调用失败")
            print(f"错误信息: {str(e)}")
            web_search_supported = False

        print()

        # 测试2：不使用工具，直接提问（测试基础功能）
        print("[5/5] 测试2：基础对话功能（不使用工具）...")
        print("-" * 80)

        try:
            response2 = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {
                        "role": "user",
                        "content": "你好，请用一句话介绍你自己。"
                    }
                ]
            )

            print("✓ 基础对话功能正常")
            print()
            print("GLM-4 回复：")
            print(f"  {response2.choices[0].message.content}")
            basic_chat_ok = True

        except Exception as e:
            print(f"✗ 基础对话失败")
            print(f"错误信息: {str(e)}")
            basic_chat_ok = False

        print()
        print("=" * 80)
        print("测试结论")
        print("=" * 80)
        print()
        print(f"web_search 工具支持: {'✓ 是' if web_search_supported else '✗ 否'}")
        print(f"基础对话功能: {'✓ 正常' if basic_chat_ok else '✗ 异常'}")
        print()

        if web_search_supported:
            print("🎉 结论：GLM-4.7 API 支持 web_search 工具，可用于网络搜索！")
            print()
            print("建议：")
            print("  1. 可以创建 GLM 搜索工具脚本")
            print("  2. 中文搜索任务优先使用 GLM")
            print("  3. Claude WebSearch 达到上限时作为备选")
        else:
            print("⚠️  结论：GLM-4.7 API 不支持 web_search 工具")
            print()
            print("可能的原因：")
            print("  1. API 参数格式不正确")
            print("  2. 当前模型版本不支持 web_search")
            print("  3. 需要 API 权限或特殊配置")
            print()
            print("建议：")
            print("  1. 查看 GLM 官方文档确认 web_search 支持情况")
            print("  2. 尝试其他模型（如 glm-4-plus）")
            print("  3. 联系智谱 AI 客服确认")

        print()
        print("=" * 80)

        return web_search_supported

    except ImportError as e:
        print(f"✗ 错误：未安装 zhipuai 库")
        print(f"  请运行: pip3 install zhipuai")
        return False
    except Exception as e:
        print(f"✗ 测试过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_glm_search()
    sys.exit(0 if success else 1)
