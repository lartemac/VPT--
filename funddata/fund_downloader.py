"""
场内基金全市场数据库下载器
功能: 从 Tushare Pro 下载全市场基金数据，存储到 SQLite 数据库
创建时间: 2026-04-29
创建系统: macOS → Windows 执行
平台检测: if os.name == 'nt': Windows, else: macOS/Linux
"""

import os
import sys
import json
import time
import sqlite3
import logging
import platform
from datetime import datetime
from pathlib import Path

import tushare as ts
import pandas as pd
from tqdm import tqdm

# 修复 brotli 解码兼容性问题
import tushare.pro.client as _tpc
_original_post = _tpc.requests.post
def _patched_post(*args, **kwargs):
    headers = kwargs.get('headers', {})
    if isinstance(headers, dict):
        headers['Accept-Encoding'] = 'gzip, deflate'
    kwargs['headers'] = headers
    return _original_post(*args, **kwargs)
_tpc.requests.post = _patched_post

# ============================================================
# 配置
# ============================================================

# 平台检测
if os.name == 'nt':
    BASE_DIR = Path('E:/funddata')
    # api_config.json 位置（Windows）
    API_CONFIG_PATH = Path('D:/cc-github/api_config.json')
else:
    BASE_DIR = Path.home() / 'Desktop' / 'funddata'
    API_CONFIG_PATH = Path.home() / 'Desktop' / 'VPT-初诊数据' / 'api_config.json'

DB_PATH = BASE_DIR / 'funddata.db'
PROGRESS_PATH = BASE_DIR / 'progress.json'
LOG_DIR = BASE_DIR / 'logs'

# API 调用间隔（秒）— 控制频率
INTERVAL_FAST = 0.31      # 200次/分钟 → 0.3s间隔
INTERVAL_SLOW = 0.51      # fund_nav / fund_portfolio 专用（保守）
INTERVAL_RETRY = 5        # 重试等待

# 批量插入大小
BATCH_SIZE = 1000

# ============================================================
# 日志
# ============================================================

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f'download_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# ============================================================
# Tushare 初始化
# ============================================================

def get_tushare_token():
    """从 api_config.json 读取 token"""
    # 尝试多个位置
    paths = [API_CONFIG_PATH]
    # 也尝试同目录下
    paths.append(BASE_DIR / 'api_config.json')
    # 也尝试环境变量
    env_token = os.environ.get('TUSHARE_TOKEN')
    if env_token:
        return env_token

    for p in paths:
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                config = json.load(f)
            # 支持多种结构
            if 'tushare' in config:
                return config['tushare'].get('token', '')
            if 'tushare_token' in config:
                return config['tushare_token']

    print("❌ 未找到 Tushare Token！")
    print(f"   已搜索: {[str(p) for p in paths]}")
    print("   请在 api_config.json 中配置 tushare.token")
    print("   或设置环境变量 TUSHARE_TOKEN")
    sys.exit(1)

# ============================================================
# 数据库
# ============================================================

