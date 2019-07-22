#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/22 17:12
# @Site    : 
# @File    : t2.py
# @Software: PyCharm
class Solution:
    def maxProfit(self, prices):
        if len(prices) < 2:
            return 0

        m = 2
        n = len(prices)
        DP = [[0] * n for x in range(m + 1)]
        print(DP)
        for i in range(m + 1):
            for j in range(n):
                if i == 0 or j == 0:
                    DP[i][j] = 0
                else:
                    DP[i][j] = DP[i][j - 1]
                    print('DP1',DP)
                    for k in range(j):
                        prev = 0 if k == 0 else DP[i - 1][k - 1]
                        DP[i][j] = max(DP[i][j], prev + prices[j] - prices[k])
                        print('DP2',DP)

        return DP[m][n - 1]

s = Solution()
print(s.maxProfit([3,3,5,0,0,3,1,4]))
