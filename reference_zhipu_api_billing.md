---
name: 智谱API双通道计费机制
description: 智谱平台Coding Plan套餐与原生API独立计费，同一账户两条通道额度互不相通
type: reference
originSessionId: ba60bf23-fe51-4ee2-8253-1c55887a0e86
---
## 智谱API双通道计费机制（2026-04-22确认）

### 核心结论
智谱平台的API调用有**两条独立的计费通道**，额度互不相通：

| 通道 | 端点 | 用途 | 计费方式 |
|------|------|------|----------|
| 编码工具通道 | `/api/anthropic`（Anthropic兼容） | Claude Code、Cline等编码工具 | Coding Plan套餐额度（Lite/Pro/Max） |
| 原生API通道 | `/api/paas/v4/`（OpenAI兼容） | GPT Academic、FastGPT、自定义脚本 | 账户余额或资源包，独立计费 |

### 用户当前状态
- **套餐**: GLM Coding Plan Lite
- **编码工具通道**: 可用GLM-5.1、GLM-5-turbo、GLM-4.7等（套餐包含）
- **原生API通道**: 仅GLM-4-Flash免费可用，其他模型需充值或买资源包

### 充值方案（待执行）
- 往智谱账户充值后，原生API通道可按标准定价调用GLM-5.1等所有模型
- 充值后GPT Academic和FastGPT都可以使用最强模型
- 资源包页面目前最高只到GLM-4.7，但账户充值后可按定价调用GLM-5.1

### 两个API Key说明
- `YOUR_GLM_NATIVE_KEY` — 原生API通道Key
- `YOUR_GLM_CODING_KEY` — 编码工具通道Key
- 两个Key同属一个账户，但走不同通道，权限不同

### 客服确认原文要点
- "单独调用API是独立计费的，不可享用GLM Coding Plan套餐的额度"
- "套餐升级只影响编码工具中的使用体验，原生API调用是独立计费的，与套餐等级无关"
- "不需要升级套餐，只需购买资源包或账户充值即可调用GLM-5.1"

### How to apply:
- 配置GPT Academic/FastGPT时，用原生API Key，走`/api/paas/v4/`通道
- 配置Claude Code时，用编码工具Key，走`/api/anthropic`通道
- 如需在原生API用强模型，确保账户有余额
