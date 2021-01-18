
"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
- 什么是周期转换
- 转换方法基础版
- 转换方法高阶版
- 数据清理
- 周期参数介绍
"""

import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# === 从hdf中读取1分钟数据
df: pd.DataFrame = pd.read_hdf(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\eos_1min_data.h5', key='all_data')
print(df.head(20))
# exit()

# 《数据周期转换示意图》


# === 第一种方法：1min k线数据转换为5min k线数据
# 将candle_begin_time设定为index
# df.set_index('candle_begin_time', inplace=True)

# 周期转换方法：resample
# rule_type = '5T'  # rule='5T'：意思是5分钟，意味着转变为5分钟k线数据
# period_df = df[['close']].resample(rule=rule_type).last()  # last：取这5分钟的最后一行数据
#
# # 开、高、低、收价格，成交量
# period_df['open'] = df['open'].resample(rule=rule_type).first()
# period_df['high'] = df['high'].resample(rule=rule_type).max()
# period_df['low'] = df['low'].resample(rule=rule_type).min()
# period_df['volume'] = df['volume'].resample(rule=rule_type).sum()
#
# period_df = period_df[['open', 'high', 'low', 'close', 'volume']]
# print(period_df)
# exit()

# === 第二种方法：将1分钟k线数据转为5分钟k线数据
# rule_type = '5T'
# period_df = df.resample(rule=rule_type, on='candle_begin_time', base=0, label='left', closed='left').agg(
#     {
#         'open': 'first',
#         'high': 'max',
#         'low': 'min',
#         'close': 'last',
#         'volume': 'sum',
#     }
# )
# period_df = period_df[['open', 'high', 'low', 'close', 'volume']]
# print(period_df)
# exit()
# base参数：帮助确定转换周期开始的时间
# label='left', closed='left'，建议统一设置成'left'


# === 去除不必要的数据
# 去除一次都没有交易的周期
# print(period_df)