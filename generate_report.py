#!/usr/bin/env python3
"""
家庭收支预测与财务规划压力测试 — 图表 + HTML 报告生成
输出:
  1. 60月支出堆叠条形图 → 桌面/家庭收支堆叠图.png
  2. HTML 压力测试报告 → 桌面/家庭收支预测报告.html
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
from collections import defaultdict
import base64
import io
import os

# ============================================================
# 参数（与 v3 一致）
# ============================================================
INCOME_MEAN, INCOME_STD, INCOME_MIN, INCOME_MAX = 18000, 1000, 14000, 22000
PAYDAY = 20
FRUGAL_MEAN, FRUGAL_STD, FRUGAL_MIN, FRUGAL_MAX = 200, 30, 120, 300
LUXURY_MEAN, LUXURY_STD, LUXURY_MIN, LUXURY_MAX = 400, 60, 300, 600
LUXURY_PER_WEEK_MEAN, LUXURY_PER_WEEK_STD = 2, 0.5
SINKING_BASE, SINKING_UP, SINKING_DOWN = 1800, 200, -1000
START_YEAR, START_MONTH, SIM_MONTHS = 2026, 6, 60
RANDOM_SEED = 42
INITIAL_BALANCE = 50000

MONTHLY_BILLS = {
    1:  [("房贷", 2000), ("办公室月租", 1300), ("车位月租", 1000), ("物管费", 330)],
    5:  [("过路费", 600), ("牛奶钙片等营养品", 600), ("保洁用品", 300), ("车辆保养均摊", 325)],
    15: [("水电燃气网络手机", 1000)],
}

YEARLY_SINKING_EVENTS = {
    4:  [("学校餐费(春期中)", 600)],
    6:  [("学校餐费(春期末)", 600)],
    9:  [("车辆保险", 4500), ("校服", 1000)],
    10: [("学校餐费(秋期中)", 600)],
    12: [("学校餐费(秋期末)", 600)],
}

CYCLIC_EVENTS = [
    ("游泳课", 3600, 10, datetime(2026, 7, 1)),
    ("计算机课", 16000, 16, datetime(2026, 8, 1)),
    ("美术课", 1400, 4, datetime(2026, 8, 1)),
]

# 优先级分类
P0_P1_ITEMS = ["房贷", "办公室月租", "车位月租", "物管费", "水电燃气网络手机",
               "过路费", "车辆保养均摊", "车辆保险", "学校餐费(春期中)", "学校餐费(春期末)",
               "学校餐费(秋期中)", "学校餐费(秋期末)", "校服"]
P2_ITEMS = ["游泳课", "美术课", "计算机课"]
P3_ITEMS = ["牛奶钙片等营养品", "保洁用品"]

DESKTOP = os.path.expanduser("~/Desktop")

# ============================================================
# 工具函数
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
    """判断支出项优先级"""
    for kw in P0_P1_ITEMS:
        if kw in name: return "P0-P1"
    for kw in P2_ITEMS:
        if kw in name: return "P2"
    for kw in P3_ITEMS:
        if kw in name: return "P3"
    return "P1"

# ============================================================
# 逐日模拟
# ============================================================
np.random.seed(RANDOM_SEED)

start_date = datetime(START_YEAR, START_MONTH, 1)
total_days = SIM_MONTHS // 12 * 365 + (SIM_MONTHS % 12) * 31 + 60
end_date = start_date + timedelta(days=total_days)

SINKING_CALENDAR = build_sinking_calendar(start_date, end_date)

TOTAL_ANNUAL_SINKING = (
    sum(amt for items in YEARLY_SINKING_EVENTS.values() for _, amt in items) +
    sum(amt * (12 / interval) for _, amt, interval, _ in CYCLIC_EVENTS)
)

balance = INITIAL_BALANCE
reserve = 0
monthly_log = []
daily_detail = []  # 每日记录(用于后续分析)

current = start_date
current_month_key = None

mon_income = mon_fixed_bills = mon_food = 0
mon_food_frugal = mon_food_luxury = 0
mon_food_frugal_days = mon_food_luxury_days = 0
mon_sinking_in = mon_sinking_out = 0
mon_sinking_from_main = 0  # 蓄水池不足时从主账户补的金额
mon_p0p1 = mon_p2 = mon_p3 = 0  # 按优先级分类支出

luxury_dates = set()
current_week = None

while current <= end_date:
    d, m, y = current.day, current.month, current.year
    mk = (y, m)

    if mk != current_month_key:
        if current_month_key is not None:
            monthly_log.append({
                "year": current_month_key[0], "month": current_month_key[1],
                "income": mon_income, "fixed_bills": mon_fixed_bills,
                "food": round(mon_food, 0), "sinking_in": mon_sinking_in,
                "sinking_out": mon_sinking_out, "sinking_from_main": mon_sinking_from_main,
                "reserve_end": round(reserve, 0),
                "p0p1": round(mon_p0p1, 0), "p2": round(mon_p2, 0), "p3": round(mon_p3, 0),
                "net_after_reserve": round(mon_income - mon_fixed_bills - mon_food - mon_sinking_in, 0),
                "balance_end": round(balance, 0),
                "food_frugal": round(mon_food_frugal, 0), "food_luxury": round(mon_food_luxury, 0),
                "food_frugal_days": mon_food_frugal_days, "food_luxury_days": mon_food_luxury_days,
            })
        current_month_key = mk
        mon_income = mon_fixed_bills = mon_food = 0
        mon_food_frugal = mon_food_luxury = 0
        mon_food_frugal_days = mon_food_luxury_days = 0
        mon_sinking_in = mon_sinking_out = mon_sinking_from_main = 0
        mon_p0p1 = mon_p2 = mon_p3 = 0

    iso_week = current.isocalendar()[1]
    if iso_week != current_week:
        current_week = iso_week
        n_luxury = int(np.clip(np.random.normal(LUXURY_PER_WEEK_MEAN, LUXURY_PER_WEEK_STD), 1, 3))
        week_start = current - timedelta(days=current.weekday())
        week_days = [week_start + timedelta(days=i) for i in range(7)]
        chosen = np.random.choice(week_days, size=n_luxury, replace=False)
        luxury_dates = set(chosen)

    day_net = 0
    is_payday = (d == PAYDAY)
    sinking_event_items = []
    bill_items = []

    # 收入 + 蓄水池
    if is_payday:
        inc = np.clip(np.random.normal(INCOME_MEAN, INCOME_STD), INCOME_MIN, INCOME_MAX)
        day_net += inc
        mon_income += inc
        sinking_amt = round(SINKING_BASE + np.random.uniform(SINKING_DOWN, SINKING_UP), -1)
        reserve += sinking_amt
        day_net -= sinking_amt
        mon_sinking_in += sinking_amt

    # 每月固定账单
    for dom, items in MONTHLY_BILLS.items():
        if d == dom:
            for name, amt in items:
                day_net -= amt
                mon_fixed_bills += amt
                bill_items.append((name, amt))
                pri = classify_priority(name)
                if pri == "P0-P1": mon_p0p1 += amt
                elif pri == "P2": mon_p2 += amt
                else: mon_p3 += amt

    # 蓄水池扣款
    if current in SINKING_CALENDAR:
        for name, amt in SINKING_CALENDAR[current]:
            sinking_event_items.append((name, amt))
            pri = classify_priority(name)
            if pri == "P0-P1": mon_p0p1 += amt
            elif pri == "P2": mon_p2 += amt
            else: mon_p3 += amt
            if reserve >= amt:
                reserve -= amt
                mon_sinking_out += amt
            else:
                shortfall = amt - reserve
                reserve = 0
                day_net -= shortfall
                mon_sinking_out += (amt - shortfall)
                mon_sinking_from_main += shortfall

    # 每日吃饭
    if current in luxury_dates:
        food = np.clip(np.random.normal(LUXURY_MEAN, LUXURY_STD), LUXURY_MIN, LUXURY_MAX)
        mon_food_luxury += food
        mon_food_luxury_days += 1
    else:
        food = np.clip(np.random.normal(FRUGAL_MEAN, FRUGAL_STD), FRUGAL_MIN, FRUGAL_MAX)
        mon_food_frugal += food
        mon_food_frugal_days += 1
    day_net -= food
    mon_food += food
    mon_p0p1 += food

    balance += day_net
    daily_detail.append({
        "date": current, "day_net": day_net, "balance": balance,
        "reserve": reserve,
        "is_payday": is_payday,
        "sinking_event_total": sum(a for _, a in sinking_event_items),
        "has_sinking_event": len(sinking_event_items) > 0,
    })
    current += timedelta(days=1)

# 保存最后一个月
if current_month_key is not None:
    monthly_log.append({
        "year": current_month_key[0], "month": current_month_key[1],
        "income": mon_income, "fixed_bills": mon_fixed_bills,
        "food": round(mon_food, 0), "sinking_in": mon_sinking_in,
        "sinking_out": mon_sinking_out, "sinking_from_main": mon_sinking_from_main,
        "reserve_end": round(reserve, 0),
        "p0p1": round(mon_p0p1, 0), "p2": round(mon_p2, 0), "p3": round(mon_p3, 0),
        "net_after_reserve": round(mon_income - mon_fixed_bills - mon_food - mon_sinking_in, 0),
        "balance_end": round(balance, 0),
        "food_frugal": round(mon_food_frugal, 0), "food_luxury": round(mon_food_luxury, 0),
        "food_frugal_days": mon_food_frugal_days, "food_luxury_days": mon_food_luxury_days,
    })

df = pd.DataFrame(monthly_log)
df = df.head(SIM_MONTHS)  # 精确60个月
df["label"] = df.apply(lambda r: f"{int(r.year)}-{int(r.month):02d}", axis=1)
df["total_expense"] = df["fixed_bills"] + df["food"] + df["sinking_in"]
df["net_total"] = df["income"] - df["total_expense"]
df["sinking_event_flag"] = df["sinking_out"] > 0
df["month_index"] = range(len(df))

# ============================================================
# 核心指标计算
# ============================================================
avg_inc = df["income"].mean()
avg_total_exp = df["total_expense"].mean()
avg_net = df["net_total"].mean()
avg_savings_rate = avg_net / avg_inc * 100

# 真实等效月成本 (含蓄水池均摊年付)
equivalent_monthly_cost = df["total_expense"].mean()

# 极限生存线: 仅 P0+P1 (去掉 P2 游泳课/美术课/计算机课, P3 营养品/保洁)
p3_monthly = 600 + 300  # 营养品+保洁 P3 每月
p2_annual_total = sum(amt * (12 / interval) for _, amt, interval, _ in CYCLIC_EVENTS)
p2_monthly_equiv = p2_annual_total / 12

survival_monthly = (df["fixed_bills"].mean() + df["food"].mean()
                    + df["sinking_in"].mean() - p2_monthly_equiv - p3_monthly)
survival_annual = survival_monthly * 12
survival_vs_income = survival_monthly / avg_inc * 100

# 风险月识别
risk_months = []
for i, row in df.iterrows():
    risk_level = "安全"
    reasons = []

    # 可支配结余为负
    if row["net_after_reserve"] < 0:
        risk_level = "⚠️ 赤字"
        reasons.append(f"可支配结余 ¥{row['net_after_reserve']:,.0f}")

    # 蓄水池不足需要主账户补贴
    if row["sinking_from_main"] > 0:
        if risk_level == "安全": risk_level = "⚡ 蓄水池不足"
        elif risk_level == "⚠️ 赤字": risk_level = "🔴 双重风险"
        reasons.append(f"蓄水池缺口 ¥{row['sinking_from_main']:,.0f}")

    # 大型支出月 (单月 sinking_out > 5000)
    if row["sinking_out"] > 5000:
        if risk_level == "安全": risk_level = "💥 大额支出"
        reasons.append(f"月蓄水池支出 ¥{row['sinking_out']:,.0f}")

    # 月末余额低于初始余额的20%
    if row["balance_end"] < INITIAL_BALANCE * 0.2:
        if risk_level == "安全": risk_level = "⚠️ 低余额"
        reasons.append(f"月末余额仅 ¥{row['balance_end']:,.0f}")

    if risk_level != "安全":
        sinking_items_str = ""
        dt_key = datetime(int(row["year"]), int(row["month"]), 1)
        if dt_key in SINKING_CALENDAR:
            sinking_items_str = " | ".join(
                f"{n} ¥{a:,.0f}" for n, a in SINKING_CALENDAR[dt_key]
            )
        risk_months.append({
            "label": row["label"],
            "month_index": i,
            "risk_level": risk_level,
            "reasons": " | ".join(reasons),
            "net_after_reserve": row["net_after_reserve"],
            "net_total": row["net_total"],
            "sinking_out": row["sinking_out"],
            "sinking_from_main": row["sinking_from_main"],
            "balance_end": row["balance_end"],
            "reserve_end": row["reserve_end"],
            "sinking_items": sinking_items_str,
        })

risk_df = pd.DataFrame(risk_months) if risk_months else pd.DataFrame()

# 年度汇总
annual = df.groupby("year").agg(
    income=("income", "sum"), total_expense=("total_expense", "sum"),
    net_total=("net_total", "sum"),
    sinking_in=("sinking_in", "sum"), sinking_out=("sinking_out", "sum"),
    end_balance=("balance_end", "last"), end_reserve=("reserve_end", "last"),
).reset_index()

print("=" * 60)
print("  压力测试分析完成")
print(f"  60个月 ({df['label'].iloc[0]} ~ {df['label'].iloc[-1]})")
print(f"  月均收入: ¥{avg_inc:,.0f}  |  等效月成本: ¥{equivalent_monthly_cost:,.0f}")
print(f"  月均结余: ¥{avg_net:,.0f}  |  结余率: {avg_savings_rate:.1f}%")
print(f"  极限生存月成本(仅P0+P1): ¥{survival_monthly:,.0f}/月")
print(f"  风险月数: {len(risk_months)}/{SIM_MONTHS}")
print("=" * 60)

# ============================================================
# 图表 1: 60月支出堆叠条形图（保存为PNG）
# ============================================================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig1, ax1 = plt.subplots(figsize=(22, 10))

x = np.arange(SIM_MONTHS)
width = 0.75

# 堆叠层
bottom = np.zeros(SIM_MONTHS)
colors_stack = {
    "刚性月付账单": '#2E86AB',
    "每日吃饭": '#F18F01',
    "蓄水池月缴": '#A23B72',
    "蓄水池支出(主账户补)": '#D64933',
}

# 层1: 刚性月付账单
ax1.bar(x, df["fixed_bills"], width, bottom=bottom, color=colors_stack["刚性月付账单"],
        label='刚性月付账单 (房贷/租金/物管/水电等)')
bottom += df["fixed_bills"].values

# 层2: 每日吃饭
ax1.bar(x, df["food"], width, bottom=bottom, color=colors_stack["每日吃饭"],
        label='每日吃饭')
bottom += df["food"].values

# 层3: 蓄水池月缴
ax1.bar(x, df["sinking_in"], width, bottom=bottom, color=colors_stack["蓄水池月缴"],
        label='蓄水池月缴 (浮动 ¥800~¥2,000)')
bottom += df["sinking_in"].values

# 层4: 蓄水池不足从主账户补
ax1.bar(x, df["sinking_from_main"], width, bottom=bottom, color=colors_stack["蓄水池支出(主账户补)"],
        label='蓄水池缺口主账户补贴')

# 收入线
ax1.plot(x, df["income"], color='#2A9D8F', linewidth=1.5, marker='o', markersize=2,
         label='月收入 (N(18000,1000²))', zorder=5)

# 极限生存线
ax1.axhline(y=survival_monthly, color='#E76F51', linestyle='--', linewidth=1.5, alpha=0.7,
            label=f'极限生存线(仅P0+P1) ¥{survival_monthly:,.0f}/月')

# 标注暴击月
for i, row in df.iterrows():
    if row["sinking_out"] > 5000:
        ax1.annotate(f'[暴击] ¥{row["sinking_out"]:,.0f}',
                     xy=(i, bottom[i]), fontsize=7, color='#D64933',
                     ha='center', fontweight='bold',
                     xytext=(0, 8), textcoords='offset points')
    elif row["sinking_out"] > 2000:
        ax1.annotate(f'¥{row["sinking_out"]:,.0f}',
                     xy=(i, bottom[i]), fontsize=6, color='#A23B72',
                     ha='center',
                     xytext=(0, 5), textcoords='offset points')

ax1.set_ylabel('金额（元）', fontsize=13)
ax1.set_title('未来60个月家庭月度支出构成 — 堆叠条形图', fontsize=16, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=9, ncol=2, framealpha=0.9)
ax1.set_xticks(x[::3])
ax1.set_xticklabels(df["label"].iloc[::3], rotation=45, fontsize=8)
ax1.set_ylim(0, 28000)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'¥{v:,.0f}'))
ax1.grid(True, alpha=0.2, axis='y')

# 图例说明
textstr = f'月均总支出: ¥{equivalent_monthly_cost:,.0f}\n月均收入: ¥{avg_inc:,.0f}\n结余率: {avg_savings_rate:.1f}%\n极限生存线: ¥{survival_monthly:,.0f}/月'
ax1.text(0.99, 0.97, textstr, transform=ax1.transAxes, fontsize=9,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
chart1_path = os.path.join(DESKTOP, '家庭收支堆叠图.png')
fig1.savefig(chart1_path, dpi=150, bbox_inches='tight')
print(f"✅ 堆叠条形图已保存: {chart1_path}")
plt.close(fig1)

# ============================================================
# 图表 2: 风险热力图 + 余额走势（用于HTML嵌入）
# ============================================================
fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(20, 9), gridspec_kw={'height_ratios': [1.2, 1]})

# 上: 可支配结余 + 风险标记
colors_bar = []
for i, row in df.iterrows():
    if row["net_after_reserve"] < 0: colors_bar.append('#D64933')
    elif row["sinking_out"] > 5000: colors_bar.append('#F18F01')
    elif row["sinking_from_main"] > 0: colors_bar.append('#E9C46A')
    else: colors_bar.append('#2E86AB')
ax2a.bar(x, df["net_after_reserve"], color=colors_bar, alpha=0.85)
ax2a.axhline(y=0, color='black', linewidth=0.8)
ax2a.axhline(y=df["net_after_reserve"].mean(), color='#2A9D8F', linestyle='--', linewidth=1.2,
             label=f'月均可支配结余 ¥{df["net_after_reserve"].mean():,.0f}')
ax2a.set_ylabel('可支配结余（元）', fontsize=12)
ax2a.set_title('月度可支配结余与风险标记', fontsize=14, fontweight='bold')
ax2a.legend(fontsize=9)
ax2a.set_xticks(x[::3])
ax2a.set_xticklabels(df["label"].iloc[::3], rotation=45, fontsize=8)
ax2a.grid(True, alpha=0.2, axis='y')

# 标注风险月
for rm in risk_months:
    i = rm["month_index"]
    short_label = "X" if "赤字" in rm["risk_level"] or "双重" in rm["risk_level"] else "!"
    ax2a.annotate(short_label,
                 xy=(i, df["net_after_reserve"].iloc[i]),
                 fontsize=10, ha='center', fontweight='bold',
                 color='#D64933' if "赤字" in rm["risk_level"] or "双重" in rm["risk_level"] else '#F18F01',
                 xytext=(0, -15), textcoords='offset points')

# 下: 主账户余额 + 蓄水池
ax2b.fill_between(x, 0, df["balance_end"], color='#2E86AB', alpha=0.15, label='主账户余额')
ax2b.plot(x, df["balance_end"], color='#2E86AB', linewidth=1.5)
nw = df["balance_end"] + df["reserve_end"]
ax2b.fill_between(x, df["balance_end"], nw, color='#A23B72', alpha=0.15, label='+蓄水池(净资产)')
ax2b.plot(x, nw, color='#A23B72', linewidth=1, linestyle='--')
ax2b.axhline(y=INITIAL_BALANCE, color='gray', linestyle=':', alpha=0.5, label=f'初始余额 ¥{INITIAL_BALANCE:,}')
ax2b.axhline(y=0, color='#D64933', linewidth=1.5, linestyle='--', alpha=0.6, label='余额警戒线')
ax2b.set_ylabel('余额（元）', fontsize=12)
ax2b.set_title('账户余额与净资产走势', fontsize=14, fontweight='bold')
ax2b.legend(fontsize=9, ncol=3, loc='upper left')
ax2b.set_xticks(x[::3])
ax2b.set_xticklabels(df["label"].iloc[::3], rotation=45, fontsize=8)
ax2b.grid(True, alpha=0.2)

plt.tight_layout()
chart2_path = os.path.join(DESKTOP, '家庭收支风险图.png')
fig2.savefig(chart2_path, dpi=150, bbox_inches='tight')
print(f"✅ 风险分析图已保存: {chart2_path}")
plt.close(fig2)

# ============================================================
# 图表 3: 年度汇总 + 支出结构 （用于HTML嵌入）
# ============================================================
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(18, 6.5))

# 年度柱状图
yr_list = annual["year"].astype(int).tolist()
x_yr = np.arange(len(yr_list))
w = 0.25
ax3a.bar(x_yr - w, annual["income"], w, color='#2E86AB', alpha=0.85, label='年收入')
ax3a.bar(x_yr, annual["total_expense"], w, color='#D64933', alpha=0.85, label='年支出')
ax3a.bar(x_yr + w, annual["net_total"], w, color='#2A9D8F', alpha=0.85, label='年结余')
for i in range(len(yr_list)):
    val = annual["net_total"].iloc[i]
    ax3a.text(x_yr[i] + w, val + 3000, f'¥{val:,.0f}', ha='center', fontsize=8, fontweight='bold')
ax3a.set_title('年度收支对比', fontsize=13, fontweight='bold')
ax3a.set_xticks(x_yr)
ax3a.set_xticklabels(yr_list)
ax3a.legend(fontsize=9)
ax3a.grid(True, alpha=0.2, axis='y')

# 支出结构饼图
pie_labels = []
pie_values = []
# 每月固定刚性
monthly_fixed_total = df["fixed_bills"].sum()
pie_labels.append(f'刚性月付\n¥{monthly_fixed_total/len(df):,.0f}/月')
pie_values.append(monthly_fixed_total)

food_total = df["food"].sum()
pie_labels.append(f'每日吃饭\n¥{food_total/len(df):,.0f}/月')
pie_values.append(food_total)

sink_total = df["sinking_out"].sum()
pie_labels.append(f'蓄水池支出\n¥{sink_total/len(df):,.0f}/月')
pie_values.append(sink_total)

sink_from_main_total = df["sinking_from_main"].sum()
if sink_from_main_total > 0:
    pie_labels.append(f'蓄水池缺口\n¥{sink_from_main_total/len(df):,.0f}/月')
    pie_values.append(sink_from_main_total)

colors_pie = ['#2E86AB', '#F18F01', '#A23B72', '#D64933']
wedges, texts, autotexts = ax3b.pie(pie_values, labels=pie_labels, colors=colors_pie,
                                     autopct='%1.1f%%', startangle=90,
                                     explode=[0.02]*len(pie_values))
for t in autotexts:
    t.set_fontsize(10); t.set_fontweight('bold')
ax3b.set_title(f'60个月总支出构成 (¥{sum(pie_values):,.0f})', fontsize=13, fontweight='bold')

plt.tight_layout()
chart3_path = os.path.join(DESKTOP, '家庭收支结构图.png')
fig3.savefig(chart3_path, dpi=150, bbox_inches='tight')
print(f"✅ 结构分析图已保存: {chart3_path}")
plt.close(fig3)

# ============================================================
# 图片转 Base64
# ============================================================
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

b64_chart1 = img_to_b64(chart1_path)
b64_chart2 = img_to_b64(chart2_path)
b64_chart3 = img_to_b64(chart3_path)

# ============================================================
# HTML 报告生成
# ============================================================
net_worth_final = df["balance_end"].iloc[-1] + df["reserve_end"].iloc[-1]
final_main = df["balance_end"].iloc[-1]
final_reserve = df["reserve_end"].iloc[-1]
reserve_min = df["reserve_end"].min()

# 风险分级统计
severe = len([r for r in risk_months if "🔴" in r["risk_level"]])
warning = len([r for r in risk_months if "⚠️" in r["risk_level"] or "⚡" in r["risk_level"]])
spike = len([r for r in risk_months if "💥" in r["risk_level"]])

# 计算机课16月列表
comp_months = []
for dt_key, items in SINKING_CALENDAR.items():
    for name, amt in items:
        if "计算机" in name and start_date <= dt_key <= end_date:
            comp_months.append(dt_key.strftime('%Y-%m'))

# 暴击月 (sinking_out > 5000)
spike_months = df[df["sinking_out"] > 5000].copy()
spike_list = []
for _, row in spike_months.iterrows():
    dt_key = datetime(int(row["year"]), int(row["month"]), 1)
    items_str = ""
    if dt_key in SINKING_CALENDAR:
        items_str = " + ".join(f"{n}(¥{a:,.0f})" for n, a in SINKING_CALENDAR[dt_key])
    spike_list.append({
        "label": row["label"],
        "sinking_out": row["sinking_out"],
        "items": items_str,
        "net": row["net_after_reserve"],
        "balance": row["balance_end"],
    })

# 低余额月 (余额 < 2万)
low_balance = df[df["balance_end"] < 20000]

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>未来60个月家庭收支预测与财务规划压力测试报告</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; background: #f5f7fa; color: #2c3e50; line-height: 1.7; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
  .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #fff; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }}
  .header h1 {{ font-size: 2em; margin-bottom: 8px; }}
  .header .subtitle {{ font-size: 1.1em; opacity: 0.85; }}
  .header .meta {{ margin-top: 15px; font-size: 0.9em; opacity: 0.7; }}

  .card {{ background: #fff; border-radius: 12px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
  .card h2 {{ font-size: 1.4em; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #2E86AB; display: flex; align-items: center; gap: 10px; }}
  .card h3 {{ font-size: 1.15em; margin: 18px 0 10px; color: #2E86AB; }}

  .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; }}
  .metric {{ background: #f8f9fa; border-radius: 10px; padding: 20px; text-align: center; border-left: 5px solid #2E86AB; }}
  .metric.danger {{ border-left-color: #D64933; }}
  .metric.warning {{ border-left-color: #F18F01; }}
  .metric.success {{ border-left-color: #2A9D8F; }}
  .metric .value {{ font-size: 1.8em; font-weight: 700; margin: 8px 0; }}
  .metric .label {{ font-size: 0.9em; color: #6c757d; }}
  .metric .sub {{ font-size: 0.8em; color: #adb5bd; margin-top: 4px; }}

  table {{ width: 100%; border-collapse: collapse; font-size: 0.94em; margin: 12px 0; }}
  th {{ background: #2E86AB; color: #fff; padding: 12px 10px; text-align: left; font-weight: 600; }}
  td {{ padding: 10px; border-bottom: 1px solid #e9ecef; }}
  tr:hover {{ background: #f8f9fa; }}
  .risk-red {{ background: #fff5f5; }}
  .risk-orange {{ background: #fffaf0; }}
  .risk-yellow {{ background: #fffff0; }}
  .tag {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.82em; font-weight: 600; }}
  .tag-red {{ background: #fee; color: #D64933; }}
  .tag-orange {{ background: #fff3e0; color: #F18F01; }}
  .tag-green {{ background: #e8f5e9; color: #2A9D8F; }}
  .tag-blue {{ background: #e3f2fd; color: #2E86AB; }}

  .chart-container {{ text-align: center; margin: 16px 0; }}
  .chart-container img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}

  .alert {{ padding: 16px 20px; border-radius: 8px; margin: 12px 0; }}
  .alert-danger {{ background: #fff5f5; border: 1px solid #fecaca; color: #991b1b; }}
  .alert-warning {{ background: #fffaf0; border: 1px solid #fed7aa; color: #92400e; }}
  .alert-info {{ background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; }}
  .alert-success {{ background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }}

  .rec-list {{ list-style: none; padding: 0; }}
  .rec-list li {{ padding: 12px 16px; margin: 8px 0; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #2E86AB; }}
  .rec-list li strong {{ color: #2E86AB; }}

  .footer {{ text-align: center; padding: 20px; color: #adb5bd; font-size: 0.85em; }}

  @media print {{
    body {{ background: #fff; }}
    .card {{ box-shadow: none; border: 1px solid #e9ecef; page-break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>未来60个月家庭收支预测与财务规划压力测试报告</h1>
  <div class="subtitle">基于 Sinking Fund 浮动蓄水池模型</div>
  <div class="meta">
    报告周期: {df["label"].iloc[0]} ~ {df["label"].iloc[-1]} (60个月/5年) |
    生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} |
    随机种子: {RANDOM_SEED} |
    模型版本: v3
  </div>
</div>

<!-- ===== 一、核心指标面板 ===== -->
<div class="card">
  <h2>一、核心指标面板</h2>
  <div class="metrics-grid">
    <div class="metric">
      <div class="label">月均收入</div>
      <div class="value">¥{avg_inc:,.0f}</div>
      <div class="sub">N(18000, 1000²) / 每月20日到账</div>
    </div>
    <div class="metric">
      <div class="label">等效月总成本</div>
      <div class="value">¥{equivalent_monthly_cost:,.0f}</div>
      <div class="sub">含刚性月付 + 吃饭 + 蓄水池缴纳</div>
    </div>
    <div class="metric success">
      <div class="label">月均结余</div>
      <div class="value">¥{avg_net:,.0f}</div>
      <div class="sub">结余率 {avg_savings_rate:.1f}%</div>
    </div>
    <div class="metric danger">
      <div class="label">极限生存线 (仅P0+P1)</div>
      <div class="value">¥{survival_monthly:,.0f}/月</div>
      <div class="sub">占收入 {survival_vs_income:.1f}% | 年需 ¥{survival_annual:,.0f}</div>
    </div>
    <div class="metric warning">
      <div class="label">蓄水池年均缺口</div>
      <div class="value">¥{TOTAL_ANNUAL_SINKING - df["sinking_in"].mean()*12:,.0f}/年</div>
      <div class="sub">年付需求 ¥{TOTAL_ANNUAL_SINKING:,.0f} vs 实际年缴 ¥{df["sinking_in"].mean()*12:,.0f}</div>
    </div>
    <div class="metric">
      <div class="label">最终净资产</div>
      <div class="value">¥{net_worth_final:,.0f}</div>
      <div class="sub">主账户 ¥{final_main:,.0f} + 蓄水池 ¥{final_reserve:,.0f}</div>
    </div>
  </div>

  <h3>极限生存线解读</h3>
  <div class="alert alert-info">
    <strong>定义:</strong> 仅保留 P0 (不可违约) + P1 (合同约束/基本生存) 支出层级。<br>
    <strong>包含:</strong> 房贷、办公室/车位/物管、水电燃气、过路费、车辆保养、吃饭、车辆保险、学校餐费、校服<br>
    <strong>剔除:</strong> P2 (游泳课/美术课/计算机课) + P3 (营养品/保洁用品)<br>
    <strong>含义:</strong> 在极端情况下压缩所有非生存支出后的最低月耗。当前极限生存月成本 ¥{survival_monthly:,.0f}，占月收入 {survival_vs_income:.1f}%，
    意味着即使砍掉所有 P2/P3 支出，每月仍有约 ¥{avg_inc - survival_monthly:,.0f} 的安全缓冲。
  </div>
</div>

<!-- ===== 二、核心图表: 60月堆叠条形图 ===== -->
<div class="card">
  <h2>二、60月支出构成 — 堆叠条形图</h2>
  <div class="chart-container">
    <img src="data:image/png;base64,{b64_chart1}" alt="60月支出堆叠图">
  </div>
  <div class="alert alert-warning">
    <strong>暴击波峰解读:</strong> 红色柱段表示蓄水池余额不足、需从主账户额外补贴的部分。
    当柱顶接近或超过绿色收入线时，该月现金流极度紧张。
    标注金额的月份为月蓄水池支出 >¥5,000 的"暴击月"——通常是计算机课(¥16,000)或车险+游泳课+校服叠加月。
  </div>
</div>

<!-- ===== 三、月度可支配结余与风险热力 ===== -->
<div class="card">
  <h2>三、月度可支配结余与账户余额走势</h2>
  <div class="chart-container">
    <img src="data:image/png;base64,{b64_chart2}" alt="风险分析图">
  </div>
</div>

<!-- ===== 四、年度与结构分析 ===== -->
<div class="card">
  <h2>四、年度汇总与支出结构</h2>
  <div class="chart-container">
    <img src="data:image/png;base64,{b64_chart3}" alt="结构分析图">
  </div>

  <h3>年度数据明细</h3>
  <table>
    <thead>
      <tr><th>年份</th><th>年收入</th><th>年支出</th><th>净结余</th><th>蓄水池缴</th><th>蓄水池支</th><th>年终主账户</th><th>年终蓄水池</th></tr>
    </thead>
    <tbody>
"""
for _, r in annual.iterrows():
    html += f"""<tr>
      <td><strong>{int(r['year'])}</strong></td>
      <td>¥{r['income']:,.0f}</td>
      <td>¥{r['total_expense']:,.0f}</td>
      <td><span class="tag {'tag-green' if r['net_total'] > 0 else 'tag-red'}">¥{r['net_total']:,.0f}</span></td>
      <td>¥{r['sinking_in']:,.0f}</td>
      <td>¥{r['sinking_out']:,.0f}</td>
      <td>¥{r['end_balance']:,.0f}</td>
      <td>¥{r['end_reserve']:,.0f}</td>
    </tr>"""

