# Claude Code Memory (Compressed)

> **NOTE**: This file uses machine-readable compressed format. Full history stored in `memory-archive.md`

---

## META

### USER
- NAME: FattyTiger
- ROLE: Product Manager + Researcher
- FIELD: Dental Clinical Medicine, Endodontics, Statistics, ML/AI
- LANG: zh-CN
- CODE: No coding skills

### GIT
- USER: lartemac
- EMAIL: REDACTED_EMAIL
- REPO: https://github.com/lartemac/VPT--
- PATH_WIN: D:\cc-github\
- PATH_MAC: ~/cc-github/

### PLATFORM
- WIN: PowerShell, `\` separator, GPU: NVIDIA RTX 4060 Ti, Python 3.14
- MAC: bash/zsh, `/` separator, Python 3.14
- DETECT: Check `Platform` env var
- NOTE: 两台电脑均未部署本地大模型

### LESSONS
- FILE: lessons.md
- PURPOSE: 经验教训与失败项目集
- USAGE: 在需要时查阅，不在每次启动时自动加载
- RULE: 遇到问题前先检查 lessons.md，避免重复犯错

---

## PROJECTS

### ACTIVE
1. **VPT初诊数据收集系统** (WeChat Mini Program)
   - PURPOSE: Medical research data collection
   - TECH: WeChat Mini Program + Cloud Dev
   - STATUS: In development

2. **游戏系统开发** (Game System)
   - LOGIC: 7局4胜 + 流局优先级
   - PRIORITY: 正常击杀 > 流局判定 > 平局

3. **Fish Speech S2 Pro** (TTS 语音合成，备用方案)
   - PURPOSE: 文字转语音、声音克隆
   - TECH: Python + PyTorch + CUDA/MPS
   - STATUS: 备用（未部署，有需求时提醒用户）
   - REPO: https://github.com/fishaudio/fish-speech
   - STARS: 29.4k
   - CAPABILITIES:
     * 多语言TTS（80+语言，中文第一梯队）
     * 声音克隆（10-30秒参考音频）
     * 情感标签控制（15000+种标签）
     * 多角色对话、实时流式生成
   - HW_REQ: NVIDIA 8GB+ VRAM（Win RTX 4060 Ti 满足）/ Mac M系列可用但较慢
   - USE_CASES: 视频配音、有声书、游戏NPC、小程序语音、声音克隆
   - NOTE: 可先用在线版（零安装），本地部署需PyTorch+CUDA+模型权重(4B参数)

4. **A股数据下载系统** (A-Stock Data Downloader)
   - PURPOSE: Academic research backtesting (avoid survivorship bias)
   - TECH: Tushare Pro + Python + Parquet
   - PATH: E:\BigA\
   - STATUS: ✅ COMPLETED (2026-02-09) + 数据增强 (2026-02-11)
   - FEATURES:
     * Auto-download adj_factor for backup
     * Daily auto-update at 20:00 via Windows Task Scheduler
   - SCRIPTS:
     * tushare_downloader_v2.py (main downloader)
     * start_download.py (auto-start script)
     * daily_update_v2.py (daily auto-update w/ market cap)
     * add_market_cap_to_biga.py (market cap enhancer)
     * get_all_stock_names_v2.py (stock info fetcher)
   - TOKEN: REDACTED_TUSHARE_TOKEN
   - DEPS: tushare, pandas==2.3.3, pyarrow
   - RESULTS:
     * Daily data: 5799 stocks (100% success)
     * Adj factors: 5798 stocks (1 failed)
     * Total files: 11,596 parquet files
     * Time range: Each stock from listing date to 2026-02-06
     * File format: CODE-START-END-STATUS.parquet
     * 838 stocks (14.5%) at 6000-record limit (API limit, acceptable)
   - MARKET CAP ENHANCEMENT (2026-02-11):
     * Added fields: 总市值(万元), 流通市值(万元), 换手率(%), 量比(%)
     * Source: Tushare daily_basic API
     * Processing: Batch mode (500 files/batch), 0.31s API interval
     * Progress tracking: market_cap_add_progress.json
     * Status: Processing (499/5798 files in batch 1)
   - PERFORMANCE: 86 minutes download (29min daily + 57min factors)
   - FILE STRUCTURE:
     * E:\BigA\*.parquet (5798 daily data files)
     * E:\BigA\adjfactor\*_adj_factor.parquet (5798 adj factor files)

---

## TOOLS

### MCP_SERVERS (6)
1. @yfme/weapp-dev-mcp (WeChat Mini Program)
2. github-mcp (GitHub)
3. @playwright/mcp (Browser automation)
4. @modelcontextprotocol/server-filesystem (File system)
5. @modelcontextprotocol/server-google-search (Google search)
6. @modelcontextprotocol/server-tavily (Tavily AI search) ⭐

### SKILLS (5 Tavily AI Skills)
1. search - Smart search (LLM optimized)
2. research - Deep research with citations ⭐
3. crawl - Web scraping
4. extract - Data extraction
5. tavily-best-practices - API guide

### PYTHON_LIBS (173 packages)

**Core Data Analysis**:
- pandas==2.3.3, numpy==2.2.6, polars==1.38.1, scipy==1.17.0

**Machine Learning**:
- scikit-learn==1.8.0, gplearn==0.4.3, numba==0.61.2, optuna==4.7.0, pygad==3.5.0

**Visualization**:
- matplotlib==3.10.8, seaborn==0.13.2, plotly==6.5.2

**Financial Data** ⭐:
- tushare==1.4.24, akshare==1.18.22, yfinance==1.1.0
- pandas-ta==0.4.71b0, quantstats==0.0.81, vectorbt==0.28.4

**Data Storage**:
- pyarrow==23.0.0, fastparquet==2025.12.0, SQLAlchemy==2.0.46
- openpyxl==3.1.5, xlrd==2.0.2

**Web & API**:
- requests, beautifulsoup4==4.14.3, lxml==6.0.2

**File Processing**:
- Pillow==12.1.0, pyinstaller==6.18.0

**Document Processing**:
- pypdf, pdfplumber, python-docx, python-pptx

**Interactive Dev**:
- IPython==9.10.0, Jupyter widgets

### TOOLS_PATHS
- PubMedConsult: E:\pubmedconsult\ (PUBMEDCONSULT_V2.py - Tavily+PubMed dual engine)
- GLM Helper: ~/Desktop/VPT-初诊数据/glm_helper.py (GLM-5.1 assistant)
- GLM Model Fetcher: ~/Desktop/VPT-初诊数据/fetch_latest_glm_model.py (auto-update)

---

## RULES

### DEV_RULES
- ⚠️⚠️⚠️ NO hardcoded API keys/Token/密码（必须用环境变量或 api_config.json）
- ⚠️⚠️⚠️ 提交前必须扫描密钥泄露：`grep -rn "api_key\|token\|secret" *.py`
- ⚠️⚠️⚠️ 新项目第一天就配置 .gitignore 排除敏感文件
- Git 邮箱：lartemac@users.noreply.github.com（不用真实邮箱）
- Code: concise, efficient, no over-engineering
- Game priority: 1.正常击杀 > 2.流局判定 > 3.平局
- 安全事件记录：lessons.md #22（API Key 泄露）

### SCI_RULES
- Cite: PubMed/Nature/Science/high-impact journals
- Prefer: Recent papers (date close to current)
- Keywords: 牙体牙髓, VPT, 活髓保存, NSFC, 国自然
- Mode C trigger: 牙髓炎, VPT, 活髓保存, 文献, PubMed

### PLOT_RULES
- NO grid lines/dashed lines in academic charts
- Boxplot width: 0.17 (1/3 of original 0.5)
- Clean layout, no decoration
- Axis range: reasonable (not always 0-10)

### OUTPUT_FORMAT_RULES (2026-01-10)
- Principle: Strictly follow user's explicit format request
- If user says "生成Excel" → only .xlsx
- If user says "创建Word" → only .docx
- If no format specified → free choice (.py, .md, .txt, etc.)

### FILE_NAMING
- Python: concise, descriptive (e.g., 图1绘制.py, PUBMEDCONSULT.py)
- NO: test_, temp_, debug_ prefixes
- Excel: [query_summary]_pubmed查询.xlsx

### SCRIPT_ANNOTATION
```python
"""
功能描述
创建时间: YYYY-MM-DD
创建系统: Windows 11 / macOS
平台检测: if os.name == 'nt': Windows, else: macOS/Linux
"""
```

### API_USAGE (GLM-5.1)
- Auto-select model based on task (no user prompts)
- Auto-use latest model (glm-5.1 or higher)
- glm-5.1: Medical, research, complex code (200K context, 128K output)
- glm-5-turbo: Fast response, real-time interaction
- glm-5: Standard complex tasks, deep reasoning
- API Key: REDACTED_GLM_API_KEY
- Auto-update: fetch_latest_glm_model.py

### MCP_SEARCH_LIMITS
- Ask user BEFORE calling MCP services or WebSearch
- Purpose: Conserve limited API calls
- Local alternatives: Python (requests+BS4) for web scraping

### LOCAL_PYTHON_PRIORITY (Token Saving) ⭐
- **PRINCIPLE**: Use local Python whenever possible to save tokens
- **PRIORITY**: Local Python > MCP Services > WebSearch > AI Generation

**Local Python Solutions (Use First)**:
| Task | Python Libs | Token Saved |
|------|------------|-------------|
| File operations | os, pathlib, shutil | 1000+ |
| Data processing | pandas, numpy | 2000+ |
| Excel read/write | openpyxl, xlrd, pandas | 1500+ |
| Word read/write | python-docx | 1500+ |
| PDF text extraction | pypdf, pdfplumber | 2000+ |
| Web scraping | requests, BeautifulSoup4 | 1000+ |
| Image processing | Pillow (PIL) | 1000+ |
| Data visualization | matplotlib, seaborn | 1500+ |
| Text processing | re, string, textwrap | 500+ |
| Date/time | datetime, time | 300+ |
| Math calculations | math, statistics, scipy | 500+ |

**Use AI Only When**:
- User asks for explanation/teaching
- Need creative content generation
- Complex decision making required
- No local solution available

**Example**:
```
Task: Convert CSV to Excel
❌ Don't: Ask AI to write code (wastes tokens)
✅ Do: Write pandas script directly (save tokens)
```

---

## TIMELINE (Compressed)

### 2026-04-21
+ 德州扑克教程修改扩写完成 ✅
  * 任务：修改扩写桌面"德州扑克.docx"教程（11章）
  * 原文：385段，22,710字 → 修改版：541段，41,975字（+84.8%）
  * 方法：python-docx提取 → 拆分为11个独立txt → 6个并行Agent扩写 → 合并回docx
  * 主要改进：新增实战牌局示例、各位置起手牌推荐、完整牌局演示（4.6节）、线上礼仪（8.4节）、数学计算案例
  * 新增章节：4.6完整牌局示例、5.1.4位置起手牌范围、6.2.5综合实战决策、8.4线上礼仪、9.3差异对照表
  * 输出文件：桌面/德州扑克_修改版.docx
+ 用户对NCCL文献表格工作流评价"质量非常高"，已记录为固定工作流（feedback_literature_table.md）

### 2026-04-20
+ NCCL文献综述表格填写完成 ✅
  * 任务：阅读桌面NCCL文件夹中17篇PDF论文，提取信息填入NCCL.xlsx
  * 表格结构：文献题目 | 发表时间 | 研究目的 | 核心发现 | 创新性 | 局限性
  * 方法：pdfplumber提取PDF文本 → 3个并行Agent分析 → openpyxl填写Excel
  * 输出文件：桌面/NCCL_filled.xlsx（原文件被Excel占用，用新文件名保存）
  * 论文年份范围：2021-2025，涵盖NCCL修复材料、粘接策略、生物力学、诊断、系统综述等方向
+ FastGPT 知识库部署完成 ✅
  * 模型问题修复：通过网页端 账号→模型提供商 配置，模型从 active:0 → active:4
  * MinIO 外部端点修复：172.18.112.1:9000 → host.docker.internal:9000
  * 当前状态：12个容器全部健康，模型已激活，可正常使用
  * 访问：http://localhost:4000 (root/1234)，MinIO: http://localhost:9001

### 2026-04-19
+ AI 文献知识库方案深化
  * RAG 技术详解：索引检索机制（向量嵌入 + 语义匹配 + 片段召回）
  * 确认方向：放弃本地部署大模型，采用"本地 RAG + 云端 API"架构
  * 方案选定：FastGPT（开源，原生支持智谱 API，专为知识库设计）
  * 安装方式：Docker Desktop + docker compose 一键启动
  * 支持数据源：PDF/Word/Excel/TXT 直接上传、网页链接自动抓取、手动粘贴文本
  * 原则：正文越干净检索越准确，不需要转 PDF
  * 硬件：32G 内存充足，不用时关掉 Docker Desktop 即可
  * FastGPT 安装完成：Docker Desktop v4.68.0 + WSL2
  * 详见：auto-memory project_fastgpt.md
  * ⏳ 待办：NVIDIA 更新缓存清理（C:\ProgramData\NVIDIA Corporation\NVIDIA app\UpdateFramework\ota-artifacts，824MB）
+ Windows C 盘瘦身（180 GB 已用 → 120 GB 已用，释放约 40 GB）
  * Windows.old 删除：~25 GB（磁盘清理工具）
  * QQ 音乐卸载：~7 GB
  * duowan/YY 删除：~1 GB
  * pip cache 清理：1 GB
  * WPS addons 缓存清理：6 GB（addons 目录为遗留缓存，非云文档同步目录）
  * 当前剩余：~60 GB（健康状态）
  * 未清理（保留）：Chrome(5.2G)、钉钉(3.84G)、夸克(4.46G)、Adobe CameraRaw(2.57G)
  * NVIDIA 驱动：不更新（当前稳定，近期有翻车更新），关闭自动更新
  * Node.js：仅 0.32 GB，保留
  * Python 第三方库：1.93 GB，保留（torch/casadi/scipy 等科研+A股用途）
  * NVIDIA 更新缓存(ota-artifacts 824MB)：建议手动删除

### 2026-04-18
+ 路由器 IPv6 配置修复（Clash 节点 IPv4 大规模掉线）
  * 背景：上游 SSR 节点 IPv4 地址不可用，只能通过 IPv6 连接
  * 小米路由器（192.168.31.x）IPv6 配置步骤：
    - 开启 IPv6 → Native 模式 → 只有 WAN 地址，LAN 无分配
    - 改为 NAT6 模式 → LAN 分配 fd00:6868:6868::/64，电脑获得 IPv6 地址
  * Windows DNS 修复：设置阿里 IPv6 DNS（2400:3200::1）
  * 结果：Clash 通过 IPv6 连上存活节点，GitHub/git pull 恢复正常
  * 知识点：fe80:: 为本地链接地址（不代表公网IPv6）；公网 IPv6 以 2400/2408/2409 开头
  * NAT6 原理：类似 IPv4 NAT，路由器用1个公网 IPv6 地址代理所有设备
+ Obsidian 评估
  * 结论：不适合用户需求（需要 AI 全文阅读+智能问答，Obsidian 是纯笔记软件）
  * CLI 功能：面向开发者，用户目前不需要
+ AI 文献知识库方案调研
  * 用户需求：上传100+篇论文全文 → AI全文阅读 → 智能问答 → 自动分类
  * 核心难点：需要 AI 读懂全文（不只是摘要），从正文中精确检索
  * 调研产品：
    - Google NotebookLM：最接近需求，免费，50源/笔记本限制
    - SciSpace：科研专用，免费版限20篇/月
    - Zotero：文献管理王者，但不做AI问答
  * 最终推荐方案：本地部署 RAG 系统
    - 路线A（快速体验）：Ollama + AnythingLLM（桌面软件，零门槛）
    - 路线B（专业方案）：Ollama + RAGFlow（PDF解析最强，支持表格/公式/图片）
    - 模型选择：Qwen3:8B（~5GB显存，中文第一梯队）
    - 方案文档已保存：桌面\本地AI文献知识库方案.md
  * 待确认：用户电脑内存大小（建议 ≥16GB）
+ IPv6 相关知识（新增 RULES 参考）
  * Windows IPv6 诊断命令：
    - ipconfig：查看 IPv6 地址（fe80=本地，2400/2408=公网）
    - ping -6：测试 IPv6 连通性
    - Get-NetRoute -AddressFamily IPv6：查看路由表
    - Set-DnsClientServerAddress：设置 IPv6 DNS

### 2026-04-16
+ Windows 待办任务全部完成
  * api_config.json 更新到 v3.0.0（智谱主 + Gemini 备用）
  * settings.local.json Key 同步为 api_config.json 的 GLM Key
  * smart_claude.py Windows 兼容修复：UTF-8 编码、settings.local.json 路径
  * gemini_proxy.py Windows 编码修复
  * google-generativeai 安装完成
  * Gemini 代理测试通过（健康检查 + API 请求 + 自动模式）
  * PowerShell profile 配置 claude 自动包装
  * 旧密钥 232b1236 残留扫描：无残留
  * PENDING-TASKS.md 已删除

### 2026-04-15
+ 安全修复：移除硬编码 API Key（续 04-14 未完成工作）
  * Python脚本改造：glm47_helper.py, glm_search.py, auto_search.py
    - 硬编码 API_KEY → 环境变量 ZHIPU_API_KEY → api_config.json 读取
  * api_config.json：更新为新密钥，加入 .gitignore 排除
  * api_config.json.template：创建模板文件（不含真实密钥）
  * .gitignore：添加敏感文件排除规则（api_config.json, *.env, credentials 等）
  * memory.md / memory-archive.md：清除明文密钥，替换为占位符
  * Git邮箱：13654569388@139.com → lartemac@users.noreply.github.com
  * Git历史清理：git-filter-repo（3次）
    - replace-text：替换所有历史文件中的明文密钥
    - mailmap：替换提交者邮箱
  * Force push：重写远程仓库历史
  * 验证：历史 blob 中无明文密钥，diff 上下文残留不影响安全
  * 清理：删除含密钥的导出文件（2026-04-14-153744-memory.txt）
  * 提交：superpowers-zh skills（54个文件）
+ 安全记录更新
  * lessons.md 新增 #22（API Key泄露事故）、#23（跨平台配置盲区）
  * 核心原则：信息安全提升为第1优先级
  * DEV_RULES：新增3条⚠️⚠️⚠️最高级安全规则
+ Claude Code 智能启动器（自动 API 切换）
  * 问题：智谱 5小时30M token 限额 → 超出后 Claude Code 卡死
  * 方案：智谱(主) + Gemini(备用)，自动检测无缝切换
  * 架构：smart_claude.py(检测+切换) + gemini_proxy.py(格式转换代理)
  * gemini_proxy.py：本地 Anthropic→Gemini 格式转换（支持流式SSE）
    - 将 Anthropic Messages API 格式转为 Google Gemini 原生格式
    - 支持流式和非流式两种模式
    - 支持 system prompt、多轮对话
    - 端口：4000
  * smart_claude.py --auto：自动模式
    - 缓存机制：智谱正常时3分钟内跳过检测（0.03s，无感）
    - 缓存过期或429 → 检测智谱 → 不可用则启动代理+切Gemini
    - 智谱恢复后自动切回
  * .zshrc：claude 命令自动包装（command claude 调用原始二进制）
  * Gemini API Key：已配置（api_config.json → gemini节）
  * 新增依赖：google-generativeai, litellm
  * PENDING-TASKS.md：已更新 Windows 配置步骤
  * 测试：代理健康检查✅、非流式✅、流式SSE✅、自动模式缓存✅

### 2026-04-08
+ macOS Claude Code 升级完成
  * 版本：2.1.96
  * 平台：macOS (Darwin 24.2.0)
  * 安装 superpowers-zh skills（25个AI编程skills）
  * 状态：✅ 升级成功

### 2026-04-07
+ Kindle越狱项目完成
  * 设备：Kindle Paperwhite 6th Generation (KPW2)
  * 固件：5.12.2.2
  * 方法：WatchThis越狱（演示模式漏洞）
  * 状态：✅ 完成
  * 参考教程：书伴 https://bookfere.com/post/970.html
+ 桌面Python脚本清理
  * 删除5个测试/诊断脚本
  * 保留convert_to_azw3.py（完善的电子书转换工具）
+ A股更新脚本修复（daily_update_v2.py）
  * 问题：代理错误（localhost:1080）
  * 解决方案：
    - 禁用HTTP/HTTPS代理环境变量
    - 添加重试机制（最多3次，递增等待时间）
  * 影响：处理网络波动和代理配置问题
+ Claude Code CLI 升级（Windows）
  * 旧版本：通过npm安装（已卸载）
  * 新版本：v2.1.92
  * 安装位置：C:\Users\Administrator\AppData\Roaming\npm\claude.cmd
  * 配置文件：已恢复个性化CLAUDE.md（4.2KB）

### 2026-04-01
+ A股历史数据下载完成（to20260211目录）
  * 总文件数：5,180个.parquet文件
  * 数据质量：抽查合格率100%，全量统计通过
  * 数据范围：5,170个文件截止至2026-02-11（99.8%）
  * 记录数分布：平均2,940条/文件，最大6,000条（API上限）
  * 字段完整性：11列/文件，无空值
  * 数据可用性：可直接用于学术研究、量化回测、统计分析
  * 检查工具：check_data_quality.py, full_analysis.py
  * 质量报告：E:\BigA\data_quality_report.txt
+ Kindle越狱项目启动
  * 设备确认：Kindle Paperwhite 6th Generation (KPW2)
  * 固件版本：5.12.2.2（可越狱）
  * 越狱方法：WatchThis（演示模式漏洞）
  * 参考教程：书伴 https://bookfere.com/post/970.html
  * ⚠️ 重要提示：越狱会清空所有数据，需先备份
+ TaskOutput上下文窗口溢出教训
  * 问题：使用TaskOutput检查长时间运行任务，9769+行输出导致上下文溢出
  * 教训：长时间任务必须使用进度文件（JSON/CSV）或block=False非阻塞检查
  * 记录：已添加到lessons.md #20

### 2026-03-31
+ AI开发工具升级
  * GLM模型升级到5.1系列（api_config.json v2.0.0）
  * 安装superpowers-zh（25个AI编程skills）
  * 安装planning-with-files-zh（文件规划系统）
  * 确认Tushare moneyflow接口可用（2000+积分）
+ A股四步分析法系统建立
  * 创建stock-analysis-cn skill（价值/成长/质量/资金/风险五步分析）
  * 创建stock_analysis_helper.py（Tushare数据获取助手）
  * 支持多因子筛选、财务分析、资金流向分析
  * 实战案例：德美化工(观望)、长江电力(谨慎补仓)
+ 跨平台配置同步
  * 创建.claude-sync/目录同步全局配置
  * 创建sync_config.py自动检测macOS/Windows平台
  * CLAUDE.md全局配置已更新到GLM-5.1策略

### 2026-03-10
+ macOS Python环境补全
  * 对齐Windows平台核心库
  * 新安装：polars, pyarrow, fastparquet, scikit-learn, gplearn, numba, optuna, pygad, seaborn, plotly
  * 新安装：tushare, akshare, yfinance, quantstats, vectorbt, statsmodels, arch
  * 总计约160个包（macOS）
+ A股个股数据下载（macOS桌面）
  * 600377.SH 宁沪高速：2001-02-22 至 2026-03-09（6000条）
  * 600900.SH 长江电力：2003-11-18 至 2026-03-09（4991条）
  * 002054.SZ 德美化工：2006-07-25 至 2026-03-09（4728条）
  * 000001.SH 上证指数：1993-04-22 至 2026-03-09（8000条）
  * 601398.SH 工商银行：2006-10-27 至 2026-03-09（4682条）
  * 文件命名规则：股票名称+代码+起始日期+结束日期.parquet
+ 股票涨跌同步分析（皮尔逊相关系数）
  * 600377 vs 600900（2018至今）：同步率55.81%，相关系数0.2933
  * 002054 vs 600900（2018至今）：相反率51.29%，相关系数0.0093（无相关）
  * 002054 vs 600900（2023至今）：相反率56.45%，相关系数-0.1132（弱负相关）
  * 002054 vs 600900（2025至今）：相反率60.78%，相关系数-0.1022
  * 002054 vs 600900（2025-06至今）：相反率60.22%，相关系数-0.0739
  * 002054 vs 600377（2025-06至今）：相反率54.84%，相关系数-0.0368
  * 601398 vs 000001（有史以来）：同步率62.20%，相关系数0.6339（较强正相关）
  * 600900 vs 000001（有史以来）：同步率62.01%，相关系数0.4895（中等正相关）
+ 德美化工深度分析
  * 最长连涨：10天（2009-09-02至2009-09-16），涨幅+42.83%
  * 最长连跌：8天（2023-12-15至2023-12-26），跌幅-4.34%
  * 历史最高：32.81元（2009-09-16）
  * 历史最低：4.04元（2018-10-12）
  * 上市至今：-15.80%（表现不佳）

### 2026-02-12
+ A股系统完善项目完成
  * daily_update.py升级：新增市值数据获取功能
    * 创建v2版本：add_market_cap_to_biga.py的市值字段
    * 新增4个字段：总市值(万元)、流通市值(万元)、换手率(%)、量比(%)
    * API控制：日线0.62秒/次，复权0.31秒/次
  * 数据验证完成：抽查10个文件，市值数据完整性100%
  * 股票信息文件创建：stock_info.parquet
    * 包含5479只股票的基本信息（代码、名称、行业、上市日期、市场）
    * 数据来源：Tushare stock_basic API（分市场获取）
    * 用途：未来查询股票名称、行业分类等
  * 市场分布：主板3193只、深交所1392只、上交所602只、北交所292只
  * 行业分布（前10）：软件服务341只、化学原料301只、电子282只等
+ 中证500成分股历史变动数据获取完成
  * 脚本：get_zz500_index_changes_10y.py（10年完整版）
  * 数据源：Tushare index_weight API
  * API限制发现：index_weight接口只能获取1年数据，需分年度查询
  * 解决方案：从2016年到2026年逐年查询（11个年度）
  * 最终数据：zz500_index_changes_10y.parquet
    * 总记录数：60,500条
    * 时间跨度：2016-01-29 至 2026-01-30（11年）
    * 唯一股票数：1,265只
    * 数据完整性：无缺失值
  * 年度分布：
    * 2016-2025：每年6,000条
    * 2026：500条（截至当前）
  * 数据字段：
    * index_code - 指数代码（000905.SH）
    * 股票代码 - 成分股代码
    * 变动日期 - 变动发生日期
    * 权重 - 成分股权重
  * 技术细节：
    * API返回的列名为trade_date（非index_date）
    * 需使用drop_duplicates()去除重复记录
    * API间隔：0.31秒（遵守200次/分钟限制）

### 2026-02-11
+ A股520回顾性研究筛选项目（已废弃）
  * 筛选条件：股价5-20元、市值80-500亿、波动率条件、2018-01-01起始
  * 结果：6只股票通过筛选，但多数2018年后上市（数据不足）
  * 用户决策：筛选条件过于苛刻，不现实，放弃520项目
+ BigA市值数据增强项目启动
  * 脚本：add_market_cap_to_biga.py
  * 功能：为所有5798个parquet文件添加市值和交易量数据
  * 新增字段：总市值(万元)、流通市值(万元)、换手率(%)、量比(%)
  * 数据源：Tushare daily_basic API
  * 批处理模式：500文件/批，API间隔0.31秒（200次/分钟限制）
  * 进度追踪：market_cap_add_progress.json
  * 当前状态：处理中（499/5798文件）

### 2026-02-09
+ 数据完整性检查：838只股票达6000条记录限制
+ Tushare Pro API限制确认：pro_bar接口硬限制6000条（约24年数据）
+ 用户决策：接受当前数据（2000年后数据完整）
+ 文件组织：创建/adjfactor子目录，移动5798个复权因子文件
+ 自动更新脚本：daily_update.py（每日20:00自动更新数据）
+ 文件名修正：修正所有parquet文件起始日期与实际数据一致
+ 修复文件名重复后缀问题：_adj_factor_adj_factor → _adj_factor
+ 数据验证：将000004.parquet转换为CSV查看数据结构
+ Python库清单更新：记录173个库的分类功能（金融分析、机器学习、可视化）

### 2026-02-08
+ A股数据下载系统开发完成
+ Tushare Pro集成（避免幸存者偏差）
+ 前复权数据+复权因子（学术研究标准）
+ Parquet格式存储（性能优化）
+ pandas降级到2.3.3（兼容tushare）

### 2026-02-03
+ LOCAL_PYTHON_PRIORITY rule added (save tokens)
+ Three core capabilities confirmed: API auto-switch, MCP caution, Python priority

### 2026-02-01
+ Tavily MCP added (1000次/月)
+ Tavily Skills installed (5 skills)
+ PC lag fixed (iFlytek input residue in startup)
+ Google Custom Search API failed (deprecated)
+ API usage rules established
+ File→HTML tool developed (converter_fixed.py)

### 2026-01-29
+ Windows medical chart reproduction (图1)
+ PubMed consultation system (PUBMEDCONSULT.py)
+ Key lessons: NO grid lines in academic charts

### 2026-01-28
+ GLM-4.7 auto-selection system
+ API priority rules established

### 2026-01-11
+ PPT generator bugs fixed (table abuse, content repetition)
+ Layout optimization (spacing, numbering, section covers)

### 2026-01-10
+ File output format rules established

### 2026-01-09
+ Literature search: IL-1β, miR-155, circRNA markers

### 2026-01-08
+ Mac dev environment configured (WeChat Dev Tools, VS Code, Node.js)

### 2026-01-07
+ MCP servers installed (4 core)
+ C drive cleaned (17.5 GB freed)

### 2026-01-06
+ Claude Code tutorial processed
+ Course scraping completed (21 chapters)

### 2026-01-05
+ GitHub sync established
+ Memory optimization (archive created)
+ iPhone-style alarm clock developed

---

## POLYMATH_CONTEXT

### CURRENT_MODE
- **Mode B (全栈开发)** - Multi-project active

### USER_RULES
- Development: No hardcoded keys, concise code, game priority logic
- Research: Cite权威文献, prefer recent, keywords specific
- Platform: Auto-detect (win32=Windows, darwin=macOS)

### SKILLS_MAPPING
1. **medical-research** → Mode C
   - Keywords: 牙髓, VPT, 活髓保存, 国自然, 文献, PubMed
   - Features: Literature search, grant writing, statistics

2. **weapp-development** → Mode B
   - Keywords: 小程序, 微信, 云开发, wxml, wxss
   - Features: Mini program dev, cloud functions, data export

3. **quantitative-trading** → Mode B
   - Keywords: 交易, 股票, A股, Tushare, 量化, 策略, 回测
   - Features: API integration, data download, backtesting, survivorship bias avoidance

4. **game-logic** → Mode B
   - Keywords: 游戏, 7局4胜, 流局, 比赛
   - Features: 7-game series, flow draw priority

5. **python-tutoring** → Mode A
   - Keywords: 孩子, 儿子, 8岁, 学编程
   - Features: Bilingual teaching, gamified lessons

---

## QUICK_REFERENCES

### PubMed_API
- esearch: Search → PMID list
- esummary: Basic info (title, author, DOI)
- efetch: Full abstract (Background, Methods, Results, Conclusions)
- Limit: 3 req/sec (0.34s interval)
- Sort: sort='relevance'
- Dedup: By PMID

### Chart_Standards
- Boxplot width: 0.17
- NO grid lines
- Axis: reasonable range
- Colors: light blue + gray + red
- Scatter: bidirectional jitter
- Font: Microsoft YaHei

### File_Read_Strategy
- PDF → Python local (pypdf/pdfplumber)
- Word → python-docx
- Excel → openpyxl/xlrd
- Images/TXT → Read tool

---

### 2026-04-06
+ A股数据更新脚本修复（daily_update_v2.py）
  * 问题：复权因子文件名重复追加 `_adj_factor` 后缀
  * 错误示例：`603617-xxx-L_adj_factor_adj_factor_adj_factor_...parquet`
  * 根本原因：第353行解析文件名时未清理已存在的后缀
  * 解决方案：添加后缀清理逻辑（第355-357行）
    ```python
    if status.endswith('_adj_factor'):
        status = status[:-11]  # 去掉'_adj_factor'（11个字符）
    ```
  * 文件名清理：创建并运行 `clean_adjfactor_filenames.py`
    - 成功清理：5,187个复权因子文件
    - 清理率：100%（错误0个）
    - 清理脚本：E:\BigA\clean_adjfactor_filenames.py
+ 电子书转换脚本修复（convert_to_azw3.py）
  * 路径更新：Calibre 路径改为 D:\Program Files\Calibre2
  * 编码修复：添加 UTF-8 输出支持（解决 Windows 中文显示问题）
  * 文件格式支持优化：
    - 移除：AZW、AZW3（DRM保护，无法转换）
    - 移除：DOC（需要 Antiword 工具）
    - 保留：PDF、EPUB、MOBI、TXT、HTML、HTM、DOCX、RTF
  * subprocess 调用修复：
    - 问题：使用 stdout=subprocess.DEVNULL 干扰 ebook-convert 运行
    - 问题：使用 encoding='gbk' 导致参数解析错误
    - 解决：移除 stdout 重定向，使用 capture_output=True
  * 参数优化：
    - 移除失败参数：--max-line-length、--pdf-hyphenate、--pdf-page-numbers
    - 保留安全参数：--output-profile kindle_pw、--enable-heuristics、--pretty-print、--chapter-mark pagebreak
    - 分级处理：TXT/EPUB 等使用默认参数，PDF 使用优化参数
  * 性能优化：
    - 按文件大小排序（小文件优先，避免大文件阻塞）
    - 动态超时设置：小文件（<10MB）2分钟，大文件（≥10MB）5分钟
    - 显示文件大小和转换耗时
    - 大文件（>20MB）每30秒显示进度
  * 转换结果：
    - 总文件数：286个
    - 成功转换：283个（99.0%）
    - 超时跳过：12个（大文件超过5分钟限制）
    - 最终输出：E:\calied\ 目录下 283 个 .azw3 文件
    - 转换完成时间：2026-04-06
  * 跳过文件清单：
    - 《永恒的终结》作者：阿西莫夫.pdf (3.1MB)
    - 金日成回忆录-与世纪同行中文版5.pdf (17.5MB)
    - 倚天屠龙记(共四册).pdf (9.6MB)
    - 天龙八部（全五册）.pdf (11.4MB)
    - 054【网师】《非理性的人》(2011批注版).pdf (19.2MB)
    - 008《清日战争》【高清完整版】.pdf (37.3MB)
    - 043霍乱时期的爱情.pdf (39.6MB)
    - 追寻现代中国·三卷合集（史景迁）.pdf (50.4MB)
    - 于建嵘《安源实录-一个阶级的光荣与梦想》全本pdf.pdf (183.4MB)
    - 其他3个小体积PDF（参数兼容问题）
+ 工具安装：MarkItDown（微软开源 CLI）
  * 功能：将各种文档格式转换为 Markdown
  * 用途：科研文献分析、文档预处理
  * 安装命令：pip install 'markitdown[all]'
  * 版本：0.1.5
+ 电子书转换后处理（体积优化）
  * 问题发现：转换后总体积从 2.70 GB → 3.43 GB（增加27%）
  * 原因分析：78个PDF转AZW3后体积膨胀（2-7倍），12个超时未转换
  * 解决方案：删除体积变大的AZW3，保留原PDF
  * 优化结果：
    - 删除78个膨胀的AZW3文件，节省 2.83 GB
    - 保留197个优质AZW3（转换后体积变小）
    - 复制89个PDF到calied文件夹
  * 最终统计（E:\calied）：
    - AZW3文件：197个（0.59 GB）
    - PDF文件：89个（1.96 GB）
    - 总文件数：286个 + 1个清单文件
    - 总大小：2.55 GB（相比转换后节省0.88 GB）
  * 文件清单：创建 `PDF文件清单_无对应AZW3.md`
    - 列出89个需要使用原PDF的书籍
    - 包含文件名和大小信息
  * PDF转换膨胀案例：
    - 6.7倍：12.97 MB → 86.55 MB（010间谍王）
    - 4.3倍：17.86 MB → 77.15 MB（011封建社会）
    - 3.1倍：31.51 MB → 96.17 MB（法国革命史）
  * 使用建议：所有286个文件（197个AZW3 + 89个PDF）可直接复制到Kindle使用

---

### 2026-04-14
+ GitHub 项目评估（4个项目）
  * **claude-mem** (53k stars) — 自动记忆插件
    - 评估结论：❌ 不安装
    - 原因：与现有memory.md系统重叠、跨平台同步困难、依赖链长、AI压缩消耗额外token
    - 关联$CMEM代币（Solana），带投机色彩
  * **fish-speech** (29.4k stars) — 文字转语音（TTS）
    - 评估结论：✅ 记录为备用方案（未部署）
    - 能力：80+语言TTS、声音克隆（10-30秒）、情感标签控制
    - Windows GPU RTX 4060 Ti 满足最低要求（8GB VRAM）
    - 使用方式：先用在线版，需要时再本地部署
    - REPO: https://github.com/fishaudio/fish-speech
  * **antigravity-awesome-skills** (33k stars) — 1404个技能合集
    - 评估结论：❌ 不安装
    - 原因：已有superpowers-zh覆盖核心需求、1404个太多导致上下文膨胀、质量参差
    - 按需使用：未来有特定需求可从在线目录单独找技能
  * **everything-claude-code (ECC)** (154.5k stars) — 全面增强包
    - 评估结论：❌ 不安装
    - 原因：面向专业全栈团队、场景不匹配、会吃掉上下文窗口、与现有配置冲突
    - 值得借鉴的理念：token优化、战略压缩、上下文管理
+ 工作流优化评估
  * 评估ECC的四项优化理念是否适合融入工作流：
    - 模型切换优化：❌ 不需要（已固定glm-5.1）
    - 自动压缩阈值：❌ 不需要（手动管理memory更精准）
    - 思考token限制：❌ 不需要（可能影响复杂任务执行）
    - 战略压缩规则：❌ 不需要（手动memory管理已覆盖此理念）
  * 结论：现有工作流（手动memory + 固定模型 + 6个MCP）已是最优配置
+ 硬件信息更新
  - Windows: NVIDIA RTX 4060 Ti, Python 3.14
  - macOS: Python 3.14
  - 两台电脑均未部署本地大模型

---

## END

**Full history**: See `memory-archive.md`
+ claude-api-switcher 开源项目规划（产品需求已确认）
  * 定位：Claude Code API 自动切换器，中国大陆用户，轻量工具
  * 第一期服务商：智谱(直连) + DeepSeek(代理) + 千问(代理)
  * 安装：pip install claude-api-switcher → config → 重启终端
  * 配置：~/.claude-api-switcher/config.json，2-3个Key按优先级
  * 自愈：代理健康检查 + 自动重启 + 降级跳过
  * 切换提示：显示服务商名 + 限额重置时间
  * PRD文档：claude-api-switcher-PRD.md
  * 开源时机：代码写好测试通过后再公开
  * 状态：需求确认完成，待开发

**Last updated**: 2026-04-21 (德州扑克教程扩写 + NCCL工作流固定化)
