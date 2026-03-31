#!/usr/bin/env python3
"""
功能描述: 自动获取智谱AI最新可用模型
创建时间: 2026-03-31
创建系统: macOS
平台检测: 自动检测 Windows/macOS/Linux

用途:
1. 查询智谱AI最新可用模型列表
2. 自动更新配置文件中的模型版本
3. 确保始终使用最新模型
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 平台检测
IS_WINDOWS = os.name == 'nt'

# 配置文件路径
if IS_WINDOWS:
    CONFIG_PATH = Path(r"D:\cc-github\api_config.json")
else:
    CONFIG_PATH = Path.home() / "Desktop" / "VPT-初诊数据" / "api_config.json"

# API配置
API_BASE_URL = "https://open.bigmodel.cn/api/anthropic/v1/models"


def get_api_key():
    """从环境变量或配置文件获取API密钥"""
    # 优先使用环境变量
    api_key = os.environ.get("ZHIPU_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")

    if api_key:
        return api_key

    # 从配置文件读取
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("glm", {}).get("api_key", "")

    return None


def fetch_latest_models(api_key: str) -> dict:
    """获取最新可用模型列表"""
    import urllib.request
    import urllib.error

    req = urllib.request.Request(
        API_BASE_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        # 解析模型列表
        models = {}
        for model in data.get("data", []):
            model_id = model.get("id")
            display_name = model.get("display_name", model_id)
            created_at = model.get("created_at", "")

            models[model_id] = {
                "id": model_id,
                "display_name": display_name,
                "created_at": created_at
            }

        return models

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
        return {}
    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e.reason}")
        return {}
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return {}


def get_latest_model(models: dict) -> str:
    """获取最新模型ID（按创建时间排序）"""
    if not models:
        return "glm-5.1"  # 默认值

    # 按创建时间排序，返回最新的
    sorted_models = sorted(
        models.items(),
        key=lambda x: x[1].get("created_at", ""),
        reverse=True
    )

    return sorted_models[0][0] if sorted_models else "glm-5.1"


def update_config(latest_model: str):
    """更新配置文件中的最新模型"""
    if not CONFIG_PATH.exists():
        print(f"⚠️  配置文件不存在: {CONFIG_PATH}")
        return False

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        # 更新最新模型
        config["glm"]["latest_model"] = latest_model
        config["glm"]["models"]["latest"]["model_name"] = latest_model
        config["updated"] = datetime.now().strftime("%Y-%m-%d")

        # 写回文件
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"✅ 配置已更新: 最新模型 = {latest_model}")
        return True

    except Exception as e:
        print(f"❌ 更新配置失败: {e}")
        return False


def main():
    """主函数"""
    print("🔍 查询智谱AI最新模型...")
    print("-" * 40)

    # 获取API密钥
    api_key = get_api_key()
    if not api_key:
        print("❌ 未找到API密钥")
        print("   请设置环境变量 ZHIPU_API_KEY 或检查配置文件")
        return 1

    # 获取最新模型列表
    models = fetch_latest_models(api_key)

    if not models:
        print("❌ 无法获取模型列表")
        return 1

    # 显示所有可用模型
    print("\n📋 可用模型列表:")
    print("-" * 40)
    for model_id, info in sorted(models.items(), reverse=True):
        created = info.get("created_at", "未知")[:10]
        print(f"  • {info['display_name']:20} ({model_id}) - {created}")

    # 获取最新模型
    latest = get_latest_model(models)
    print("-" * 40)
    print(f"\n🆕 最新模型: {latest}")

    # 询问是否更新配置
    if len(sys.argv) > 1 and sys.argv[1] in ["-y", "--yes"]:
        # 自动更新
        update_config(latest)
    else:
        # 交互式
        response = input(f"\n是否更新配置文件到 {latest}? (y/n): ").strip().lower()
        if response in ["y", "yes", "是"]:
            update_config(latest)
        else:
            print("⏭️  已取消更新")

    return 0


if __name__ == "__main__":
    sys.exit(main())
