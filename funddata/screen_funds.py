"""
基金多维度筛选脚本
条件:
1. 成立>=3年, 年化收益>=12%
2. 近3年基金经理无变动
3. 净值处于85%分位以下
4. 回撤修复时间<=3个月
5. 基金规模>=2亿
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DB_PATH = 'E:/funddata/funddata.db'

def screen_funds():
    conn = sqlite3.connect(DB_PATH)
    print("正在加载数据...")

    # 1. 基金基本信息
    basic = pd.read_sql("SELECT * FROM fund_basic", conn)
    three_years_ago = (datetime.now() - timedelta(days=3*365)).strftime('%Y%m%d')
    basic = basic[basic['found_date'].notna()]
    basic = basic[basic['found_date'] <= three_years_ago]
    # 只看股票型和混合型
    basic = basic[basic['fund_type'].isin(['股票型', '混合型'])]
    # 排除已退市的
    basic = basic[basic['delist_date'].isna()]
    print(f"  符合条件(成立>=3年, 股票/混合型, 未退市): {len(basic)} 只")

    codes = basic['ts_code'].tolist()

    # 2. 净值数据 - 全量加载（内存够用）
    print("  加载净值数据...")
    nav = pd.read_sql("SELECT ts_code, ann_date, unit_nav FROM fund_nav WHERE unit_nav IS NOT NULL AND ann_date IS NOT NULL", conn)
    nav.rename(columns={'ann_date': 'nav_date'}, inplace=True)
    nav['nav_date'] = nav['nav_date'].astype(str)
    nav['unit_nav'] = nav['unit_nav'].astype(float)
    nav = nav[nav['ts_code'].isin(codes)]
    print(f"  净值记录: {len(nav):,}")

    # 3. 基金经理数据
    mgr = pd.read_sql("SELECT * FROM fund_manager", conn)
    print(f"  基金经理记录: {len(mgr):,}")

    # 4. 份额数据（最近）
    share = pd.read_sql("SELECT ts_code, trade_date, fd_share FROM fund_share", conn)
    share['fd_share'] = share['fd_share'].astype(float)
    # 每只基金取最新份额
    latest_share = share.sort_values('trade_date').groupby('ts_code').last().reset_index()
    print(f"  份额记录: {len(latest_share):,}")

    conn.close()

    # ========== 开始筛选 ==========
    print("\n" + "=" * 60)
    print("  开始多维度筛选")
    print("=" * 60)

    results = []

    for idx, (_, fund) in enumerate(basic.iterrows()):
        ts_code = fund['ts_code']
        name = fund['name']
        found_date = str(fund['found_date'])

        # 获取该基金的净值
        fund_nav = nav[nav['ts_code'] == ts_code].copy()
        if len(fund_nav) < 250:  # 至少1年数据
            continue

        fund_nav = fund_nav.sort_values('nav_date').reset_index(drop=True)

        # === 条件1: 年化收益率 >= 12% ===
        first_nav = fund_nav.iloc[0]['unit_nav']
        latest_nav = fund_nav.iloc[-1]['unit_nav']
        latest_date = fund_nav.iloc[-1]['nav_date']

        if first_nav <= 0 or latest_nav <= 0:
            continue

        # 计算运作年数
        try:
            d_start = datetime.strptime(found_date, '%Y%m%d')
            d_end = datetime.strptime(latest_date, '%Y%m%d')
        except:
            continue
        years = (d_end - d_start).days / 365.25
        if years < 3:
            continue

        # 年化收益率 (CAGR)
        total_return = latest_nav / first_nav
        annual_return = (total_return ** (1/years) - 1) * 100
        if annual_return < 12:
            continue

        # 近1年/3年收益率
        for days, label in [(365, '1y'), (1095, '3y')]:
            target = (d_end - timedelta(days=days)).strftime('%Y%m%d')
            past = fund_nav[fund_nav['nav_date'] <= target]
            if not past.empty:
                pn = past.iloc[-1]['unit_nav']
                if pn > 0:
                    ret_days = (d_end - datetime.strptime(str(past.iloc[-1]['nav_date']), '%Y%m%d')).days
                    if ret_days > 0:
                        yr = ret_days / 365.25
                        if yr > 0:
                            fund[f'ret_{label}'] = ((latest_nav/pn)**(1/yr) - 1) * 100

        # === 条件2: 近3年基金经理无变动 ===
        fund_mgr = mgr[mgr['ts_code'] == ts_code]
        three_yr_ago_str = (datetime.now() - timedelta(days=3*365)).strftime('%Y%m%d')
        manager_changed = False
        if not fund_mgr.empty:
            for _, m in fund_mgr.iterrows():
                end_date = str(m.get('end_date', '')) if pd.notna(m.get('end_date')) else ''
                if end_date and end_date != 'None' and end_date >= three_yr_ago_str:
                    manager_changed = True
                    break
            current_mgrs = fund_mgr[fund_mgr['end_date'].isna() | (fund_mgr['end_date'].astype(str) == '') | (fund_mgr['end_date'].astype(str) == 'None')]
            mgr_name = ','.join(current_mgrs['name'].tolist()) if not current_mgrs.empty else '未知'
        else:
            # 场内基金经理数据不全，无数据则标注"场内/无数据"跳过此条件
            mgr_name = '场内基金'
        if manager_changed:
            continue

        # === 条件3: 净值85%分位以下 ===
        # 用近250个交易日的净值范围计算当前位置
        recent = fund_nav.tail(250)
        if len(recent) < 60:
            continue
        r_min = recent['unit_nav'].min()
        r_max = recent['unit_nav'].max()
        if r_max <= r_min:
            continue
        position = (latest_nav - r_min) / (r_max - r_min) * 100
        if position >= 85:
            continue

        # === 条件4: 回撤修复时间 <= 3个月 ===
        fund_nav['cummax'] = fund_nav['unit_nav'].cummax()
        fund_nav['drawdown'] = (fund_nav['unit_nav'] - fund_nav['cummax']) / fund_nav['cummax']

        # 找出所有回撤事件和修复时间
        in_drawdown = False
        max_recovery_days = 0
        dd_start_idx = 0
        dd_count = 0

        for i in range(1, len(fund_nav)):
            if fund_nav.iloc[i]['drawdown'] < -0.05:  # 回撤超过5%才算
                if not in_drawdown:
                    in_drawdown = True
                    dd_start_idx = i
            else:
                if in_drawdown:
                    # 回撤修复了
                    dd_end_idx = i
                    if dd_start_idx > 0 and dd_end_idx > dd_start_idx:
                        # 计算修复天数
                        start_d = fund_nav.iloc[dd_start_idx]['nav_date']
                        end_d = fund_nav.iloc[dd_end_idx]['nav_date']
                        try:
                            recovery_days = (datetime.strptime(end_d, '%Y%m%d') - datetime.strptime(start_d, '%Y%m%d')).days
                            max_recovery_days = max(max_recovery_days, recovery_days)
                            dd_count += 1
                        except:
                            pass
                    in_drawdown = False

        # 如果当前仍在回撤中，计算已持续天数
        if in_drawdown:
            try:
                current_dd_days = (datetime.strptime(latest_date, '%Y%m%d') - datetime.strptime(fund_nav.iloc[dd_start_idx]['nav_date'], '%Y%m%d')).days
                max_recovery_days = max(max_recovery_days, current_dd_days)
                dd_count += 1
            except:
                pass

        if max_recovery_days > 90:  # 超过3个月
            continue

        # === 条件5: 基金规模 >= 2亿 ===
        fund_share_data = latest_share[latest_share['ts_code'] == ts_code]
        if fund_share_data.empty:
            continue
        fund_size = fund_share_data.iloc[0]['fd_share'] * latest_nav / 10000  # 份额(亿)*净值
        # fd_share 单位是亿份，规模 = 份额 * 净值
        fund_size_val = fund_share_data.iloc[0]['fd_share'] * latest_nav / 10000  # 万份 -> 亿元
        if fund_size_val < 2:
            continue

        # 历史最大回撤
        max_dd = fund_nav['drawdown'].min() * 100

        # 近1年指标
        recent_1y = fund_nav.tail(252)
        if len(recent_1y) > 20:
            daily_ret = recent_1y['unit_nav'].pct_change().dropna()
            ann_vol = daily_ret.std() * np.sqrt(252) * 100
            ann_ret_1y = daily_ret.mean() * 252 * 100
            sharpe = ann_ret_1y / ann_vol if ann_vol > 0 else 0
            dd_1y = ((recent_1y['unit_nav'] - recent_1y['unit_nav'].cummax()) / recent_1y['unit_nav'].cummax() * 100).min()
        else:
            ann_vol = ann_ret_1y = sharpe = dd_1y = 0

        results.append({
            'ts_code': ts_code,
            'name': name,
            'fund_type': fund['fund_type'],
            'found_date': found_date,
            'years': round(years, 1),
            'latest_nav': round(latest_nav, 4),
            'annual_return': round(annual_return, 2),
            'ann_ret_1y': round(ann_ret_1y, 2),
            'sharpe_1y': round(sharpe, 2),
            'max_dd': round(max_dd, 2),
            'dd_1y': round(dd_1y, 2),
            'position': round(position, 1),
            'max_recovery': max_recovery_days,
            'dd_count': dd_count,
            'fund_size': round(fund_size_val, 2),
            'manager': mgr_name,
            'management': fund.get('management', ''),
        })

        if len(results) % 10 == 0:
            print(f"  已找到 {len(results)} 只符合条件的基金... (已扫描 {idx+1}/{len(basic)})")

    # 输出结果
    print(f"\n{'='*60}")
    print(f"  筛选完成！共找到 {len(results)} 只基金")
    print(f"{'='*60}")

    if not results:
        print("  未找到符合条件的基金")
        return

    df = pd.DataFrame(results)
    # 按年化收益排序
    df = df.sort_values('annual_return', ascending=False)

    # 保存结果
    df.to_excel('E:/funddata/screened_funds.xlsx', index=False)
    print(f"  结果已保存到: E:/funddata/screened_funds.xlsx")

    # 打印TOP结果
    print(f"\n{'='*100}")
    print(f"{'代码':12s} {'名称':20s} {'类型':6s} {'年限':>4s} {'年化%':>6s} {'近1年%':>7s} {'夏普':>5s} {'最大回撤%':>8s} {'仓位%':>5s} {'最长修复(天)':>10s} {'规模(亿)':>8s} {'经理'}")
    print('-' * 100)
    for _, r in df.head(30).iterrows():
        print(f"{r['ts_code']:12s} {r['name'][:20]:20s} {r['fund_type']:6s} {r['years']:4.1f} {r['annual_return']:6.2f} {r['ann_ret_1y']:7.2f} {r['sharpe_1y']:5.2f} {r['max_dd']:8.2f} {r['position']:5.1f} {r['max_recovery']:10d} {r['fund_size']:8.2f} {r['manager'][:10]}")

    # 汇总
    print(f"\n  共 {len(df)} 只基金通过全部5项筛选条件")
    print(f"  平均年化收益: {df['annual_return'].mean():.2f}%")
    print(f"  平均夏普比率: {df['sharpe_1y'].mean():.2f}")
    print(f"  平均最大回撤: {df['max_dd'].mean():.2f}%")
    print(f"  平均当前仓位: {df['position'].mean():.1f}%")

if __name__ == '__main__':
    screen_funds()
