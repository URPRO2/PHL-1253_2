"""
在此之前需要行情数据，备份
回测大小盘（BTC、ETH）
"""
import pandas as pd
from Tool import *
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# ==========整理出历史数据、转换4小时数据============
btcDf = getSymbolData('BTC-USDT_5m')
ethDf = getSymbolData('ETH-USDT_5m')
print(btcDf)
# btcDf['mean120'] = btcDf['cl