---
name: 基金研究 Skill
description: 单支基金全面分析标准工作流v3（Tushare分批查询+搜索Agent+Python生成HTML+净值曲线图），016520/024240/017998/006195/001917验证通过
type: feedback
originSessionId: ae47c039-7b09-453e-bdcb-c20fcda83775
---

## 基金研究 Skill（单支基金全面分析工作流）

当用户要求"分析XXX基金""研究XX代码的基金""帮我全面分析某基金"时，严格按以下流程执行。

### 触发条件
用户提到具体基金代码（如 016520、005820）或基金名称，要求全面分析/研究/出报告。

---

## 第一步：数据采集（并行执行）

### 1A. Tushare 数据查询（拆分为独立脚本，避免单点失败）

**脚本1：基础信息 + 经理 + 净值 + 分红 + 净值曲线图（核心数据，优先执行）**
```python
# 用 tushare pro API，token 从 D:\cc-github\api_config.json → cfg['tushare']['token'] 读取
ts_code = 'XXXXXX.OF'  # 用户给的代码 + .OF 后缀

# 查询接口及关键参数：
pro.fund_basic(ts_code=ts_code)        # 基金名称、类型、成立日期、费率、业绩基准、管理人
pro.fund_manager(ts_code=ts_code)      # 历任基金经理、任职/离任日期、简历
pro.fund_nav(ts_code=ts_code)          # 全量历史净值（unit_nav, accum_nav, net_asset, ann_date）
pro.fund_div(ts_code=ts_code)          # 分红记录

# 完成后输出 JSON 汇总文件（summary_XXXXXX.json）+ base64 图表文件（nav_b64_XXXXXX.txt）
```

**关键标记项**：
1. 历史最高点（蓝色圆点 + 日期 + 净值）
2. 最大回撤点（红色三角 + 回撤百分比 + 日期 + 净值）
3. 回撤修复点（绿色方块 + 修复日期 + 修复耗时天数）
4. 回撤区间阴影（红色半透明背景）
5. 净值曲线下方浅色填充

**脚本2：持仓 + 份额（独立脚本，含异常处理）**
```python
# fund_portfolio 查询大数据集时可能触发 brotli 解码错误
# 解决方案：按年份分批查询，失败时自动重试

for yr in ['2026', '2025', '2024', '2023']:
    try:
        df = pro.fund_portfolio(ts_code=ts_code, end_date=f'{yr}1231')
        all_data.append(df)
    except Exception:
        pass  # 跳过失败年份，用搜索数据补充
    time.sleep(1)

# 合并去重后输出 portfolio_XXXXXX.json
pro.fund_share(ts_code=ts_code)       # 份额变动（trade_date, fd_share）
# 输出 shares_XXXXXX.json
```
```python
# 注意事项：
# - fund_share 的列名是 trade_date（非 end_date）、fd_share
# - fund_nav 的 net_asset 字段单位是元（需 /10000 得万元，/100000000 得亿元）
# - fund_portfolio 的列名是 mkv/amount/stk_mkv_ratio（非 hold_amount）

# 收益率计算逻辑：
# 1. 按年分组，年初/年末净值 → 年度收益率
# 2. 成立以来总收益率 = (最新净值 / 最早净值 - 1)
# 3. 最大回撤 = cummax 差值的最小值
# 4. 年化波动率 = 日收益率标准差 × sqrt(252)
# 5. 近1年/3年/6月收益率
# 6. 近3年年化收益率 = (总收益)^(1/年数) - 1
```

**第三轮：份额变动 + 股票名称映射 + 行业分布**
```python
pro.fund_share(ts_code=ts_code)       # 份额变动（trade_date, fd_share）
# 按行业汇总 mkv → 行业占比
# 按报告期取最近4期，每期展示前10-15只重仓股
```

**重要：股票名称查询——必须确保报告中不出现"未知"**

用户本地有完整的A股数据库（Tushare Pro 已下载），持仓中所有股票的名称和行业必须查全，不允许出现"未知"。

**查询策略（优先使用本地数据库）**：
1. **首选**：用 `pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')` 一次性获取全部A股名称+行业，建立本地字典（约5000条），然后用 `df['symbol'].map(stock_dict)` 批量映射
2. **备选**：如果全量查询失败，对持仓中的 `symbol` 逐只查询 `pro.stock_basic(ts_code=sym)`，但不受80只限制——必须查完所有持仓股票，每20只 sleep 0.3秒
3. **兜底**：若仍有遗漏，用 Grep 工具在本地数据库文件中搜索代码对应的名称
4. **禁止**：在最终HTML报告中出现股票名称为"未知"的情况——如有未查到的股票，用 Grep 在网上搜索补充

