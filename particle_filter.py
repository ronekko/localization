# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 12:28:02 2016

@author: Fujiichang
"""

import bayes_filter
import collections


p_o_s = [[0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]]

p_s_a = [[[1, 0, 0, 0, 0], [0.9, 0.1, 0, 0, 0], [0, 0.9, 0.1, 0, 0], [0, 0, 0.9, 0.1, 0], [0, 0, 0, 0.9, 0.1]],
         [[0.1, 0.9, 0, 0, 0], [0, 0.1, 0.9, 0, 0], [0, 0, 0.1, 0.9, 0], [0, 0, 0, 0.1, 0.9],  [0, 0, 0, 0, 1]],
         [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]]

p_s_o = [[0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.85],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.85, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.85, 0.85, 0.85, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01]]


class ParticleFilter(object):
    def __init__(self):
        self.p_s_a = p_s_a
        self.p_o_s = p_o_s

    def update_p_s_bar(self, particle, a):
        for i in range(len(particle)):
            s = particle[i]
            p_s = bayes_filter.p_s_a[a][s]
            new_s = bayes_filter.multinomial(p_s)
            particle[i] = new_s
        return particle

    def add_weight(self, particle, particle_num, o):
        self.p_s_o = p_s_o
        w_particle = 5 * [0]
        particle_counter = 5 * [0]
        new_w_particle = 5 * [0]

        for i in range(len(particle_counter)):
            particle_counter[i] = particle.count(i)
        print "particle_counter:", particle_counter

        for i in range(len(particle_counter)):
            w_particle[i] = particle_counter[i] * p_s_o[o][i]
        print "w_particle:", w_particle

        sum_w = sum(w_particle[i] for i in range(len(w_particle)))

        for i in range(len(w_particle)):
            new_w_particle[i] = (w_particle[i] / sum_w)
        print "new_w_particle:", new_w_particle
        return new_w_particle

    def update_p_s(self, particle, w_particle, particle_num):
        for i in range(particle_num):
            particle[i] = bayes_filter.multinomial(w_particle)
        return particle


class Controller(object):

    def __init__(self, goals):
        self.goals = goals

    def determine_a(self, determined_s):
        next_goal = self.goals[0]
        if next_goal == determined_s:
            self.goals.pop(0)
            if self.is_terminated() is False:
                next_goal = self.goals[0]
        if next_goal - determined_s < 0:
            a = 0
        elif next_goal - determined_s > 0:
            a = 1
        else:
            a = 2
        return a

    def is_terminated(self):
        return bayes_filter.is_empty(self.goals)


if __name__ == "__main__":
    estimater = ParticleFilter()
    simulator = bayes_filter.Simulator(p_s_a, p_o_s)
    goals = [4, 0]
    controller = Controller(goals)
    particle_num = 100
    w_particle = particle_num * [0]
    w_particle[0] = 1
    particle = particle_num * [0]
    t = 0

    while True:
        print "step:", t, "##########################"
        o = simulator.get_o()
        print "o =", o
        w_particle = estimater.add_weight(particle, particle_num, o)
        particle = estimater.update_p_s(particle, w_particle, particle_num)
        print "after observe:", particle
        print collections.Counter(particle).most_common(1)
        determined_s = collections.Counter(particle).most_common(1)[0][0]

        a = controller.determine_a(determined_s)
        print "a =", a

        if controller.is_terminated() is True:
#            print_result(o_log, actual_s_log, determined_s_log, a_log, t)
            print "Finish"
            break

        simulator.set_a(a)
        s = simulator.get_s()
        print "s =", s
        t = t + 1
        particle = estimater.update_p_s_bar(particle, a)
        print "before observe:", particle
