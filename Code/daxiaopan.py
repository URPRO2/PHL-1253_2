import ccxt
from datetime import timedelta
import pandas as pd
import time
import sys,os
if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
from base.Tool import *
from Code.base import w