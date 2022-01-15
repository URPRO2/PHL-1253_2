"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

大作业2.1的答案
"""
import pandas as pd
import ccxt
import time
import os
import datetime
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


"""
作业内容：
抓取币安交易所的历史数据
    至少抓取最近1个月的数据，建议抓取一年
    交易对自己选择，至少包括：btc/usdt、eth/usdt、eos/usdt、ltc/usdt
    时间周期至少包括：5分钟、15分钟
"""

"""
解题思路：
本作业较为简单，答案基本就是基于课程2.3.7代码的代码稍作修改。

课程2.3.7代码只能抓取指定一天的历史数据。作业要求是抓取某一段时间的全部历史数据，那只需要获取到该段时间每天的日期，然后遍历这些日期抓取每天的数据即可。
"""


# ===来自课程2.3.7的函数save_spot_candle_data_from_exchange
def save_spot_candle_data_from_exchange(exchange, symbol, time_interval, start_time, path):
    """
    将某个交易所在指定日期指定交易对的K线数据，保存到指定文件夹
    :param exchange: ccxt交易所
    :param symbol: 指定交易对，例如'BTC/USDT'
    :param time_interval: K线的时间周期
    :param start_time: 指定日期，格式为'2020-03-16 00:00:00'
    :param path: 文件保存根目录
    :return:
    """

    # ===对火币的limit做特殊处理
    limit = None
    if exchange.id == 'huobipro':
        limit = 2000

    # ===开始抓取数据
    df_list = []
    start_time_since = exchange.parse8601(start_time)
    end_time = pd.to_datetime(start_time) + datetime.timedelta(days=1)

    while True:
        # 获取数据
        df = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, since=start_time_since, limit=limit)
        # 整理数据
        df = pd.DataFrame(df, dtype=float)  # 将数据转换为dataframe
        # 合并数据
        df_list.append(df)
        # 新的since
        t = pd.to_datetime(df.iloc[-1][0], unit='ms')
        start_time_since = exchange.parse8601(str(t))
        # 判断是否挑出循环
        if t >= end_time or df.shape[0] <= 1:
            break
        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(