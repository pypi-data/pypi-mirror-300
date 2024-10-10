from enum import Enum, auto
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

BANNER: str = ...
"""Banner"""

class Mode(Enum):
    """运行模式"""

    Backtest = auto()
    """回测"""
    Sandbox = auto()
    """模拟"""
    Real = auto()
    """实盘"""

class PosSide(Enum):
    """持仓方向"""

    Long = auto()
    """做多"""
    Short = auto()
    """做空"""

class Type(Enum):
    """交易类型"""

    Limit = auto()
    """限价交易"""
    Market = auto()
    """市价交易"""

class Side(Enum):
    """交易方向"""

    Buy = auto()
    """买入"""
    Sell = auto()
    """卖出"""

class CandleInterval(Enum):
    """K线周期"""

    Minute = auto()
    Minute3 = auto()
    Minute5 = auto()
    Minute15 = auto()
    Minute30 = auto()
    Hour = auto()
    Hour2 = auto()
    Hour4 = auto()
    Hour6 = auto()
    Hour8 = auto()
    Hour12 = auto()
    Day = auto()
    Day3 = auto()
    Week = auto()
    Month = auto()

class Account:
    cash: Decimal
    available: Decimal
    margin: Decimal
    pnl: Decimal

class Candle:
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float
    taker_volume: float
    taker_amount: float
    trades: int

class Order:
    symbol: str
    id: str
    pside: PosSide
    side: Side
    type: Type
    leverage: Decimal
    volume: Decimal
    price: Decimal
    time: int
    margin: Decimal
    deal_volume: Decimal
    deal_price: Decimal
    deal_fee: Decimal

class Position:
    pside: PosSide
    leverage: Decimal
    mark_price: Decimal
    volume: Decimal
    price: Decimal
    available: Decimal
    margin: Decimal
    pnl: Decimal
    taker_rate: Decimal
    maker_rate: Decimal

class Positions:
    long: Position
    short: Position

def str_to_date(s: str) -> datetime:
    """
    字符串转日期 `UTC+0`
    ---
    - 格式1 : 2000
    - 格式2 : 200001
    - 格式3 : 20000102
    - 格式4 : 2000010203
    - 格式5 : 200001020304
    - 格式6 : 20000102030405
    ---
    其他格式均返回错误
    """

def ms_to_date(ts: int) -> datetime:
    """毫秒转日期 `UTC+0`"""

def now_ms() -> int:
    """当前毫秒时间戳"""

def stop():
    """停止运行"""

def set_benchmark(symbol: str):
    """设置基准"""

def set_symbol(symbol: str, taker_rate: str, maker_rate: str):
    """设置交易对"""

def set_leverage(symbol: str, leverage: Decimal):
    """设置杠杆倍数"""

def set_order(
    symbol: str,
    pside: PosSide,
    side: Side,
    type: Type,
    volume: Decimal,
    price: Decimal,
) -> str:
    """下单"""

def close_order(id: str):
    """关闭订单"""

def debug(msg: str):
    """输出调试消息"""

def info(msg: str):
    """输出普通消息"""

def warn(msg: str):
    """输出警告消息"""

def error(msg: str):
    """输出错误消息"""

def get_trade_time() -> datetime:
    """获取交易时间"""

def get_account() -> Account:
    """获取账户"""

def get_benchmark() -> str:
    """获取基准"""

def get_symbols() -> List[str]:
    """获取交易对"""

def get_position(symbol: str) -> Optional[Positions]:
    """获取持仓"""

def get_order(id: str) -> Optional[Order]:
    """获取订单"""

def get_candle(symbol: str, interval: CandleInterval) -> Optional[Candle]:
    """获取K线"""

def get_candles(
    symbol: str,
    interval: CandleInterval,
    begin: datetime,
    end: datetime,
) -> List[Candle]:
    """获取K线列表"""

class BacktestConfig:
    def __init__(self) -> BacktestConfig: ...
    def begin(self, begin: str) -> BacktestConfig: ...
    def end(self, end: str) -> BacktestConfig: ...
    def cash(self, cash: str) -> BacktestConfig: ...
    def slippage(self, slippage: str) -> BacktestConfig: ...
    def sync_market(self, sync_market: bool) -> BacktestConfig: ...
    def show_on_tick_time_consuming(
        self, show_on_tick_time_consuming: bool
    ) -> BacktestConfig: ...
    def show_on_candle_time_consuming(
        self, show_on_candle_time_consuming: bool
    ) -> BacktestConfig: ...

def start_backtest(config: BacktestConfig, strategy: str):
    """运行回测"""