CREATE_TABLES_SQL = """
-- 1. 基金主表
CREATE TABLE IF NOT EXISTS fund_basic (
    ts_code         TEXT PRIMARY KEY,
    name            TEXT,
    fund_type       TEXT,
    found_date      TEXT,
    due_date        TEXT,
    list_date       TEXT,
    issue_date      TEXT,
    delist_date     TEXT,
    issue_amount    REAL,
    m_fee           REAL,
    c_fee           REAL,
    benchmark       TEXT,
    invest_type     TEXT,
    type            TEXT,
    trustee         TEXT,
    management      TEXT,
    custodian       TEXT,
    duration_type   TEXT,
    index_code      TEXT,
    p_value         REAL,
    min_amount      REAL,
    update_time     TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 2. 日线行情
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

-- 3. 基金净值
CREATE TABLE IF NOT EXISTS fund_nav (
    ts_code     TEXT,
    end_date    TEXT,
    ann_date    TEXT,
    acc_nav     REAL,
    unit_nav    REAL,
    daily_return REAL,
    PRIMARY KEY (ts_code, end_date)
);

-- 4. 复权因子
CREATE TABLE IF NOT EXISTS fund_adj (
    ts_code     TEXT,
    trade_date  TEXT,
    adj_factor  REAL,
    PRIMARY KEY (ts_code, trade_date)
);

-- 5. 持仓明细
CREATE TABLE IF NOT EXISTS fund_portfolio (
    ts_code         TEXT,
    ann_date        TEXT,
    end_date        TEXT,
    symbol          TEXT,
    stk_mkv_ratio   REAL,
    stk_mkv         REAL,
    stk_vol         REAL,
    stk_number      INTEGER,
    report_type     TEXT,
    PRIMARY KEY (ts_code, end_date, symbol)
);

-- 6. 份额变动
CREATE TABLE IF NOT EXISTS fund_share (
    ts_code     TEXT,
    trade_date  TEXT,
    fd_share    REAL,
    PRIMARY KEY (ts_code, trade_date)
);

-- 7. 基金经理
CREATE TABLE IF NOT EXISTS fund_manager (
    ts_code     TEXT,
    name        TEXT,
    gender      TEXT,
    edu_level   TEXT,
    begin_date  TEXT,
    end_date    TEXT,
    resume      TEXT,
    PRIMARY KEY (ts_code, begin_date, name)
);

-- 8. 分红送配
CREATE TABLE IF NOT EXISTS fund_dividend (
    ts_code         TEXT,
    ann_date        TEXT,
    end_date        TEXT,
    record_date     TEXT,
    ex_date         TEXT,
    pay_date        TEXT,
    dividend        REAL,
    plan_amount     REAL,
    execute_date    TEXT,
    imp_ann_date    TEXT,
    PRIMARY KEY (ts_code, end_date, record_date)
);
"""

