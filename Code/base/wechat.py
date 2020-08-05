#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
import os


class WeChat:
    def __init__(self):
        self.CORPID = 'ww3ffaaf40c09cf232'  #企业ID，在管理后台获取
        self.CORPSECRET = 'IZ1XYgpPlldPAnGf3j-q1lx5tFTuLXz9kSt2DVkRRFM'#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000004'  #应用ID，在后台应用中获取
        self.TOUSER = "ZhouJian"  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        if not os.path.isdir('./tmp'):
            os.mkdir('./tmp')
        try:
            with open('./tmp/wechat.config', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('./tmp/wechat.config', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('./tmp/wechat.config', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENT