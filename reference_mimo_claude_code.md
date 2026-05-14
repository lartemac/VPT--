---
name: reference-mimo-claude-code
description: 小米MiMo API完整文档：模型列表、API格式、Claude Code配置、兼容性细节（2026-05-14更新）
type: reference
---

# 小米 MiMo API 完整文档

## 基本信息
- **平台**：Xiaomi MiMo API Open Platform (platform.xiaomimimo.com)
- **登录方式**：小米账号（id.mi.com 注册）
- **API Key 获取**：控制台 → API Keys
- **兼容格式**：OpenAI API + Anthropic API

## 接入端点

| 格式 | base_url |
|------|----------|
| OpenAI | `https://api.xiaomimimo.com/v1` |
| Anthropic | `https://api.xiaomimimo.com/anthropic` |

## 模型列表
| 模型 | 用途 | 上下文 | 思考模式 |
|------|------|--------|----------|
| `mimo-v2.5-pro` | 最强（Opus/Sonnet） | 1M（加[1m]后缀） | 默认启用 |
| `mimo-v2.5` | 次强 | 32K | 默认启用 |
| `mimo-v2-pro` | 上一代旗舰 | 131K | 默认启用 |
| `mimo-v2-omni` | 多模态 | 32K | 默认启用 |
| `mimo-v2-flash` | 轻量快速（Haiku/SubAgent） | 64K | 默认关闭 |

## 两种付费模式

| 模式 | API Key 格式 | BASE_URL（Anthropic） | 适用场景 |
|------|-------------|----------------------|---------|
| 按量付费 | `sk-xxxxx`（控制台→API Keys 创建） | `https://api.xiaomimimo.com/anthropic` | 轻度使用，按量计费 |
| Token Plan | `tp-xxxxx`（订阅管理获取） | `https://token-plan-cn.xiaomimimo.com/anthropic` | 固定订阅费，按套餐限量调用 |

注意：两种模式的 BASE_URL 不同，需根据 Key 类型选择对应的地址。

## 推荐系统提示词
- 中文：`你是MiMo（中文名称也是MiMo），是小米公司研发的AI智能助手。今天的日期：{date} {week}，你的知识截止日期是2024年12月。`
- 英文：`You are MiMo, an AI assistant developed by Xiaomi. Today's date: {date} {week}. Your knowledge cutoff date is December 2024.`

## API 调用示例

### OpenAI 格式（Python）
```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_KEY", base_url="https://api.xiaomimimo.com/v1")
completion = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[...],
    max_completion_tokens=1024,
    temperature=1.0, top_p=0.95, stream=False,
    frequency_penalty=0, presence_penalty=0
)
```

### Anthropic 格式（Python）
```python
from anthropic import Anthropic
client = Anthropic(api_key="YOUR_KEY", base_url="https://api.xiaomimimo.com/anthropic")
message = client.messages.create(
    model="mimo-v2.5-pro",
    max_tokens=1024, system="...", messages=[...],
    top_p=0.95, stream=False, temperature=1.0
)
```

### 认证方式
- Header: `api-key: YOUR_KEY` 或 `Authorization: Bearer YOUR_KEY`

## 思考模式多轮工具调用
- 模型返回 `reasoning_content` + `tool_calls`
- 后续请求需保留所有历史 `reasoning_content` 以获得最佳表现

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

## 模型超参

### temperature 和 top_p 默认值与范围

| 模型 | temperature 默认 | temperature 范围 | top_p 默认 | top_p 范围 |
|------|-----------------|-----------------|------------|------------|
| mimo-v2.5-pro / mimo-v2-pro | 1.0 | [0, 1.5] | 0.95 | [0.01, 1.0] |
| mimo-v2.5 / mimo-v2-omni | 1.0 | [0, 1.5] | 0.95 | [0.01, 1.0] |
| mimo-v2-flash | 0.3 | [0, 1.5] | 0.95 | [0.01, 1.0] |
| mimo-tts 系列 | 0.6 | [0, 1.5] | 0.95 | [0.01, 1.0] |

### 思考模式限制
- mimo-v2.5-pro 和 mimo-v2.5 在思考模式下**不支持自定义 temperature**，强制使用 1.0

### mimo-v2-flash 按任务推荐值

| 任务类型 | temperature | top_p |
|---------|-------------|-------|
| AI 编程 | 0.3 | 0.95 |
| 工具调用 | 0.3 | 0.95 |
| 通用问答 | 0.8 | 0.95 |
| 创意写作 | 0.8 | 0.95 |
| 前端网页开发 | 0.8 | 0.95 |
| 数学推理 | 1.0 | 0.95 |

