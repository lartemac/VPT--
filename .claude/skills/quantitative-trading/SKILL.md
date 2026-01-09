---
name: quantitative-trading
description: 量化交易系统开发，专长于加密货币交易（OKX、Binance等）、API对接、数据加密、风险管理、回测系统。核心原则：禁止硬编码私钥、数据安全第一、风险控制优先。触发关键词：交易、OKX、Binance、API、量化、策略、回测、K线。
allowed-tools: Bash(python*), Read, Write, Edit
model: sonnet
---

# 量化交易系统开发 Skill

## 核心原则

### 🔒 安全第一
1. **禁止硬编码私钥**：所有敏感信息必须使用环境变量或加密配置文件
2. **API 密钥管理**：使用 `.env` 文件或系统环境变量存储
3. **日志脱敏**：日志中禁止输出完整的 API 密钥、交易密码

### ⚠️ 风险控制优先
1. **止损止盈**：每个策略必须设置止损和止盈
2. **仓位管理**：单次交易风险不超过总资金的 2%
3. **最大回撤**：设置最大回撤阈值（如 20%）
4. **熔断机制**：当日亏损超过 5% 时暂停交易

### 📊 数据驱动
1. **回测验证**：所有策略必须经过历史数据回测
2. **实盘验证**：小资金验证后再放大仓位
3. **持续监控**：实时监控策略表现

## 何时激活此 Skill

当用户提及以下关键词时，自动激活此 Skill：
- **交易平台**：OKX、Binance、火币、币安
- **交易功能**：API对接、下单、撤单、查询余额
- **策略开发**：量化、策略、回测、K线、技术指标
- **交易类型**：现货、合约、杠杆、期权

## 技术栈

### Python 核心库
```python
# 交易所对接
import ccxt           # 统一交易所API（支持100+交易所）
import okx.Account as OKXAccount
import okx.Trade as OKXTrade
import okx.MarketData as OKXMarket

# 数据分析
import pandas as pd   # 数据处理
import numpy as np    # 数值计算
import ta             # 技术指标库

# 可视化
import matplotlib.pyplot as plt
import mplfinance as mpf

# 网络请求
import requests
import websocket
```

### 环境配置
```bash
# 安装依赖
pip install ccxt pandas numpy ta matplotlib mplfinance python-dotenv
```

## 项目结构

```
quantitative-trading/
├── .env                    # 环境变量（密钥配置，不提交到Git）
├── .env.example           # 环境变量示例
├── config.py              # 配置文件
├── main.py                # 主程序入口
│
├── exchanges/             # 交易所封装
│   ├── base_exchange.py   # 基础交易所类
│   ├── okx_exchange.py    # OKX 交易所
│   └── binance_exchange.py # Binance 交易所
│
├── strategies/            # 交易策略
│   ├── base_strategy.py   # 基础策略类
│   ├── grid_trading.py    # 网格交易策略
│   ├── dca_strategy.py    # 定投策略
│   └── momentum_strategy.py # 动量策略
│
├── indicators/            # 技术指标
│   ├── ma.py             # 移动平均线
│   ├── macd.py           # MACD
│   └── rsi.py            # RSI
│
├── backtest/             # 回测系统
│   ├── backtester.py     # 回测引擎
│   └── reports.py        # 回测报告
│
├── risk/                 # 风险管理
│   ├── position_sizing.py # 仓位管理
│   └── stop_loss.py      # 止损止盈
│
└── utils/                # 工具函数
    ├── logger.py         # 日志工具
    └── encryption.py     # 加密工具
```

## 核心功能实现

### 1. 环境配置（安全）

#### .env 文件（禁止提交到Git）
```bash
# .env（必须添加到 .gitignore）
# OKX API 配置
OKX_API_KEY=your_api_key_here
OKX_SECRET_KEY=your_secret_key_here
OKX_PASSPHRASE=your_passphrase_here
OKX_SANDBOX=true  # true: 测试环境, false: 正式环境

# Binance API 配置
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=true  # true: 测试网, false: 正式网

# 数据库（存储交易记录）
DATABASE_URL=sqlite:///trading.db

# 日志级别
LOG_LEVEL=INFO
```

