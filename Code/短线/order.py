
import ccxt
import pandas as pd
"""
获取现货数据
             free  locked
asset                    
LTC      0.000010     0.0
BNB      0.897109     0.0
USDT     0.037928     0.0
BAT    318.220000     0.0
DOGE   101.100000     0.0
"""
def update_account(exchange):
    # 获取账户信息
    account_info = exchange.privateGetAccount()
    # 将持仓信息转变成datafra