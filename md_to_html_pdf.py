#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 转换为 HTML，然后使用浏览器转换为 PDF
"""

import markdown2
import os
import subprocess

def markdown_to_html(md_file, html_file):
    """将Markdown转换为HTML"""
    
    print("📖 正在读取Markdown文件...")
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print("🔄 正在转换Markdown为HTML...")
    html_content = markdown2.markdown(
        md_content,
        extras=[
            'fenced-code-blocks',
            'code-friendly',
            'tables',
            'strike',
            'task_list',
            'header-ids'
        ]
    )
    
    # 创建完整的HTML文档
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Claude Code 实战课程</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}

            @media print {{
                body {{
                    font-size: 11pt;
                }}
                
                h1 {{
                    page-break-after: avoid;
                }}
                
                h2, h3, h4 {{
                    page-break-after: avoid;
                }}
                
                pre, blockquote {{
                    page-break-inside: avoid;
                }}
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;
                font-size: 11pt;
                line-height: 1.8;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 20px;
                background-color: #fff;
            }}

            h1 {{
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 50px;
                margin-bottom: 25px;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
            }}

            h2 {{
                font-size: 24px;
                font-weight: bold;
                color: #34495e;
                margin-top: 40px;
                margin-bottom: 20px;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 10px;
            }}

            h3 {{
                font-size: 20px;
                font-weight: bold;
                color: #555;
                margin-top: 30px;
                margin-bottom: 15px;
            }}

            h4 {{
                font-size: 16px;
                font-weight: bold;
                color: #666;
                margin-top: 25px;
                margin-bottom: 12px;
            }}

            p {{
                margin-bottom: 12px;
                text-align: justify;
                line-height: 1.8;
            }}

            blockquote {{
                margin: 20px 0;
                padding: 15px 25px;
                background-color: #f8f9fa;
                border-left: 5px solid #3498db;
                color: #555;
                font-style: italic;
            }}

            code {{
                font-family: "Monaco", "Menlo", "Consolas", "Courier New", monospace;
                background-color: #f4f4f4;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 0.9em;
                color: #e74c3c;
            }}

            pre {{
                background-color: #2d2d2d;
                color: #f8f8f2;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                margin: 20px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}

            pre code {{
                background-color: transparent;
                padding: 0;
                color: #f8f8f2;
                font-size: 0.9em;
            }}

            ul, ol {{
                margin: 12px 0;
                padding-left: 40px;
            }}

            li {{
                margin-bottom: 8px;
                line-height: 1.6;
            }}

            a {{
                color: #3498db;
                text-decoration: none;
                border-bottom: 1px dotted #3498db;
                transition: all 0.2s ease;
            }}

            a:hover {{
                color: #2980b9;
                border-bottom-style: solid;
            }}

            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 25px auto;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}

            hr {{
                border: none;
                border-top: 2px solid #ecf0f1;
                margin: 40px 0;
            }}

            strong {{
                color: #2c3e50;
                font-weight: 600;
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
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
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

            tr:hover {{
                background-color: #e9ecef;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    print(f"💾 正在保存HTML文件...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ HTML文件已生成: {html_file}")
    return html_file

def html_to_pdf_cups(html_file, pdf_file):
    """使用macOS的命令行工具转换为PDF"""
    
    print("🖨️  正在使用浏览器转换HTML为PDF...")
    
    # 使用AppleScript打开Safari并打印为PDF
    applescript = f'''
    tell application "Safari"
        activate
        open POSIX file "{html_file}"
        delay 3
        tell application "System Events"
            keystroke "p" using command down
            delay 2
        end tell
    end tell
    '''
    
    # 这个方案比较复杂，改用更简单的方案
    print("⚠️  浏览器自动化方案需要用户手动操作")
    print("📋 请在浏览器中打开以下HTML文件，然后使用浏览器的打印功能保存为PDF：")
    print(f"   file://{html_file}")
    print(f"\n💡 提示：在打印对话框中选择'保存为PDF'即可")
    
    return False

def main():
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.md"
    html_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.html"
    pdf_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code实战课程_完整版.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ 错误: 找不到Markdown文件: {md_file}")
        return
    
    # 转换为HTML
    html_to_html = markdown_to_html(md_file, html_file)
    
    print("\n🎉 HTML转换完成！")
    print(f"📁 HTML文件位置: {html_file}")
    print(f"\n📋 接下来的步骤：")
    print(f"   1. 在浏览器中打开: file://{html_file}")
    print(f"   2. 按 Cmd+P 打开打印对话框")
    print(f"   3. 选择'保存为PDF'或'Microsoft Print to PDF'")
    print(f"   4. 点击保存，位置: {pdf_file}")

if __name__ == "__main__":
    main()
