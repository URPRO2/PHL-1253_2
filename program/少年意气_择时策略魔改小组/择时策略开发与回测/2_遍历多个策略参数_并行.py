
"""
《邢不行-2020新版|Python数字货币量化投资课程》
择时策略魔改研究小组（第1期）
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9585
本程序作者: 邢不行
"""
from datetime import timedelta
from multiprocessing import Pool, cpu_count
from datetime import datetime
from program.少年意气_择时策略魔改小组.择时策略开发与回测 import Signals
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Position import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Evaluate import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Function import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Statistics import *
from functools import partial
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====回测固定参数
tag = '20210415'  # 本次回测标记
description = '回测数据基于币安usdt现货的分钟数据（~-2020年8月31日），在okex的usdt本位交割合约进行交易回测。' \
              'pos:position_for_OKEx_future, equity:equity_curve_for_OKEx_USDT_future_next_open'

leverage_rate = 2
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
symbol_face_value = {'BTC': 0.01, 'EOS': 10, 'ETH': 0.1, 'LTC': 1,  'XRP': 100}
drop_days = 10  # 币种刚刚上线10天内不交易


# =====批量遍历策略参数
# ===单次循环
def calculate_by_one_loop(para, df, signal_name, symbol, rule_type):
    _df = df.copy()
    # 计算交易信号
    _df = getattr(Signals, signal_name)(_df, para=para)
    # 计算实际持仓
    _df = position_for_OKEx_future(_df)
    # 币种上线10天之后的日期
    t = _df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
    _df = _df[_df['candle_begin_time'] > t]
    # 计算资金曲线
    face_value = symbol_face_value[symbol]
    _df = equity_curve_for_OKEx_USDT_future_next_open(_df, slippage=slippage, c_rate=c_rate,
                                                      leverage_rate=leverage_rate,
                                                      face_value=face_value,
                                                      min_margin_ratio=min_margin_ratio)

    # 保存策略收益
    rtn = pd.DataFrame()
    rtn.loc[0, 'para'] = str(para)
    r = _df.iloc[-1]['equity_curve']
    rtn.loc[0, '累计净值'] = r  # 最终收益
    rtn.loc[0, '年化收益'], rtn.loc[0, '最大回撤'], rtn.loc[0, '年化收益回撤比'] = return_drawdown_ratio(_df)
    print(signal_name, symbol, rule_type, para, '策略收益：', r)
    return rtn


if __name__ == '__main__':
    for signal_name in ['signal_simple_bolling']:
        for symbol in ['BTC', 'ETH']:
            for rule_type in ['4H', '2H', '1H', '30T', '15T']:
                print(signal_name, symbol, rule_type)
                print('开始遍历该策略参数：', signal_name, symbol, rule_type)

                # ===读入数据
                df = pd.read_pickle(root_path + '/data/%s-USDT_5m.pkl' % symbol)
                # 任何原始数据读入都进行一下排序、去重，以防万一
                df.sort_values(by=['candle_begin_time'], inplace=True)
                df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
                df.reset_index(inplace=True, drop=True)

                # =====转换为其他分钟数据
                period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
                    {'open': 'first',
                     'high': 'max',