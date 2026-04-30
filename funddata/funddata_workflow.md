# 场内基金全市场数据库 — 工作流程设计

> 创建时间: 2026-04-29
> 目标平台: Windows (E:\funddata\)
> 数据库类型: SQLite（跨平台，Mac/Windows 通用）
> 预计耗时: ~5小时

---

## 一、Tushare 接口权限检查

| 接口 | 功能 | 积分要求 | 2000积分是否够 | 频率限制 |
|------|------|---------|--------------|---------|
| fund_basic | 基金基本信息 | 120 | ✅ | 200次/分 |
| fund_daily | 日线行情 | 120 | ✅ | 200次/分 |
| fund_nav | 基金净值 | 2000 | ✅（刚好） | 200次/分 |
| fund_adj | 复权因子 | 2000 | ✅（刚好） | 200次/分 |
| fund_portfolio | 持仓明细 | 2000 | ✅（刚好） | 50次/分 |
| fund_share | 基金份额 | 2000 | ✅（刚好） | 200次/分 |
| fund_manager | 基金经理 | 2000 | ✅（刚好） | 200次/分 |
| fund_dividend | 分红送配 | 120 | ✅ | 200次/分 |

> ⚠️ **注意**: fund_nav、fund_adj、fund_portfolio 三个接口都在 2000 积分门槛上。
> 如果遇到权限不足，需要购买积分提升到 3000-5000。

---

## 二、数据库表结构设计

