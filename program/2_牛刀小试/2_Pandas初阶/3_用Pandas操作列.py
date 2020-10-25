"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 列操作
- 针对列的统计函数
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# =====导入数据
df = pd.read_csv(
    # 该参数为数据在电脑中的路径，
    # 要注意字符串转义符号 \ ，可以使用加r变为raw string或者每一个进行\\转义
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    # 编码格式，不同的文件有不同的编码方式，一般文件中有中文的，编码是gbk，默认是utf8
    # ** 大家不用去特意记住很多编码，我们常用的就是gbk和utf8，切换一下看一下程序不报错就好了
    encoding='gbk',
    nrows=15,
    # 该参数代表跳过数据文件的的第1行不读入
    skiprows=1,
    # 将指定列设置为index。若不指定，index默认为0, 1, 2, 3, 4...
    # index_col=['candle_begin_time'],
)

# =====列操作
# 行列加减乘除
# print(df['candle_begin_time'] + ' UTC时间')  # 字符串列可以直接加上字符串，对整列进行操作
# print(df['close'] * 