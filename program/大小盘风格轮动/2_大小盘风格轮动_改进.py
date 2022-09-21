
'''
邢不行 | 量化小讲堂系列文章
《抱团股会一直涨？无脑执行大小盘轮动策略，轻松跑赢指数5倍【附Python代码】》
https://mp.weixin.qq.com/s/hPjVbBKomfMhowc32jUwhA
获取更多量化文章，请联系邢不行个人微信：xbx3642
'''
import pandas as pd
import numpy as np
from function import *
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

import pandas as pd


def getSymbolData(symbol, rule_type='4H'):
    df = pd.read_hdf(r'C:\Users\jan\Documents\xingbuxing\coin2020\data\%s.h5' % symbol, key='df')
