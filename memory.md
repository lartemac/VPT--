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

### MCP 服务器（2026-01-07 安装）
- **@yfme/weapp-dev-mcp** - 微信小程序 AI 辅助开发
- **github-mcp** - GitHub 仓库管理
- **@playwright/mcp** - 浏览器自动化测试
- **@modelcontextprotocol/server-filesystem** - 文件系统访问
- **配置文件**：
  - Windows: `C:\Users\Administrator\.claude\mcp-servers.json`
  - macOS: `~/.claude/mcp-servers.json` 或 `~/.config/claude/mcp-servers.json`

### Mac 开发环境（2026-01-08 配置）
- **微信开发者工具** v2.01.2510260（已安装）
- **Visual Studio Code** v1.107.1 ARM64（已安装）
- **Node.js** v24.12.0（已安装）
- **npm** v11.6.2（已安装）
- **VS Code 插件**（7个）：
  - `crazyurus.miniprogram-vscode-extension` v1.5.1 - 微信小程序开发工具
  - `qinjia.vscode-wechat` v0.0.6 - VS Code 微信小程序支持
  - `wuxianqiang.wx-snippets` v1.0.9 - WeChat 代码片段
  - `iehong.miniprogram-minapp` v1.0.0 - WXML 格式化/高亮/自动补全
  - `dbaeumer.vscode-eslint` v3.0.20 - JavaScript 代码质量检查
  - `esbenp.prettier-vscode` v11.0.2 - 代码格式化工具
  - `hookyqr.beautify` v1.5.0 - HTML/CSS/JS 代码格式化

### 设计工具
- **Pixso**（免费，国产）- UI/UX 设计工具：https://pixso.cn/
- **WeUI** - 微信官方组件库
- **TDesign** - 腾讯企业级组件库

---

