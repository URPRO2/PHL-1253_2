'''
邢不行 | 量化小讲堂系列文章
《抱团股会一直涨？无脑执行大小盘轮动策略，轻松跑赢指数5倍【附Python代码】》
https://mp.weixin.qq.com/s/hPjVbBKomfMhowc32jUwhA
获取更多量化文章，请联系邢不行个人微信：xbx3642
'''
import pandas as pd

def evaluate_investment(source_data, tittle,time='交易日期'):
    temp = source_data.copy()
    # ===新建一个datafr