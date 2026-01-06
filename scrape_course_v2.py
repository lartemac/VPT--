#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 实战课程内容抓取脚本（改进版）
完整抓取所有章节内容并保存为 Markdown 文档
"""

import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin

# 基础 URL
BASE_URL = "https://cholf5.com/claude-code-in-action/"

# 所有章节列表
CHAPTERS = [
    ("01", "引言", "01-introduction.html"),
    ("02", "什么是编码助手？", "02-what-is-a-coding-assistant.html"),
    ("03", "Claude Code 实战", "03-claude-code-in-action.html"),
    ("04", "Claude Code 安装与配置", "04-claude-code-setup.html"),
    ("05", "项目准备", "05-project-setup.html"),
    ("06", "添加上下文", "06-adding-context.html"),
    ("07", "进行修改", "07-making-changes.html"),
    ("08", "课程满意度调查", "08-course-satisfaction-survey.html"),
    ("09", "控制上下文", "09-controlling-context.html"),
    ("10", "自定义命令", "10-custom-commands.html"),
    ("11", "Claude Code 的 MCP 服务器", "11-mcp-servers-with-claude-code.html"),
    ("12", "GitHub 集成", "12-github-integration.html"),
    ("13", "认识 Hooks", "13-introducing-hooks.html"),
    ("14", "定义 Hooks", "14-defining-hooks.html"),
    ("15", "实现一个 Hook", "15-implementing-a-hook.html"),
    ("16", "Hooks 常见坑点", "16-gotchas-around-hooks.html"),
    ("17", "实用的 Hooks", "17-useful-hooks.html"),
    ("18", "另一个实用 Hook", "18-another-useful-hook.html"),
    ("19", "Claude Code SDK", "19-the-claude-code-sdk.html"),
    ("20", "Claude Code 测验", "20-quiz-on-claude-code.html"),
    ("21", "总结与下一步", "21-summary-and-next-steps.html")
]

def fetch_page(url):
    """获取页面内容"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        print(f"❌ 获取失败: {url} - {str(e)}")
        return None

def html_to_markdown(element, base_url=""):
    """将HTML元素转换为Markdown"""
    if not element:
        return ""

    markdown_lines = []

    # 处理不同的HTML标签
    if element.name == 'h1':
        text = element.get_text().strip()
        markdown_lines.append(f"\n\n# {text}\n\n")
    elif element.name == 'h2':
        text = element.get_text().strip()
        markdown_lines.append(f"\n\n## {text}\n\n")
    elif element.name == 'h3':
        text = element.get_text().strip()
        markdown_lines.append(f"\n\n### {text}\n\n")
    elif element.name == 'h4':
        text = element.get_text().strip()
        markdown_lines.append(f"\n\n#### {text}\n\n")
    elif element.name == 'p':
        text = element.get_text().strip()
        if text:
            markdown_lines.append(f"{text}\n\n")
    elif element.name in ['ul', 'ol']:
        items = element.find_all('li', recursive=False)
        for li in items:
            text = li.get_text().strip()
            # 保留加粗标记
            for strong in li.find_all('strong'):
                text = text.replace(strong.get_text(), f"**{strong.get_text()}**")
            markdown_lines.append(f"- {text}\n")
        markdown_lines.append("\n")
    elif element.name == 'ol':
        items = element.find_all('li', recursive=False)
        for i, li in enumerate(items, 1):
            text = li.get_text().strip()
            # 保留加粗标记
            for strong in li.find_all('strong'):
                text = text.replace(strong.get_text(), f"**{strong.get_text()}**")
            markdown_lines.append(f"{i}. {text}\n")
        markdown_lines.append("\n")
    elif element.name == 'pre':
        code = element.get_text()
        markdown_lines.append(f"\n```\n{code}\n```\n\n")
    elif element.name == 'img':
        src = element.get('src', '')
        alt = element.get('alt', '图片')
        markdown_lines.append(f"\n![{alt}]({src})\n\n")
    elif element.name == 'a':
        href = element.get('href', '')
        text = element.get_text().strip()
        if href and not href.startswith('javascript'):
            markdown_lines.append(f"[{text}]({href})")
    elif element.name == 'strong' or element.name == 'b':
        text = element.get_text().strip()
        markdown_lines.append(f"**{text}**")
    elif element.name == 'code':
        text = element.get_text().strip()
        markdown_lines.append(f"`{text}`")
    elif element.name == 'blockquote':
        text = element.get_text().strip()
        markdown_lines.append(f"\n> {text}\n\n")
    elif element.name == 'div' or element.name == 'section':
        # 递归处理子元素
        for child in element.children:
            if hasattr(child, 'name'):
                markdown_lines.append(html_to_markdown(child, base_url))

    return ''.join(markdown_lines)

