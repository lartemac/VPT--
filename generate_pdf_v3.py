#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 文档转换为 PDF（使用 markdown2 + weasyprint 的简化版本）
"""

import markdown2
from weasyprint import HTML, CSS
import os
import re

def markdown_to_pdf_simple(md_file, pdf_file):
    """将Markdown文件转换为PDF - 简化版"""
    
    print("📖 正在读取Markdown文件...")
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print("🔄 正在转换Markdown为HTML...")
    # 使用markdown2转换
    html_content = markdown2.markdown(
        md_content,
        extras=[
            'fenced-code-blocks',
            'code-friendly',
            'tables',
            'strike',
            'task_list'
        ]
    )
    
    print("📄 正在生成PDF...")
    # 创建完整的HTML文档
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
                    content: counter(page);
                    font-size: 10pt;
                    color: #999;
                }}
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
                font-size: 11pt;
                line-height: 1.8;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 20px;
            }}

            h1 {{
                font-size: 26px;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 40px;
                margin-bottom: 20px;
                page-break-after: avoid;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}

            h2 {{
                font-size: 20px;
                font-weight: bold;
                color: #34495e;
                margin-top: 30px;
                margin-bottom: 15px;
                page-break-after: avoid;
            }}

            h3 {{
                font-size: 16px;
                font-weight: bold;
                color: #555;
                margin-top: 25px;
                margin-bottom: 12px;
                page-break-after: avoid;
            }}

            h4 {{
                font-size: 14px;
                font-weight: bold;
                color: #666;
                margin-top: 20px;
                margin-bottom: 10px;
                page-break-after: avoid;
            }}

            p {{
                margin-bottom: 12px;
                text-align: justify;
                line-height: 1.8;
            }}

            blockquote {{
                margin: 15px 0;
                padding: 12px 20px;
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                color: #555;
            }}

            code {{
                font-family: "Monaco", "Menlo", "Consolas", "Courier New", monospace;
                background-color: #f4f4f4;
                padding: 3px 6px;
                border-radius: 3px;
                font-size: 0.9em;
                color: #e74c3c;
            }}

            pre {{
                background-color: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                margin: 15px 0;
                page-break-inside: avoid;
            }}

            pre code {{
                background-color: transparent;
                padding: 0;
                color: #f8f8f2;
            }}

            ul, ol {{
                margin: 12px 0;
                padding-left: 35px;
            }}

            li {{
                margin-bottom: 8px;
                line-height: 1.6;
            }}

            a {{
                color: #3498db;
                text-decoration: none;
                border-bottom: 1px dotted #3498db;
            }}

            a:hover {{
                color: #2980b9;
                border-bottom-style: solid;
            }}

            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
                border-radius: 5px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}

            hr {{
                border: none;
                border-top: 2px solid #ecf0f1;
                margin: 30px 0;
            }}

            strong {{
                color: #2c3e50;
                font-weight: bold;
            }}

            em {{
                font-style: italic;
                color: #555;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                font-size: 10pt;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
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
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    try:
        # 尝试使用weasyprint生成PDF
        HTML(string=full_html, base_url=os.path.dirname(md_file)).write_pdf(pdf_file)
        print(f"✅ PDF文档已生成: {pdf_file}")
        
        # 获取文件大小
        file_size = os.path.getsize(pdf_file)
        file_size_mb = file_size / (1024 * 1024)
        print(f"📊 文件大小: {file_size_mb:.2f} MB")
        
        return True
    except Exception as e:
        print(f"❌ PDF生成失败: {str(e)}")
        return False

def main():
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.md"
    pdf_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ 错误: 找不到Markdown文件: {md_file}")
        return
    
    print("🚀 开始PDF转换...")
    success = markdown_to_pdf_simple(md_file, pdf_file)
    
    if success:
        print("\n🎉 PDF转换完成！")
        print(f"📁 文件位置: {pdf_file}")
    else:
        print("\n❌ PDF转换失败，请查看错误信息")

if __name__ == "__main__":
    main()