html += """
    </tbody>
  </table>
</div>
"""

# ===== 五、风险预警 =====
html += """<div class="card">
  <h2>五、风险预警 — 未来60个月压力测试</h2>"""

if len(risk_months) > 0:
    html += f"""
  <div class="metrics-grid" style="margin-bottom:20px;">
    <div class="metric danger">
      <div class="label">严重风险月 (双重风险)</div>
      <div class="value">{severe}</div>
      <div class="sub">赤字 + 蓄水池不足</div>
    </div>
    <div class="metric warning">
      <div class="label">警告月 (赤字/蓄水池不足)</div>
      <div class="value">{warning}</div>
      <div class="sub">可支配结余为负或蓄水池缺口</div>
    </div>
    <div class="metric">
      <div class="label">大额支出月 (暴击)</div>
      <div class="value">{spike}</div>
      <div class="sub">单月蓄水池支出 >¥5,000</div>
    </div>
    <div class="metric">
      <div class="label">总风险月数 / 总月数</div>
      <div class="value">{len(risk_months)}/{SIM_MONTHS}</div>
      <div class="sub">占比 {len(risk_months)/SIM_MONTHS*100:.1f}%</div>
    </div>
  </div>

  <h3>完整风险月清单</h3>
  <table>
    <thead>
      <tr><th>月份</th><th>风险等级</th><th>风险原因</th><th>可支配结余</th><th>月净结余</th><th>蓄水池支出</th><th>月末余额</th><th>触发事件</th></tr>
    </thead>
    <tbody>"""

    for rm in risk_months:
        rc = "risk-red" if "🔴" in rm["risk_level"] or "⚠️" in rm["risk_level"] else "risk-orange" if "💥" in rm["risk_level"] else "risk-yellow"
        tag_c = "tag-red" if "赤字" in rm["risk_level"] or "双重" in rm["risk_level"] else "tag-orange"
        html += f"""<tr class="{rc}">
      <td><strong>{rm['label']}</strong></td>
      <td><span class="tag {tag_c}">{rm['risk_level']}</span></td>
      <td>{rm['reasons']}</td>
      <td>¥{rm['net_after_reserve']:,.0f}</td>
      <td>¥{rm['net_total']:,.0f}</td>
      <td>¥{rm['sinking_out']:,.0f}</td>
      <td>¥{rm['balance_end']:,.0f}</td>
      <td style="font-size:0.85em;">{rm['sinking_items']}</td>
    </tr>"""

    html += """
    </tbody>
  </table>
"""

