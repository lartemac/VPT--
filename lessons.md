# Claude Code 经验教训集

> **定位**：专门收集工作中积累的经验教训和失败项目，避免重复犯错
> **更新频率**：不定期更新（遇到重要问题时记录）
> **同步方式**：通过 Git 同步到 GitHub
> **使用方式**：在需要时查阅，不在每次启动时自动加载

---

## 软件开发相关

### 1. PyInstaller 打包第三方 GUI 库的陷阱
**日期**：2026-02-01
**项目**：桌面文件转换工具（converter.exe）

**问题现象**：
- 使用 PyInstaller 打包 tkinterdnd2 库后，生成的 .exe 文件双击无响应
- 鼠标沙漏闪烁，但界面不显示
- 任务管理器显示进程短暂运行后立即退出

**根本原因**：
- PyInstaller 打包第三方 GUI 库（如 tkinterdnd2）容易出现依赖缺失
- 复杂的拖拽功能库在单文件打包模式下可能无法正确加载

**解决方案**：
- ❌ 放弃拖拽功能，仅保留按钮选择文件方式
- ✅ 使用标准 tkinter 组件（filedialog），稳定性更好
- ✅ 简化设计比复杂功能更可靠

**经验教训**：
- ⚠️ PyInstaller 打包第三方 GUI 库容易出现依赖缺失
- ✅ 简化设计（仅按钮选择）比复杂功能（拖拽）更稳定可靠
- ✅ 12 MB 单文件 exe 已包含所有依赖，可独立运行
- 💡 如果打包失败，优先考虑功能简化而非依赖修复

---

### 2. Windows 文件被锁定无法删除的解决方案
**日期**：2026-02-01
**问题**：旧版 .exe 文件被系统锁定，无法删除或替换

**尝试方案（均失败）**：
- 直接删除（文件被占用）
- 移除只读属性后删除
- 重启 Windows 资源管理器后删除
- 使用 process explorer 查找占用进程

**最终解决方案**：
```python
import ctypes
from ctypes import wintypes

# 标记文件在重启时删除
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
MOVEFILE_DELAY_UNTIL_REBOOT = 0x4
kernel32.MoveFileExW(old_file, None, MOVEFILE_DELAY_UNTIL_REBOOT)
```

**经验教训**：
- 💡 Windows 文件被锁定时可使用 MoveFileEx API 标记重启删除
- ⚠️ 可能的原因：Windows Defender、文件索引服务、云同步软件

---

### 3. Google Custom Search API 已停用
**日期**：2026-02-01
**问题**：反复配置 Google Custom Search API，持续报 403 错误

**排查过程**：
- ✅ 确认 API 已启用
- ✅ 确认 CX ID 有效
- ✅ 移除 API 所有限制
- ✅ 等待 API 激活
- ✅ 尝试多个项目和新 API Key
- ❌ 所有尝试均失败

**根本原因**：
- ⚠️ Google Custom Search API 已被官方停用/限制访问
- 403 错误不是配置问题，而是服务本身已不可用

**经验教训**：
- ❌ Custom Search API 已被 Google 停用，不应再尝试配置
- ⭐ 需要使用新的搜索服务：Vertex AI Search（discoveryengine.googleapis.com/v1）
- ⭐ 或继续使用 DuckDuckGo（完全免费、无需 API Key）
- 💡 Gemini 助手建议使用新版接口：需要 Engine ID + OAuth/Service Account 认证

---

### 4. 路径问题的系统性解决（相对路径 vs 绝对路径）
**日期**：2026-01-11
**项目**：PPTGen v2.1（PyInstaller 打包）

**核心问题**：
- PyInstaller 打包后，`sys.executable` 指向临时解压目录
- 导致相对路径和 `config.json` 查找失败
- 错误信息：`[Errno 2] No such file or directory: C:\Users\Administrator\AppData\Local\Temp\_MEI391162\temp\ppt_outline.json`

**解决方案**：
```python
# 获取真实工作目录
if getattr(sys, 'frozen', False):
    # PyInstaller 打包后的可执行文件
    real_path = os.path.dirname(sys.executable)
else:
    # 正常 Python 脚本
    real_path = os.path.dirname(os.path.abspath(__file__))

# 修改工作目录
os.chdir(real_path)
```

