# 待办任务：Windows 电脑安全修复 + 智能启动器配置

> **触发条件**：在 Windows 电脑上启动 Claude Code 并读取 memory 后，发现此文件，立即执行
> **优先级**：高
> **创建时间**：2026-04-15（macOS）

---

## 背景

macOS 上已完成两项工作，Windows 需同步：

**工作一：API Key 安全修复**
- 旧 GLM API Key 曾硬编码在代码中并推送到公开 GitHub（已清理）
- Windows 本地配置（settings.json、api_config.json）仍使用旧 Key
- 需要替换为新 Key，确认正常后由用户手动删除旧 Key

**工作二：Claude Code 智能启动器**
- 智谱每5小时30M token限额，超出后 Claude Code 卡死
- 已实现自动检测：智谱可用→直连，智谱429→自动切Gemini
- macOS 已配置完成，Windows 需要安装依赖+配置自动启动

---

## 第一阶段：拉代码 + API 替换

### 1. 拉取最新代码
```powershell
cd D:\cc-github
git pull origin main
```

### 2. 创建/更新 api_config.json
api_config.json 被 .gitignore 排除，Windows 上可能不存在或使用旧 Key。
**直接创建完整文件**（内容如下）：

```powershell
# 在 D:\cc-github 目录下创建
Set-Content -Path "D:\cc-github\api_config.json" -Value @'
{
  "version": "3.0.0",
  "updated": "2026-04-15",
  "note": "AI API 配置文件 - 智谱主 + Gemini 备用",
  "glm": {
    "name": "智谱 GLM-5.1",
    "api_key": "REDACTED_GLM_KEY",
    "base_url": "https://open.bigmodel.cn/api/paas/v4/",
    "anthropic_url": "https://open.bigmodel.cn/api/anthropic",
    "latest_model": "glm-5.1"
  },
  "gemini": {
    "name": "Google Gemini 2.5 Flash",
    "api_key": "REDACTED_GEMINI_KEY",
    "model": "gemini-2.5-flash",
    "proxy_port": 4000,
    "role": "fallback"
  }
}
'@
```

⚠️ **重要**：请提示用户告知两个密钥值，替换 `REDACTED_GLM_KEY` 和 `REDACTED_GEMINI_KEY`。
- GLM 新 Key：让用户从智谱控制台查看（或从 macOS 的 api_config.json 获取）
- Gemini Key：让用户提供

### 3. 更新 Claude Code settings.json
- **文件**：`C:\Users\Administrator\.claude\settings.json`
- **替换** `env.ANTHROPIC_AUTH_TOKEN` 为 api_config.json 中的 glm.api_key
- **确认** `env.ANTHROPIC_BASE_URL` 为 `https://open.bigmodel.cn/api/anthropic`

### 4. 扫描旧密钥残留
```powershell
Select-String -Path "C:\Users\Administrator\.claude\settings.json" -Pattern "232b1236" -ErrorAction SilentlyContinue
Select-String -Path "D:\BigA\*.py" -Pattern "232b1236" -ErrorAction SilentlyContinue
Get-ChildItem -Path "C:\Users\Administrator" -Recurse -Include "*.json","*.py" -ErrorAction SilentlyContinue | Select-String "232b1236" | Select-Object -First 10
```
如有残留，逐一替换。

### 5. 验证 API 可用
```powershell
cd D:\cc-github
python smart_claude.py --status
```
确认智谱显示 ✅ 可用。

---

## 第二阶段：智能启动器配置

### 6. 安装 Gemini 依赖
```powershell
pip install google-generativeai
```

### 7. 测试 Gemini 代理
```powershell
# 后台启动代理
Start-Process python -ArgumentList "D:\cc-github\gemini_proxy.py" -WindowStyle Hidden
Start-Sleep -Seconds 3

# 测试健康检查
Invoke-RestMethod -Uri "http://127.0.0.1:4000/health"

# 测试 Anthropic 格式请求
$body = '{"model":"gemini-2.5-flash","max_tokens":20,"messages":[{"role":"user","content":"say ok"}]}'
Invoke-RestMethod -Uri "http://127.0.0.1:4000/v1/messages" -Method POST -ContentType "application/json" -Body $body
```

### 8. 测试自动模式
```powershell
# 应秒过（无输出 = 智谱正常，缓存生效）
python D:\cc-github\smart_claude.py --auto
echo "退出码: $LASTEXITCODE"
```

### 9. 配置 PowerShell 自动包装
```powershell
# 创建或编辑 PowerShell 配置文件
if (-not (Test-Path $PROFILE)) { New-Item -Path $PROFILE -ItemType File -Force }
notepad $PROFILE
```
在文件末尾添加（注意 claude.cmd 路径）：
```powershell
# Claude Code 自动 API 检测 + 智谱/Gemini 自动切换
$global:ClaudeCmd = "$env:APPDATA\npm\claude.cmd"
function claude {
    python D:\cc-github\smart_claude.py --auto 2>$null
    & $global:ClaudeCmd @args
}
```
保存后**重启 PowerShell**，输入 `claude` 验证自动检测生效。

### 10. 端到端验证
```powershell
# 在新 PowerShell 中执行
claude
```
确认正常启动且无报错。

---

## 第三阶段：收尾（用户手动）

### 11. 用户确认 + 删除旧 Key
用户需**手动**完成（不要自动执行）：
1. 确认 Windows 上 Claude Code 正常工作（智谱后端）
2. 确认 `python smart_claude.py --status` 两个 API 都显示可用
3. 登录 **智谱开放平台控制台** → API Keys 管理
4. 删除旧 Key（前缀 `232b1236...`）
5. 在保留的新 Key 上备注「2026-04-15 创建，替换泄露旧 Key」

---

## 完成后

1. 更新 memory.md 的 `⚠️ PENDING TASK` 为已完成
2. 删除此文件：`git rm PENDING-TASKS.md`
3. 提交推送
