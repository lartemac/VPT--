#!/bin/bash
# 同步 Claude Code 全局配置文件
# 从项目文件夹同步到系统配置位置 (macOS/Linux)

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_CONFIG="$SCRIPT_DIR/CLAUDE-global.md"
CONFIG_DIR="$HOME/.claude"
SYSTEM_CONFIG="$CONFIG_DIR/CLAUDE.md"

echo "正在同步 Claude Code 配置文件..."
echo

# 检查项目配置文件是否存在
if [ ! -f "$PROJECT_CONFIG" ]; then
    echo "错误: 项目配置文件不存在: $PROJECT_CONFIG"
    exit 1
fi

# 创建配置目录（如果不存在）
mkdir -p "$CONFIG_DIR"

# 备份现有配置
if [ -f "$SYSTEM_CONFIG" ]; then
    echo "备份现有配置..."
    cp "$SYSTEM_CONFIG" "$SYSTEM_CONFIG.backup"
fi

# 复制配置文件
echo "从项目同步配置到系统..."
cp "$PROJECT_CONFIG" "$SYSTEM_CONFIG"

echo
echo "✓ 配置文件同步完成！"
echo
echo "源文件: $PROJECT_CONFIG"
echo "目标文件: $SYSTEM_CONFIG"
echo
