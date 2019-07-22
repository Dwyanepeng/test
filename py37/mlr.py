#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 10:14
# @Site    : 
# @File    : mlr.py
# @Software: PyCharm

import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#读取原始文件数据
X = pd.read_csv('params.csv').values
y = pd.read_csv('label.csv', usecols=['SituComp']).values

# X = X[:]
# y = y[:, 0]
print(X)
print(y)

#准备数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, shuffle=True)
print(len(X_train), X_train)
print(len(X_test), X_test)
print(len(y_train), y_train)
print(len(y_test), y_test)
X_train = X_train*100
X_test = X_test*100
y_train = y_train[:, 0]*100
y_test = y_test[:, 0]*100


# 训练数据
regr = linear_model.LinearRegression(normalize=True)
regr.fit(X_train, y_train)
print('coefficients(b1,b2...):',regr.coef_)
print('intercept(b0):',regr.intercept_)
#
# # 预测
# x_test = np.array([[8,2.0,1.2,90,17.5,0.85,120,2.5,55,22.5],[6,2.0,1.2,90,17.5,0.85,80,4.0,55,32.5],[10,2.0,1.2,30,17.5,1.05,40,4.0,35,32.5]])
y_pre = regr.predict(X_test)
print(y_pre)
print(y_test)

plt.plot(range(1, 2954, 1), y_test, label='True')
plt.plot(range(1, 2954, 1), y_pre, label='NN', color='r')
plt.legend()
plt.show()