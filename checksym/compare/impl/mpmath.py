from checksym.util import compare_to_significance_complex
from .compare_base import CompareBase
from sympy import re, im
from math import isnan
import mpmath
from sympy import lambdify

class Mpmath(CompareBase):

    def _evaluate(self):
        """
        Doesn't work yet
        """
        expr1_evaled = self.expr1.doit()
        expr2_evaled = self.expr2.doit()
        lambdify_modules = ['mpmath']
        test_value_set_for_lambdify = list(map(self.cleanup_for_lambdify, self.test_value_set))
        this_expr1_lambdify_evaled = lambdify(self.symbols, expr1_evaled, lambdify_modules)(*test_value_set_for_lambdify)
        this_expr2_lambdify_evaled = lambdify(self.symbols, expr2_evaled, lambdify_modules)(*test_value_set_for_lambdify)
        return (this_expr1_lambdify_evaled, this_expr1_lambdify_evaled.real, this_expr1_lambdify_evaled.imag,
            this_expr2_lambdify_evaled, this_expr2_lambdify_evaled.real, this_expr1_lambdify_evaled.imag)
    
    def cleanup_for_lambdify(self, expr):
        real_imag = expr.as_real_imag()
        return float(real_imag[0]) + 1j * float(real_imag[1])
    
    def _check_for_zero(self, value):
        return value == 0
    
    def _check_for_nan(self, value):
        return False