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
    :param start_time: 指定日期，格式为'2020-03