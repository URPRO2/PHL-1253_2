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