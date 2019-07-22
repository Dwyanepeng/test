#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 9:59
# @Site    : 
# @File    : parse.py
# @Software: PyCharm

# _*_ coding=utf-8 _*_

import requests
import json
url='http://credit.customs.gov.cn/ccppserver/ccpp/queryList'
payload={"manaType":"0","apanage":"","depCodeChg":"","curPage":"2","pageSize":20}
headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '73',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'credit.customs.gov.cn',
        'Origin': 'http://credit.customs.gov.cn',
        'Referer': 'http://credit.customs.gov.cn/ccppwebserver/pages/ccpp/html/directory.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
aa=requests.post(url=url,headers=headers,data=json.dumps(payload))
print(aa.text)
