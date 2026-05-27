#!/usr/bin/env python3
"""
家庭月收支数学模型（每日现金流粒度）
- 收入: 每月20日到账, N(18000, 1000²), 截断[14000, 22000]
- 支出: 每月刚性支出 + 每日吃饭 + 年度支出
- 可模拟多年收支趋势与每日余额变化
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================
# 参数设置
# ============================================================
INCOME_MEAN = 18000       # 月收入均值
INCOME_STD = 1000         # 月收入标准差
INCOME_MIN = 14000        # 月收入下限
INCOME_MAX = 22000        # 月收入上限
PAYDAY = 20               # 到账日

FOOD_MEAN = 200           # 每日吃饭均值
FOOD_STD = 35             # 每日吃饭标准差
FOOD_MIN = 100            # 每日吃饭下限
FOOD_MAX = 350            # 每日吃饭上限

START_YEAR = 2026
START_MONTH = 6
SIM_YEARS = 5
RANDOM_SEED = 42

INITIAL_BALANCE = 50000   # 初始余额（元）

# ============================================================
# 支出定义
# ============================================================

# 每月固定支出: {日: [(名称, 金额), ...]}
MONTHLY_EXPENSES = {
    1:  [("办公室月租", 1300), ("车位月租", 1000), ("物管费", 330), ("还贷", 2000)],
    5:  [("过路费", 600), ("营养品", 600), ("保洁用品", 300)],
    15: [("水电燃气网络手机", 1000)],
}

# 年度支出: {月: [(名称, 金额), ...]}（在指定月的1日扣除）
ANNUAL_EXPENSES = {
    1:  [("车辆保险", 4000)],
    2:  [("学校餐费校服(春)", 2000)],
    3:  [("游泳课(春)", 2000), ("美术课(春)", 2000)],
    7:  [("车辆保养维修", 4400)],
    9:  [("游泳课(秋)", 2000), ("美术课(秋)", 2000), ("计算机课", 1200), ("学校餐费校服(秋)", 2000)],
}

# ============================================================
# 初始化
# ============================================================
np.random.seed(RANDOM_SEED)

start_date = datetime(START_YEAR, START_MONTH, 1)
total_days = SIM_YEARS * 365 + 30  # 多取一些天数
end_date = start_date + timedelta(days=total_days)

# ============================================================
# 逐日模拟
# ============================================================
balance = INITIAL_BALANCE
daily_records = []      # [(日期, 当日收支, 余额, 备注)]
monthly_income = []     # [(日期, 金额)]
monthly_expense_total = []  # [(日期, 金额)]
monthly_food_total = []     # [(日期, 金额)]
monthly_annual_exp = []     # [(日期, 金额)]

current = start_date
while current <= end_date:
    day_net = 0
    notes = []
    d = current.day
    m = current.month
    y = current.year

    # ---- 收入：每月20日 ----
    if d == PAYDAY:
        month_idx = (y - START_YEAR) * 12 + (m - START_MONTH)
        raw = np.random.normal(INCOME_MEAN, INCOME_STD)
        inc = np.clip(raw, INCOME_MIN, INCOME_MAX)
        day_net += inc
        notes.append(f"+收入 {inc:.0f}")
        monthly_income.append((current, inc))

    # ---- 每月固定支出 ----
    for day_of_month, items in MONTHLY_EXPENSES.items():
        if d == day_of_month:
            for name, amt in items:
                day_net -= amt
                notes.append(f"-{name} {amt}")

    # ---- 年度支出（指定月1日） ----
    if d == 1 and m in ANNUAL_EXPENSES:
        for name, amt in ANNUAL_EXPENSES[m]:
            day_net -= amt
            notes.append(f"-{name}(年) {amt}")

    # ---- 每日吃饭 ----
    raw_food = np.random.normal(FOOD_MEAN, FOOD_STD)
    food = np.clip(raw_food, FOOD_MIN, FOOD_MAX)
    day_net -= food
    # 吃饭不写备注，避免记录太长

    # ---- 更新余额 ----
    balance += day_net
    daily_records.append((current, day_net, balance))

    current += timedelta(days=1)

# ============================================================
# 按月汇总
# ============================================================
monthly_summary = defaultdict(lambda: {"income": 0, "fixed_exp": 0, "food_exp": 0, "annual_exp": 0, "net": 0, "days": 0, "balance_end": 0})

for date, net, bal in daily_records:
    key = (date.year, date.month)
    monthly_summary[key]["net"] += net
    monthly_summary[key]["balance_end"] = bal
    monthly_summary[key]["days"] += 1

for date, inc in monthly_income:
    key = (date.year, date.month)
    monthly_summary[key]["income"] += inc

# 从 daily_records 提取分类支出（仅在交易发生的日期）
for date, net, bal in daily_records:
    key = (date.year, date.month)
    d, m = date.day, date.month

    # 每月固定支出
    if d in MONTHLY_EXPENSES:
        for name, amt in MONTHLY_EXPENSES[d]:
            monthly_summary[key]["fixed_exp"] += amt

    # 年度支出
    if d == 1 and m in ANNUAL_EXPENSES:
        for name, amt in ANNUAL_EXPENSES[m]:
            monthly_summary[key]["annual_exp"] += amt

# 吃饭支出 = net - income + fixed_exp + annual_exp（从net反推）
for key in monthly_summary:
    ms = monthly_summary[key]
    ms["food_exp"] = ms["income"] - ms["fixed_exp"] - ms["annual_exp"] - ms["net"]

# ============================================================
# 整理月度数据
# ============================================================
month_labels = []
month_incomes = []
month_fixed = []
month_food = []
month_annual = []
month_nets = []
month_balances = []

for key in sorted(monthly_summary.keys()):
    ms = monthly_summary[key]
    month_labels.append(datetime(key[0], key[1], 15))  # 用每月15日代表该月
    month_incomes.append(ms["income"])
    month_fixed.append(ms["fixed_exp"])
    month_food.append(ms["food_exp"])
    month_annual.append(ms["annual_exp"])
    month_nets.append(ms["net"])
    month_balances.append(ms["balance_end"])

month_incomes = np.array(month_incomes)
month_fixed = np.array(month_fixed)
month_food = np.array(month_food)
month_annual = np.array(month_annual)
month_nets = np.array(month_nets)
month_balances = np.array(month_balances)
month_total_exp = month_fixed + month_food + month_annual

# ============================================================
# 年度汇总
# ============================================================
annual_summary = defaultdict(lambda: {"income": 0, "fixed_exp": 0, "food_exp": 0, "annual_exp": 0, "net": 0})
for i, lbl in enumerate(month_labels):
    yr = lbl.year
    annual_summary[yr]["income"] += month_incomes[i]
    annual_summary[yr]["fixed_exp"] += month_fixed[i]
    annual_summary[yr]["food_exp"] += month_food[i]
    annual_summary[yr]["annual_exp"] += month_annual[i]
    annual_summary[yr]["net"] += month_nets[i]

# ============================================================
# 终端输出
# ============================================================
print("=" * 70)
print(f"  家庭收支模拟（{START_YEAR}年{START_MONTH}月 ~ {month_labels[-1].year}年{month_labels[-1].month}月）")
print("=" * 70)
print(f"  收入: N({INCOME_MEAN}, {INCOME_STD}²), 截断 [{INCOME_MIN}, {INCOME_MAX}], 每月{PAYDAY}日到账")
print(f"  吃饭: N({FOOD_MEAN}, {FOOD_STD}²), 截断 [{FOOD_MIN}, {FOOD_MAX}], 每日")
print(f"  每月刚性支出: ¥{sum(amt for items in MONTHLY_EXPENSES.values() for _, amt in items):,}")
print(f"  年度支出合计: ¥{sum(amt for items in ANNUAL_EXPENSES.values() for _, amt in items):,}")
print(f"  初始余额: ¥{INITIAL_BALANCE:,}")
print(f"  随机种子: {RANDOM_SEED}")
print("-" * 70)

total_income = sum(month_incomes)
total_expense = sum(month_total_exp)
total_net = sum(month_nets)
n_months = len(month_labels)

print(f"  【月均统计】({n_months}个月)")
print(f"  月均收入:    ¥{np.mean(month_incomes):>10,.2f}")
print(f"  月均总支出:  ¥{np.mean(month_total_exp):>10,.2f}")
print(f"    ┣ 刚性支出: ¥{np.mean(month_fixed):>10,.2f}")
print(f"    ┣ 每日吃饭: ¥{np.mean(month_food):>10,.2f}")
print(f"    ┗ 年度支出: ¥{np.mean(month_annual):>10,.2f}")
print(f"  月均结余:    ¥{np.mean(month_nets):>10,.2f}")
print(f"  最终余额:    ¥{month_balances[-1]:>10,.2f}")
print("-" * 70)

print(f"  【年度汇总】")
for yr in sorted(annual_summary.keys()):
    a = annual_summary[yr]
    months_in_yr = sum(1 for lbl in month_labels if lbl.year == yr)
    print(f"  {yr}年 ({months_in_yr}个月): 收入 ¥{a['income']:,.0f} | 支出 ¥{a['income']-a['net']:,.0f} | 结余 ¥{a['net']:,.0f}")
print("=" * 70)

# ============================================================
# 图表可视化
# ============================================================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 3, figsize=(20, 11))
fig.suptitle(f'家庭收支模型 — {SIM_YEARS}年模拟', fontsize=17, fontweight='bold', y=0.99)

# ---- 子图1: 月度收入 vs 总支出 ----
ax1 = axes[0, 0]
x = np.arange(len(month_labels))
width = 0.4
ax1.bar(x - width/2, month_incomes, width, color='#2E86AB', alpha=0.85, label='月收入')
ax1.bar(x + width/2, month_total_exp, width, color='#D64933', alpha=0.85,
        label='月总支出 (刚性+吃饭+年度)')
avg_income_line = ax1.axhline(y=INCOME_MEAN, color='#2E86AB', linestyle=':', linewidth=1, alpha=0.6)
avg_exp_line = ax1.axhline(y=np.mean(month_total_exp), color='#D64933', linestyle=':', linewidth=1, alpha=0.6)
ax1.set_ylabel('金额（元）', fontsize=11)
ax1.set_title('月度收入 vs 总支出', fontsize=13, fontweight='bold')
ax1.legend(fontsize=8, loc='upper right')
ax1.set_xticks(x[::6])
ax1.set_xticklabels([month_labels[i].strftime('%Y-%m') for i in range(0, len(month_labels), 6)],
                    rotation=45, fontsize=8)
ax1.grid(True, alpha=0.25, axis='y')

# ---- 子图2: 月度结余 ----
ax2 = axes[0, 1]
colors = ['#2E86AB' if v >= 0 else '#D64933' for v in month_nets]
ax2.bar(x, month_nets, color=colors, alpha=0.85)
ax2.axhline(y=0, color='black', linewidth=0.8)
ax2.axhline(y=np.mean(month_nets), color='#F18F01', linestyle='--', linewidth=1.2,
            label=f'月均结余 ¥{np.mean(month_nets):,.0f}')
ax2.set_ylabel('结余（元）', fontsize=11)
ax2.set_title('月度结余（收入 - 总支出）', fontsize=13, fontweight='bold')
ax2.legend(fontsize=8)
ax2.set_xticks(x[::6])
ax2.set_xticklabels([month_labels[i].strftime('%Y-%m') for i in range(0, len(month_labels), 6)],
                    rotation=45, fontsize=8)
ax2.grid(True, alpha=0.25, axis='y')

# ---- 子图3: 支出构成 ----
ax3 = axes[0, 2]
total_fixed = sum(month_fixed)
total_food = sum(month_food)
total_annual = sum(month_annual)
expense_labels = [f'每月刚性\n¥{total_fixed:,.0f}',
                  f'每日吃饭\n¥{total_food:,.0f}',
                  f'年度支出\n¥{total_annual:,.0f}']
expense_values = [total_fixed, total_food, total_annual]
expense_colors = ['#2E86AB', '#F18F01', '#A23B72']
wedges, texts, autotexts = ax3.pie(expense_values, labels=expense_labels, colors=expense_colors,
                                     autopct='%1.1f%%', startangle=90, explode=(0.02, 0.02, 0.02))
for t in autotexts:
    t.set_fontsize(10)
    t.set_fontweight('bold')
ax3.set_title(f'{SIM_YEARS}年总支出构成', fontsize=13, fontweight='bold')

# ---- 子图4: 每日余额曲线 ----
ax4 = axes[1, 0]
daily_dates = [r[0] for r in daily_records]
daily_bals = [r[2] for r in daily_records]
# 降采样以提高性能（取每7天的点）
sample_step = 7
ax4.fill_between(daily_dates[::sample_step], INITIAL_BALANCE, daily_bals[::sample_step],
                 color='#2E86AB', alpha=0.15)
ax4.plot(daily_dates[::sample_step], daily_bals[::sample_step], color='#2E86AB', linewidth=0.8)
ax4.axhline(y=INITIAL_BALANCE, color='gray', linestyle='--', linewidth=0.8, alpha=0.5, label=f'初始余额 ¥{INITIAL_BALANCE:,}')
ax4.axhline(y=0, color='#D64933', linewidth=1.2, linestyle='--', alpha=0.6, label='余额警戒线')
ax4.set_ylabel('账户余额（元）', fontsize=11)
ax4.set_title('每日账户余额', fontsize=13, fontweight='bold')
ax4.legend(fontsize=8)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax4.tick_params(axis='x', rotation=45, labelsize=8)
ax4.grid(True, alpha=0.25)

# ---- 子图5: 年度收支柱状图 ----
ax5 = axes[1, 1]
years_list = sorted(annual_summary.keys())
x_yr = np.arange(len(years_list))
w = 0.3
yr_income = [annual_summary[y]["income"] for y in years_list]
yr_expense = [annual_summary[y]["income"] - annual_summary[y]["net"] for y in years_list]
yr_net = [annual_summary[y]["net"] for y in years_list]
ax5.bar(x_yr - w, yr_income, w, color='#2E86AB', alpha=0.85, label='年收入')
ax5.bar(x_yr, yr_expense, w, color='#D64933', alpha=0.85, label='年支出')
ax5.bar(x_yr + w, yr_net, w, color='#2A9D8F', alpha=0.85, label='年结余')
for i in range(len(years_list)):
    ax5.text(x_yr[i] + w, yr_net[i] + 2000, f'¥{yr_net[i]:,.0f}',
             ha='center', fontsize=8, fontweight='bold')
ax5.set_ylabel('金额（元）', fontsize=11)
ax5.set_title('年度收支对比', fontsize=13, fontweight='bold')
ax5.set_xticks(x_yr)
ax5.set_xticklabels(years_list, fontsize=10)
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.25, axis='y')

# ---- 子图6: 摘要卡片 ----
ax6 = axes[1, 2]
ax6.axis('off')
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 12)

summary_text = f"""
[模拟参数]
  收入模型: N({INCOME_MEAN}, {INCOME_STD}²)
  到账日:   每月{PAYDAY}日
  模拟跨度: {month_labels[0].strftime('%Y-%m')} ~ {month_labels[-1].strftime('%Y-%m')}
  模拟月数: {n_months}个月

