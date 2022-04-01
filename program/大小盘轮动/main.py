import pandas as pd
import datetime
import ccxt
import time

# import talib
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', None)


def get_sma_diff(symbol, limit, timeframe):
    df = ex.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=20)
    df = pd.DataFrame(df, dtype=float)
    df.rename(columns={0: 'candle_begin_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
