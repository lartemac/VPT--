#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并补充第24章内容，然后生成PDF文档
"""

import re
import os
import json
from urllib.parse import quote

# 检查第24章是否缺失
def check_chapter_24():
    """检查markdown文件中是否有第24章"""
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版.md"

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有章节
    chapters = re.findall(r'^# 第 ([0-9]+) 章', content, re.MULTILINE)
    chapter_nums = [int(ch) for ch in chapters]

    print(f"找到的章节: {sorted(chapter_nums)}")

    # 检查是否有第24章
    if 24 in chapter_nums:
        print("✓ 第24章存在")
        return True, None
    else:
        print("✗ 第24章缺失")
        # 检查第23章和第25章的位置
        lines = content.split('\n')
        ch23_pos = None
        ch25_pos = None
        for i, line in enumerate(lines):
            if line.startswith('# 第 23 章'):
                ch23_pos = i
            elif line.startswith('# 第 25 章'):
                ch25_pos = i

        print(f"第23章位置: 第{ch23_pos}行")
        print(f"第25章位置: 第{ch25_pos}行")

        if ch23_pos and ch25_pos:
            gap = ch25_pos - ch23_pos
            print(f"两章之间间隔: {gap}行")
            if gap < 100:
                print("⚠️ 警告: 第23章和第25章之间距离很近，可能第24章确实缺失")

        return False, None

# 使用course_links.json查找第24章
def find_chapter_24_from_json():
    """从course_links.json中查找第24章相关内容"""
    json_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/course_links.json"

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 查找所有包含"24"或"27.1-27.6"的链接
    chapter_24_candidates = []
    chapter_27_candidates = []

    for title, url in data.items():
        if '24.' in title or '第24' in title:
            chapter_24_candidates.append((title, url))
        if '27.1' in title or '27.2' in title or '27.3' in title or '27.4' in title or '27.5' in title or '27.6' in title:
            chapter_27_candidates.append((title, url))

    print("\n=== 可能是第24章的内容（包含24） ===")
    for title, url in chapter_24_candidates[:10]:
        print(f"- {title}")
        print(f"  {url}\n")

    print("=== 可能是第24章的内容（27.1-27.6 高级代码生成） ===")
    for title, url in chapter_27_candidates[:10]:
        print(f"- {title}")
        print(f"  {url}\n")

    return chapter_27_candidates

# 检查markdown中第27章的内容
def check_chapter_27_content():
    """查看第27章的内容，确认是否应该是第24章"""
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版.md"

    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 找到第27章的位置
    ch27_start = None
    for i, line in enumerate(lines):
        if line.startswith('# 第 27 章'):
            ch27_start = i
            break

    if ch27_start:
        # 打印第27章的前2000行
        content = ''.join(lines[ch27_start:ch27_start+2000])
        print("\n=== 第27章内容预览 ===")
        print(content[:3000])
        print("...\n")

        # 检查第27章的小节标题
        sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
        print("第27章包含的小节:")
        for section in sections[:10]:
            print(f"  - {section}")

# 主函数
def main():
    print("=" * 80)
    print("任务1: 检查第24章内容")
    print("=" * 80)

    has_ch24, _ = check_chapter_24()
    ch27_candidates = find_chapter_24_from_json()
    check_chapter_27_content()

    print("\n" + "=" * 80)
    print("分析结论")
    print("=" * 80)

    if not has_ch24:
        print("✗ 确认第24章缺失")
        print("\n根据用户反馈，第24章可能被错误标记为第27章（27.1-27.6）")
        print("第27章标题为'高级代码生成技巧'，这应该是第24章的内容")
        print("\n建议：将第27章（27.1-27.6）重新编号为第24章")
    else:
        print("✓ 第24章存在")

if __name__ == '__main__':
    main()
