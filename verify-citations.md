# 引用真实性检验 Skill

对中文学术论文中的引用文献进行真实性检验，验证正文及表格中每一条带引用角标的断言是否与所引文献的实际内容一致。

## 输入参数

- $ARGUMENTS（必需）：待检验文件路径（支持 PDF / .doc / .docx / .txt）

## 执行流程

### 第一步：原始文件转为 Markdown（多格式支持）

根据输入文件格式自动选择转换方式，统一输出为 Markdown：

#### PDF 文件

使用 opendataloader-pdf（需 JDK 17），输出干净 Markdown：

```bash
# Windows
$env:JAVA_HOME = 'D:\Java\jdk-17.0.19+10'
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
java -jar "D:\opendataloader-pdf\opendataloader-pdf.jar" --input "输入路径" --output "输出md路径" --format markdown

# macOS
export JAVA_HOME=/path/to/jdk17
java -jar opendataloader-pdf.jar --input "输入路径" --output "输出md路径" --format markdown
```

#### .doc 文件（旧版 Word 二进制格式）

使用 Word COM 对象（Windows）转为 TXT：

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("输入路径")
$doc.SaveAs([ref]"输出txt路径", [ref]2)   # 2 = wdFormatText
$doc.Close()
$word.Quit()
```

macOS 上使用 `textutil` 或 LibreOffice 命令行：
```bash
textutil -convert txt "输入路径" -output "输出txt路径"
```

#### .docx 文件

优先使用 `pandoc`：
```bash
pandoc "输入路径" -f docx -t markdown -o "输出md路径"
```

备选：Word COM 对象（Windows）或 python-docx 库提取文本。

#### 输出位置

所有转换后的 MD/TXT 文件统一保存到 `D:\cc-github\temp_docs\`（Windows）或 `~/cc-github/temp_docs/`（macOS）。

### 第二步：提取引用断言和参考文献

用 Python 脚本从 Markdown 中提取：

1. **引用断言**：正文和表格中所有带 `[n]` 或 `[n-m]` 角标的句子
   - 提取断言文本 + 引用的文献编号
   - 合并同一断言中连续引用的范围（如 [3-5] → [3,4,5]）
   - 保存为 `individual_claims.json`

2. **参考文献列表**：文末参考文献列表
   - 提取每条文献的编号、标题、完整引用信息
   - 保存为 `citation_claims.json`

```python
import re, json

# 提取断言（示例逻辑）
claim_pattern = r'([^\n。]+[。])\s*[［\[]([\d,\-‐–]+)[］\]]'
# 提取参考文献
ref_pattern = r'^\s*(\d+)\s*[．.]\s*(.+)'
```

### 第三步：智能分组并行验证（核心步骤）

**根据断言数量和涉及文献数动态决定 Agent 数量：**

```
# 拆分逻辑（Python伪代码）
total_claims = len(claims)       # 断言总数
unique_refs = len(set(all_refs)) # 涉及的唯一文献数

if total_claims <= 15:
    agent_count = 2              # 少量断言，2个Agent足够
elif total_claims <= 40:
    agent_count = 3              # 中等规模
elif total_claims <= 80:
    agent_count = 4              # 较大规模（如62条断言）
elif total_claims <= 130:
    agent_count = 6              # 大规模