**经验教训**：
- ✅ `os.chdir()` 修改工作目录，解决相对路径问题
- ✅ 三处统一修复逻辑（主程序、GUI、生成器），避免路径不一致
- ⚠️ 打包后的可执行文件工作目录会变化，不要依赖 `os.getcwd()`

---

### 5. Python 脚本编码问题（Windows GBK vs UTF-8）
**日期**：2026-01-10
**问题**：Windows GBK 编码无法处理特殊字符（\xa0）

**解决方案**：
```python
# 清理不可见字符
text = text.replace('\xa0', ' ')
text = text.replace('\u3000', ' ')

# 统一使用 UTF-8 编码
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()
```

**经验教训**：
- ⚠️ Windows GBK 编码无法处理特殊字符（\xa0），需要提前清理
- ✅ 统一使用 UTF-8 编码读写文件
- ✅ 处理外部数据时先清理不可见字符

---

## API 与网络相关

### 6. PubMed API 使用规范
**日期**：2026-01-29
**项目**：PUBMEDCONSULT.py（医学文献查询系统）

**API 限制**：
- 请求限制：每秒最多 3 次（0.34 秒间隔）
- 无月度限制（与 Claude WebSearch 不同）
- 使用官方 E-utilities API

**最佳实践**：
```python
import time

# 遵守 API 请求限制
time.sleep(0.34)  # 每次请求间隔 0.34 秒

# esummary：基础信息（标题、作者、DOI）
# efetch：完整摘要（Background、Methods、Results、Conclusions）
```

**经验教训**：
- ⭐ PubMed API 无月度限制，可放心使用
- ⭐ 排序使用 `sort='relevance'` 提高相关性
- ⭐ 基于 PMID 去重，避免重复文献
- ⭐ 相关性评分系统：系统评价/Meta分析 +8分，RCT +5分

---

### 7. MCP 和 WebSearch 使用限制（节约 API 调用）
**日期**：2026-02-01
**问题**：MCP 服务次数每月刷新，需要优化使用策略

**新规范**：
- ❌ 禁止直接调用 MCP 服务和 WebSearch
- ✅ 必须先询问用户是否同意调用
- 💡 目的：节约有限的 API 调用次数

**本地 Python 替代方案**：
| 任务 | Python 库 | Token 节省 |
|------|----------|-----------|
| 文件操作 | os, pathlib, shutil | 1000+ |
| 数据处理 | pandas, numpy | 2000+ |
| Excel 读写 | openpyxl, xlrd, pandas | 1500+ |
| Word 读写 | python-docx | 1500+ |
| PDF 提取 | pypdf, pdfplumber | 2000+ |
| 网页爬取 | requests, BeautifulSoup4 | 1000+ |
| 图片处理 | Pillow (PIL) | 1000+ |
| 数据可视化 | matplotlib, seaborn | 1500+ |

**经验教训**：
- 💡 优先使用本地 Python 脚本，避免不必要的 API 调用
- 💡 评估 Python 脚本的可行性后再考虑 MCP/WebSearch
- ❌ 图片 OCR：部分可用 Python 替代（Tesseract/PaddleOCR，仅提取文字）
- ❌ 图片理解：必须用 MCP（理解内容、分析布局）

---

## 学术与科研相关

### 8. 学术图表绘制规范（无网格线）
**日期**：2026-01-29
**用户明确要求**："记住，以后绘图不要随意画虚线，这不符合学术文章图表规范"

**规范要点**：
- ❌ 禁止在学术图表中画网格线/虚线
- ❌ 网格线会被视为装饰性元素，降低专业性和可读性
- ✅ 除非用户明确要求，否则默认 `ax.grid(False)`

**其他规范**：
- 箱线图宽度：0.17（学术图表更窄）
- Y 轴范围：合理范围（不一定是 0-10）
- 图例：仅在有需要时显示，避免遮挡数据
- 分辨率：300 DPI（学术出版要求）

**经验教训**：
- ⭐⭐⭐ 学术图表不应包含网格线/虚线装饰元素
- ⭐ 箱线图宽度 0.17（原 0.5 的 1/3）
- ⭐ 散点双向抖动（水平+竖直）使分布更自然
- ⭐ P 值标注位置需在箱线图上方预留足够空间

