from .client import Client
from .consts import *


class TradeAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_ser