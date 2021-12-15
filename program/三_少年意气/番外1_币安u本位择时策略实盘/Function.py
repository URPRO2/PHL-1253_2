
"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
币安u本位择时策略实盘框架相关函数
"""
import ccxt
import math
import pandas as pd
from datetime import datetime, timedelta
import time
from program.三_少年意气.番外1_币安u本位择时策略实盘.Config import *
from program.三_少年意气.番外1_币安u本位择时策略实盘 import Signals


# ==========辅助功能函数==========
# ===下次运行时间，和课程里面讲的函数是一样的
def next_run_time(time_interval, ahead_seconds=5):
    """
    根据time_interval，计算下次运行的时间，下一个整点时刻。
    目前只支持分钟和小时。
    :param time_interval: 运行的周期，15m，1h
    :param ahead_seconds: 预留的目标时间和当前时间的间隙
    :return: 下次运行的时间
    案例：
    15m  当前时间为：12:50:51  返回时间为：13:00:00
    15m  当前时间为：12:39:51  返回时间为：12:45:00
    10m  当前时间为：12:38:51  返回时间为：12:40:00
    5m  当前时间为：12:33:51  返回时间为：12:35:00
    5m  当前时间为：12:34:51  返回时间为：12:35:00

    1h  当前时间为：14:37:51  返回时间为：15:00:00
    2h  当前时间为：00:37:51  返回时间为：02:00:00

    30m  当前时间为：21日的23:33:51  返回时间为：22日的00:00:00
    5m  当前时间为：21日的23:57:51  返回时间为：22日的00:00:00

    ahead_seconds = 5
    15m  当前时间为：12:59:57  返回时间为：13:15:00，而不是 13:00:00
    """
    if time_interval.endswith('m') or time_interval.endswith('h'):
        pass
    elif time_interval.endswith('T'):
        time_interval = time_interval.replace('T', 'm')
    elif time_interval.endswith('H'):
        time_interval = time_interval.replace('H', 'h')
    else:
        print('time_interval格式不符合规范。程序exit')
        exit()

    ti = pd.to_timedelta(time_interval)
    now_time = datetime.now()
    # now_time = datetime(2019, 5, 9, 23, 50, 30)  # 指定now_time，可用于测试
    this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    min_step = timedelta(minutes=1)

    target_time = now_time.replace(second=0, microsecond=0)

    while True:
        target_time = target_time + min_step
        delta = target_time - this_midnight
        if delta.seconds % ti.seconds == 0 and (target_time - now_time).seconds >= ahead_seconds:
            # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
            break

    print('\n程序下次运行的时间：', target_time, '\n')
    return target_time


# ===依据时间间隔, 自动计算并休眠到指定时间
def sleep_until_run_time(time_interval, ahead_time=1, if_sleep=True):
    """
    根据next_run_time()函数计算出下次程序运行的时候，然后sleep至该时间
    :param time_interval:
    :param ahead_time:
    :param if_sleep:
    :return:
    """

    # 计算下次运行时间
    run_time = next_run_time(time_interval, ahead_time)

    # sleep
    if if_sleep:
        time.sleep(max(0, (run_time - datetime.now()).seconds))
        # 可以考察：print(run_time - n)、print((run_time - n).seconds)
        while True:  # 在靠近目标时间时
            if datetime.now() > run_time:
                break

    return run_time


# ===将最新数据和历史数据合并
def symbol_candle_data_append_recent_candle_data(symbol_candle_data, recent_candle_data, symbol_config, max_candle_num):

    for symbol in symbol_config.keys():
        df = symbol_candle_data[symbol].append(recent_candle_data[symbol], ignore_index=True)
        df.drop_duplicates(subset=['candle_begin_time_GMT8'], keep='last', inplace=True)
        df.sort_values(by='candle_begin_time_GMT8', inplace=True)  # 排序，理论上这步应该可以省略，加快速度
        df = df.iloc[-max_candle_num:]  # 保持最大K线数量不会超过max_candle_num个
        df.reset_index(drop=True, inplace=True)
        symbol_candle_data[symbol] = df

    return symbol_candle_data


# ===重试机制
def retry_wrapper(func, params={}, act_name='', sleep_seconds=3, retry_times=5):
    """
    需要在出错时不断重试的函数，例如和交易所交互，可以使用本函数调用。
    :param func: 需要重试的函数名
    :param params: func的参数
    :param act_name: 本次动作的名称
    :param sleep_seconds: 报错后的sleep时间
    :param retry_times: 为最大的出错重试次数
    :return:
    """

    for _ in range(retry_times):
        try:
            result = func(params=params)
            return result
        except Exception as e:
            print(act_name, '报错，报错内容：', str(e), '程序暂停(秒)：', sleep_seconds)
            time.sleep(sleep_seconds)
    else:
        # send_dingding_and_raise_error(output_info)
        raise ValueError(act_name, '报错重试次数超过上限，程序退出。')


# ==========交易所交互函数==========
# ===判断当前持仓模式
def if_oneway_mode(exchange):
    """
    判断当前合约持仓模式。必须得是单向模式。如果是双向模式，就报错。
    查询当前的持仓模式。使用函数：GET /fapi/v1/positionSide/dual (HMAC SHA256)
    判断持仓情况，False为单向持仓，True为单向持仓
    :param exchange:
    :return:
    """

    positionSide = retry_wrapper(exchange.fapiPrivateGetPositionSideDual, act_name='查看合约持仓模式')

    if positionSide['dualSidePosition']:
        raise ValueError("当前持仓模式为双向持仓，程序已停止运行。请去币安官网改为单向持仓。")
    else:
        print('当前持仓模式：单向持仓')


# ===获得币对精度
def usdt_future_exchange_info(exchange, symbol_config):
    """
    获取symbol_config中币种的最小下单价格、数量
    :param exchange:
    :return:
    使用接口：GET /fapi/v1/exchangeInfo
    文档：https://binance-docs.github.io/apidocs/futures/cn/#0f3f2d5ee7
    """

    # 获取u本为合约交易对的信息
    exchange_info = retry_wrapper(exchange.fapiPublic_get_exchangeinfo, act_name='查看合约基本信息')

    # 转化为dataframe
    df = pd.DataFrame(exchange_info['symbols'])
    # df['minPrice'] = df['filters'].apply(lambda x: x[0]['minPrice'])
    # df['minQty'] = df['filters'].apply(lambda x: x[1]['minQty'])
    df['tickSize'] = df['filters'].apply(lambda x: math.log(1/float(x[0]['tickSize']), 10))
    df['stepSize'] = df['filters'].apply(lambda x: math.log(1/float(x[1]['stepSize']), 10))
    df = df[['symbol', 'pricePrecision', 'quantityPrecision', 'tickSize', 'stepSize']]
    df.set_index('symbol', inplace=True)

    # 赋值
    for symbol in symbol_config.keys():
        symbol_config[symbol]['最小下单价精度'] = round(df.at[symbol, 'tickSize'])

        p = float(df.at[symbol, 'quantityPrecision'])  #
        symbol_config[symbol]['最小下单量精度'] = None if p == 0 else round(p)


# ===获取当前持仓信息
def binance_update_account(exchange, symbol_config, symbol_info):
    """
    获取u本位账户的持仓信息、账户余额信息