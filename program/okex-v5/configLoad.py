import os
import configparser


class Config(object):
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        self._path = "config.ini"
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)


global_config = Config()
apiKey = global_config.getRaw('config', 'apiKey')
secret = global_config.getRaw('config', 'secret')
password = global_config.getRaw('config', 'password')
short_sleep_time = int(global_config.getRaw('config', 'short_sleep_time'))  # 用于和交易所交互时比较紧急的时间sleep，例如获取数据、下单
medium_sleep_time = i