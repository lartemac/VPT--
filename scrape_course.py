#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 实战课程内容抓取脚本
批量抓取所有章节内容并保存为 Markdown 文档
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import urljoin

# 基础 URL
BASE_URL = "https://cholf5.com/claude-code-in-action/"

# 所有章节列表
CHAPTERS = [
    "01-introduction.html",
    "02-what-is-a-coding-assistant.html",
    "03-claude-code-in-action.html",
    "04-claude-code-setup.html",
    "05-project-setup.html",
    "06-adding-context.html",
    "07-making-changes.html",
    "08-course-satisfaction-survey.html",
    "09-controlling-context.html",
    "10-custom-commands.html",
    "11-mcp-servers-with-claude-code.html",
    "12-github-integration.html",
    "13-introducing-hooks.html",
    "14-defining-hooks.html",
    "15-implementing-a-hook.html",
    "16-gotchas-around-hooks.html",
    "17-useful-hooks.html",
    "18-another-useful-hook.html",
    "19-the-claude-code-sdk.html",
    "20-quiz-on-claude-code.html",
    "21-summary-and-next-steps.html"
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

def extract_content(html, chapter_title):
    """从 HTML 中提取主要内容"""
    soup = BeautifulSoup(html, 'html.parser')

    # 移除导航栏等不需要的内容
    for nav in soup.find_all('nav'):
        nav.decompose()
    for header in soup.find_all(['header', 'footer']):
        header.decompose()

    # 查找主要内容区域
    content = soup.find('main') or soup.find('article') or soup.find('body')

    if not content:
        return None

    # 提取标题
    title_tag = content.find(['h1', 'h2'])
    title = title_tag.get_text().strip() if title_tag else chapter_title

    # 转换为 Markdown
    markdown_parts = []
    markdown_parts.append(f"\n\n# {title}\n\n")

    # 处理所有子元素
    for element in content.find_all(recursive=False):
        # 跳过标题（已经处理过）
        if element.name in ['h1', 'h2']:
            continue

        # 处理不同的 HTML 标签
        if element.name == 'h3':
            markdown_parts.append(f"\n## {element.get_text().strip()}\n")
        elif element.name == 'h4':
            markdown_parts.append(f"\n### {element.get_text().strip()}\n")
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                markdown_parts.append(f"{text}\n\n")
        elif element.name == 'ul' or element.name == 'ol':
            items = element.find_all('li', recursive=False)
            for li in items:
                markdown_parts.append(f"- {li.get_text().strip()}\n")
            markdown_parts.append("\n")
        elif element.name == 'pre':
            code = element.get_text()
            markdown_parts.append(f"\n```\n{code}\n```\n\n")
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', '图片')
            markdown_parts.append(f"![{alt}]({src})\n\n")
        elif element.name == 'a':
            href = element.get('href', '')
            text = element.get_text().strip()
            markdown_parts.append(f"[{text}]({href})")

    return ''.join(markdown_parts)

def scrape_all_chapters():
    """抓取所有章节"""
    all_content = []
    failed_chapters = []

    print("🚀 开始抓取 Claude Code 实战课程内容...\n")

    for i, chapter_file in enumerate(CHAPTERS, 1):
        url = urljoin(BASE_URL, chapter_file)
        chapter_title = f"第 {i:02d} 节: {chapter_file.replace('.html', '')}"

        print(f"📖 正在抓取 [{i}/{len(CHAPTERS)}]: {chapter_title}")

        html = fetch_page(url)
        if html:
            content = extract_content(html, chapter_title)
            if content:
                all_content.append(content)
                print(f"✅ 成功: {chapter_title}\n")
            else:
                failed_chapters.append((url, "内容提取失败"))
                print(f"⚠️  内容提取失败: {chapter_title}\n")
        else:
            failed_chapters.append((url, "页面获取失败"))
            print(f"❌ 失败: {chapter_title}\n")

        # 避免请求过快
        time.sleep(0.5)

    # 生成完整的 Markdown 文档
    full_markdown = "# Claude Code 实战课程（中文翻译）\n\n"
    full_markdown += "> 本文档由自动化脚本抓取生成\n"
    full_markdown += "> 原课程链接: https://anthropic.skilljar.com/claude-code-in-action/303233\n\n"
    full_markdown += "---\n\n"

    full_markdown += ''.join(all_content)

    # 保存文件
    output_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

    print(f"\n📄 Markdown 文档已保存: {output_file}")

    # 生成报告
    report = f"""# Claude Code 实战课程抓取报告

## 统计信息
- 总章节数: {len(CHAPTERS)}
- 成功抓取: {len(all_content)}
- 失败章节: {len(failed_chapters)}
- 成功率: {len(all_content)/len(CHAPTERS)*100:.1f}%

## 章节列表
"""

    for i, chapter in enumerate(CHAPTERS, 1):
        report += f"{i}. {chapter}\n"

    if failed_chapters:
        report += "\n## 失败章节\n"
        for url, reason in failed_chapters:
            report += f"- ❌ {url} - {reason}\n"

    report += f"\n## 输出文件\n- Markdown: {output_file}\n\n生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    report_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/实战课程抓取报告.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📊 抓取报告已保存: {report_file}")

    print(f"\n✨ 抓取完成!")
    print(f"✅ 成功: {len(all_content)} 章")
    if failed_chapters:
        print(f"❌ 失败: {len(failed_chapters)} 章")

if __name__ == "__main__":
    scrape_all_chapters()
