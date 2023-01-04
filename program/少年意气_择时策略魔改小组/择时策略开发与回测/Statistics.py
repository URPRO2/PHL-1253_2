"""
《邢不行-2020新版|Python数字货币量化投资课程》
择时策略魔改研究小组（第1期）
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9585
本程序作者: 邢不行
"""
import pandas as pd
import numpy as np
import itertools


# ======= 策略评价 =========
# 将资金曲线数据，转化为交易数据
def transfer_equity_curve_to_trade(equity_curve):
    """
    将资金曲线数据，转化为一笔一笔的交易
    :param equity_curve: 资金曲线函数计算好的结果，必须包含pos
    :return:
    """
    # =选取开仓、平仓条件
    condition1 = equity_curve['pos'] != 0
    condition2 = equity_curve['pos'] != equity_curve['pos'].shift(1)
    open_pos_condition = condition1 & condition2

    # =计算每笔交易的start_time
    if 'start_time' not in equity_curve.columns:
        equity_curve.loc[open_pos_condition, 'start_time'] = equity_curve['candle_begin_time']
        equity_curve['start_time'].fillna(method='ffill', inplace=True)
        equity_curve.loc[equity_curve['pos'] == 0, 'start_time'] = pd.NaT

    # =对每次交易进行分组，遍历每笔交易
    trade = pd.DataFrame()  # 计算结果放在trade变量中

    for _index, group in equity_curve.groupby('start_time'):

        # 记录每笔交易
        # 本次交易方向
        trade.loc[_index, 'signal'] = group['pos'].iloc[0]

        # 本次交易杠杆倍数
        if 'leverage_rate' in group:
            trade.loc[_index, 'leverage_rate'] = group['leverage_rate'].iloc[0]

        g = group[group['pos'] != 0]  # 去除pos=0的行
        # 本次交易结束那根K线的开始时间
        trade.loc[_index, 'end_bar'] = g.iloc[-1]['candle_begin_time']
        # 开仓价格
        trade.loc[_index, 'start_price'] = g.iloc[0]['open']
        # 平仓信号的价格
        trade.loc[_index, 'end_price'] = g.iloc[-1]['close']
        # 持仓k线数量
        trade.loc[_index, 'bar_num'] = g.shape[0]
        # 本次交易收益
        trade.loc[_index, 'change'] = (group['equity_change'] + 1).prod() - 1
        # 本次交易结束时资金曲线
        trade.loc[_index, 'end_equity_curve'] = g.iloc[-1]['equity_curve']
        # 本次交易中资金曲线最低值
        trade.loc[_index, 'min_equity_curve'] = g['equity_curve'].min()

    return trade


# 计算策略评价指标
def strategy_evaluate(equity_curve, trade):
    """
    :param equity_curve: 带资金曲线的df
    :param trade: transfer_equity_curve_to_trade的输出结果，每笔交易的df
    :return:
    """

    # ===新建一个dataframe保存回测指标
    results = pd.DataFrame()

    # ===计算累积净值
    results.loc[0, '累积净值'] = round(equity_curve['equity_curve'].iloc[-1], 2)

    # ===计算年化收益
    annual_return = (equity_curve['equity_curve'].iloc[-1] / equity_curve['equity_curve'].iloc[0]) ** (
        '1 days 00:00:00' / (equity_curve['candle_begin_time'].iloc[-1] - equity_curve['candle_begin_time'].iloc[0]) * 365) - 1
    results.loc[0, '年化收益'] = str(round(annual_return, 2)) + ' 倍'

    # ===计算最大回撤，最大回撤的含义：《如何通过3