---

### 9. 文献引用验证的失败尝试
**日期**：2026-01-09
**项目**：国自然标书引用验证

**尝试方案（均失败）**：

1. **训练数据验证**（❌ 用户拒绝）
   - 问题：用户明确反对使用训练数据验证引用

2. **WebSearch 验证**（❌ 达到使用上限）
   - 问题：WebSearch 工具提示"Usage limit reached for 1 month"

3. **GLM-4 直接验证**（❌ 无网络访问）
   - 问题：GLM-4 Flash API 没有实时网络访问权限

4. **PubMed 直接爬取**（❌ 403 错误）
   - 问题：直接爬取 PubMed 网页遇到 403 Forbidden

5. **PubMed E-utilities API + 智能算法**（⚠️ 中文匹配失败）
   - 核心问题：中文引用语句无法用英文正则表达式提取关键词
   - 结果：所有匹配都是 0/15 分

**最终结果**：
- 36 条引用中，18 条不相关（50.0%）
- 发现重复文献：Ref [6] 和 [16] 是同一篇文献
- 未找到 PMID 的 4 篇文献

**经验教训**：
- ⚠️ 语言差异问题：中文引用语句 vs 英文文献摘要，正则表达式匹配完全失效
- ⚠️ 需要人工验证引用的准确性
- ⚠️ 使用 PubMed E-utilities API（而非网页爬取）
- ⚠️ 提前暴露问题，避免被评审专家质疑

---

## 系统与工具相关

### 10. 电脑卡顿问题诊断与解决（讯飞输入法残留）
**日期**：2026-02-01
**问题**：安装讯飞输入法后电脑变卡，卸载后仍然卡顿

**问题诊断**：
- ✅ 讯飞安装目录已删除（无残留文件）
- ⚠️ **关键问题**：启动项中仍有讯飞输入法残留
  - 残留项：`iFlyInput: "D:\Program Files (x86)\iFlytek\iFlyIME\3.0.1746\iFlyInput.exe" /start`
  - 原因：卸载时启动项未清理，导致系统每次启动尝试运行不存在的程序

