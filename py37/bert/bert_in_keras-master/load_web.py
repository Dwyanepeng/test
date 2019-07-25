#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 9:58
# @Site    : 
# @File    : load_web.py
# @Software: PyCharm

'''运行bert_web.py，模拟浏览器登录，前台传参数给后台循环测试bert 关系抽取模型'''
from selenium import webdriver
from scrapy.selector import Selector
import random

browser = webdriver.Firefox()
root_url = 'http://127.0.0.1:8000/ml/relation_extract/?txt='
txt = ['《当痞子女爱上黑道少爷》是在小说阅读网上连载的一部热血青春小说，作者是嗜血梦儿',
       '《血战异世》是所谓节写的网络小说连载于17k小说网',
       '不够完美是由蔡健雅演唱的一首歌，歌曲收录在 《i do believe》专辑里,国语歌曲',
       '《金蛇缘》是连载于晋江文学城的一部小说，作者是唐孑',
       '《摩登时代》是2016年发行，刘凤瑶演唱的音乐单曲',
       '《相遇》是2010年上海译文出版社出版的图书，作者是米兰·昆德拉',
       '《魔武杀神》是连载于纵横中文网的网络小说，作者是风家少主',
       '《儿童看图读古谣》是2005年金盾出版社出版的书籍，作者是崔亮海',
       '《古城堡》是岳夏的音乐作品，收录在《爱你胜过爱自己》专辑中',
       '俞恩焕  [明]字二酉，浙江平湖诸生',
       '《蜜宠—老婆你最大》是乔茉児写的网络小说连载于潇湘书院',
       '麝鹿，拉丁学名noschus noschiferus linnaeus，是哺乳纲偶蹄目麝科的一种动物，形状像鹿而且小，在我国四川、湖南、湖北、青海等地广泛分布，是国家一级保护动物',
       '《今夜星光灿烂》由陈秀男谱曲，丁晓雯作词，由姜育恒演唱',
       '简介都邦财产保险股份有限公司（简称“都邦保险”）是经中国保险监督  管理委员会批准，于2005年10月19日开业的全国性财产保险公司，注册地为吉林省吉林市，总部位于北京',
       '铅色食籽雀是一种脊索动物门、鸟纲、雀形目、鹀科、食籽雀属类生物，分布于阿根廷，玻利维亚，巴西，哥伦比亚，法属圭亚那，圭亚那，巴拉圭，秘鲁，苏里南，委内瑞拉',
       '后来吴宇森得到了电影《终极标靶》导演的机会，由当时当红的动作明星尚格云顿主演',
       '《腾空的日子》是由毕鑫业执导，李佳航、胡冰卿、郑家彬领衔主演',]
for i in range(1000):
    txt.append(txt[random.randint(0,16)])
    # print(type(random.randint(0,16)), random.randint(0, 16))
print(len(txt), txt)

for j in range(len(txt)):
    url = root_url + txt[j]
    browser.get(url)
# res = Selector(text=browser.page_source)
