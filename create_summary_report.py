#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建教程摘要报告
"""

import json
import re
from pathlib import Path


def create_summary_report():
    """创建详细的摘要报告"""
    print("正在创建摘要报告...")

    # 加载数据
    with open('/Users/lartemacfiles/Desktop/VPT-初诊数据/course_links.json', 'r', encoding='utf-8') as f:
        all_links = json.load(f)

    with open('/Users/lartemacfiles/Desktop/VPT-初诊数据/scraping_progress.json', 'r', encoding='utf-8') as f:
        progress = json.load(f)

    # 按章节组织
    chapters = {}

    for url in progress['completed']:
        # 找到对应的链接信息
        link_info = None
        for link in all_links:
            full_url = f"https://claudecode.tangshuang.net{link['href']}"
            if full_url == url and link['text']:
                link_info = link
                break

        if not link_info:
            continue

        # 提取章节号
        match = re.search(r'(\d+)\.(.+)', link_info['text'])
        if match:
            chapter_num = match.group(1)
            section_title = match.group(2).strip()

            if chapter_num not in chapters:
                chapters[chapter_num] = []

            chapters[chapter_num].append({
                'title': section_title,
                'url': url
            })

    # 章节标题映射
    chapter_titles = {
        '1': 'Claude Code 简介',
        '2': '安装与配置',
        '3': '基础使用指南',
        '4': '命令系统概述',
        '5': '基础命令详解',
        '6': 'CLI 标志说明',
        '7': '斜杠命令指南',
        '8': '文件操作与上下文管理',
        '9': '交互模式',
        '10': '多轮对话与记忆',
        '11': '代码生成进阶',
        '12': '代码理解与分析',
        '13': '测试与调试',
        '14': '版本控制集成',
        '15': '技能(Skills)系统',
        '16': '高级配置',
        '17': '性能优化',
        '18': '安全最佳实践',
        '19': '团队协作',
        '20': '项目管理',
        '21': '插件开发基础',
        '22': '插件开发进阶',
        '23': '自定义AI智能体',
        '25': '智能开发工作流',
        '26': '自动化任务',
        '27': '高级代码生成与理解',
        '28': 'Claude Code 架构解析',
        '29': '扩展与集成',
        '30': '部署架构',
        '31': '监控与日志',
        '32': '安全与合规',
        '33': '企业部署',
        '34': '运维与监控'
    }

    # 生成报告
    report = []
    report.append("# Claude Code 中文教程 - 抓取摘要报告\n")
    report.append(f"**抓取日期**: 2026-01-06\n")
    report.append(f"**数据来源**: https://claudecode.tangshuang.net\n")
    report.append(f"**总章节数**: {len(chapters)} 章\n")
    report.append(f"**总小节数**: {len(progress['completed'])} 节\n")
    report.append(f"**失败数量**: {len(progress['failed'])} 节\n")
    report.append("\n---\n\n")

    report.append("## 章节目录\n\n")

    for chapter_num in sorted(chapters.keys(), key=lambda x: int(x)):
        chapter_title = chapter_titles.get(chapter_num, f'第{chapter_num}章')
        sections = chapters[chapter_num]

        report.append(f"### 第 {chapter_num} 章：{chapter_title}\n\n")
        report.append(f"**小节数**: {len(sections)}\n\n")

        for section in sections:
            report.append(f"- {section['title']}\n")

        report.append("\n")

    # 保存报告
    report_file = Path("/Users/lartemacfiles/Desktop/VPT-初诊数据/教程摘要报告.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(''.join(report))

    print(f"✓ 摘要报告已保存: {report_file}")

    # 同时保存JSON格式的摘要
    summary_json = {
        'total_chapters': len(chapters),
        'total_sections': len(progress['completed']),
        'failed_sections': len(progress['failed']),
        'chapters': {}
    }

    for chapter_num in sorted(chapters.keys(), key=lambda x: int(x)):
        chapter_title = chapter_titles.get(chapter_num, f'第{chapter_num}章')
        summary_json['chapters'][chapter_num] = {
            'title': chapter_title,
            'sections_count': len(chapters[chapter_num]),
            'sections': [s['title'] for s in chapters[chapter_num]]
        }

    summary_file = Path("/Users/lartemacfiles/Desktop/VPT-初诊数据/tutorial_summary_final.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_json, f, ensure_ascii=False, indent=2)

    print(f"✓ JSON摘要已保存: {summary_file}")

    # 打印统计信息
    print("\n统计信息:")
    print(f"  总章节数: {len(chapters)}")
    print(f"  总小节数: {len(progress['completed'])}")
    print(f"  失败数量: {len(progress['failed'])}")

    print("\n章节概览:")
    for chapter_num in sorted(chapters.keys(), key=lambda x: int(x)):
        chapter_title = chapter_titles.get(chapter_num, f'第{chapter_num}章')
        sections_count = len(chapters[chapter_num])
        print(f"  第 {chapter_num:>2} 章：{chapter_title:<30} ({sections_count:>3} 节)")


if __name__ == "__main__":
    print("=" * 70)
    print("创建教程摘要报告")
    print("=" * 70)
    print()

    create_summary_report()

    print("\n" + "=" * 70)
    print("完成！")
    print("=" * 70)
