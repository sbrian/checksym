import itertools
from sympy import *
import functools
import sympy
import numpy
import mpmath
from checksym.util import compare_to_significance, build_test_value_sets
from pprint import pp
import datetime
from .impl import SciPyNumPy, Evalf, Mpmath

class Compare:

    def __init__(self, *, test_time_limit=None, convert_exceptions=True):
        """
        Args:
        test_time_limit: Execute no more than this many tests
        convert_exceptions: Don't throw exceptions. Return them as part of the result
        """
        self.test_time_limit = test_time_limit
        self.convert_exceptions = convert_exceptions

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

        # Imaginary parts, combined with integrals with limits at infinity, provoke
        # `NameError: name 'polar_lift' is not defined` errors.
        # So if we have non-real symbols involved, replace such integrals with integrals
        # from -1 to 1.
        # It would be more complete to only replace integrals that have a non-real symbol
        # within them instead of all integrals in the expression, but we will keep it simple for now.
        # Right now we only change integrals where both bounds are infinite. It's tricky otherwise,
        # because we can just set a bound to -1 or 1 without considering what the other bound is.
        # Probably also need to consider both expressions, as one might be shifted version of the other.
        # Maybe we will need to address that later.
        if any(map(lambda x: not x.is_real, symbols)):
            expr1 = replace_infinite_integrals(expr1)
            expr2 = replace_infinite_integrals(expr2)

        test_value_sets = build_test_value_sets(*symbols)

        significance = 10

        impl = SciPyNumPy(expr1, expr2, symbols, significance, self.convert_exceptions)

        result = self.compare_with_impl(impl, symbols, test_value_sets)

        if result != None:
            impl.do_sympy_doit_first = True
            result = self.compare_with_impl(impl, symbols, test_value_sets)

        return result

    def compare_with_impl(self, impl, symbols, test_value_sets):
        if self.test_time_limit != None:
            start = datetime.datetime.now()

        for test_value_set in test_value_sets:
            if len(symbols) != len(test_value_set):
                raise Exception("Invalid test_value_set length")
            
            this_result = impl.compare_for_symbols_with_test_values(test_value_set)

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

def replace_infinite_integrals(expr):
    if expr.is_Atom or expr.is_Dummy:
        return expr
    elif isinstance(expr, Integral):
        limit_tuple = expr.args[-1]
        if limit_tuple[1] == -oo and limit_tuple[2] == oo:
            limit_tuple = (limit_tuple[0], -1, 1)
        elif limit_tuple[1] == oo and limit_tuple[2] == -oo:
            limit_tuple = (limit_tuple[0], 1, -1)
        return Integral(*(expr.args[:-1]), limit_tuple)
    else:
        newargs = map(lambda arg: replace_infinite_integrals(arg), expr.args)
    return expr.func(*newargs)
    
