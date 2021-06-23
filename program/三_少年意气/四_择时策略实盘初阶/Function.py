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
    {'long_qty': '1', 'long_avail_qty': '1', 'long_margin': '0.04127', 'long_liqui_price': '3.753', 'long_pnl_ratio': '-0.0048473', 'long_avg_cost': '4.126', 'long_settlement_price': '4.126', 'realised_pnl': '-0.0010528', 'short_qty': '1', 'short_avail_qty': '1', 'short_margin': '0.0404', 'short_liqui_price': '4.476', 'short_pnl_ratio': '-0.0097087', 'short_avg_cost': '4.12', 'short_settlement_price': '4.12', 'instrument_id': 'EOS-USDT-200327', 'long_leverage': '10', 'short_leverage': '10', 'created_at': '2020-02-20T06:17:21.890Z', 'updated_at': '2020-02-22T09:53:15.931Z', 'margin_mode': 'fixed', 'short_margin_ratio': '0.09699321', 'short_maint_margin_ratio': '0.01', 'short_pnl': '-4.0E-4', 'short_unrealised_pnl': '-4.0E-4', 'long_margin_ratio': '0.09958778', 'long_maint_margin_ratio': '0.01', 'long_pnl': '-2.0E-4', 'long_unrealised_pnl': '-2.0E-4', 'long_settled_pnl': '0', 'short_settled_pnl': '0', 'last': '4.123'}],
    [{'long_qty': '0', 'long_avail_qty': '0', 'long_avg_cost': '0', 'long_settlement_price': '0', 'realised_pnl': '0', 'short_qty': '3', 'short_avail_qty': '3', 'short_avg_cost': '4.53509442', 'short_settlement_price': '4.114', 'liquidation_price': '130311.677', 'instrument_id': 'EOS-USD-200327', 'leverage': '10', 'created_at': '2020-02-18T06:42:29.924Z', 'updated_at': '2020-02-22T08:00:16.315Z', 'margin_mode': 'crossed', 'short_margin': '0.72184793', 'short_pnl': '0.60340204', 'short_pnl_ratio': '0.9121617', 'short_unrealised_pnl': '-0.07369376', 'long_margin': '0.0', 'long_pnl': '0.0', 'long_pnl_ratio': '0.0', 'long_unrealised_pnl': '0.0', 'long_settled_pnl': '0', 'short_settled_pnl': '0.6770958', 'last': '4.156'},
    {'long_qty': '0', 'long_avail_qty': '0', 'long_avg_cost': '75.37', 'long_settlement_price': '75.37', 'realised_pnl': '-0.00029526', 'short_qty': '0', 'short_avail_qty': '0', 'short_avg_cost': '0', 'short_settlement_price': '0', 'liquidation_price': '0.00', 'instrument_id': 'LTC-USDT-200327', 'leverage': '3', 'created_at': '2020-02-22T08:02:07.424Z', 'updated_at': '2020-02-22T08:07:05.078Z', 'margin_mode': 'crossed', 'short_margin': '0.0', 'short_pnl': '0.0', 'short_pnl_ratio': '0.0', 'short_unrealised_pnl': '0.0', 'long_margin': '0.0', 'long_pnl': '0.0', 'long_pnl_ratio': '0.01791165', 'long_unrealised_pnl': '0.0', 'long_settled_pnl': '0', 'short_settled_pnl': '0', 'last': '75.82'}]]}
    返回结果说明：
    1.币本位合约和usdt本位合约的信息会一起返回。例如holding中第一行返回的是usdt本位合约数据，第二行返回的是币本位合约的数据
    2.一个币种同时有多头或者空头，也会在一行里面返回数据

    本函数输出示例：
         created_at    instrument_id     last  leverage  liquidation_price  long_avail_qty  long_avg_cost  long_leverage  long_liqui_price  long_maint_margin_ratio  long_margin  long_margin_ratio  long_pnl  long_pnl_ratio  long_qty  long_settled_pnl  long_settlement_price  long_unrealised_pnl margin_mode  realised_pnl  short_avail_qty  short_avg_cost  short_leverage  short_liqui_price  short_maint_margin_ratio  short_margin  short_margin_ratio  short_pnl  short_pnl_ratio  short_qty  short_settled_pnl  short_settlement_price  short_unrealised_pnl                updated_at
    eth-usdt  2020-02-22T08:02:04.469Z  ETH-USDT-200327  264.090       NaN                NaN             1.0        265.630           10.0           241.070                     0.01     0.027094           0.096762  -0.00154       -0.057975       1.0               0.0                265.630             -0.00154       fixed      0.000518              0.0      265.840000            10.0              0.000                      0.01      0.000000        10000.000000   0.000000         0.065829        0.0           0.000000                 265.840               0.00000  2020-02-22T08:42:02.484Z
    eos-usdt  2020-02-20T06:17:21.890Z  EOS-USDT-200327    4.127       NaN                NaN             1.0          4.126           10.0             3.753                     0.01     0.041270           0.100024   0.00000        0.000000       1.0               0.0                  4.126              0.00000       fixed     -0.001053              1.0        4.120000            10.0              4.476                      0.01      0.040400            0.096461  -0.000600        -0.014563        1.0           0.000000                   4.120              -0.00060  2020-02-22T09:53:15.931Z
    eos-usd   2020-02-18T06:42:29.924Z   EOS-USD-200327    4.158      10.0         130311.677             0.0          0.000            NaN               NaN                      NaN     0.000000                NaN   0.00000        0.000000       0.0               0.0                  0.000              0.00000     crossed      0.000000              3.0        4.535094             NaN                NaN                       NaN      0.721674                 NaN   0.601666         0.909537        3.0           0.677096                   4.114              -0.07543  2020-02-22T08:00:16.315Z
    ltc-usdt  2020-02-22T08:02p:07.424Z  LTC-USDT-200327   75.910       3.0              0.000             0.0         75.370            NaN               NaN                      NaN     0.000000                NaN   0.00000        0.020698       0.0               0.0                 75.370              0.00000     crossed     -0.000295              0.0        0.000000             NaN                NaN                       NaN      0.000000                 NaN   0.000000         0.000000        0.0           0.000000                   0.000               0.00000  2020-02-22T08:07:05.078Z
    """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            position_info = exchange.futures_get_position()['holding']
            # 整理数据
            df = pd.DataFrame(sum(position_info, []), dtype=float)
            # 防止账户初始化时出错
            if "instrument_id" in df.columns:
                df['index'] = df['instrument_id'].str[:-7].str.lower()
                df.set_index(keys='index', inplace=True)
                df.index.name = None
            return df
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


# ===通过ccxt获取K线数据
def ccxt_fetch_candle_data(exchange, symbol, time_interval, limit, max_try_amount=5):
    """
    本程序使用ccxt的fetch_ohlcv()函数，获取最新的K线数据，用于实盘
    :param exchange:
    :param symbol:
    :param time_interval:
    :param limit:
    :param max_try_amount:
    :return:
    """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            data = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, limit=limit)
            # 整理数据
            df = pd.DataFrame(data, dtype=float)
            df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                               3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
            df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
            df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
            df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
            return df
        except Exception as e:
            print('获取fetch_ohlcv获取合约K线数据，失败，稍后重试。失败原因：\n', e)
            time.sleep(short_sleep_time)

    _ = '获取fetch_ohlcv合约K线数据，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


# ===获取指定账户，例如btcusdt合约，目前的现金余额。
def ccxt_update_account_equity(exchange, symbol, max_try_amount=5):
    """
    使用okex私有函数，GET/api/futures/v3/accounts/<underlying>，获取指定币种的账户现金余额。
    :param exchange:
    :param underlying:  例如btc-usd，btc-usdt
    :param max_try_amount:
    :return:
    """
    for _ in range(max_try_amount):
        try:
            result = exchange.futures_get_accounts_underlying(params={"underlying": symbol.lower()})
            return float(result['equity'])
        except Exception as e:
            print(e)
            print('ccxt_update_account_equity函数获取账户可用余额失败，稍后重试')
            time.sleep(short_sleep_time)
            pass


# =====趋势策略相关函数
# 根据账户信息、持仓信息，更新symbol_info
def update_symbol_info(exchange, symbol_info, symbol_config):
    """
    本函数通过ccxt_fetch_future_account()获取合约账户信息，ccxt_fetch_future_position()获取合约账户持仓信息，并用这些信息更新symbol_config
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :return:
    """

    # 通过交易所接口获取合约账户信息
    future_account = ccxt_fetch_future_account(exchange)
    # 将账户信息和symbol_info合并
    if future_account.empty is False:
        symbol_info['账户权益'] = future_account['equity']

    # 通过交易所接口获取合约账户持仓信息
    future_position = ccxt_fetch_future_position(exchange)
    # 将持仓信息和symbol_info合并
    if future_position.empty is False:
        # 去除无关持仓：账户中可能存在其他合约的持仓信息，这些合约不在symbol_config中，将其删除。
        instrument_id_list = [symbol_config[x]['instrument_id'] for x in symbol_config.keys()]
        future_position = future_position[future_position.instrument_id.isin(instrument_id_list)]

        # 从future_position中获取原始数据
        symbol_info['最大杠杆'] = future_position['leverage']
        symbol_info['当前价格'] = future_position['last']

        symbol_info['多头持仓量'] = future_position['long_qty']
        symbol_info['多头均价'] = future_position['long_avg_cost']
        symbol_info['多头收益率'] = future_position['long_pnl_ratio']
        symbol_info['多头收益'] = future_position['long_pnl']

        symbol_info['空头持仓量'] = future_position['short_qty']
        symbol_info['空头均价'] = future_position['short_avg_cost']
        symbol_info['空头收益率'] = future_position['short_pnl_ratio']
        symbol_info['空头收益'] = future_position['short_pnl']

        # 检验是否同时持有多头和空头
        temp = symbol_info[(symbol_info['多头持仓量'] > 0) & (symbol_info['空头持仓量'] > 0)]
        if temp.empty is False:
            print(list(temp.index), '当前账户同时存在多仓和空仓，请平掉其中至少一个仓位后再运行程序，程序exit')
            exit()

        # 整理原始数据，计算需要的数据
        # 多头、空头的index
        long_index = symbol_info[symbol_info['多头持仓量'] > 0].index
        short_index = symbol_info[symbol_info['空头持仓量'] > 0