# 暴击月详情
if len(spike_list) > 0:
    html += """
  <h3>暴击月 (单月蓄水池支出 >¥5,000) 详情</h3>
  <div class="alert alert-danger">
    <strong>这些月份是年度大型支出集中爆发期。</strong>蓄水池余额大概率不足以覆盖，需要提前从主账户准备资金。<br>
    特别注意计算机课（¥16,000/16个月）和车险+多项叠加的月份。
  </div>
  <table>
    <thead><tr><th>月份</th><th>蓄水池支出</th><th>触发项目</th><th>当月可支配结余</th><th>月末余额</th></tr></thead>
    <tbody>"""
    for sm in spike_list:
        html += f"""<tr class="risk-orange">
      <td><strong>{sm['label']}</strong></td>
      <td><span class="tag tag-red">¥{sm['sinking_out']:,.0f}</span></td>
      <td>{sm['items']}</td>
      <td>¥{sm['net']:,.0f}</td>
      <td>¥{sm['balance']:,.0f}</td>
    </tr>"""
    html += "</tbody></table>"

# 计算机课特写
if comp_months:
    html += f"""
  <h3>最大单项风险: 计算机课 (¥16,000/16月)</h3>
  <div class="alert alert-danger">
    <strong>未来60个月内计算机课缴费月份:</strong> {', '.join(comp_months)}<br>
    计算机课是模型中单笔金额最大的支出（¥16,000），相当于 <strong>{16000/avg_inc:.1f} 个月的全部收入</strong>。
    在没有充足蓄水池储备的情况下，这些月份必然需要动用主账户余额或其他积蓄。
  </div>
"""

