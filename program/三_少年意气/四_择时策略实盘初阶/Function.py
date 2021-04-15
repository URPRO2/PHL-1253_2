"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
择时策略实盘需要的相关函数
"""
import ccxt
import math
import time
import pandas as pd
from datetime import datetime, timedelta
import json
import requests
import time
import hmac
import hashlib
import base64
from urllib import parse
from multiprocessing import Pool
from functools import partial
from program.三_少年意气.四_择时策略实盘初阶.Config import *
from program.三_少年意气.四_择时策略实盘初阶.Signals import *


# =====okex交互函数
# ===通过ccxt、交易所接口获取合约账户信息
def ccxt_fetch_future_account(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:

    本程序使用okex3中“交割合约API”、“所有币种合约账户信息”接口，获取合约账户所有币种的账户信息。
    使用ccxt函数：exchange.futures_get_accounts()
    请求此接口，okex服务器会在其数据库中遍历所有币对下的账户数据，有大量的性能消耗，请求频率较低，时间较长。

    接口返回数据格式样例：
    {'info':
    {
    'eth-usdt': {'auto_margin': '0', 'can_withdraw': '9.97342426', 'contracts': [{'available_qty': '9.97342426', 'fixed_balance': '0.02657574', 'instrument_id': 'ETH-USDT-200327', 'margin_for_unfilled': '0', 'margin_frozen': '0.027094', 'realized_pnl': '0.00051826', 'unrealized_pnl': '-0.0018'}], 'currency': 'USDT', 'equity': '9.99878826', 'liqui_mode': 'tier', 'margin_mode': 'fixed', 'total_avail_balance': '9.97342426'},
    'ltc-usdt': {'can_withd