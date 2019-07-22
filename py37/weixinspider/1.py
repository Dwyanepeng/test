#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 9:13
# @Site    : 
# @File    : 1.py
# @Software: PyCharm

#遵循PEP8规则
import time
import json
import re
import random
import csv

from selenium import webdriver
from lxml import html, etree
from scrapy import Selector
import requests



# 获取cookies和token
class C_ookie:
    # 初始化
    def __init__(self):
        self.html = ''

    # 获取cookie
    def get_cookie(self):
        url = 'https://mp.weixin.qq.com'
        Browner = webdriver.Chrome()
        Browner.get(url)
        # 获取账号输入框
        ID = Browner.find_element_by_name('account')
        # 获取密码输入框
        PW = Browner.find_element_by_name('password')
        # 输入账号
        id = '1406133166@qq.com'
        pw = 'pl19940314'
        # id = input('请输入账号:')
        # pw = input('请输入密码:')
        ID.send_keys(id)
        PW.send_keys(pw)
        # 获取登录button，点击登录
        Browner.find_element_by_class_name('btn_login').click()
        # 等待扫二维码
        time.sleep(10)
        ck = Browner.get_cookies()
        ck1 = json.dumps(ck)
        with open('ck.txt','w') as f :
            f.write(ck1)
            f.close()
        self.html = Browner.page_source
        # with open('html.txt', 'w') as f:
        #     f.write(self.html)
        #     f.close()
        print(type(self.html), 'html', self.html)

	# 获取token，在页面中提取
    def Token(self):
        print('type', type(html))
        etree = html.etree
        h = etree.HTML(self.html)
        url = h.xpath('//a[@title="首页"]/@href')[0]
        print(url)
        token = re.findall('\d+',url)
        print('token', type(token), token)
        with open('token.txt', 'w') as f:
            f.write(token[0])
            f.close()
        return token

# 获取文章
class getEssay:
    def __init__(self):
        html = ''
        url = 'https://mp.weixin.qq.com'
        Browner = webdriver.Chrome()
        Browner.get(url)
        # 获取账号输入框
        ID = Browner.find_element_by_name('account')
        # 获取密码输入框
        PW = Browner.find_element_by_name('password')
        # 输入账号
        id = '1406133166@qq.com'
        pw = 'pl19940314'
        # id = input('请输入账号:')
        # pw = input('请输入密码:')
        ID.send_keys(id)
        PW.send_keys(pw)
        # 获取登录button，点击登录
        Browner.find_element_by_class_name('btn_login').click()
        # 等待扫二维码
        time.sleep(10)
        cooki={}
        cks = Browner.get_cookies()
        # self.cookie = ck
        # ck1 = json.dumps(ck)
        # with open('ck.txt', 'w') as f:
        #     f.write(ck1)
        #     f.close()
            # 获取cookies
        # with open('ck.txt', 'r') as f:
        #     cookie = f.read()
        #     f.close()
        for ck in cks:
            cooki[ck['name']] = ck['value']
        ck1 = json.dumps(cooki)
        ck1= json.loads(ck1)
        self.cookie = ck1
        print('type_cookie', type(ck1), ck1)
        html = Browner.page_source
        # etree = html.etree
        h = Selector(text=html)
        # h = etree.HTML(html)

        # h = requests.get(html)
        # h = h.text
        url = h.xpath('//a[@title="首页"]/@href').extract_first()
        print('url', url)
        self.token = re.findall(r'token=(\d+)', url)[0]
        # print(token)
        # with open('token.txt', 'w') as f:
        #     f.write(token[0])
        #     f.close()

        # 获取cookies
        # with open('ck.txt','r') as f :
        #     cookie = f.read()
        #     f.close()
        # self.cookie = json.loads(cookie)

        # 获取token
        self.header = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'
        }
        m_url = 'https://mp.weixin.qq.com'
        # response = requests.get(url=m_url, cookies=self.cookie)
        # print(response.text)
        # self.token = re.findall(r'token=(\d+)', str(response.url))[0]

        # fakeid与name
        self.fakeid = []


    # 获取公众号信息
    def getGname(self):
        # 请求头
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mp.weixin.qq.com',
        'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=%d&lang=zh_CN'%int(self.token),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
         }
        # 地址
        url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        # query = input('请输入要搜索的公众号关键字:')
        # begin = int(input('请输入开始的页数:'))
        query = '海关'
        begin = 0
        begin *= 5
        # 请求参数
        data = {
            'action': 'search_biz',
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax':' 1',
            'random': random.random(),
            'query': query,
            'begin': begin,
            'count': '5'
        }
        # 请求页面，获取数据
        res = requests.get(url=url, cookies=self.cookie, headers=headers, params=data)
        name_js = res.text
        name_js = json.loads(name_js)
        print('name_js', name_js)
        list = name_js['list']
        for i in list:
            time.sleep(1)
            fakeid = i['fakeid']
            nickname =i['nickname']
            print(nickname,fakeid)
            self.fakeid.append((nickname,fakeid))

    # 获取文章url
    def getEurl(self):

        url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mp.weixin.qq.com',
        'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=%d&lang=zh_CN'%int(self.token),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
         }

        # 遍历fakeid，访问获取文章链接
        for i in self.fakeid:
            time.sleep(1)
            fake = i[1]
            data = {
                'token': self.token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': 0,
                'count': 5,
                'fakeid': fake,
                'type': 9
                 }
            res = requests.get(url, cookies=self.cookie, headers=headers, params=data)
            js = res.text
            link_l = json.loads(js)
            self.parJson(link_l)

    # 解析提取url
    def parJson(self,link_l):
        l = link_l['app_msg_list']
        for i in l:
            link = i['link']
            name = i['digest']
            self.saveData(name,link)

    # 保存数据进csv中
    def saveData(self,name,link):
        with open('link.csv' ,'a',encoding='utf8') as f:
            w = csv.writer(f)
            w.writerow((name,link))
            print('ok')


# C = C_ookie()
# C.get_cookie()
# token = C.Token()
#
G = getEssay()
G.getGname()
G.getEurl()


# C = C_ookie()
# C.get_cookie()
# C.Token()