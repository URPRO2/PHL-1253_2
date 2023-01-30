
# encoding: utf-8
# !/usr/bin/env python


import configparser
import time
import os
from http import cookiejar
import requests
import datetime

import wechat2
import json
from time import sleep
import getpass

class LeagueEngine:
    def __init__(self):
        self.USERID = 'zt007'
        self.PASSWORD = 'wsx123'
        self.URL = "47.111.231.208:8200"
        self._path = 'tmp/config.ini'
        self.headers = {
            "Host": self.URL,
            "Referer": "http://" + self.URL + "/bet/login",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self.token = ''
        self._get_access_token()

        self.itemPath = 'C:/Users/' + getpass.getuser() + '/Documents/GitHub/zuqiu/tmp/item_config.ini'
        self.itemConfig = configparser.ConfigParser()
        self.itemConfig.read(self.itemPath)

    def getItemName(self, name):
        h = self.itemConfig['name'].get(name)
        if not h:
            # print('未找到对应的xjw队名')
            return name  #None
        else:
            return h

    def _get_access_token(self):
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            pass  # print("还没有cookie信息")
        self.login()
        # self.cf = configparser.ConfigParser()  # configparser类来读取config文件

    def login(self):
        login_url = 'http://' + self.URL + '/api_v1/coolstorm/login'
        data = {
            'username': self.USERID,
            'password': self.PASSWORD
        }
        response = self.session.post(login_url, data=data, headers=self.headers)
        login_code = response.json()
        self.token = str(login_code['code'])

    def find_betid(self, betid, data):
        for item in data['bets']: