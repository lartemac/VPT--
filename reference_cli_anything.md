---
name: CLI-Anything 备用
description: 33.4k star CLI工具封装器（Apache 2.0），源码在D:\CLI-Anything，待需要时安装为Claude Code插件
type: reference
originSessionId: ae47c039-7b09-453e-bdcb-c20fcda83775
---
## CLI-Anything（2026-05-05 评估记录）

### 基本信息
- **GitHub**: https://github.com/HKUDS/CLI-Anything
- **Star**: 33.4k
- **协议**: Apache 2.0
- **源码位置**: `D:\CLI-Anything`
- **状态**: 已克隆，未安装为插件

### 功能
将任何命令行软件封装为 AI Agent 可调用的工具（CLI wrapper），支持 35+ 软件的现成封装：
- ffmpeg（视频处理）、pandoc（文档转换）、git、docker、npm、python 等

### 安装方式（待需要时执行）
```bash
# 方式1: Claude Code 插件市场（如果可用）
/plugin marketplace add HKUDS/CLI-Anything

# 方式2: 手动复制
cp -r D:\CLI-Anything\cli-anything-plugin ~/.claude/plugins/cli-anything/
```

### 评估结论
- 安全：Apache 2.0，纯CLI封装，无网络风险
- 高效：自动生成CLI wrapper，免去手写API调用
- 建议：记录备用，当需要自动化操作某个软件时再安装

## Why: 用户喜欢自动化，但当前无直接需求，先记录备用
## How to apply: 当用户需要自动化操作某个CLI软件（如ffmpeg/pandoc等）时，安装此插件