**Tushare 常见坑（已验证）**：
- `fund_share` 排序列名是 `trade_date` 不是 `ann_date` 或 `end_date`
- `fund_portfolio` 没有 `hold_amount`/`hold_ratio`，实际列名是 `mkv`/`stk_mkv_ratio`
- `fund_nav` 的 `net_asset` 仅在季末/年末报告期有值（非每天更新），单位是元
- `adj_nav`（复权净值）需要 5000 积分，2000 积分可能查不到 → 跳过
- 场外基金的 `fund_share.fd_share` 单位是万份
- **brotli 解码错误**：`fund_portfolio` 查询大数据集（持仓超1000只的量化基金）时可能触发 `urllib3.exceptions.DecodeError`，解决方案是按年份分批查询（`end_date=YYYY1231`），每批 sleep 1秒
- **API config 路径**：token 在 `cfg['tushare']['token']`（非 `cfg['tushare_token']`）

### 1B. 联网搜索（后台 Agent 并行）

派出后台搜索 Agent，按以下关键词分次搜索：
1. `"基金代码+基金名称" 基金经理 管理规模 履历`
2. `"基金名称" 历年收益率 排名 2024 2025 2026`
3. `"基金名称" 卡玛比率 夏普比率 最大回撤 风险指标`
4. `"基金名称" 机构持有 持有人结构 机构占比`
5. `"基金名称" 处罚 违规 警告 负面新闻 监管`
6. `"基金名称" 仓位变动 资产配置 2024 2025`
7. `"基金名称" 同类排名 晨星评级 银河证券`

搜索目标网站优先级：天天基金网 > 雪球基金 > 东方财富 > 好买基金 > 晨星

**补充数据获取**：当 Tushare 持仓数据缺失时，用 webReader 工具读取天天基金网页补充：
- `https://fund.eastmoney.com/XXXXXX.html` — 基本信息、阶段涨幅、持仓
- 注意：天天基金网页部分数据为 JS 动态渲染，webReader 可能无法获取完整持有人结构

---

## 第二步：数据分析与整合

### 必须计算的指标
| 指标 | 计算方法 |
|------|---------|
| 年度收益率 | 每年(年末净值/上年末净值 - 1) |
| 成立以来总收益 | (最新净值/最早净值 - 1) |
| 近1/3/6月收益率 | 对应日期净值比较 |
| 近3年年化 | (总收益)^(1/年数) - 1 |
| 最大回撤 | min((净值-累计最大值)/累计最大值) |
| 年化波动率 | 日收益标准差 × sqrt(252) |
| 行业集中度 | 前三大行业占股票市值比 |
| 规模趋势 | 各报告期净资产连线 |

### 必须交叉验证的信息
- 基金经理是否变更（Tushare fund_manager 可能未更新，需与搜索结果比对）
- 年度收益率数据（不同来源可能有分红再投资/不复权差异）
- 基金规模（Tushare net_asset 与搜索到的规模数据对比）

---

## 第三步：报告生成

### 重要：直接生成 HTML 报告，不生成 MD 文件
用户要求最终报告为 HTML 格式（美观、可直接浏览器打开），省去 MD→HTML 转换步骤。
由于 HTML 内含 base64 图表（10-17万字符），超过 Write 工具合理长度，改用 Python 脚本生成：
1. 读取 nav_b64_XXXXXX.txt + summary_XXXXXX.json + shares_XXXXXX.json + portfolio_XXXXXX.json
2. Python f-string 拼接完整 HTML（注意 f-string 中 `s["key"]` 的引号转义问题）
3. 写入 `桌面/XXXXXX全面报告.html`
4. 执行后删除所有临时文件（脚本 + JSON + base64 文本）

### HTML 报告结构（13章，严格遵循）

