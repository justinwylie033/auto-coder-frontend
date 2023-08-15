
import math

def sqrt(num):
    """
    This function calculates the square root of a number.

    Parameters:
    num (float): The number for which square root needs to be calculated.

    Returns:
    float: The square root of the number.

    Raises:
    ValueError: If num is negative.
    """
    # check if the given number is positive
    if num >= 0:
        return math.sqrt(num)
    else:
        raise ValueError("Number must be positive")


import unittest
from calculator.squareroot import sqrt

class TestSquareroot(unittest.TestCase):

    def test_sqrt(self):
        self.assertEqual(sqrt(9), 3.0)
        self.assertRaises(ValueError, sqrt, -4)

if __name__ == '__main__':
    unittest.main()

