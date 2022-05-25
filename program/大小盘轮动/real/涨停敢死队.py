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

def m