#### .env.example（提交到Git）
```bash
# .env.example
# OKX API 配置
OKX_API_KEY=
OKX_SECRET_KEY=
OKX_PASSPHRASE=
OKX_SANDBOX=true

# Binance API 配置
BINANCE_API_KEY=
BINANCE_SECRET_KEY=
BINANCE_TESTNET=true
```

#### config.py（读取环境变量）
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

class Config:
    """配置类（从环境变量读取）"""

    # OKX 配置
    OKX_API_KEY = os.getenv('OKX_API_KEY')
    OKX_SECRET_KEY = os.getenv('OKX_SECRET_KEY')
    OKX_PASSPHRASE = os.getenv('OKX_PASSPHRASE')
    OKX_SANDBOX = os.getenv('OKX_SANDBOX', 'true').lower() == 'true'

    # Binance 配置
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
    BINANCE_TESTNET = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'

    # 风险控制
    MAX_POSITION_SIZE = 0.02  # 单次交易最大仓位（2%）
    MAX_DAILY_LOSS = 0.05     # 最大日亏损（5%）
    STOP_LOSS_PERCENT = 0.03  # 止损百分比（3%）
    TAKE_PROFIT_PERCENT = 0.06 # 止盈百分比（6%）

    # 日志
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.OKX_API_KEY or not cls.OKX_SECRET_KEY:
            raise ValueError('OKX API 密钥未配置')

        # 检查是否在测试环境
        if not cls.OKX_SANDBOX:
            print('⚠️ 警告：当前连接到 OKX 正式环境')
            confirm = input('确认继续？(yes/no): ')
            if confirm.lower() != 'yes':
                exit(0)

# 启动时验证配置
Config.validate()
```

### 2. OKX 交易所封装

#### 基础交易所类
```python
# exchanges/base_exchange.py
from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime

