# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:42:03 2016

@author: Fujiichang
"""
import random


def calculate_cum_sum(p):

    K = len(p)
    cum_sum = K*[0]
    for n in range(K):
        if n == 0:
            cum_sum[n] = p[n]
        elif n != 0:
            cum_sum[n] = cum_sum[n-1] + p[n]
    return cum_sum


def multinomial(p):

    assert(sum(p) == 1)
    cum_sum = len(p)*[0]
    cum_sum = calculate_cum_sum(p)
    K = len(cum_sum)
    u = random.random()

    for k in range(K):
        if u <= cum_sum[k]:
            return k
    return k-1
