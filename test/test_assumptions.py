import unittest
from sympy import symbols, Rational, I, E, Symbol
from pprint import pp
from checksym.util import get_test_numbers_for_assumptions, build_test_value_sets

class TestAssumptions(unittest.TestCase):
    
    def test_get_test_numbers_for_positive_integer(self):
        x = symbols("x", integer=True, positive=True)
        test_numbers = get_test_numbers_for_assumptions(x.assumptions0, 1)
        self.assertEqual([2, 5, 3], test_numbers)

    def test_get_test_numbers_for_integer(self):
        x = symbols("x", integer=True)
        test_numbers = get_test_numbers_for_assumptions(x.assumptions0, 1)
        self.assertEqual([2, 5, -3], test_numbers)

    def test_get_test_numbers_for_positive_rational(self):
        x = symbols("x", rational=True, positive=True)
        test_numbers = get_test_numbers_for_assumptions(x.assumptions0, 1)
        self.assertEqual([Rational(13, 10), Rational(1, 7), Rational(12, 5)], test_numbers)

    def test_get_test_numbers_for_complex(self):
        x = symbols("x", complex=True)
        test_numbers = list(get_test_numbers_for_assumptions(x.assumptions0, 1))
        self.assertEqual([Rational(13, 10) + 13*I/5, Rational(1, 7) + 2*I/7, -Rational(12, 5) - 24*I/5], test_numbers)

    def test_get_test_numbers_for_complex_real_part_positive(self):
        x = symbols("x", complex=True, real_part_positive=True)
        test_numbers = list(get_test_numbers_for_assumptions(x.assumptions0, 1))
        self.assertEqual([Rational(13, 10) + 13*I/5, Rational(1, 7) + 2*I/7, Rational(12, 5) - 24*I/5], test_numbers)

    def test_get_test_numbers_for_complex_imaginary_part_positive(self):
        x = symbols("x", complex=True, imaginary_part_positive=True)
        test_numbers = list(get_test_numbers_for_assumptions(x.assumptions0, 1))
        self.assertEqual([Rational(13, 10) + 13*I/5, Rational(1, 7) + 2*I/7, -Rational(12, 5) + 24*I/5], test_numbers)

    def test_build_test_value_sets_for_real(self):
        x, y = symbols("x y", real=True)
        test_sets = build_test_value_sets(x, y)
        self.assertEqual([[Rational(13, 10), Rational(39, 10)], [Rational(1, 7), Rational(3, 7)], [-Rational(12, 5), -Rational(36, 5)]], test_sets)

    def test_build_test_value_sets_for_complex(self):
        x, y = symbols("x y", complex=True)
        test_sets = build_test_value_sets(x, y)
        self.assertEqual([[Rational(13, 10) + 13*I/5, Rational(39, 10) + 26*I/5],
            [Rational(1, 7) + 2*I/7, Rational(3, 7) + 4*I/7],
            [-Rational(12, 5) - 24*I/5, -Rational(36, 5) - 48*I/5]], test_sets)
    
    def test_build_test_value_sets_for_real_and_positive(self):
        x = symbols("x", real=True)
        y = symbols("y", real=True, positive=True)
        test_sets = build_test_value_sets(x, y)
        self.assertEqual([[Rational(13, 10), Rational(39, 10)], [Rational(1, 7), Rational(3, 7)], [-Rational(12, 5), Rational(36, 5)]], test_sets)

    def test_build_test_value_sets_for_complex_positive_and_real(self):
        z = symbols("z", complex=True)
        n = symbols("n", positive=True)
        x = symbols("x", real=True)
        test_sets = build_test_value_sets(z, n, x)
        self.assertEqual([[Rational(13, 10) + 13*I/5, Rational(39, 10), Rational(13, 2)],
            [Rational(1, 7) + 2*I/7, Rational(3, 7), Rational(5, 7)],
            [-Rational(12, 5) - 24*I/5, Rational(36, 5), -12]], test_sets)
        
    def test_build_test_value_sets_for_positive_integers(self):
        x = symbols("x", integer=True, positive=True)
        y = symbols("y", integer=True, positive=True)
        test_sets = build_test_value_sets(x, y)
        self.assertEqual([[2, 6], [5, 15], [3, 9]], test_sets)

    def test_build_test_value_sets_for_three_positive_integers(self):
        x = symbols("x", integer=True, positive=True)
        y = symbols("y", integer=True, positive=True)
        z = symbols("z", integer=True, positive=True)
        test_sets = build_test_value_sets(x, y, z)
        self.assertEqual([[2, 6, 10], [5, 15, 25], [3, 9, 15]], test_sets)