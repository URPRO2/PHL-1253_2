'''
邢不行 | 量化小讲堂系列文章
《抱团股会一直涨？无脑执行大小盘轮动策略，轻松跑赢指数5倍【附Python代码】》
https://mp.weixin.qq.com/s/hPjVbBKomfMhowc32jUwhA
获取更多量化文章，请联系邢不行个人微信：xbx3642
'''
import pandas as pd
import numpy as np
from function import *
import matplotlib.pyplot as plt


pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取数据
df_big = pd.read_csv('sh000300.csv', encoding='gbk', parse_dates=['candle_end_time'])
df_small = pd.read_csv('sz399006.csv', encoding='gbk', parse_dates=['candle_end_time'])

# df_big = getSymbolData('BTC-USDT_5m')
# df_small = getSymbolData('ETH-USDT_5m')
# 设置参数
trade_rate = 0.6 / 10000  # 场内基金万分之0.6，买卖手续费相同，无印花税
momentum_days = 20  # 计算多少天的动量

# 计算大小盘每天的涨跌幅amplitude
df_big['big_amp'] = df_big['close'] / df_big['close'].shift(1) - 1
df_small['small_amp'] = df_small['close'] / df_small['close'].shift(1) - 1
# 重命名行
df_big.rename(columns={'open': 'big_open', 'close': 'big_close'}, inplace=True)
df_small.rename(columns={'open': 'small_open', 'close': 'small_close'}, inplace=True)
# 合并数据
df = pd.merge(left=df_big[['candle_end_time', 'big_open', 'big_close', 'big_amp']], left_on=['candle_end_time'],
              right=df_small[['candle_end_time', 'small_open', 'small_close', 'small_amp']],
 