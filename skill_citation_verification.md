---
name: 引用真实性检验 Skill
description: 中文学术论文引用文献真实性检验标准工作流：PDF解析→断言提取→PubMed验证→HTML报告，已验证62条断言
type: project
---

## 引用真实性检验 Skill（2026-05-05 创建）

### 工作流概览
1. **PDF解析**：opendataloader-pdf（需JDK17）→ 干净Markdown
2. **断言提取**：Python正则提取正文+表格中带[n]角标的句子 → JSON
3. **并行验证**：4个后台Agent同时通过PubMed API验证不同批次
4. **报告生成**：汇总为HTML报告保存到桌面

### Skill文件位置
- `~/.claude/commands/verify-citations.md`
- 调用方式：`/verify-citations [PDF路径]`

### 验证标准
- ✅准确：断言与摘要结论完全一致
- ⚠️部分准确：方向正确但细节有偏差
- ❌不准确：事实性错误
- ❓无法验证：中文文献/信息不完整

### 关键技术要点
- PubMed API间隔≥0.5秒防429限流
- Python脚本必须设UTF-8编码
- 中文文献PubMed未收录，标❓
- 验证基于摘要，需注明全文限制

### 已验证项目
- 江千舟等《恒牙不可复性牙髓炎的保髓之路》（2026）
  - 62条断言，84篇参考文献
  - 准确21(33.9%)，部分准确29(46.8%)，不准确2(3.2%)，无法验证10(16.1%)
  - 关键错误：断言38 CaSR→TRPA1，断言47 PI3K/Akt→MAPK

## Why: 用户作为科研人员经常需要检验论文引用真实性，需可复用的标准流程
## How to apply: 当用户提供PDF论文要求检验引用时，使用 /verify-citations 命令启动
