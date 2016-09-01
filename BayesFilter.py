# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 18:42:50 2016

@author: Fujiichang
"""

import estimate_s
import multinomial


p_o_s = [[0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]]
#
#p_o_s = [[0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.02, 0.02, 0.02, 0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
#         [0.02, 0.70, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]]
#
#p_o_s = [[0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.03, 0.03, 0.03, 0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
#         [0.03, 0.55, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]]

p_s_a = [[[1, 0, 0, 0, 0], [0.1, 0.9, 0, 0, 0], [1, 0, 0, 0, 0]],
         [[0.9, 0.1, 0, 0, 0], [0, 0.1, 0.9, 0, 0], [0, 1, 0, 0, 0]],
         [[0, 0.9, 0.1, 0, 0], [0, 0, 0.1, 0.9, 0], [0, 0, 1, 0, 0]],
         [[0, 0, 0.9, 0.1, 0], [0, 0, 0, 0.1, 0.9], [0, 0, 0, 1, 0]],
         [[0, 0, 0, 0.9, 0.1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]]


class BayesFilter(object):
    def __init__(self, p_s_a, p_o_s):
        self.p_s_a = p_s_a
        self.p_o_s = p_o_s

    def update_p_s(self, o, p_s_bar):
        p_s = estimate_s.calculate_corrected_distribution(p_o_s, p_s_bar, o)
        return p_s

    def update_p_s_bar(self, p_s, a):
        p_s_bar = estimate_s.calculate_predicted_distribution(self.p_s_a, p_s, a)
        return p_s_bar


class Controller(object):
    def __init__(self):
        self.s = 0

    def determine_a(self, p_s, goals):
        determined_s = estimate_s.calculate_expectation(p_s)
        self.s = 0
        if goals[self.s] - determined_s > 0:
            a = 1
        elif goals[self.s] - determined_s < 0:
            a = -1
        elif goals[self.s] - determined_s == 0:
            self.s = self.s + 1
            a = -1 * a
        return a


class Simulator(object):
    def __init__(self, p_s_a, p_o_s):
        self._s = 0
        self.p_s_a = p_s_a
        self.p_o_s = p_o_s

    def get_o(self):
        o = multinomial.multinomial(self.p_o_s[self._s])
        return o

    def set_a(self, a):
        self._s = self.draw_s(self._s, a)

    def get_s(self):
        return self._s

    def _draw_s(self, previous_s, a):
        p_s = self.p_s_a[previous_s][a]
        new_s = multinomial.multinomial(p_s)
        return new_s
