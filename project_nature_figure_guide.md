---
name: project_nature_figure_guide
description: Nature Research Figure Guide 6章完整中文翻译项目（2026-06-05），HTML+打印优化PDF双格式
metadata:
  type: project
  date: 2026-06-05
---

# Nature 图表指南完整翻译项目

## 项目概述

翻译了 Nature 官方 Research Figure Guide（https://research-figure-guide.nature.com/figures/）的全部 6 个章节，生成 HTML 完整中文版和打印优化 PDF。

## 输出文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `Nature_Figure_Guide_完整中文版.html` | 桌面 | 完整翻译版 HTML，含打印优化 CSS |
| `Nature_Figure_Guide_完整中文版.pdf` | 桌面 | Chrome headless 生成，约 9.7 MB |
| `Nature_Science_Cell_Figure_Guidelines_zh.html` | 桌面 | ConceptViz 文章翻译（补充参考） |

## 包含内容

### 第1章：Figures 概述
- 欢迎页 + 5 个子章节导航

### 第2章：准备图表 — 规范
- Graphs 规范：轴线、刻度、色盲配色、无图案填充、无彩色文本（6 组 Avoid/Recommended 对比图）
- Images 规范：RGB 色彩空间、≥300 dpi、比例尺独立图层（3 组对比图）
- Text 规范：Arial/Helvetica、5-7pt、8pt 粗体 panel 标签、禁止文字转轮廓
- Python/Matlab/Prism 用户特定解决方案
- 导出要求：矢量格式 PDF/EPS、RGB、≥450 dpi

### 第3章：构建和导出图表面板
- 尺寸：单栏 89mm / 双栏 183mm / 最大高度 170mm
- 面板排列：字母顺序、减少空白
- 无障碍色板：8 色含 Hex/RGB/CMYK + 色盲模拟
- 主图格式：首选 .ai/.eps/.pdf，不接受 JPEG/TIFF/PNG，限 50MB
- Extended Data 格式：JPEG 首选，300dpi，≤10MB

### 第4章：图像完整性
- Photoshop 十大禁用工具清单
- **禁止生成式 AI**（含内容感知编辑）
- 凝胶/Western Blot 完整规范
- 4 组对比图（原始凝胶、拼接、对比度）

### 第5章：Extended Data 格式指南
- 尺寸 180mm×170mm，线宽 0.25-1pt
- 表格格式、文件格式 JPEG/TIFF/EPS ≤10MB
- 3 个正确格式示例

### 第6章：拖延论文的十大方式
- 尺寸超限/图层合并/文字太小/文字损坏/无障碍缺失/模糊/面板缺失/Western Blot问题/化学结构/格式错误

## 技术细节

### 打印 PDF 生成
- 使用 Chrome headless `--print-to-pdf` 命令
- HTML 中嵌入了 `@media print` CSS：
  - 每章 `page-break-before: always`
  - 图表/表格/代码块 `page-break-inside: avoid`
  - 对比卡改为纵向堆叠
  - 自动页码（封面除外）
- 页面设置：A4、18mm/15mm 页边距

### Chrome headless 命令
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu --print-to-pdf="output.pdf" --no-pdf-header-footer "file:///html-path"
```

## 相关记忆
- [[feedback_literature_table]] — 文献综述表格填写工作流
- [[project_vpt_literature_review]] — VPT 文献综述项目，可应用此图表指南
- [[project_gcf_literature_review]] — GCF 龈沟液文献综述

**Why:** 用户在准备向 Nature 系列期刊投稿时需要遵循官方图表规范，翻译后方便随时查阅。

**How to apply:** 桌面 HTML/PDF 文件可直接打开；图表制作时按规范逐条检查；化学结构参考 Nature 官方 PDF 样式指南。