```
页头（.header）：标题 + 基金代码 + 报告日期 + 数据来源

核心指标卡片（.score-bar，6个）：
  成立收益 | 近1年收益 | 近3年年化 | 最大回撤 | 晨星评级 | 基金规模

一、基金基本信息（.section）
  - 表格：全称、类型、成立日期、管理人、托管人、费率、业绩基准、是否分红
  - 份额说明（info-box）

二、基金经理变动及履历（.section）
  - 历任经理表格（在任者高亮绿色背景）
  - 现任经理详情（学历、履历列表、在管基金表格）
  - 经理风格分析（info-box）

三、净值走势曲线（.section）
  - 嵌入 base64 编码的 PNG 净值曲线图（width:100%）
  - 图例说明（历史最高/最大回撤/回撤修复 的颜色含义）
  - 图下方标注关键数据摘要行

四、历年收益率表现（.section）
  - 年度收益率表格（绿涨红跌）
  - 区间收益率汇总
  - 关键观察（有序列表）

五、风险指标分析（.section）
  - 核心风险指标表格
  - 风险等级评定表格
  - 持有盈利概率表格

六、基金规模变动（.section）
  - 份额变动表格 + 可视化进度条（.progress-bar）
  - 净资产变动表格（万元+亿元双列）
  - 规模分析（warn-box 提示清盘风险）

七、投资方向与持仓详情（.section）
  - 投资风格表格
  - 十大重仓股表格（行业 tag 标签）
  - 行业分布表格 + 可视化进度条
  - 持仓分析（warn-box 提示集中度风险）
  - 历史持仓变迁表格

八、仓位变动情况（.section）
  - 大类资产配置表格（关键转折点绿色背景高亮）
  - 仓位核心发现（info-box）

九、机构投资者与持有人结构（.section）
  - 持有人结构表格（机构大举入场行绿色高亮）
  - 机构动向分析（info-box）

十、同类基金收益对比（.section）
  - 同类排名表格（优秀/良好 tag）
  - 与基准对比表格（超额收益高亮）
  - 风险收益对比表格

十一、负面信息与风险提示（.section）
  - 已核实信息列表
  - 核心风险点 → 红色边框卡片网格（.risk-grid > .risk-item）
    - risk-high（红色左边框）、risk-mid（橙色左边框）
  - 补充建议

十二、深度解读与投资建议（.section）
  - 基金画像总结（warn-box，一句话定位 + 4条结论）
  - 适合/不适合投资者对比表
  - 关键关注指标列表
  - 综合评分表格（金色星级 ★ + 空星 ☆）

十三、重要数据附录（.section）
  - 净值走势关键节点表格（最新行绿色高亮）
  - 全部经理履历表格：现任经理行高亮绿色+标注"现任"，离任经理行标注"前任"（不可省略"前任"标签，否则读者会误以为仍是现任经理）

页脚（.footer）：免责声明 + 数据来源 + 报告时间
```

### HTML 样式规范（内嵌 CSS，无外部依赖）

```
配色方案：
  主色: #2b6cb0 / #3182ce（蓝色系）
  涨: #38a169（绿）/ 跌: #e53e3e（红）
  警告: #dd6b20（橙）/ 星级: #d69e2e（金）
  背景: #f8f9fa / 卡片: #ffffff / 边框: #e2e8f0

布局：
  body: max-width 1100px, margin auto, padding 20px
  .header: 渐变蓝背景(#1a365d→#2b6cb0), 12px圆角, 白字
  .score-bar: flex布局, 6个指标卡片
  .score-card: flex:1, min-width:150px, 居中, 边框阴影
  .section: 白色卡片, 10px圆角, 28px内边距, 底部间距20px

组件：
  .tag / .tag-green / .tag-red / .tag-blue / .tag-orange: pill badge
  .warn-box: 黄色背景(#fffbeb) + 黄色边框, 圆角8px
  .info-box: 蓝色背景(#ebf8ff) + 蓝色边框, 圆角8px
  .risk-grid: CSS Grid, 列宽minmax(280px,1fr)
  .risk-item: 红色背景(#fff5f5), 左边框4px
  .progress-bar: 高8px, 灰色底(#edf2f7), 圆角4px
  .star: 金色 #d69e2e / .star-empty: 灰色 #cbd5e0
  table: 全宽, thead灰底, tbody悬停高亮(#f7fafc)
  .up: 绿色加粗 / .down: 红色加粗

响应式：
  @media (max-width: 768px): 缩小padding/字号
```

### 文件保存
- HTML 文件：`桌面/XXXXXX全面报告.html`（唯一输出文件）
- 临时查询脚本：用完即删（rm 清理）

---

## 质量标准

1. **数据必须来自两个以上独立来源**（Tushare + 联网搜索）
2. **所有收益率必须有原始净值佐证**（不引用未经验证的第三方数据）
3. **风险提示必须包含至少5个风险点**，按高/中分级
4. **综合评分必须给出明确结论**（几星 + 一句话总结）
5. **行业分析必须量化**（具体百分比，非模糊描述）
6. **经理分析必须包含履历和在管基金列表**
7. **负面信息搜索不可省略**，即使结果为"未发现"

## Why: 用户评价本次016520分析"完成的非常好"，要求将此流程固化为可复用的skill。后续用户要求去掉MD中间文件，直接生成HTML报告，更加美观高效。
## How to apply: 每当用户说"分析某基金""研究XX基金""帮我看看XXX基金"时，自动启用此skill，直接生成HTML报告，无需用户再次说明流程
