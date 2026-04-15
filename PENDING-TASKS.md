# 待办任务：Windows 电脑安全修复

> **触发条件**：在 Windows 电脑上启动 Claude Code 并读取 memory 后，发现此文件，立即执行
> **优先级**：高（安全相关）
> **创建时间**：2026-04-15（macOS）

---

## 背景

macOS 上已完成 API Key 安全修复（移除硬编码、git 历史清理）。Windows 电脑的 git 仓库代码已通过 pull 更新，但以下本地配置文件（不在 git 中）仍使用旧密钥：

- 旧 GLM API Key：`232b1236880a4699957a592bed87aad2.3gYzmvvyIQN98DZb`（已失效）
- 新 GLM API Key：在 macOS 的 `~/Desktop/VPT-初诊数据/api_config.json` 中
- 旧 Tushare Token：`e63bfa9a805512aca05dcca1df35d035618f2aba8fc946a36a13b94e`（需确认是否更换）

---

## 任务清单

### 1. 拉取最新代码
```bash
cd D:\cc-github
git pull origin main
```
确认 Python 脚本已使用环境变量读取 API Key。

### 2. 更新 Claude Code 本地配置（settings.json）
- **文件位置**：`C:\Users\Administrator\.claude\settings.json`
- **需要替换**：`ANTHROPIC_AUTH_TOKEN` 的值
- **新值**：从 macOS 的 `api_config.json` 中获取，或让用户提供
- **同时确认**：`ANTHROPIC_BASE_URL` 是否正确

### 3. 更新本地 api_config.json
- **文件位置**：`D:\cc-github\api_config.json`（在 .gitignore 中，不会自动同步）
- **需要确认**：api_key 字段是否为新密钥
- **如果不是**：更新为新密钥

### 4. 检查 Windows 本地其他文件
搜索 Windows 本地（非 git 仓库）是否还有旧密钥：
```powershell
# 搜索用户目录下的配置文件
Select-String -Path "C:\Users\Administrator\.claude\*" -Pattern "232b1236" -ErrorAction SilentlyContinue
Select-String -Path "D:\BigA\*.py" -Pattern "232b1236" -ErrorAction SilentlyContinue
```

### 5. 验证 Python 脚本可用性
```bash
cd D:\cc-github
python glm47_helper.py --test
```

### 6. ⚠️ 删除智谱控制台旧 API Key（最后一步）
- **前提**：确认步骤 1-5 全部完成，新 Key 在两台电脑上均正常工作
- **操作**：登录智谱开放平台控制台 → API Keys 管理 → 删除旧 Key
- **旧 Key 前缀**：`232b1236...`
- **原因**：旧 Key 曾泄露在 GitHub 公开仓库中，即使已清理 git 历史，仍存在被缓存/索引的风险
- **建议**：删除后在保留的新 Key 上添加备注「2026-04-15 创建，替换泄露旧 Key」

---

## 完成后

1. 在 memory.md 的 PENDING TASKS 部分标记为已完成
2. 删除此文件（或移动到 archive）

---

## 重要密钥对照（仅用于迁移，完成后应从本文档移除）

| 用途 | 旧值前缀 | 新值位置 |
|------|----------|---------|
| GLM API | `232b1236...` | api_config.json（macOS 端查看） |
| Tushare | `e63bfa9a...` | 环境变量或 api_config.json |
| ANTHROPIC_AUTH_TOKEN | 旧值 | settings.json（macOS 端查看） |

**安全提示**：迁移完成后，将此文件中的密钥前缀也清除。
