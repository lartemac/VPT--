# claude-api-switcher 产品需求文档

> **状态**：需求确认完成，待开发
> **日期**：2026-04-15
> **作者**：FattyTiger（产品经理）+ Claude（技术架构）

---

## 一、产品定位

**一句话描述**：Claude Code 的 API 自动切换器，token 限额时无缝切换到备用服务商。

**目标用户**：中国大陆使用 Claude Code 的开发者/研究者。

**核心价值**：
- 安装配置一次，之后完全无感
- 解决国内 API 服务商 token 限额导致 Claude Code 卡死的痛点

---

## 二、第一期支持服务商

| 优先级 | 服务商 | Anthropic 兼容 | 代理需求 | 默认模型 |
|--------|--------|:-:|:-:|----------|
| 1（推荐首选） | 智谱 GLM | ✅ 原生支持 | 无需 | glm-5.1 |
| 2 | DeepSeek | ❌ | 本地代理（OpenAI→Anthropic） | deepseek-chat |
| 3 | 通义千问 | ❌ | 本地代理（OpenAI→Anthropic） | qwen-max |

**第二期（暂不实现）**：小米、Gemini、MiniMax 等

---

## 三、用户体验流程

### 3.1 安装（一次性）

```bash
pip install claude-api-switcher
```

### 3.2 配置（一次性）

```bash
$ claude-api-switcher config

🎯 Claude Code API 自动切换器 - 配置向导

请输入 API Key（2-3个，按优先级排列，回车跳过）：

1. 智谱 GLM（推荐首选）
   API Key: ****
   ✅ 验证通过（glm-5.1）
   模型（回车使用默认 glm-5.1）: _

2. DeepSeek
   API Key: ****
   ✅ 验证通过（deepseek-chat）
   模型（回车使用默认 deepseek-chat）: _

3. 通义千问
   API Key: （回车跳过）

✅ 配置完成！优先级：智谱 → DeepSeek
✅ 已自动配置 shell 集成（~/.zshrc）
   请重启终端生效
```

### 3.3 日常使用（零操作）

**正常启动（智谱可用）：**
```
$ claude
[api-switcher] 智谱 GLM ✅
（Claude Code 正常启动）
```

**智谱限额，自动切换：**
```
$ claude
[api-switcher] ⚠️ 智谱 429（重置时间: 19:33）→ DeepSeek ✅
（Claude Code 正常启动，使用 DeepSeek 后端）
```

**修改配置（API Key 变更时）：**
```bash
$ claude-api-switcher config       # 重新配置全部
$ claude-api-switcher config zhipu # 只改智谱
```

**查看状态：**
```bash
$ claude-api-switcher status

📡 智谱 GLM (glm-5.1)     ✅ 可用
📡 DeepSeek (deepseek-chat) ✅ 可用
🔧 当前后端：智谱 GLM
```

---

## 四、技术架构

### 4.1 组件

```
claude-api-switcher/
├── __init__.py
├── cli.py              # 命令行入口（config / status）
├── checker.py          # API 可用性检测 + 缓存
├── proxy.py            # Anthropic↔OpenAI 格式转换代理
├── settings.py         # Claude Code settings.json 读写
├── shell.py            # .zshrc / PowerShell 集成
└── providers/
    ├── __init__.py
    ├── zhipu.py        # 智谱（直连，无需代理）
    ├── deepseek.py     # DeepSeek（需代理）
    └── qwen.py         # 千问（需代理）
```

### 4.2 运行机制

```
用户输入 claude
    ↓
shell 函数触发 claude-api-switcher --auto
    ↓
① 读缓存（3分钟内跳过检测）
    ↓ 缓存过期
② 按优先级检测 API 可用性
    ↓
③ 首个可用服务商 → 更新 settings.json
    ↓  需要代理的服务商 → 启动本地代理（端口 4000）
    ↓
④ 启动 Claude Code
```

### 4.3 自愈机制

**代理健康检查**：
- 每次 `claude` 启动时 ping 代理端口
- 无响应 → 自动重启代理
- 重启失败 → 跳过该服务商，尝试下一个

**降级策略**：
- 智谱 429 → 尝试 DeepSeek → 尝试千问
- 全部不可用 → 显示提示，建议等待重置

### 4.4 配置存储

- 位置：`~/.claude-api-switcher/config.json`
- 内容：各服务商 API Key、模型名、优先级顺序
- 不在任何项目仓库中，避免泄露风险

### 4.5 Shell 集成

**macOS/Linux**（.zshrc / .bashrc）：
```bash
claude() {
    claude-api-switcher --auto
    command claude "$@"
}
```

**Windows**（PowerShell $PROFILE）：
```powershell
function claude {
    claude-api-switcher --auto 2>$null
    & "$env:APPDATA\npm\claude.cmd" @args
}
```

`claude-api-switcher config` 自动完成写入，用户无需手动编辑。

---

## 五、已确认的设计决策

| # | 问题 | 决策 |
|---|------|------|
| 1 | 项目名称 | `claude-api-switcher` |
| 2 | API Key 数量 | 最少 2 个，最多 3 个 |
| 3 | 第一期服务商 | 智谱 + DeepSeek + 千问 |
| 4 | 自愈机制 | 健康检查 + 自动重启 + 降级跳过 |
| 5 | 模型选择 | 默认最强，允许手动配置 |
| 6 | 切换提示 | 显示服务商名 + 限额重置时间 |
| 7 | 配置位置 | `~/.claude-api-switcher/` |
| 8 | 开源时机 | 代码写好测试通过后再公开 |
| 9 | pip 包名 | `claude-api-switcher` |
| 10 | 修改配置 | `config` 全量重配，`config zhipu` 单项修改 |

---

## 六、待开发阶段

1. **Phase 1 - 核心功能**：智谱直连 + config 向导 + shell 集成
2. **Phase 2 - 代理层**：DeepSeek + 千问的 Anthropic↔OpenAI 代理
3. **Phase 3 - 自愈 + 打磨**：健康检查、降级、错误提示、README
4. **Phase 4 - 发布**：PyPI 发布 + GitHub 公开 + 文档

---

## 七、技术风险

| 风险 | 影响 | 应对 |
|------|------|------|
| 各服务商 API 格式差异大 | 代理兼容性 | 逐个测试验证 |
| 流式 SSE 转发性能 | 响应延迟 | 用异步处理，实测延迟 |
| PyPI 包名被占用 | 无法发布 | 备选名：cswitcher |
| Python 版本兼容 | 用户安装失败 | 支持 3.9+（国内常见） |
