from sympy import lambdify, Expr
from .compare_base import CompareBase
from checksym.compare.exception import CompareException
from math import isnan
from pprint import pp
from numpy import ndarray, ComplexWarning
from warnings import catch_warnings, filterwarnings

class SciPyNumPy(CompareBase):

    do_sympy_doit_first = False

    def _evaluate(self):

        # Without the 'doit()' here, test_integrate_small_value_ensure_non_zero will fail
        if self.do_sympy_doit_first:
            expr1 = self.expr1.doit()
            expr2 = self.expr2.doit()
        else:
            expr1 = self.expr1
            expr2 = self.expr2

        lambdify_modules = ['scipy', 'numpy']
        test_value_set_for_lambdify = list(map(self.cleanup_for_lambdify, self.test_value_set))

        with catch_warnings():
            filterwarnings('ignore', category=ComplexWarning)
            this_expr1_lambdify_evaled = lambdify(self.symbols, expr1, lambdify_modules)(*test_value_set_for_lambdify)
            this_expr2_lambdify_evaled = lambdify(self.symbols, expr2, lambdify_modules)(*test_value_set_for_lambdify)
        
        this_expr1_lambdify_evaled = self._cleanup_result(this_expr1_lambdify_evaled)
        this_expr2_lambdify_evaled = self._cleanup_result(this_expr2_lambdify_evaled)
        
        return (this_expr1_lambdify_evaled, this_expr1_lambdify_evaled.real, this_expr1_lambdify_evaled.imag,
            this_expr2_lambdify_evaled, this_expr2_lambdify_evaled.real, this_expr1_lambdify_evaled.imag)
    
    def _cleanup_result(self, value):
        if isinstance(value, Expr):
            raise CompareException("Result is still an expression. Check to be sure all free variables are passed in the compare call.")
        return value

    def cleanup_for_lambdify(self, expr):
        real_imag = expr.as_real_imag()
        return float(real_imag[0]) + 1j * float(real_imag[1])
    
    def _check_for_zero(self, value):
        return value == 0
    
    def _check_for_nan(self, value):
        return isnan(value.real) or isnan(value.imag)