[关键指标]
  月均收入:   ¥{np.mean(month_incomes):,.0f}
  月均总支出: ¥{np.mean(month_total_exp):,.0f}
  月均结余:   ¥{np.mean(month_nets):,.0f}
  结余率:     {np.mean(month_nets)/np.mean(month_incomes)*100:.1f}%

[账户余额]
  初始余额:   ¥{INITIAL_BALANCE:,}
  最终余额:   ¥{month_balances[-1]:,.0f}
  {'资产增长:   ¥' + f'{month_balances[-1] - INITIAL_BALANCE:,.0f}' if month_balances[-1] > INITIAL_BALANCE else '资产减少:   ¥' + f'{INITIAL_BALANCE - month_balances[-1]:,.0f}'}

[月度波动]
  最高结余月: ¥{np.max(month_nets):,.0f}
  最低结余月: ¥{np.min(month_nets):,.0f}
  结余标准差: ¥{np.std(month_nets):,.0f}
"""

ax6.text(0, 12, summary_text, fontsize=10, fontfamily='sans-serif', verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA', edgecolor='#DEE2E6', alpha=0.9))

plt.tight_layout()
output_path = '/Users/lartemacfiles/Desktop/VPT-初诊数据/收支模拟结果.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\n✅ 图表已保存: {output_path}")
plt.show()