使用 SQLite 单文件数据库 `funddata.db`，存放在 `E:\funddata\`。

### 表 1: fund_basic（基金主表）

```sql
CREATE TABLE IF NOT EXISTS fund_basic (
    ts_code         TEXT PRIMARY KEY,  -- 基金代码 (如 510050.SH)
    name            TEXT,              -- 基金名称
    fund_type       TEXT,              -- 基金类型 (ETF/LOF/封闭式等)
    found_date      TEXT,              -- 成立日期
    due_date        TEXT,              -- 到期日期
    list_date       TEXT,              -- 上市日期
    issue_date      TEXT,              -- 发行日期
    delist_date     TEXT,              -- 退市日期
    issue_amount    REAL,              -- 发行份额(亿)
    m_fee           REAL,              -- 管理费
    c_fee           REAL,              -- 托管费
    benchmark       TEXT,              -- 业绩比较基准
    invest_type     TEXT,              -- 投资类型
    type            TEXT,              -- 基金风格
    trustee         TEXT,              -- 托管人
    management      TEXT,              -- 管理人
    custodian       TEXT,              -- 托管人(备用)
    duration_type   TEXT,              -- 存续期
    index_code      TEXT,              -- 跟踪指数代码
    p_value         REAL,              -- 面值
    min_amount      REAL,              -- 最低申购金额
    update_time     TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### 表 2: fund_daily（日线行情表）

```sql
CREATE TABLE IF NOT EXISTS fund_daily (
    ts_code     TEXT,
    trade_date  TEXT,
    pre_close   REAL,
    open        REAL,
    high        REAL,
    low         REAL,
    close       REAL,
    change      REAL,
    pct_chg     REAL,
    vol         REAL,
    amount      REAL,
    PRIMARY KEY (ts_code, trade_date)
);
```

### 表 3: fund_nav（净值表 — 核心大表）

```sql
CREATE TABLE IF NOT EXISTS fund_nav (
    ts_code     TEXT,
    end_date    TEXT,
    ann_date    TEXT,
    acc_nav     REAL,       -- 累计净值
    unit_nav    REAL,       -- 单位净值
    daily_return REAL,      -- 日增长率
    PRIMARY KEY (ts_code, end_date)
);
```

### 表 4: fund_adj（复权因子表）

```sql
CREATE TABLE IF NOT EXISTS fund_adj (
    ts_code     TEXT,
    trade_date  TEXT,
    adj_factor  REAL,
    PRIMARY KEY (ts_code, trade_date)
);
```

### 表 5: fund_portfolio（持仓明细表）

```sql
CREATE TABLE IF NOT EXISTS fund_portfolio (
    ts_code         TEXT,
    ann_date        TEXT,       -- 公告日期
    end_date        TEXT,       -- 截止日期
    symbol          TEXT,       -- 持仓股票代码
    stk_mkv_ratio   REAL,      -- 占净值比例
    stk_mkv         REAL,      -- 持仓市值
    stk_vol         REAL,      -- 持仓数量
    stk_number      INTEGER,   -- 持仓排名
    report_type     TEXT,       -- 报告类型
    PRIMARY KEY (ts_code, end_date, symbol)
);
```

### 表 6: fund_share（份额变动表）

```sql
CREATE TABLE IF NOT EXISTS fund_share (
    ts_code     TEXT,
    trade_date  TEXT,
    fd_share    REAL,       -- 基金份额(亿)
    PRIMARY KEY (ts_code, trade_date)
);
```

### 表 7: fund_manager（基金经理表）

```sql
CREATE TABLE IF NOT EXISTS fund_manager (
    ts_code     TEXT,
    name        TEXT,           -- 经理姓名
    gender      TEXT,           -- 性别
    edu_level   TEXT,           -- 学历
    begin_date  TEXT,           -- 任职日期
    end_date    TEXT,           -- 离任日期
    resume      TEXT,           -- 简历
    PRIMARY KEY (ts_code, begin_date, name)
);
```

### 表 8: fund_dividend（分红送配表）

```sql
CREATE TABLE IF NOT EXISTS fund_dividend (
    ts_code         TEXT,
    ann_date        TEXT,       -- 公告日期
    end_date        TEXT,       -- 分红年度
    record_date     TEXT,       -- 权益登记日
    ex_date         TEXT,       -- 除息日
    pay_date        TEXT,       -- 发放日
    dividend        REAL,       -- 每份分红
    plan_amount     REAL,       -- 预案金额
    execute_date    TEXT,       -- 决议日期
    imp_ann_date    TEXT,       -- 实施公告日
    PRIMARY KEY (ts_code, end_date, record_date)
);
```

### 索引设计

```sql
-- 常用查询索引
CREATE INDEX IF NOT EXISTS idx_nav_code ON fund_nav(ts_code);
CREATE INDEX IF NOT EXISTS idx_nav_date ON fund_nav(end_date);
CREATE INDEX IF NOT EXISTS idx_daily_code ON fund_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_daily_date ON fund_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_portfolio_code ON fund_portfolio(ts_code);
CREATE INDEX IF NOT EXISTS idx_portfolio_date ON fund_portfolio(end_date);
CREATE INDEX IF NOT EXISTS idx_adj_code ON fund_adj(ts_code);
CREATE INDEX IF NOT EXISTS idx_share_code ON fund_share(ts_code);
```

---

## 三、文件结构

```
E:\funddata\
├── funddata.db                  -- SQLite 数据库（主文件，可拷贝到Mac使用）
├── fund_downloader.py           -- 主下载脚本
├── config.py                    -- 配置文件（API路径、间隔等）
├── progress.json                -- 下载进度追踪
├── funddata_workflow.md         -- 本说明文件
└── logs\
    └── download_YYYYMMDD.log   -- 运行日志
```

---

## 四、下载策略与时间估算

### 执行顺序（从快到慢，先验证权限）

| 步骤 | 接口 | 预计记录数 | API调用次数 | 间隔 | 预计耗时 |
|------|------|-----------|------------|------|---------|
| 1 | fund_basic | ~12,000 | 1次 | 0s | 1分钟 |
| 2 | fund_manager | ~30,000 | ~12,000 | 0.3s | 60分钟 |
| 3 | fund_dividend | ~50,000 | ~12,000 | 0.3s | 60分钟 |
| 4 | fund_portfolio | ~500,000 | ~12,000 | 0.5s | 100分钟 |
| 5 | fund_share | ~1,000,000 | ~12,000 | 0.3s | 60分钟 |
| 6 | fund_adj | ~50,000,000 | ~12,000 | 0.3s | 60分钟 |
| 7 | fund_daily | ~50,000,000 | ~12,000 | 0.3s | 60分钟 |
| 8 | fund_nav | ~50,000,000 | ~12,000 | 0.5s | 100分钟 |

> **总计: ~5小时**

### 优化策略

1. **fund_basic 一次性获取全量**（1次调用）
2. **逐基金循环**: 遍历 fund_basic 中的 ts_code 列表
3. **断点续传**: progress.json 记录每个基金每个接口的完成状态
4. **失败重试**: 单个基金失败最多重试3次，间隔递增（5s/15s/30s）
5. **批量插入**: 使用 SQLAlchemy 的 bulk_insert，每 1000 条提交一次
6. **fund_nav 频率控制**: 使用 0.5s 间隔（最保守），避免触发限制

---

## 五、断点续传机制

progress.json 格式：

```json
{
    "start_time": "2026-04-29T10:00:00",
    "last_update": "2026-04-29T12:30:00",
    "fund_basic": "done",
    "fund_manager": {
        "completed": 5423,
        "total": 12000,
        "last_code": "159001.SZ"
    },
    "fund_dividend": "pending",
    "fund_portfolio": "pending",
    "fund_share": "pending",
    "fund_adj": "pending",
    "fund_daily": "pending",
    "fund_nav": "pending",
    "errors": []
}
```

---

## 六、脚本核心逻辑

```
fund_downloader.py 主流程:

1. 初始化
   ├── 读取 api_config.json 获取 token
   ├── 连接/创建 SQLite 数据库
   ├── 创建8张表 + 索引
   └── 读取 progress.json 恢复进度

2. Step 1: 下载 fund_basic（全量，1次调用）
   └── 写入 fund_basic 表

3. Step 2-8: 逐基金循环下载
   ├── 遍历 fund_basic.ts_code
   ├── 跳过 progress.json 中已完成的
   ├── 调用对应接口，获取数据
   ├── bulk_insert 写入数据库
   ├── 更新 progress.json
   └── time.sleep(interval) 频率控制

4. 完成后
   ├── 输出统计报告
   └── 关闭数据库连接
```

---

## 七、Windows 执行步骤

### 环境准备（5分钟）

```powershell
# 1. 创建目录
mkdir E:\funddata

# 2. 确认 Python 环境
python --version    # 需要 3.11+

# 3. 安装依赖
pip install tushare pandas tqdm sqlalchemy

# 4. 确认 api_config.json 中有 tushare token
#    位置: D:\cc-github\api_config.json
```

### 执行下载（~5小时）

```powershell
# 进入目录
cd E:\funddata

# 运行下载脚本
python fund_downloader.py

# 如果中断，重新运行同一命令即可（自动续传）
python fund_downloader.py
```

### 验证数据

```powershell
# 运行验证脚本
python fund_verify.py
```

---

## 八、Mac 端使用

```bash
# 从 Windows 拷贝 funddata.db 到 Mac（通过 Git/网盘/U盘）
# 直接用 Python 读取即可

import sqlite3
conn = sqlite3.connect('funddata.db')
df = pd.read_sql('SELECT * FROM fund_nav WHERE ts_code = "510050.SH"', conn)
```

---

## 九、风险提示

1. **积分不够**: 如果遇到权限不足报错，需要购买 Tushare 积分（建议提升到 3000+）
2. **网络中断**: 脚本支持断点续传，重新运行即可
3. **API限流**: 如果频繁触发限流，脚本会自动退避重试
4. **磁盘空间**: SQLite 数据库预计 2-5 GB，确保 E 盘有足够空间
5. **内存占用**: 使用 bulk_insert 批量提交，避免内存溢出

---

## 十、待确认事项

- [ ] Windows 端 Python 版本确认
- [ ] api_config.json 中 Tushare Token 确认可用
- [ ] E 盘剩余空间确认（建议 ≥10GB）
- [ ] 是否需要定时增量更新功能（daily_update）
