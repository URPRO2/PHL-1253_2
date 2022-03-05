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

    df.loc[open_pos_condition, 'sta