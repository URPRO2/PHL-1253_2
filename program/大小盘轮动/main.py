import pandas as pd
import datetime
import ccxt
import time

# import talib
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', None)


def get_sma_diff(symbol, limit, timeframe):
    df = ex.fetc