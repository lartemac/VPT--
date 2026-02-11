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
- WIN: PowerShell, `\` separator
- MAC: bash/zsh, `/` separator
- DETECT: Check `Platform` env var

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

3. **A股数据下载系统** (A-Stock Data Downloader)
   - PURPOSE: Academic research backtesting (avoid survivorship bias)
   - TECH: Tushare Pro + Python + Parquet
   - PATH: E:\BigA\
   - STATUS: ✅ COMPLETED (2026-02-09) + 数据增强 (2026-02-11)
   - FEATURES:
     * Include all stocks (L+D+P) to avoid survivorship bias
     * Use QFQ (前复权) for price continuity (already adjusted)
     * Parquet format for performance
     * Auto-download adj_factor for backup
     * Daily auto-update at 20:00 via Windows Task Scheduler
   - SCRIPTS:
     * tushare_downloader_v2.py (main downloader)
     * start_download.py (auto-start script)
     * daily_update.py (daily auto-update script)
     * add_market_cap_to_biga.py (market cap enhancer)
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

---

## RULES

### DEV_RULES
- NO hardcoded API keys (use env vars)
- Code: concise, efficient, no over-engineering
- Game priority: 1.正常击杀 > 2.流局判定 > 3.平局

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

### API_USAGE (GLM-4.7)
- Auto-select model based on task (no user prompts)
- glm-4-plus: Medical, research, complex code
- glm-4-flash: Simple Q&A, quick snippets
- glm-4-air: Light tasks, batch processing
- API Key: REDACTED_GLM_API_KEY

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

## END

**Full history**: See `memory-archive.md`
**Last updated**: 2026-02-11 (市值数据增强处理中) (自动监控部署中)
