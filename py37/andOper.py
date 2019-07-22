#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 9:38
# @Site    : 
# @File    : andOper.py
# @Software: PyCharm

#找出数组中只出现一次的两个数，其他数只出现两次
def twoNumber(numbers):
    acc = 0
    for num in numbers:
        acc ^= num
        print('acc', acc)
        print(bin(acc))
    n = len(bin(acc)) - 3
    a, b = 0, 0
    for num in numbers:
        print('num>>n', num >> n)
        if num >> n & 1:
            a ^= num
        else:
            b ^= num
    return [a,b]

print(twoNumber([1,2,4,1,2,6]))