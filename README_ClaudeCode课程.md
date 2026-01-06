# Claude Code 实战课程 - 完整版

## 项目简介

本项目是对 Anthropic 官方课程 "Claude Code in Action" 的完整中文翻译版本，包含所有21个章节的文字讲义内容。

## 课程信息

- **原课程名称**: Claude Code in Action
- **原课程链接**: https://anthropic.skilljar.com/claude-code-in-action/303233
- **中文翻译网站**: https://cholf5.com/claude-code-in-action/index.html
- **抓取日期**: 2026-01-06
- **总章节数**: 21章

## 文件说明

### 主要文件

1. **Claude_Code实战课程_完整版.md** (36 KB, 1,369行, 2,525词)
   - Markdown格式的完整课程内容
   - 包含所有21个章节的文字讲义
   - 保留了原有格式和结构
   - 支持代码高亮和图片链接

2. **Claude_Code实战课程_完整版.html** (已在浏览器中打开)
   - HTML格式的完整课程内容
   - 优化的网页样式
   - 可以直接在浏览器中查看
   - 可以通过浏览器打印为PDF

3. **Claude_Code实战课程_完整版.pdf** (待生成)
   - PDF格式的完整课程文档
   - 适合打印和离线阅读
   - 请参考下面的生成方法

4. **实战课程抓取报告.md**
   - 详细的抓取统计信息
   - 课程大纲和章节链接
   - 抓取成功率报告

## 课程大纲

### 基础部分 (01-05)
- 01. 引言
- 02. 什么是编码助手？
- 03. Claude Code 实战
- 04. Claude Code 安装与配置
- 05. 项目准备

### 进阶部分 (06-12)
- 06. 添加上下文
- 07. 进行修改
- 08. 课程满意度调查
- 09. 控制上下文
- 10. 自定义命令
- 11. Claude Code 的 MCP 服务器
- 12. GitHub 集成

### 高级部分 (13-21)
- 13. 认识 Hooks
- 14. 定义 Hooks
- 15. 实现一个 Hook
- 16. Hooks 常见坑点
- 17. 实用的 Hooks
- 18. 另一个实用 Hook
- 19. Claude Code SDK
- 20. Claude Code 测验
- 21. 总结与下一步

## PDF生成指南

### 方案1: 使用浏览器打印（推荐，最简单）

**步骤：**
1. 双击打开 `Claude_Code实战课程_完整版.html` 文件
2. 在浏览器中按 `Cmd + P` (Mac) 或 `Ctrl + P` (Windows) 打开打印对话框
3. 在打印对话框中：
   - 目标打印机选择: "保存为PDF" 或 "Microsoft Print to PDF"
   - 可以调整页面设置（边距、页眉页脚等）
   - 点击"打印"或"保存"
4. 选择保存位置：默认为 `/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.pdf`

**优点：**
- 无需安装任何软件
- 生成的PDF质量高
- 可以自定义打印设置
- 支持所有格式（图片、代码块、表格等）

### 方案2: 在线转换工具

**推荐网站：**
- https://www.markdowntopdf.com/
- https://cloudconvert.com/md-to-pdf
- https://www.ilovepdf.com/

**步骤：**
1. 访问上述网站
2. 上传 `Claude_Code实战课程_完整版.md` 文件
3. 等待转换完成
4. 下载生成的PDF文件

**注意：** 
- 部分网站可能有文件大小限制
- 建议选择支持中文的转换工具
- 某些工具可能无法正确处理复杂的Markdown格式

### 方案3: 使用专业工具（适合技术人员）

#### a) 安装 Homebrew（如果未安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### b) 安装 pandoc 和 LaTeX

```bash
# 安装 pandoc
brew install pandoc

# 安装 BasicTeX（用于PDF支持）
brew install --cask basictex
```

#### c) 使用 pandoc 生成PDF

```bash
pandoc "Claude_Code实战课程_完整版.md" \
  -o "Claude_Code实战课程_完整版.pdf" \
  --pdf-engine=xelatex \
  -V CJKmainfont='PingFang SC' \
  -V geometry:margin=2cm \
  --toc \
  --number-sections
```

**参数说明：**
- `-o`: 输出文件名
- `--pdf-engine=xelatex`: 使用XeLaTeX引擎（支持中文）
- `-V CJKmainfont`: 设置中文字体
- `-V geometry:margin`: 设置页边距
- `--toc`: 生成目录
- `--number-sections`: 章节编号

## 抓取脚本

项目中包含以下Python脚本：

1. **scrape_course_v2.py** - 课程内容抓取脚本
   - 自动抓取所有章节内容
   - 转换为Markdown格式
   - 生成完整文档

2. **md_to_html_pdf.py** - Markdown转HTML脚本
   - 将Markdown转换为HTML
   - 添加优化的CSS样式
   - 生成网页版本

3. **generate_pdf_guide.sh** - PDF生成指南脚本
   - 显示所有PDF生成方案
   - 自动打开HTML文件
   - 提供详细的操作说明

## 使用建议

### 阅读方式选择

1. **在线浏览**：打开HTML文件，在浏览器中查看
2. **Markdown编辑器**：使用Typora、VS Code等编辑器打开.md文件
3. **PDF阅读**：按照上述方法生成PDF后使用PDF阅读器

### 学习建议

1. 按照课程顺序学习，从基础到高级
2. 结合原课程的视频内容（需要访问原课程网站）
3. 实践每个章节的内容，跟随课程操作
4. 遇到问题时可以参考原课程链接

## 技术细节

### 依赖库

- Python 3.x
- requests - HTTP请求
- beautifulsoup4 - HTML解析
- markdown2 - Markdown转换

### 安装依赖

```bash
pip3 install requests beautifulsoup4 markdown2
```

## 抓取统计

- **总章节数**: 21章
- **成功抓取**: 21章
- **失败章节**: 0章
- **成功率**: 100%

## 文件位置

所有文件位于：`/Users/lartemacfiles/Desktop/VPT-初诊数据/`

## 更新记录

- 2026-01-06: 初始版本，完成所有章节抓取

## 许可说明

本课程内容由 Anthropic 提供，中文翻译由 cholf5.com 提供。本项目仅供个人学习使用，请勿用于商业用途。

## 联系方式

如有问题或建议，请访问原课程网站或中文翻译网站。

---

**祝你学习愉快！🎉**
