---
name: project-zhihu-mcp
description: 知乎开放平台API/MCP接入配置（全网搜索+知乎搜索），Bearer鉴权，已配置到三个settings文件
metadata:
  type: project
---

## 知乎开放平台 MCP 接入（2026-05-17）

已配置两个 MCP 服务到 Claude Code：
- **zhihu-search**：知乎站内搜索（SSE）
- **zhihu-global-search**：全网搜索（SSE）

### 配置位置
三个 settings 文件均已添加 `mcpServers` 配置（不影响模型切换）：
- `C:\Users\Administrator\.claude\settings.json`（mimo）
- `C:\Users\Administrator\.claude\settings-ds.json`（DeepSeek）
- `C:\Users\Administrator\.claude\settings-glm.json`（智谱 GLM）

### 关键信息
- **鉴权方式**：`Authorization: Bearer <access_secret>`
- **Access Secret**：已配置（存储在 settings 文件中，注意不要上传到公开仓库）
- **每日额度**：知乎搜索 1000 次、全网搜索 1000 次、热榜 10 次、直答 10 次
- **额度共享**：页面测试与 API Token 调用扣减同一额度池
- **count 限制**：知乎搜索最大 10，全网搜索最大 20
- **不加热榜和直答**：用户明确不需要

### MCP 端点
- 知乎搜索 SSE：`https://developer.zhihu.com/api/mcp/zhihu_search/v1/sse`
- 全网搜索 SSE：`https://developer.zhihu.com/api/mcp/global_search/v1/sse`

### 注意事项
- 知乎 MCP 与智谱 Coding Plan 的 100 次 MCP 额度互不相干
- MCP 工具是叠加式，不会替换模型自带的 WebSearch 等能力
- Access Secret 明文存储在配置文件中，避免公开泄露
