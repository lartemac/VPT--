#!/usr/bin/env python3
"""
功能描述: 跨平台同步 Claude Code 全局配置
创建时间: 2026-03-31
创建系统: macOS/Windows 通用
平台检测: 自动检测平台并使用对应路径

用途:
在 macOS 和 Windows 之间同步 CLAUDE.md 全局配置文件
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ==================== 平台检测 ====================
IS_WINDOWS = os.name == 'nt'
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

# ==================== 路径配置 ====================
if IS_WINDOWS:
    # Windows 路径
    PROJECT_ROOT = Path(r"D:\cc-github")
    CLAUDE_CONFIG_DIR = Path.home() / ".claude"
elif IS_MACOS:
    # macOS 路径
    PROJECT_ROOT = Path.home() / "Desktop" / "VPT-初诊数据"
    CLAUDE_CONFIG_DIR = Path.home() / ".claude"
else:
    # Linux 路径（与 macOS 相同）
    PROJECT_ROOT = Path.home() / "VPT-初诊数据"
    CLAUDE_CONFIG_DIR = Path.home() / ".claude"

# 配置文件路径
SOURCE_CONFIG = PROJECT_ROOT / ".claude-sync" / "CLAUDE.md"
TARGET_CONFIG = CLAUDE_CONFIG_DIR / "CLAUDE.md"


def detect_platform():
    """检测当前平台"""
    if IS_WINDOWS:
        return "Windows"
    elif IS_MACOS:
        return "macOS"
    else:
        return "Linux"


def check_paths():
    """检查路径是否存在"""
    issues = []

    if not PROJECT_ROOT.exists():
        issues.append(f"项目根目录不存在: {PROJECT_ROOT}")

    if not CLAUDE_CONFIG_DIR.exists():
        issues.append(f"Claude配置目录不存在: {CLAUDE_CONFIG_DIR}")

    return issues


def get_file_mtime(filepath: Path) -> float:
    """获取文件修改时间"""
    if filepath.exists():
        return filepath.stat().st_mtime
    return 0


def sync_config(direction: str = "auto"):
    """
    同步配置文件

    direction:
    - "auto": 自动检测哪个文件更新（默认）
    - "to_local": 从项目同步到本地配置
    - "to_project": 从本地配置同步到项目
    """
    print("=" * 50)
    print(f"🔄 Claude Code 配置同步工具")
    print(f"📍 平台: {detect_platform()}")
    print(f"📂 项目目录: {PROJECT_ROOT}")
    print(f"📂 配置目录: {CLAUDE_CONFIG_DIR}")
    print("=" * 50)
    print()

    # 检查路径
    issues = check_paths()
    if issues:
        print("❌ 路径检查失败:")
        for issue in issues:
            print(f"   {issue}")
        return False

    # 检查文件是否存在
    source_exists = SOURCE_CONFIG.exists()
    target_exists = TARGET_CONFIG.exists()

    if not source_exists and not target_exists:
        print("❌ 配置文件都不存在，无法同步")
        return False

    # 自动检测方向
    if direction == "auto":
        source_time = get_file_mtime(SOURCE_CONFIG)
        target_time = get_file_mtime(TARGET_CONFIG)

        if source_time > target_time:
            direction = "to_local"
            print(f"📤 项目配置更新 ({datetime.fromtimestamp(source_time)})")
            print(f"   本地配置较旧 ({datetime.fromtimestamp(target_time)})")
            print(f"   → 将从项目同步到本地")
        elif target_time > source_time:
            direction = "to_project"
            print(f"📥 本地配置更新 ({datetime.fromtimestamp(target_time)})")
            print(f"   项目配置较旧 ({datetime.fromtimestamp(source_time)})")
            print(f"   → 将从本地同步到项目")
        else:
            print("✅ 配置文件已是最新，无需同步")
            return True

    print()

    # 执行同步
    try:
        if direction == "to_local":
            # 从项目同步到本地
            shutil.copy2(SOURCE_CONFIG, TARGET_CONFIG)
            print(f"✅ 已同步: {SOURCE_CONFIG}")
            print(f"   → {TARGET_CONFIG}")
            return True

        elif direction == "to_project":
            # 从本地同步到项目
            # 确保目标目录存在
            SOURCE_CONFIG.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(TARGET_CONFIG, SOURCE_CONFIG)
            print(f"✅ 已同步: {TARGET_CONFIG}")
            print(f"   → {SOURCE_CONFIG}")
            return True

    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False


def main():
    """主函数"""
    # 解析命令行参数
    direction = "auto"
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["to-local", "to_local"]:
            direction = "to_local"
        elif arg in ["to-project", "to_project"]:
            direction = "to_project"
        elif arg in ["-h", "--help", "help"]:
            print("用法:")
            print("  python sync_config.py           # 自动检测并同步")
            print("  python sync_config.py to-local  # 从项目同步到本地")
            print("  python sync_config.py to-project # 从本地同步到项目")
            return 0

    # 执行同步
    success = sync_config(direction)

    if success:
        print()
        print("💡 提示: 配置已同步，建议提交到 Git")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
