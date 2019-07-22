#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 9:25
# @Site    : 
# @File    : xgb_pred_f2.py
# @Software: PyCharm

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

#读取原始文件数据
X = pd.read_csv('params.csv').values
y = pd.read_csv('label.csv', usecols=['SituComp']).values

#准备数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

tar = xgb.Booster(model_file='tree100.model')
x_test1 = xgb.DMatrix(X_test)
fit_pred1 = tar.predict(x_test1)
fit_pred1 = pd.DataFrame(fit_pred1)
fit_pred1.to_csv('fit_pred2.csv', index=None)