**解决方案**：
1. 删除启动项（最关键）
   - 方法 A：任务管理器 → 启动 → 禁用 iFlyInput
   - 方法 B：注册表删除
     - 路径：`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
     - 删除项：iFlyInput

2. 清理系统临时文件
   - 运行 cleanmgr（磁盘清理工具）
   - 手动清理 %temp% 和 C:\Windows\Temp

**重要教训**：
- ⭐ 安装软件时注意：不要勾选"开机启动"
- ⭐ 卸载软件后务必检查启动项
- ⭐ 软件选择原则：优先轻量级，避免"全家桶"

---

### 11. Windows Git 推送 SSL/TLS 问题
**日期**：2026-01-06
**问题**：无法推送到 GitHub，SSL/TLS 连接失败

**错误信息**：
```
fatal: unable to access 'https://github.com/lartemac/VPT--/':
Failed to connect to github.com port 443 after 21078 ms: Couldn't connect to server
```

**解决方案**：
```bash
git config --global http.sslBackend openssl
git config --global http.postBuffer 524288000
```

**配置生效**：永久保存，以后推送 GitHub 不会再有问题

**经验教训**：
- ⚠️ Windows Git 的 schannel 后端与某些服务存在兼容性问题
- ✅ 切换到 openssl 后端可解决大部分 SSL/TLS 问题
- ✅ 增加 http.postBuffer 提高大文件传输稳定性

---

### 12. 桌面顽固空文件夹删除问题（待重启解决）
**日期**：2026-01-06
**问题**：桌面有两个无法删除的空文件夹（"落户"和"PDF"）

**尝试方案（均失败）**：
- ❌ PowerShell Remove-Item（失败：文件被占用）
- ❌ cmd rmdir 命令（失败：文件被占用）
- ❌ 移除只读/系统属性后删除（失败）
- ❌ 重启 Windows 资源管理器后删除（失败）
- ❌ robocopy 清空文件夹后删除（失败）
- ❌ 获取所有权和权限后删除（失败）

**可能原因**：
- 百度网盘同步功能锁定
- 其他云同步软件（OneDrive、Dropbox）

**经验教训**：
- ⚠️ 排查问题时应优先检查常用软件的同步/锁定功能
- 💡 如果无法删除，检查百度网盘、OneDrive 等云同步软件

---

## 代码规范相关

### 13. 文件命名规范
**日期**：2026-01-10
**原则**：简洁、描述性、易识别

**Python 文件命名**：
- ✅ 推荐：`图1绘制.py`、`PUBMEDCONSULT.py`、`glm_analyzer.py`
- ❌ 避免：`test_`、`temp_`、`debug_` 等临时性前缀

**Excel 文件命名**：
- ✅ 推荐：`[query_summary]_pubmed查询.xlsx`
- ✅ 示例：`pulpitis_pain_manage_pubmed查询.xlsx`

**经验教训**：
- ⭐ 文件名应描述功能而非临时状态
- ⭐ 删除临时测试脚本，保持目录整洁
- ⭐ 中文命名在科研场景下更直观

---

### 14. GLM-4 API 使用规范
**日期**：2026-01-28
**规则**：自动选择模型，不询问用户

**模型选择原则**：
- `glm-4-plus`：医学、科研、复杂代码
- `glm-4-flash`：简单问答、快速代码片段
- `glm-4-air`：轻量任务、批处理

**禁止事项**：
- ❌ 禁止询问用户"使用哪个模型？"
- ❌ 禁止让用户手动指定模型参数

**经验教训**：
- ⭐ AI 模型选择应由 AI 根据任务自动判断
- ⭐ 减少用户决策负担，提高效率

---

### 15. Claude API Key 混淆问题
**日期**：2026-01-11
**问题**：用户提供的 Claude API key 实际是智谱 AI GLM 的 key

**错误现象**：
- Claude API 返回 401 错误（无效的 x-api-key）
- `anthropic` 库调用失败

**解决方案**：
- 使用正确的 API（智谱 GLM：`zhipuai` 库）
- API Key: `REDACTED_GLM_API_KEY`

**经验教训**：
- ⚠️ API Key 格式不同（Claude: sk-ant-xxx, GLM: xxx.xxx）
- ⚠️ 测试 API 连接前，先确认 API 类型
- ✅ 使用 `zhipuai` 库调用 GLM-4 API

---

## 项目管理相关

### 16. 跨平台开发路径混淆问题
**日期**：2026-01-10
**问题**：多次引用 Mac 路径导致脚本在 Windows 系统上失败

**解决方案**：
```python
import os

# 平台检测
if os.name == 'nt':
    # Windows
    base_path = r'D:\cc-github'
else:
    # macOS/Linux
    base_path = '~/cc-github'
