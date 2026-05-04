---
name: 基金数据库项目（场内+场外）
description: 基于 Tushare Pro 的场内+场外基金全市场 SQLite 数据库，含多维度筛选工具
type: project
originSessionId: 99bb7435-c83d-4153-8d7d-2c52bbe75edd
---
## 项目概述
- 位置: `E:\funddata\`
- 数据源: Tushare Pro（2000积分级别）
- Token: 保存于 `D:\cc-github\api_config.json` 的 tushare 字段

## 数据库

### funddata.db（场内基金，1.5 GB）
下载日期: 2026-04-30
| 表 | 记录数 |
|---|---|
| fund_basic | 2,558 |
| fund_manager | 5,936 |
| fund_dividend | 8,104 |
| fund_portfolio | 2,885,870 |
| fund_share | 1,876,266 |
| fund_daily | 2,976,949 |
| fund_nav | 3,625,428 |
| 总计 | 11,381,111 |

### outfunddata.db（全量基金含场外，1.6 GB）
下载日期: 2026-05-02
| 表 | 记录数 |
|---|---|
| fund_basic | 14,975（场外13,923 + 场内1,052）|
| fund_manager | 23,823 |
| fund_dividend | 19,781 |
| fund_portfolio | 3,957,814 |
| fund_share | 594,505 |
| fund_daily | 505,428 |
| fund_nav | 8,140,508 |
| 总计 | 13,256,834 |

## 脚本文件
- `fund_downloader.py` v1.1: 场内基金下载（断点续传）
- `outfund_downloader.py` v1.0: 场外基金全量下载（断点续传）
- `fund_verify.py`: 数据验证
- `screen_funds.py`: 场内基金多维度筛选
- 进度文件: `progress.json` / `outfund_progress.json`

## 已解决的技术问题
- brotli 解码兼容性：patch requests 禁用 brotli
- Windows GBK 编码：sys.stdout.reconfigure('utf-8')，emoji 替换纯文本
- 列名不匹配：safe_bulk_insert 自动过滤只保留表中已有列
- fund_nav 日期：场内 end_date 全为 NULL，实际日期在 ann_date 列
- fund_div API 名：Tushare 实际名为 fund_div（非 fund_dividend）
- 份额单位：场内基金 fd_share 为万份，规模 = fd_share * nav / 10000

## 基金筛选功能
支持5维度筛选：年化收益/经理稳定性/净值分位/回撤修复/基金规模
筛选结果已输出到桌面：`场外基金筛选结果.html`

## 未完成项
- fund_adj（复权因子）: 需要 5000 积分，已跳过

## Why: 用户构建基金数据库用于投资分析和筛选
## How to apply: 数据库在 E:\funddata\，脚本同步到 D:\cc-github\funddata\
