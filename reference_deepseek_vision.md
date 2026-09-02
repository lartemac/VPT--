---
name: deepseek-vision-script
description: DeepSeek 视觉模型 deepseek-v4-flash-vision-exp + vision.py 脚本（主对话自动看图）
type: reference
---

# DeepSeek 视觉模型 + vision.py 脚本

## 模型信息（deepseek-v4-flash-vision-exp）
- 上线：2026-08-21（实验版 exp），2026-08-31 开源（MIT）
- 能力：图片输入 → 描述图片 / 识别截图文字(OCR) / 分析图表
- 格式：JPEG、PNG、GIF、WebP
- 文本能力与 V4-Flash 持平，支持工具调用（Agent 定位）
- 计费：图片最多 384 token/张，价格与 V4-Flash 一致
- 接口：OpenAI 兼容（chat/completions）+ Anthropic 兼容（/messages 用 image 块）

## vision.py 脚本
- 位置：`D:\cc-github\vision.py`
- 用法：`python vision.py "图片路径或URL" "问题"`
- 密钥：同目录 `vision_secret.json`（已 gitignore，不上传）
- 机制：主对话(deepseek-v4-pro)无视觉，通过 Bash 调此脚本把图片交给 vision 模型，拿回文字结果
- 测试通过（2026-09-02）：VPT/RCT 生存率柱状图，准确读出标题/数据/颜色/差值/结论

## 触发规则（已写入 CLAUDE.md）
当用户要求「看图/OCR/图表分析」时，自动用 Bash 调 vision.py，不尝试自己直接看图。

## 联网搜索现状（2026-09-02 更新）
- DeepSeek Web Search 现已可用（Claude Code 内置，模型自动触发），但产生额外 Token 费
- 知乎 API（zhihu_mcp/search.py）免费 1000 次/天，仍为默认优先
- 结论：日常随手搜用 Web Search，科研/精准/免费用知乎 API

## Mac 端同步待办（跨平台）
vision.py 会随 Git 同步到 Mac，但以下需在 Mac 端手动补：
1. 创建 `~/cc-github/vision_secret.json`，内容 `{"api_key":"<DeepSeek Key>"}`（密钥不入 Git，需手动放）
2. 在 Mac 的 `~/.claude/CLAUDE.md` 加同样的「图片处理规则」（CLAUDE.md 不入 Git，不同步）
3. 知乎搜索同理需 Mac 端 `zhihu_mcp/zhihu_secret.json`