class BaseExchange(ABC):
    """交易所基础类"""

    def __init__(self, api_key, secret_key, passphrase=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    @abstractmethod
    def get_balance(self):
        """获取账户余额"""
        pass

    @abstractmethod
    def get_ticker(self, symbol):
        """获取当前价格"""
        pass

    @abstractmethod
    def get_klines(self, symbol, timeframe='1h', limit=100):
        """获取K线数据"""
        pass

    @abstractmethod
    def place_order(self, symbol, side, order_type, amount, price=None):
        """下单"""
        pass

    @abstractmethod
    def cancel_order(self, order_id):
        """撤单"""
        pass
```

#### OKX 交易所实现
```python
# exchanges/okx_exchange.py
import okx.Account as OKXAccount
import okx.Trade as OKXTrade
import okx.MarketData as OKXMarket
import okx.PublicData as OKXPublic
from exchanges.base_exchange import BaseExchange
import pandas as pd

class OKXExchange(BaseExchange):
    """OKX 交易所封装"""

    def __init__(self, api_key, secret_key, passphrase, sandbox=True):
        super().__init__(api_key, secret_key, passphrase)
        self.sandbox = sandbox

        # 初始化 API
        flag = '1' if sandbox else '0'  # 1: 模拟盘, 0: 实盘

        self.account_api = OKXAccount.AccountAPI(
            api_key, secret_key, passphrase, False, flag
        )
        self.trade_api = OKXTrade.TradeAPI(
            api_key, secret_key, passphrase, False, flag
        )
        self.market_api = OKXMarket.MarketAPI(
            api_key, secret_key, passphrase, False, flag
        )
        self.public_api = OKXPublic.PublicAPI(
            api_key, secret_key, passphrase, False, flag
        )

    def get_balance(self):
        """获取账户余额"""
        result = self.account_api.get_account_balance()

        if result['code'] != '0':
            raise Exception(f'获取余额失败: {result["msg"]}')

        # 解析余额数据
        balances = []
        for item in result['data'][0]['details']:
            if float(item['bal']) > 0:  # 只显示有余额的币种
                balances.append({
                    'currency': item['ccy'],
                    'balance': float(item['bal']),
                    'available': float(item['availBal']),
                    'frozen': float(item['frozenBal'])
                })

        return pd.DataFrame(balances)

    def get_ticker(self, symbol):
        """获取当前价格"""
        # symbol 格式: BTC-USDT
        result = self.public_api.get_ticker(instId=symbol)

        if result['code'] != '0':
            raise Exception(f'获取价格失败: {result["msg"]}')

        data = result['data'][0]
        return {
            'symbol': symbol,
            'last_price': float(data['last']),
            'bid_price': float(data['bidPx']),
            'ask_price': float(data['askPx']),
            'volume_24h': float(data['volCcy24h']),
            'timestamp': data['ts']
        }

    def get_klines(self, symbol, timeframe='1H', limit=100):
        """获取K线数据

        Args:
            symbol: 交易对，如 BTC-USDT
            timeframe: 时间周期 (1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 12H, 1D, 1W, 1M)
            limit: 数据条数 (最大300)
        """
        result = self.public_api.get_candlesticks(
            instId=symbol,
            bar=timeframe,
            limit=str(limit)
        )

        if result['code'] != '0':
            raise Exception(f'获取K线失败: {result["msg"]}')

        # 转换为 DataFrame
        df = pd.DataFrame(result['data'], columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'vol_ccy', 'vol_ccy_quote', 'confirm'
        ])

        # 数据类型转换
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)

        # 按时间排序
        df = df.sort_values('timestamp').reset_index(drop=True)

        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    def place_order(self, symbol, side, order_type, amount, price=None):
        """下单

        Args:
            symbol: 交易对
            side: 买/卖 ('buy' 或 'sell')
            order_type: 订单类型 ('market' 市价单, 'limit' 限价单)
            amount: 数量
            price: 价格（限价单必需）
        """
        # OKX 的 side 映射
        okx_side = 'buy' if side == 'buy' else 'sell'

        # OKX 的订单类型映射
        okx_type = 'market' if order_type == 'market' else 'limit'

        # 构建订单参数
        params = {
            'instId': symbol,
            'tdMode': 'cash',  # 现货交易
            'side': okx_side,
            'ordType': okx_type,
            'sz': str(amount)
        }

        if order_type == 'limit' and price:
            params['px'] = str(price)

        # 下单
        result = self.trade_api.place_order(**params)

        if result['code'] != '0':
            raise Exception(f'下单失败: {result["msg"]}')

        return {
            'order_id': result['data'][0]['ordId'],
            'client_order_id': result['data'][0]['clOrdId'],
            'symbol': symbol,
            'side': side,
            'amount': amount,
            'price': price
        }

    def cancel_order(self, symbol, order_id):
        """撤单"""
        result = self.trade_api.cancel_order(
            instId=symbol,
            ordId=order_id
        )

        if result['code'] != '0':
            raise Exception(f'撤单失败: {result["msg"]}')

        return {'order_id': order_id, 'status': 'cancelled'}
```

### 3. 交易策略实现

#### 基础策略类
```python
# strategies/base_strategy.py
from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """策略基础类"""

    def __init__(self, exchange, symbol, config):
        self.exchange = exchange
        self.symbol = symbol
        self.config = config

    @abstractmethod
    def generate_signals(self, data):
        """生成交易信号"""
        pass

    @abstractmethod
    def calculate_position_size(self, balance, price):
        """计算仓位大小"""
        pass

    def risk_check(self, entry_price, stop_loss_price, balance):
        """风险检查"""
        # 计算潜在损失
        loss_percent = abs(entry_price - stop_loss_price) / entry_price

        # 检查是否超过最大单次风险
        if loss_percent > self.config.STOP_LOSS_PERCENT:
            print(f'⚠️ 风险警告：潜在损失 {loss_percent*100:.2f}% 超过止损线')
            return False

        # 检查仓位是否过大
        position_value = balance * self.config.MAX_POSITION_SIZE
        if position_value > balance:
            print('⚠️ 风险警告：仓位过大')
            return False

        return True
