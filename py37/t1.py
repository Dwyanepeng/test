#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/22 10:03
# @Site    : 
# @File    : t1.py
# @Software: PyCharm

class Solution:
    def oneTime(self, nums):
        s = 0
        for num in nums:
            s ^= num
        return s

s = Solution()
print(s.oneTime([1,3,5,1,3,5,8]))