import pandas as pd
import numpy as np


def equity_curve_for_OKEx_USDT_future_next_open(df, slippage=1/1000,c_rate=5/10000,leverage_rate=3,face_value=0.01,min_margin_ratio=1/100):
    """
    计算持仓的开始时间
    计算持仓时能买入多少张
    计算买入后剩余的钱（扣除买入手续费）
    计算卖出的手续费
    计算盈亏（滑点的