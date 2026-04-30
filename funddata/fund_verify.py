"""
场内基金数据库验证脚本
功能: 检查数据库完整性、数据质量、记录统计
创建时间: 2026-04-29
"""

import sqlite3
import pandas as pd
from pathlib import Path
import os
import sys

# 平台检测
if os.name == 'nt':
    DB_PATH = Path('E:/funddata/funddata.db')
else:
    DB_PATH = Path.home() / 'Desktop' / 'funddata' / 'funddata.db'

def verify():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    if not DB_PATH.exists():
        print(f"❌ 数据库不存在: {DB_PATH}")
        sys.exit(1)

    print(f"数据库: {DB_PATH}")
    print(f"文件大小: {DB_PATH.stat().st_size / 1024 / 1024:.1f} MB")
    print()

    conn = sqlite3.connect(str(DB_PATH))

    # 1. 各表记录数
    print("=" * 55)
    print(f"{'表名':20s} {'记录数':>12s} {'说明':15s}")
    print("-" * 55)

    tables = {
        'fund_basic': '基金主表',
        'fund_daily': '日线行情',
        'fund_nav': '净值数据',
        'fund_adj': '复权因子',
        'fund_portfolio': '持仓明细',
        'fund_share': '份额变动',
        'fund_manager': '基金经理',
        'fund_dividend': '分红送配',
    }

    total = 0
    for table, desc in tables.items():
        try:
            count = pd.read_sql(f'SELECT COUNT(*) as cnt FROM {table}', conn).iloc[0, 0]
            print(f"{table:20s} {count:>12,} {desc:15s}")
            total += count
        except Exception as e:
            print(f"{table:20s} {'❌ 错误':>12s} {str(e)[:30]}")

    print("-" * 55)
    print(f"{'总计':20s} {total:>12,}")
    print()

    # 2. 基金类型分布
    print("=" * 55)
    print("基金类型分布:")
    type_dist = pd.read_sql(
        'SELECT fund_type, COUNT(*) as cnt FROM fund_basic GROUP BY fund_type ORDER BY cnt DESC',
        conn
    )
    for _, row in type_dist.iterrows():
        print(f"  {row['fund_type'] or '未知':10s}: {row['cnt']:>6,} 只")
    print()

    # 3. 数据时间范围抽查
    print("=" * 55)
    print("数据时间范围抽查:")

    # 随机抽5只基金
    sample_codes = pd.read_sql(
        'SELECT ts_code, name FROM fund_basic WHERE fund_type IN ("ETF","LOF") LIMIT 5',
        conn
    )

    for _, row in sample_codes.iterrows():
        code, name = row['ts_code'], row['name']

        # 净值范围
        nav_range = pd.read_sql(
            f"SELECT MIN(end_date) as min_d, MAX(end_date) as max_d, COUNT(*) as cnt "
            f"FROM fund_nav WHERE ts_code='{code}'",
            conn
        )
        if not nav_range.empty and nav_range.iloc[0]['cnt'] > 0:
            r = nav_range.iloc[0]
            print(f"  {code} {name}: 净值 {r['min_d']} ~ {r['max_d']} ({r['cnt']} 条)")

        # 行情范围
        daily_range = pd.read_sql(
            f"SELECT MIN(trade_date) as min_d, MAX(trade_date) as max_d, COUNT(*) as cnt "
            f"FROM fund_daily WHERE ts_code='{code}'",
            conn
        )
        if not daily_range.empty and daily_range.iloc[0]['cnt'] > 0:
            r = daily_range.iloc[0]
            print(f"  {code} {name}: 行情 {r['min_d']} ~ {r['max_d']} ({r['cnt']} 条)")

    print()

    # 4. 空值检查
    print("=" * 55)
    print("关键字段空值检查:")
    for table, col in [
        ('fund_basic', 'ts_code'), ('fund_basic', 'name'),
        ('fund_nav', 'acc_nav'), ('fund_nav', 'unit_nav'),
        ('fund_daily', 'close'), ('fund_daily', 'vol'),
    ]:
        try:
            null_count = pd.read_sql(
                f"SELECT COUNT(*) as cnt FROM {table} WHERE {col} IS NULL",
                conn
            ).iloc[0, 0]
            status = "[OK]" if null_count == 0 else f"[WARN] {null_count} null values"
            print(f"  {table}.{col}: {status}")
        except Exception:
            pass

    # 5. 下载进度检查
    progress_path = DB_PATH.parent / 'progress.json'
    if progress_path.exists():
        import json
        with open(progress_path, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print()
        print("=" * 55)
        print("下载进度:")
        for key in ['fund_basic', 'fund_manager', 'fund_div', 'fund_portfolio',
                     'fund_share', 'fund_adj', 'fund_daily', 'fund_nav']:
            status = progress.get(key, 'pending')
            icon = "[OK]" if status == "done" else ("[...]" if isinstance(status, dict) else "[--]")
            print(f"  {icon} {key}: {status}")

        errors = progress.get('errors', [])
        if errors:
            print(f"\n  ❌ 错误记录: {len(errors)} 条")
            for err in errors[:5]:
                print(f"     {err.get('api')} | {err.get('code')} | {err.get('error')}")

    conn.close()
    print()
    print("验证完成 ✅")

if __name__ == '__main__':
    verify()
