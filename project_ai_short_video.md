---
name: AI短视频自动生成工具
description: 4个开源AI短视频工具对比：MoneyPrinterTurbo(56k星)、Pixelle-Video(11k星)、火宝短剧(11k星)、NarratoAI(9k星)，用户需求是云端/API方式、不本地部署
type: project
---

## AI短视频自动生成工具（2026-05-06 调研）

### 用户需求
- 只给出 idea 或主要观点，全自动生成短视频
- 不本地部署，通过 API 或云端方式
- 越自动化越好
- 免费优先

### 工具对比

#### 1. MoneyPrinterTurbo（最推荐）
- GitHub: https://github.com/harry0703/MoneyPrinterTurbo
- Stars: 56,782 | MIT 协议 | Python | 活跃更新
- 输入主题/关键词 → 全自动生成：文案+视频素材+字幕+配音+BGM+合成
- 不依赖本地GPU，视频素材来自网络高清无版权素材
- 有 Google Colab 一键运行（云端免费）
- LLM 用 DeepSeek（注册送额度）成本极低
- 支持 Web界面 + API
- 支持批量生成、中英文
- 不足：素材是网络片段拼接，非AI原创画面

#### 2. Pixelle-Video
- GitHub: https://github.com/AIDC-AI/Pixelle-Video
- Stars: 11,767 | Apache 2.0 | Python | AIDC-AI（阿里系）
- AI生成原创配图/视频（FLUX、WAN 2.1等），画面质量更高
- 扩展：数字人口播、图生视频、动作迁移
- 云端方案：LLM用通义千问API + 图像用RunningHub（付费）
- Windows一键整合包
- 不足：完全云端需RunningHub付费，配置较复杂

#### 3. 火宝短剧 huobao-drama
- GitHub: https://github.com/chatfire-AI/huobao-drama
- Stars: 11,554 | TypeScript
- 专注短剧生成（一句话→完整短剧）
- 适合剧情类短视频，不适合知识科普类

#### 4. NarratoAI
- GitHub: https://github.com/linyqh/NarratoAI
- Stars: 9,148 | Python
- 专注影视解说：上传视频→AI自动写解说词+剪辑
- 适合影视解说类账号

### 推荐方案
- **首选 MoneyPrinterTurbo**：Colab云端+DeepSeek免费额度=零成本
- **高质量画面需求选 Pixelle-Video**：AI原创画面但需付费
- 用户准备制作短视频时提醒使用

## Why: 用户有制作短视频的需求，偏好免费、云端、自动化方案
## How to apply: 当用户提到要制作短视频时，推荐MoneyPrinterTurbo作为首选工具，协助配置和运行