```

**经验教训**：
- ⚠️ 避免硬编码路径
- ✅ 使用平台检测自动切换路径
- ✅ 配置文件中定义路径变量

---

### 17. PPT 生成器的三个核心问题修复
**日期**：2026-01-11
**项目**：PPTGen v2.0

**用户反馈的三个关键问题**：

1. **表格功能被滥用**
   - 问题：70% 检测阈值太低，普通文本被强制转表格
   - 修复：提高到 90%，至少 3 个内容项才考虑表格

2. **表格右侧列空白**
   - 问题：有冒号但冒号后为空时，表格右侧列完全空白
   - 修复：智能解析内容，确保表格有实际内容

3. **AI 解析长文档重复内容（核心）**
   - 问题：同一一级目录下的内容重复十余次
   - 修复：完全重构提示词，实现文档性质判断和树形结构

**经验教训**：
- ⭐ AI 提示词需要根据文档类型动态调整
- ⭐ 表格检测需要更严格的阈值和规则
- ⭐ 树形结构（Lv 0 → Lv 1 → Lv 2）避免内容重复

---

## 未分类经验
---

### 20. A股520回顾性研究筛选项目失败（多条件筛选过于苛刻）
**日期**：2026-02-11
**项目**：A股520回顾性研究筛选

**原始筛选条件**：
1. 股价5-20元区间
2. 市值80-500亿元
3. 2018-01-01至今从未连续10个交易日涨跌幅小于1%（波动率条件）
4. 未退市、未ST

**筛选结果**：
- 第一阶段（股价5-20元）：296只股票通过
- 第二阶段（波动率1%）：0只股票通过（条件过于严格）
- 调整后（降低波动率阈值）：6只股票通过全部条件
- 问题：6只股票中仅603885.SH在2018年前上市，其余均为2019年后上市
- 根本问题：数据时间窗口不足，无法进行2018年起的回顾性研究

**股票名称更正**：
- 001369.SZ = 双欣环保
- 301039.SZ = 中集车辆
- 301301.SZ = 川宁生物
- 601022.SH = 宁波远洋
- 603565.SH = 中谷物流
- 603885.SH = 吉祥航空

**用户决策**：
- "520项目已经可以放弃了，这个选定标准太苛刻，不现实"
- "这只能说明我的筛选条件太过于苛刻"

**经验教训**：
- ⚠️ 多条件交叉筛选时，每个条件都会大幅减少候选股票数量
- ⚠️ 时间窗口要求（2018年起）+ 股价/市值限制 = 数据严重不足
- ⚠️ 大多数优质股票（2019年后上市的科创板、创业板）被时间窗口排除
- ⭐ 历史数据要求与数据可用性需提前评估（API限制6000条记录≈24年）
- ✅ 及时止损：发现筛选条件不合理时，果断放弃并调整方向
- ✅ 基础数据完善更重要：转向为全部5798只股票添加市值数据


### 18. Markdown 转 PDF 的多次尝试
**日期**：2026-01-07

**尝试方案**：

1. **markdown + weasyprint**（⚠️ 待配置）
   - 问题：tinycss2 版本冲突（weasyprint 要求 ≥1.5.0，当前 1.4.0）
   - 影响：PDF 生成失败

2. **fpdf2**（❌ 不支持 Markdown）
   - 问题：需要手动转换 Markdown 到 HTML

3. **pypandoc**（⚠️ 需安装 pandoc）
   - 问题：需要外部依赖

4. **pdfkit**（⚠️ 需安装 wkhtmltopdf）
   - 问题：需要外部依赖

**经验教训**：
- ⚠️ Markdown 转 PDF 工具都有依赖问题
- ✅ 推荐方案：pandoc（命令行工具）+ 基础 CSS
- ⚠️ 图表/图片支持待完善

---

### 19. Claude Code 课程抓取项目（已废弃）
**日期**：2026-01-06
**状态**：内容已整合，源文件已删除

**最终成果**：
- 10 个教程文件（.md、.docx、.html、.pdf）
- 约 17.5 MB 的文件已清理

**经验教训**：
- ⭐ 网页抓取内容需要及时整理，避免占用磁盘空间
- ⭐ 整合后删除源文件，保持项目整洁

---

## 总结与原则

### 核心原则

1. **简洁高效**
   - 代码要求：简洁、高效，避免过度设计
   - 功能优先：简化设计比复杂功能更可靠

2. **资源节约**
   - 优先使用本地工具，避免不必要的 API 调用
   - MCP/WebSearch 前必须征得用户同意

3. **学术规范**
   - 学术图表不应包含网格线/虚线装饰元素
   - 引用验证需要人工确认，不可完全依赖 AI

4. **跨平台兼容**
   - 避免硬编码路径
   - 使用平台检测自动切换

5. **错误处理**
   - 遇到问题时，优先检查常用软件的同步/锁定功能
   - API 失败时，考虑替代方案而非反复重试

### 避免重复犯错的检查清单

- [ ] PyInstaller 打包是否使用了第三方 GUI 库？→ 考虑简化功能
- [ ] 是否使用了硬编码路径？→ 使用平台检测
- [ ] 学术图表是否包含网格线？→ 删除网格线
- [ ] 是否直接调用 MCP/WebSearch？→ 先询问用户
- [ ] 文件命名是否使用了 test_/temp_/debug_ 前缀？→ 改用描述性名称
- [ ] 是否混淆了 API Key 类型？→ 确认 API 类型
- [ ] 卸载软件后是否检查了启动项？→ 清理启动项

---

**最后更新**：2026-02-11
**维护者**：FattyTiger
**版本**：v1.0
