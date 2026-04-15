# 待办任务：Windows 电脑安全修复 + 智能启动器配置

> **触发条件**：在 Windows 电脑上启动 Claude Code 并读取 memory 后，发现此文件，立即执行
> **优先级**：高（安全相关）
> **创建时间**：2026-04-15（macOS）

---

## 背景

macOS 上已完成：
1. API Key 安全修复（移除硬编码、git 历史清理）
2. Claude Code 智能启动器（自动检测 API → 智谱限额时切换 Gemini）
3. Gemini 本地代理（gemini_proxy.py，将 Anthropic 格式转为 Gemini 格式）

Windows 需要完成的本地配置（不在 git 中）。

---

## 任务清单

### 1. 拉取最新代码
```powershell
cd D:\cc-github
git pull origin main
```

### 2. 更新 Claude Code 本地配置（settings.json）
- **文件位置**：`C:\Users\Administrator\.claude\settings.json`
- **需要替换**：`ANTHROPIC_AUTH_TOKEN` 的值
- **新值**：从 macOS 的 `api_config.json` 中获取
- **同时确认**：`ANTHROPIC_BASE_URL` 指向智谱

### 3. 更新本地 api_config.json
- **文件位置**：`D:\cc-github\api_config.json`（在 .gitignore 中，不会自动同步）
- **操作**：从 macOS 复制完整的 api_config.json（包含 gemini 配置）
- **关键**：确保 gemini.api_key 和 glm.api_key 都正确

### 4. 安装 Gemini 依赖
```powershell
pip install google-generativeai
```

### 5. 配置 Claude Code 自动启动（PowerShell profile）
```powershell
# 编辑 PowerShell 配置文件
notepad $PROFILE
```
添加以下内容：
```powershell
# Claude Code 自动 API 检测
function claude {
    python D:\cc-github\smart_claude.py --auto 2>$null
    claude.exe @args
}
```
保存后重启 PowerShell 生效。

### 6. 测试智能启动器
```powershell
python D:\cc-github\smart_claude.py --status
```
确认两个 API 都显示可用。

### 7. 检查 Windows 本地其他文件
```powershell
Select-String -Path "C:\Users\Administrator\.claude\*" -Pattern "232b1236" -ErrorAction SilentlyContinue
Select-String -Path "D:\BigA\*.py" -Pattern "232b1236" -ErrorAction SilentlyContinue
```

### 8. 验证 Python 脚本可用性
```powershell
cd D:\cc-github
python glm47_helper.py
```

### 9. ⚠️ 删除智谱控制台旧 API Key（最后一步）
- **前提**：步骤 1-8 全部完成，新 Key 在两台电脑上均正常
- **操作**：登录智谱开放平台 → API Keys 管理 → 删除旧 Key
- **旧 Key 前缀**：`232b1236...`

---

## 完成后

1. 在 memory.md 的 PENDING TASKS 部分标记为已完成
2. 清除本文档中的密钥前缀
3. 将此文件改名为 `PENDING-TASKS-DONE.md`

---

## 密钥对照（迁移完成后清除）

| 用途 | 旧值前缀 | 新值位置 |
|------|----------|---------|
| GLM API | `232b1236...` | api_config.json |
| Gemini | — | api_config.json → gemini.api_key |
| ANTHROPIC_AUTH_TOKEN | 旧值 | settings.json |

**安全提示**：迁移完成后，将此文件中的密钥前缀也清除。
