"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 排序
- 合并
- 去重
- 其他
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_20200302_5T.csv',
    skiprows=1,
    encoding='gbk'
)

# =====排序函数
# print(df.sort_values(by=['candle_begin_time'], ascending=True))  # by参数指定按照什么进行排序，ascending参数指定是顺序还是逆序
# print(df.sort_values(by=['symbol', 'candle_begin_time'], ascending=[1, 0]))  # 按照多列进行排序


# =====两个df上下合并操作，append操作
# df1 = df.iloc[0:10][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df1)
# df2 = df.iloc[5:15][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df2)
# print(df1.append(df2))  # append操作，将df1和df2上下拼接起来。注意观察拼接之后的index。index可以重复
# df3 = df1.append(df2, ignore_index=True)  # ignore_index参数，用户重新确定index
# print(df3)


# =====两个df左右合并操作，merge操作
# df1 = df.iloc[0:10][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df1)
# df2 = df.iloc[5:15][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df2)
#
# df_merged = pd.merge(left=df1, ri