#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 9:38
# @Site    : 
# @File    : LogisticRegression.py
# @Software: PyCharm

import numpy as np
from sklearn.metrics import accuracy_score

class LogisticRegression(object):
    def __init__(self):
        """初始化Logistic Regression模型"""
        self.coef = None
        self.intercept = None
        self._theta = None

    def sigmoid(self, t):
        return 1. / (1. + np.exp(-t))

    def fit(self, X_train, y_train, alpha=0.01, n_iters=1e4):
        """使用梯度下降法训练LR模型"""
        assert  X_train.shape[0] == y_train.shape[0] #判断长度是否相等

        def J(theta, X_b, y):
            y_hat = self.sigmoid(X_b.dot(theta))
            try:
                return -np.sum(y * np.log(y_hat) + (1-y) * np.log(1 - y_hat))
            except:
                return float('inf')

        def dJ(theta, X_b, y):
            #求导后公式
            return X_b.T.dot(self.sigmoid(X_b.dot(theta)) - y) / len(y)

        def gradient_descent(X_b, y, initial_theta, alpha, n_iters=1e4, epsilon=1e-8):
            theta = initial_theta
            cur_iter = 0

            while cur_iter < n_iters:
                gradient = dJ(theta, X_b, y)
                last_theta = theta
                theta = theta - alpha * gradient
                if abs(J(theta, X_b, y) - J(last_theta, X_b, y)) < epsilon:
                    break
                cur_iter += 1
            return theta

        X_b = np.hstack([np.ones((len(X_train), 1)), X_train])
        initial_theta = np.zeros(X_b.shape[1])
        self._theta = gradient_descent(X_b, y_train, initial_theta, alpha, n_iters)

        #截距
        self.intercept = self._theta[0]
        #x_i前的参数
        self.coef = self._theta[1:]

        return self

    def predict_proba(self, X_predict):
        """给定待预测数据集X_predict, 返回表示X_predict的结果概率向量"""
        assert self.intercept is not None and self.coef is not None
        assert X_predict.shape[1] == len(self.coef)
        # prob = self.predict_proba(X_predict)
        X_b = np.hstack([np.ones((len(X_predict), 1)), X_predict])
        return self.sigmoid(X_b.dot(self._theta))

    def predict(self, X_predict):
        """给定待预测数据集X_predict, 返回表示X_predict的结果向量"""
        assert self.intercept is not None and self.coef is not None
        assert X_predict.shape[1] == len(self.coef)
        prob = self.predict_proba(X_predict)
        return np.array(prob >= 0.5, dtype='int')

    def score(self, X_test, y_test):
        """根据测试数据集X_test和y_test确定当前模型的准确度"""
        y_predict = self.predict(X_test)
        return accuracy_score(y_test, y_predict)

    def __repr__(self):
        return "LogisticRegression()"