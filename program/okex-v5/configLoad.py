import os
import configparser


class Config(object):
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        self._path = "config.ini"
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self.