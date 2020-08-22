"""
"""
import ccxt
from Code.Function import *
from Code.config.configLoad import *

print(ccxt.__version__)  # 检查ccxt版本，需要最新版本，1.44.21以上

# ===参数设定
coin = 'btc'.upper()  # 要套利的币种
future_date = '210625'  # 要套利的合约到期时间
coin_precision = 1  # 去行情页面上，看下这个币种合约的价格是小数点后几位。如果小数点后有3位，那么c