## 最近动态
### 2026-01-10
- ❌ **夸克网盘自动上传系统开发尝试（已放弃）**
  - **目标**：开发自动监控文件夹并上传到夸克网盘的系统
  - **尝试方案**：
    - 使用 Python + watchdog 监控文件变化
    - 使用剪贴板 + Ctrl+V 自动化上传到夸克网盘
    - 使用 pyautogui + pygetwindow 激活窗口并粘贴
    - 使用 JSON 队列管理延迟删除（60分钟）
  - **发现的问题**：
    - ❌ 剪贴板方式实际上传到夸克网盘失败
    - 用户确认夸克网盘界面没有看到任何上传文件
    - 自动化方法不适用于夸克网盘客户端
  - **技术问题**：
    - ⚠️ 发现死锁问题：`add()` 方法内部调用 `save_queue()` 导致锁重复获取
    - 修复方案：创建内部方法 `_save_queue_impl()` 避免嵌套锁
  - **最终决定**：
    - 用户决定直接使用夸克网盘自身的同步功能
    - 清理所有开发文件和痕迹
  - **清理完成**：
    - ✅ 删除 `E:\夸克自动_upload\` 完整文件夹
    - ✅ 删除 `E:\夸克自动上传\` 完整文件夹
    - ✅ 停止所有 Python 后台进程
    - ✅ 删除所有临时文件和 PDF 文档
    - ✅ 删除 build 和 dist 构建目录
    - ✅ 清理启动文件夹中的项目
    - ✅ 删除 QuarkAutoUpload.exe 及其进程
  - **经验教训**：
    - 网盘类软件应优先使用官方同步文件夹功能
    - 自动化 GUI 操作（剪贴板+Ctrl+V）不可靠
    - 开发前应先验证目标软件是否支持自动化接口

- ✅ **桌面图标整理**
  - 设置注册表启用桌面图标自动整理功能
  - 刷新桌面应用新设置
  - 用户可通过右键菜单"查看"→"自动整理图标"手动启用

- ⏳ **桌面顽固空文件夹删除问题（待重启解决）**
  - **问题**：桌面有两个无法删除的空文件夹（"落户"和"PDF"）
  - **尝试的方案**：
    - ❌ PowerShell Remove-Item（失败：文件被占用）
    - ❌ cmd rmdir 命令（失败：文件被占用）
    - ❌ 移除只读/系统属性后删除（失败）
    - ❌ 重启 Windows 资源管理器后删除（失败）
    - ❌ robocopy 清空文件夹后删除（失败）
    - ❌ 获取所有权和权限后删除（失败）
  - **根本原因**：✅ 用户指出真正原因是文件夹在 WPS 中被设置为同步文件夹（而非进程占用）
  - **最终解决方案**：
    - 用户在 WPS 中取消同步设置后成功删除
    - 清理 `一键重启删除.bat` 工具
  - **经验教训**：
    - 排查问题时应优先检查常用软件的同步/锁定功能
    - WPS、坚果云、OneDrive 等软件的同步功能会导致文件占用

- ✅ **Claude Code 自动同步机制增强**
  - **需求**：每次启动 Claude Code 时自动同步 GitHub 获取最新 memory.md 和 CLAUDE.md，并自动加载 Polymath 模式
  - **实施方式**：增强 `C:\Users\Administrator\.claude\CLAUDE.md` 配置文件（未创建外部脚本）
  - **具体修改**：
    - 将"自动同步规则"标注为"强制执行"
    - 新增：每次启动时必须自动激活 Polymath 模式
    - 新增：启动检查清单（6个步骤）：
      1. 检测当前平台（Windows/macOS）
      2. 切换到项目目录（`D:\cc-github\` 或 `~/cc-github/`）
      3. 执行 `git pull` 拉取最新代码
      4. 读取 `memory.md` 获取最新记录
      5. 检查并激活 Polymath 状态区
      6. 向用户汇报同步状态和近期工作
  - **实现原则**：
    - ✅ 未删除既往内容
    - ✅ 采用新增内容方式实现新功能
    - ✅ 保留所有原有配置和规则
  - **状态**：✅ 已完成并生效
  - **效果**：从现在开始，每次启动 Claude Code 都会自动执行完整同步流程

### 2026-01-09
- ✅ **Windows 开发环境全面检查与 Polymath 模式初始化**
  - **开发工具检查**：
    - ✅ 微信开发者工具 v2.01.2510260（已安装在 `D:\Program Files (x86)\Tencent\微信web开发者工具\`）
    - ✅ Visual Studio Code（已安装在 `C:\Users\Administrator\AppData\Local\Programs\Microsoft VS Code\`）
    - ✅ Python 3.14.0（最新版）
    - ✅ Git v2.52.0.windows.1
    - ✅ Node.js v24.12.0 + npm 11.6.2
  - **Polymath Python 核心库安装**（满足金融量化+医学统计双重需求）：
    - **数据分析与统计**（科研/金融基础）：
      - pandas 2.3.3, numpy 2.4.0, scipy 1.16.3
      - statsmodels 0.14.6, matplotlib 3.10.8, seaborn 0.13.2
    - **交易与网络**（量化/API）：
      - ccxt 4.5.32（支持100+交易所，包括OKX）
      - requests 2.32.5, websocket-client 1.9.0
    - **辅助工具**：
      - jupyter 1.1.1（含 JupyterLab 4.5.1）
      - openpyxl 3.1.5（Excel 读写）
      - python-docx 1.2.0（Word 文档处理）
  - **VS Code 插件配置检查**：
    - ✅ ms-python.python v2026.0.0（Python 核心支持）
    - ✅ ms-toolsai.jupyter v2025.9.1（Jupyter Notebook 支持）
    - ✅ crazyurus.miniprogram-vscode-extension v1.5.1（微信小程序开发）
    - ✅ github.copilot v1.388.0（AI 编程助手）
    - ✅ ms-ceintl.vscode-language-pack-zh-hans（中文语言包）
  - **VS Code 添加到系统 PATH**：
    - 使用 `setx` 命令成功添加路径到用户环境变量
    - 添加路径：`C:\Users\Administrator\AppData\Local\Programs\Microsoft VS Code`
    - 验证成功：重启后可使用 `code` 命令快速打开项目
  - **Polymath 开发环境初始化报告**：
    - ✅ 生成 Markdown 格式报告
    - ✅ 生成 HTML 格式报告（`Polymath_Report.html`）
    - ✅ 生成 PDF 生成说明文档
    - 位置：`C:\Users\Administrator\Desktop\`
  - **Polymath 模式验证**：
    - ✅ Mode B (全栈开发) - 就绪
    - ✅ 金融量化：Python + ccxt + pandas + numpy
    - ✅ 医学统计：scipy + statsmodels + jupyter
    - ✅ 小程序开发：VS Code + 微信开发者工具
    - ✅ 游戏逻辑：Python + numpy + scipy
    - ✅ API 开发：requests + websocket-client
  - **待优化项**：
    - ⚠️ VS Code 需重启后 `code` 命令才生效
    - ⚠️ tinycss2 版本冲突（weasyprint 要求 ≥1.5.0，当前 1.4.0，影响 PDF 生成）
  - **建议安装的手动工具**：
    - Zotero（免费）- 文献管理与引用
    - Obsidian（免费）- 知识管理与笔记
    - GraphPad Prism（付费）- 医学统计绘图
    - Docker Desktop（可选）- 容器化开发环境
    - Postman（免费）- API 调试工具
    - Wireshark（免费）- 网络抓包分析



### 2026-01-08
- ✅ **Mac mini 开发环境完整检查与配置**
  - **系统环境检查**：
    - ✅ 微信开发者工具 v2.01.2510260（已安装，位于 `/Applications/wechatwebdevtools.app`）
    - ✅ Node.js v24.12.0 + npm 11.6.2（已安装）
    - ✅ 微信客户端（已安装）
  - **Visual Studio Code 安装**：
    - 版本：v1.107.1 ARM64（Apple Silicon 优化版）
    - 安装位置：`/Applications/Visual Studio Code.app`
    - 下载来源：官方稳定版（149 MB）
    - 安装方式：命令行下载 + 手动安装
  - **VS Code 插件安装**（7个）：
    1. `crazyurus.miniprogram-vscode-extension` v1.5.1 - 微信小程序开发工具（预览、打包上传、代码补全）
    2. `qinjia.vscode-wechat` v0.0.6 - VS Code 微信小程序支持
    3. `wuxianqiang.wx-snippets` v1.0.9 - WeChat 代码片段
    4. `iehong.miniprogram-minapp` v1.0.0 - WXML 格式化/高亮/自动补全
    5. `dbaeumer.vscode-eslint` v3.0.20 - JavaScript 代码质量检查
    6. `esbenp.prettier-vscode` v11.0.2 - 代码格式化工具
    7. `hookyqr.beautify` v1.5.0 - HTML/CSS/JS 代码格式化
  - **状态**：✅ Mac mini 微信小程序开发环境已就绪

### 2026-01-07
- ✅ **微信小程序开发环境完整搭建**
  - **系统环境检查**：Node.js v24.12.0, npm 11.6.2（已安装）
  - **安装 4 个核心 MCP 服务器**：
    - `@yfme/weapp-dev-mcp` (微信小程序 AI 辅助开发，213个包)
    - `github-mcp` (GitHub 仓库管理，92个包)
    - `@playwright/mcp` (浏览器自动化测试，3个包)
    - `@modelcontextprotocol/server-filesystem` (文件系统访问，130个包)
  - **创建 MCP 配置文件**：`C:\Users\Administrator\.claude\mcp-servers.json`

- ✅ **C 盘空间清理（释放 17.5 GB）**
  - 清理前：已使用 167.75 GB (84%)，可用 32.23 GB
  - 清理后：可用约 50 GB（增加 17.5 GB）
  - 清理项目：
    - 临时 Windows 安装文件（17.5 GB）
    - Windows 临时文件夹
    - 用户临时文件夹
    - 回收站
    - npm 缓存

- ✅ **Visual Studio Build Tools 2022 安装**
  - 版本：17.14.23
  - 安装组件：
    - MSVC v143 - VS 2022 C++ x64/x86 生成工具（编译器）
    - Windows 11 SDK
    - 用于 Windows 的 C++ CMake 工具
  - 用途：编译 Node.js 原生模块（如 better-sqlite3）
  - 状态：✅ 安装成功（待重启验证）

- ✅ **创建完整文档体系**
  - `C:\Users\Administrator\Downloads\wechat-devtools\完整安装指南.md`
  - `C:\Users\Administrator\Downloads\wechat-devtools\安装总结报告.md`
  - `C:\Users\Administrator\Downloads\visual-studio-build-tools\Visual_CPP_编译工具安装指南.md`
  - `C:\Users\Administrator\Downloads\visual-studio-build-tools\快速安装指南.md`
  - `C:\Users\Administrator\Downloads\快速扫描指南.md`
  - `C:\Users\Administrator\Downloads\应用程序移动指南.md`
  - `C:\Users\Administrator\Downloads\ProgramFiles_移动建议.md`

- ⏳ **待完成任务（重启后）**
  - 验证 C++ 编译工具安装
  - 重新安装 SQLite MCP Server (@berthojoris/mcp-sqlite-server)
  - 测试原生模块编译
  - 检查是否需要移动 Program Files 中的应用程序到 D/E 盘

- 📝 **推荐工具清单**
  - 微信开发者工具 v2.01.2510260（需手动安装）
  - Pixso 设计工具（免费，国产，https://pixso.cn/）
  - WeUI + TDesign 组件库
  - SpaceSniffer（磁盘空间可视化工具）

### 2026-01-06
- ✅ **Claude Code 中文教程完整版处理**
  - 检查并修复第24章缺失问题
  - 发现第27章的前6个小节（27.1-27.6）实际应该是第24章
  - 内容包括：高级代码生成技巧、复杂系统设计、代码理解与分析、代码质量评估、跨语言代码生成、大规模代码库处理
  - 提取并重新编号为第24章，插入到第23章和第25章之间
  - 使用python-docx生成排版优化的Word文档
  - 统一字体（微软雅黑 11pt）、标题层级（18pt/14pt/12pt）、代码块（Consolas 9pt）
  - 最终文档：`Claude_Code中文教程_完整版.md` + `Claude_Code中文教程_完整版_优化版.docx`

- ✅ **Claude Code 实战课程抓取任务完成**
  - 成功抓取 https://cholf5.com/claude-code-in-action/ 全部21个章节
  - 抓取成功率：100%（21/21章节）
  - 生成文件：
    - `Claude_Code实战课程_完整版.md` (34 KB, 1,369行, 2,525词)
    - `Claude_Code实战课程_完整版.html` (46 KB，已在浏览器中打开)
    - `Claude_Code实战课程_完整版.pdf` ✨ (使用Playwright成功生成)
    - `实战课程抓取报告.md` (详细统计信息)
    - `README_ClaudeCode课程.md` (完整使用指南)
    - `快速开始.md` (3分钟上手指南)
    - `任务完成总结.md` (任务执行总结)
  - 工具脚本：`scrape_course_v2.py`, `md_to_html_pdf.py`, `generate_pdf_guide.sh`
  - PDF生成：使用Playwright + Chromium成功生成完整PDF文档
  - 课程内容：基础部分(1-5章)、进阶部分(6-12章)、高级部分(13-21章)
  - 技术栈：Python 3.9 + requests + BeautifulSoup4 + markdown2 + Playwright

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

---

## 🧠 Polymath Context (Agent State)

### 当前激活项目
- **Mode B (全栈开发)** - 多项目并行
  1. **VPT 初诊数据收集系统**：微信小程序，医学研究数据采集
  2. **游戏系统开发**：7局4胜制 + 流局优先级判定逻辑

### User Rules
- **开发规范**：
  - 交易 API 禁止硬编码私钥，必须使用环境变量或加密配置
  - 代码要求：简洁、高效，避免过度设计
  - 游戏逻辑优先级：1.正常击杀 > 2.流局判定 > 3.平局
- **科研规范**：
  - 科研结论需引用权威文献（PubMed/Nature/Science/高影响因子期刊）
  - 优先检索最新文献（发表日期与当前日期相近）
  - 医学科研关键词：牙体牙髓、VPT、活髓保存、NSFC、国自然

### 平台适配
- **Windows**: 使用 PowerShell/cmd，路径分隔符 `\`
- **macOS**: 使用 bash/zsh，路径分隔符 `/`
- **自动检测**: 根据 `Platform` 环境变量自动切换
