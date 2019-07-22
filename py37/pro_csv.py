#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 16:52
# @Site    : 
# @File    : pro_csv.py
# @Software: PyCharm

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r'label.csv', usecols=[1]    )
print(data)
df = data.values
d = []
for i in df:
    d.append(i[0])
print(d, type(d))
x = pd.read_csv(r'f2_pre_test2.csv')
df1 = x.values
d1 = []
for j in df1:
    d1.append(j[0])
print(type(d1), len(d1), d1)
plt.plot(range(1,1001,1), d[-1000::])
plt.plot(range(1,1001,1), d1[-1000::], color = 'r')
plt.show()