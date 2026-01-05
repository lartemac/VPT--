# Claude Code 记忆文件

> **重要提示**：本文件位于项目文件夹中，可通过 Git 同步到 GitHub，支持跨平台（Windows/macOS）和跨设备使用。

## 文件位置
- **Windows 路径**：`D:\cc-github\memory.md`
- **macOS 路径**：`~/cc-github/memory.md` 或克隆项目的任意位置
- **GitHub 仓库**：https://github.com/lartemac/VPT--

## 用户信息
- **姓名**：FattyTiger
- **身份**：产品经理 + 科研人员
- **专业领域**：口腔临床医学、牙体牙髓、统计分析、机器学习、人工智能
- **编程能力**：不会写代码
- **语言偏好**：中文

---

## 2025-01-05 对话记录

### 跨平台记忆文件迁移

**迁移内容**：
- ✅ 将 `E:\memory.md` 移至 `D:\cc-github\memory.md`
- ✅ 通过 Git 同步到 GitHub 仓库
- ✅ 支持 Windows 和 macOS 跨平台访问
- ✅ 换设备或换系统都能继续使用

**Git 配置**：
- 用户名：lartemac
- 邮箱：13654569388@139.com

---

### 全局配置文件同步设置

**配置文件位置**：
- 项目文件：`D:\cc-github\CLAUDE-global.md`（可编辑，通过 Git 同步）
- 系统文件：`C:\Users\Administrator\.claude\CLAUDE.md`（Claude Code 读取位置，不可移动）

**同步脚本**：
- Windows: `D:\cc-github\sync-claude-config.bat`
- macOS/Linux: `D:\cc-github\sync-claude-config.sh`

**使用方法**：
1. 编辑 `CLAUDE-global.md`
2. 运行同步脚本将配置复制到系统位置
3. 提交到 GitHub：`git add` + `git commit` + `git push`
4. 换系统后先 `git pull`，再运行同步脚本

**重要**：全局配置文件必须在系统特定位置才能生效，所以需要同步脚本

---

### 启动方式确认

**桌面快捷方式**：
- 文件位置：`C:\Users\Administrator\Desktop\Claude Code.lnk`
- 目标路径：`C:\Users\Administrator\AppData\Roaming\npm\claude.cmd`
- 工作目录：`C:\Users\Administrator`

**重启确认**：
- ✅ 所有设置均为永久性
- ✅ 桌面快捷方式重启后可用
- ✅ Claude CLI 安装在用户目录，重启后不受影响
- ✅ PATH 环境变量已正确配置
- ✅ 启动脚本已保存在 `C:\Users\Administrator\bin\`

**结论**：电脑重启后可以正常使用，双击桌面图标即可启动 Claude Code

---

### GitHub 同步设置完成

**项目信息**：
- 项目名称：VPT 初诊数据收集系统
- GitHub 仓库：https://github.com/lartemac/VPT--
- 本地位置：D:\cc-github
- 项目类型：微信小程序
- 用途：医学研究数据采集，用于收集患者临床数据并导出为 CSV 格式

**项目功能**：
- ✅ 患者管理（姓名、性别、年龄、联系方式等）
- ✅ 多阶段数据采集（术前、术中、术后回访）
- ✅ 图片上传（支持术中照片）
- ✅ 数据导出（CSV 格式，兼容 SPSS、R、Python）
- ✅ 实时同步（基于微信云数据库）

**待完善功能**：
- ⏳ 数据字段需要根据实际研究需求补充
- ⏳ 数据验证规则
- ⏳ 权限管理和用户系统
- ⏳ 数据统计分析图表
- ⏳ 数据备份功能

**技术栈**：
- 微信小程序原生开发（WXML、WXSS、JavaScript）
- 微信云开发（云数据库、云存储、云函数）

**同步状态**：
- ✅ 已成功同步到 D:\cc-github
- ✅ Git 远程仓库配置正确
- ✅ 当前分支：main
- ✅ 工作区干净

**其他文件夹**：
- D:\MiniProjects\VPT信息（用户要求保留，不删除）

---

## 重要提醒

### 自动化任务
- 每次启动时：从 GitHub 拉取最新代码
- 每次大改动后：主动提交代码到 GitHub
- 退出前：提醒用户保存记录到 memory.md

### 用户偏好
- 喜欢免费软件和自动化功能
- 拒绝付费软件
- 代码要求：简洁、高效

### 工作环境
- 在 macOS 和 Windows 间切换
- 使用 GitHub 完成项目同步开发

---

## 2026-01-05 对话记录

### GitHub 项目同步

**操作内容**：
- ✅ 从远程仓库拉取最新更新
- ✅ 项目位置：`/Users/lartemacfiles/Desktop/VPT-初诊数据`
- ✅ 远程仓库：`git@github.com:lartemac/VPT--.git`
- ✅ 当前分支：main

**更新内容**：
- `CLAUDE-global.md` - 全局配置文件（60行）
- `memory.md` - 记忆文件（125行）
- `sync-claude-config.bat` - Windows同步脚本（36行）
- `sync-claude-config.sh` - macOS/Linux同步脚本（38行）
- 共新增：259行代码
- 更新范围：`6784c57..38fe2f0`

### 全局配置文件设置

**操作内容**：
- ✅ 查看 `CLAUDE-global.md` 文件内容
- ✅ 创建 `~/.claude/` 目录
- ✅ 将 `CLAUDE-global.md` 内容复制到 `~/.claude/CLAUDE.md`

**文件位置**：
- 项目文件：`/Users/lartemacfiles/Desktop/VPT-初诊数据/CLAUDE-global.md`（可编辑，通过 Git 同步）
- 系统文件：`~/.claude/CLAUDE.md`（Claude Code 读取位置）

**配置要点**：
- 语言设置：简体中文
- 用户介绍：FattyTiger，产品经理兼科研人员
- 开发需求：微信小程序、支付宝小程序（不会写代码）
- 研究领域：口腔临床医学、牙体牙髓、统计分析、机器学习、AI
- 文献偏好：近期高影响因子的权威论文（PubMed、Science、Nature）
- 个人特点：喜欢自动化和免费软件，追求简洁高效
- 工作方式：macOS 和 Windows 间切换，使用 GitHub 同步项目

---
