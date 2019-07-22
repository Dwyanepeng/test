#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 15:03
# @Site    : 
# @File    : 504.py
# @Software: PyCharm

#抓成七进制
class Solution:
    def convertToBase7(self, num):
        if num > 0:
            s = ''
            n = 1
            while n != 0:
                n = num // 7
                # print(n)
                s += str(num - n * 7)
                num = n
            return s[::-1]
        elif num < 0:
            # return '-' + to7(-num)
            s = ''
            n = 1
            num = -num
            while n != 0:
                n = num // 7
                # print(n)
                s += str(num - n * 7)
                num = n
            return '-' + s[::-1]
        else:
            return str(0)

s = Solution()
print(s.convertToBase7(-7))