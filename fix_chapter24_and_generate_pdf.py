#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复第24章并生成PDF文档
根据用户反馈，第27章（27.1-27.6 高级代码生成）实际应该是第24章
需要：
1. 提取第27章内容
2. 将其重新编号为第24章
3. 插入到第23章和第25章之间
4. 重新编号后续章节（原25-34章 -> 26-35章）
5. 生成PDF文档
"""

import re
import os
import sys

def extract_chapter_content(lines, start_line, next_chapter_line=None):
    """提取从start_line开始到下一章之前的所有内容"""
    content = []
    for i in range(start_line - 1, len(lines)):
        if next_chapter_line and i >= next_chapter_line - 1:
            break
        # 检查是否遇到了新的一章（不是我们要的章节）
        if i > start_line - 1:
            line = lines[i]
            if re.match(r'^# 第 [0-9]+ 章', line):
                break
        content.append(lines[i])
    return content

def renumber_chapter(content, old_num, new_num):
    """重新编号章节"""
    content_str = ''.join(content)

    # 替换章标题
    content_str = re.sub(f'# 第 {old_num} 章', f'# 第 {new_num} 章', content_str)

    # 替换内部的小节编号（如 27.1 -> 24.1）
    # 需要小心处理，只替换这一章内部的编号
    def replace_section(match):
        section_num = match.group(2)
        return f"{match.group(1)}{new_num}.{section_num}"

    # 替换类似 27.1 的格式（使用字符串替换避免正则表达式引用问题）
    pattern = f"{old_num}."
    replacement = f"{new_num}."
    # 只替换这一章内部的编号
    lines = content_str.split('\n')
    result_lines = []
    for line in lines:
        # 查找所有包含 old_num. 的情况并替换
        new_line = line.replace(pattern, replacement)
        result_lines.append(new_line)
    content_str = '\n'.join(result_lines)

    return content_str.split('\n')

def main():
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版.md"

    print("=" * 80)
    print("步骤1: 读取原文件")
    print("=" * 80)

    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"文件总行数: {len(lines)}")

    # 章节位置
    ch23_line = 104463
    ch25_line = 106495
    ch27_line = 122306
    ch28_line = 138493

    print(f"\n第23章位置: 第{ch23_line}行")
    print(f"第25章位置: 第{ch25_line}行")
    print(f"第27章位置: 第{ch27_line}行")
    print(f"第28章位置: 第{ch28_line}行")

    print("\n" + "=" * 80)
    print("步骤2: 提取第27章内容（将重新编号为第24章）")
    print("=" * 80)

    # 提取第27章内容
    ch27_content = extract_chapter_content(lines, ch27_line, ch28_line)
    print(f"第27章内容行数: {len(ch27_content)}")

    # 查看第27章标题
    for i, line in enumerate(ch27_content[:20]):
        if '第 27 章' in line or '高级代码生成' in line:
            print(f"  {i}: {line.rstrip()}")

    print("\n" + "=" * 80)
    print("步骤3: 重新编号第27章为第24章")
    print("=" * 80)

    # 重新编号为第24章
    ch24_content = renumber_chapter(ch27_content, 27, 24)
    print(f"重新编号后行数: {len(ch24_content)}")

    # 查看重新编号后的标题
    for i, line in enumerate(ch24_content[:20]):
        if '第' in line and '章' in line:
            print(f"  {i}: {line.rstrip()}")

    print("\n" + "=" * 80)
    print("步骤4: 提取其他章节并重新编号")
    print("=" * 80)

    # 提取第25章（将变为第26章）
    print("\n提取第25章...")
    ch25_content = extract_chapter_content(lines, ch25_line, ch27_line)
    print(f"  第25章行数: {len(ch25_content)}")

    # 提取第26章（将变为第27章）
    ch26_line = None
    for i in range(ch25_line, len(lines)):
        if lines[i].startswith('# 第 26 章'):
            ch26_line = i + 1
            break

    if ch26_line:
        print(f"  第26章位置: 第{ch26_line}行")
        ch26_content = extract_chapter_content(lines, ch26_line, ch27_line)
        print(f"  第26章行数: {len(ch26_content)}")
    else:
        print("  未找到第26章")
        ch26_content = []

    # 提取第28章及后续章节
    print("\n提取第28章及后续章节...")
    remaining_chapters = []
    current_line = ch28_line

    # 先找出所有后续章节的位置
    chapter_positions = []
    for i in range(ch28_line - 1, len(lines)):
        if re.match(r'^# 第 [0-9]+ 章', lines[i]):
            match = re.search(r'# 第 ([0-9]+) 章', lines[i])
            if match:
                chapter_num = int(match.group(1))
                chapter_positions.append((chapter_num, i + 1))

    print(f"找到后续章节: {[ch[0] for ch in chapter_positions]}")

    # 提取并重新编号
    renumbered_content = []
    for i, (old_num, line_num) in enumerate(chapter_positions):
        # 找下一章的位置
        next_line = None
        if i < len(chapter_positions) - 1:
            next_line = chapter_positions[i + 1][1]

        content = extract_chapter_content(lines, line_num, next_line)
        new_num = old_num + 1  # 章节号加1（因为插入了第24章）
        renumbered = renumber_chapter(content, old_num, new_num)
        renumbered_content.extend(renumbered)
        print(f"  第{old_num}章 -> 第{new_num}章 ({len(content)}行)")

    print("\n" + "=" * 80)
    print("步骤5: 组装新的文档")
    print("=" * 80)

    # 组装新文档
    # 1. 第1-23章（保持不变）
    new_lines = lines[:ch25_line - 1]

    # 2. 新的第24章（原第27章）
    new_lines.extend(ch24_content)
    new_lines.append('\n')

    # 3. 第26章（原第25章）
    ch26_renumbered = renumber_chapter(ch25_content, 25, 26)
    new_lines.extend(ch26_renumbered)
    new_lines.append('\n')

    # 4. 第27章（原第26章）
    if ch26_content:
        ch27_renumbered = renumber_chapter(ch26_content, 26, 27)
        new_lines.extend(ch27_renumbered)
        new_lines.append('\n')

    # 5. 第29章及后续章节（原第28章及后续）
    new_lines.extend(renumbered_content)

    print(f"新文档总行数: {len(new_lines)}")
    print(f"原文档总行数: {len(lines)}")
    print(f"增加行数: {len(new_lines) - len(lines)}")

    # 保存修复后的文档
    output_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版_已修复第24章.md"

    print("\n" + "=" * 80)
    print("步骤6: 保存修复后的文档")
    print("=" * 80)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✓ 已保存到: {output_file}")

    # 验证新文档
    print("\n" + "=" * 80)
    print("步骤7: 验证新文档")
    print("=" * 80)

    new_content = ''.join(new_lines)
    chapters = re.findall(r'^# 第 ([0-9]+) 章', new_content, re.MULTILINE)
    chapter_nums = sorted([int(ch) for ch in chapters])

    print(f"新文档包含的章节: {chapter_nums}")

    # 检查是否有第24章
    if 24 in chapter_nums:
        print("✓ 第24章已成功添加")
    else:
        print("✗ 警告: 第24章未找到")

    # 检查章节是否连续
    is_continuous = all(chapter_nums[i] == chapter_nums[i-1] + 1
                       for i in range(1, len(chapter_nums)))
    if is_continuous:
        print("✓ 章节编号连续")
    else:
        print("✗ 警告: 章节编号不连续")

    print("\n" + "=" * 80)
    print("完成！")
    print("=" * 80)

    return output_file

if __name__ == '__main__':
    output_file = main()
    print(f"\n修复后的文档已保存到:\n{output_file}")
