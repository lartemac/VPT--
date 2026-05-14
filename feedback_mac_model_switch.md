---
name: Mac模型切换注意事项
description: Mac端settings.local.json被Claude Code进程自动管理，切换模型时必须删除整个文件
type: feedback
---

## 规则

在 Mac 端切换 AI 后端（智谱/DeepSeek/MiMo）时，除了替换 `settings.json`，**必须删除整个 `settings.local.json` 文件**，不能只删除其中的 env 部分。

## Why: 2026-05-14 实测发现

- `settings.local.json` 是 Claude Code 进程**自动管理**的运行时缓存，不是静态配置文件
- Claude Code 进程持有该文件的文件描述符（lsof 可见），会持续读写
- 手动删除 env 部分后，进程会从内部状态自动恢复，env 固定指向首次配置的后端
- Windows 端不存在此问题（改名 settings.json 即可切换）

## How to apply

Mac 端切换步骤：
1. 退出 Claude Code
2. `mv settings.json settings-zhipu.json`（备份当前）
3. `mv settings-mimo.json settings.json`（替换为目标）
4. `rm settings.local.json`（删除整个文件，不是只删 env）
5. 重启 Claude Code → 会从新 settings.json 重建 settings.local.json