else:
    agent_count = min(10, total_claims // 15)  # 超大规模，上限10个

# 每个Agent分配的断言数（尽量均匀）
batch_size = ceil(total_claims / agent_count)
```

**拆分原则：**
- 每个 Agent 负责约 12-18 条断言（PubMed API 请求间隔0.5s，每条约需2-3次请求，一个Agent完成约需10-15分钟）
- Agent 数量上限为 10（过多会同时消耗大量 API 配额，反而触发限流）
- 如果涉及大量中文文献（PubMed无法检索），可适当减少 Agent 数量
- 确保**同一文献**的多条断言尽量分到同一 Agent，避免重复检索同一篇文献

**每个验证 Agent 的标准工作流程：**

1. 通过 PubMed eutils API 逐条查找文献摘要：
   ```
   # 搜索文献
   curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term=作者+关键词+年份"
   
   # 获取摘要
   curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID&retmode=xml&rettype=abstract"
   ```

2. 对比断言内容与文献摘要中的实际结论

3. 判定每条断言为以下之一：
   - ✅ **准确**：断言内容与文献摘要结论完全一致
   - ⚠️ **部分准确**：方向正确但存在细节偏差（如数据来源不在摘要中、引用的机制非该文献核心内容）
   - ❌ **不准确**：事实性错误（如名称写错、方向相反、数据捏造）
   - ❓ **无法验证**：中文文献（PubMed未收录）或文献信息不完整

4. 输出格式要求：
   - 每条断言：编号、引用文献、判定、详细说明（含摘要关键语句引用）
   - 汇总表：准确/部分准确/不准确/无法验证的数量统计
   - 重点问题清单：按严重程度排序

**关键技术注意事项：**
- Python脚本必须设置 UTF-8 编码：`sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`
- PubMed API 请求间隔 ≥0.5秒，避免 429 限流
- 中文文献无法通过 PubMed 验证，标注为 ❓
- CrossRef API 可作为备选（通过 DOI 获取文献元数据）
- 摘要中未覆盖的数据可能在全文中有支持，需在报告中注明此限制

### 第四步：汇总生成 HTML 报告

所有 Agent 全部完成后，汇总结果生成 HTML 报告：

**报告结构：**
1. 头部：论文标题、检验范围、验证方法说明
2. 统计卡片：准确/部分准确/不准确/无法验证的数量和占比
3. 比例条：可视化分布
4. 重点问题：按严重程度排序的需修正项（红色高亮）
5. 分批详情表：每批断言的逐条验证结果
6. 总体结论：综合评价和建议

**报告保存到桌面**，命名格式：`引用真实性检验报告-[论文简称].html`

### 第五步：更新 Memory 并同步 GitHub

1. 在 `memory.md` 中添加本次工作的 skill 记录
2. 创建详细的 skill 说明记忆文件
3. 执行 `git add + commit + push`

## 输出物

| 文件 | 位置 | 说明 |
|------|------|------|
| Markdown原文 | `D:\cc-github\temp_docs\` | 多格式转换结果 |
| claims JSON | `D:\cc-github\` | 提取的断言和参考文献数据 |
| HTML报告 | 桌面 | 最终验证报告 |
| memory文件 | `D:\cc-github\` | 工作流记忆 |

## 质量标准

- 每条断言必须引用文献摘要中的原句进行对比
- 数值型断言（AUC、灵敏度、成功率等）必须精确到小数点
- 通路/受体/基因名称必须逐字核对
- "部分准确"判定需明确指出哪个部分有问题
- 报告需注明"基于摘要验证，可能需查全文确认"的限制

## 已验证项目

- 江千舟等《恒牙不可复性牙髓炎的保髓之路》（2026）：62条断言，84篇文献，准确33.9%，部分准确46.8%，不准确3.2%，无法验证16.1%
- 黄颖思等《基于AI预测模型的牙周病患者复诊依从性风险分层及护理干预策略研究》（2026）：12条参考文献，6条通过（50%），1条作者错误（8.3%），4条高度疑似虚构（33.3%），2处编号结构错误

## 变体流程：直接引用列表检验

当输入为项目申请书等**不含正文引用角标**的文件时，跳过第二步（断言提取），直接对参考文献列表进行存在性检验：

1. **文档转换**：按第一步多格式支持，将 .doc/.docx 等转为可读文本
2. **提取参考文献列表**，与用户逐一核实确认后开始检验
3. **英文文献**：通过 PubMed E-utilities API（`esearch.fcgi` + `esummary.fcgi`）验证
4. **中文文献**：通过 WebSearch 多源交叉验证（CNKI/万方/百度学术/期刊官网）
5. **判定标准从"断言准确性"调整为"文献存在性+信息一致性"**
6. **局限性**：中文文献 WebSearch 的覆盖面不及 PubMed API，负面结果需注明"基于公开网页搜索，可能漏检付费墙内文献"
