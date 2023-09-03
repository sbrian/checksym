import itertools
from sympy import *
import functools
import sympy
import numpy
import mpmath
from checksym.util import compare_to_significance, build_test_value_sets
from pprint import pp
import datetime
from .impl import SciPyNumPy, Evalf

class Compare:

    def __init__(self, *, test_time_limit=None):
        """
        Args:
        test_time_limit: Execute no more than this many tests
        test_count_limit: Stop executing tests after this much time as passed
        """
        self.test_time_limit = test_time_limit

    @functools.lru_cache(maxsize=None)
    def compare(self, expr1, expr2, *symbols):
        """
        Compare the two expressions numerically, making replacements for the given symbols.

        Test values are automatically populated for all the given symbols, using their assumptions.

        Additional assumptions can be applied to the real and imaginary parts of complex numbers, by 
        prepending "real_part_" or "imaginary_part_" from the usual supported assumptions.

        For example: x = symbols("x", complex=True, real_part_positive=True)

        See sympy/core/assumptions.py in the sympy source for the standard assumptions. 

        The error 'TypeError: loop of ufunc does not support argument 0 of type Mul which has no callable exp method'
        in lambdify might mean that the list of symbols is incomplete.
        """

        test_value_sets = build_test_value_sets(*symbols)

        counter = 0

        significance = 10

        impl = SciPyNumPy()

        if self.test_time_limit != None:
            start = datetime.datetime.now()

        for test_value_set in test_value_sets:
            if len(symbols) != len(test_value_set):
                raise Exception("Invalid test_value_set length")
            
            counter = counter+1
            
            this_result = impl.compare_for_symbols_with_test_values(expr1, expr2, symbols, test_value_set, significance)

            if not (this_result is None):
                return this_result
            
            if self.test_time_limit != None:
                now = datetime.datetime.now()
                if now.timestamp() - start.timestamp() > self.test_time_limit:
                    return None
        
        return None
    
    def change(self, expr, op, *symbols):
        """
        Apply the function op to expr, and then compare to see if the
        modified result is equivalent, substituting test values
        for the symbols
        """
        new_expr = op(expr)
        this_result = self.compare(expr, new_expr, *symbols)
        if not (this_result is None):
            return this_result
        return new_expr

    
