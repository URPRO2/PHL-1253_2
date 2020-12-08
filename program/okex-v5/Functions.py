
import datetime
import base64
import hmac
from hashlib import sha256
import time
import math
import json
import requests
from urllib import parse
import pandas as pd

from configLoad import *
import Signals
import okex.Trade_api as Trade
tradeAPI = Trade.TradeAPI(apiKey, secret, password, False, '1')

# baseUrl = 'http://www.okex.com/' # 服务器用这个域名
baseUrl = 'http://www.okex.vip/'


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}

session = requests.session()  # 利用session记录每次请求的cookie，加快请求获取数据速度


def getPrivateHeaders(requestPath, requestMethod):
    """
    okex sign生成方式：
    OK-ACCESS-SIGN的请求头是对timestamp + method + requestPath + body字符串（+表示字符串连接），以及SecretKey，
    使用HMAC SHA256方法加密，通过Base-64编码输出而得到的。

    如：sign=CryptoJS.enc.Base64.Stringify(CryptoJS.HmacSHA256(timestamp + 'GET' + '/users/self/verify', SecretKey))

    其中，timestamp的值与OK-ACCESS-TIMESTAMP请求头相同，为ISO格式，如2020-12-08T09:08:57.715Z。
    :param urlAddress:
    :param requestMethod: 'GET/POST'
    :return:
    """
    timestamp = str(datetime.datetime.utcnow().replace(microsecond=0).isoformat()) + '.715Z'
    headers = {
        'Content-Type':'application/json',
        'OK-ACCESS-KEY': apiKey,
        'OK-ACCESS-SIGN': get_hmac_sha256(timestamp + requestMethod + requestPath, secret),
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': password,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'x-simulated-trading': '1'  # 模拟盘需要加这个参数，实盘得去掉该参数
    }
    return headers


