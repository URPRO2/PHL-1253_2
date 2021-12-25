
import os, sys
import time

if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
import pandas as pd
import ccxt

import Code.base.wechat as wechat
from Code.config.configLoad import *

from program.三_少年意气.番外1_币安u本位择时策略实盘.Function import *
from program.三_少年意气.番外1_币安u本位择时策略实盘.Config import *
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.unicode.ambiguous_as_wide', True)  # 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.east_asian_width', True)

wx = wechat.WeChat()




def main(exchange, symbol_config, time_interval):
    # =判断是否单向持仓，若不是程序退出
    if_oneway_mode(exchange)

    # ==========获取需要交易币种的历史数据==========
    # 获取数据
    max_candle_num = 500  # 每次获取的K线数量
    symbol_candle_data = get_binance_history_candle_data(exchange, symbol_config, time_interval, max_candle_num)

    # =进入每次的循环
    while True:
        # ==========获取持仓数据==========
        # 初始化symbol_info，在每次循环开始时都初始化，防止上次循环的内容污染本次循环的内容。
        symbol_info_columns = ['账户权益', '分配比例', '分配资金', '持仓方向', '持仓量', '持仓收益', '持仓均价', '当前价格']
        symbol_info = pd.DataFrame(index=symbol_config.keys(), columns=symbol_info_columns)  # 转化为dataframe
        symbol_info['分配比例'] = pd.DataFrame(symbol_config).T['position']

        # 更新账户信息symbol_info
        symbol_info = binance_update_account(exchange, symbol_config, symbol_info)
        print('持仓信息\n', symbol_info)

        # ==========根据当前时间，获取策略下次执行时间，例如16:15。并sleep至该时间==========
        run_time = sleep_until_run_time(time_interval, if_sleep=True)

        # ==========获取最新的k线数据==========
        exchange.timeout = 1000  # 即将获取最新数据，临时将timeout设置为1s，加快获取数据速度
        # 获取数据
        recent_candle_num = 1000
        recent_candle_data = single_threading_get_binance_candle_data(exchange, symbol_config, symbol_info,
                                                                      time_interval, run_time, recent_candle_num)
        # 将最近的数据打印出
        for symbol in symbol_config.keys():
            print(recent_candle_data[symbol].tail(min(2, recent_candle_num)))

        # 将symbol_candle_data和最新获取的recent_candle_data数据合并
        symbol_candle_data = symbol_candle_data_append_recent_candle_data(symbol_candle_data, recent_candle_data,
                                                                          symbol_config, max_candle_num)

        # ==========计算每个币种的交易信号==========
        symbol_signal = calculate_signal(symbol_info, symbol_config, symbol_candle_data)
        print('\n产生信号时间:\n', symbol_info[['当前价格', '持仓方向', '目标持仓', '信号时间']])
        print('\n本周期交易计划:', symbol_signal)

        # ==========下单==========
        exchange.timeout = exchange_timeout  # 下单时需要增加timeout的时间，将timout恢复正常
        # 计算下单信息
        symbol_order_params = cal_all_order_info(symbol_signal, symbol_info, symbol_config, exchange)
        print('\n订单参数\n', symbol_order_params)

        # 开始批量下单
        place_binance_batch_order(exchange, symbol_order_params)

        if len(symbol_order_params) != 0:
            wx.send_data('\n本周期交易计划:' + sys.argv[1] + ' ' + str(symbol_signal) + str(symbol_candle_data.iloc[-1]['close']))
        # 本次循环结束
        print('\n', '-' * 40, '本次循环结束，%d秒后进入下一次循环' % long_sleep_time, '-' * 40, '\n\n')
        time.sleep(long_sleep_time)


if __name__ == '__main__':
    arv = sys.argv[1]
    # ==========配置运行相关参数==========
    # =k线周期
    time_interval = '15m'  # 目前支持5m，15m，30m，1h，2h等。得交易所支持的K线才行。最好不要低于5m

    # =交易所配置
    BINANCE_CONFIG = {
        'apiKey': apiSecretDict[arv][0],
        'secret': apiSecretDict[arv][1],
        'timeout': exchange_timeout,
        'rateLimit': 10,
        'verbose': False,
        'hostname': 'fapi.binance.com',
        'enableRateLimit': False}