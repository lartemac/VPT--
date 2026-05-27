#!/usr/bin/env python3
"""
家庭月收入数学模型
- 每月20日到账，金额服从正态分布 N(18000, 1000²)
- 可模拟多年收入趋势
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================
# 参数设置（根据需要修改）
# ============================================================
INCOME_MEAN = 18000       # 月收入均值（元）
INCOME_STD = 1000         # 月收入标准差（元）
INCOME_MIN = 14000        # 月收入下限（元），防止极端值过低
INCOME_MAX = 22000        # 月收入上限（元），防止极端值过高
PAYDAY = 20               # 每月到账日
START_YEAR = 2026         # 起始年份
START_MONTH = 6           # 起始月份
SIM_YEARS = 5             # 模拟年数
RANDOM_SEED = 42          # 随机种子（固定可复现；设 None 则每次不同）

# ============================================================
# 收入生成
# ============================================================
np.random.seed(RANDOM_SEED)

total_months = SIM_YEARS * 12
# 生成原始收入
raw_income = np.random.normal(INCOME_MEAN, INCOME_STD, total_months)
# 截断到合理范围
income = np.clip(raw_income, INCOME_MIN, INCOME_MAX)

# 生成日期标签（每月20日）
dates = []
for i in range(total_months):
    y = START_YEAR + (START_MONTH - 1 + i) // 12
    m = (START_MONTH - 1 + i) % 12 + 1
    dates.append(datetime(y, m, PAYDAY))

# ============================================================
# 统计汇总
# ============================================================
cumulative = np.cumsum(income)
annual = defaultdict(float)
for d, v in zip(dates, income):
    annual[d.year] += v

print("=" * 60)
print(f"  家庭月收入模拟（{START_YEAR}年{START_MONTH}月 ~ {dates[-1].year}年{dates[-1].month}月）")
print("=" * 60)
print(f"  月收入分布: N({INCOME_MEAN}, {INCOME_STD}²), 截断 [{INCOME_MIN}, {INCOME_MAX}]")
print(f"  到账日: 每月{PAYDAY}日")
print(f"  模拟月数: {total_months}")
print(f"  随机种子: {RANDOM_SEED}")
print("-" * 60)
print(f"  月均收入:  ¥{np.mean(income):,.2f}")
print(f"  月收入中位数: ¥{np.median(income):,.2f}")
print(f"  月收入标准差: ¥{np.std(income, ddof=1):,.2f}")
print(f"  最高月收入: ¥{np.max(income):,.2f}  ({dates[np.argmax(income)].strftime('%Y-%m')})")
print(f"  最低月收入: ¥{np.min(income):,.2f}  ({dates[np.argmin(income)].strftime('%Y-%m')})")
print(f"  累计总收入: ¥{cumulative[-1]:,.2f}")
print(f"  年均收入:  ¥{cumulative[-1]/SIM_YEARS:,.2f}")
print("-" * 60)
for yr in sorted(annual.keys()):
    print(f"  {yr}年: ¥{annual[yr]:,.2f}  (月均 ¥{annual[yr]/12:,.2f})")
print("=" * 60)

# ============================================================
# 图表可视化
# ============================================================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle(f'家庭月收入模型 — {SIM_YEARS}年模拟 ({dates[0].strftime("%Y-%m")} ~ {dates[-1].strftime("%Y-%m")})',
             fontsize=16, fontweight='bold', y=0.98)

# ---- 子图1：月度收入曲线 ----
ax1 = axes[0, 0]
ax1.plot(dates, income, color='#2E86AB', linewidth=1.2, marker='o', markersize=3, label='月收入')
mean_line = ax1.axhline(y=INCOME_MEAN, color='#A23B72', linestyle='--', linewidth=1.2, alpha=0.7, label=f'均值 ¥{INCOME_MEAN}')
ax1.fill_between(dates, INCOME_MEAN - INCOME_STD, INCOME_MEAN + INCOME_STD,
                 color='#A23B72', alpha=0.08, label=f'±1σ (¥{INCOME_STD})')
ax1.set_ylabel('月收入（元）', fontsize=12)
ax1.set_title('月度收入波动', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right', fontsize=9)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax1.tick_params(axis='x', rotation=45, labelsize=9)
ax1.set_ylim(INCOME_MIN - 500, INCOME_MAX + 500)
ax1.grid(True, alpha=0.3)

# ---- 子图2：累计收入 ----
ax2 = axes[0, 1]
ax2.fill_between(dates, 0, cumulative, color='#F18F01', alpha=0.25)
ax2.plot(dates, cumulative, color='#F18F01', linewidth=2, label='累计收入')
ax2.set_ylabel('累计收入（元）', fontsize=12)
ax2.set_title('累计收入增长', fontsize=13, fontweight='bold')
# 标注每10万
for level in range(100000, int(cumulative[-1]) + 100000, 100000):
    ax2.axhline(y=level, color='gray', linestyle=':', alpha=0.3, linewidth=0.8)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax2.tick_params(axis='x', rotation=45, labelsize=9)
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)

# ---- 子图3：年度柱状图 ----
ax3 = axes[1, 0]
years_list = list(annual.keys())
values = [annual[y] for y in years_list]
bars = ax3.bar(years_list, values, color='#2E86AB', edgecolor='white', linewidth=0.8)
avg_annual = cumulative[-1] / SIM_YEARS
ax3.axhline(y=avg_annual, color='#A23B72', linestyle='--', linewidth=1.2, alpha=0.7, label=f'年均 ¥{avg_annual:,.0f}')
for bar, val in zip(bars, values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
             f'¥{val:,.0f}', ha='center', fontsize=10, fontweight='bold')
ax3.set_ylabel('年收入（元）', fontsize=12)
ax3.set_title('年度收入对比', fontsize=13, fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3, axis='y')

# ---- 子图4：收入分布直方图 ----
ax4 = axes[1, 1]
n, bins, patches = ax4.hist(income, bins=20, color='#F18F01', edgecolor='white',
                             alpha=0.8, density=True)
# 叠加理论正态曲线
x = np.linspace(INCOME_MIN, INCOME_MAX, 200)
pdf = np.exp(-(x - INCOME_MEAN)**2 / (2 * INCOME_STD**2)) / (INCOME_STD * np.sqrt(2 * np.pi))
ax4.plot(x, pdf, color='#A23B72', linewidth=2, label=f'理论 N({INCOME_MEAN},{INCOME_STD}²)')
ax4.axvline(x=np.mean(income), color='#2E86AB', linestyle='--', linewidth=1.5, label=f'实际均值 ¥{np.mean(income):,.0f}')
ax4.axvline(x=np.median(income), color='green', linestyle=':', linewidth=1.5, label=f'中位数 ¥{np.median(income):,.0f}')
ax4.set_xlabel('月收入（元）', fontsize=12)
ax4.set_ylabel('概率密度', fontsize=12)
ax4.set_title('月收入分布', fontsize=13, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
output_path = '/Users/lartemacfiles/Desktop/VPT-初诊数据/收入模拟结果.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\n✅ 图表已保存: {output_path}")
plt.show()
