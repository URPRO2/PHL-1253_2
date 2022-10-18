"""
《邢不行-2020新版|Python数字货币量化投资课程》
择时策略魔改研究小组（第1期）
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9585
本程序作者: 邢不行
"""

from datetime import timedelta
from program.少年意气_择时策略魔改小组.择时策略开发与回测 import Signals
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Position import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Evaluate import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Function import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Statistics import *

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 500)  # 最多显示数据的行数

# =====手工设定策略参数
symbol = 'BTC-USDT_5m'
para = [220, 2.3]
signal_name = 'signal_my_bolling'
rule_type = '4H'

symbol_face_value = {'BTC': 0.01, 'EOS': 10, 'ETH': 0.1, 'LTC': 1, 'XRP': 100}
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 2
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
drop_days = 10  # 币种刚刚上线10天内不交易

# =====读入数据
df = pd.read_pickle(root_path + '/data/%s.pkl' % symbol)
# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)

# =====转换为其他分钟数据
period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
    {'open': 'first',
     'high': 'max',
     'low': 'min',
     'close': 'last',
     'volume': 'sum',
     'quote_volume': 'sum',
     'trade_num': 'sum',
     'taker_buy_base_asset_volume': 'sum',
     'taker_buy_quote_asset_volume': 'sum',
     })
period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
period_df.reset_index(inplace=True)
df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_volume', 'trade_num',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']]
df = df[df['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
df.reset_index(inplace=True, drop=True)

# =====计算交易信号
df = getattr(Signals, signal_name)(df, para=para)

# =====计算实际持仓
df = position_for_OKEx_future(df)

# =====计算资金曲线
# 选取相关时间。币种上线10天之后的日期
t = df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
df = df[df['candle_begin_time'] > t]

df = df[df['candle_begin_time'] >= pd.to_datetime('2018-01-01')]


# 计算资金曲线
face_value = symbol_face_value[symbol.