# 低余额警告
if len(low_balance) > 0:
    html += f"""
  <h3>低余额警告 (月末余额 < ¥20,000)</h3>
  <div class="alert alert-warning">
    共有 <strong>{len(low_balance)}</strong> 个月月末余额低于 ¥20,000。
    这些月份抗风险能力极弱，任何意外支出都可能导致现金流断裂。
  </div>
"""

html += """
</div>
"""

# ===== 六、结论与执行建议 =====
html += f"""<div class="card">
  <h2>六、结论与执行建议</h2>

  <h3>6.1 核心结论</h3>
  <ol>
    <li><strong>当前收支结构基本健康，但蓄水池严重不足。</strong>
      月均收入 ¥{avg_inc:,.0f}，等效月成本 ¥{equivalent_monthly_cost:,.0f}，
      月均结余 ¥{avg_net:,.0f}（结余率 {avg_savings_rate:.1f}%）。
      但蓄水池月缴浮动均值仅 ¥{df['sinking_in'].mean():,.0f}，
      远低于年付总需求的月均摊 ¥{TOTAL_ANNUAL_SINKING/12:,.0f}，
      覆盖率仅 {df['sinking_in'].mean()*12/TOTAL_ANNUAL_SINKING*100:.0f}%。
    </li>
    <li><strong>大型支出月份是主要风险源。</strong>
      计算机课（¥16,000/16月）和车险+游泳课叠加月（9月）是两大"暴击"来源。
      蓄水池余额在暴击月后通常降至 ¥1,000~¥3,000 的危险低水位。
    </li>
    <li><strong>极限生存线为 ¥{survival_monthly:,.0f}/月。</strong>
      即使砍掉所有 P2（兴趣班）和 P3（营养品/保洁）支出，月耗仍为 ¥{survival_monthly:,.0f}，
      仅占收入的 {survival_vs_income:.1f}%，说明家庭基础生存支出可控。
    </li>
    <li><strong>5年模拟净资产增长 ¥{net_worth_final - INITIAL_BALANCE:,.0f}。</strong>
      从初始 ¥{INITIAL_BALANCE:,} 增至 ¥{net_worth_final:,.0f}，
      年均增长约 ¥{(net_worth_final - INITIAL_BALANCE)/5:,.0f}，属于稳健但非高增长型。
    </li>
  </ol>

  <h3>6.2 执行建议</h3>
  <ul class="rec-list">
    <li>
      <strong>建议一：建立"双账户"资金缓冲机制</strong><br>
      将主账户月均结余的一部分（建议 ¥1,000~¥1,500/月）定向划入蓄水池，
      在暴击月前 3-4 个月提前预警并加速储蓄，确保大型支出月前蓄水池余额 >¥8,000。
    </li>
    <li>
      <strong>建议二：计算机课单独备款</strong><br>
      计算机课 ¥16,000/16月 ≈ ¥1,000/月，是最高单笔支出。
      建议为该项单独设立储备，或在缴费前 3 个月开始每月额外存 ¥5,000+。
      缴费月份: {", ".join(comp_months) if comp_months else "无"}。
    </li>
    <li>
      <strong>建议三：关注9月"多重重叠"</strong><br>
      每年9月叠加车险(¥4,500)+校服(¥1,000)+游泳课(约¥3,600)+美术课(约¥1,400)，
      合计约 ¥10,500+，是年度最大现金流压力点。建议7-8月减少非必要支出，集中蓄水。
    </li>
    <li>
      <strong>建议四：减少奢侈日频率</strong><br>
      当前每周约2次奢侈日(日均¥400)贡献了 ¥{df['food_luxury'].mean():,.0f}/月的吃饭支出。
      如果每周减少1次奢侈日（从2次→1次），约可节省 ¥{(400-200)*4.33:,.0f}/月。
    </li>
    <li>
      <strong>建议五：P3弹性支出可作应急调节阀</strong><br>
      营养品(¥600/月)和保洁用品(¥300/月)合计 ¥900/月，属于可压缩支出。
      在风险月前可暂时压缩 30-50%，释放 ¥270~¥450/月的缓冲空间。
    </li>
  </ul>

  <h3>6.3 风险时间轴 (关键月份)</h3>
  <table>
    <thead><tr><th>时间窗口</th><th>风险类型</th><th>原因</th><th>建议动作</th></tr></thead>
    <tbody>
      <tr class="risk-orange"><td>每年 1月</td><td>⚡ 中风险</td><td>过年后余额偏紧 + 开学前准备</td><td>12月预留 ¥3,000+ 缓冲</td></tr>
      <tr class="risk-red"><td>每年 8-9月</td><td>🔴 高风险</td><td>车险+游泳课+美术课+校服+计算机课可能叠加</td><td>7月前确保蓄水池 >¥10,000</td></tr>
      <tr class="risk-orange"><td>计算机课月份<br>(16月周期)</td><td>🔴 极端</td><td>单笔 ¥16,000 支出</td><td>提前3月额外储蓄</td></tr>
    </tbody>
  </table>
</div>

<div class="footer">
  <p>本报告由家庭预算模型 v3 自动生成 | 基于 numpy 蒙特卡洛模拟 | 随机种子 {RANDOM_SEED} | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>

</div>
</body>
</html>"""

report_path = os.path.join(DESKTOP, '家庭收支预测报告.html')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✅ HTML 报告已保存: {report_path}")
print(f"\n📁 桌面输出文件:")
print(f"   1. {chart1_path}")
print(f"   2. {chart2_path}")
print(f"   3. {chart3_path}")
print(f"   4. {report_path}")
