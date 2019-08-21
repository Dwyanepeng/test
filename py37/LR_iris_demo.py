#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 10:16
# @Site    : 
# @File    : LR_iris_demo.py
# @Software: PyCharm
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from LogisticRegression import LogisticRegression

#取鸢尾花数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target
#筛选特征
X = X[y<2, :2]
y = y[y<2]

#绘制图像
plt.scatter(X[y == 0, 0], X[y == 0, 1], color="red")
plt.scatter(X[y == 1, 0], X[y == 1, 1], color="blue")
plt.show()

#切分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=666)

#调用自己写的逻辑回归函数
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
print("final score is :%s" % log_reg.score(X_test, y_test))
print("actual prob is :", log_reg.predict_proba(X_test))