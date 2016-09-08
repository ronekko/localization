# -*- coding: utf-8 -*-
"""
Created on Thu Sep 08 22:15:36 2016

@author: ryuhei
"""

import numpy as np
import matplotlib.pyplot as plt


class Continuous1dSimulator(object):
    def __init__(self, var_p_s_a=0.01, var_p_o_s=0.01):
        self._s = 0
        self.var_p_s_a = var_p_s_a
        self.var_p_o_s = var_p_o_s
        self.landmark_positions = np.arange(5, dtype=np.float)

    def _draw_s(self, previous_s, a):
        stddev = self.var_p_s_a ** 0.5
        displacement = np.random.normal(a, stddev)
        new_s = self._s + displacement
        return new_s

    def get_o(self):
        current_s = self._s
        landmark_distances = self.landmark_positions - current_s
        stddev = self.var_p_o_s ** 0.5
        o = np.random.normal(landmark_distances, stddev).tolist()
        return o

    def set_a(self, a):
        self._s = self._draw_s(self._s, a)

    def get_s(self):
        return self._s

def show_o(o):
    K = len(o)
    plt.bar(range(K), o, align='center')
    plt.xlabel("landmark")
    plt.ylabel("distance")
    plt.ylim([-5, 5])
    plt.grid()
    plt.show()

if __name__ == '__main__':
    stddev_p_s_a = 0.1
    stddev_p_o_s = 0.1

    var_p_s_a = stddev_p_s_a ** 2
    var_p_o_s = stddev_p_o_s ** 2
    simulator = Continuous1dSimulator(var_p_s_a, var_p_o_s)

    s_log = [simulator.get_s()]

    # "go right 1 meter" 4 times, then "go left 1 meter" 4 times
    actions = [1] * 4 + [-1] * 4
    for t, a in enumerate(actions):
        print "step:", t
        show_o(simulator.get_o())
        simulator.set_a(a)
        s_log.append(simulator.get_s())

    # plot trajectory
    plt.plot(s_log, range(len(s_log)), '-+', markersize=10)
    plt.xlim([-2, 6])
    plt.xlabel("state")
    plt.ylabel("$\leftarrow$ time")
    plt.grid()
    plt.gca().invert_yaxis()
    plt.show()
