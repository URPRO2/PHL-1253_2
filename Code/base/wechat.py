#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
import os


class WeChat:
    def __init__(self):
        self.CORPID = 'ww3ffaaf40c09cf232'  #企业ID，在管理后台获取
  