```

#### 网格交易策略
```python
# strategies/grid_trading.py
from strategies.base_strategy import BaseStrategy
import pandas as pd

class GridTradingStrategy(BaseStrategy):
    """网格交易策略

    原理：在价格区间内设置买入和卖出网格，价格下跌时分批买入，
         价格上涨时分批卖出，赚取波动利润。
    """

    def __init__(self, exchange, symbol, config, upper_price, lower_price, grid_count=10):
        super().__init__(exchange, symbol, config)
        self.upper_price = upper_price  # 网格上限
        self.lower_price = lower_price  # 网格下限
        self.grid_count = grid_count    # 网格数量
        self.grid_spacing = (upper_price - lower_price) / grid_count

        # 生成网格价格
        self.buy_grids = []
        self.sell_grids = []

        for i in range(grid_count):
            price = lower_price + i * self.grid_spacing
            self.buy_grids.append(price)
            self.sell_grids.append(price + self.grid_spacing)

    def generate_signals(self, current_price):
        """生成交易信号"""
        signals = []

        # 检查买入信号
        for buy_price in self.buy_grids:
            if abs(current_price - buy_price) / buy_price < 0.001:  # 0.1% 容差
                signals.append({
                    'action': 'buy',
                    'price': buy_price,
                    'type': 'limit'
                })

        # 检查卖出信号
        for sell_price in self.sell_grids:
            if abs(current_price - sell_price) / sell_price < 0.001:
                signals.append({
                    'action': 'sell',
                    'price': sell_price,
                    'type': 'limit'
                })

        return signals

    def calculate_position_size(self, balance, price):
        """计算仓位大小（平均分配资金到每个网格）"""
        grid_balance = balance * self.config.MAX_POSITION_SIZE
        position_size = (grid_balance / self.grid_count) / price
        return position_size
```

#### 动量策略
```python
# strategies/momentum_strategy.py
from strategies.base_strategy import BaseStrategy
import pandas as pd
import ta

class MomentumStrategy(BaseStrategy):
    """动量策略

    原理：使用 MACD 和 RSI 指标识别趋势和超买超卖，
         MACD 金叉且 RSI 不超买时买入，死叉且 RSI 不超卖时卖出。
    """

    def __init__(self, exchange, symbol, config, rsi_period=14, macd_fast=12, macd_slow=26, macd_signal=9):
        super().__init__(exchange, symbol, config)
        self.rsi_period = rsi_period
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal

    def calculate_indicators(self, data):
        """计算技术指标"""
        df = data.copy()

        # 计算 RSI
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=self.rsi_period).rsi()

        # 计算 MACD
        macd = ta.trend.MACD(
            df['close'],
            window_fast=self.macd_fast,
            window_slow=self.macd_slow,
            window_sign=self.macd_signal
        )
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        return df

    def generate_signals(self, data):
        """生成交易信号"""
        # 计算指标
        df = self.calculate_indicators(data)

        # 获取最新数据
        latest = df.iloc[-1]
        previous = df.iloc[-2]

        signals = []

        # 买入信号：MACD 金叉 且 RSI < 70（不超买）
        if (latest['macd_diff'] > 0 and previous['macd_diff'] <= 0) and latest['rsi'] < 70:
            signals.append({
                'action': 'buy',
                'price': latest['close'],
                'type': 'market',
                'reason': f'MACD金叉，RSI={latest["rsi"]:.2f}'
            })

        # 卖出信号：MACD 死叉 且 RSI > 30（不超卖）
        if (latest['macd_diff'] < 0 and previous['macd_diff'] >= 0) and latest['rsi'] > 30:
            signals.append({
                'action': 'sell',
                'price': latest['close'],
                'type': 'market',
                'reason': f'MACD死叉，RSI={latest["rsi"]:.2f}'
            })

        return signals

    def calculate_position_size(self, balance, price):
        """计算仓位大小（固定2%风险）"""
        return balance * self.config.MAX_POSITION_SIZE / price
