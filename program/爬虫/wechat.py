#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = 'ww3ffaaf40c09cf232'  #企业ID，在管理后台获取
        self.CORPSECRET = 'IZ1XYgpPlldPAnGf3j-q1lx5tFTuLXz9kSt2DVkRRFM'#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000004'  #应用ID，在后台应用中获取
        self.TOUSER = "KongKong"  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret