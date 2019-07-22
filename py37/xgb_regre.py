#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 16:13
# @Site    : 
# @File    : xgb_regre.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_absolute_error

#读取原始文件数据
X = pd.read_csv('params.csv').values
y = pd.read_csv('label.csv', usecols=['AntiSpot']).values

#准备数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
print(len(X_train), len(X_test), y_train, y_test)

model = xgb.XGBRegressor(max_depth=60, learning_rate=0.9,  n_estimators=320, silent=True, objective='reg:gamma')
# model = xgb.XGBRegressor(max_depth=60, learning_rate=0.1, n_estimators=5,
#              silent=True, objective='reg:linear', booster='gblinear', n_jobs=50,
#              nthread=None, gamma=0, min_child_weight=1, max_delta_step=0, subsample=1,
#              colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1,
#              scale_pos_weight=1, base_score=0.5, random_state=0, seed=None,
#              missing=None, importance_type='gain')
model.fit(X_train, y_train)
model.save_model('model1')
#tar = xgb.Booster(model_file='tree100.model')
#x_test1 = xgb.DMatrix(x_test)
#fit_pred1 = tar.predict(x_test1)
#预测训练集
ans = model.predict(X_train)
print('ans', len(ans), ans)
ans = pd.DataFrame(ans)
ans.to_csv('f1_pre_train3.csv', index=None)
mae = mean_absolute_error(ans,y_train)
print('训练集mae', mae)

#预测测试集
ans1 = model.predict(X_test)
print('ans1', len(ans1), ans1)
ans1 = pd.DataFrame(ans1)
ans1.to_csv('f1_pre_test.csv', index=None)
mae1 = mean_absolute_error(ans1,y_test)
print('测试集mae', mae1)



# plot_importance(model)
# plt.show()