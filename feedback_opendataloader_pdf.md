---
name: PDF转MD必须优先使用opendataloader-pdf
description: 用户明确要求所有PDF转Markdown任务必须优先使用opendataloader-pdf，禁止使用其他效果差的方法
type: feedback
---

## PDF转MD工具使用规则

**必须使用 opendataloader-pdf 作为 PDF 转 Markdown 的首选工具，禁止使用其他方法。**

- 工具：opendataloader-pdf（Benchmark #1，评分 0.907）
- JDK 路径：`D:\Java\jdk-17.0.19+10`
- jar 文件：`D:\opendataloader-pdf\opendataloader-pdf.jar`
- 命令：`java -jar opendataloader-pdf.jar --input PDF路径 --output md路径 --format markdown`
- macOS 对应路径需根据实际安装位置调整

**Why:** 用户经过实际使用验证，opendataloader-pdf 转换质量远超其他方法，在引用真实性检验等任务中表现出色
**How to apply:** 任何需要将 PDF 转为 Markdown 的场景（论文解析、文献提取、文档处理等），第一步就是启动 opendataloader-pdf，不要考虑 PyMuPDF、pdfplumber、marker 等替代方案
