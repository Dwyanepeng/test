#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 15:07
# @Site    : 
# @File    : norm.py
# @Software: PyCharm

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

data = pd.read_csv(r'params.csv')
df = data.values
enc = preprocessing.OneHotEncoder()
e = enc.fit_transform(df)
print(e)
# enc.transform(e)
# print(enc.transform(e))