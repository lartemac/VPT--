#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 文档转换为 PDF
使用 WeasyPrint 库，支持中文和复杂格式
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def markdown_to_pdf(md_file, pdf_file):
    """将Markdown文件转换为PDF"""

    # 读取Markdown文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 转换Markdown到HTML
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'extra',           # 额外功能
            'codehilite',      # 代码高亮
            'tables',          # 表格支持
            'toc',             # 目录生成
            'nl2br',           # 换行转换
            'sane_lists',      # 列表处理
        ]
    )

    # 添加完整的HTML结构和CSS样式
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>Claude Code 实战课程</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-center {{
                    content: "第 " counter(page) " 页";
                    font-size: 10pt;
                    color: #666;
                }}
            }}

            body {{
                font-family: "PingFang SC", "STHeiti", "Microsoft YaHei", sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 0;
            }}

            h1 {{
                font-size: 24pt;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 30pt;
                margin-bottom: 15pt;
                page-break-after: avoid;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10pt;
            }}

            h2 {{
                font-size: 18pt;
                font-weight: bold;
                color: #34495e;
                margin-top: 20pt;
                margin-bottom: 10pt;
                page-break-after: avoid;
            }}

            h3 {{
                font-size: 14pt;
                font-weight: bold;
                color: #555;
                margin-top: 15pt;
                margin-bottom: 8pt;
                page-break-after: avoid;
            }}

            h4 {{
                font-size: 12pt;
                font-weight: bold;
                color: #666;
                margin-top: 12pt;
                margin-bottom: 6pt;
                page-break-after: avoid;
            }}

            p {{
                margin-bottom: 10pt;
                text-align: justify;
            }}

            blockquote {{
                margin: 15pt 0;
                padding: 10pt 15pt;
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                font-style: italic;
            }}

            code {{
                font-family: "Menlo", "Monaco", "Consolas", "Courier New", monospace;
                background-color: #f4f4f4;
                padding: 2pt 4pt;
                border-radius: 3px;
                font-size: 10pt;
            }}

            pre {{
                background-color: #2d2d2d;
                color: #f8f8f2;
                padding: 15pt;
                border-radius: 5px;
                overflow-x: auto;
                margin: 15pt 0;
                page-break-inside: avoid;
            }}

            pre code {{
                background-color: transparent;
                padding: 0;
                color: inherit;
            }}

            ul, ol {{
                margin: 10pt 0;
                padding-left: 30pt;
            }}

            li {{
                margin-bottom: 5pt;
            }}

            a {{
                color: #3498db;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15pt 0;
                font-size: 10pt;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 8pt;
                text-align: left;
            }}

            th {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }}

            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}

            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 15pt auto;
            }}

            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 20pt 0;
            }}

            /* 目录样式 */
            .toc {{
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                padding: 15pt;
                margin: 20pt 0;
                border-radius: 5px;
            }}

            .toc ul {{
                list-style-type: none;
                padding-left: 0;
            }}

            .toc li {{
                margin-bottom: 5pt;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # 配置字体
    font_config = FontConfiguration()

    # 生成PDF
    print("📄 正在生成PDF文档...")
    HTML(string=full_html).write_pdf(
        pdf_file,
        font_config=font_config,
        stylesheets=[CSS(string="""
            @font-face {{
                font-family: "PingFang SC";
                src: local("PingFang SC"), local("STHeiti");
            }}
        """, font_config=font_config)]
    )

    print(f"✅ PDF文档已生成: {pdf_file}")

    # 获取文件大小
    file_size = os.path.getsize(pdf_file)
    file_size_mb = file_size / (1024 * 1024)

    print(f"📊 文件大小: {file_size_mb:.2f} MB")

def main():
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.md"
    pdf_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.pdf"

    if not os.path.exists(md_file):
        print(f"❌ 错误: 找不到Markdown文件: {md_file}")
        return

    print(f"📖 读取Markdown文件: {md_file}")
    markdown_to_pdf(md_file, pdf_file)
    print("\n🎉 PDF转换完成！")

if __name__ == "__main__":
    main()
