#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复第24章 - 完整版本
将原第27章（高级代码生成技巧）重新编号为第24章，并调整所有后续章节
"""

import re

def extract_chapter(lines, start_line, end_line=None):
    """提取章节内容"""
    if end_line:
        return lines[start_line-1:end_line-1]
    else:
        return lines[start_line-1:]

def renumber_chapter_simple(content, old_num, new_num):
    """简单的章节重新编号"""
    result = []
    for line in content:
        # 替换章标题
        line = line.replace(f'# 第 {old_num} 章', f'# 第 {new_num} 章')
        # 替换小节编号 (27. -> 24.)
        line = line.replace(f'{old_num}.', f'{new_num}.')
        result.append(line)
    return result

def main():
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版.md"

    print("读取文件...")
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"总行数: {len(lines)}")

    # 查找所有章节位置
    chapter_info = []
    for i, line in enumerate(lines):
        match = re.match(r'^# 第 ([0-9]+) 章', line)
        if match:
            num = int(match.group(1))
            chapter_info.append((num, i + 1))

    print(f"\n找到的章节: {[ch[0] for ch in chapter_info]}")
    print(f"总章节数: {len(chapter_info)}")

    # 定位关键章节
    chapters_dict = {num: line for num, line in chapter_info}

    # 检查缺失的章节
    all_nums = set(chapters_dict.keys())
    expected_nums = set(range(1, max(all_nums) + 1))
    missing = sorted(expected_nums - all_nums)

    print(f"\n缺失的章节: {missing}")

    if 24 not in missing:
        print("\n第24章已存在，无需修复")
        return

    print("\n需要修复：将第27章移至第24章位置")

    # 找到关键章节位置
    ch23_line = chapters_dict.get(23)
    ch25_line = chapters_dict.get(25)
    ch27_line = chapters_dict.get(27)
    ch28_line = chapters_dict.get(28)

    # 计算每个章节的结束位置
    chapter_ranges = {}
    for i, (num, start) in enumerate(chapter_info):
        if i < len(chapter_info) - 1:
            end = chapter_info[i + 1][1]
        else:
            end = len(lines) + 1
        chapter_ranges[num] = (start, end)

    print("\n章节范围:")
    for num in sorted(chapter_ranges.keys()):
        start, end = chapter_ranges[num]
        print(f"  第{num}章: 第{start}行 - 第{end}行 ({end-start}行)")

    # 提取各章节内容
    print("\n提取章节内容...")

    # 第1-23章（保持不变）
    content_before_ch24 = []
    if 23 in chapter_ranges:
        start, end = chapter_ranges[23]
        content_before_ch24 = extract_chapter(lines, 1, end)
    print(f"  第1-23章: {len(content_before_ch24)}行")

    # 第27章内容（将变成第24章）
    ch24_content = []
    if 27 in chapter_ranges:
        start, end = chapter_ranges[27]
        ch24_content = extract_chapter(lines, start, end)
        ch24_content = renumber_chapter_simple(ch24_content, 27, 24)
    print(f"  新第24章（原第27章）: {len(ch24_content)}行")

    # 第25章内容（将变成第26章）
    ch26_content = []
    if 25 in chapter_ranges:
        start, end = chapter_ranges[25]
        ch26_content = extract_chapter(lines, start, end)
        ch26_content = renumber_chapter_simple(ch26_content, 25, 26)
    print(f"  新第26章（原第25章）: {len(ch26_content)}行")

    # 第26章内容（将变成第27章）
    ch27_new_content = []
    if 26 in chapter_ranges:
        start, end = chapter_ranges[26]
        ch27_new_content = extract_chapter(lines, start, end)
        ch27_new_content = renumber_chapter_simple(ch27_new_content, 26, 27)
    print(f"  新第27章（原第26章）: {len(ch27_new_content)}")

    # 第28章及后续内容（编号都+1）
    remaining_content = []
    for num in sorted(chapter_ranges.keys()):
        if num >= 28:
            start, end = chapter_ranges[num]
            content = extract_chapter(lines, start, end)
            content = renumber_chapter_simple(content, num, num + 1)
            remaining_content.extend(content)
            print(f"  新第{num+1}章（原第{num}章）: {end-start}行")

    # 组装新文档
    print("\n组装新文档...")
    new_lines = []

    # 添加第1-23章
    new_lines.extend(content_before_ch24)

    # 添加新的第24章
    new_lines.extend(ch24_content)
    new_lines.append('\n')

    # 添加新的第26章（原第25章）
    new_lines.extend(ch26_content)
    new_lines.append('\n')

    # 添加新的第27章（原第26章）
    new_lines.extend(ch27_new_content)
    new_lines.append('\n')

    # 添加第29章及后续
    new_lines.extend(remaining_content)

    print(f"新文档总行数: {len(new_lines)}")

    # 验证
    print("\n验证新文档...")
    new_content = ''.join(new_lines)
    chapters = re.findall(r'^# 第 ([0-9]+) 章', new_content, re.MULTILINE)
    chapter_nums = sorted([int(ch) for ch in chapters])

    print(f"新文档章节: {chapter_nums}")

    # 检查连续性
    is_continuous = True
    for i in range(1, len(chapter_nums)):
        if chapter_nums[i] != chapter_nums[i-1] + 1:
            is_continuous = False
            print(f"✗ 不连续: 第{chapter_nums[i-1]}章 -> 第{chapter_nums[i]}章")

    if is_continuous and 24 in chapter_nums:
        print("✓ 第24章已成功添加，章节编号连续")
    else:
        print("✗ 章节编号有问题")

    # 保存
    output_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版_已修复第24章.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✓ 已保存到: {output_file}")

    return output_file

if __name__ == '__main__':
    main()
