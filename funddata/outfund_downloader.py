"""
场外基金全市场数据库下载器
功能: 从 Tushare Pro 下载全部场外基金数据，存储到 SQLite 数据库
存储: E:\\funddata\\outfunddata.db
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

# 修复 brotli 解码兼容性
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
if os.name == 'nt':
    BASE_DIR = Path('E:/funddata')
    API_CONFIG_PATH = Path('D:/cc-github/api_config.json')
else:
    BASE_DIR = Path.home() / 'Desktop' / 'funddata'
    API_CONFIG_PATH = Path.home() / 'cc-github' / 'api_config.json'

DB_PATH = BASE_DIR / 'outfunddata.db'
PROGRESS_PATH = BASE_DIR / 'outfund_progress.json'
LOG_DIR = BASE_DIR / 'logs'

INTERVAL_FAST = 0.31
INTERVAL_SLOW = 0.51

# ============================================================
# 日志
# ============================================================
def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f'outfund_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
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
    paths = [API_CONFIG_PATH, BASE_DIR / 'api_config.json']
    env_token = os.environ.get('TUSHARE_TOKEN')
    if env_token:
        return env_token
    for p in paths:
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if 'tushare' in config:
                return config['tushare'].get('token', '')
            if 'tushare_token' in config:
                return config['tushare_token']
    sys.exit("未找到 Tushare Token")

# ============================================================
# 数据库
# ============================================================
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS fund_basic (
    ts_code TEXT PRIMARY KEY, name TEXT, fund_type TEXT,
    found_date TEXT, due_date TEXT, list_date TEXT, issue_date TEXT,
    delist_date TEXT, issue_amount REAL, m_fee REAL, c_fee REAL,
    benchmark TEXT, invest_type TEXT, type TEXT, trustee TEXT,
    management TEXT, custodian TEXT, duration_type TEXT,
    index_code TEXT, p_value REAL, min_amount REAL,
    update_time TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS fund_daily (
    ts_code TEXT, trade_date TEXT, pre_close REAL, open REAL,
    high REAL, low REAL, close REAL, change REAL, pct_chg REAL,
    vol REAL, amount REAL, PRIMARY KEY (ts_code, trade_date)
);
CREATE TABLE IF NOT EXISTS fund_nav (
    ts_code TEXT, end_date TEXT, ann_date TEXT,
    acc_nav REAL, unit_nav REAL, daily_return REAL,
    PRIMARY KEY (ts_code, ann_date)
);
CREATE TABLE IF NOT EXISTS fund_portfolio (
    ts_code TEXT, ann_date TEXT, end_date TEXT, symbol TEXT,
    stk_mkv_ratio REAL, stk_mkv REAL, stk_vol REAL,
    stk_number INTEGER, report_type TEXT,
    PRIMARY KEY (ts_code, end_date, symbol)
);
CREATE TABLE IF NOT EXISTS fund_share (
    ts_code TEXT, trade_date TEXT, fd_share REAL,
    PRIMARY KEY (ts_code, trade_date)
);
CREATE TABLE IF NOT EXISTS fund_manager (
    ts_code TEXT, name TEXT, gender TEXT, edu_level TEXT,
    begin_date TEXT, end_date TEXT, resume TEXT,
    PRIMARY KEY (ts_code, begin_date, name)
);
CREATE TABLE IF NOT EXISTS fund_dividend (
    ts_code TEXT, ann_date TEXT, end_date TEXT, record_date TEXT,
    ex_date TEXT, pay_date TEXT, dividend REAL, plan_amount REAL,
    execute_date TEXT, imp_ann_date TEXT,
    PRIMARY KEY (ts_code, end_date, record_date)
);
"""
CREATE_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_nav_code ON fund_nav(ts_code);
CREATE INDEX IF NOT EXISTS idx_nav_date ON fund_nav(ann_date);
CREATE INDEX IF NOT EXISTS idx_daily_code ON fund_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_daily_date ON fund_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_portfolio_code ON fund_portfolio(ts_code);
CREATE INDEX IF NOT EXISTS idx_portfolio_date ON fund_portfolio(end_date);
CREATE INDEX IF NOT EXISTS idx_share_code ON fund_share(ts_code);
CREATE INDEX IF NOT EXISTS idx_dividend_code ON fund_dividend(ts_code);
"""

def init_database():
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
        'fund_daily': 'pending',
        'fund_nav': 'pending',
        'completed_codes': {},
        'errors': []
    }

def save_progress(progress):
    progress['last_update'] = datetime.now().isoformat()
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

# ============================================================
# 数据写入
# ============================================================
def safe_bulk_insert(conn, table_name, df, logger):
    if df is None or df.empty:
        return 0
    cur = conn.execute(f"PRAGMA table_info({table_name})")
    db_cols = set(row[1] for row in cur.fetchall())
    df = df[[c for c in df.columns if c in db_cols]]
    if df.empty:
        return 0
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False, method='multi')
        return len(df)
    except Exception as e:
        logger.warning(f"  bulk insert failed, fallback: {e}")
        count = 0
        cols = list(df.columns)
        placeholders = ','.join(['?' for _ in cols])
        sql = f"INSERT OR IGNORE INTO {table_name} ({','.join(cols)}) VALUES ({placeholders})"
        for _, row in df.iterrows():
            try:
                conn.execute(sql, tuple(row[c] for c in cols))
                count += 1
            except Exception:
                pass
        conn.commit()
        return count

# ============================================================
# 下载函数
# ============================================================
def download_fund_basic(pro, conn, progress, logger):
    logger.info("Step 1/7: 下载 fund_basic（全部场外基金）")
    if progress.get('fund_basic') == 'done':
        logger.info("  [SKIP] 已完成")
        return True
    try:
        # 获取全部基金
        df = pro.fund_basic()
        if df is None or df.empty:
            logger.error("  [FAIL] fund_basic 返回空")
            return False
        total = len(df)
        # 场外基金: 没有 list_date 或 list_date 为空（未在场内上市）
        # 实际上我们想要全部基金（排除已退市的），让后续筛选更灵活
        active = df[df['delist_date'].isna()].copy()
        listed = df[df['list_date'].notna() & df['delist_date'].isna()].copy()
        # 场外 = 全部活跃 - 场内上市
        # 但为简单起见，下载全部活跃基金，用户可后续筛选
        active.columns = [c.lower() for c in active.columns]
        cur = conn.execute("PRAGMA table_info(fund_basic)")
        db_cols = set(row[1] for row in cur.fetchall())
        active = active[[c for c in active.columns if c in db_cols]]
        count = safe_bulk_insert(conn, 'fund_basic', active, logger)
        conn.commit()
        if count > 0:
            progress['fund_basic'] = 'done'
            save_progress(progress)
            logger.info(f"  [OK] 完成: {count} 只基金 (全部活跃, 含场内+场外)")
        else:
            logger.error(f"  [FAIL] 写入0条")
        return count > 0
    except Exception as e:
        logger.error(f"  [FAIL] {e}")
        return False

def download_per_fund(pro, conn, progress, api_name, table_name, logger,
                      interval=0.31):
    logger.info(f"下载 {api_name} -> {table_name}")
    if progress.get(api_name) == 'done':
        logger.info("  [SKIP] 已完成")
        return

    codes_df = pd.read_sql('SELECT ts_code FROM fund_basic', conn)
    all_codes = codes_df['ts_code'].tolist()
    completed = set(progress.get('completed_codes', {}).get(api_name, []))
    remaining = [c for c in all_codes if c not in completed]

    logger.info(f"  总计: {len(all_codes)}, 已完成: {len(completed)}, 剩余: {len(remaining)}")
    if not remaining:
        progress[api_name] = 'done'
        save_progress(progress)
        return

    if api_name not in progress.get('completed_codes', {}):
        if 'completed_codes' not in progress:
            progress['completed_codes'] = {}
        progress['completed_codes'][api_name] = list(completed)

    api_func = getattr(pro, api_name)
    total_records = 0
    error_count = 0
    pbar = tqdm(remaining, desc=api_name, unit='fund')

    for ts_code in pbar:
        retries = 0
        success = False
        while retries < 3 and not success:
            try:
                df = api_func(ts_code=ts_code)
                if df is not None and not df.empty:
                    df.columns = [c.lower() for c in df.columns]
                    count = safe_bulk_insert(conn, table_name, df, logger)
                    total_records += count
                success = True
                progress['completed_codes'][api_name].append(ts_code)
                if len(progress['completed_codes'][api_name]) % 50 == 0:
                    save_progress(progress)
                    conn.commit()
                pbar.set_postfix({'records': total_records, 'errors': error_count})
            except Exception as e:
                retries += 1
                error_count += 1
                err_msg = str(e)
                if '每分钟' in err_msg or 'limit' in err_msg.lower() or '频率' in err_msg:
                    logger.warning(f"  [WARN] 频率限制, 等待30s ({ts_code})")
                    time.sleep(30)
                elif '权限' in err_msg or '积分' in err_msg:
                    logger.error(f"  [FAIL] 权限不足: {err_msg}")
                    save_progress(progress)
                    return
                else:
                    logger.warning(f"  [WARN] 重试 {retries}/3: {ts_code} - {err_msg}")
                    time.sleep(5 * retries)
        if not success:
            progress['errors'].append({
                'api': api_name, 'code': ts_code,
                'error': '3次重试失败', 'time': datetime.now().isoformat()
            })
        time.sleep(interval)

    conn.commit()
    progress[api_name] = 'done'
    save_progress(progress)
    logger.info(f"  [OK] {api_name}: {total_records} 条, {error_count} 错误")

# ============================================================
# 主函数
# ============================================================
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    print("=" * 50)
    print("  场外基金全市场数据库下载器 v1.0")
    print(f"  存储: {DB_PATH}")
    print("  支持断点续传")
    print("=" * 50)

    logger = setup_logging()
    logger.info(f"平台: {platform.system()} | Python: {platform.python_version()}")

    token = get_tushare_token()
    ts.set_token(token)
    pro = ts.pro_api()
    logger.info("[OK] Tushare 连接成功")

    # 测试
    try:
        test = pro.fund_basic()
        logger.info(f"[OK] fund_basic 权限正常, 返回 {len(test)} 条")
    except Exception as e:
        logger.error(f"[FAIL] 权限测试失败: {e}")
        sys.exit(1)

    conn = init_database()
    logger.info(f"[OK] 数据库初始化: {DB_PATH}")
    progress = load_progress()

    start_time = time.time()

    # Step 1: fund_basic (全部基金)
    download_fund_basic(pro, conn, progress, logger)

    # 检查场外基金数量
    total_funds = pd.read_sql('SELECT COUNT(*) as c FROM fund_basic', conn).iloc[0, 0]
    on_exchange = pd.read_sql("SELECT COUNT(*) as c FROM fund_basic WHERE list_date IS NOT NULL", conn).iloc[0, 0]
    off_exchange = total_funds - on_exchange
    logger.info(f"  全部基金: {total_funds}, 场内: {on_exchange}, 场外: {off_exchange}")

    # Step 2-7: 逐基金下载
    download_per_fund(pro, conn, progress, 'fund_manager', 'fund_manager',
                     logger, interval=INTERVAL_FAST)
    download_per_fund(pro, conn, progress, 'fund_div', 'fund_dividend',
                     logger, interval=INTERVAL_FAST)
    download_per_fund(pro, conn, progress, 'fund_portfolio', 'fund_portfolio',
                     logger, interval=INTERVAL_SLOW)
    download_per_fund(pro, conn, progress, 'fund_share', 'fund_share',
                     logger, interval=INTERVAL_FAST)
    download_per_fund(pro, conn, progress, 'fund_daily', 'fund_daily',
                     logger, interval=INTERVAL_FAST)
    download_per_fund(pro, conn, progress, 'fund_nav', 'fund_nav',
                     logger, interval=INTERVAL_SLOW)

    # 统计
    elapsed = (time.time() - start_time) / 3600
    size_mb = DB_PATH.stat().st_size / 1024 / 1024

    logger.info("=" * 50)
    logger.info(f"下载完成! 耗时: {elapsed:.1f}h, 大小: {size_mb:.0f}MB")
    for table in ['fund_basic','fund_daily','fund_nav','fund_portfolio',
                   'fund_share','fund_manager','fund_dividend']:
        count = pd.read_sql(f'SELECT COUNT(*) as c FROM {table}', conn).iloc[0, 0]
        logger.info(f"  {table:20s}: {count:>12,}")
    conn.close()

if __name__ == '__main__':
    main()
