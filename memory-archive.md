# Claude Code 历史记录归档

> 本文件存储历史对话的详细记录，memory.md 只保留最新动态

---

## 2025-01-05 记录

### 跨平台记忆文件迁移
- 将 `E:\memory.md` 移至 `D:\cc-github\memory.md`
- 通过 Git 同步到 GitHub 仓库
- 支持 Windows 和 macOS 跨平台访问

**Git 配置**：
- 用户名：lartemac
- 邮箱：13654569388@139.com

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

### 启动方式确认
**桌面快捷方式**：
- 文件位置：`C:\Users\Administrator\Desktop\Claude Code.lnk`
- 目标路径：`C:\Users\Administrator\AppData\Roaming\npm\claude.cmd`
- 工作目录：`C:\Users\Administrator`

### GitHub 同步设置完成
**项目信息**：
- 项目名称：VPT 初诊数据收集系统
- GitHub 仓库：https://github.com/lartemac/VPT--
- 本地位置：D:\cc-github
- 项目类型：微信小程序
- 用途：医学研究数据采集，用于收集患者临床数据并导出为 CSV 格式

**项目功能**：
- 患者管理（姓名、性别、年龄、联系方式等）
- 多阶段数据采集（术前、术中、术后回访）
- 图片上传（支持术中照片）
- 数据导出（CSV 格式，兼容 SPSS、R、Python）
- 实时同步（基于微信云数据库）

**待完善功能**：
- 数据字段需要根据实际研究需求补充
- 数据验证规则
- 权限管理和用户系统
- 数据统计分析图表
- 数据备份功能

**技术栈**：
- 微信小程序原生开发（WXML、WXSS、JavaScript）
- 微信云开发（云数据库、云存储、云函数）

**同步状态**：
- 已成功同步到 D:\cc-github
- Git 远程仓库配置正确
- 当前分支：main
- 工作区干净

---

## 2026-01-05 记录

### GitHub 项目同步
**操作内容**：
- 从远程仓库拉取最新更新
- 项目位置：`/Users/lartemacfiles/Desktop/VPT-初诊数据`
- 远程仓库：`git@github.com:lartemac/VPT--.git`
- 当前分支：main

**更新内容**：
- `CLAUDE-global.md` - 全局配置文件（60行）
- `memory.md` - 记忆文件（125行）
- `sync-claude-config.bat` - Windows同步脚本（36行）
- `sync-claude-config.sh` - macOS/Linux同步脚本（38行）
- 共新增：259行代码

### 全局配置文件设置
**操作内容**：
- 查看 `CLAUDE-global.md` 文件内容
- 创建 `~/.claude/` 目录
- 将 `CLAUDE-global.md` 内容复制到 `~/.claude/CLAUDE.md`

**配置要点**：
- 语言设置：简体中文
- 用户介绍：FattyTiger，产品经理兼科研人员
- 开发需求：微信小程序、支付宝小程序（不会写代码）
- 研究领域：口腔临床医学、牙体牙髓、统计分析、机器学习、AI
- 文献偏好：近期高影响因子的权威论文（PubMed、Science、Nature）
- 个人特点：喜欢自动化和免费软件，追求简洁高效
- 工作方式：macOS 和 Windows 间切换，使用 GitHub 同步项目

### PDF 读取问题与解决方案
**问题发现**：
- Claude Code 的 PDF 读取工具存在服务器端缓存 bug
- 相同 MD5 的文件会返回错误的提取内容

**解决方案**：
- 安装 Python 文件读取库（通过 pip3）
- 已安装库：pypdf, pdfplumber, python-docx, openpyxl, xlrd, python-pptx, Pillow
- 优先使用 Python 本地提取确保准确性

**读取策略**：
1. PDF → 使用 `pypdf` 或 `pdfplumber`
2. Word (.docx) → 使用 `python-docx`
3. Excel (.xlsx/.xls) → 使用 `openpyxl` 或 `xlrd`
4. PowerPoint (.pptx) → 使用 `python-pptx`
5. 图片 (PNG/JPG) → 使用 Read 工具
6. TXT → 使用 Read 工具

### 磁盘清理工具创建
**创建内容**：
- 桌面脚本：`~/Desktop/清理磁盘空间.command`
- 可双击直接运行，交互式菜单
- 功能：查找大文件、清理缓存、显示清理建议

**脚本功能**：
1. 查看磁盘使用情况
2. 查找最大的文件（前20个）
3. 查找最大的目录（前15个）
4. 查看可清理的缓存文件
5. 查找重复文件
6. 执行清理操作（需确认）
7. 显示清理建议
8. 全部检查（选项1-5）

**清理内容**：
- Homebrew、npm、pip、CocoaPods 缓存
- 废纸篓
- Xcode 派生数据（可选）
- iOS 模拟器数据（可选）

### 磁盘清理操作记录
**清理前状态**（2026-01-05）：
- 总容量：228 GB
- 已使用：154 GB (73%)
- 可用空间：58 GB

**已删除文件**：
1. 微信视频文件：
   - `c721d9366a858502aa81433a8e71fed1_raw.mp4` (417 MB)
   - `c721d9366a858502aa81433a8e71fed1.mp4` (58 MB)
   - 相关缩略图和封面图
   - 微信视频文件夹从 712 MB → 237 MB

2. Windows 可执行文件：
   - `综合调查统计系统单机版-Windows版.exe` (280 MB)
   - Mac 无法运行，删除释放空间

3. 用户手动删除：
   - Pictures 目录全部内容（约 89 GB）

4. 缓存清理：
   - npm 缓存：67 MB
   - pip 缓存：31 MB
   - 系统缓存

**清理后状态**：
- 已使用：154 GB (73%)
- 可用空间：57 GB
- 释放空间：约 770 MB（系统可能延迟显示 Pictures 删除的效果）

**主要占用空间目录**：
- Library/Containers：12 GB
  - 微信：8.0 GB
    - xwechat_files：6.9 GB
      - video：3.0 GB
      - attach：1.8 GB
      - file：1.3 GB
  - WPS：1.4 GB
  - QQ音乐：1.0 GB
  - 钉钉：866 MB
- Library/Application Support：5.1 GB
- Library/Caches：1.8 GB
- Downloads：374 MB

---
