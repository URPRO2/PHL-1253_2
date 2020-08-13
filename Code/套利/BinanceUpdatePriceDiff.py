"""
自动更新 期现价差
"""
import pandas
import time
import datetime
import ccxt

time_interval = 5  # 数据抓取间隔时间
diff_target = 0.08  