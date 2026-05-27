#!/usr/bin/env python3
"""
家庭月收支数学模型 — 完整报告生成器（单文件版）
================================================
使用方法:
  1. 修改下方 ==== 参数设置 ==== 区域中的各项金额和周期
  2. 终端运行: python3 家庭预算模型_完整报告生成器.py
  3. 桌面自动生成: 家庭收支预测报告.html（含所有嵌入式图表）

依赖: numpy, pandas, matplotlib (均为标准科学计算库)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
from collections import defaultdict
import base64, os

DESKTOP = os.path.expanduser("~/Desktop")
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')

# ============================================================
# ===== 参数设置（在此区域修改各项金额和周期）=====
# ============================================================

# -- 收入模型 --
INCOME_MEAN   = 18000    # 月收入均值（元）
INCOME_STD    = 1000     # 月收入标准差
INCOME_MIN    = 14000    # 月收入下限
INCOME_MAX    = 22000    # 月收入上限
PAYDAY        = 20       # 每月到账日

# -- 每日吃饭（双模：节约日 / 奢侈日）--
FRUGAL_MEAN   = 200      # 节约日餐费均值
FRUGAL_STD    = 30       # 节约日标准差
FRUGAL_MIN    = 120      # 节约日下限
FRUGAL_MAX    = 300      # 节约日上限
LUXURY_MEAN   = 400      # 奢侈日餐费均值
LUXURY_STD    = 60       # 奢侈日标准差
LUXURY_MIN    = 300      # 奢侈日下限
LUXURY_MAX    = 600      # 奢侈日上限
LUXURY_PER_WEEK_MEAN = 2       # 每周奢侈日次数均值
LUXURY_PER_WEEK_STD  = 0.5     # 每周奢侈日次数标准差

# -- 蓄水池（年付准备金）每月浮动缴纳 --
SINKING_BASE  = 1800     # 基准月缴额
SINKING_UP    = 200      # 上浮上限
SINKING_DOWN  = -1000    # 下浮下限（负数表示下浮）
# 每月实际缴纳 = SINKING_BASE + uniform(SINKING_DOWN, SINKING_UP)

# -- 模拟设置 --
START_YEAR    = 2026
START_MONTH   = 6
SIM_MONTHS    = 60       # 模拟月数
RANDOM_SEED   = 42       # 随机种子（修改可得到不同随机结果）
INITIAL_BALANCE = 50000  # 初始余额（元）

# ============================================================
# ===== 每月刚性账单（可在此增删改）=====
# ===== 格式: {日期: [(名称, 金额), ...]}
# ============================================================
MONTHLY_BILLS = {
    1:  [("房贷", 2000),
         ("办公室月租", 1300),
         ("车位月租", 1000),
         ("物管费", 330)],
    5:  [("过路费", 600),
         ("牛奶钙片等营养品", 600),
         ("保洁用品", 300),
         ("车辆保养均摊", 325)],
    15: [("水电燃气网络手机", 1000)],
}

# ============================================================
# ===== 年度/周期支出（从蓄水池扣款）=====
# ============================================================

# 固定在指定月份的年付事件
# 格式: {月: [(名称, 金额)]}
YEARLY_SINKING_EVENTS = {
    4:  [("学校餐费(春期中)", 600)],
    6:  [("学校餐费(春期末)", 600)],
    9:  [("车辆保险", 4500),
         ("校服", 1000)],
    10: [("学校餐费(秋期中)", 600)],
    12: [("学校餐费(秋期末)", 600)],
}

# 自定义周期事件（非年度周期）
# 格式: [(名称, 金额, 周期间隔月数, 首次缴费日期)]
CYCLIC_EVENTS = [
    ("游泳课",   3600,  10, datetime(2026, 7, 1)),
    ("计算机课", 16000, 16, datetime(2026, 8, 1)),
    ("美术课",   1400,  4,  datetime(2026, 8, 1)),
]

# ============================================================
# ===== 优先级分类（决定"极限生存线"怎么算）=====
# ============================================================
P0_P1_ITEMS = [
    "房贷", "办公室月租", "车位月租", "物管费", "水电燃气网络手机",
    "过路费", "车辆保养均摊", "车辆保险",
    "学校餐费(春期中)", "学校餐费(春期末)",
    "学校餐费(秋期中)", "学校餐费(秋期末)", "校服"
]
P2_ITEMS = ["游泳课", "美术课", "计算机课"]
P3_ITEMS = ["牛奶钙片等营养品", "保洁用品"]

# ============================================================
# ===== 支出目录 DataFrame（仅用于展示）=====
# ============================================================
def _make_expense_df():
    rows = []
    for dom, items in MONTHLY_BILLS.items():
        for name, amt in items:
            rows.append((name, amt, "monthly", amt))
    rows.append(("每日吃饭(双模:节约¥200+奢侈¥400)", 7800, "daily", 7800))
    for m, items in YEARLY_SINKING_EVENTS.items():
        for name, amt in items:
            rows.append((name, amt, "yearly", round(amt/12, 0)))
    for name, amt, interval, _ in CYCLIC_EVENTS:
        rows.append((f"{name}(每{interval}月)", amt, f"{interval}-month", round(amt/interval, 0)))
    return pd.DataFrame(rows, columns=["支出项目","原金额","支付周期","月均摊"])

# ============================================================
# ===== 核心模拟引擎（请勿修改）=====
# ============================================================
def build_sinking_calendar(start_dt, end_dt):
    cal = defaultdict(list)
    for yr in range(start_dt.year, end_dt.year + 1):
        for month, items in YEARLY_SINKING_EVENTS.items():
            d = datetime(yr, month, 1)
            if start_dt <= d <= end_dt:
                for name, amt in items:
                    cal[d].append((name, amt))
    for name, amt, interval, next_date in CYCLIC_EVENTS:
        d = next_date
        while d <= end_dt:
            if d >= start_dt:
                cal[d].append((name, amt))
            new_month = d.month + interval
            new_year = d.year + (new_month - 1) // 12
            new_month = (new_month - 1) % 12 + 1
            d = datetime(new_year, new_month, 1)
    return dict(sorted(cal.items()))

def classify_priority(name):
    for kw in P0_P1_ITEMS:
        if kw in name: return "P0-P1"
    for kw in P2_ITEMS:
        if kw in name: return "P2"
    for kw in P3_ITEMS:
        if kw in name: return "P3"
    return "P1"

def run_simulation():
    np.random.seed(RANDOM_SEED)
    start_date = datetime(START_YEAR, START_MONTH, 1)
    total_days = SIM_MONTHS // 12 * 365 + (SIM_MONTHS % 12) * 31 + 60
    end_date = start_date + timedelta(days=total_days)
    calendar = build_sinking_calendar(start_date, end_date)

    total_annual_sinking = (
        sum(amt for items in YEARLY_SINKING_EVENTS.values() for _, amt in items) +
        sum(amt * (12 / interval) for _, amt, interval, _ in CYCLIC_EVENTS)
    )

    balance = INITIAL_BALANCE
    reserve = 0
    monthly_log = []
    current = start_date
    current_month_key = None

    mon = lambda: None
    mon.income = mon.fixed = mon.food = mon.food_fr = mon.food_lx = 0
    mon.fr_days = mon.lx_days = mon.sink_in = mon.sink_out = mon.sink_fm = 0
    mon.p0p1 = mon.p2 = mon.p3 = 0

    luxury_dates = set()
    current_week = None

    while current <= end_date:
        d, m, y = current.day, current.month, current.year
        mk = (y, m)

        if mk != current_month_key:
            if current_month_key is not None:
                monthly_log.append({
                    "year": current_month_key[0], "month": current_month_key[1],
                    "income": mon.income, "fixed_bills": mon.fixed,
                    "food": round(mon.food, 0), "sinking_in": mon.sink_in,
                    "sinking_out": mon.sink_out, "sinking_from_main": mon.sink_fm,
                    "reserve_end": round(reserve, 0),
                    "p0p1": round(mon.p0p1, 0), "p2": round(mon.p2, 0), "p3": round(mon.p3, 0),
                    "net_after_reserve": round(mon.income - mon.fixed - mon.food - mon.sink_in, 0),
                    "balance_end": round(balance, 0),
                    "food_frugal": round(mon.food_fr, 0), "food_luxury": round(mon.food_lx, 0),
                    "food_frugal_days": mon.fr_days, "food_luxury_days": mon.lx_days,
                })
            current_month_key = mk
            mon.income = mon.fixed = mon.food = mon.food_fr = mon.food_lx = 0
            mon.fr_days = mon.lx_days = mon.sink_in = mon.sink_out = mon.sink_fm = 0
            mon.p0p1 = mon.p2 = mon.p3 = 0

        iso_week = current.isocalendar()[1]
        if iso_week != current_week:
            current_week = iso_week
            n_lx = int(np.clip(np.random.normal(LUXURY_PER_WEEK_MEAN, LUXURY_PER_WEEK_STD), 1, 3))
            ws = current - timedelta(days=current.weekday())
            chosen = np.random.choice([ws + timedelta(days=i) for i in range(7)], size=n_lx, replace=False)
            luxury_dates = set(chosen)

        day_net = 0

        if d == PAYDAY:
            inc = np.clip(np.random.normal(INCOME_MEAN, INCOME_STD), INCOME_MIN, INCOME_MAX)
            day_net += inc; mon.income += inc
            sa = round(SINKING_BASE + np.random.uniform(SINKING_DOWN, SINKING_UP), -1)
            reserve += sa; day_net -= sa; mon.sink_in += sa

        for dom, items in MONTHLY_BILLS.items():
            if d == dom:
                for name, amt in items:
                    day_net -= amt; mon.fixed += amt
                    p = classify_priority(name)
                    if p == "P0-P1": mon.p0p1 += amt
                    elif p == "P2": mon.p2 += amt
                    else: mon.p3 += amt

        if current in calendar:
            for name, amt in calendar[current]:
                p = classify_priority(name)
                if p == "P0-P1": mon.p0p1 += amt
                elif p == "P2": mon.p2 += amt
                else: mon.p3 += amt
                if reserve >= amt:
                    reserve -= amt; mon.sink_out += amt
                else:
                    sf = amt - reserve; reserve = 0
                    day_net -= sf; mon.sink_out += (amt - sf); mon.sink_fm += sf

        if current in luxury_dates:
            food = np.clip(np.random.normal(LUXURY_MEAN, LUXURY_STD), LUXURY_MIN, LUXURY_MAX)
            mon.food_lx += food; mon.lx_days += 1
        else:
            food = np.clip(np.random.normal(FRUGAL_MEAN, FRUGAL_STD), FRUGAL_MIN, FRUGAL_MAX)
            mon.food_fr += food; mon.fr_days += 1
        day_net -= food; mon.food += food; mon.p0p1 += food
        balance += day_net
        current += timedelta(days=1)

    if current_month_key is not None:
        monthly_log.append({
            "year": current_month_key[0], "month": current_month_key[1],
            "income": mon.income, "fixed_bills": mon.fixed,
            "food": round(mon.food, 0), "sinking_in": mon.sink_in,
            "sinking_out": mon.sink_out, "sinking_from_main": mon.sink_fm,
            "reserve_end": round(reserve, 0),
            "p0p1": round(mon.p0p1, 0), "p2": round(mon.p2, 0), "p3": round(mon.p3, 0),
            "net_after_reserve": round(mon.income - mon.fixed - mon.food - mon.sink_in, 0),
            "balance_end": round(balance, 0),
            "food_frugal": round(mon.food_fr, 0), "food_luxury": round(mon.food_lx, 0),
            "food_frugal_days": mon.fr_days, "food_luxury_days": mon.lx_days,
        })

    df = pd.DataFrame(monthly_log).head(SIM_MONTHS)
    df["label"] = df.apply(lambda r: f"{int(r.year)}-{int(r.month):02d}", axis=1)
    df["total_expense"] = df["fixed_bills"] + df["food"] + df["sinking_in"]
    df["net_total"] = df["income"] - df["total_expense"]
    df["month_index"] = range(len(df))
    return df, calendar, total_annual_sinking

# ============================================================
# ===== 图表生成函数 =====
# ============================================================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return b64

def make_stacked_bar(df, survival_monthly):
    """图表1: 60月支出堆叠条形图"""
    fig, ax = plt.subplots(figsize=(22, 10))
    x = np.arange(len(df))
    w = 0.75
    bt = np.zeros(len(df))
    ax.bar(x, df["fixed_bills"], w, bottom=bt, color='#2E86AB', label='刚性月付账单')
    bt += df["fixed_bills"].values
    ax.bar(x, df["food"], w, bottom=bt, color='#F18F01', label='每日吃饭')
    bt += df["food"].values
    ax.bar(x, df["sinking_in"], w, bottom=bt, color='#A23B72', label='蓄水池月缴(浮动)')
    bt += df["sinking_in"].values
    ax.bar(x, df["sinking_from_main"], w, bottom=bt, color='#D64933', label='蓄水池缺口(主账户补)')
    ax.plot(x, df["income"], color='#2A9D8F', linewidth=1.5, marker='o', markersize=2, label='月收入', zorder=5)
    ax.axhline(y=survival_monthly, color='#E76F51', linestyle='--', linewidth=1.5, alpha=0.7,
               label=f'极限生存线(仅P0+P1) {survival_monthly:,.0f}/月')
    for i, row in df.iterrows():
        if row["sinking_out"] > 5000:
            ax.annotate(f'[暴击]{row["sinking_out"]:,.0f}', xy=(i, bt[i]), fontsize=7,
                        color='#D64933', ha='center', fontweight='bold', xytext=(0,8), textcoords='offset points')
        elif row["sinking_out"] > 2000:
            ax.annotate(f'{row["sinking_out"]:,.0f}', xy=(i, bt[i]), fontsize=6, color='#A23B72',
                        ha='center', xytext=(0,5), textcoords='offset points')
    avg_exp = df["total_expense"].mean()
    ax.set_ylabel('金额(元)', fontsize=13)
    ax.set_title('未来60个月家庭月度支出构成 — 堆叠条形图', fontsize=16, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=9, ncol=2, framealpha=0.9)
    ax.set_xticks(x[::3])
    ax.set_xticklabels(df["label"].iloc[::3], rotation=45, fontsize=8)
    ax.set_ylim(0, 28000)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{v:,.0f}'))
    ax.grid(True, alpha=0.2, axis='y')
    ax.text(0.99, 0.97, f'月均总支出: {avg_exp:,.0f}\n极限生存线: {survival_monthly:,.0f}/月',
            transform=ax.transAxes, fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    return fig

def make_risk_chart(df, risk_months):
    """图表2: 可支配结余 + 余额走势"""
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(20,9), gridspec_kw={'height_ratios':[1.2,1]})
    x = np.arange(len(df))
    colors = []
    for i, row in df.iterrows():
        if row["net_after_reserve"] < 0: colors.append('#D64933')
        elif row["sinking_out"] > 5000: colors.append('#F18F01')
        elif row["sinking_from_main"] > 0: colors.append('#E9C46A')
        else: colors.append('#2E86AB')
    ax1.bar(x, df["net_after_reserve"], color=colors, alpha=0.85)
    ax1.axhline(y=0, color='black', linewidth=0.8)
    ax1.axhline(y=df["net_after_reserve"].mean(), color='#2A9D8F', linestyle='--', linewidth=1.2,
                label=f'月均可支配结余 {df["net_after_reserve"].mean():,.0f}')
    ax1.set_ylabel('可支配结余(元)', fontsize=12)
    ax1.set_title('月度可支配结余与风险标记', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.set_xticks(x[::3]); ax1.set_xticklabels(df["label"].iloc[::3], rotation=45, fontsize=8)
    ax1.grid(True, alpha=0.2, axis='y')
    for rm in risk_months:
        i = rm["month_index"]
        lbl = "X" if "赤字" in rm["risk_level"] or "双重" in rm["risk_level"] else "!"
        ax1.annotate(lbl, xy=(i, df["net_after_reserve"].iloc[i]),
                     fontsize=10, ha='center', fontweight='bold',
                     color='#D64933' if "赤字" in rm["risk_level"] else '#F18F01',
                     xytext=(0,-15), textcoords='offset points')
    ax2.fill_between(x, 0, df["balance_end"], color='#2E86AB', alpha=0.15, label='主账户余额')
    ax2.plot(x, df["balance_end"], color='#2E86AB', linewidth=1.5)
    nw = df["balance_end"] + df["reserve_end"]
    ax2.fill_between(x, df["balance_end"], nw, color='#A23B72', alpha=0.15, label='+蓄水池(净资产)')
    ax2.plot(x, nw, color='#A23B72', linewidth=1, linestyle='--')
    ax2.axhline(y=INITIAL_BALANCE, color='gray', linestyle=':', alpha=0.5, label=f'初始余额 {INITIAL_BALANCE:,}')
    ax2.axhline(y=0, color='#D64933', linewidth=1.5, linestyle='--', alpha=0.6, label='余额警戒线')
    ax2.set_ylabel('余额(元)', fontsize=12)
    ax2.set_title('账户余额与净资产走势', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9, ncol=3, loc='upper left')
    ax2.set_xticks(x[::3]); ax2.set_xticklabels(df["label"].iloc[::3], rotation=45, fontsize=8)
    ax2.grid(True, alpha=0.2)
    return fig

def make_structure_chart(df, annual):
    """图表3: 年度汇总 + 结构饼图"""
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(18,6.5))
    yr_list = annual["year"].astype(int).tolist()
    x_yr = np.arange(len(yr_list)); w = 0.25
    ax1.bar(x_yr-w, annual["income"], w, color='#2E86AB', alpha=0.85, label='年收入')
    ax1.bar(x_yr, annual["total_expense"], w, color='#D64933', alpha=0.85, label='年支出')
    ax1.bar(x_yr+w, annual["net_total"], w, color='#2A9D8F', alpha=0.85, label='年结余')
    for i in range(len(yr_list)):
        ax1.text(x_yr[i]+w, annual["net_total"].iloc[i]+3000, f'{annual["net_total"].iloc[i]:,.0f}',
                 ha='center', fontsize=8, fontweight='bold')
    ax1.set_title('年度收支对比', fontsize=13, fontweight='bold')
    ax1.set_xticks(x_yr); ax1.set_xticklabels(yr_list); ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.2, axis='y')
    labels = ['刚性月付', '每日吃饭', '蓄水池支出']
    vals = [df["fixed_bills"].sum(), df["food"].sum(), df["sinking_out"].sum()]
    colors_pie = ['#2E86AB','#F18F01','#A23B72']
    if df["sinking_from_main"].sum() > 0:
        labels.append('蓄水池缺口')
        vals.append(df["sinking_from_main"].sum())
        colors_pie.append('#D64933')
    labels = [f'{l}\n{v/len(df):,.0f}/月' for l,v in zip(labels,vals)]
    wedges, texts, autotexts = ax2.pie(vals, labels=labels, colors=colors_pie,
                                        autopct='%1.1f%%', startangle=90,
                                        explode=[0.02]*len(vals))
    for t in autotexts: t.set_fontsize(10); t.set_fontweight('bold')
    ax2.set_title(f'60个月总支出构成 ({sum(vals):,.0f})', fontsize=13, fontweight='bold')
    return fig

# ============================================================
# ===== HTML 报告生成 =====
# ============================================================
def generate_report():
    print("=" * 50)
    print("  家庭预算模型 — 报告生成中...")
    print("=" * 50)

    df, calendar, total_annual = run_simulation()
    expense_df = _make_expense_df()

    # -- 基础指标 --
    avg_inc = df["income"].mean()
    avg_exp = df["total_expense"].mean()
    avg_net = df["net_total"].mean()
    savings_rate = avg_net / avg_inc * 100
    avg_sink_in = df["sinking_in"].mean()
    avg_sink_out = df["sinking_out"].mean()

    # 极限生存线
    p3_monthly = sum(amt for items in MONTHLY_BILLS.values() for _, amt in items
                     if classify_priority(_[-1]) == "P3") / len(MONTHLY_BILLS)  # approximate
    # 更准确的计算：P3 月付总额
    p3_mo = sum(amt for dom, items in MONTHLY_BILLS.items() for name, amt in items
                if classify_priority(name) == "P3")
    p2_annual = sum(amt * (12 / interval) for _, amt, interval, _ in CYCLIC_EVENTS)
    p2_mo_eq = p2_annual / 12
    survival_mo = df["fixed_bills"].mean() + df["food"].mean() + avg_sink_in - p2_mo_eq - p3_mo
    survival_rate = survival_mo / avg_inc * 100

    # -- 风险月识别 --
    risk_months = []
    for i, row in df.iterrows():
        level = "安全"; reasons = []
        if row["net_after_reserve"] < 0:
            level = "⚠️ 赤字"; reasons.append(f"可支配结余 {row['net_after_reserve']:,.0f}")
        if row["sinking_from_main"] > 0:
            level = ("🔴 双重风险" if level == "⚠️ 赤字" else "⚡ 蓄水池不足")
            reasons.append(f"蓄水池缺口 {row['sinking_from_main']:,.0f}")
        if row["sinking_out"] > 5000:
            if level == "安全": level = "💥 大额支出"
            reasons.append(f"蓄水池支出 {row['sinking_out']:,.0f}")
        if row["balance_end"] < INITIAL_BALANCE * 0.2:
            if level == "安全": level = "⚠️ 低余额"
            reasons.append(f"月末余额仅 {row['balance_end']:,.0f}")
        if level != "安全":
            dt_key = datetime(int(row["year"]), int(row["month"]), 1)
            items_str = " | ".join(f"{n} {a:,.0f}" for n,a in calendar.get(dt_key,[]))
            risk_months.append({
                "label": row["label"], "month_index": i, "risk_level": level,
                "reasons": " | ".join(reasons), "net_after_reserve": row["net_after_reserve"],
                "net_total": row["net_total"], "sinking_out": row["sinking_out"],
                "sinking_from_main": row["sinking_from_main"],
                "balance_end": row["balance_end"], "reserve_end": row["reserve_end"],
                "sinking_items": items_str,
            })

    # 年度
    annual = df.groupby("year").agg(
        income=("income","sum"), total_expense=("total_expense","sum"),
        net_total=("net_total","sum"), sinking_in=("sinking_in","sum"),
        sinking_out=("sinking_out","sum"),
        end_balance=("balance_end","last"), end_reserve=("reserve_end","last"),
    ).reset_index()

    final_nw = df["balance_end"].iloc[-1] + df["reserve_end"].iloc[-1]
    reserve_min = df["reserve_end"].min()

    # 计算机课月份
    comp_months = []
    for dt_key, items in calendar.items():
        for n, a in items:
            if "计算机" in n and datetime(START_YEAR,START_MONTH,1) <= dt_key:
                comp_months.append(dt_key.strftime('%Y-%m'))

    # 暴击月
    spike_months = df[df["sinking_out"] > 5000]
    spike_list = []
    for _, row in spike_months.iterrows():
        dt_key = datetime(int(row["year"]), int(row["month"]), 1)
        its = " + ".join(f"{n}({a:,.0f})" for n,a in calendar.get(dt_key,[]))
        spike_list.append({"label":row["label"], "sinking_out":row["sinking_out"],
                           "items":its, "net":row["net_after_reserve"],
                           "balance":row["balance_end"]})

    severe = sum(1 for r in risk_months if "双重" in r["risk_level"])
    warning_n = sum(1 for r in risk_months if "赤字" in r["risk_level"] or "蓄水池不足" in r["risk_level"])

    print(f"  模拟: {df['label'].iloc[0]} ~ {df['label'].iloc[-1]} ({len(df)}个月)")
    print(f"  月均收入: {avg_inc:,.0f} | 等效月成本: {avg_exp:,.0f}")
    print(f"  月均结余: {avg_net:,.0f} ({savings_rate:.1f}%) | 极限生存线: {survival_mo:,.0f}/月")
    print(f"  风险月: {len(risk_months)}/{len(df)} | 蓄水池覆盖率: {avg_sink_in*12/total_annual*100:.0f}%")
    print("  生成图表...")

    # -- 生成图表 --
    fig1 = make_stacked_bar(df, survival_mo)
    fig2 = make_risk_chart(df, risk_months)
    fig3 = make_structure_chart(df, annual)
    b64_1 = fig_to_b64(fig1)
    b64_2 = fig_to_b64(fig2)
    b64_3 = fig_to_b64(fig3)

    print("  生成HTML报告...")

    # -- HTML --
    # 支出目录表格
    exp_table_rows = ""
    for _, r in expense_df.iterrows():
        exp_table_rows += f"<tr><td>{r['支出项目']}</td><td>{r['原金额']:,.0f}</td><td>{r['支付周期']}</td><td>{r['月均摊']:,.0f}</td></tr>"

    # 年度表格
    ann_table_rows = ""
    for _, r in annual.iterrows():
        tag = 'tag-green' if r['net_total']>0 else 'tag-red'
        ann_table_rows += f"""<tr>
          <td><strong>{int(r['year'])}</strong></td>
          <td>{r['income']:,.0f}</td><td>{r['total_expense']:,.0f}</td>
          <td><span class="tag {tag}">{r['net_total']:,.0f}</span></td>
          <td>{r['sinking_in']:,.0f}</td><td>{r['sinking_out']:,.0f}</td>
          <td>{r['end_balance']:,.0f}</td><td>{r['end_reserve']:,.0f}</td></tr>"""

    # 风险表格
    risk_table_rows = ""
    for rm in risk_months:
        rc = "risk-red" if "双重" in rm["risk_level"] or "赤字" in rm["risk_level"] else "risk-orange"
        tag_c = "tag-red" if "赤字" in rm["risk_level"] or "双重" in rm["risk_level"] else "tag-orange"
        risk_table_rows += f"""<tr class="{rc}">
          <td><strong>{rm['label']}</strong></td>
          <td><span class="tag {tag_c}">{rm['risk_level']}</span></td>
          <td>{rm['reasons']}</td>
          <td>{rm['net_after_reserve']:,.0f}</td><td>{rm['net_total']:,.0f}</td>
          <td>{rm['sinking_out']:,.0f}</td><td>{rm['balance_end']:,.0f}</td>
          <td style="font-size:0.85em;">{rm['sinking_items']}</td></tr>"""

    # 暴击表格
    spike_rows = ""
    for sm in spike_list:
        spike_rows += f"""<tr class="risk-orange">
          <td><strong>{sm['label']}</strong></td>
          <td><span class="tag tag-red">{sm['sinking_out']:,.0f}</span></td>
          <td>{sm['items']}</td>
          <td>{sm['net']:,.0f}</td><td>{sm['balance']:,.0f}</td></tr>"""

    comp_str = ", ".join(comp_months) if comp_months else "无"

    # 费用变更说明
    param_details = f"""
    <table style="margin-top:10px;">
      <tr><th>参数类别</th><th>当前设定</th></tr>
      <tr><td>收入模型</td><td>N({INCOME_MEAN}, {INCOME_STD}²), 截断[{INCOME_MIN},{INCOME_MAX}], 每月{PAYDAY}日到账</td></tr>
      <tr><td>吃饭模型</td><td>节约日 N({FRUGAL_MEAN},{FRUGAL_STD}²)[{FRUGAL_MIN},{FRUGAL_MAX}] + 奢侈日 N({LUXURY_MEAN},{LUXURY_STD}²)[{LUXURY_MIN},{LUXURY_MAX}], 周均{LUXURY_PER_WEEK_MEAN}次</td></tr>
      <tr><td>蓄水池月缴</td><td>{SINKING_BASE} + uniform({SINKING_DOWN}, {SINKING_UP}) → [{SINKING_BASE+SINKING_DOWN}, {SINKING_BASE+SINKING_UP}]</td></tr>
      <tr><td>模拟设定</td><td>{START_YEAR}年{START_MONTH}月起 {SIM_MONTHS}个月, 初始余额 {INITIAL_BALANCE:,}, 随机种子{RANDOM_SEED}</td></tr>
    </table>
    """

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>家庭收支预测与财务规划压力测试报告</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background:#f5f7fa; color:#2c3e50; line-height:1.7; }}
  .container {{ max-width:1100px; margin:0 auto; padding:20px; }}
  .header {{ background:linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); color:#fff; padding:40px; border-radius:12px; margin-bottom:30px; text-align:center; }}
  .header h1 {{ font-size:2em; margin-bottom:8px; }}
  .header .subtitle {{ font-size:1.1em; opacity:0.85; }}
  .header .meta {{ margin-top:15px; font-size:0.9em; opacity:0.7; }}
  .card {{ background:#fff; border-radius:12px; padding:28px; margin-bottom:24px; box-shadow:0 2px 12px rgba(0,0,0,0.06); }}
  .card h2 {{ font-size:1.4em; margin-bottom:20px; padding-bottom:10px; border-bottom:3px solid #2E86AB; }}
  .card h3 {{ font-size:1.15em; margin:18px 0 10px; color:#2E86AB; }}
  .metrics-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:18px; }}
  .metric {{ background:#f8f9fa; border-radius:10px; padding:20px; text-align:center; border-left:5px solid #2E86AB; }}
  .metric.danger {{ border-left-color:#D64933; }}
  .metric.warning {{ border-left-color:#F18F01; }}
  .metric.success {{ border-left-color:#2A9D8F; }}
  .metric .value {{ font-size:1.8em; font-weight:700; margin:8px 0; }}
  .metric .label {{ font-size:0.9em; color:#6c757d; }}
  .metric .sub {{ font-size:0.8em; color:#adb5bd; margin-top:4px; }}
  table {{ width:100%; border-collapse:collapse; font-size:0.94em; margin:12px 0; }}
  th {{ background:#2E86AB; color:#fff; padding:12px 10px; text-align:left; font-weight:600; }}
  td {{ padding:10px; border-bottom:1px solid #e9ecef; }}
  tr:hover {{ background:#f8f9fa; }}
  .risk-red {{ background:#fff5f5; }} .risk-orange {{ background:#fffaf0; }} .risk-yellow {{ background:#fffff0; }}
  .tag {{ display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.82em; font-weight:600; }}
  .tag-red {{ background:#fee; color:#D64933; }} .tag-orange {{ background:#fff3e0; color:#F18F01; }}
  .tag-green {{ background:#e8f5e9; color:#2A9D8F; }} .tag-blue {{ background:#e3f2fd; color:#2E86AB; }}
  .chart-container {{ text-align:center; margin:16px 0; }}
  .chart-container img {{ max-width:100%; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1); }}
  .alert {{ padding:16px 20px; border-radius:8px; margin:12px 0; }}
  .alert-danger {{ background:#fff5f5; border:1px solid #fecaca; color:#991b1b; }}
  .alert-warning {{ background:#fffaf0; border:1px solid #fed7aa; color:#92400e; }}
  .alert-info {{ background:#eff6ff; border:1px solid #bfdbfe; color:#1e40af; }}
  .alert-success {{ background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; }}
  .rec-list {{ list-style:none; padding:0; }}
  .rec-list li {{ padding:12px 16px; margin:8px 0; background:#f8f9fa; border-radius:8px; border-left:4px solid #2E86AB; }}
  .rec-list li strong {{ color:#2E86AB; }}
  .footer {{ text-align:center; padding:20px; color:#adb5bd; font-size:0.85em; }}
  @media print {{ body {{ background:#fff; }} .card {{ box-shadow:none; border:1px solid #e9ecef; page-break-inside:avoid; }} }}
</style>
</head>
<body><div class="container">

<div class="header">
  <h1>未来60个月家庭收支预测与财务规划压力测试报告</h1>
  <div class="subtitle">基于 Sinking Fund 浮动蓄水池模型 | 单文件报告生成器</div>
  <div class="meta">报告周期: {df['label'].iloc[0]} ~ {df['label'].iloc[-1]} ({len(df)}个月) | 生成: {NOW} | 随机种子: {RANDOM_SEED}</div>
</div>

<!-- ===== 0. 参数设定 ===== -->
<div class="card">
  <h2>参数设定（可在脚本顶部修改后重新生成）</h2>
  {param_details}
  <h3 style="margin-top:16px;">支出目录</h3>
  <table>
    <thead><tr><th>支出项目</th><th>原金额</th><th>支付周期</th><th>月均摊</th></tr></thead>
    <tbody>{exp_table_rows}</tbody>
  </table>
</div>

<!-- ===== 1. 核心指标 ===== -->
<div class="card">
  <h2>一、核心指标面板</h2>
  <div class="metrics-grid">
    <div class="metric"><div class="label">月均收入</div><div class="value">{avg_inc:,.0f}</div><div class="sub">N({INCOME_MEAN},{INCOME_STD}²)/每月{PAYDAY}日到账</div></div>
    <div class="metric"><div class="label">等效月总成本</div><div class="value">{avg_exp:,.0f}</div><div class="sub">刚性月付+吃饭+蓄水池缴纳</div></div>
    <div class="metric success"><div class="label">月均结余</div><div class="value">{avg_net:,.0f}</div><div class="sub">结余率 {savings_rate:.1f}%</div></div>
    <div class="metric danger"><div class="label">极限生存线 (仅P0+P1)</div><div class="value">{survival_mo:,.0f}/月</div><div class="sub">占收入 {survival_rate:.1f}% | 年需 {survival_mo*12:,.0f}</div></div>
    <div class="metric warning"><div class="label">蓄水池年均缺口</div><div class="value">{total_annual - avg_sink_in*12:,.0f}/年</div><div class="sub">年付需求 {total_annual:,.0f} vs 年缴 {avg_sink_in*12:,.0f}</div></div>
    <div class="metric"><div class="label">最终净资产</div><div class="value">{final_nw:,.0f}</div><div class="sub">主账户 {df['balance_end'].iloc[-1]:,.0f} + 蓄水池 {df['reserve_end'].iloc[-1]:,.0f}</div></div>
  </div>
  <div class="alert alert-info" style="margin-top:18px;">
    <strong>极限生存线定义:</strong> 仅保留P0(不可违约)+P1(合同约束/基本生存)。剔除P2(游泳课/美术课/计算机课)和P3(营养品/保洁)。当前生存线 {survival_mo:,.0f}/月，意味着即使砍掉所有非生存支出，仍有约 {avg_inc-survival_mo:,.0f}/月的安全垫。
  </div>
</div>

<!-- ===== 2. 堆叠条形图 ===== -->
<div class="card">
  <h2>二、60月支出构成 — 堆叠条形图</h2>
  <div class="chart-container"><img src="data:image/png;base64,{b64_1}" alt="堆叠条形图"></div>
  <div class="alert alert-warning">
    <strong>图表解读:</strong> 红色柱段=蓄水池余额不足、从主账户额外补贴。柱顶接近或超过绿色收入线时该月现金流极度紧张。
    [暴击]标注=单月蓄水池支出>5,000。灰色虚线=极限生存线(仅P0+P1)。
  </div>
</div>

<!-- ===== 3. 风险图 ===== -->
<div class="card">
  <h2>三、月度可支配结余与账户余额走势</h2>
  <div class="chart-container"><img src="data:image/png;base64,{b64_2}" alt="风险分析图"></div>
</div>

<!-- ===== 4. 年度+结构 ===== -->
<div class="card">
  <h2>四、年度汇总与支出结构</h2>
  <div class="chart-container"><img src="data:image/png;base64,{b64_3}" alt="结构图"></div>
  <h3>年度数据明细</h3>
  <table>
    <thead><tr><th>年份</th><th>年收入</th><th>年支出</th><th>净结余</th><th>蓄水池缴</th><th>蓄水池支</th><th>年终主账户</th><th>年终蓄水池</th></tr></thead>
    <tbody>{ann_table_rows}</tbody>
  </table>
</div>

<!-- ===== 5. 风险预警 ===== -->
<div class="card">
  <h2>五、风险预警 — 压力测试</h2>
  <div class="metrics-grid" style="margin-bottom:20px;">
    <div class="metric danger"><div class="label">严重风险 (双重)</div><div class="value">{severe}</div></div>
    <div class="metric warning"><div class="label">警告 (赤字/蓄水池不足)</div><div class="value">{warning_n}</div></div>
    <div class="metric"><div class="label">风险月总数 / 总月数</div><div class="value">{len(risk_months)}/{len(df)}</div><div class="sub">占比 {len(risk_months)/len(df)*100:.1f}%</div></div>
  </div>
  <h3>完整风险月清单</h3>
  <table>
    <thead><tr><th>月份</th><th>风险等级</th><th>风险原因</th><th>可支配结余</th><th>月净结余</th><th>蓄水池支出</th><th>月末余额</th><th>触发事件</th></tr></thead>
    <tbody>{risk_table_rows}</tbody>
  </table>

  <h3>暴击月 (单月蓄水池支出 >5,000)</h3>
  <div class="alert alert-danger">这些月份是大型支出集中爆发期，蓄水池大概率不足，需提前从主账户准备资金。</div>
  <table>
    <thead><tr><th>月份</th><th>蓄水池支出</th><th>触发项目</th><th>当月可支配结余</th><th>月末余额</th></tr></thead>
    <tbody>{spike_rows}</tbody>
  </table>

  <h3>最大单项风险: 计算机课 (16,000/16月)</h3>
  <div class="alert alert-danger">
    <strong>缴费月份:</strong> {comp_str}<br>
    计算机课是单笔最大支出(相当于 {16000/avg_inc:.1f} 个月的全部收入)。无充足蓄水池储备时，这些月份必然动用主账户余额或其他积蓄。
  </div>
</div>

<!-- ===== 6. 结论与建议 ===== -->
<div class="card">
  <h2>六、结论与执行建议</h2>
  <h3>6.1 核心结论</h3>
  <ol>
    <li><strong>收支结构基本健康，但蓄水池严重不足。</strong>月均收入 {avg_inc:,.0f}，等效月成本 {avg_exp:,.0f}，结余率 {savings_rate:.1f}%。蓄水池覆盖率仅 {avg_sink_in*12/total_annual*100:.0f}%。</li>
    <li><strong>大型支出月是主要风险源。</strong>计算机课(16,000/16月)和车险+多项目叠加月(9月)是两大暴击来源。蓄水池在暴击月后通常降至危险低水位。</li>
    <li><strong>极限生存线 {survival_mo:,.0f}/月。</strong>砍掉P2(兴趣班)和P3(营养品/保洁)后月耗仅占收入 {survival_rate:.1f}%，基础生存支出可控。</li>
    <li><strong>5年净资产增长 {final_nw-INITIAL_BALANCE:,.0f}。</strong>从 {INITIAL_BALANCE:,} 增至 {final_nw:,.0f}，年均约 {(final_nw-INITIAL_BALANCE)/5:,.0f}。</li>
  </ol>

  <h3>6.2 执行建议</h3>
  <ul class="rec-list">
    <li><strong>建议一: 建立"双账户"资金缓冲机制。</strong>将月均结余的一部分(建议1,000~1,500/月)定向划入蓄水池，暴击月前3-4月提前预警并加速储蓄。</li>
    <li><strong>建议二: 计算机课单独备款。</strong>16,000/16月≈1,000/月。缴费前3月开始每月额外存5,000+。缴费月: {comp_str}。</li>
    <li><strong>建议三: 关注9月多重重叠。</strong>车险(4,500)+校服(1,000)+游泳课(~3,600)+美术课(~1,400)合计约10,500+，建议7-8月减少非必要支出集中蓄水。</li>
    <li><strong>建议四: 减少奢侈日频率。</strong>每周减少1次奢侈日(2次→1次)约可节省 {(LUXURY_MEAN-FRUGAL_MEAN)*4.33:,.0f}/月。</li>
    <li><strong>建议五: P3弹性支出作应急调节阀。</strong>营养品+保洁900/月，风险月前压缩30-50%可释放270~450/月缓冲。</li>
  </ul>

  <h3>6.3 关键风险时间轴</h3>
  <table>
    <thead><tr><th>时间窗口</th><th>风险类型</th><th>原因</th><th>建议动作</th></tr></thead>
    <tbody>
      <tr class="risk-orange"><td>每年1月</td><td>中风险</td><td>过年后余额偏紧+开学前准备</td><td>12月预留3,000+缓冲</td></tr>
      <tr class="risk-red"><td>每年8-9月</td><td>高风险</td><td>车险+游泳课+美术课+校服+计算机课可能叠加</td><td>7月前确保蓄水池>10,000</td></tr>
      <tr class="risk-red"><td>计算机课月(16月周期)</td><td>极端</td><td>单笔16,000</td><td>提前3月额外储蓄</td></tr>
    </tbody>
  </table>
</div>

<div class="footer">
  <p>家庭预算模型 v3 自动生成 | 随机种子 {RANDOM_SEED} | 生成时间: {NOW}</p>
  <p style="margin-top:4px;">修改脚本顶部参数后重新运行即可更新报告</p>
</div>

</div></body></html>"""

    report_path = os.path.join(DESKTOP, '家庭收支预测报告.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n{'='*50}")
    print(f"  报告已保存: {report_path}")
    print(f"  文件大小: {os.path.getsize(report_path)/1024:.0f} KB")
    print(f"{'='*50}")

    return report_path

# ============================================================
# ===== 主入口 =====
# ============================================================
if __name__ == "__main__":
    import io
    generate_report()
