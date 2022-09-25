'''
邢不行 | 量化小讲堂系列文章
《抱团股会一直涨？无脑执行大小盘轮动策略，轻松跑赢指数5倍【附Python代码】》
https://mp.weixin.qq.com/s/hPjVbBKomfMhowc32jUwhA
获取更多量化文章，请联系邢不行个人微信：xbx3642
'''
import pandas as pd

def evaluate_investment(source_data, tittle,time='交易日期'):
    temp = source_data.copy()
    # ===新建一个dataframe保存回测指标
    results = pd.DataFrame()

    # ===计算累积净值
    results.loc[0, '累积净值'] = round(temp[tittle].iloc[-1], 2)

    # ===计算年化收益
    annual_return = (temp[tittle].iloc[-1]) ** (
            '1 days 00:00:00' / (temp[time].iloc[-1] - temp[time].iloc[0]) * 365) - 1
    results.loc[0, '年化收益'] = str(round(annual_return * 100, 2)) + '%'

    # ===计算最大回撤，最大回撤的含义：《如何通过3行代码计算最大回撤》https://mp.weixin.qq.com/s/Dwt4lkKR_PEnWRprLlvPVw
    # 计算当日之前的资金曲线的最高点
    temp['max2here'] = temp[tittle].expanding().max()
    # 计算到历史最高值到当日的跌幅，drowdwon
    temp['d