# ===通过交易所V5接口获取合约账户信息
def fetch_future_account(max_try_amount=5):
    """
    :param max_try_amount:最大尝试次数
    :return:

    逐仓：

        1.账户权益=账户余额+逐仓仓位账户余额+所有合约的已实现盈亏+所有合约的未实现盈亏

        2.可用保证金=账户余额+逐仓仓位账户余额+本合约已实现盈亏- 当前仓位的持仓所需保证金 - 挂单冻结保证金

    """
    for _ in range(max_try_amount):
        try:
            getFuturePositionUrl = baseUrl+'api/v5/account/balance?ccy=USDT'
            future_info = session.get(getFuturePositionUrl, headers=getPrivateHeaders('/api/v5/account/balance?ccy=USDT', 'GET'), timeout=3).json()['data']
            # 交易的是usdt本位保证金合约，因此这里用统一账户的usdt保证金余额来做可用保证金
            # isoEq		美金层面逐仓仓位权益
            # availEq	可用保证金

            for ccyMsg in future_info[0].get('details'):
                if ccyMsg.get('ccy') == 'USDT':
                    # 返回两个值，账户总权益和可用保证金
                    return float(ccyMsg.get('disEq', 0)), float(ccyMsg.get('availEq', 0))
            # 如果没查询到那么就返回0
            return 0,0
        except Exception as e:
            print('通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败，稍后重试：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


def fetch_future_position(max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:
    本程序使用okex3中“交割合约API”、“所有合约持仓信息”接口，获取合约账户所有合约的持仓信息。

    """
    for _ in range(max_try_amount):
        try:
            getFuturePositionUrl = baseUrl+'api/v5/account/positions#instType=FUTURES'
            future_info = \
            session.get(getFuturePositionUrl, headers=getPrivateHeaders('/api/v5/account/positions', 'GET'),
                         timeout=3).json()['data']
            return future_info
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


def update_symbol_info(symbol_info, symbol_config):
    """
        :param exchange:
        :param max_try_amount:
        :return:

        没考虑到同时持有反方向合约时候的错误情况
        """
    isoEquity,_ = fetch_future_account()  # 获取当前的账户权益信息
    # 将账户信息和symbol_info合并

    symbol_info['账户权益'] = isoEquity

    futurePositionMsgList = fetch_future_position()
    # futurePositionMsgDf.index = futurePositionMsgDf['instId']

    if futurePositionMsgList:
        # 去除无关持仓：账户中可能存在其他合约的持仓信息，这些合约不在symbol_config中，将其删除。
        for symbol in symbol_config.keys():
            for futureMsg in futurePositionMsgList:
                # 如果目标持仓合约的代码和返回实际持仓代码信息一致，那么我们将数据读入进来
                # ['账户权益', '持仓方向', '持仓量', '持仓收益率', '持仓收益', '持仓均价', '当前价格', '最大杠杆']
                if symbol_config[symbol].get('instrument_id') == futureMsg.get('instId'):
                    # 账户持仓量
                    symbol_info.loc[symbol, '持仓量'] = futureMsg.get('pos')

                    # 最大杠杆
                    symbol_info.loc[symbol, '最大杠杆'] = futureMsg.get('lever')

                    # 当前价格
                    symbol_info.loc[symbol, '当前价格'] = futureMsg.get('last')

                    # 持仓均价
                    symbol_info.loc[symbol, '持仓均价'] = futureMsg.get('avgPx')

                    # 持仓收益
                    symbol_info.loc[symbol, '持仓收益'] = futureMsg.get('upl')

                    # 持仓收益率
                    symbol_info.loc[symbol, '持仓收益'] = futureMsg.get('upl')

                    # 持仓方向，如果同时持有两个方向的合约那么，程序报错

                    symbol_info.loc[symbol, '持仓收益率'] = futureMsg.get('uplRatio')

                    # 账户持仓量
                    posSide = 1 if futureMsg.get('posSide') == 'long' else -1
                    # 如果已经持有同种合约的仓位，那么程序可能存在问题，程序报错退出程序
                    if type(symbol_info.loc[symbol, '持仓方向']) == type(1):
                        print('同时持有两份相同合约，请检查程序！')
                        exit()
                    symbol_info.loc[symbol, '持仓方向'] = posSide
        symbol_info['持仓方向'].fillna(value=0, inplace=True)

    else:
        # 当future_position为空时，将持仓方向的控制填充为0，防止之后判定信号时出错
        symbol_info['持仓方向'].fillna(value=0, inplace=True)

    return symbol_info


# ===通过V5api获取K线数据
def fetch_candle_data( symbol, time_interval, limit, max_try_amount=5):
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
            klineUrl = baseUrl+'api/v5/market/candles?instId={symbol}&bar={bar}&limit={limit}'.format(
                symbol=symbol, bar=time_interval,limit = limit)
            data = session.get(klineUrl,headers=headers,timeout=1).json()['data']
            # 整理数据
            df = pd.DataFrame(reversed(data), dtype=float)
            df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                               3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
            df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
            df['candle_begin_time_GMT8'] = df['candle_begin_time'] + datetime.timedelta(hours=8)
            df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
            return df
        except Exception as e:
            print('获取fetch_ohlcv获取合约K线数据，失败，稍后重试。失败原因：\n', e)
            time.sleep(short_sleep_time)

    _ = '获取fetch_ohlcv合约K线数据，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


# =========获取行情数据函数============
# 获取历史k线数据
def fetch_okex_symbol_history_candle_data(symbol, time_interval, max_len, max_try_amount=5):
    """
    获取某个币种在okex交易所所有能获取的历史数据，目前v5接口最多获取1440根。
    :param exchange:
    :param symbol:
    :param time_interval:
    :param max_len:
    :param max_try_amount:
    :return:

    函数核心逻辑：
    1.找到最早那根K线的开始时间，以此为参数获取数据
    2.获取数据的最后一行数据，作为新的k线开始时间，继续获取数据
    3.如此循环直到最新的数据
    """
    # 获取当前时间
    now_milliseconds = int(time.time() * 1e3)

    # 每根K线的间隔时间
    time_interval_int = int(time_interval[:-1])  # 若15m，则time_interval_int = 15；若2h，则time_interval_int = 2
    if time_interval.endswith('m'):
        time_segment = time_interval_int * 60 * 1000  # 15分钟 * 每分钟60s
    elif time_interval.endswith('h'):
        time_segment = time_interval_int * 60 * 60 * 1000  # 2小时 * 每小时60分钟 * 每分钟60s

    # 计算开始和结束的时间
    end = now_milliseconds - time_segment
    since = end - max_len * time_segment


    # 循环获取历史数据
    all_kline_data = []
    while end - since >= time_segment:
        kline_data = []
        klineUrl = baseUrl+'api/v5/market/history-candles?instId={symbol}&before={before}&after={after}&bar={bar}&limit=100'.format(
            symbol=symbol, before=since,after=int(since + 100 * time_segment), bar=time_interval)

        # 获取K线使，要多次尝试
        for i in range(max_try_amount):
            try:
                kline_data = session.get(klineUrl, headers=headers,timeout=3).json()['data']
                break
            except Exception as e:
                time.sleep(medium_sleep_time)
                if i == (max_try_amount - 1):
                    _ = '【获取需要交易币种的历史数据】阶段，fetch_okex_symbol_history_candle_data函数中，' \
                        '使用ccxt的fetch_ohlcv获取K线数据失败，程序Raise Error'
                    send_dingding_and_raise_error(_)

        if kline_data:
            since = int(kline_data[0][0])  # 更新since，为下次循环做准备
            all_kline_data += reversed(kline_data)


        else:
            print('【获取需要交易币种的历史数据】阶段，fetch_ohlcv失败次数过多，程序exit，请检查原因。')
            exit()
        # 对数据进行整理
    df = pd.DataFrame(all_kline_data, dtype=float)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + datetime.timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

    # 删除重复的数据
    df.drop_duplicates(subset=['candle_begin_time_GMT8'], keep='last', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 为了保险起见，去掉最后一行最新的数据
    df = df[:-1]

    print(symbol, '获取历史数据行数：', len(df))

    return df

# 获取需要的K线数据，并检测质量。
def get_candle_data(symbol_config, time_interval, run_time, max_try_amount, candle_num, symbol):
    """
    使用ccxt_fetch_candle_data(函数)，获取指定交易对最新的K线数据，并且监测数据质量，用于实盘。
    :param exchange:
    :param symbol_config:
    :param time_interval:
    :param run_time:
    :param max_try_amount:
    :param symbol:
    :param candle_num:
    :return:
    尝试获取K线数据，并检验质量
    """
    # 标记开始时间
    start_time = datetime.datetime.now()
    print('开始获取K线数据：', symbol, '开始时间：', start_time)

    # 获取数据合约的相关参数
    instrument_id = symbol_config[symbol]["instrument_id"]  # 合约id
    signal_price = None

    # 尝试获取数据
    for i in range(max_try_amount):
        # 获取symbol该品种最新的K线数据
        df = fetch_candle_data(instrument_id, time_interval, limit=candle_num)
        if df.empty:
            continue  # 再次获取

        # 判断是否包含最新一根的K线数据。例如当time_interval为15分钟，run_time为14:15时，即判断当前获取到的数据中是否包含14:15这根K线
        # 【其实这段代码可以省略】
        if time_interval.endswith('m'):
            _ = df[df['candle_begin_time_GMT8'] == (run_time - datetime.timedelta(minutes=int(time_interval[:-1])))]
        elif time_interval.endswith('h'):
            _ = df[df['candle_begin_time_GMT8'] == (run_time - datetime.timedelta(hours=int(time_interval[:-1])))]
        else:
            print('time_interval不以m或者h结尾，出错，程序exit')
            exit()
        if _.empty:
            print('获取数据不包含最新的数据，重新获取')
            time.sleep(short_sleep_time)
            continue  # 再次获取

        else:  # 获取到了最新数据
            signal_price = df.iloc[-1]['close']  # 该品种的最新价格
            df = df[df['candle_begin_time_GMT8'] < pd.to_datetime(run_time)]  # 去除run_time周期的数据
            print('结束获取K线数据', symbol, '结束时间：', datetime.datetime.now())
            return symbol, df, signal_price

    print('获取candle_data数据次数超过max_try_amount，数据返回空值')
    return symbol, pd.DataFrame(), signal_price

# 串行获取K线数据
def single_threading_get_data(symbol_info, symbol_config, time_interval, run_time, candle_num, max_try_amount=5):
    """
    串行逐个获取所有交易对的K线数据，速度较慢。和multi_threading_get_data()对应
    若获取数据失败，返回空的dataframe。
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :param time_interval:
    :param run_time:
    :param candle_num:
    :param max_try_amount:
    :return:
    """
    # 函数返回的变量
    symbol_candle_data = {}
    for symbol in symbol_config.keys():
        symbol_candle_data[symbol] = pd.DataFrame()

    # 逐个获取symbol对应的K线数据
    for symbol in symbol_config.keys():
        _, symbol_candle_data[symbol], symbol_info.at[symbol, '信号价格'] = get_candle_data(symbol_config, time_interval, run_time, max_try_amount, candle_num, symbol)

    return symbol_candle_data


# 根据最新数据，计算最新的signal
def calculate_signal(symbol_info, symbol_config, symbol_candle_data):
    """
    计算交易信号
    :param symbol_info:
    :param symbol_config:
    :param symbol_candle_data:
    :return:
    """

    # 输出变量
    symbol_signal = {}

    # 逐个遍历交易对
    for symbol in symbol_config.keys():

        # 赋值相关数据
        df = symbol_candle_data[symbol].copy()  # 最新数据
        now_pos = symbol_info.at[symbol, '持仓方向']  # 当前持仓方向
        avg_price = symbol_info.at[symbol, '持仓均价']  # 当前持仓均价

        # 需要计算的目标仓位
        target_pos = None

        # 根据策略计算出目标交易信号。
        if not df.empty:  # 当原始数据不为空的时候
            target_pos = getattr(Signals, symbol_config[symbol]['strategy_name'])(df, now_pos, avg_price, symbol_config[symbol]['para'])
        symbol_info.at[symbol, '目标仓位'] = target_pos  # 这行代码似乎可以删除
        print(target_pos)

        # 根据目标仓位和实际仓位，计算实际操作，"1": "开多"，"2": "开空"，"3": "平多"， "4": "平空"
        if now_pos == 1 and target_pos == 0:  # 平多
            symbol_signal[symbol] = [3]
        elif now_pos == -1 and target_pos == 0:  # 平空
            symbol_signal[symbol] = [4]
        elif now_pos == 0 and target_pos == 1:  # 开多
            symbol_signal[symbol] = [1]
        elif now_pos == 0 and target_pos == -1:  # 开空
            symbol_signal[symbol] = [2]
        elif now_pos == 1 and target_pos == -1:  # 平多，开空
            symbol_signal[symbol] = [3, 2]
        elif now_pos == -1 and target_pos == 1:  # 平空，开多
            symbol_signal[symbol] = [4, 1]

        symbol_info.at[symbol, '信号时间'] = datetime.datetime.now()  # 计算产生信号的时间

    return symbol_signal,symbol_info

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

# 在合约市场下单
def single_threading_place_order(symbol_info, symbol_config, symbol_signal, max_try_amount=5):
    """
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :param symbol_signal:
    :param max_try_amount:
    :return:
    串行使用okex_future_place_order()函数，下单

    函数返回值案例：
                         symbol      信号价格                       信号时间
    4476028903965698  eth-usdt  227.1300 2020-03-01 11:53:00.580063
    4476028904156161  xrp-usdt    0.2365 2020-03-01 11:53:00.580558
    """
    # 函数输出变量
    symbol_order = pd.DataFrame()

    # 如果有交易信号的话
    if symbol_signal:
        # 遍历有交易信号的交易对
        for symbol in symbol_signal.keys():
            # 下单
            _, order_id_list = okex_future_place_order(symbol_info, symbol_config, symbol_signal, max_try_amount, symbol)

            # 记录
            for order_id in order_id_list:
                symbol_order.loc[order_id, 'symbol'] = symbol
                # 从symbol_info记录下单相关信息
                symbol_order.loc[order_id, '信号价格'] = symbol_info.loc[symbol, '信号价格']
                symbol_order.loc[order_id, '信号时间'] = symbol_info.loc[symbol, '信号时间']

    return symbol_order
# 串行下单
def okex_future_place_order(symbol_info, symbol_config, symbol_signal, max_try_amount, symbol):
    """
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :param symbol_signal:
    :param max_try_amount:
    :param symbol:
    :return:
    """
    # 下单参数 "ccy": "", "clOrdId": "", "tag": "", "posSide": "short", "px": "", "reduceOnly": ""
    params = {
        'instId': symbol_config[symbol]["instrument_id"],  # 合约代码
        'tdMode':'cross', # 逐仓下单
        'ordType':'limit', # 限价单
        "ccy": "",
        "clOrdId": "",
        "tag": "",
        "reduceOnly": ""
    }

    order_id_list = []
    # 按照交易信号下单
    for order_type in symbol_signal[symbol]:
        update_price_flag = False  # 当触发限价条件时会设置为True、0
        for i in range(max_try_amount):
            try:
                # 当只要开仓或者平仓时，直接下单操作即可。但当本周期即需要平仓，又需要开仓时，需要在平完仓之后，
                # 重新评估下账户资金，然后根据账户资金计算开仓账户然后开仓。下面这行代码即处理这个情形。
                # "长度为2的判定"定位【平空，开多】或【平多，开空】两种情形，"下单类型判定"定位 处于开仓的情形。
                if len(symbol_signal[symbol]) == 2 and order_type in [1, 2]:  # 当两个条件同时满足时，说明当前处于平仓后，需要再开仓的阶段。
                    time.sleep(short_sleep_time)  # 短暂的休息1s，防止之平仓后，账户没有更新
                    _,availEq = fetch_future_account()
                    symbol_info.at[symbol, "账户权益"] = availEq

                # 确定下单参数
                """
                side	String	是	订单方向 buy：买 sell：卖
                posSide	String	可选	持仓方向 在双向持仓模式下必填，且仅可选择 long 或 short
                """
                if order_type == 1: # 开多
                    params['side'] = 'buy'
                    params['posSide'] = 'long'
                if order_type == 2: # 开空
                    params['side'] = 'sell'
                    params['posSide'] = 'short'
                if order_type == 3: # 平多
                    params['side'] = 'sell'
                    params['posSide'] = 'long'
                if order_type == 4: # 平空
                    params['side'] = 'buy'
                    params['posSide'] = 'short'


                params['px'] = str(cal_order_price(symbol_info.at[symbol, "信号价格"], order_type))
                params['sz'] = str(cal_order_size(symbol, symbol_info, symbol_config[symbol]['leverage']))

                if update_price_flag:

                    # 获取当前限价
                    # {
                    #     "code": "0",
                    #     "msg": "",
                    #     "data": [
                    #         {
                    #             "instType": "SWAP",
                    #             "instId": "BTC-USDT-SWAP",
                    #             "buyLmt": "200",
                    #             "sellLmt": "300",
                    #             "ts": "1597026383085"
                    #         }
                    #     ]
                    # }
                    limitPriceUrl = baseUrl+'api/v5/public/price-limit?instId='+symbol_config[symbol]['instrument_id']
                    response = session.get(limitPriceUrl,headers=headers,timeout=1).json()['data'][0]
                    # 依据下单类型来判定，所用的价格
                    order_type_tmp = int(order_type)
                    # 开多和平空，对应买入合约取最高
                    if order_type_tmp in [1, 4]:
                        params['price'] = response['sellLmt']
                    elif order_type_tmp in [2, 3]:
                        params['price'] = response['buyLmt']
                    update_price_flag = False

                print('开始下单：', datetime.datetime.now())
                order_info = tradeAPI.place_order(instId=params['instId'], tdMode=params['tdMode'], side=params['side'], posSide=params['posSide'],
                                              ordType=params['ordType'], sz=params['sz'],px=params['px'])['data'][0]
                # order_info = session.post(baseUrl+'api/v5/trade/order',headers=getPrivateHeaders('/api/v5/trade/order'+str(json.dumps(params)),'POST'),data=json.dumps(params),timeout=1)
                order_id_list.append(order_info['ordId'])
                print(order_info, '下单完成：', datetime.datetime.now())

                break

            except Exception as e:
                print(e)
                print(symbol, '下单失败，稍等后继续尝试')
                time.sleep(short_sleep_time)
                """
                okex {"error_message":"Order price cannot be more than 103% or less than 97% of the previous minute price","code":32019,"error_code":"32019",
                "message":"Order price cannot be more than 103% or less than 97% of the previous minute price"}
                """
                # error code 与错误是一一对应的关系，51006代表相关错误
                if "51006" in str(e):
                    update_price_flag = True

                if i == (max_try_amount - 1):
                    print('下单失败次数超过max_try_amount，终止下单')
                    send_dingding_msg('下单失败次数超过max_try_amount，终止下单，程序不退出')
                    # exit() 若在子进程中（Pool）调用okex_future_place_order，触发exit会产生孤儿进程

    return symbol, order_id_list



# 获取成交数据
def update_order_info(symbol_config, symbol_order, max_try_amount=5):
    """
    根据订单号，检查订单信息，获得相关数据
    :param exchange:
    :param symbol_config:
    :param symbol_order:
    :param max_try_amount:
    :return:

    函数返回值案例：
                             symbol      信号价格                       信号时间  订单状态 开仓方向 委托数量 成交数量    委托价格    成交均价                      委托时间
    4476028903965698  eth-usdt  227.1300 2020-03-01 11:53:00.580063  完全成交   开多  100  100  231.67  227.29  2020-03-01T03:53:00.896Z
    4476028904156161  xrp-usdt    0.2365 2020-03-01 11:53:00.580558  完全成交   开空  100  100  0.2317  0.2363  2020-03-01T03:53:00.906Z
    """

    # 下单数据不为空
    if symbol_order.empty is False:
        # 这个遍历下单id
        for order_id in symbol_order.index:
            time.sleep(medium_sleep_time)  # 每次获取下单数据时sleep一段时间
            order_info = None
            # 根据下单id获取数据
            for i in range(max_try_amount):
                try:
                    # para = {
                    #     'instrument_id': symbol_config[symbol_order.at[order_id, 'symbol']]["instrument_id"],
                    #     'order_id': order_id
                    # }
                    rightPart ='/api/v5/trade/order?ordId={ordId}&instId={instId}'.format(ordId=order_id, instId=symbol_config[symbol_order.at[order_id, 'symbol']]["instrument_id"])
                    getOrderDetailUrl=baseUrl[:-1]+rightPart
                    order_info = session.get(getOrderDetailUrl, headers=getPrivateHeaders(rightPart, 'GET'), timeout=5).json()['data'][0]
                    break
                except Exception as e:
                    print(e)
                    print('根据订单号获取订单信息失败，稍后重试')
                    time.sleep(medium_sleep_time)
                    if i == max_try_amount - 1:
                        send_dingding_msg("重试次数过多，获取订单信息失败，程序退出")
                        raise ValueError('重试次数过多，获取订单信息失败，程序退出')

            if order_info:
                symbol_order.at[order_id, "订单状态"] = order_info["state"]
                # if okex_order_state[order_info["state"]] == '失败':
                #     print('下单失败')
                # symbol_order.at[order_id, "开仓方向"] = okex_order_type[order_info["type"]]
                if order_info['side'] == 'buy' and order_info['posSide'] == 'long': # 开多
                    symbol_order.at[order_id, "开仓方向"] = okex_order_type['1']
                if order_info['side'] == 'sell' and order_info['posSide'] == 'short': # 开空
                    symbol_order.at[order_id, "开仓方向"] = okex_order_type['2']
                if order_info['side'] == 'sell' and order_info['posSide'] == 'long': # 平多
                    symbol_order.at[order_id, "开仓方向"] = okex_order_type['3']
                if order_info['side'] == 'buy' and order_info['posSide'] == 'short': # 平空