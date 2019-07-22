#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 13:56
# @Site    : 
# @File    : test.py
# @Software: PyCharm
import json

# train_data = json.load(open('../datasets/train_data.json'))

# file = open('../datasets/dev_data.json', 'r', encoding='utf-8')
# info = json.load(file)

with open("../datasets/all_50_schemas", encoding="utf-8", mode="r") as f2:
    ret = f2.readlines()
print(type(ret))
print(ret)

predicate2id = {}
id2predicate = {}
line = 0
with open("../datasets/all_50_schemas", 'r',encoding='utf-8') as f:
    for l in f:
        d = eval(l)
        predicate2id[d['predicate']] = line
        id2predicate[line] = d['predicate']
        line += 1
print('predicate2id', predicate2id)
print('id2predicate', id2predicate)
print(len(id2predicate))


def processdata(path):
    data = []
    line = 0
    with open(path,'r',encoding='utf-8') as f:
        for l in f:
            d = (eval(l))
            data.append(d)
            line += 1
            # if (line > 200):
            #     break
    return data

print(processdata(r'E:\code\py37\bert\datasets\train_data.json'))
