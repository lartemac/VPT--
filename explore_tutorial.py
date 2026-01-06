#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
探索完整教程结构
"""

import asyncio
from playwright.async_api import async_playwright

async def explore_tutorial():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 访问第一个章节
        print("正在访问第一个章节...")
        await page.goto("https://claudecode.tangshuang.net/course/1.1%20Claude%20Code%E6%98%AF%E4%BB%80%E4%B9%88", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # 获取侧边栏或导航栏
        print("\n=== 检查导航结构 ===")

        # 查找所有可能包含章节导航的元素
        navs = await page.locator('nav, aside, [class*="nav"], [class*="sidebar"], [class*="menu"]').all()
        print(f"找到 {len(navs)} 个可能的导航元素")

        # 获取所有链接
        all_links = await page.locator('a').all()
        print(f"\n页面上的所有链接 ({len(all_links)} 个):")

        course_links = []
        for link in all_links:
            href = await link.get_attribute('href')
            text = await link.text_content()

            if href and '/course/' in href:
                course_links.append({
                    'text': text.strip() if text else '',
                    'href': href
                })

        print(f"\n找到 {len(course_links)} 个课程链接:")
        for link in course_links[:50]:
            print(f"  {link['text']}: {link['href']}")

        # 尝试提取完整的目录
        print("\n=== 尝试提取目录 ===")
        toc = await page.evaluate("""() => {
            // 查找所有包含课程链接的容器
            const links = Array.from(document.querySelectorAll('a[href*="/course/"]'));
            return links.map(link => ({
                text: link.textContent.trim(),
                href: link.getAttribute('href'),
                parent: link.parentElement?.tagName,
                classList: Array.from(link.classList)
            }));
        }""")

        # 保存结果
        with open('/Users/lartemacfiles/Desktop/VPT-初诊数据/course_links.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(toc, f, ensure_ascii=False, indent=2)

        print(f"\n保存了 {len(toc)} 个链接到 course_links.json")

        # 分析链接模式
        print("\n=== 链接模式分析 ===")
        chapters = set()
        for link in toc:
            href = link['href']
            # 提取章节号
            import re
            match = re.search(r'/course/(\d+)\.', href)
            if match:
                chapters.add(match.group(1))

        print(f"发现的章节号: {sorted(chapters)}")
        print(f"共 {len(chapters)} 个章节")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(explore_tutorial())
