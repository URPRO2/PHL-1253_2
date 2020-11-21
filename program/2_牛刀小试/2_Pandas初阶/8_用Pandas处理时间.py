"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- pandas中的时间处理
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    encoding='gbk',
    skiprows=1
)

# ===== 时间处理
# print(df[