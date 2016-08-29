# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 18:34:41 2016

@author: Fujiichang
"""


def estimate_p_s(a, o, p_s_a, p_o_s, previous_f, state_number):
    f = previous_f
    g = state_number*[0]

    for s in range(state_number):
        g[s] = p_o_s[s][o] * sum([p_s_a[s][a][m] * f[m]
                                 for m in range(state_number)])

    sum_g = sum(g[s] for s in range(state_number))

    for s in range(state_number):
        f[s] = g[s]/sum_g

    return f


def calculate_predicted_distribution(p_s_a, p_s, a):
    p_s_bar = 5 * [0]
    for s in range(5):
        p_s_bar[s] = sum([p_s_a[m][a][s] * p_s[m] for m in range(5)])
    return p_s_bar


def calculate_corrected_distribution(p_o_s, p_s_bar, o):
    g = 5 * [0]
    f = 5 * [0]

    for s in range(5):
        g[s] = p_o_s[s][o] * p_s_bar[s]

    sum_g = sum(g[s] for s in range(5))

    for s in range(5):
        f[s] = g[s]/sum_g

    return f


def calculate_expectation(f):
    expectation = sum(f[s] * s for s in range(5))
    return int(round(expectation, 0))
