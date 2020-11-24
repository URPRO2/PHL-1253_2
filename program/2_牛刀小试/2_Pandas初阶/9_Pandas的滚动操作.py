"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- Rolling操作
- Expanding操作
- 输出到本地文件
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    encoding='gbk',
    skiprows=1
)

# =====rolling
# 计算'close'这一列的均值
# print(df['close'])
# 如何得到每个周期的最近3个周期收盘价的均值呢？即如何计算常用的移动平均线？
# 使用rolling函数
# df['收盘价_移动平均线'] = df['close'].r