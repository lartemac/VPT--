#!/usr/bin/env python3
"""
家庭月收支数学模型 v3 — Sinking Fund 版
- 支出 DataFrame：priority + pay_period + monthly_amount
- 每月自动划拨 ¥1,800 到 Yearly_Reserve（年付准备金）
- 年付账单从 Yearly_Reserve 扣款，不冲击当月现金流
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================
# 基础参数
# ============================================================
INCOME_MEAN = 18000
INCOME_STD = 1000
INCOME_MIN = 14000
INCOME_MAX = 22000
PAYDAY = 20

# ---- 每日吃饭：双模模型（节约日 / 奢侈日） ----
FRUGAL_MEAN = 200      # 节约日均值
FRUGAL_STD = 30        # 节约日标准差
FRUGAL_MIN = 120       # 节约日下限
FRUGAL_MAX = 300       # 节约日上限

LUXURY_MEAN = 400      # 奢侈日均值
LUXURY_STD = 60        # 奢侈日标准差
LUXURY_MIN = 300       # 奢侈日下限
LUXURY_MAX = 600       # 奢侈日上限

# 每周奢侈日次数: N(2, 0.5), 截断 [1, 3]
LUXURY_PER_WEEK_MEAN = 2
LUXURY_PER_WEEK_STD = 0.5

# ---- 蓄水池月缴（随机浮动） ----
# 基准 1800，上浮最多 200，下浮最多 1000 → 范围 [800, 2000]
SINKING_BASE = 1800
SINKING_UP = 200       # 上浮上限
SINKING_DOWN = -1000    # 下浮下限
# 每月实际: 1800 + np.random.uniform(-1000, 200)

START_YEAR = 2026
START_MONTH = 6
SIM_YEARS = 5
RANDOM_SEED = 42

INITIAL_BALANCE = 50000
INITIAL_RESERVE = 0        # 蓄水池初始余额

# ============================================================
# 支出目录 DataFrame
# ============================================================
data = [
    # (item_name, raw_amount, pay_period, monthly_amount, priority)
    ("房贷",              2000,  "monthly",  2000.0, "P0-不可违约"),
    ("办公室月租",         1300,  "monthly",  1300.0, "P1-合同约束"),
    ("车位月租",           1000,  "monthly",  1000.0, "P1-合同约束"),
    ("物管费",             330,   "monthly",   330.0, "P1-合同约束"),
    ("水电燃气网络手机",   1000,  "monthly",  1000.0, "P1-基本生存"),
    ("过路费",             600,   "monthly",   600.0, "P1-基本生存"),
    ("车辆保养均摊",        325,  "monthly",   325.0, "P1-基本生存"),
    ("每日吃饭(双模)",     7800,  "daily",    7800.0, "P1-基本生存"),
    ("车辆保险(每年9月)",   4500,  "yearly",    375.0, "P1-刚性年付"),
    ("游泳课(每10月)",     3600,  "10-month",  360.0, "P2-发展可控"),
    ("美术课(每4月)",      1400,  "4-month",   350.0, "P2-发展可控"),
    ("计算机课(每16月)",   16000, "16-month", 1000.0, "P2-发展可控"),
    ("学校餐费(×4/年)",    2400,  "yearly",    200.0, "P2-发展可控"),
    ("校服(每年9月)",      1000,  "yearly",     83.3, "P2-发展可控"),
    ("牛奶钙片等营养品",    600,  "monthly",   600.0, "P3-弹性刚性"),
    ("保洁用品",            300,  "monthly",   300.0, "P3-弹性刚性"),
]

df_expense = pd.DataFrame(data, columns=[
    "item_name", "raw_amount", "pay_period", "monthly_amount", "priority"
])

# ============================================================
# 每月固定账单（从主账户扣款）
# ============================================================
MONTHLY_BILLS = {
    1:  [("房贷", 2000), ("办公室月租", 1300), ("车位月租", 1000), ("物管费", 330)],
    5:  [("过路费", 600), ("牛奶钙片等营养品", 600), ("保洁用品", 300), ("车辆保养均摊", 325)],
    15: [("水电燃气网络手机", 1000)],
}

# ============================================================
# 蓄水池事件日历（从 Yearly_Reserve 扣款）
# 自动根据周期生成完整时间表
# ============================================================

# 固定在特定月份的年付事件: {月: [(名称, 金额)]}
YEARLY_SINKING_EVENTS = {
    4:  [("学校餐费(春期中)", 600)],
    6:  [("学校餐费(春期末)", 600)],
    9:  [("车辆保险", 4500), ("校服", 1000)],
    10: [("学校餐费(秋期中)", 600)],
    12: [("学校餐费(秋期末)", 600)],
}

# 自定义周期事件: [(名称, 金额, 周期间隔月数, 首次缴费日期)]
CYCLIC_EVENTS = [
    ("游泳课",    3600,  10, datetime(2026, 7, 1)),
    ("计算机课",  16000, 16, datetime(2026, 8, 1)),
    ("美术课",    1400,  4,  datetime(2026, 8, 1)),
]

def build_sinking_calendar(start_dt, end_dt, yearly_events, cyclic_events):
    """预生成完整的蓄水池支出日历 {date: [(name, amount)]}"""
    cal = defaultdict(list)

    # 固定年付事件
    y_start, y_end = start_dt.year, end_dt.year
    for yr in range(y_start, y_end + 1):
        for month, items in yearly_events.items():
            d = datetime(yr, month, 1)
            if start_dt <= d <= end_dt:
                for name, amt in items:
                    cal[d].append((name, amt))

    # 自定义周期事件
    for name, amt, interval, next_date in cyclic_events:
        d = next_date
        while d <= end_dt:
            if d >= start_dt:
                cal[d].append((name, amt))
            # 推进到下个周期
            new_month = d.month + interval
            new_year = d.year + (new_month - 1) // 12
            new_month = (new_month - 1) % 12 + 1
            d = datetime(new_year, new_month, 1)

    return dict(sorted(cal.items()))  # 按日期排序

# ============================================================
# 计算蓄水池年化总需求
# ============================================================
_yearly_total = sum(amt for items in YEARLY_SINKING_EVENTS.values() for _, amt in items)
_cyclic_annual = sum(amt * (12 / interval) for _, amt, interval, _ in CYCLIC_EVENTS)
TOTAL_ANNUAL_SINKING = _yearly_total + _cyclic_annual  # 蓄水池年化总需求
RECOMMENDED_SINKING_RATE = TOTAL_ANNUAL_SINKING / 12    # 推荐月缴额

# ============================================================
# 初始化和随机种子
# ============================================================
np.random.seed(RANDOM_SEED)

start_date = datetime(START_YEAR, START_MONTH, 1)
total_days = SIM_YEARS * 365 + 60
end_date = start_date + timedelta(days=total_days)

# 预生成蓄水池支出日历
SINKING_CALENDAR = build_sinking_calendar(
    start_date, end_date, YEARLY_SINKING_EVENTS, CYCLIC_EVENTS
)

# ============================================================
# 逐日模拟
# ============================================================
balance = INITIAL_BALANCE        # 主账户余额
reserve = INITIAL_RESERVE        # Yearly_Reserve 蓄水池

records = []          # 每日记录
monthly_log = []      # 月度汇总日志

current = start_date
current_month_key = None

# 累计月度变量
mon_income = 0
mon_fixed_bills = 0
mon_food = 0
mon_food_frugal = 0
mon_food_luxury = 0
mon_food_frugal_days = 0
mon_food_luxury_days = 0
mon_sinking_in = 0
mon_sinking_out = 0
mon_reserve_end = INITIAL_RESERVE

# 奢侈日调度：按周生成
luxury_dates = set()         # 当前周的奢侈日日期
current_week = None          # 当前 ISO 周编号

while current <= end_date:
    d = current.day
    m = current.month
    y = current.year
    mk = (y, m)

    # 月初切换
    if mk != current_month_key:
        # 保存上月
        if current_month_key is not None:
            monthly_log.append({
                "year": current_month_key[0],
                "month": current_month_key[1],
                "income": mon_income,
                "fixed_bills": mon_fixed_bills,
                "food": round(mon_food, 0),
                "food_frugal": round(mon_food_frugal, 0),
                "food_luxury": round(mon_food_luxury, 0),
                "food_frugal_days": mon_food_frugal_days,
                "food_luxury_days": mon_food_luxury_days,
                "sinking_in": mon_sinking_in,
                "sinking_out": mon_sinking_out,
                "reserve_end": round(mon_reserve_end, 0),
                "net_after_reserve": round(mon_income - mon_fixed_bills - mon_food - mon_sinking_in, 0),
                "balance_end": round(balance, 0),
            })
        current_month_key = mk
        mon_income = 0
        mon_fixed_bills = 0
        mon_food = 0
        mon_food_frugal = 0
        mon_food_luxury = 0
        mon_food_frugal_days = 0
        mon_food_luxury_days = 0
        mon_sinking_in = 0
        mon_sinking_out = 0

    # 每周奢侈日调度（ISO 周切换时重新生成）
    iso_week = current.isocalendar()[1]  # (year, week, weekday)
    if iso_week != current_week:
        current_week = iso_week
        n_luxury = int(np.clip(np.random.normal(LUXURY_PER_WEEK_MEAN, LUXURY_PER_WEEK_STD), 1, 3))
        # 从本周7天中随机选 n_luxury 天
        week_start = current - timedelta(days=current.weekday())  # 周一
        week_days = [week_start + timedelta(days=i) for i in range(7)]
        chosen = np.random.choice(week_days, size=n_luxury, replace=False)
        luxury_dates = set(chosen)

    day_net = 0
    notes = []

    # ---- 收入 ----
    if d == PAYDAY:
        raw = np.random.normal(INCOME_MEAN, INCOME_STD)
        inc = np.clip(raw, INCOME_MIN, INCOME_MAX)
        day_net += inc
        mon_income += inc
        notes.append(f"+收入 {inc:.0f}")

        # ---- Sinking Fund: 发薪日浮动划拨 ----
        sinking_amt = round(SINKING_BASE + np.random.uniform(SINKING_DOWN, SINKING_UP), -1)  # 取整到10元
        reserve += sinking_amt
        day_net -= sinking_amt
        mon_sinking_in += sinking_amt
        notes.append(f"→蓄水池 {sinking_amt:.0f}")

    # ---- 每月固定账单 ----
    for dom, items in MONTHLY_BILLS.items():
        if d == dom:
            for name, amt in items:
                day_net -= amt
                mon_fixed_bills += amt
                notes.append(f"-{name} {amt}")

    # ---- 蓄水池扣款：从预生成日历中查找 ----
    if current in SINKING_CALENDAR:
        for name, amt in SINKING_CALENDAR[current]:
            if reserve >= amt:
                reserve -= amt
                mon_sinking_out += amt
                notes.append(f"★{name}(蓄水池) {amt}")
            else:
                # 蓄水池不足，缺口从主账户补
                shortfall = amt - reserve
                reserve = 0
                day_net -= shortfall
                mon_sinking_out += (amt - shortfall)
                notes.append(f"★{name}(蓄水池不足! 主账户补{shortfall:.0f}) {amt}")

    # ---- 每日吃饭（双模：节约日/奢侈日） ----
    if current in luxury_dates:
        raw_food = np.random.normal(LUXURY_MEAN, LUXURY_STD)
        food = np.clip(raw_food, LUXURY_MIN, LUXURY_MAX)
        mon_food_luxury += food
        mon_food_luxury_days += 1
    else:
        raw_food = np.random.normal(FRUGAL_MEAN, FRUGAL_STD)
        food = np.clip(raw_food, FRUGAL_MIN, FRUGAL_MAX)
        mon_food_frugal += food
        mon_food_frugal_days += 1
    day_net -= food
    mon_food += food

    # ---- 更新余额 ----
    balance += day_net
    mon_reserve_end = reserve

    records.append((current, day_net, balance, reserve))

    current += timedelta(days=1)

# 保存最后一个月
if current_month_key is not None:
    monthly_log.append({
        "year": current_month_key[0],
        "month": current_month_key[1],
        "income": mon_income,
        "fixed_bills": mon_fixed_bills,
        "food": round(mon_food, 0),
        "sinking_in": mon_sinking_in,
        "sinking_out": mon_sinking_out,
        "reserve_end": round(mon_reserve_end, 0),
        "net_after_reserve": round(mon_income - mon_fixed_bills - mon_food - mon_sinking_in, 0),
        "balance_end": round(balance, 0),
    })

df_monthly = pd.DataFrame(monthly_log)

# ============================================================
# 计算月度汇总
# ============================================================
df_monthly["total_expense"] = (df_monthly["fixed_bills"] + df_monthly["food"]
                               + df_monthly["sinking_in"])
df_monthly["net_total"] = df_monthly["income"] - df_monthly["total_expense"]
df_monthly["label"] = df_monthly.apply(lambda r: f"{int(r.year)}-{int(r.month):02d}", axis=1)

# 年度汇总
annual_summary = df_monthly.groupby("year").agg(
    income=("income", "sum"),
    fixed_bills=("fixed_bills", "sum"),
    food=("food", "sum"),
    sinking_in=("sinking_in", "sum"),
    sinking_out=("sinking_out", "sum"),
    net_total=("net_total", "sum"),
).reset_index()
annual_summary["total_expense"] = (annual_summary["fixed_bills"]
                                   + annual_summary["food"]
                                   + annual_summary["sinking_in"])

# ============================================================
# 终端输出
# ============================================================
print("=" * 75)
print(f"  家庭收支模型 v3 — Sinking Fund 版")
print(f"  模拟跨度: {df_monthly['label'].iloc[0]} ~ {df_monthly['label'].iloc[-1]}")
print("=" * 75)

print(f"\n  📋 支出目录 (DataFrame)")
print("  " + "-" * 70)
print(f"  {'项目':<22s} {'原金额':>8s} {'周期':>10s} {'月均摊':>8s} {'优先级':<16s}")
print("  " + "-" * 70)
for _, row in df_expense.iterrows():
    print(f"  {row['item_name']:<22s} ¥{row['raw_amount']:>6.0f}  {row['pay_period']:>10s}  "
          f"¥{row['monthly_amount']:>6.0f}  {row['priority']:<16s}")
print("  " + "-" * 70)

monthly_sum = df_expense[df_expense["pay_period"] == "monthly"]["monthly_amount"].sum()
# ---- 预计算月均统计 ----
avg_inc = df_monthly["income"].mean()
avg_bills = df_monthly["fixed_bills"].mean()
avg_food = df_monthly["food"].mean()
avg_food_frugal = df_monthly["food_frugal"].mean()
avg_food_luxury = df_monthly["food_luxury"].mean()
avg_frugal_days = df_monthly["food_frugal_days"].mean()
avg_luxury_days = df_monthly["food_luxury_days"].mean()
avg_sink_in = df_monthly["sinking_in"].mean()
avg_sink_out = df_monthly["sinking_out"].mean()
avg_net_ar = df_monthly["net_after_reserve"].mean()
avg_net_total = df_monthly["net_total"].mean()
avg_reserve = df_monthly["reserve_end"].mean()
expected_sinking_mean = SINKING_BASE + (SINKING_UP + SINKING_DOWN) / 2  # 理论均值

sinking_sum = df_expense[~df_expense["pay_period"].isin(["monthly", "daily"])]["monthly_amount"].sum()
daily_sum = df_expense[df_expense["pay_period"] == "daily"]["monthly_amount"].sum()
print(f"  月付合计: ¥{monthly_sum:,.0f}  |  蓄水池项月均摊: ¥{sinking_sum:,.0f}  |  日付(吃饭)月均: ¥{daily_sum:,.0f}")
print(f"  月付+蓄水池项月均摊合计: ¥{monthly_sum + sinking_sum:,.0f}")
print(f"  蓄水池实际月缴均值: ¥{avg_sink_in:,.0f}  (理论 ¥{expected_sinking_mean:,.0f}, 范围 ¥{SINKING_BASE+SINKING_DOWN:,.0f}~¥{SINKING_BASE+SINKING_UP:,.0f})")
print(f"  年付总需求: ¥{TOTAL_ANNUAL_SINKING:,.0f}  |  推荐月缴额: ¥{RECOMMENDED_SINKING_RATE:,.0f}")

print(f"\n  💰 月均统计 ({len(df_monthly)}个月)")
print("  " + "-" * 70)

print(f"  月均收入:          ¥{avg_inc:>10,.0f}")
print(f"  月均刚性账单:      ¥{avg_bills:>10,.0f}")
print(f"  月均吃饭:          ¥{avg_food:>10,.0f}")
if avg_frugal_days > 0:
    print(f"    ├ 节约日({avg_frugal_days:.0f}天) ¥{avg_food_frugal:>8,.0f}  日均¥{avg_food_frugal/avg_frugal_days:.0f}")
if avg_luxury_days > 0:
    print(f"    └ 奢侈日({avg_luxury_days:.0f}天) ¥{avg_food_luxury:>8,.0f}  日均¥{avg_food_luxury/avg_luxury_days:.0f}")
print(f"  月缴蓄水池(浮动):  ¥{avg_sink_in:>10,.0f}  [¥{SINKING_BASE+SINKING_DOWN:,.0f}~¥{SINKING_BASE+SINKING_UP:,.0f}]")
print(f"  ─────────────────────────────")
print(f"  月均可支配结余:    ¥{avg_net_ar:>10,.0f}  (= 收入 - 账单 - 吃饭 - 蓄水池)")
print(f"  月均蓄水池支出:    ¥{avg_sink_out:>10,.0f}  (年付事件从蓄水池扣款)")
print(f"  月均净结余:        ¥{avg_net_total:>10,.0f}")
print(f"  结余率:            {avg_net_total/avg_inc*100:>10.1f}%")
print(f"  最终主账户余额:    ¥{df_monthly['balance_end'].iloc[-1]:>10,.0f}")
print(f"  最终蓄水池余额:    ¥{df_monthly['reserve_end'].iloc[-1]:>10,.0f}")

print(f"\n  📊 年度汇总")
print("  " + "-" * 70)
print(f"  {'年份':<6s} {'收入':>10s} {'总支出':>10s} {'蓄水池缴':>10s} {'蓄水池支':>10s} {'净结余':>10s} {'年终结余':>10s}")
print("  " + "-" * 70)
for _, row in annual_summary.iterrows():
    yr = int(row["year"])
    yr_total = row["net_total"]
    # 找到该年最后一个月的 balance_end
    yr_last_bal = df_monthly[df_monthly["year"] == yr]["balance_end"].iloc[-1]
    yr_last_res = df_monthly[df_monthly["year"] == yr]["reserve_end"].iloc[-1]
    print(f"  {yr:<6d} ¥{row['income']:>8,.0f} ¥{row['total_expense']:>8,.0f} "
          f"¥{row['sinking_in']:>8,.0f} ¥{row['sinking_out']:>8,.0f} "
          f"¥{yr_total:>8,.0f} 主¥{yr_last_bal:>8,.0f}+储¥{yr_last_res:>6,.0f}")
print("  " + "-" * 70)

net_worth_final = (df_monthly["balance_end"].iloc[-1]
                   + df_monthly["reserve_end"].iloc[-1])
print(f"  5年净资产增长: ¥{net_worth_final - INITIAL_BALANCE:,.0f}  "
      f"(主¥{df_monthly['balance_end'].iloc[-1]:,.0f} + 储¥{df_monthly['reserve_end'].iloc[-1]:,.0f})")
print("=" * 75)

# ============================================================
# 图表
# ============================================================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 3, figsize=(20, 11))
fig.suptitle(f'家庭收支模型 v3 — Sinking Fund 年付蓄水池', fontsize=17, fontweight='bold', y=0.99)

x = np.arange(len(df_monthly))

# ---- 1: 收入 vs 支出构成堆叠 ----
ax1 = axes[0, 0]
ax1.fill_between(x, 0, df_monthly["income"], color='#2E86AB', alpha=0.15, label='月收入')
ax1.plot(x, df_monthly["income"], color='#2E86AB', linewidth=1.2, marker='o', markersize=2)
ax1.bar(x, -df_monthly["fixed_bills"], color='#D64933', alpha=0.8, label='刚性账单')
ax1.bar(x, -df_monthly["food"], bottom=-df_monthly["fixed_bills"],
        color='#F18F01', alpha=0.8, label='每日吃饭')
ax1.bar(x, -df_monthly["sinking_in"],
        bottom=-(df_monthly["fixed_bills"] + df_monthly["food"]),
        color='#A23B72', alpha=0.8, label='蓄水池月缴')
ax1.axhline(y=0, color='black', linewidth=0.8)
ax1.set_title('月度收入与支出构成', fontsize=13, fontweight='bold')
ax1.legend(fontsize=8, ncol=2)
ax1.set_xticks(x[::6])
ax1.set_xticklabels(df_monthly["label"].iloc[::6], rotation=45, fontsize=8)
ax1.grid(True, alpha=0.2, axis='y')

# ---- 2: 可支配结余 vs 实际净结余 ----
ax2 = axes[0, 1]
ax2.bar(x, df_monthly["net_after_reserve"], color='#2E86AB', alpha=0.7, label='可支配结余(扣蓄水池后)')
ax2.plot(x, df_monthly["net_total"], color='#2A9D8F', linewidth=1.5, marker='s', markersize=3, label='实际净结余')
ax2.axhline(y=0, color='black', linewidth=0.8)
ax2.axhline(y=df_monthly["net_after_reserve"].mean(), color='#2E86AB', linestyle='--',
            linewidth=1, label=f'均¥{df_monthly["net_after_reserve"].mean():.0f}')
ax2.axhline(y=df_monthly["net_total"].mean(), color='#2A9D8F', linestyle=':',
            linewidth=1, label=f'均¥{df_monthly["net_total"].mean():.0f}')
ax2.set_title('月度结余对比', fontsize=13, fontweight='bold')
ax2.legend(fontsize=8)
ax2.set_xticks(x[::6])
ax2.set_xticklabels(df_monthly["label"].iloc[::6], rotation=45, fontsize=8)
ax2.grid(True, alpha=0.2, axis='y')

# ---- 3: 蓄水池水位 ----
ax3 = axes[0, 2]
ax3.fill_between(x, 0, df_monthly["reserve_end"], color='#A23B72', alpha=0.2)
ax3.plot(x, df_monthly["reserve_end"], color='#A23B72', linewidth=2)
# 标注年付事件
for i in range(len(df_monthly)):
    if df_monthly["sinking_out"].iloc[i] > 0:
        ax3.axvline(x=i, color='#D64933', linestyle='--', alpha=0.4, linewidth=0.8)
        ax3.annotate(f'-¥{df_monthly["sinking_out"].iloc[i]:.0f}',
                    xy=(i, df_monthly["reserve_end"].iloc[i]),
                    fontsize=6, color='#D64933', ha='center',
                    xytext=(0, -12), textcoords='offset points')
ax3.axhline(y=avg_sink_in * 3, color='gray', linestyle=':', alpha=0.5,
            label=f'3个月蓄积 ¥{avg_sink_in*3:,}')
ax3.set_title('Yearly_Reserve 蓄水池水位', fontsize=13, fontweight='bold')
ax3.set_ylabel('蓄水池余额（元）', fontsize=11)
ax3.legend(fontsize=8)
ax3.set_xticks(x[::6])
ax3.set_xticklabels(df_monthly["label"].iloc[::6], rotation=45, fontsize=8)
ax3.grid(True, alpha=0.2)

# ---- 4: 主账户余额 + 蓄水池 ----
ax4 = axes[1, 0]
ax4.fill_between(x, 0, df_monthly["balance_end"], color='#2E86AB', alpha=0.15, label='主账户余额')
ax4.plot(x, df_monthly["balance_end"], color='#2E86AB', linewidth=1.5)
total_nw = df_monthly["balance_end"] + df_monthly["reserve_end"]
ax4.fill_between(x, df_monthly["balance_end"], total_nw,
                 color='#A23B72', alpha=0.2, label='+蓄水池(净资产)')
ax4.plot(x, total_nw, color='#A23B72', linewidth=1.2, linestyle='--')
ax4.axhline(y=INITIAL_BALANCE, color='gray', linestyle=':', alpha=0.5, label=f'初始 ¥{INITIAL_BALANCE:,}')
ax4.set_title('账户余额 & 净资产', fontsize=13, fontweight='bold')
ax4.set_ylabel('余额（元）', fontsize=11)
ax4.legend(fontsize=8)
ax4.set_xticks(x[::6])
ax4.set_xticklabels(df_monthly["label"].iloc[::6], rotation=45, fontsize=8)
ax4.grid(True, alpha=0.2)

# ---- 5: 年度柱状图 ----
ax5 = axes[1, 1]
yr_list = annual_summary["year"].astype(int).tolist()
n_yrs = len(yr_list)
x_yr = np.arange(n_yrs)
w = 0.25
ax5.bar(x_yr - w, annual_summary["income"], w, color='#2E86AB', alpha=0.85, label='年收入')
ax5.bar(x_yr, annual_summary["total_expense"], w, color='#D64933', alpha=0.85, label='年支出(含蓄水池缴)')
ax5.bar(x_yr + w, annual_summary["net_total"], w, color='#2A9D8F', alpha=0.85, label='年净结余')
for i in range(n_yrs):
    val = annual_summary["net_total"].iloc[i]
    ax5.text(x_yr[i] + w, val + 3000, f'¥{val:,.0f}', ha='center', fontsize=8, fontweight='bold')
ax5.set_title('年度收支对比', fontsize=13, fontweight='bold')
ax5.set_xticks(x_yr)
ax5.set_xticklabels(yr_list)
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.2, axis='y')

# ---- 6: 摘要卡片 ----
ax6 = axes[1, 2]
ax6.axis('off')
# 计算蓄水池覆盖率
reserve_final = df_monthly["reserve_end"].iloc[-1]
reserve_never_empty = (df_monthly["reserve_end"] > 0).all()
reserve_min = df_monthly["reserve_end"].min()

summary_text = f"""
[Sinking Fund 模型摘要]

  收入模型: N({INCOME_MEAN}, {INCOME_STD}²)
  到账日:   每月{PAYDAY}日
  蓄水池月缴: ¥{avg_sink_in:,.0f} (范围¥{SINKING_BASE+SINKING_DOWN:,.0f}~¥{SINKING_BASE+SINKING_UP:,.0f})
  年付总需求: ¥{TOTAL_ANNUAL_SINKING:,.0f}
  推荐月缴额: ¥{RECOMMENDED_SINKING_RATE:,.0f}

  模拟月数: {len(df_monthly)}个月

