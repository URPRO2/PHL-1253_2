import ccxt
from datetime import timedelta
import pandas as pd
import time
import sys,os
if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
from base.Tool import *
from Code.base import wechat

# print(ccxt.__version__)  # 检查ccxt版本，需要最新版本，1.44.21以上
wx = wechat.WeChat()
rule_type = '4h'
num = 20
bigSymbol = 'BTC/USDT'
smallSymbol = 'ETH/USDT'

ex = ccxt.binance()


def getMom(symbo