### 其他模型（v2.5-pro / v2.5 / v2-pro / v2-omni）
- 所有任务统一推荐：temperature=1.0, top_p=0.95

## Anthropic API 兼容详情

### 请求地址
`https://api.xiaomimimo.com/anthropic/v1/messages`

### 认证方式（二选一）
- `api-key: $MIMO_API_KEY`
- `Authorization: Bearer $MIMO_API_KEY`

### 请求参数

| 参数 | 必选 | 说明 |
|------|------|------|
| messages | 是 | 消息列表，每条含 role(user/assistant) + content(string/array) |
| model | 是 | mimo-v2.5-pro / mimo-v2.5 / mimo-v2-pro / mimo-v2-omni / mimo-v2-flash |
| max_tokens | 否 | 最大输出 token，flash 默认65536，v2.5-pro/v2-pro 默认131072，v2.5/omni 默认32768，范围[1,131072] |
| stop_sequences | 否 | 自定义停止序列 |
| stream | 否 | 流式输出，默认 false |
| system | 否 | 系统提示词（string 或 array） |
| temperature | 否 | 采样温度，flash 默认0.3，其他默认1.0，范围[0,1.5] |
| top_p | 否 | 核采样阈值，默认0.95，范围[0.01,1.0] |
| thinking | 否 | 扩展思维配置，含 type(enabled/disabled)。flash 默认 disabled，其他默认 enabled |
| tools | 否 | 工具定义，含 name/description/input_schema |
| tool_choice | 否 | 工具选择，目前仅支持 type=auto，含 disable_parallel_tool_use |

### 非流式响应字段

| 字段 | 说明 |
|------|------|
| id | 对话唯一标识 |
| type | 固定 "message" |
| role | 固定 "assistant" |
| content | 内容块数组（text/thinking/tool_use） |
| model | 模型名称 |
| stop_reason | end_turn / max_tokens / tool_use / content_filter / repetition_truncation |
| usage | input_tokens + output_tokens + cache_read_input_tokens |

### 流式响应事件

| 事件 | 说明 |
|------|------|
| message_start | 消息开始（含 id/type/role/model） |
| content_block_start | 内容块开始（含 index + content_block） |
| content_block_delta | 增量数据（text_delta / thinking_delta / input_json_delta） |
| content_block_stop | 内容块结束 |
| message_delta | 消息级别增量（stop_reason / usage） |
| message_stop | 消息结束 |

## 视频理解

### 支持模型
仅 `mimo-v2.5` 和 `mimo-v2-omni`

### 视频传入方式
| 方式 | 说明 | 大小限制 |
|------|------|---------|
| URL | 公网可访问的视频地址 | 单个 ≤ 300MB |
| Base64 | 编码字符串（需带前缀 `data:{MIME_TYPE};base64,`） | 单个 ≤ 50MB |

### 支持格式
MP4, MOV, AVI, WMV（格式变种较多，建议测试验证）

### 调用方式（仅 OpenAI 格式）
```json
{"type": "video_url", "video_url": {"url": "https://..."}, "fps": 2, "media_resolution": "default"}
```

### 精细度控制参数
| 参数 | 说明 | 默认值 | 范围 |
|------|------|--------|------|
| fps | 每秒抽帧数，越高时序越精细 | 2 | [0.1, 10] |
| media_resolution | 单帧分辨率档次 | default | default / max |

### Token 计算
- video_tokens：根据时长、分辨率、fps、media_resolution 计算（公式较复杂，见官方文档）
- audio_tokens：音频秒数 × 6.25
- 实际用量以 API 响应 `usage.prompt_tokens_details.video_tokens` / `audio_tokens` 为准

### 限制
- 支持多视频输入，受上下文长度限制
- 不支持本地文件直接上传
- 最大抽帧数 2048

## 音频理解

### 支持模型
仅 `mimo-v2.5` 和 `mimo-v2-omni`

### 音频传入方式
| 方式 | 说明 | 大小限制 |
|------|------|---------|
| URL | 公网可访问的音频地址 | 单个 ≤ 100MB |
| Base64 | 编码字符串（需带前缀 `data:{MIME_TYPE};base64,`） | 单个 ≤ 50MB |

### 支持格式
MP3, WAV, FLAC, M4A, OGG（格式变种较多，建议测试验证）

