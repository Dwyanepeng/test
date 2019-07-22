#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/9 14:20
# @Site    : 
# @File    : read_excel.py
# @Software: PyCharm

#将json文件解析存入csv
import pandas as pd
import json
import numpy as np

data = pd.read_excel('gongsi.xls', sheet_name=2)

list = data['公司'].to_list()
print(data['公司'], type(data))

print(list, len(list))
people = data['人员'].to_list()
# print(people, len(people))

gongsi_list = []
for i in range(len(people)):
    dict_people = json.loads(people[i])
    # print(dict_people)
    index = ''
    for j in range(len(dict_people)):
        gongsi_list1 = []
        index = str(j+1)
        gongsi_list1.append(list[i])
        gongsi_list1.append(dict_people[index][0])
        gongsi_list1.append(dict_people[index][1])
        # matrix = np.array(gongsi_list1)
        # matrixT = matrix.T
        print(type(gongsi_list1), gongsi_list1)
        df = pd.DataFrame(data=[gongsi_list1], columns=['','',''], index=None)
        print('df', df)
        df.to_csv('gongsi4.csv', mode='a', header=False, index=None, line_terminator='\n')

