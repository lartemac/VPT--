#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 文档转换为 PDF（使用 ReportLab）
支持中文和复杂格式
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import re
import os

def register_chinese_fonts():
    """注册中文字体"""
    # macOS 常用中文字体路径
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',  # PingFang SC
        '/System/Library/Fonts/STHeiti Light.ttc',  # STHeiti
        '/System/Library/Fonts/Helvetica.ttc',  # 备用
    ]
    
    registered = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                # 尝试注册字体
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
                registered = True
                print(f"✅ 成功注册字体: {font_path}")
                break
            except:
                continue
    
    if not registered:
        print("⚠️  警告: 无法注册中文字体，使用默认字体")
        return 'Helvetica'
    
    return 'ChineseFont'

def parse_markdown_to_flowables(md_content, font_name):
    """将Markdown内容解析为ReportLab Flowable对象列表"""
    
    flowables = []
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=20,
        textColor=HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        leading=28
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        textColor=HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=15,
        leading=24
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        textColor=HexColor('#555'),
        spaceAfter=8,
        spaceBefore=12,
        leading=20
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        textColor=HexColor('#666'),
        spaceAfter=6,
        spaceBefore=10,
        leading=16
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=6,
        leading=16,
        alignment=TA_LEFT
    )
    
    quote_style = ParagraphStyle(
        'CustomQuote',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=8,
        leading=14,
        leftIndent=20,
        backColor=HexColor('#f8f9fa'),
        borderColor=HexColor('#3498db'),
        borderPadding=10
    )
    
    # 按行处理内容
    lines = md_content.split('\n')
    in_code_block = False
    code_lines = []
    
    for line in lines:
        # 处理代码块
        if line.strip().startswith('```'):
            if in_code_block:
                # 代码块结束
                code_text = '\n'.join(code_lines)
                # 将代码块作为预格式化文本添加
                code_para = Paragraph(
                    f'<font face="Courier" size="8">{code_text}</font>',
                    body_style
                )
                flowables.append(code_para)
                flowables.append(Spacer(1, 0.3*cm))
                code_lines = []
                in_code_block = False
            else:
                # 代码块开始
                in_code_block = True
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # 处理标题
        if line.startswith('# '):
            text = line[2:].strip()
            flowables.append(Paragraph(text, title_style))
            flowables.append(Spacer(1, 0.3*cm))
        elif line.startswith('## '):
            text = line[3:].strip()
            flowables.append(Paragraph(text, heading1_style))
            flowables.append(Spacer(1, 0.2*cm))
        elif line.startswith('### '):
            text = line[4:].strip()
            flowables.append(Paragraph(text, heading2_style))
            flowables.append(Spacer(1, 0.2*cm))
        elif line.startswith('#### '):
            text = line[5:].strip()
            flowables.append(Paragraph(text, heading3_style))
            flowables.append(Spacer(1, 0.2*cm))
        # 处理引用
        elif line.strip().startswith('> '):
            text = line[2:].strip()
            flowables.append(Paragraph(text, quote_style))
            flowables.append(Spacer(1, 0.2*cm))
        # 处理水平线
        elif line.strip() == '---':
            flowables.append(Spacer(1, 0.5*cm))
        # 处理列表项
        elif line.strip().startswith('- ') or re.match(r'^\d+\.', line.strip()):
            text = line.strip()
            # 移除列表标记
            if text.startswith('- '):
                text = '• ' + text[2:]
            flowables.append(Paragraph(text, body_style))
            flowables.append(Spacer(1, 0.1*cm))
        # 处理空行
        elif line.strip() == '':
            flowables.append(Spacer(1, 0.1*cm))
        # 处理普通段落
        elif line.strip():
            # 转换Markdown格式到HTML
            text = line.strip()
            # 加粗
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            # 斜体
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            # 链接
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'<link href="\2">\1</link>', text)
            # 代码
            text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="8">\1</font>', text)
            
            flowables.append(Paragraph(text, body_style))
            flowables.append(Spacer(1, 0.2*cm))
    
    return flowables

def markdown_to_pdf(md_file, pdf_file):
    """将Markdown文件转换为PDF"""
    
    print("📖 正在读取Markdown文件...")
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print("🔤 正在注册中文字体...")
    font_name = register_chinese_fonts()
    
    print("📄 正在解析Markdown内容...")
    # 创建PDF文档
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 解析内容
    flowables = parse_markdown_to_flowables(md_content, font_name)
    
    print("📝 正在生成PDF文档...")
    # 构建PDF
    doc.build(flowables)
    
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
    
    try:
        markdown_to_pdf(md_file, pdf_file)
        print("\n🎉 PDF转换完成！")
    except Exception as e:
        print(f"\n❌ PDF生成失败: {str(e)}")
        print("\n尝试使用备用方案...")

if __name__ == "__main__":
    main()
