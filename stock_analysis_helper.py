#!/usr/bin/env python3
"""
功能描述: A股股票分析数据获取助手
创建时间: 2026-03-31
创建系统: macOS/Windows 通用

用途:
为 stock-analysis-cn skill 提供数据获取支持
通过 Tushare API 获取股票分析所需的各类数据
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# 平台检测
IS_WINDOWS = os.name == 'nt'

# Tushare 导入
try:
    import tushare as ts
except ImportError:
    print("❌ 未安装 tushare，请运行: pip3 install tushare")
    sys.exit(1)

# ==================== 配置 ====================
# API Token 配置文件
CONFIG_FILE = Path(__file__).parent / "api_config.json"

def get_tushare_token():
    """获取 Tushare API Token"""
    # 从环境变量获取
    token = os.environ.get("TUSHARE_TOKEN")
    if token:
        return token

    # 从配置文件获取
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("tushare_token", "")

    return None

def get_api():
    """初始化 Tushare API"""
    token = get_tushare_token()
    if not token:
        print("❌ 未找到 Tushare Token，请设置环境变量 TUSHARE_TOKEN")
        print("   或在配置文件中添加 tushare_token")
        return None
    return ts.pro_api(token)


def get_trade_date(offset=0):
    """获取交易日日期
    offset: 0=最新交易日, -1=前一个交易日, 1=下一个交易日
    """
    pro = get_api()
    if not pro:
        return None

    try:
        # 获取最近交易日
        trade_cal = pro.trade_cal(exchange='SSE',
                                   start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'),
                                   end_date=datetime.now().strftime('%Y%m%d'))
        trade_dates = trade_cal[trade_cal.is_open == 1]['cal_date'].tolist()
        if trade_dates and offset < len(trade_dates):
            return trade_dates[offset]
    except Exception as e:
        print(f"❌ 获取交易日失败: {e}")

    return datetime.now().strftime('%Y%m%d')


# ==================== 第一步：初步筛选 ====================

def get_daily_basic(trade_date=None):
    """获取全市场日线基本面数据（市值、PE、PB等）"""
    pro = get_api()
    if not pro:
        return None

    if not trade_date:
        trade_date = get_trade_date()

    try:
        print(f"📊 获取 {trade_date} 市场数据...")
        df = pro.daily_basic(trade_date=trade_date,
                             fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,ps,total_mv,circ_mv')
        return df
    except Exception as e:
        print(f"❌ 获取日线数据失败: {e}")
        return None


def screen_stocks(value_pe_max=30, value_pb_max=3, growth_roe_min=10,
                  quality_debt_max=60, limit=50):
    """多因子筛选股票

    参数:
    - value_pe_max: PE上限
    - value_pb_max: PB上限
    - growth_roe_min: ROE下限
    - quality_debt_max: 资产负债率上限
    - limit: 返回数量限制
    """
    pro = get_api()
    if not pro:
        return None

    trade_date = get_trade_date()
    print(f"🔍 开始多因子筛选（{trade_date}）...")

    # 1. 获取日线基本面
    daily_df = get_daily_basic(trade_date)
    if daily_df is None:
        return None

    # 2. 获取财务指标（需要多次请求）
    print("📈 获取财务指标...")
    try:
        # 获取最新财务指标
        trade_date_ym = trade_date[:6]  # YYYYMM
        fina_df = pro.fina_indicator(end_date=trade_date,
                                     fields='ts_code,end_date,roe,roe_waa,roe_dt,roa,roe_yearly,debt_to_assets,current_ratio,quick_ratio')
        # 取每个股票的最新一期
        fina_df = fina_df.sort_values('end_date').groupby('ts_code').last().reset_index()
    except Exception as e:
        print(f"⚠️  获取财务指标失败: {e}")
        fina_df = None

    # 3. 合并数据
    if fina_df is not None:
        merged_df = daily_df.merge(fina_df, on='ts_code', how='left')
    else:
        merged_df = daily_df

    # 4. 应用筛选条件
    print("🔎 应用筛选条件...")

    # 价值因子
    value_mask = (
        (merged_df['pe'] > 0) & (merged_df['pe'] <= value_pe_max) &
        (merged_df['pb'] > 0) & (merged_df['pb'] <= value_pb_max)
    )

    # 质量因子
    if 'debt_to_assets' in merged_df.columns:
        quality_mask = merged_df['debt_to_assets'] <= quality_debt_max
    else:
        quality_mask = pd.Series(True, index=merged_df.index)

    # 成长因子
    if 'roe' in merged_df.columns:
        growth_mask = merged_df['roe'] >= growth_roe_min
    else:
        growth_mask = pd.Series(True, index=merged_df.index)

    # 综合筛选
    filtered_df = merged_df[value_mask & quality_mask & growth_mask]

    # 排序（按ROE降序）
    if 'roe' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('roe', ascending=False)

    result = filtered_df.head(limit).copy()

    print(f"\n✅ 筛选完成: {len(result)} 只股票通过筛选")
    return result


# ==================== 第二步：确认基本盘 ====================

def get_fundamental_analysis(ts_code, years=3):
    """获取个股财务健康数据（近3年）

    返回: {
        'income': 利润表数据,
        'cashflow': 现金流表数据,
        'balancesheet': 资产负债表数据,
        'indicator': 财务指标数据
    }
    """
    pro = get_api()
    if not pro:
        return None

    print(f"📊 获取 {ts_code} 财务数据（近{years}年）...")

    result = {}

    # 计算起始日期
    start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y%m%d')

    try:
        # 利润表
        income = pro.income(ts_code=ts_code, start_date=start_date, period='年度')
        result['income'] = income

        # 现金流表
        cashflow = pro.cashflow(ts_code=ts_code, start_date=start_date, period='年度')
        result['cashflow'] = cashflow

        # 资产负债表
        balancesheet = pro.balancesheet(ts_code=ts_code, start_date=start_date, period='年度')
        result['balancesheet'] = balancesheet

        # 财务指标
        indicator = pro.fina_indicator(ts_code=ts_code, start_date=start_date)
        result['indicator'] = indicator

        print(f"✅ 财务数据获取完成")
        return result

    except Exception as e:
        print(f"❌ 获取财务数据失败: {e}")
        return None


def analyze_fundamental(ts_code, years=3):
    """分析财务健康度

    返回分析报告字典
    """
    data = get_fundamental_analysis(ts_code, years)
    if not data or not data.get('indicator'):
        return None

    ind = data['indicator'].sort_values('end_date').tail(years)

    report = {
        'ts_code': ts_code,
        'years_analyzed': len(ind),
        'roe_trend': [],
        'revenue_growth': None,
        'profit_growth': None,
        'debt_ratio': None,
        'current_ratio': None,
    }

    # ROE趋势
    if 'roe' in ind.columns:
        report['roe_trend'] = ind['roe'].tolist()

    # 资产负债率
    if 'debt_to_assets' in ind.columns:
        report['debt_ratio'] = ind['debt_to_assets'].iloc[-1] if len(ind) > 0 else None

    # 流动比率
    if 'current_ratio' in ind.columns:
        report['current_ratio'] = ind['current_ratio'].iloc[-1] if len(ind) > 0 else None

    return report


# ==================== 第三步：资金动向 ====================

def get_money_flow(ts_code, days=30):
    """获取个股资金流向数据

    注意：Tushare 普通版可能不支持 moneyflow 接口
    需要高级权限或使用其他数据源
    """
    pro = get_api()
    if not pro:
        return None

    end_date = get_trade_date()
    start_date = (datetime.now() - timedelta(days=days+30)).strftime('%Y%m%d')

    try:
        print(f"💰 获取 {ts_code} 资金流向（近{days}天）...")
        df = pro.moneyflow(ts_code=ts_code, start_date=start_date, end_date=end_date)
        print(f"⚠️  注意：资金流向数据需要 Tushare 高级权限")
        return df.tail(days)
    except Exception as e:
        print(f"⚠️  获取资金流向失败（可能需要高级权限）: {e}")
        return None


def get_top_list(ts_code, days=30):
    """获取龙虎榜数据"""
    pro = get_api()
    if not pro:
        return None

    end_date = get_trade_date()
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')

    try:
        df = pro.top_list(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df
    except Exception as e:
        print(f"⚠️  获取龙虎榜失败: {e}")
        return None


# ==================== 第四步：风险数据 ====================

def get_risk_data(ts_code):
    """获取风险相关数据

    包括：解禁、减持、质押等
    """
    pro = get_api()
    if not pro:
        return None

    result = {}

    try:
        # 解禁数据
        unlock = pro.tk_unlock(ts_code=ts_code)
        result['unlock'] = unlock
    except:
        result['unlock'] = None

    try:
        # 减持数据
        shareholder = pro.shareholder(ts_code=ts_code)
        result['shareholder'] = shareholder
    except:
        result['shareholder'] = None

    return result


# ==================== 输出格式化 ====================

def format_screen_result(df):
    """格式化筛选结果"""
    if df is None or len(df) == 0:
        return "❌ 无股票通过筛选"

    output = ["\n【初步筛选结果】"]
    output.append(f"- 筛选日期: {df['trade_date'].iloc[0] if 'trade_date' in df.columns else 'N/A'}")
    output.append(f"- 通过数量: {len(df)} 只")
    output.append("\n排名 | 代码 | 名称 | PE | PB | ROE")
    output.append("-" * 50)

    for i, row in df.head(20).iterrows():
        roe = f"{row.get('roe', 0):.2f}%" if 'roe' in row else "N/A"
        output.append(f"{i+1:2d} | {row['ts_code']} | ??? | {row['pe']:.2f} | {row['pb']:.2f} | {roe}")

    return "\n".join(output)


def format_fundamental_report(report):
    """格式化财务分析报告"""
    if not report:
        return "❌ 无财务数据"

    output = [f"\n【财务健康评估】{report['ts_code']}"]
    output.append(f"- 分析年数: {report.get('years_analyzed', 'N/A')}")

    if report['roe_trend']:
        output.append(f"- ROE趋势: {report['roe_trend']}")

    return "\n".join(output)


# ==================== 主函数 ====================

def main():
    """主函数 - 命令行使用"""
    import argparse

    parser = argparse.ArgumentParser(description='A股分析数据获取助手')
    parser.add_argument('action', choices=['screen', 'analyze', 'moneyflow'],
                       help='操作类型: screen=筛选, analyze=个股分析, moneyflow=资金流向')
    parser.add_argument('--code', help='股票代码（用于analyze和moneyflow）')
    parser.add_argument('--limit', type=int, default=50, help='筛选返回数量')

    args = parser.parse_args()

    if args.action == 'screen':
        result = screen_stocks(limit=args.limit)
        print(format_screen_result(result))

    elif args.action == 'analyze':
        if not args.code:
            print("❌ 请指定股票代码，如: 600000.SH")
            return
        report = analyze_fundamental(args.code)
        print(format_fundamental_report(report))

    elif args.action == 'moneyflow':
        if not args.code:
            print("❌ 请指定股票代码")
            return
        result = get_money_flow(args.code)
        if result is not None:
            print(result)


if __name__ == "__main__":
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        print("""
A股分析数据获取助手
==================

用法:
  python stock_analysis_helper.py screen [--limit 50]
  python stock_analysis_helper.py analyze --code 600000.SH
  python stock_analysis_helper.py moneyflow --code 600000.SH

功能:
  1. screen    - 多因子筛选股票
  2. analyze   - 个股财务健康分析
  3. moneyflow - 资金流向分析
        """)
    else:
        main()
