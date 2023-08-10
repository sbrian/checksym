import unittest
from checksym.util import convert_to_order_one, compare_to_significance

class TestCompareFunctions(unittest.TestCase):

    def test_convert_to_order_one_a(self):
        (result, places) = convert_to_order_one(0.0001234)
        self.assertEqual(1.234, result)
        self.assertEqual(-4, places)

    def test_convert_to_order_one_b(self):
        (result, places) = convert_to_order_one(123.4)
        self.assertEqual(1.234, result)
        self.assertEqual(2, places)

    def test_convert_to_order_one_c(self):
        (result, places) = convert_to_order_one(100.1)
        self.assertEqual(1.001, result)
        self.assertEqual(2, places)
    
    def test_convert_to_order_one_d(self):
        (result, places) = convert_to_order_one(0.00000000090000009)
        self.assertEqual(9.0000009, result)
        self.assertEqual(-10, places)

    def test_compare_to_significance_a(self):
        self.assertTrue(compare_to_significance(0.01, 0.012, 1))
    
    def test_compare_to_significance_b(self):
        self.assertFalse(compare_to_significance(0.01, 0.012, 2))

    def test_compare_to_significance_c(self):
        self.assertFalse(compare_to_significance(0.12, 0.012, 2))

    def test_compare_to_significance_d(self):
        self.assertTrue(compare_to_significance(110000, 100000, 1))

    def test_compare_to_significance_e(self):
        self.assertTrue(compare_to_significance(10000.000000001, 10000.000000011, 12))

    def test_compare_to_significance_f(self):
        self.assertFalse(compare_to_significance(10000.000000001, 10000.00000011, 13))

    def test_compare_to_significance_g(self):
        self.assertTrue(compare_to_significance(1 + 2j, 1 + 2j, 1))

    def test_compare_to_significance_h(self):
        self.assertTrue(compare_to_significance(2.24j, 2.23j, 2))

    def test_compare_to_significance_i(self):
        self.assertFalse(compare_to_significance(2.24j, 2.23j, 3))

    def test_compare_to_significance_j(self):
        self.assertFalse(compare_to_significance(2.24+2.24j, 2.24+2.23j, 3))

    def test_compare_to_significance_j(self):
        self.assertFalse(compare_to_significance(2.23+2.24j, 2.22+2.24j, 3))

    def test_compare_to_significance_j(self):
        self.assertFalse(compare_to_significance(1-1j, 1+1j, 3))