CREATE_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_nav_code ON fund_nav(ts_code);
CREATE INDEX IF NOT EXISTS idx_nav_date ON fund_nav(end_date);
CREATE INDEX IF NOT EXISTS idx_daily_code ON fund_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_daily_date ON fund_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_adj_code ON fund_adj(ts_code);
CREATE INDEX IF NOT EXISTS idx_share_code ON fund_share(ts_code);
CREATE INDEX IF NOT EXISTS idx_portfolio_code ON fund_portfolio(ts_code);
CREATE INDEX IF NOT EXISTS idx_portfolio_date ON fund_portfolio(end_date);
CREATE INDEX IF NOT EXISTS idx_dividend_code ON fund_dividend(ts_code);
"""

def init_database():
    """初始化数据库和表结构"""
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(CREATE_TABLES_SQL)
    conn.executescript(CREATE_INDEXES_SQL)
    conn.commit()
    return conn

# ============================================================
# 进度管理
# ============================================================

def load_progress():
    """加载下载进度"""
    if PROGRESS_PATH.exists():
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'start_time': datetime.now().isoformat(),
        'last_update': None,
        'fund_basic': 'pending',
        'fund_manager': 'pending',
        'fund_div': 'pending',
        'fund_portfolio': 'pending',
        'fund_share': 'pending',
        'fund_adj': 'pending',
        'fund_daily': 'pending',
        'fund_nav': 'pending',
        'completed_codes': {},  # {接口名: [已完成ts_code列表]}
        'errors': []
    }

def save_progress(progress):
    """保存下载进度"""
    progress['last_update'] = datetime.now().isoformat()
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

# ============================================================
# 数据下载函数
# ============================================================

def safe_bulk_insert(conn, table_name, df, logger):
    """安全批量插入数据，遇到主键冲突则跳过"""
    if df is None or df.empty:
        return 0
    # 只保留表中已有的列，避免列名不匹配
    cur = conn.execute(f"PRAGMA table_info({table_name})")
    db_cols = set(row[1] for row in cur.fetchall())
    df = df[[c for c in df.columns if c in db_cols]]
    if df.empty:
        return 0
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False, method='multi')
        return len(df)
    except Exception as e:
        logger.warning(f"  bulk insert failed, fallback to row-by-row: {e}")
        count = 0
        cols = list(df.columns)
        placeholders = ','.join(['?' for _ in cols])
        insert_sql = f"INSERT OR IGNORE INTO {table_name} ({','.join(cols)}) VALUES ({placeholders})"
        for _, row in df.iterrows():
            try:
                conn.execute(insert_sql, tuple(row[c] for c in cols))
                count += 1
            except Exception:
                pass
        conn.commit()
        return count

def download_fund_basic(pro, conn, progress, logger):
    """Step 1: 下载基金基本信息（1次调用）"""
    logger.info("=" * 50)
    logger.info("Step 1/8: 下载 fund_basic（基金基本信息）")

    if progress.get('fund_basic') == 'done':
        logger.info("  [SKIP] 已完成，跳过")
        return True

    try:
        df = pro.fund_basic(market='E')  # E=场内基金
        if df is None or df.empty:
            df = pro.fund_basic()

        if df is not None and not df.empty:
            listed = df[df['list_date'].notna()].copy()
            # 标准化列名为小写
            listed.columns = [c.lower() for c in listed.columns]
            # 只保留表中已有的列
            cur = conn.execute("PRAGMA table_info(fund_basic)")
            db_cols = [row[1] for row in cur.fetchall()]
            listed = listed[[c for c in listed.columns if c in db_cols]]
            count = safe_bulk_insert(conn, 'fund_basic', listed, logger)
            conn.commit()
            if count > 0:
                progress['fund_basic'] = 'done'
                save_progress(progress)
                logger.info(f"  [OK] 完成: {count} 只基金")
            else:
                logger.error(f"  [FAIL] 写入0条，数据可能有问题")
            return count > 0
        else:
            logger.error("  [FAIL] fund_basic 返回空数据")
            return False
    except Exception as e:
        logger.error(f"  [FAIL] fund_basic 失败: {e}")
        return False

def download_per_fund(pro, conn, progress, api_name, table_name, logger,
                      interval=0.31, extra_params=None):
    """通用: 逐基金下载并写入数据库"""
    logger.info("=" * 50)
    logger.info(f"下载 {api_name} → {table_name}")

    if progress.get(api_name) == 'done':
        logger.info("  [SKIP] 已完成，跳过")
        return

    # 获取基金列表
    codes_df = pd.read_sql('SELECT ts_code FROM fund_basic', conn)
    all_codes = codes_df['ts_code'].tolist()

    # 已完成的基金
    completed = set(progress.get('completed_codes', {}).get(api_name, []))
    remaining = [c for c in all_codes if c not in completed]

    logger.info(f"  总计: {len(all_codes)}, 已完成: {len(completed)}, 剩余: {len(remaining)}")

    if not remaining:
        progress[api_name] = 'done'
        save_progress(progress)
        logger.info("  [SKIP] 全部已完成")
        return

    # 初始化进度记录
    if api_name not in progress.get('completed_codes', {}):
        if 'completed_codes' not in progress:
            progress['completed_codes'] = {}
        progress['completed_codes'][api_name] = list(completed)

    api_func = getattr(pro, api_name)
    total_records = 0
    error_count = 0

    pbar = tqdm(remaining, desc=api_name, unit='基金')

    for ts_code in pbar:
        retries = 0
        success = False

        while retries < 3 and not success:
            try:
                params = {'ts_code': ts_code}
                if extra_params:
                    params.update(extra_params)

                # 某些接口限制单次返回条数，需要分页
                df = api_func(**params)

                if df is not None and not df.empty:
                    # 标准化列名
                    df.columns = [c.lower() for c in df.columns]
                    count = safe_bulk_insert(conn, table_name, df, logger)
                    total_records += count

                success = True
                # 记录完成
                progress['completed_codes'][api_name].append(ts_code)

                # 每50只基金保存一次进度
                if len(progress['completed_codes'][api_name]) % 50 == 0:
                    save_progress(progress)
                    conn.commit()

                pbar.set_postfix({'records': total_records, 'errors': error_count})

            except Exception as e:
                retries += 1
                error_count += 1
                err_msg = str(e)

                if '每分钟' in err_msg or 'limit' in err_msg.lower() or '频率' in err_msg:
                    logger.warning(f"  [WARN] 频率限制，等待30秒... ({ts_code})")
                    time.sleep(30)
                elif '权限' in err_msg or '积分' in err_msg:
                    logger.error(f"  [FAIL] 权限不足: {err_msg}")
                    logger.error("  [TIP] 请购买 Tushare 积分后重试")
                    progress['errors'].append({
                        'api': api_name, 'code': ts_code,
                        'error': err_msg, 'time': datetime.now().isoformat()
                    })
                    save_progress(progress)
                    return  # 停止当前接口
                else:
                    logger.warning(f"  [WARN] 重试 {retries}/3: {ts_code} - {err_msg}")
                    time.sleep(INTERVAL_RETRY * retries)

        if not success:
            progress['errors'].append({
                'api': api_name, 'code': ts_code,
                'error': f'3次重试失败', 'time': datetime.now().isoformat()
            })

        # 频率控制
        time.sleep(interval)

    # 完成
    conn.commit()
    progress[api_name] = 'done'
    save_progress(progress)
    logger.info(f"  [OK] {api_name} 完成: {total_records} 条记录, {error_count} 个错误")

# ============================================================
# 主函数
# ============================================================

def main():
    # 修复 Windows 编码问题
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    print("""
==================================================
  场内基金全市场数据库下载器 v1.1
  数据源: Tushare Pro
  存储: SQLite (funddata.db)
  支持断点续传，中断后重新运行即可
