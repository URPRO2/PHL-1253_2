"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍择时策略实盘
"""
import ccxt
from time import sleep
import pandas as pd
from datetime import datetime

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# =====配置运行相关参数=====

# =执行的时间间隔
time_interval = '1m'  # 目前支持5m，15m，30m，1h，2h等。得okex支持的K线才行。最好不要低于5m

exchange = ccxt.binance()
exchange.apiKey = 'uyae67zOFA38gl93adYhNALlGMmMRswQapow63kzI1lYwKhUZblwLdZrlAzsEPWe'
exchange.secret = 'SqetI8JCn2do1gkzKlCAQyOJ7CgXG3TqiWZltTrRxhADNdVg3czqUx5uhBtOG0pf'
# =====配置交易相关参数=====
# 更新需要交易的合约、策略参数、下单量等配置信息

def main():
    df = exchange.fetch_tickers()
    df = pd.DataFrame(df, dtype=float)
    df = df.T

    df = df[df['symbol'].str.contains('/USDT')]  # 剔除 非 USDT
    df = df[df['symbol'].str.contains('UP/USDT') == False]
    df = df[df['symbol'].str.contains('DOWN/USDT') == False]  # 剔除期货
    df = df[df['bid'] != 0]
    df = df[df['ask'] != 0]  # 剔除0交易量
    wendingbi = ['USDC/USDT', 'TUSD/USDT', 'PAX/USDT', 'BUSD/USDT']  # 剔除稳定币
    df = df[df['symbol'].isin(values=wendingbi) == False]

    # df['价差率'] = (df['ask'] - df['bid']) / df['bid']
    df.sort_values(by=['vwap'], inplace=True, ascending=False)
    df.reset_index(inplace=True, drop=True)

    # print(df)

    sum = df['percentage'].sum()
    print('所有币种平均涨幅:' + str(sum / df.shape[0]))

    df = df[(df['close'] > 0.02) & (df['close'] < 1)]

    df.reset_index(inplace=True, drop=True)
    symbols = list(df['symbol'])
    print(df)
    # for i in range(5):
    #     _price = df.at[i, 'last']
    #     _price = _price - _price * 0.05
    #     ret = exchange.create_limit_buy_order(symbol=df.at[i, 'symbol'], amount=10, price=_price)
    #     print(ret)
    # =下单
    # symbol_order = pd.DataFrame()
    # symbol_order = single_threading_place_order(exchange, symbol_info, symbol_config, symbol_signal)  # 单线程下单
    # print('下单记录：\n', symbol_order)
    #
    # # 更新订单信息，查看是否完全成交
    # time.sleep(short_sleep_time)  # 休息一段时间再更新订单信息
    # sym