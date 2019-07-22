#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 14:22
# @Site    : 
# @File    : f2.py
# @Software: PyCharm

import pandas as pd
import numpy as np
from keras.layers import Dense,Dropout,Activation,Input
from keras.models import Sequential,Model
from keras import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn import preprocessing


#神经网络模型构建
def make_model(InputSize):
    model=Sequential()
    model.add(Dense(units=1024, kernel_initializer='normal', activation='tanh',input_shape=(InputSize,)))
    # model.add(Dense(units=2048, kernel_initializer='normal', activation='tanh'))
    # model.add(Dense(units=256, kernel_initializer='normal', activation='tanh'))
    # model.add(Dense(units=128, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(units=1, kernel_initializer='normal', activation='sigmoid'))
    model.compile(loss='mean_squared_error',optimizer='adam',metrics=[metrics.mae])
    print(model.summary())
    return model

if __name__ == '__main__':
    #划分训练集和测试集的输入输出
    data = pd.read_csv('params.csv')
    data['para11'] = data['para1'] + data['para2']
    data['para12'] = data['para3'] + data['para4']
    data['para13'] = data['para5'] + data['para6']
    data['para14'] = data['para7'] + data['para8']
    data['para15'] = data['para9'] + data['para10']
    data['para16'] = data['para2'] + data['para3']
    data['para17'] = data['para4'] + data['para5']
    data['para18'] = data['para6'] - data['para7']
    data['para19'] = data['para8'] - data['para9']

    x = data.values
    min_max_scaler = preprocessing.MinMaxScaler([-50,90])
    x = min_max_scaler.fit_transform(x)
    print('x', x)
    train_X = x[0:54000]
    train_X = pd.DataFrame(train_X)
#     print(len(trainX),trainX)
    test_X = x[54000::]
    test_X = pd.DataFrame(test_X)
#     print(type(testX), len(testX),testX)

    y = pd.read_csv('label.csv', usecols=['SituComp'])
#     print(type(y), y)
    train_Y = y[0:54000]
    test_Y = y[54000::]
#     print(trainY, testY)

    model=make_model(19)

    #训练模型并保存为module.h5
    model.fit(train_X,train_Y,batch_size=32,epochs=10,verbose=1,validation_data=(test_X,test_Y),shuffle=True)
    model.save_weights('modulef2_1.h5')

    #加载已保存的模型
    # model.load_weights('modulef2_效果比较好.h5',by_name=False)

    #预测并评估结果
    pred=model.predict(test_X)
    # pd.DataFrame(pred).to_csv('f2_效果不错的.csv')
    print('test_Y', len(test_Y), test_Y)
    print('pred', len(pred), pred)
    plt.plot(range(1, 5050, 1), test_Y[-5049::],label='True')
    plt.plot(range(1, 5050, 1), pred, label='NN', color='r')
    plt.legend()
    plt.show()
    score=r2_score(test_Y,pred)
    error=mean_squared_error(test_Y,pred)
    print('score', score)
    print('mse', error)