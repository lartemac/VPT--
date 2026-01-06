#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确提取第24章并重新组织文档
第27章的前6个小节（27.1-27.6）应该是第24章
"""

import re

def find_section_end(lines, start_line, section_num):
    """找到某个小节的结束位置（下一节开始前）"""
    for i in range(start_line, len(lines)):
        # 查找下一个同级标题（## 数字）
        match = re.match(r'^## (\d+)\s+(.+)', lines[i])
        if match:
            next_num = int(match.group(1))
            if next_num > section_num:
                return i
    return len(lines)

def main():
    md_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版.md"

    print("=" * 80)
    print("精确提取第24章并重新组织文档")
    print("=" * 80)

    print("\n读取文件...")
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"总行数: {len(lines)}")

    # 找到第27章的位置
    ch27_line = None
    for i, line in enumerate(lines):
        if line.strip() == '# 第 27 章':
            ch27_line = i + 1
            break

    if not ch27_line:
        print("✗ 未找到第27章")
        return

    print(f"第27章位置: 第{ch27_line}行")

    # 找到第27章第6节结束的位置
    # 第27章包含6个小节，我们需要找到第6节结束的位置
    # 第6节是"大规模代码库处理"
    print("\n查找第27章第6节的结束位置...")

    section_6_end = None
    found_section_6 = False

    for i in range(ch27_line, len(lines)):
        match = re.match(r'^## (\d+)\s+(.+)', lines[i])
        if match:
            section_num = int(match.group(1))
            section_title = match.group(2).strip()

            if section_num == 6:
                found_section_6 = True
                print(f"  找到第6节: {section_title} (第{i+1}行)")
            elif section_num > 6 and found_section_6:
                section_6_end = i
                print(f"  第6节结束于第{i}行")
                break

    if not section_6_end:
        # 检查是否遇到了新的一章
        for i in range(ch27_line, len(lines)):
            if re.match(r'^# 第 [0-9]+ 章', lines[i]) and i > ch27_line:
                section_6_end = i
                print(f"  找到下一章，第6节结束于第{i}行")
                break

    if not section_6_end:
        print("✗ 无法确定第6节结束位置")
        return

    # 提取第27章的前6节内容（将作为第24章）
    print(f"\n提取第27章第1-6节内容...")
    ch24_raw = lines[ch27_line-1:section_6_end]
    print(f"  提取了{len(ch24_raw)}行")

    # 查看提取内容的开始和结束
    print("\n第24章内容预览:")
    print("开始:")
    for i, line in enumerate(ch24_raw[:10]):
        print(f"  {i+1}: {line.rstrip()}")
    print("结束:")
    for i, line in enumerate(ch24_raw[-10:]):
        print(f"  {len(ch24_raw)-9+i}: {line.rstrip()}")

    # 重新编号：将"第27章"改为"第24章"，将"27."改为"24."
    print("\n重新编号第24章...")
    ch24_renumbered = []
    for line in ch24_raw:
        # 替换章标题
        line = line.replace('# 第 27 章', '# 第 24 章')
        # 替换小节编号（## 1 -> ## 24.1，但保持原有数字）
        # 这里我们不做太多修改，只改章标题
        ch24_renumbered.append(line)

    print(f"  重新编号后: {len(ch24_renumbered)}行")

    # 现在我们需要：
    # 1. 提取第1-23章（保持不变）
    # 2. 插入新的第24章
    # 3. 提取第25-26章（保持不变）
    # 4. 提取第27章的剩余内容（第7节及以后）- 这部分需要特殊处理
    # 5. 提取第28章及后续

    # 找到各章节位置
    chapter_positions = {}
    for i, line in enumerate(lines):
        match = re.match(r'^# 第 ([0-9]+) 章', line)
        if match:
            num = int(match.group(1))
            chapter_positions[num] = i + 1

    print("\n章节位置:")
    for num in sorted(chapter_positions.keys()):
        print(f"  第{num}章: 第{chapter_positions[num]}行")

    # 构建新文档
    print("\n构建新文档...")

    new_lines = []

    # 1. 第1-23章
    if 23 in chapter_positions:
        end_ch23 = chapter_positions[25] if 25 in chapter_positions else chapter_positions[24]
        new_lines.extend(lines[:end_ch23-1])
        print(f"  添加第1-23章: {len(new_lines)}行")

    # 2. 新的第24章
    new_lines.extend(ch24_renumbered)
    new_lines.append('\n')
    print(f"  添加新第24章: {len(new_lines)}行")

    # 3. 第25-26章（保持不变）
    if 25 in chapter_positions:
        start_ch25 = chapter_positions[25]
        end_ch25 = chapter_positions[26] if 26 in chapter_positions else chapter_positions[27]
        new_lines.extend(lines[start_ch25-1:end_ch25-1])
        print(f"  添加第25章: {len(new_lines)}行")

    if 26 in chapter_positions:
        start_ch26 = chapter_positions[26]
        end_ch26 = ch27_line
        new_lines.extend(lines[start_ch26-1:end_ch26-1])
        print(f"  添加第26章: {len(new_lines)}行")

    # 4. 第27章的剩余内容（第7节及以后）
    # 这部分内容从第6节结束到第28章开始
    # 但这些内容似乎应该是第28章的一部分
    # 让我们检查一下这部分内容
    ch27_remaining = lines[section_6_end:chapter_positions[28]-1] if 28 in chapter_positions else lines[section_6_end:]

    # 查看这部分内容的结构
    print(f"\n第27章剩余内容（第7节及以后）:")
    print(f"  行数: {len(ch27_remaining)}")
    print("  前20行:")
    for i, line in enumerate(ch27_remaining[:20]):
        if line.strip():
            print(f"    {i+1}: {line.rstrip()}")

    # 这部分内容看起来应该还是第27章的内容（大语言模型基础等）
    # 我们暂时保留它作为第27章的后续部分

    # 5. 第28章及后续（保持不变，但需要重新编号）
    if 28 in chapter_positions:
        start_ch28 = chapter_positions[28]
        remaining = lines[start_ch28-1:]

        # 重新编号第28章及后续为第29章及后续
        # 因为第27章还在，只是减少了前6节
        # 所以实际上应该是：
        # - 新第24章（原第27章1-6节）
        # - 第25章（保持）
        # - 第26章（保持）
        # - 第27章（原第27章7节及以后）
        # - 第28章（保持）-> 不需要重新编号
        # 等等，这样不对...

        # 让我重新理解：
        # 用户说第27章（27.1-27.6）应该是第24章
        # 这意味着第27章的前6节要变成一个独立的第24章
        # 那么第27章的剩余部分怎么办？

        # 让我先保持简单：只提取前6节作为第24章，其他保持不变
        new_lines.extend(ch27_remaining)
        new_lines.extend(remaining)
        print(f"  添加第27章剩余及后续章节: {len(new_lines)}行")

    print(f"\n新文档总行数: {len(new_lines)}")

    # 验证
    print("\n验证新文档...")
    new_content = ''.join(new_lines)
    chapters = re.findall(r'^# 第 ([0-9]+) 章', new_content, re.MULTILINE)
    chapter_nums = sorted([int(ch) for ch in chapters])

    print(f"新文档章节: {chapter_nums}")

    if 24 in chapter_nums:
        print("✓ 第24章已添加")
    else:
        print("✗ 第24章未找到")

    # 保存
    output_file = "/Users/lartemacfiles/Desktop/VPT-初诊数据/Claude_Code中文教程_完整版_已修复第24章.md"

    print(f"\n保存到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("✓ 完成")

    return output_file

if __name__ == '__main__':
    main()