def extract_content(html, chapter_num, chapter_title):
    """从 HTML 中提取主要内容"""
    soup = BeautifulSoup(html, 'html.parser')

    # 查找内容区域
    content_body = soup.find('div', class_='content-body')

    if not content_body:
        return None

    # 提取标题
    title_tag = content_body.find('h1')
    title = title_tag.get_text().strip() if title_tag else chapter_title

    # 生成Markdown
    markdown_parts = []
    markdown_parts.append(f"\n\n# {title}\n\n")

    # 处理所有直接子元素
    for element in content_body.find_all(recursive=False):
        if element.name == 'h1':
            continue  # 已经处理过标题
        markdown_parts.append(html_to_markdown(element))

    return ''.join(markdown_parts)

def scrape_all_chapters():
    """抓取所有章节"""
    all_content = []
    failed_chapters = []

    print("🚀 开始抓取 Claude Code 实战课程内容...\n")

    for chapter_num, chapter_title, chapter_file in CHAPTERS:
        url = urljoin(BASE_URL, chapter_file)

        print(f"📖 正在抓取: [{chapter_num}] {chapter_title}")

        html = fetch_page(url)
        if html:
            content = extract_content(html, chapter_num, chapter_title)
            if content:
                all_content.append(content)
                print(f"✅ 成功: [{chapter_num}] {chapter_title}\n")
            else:
                failed_chapters.append((url, "内容提取失败"))
                print(f"⚠️  内容提取失败: [{chapter_num}] {chapter_title}\n")
        else:
            failed_chapters.append((url, "页面获取失败"))
            print(f"❌ 失败: [{chapter_num}] {chapter_title}\n")

        # 避免请求过快
        time.sleep(0.5)

    # 生成完整的 Markdown 文档
    full_markdown = "# Claude Code 实战课程（中文翻译）\n\n"
    full_markdown += "> **课程说明**：本文档由自动化脚本抓取生成\n\n"
    full_markdown += "> **原课程链接**：https://anthropic.skilljar.com/claude-code-in-action/303233\n\n"
    full_markdown += "> **官方网站**：https://cholf5.com/claude-code-in-action/index.html\n\n"
    full_markdown += "---\n\n"
    full_markdown += "## 课程目录\n\n"

    for chapter_num, chapter_title, _ in CHAPTERS:
        full_markdown += f"{chapter_num}. [{chapter_title}](#章节-{chapter_num})\n"

    full_markdown += "\n---\n\n"

    # 添加所有章节内容
    for i, content in enumerate(all_content, 1):
        # 添加章节锚点
        full_markdown += f'<a id="章节-{i}"></a>\n\n'
        full_markdown += content
        full_markdown += "\n\n---\n\n"

    # 保存文件
    output_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

    print(f"\n📄 Markdown 文档已保存: {output_file}")

    # 生成报告
    report = f"""# Claude Code 实战课程抓取报告

## 统计信息
- **总章节数**: {len(CHAPTERS)}
- **成功抓取**: {len(all_content)} 章
- **失败章节**: {len(failed_chapters)} 章
- **成功率**: {len(all_content)/len(CHAPTERS)*100:.1f}%

## 课程大纲
"""

    for chapter_num, chapter_title, chapter_file in CHAPTERS:
        report += f"**{chapter_num}. {chapter_title}**\n"
        report += f"   - 文件: {chapter_file}\n"
        report += f"   - 链接: {urljoin(BASE_URL, chapter_file)}\n\n"

    if failed_chapters:
        report += "\n## 失败章节\n\n"
        for url, reason in failed_chapters:
            report += f"- ❌ {url}\n"
            report += f"  原因: {reason}\n\n"

    report += f"\n## 输出文件\n\n"
    report += f"- **Markdown文档**: `{output_file}`\n\n"
    report += f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"

    report_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/实战课程抓取报告.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📊 抓取报告已保存: {report_file}")

    print(f"\n✨ 抓取完成!")
    print(f"✅ 成功: {len(all_content)} 章")
    if failed_chapters:
        print(f"❌ 失败: {len(failed_chapters)} 章")
    else:
        print(f"🎉 所有章节全部成功抓取！")

if __name__ == "__main__":
    scrape_all_chapters()
