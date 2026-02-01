#!/usr/bin/env python3
"""
Google Custom Search API 搜索工具
功能：使用Google Custom Search API进行网络搜索
作者：Claude Code
创建时间：2026-02-01
系统：Windows 11

依赖安装：
pip install requests

使用方法：
1. 先配置 google_search_config.json 填入API Key和CX ID
2. 运行：python google_search_tool.py "搜索关键词"

注意事项：
- 免费版API每天限制100次查询
- 建议先用小规模测试
- API Key不要泄露或上传到公开仓库
"""

import requests
import json
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# 配置区域
# ============================================================================

CONFIG_FILE = Path(__file__).parent / "google_search_config.json"
API_URL = "https://www.googleapis.com/customsearch/v1"

# 搜索参数
MAX_RESULTS = 10  # 每次搜索返回结果数量
SAFE_SEARCH = "medium"  # 安全搜索级别: off, medium, high

# ============================================================================
# 工具函数
# ============================================================================

def load_config():
    """
    加载配置文件

    返回:
        配置字典，如果失败则返回None
    """
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 检查是否已配置API密钥
        if config.get('api_key') == 'YOUR_API_KEY_HERE' or config.get('cx_id') == 'YOUR_CX_ID_HERE':
            print('[错误] 请先配置 google_search_config.json')
            print('\n配置步骤：')
            print('1. 用文本编辑器打开 google_search_config.json')
            print('2. 将 YOUR_API_KEY_HERE 替换为您的Google API Key')
            print('3. 将 YOUR_CX_ID_HERE 替换为您的搜索引擎ID (CX)')
            print('4. 保存文件后重新运行脚本\n')
            return None

        return config

    except FileNotFoundError:
        print(f'[错误] 找不到配置文件: {CONFIG_FILE}')
        return None
    except json.JSONDecodeError as e:
        print(f'[错误] 配置文件格式错误: {e}')
        return None


def update_usage_count():
    """
    更新使用次数统计
    """
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        config['usage']['total_queries'] += 1

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f'[警告] 无法更新使用次数: {e}')


def google_search(query, api_key, cx_id, num_results=MAX_RESULTS):
    """
    执行Google搜索

    参数:
        query: 搜索关键词
        api_key: Google API密钥
        cx_id: 搜索引擎ID
        num_results: 返回结果数量

    返回:
        搜索结果列表，每个结果包含标题、链接、摘要
    """
    print('='*80)
    print('Google Custom Search API - 搜索工具')
    print('='*80)
    print(f'\n查询时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'搜索关键词: {query}')
    print('='*80)

    # 构建API请求参数
    params = {
        'key': api_key,
        'cx': cx_id,
        'q': query,
        'num': num_results,
        'safe': SAFE_SEARCH,
    }

    try:
        print('\n[正在搜索...]')
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # 检查是否有错误
        if 'error' in data:
            error = data['error']
            print(f'\n[API错误] 代码: {error.get("code")}')
            print(f'原因: {error.get("message")}')
            print(f'\n常见问题：')
            print(f'1. API Key无效 - 请检查配置文件中的密钥')
            print(f'2. 已达到每日限额 - 免费版每天100次查询')
            print(f'3. CX ID无效 - 请确认搜索引擎ID正确')
            return None

        # 提取搜索结果
        results = []
        items = data.get('items', [])

        if not items:
            print('\n未找到相关结果')
            return results

        print(f'\n找到 {len(items)} 个结果:\n')
        print('='*80)

        for idx, item in enumerate(items, 1):
            title = item.get('title', 'N/A')
            link = item.get('link', 'N/A')
            snippet = item.get('snippet', 'N/A')

            result = {
                'index': idx,
                'title': title,
                'link': link,
                'snippet': snippet
            }
            results.append(result)

            # 显示结果
            print(f'\n{idx}. {title}')
            print(f'   链接: {link}')
            print(f'   摘要: {snippet[:100]}...')

        # 显示搜索信息
        total_results = data.get('searchInformation', {}).get('totalResults', 'N/A')
        search_time = data.get('searchInformation', {}).get('formattedSearchTime', 'N/A')

        print('\n' + '='*80)
        print(f'[搜索完成] 总结果数: {total_results} | 耗时: {search_time}')
        print('='*80)

        # 更新使用次数
        update_usage_count()

        return results

    except requests.exceptions.Timeout:
        print('\n[错误] 请求超时，请检查网络连接')
        return None
    except requests.exceptions.HTTPError as e:
        print(f'\n[HTTP错误] {e}')
        if response.status_code == 403:
            print('\n可能原因：')
            print('1. API Key无效或未启用Custom Search API')
            print('2. 已达到每日查询限额（免费版100次/天）')
            print('3. 未配置正确的CX ID')
        return None
    except Exception as e:
        print(f'\n[错误] {e}')
        return None


def save_results_to_file(results, query):
    """
    保存搜索结果到文件

    参数:
        results: 搜索结果列表
        query: 搜索关键词
    """
    if not results:
        return

    # 生成文件名
    safe_query = query[:30].replace(' ', '_').replace('/', '_').replace('\\', '_')
    safe_query = ''.join(c if c.isalnum() or c in '_-' else '_' for c in safe_query)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"google_search_{safe_query}_{timestamp}.txt"

    # 保存到桌面
    output_path = Path.home() / 'Desktop' / filename

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('='*80 + '\n')
            f.write(f'Google搜索结果 - {query}\n')
            f.write(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write('='*80 + '\n\n')

            for result in results:
                f.write(f"\n[{result['index']}] {result['title']}\n")
                f.write(f"链接: {result['link']}\n")
                f.write(f"摘要: {result['snippet']}\n")
                f.write('-'*80 + '\n')

        print(f'\n[保存成功] 结果已保存到: {output_path}')

    except Exception as e:
        print(f'\n[警告] 无法保存结果: {e}')


def show_usage_stats(config):
    """
    显示使用统计信息
    """
    usage = config.get('usage', {})
    total = usage.get('total_queries', 0)
    limit = usage.get('daily_limit', 100)
    reset = usage.get('last_reset', 'N/A')

    print(f'\n[使用统计]')
    print(f'  今日已查询: {total} 次')
    print(f'  每日限额: {limit} 次')
    print(f'  剩余额度: {max(0, limit - total)} 次')
    print(f'  重置日期: {reset}')


# ============================================================================
# 主函数
# ============================================================================

def main():
    """
    主程序入口
    """
    print('\n' + '='*80)
    print(' ' * 25 + 'Google 搜索工具 v1.0')
    print('='*80)

    # 加载配置
    config = load_config()
    if config is None:
        sys.exit(1)

    api_key = config.get('api_key')
    cx_id = config.get('cx_id')

    # 获取搜索关键词
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        print('\n请输入搜索关键词（按回车开始搜索）:')
        print('提示: 输入越具体，结果越精确')
        print('-'*80)
        query = input('\n搜索关键词: ').strip()

        if not query:
            print('[错误] 搜索关键词不能为空')
            sys.exit(1)

    # 显示使用统计
    show_usage_stats(config)

    # 执行搜索
    results = google_search(query, api_key, cx_id)

    if results:
        # 询问是否保存
        print('\n是否保存搜索结果到桌面？(y/n): ', end='')
        try:
            choice = input().strip().lower()
            if choice in ['y', 'yes', '是', 'Y']:
                save_results_to_file(results, query)
        except:
            pass

    print('\n[程序结束]')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n[中断] 用户取消搜索')
    except Exception as e:
        print(f'\n[错误] {e}')
        import traceback
        traceback.print_exc()