[核心指标]
  月均收入:        ¥{avg_inc:,.0f}
  月均刚性账单:    ¥{avg_bills:,.0f}
  月均吃饭:        ¥{avg_food:,.0f}
  月缴蓄水池(浮动): ¥{avg_sink_in:,.0f}
  ────────────────────────
  可支配结余:    ¥{avg_net_ar:,.0f}
  实际净结余:    ¥{avg_net_total:,.0f}
  结余率:        {avg_net_total/avg_inc*100:.1f}%

[蓄水池]
  月蓄积(均值):  ¥{avg_sink_in:,.0f}
  年蓄积(均值):  ¥{avg_sink_in*12:,.0f}
  年付总需求:    ¥{TOTAL_ANNUAL_SINKING:,.0f}
  覆盖率:        {avg_sink_in*12/TOTAL_ANNUAL_SINKING*100:.0f}%
  最终蓄水池余额: ¥{reserve_final:,.0f}
  蓄水池最低水位: ¥{reserve_min:,.0f}
  蓄水池是否枯竭: {'否' if reserve_never_empty else '是 - 某月不足!'}

[资产]
  主账户: ¥{df_monthly['balance_end'].iloc[-1]:,.0f}
  蓄水池: ¥{reserve_final:,.0f}
  净资产: ¥{net_worth_final:,.0f}
  初始:   ¥{INITIAL_BALANCE:,}
  增长:   ¥{net_worth_final - INITIAL_BALANCE:,.0f}
"""

ax6.text(0, 12, summary_text, fontsize=9.5, fontfamily='sans-serif',
         verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA',
                   edgecolor='#DEE2E6', alpha=0.9))

plt.tight_layout()
output_path = '/Users/lartemacfiles/Desktop/VPT-初诊数据/收支模拟结果_v3.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\n✅ 图表已保存: {output_path}")

# 输出 DataFrame 供查阅
print(f"\n📋 支出目录 DataFrame (df_expense):")
print(df_expense.to_string(index=False))
print(f"\n📊 近6个月流水 (df_monthly.tail(6)):")
cols_show = ["label", "income", "fixed_bills", "food", "sinking_in",
             "sinking_out", "reserve_end", "net_after_reserve", "net_total", "balance_end"]
print(df_monthly[cols_show].tail(6).to_string(index=False))

plt.show()
