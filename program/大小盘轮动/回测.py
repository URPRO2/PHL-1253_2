"""
在此之前需要行情数据，备份
回测大小盘（BTC、ETH）
"""
import pandas as pd
from Tool import *
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# ==========整理出历史数据、转换4小时数据============
btcDf = getSymbolData('BTC-USDT_5m')
ethDf = getSymbolData('ETH-USDT_5m')
print(btcDf)
# btcDf['mean120'] = btcDf['close'].rolling(120, min_periods=1).mean()
btcDf['mean120'] = btcDf['close'].pct_change(periods=120)
btcDf['next_open'] = btcDf['open'].shift(-1)  # 下根K线的开盘价
btcDf['next_open'].fillna(value=btcDf['close'], inplace=True)
btcDf = btcDf.loc[120:]
# ethDf['mean120'] = ethDf['close'].rolling(120, min_periods=1).mean()
ethDf['mean120'] = ethDf['close'].pct_change(periods=120)
ethDf['next_open'] = ethDf['open'].shift(-1)  # 下根K线的开盘价
ethDf['next_open'].fillna(value=ethDf['close'], inplace=True)
ethDf = ethDf.loc[120:]
# =====两个df左右合并操作，merge操作
df_merged = pd.merge(left=btcDf, right=ethDf, left_on='candle_begin_time', right_on='candle_begin_time',
                     suffixes=['_btc', '_eth'])
# 计算信号
df_merged.loc[df_merged['mean120_btc'] > df_merged['mean120_eth'], 'signal'] = 1
df_merged.loc[df_merged['mean120_btc'] > df_merged['mean120_eth'], 'open'] = df_merged['open_btc']
df_merged.loc[df_merged['mean120_btc'] > df_merged['mean120_eth'], 'close'] = df_merged['close_btc']
df_merged.loc[df_merged['mean120_eth'] > df_merged['mean120_btc'], 'sig