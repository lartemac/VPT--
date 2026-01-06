#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查网站结构
"""

import asyncio
import json
from playwright.async_api import async_playwright

async def check_site_structure():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 监听所有网络请求
        requests = []
        def log_request(request):
            requests.append({
                'url': request.url,
                'method': request.method,
                'resource_type': request.resource_type
            })

        page.on('request', log_request)

        print("正在访问网站...")
        await page.goto("https://claudecode.tangshuang.net", wait_until="networkidle")
        await page.wait_for_timeout(5000)

        print("\n=== 网络请求 ===")
        for req in requests:
            if 'json' in req['url'] or 'api' in req['url'] or 'data' in req['url']:
                print(f"{req['method']}: {req['url']}")

        # 获取页面内容
        print("\n=== 页面标题 ===")
        titles = await page.locator('h1, h2, h3').all_text_contents()
        for title in titles[:20]:
            print(f"- {title}")

        # 获取所有链接
        print("\n=== 教程链接示例 ===")
        links = await page.locator('a[href*="/course/"]').all()
        print(f"找到 {len(links)} 个 /course/ 链接")

        for link in links[:10]:
            text = await link.text_content()
            href = await link.get_attribute('href')
            print(f"- {text}: {href}")

        # 尝试获取页面数据
        print("\n=== 检查页面数据 ===")
        page_data = await page.evaluate("""() => {
            // 查找可能包含数据的全局变量
            const dataKeys = []
            for (let key in window) {
                if (key.toLowerCase().includes('data') ||
                    key.toLowerCase().includes('content') ||
                    key.toLowerCase().includes('route') ||
                    key.toLowerCase().includes('page')) {
                    try {
                        const value = JSON.stringify(window[key])
                        if (value.length < 500) {
                            dataKeys.push({key, value})
                        }
                    } catch(e) {}
                }
            }
            return dataKeys
        }""")

        print("可能包含数据的变量:")
        for item in page_data[:10]:
            print(f"  {item['key']}: {item['value'][:100]}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_site_structure())
