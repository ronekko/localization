# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 18:43:53 2016

@author: Fujiichang
"""
import random
import calculate_cum_sum


def multinomial(p):
    sum_p = sum(p)
    assert(sum_p >= 1)
    cum_sum = len(p)*[0]
    cum_sum = calculate_cum_sum.calculate_cum_sum(p)
    K = len(cum_sum)
    u = random.random()

    for k in range(K):
        if u <= cum_sum[k]:
            return k
    return k - 1
