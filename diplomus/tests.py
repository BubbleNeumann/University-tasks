import unittest
import numpy as np


class QtableUtilsTest(unittest.TestCase):

    def test_normalize_qtable(self):
        from qlearning import normalize_qtable

        matrix = np.ones((2, 2))
        matrix[0, 0] = 2
        matrix[0, 1] = 5

        expected = np.ones((2, 2))
        expected[1, 0] = 0.5
        expected[1, 1] = 0.2

        self.assertTrue((normalize_qtable(matrix) == expected).all())
