"""
邢不行2021策略分享会
币安期现套利自动建仓程序
邢不行微信：xbx3636
"""
import ccxt
from Function import *

print(ccxt.__version__)  # 检查ccxt版本，需要最新版本，1.44.21以上

# ===参数设定
coin = 'btc'.upper()  # 要套利的币种
future_date = '210625'  # 要套利的合约到期时间
coin_precision = 1  # 去行情页面上，看下这个币种合约的价格是小数点后几位。如果小数点后有3位，那么coin_precision就是3
execute_amount = 2000  # 每次建仓usdt的数量。如果是btc的话，得是100的整数倍。其他币种得是10的整数倍。每次数量不要太多，太多会造成价格波动。建议数量在1000-3000之间。
max_execute_num = 5  # 最大建仓次数。建仓这些次数之后程序就会停止。
r_threshold = 0.1  # 高于利差就开始入金，0.05代表5%
spot_fee_rate = 1 / 1000 