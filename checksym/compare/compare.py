import itertools
from sympy import *
import functools
import sympy
import numpy
import mpmath
from checksym.util import compare_to_significance, build_test_value_sets
from pprint import pp
import datetime

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

        def do_compare(test_value_set):
            return self.compare_for_symbols_with_test_values(expr1, expr2, symbols, test_value_set)

        if self.test_time_limit != None:
            start = datetime.datetime.now()

        for test_value_set in test_value_sets:
            counter = counter+1
            this_result = do_compare(test_value_set)
            if not (this_result is None):
                return this_result
            
            if self.test_time_limit != None:
                now = datetime.datetime.now()
                if now.timestamp() - start.timestamp() > self.test_time_limit:
                    return None
        
        return None
    
    def compare_for_symbols_with_test_values(self, expr1, expr2, symbols, test_value_set):
        significance = 10
        expr1_evaled = expr1.doit()
        expr2_evaled = expr2.doit()
        if len(symbols) != len(test_value_set):
            raise Exception("Invalid test_value_set length")
        lambdify_modules = ['scipy', 'numpy']
        test_value_set_for_lambify = list(map(self.cleanup_for_lambdify, test_value_set))
        this_expr1_lambdify_evaled = lambdify(symbols, expr1_evaled, lambdify_modules)(*test_value_set_for_lambify)
        this_expr2_lambdify_evaled = lambdify(symbols, expr2_evaled, lambdify_modules)(*test_value_set_for_lambify)
        if not compare_to_significance(this_expr1_lambdify_evaled, this_expr2_lambdify_evaled, significance):
            return {
                'symbols' : symbols,
                'test_value_set': test_value_set,
                'expr1': expr1,
                'expr1_evaluated': expr1,
                'expr1_final': this_expr1_lambdify_evaled,
                'expr2': expr2,
                'expr2_evaluated': expr2,
                'expr2_final': this_expr2_lambdify_evaled
            }
        return None
    
    def cleanup_for_lambdify(self, expr):
        real_imag = expr.as_real_imag()
        return float(real_imag[0]) + 1j * float(real_imag[1])

def remove(expr, *search):

    """
    Remove an expression from another expression
    
    Keyword arguments:
    expr -- the expression to search through
    search -- the subexpression to find and remove

    We know that the search expression will be one of these
    1) An argument to Add()
    2) An argument to Mul()

    We don't support these cases
    1) An argument to Pow()
    2) An argument to Rational()
    3) An argument to some other function

    """

    def _remove(expr, search):

        if expr.is_Atom or expr.is_Dummy:
            return expr
        elif expr.is_Mul or expr.is_Add:
            newargs = map(lambda arg: remove(arg, search), filter(lambda n: n!=search, expr.args))
            return expr.func(*newargs)
        else:
            newargs = map(lambda arg: remove(arg, search), expr.args)
            return expr.func(*newargs)
    
    expr = _remove(expr, search[0])
    if len(search) == 1:
        return expr
    else:
        return remove(expr, *search[1:])
    
def change(expr, op, *test_symbols):
    new_expr = op(expr)
    this_result = compare(expr, new_expr, *test_symbols)
    if not (this_result is None):
        return this_result
    return new_expr