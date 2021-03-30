
"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍择时策略实盘的整体思路
"""
import pandas as pd
import ccxt
from program.三_少年意气.四_择时策略实盘初阶.Function import *


# 大象放进冰箱只需要3步。


# =====配置运行相关参数=====
exchange = ccxt.okex()  # 交易所api
time_interval = '15m'  # 目前支持5m，15m，30m，1h，2h等
# 以及其他各类参数，例如钉钉id等


# =====配置交易相关参数=====
# symbol_config，更新需要交易的合约、策略参数、下单量等配置信息
symbol_config = {
    'eth-usdt': {'instrument_id': 'ETH-USDT-200626',  # 合约代码，当更换合约的时候需要手工修改
                 'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                 'strategy_name': 'real_signal_random',  # 使用的策略的名称
                 'para': [10]},  # 策略参数
    'eos-usdt': {'instrument_id': 'EOS-USDT-200327',
                 'leverage': '3',
                 'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
                 'para': [20, 2]},
}


# =====获取需要交易币种的历史数据=====
# 因为okex每次最多只能获取300根K线数据，不能满足有些策略的参数需求。
# 但是OKEx可以根据k线开始的时间，获取之前的k线，最多可以获取1440根k线数据。大致可以满足我们的需求。
# 所以需要在程序刚开始运行的时候，不断获取300K根K线，并且往前推，总共获取1440根K线数据。
# 如果参数超过1440，那么需要使用本地文件存储数据，逻辑相同。
symbol_candle_data = {
    'eth-usdt': pd.DataFrame(),  # 此处的交易对，要和symbol_config中一一对应
    'eos-usdt': pd.DataFrame()
}  # 是一个dict，用于存放每个币种的1440根K线数据


# =====在每根K线结束时，进行一次循环，无穷无尽=====
while True:
