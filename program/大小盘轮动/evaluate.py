import pandas as pd
import numpy as np


def equity_curve_for_OKEx_USDT_future_next_open(df, slippage=1/1000,c_rate=5/10000,leverage_rate=3,face_value=0.01,min_margin_ratio=1/100):
    """
    计算持仓的开始时间
    计算持仓时能买入多少张
    计算买入后剩余的钱（扣除买入手续费）
    计算卖出的手续费
    计算盈亏（滑点的计算）
    计算净值 （收盘价）
    计算最小最大净值（最高最低）计算爆仓用
    """

    df['next_open'] = df['open'].shift(-1)
    df['next_open'].fillna(value=df['close'],inplace=True)

    #开仓（开空，开多）K线
    condition1 = df['pos'] != 0
    condition2 = df['pos'] != df['pos'].shift(1)
    open_pos_condition = condition1 & condition2

    condition3 = df['pos'] != df['pos'].shift(-1)
    close_pos_condition = condition3 & condition1

    df.loc[open_pos_condition, 'start_time'] = df['candle_begin_time']
    # df['start_time'].fillna(method='ffill',inplace=True)
    df.loc[df['pos']==0, 'start_time'] = pd.NaT

    # ===计算资金曲线
    initial_cash = 10000  # 初始资金
    # ---在开仓时
    # 以开盘价计算合约数量 （当资金量大可以用5分钟均价）   :   多少张 = 价格 / 单张价格
    df.loc[open_pos_condition, 'contract_num'] = initial_cash * leverage_rate / ( face_value * df['open'])
    df['contract_num'] = np.floor(df['contract_num'])  # 取整

    df.loc[open_pos_condition,'open_pos_price'] = df['open'] * (1 + slippage * df['pos'])  # 滑点价
    df['cash'] = initial_cash - df['open_pos_price'] * face_value * df['contract_num'] * c_rate  # 剩余钱 = 保证金 （扣除手续费）