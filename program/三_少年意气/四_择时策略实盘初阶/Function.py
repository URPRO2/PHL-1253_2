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
    ltc-usdt         NaN   9.99970474                                                NaN     USDT   9.99970474         0.0005       tier               0.01           0                   0             0     crossed        10000  -0.00029526                  10   LTC-USDT              0
    eos              NaN   6.49640362                                                NaN      EOS   7.21825155         0.0005       tier               0.01  0.72184793                   0    0.72184793     crossed   0.99996845            0          7.29194531    EOS-USD    -0.07369376
    eos-usdt           0   9.91366074  [{'available_qty': '9.91366074', 'fixed_balanc...     USDT   9.99473074            NaN       tier                NaN         NaN                 NaN           NaN       fixed          NaN          NaN          9.91366074        NaN            NaN
    btc-usdt         NaN  57.07262111                                                NaN     USDT  57.07262111         0.0005       tier              0.005           0                   0             0     crossed        10000            0         57.07262111   BTC-USDT              0
    """
    for _ in range(max_try_amount):
        try:
            future_info = exchange.futures_get_accounts()['info']
            df = pd.DataFrame(future_info, dtype=float).T  # 将数据转化为df格式
            return df
        except Exception as e:
            print('通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败，稍后重试：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


# ===通过ccxt、交易所接口获取合约账户持仓信息
def ccxt_fetch_future_position(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:
    本程序使用okex3中“交割合约API”、“所有合约持仓信息”接口，获取合约账户所有合约的持仓信息。
    使用ccxt函数：exchange.futures_get_position()
    请求此接口，okex服务器会在其数据库中遍历所有币对下的持仓数据，有大量的性能消耗，请求频率较低，时间较长。

    接口返回数据格式样例：
    {'result': True, 'holding':
    [[{'long_qty': '1', 'long_avail_qty': '1', 'long_margin': '0.027094', 'long_liqui_price': '241.07', 'long_pnl_ratio': '-0.0636223', 'long_avg_cost': '265.63', 'long_settlement_price': '265.63', 'realised_pnl': '0.00051826', 'short_qty': '0', 'short_avail_qty': '0', 'short_margin': '0', 'short_liqui_price': '0', 'short_pnl_ratio': '0.0714716', 'short_avg_cost': '265.84', 'short_settlement_price': '265.84', 'instrument_id': 'ETH-USDT-200327', 'long_leverage': '10', 'short_leverage': '10', 'created_at': '2020-02-22T08:02:04.469Z', 'updated_at': '2020-02-22T08:42:02.484Z', 'margin_mode': 'fixed', 'short_margin_ratio': '10000.0', 'short_maint_margin_ratio': '0.01', 'short_pnl': '0.0', 'short_unrealised_pnl': '0.0', 'long_margin_ratio': '0.09624915', 'long_maint_margin_ratio': '0.01', 'long_pnl': '-0.00169', 'long_unrealised_pnl': '-0.00169', 'long_settled_pnl': '0', 'short_settled_pnl': '0', 'last': '264.08'},
    {'long_qty': '1', 'long_avail_qty': '1', 'long_margin': '0.04127', 'long_liqui_price': '3.753', 'long_pnl