```

### 4. 回测系统

#### 回测引擎
```python
# backtest/backtester.py
import pandas as pd
from datetime import datetime

class Backtester:
    """回测引擎"""

    def __init__(self, strategy, exchange, initial_balance=10000):
        self.strategy = strategy
        self.exchange = exchange
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.position = 0  # 持仓数量
        self.trades = []   # 交易记录

    def run(self, symbol, start_date, end_date):
        """运行回测"""
        print(f'开始回测 {symbol} ({start_date} 至 {end_date})')

        # 获取历史数据
        data = self.exchange.get_klines(symbol, timeframe='1D', limit=365)

        # 过滤日期范围
        data = data[(data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)]

        # 逐日回测
        for i in range(len(data)):
            current_data = data.iloc[:i+1]
            current_price = current_data.iloc[-1]['close']

            # 生成信号
            signals = self.strategy.generate_signals(current_data)

            # 执行交易
            for signal in signals:
                self.execute_signal(signal, current_price, current_data.iloc[-1]['timestamp'])

        # 生成报告
        self.generate_report(data)

    def execute_signal(self, signal, price, timestamp):
        """执行交易信号"""
        if signal['action'] == 'buy' and self.position == 0:
            # 买入
            amount = self.strategy.calculate_position_size(self.balance, price)
            cost = amount * price

            if cost <= self.balance:
                self.balance -= cost
                self.position = amount

                self.trades.append({
                    'timestamp': timestamp,
                    'action': 'buy',
                    'price': price,
                    'amount': amount,
                    'cost': cost,
                    'reason': signal.get('reason', '')
                })

                print(f'[{timestamp}] 买入 {amount:.4f} @ {price:.2f}')

        elif signal['action'] == 'sell' and self.position > 0:
            # 卖出
            revenue = self.position * price
            profit = revenue - (self.position * self.trades[-1]['price'])

            self.balance += revenue
            self.position = 0

            self.trades.append({
                'timestamp': timestamp,
                'action': 'sell',
                'price': price,
                'amount': self.trades[-1]['amount'],
                'revenue': revenue,
                'profit': profit,
                'reason': signal.get('reason', '')
            })

            print(f'[{timestamp}] 卖出 @ {price:.2f}, 利润: {profit:.2f}')

    def generate_report(self, data):
        """生成回测报告"""
        # 计算总收益
        total_return = (self.balance - self.initial_balance) / self.initial_balance * 100

        # 计算胜率
        winning_trades = [t for t in self.trades if t['action'] == 'sell' and t.get('profit', 0) > 0]
        win_rate = len(winning_trades) / (len(self.trades) // 2) * 100 if self.trades else 0

        # 最大回撤
        peak_balance = self.initial_balance
        max_drawdown = 0

        for trade in self.trades:
            if trade['action'] == 'sell':
                current_balance = self.balance if trade == self.trades[-1] else self.initial_balance + trade.get('profit', 0)

                if current_balance > peak_balance:
                    peak_balance = current_balance

                drawdown = (peak_balance - current_balance) / peak_balance * 100
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

        # 打印报告
        print('\n' + '='*50)
        print('回测报告')
        print('='*50)
        print(f'初始资金: ${self.initial_balance:,.2f}')
        print(f'最终资金: ${self.balance:,.2f}')
        print(f'总收益率: {total_return:+.2f}%')
        print(f'最大回撤: {max_drawdown:.2f}%')
        print(f'交易次数: {len(self.trades) // 2}')
        print(f'胜率: {win_rate:.2f}%')
        print('='*50)
```

### 5. 风险管理

#### 仓位管理
```python
# risk/position_sizing.py

class PositionSizer:
    """仓位管理器"""

    @staticmethod
    def fixed_ratio(balance, ratio=0.02):
        """固定比例仓位

        Args:
            balance: 账户余额
            ratio: 仓位比例（默认2%）
        """
        return balance * ratio

    @staticmethod
    def kelly_criterion(balance, win_rate, avg_win, avg_loss):
        """凯利公式计算仓位

        Args:
            balance: 账户余额
            win_rate: 胜率（0-1）
            avg_win: 平均盈利
            avg_loss: 平均亏损
        """
        # 凯利公式: f = (bp - q) / b
        # b = avg_win / avg_loss (盈亏比)
        # p = win_rate (胜率)
        # q = 1 - p (败率)

        b = avg_win / avg_loss if avg_loss != 0 else 1
        p = win_rate
        q = 1 - p

        kelly_ratio = (b * p - q) / b

        # 保守起见，使用凯利值的25%
        return balance * max(kelly_ratio * 0.25, 0)

    @staticmethod
    def volatility_based(balance, volatility, target_volatility=0.02):
        """基于波动率的仓位

        Args:
            balance: 账户余额
            volatility: 当前波动率（标准差）
            target_volatility: 目标波动率（默认2%）
        """
        if volatility == 0:
            return balance * 0.02

        position_size = balance * (target_volatility / volatility)
        return min(position_size, balance * 0.05)  # 最大不超过5%
```

#### 止损止盈
```python
# risk/stop_loss.py

class StopLossManager:
    """止损止盈管理器"""

    @staticmethod
    def calculate_stop_loss(entry_price, side, percent=0.03):
        """计算止损价格

        Args:
            entry_price: 入场价格
            side: 买/卖 ('buy' 或 'sell')
            percent: 止损百分比（默认3%）
        """
        if side == 'buy':
            return entry_price * (1 - percent)
        else:
            return entry_price * (1 + percent)

    @staticmethod
    def calculate_take_profit(entry_price, side, percent=0.06):
        """计算止盈价格

        Args:
            entry_price: 入场价格
            side: 买/卖 ('buy' 或 'sell')
            percent: 止盈百分比（默认6%）
        """
        if side == 'buy':
            return entry_price * (1 + percent)
        else:
            return entry_price * (1 - percent)

    @staticmethod
    def trailing_stop(current_price, highest_price, side, percent=0.02):
        """移动止损

        Args:
            current_price: 当前价格
            highest_price: 最高价格（买入后的最高价）
            side: 买/卖
            percent: 移动止损百分比
        """
        if side == 'buy':
            # 价格创新高时更新止损线
            if current_price > highest_price:
                stop_price = current_price * (1 - percent)
            else:
                stop_price = highest_price * (1 - percent)
        else:
            if current_price < highest_price:
                stop_price = current_price * (1 + percent)
            else:
                stop_price = highest_price * (1 + percent)

        return stop_price
```

## 常见问题

### Q1: 如何选择交易所？
**A**:
- **OKX**：手续费低（0.1%），支持现货、合约、期权，API稳定
- **Binance**：流动性最好，交易对最多，适合高频交易
- **推荐**：新手使用OKX，专业交易者使用Binance

### Q2: 如何避免策略过拟合？
**A**:
1. **样本外测试**：保留20%数据不参与策略开发
2. **参数稳健性**：参数小幅度变化不应导致收益大幅下降
3. **实盘验证**：小资金运行1-2个月再放大仓位

### Q3: 如何处理API限流？
**A**:
1. **使用WebSocket**：实时行情订阅，减少API调用
2. **本地缓存**：价格数据缓存5秒
3. **请求限流**：使用 rate limiter 限制请求频率

```python
import time
from functools import wraps

def rate_limit(max_calls, period):
    """请求限流装饰器"""
    def decorator(func):
        calls = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # 移除过期记录
            calls[:] = [c for c in calls if c > now - period]

            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                time.sleep(sleep_time)
                calls[:] = []

            calls.append(time.time())
            return func(*args, **kwargs)

        return wrapper
    return decorator

# 使用示例
@rate_limit(max_calls=10, period=1)  # 每秒最多10次请求
def get_ticker(symbol):
    return exchange.get_ticker(symbol)
```

---

**最后更新**：2026-01-10
**适用平台**：OKX、Binance 等100+交易所（通过ccxt）
**核心原则**：安全第一、风险控制优先、数据驱动
