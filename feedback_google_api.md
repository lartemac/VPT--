---
name: Google Gemini API 不可作为 Claude Code 备用
description: Google Gemini API 代理方案已验证失败，不可用作 Claude Code 的备用 API 路径
type: feedback
originSessionId: 495ad864-1c24-4ef4-a5f0-92654dd55575
---
Google Gemini API 不可作为 Claude Code 备用路径，已放弃。

**Why:** 2026-05-10 验证，通过 gemini_proxy.py 代理脚本将 Anthropic 格式转为 Gemini 原生格式，切换后 Google API 拒绝请求，疑为 proxy/网络问题导致。中国大陆网络环境下 Gemini API 不可靠。

**How to apply:** 不要再尝试将 Google Gemini 作为 Claude Code 的 API 备用方案。当前唯一可用路径是智谱 GLM API（glm-5.1 主模型 / GLM-4.5-Air 轻量模型）。相关代理脚本 gemini_proxy.py 已于 2026-05-10 删除。
