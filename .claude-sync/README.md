# Claude Code 全局配置同步

此目录用于在 macOS 和 Windows 之间同步 Claude Code 的全局配置文件。

## 文件说明

| 文件 | 说明 |
|---|---|
| `CLAUDE.md` | Claude Code 全局配置文件 |
| `sync_config.py` | 跨平台同步脚本 |
| `README.md` | 本说明文件 |

## 使用方法

### macOS

```bash
# 自动检测并同步（推荐）
python3 ~/Desktop/VPT-初诊数据/.claude-sync/sync_config.py

# 从项目同步到本地配置
python3 ~/Desktop/VPT-初诊数据/.claude-sync/sync_config.py to-local

# 从本地配置同步到项目
python3 ~/Desktop/VPT-初诊数据/.claude-sync/sync_config.py to-project
```

### Windows

```powershell
# 自动检测并同步（推荐）
python D:\cc-github\.claude-sync\sync_config.py

# 从项目同步到本地配置
python D:\cc-github\.claude-sync\sync_config.py to-local

# 从本地配置同步到项目
python D:\cc-github\.claude-sync\sync_config.py to-project
```

## 路径配置

脚本会自动检测平台并使用对应路径：

| 平台 | 项目目录 | Claude配置目录 |
|---|---|---|
| macOS | `~/Desktop/VPT-初诊数据/` | `~/.claude/` |
| Windows | `D:\cc-github\` | `C:\Users\<用户>\.claude\` |
| Linux | `~/VPT-初诊数据/` | `~/.claude/` |

## 工作流程

1. **修改配置**：直接编辑 `~/.claude/CLAUDE.md`
2. **同步到项目**：运行 `sync_config.py to-project`
3. **提交到 Git**：在项目目录执行 `git add/commit/push`
4. **切换平台**：在新平台运行 `sync_config.py to-local`

## 自动检测模式

默认使用 `auto` 模式，脚本会：
- 比较两个文件的修改时间
- 自动选择同步方向（从新到旧）
- 如果时间相同则跳过同步

## 注意事项

- 同步操作会**覆盖**目标文件，请确认后再执行
- 建议在同步前先提交 Git，避免配置丢失
- 如果路径不同，请修改 `sync_config.py` 中的路径配置
