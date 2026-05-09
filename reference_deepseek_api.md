---
name: DeepSeek API Claude Code 集成配置
description: DeepSeek 原生 Anthropic 兼容接口配置，settings-deepseek.json 预置文件，切换方式
type: reference
originSessionId: 495ad864-1c24-4ef4-a5f0-92654dd55575
---
## DeepSeek API 切换方式

已创建预置配置文件 `C:\Users\Administrator\.claude\settings-deepseek.json`，切换时：

1. 退出 Claude Code
2. 将 `settings.json` 改名为 `settings-zhipu.json`（备份当前智谱配置）
3. 将 `settings-deepseek.json` 改名为 `settings.json`
4. 重启 Claude Code

切回智谱时反向操作即可。

## DeepSeek API 关键参数（来源：官方文档 2026-05）

| 设置项 | 值 |
|--------|-----|
| ANTHROPIC_BASE_URL | `https://api.deepseek.com/anthropic` |
| 主模型（Opus/Sonnet） | `deepseek-v4-pro[1m]` |
| 轻量模型（Haiku） | `deepseek-v4-flash` |
| Subagent 模型 | `deepseek-v4-flash` |

## 安全说明

- API Key 存放于 `settings-deepseek.json`（在 `~/.claude/` 目录，不入 Git）
- `api_config.json`（cc-github 仓库）中不含真实 Key，仅记录参数模板
- `settings.local.json` 中的权限规则在两套配置间通用，无需修改
