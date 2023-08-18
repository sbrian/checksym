import unittest
from sympy import symbols, Rational, I, E, Symbol
from pprint import pp
from checksym.util import get_test_numbers_for_assumptions

class TestAssumptionFunctions(unittest.TestCase):
    
    def test_get_test_numbers_for_positive_integer(self):
        x = symbols("x", integer=True, positive=True)
        test_numbers = get_test_numbers_for_assumptions(x.assumptions0)
        self.assertEqual([1, 3], test_numbers)

    def test_get_test_numbers_for_integer(self):
        x = symbols("x", integer=True)
        test_numbers = get_test_numbers_for_assumptions(x.assumptions0)
        self.assertEqual([1, 3, -1, -3, 0], test_numbers)

    def test_get_test_numbers_for_positive_rational(self):
        x = symbols("x", rational=True, positive=True)
        test_numbers = get_test_numbers_for_assumptions(x.assumptions0)
        self.assertEqual([1, 3, Rational(1, 4), Rational(5, 3)], test_numbers)

    def test_get_test_numbers_for_complex(self):
        x = symbols("x", complex=True)
        test_numbers = list(get_test_numbers_for_assumptions(x.assumptions0))
        self.assertTrue(0 in test_numbers)
        self.assertTrue(I in test_numbers)
        self.assertTrue(E + I in test_numbers)

    def test_get_test_numbers_for_complex_real_part_positive(self):
        x = symbols("x", complex=True, real_part_positive=True)
        test_numbers = list(get_test_numbers_for_assumptions(x.assumptions0))
        self.assertFalse(0 in test_numbers)
        self.assertFalse(I in test_numbers)
        self.assertTrue(E + I in test_numbers)

    def test_get_test_numbers_for_complex_imaginary_part_positive(self):
        x = symbols("x", complex=True, imaginary_part_positive=True)
        test_numbers = list(get_test_numbers_for_assumptions(x.assumptions0))
        self.assertFalse(0 in test_numbers)
        self.assertTrue(I in test_numbers)
        self.assertFalse(1 in test_numbers)
        self.assertTrue(E + I in test_numbers)