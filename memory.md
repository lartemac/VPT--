# Claude Code 记忆文件

> **重要提示**：本文件位于项目文件夹中，可通过 Git 同步到 GitHub，支持跨平台（Windows/macOS）和跨设备使用。

## 文件位置
- **Windows 路径**：`D:\cc-github\memory.md`
- **macOS 路径**：`~/Desktop/VPT-初诊数据/memory.md`
- **GitHub 仓库**：https://github.com/lartemac/VPT--

## 用户信息
- **姓名**：FattyTiger
- **身份**：产品经理 + 科研人员
- **专业领域**：口腔临床医学、牙体牙髓、统计分析、机器学习、人工智能
- **编程能力**：不会写代码
- **语言偏好**：中文

## Git 配置
- 用户名：lartemac
- 邮箱：13654569388@139.com

---

## 当前项目

### VPT 初诊数据收集系统（微信小程序）
- **仓库**：https://github.com/lartemac/VPT--
- **本地**：`/Users/lartemacfiles/Desktop/VPT-初诊数据`
- **用途**：医学研究数据采集，收集患者临床数据并导出 CSV
- **功能**：患者管理、多阶段数据采集、图片上传、CSV 导出、云同步
- **技术栈**：微信小程序原生开发 + 微信云开发
- **状态**：开发中

### 开发工具配置
- **全局配置**：`CLAUDE-global.md` → `~/.claude/CLAUDE.md`
- **同步脚本**：`sync-claude-config.bat` / `sync-claude-config.sh`
- **Python 工具库**：pypdf, pdfplumber, python-docx, openpyxl, xlrd, python-pptx, Pillow
- **磁盘清理工具**：`~/Desktop/清理磁盘空间.command`
- **iPhone 闹钟工具**：`~/Desktop/16点43闹钟.command`（交互式闹钟，音量渐增）

---

## 最近动态

### 2026-01-05
- ✅ GitHub 项目同步（main 分支）
- ✅ 全局配置文件设置（macOS）
- ✅ Python 文件读取库安装（解决 PDF 缓存 bug）
- ✅ 创建磁盘清理工具
- ✅ 清理磁盘空间（释放 770 MB+）
- ✅ 优化 memory.md 结构（创建归档文件）
- ✅ **开发 iPhone 风格交互式闹钟系统**
  - 创建 `~/Desktop/16点43闹钟.command`
  - 功能：交互式时间设置、音量渐增（20%→80%）、iPhone 风格铃声
  - 三按钮界面：设置闹钟、关闭所有闹钟、测试铃声
  - 支持 24 小时制输入，后台运行，自动恢复音量
  - 修复 AppleScript 对话框按钮限制（最多 3 个）和错误处理

### 2025-01-05
- ✅ 跨平台记忆文件迁移（E:\ → D:\cc-github）
- ✅ Git 同步机制建立
- ✅ VPT 项目初始化

---

## 重要提醒

### 自动化任务
- **每次启动时**：从 GitHub 拉取最新代码（`git pull`）
- **每次大改动后**：主动提交到 GitHub（`git add` + `git commit` + `git push`）
- **退出前**：保存记录到 memory.md

### 文件读取策略
- PDF → 优先使用 Python 本地读取（pypdf/pdfplumber）
- Word → python-docx
- Excel → openpyxl/xlrd
- 图片/TXT → Read 工具

### 用户偏好
- 喜欢免费软件和自动化功能
- 拒绝付费软件
- 代码要求：简洁、高效

### 工作环境
- 在 macOS 和 Windows 间切换
- 使用 GitHub 完成项目同步开发

---

**历史详细记录**：参见 `memory-archive.md`
