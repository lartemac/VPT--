---
name: DeepSeek API 配置与使用
description: DeepSeek V4 API 参数、模型列表、Anthropic兼容接口、Claude Code集成配置（2026-05-14更新）
type: reference
originSessionId: 495ad864-1c24-4ef4-a5f0-92654dd55575
---
## DeepSeek API 基本信息

| 设置项 | 值 |
|--------|-----|
| OpenAI base_url | `https://api.deepseek.com` |
| Anthropic base_url | `https://api.deepseek.com/anthropic` |
| 认证方式 | `Authorization: Bearer ${DEEPSEEK_API_KEY}` |

## 模型列表（2026-05-14更新）

| 模型名 | 用途 | 说明 |
|--------|------|------|
| `deepseek-v4-pro` | 旗舰模型（Opus/Sonnet） | 支持思考模式、reasoning_effort |
| `deepseek-v4-flash` | 轻量快速模型（Haiku/SubAgent） | 支持非思考模式 |
| `deepseek-chat` | 旧名称 | **2026/07/24 弃用**，对应 v4-flash 非思考模式 |
| `deepseek-reasoner` | 旧名称 | **2026/07/24 弃用**，对应 v4-flash 思考模式 |
| `deepseek-v4-flash-vision-exp` | 视觉模型（实验版） | 图片输入(JPEG/PNG/GIF/WebP)：描述/OCR/图表分析，2026-08-21上线 |

## 关键参数

| 参数 | 说明 |
|------|------|
| `thinking` | `{"type": "enabled"}` 启用思考模式 |
| `reasoning_effort` | `"high"` / `"medium"` / `"low"` 推理强度 |
| `stream` | `true` 流式 / `false` 非流式 |

## 已接入的 Agent 工具

Claude Code、GitHub Copilot、OpenCode 等均可直接使用 DeepSeek 作为后端模型。

## Claude Code 接入方式

### 方式一：环境变量（终端临时生效）

**Linux / Mac：**
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<你的 DeepSeek API Key>
export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

**Windows PowerShell：**
```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<你的 DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

配置完成后执行：
```bash
cd /path/to/my-project
claude
```

### 方式二：settings.json 持久化配置

将环境变量写入 `~/.claude/settings.json` 的 `env` 字段，重启 Claude Code 即生效。

**关键参数对照：**

| 设置项 | 值 |
|--------|-----|
| ANTHROPIC_BASE_URL | `https://api.deepseek.com/anthropic` |
| ANTHROPIC_MODEL | `deepseek-v4-pro[1m]` |
| ANTHROPIC_DEFAULT_OPUS_MODEL | `deepseek-v4-pro[1m]` |
| ANTHROPIC_DEFAULT_SONNET_MODEL | `deepseek-v4-pro[1m]` |
| ANTHROPIC_DEFAULT_HAIKU_MODEL | `deepseek-v4-flash` |
| CLAUDE_CODE_SUBAGENT_MODEL | `deepseek-v4-flash` |
| CLAUDE_CODE_EFFORT_LEVEL | `max` |

### 切换方式（Windows 改文件名）

预置配置文件 `C:\Users\Administrator\.claude\settings-deepseek.json`，切换时：

1. 退出 Claude Code
2. 将 `settings.json` 改名为 `settings-zhipu.json`（备份当前智谱配置）
3. 将 `settings-deepseek.json` 改名为 `settings.json`
4. 重启 Claude Code

切回智谱时反向操作即可。

## Anthropic SDK 调用示例

```bash
pip install anthropic
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=${YOUR_API_KEY}
```

```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="deepseek-v4-pro",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Hi, how are you?"}]}]
)
print(message.content)
```

注意：传入不支持的模型名时，后端自动映射到 `deepseek-v4-flash`。

## Anthropic API 兼容性

### 完全支持
max_tokens, stop_sequences, stream, system, temperature(0.0~2.0), top_p, tools(name/input_schema/description), tool_choice, thinking(仅budget_tokens忽略), output_config(仅effort)

### 忽略（不影响运行）
anthropic-beta, anthropic-version, container, mcp_servers, metadata, service_tier, top_k, cache_control, is_error

### 不支持（pro/flash 文本模型）
document, search_result, redacted_thinking, server_tool_use, web_search_tool_result, code_execution_tool_result, mcp_tool_use, mcp_tool_result, container_upload

> 注：`image` 现已由视觉模型 `deepseek-v4-flash-vision-exp` 支持（见 reference_deepseek_vision.md）；Web Search 现由 DeepSeek 原生支持。

## 安全说明

- API Key 存放于 `settings.json` 或 `settings-deepseek.json`（在 `~/.claude/` 目录，不入 Git）
- `api_config.json`（cc-github 仓库）中不含真实 Key，仅记录参数模板
- `settings.local.json` 中的权限规则在两套配置间通用，无需修改
