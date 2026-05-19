---
name: windows-superpowers
description: Windows端superpowers插件安装记录（已完成）
metadata: 
  node_type: memory
  type: reference
  originSessionId: bd1f7d4f-8c33-407b-9a5e-2ea8e557ccde
---

## Windows端 superpowers v5.1.0 安装完成（2026-05-20）

### 安装步骤
1. 问题：`/plugin marketplace update` 无输出，`/plugin install superpowers` 报 "not found"
2. 原因：未注册任何 marketplace（`claude plugin marketplace list` 返回空）
3. 解决：
   - `claude plugin marketplace add https://github.com/anthropics/claude-plugins-official`
   - `claude plugin install superpowers`
4. 状态：v5.1.0 已安装并启用，重启后生效

### Mac/Windows 双端均已完成
- Mac端：2026-05-14 完成
- Windows端：2026-05-20 完成
- 两端版本一致：v5.1.0
