#!/usr/bin/env python3
"""
VPT 急性牙髓炎15例数据医学统计图表
按确定的医学期刊标准风格绘制
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# 设置中文字体（Mac 系统字体）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Helvetica', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

# 导入路径处理模块
from pathlib import Path

# 设置保存路径
save_dir = Path('~/Desktop').expanduser()

# 配色方案（按标准）
COLOR_SCATTER = '#808080'  # 散点灰色
COLOR_MEAN_LINE = '#FF0000'  # 均值连线红色
COLOR_BOX_FILL = 'lightblue'  # 箱线图填充淡蓝色
COLOR_BOX_EDGE = 'blue'  # 箱线图边框蓝色
COLOR_MEDIAN = 'darkblue'  # 中位数线深蓝色

# 字体设置（Mac 兼容）
FONT_CHINESE = 'Arial Unicode MS'  # Mac 系统中文字体
FONT_ENGLISH = 'Times New Roman'  # 英文字体

# 加载数据
file = '~/Desktop/副本急性牙髓炎15例最终数据20251122.xlsx'
df = pd.read_excel(file)

# 提取 VAS 数据（列索引从0开始，所以减1）
vas_pre = df.iloc[:, 11]  # 术前 VAS（第12列）
vas_24h = df.iloc[:, 31]  # 术后24h（第32列）
vas_3d = df.iloc[:, 33]   # 术后3天（第34列）
vas_7d = df.iloc[:, 35]   # 术后7天（第36列）
vas_1m = df.iloc[:, 37]   # 术后1个月（第38列）
vas_6m = df.iloc[:, 41]   # 术后6个月（第42列）
age = df.iloc[:, 3]       # 年龄（第4列）

# 创建时间点标签
time_points = ['术前', '术后24h', '术后3天', '术后7天', '术后1个月', '术后6个月']
vas_data = [vas_pre, vas_24h, vas_3d, vas_7d, vas_1m, vas_6m]

# 计算均值
mean_vas = [np.mean(v.dropna()) for v in vas_data]

print('=' * 60)
print('VPT 数据统计')
print('=' * 60)
print(f'样本数: {len(df)}')
print(f'\nVAS 评分均值:')
for tp, m in zip(time_points, mean_vas):
    print(f'  {tp:12s}: {m:.2f}')
print()

# ============================================================================
# 图1-5：各时间点 VAS 变化情况图
# ============================================================================
print('正在生成 图1-5：各时间点 VAS 变化情况图...')

fig1, ax1 = plt.subplots(figsize=(12, 8))

# 绘制箱线图（只在术前和术后24h绘制）
bp1 = ax1.boxplot([vas_pre, vas_24h],
                   positions=[0, 1],
                   widths=0.5,
                   showmeans=False,
                   patch_artist=True)

# 箱线图样式
for box in bp1['boxes']:
    box.set_facecolor(COLOR_BOX_FILL)
    box.set_alpha(0.7)
    box.set_edgecolor(COLOR_BOX_EDGE)
    box.set_linewidth(1.5)

for median in bp1['medians']:
    median.set_color(COLOR_MEDIAN)
    median.set_linewidth(2)

for whisker in bp1['whiskers']:
    whisker.set_color(COLOR_BOX_EDGE)
    whisker.set_linewidth(1.5)

for cap in bp1['caps']:
    cap.set_color(COLOR_BOX_EDGE)
    cap.set_linewidth(1.5)

# 绘制散点（所有时间点）
np.random.seed(42)  # 确保可重复
for i, (x_pos, data) in enumerate(zip(range(6), vas_data)):
    # 双向抖动
    y_jitter = np.random.uniform(-0.15, 0.15, len(data))
    x_jitter = np.random.uniform(-0.12, 0.12, len(data))

    ax1.scatter(x_pos + x_jitter, data + y_jitter,
               s=50, c=COLOR_SCATTER, alpha=0.6,
               edgecolors='#404040', linewidth=0.5, zorder=3)

# 绘制均值连线
ax1.plot(range(6), mean_vas, color=COLOR_MEAN_LINE,
        linewidth=2.5, marker='o', markersize=8,
        markerfacecolor='white', markeredgecolor=COLOR_MEAN_LINE,
        markeredgewidth=2, zorder=4, label='均值')

# 统计检验（术前 vs 术后24h）
t_stat, p_value = stats.ttest_rel(vas_pre, vas_24h)
print(f'配对 t 检验: t = {t_stat:.4f}, P = {p_value:.6f}')

# P值标注
if p_value < 0.001:
    p_text = 'P < 0.001'
else:
    p_text = f'P = {p_value:.4f}'

ax1.annotate(p_text, xy=(0.5, 0.95), xycoords='axes fraction',
            fontsize=14, fontweight='bold', ha='center',
            family=FONT_ENGLISH)

# 设置坐标轴
ax1.set_xticks(range(6))
ax1.set_xticklabels(time_points, fontsize=14, fontweight='bold', family=FONT_CHINESE)
ax1.set_ylabel('VAS 评分', fontsize=16, fontweight='bold', family=FONT_CHINESE)
ax1.set_ylim(0, 10)

# Y轴刻度
ax1.set_yticks([0, 2.5, 5.0, 7.5, 10])
ax1.set_yticklabels(['0', '2.5', '5.0', '7.5', '10'], fontsize=12)

# 网格线
ax1.grid(True, linestyle='--', alpha=0.3, linewidth=0.5)
ax1.set_axisbelow(True)

# 边框设置
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)

# 标题
ax1.set_title('各时间点 VAS 变化情况', fontsize=18, fontweight='bold',
             pad=20, family=FONT_CHINESE)

# 图例
ax1.legend(loc='upper right', fontsize=12, framealpha=0.9)

plt.tight_layout()
plt.savefig(save_dir / '图1-5.png', dpi=300, bbox_inches='tight')
print(f'✅ 已保存: {save_dir}/图1-5.png')
plt.close()

# ============================================================================
# 图2：术前 VAS 及年龄与术后 24h VAS 的相关性分析
# ============================================================================
print('\n正在生成 图2：相关性分析图...')

fig2, axes2 = plt.subplots(1, 3, figsize=(12, 8))

# 子图A：术前 VAS vs 术后24h VAS
ax2a = axes2[0]
ax2a.scatter(vas_pre, vas_24h, s=50, c=COLOR_SCATTER, alpha=0.6,
            edgecolors='#404040', linewidth=0.5)

# Spearman 相关
corr_a, p_a = stats.spearmanr(vas_pre, vas_24h)

# 回归线
z_a = np.polyfit(vas_pre, vas_24h, 1)
p_a_poly = np.poly1d(z_a)
x_line_a = np.linspace(vas_pre.min(), vas_pre.max(), 100)
ax2a.plot(x_line_a, p_a_poly(x_line_a), color=COLOR_MEDIAN,
         linewidth=2, label=f'回归线')

ax2a.set_xlabel('术前 VAS 评分', fontsize=12, fontweight='bold', family=FONT_CHINESE)
ax2a.set_ylabel('术后24h VAS 评分', fontsize=12, fontweight='bold', family=FONT_CHINESE)
ax2a.set_xlim(3, 10)
ax2a.set_ylim(-2, 6)
ax2a.grid(True, linestyle='--', alpha=0.3, linewidth=0.5)
ax2a.spines['top'].set_visible(False)
ax2a.spines['right'].set_visible(False)

# 标注
ax2a.text(0.5, 0.95, f"A. 术前 vs 术后24h\nSpearman R = {corr_a:.3f}, P = {p_a:.3f}",
         transform=ax2a.transAxes, fontsize=10, ha='center', va='top',
         family='Times New Roman', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 子图B（左）：年龄 vs 术前 VAS
ax2b = axes2[1]
ax2b.scatter(age, vas_pre, s=50, c=COLOR_SCATTER, alpha=0.6,
            edgecolors='#404040', linewidth=0.5)

corr_b, p_b = stats.spearmanr(age, vas_pre)

z_b = np.polyfit(age, vas_pre, 1)
p_b_poly = np.poly1d(z_b)
x_line_b = np.linspace(age.min(), age.max(), 100)
ax2b.plot(x_line_b, p_b_poly(x_line_b), color=COLOR_MEDIAN,
         linewidth=2)

ax2b.set_xlabel('年龄（岁）', fontsize=12, fontweight='bold', family=FONT_CHINESE)
ax2b.set_ylabel('术前 VAS 评分', fontsize=12, fontweight='bold', family=FONT_CHINESE)
ax2b.set_xticks([20, 30, 40, 50, 60])
ax2b.set_ylim(4, 10)
ax2b.grid(True, linestyle='--', alpha=0.3, linewidth=0.5)
ax2b.spines['top'].set_visible(False)
ax2b.spines['right'].set_visible(False)

ax2b.text(0.5, 0.95, f"B. 年龄 vs 术前\nSpearman R = {corr_b:.3f}, P = {p_b:.3f}",
         transform=ax2b.transAxes, fontsize=10, ha='center', va='top',
         family='Times New Roman', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 子图B（右）：年龄 vs 术后24h VAS
ax2c = axes2[2]
ax2c.scatter(age, vas_24h, s=50, c=COLOR_SCATTER, alpha=0.6,
            edgecolors='#404040', linewidth=0.5)

corr_c, p_c = stats.spearmanr(age, vas_24h)

z_c = np.polyfit(age, vas_24h, 1)
p_c_poly = np.poly1d(z_c)
x_line_c = np.linspace(age.min(), age.max(), 100)
ax2c.plot(x_line_c, p_c_poly(x_line_c), color=COLOR_MEDIAN,
         linewidth=2)

ax2c.set_xlabel('年龄（岁）', fontsize=12, fontweight='bold', family=FONT_CHINESE)
ax2c.set_ylabel('术后24h VAS 评分', fontsize=12, fontweight='bold', family=FONT_CHINESE)
ax2c.set_xticks([20, 30, 40, 50, 60])
ax2c.set_ylim(-2, 6)
ax2c.grid(True, linestyle='--', alpha=0.3, linewidth=0.5)
ax2c.spines['top'].set_visible(False)
ax2c.spines['right'].set_visible(False)

ax2c.text(0.5, 0.95, f"C. 年龄 vs 术后24h\nSpearman R = {corr_c:.3f}, P = {p_c:.3f}",
         transform=ax2c.transAxes, fontsize=10, ha='center', va='top',
         family='Times New Roman', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(save_dir / '图2.png', dpi=300, bbox_inches='tight')
print(f'✅ 已保存: {save_dir}/图2.png')
plt.close()

# ============================================================================
# 图3：临床参数与术后24h VAS 相关性分析（5幅子图）
# ============================================================================
print('\n正在生成 图3：临床参数与术后24h VAS 相关性分析...')

# 提取临床参数数据
bite_pain = df.iloc[:, 9]      # 咬合痛（第10列）
pai = df.iloc[:, 17]           # 根尖周围透亮区（第18列）
restoration = df.iloc[:, 18]   # 充填物（第19列）
anesthesia = df.iloc[:, 23]    # 麻醉方式（第24列）
pulp_texture = df.iloc[:, 24]  # 近髓处探诊质地（第25列）

fig3, axes3 = plt.subplots(2, 3, figsize=(16, 11))
axes3 = axes3.flatten()

# 删除最后一个子图（右下角）
fig3.delaxes(axes3[5])

# 参数配置
params = [
    (bite_pain, '咬合痛', ['否', '是']),
    (pai, '根尖周围透亮区', ['PAI 1', 'PAI 2']),
    (restoration, '充填物', ['无', '有']),
    (anesthesia, '麻醉方式', ['局部', '阻滞']),
    (pulp_texture, '近髓处探诊质地', ['硬', '软']),
]

for idx, (data, title, groups) in enumerate(params):
    ax = axes3[idx]

    # 准备数据
    group_data = []
    for g in groups:
        mask = data == g
        group_data.append(vas_24h[mask])

    # 绘制散点（两组都有）
    np.random.seed(42 + idx)
    for g_idx, g in enumerate(groups):
        mask = data == g
        y_data = vas_24h[mask]

        # 抖动
        x_jitter = np.random.uniform(-0.12, 0.12, len(y_data))
        y_jitter = np.random.uniform(-0.15, 0.15, len(y_data))

        ax.scatter(g_idx + x_jitter, y_data + y_jitter,
                  s=50, c=COLOR_SCATTER, alpha=0.6,
                  edgecolors='#404040', linewidth=0.5, zorder=3)

    # 统计检验
    if len(group_data[0]) > 0 and len(group_data[1]) > 0:
        t_stat, p_val = stats.ttest_ind(group_data[0].dropna(),
                                       group_data[1].dropna())

        # 绘制显著性标记
        if p_val < 0.05:
            y_max = max([np.nanmax(d) for d in group_data])
            y_pos = y_max + 0.5

            # 画星号线
            ax.plot([0, 1], [y_pos, y_pos], color='black', linewidth=1)
            ax.plot([0, 0], [y_pos-0.2, y_pos], color='black', linewidth=1)
            ax.plot([1, 1], [y_pos-0.2, y_pos], color='black', linewidth=1)

            # 星号
            if p_val < 0.001:
                stars = '***'
            elif p_val < 0.01:
                stars = '**'
            else:
                stars = '*'

            ax.text(0.5, y_pos + 0.2, stars,
                   ha='center', fontsize=14, fontweight='bold',
                   family='Times New Roman')

            ax.text(0.5, y_pos - 0.5, f'P = {p_val:.3f}',
                   ha='center', fontsize=10, style='italic',
                   family='Times New Roman')

    # 设置坐标轴
    ax.set_xticks([0, 1])
    ax.set_xticklabels(groups, fontsize=12, fontweight='bold', family=FONT_CHINESE)
    ax.set_ylabel('术后24h VAS 评分', fontsize=12, fontweight='bold', family=FONT_CHINESE)
    ax.set_title(title, fontsize=14, fontweight='bold', family=FONT_CHINESE, pad=10)
    ax.set_ylim(-2, 8)
    ax.grid(True, linestyle='--', alpha=0.3, linewidth=0.5, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(save_dir / '图3.png', dpi=300, bbox_inches='tight')
print(f'✅ 已保存: {save_dir}/图3.png')
plt.close()

print('\n' + '=' * 60)
print('✅ 所有图表生成完成！')
print('=' * 60)
print(f'保存位置：{save_dir}/')
print('  - 图1-5.png  (12×8英寸, 300 DPI)')
print('  - 图2.png    (12×8英寸, 300 DPI)')
print('  - 图3.png    (16×11英寸, 300 DPI)')
