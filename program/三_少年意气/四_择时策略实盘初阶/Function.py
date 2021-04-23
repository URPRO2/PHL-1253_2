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
    'ltc-usdt': {'can_withdraw': '9.99970474', 'currency': 'USDT', 'equity': '9.99970474', 'liqui_fee_rate': '0.0005', 'liqui_mode': 'tier', 'maint_margin_ratio': '0.01', 'margin': '0', 'margin_for_unfilled': '0', 'margin_frozen': '0', 'margin_mode': 'crossed', 'margin_ratio': '10000', 'realized_pnl': '-0.00029526', 'total_avail_balance': '10', 'underlying': 'LTC-USDT', 'unrealized_pnl': '0'},
    'eos': {'can_withdraw': '6.49953151', 'currency': 'EOS', 'equity': '7.22172698', 'liqui_fee_rate': '0.0005', 'liqui_mode': 'tier', 'maint_margin_ratio': '0.01', 'margin': '0.72219547', 'margin_for_unfilled': '0', 'margin_frozen': '0.72219547', 'margin_mode': 'crossed', 'margin_ratio': '0.99996847', 'realized_pnl': '0', 'total_avail_balance': '7.29194531', 'underlying': 'EOS-USD', 'unrealized_pnl': '-0.07021833'},
    'eos-usdt': {'auto_margin': '0', 'can_withdraw': '9.91366074', 'contracts': [{'available_qty': '9.91366074', 'fixed_balance': '0.0827228', 'instrument_id': 'EOS-USDT-200327', 'margin_for_unfilled': '0', 'margin_frozen': '0.08167', 'realized_pnl': '-0.0010528', 'unrealized_pnl': '-0.0006'}], 'currency': 'USDT', 'equity': '9.99473074', 'liqui_mode': 'tier', 'margin_mode': 'fixed', 'total_avail_balance': '9.91366074'},
    返回结果说明：
    eth-usdt为usdt本位合约有持仓时返回的结果
    ltc-usdt为usdt本位合约没有持仓，但是账户有usdt时返回的结果
    eos-usdt为usdt本位合约同时有多、空持仓时返回的结果
    eos为币本位合约有持仓时返回的结果

    本函数输出示例：

         auto_margin can_withdraw                                          contracts currency       equity liqui_fee_rate liqui_mode maint_margin_ratio      margin margin_for_unfilled margin_frozen margin_mode margin_ratio realized_pnl total_avail_balance underlying unrealized_pnl
    eth-usdt           0   9.97342426  [{'available_qty': '9.97342426', 'fixed_balanc...     USDT   9.99847826            NaN       tier                NaN         NaN                 NaN           NaN       fixed          NaN          NaN          9.97342426        NaN            NaN
    ltc-usdt         NaN   9.99970474                                                NaN     USDT   9.9