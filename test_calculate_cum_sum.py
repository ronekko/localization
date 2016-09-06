# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:23:31 2016

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

if __name__ == "__main__":
    unittest.main()
