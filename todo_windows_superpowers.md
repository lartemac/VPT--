---
name: Windows待办：安装superpowers插件
description: Windows端Claude Code需更新marketplace并安装superpowers插件
type: project
---

## 待办任务（切换到 Windows 后执行）

1. `/plugin marketplace update`
2. `/plugin install superpowers@claude-plugins-official`
3. `/reload-plugins`
4. 验证 14 个 superpowers skills 是否自动加载

## Mac 端已完成（2026-05-14）
- superpowers v5.1.0 已安装成功
- 14 个 skills 通过 SessionStart hook 自动生效
- brainstorming / writing-plans / test-driven-development / systematic-debugging 等全部可用

## Why: Mac/Windows 两端保持一致的 superpowers 插件配置
## How to apply: 切换到 Windows 后第一时间执行上述命令
