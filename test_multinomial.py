# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:47:11 2016

@author: Fujiichang
"""

import unittest
import bayes_filter


class TestCalculateCumSum(unittest.TestCase):

    def test_calculate_cum_sum(self):
        p = [0.2, 0.3, 0.5]
        expected = [0.2, 0.5, 1.0]
        actual = bayes_filter.calculate_cum_sum(p)
        self.assertEquals(actual, expected)


class TestMultinomial(unittest.TestCase):

    def test_multinomial(self):
        p = [0.20, 0.80]
        N = 500000
        sample = N*[0]
        expected = 0.80
        for n in range(N):
            sample[n] = bayes_filter.multinomial(p)
        avg_sample = sum(sample)/float(N)
        self.assertAlmostEqual(expected, avg_sample, 2)

    def test_sum_p_not_equal_one(self):
        p = [0.2, 0.3, 0.4]
        self.assertRaises(AssertionError, bayes_filter.multinomial, p)

    def test_p_elements_are_one_or_zero(self):
        p = [1, 0, 0, 0]
        expected = 0
        actual = bayes_filter.multinomial(p)
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