==================================================
    """)

    # 初始化日志
    logger = setup_logging()
    logger.info(f"平台: {platform.system()} {platform.release()}")
    logger.info(f"Python: {platform.python_version()}")
    logger.info(f"数据库: {DB_PATH}")

    # 获取 Token
    token = get_tushare_token()
    ts.set_token(token)
    pro = ts.pro_api()
    logger.info("[OK] Tushare 连接成功")

    # 测试权限
    try:
        test = pro.fund_basic(market='E')
        logger.info(f"[OK] fund_basic 权限正常, 返回 {len(test) if test is not None else 0} 条")
    except Exception as e:
        logger.error(f"[FAIL] fund_basic 权限测试失败: {e}")
        sys.exit(1)

    # 初始化数据库
    conn = init_database()
    logger.info(f"[OK] 数据库初始化完成: {DB_PATH}")

    # 加载进度
    progress = load_progress()
    logger.info(f"[OK] 进度加载完成")

    start_time = time.time()

    # Step 1: fund_basic
    download_fund_basic(pro, conn, progress, logger)

    # Step 2: fund_manager（经理变动，数据量小）
    download_per_fund(pro, conn, progress, 'fund_manager', 'fund_manager',
                     logger, interval=INTERVAL_FAST)

    # Step 3: fund_div（分红送配，数据量小）
    download_per_fund(pro, conn, progress, 'fund_div', 'fund_dividend',
                     logger, interval=INTERVAL_FAST)

    # Step 4: fund_portfolio（持仓明细，频率限制严格）
    download_per_fund(pro, conn, progress, 'fund_portfolio', 'fund_portfolio',
                     logger, interval=INTERVAL_SLOW)

    # Step 5: fund_share（份额变动）
    download_per_fund(pro, conn, progress, 'fund_share', 'fund_share',
                     logger, interval=INTERVAL_FAST)

    # Step 6: fund_adj（复权因子）— 需要5000积分，2000积分跳过
    # download_per_fund(pro, conn, progress, 'fund_adj', 'fund_adj',
    #                  logger, interval=INTERVAL_FAST)

    # Step 7: fund_daily（日线行情，数据量大）
    download_per_fund(pro, conn, progress, 'fund_daily', 'fund_daily',
                     logger, interval=INTERVAL_FAST)

    # Step 8: fund_nav（净值数据，数据量最大，最耗时）
    download_per_fund(pro, conn, progress, 'fund_nav', 'fund_nav',
                     logger, interval=INTERVAL_SLOW)

    # 完成
    elapsed = time.time() - start_time
    hours = elapsed / 3600

    print(f"""
==================================================
  [OK] 下载完成！
  耗时: {hours:.1f} 小时
  数据库: {DB_PATH}
  大小: {DB_PATH.stat().st_size / 1024 / 1024:.0f} MB
==================================================
    """)

    # 输出统计
    logger.info("=" * 50)
    logger.info("数据统计:")
    for table in ['fund_basic', 'fund_daily', 'fund_nav', 'fund_adj',
                   'fund_portfolio', 'fund_share', 'fund_manager', 'fund_dividend']:
        count = pd.read_sql(f'SELECT COUNT(*) as cnt FROM {table}', conn).iloc[0, 0]
        logger.info(f"  {table:20s}: {count:>10,} 条")

    conn.close()

if __name__ == '__main__':
    main()