### 调用方式（仅 OpenAI 格式）
```json
{"type": "input_audio", "input_audio": {"data": "https://...或data:{MIME};base64,..."}}
```

### Token 计算
- 总 Tokens ≈ 音频时长（秒）× 6.25
- 实际用量以 API 响应 `usage.prompt_tokens_details.audio_tokens` 为准

### 限制
- 支持多音频输入，受上下文长度限制
- 不支持本地文件直接上传

## 图片理解

### 支持模型
仅 `mimo-v2.5` 和 `mimo-v2-omni`

### 图片传入方式
| 方式 | 说明 | 大小限制 |
|------|------|---------|
| URL | 公网可访问的图片地址 | 单张 ≤ 50MB |
| Base64 | 编码字符串（需带前缀 `data:{MIME_TYPE};base64,`） | 单张 ≤ 50MB |

### 支持格式
JPEG, PNG, GIF, WebP, BMP

### 多图输入
- 支持同时传入多张图片（URL + Base64 可混用）
- 图片数量受模型上下文长度限制

### OpenAI 格式（URL）
```json
{"type": "image_url", "image_url": {"url": "https://..."}}
```

### Anthropic 格式（URL）
```json
{"type": "image", "source": {"type": "url", "url": "https://..."}}
```

### Anthropic 格式（Base64）
```json
{"type": "image", "source": {"type": "base64", "media_type": "{MIME_TYPE}", "data": "$BASE64_IMAGE"}}
```

### Token 计算规则
- PATCH_SIZE=16, SPATIAL_MERGE_SIZE=2, IMAGE_MIN_PIXELS=8192, IMAGE_MAX_PIXELS=8388608
- 实际用量以 API 响应中的 `usage.prompt_tokens_details.image_tokens` 为准
- 估算公式：`num_tokens = (grid_h * grid_w) // 4`

## 联网搜索插件

### 前置条件
- 需在控制台→插件管理开通「联网服务插件」
- **仅支持 OpenAI API 格式**，暂不支持 Anthropic API 协议

### 支持模型
mimo-v2.5-pro / mimo-v2.5 / mimo-v2-pro / mimo-v2-omni / mimo-v2-flash

### 核心能力
- 两种模式：强制搜索（force_search=true）和意图识别（模型自主判断）
- 流式首包返回所有搜索来源
- 可与自定义 Function/工具混合调用

### 调用参数（tools 中 type="web_search"）

| 参数 | 说明 |
|------|------|
| max_keyword | 一轮搜索最大关键词数量，控制调用频次与成本 |
| force_search | true 强制联网，false 由模型判断 |
| limit | 搜索结果数量限制 |
| user_location | 用户位置（含 country/region/city），提升搜索精度 |

### 计费
- 联网搜索工具：国内 ¥25/1000次，海外 $5/1000次
- 一轮搜索会按 max_keyword 数量发起多次关键词搜索，每次计费
- 搜索内容拼接到提示词中，额外消耗模型 input token

### 响应格式
- 搜索来源通过 `annotations` 字段返回（含 url/title/summary/site_name/publish_time/logo_url）
- 用量统计在 `usage.web_search_usage` 中（tool_usage + page_usage）

## 注意事项

### 思考模式多轮工具调用（重要）
- **必须回传 reasoning_content**：Agent 类产品在多轮会话中开启思考模式且历史存在工具调用时，后续轮次回传的 assistant 消息必须包含完整 reasoning_content，否则 API 返回 400 错误
- 缺失 reasoning_content 会导致：指令遵循下降、幻觉增多
- **Claude Code 自动处理此逻辑**，无需手动操作

### 受影响的 Agent 产品
TRAE、Cursor、Roo Code、Codex、GitHub Copilot CLI、Zed、AutoGen、Goose、OpenClaw、OpenCode、Kilo Code（后三者仅在使用 Anthropic 协议时受影响）

### 其他限制
- mimo-v2.5-pro 和 mimo-v2.5 思考模式下 temperature 强制 1.0
- tool_choice 目前仅支持 auto，非 auto 值会被忽略
- 联网搜索暂不支持 Anthropic API 协议，仅限 OpenAI 格式
- `[1m]` 后缀启用百万 token 上下文
- Claude Code 兼容性良好，不在受影响列表中

## 相关文件
- `~/.claude/settings-mimo.json` — MiMo 配置文件
- `~/.claude/settings.json` — 当前配置
- `~/.claude/settings-deepseek.json` — DeepSeek 配置
