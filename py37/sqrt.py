#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 9:14
# @Site    : 
# @File    : sqrt.py
# @Software: PyCharm

'''题目：已知 sqrt (2)约等于 1.414，要求不用数学库，求 sqrt (2)精确到小数点后 10 位。'''
class Solution:
    def sqrt(self):
        low = 1.4
        high = 1.5
        eps = 0.0000000001
        mid = (low+high) / 2
        while (high-low) > eps:
            if mid * mid > 2:
                high = mid
            elif mid * mid < 2:
                low = mid
            mid = (low+high) / 2
        return mid

s = Solution()
print(s.sqrt())
