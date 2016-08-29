# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:21:10 2016

@author: Fujiichang
"""


def calculate_cum_sum(p):

    K = len(p)
    cum_sum = K*[0]
    for n in range(K):
        if n == 0:
            cum_sum[n] = p[n]
        elif n != 0:
            cum_sum[n] = cum_sum[n-1] + p[n]
    return cum_sum
