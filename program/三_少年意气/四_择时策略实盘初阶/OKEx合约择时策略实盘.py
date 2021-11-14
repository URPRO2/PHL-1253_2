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
from program.三_少年意气.四_择时策略实盘初阶.Function import *
from program.三_少年意气.四_择时策略实盘初阶.Config import *
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# 测试时ccxt版本为1.27.28。若不是此版本，可能会报错，可能性很低。print(ccxt.__version__)可以查看ccxt版本。

# =====配置运行相关参数=====

# =执行的时间间隔
time_interval = '15m'  # 目前支持5m，15m，30m，1h，2h等。得okex支持的K线才行。最好不要低于5m

# =钉钉
# 在一个钉钉群中，可以创建多个钉钉机器人。
# 建议单独建立一个报错机器人，该机器人专门发报错信息。请务必将报错机器人在id和secret放到function.send_dingding_msg的默认参数中。
robot_id = ''
secret = ''
robot_id_secret = [robot_id, secret]

# =交易所配置
OKEX_CONFIG = {
    'apiKey': '',
    'secret': '',
    'password': '',
    'timeout': exchange_timeout,
    'rateLimit': 10,
    'hostname': 'okex.me',  # 无法fq的时候启用
    'enableRateLimit': False}
exchange = ccxt.okex(OKEX_CONFIG)

# =====配置交易相关参数=====
# 更新需要交易的合约、策略参数、下单量等配置信息
symbol_config = {
    'eth-usdt': {'instrument_id': 'ETH-USDT-200626',  # 合约代码，当更换合约的时候需要手工修改
                 'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                 'strategy_name': 'real_signal_simple_bolling',  # 使用的策略的名称
                 'para': [20, 2]},  # 策略参数
    'eos-usdt': {'instrument_id': 'EOS-USDT-200626',
                 'leverage': '3',
                 'strategy_name