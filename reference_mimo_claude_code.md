---
name: reference-mimo-claude-code
description: 小米MiMo API通过Anthropic兼容接口接入Claude Code的完整配置
metadata:
  type: reference
---

# 小米 MiMo API → Claude Code 配置

## 基本信息
- **平台**：Xiaomi MiMo API Open Platform (platform.xiaomimimo.com)
- **接入方式**：Anthropic 兼容协议
- **端点**：`https://api.xiaomimimo.com/anthropic/v1/messages`
- **认证**：`api-key` 头 或 `Authorization: Bearer`
- **创建日期**：2026-05-13

## 模型列表
| 模型 | 用途 | 上下文 | 思考模式 |
|------|------|--------|----------|
| `mimo-v2.5-pro` | 最强（Opus/Sonnet） | 1M（加[1m]后缀） | 默认启用 |
| `mimo-v2.5` | 次强 | 32K | 默认启用 |
| `mimo-v2-pro` | 上一代旗舰 | 131K | 默认启用 |
| `mimo-v2-omni` | 多模态 | 32K | 默认启用 |
| `mimo-v2-flash` | 轻量快速（Haiku/SubAgent） | 64K | 默认关闭 |

## Claude Code 配置（settings-mimo.json）
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.xiaomimimo.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-xxxxx或tp-xxxxx",
    "ANTHROPIC_MODEL": "mimo-v2.5-pro",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "mimo-v2-flash",
    "API_TIMEOUT_MS": "300000"
  }
}
```

## 两种付费模式
- **按量付费**：`sk-` 开头 Key，BASE_URL 用 `api.xiaomimimo.com`
- **Token Plan 套餐**：`tp-` 开头 Key，BASE_URL 用 `token-plan-cn.xiaomimimo.com`

## 注意事项
- 思考模式下多轮工具调用需保留 thinking 内容块（Claude Code 自动处理）
- `[1m]` 后缀启用百万 token 上下文
- 受影响的 Agent 产品列表中不包含 Claude Code，兼容性良好

## 相关文件
- `C:\Users\Administrator\.claude\settings-mimo.json` — MiMo 配置文件
- `C:\Users\Administrator\.claude\settings.json` — 当前 DeepSeek 配置
- `C:\Users\Administrator\.claude\settings-glm.json` — GLM 备用配置
